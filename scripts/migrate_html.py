import os
from bs4 import BeautifulSoup
from datetime import datetime

# Load the HTML file
with open('GradSACRunningMeetingNotes.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all dates
dates = soup.find_all('span', class_='c31')

# Initialize previous note link
prev_note_link = None
prev_note_filename = str()

def check_if_todos(date):
    todos = False
    
    all_todos = [date.find_next('p', string='Todos:'), date.find_next('p', string='TODOS:'), date.find_next('p', string='todos:'), date.find_next('p', string='toDos:'), date.find_next('p', string='ToDos:')]
    
    for todo in all_todos:
        if todo:
            todos = todo
            return todo
        
    return todos

# For each date, find the corresponding attendees, todos, and notes
for date in dates:
    attendees = date.find_next('p', class_='c34').find('span', class_='c3').text.replace('Attendees:', '').strip()

    todos = check_if_todos(date)
    if todos:
        todos = [li.text for li in todos.find_next('ul').find_all('li')]
    else:
        todos = []
        
    try:
        notes = [li.text for li in date.find_next(string='Notes:').find_next('ul').find_all('li')]
    except AttributeError:
        print(f'No notes for {date.text}')
        notes = []
        exit(-1)


    # Convert the date to a datetime object
    
    try:
        date_obj = datetime.strptime(date.text, '%B %d, %Y')
    except:
        try:
            date_obj = datetime.strptime(date.text, '%b %d, %Y')
        except:
            # check if date.text contains a —
            if '—' in date.text:
                try:
                    date_obj = datetime.strptime(date.text.split('—')[0].strip(), '%B %d, %Y')
                except:
                    date_obj = datetime.strptime(date.text.split('—')[0].strip(), '%b %d, %Y')

    # Create the directory structure YYYY/MM if it doesn't exist
    directory = os.path.join(str(date_obj.year), str(date_obj.month).zfill(2))
    os.makedirs(directory, exist_ok=True)

    # Create the markdown file
    filename = os.path.join(directory, f'{date_obj.year}-{str(date_obj.month).zfill(2)}-{str(date_obj.day).zfill(2)}.md')
    with open(filename, 'w', encoding='utf-8') as file:
        # Convert each part of the meeting note to markdown
        file.write(f'# {date.text}\n\n**Attendees:** {attendees}\n\n## Todos\n\n- [ ] ' + '\n- [ ] '.join([todo.strip('\n') for todo in todos]) + '\n\n## Notes\n\n- ' + '\n- '.join([note.strip('\n') for note in notes]))
        
        # Add link to previous note if it exists
        if prev_note_link:
            file.write(f'\n\n[Previous Note]({prev_note_link}) | [[{prev_note_filename}|Previous Note (Obsidian)]]')
            
    todos = list()
    notes = list()

    # Update previous note link
    prev_note_link = filename
    prev_note_filename = f'{date_obj.year}-{str(date_obj.month).zfill(2)}-{str(date_obj.day).zfill(2)}.md'