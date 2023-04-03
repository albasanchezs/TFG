import descarga_web
import datos_generales
import main
import errno
import time
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import lxml

#2. Datos de la web importantes:

#Datos basicos

def datos_basicos(url_basicos,id,df):
     dic={}
     time.sleep(1)
     soup = BeautifulSoup(requests.get(re.sub('codigoin',id,url_basicos)).text, 'lxml')

     try: nom = soup.findAll(attrs={"name": "denominacion"})[0]['value']
     except Exception as e:  nom = 'No encontrado'

     try: conju = soup.findAll(attrs={"name": "conjunto"})[0]['value']
     except Exception as e: conju='No encontrado'

     try: rama = soup.findAll(attrs={"name": "rama.codigo"})[0]['value']
     except Exception as e: rama='No encontrado'

     try: conv = soup.findAll(attrs={"name": "habilita"})[0]['value']
     except Exception as e: conv='No encontrado'

     try: vinculacion = soup.findAll(attrs={"name": "vinculado"})[0]['value']
     except Exception as e: vinculacion = 'No encontrado'

     try: codigoAgencia = soup.findAll(attrs={"name": "codigoAgencia"})[0]['value']
     except Exception as e: codigoAgencia = 'No encontrado'

     dic[id] = [nom, conju, rama, conv, vinculacion, codigoAgencia]
     df_int = pd.DataFrame.from_dict(dic, orient='index').rename(
          columns={0: 'Nombre', 1: 'Conjunto', 2: 'Rama', 3: 'Habilita', 4: 'Vinculacion', 5: 'Codigo de Agencia'})
     df['Nombre'] = df_int['Nombre']
     df['Conjunto'] = df_int['Conjunto']
     df['Rama'] = df_int['Rama']
     df['Habilita'] = df_int['Habilita']
     df['Vinculacion'] = df_int['Vinculacion']
     df['Condigo de Agencia'] = df_int['Codigo de Agencia']


#Descripcion de competencias dado el tipo de competencias que quieres.Dado 1,2 o las 3 competencias va leyendo y crea columnas en funcion de ellas.


def datos_competencias(url_competencias,id,df,list_ident):
     nombre_competencia = ""
     dic={}
     for tipodecomp in list_ident:
          time.sleep(2)
          t_competencias = re.sub('codigoin', id, url_competencias)
          if tipodecomp == 'G':
              nombre_competencia = "Compentencias Generales"
              t_competencias = re.sub('palabratipocomp', 'generales', t_competencias)
              t_competencias = requests.get(re.sub('tipodecomp', 'G', t_competencias))
          elif tipodecomp == 'T':
               nombre_competencia = "Compentencias transversales"
               t_competencias = re.sub('palabratipocomp', 'transversales', t_competencias)
               t_competencias = requests.get(re.sub('tipodecomp', 'T', t_competencias))
          elif tipodecomp == 'E':
                nombre_competencia = "Compentencias Especificas"
                t_competencias = re.sub('palabratipocomp', 'especificas', t_competencias)
                t_competencias = requests.get(re.sub('tipodecomp', 'E', t_competencias))

          soup_competencias = BeautifulSoup(t_competencias.text, 'lxml')
          try:
               df_sistemaforma = pd.read_html(str(soup_competencias.select('table')[0]))[0]
               dic[id] = df_sistemaforma['Denominación'].tolist()
          except Exception as e:
               dic[id] = 'Tabla no encontrada'

          df[nombre_competencia] = dic



#Fechas de inicio:
def datos_calendarios(url_calendario,id,df):
     time.sleep(2)
     soup=BeautifulSoup(requests.get(re.sub('codigoin',id,url_calendario)).text,'lxml')
     try:  output = soup.findAll(attrs={"name": "curso_Inicio"})[0]['value']
     except Exception as e:  output = 0

     df['calendario']=output


#Modulo de materias:
def datos_modulo(url_modulos,id,df):
     time.sleep(2)
     soup = BeautifulSoup(requests.get(re.sub('codigoin', id, url_modulos)).text, 'lxml')
     try:
          df_modulo = pd.read_html(str(soup.select('table')[0]))[0]
          cont = df_modulo['Denominación'].tolist()
     except Exception as e:
           cont='No encontrado'

     df['Modulo']=cont

#Metodología:
def datos_metodologia(url_metodologia,id,df):
     dic={}
     time.sleep(2)
     soup=BeautifulSoup(requests.get(re.sub('codigoin',id,url_metodologia)).text,'lxml')
     try :
         df_metodologia = pd.read_html(str(soup.select('table')[0]))[0]
         dic[id]=df_metodologia['Denominación'].tolist()
     except Exception as e:
          dic[id]='Tabla no encontrada'
     df['Metodologia']=dic

#Sistema de Evaluación:
def datos_sistemas(url_sistemaforma,id,df):
     dic={}
     time.sleep(2)
     soup=BeautifulSoup(requests.get(re.sub('codigoin',id,url_sistemaforma)).text,'lxml')
     try :
        df_sistemaforma = pd.read_html(str(soup.select('table')[0]))[0]
        dic[id] = df_sistemaforma['Denominación'].tolist()
     except Exception as e:
         dic[id] = 'Tabla no encontrada'
     df['Formacion']=dic