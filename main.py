import re

from os import path

from pprint import pprint

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

# This is to build the path of the file in any system
filename = 'Scielo.bib'
path_file = path.join('Bibtex', filename)


# Function to get just the from the match
def get_id(match):
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
    
def get_keys_values(matches):
      keys_values = []
      
      for match in matches:
            key, value = match
            key = key.replace('=', '').rstrip().lstrip()
            if(value[0:2] == '{{'):
                  value = value[2:-2]
            else:
                  value = value[1:-1]
            
            keys_values.append((key, value))
      
      return keys_values

with open(path_file) as file:
    data = file.read()
    articles = regex_article.findall(data)
    
    list_articles = []
    
    if (articles):
        for article in articles:
            match_id = regex_id.search(article)
            id = get_id(match_id)
            
            match_keys_values = regex_keys_values.findall(article)
            dict_article = {}
            if (match_keys_values):
              size = len(match_keys_values)
              print(id, size)
              keys_values = get_keys_values(match_keys_values)
              dict_article = dict(keys_values)
              my_article = (id, dict_article)
              list_articles.append(my_article)
              
    my_articles = dict(list_articles)
    
    for article in my_articles:
      title = my_articles[article]['title']
      print (article+':', title)