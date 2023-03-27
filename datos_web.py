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

def datos_basicos(url_basicos,identificadores,df):
     dic ={}
     for i in identificadores:
               time.sleep(1)
               soup_datos_basicos = BeautifulSoup(requests.get(re.sub('codigoin',i,url_basicos)).text, 'lxml')

               try:
                    inputTag0 = soup_datos_basicos.findAll(attrs={"name": "denominacion"})[0]['value']
                    #dic_ttitulo[i]=output0
               except Exception as e:
                    inputTag0 = 'No encontrado'
               try:
                    inputTag = soup_datos_basicos.findAll(attrs={"name": "conjunto"})[0]['value']
                    #dic_conjungo[i]=output
               except Exception as e:
                    inputTag='No encontrado'

               try:
                    inputTag1 = soup_datos_basicos.findAll(attrs={"name": "rama.codigo"})[0]['value']
               except Exception as e:
                    inputTag1='No encontrado'

               try:
                    inputTag3 = soup_datos_basicos.findAll(attrs={"name": "habilita"})[0]['value']
               except Exception as e:
                    inputTag3='No encontrado'

               try:
                    inputTag4 = soup_datos_basicos.findAll(attrs={"name": "vinculado"})[0]['value']
               except Exception as e:
                    inputTag4 = 'No encontrado'
               try:
                    inputTag5 = soup_datos_basicos.findAll(attrs={"name": "codigoAgencia"})[0]['value']
               except Exception as e:
                    inputTag5 = 'No encontrado'

               dic[i]=[inputTag0,inputTag,inputTag1,inputTag3,inputTag4,inputTag5]
     df_int =pd.DataFrame.from_dict(dic, orient='index').rename(columns={0: 'Nombre',1:'Conjunto',2:'Rama',3:'Habilita',4:'Vinculacion',5:'Codigo de Agencia'})
     df['Nombre']=df_int['Nombre']
     df['Conjunto'] = df_int['Conjunto']
     df['Rama'] = df_int['Rama']
     df['Habilita'] = df_int['Habilita']
     df['Vinculacion'] = df_int['Vinculacion']
     df['Condigo de Agencia'] = df_int['Codigo de Agencia']




#Descripcion de competencias dado el tipo de competencias que quieres.Dado 1,2 o las 3 competencias va leyendo y crea columnas en funcion de ellas.


def datos_competencias(url_competencias,identificadores,df,list_ident):
     dic = {}
     nombre_competencia = ""
     for tipodecomp in list_ident:
          for i in identificadores:
               time.sleep(2)#aqui es donde se para pero despues de bastante tiempo
               t_competencias = re.sub('codigoin', i, url_competencias)
               if tipodecomp == 'G':
                    nombre_competencia = "Compentencias Generales"
                    t_competencias = re.sub('palabratipocomp', 'generales', t_competencias)
                    t_competencias = requests.get(re.sub('tipodecomp', 'G', t_competencias))
               elif tipodecomp == 'T':
                    nombre_competencia = "Compentencias transversles"
                    t_competencias = re.sub('palabratipocomp', 'transversales', t_competencias)
                    t_competencias = requests.get(re.sub('tipodecomp', 'T', t_competencias))
               elif tipodecomp == 'E':
                    nombre_competencia = "Compentencias Especificas"
                    t_competencias = re.sub('palabratipocomp', 'especificas', t_competencias)
                    t_competencias = requests.get(re.sub('tipodecomp', 'E', t_competencias))

               soup_competencias = BeautifulSoup(t_competencias.text, 'lxml')
               try:
                    inputTag = soup_competencias.findAll('td')
                    df_sistemaforma = pd.read_html(str(soup_competencias.select('table')[0]))[0]
                    dic[i] = df_sistemaforma['Denominación'].tolist()
               except Exception as e:
                    dic[i] = 'Tabla no encontrada'

          df[nombre_competencia] = dic


#Fechas de inicio:
def datos_calendarios(url_calendario,identificadores,df):
     dic={}
     for i in identificadores:
          time.sleep(2)
          soup_calendario=BeautifulSoup(requests.get(re.sub('codigoin',i,url_calendario)).text,'lxml')
          try:
               output = soup_calendario.findAll(attrs={"name": "curso_Inicio"})[0]['value']
          except Exception as e:
               output = 0
          dic[i]=output
     df['Fecha de Inicio'] = dic



#Modulo de materias:
def datos_modulo(url_modulos,identificadores,df):
     dic ={}
     sal ={}
     for i in identificadores:
          time.sleep(2)
          soup_modulo = BeautifulSoup(requests.get(re.sub('codigoin', i, url_modulos)).text, 'lxml')
          try:
               #table = soup_modulo.select('table')[0]
               df_modulo = pd.read_html(str(soup_modulo.select('table')[0]))[0]
               dic[i] = df_modulo['Denominación'].tolist()
          except Exception as e:
               dic[i]='No encontrado'
     df['Modulo']= dic



#Metodología:
def datos_metodologia(url_metodologia,identificadores,df):
     dic={}
     sal={}
     for i in identificadores:
          time.sleep(2)
          soup_metodologia=BeautifulSoup(requests.get(re.sub('codigoin',i,url_metodologia)).text,'lxml')
          try :
               df_metodologia = pd.read_html(str(soup_metodologia.select('table')[0]))[0]
               dic[i]=df_metodologia['Denominación'].tolist()
          except Exception as e:
               dic[i]='Tabla no encontrada'

     df['Metodologia']=dic


#Sistema de Evaluación:
def datos_sistemas(url_sistemaforma,identificadores,df):
     dic={}
     for i in identificadores:
          time.sleep(2)
          soup_formacion=BeautifulSoup(requests.get(re.sub('codigoin',i,url_sistemaforma)).text,'lxml')
          try :
              # table = soup_formacion.select('table')[0]
               df_sistemaforma = pd.read_html(str(soup_formacion.select('table')[0]))[0]
               dic[i] = df_sistemaforma['Denominación'].tolist()
          except Exception as e:
               dic[i] = 'Tabla no encontrada'
     df['Evaluacion']=dic
