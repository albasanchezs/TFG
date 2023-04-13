import datos_web
import descarga_web
import main
import errno
import time
from bs4 import BeautifulSoup
import requests
import re
import contractions
import pandas as pd
import pdfplumber

#1. Primera parte:

#Extrae todos los identificativos de todas las universidades que hay en la web y lo introduce en una lista
def universidades(opciones):
     soup = BeautifulSoup( requests.get('https://www.educacion.gob.es/ruct/consultaestudios?actual=estudios').text, 'lxml')
     opciones=[elem['value'] for elem in soup.find(id ='codigoUniversidad').find_all('option') if elem['value'] !="" ]
     return opciones



#Creacion de identificadores para los urls: dado el numero lee tablas del numero hasta 1 y todos sus identificadores de la url que te manda
def creacion_identificadores(cad,url_tablas):
     identificadores=[]
     numtablas = []
     while cad > 0:
          numtablas.append(str(cad))
          cad = cad - 1
     for i in numtablas:
          soup = BeautifulSoup(requests.get(re.sub('codigotablas', i, url_tablas)).text, 'lxml')
          enlace_siguiente = soup.find_all(class_="ver")
          for sep in enlace_siguiente:
               # mirar esto del indice
               subcadena = str(sep)[str(sep).index('cod=') + 4:str(sep).index('&amp')]
               if subcadena != None:
                    identificadores.append(subcadena)
     return identificadores


#lectura de identificadores de todas las universidades de todas las tablas: Por cada universidad lee el numero max de tabla
#saca todos los identificativos de esa universidad y los concatena con los que ya tiene.

def creacion_tablas(url_tabla,opciones):
     cadena=""
     url_uni = re.sub('universidad', opciones, url_tabla)
     soup = BeautifulSoup(requests.get(re.sub('universidad', opciones, url_tabla)).text, 'lxml')
     num = soup.findAll(class_="pagelinks")
     if not num:
          cad=1
     else:
          for i in num:
               y = i.find_all('a')
               cadena = str(y[len(y) - 1])
          cad = int(cadena[cadena.index("-p=") + 3:cadena.index("&amp;ambito=&amp;")])

     identificadores = creacion_identificadores(cad, url_uni)
     list =[identificadores,cad]
     return list

def curves_to_edges(cs):
    edges = []
    for c in cs:
        edges += pdfplumber.utils.rect_to_edges(c)
    return edges


def limpieza(text):
    page_text = re.sub('(http[s]?:\/\/|www\.)[^\s]+', '', text)
    page_text = re.sub('\n', '', text)
    page_text = re.sub("r'https://\S+|www\.\S+'", '', page_text)
    expanded_text = contractions.fix(page_text).lower()
    return expanded_text

def insert_multiple_rows(self):
    workbook = self.Workbook(self.dataDir + 'Prueba.xlsx')
    worksheet = workbook.getWorksheets().get(0)
    worksheet.getCells().insertRows(2,10)
    workbook.save(self.dataDir + "Insert Multiple Rows.xls")
    print("exito")