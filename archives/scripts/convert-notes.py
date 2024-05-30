import os
import re
from datetime import datetime

from pprint import pprint

# Read the markdown file
with open('meeting-notes.md', 'r') as file:
    data = file.readlines()

dates = list()

for i, line in enumerate(data):
    if 'anchor-' in line:
        match = re.search(r'(\w+ \d{2}, \d{4})', line)
    
        if match:
            dates.append(i)

# for i in dates:
#     print(data[i])

notes_dict = dict()

for i, line in enumerate(data):
    if i in dates:
        match = re.search(r'(\w+ \d{2}, \d{4})', line)
        if match:
            try:
                date = datetime.strptime(match.group(1), '%B %d, %Y')
            except ValueError:
                date = datetime.strptime(match.group(1), '%b %d, %Y')
            
            date_string = date.strftime('%Y-%m-%d')
            
            notes_dict[date_string] = list()
            
            notes_dict[date_string].append(f'# {date_string}\n')
            
            j = i + 1
            while j < len(data) and j not in dates:
                notes_dict[date_string].append(data[j])
                j += 1
                
                

# pprint(notes_dict)s


for date, notes in notes_dict.items():
    print(date, date[:4], date[5:7])
    year_dir = date[:4]
    month_dir = datetime.strptime(date[5:7], '%m').strftime('%B')
    
    print(year_dir, month_dir, date)
    
    os.makedirs(os.path.join(year_dir, month_dir), exist_ok=True)
    
    with open(os.path.join(year_dir, month_dir, date + '.md'), 'w') as file:
        for note in notes:
            file.write(note)
    

# # Process each note
# for note in notes:
#     # Find the date in the note
#     match = re.search(r'(\w+ \d{2}, \d{4})', note)
#     if match:
#         # Parse the date
#         try:
#             date = datetime.strptime(match.group(1), '%B %d, %Y')
#         except ValueError:
#             date = datetime.strptime(match.group(1), '%b %d, %Y')
        
        
#         # Create the year and month directories
#         year_dir = str(date.year)
#         month_dir = date.strftime('%B')
#         # os.makedirs(os.path.join(year_dir, month_dir), exist_ok=True)
#         os.makedirs(os.path.join(year_dir, month_dir), exist_ok=True)
        
#         # Write the note to a file
#         filename = date.strftime('%m-%d-%y.md')
#         with open(os.path.join(year_dir, month_dir, filename), 'w') as file:
#             file.write(note)