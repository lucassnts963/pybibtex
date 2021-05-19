

from pybibtex import FileHandler


file = FileHandler('Scielo.bib')

entries = file.entries

for id in entries:
  title = entries [id]['title']
  
  print (title)