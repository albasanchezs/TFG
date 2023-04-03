import datos_web
import descarga_web
import main
import errno
import time
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

#1. Primera parte:

#Extrae todos los identificativos de todas las universidades que hay en la web y lo introduce en una lista
def universidades(opciones):
     soup = BeautifulSoup( requests.get('https://www.educacion.gob.es/ruct/consultaestudios?actual=estudios').text, 'lxml')
     opciones=[elem['value'] for elem in soup.find(id ='codigoUniversidad').find_all('option') if elem['value'] !="" ]
     return opciones

#Creacion de la tabla iniciar de la url que se le pasa y guarda nombre, uni,estado.

def tabla_inicial(url_tabla,id,df,op,cad):
     numtablas=[]
     encontrado=1
     dic1={}
     dic2 = {}
     while cad > 0:
          numtablas.append(str(cad))
          cad = cad - 1
     url_tabla = re.sub('universidad', op, url_tabla)
     for i in numtablas:
          soup = BeautifulSoup(requests.get(re.sub('codigotablas', i, url_tabla)).text, 'lxml')
          try:
               df_tabla = pd.read_html(str(soup.select('table')[0]))[0]
               for codigoentabla in df_tabla["Código"]:
                    #for id in identificadores:
                    try:
                       if str(codigoentabla) == id[0:7]:
                            dic1[id] = df_tabla.loc[df_tabla['Código'] == codigoentabla]['Universidad'].tolist()
                            dic2[id] = df_tabla.loc[df_tabla['Código'] == codigoentabla]['Estado'].tolist()

                    except Exception as e:
                         encontrado=0

          except Exception as e:
               encontrado=0
     df['Codigo']=dic1
     df['Estado']=dic2

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
