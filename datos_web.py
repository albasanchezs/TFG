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

def datos_basicos(url_basicos,identificadores,df_final):
     dic ={}
     for i in identificadores:
               url_basicos_nuevo=requests.get(re.sub('codigoin',i,url_basicos))
               soup_datos_basicos = BeautifulSoup(url_basicos_nuevo.text, 'lxml')

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
     df =pd.DataFrame.from_dict(dic, orient='index').rename(columns={0: 'Nombre',1:'Conjunto',2:'Rama',3:'Habilita',4:'Vinculacion',5:'Codigo de Agencia'})
     df_final['Nombre']=df['Nombre']
     df_final['Conjunto'] = df['Conjunto']
     df_final['Rama'] = df['Rama']
     df_final['Habilita'] = df['Habilita']
     df_final['Vinculacion'] = df['Vinculacion']
     df_final['Condigo de Agencia'] = df['Codigo de Agencia']




#Descripcion de competencias dado el tipo de competencias que quieres.Dado 1,2 o las 3 competencias va leyendo y crea columnas en funcion de ellas.


def datos_competencias(url_competencias,identificadores,df_final,list_ident):
     dic = {}
     nombre_competencia = ""
     #identificadores = creacion_tablas(url_tablas, lis_titulo, lis_uni, lis_estado)
     for tipodecomp in list_ident:
          print(tipodecomp)
          for i in identificadores:
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
                    #table = soup_competencias.select('table')[0]
                    df_sistemaforma = pd.read_html(str(soup_competencias.select('table')[0]))[0]
                    inputTagultimo = df_sistemaforma['Denominación'].tolist()
                    dic[i] = inputTagultimo
               except Exception as e:
                    dic[i] = 'Tabla no encontrada'

          df_final[nombre_competencia] = dic


#Fechas de inicio:
def datos_calendarios(url_calendario,identificadores,df_final):
     dic={}
     for i in identificadores:
          calendario=requests.get(re.sub('codigoin',i,url_calendario))
          soup_calendario=BeautifulSoup(calendario.text,'lxml')
          try:
               output = soup_calendario.findAll(attrs={"name": "curso_Inicio"})[0]['value']
          except Exception as e:
               output = 0
          dic[i]=output
     df_final['Fecha de Inicio'] = dic



#Modulo de materias:
def datos_modulo(url_modulos,identificadores,df_final):
     dic ={}
     sal ={}
     for i in identificadores:
          modulo = requests.get(re.sub('codigoin', i, url_modulos))
          soup_modulo = BeautifulSoup(modulo.text, 'lxml')
          try:
               #table = soup_modulo.select('table')[0]
               df_modulo = pd.read_html(str(soup_modulo.select('table')[0]))[0]
               modulo = df_modulo['Denominación'].tolist()
               dic[i] = modulo
          except Exception as e:
               dic[i]='No encontrado'
     df_final['Modulo']= dic



#Metodología:
def datos_metodologia(url_metodologia,identificadores,df_final):
     dic={}
     sal={}
     for i in identificadores:
          metodologia=requests.get(re.sub('codigoin',i,url_metodologia))
          soup_metodologia=BeautifulSoup(metodologia.text,'lxml')
          try :

               #table = soup_metodologia.select('table')[0]
               df_metodologia = pd.read_html(str(soup_metodologia.select('table')[0]))[0]
               meto = df_metodologia['Denominación'].tolist()
               dic[i]=meto
          except Exception as e:
               dic[i]='Tabla no encontrada'

     df_final['Metodologia']=dic


#Sistema de Evaluación:
def datos_sistemas(url_sistemaforma,identificadores,df_final):
     dic={}
     sal={}
     for i in identificadores:
          formacion=requests.get(re.sub('codigoin',i,url_sistemaforma))
          soup_formacion=BeautifulSoup(formacion.text,'lxml')
          try :

              # table = soup_formacion.select('table')[0]
               df_sistemaforma = pd.read_html(str(soup_formacion.select('table')[0]))[0]
               sistemaforma=df_sistemaforma['Denominación'].tolist()
               dic[i] = sistemaforma
          except Exception as e:
               dic[i] = 'Tabla no encontrada'
     df_final['Evaluacion']=dic
