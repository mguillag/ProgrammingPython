import re
import string
from typing import Dict

PATH = "path"

def reed_text(file_name:str):
    """    
    Args:
        file_name (str)
    Returns:
        text en forma de cadena
    """
    file = open( PATH + file_name, encoding="utf8")
    text = file.read()
    return text

def read_punctuations(file_name:str):
    """Open a two-column file and save into a dictionary
    each row, where the first column is the key and the second the value.
    
    Args:
        file_name (str)
    Returns:
        dictionary
    """
    file = open(file_name, encoding="utf8")
    dic_word = {}
    for row in file:
        data = row.split()
        dic_word[data[0]]= float(data[1])
    return dic_word

    
def lowercase(text):
    """   
    Args:
        string
    Returns:
        string in lowercase
    """
    return text.lower()

def uppercase(text):
    """    
    Args:
        string
    Returns:
        string in uppercase
    """
    return text.upper()

def count_words(text):
    """Cuenta el numero de palabras seprando el string con el metodo split
    
    Args:
        text(str)
    Returns:
        table de strings
    """
    num_words = len(text.split())
    return num_words
    
def remove_punctuation(text):
    """    
    Args:
        text(str)
    Returns:
        list
    """
    pattern = re.findall(r"[^\w\s]",text)
    remove_pattern = re.sub(r"[^\w\s]","",text)
    return pattern, remove_pattern
  
   
def remove_accents(text):
    """    
    Args:
        text (str)
    Returns:
        text
    """
    pattern={'a':'áàä','e':'éèë','i':'íìï','o':'óòö','u':'úùü'}
    for key,value in pattern.items():
        for letter in value:
            text = text.replace(letter,key)
    return text

def remove_numbers(text):
    """    
    Args:
        text (str)
    Returs:
        text (str)
    """
    pattern = re.sub(r"\d+", "", text)
    return pattern

def remove_acronym(text):
    """    
    Args:
        text (str)
    Returs:
        lits
    """
    acronym = re.findall(r"[A-Z]{2,}",text)
    remove_acronym = re.sub(r"[A-Z]{2,}","",text)
    return acronym,remove_acronym

def remove_stop_words(text,table):
    """   
    Args:
        text (str)
        list (list)
    Returns:
        String sin los elementos de la list
    """
    match = re.sub(fr"\b({'|'.join(table)})\b","", text)
    if match: return match
    else: return 0

def words_frecuency(text):
    """
    Args:
        text(str)
    Returns:
        dictionary
    """
    list_text = text.split()
    words_frecuency = [list_text.count(p) for p in list_text]
    return dict(list(zip(list_text,words_frecuency)))

def remove_url(text):
    """
    Args:
        text(str)
    Returns:
        text(str) 
    """
    return re.sub("https?\://[a-zA-Z0-9$-_@.&\+!\*\(]+","",text)

def remove_quotes(text):
    """    
    Args:
        text(str)
    Returns:
        text(str)
    """
    return re.sub(r'@[\w\-]+'," ",text)

def remove_hastags(text):
    """    
    Args:
        text(str)
    Returns:
        text(str)
    """
    return re.sub (r'#[\w\-]+'," ",text)

def standardizing_text(text,table):
    """
    Args:
        text (str)
        table (list)

    Returns:
        text(str) 
    """
    text_standard = remove_url(text)
    text_standard = remove_quotes(text_standard)
    text_standard = remove_hastags(text_standard)
    text_standard = remove_acronym(text_standard)[1]
    text_standard = lowercase(text_standard)
    text_standard = remove_accents(text_standard)
    text_standard = remove_punctuation(text_standard)[1]
    text_standard = remove_numbers(text_standard)
    text_standard = remove_stop_words(text_standard,table)
    return text_standard
    
def calculate_score(text_standard:str,positive:Dict[str,float],negative:Dict[str,float]):
    total_dictionary = {}
    total_dictionary.update(positive)
    total_dictionary.update(negative)
    return sum(total_dictionary.get(word,0) for word in text_standard.split())