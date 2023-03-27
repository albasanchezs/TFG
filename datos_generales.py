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

def tabla_inicial(url_uni,cad,identificadores,dic1,dic2):
     numtablas = []
     #while num > 5:
     num=cad
     while num>0:
          numtablas.append(str(num))
          num = num - 1
     for i in numtablas:
          soupprincipal = BeautifulSoup(requests.get(re.sub('codigotablas', i, url_uni)).text, 'lxml')
          try:
               df_tabla = pd.read_html(str(soupprincipal.select('table')[0]))[0]
               for codigoentabla in df_tabla["Código"]:
                    for codigoiden in identificadores:
                         if str(codigoentabla) == codigoiden[0:7]:
                              dic1[codigoiden]=df_tabla.loc[df_tabla['Código']==codigoentabla]['Universidad'].tolist()
                              dic2[codigoiden]=df_tabla.loc[df_tabla['Código'] == codigoentabla]['Estado'].tolist()
          except Exception as e:
               print('Aqui no hay dato')

#Creacion de identificadores para los urls: dado el numero lee tablas del numero hasta 1 y todos sus identificadores de la url que te manda
def creacion_identificadores(num,url_tablas):
     identificadores=[]
     numtablas = []
     #while num > 5:
     while num > 0:
          numtablas.append(str(num))
          num = num - 1
     for i in numtablas:
          soupprincipal = BeautifulSoup(requests.get(re.sub('codigotablas', i, url_tablas)).text, 'lxml')
          enlace_siguiente = soupprincipal.find_all(class_="ver")
          cadenain ='cod='
          cadenafin ='&amp'
          for sep in enlace_siguiente:
               indice1 = str(sep).index(cadenain)
               indice2 = str(sep).index(cadenafin)
               # mirar esto del indice
               subcadena = str(sep)[indice1 + 4:indice2]
               if subcadena != None:
                    identificadores.append(subcadena)
     return identificadores


#lectura de identificadores de todas las universidades de todas las tablas: Por cada universidad lee el numero max de tabla
#saca todos los identificativos de esa universidad y los concatena con los que ya tiene.

def creacion_tablas(url_tabla,df,opciones):
     dic1={}
     dic2={}
     identificadores =[]
     cadena=""
     cad=1
     url_uni = re.sub('universidad', opciones, url_tabla)
     soup = BeautifulSoup(requests.get(re.sub('universidad', opciones, url_tabla)).text, 'lxml')
     num = soup.findAll(class_="pagelinks")
     if not num:
          cad=1
     else:
          for i in num:
               y = i.find_all('a')
               cadena = y[len(y) - 1]
               cadena = str(cadena)
          indice1 = cadena.index("-p=")
          indice2 = cadena.index("&amp;ambito=&amp;")

          # mirar esto del indice
          cad = int(cadena[indice1 + 3:indice2])
          #cad = 6 #aqui debería estar num pero se me hace muy largo
          identificadores = creacion_identificadores(cad, url_uni)
     tabla_inicial(url_uni,cad,creacion_identificadores(cad, url_uni),dic1,dic2)
     if not dic1 and not dic2:
          df['Universidad'] = "No encontrado"
          df['Estado'] = "No encontrado"
     else:
          df['Universidad']= dic1
          df['Estado'] = dic2
     return identificadores
