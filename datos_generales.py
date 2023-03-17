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
     url_universidades = requests.get('https://www.educacion.gob.es/ruct/consultaestudios?actual=estudios')
     soupuni = BeautifulSoup(url_universidades.text, 'lxml')
     listopc=soupuni.find(id ='codigoUniversidad').find_all('option')
     for elem in listopc:
          if elem['value'] !="":
               opciones.append(elem['value'])

     return opciones

#Creacion de la tabla iniciar de la url que se le pasa y guarda nombre, uni,estado.

def tabla_inicial(url_uni,cad,identificadores,dic1,dic2):
     listanumeros = []
     #while num > 0:
     num=cad
     while num>5:
          listanumeros.append(str(num))
          num = num - 1
     for i in listanumeros:
          ex = requests.get(re.sub('codigotablas', i, url_uni))
          soupprincipal = BeautifulSoup(ex.text, 'lxml')
          table = soupprincipal.select('table')[0]
          df_tabla = pd.read_html(str(table))[0]
          for codigoentabla in df_tabla["Código"]:
               for codigoiden in identificadores:
                    u=codigoiden[0:7]
                    if str(codigoentabla) == u:
                         dic1[codigoiden]=df_tabla.loc[df_tabla['Código']==codigoentabla]['Universidad'].tolist()
                         dic2[codigoiden]=df_tabla.loc[df_tabla['Código'] == codigoentabla]['Estado'].tolist()

#Creacion de identificadores para los urls: dado el numero lee tablas del numero hasta 1 y todos sus identificadores de la url que te manda
def creacion_identificadores(num,url_tablas):
     identificadores=[]
     listanumeros = []
     #while num > 0:
     while num > 5:
          listanumeros.append(str(num))
          num = num - 1
     for i in listanumeros:
          ex = requests.get(re.sub('codigotablas', i, url_tablas))
          soupprincipal = BeautifulSoup(ex.text, 'lxml')
          enlace_siguiente = soupprincipal.find_all(class_="ver")
          listsep = []
          cadenain ='cod='
          cadenafin ='&amp'
          for sep in enlace_siguiente:
               i=str(sep)
               indice1 = i.index(cadenain)
               indice2 = i.index(cadenafin)
               # mirar esto del indice
               subcadena = i[indice1 + 4:indice2]
               if subcadena != None:
                    identificadores.append(subcadena)
     return identificadores


#lectura de identificadores de todas las universidades de todas las tablas: Por cada universidad lee el numero max de tabla
#saca todos los identificativos de esa universidad y los concatena con los que ya tiene.

def creacion_tablas(url_tabla,df_final):
     dic1={}
     dic2={}
     identificadores =[]
     opciones = []
     cadena=""
     opciones=universidades(opciones)
     opciones=['036'] #prueba que solo lee la de catalunya y la de la uc3m
     for i in opciones:
          url_uni = re.sub('universidad', i, url_tabla)
          text_url = requests.get(url_uni)
          soup = BeautifulSoup(text_url.text, 'lxml')
          num = soup.findAll(class_="pagelinks")
          for i in num:
               y = i.find_all('a')
               cadena = y[len(y) - 1]
               cadena = str(cadena)
          indice1 = cadena.index("-p=")
          indice2 = cadena.index("&amp;ambito=&amp;")

          # mirar esto del indice
          cad = cadena[indice1 + 3:indice2]
          cad = int(cad)
          cad = 6 #aqui debería estar num pero se me hace muy largo
          identificadores += creacion_identificadores(cad, url_uni)
          tabla_inicial(url_uni,cad,creacion_identificadores(cad, url_uni),dic1,dic2)
     df_final['Universidad']= dic1
     df_final['Estado'] = dic2
     return identificadores
