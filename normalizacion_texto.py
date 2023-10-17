import re
import string
from typing import Dict

PATH = "path"

def leer_texto(nombre_archivo:str):
    """Abre y lee un fichero localizado en el PATH.
    
    Args:
        nombre_archivo (str)
    Returns:
        texto en forma de cadena
    """
    archivo = open( PATH + nombre_archivo, encoding="utf8")
    texto = archivo.read()
    return texto

def leer_puntuaciones(nombre_archivo:str):
    """Abre un archivo de dos columnas y guarda en un diccionario
    cada fila, donde la primera columna es la clave y la segunda el valor.
    
    Args:
        nombre_archivo (str)
    Returns:
        diccionario donde la palabra es la clave y su puntuacion
        asociada es el valor.
    """
    archivo = open(nombre_archivo, encoding="utf8")
    dic_palabras = {}
    for fila in archivo:
        datos = fila.split()
        dic_palabras[datos[0]]= float(datos[1])
    return dic_palabras

    
def convertir_minuscula(texto):
    """Convierte el texto en minuscula
    
    Args:
        string
    Returns:
        string en minuscula
    """
    return texto.lower()

def convertir_mayuscula(texto):
    """Convierte el texto en mayuscula
    
    Args:
        string
    Returns:
        string en mayuscula
    """
    return texto.upper()

def contar_palabras(texto):
    """Cuenta el numero de palabras seprando el string con el metodo split
    
    Args:
        texto(str)
    Returns:
        Lista de strings
    """
    num_palabras = len(texto.split())
    return num_palabras
    
def quitar_puntuacion(texto):
    """Busca caracteres especiales mediante una expresion regular
    
    Args:
        texto(str)
    Returns:
        Lista(list) con los caracteres encontrados y con el texto sin esos caracteres.
    """
    patron = re.findall(r"[^\w\s]",texto)
    quitar_patron = re.sub(r"[^\w\s]","",texto)
    return patron, quitar_patron
  
   
def quitar_acentos(texto):
    """Substituye las vocales con acento por vocales sin acento mediante una expresion regular
    
    Args:
        texto (str)
    Returns:
        Texto donde se han sustituido las vocales que llevaban acento
        a vocales sin acento
    """
    patron={'a':'áàä','e':'éèë','i':'íìï','o':'óòö','u':'úùü'}
    for key,value in patron.items():
        for letra in value:
            texto = texto.replace(letra,key)
    return texto

def quitar_numeros(texto):
    """Elimina los numeros encontrados en el texto mediante una expresion regular
    
    Args:
        texto (str)
    Returs:
        texto sin numeros
    """
    patron = re.sub(r"\d+", "", texto)
    return patron

def quitar_siglas(texto):
    """Busca y elimina las siglas encontradas en el texto mediante una expresion regular
    
    Args:
        texto (str)
    Returs:
        Lista con las siglas encontradas y el texto sin siglas
    """
    siglas = re.findall(r"[A-Z]{2,}",texto)
    quitar_siglas = re.sub(r"[A-Z]{2,}","",texto)
    return siglas,quitar_siglas

def quitar_stop_words(texto,lista):
    """Elimina del texto las palabras que se le pasan en una lista
    
    Args:
        texto (str)
        lista (list)
    Returns:
        String sin los elementos de la lista
    """
    match = re.sub(fr"\b({'|'.join(lista)})\b","", texto)
    if match: return match
    else: return 0

def frecuencia_palabras(texto):
    """Cuenta la frecuencia de cada palabra y lo devuelve en forma de diccionario
   
    Args:
        texto(str)
    Returns:
        Diccionario donde las claves son las palabras y los valores su frecuencia de 
        aparacion
    """
    lista_texto = texto.split()
    frecuencia_palabras = [lista_texto.count(p) for p in lista_texto]
    return dict(list(zip(lista_texto,frecuencia_palabras)))

def quitar_url(texto):
    """Elimina las url del texto mediante una expresion regular
    Args:
        texto(str)
    Returns:
        texto sin las url
    """
    return re.sub("https?\://[a-zA-Z0-9$-_@.&\+!\*\(]+","",texto)

def quitar_menciones(texto):
    """Elimina las mencions del texto mediante una expresion regular. Elimina
    aquellos string que van precedidos de @.    
    
    Args:
        texto(str)
    Returns:
        texto sin menciones
    """
    return re.sub(r'@[\w\-]+'," ",texto)

def quitar_hastags(texto):
    """Elimina los hastags del texto mediante una expresion regular. Elimina
    aquellos string que van precedidos de #.    
    
    Args:
        texto(str)
    Returns:
        texto sin hastags
    """
    return re.sub (r'#[\w\-]+'," ",texto)

def normalizar_texto(texto,lista):
    """Normaliza el texto llamando a las funciones definidas anteriormente

    Args:
        texto (str)
        lista (list)

    Returns:
        texto(str) normalizado
    """
    texto_norm = quitar_url(texto)
    texto_norm = quitar_menciones(texto_norm)
    texto_norm = quitar_hastags(texto_norm)
    texto_norm = quitar_siglas(texto_norm)[1]
    texto_norm = convertir_minuscula(texto_norm)
    texto_norm = quitar_acentos(texto_norm)
    texto_norm = quitar_puntuacion(texto_norm)[1]
    texto_norm = quitar_numeros(texto_norm)
    texto_norm = quitar_stop_words(texto_norm,lista)
    return texto_norm
    
def calcula_puntuacion(texto_normalizado:str,positivo:Dict[str,float],negativo:Dict[str,float]):
    diccionario_total = {}
    diccionario_total.update(positivo)
    diccionario_total.update(negativo)
    return sum(diccionario_total.get(palabra,0) for palabra in texto_normalizado.split())