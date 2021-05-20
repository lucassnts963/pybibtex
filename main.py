import os

from pybibtex import FileHandler


PATH = os.path.join('Bibtex')

files = os.listdir(PATH)


for file in files:
    source = file.split('.')[0]
    csv_dir = os.path.join('csv', source)
    if not os.path.exists('csv'):
        os.mkdir('csv')
    f = FileHandler(file, source)
    f.to_csv(csv_dir)