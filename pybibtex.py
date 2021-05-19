from os import path

import re
import csv

# This is a pattern to locate ids of the articles from a file .bib
pattern_id = r'(@(?:article|incollection)\{.*?,)'
regex_id = re.compile(pattern_id, flags=re.I | re.S)

# This pattern is to locate any article from a file .bib
pattern_article = r'''
(@
  (?:article|incollection)\{.*?,\s+
  (?:[a-z]+\s*=\s*
    (?:
      (?:"|\{){1,2}
      .*?
      (?:"|\}){1,2}
    ),{0,1}\s+
  )+
  \}
)
'''
regex_article = re.compile(pattern_article, flags=re.I | re.S | re.M | re.X)


# This pattern is to locate the keys and values in the articles found
pattern_keys_values = r'''
(?:
  ([a-z]+\s*=\s*)
  (
    (?:"|\{){1,2}
      .*?
    (?:"|\}){1,2}
  )
)
'''
regex_keys_values = re.compile(pattern_keys_values, flags=re.I | re.S | re.M | re.X)


class FileHandler:
  
  def __init__ (self, filename):
    self.path = path.join('Bibtex', filename)
    self.entries = find_entries(self.path)
  
  #TODO  
  def to_csv(self):
    pass


# Function to get just id the from the match
def get_id(match_article):
      match = regex_id.search(match_article)
      
      if (not match):
        pass
        
      string_found = match.group()
      string_found = string_found.replace(',', '')
      string_found = string_found.replace('@article{', '')
      string_found = string_found.replace('@ARTICLE{', '')
      string_found = string_found.replace('@incollection{', '')
      string_found = string_found.replace('@INCOLLECTION{', '')
      string_found = string_found.rstrip().lstrip()
      
      return string_found
    
def get_keys_values(article):
      id = get_id(article)
      matches = regex_keys_values.findall(article)
      
      if (not matches):
        return {}
      
      keys_values = []
      
      for match in matches:
            key, value = match
            key = key.replace('=', '').rstrip().lstrip()
            if(value[0:2] == '{{'):
                  value = value[2:-2]
            else:
                  value = value[1:-1]
            
            keys_values.append((key, value))
            
      article = (id, dict(keys_values))
      
      return article
      
def find_entries(path):
  with open (path) as file:
    data = file.read()
    matches = regex_article.findall(data)
    
    articles = []
    
    if (matches):
      for match in matches:
        article = get_keys_values(match)
        articles.append(article)
        
    return dict(articles)