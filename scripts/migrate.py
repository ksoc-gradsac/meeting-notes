import re
import os
from datetime import datetime

def convert_notes_to_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    note = []
    
    current_date = None
    next_meeting = None
    in_todos = False
    in_notes = False

    current_date_str = str()
    next_meeting_str = str()
    
    for line in content:
        if re.match(r'\w+ \d{2}, \d{4}', line):

            try:
                current_date = datetime.strptime(current_date_str, '%b %d, %Y')
            except ValueError:
                try:
                    current_date = datetime.strptime(current_date_str, '%B %d, %Y')
                except ValueError:
                    try:
                        current_date = datetime.strptime(current_date_str.split('—')[0].strip(), '%b %d, %Y')
                    except ValueError as e:
                        print(e, current_date_str.split('-')[0].strip())
                        # continue
                        # exit(-1)

            if current_date:
                with open(f'{next_meeting.year}/{next_meeting.month}/{next_meeting_str}.md', 'w', encoding='utf-8') as note_file:
                    if next_meeting:
                        note_file.write(f'\n[Previous Meeting]({current_date.year}/{current_date.month}/{current_date_str}.md)\n')
                    note_file.writelines(note)
                next_meeting = current_date

                current_date_str = current_date.strftime('%Y-%m-%d')

            note = [f'# {current_date_str}']
            in_todos = False
            in_notes = False
        elif 'Attendees:' in line:
            note.append(f'**Attendees:** {line.strip()[11:]}\n')
        elif 'Todos:' in line:
            in_todos = True
            in_notes = False
            note.append(f'## {line.strip()}\n')
        elif 'Notes:' in line:
            in_todos = False
            in_notes = True
            note.append(f'## {line.strip()}\n')
        elif in_todos:
            note.append(f'- [ ] {line.lstrip("*")}')
        elif in_notes:
            note.append(f'- {line.lstrip("*")}')
        else:
            note.append(line)

    if current_date and note:
        with open(f'{current_date.year}/{current_date.month}/{current_date_str}.md', 'w') as note_file:
            note_file.writelines(note)
            
        next_meeting = current_date
        current_date = None
        next_meeting_str = next_meeting.strftime('%Y-%m-%d')

convert_notes_to_md('original_notes.txt')