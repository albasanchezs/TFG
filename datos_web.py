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
from tabula import read_pdf
import logging

class datos_web():
     """
     Clase para comprobar que los enlaces a url, lista , id estan correctos
          -extraer datos basicos
          -tablas de competencias,modulo,formacion,metodologia
          -fecha de calendario

     """
     def __init__(self,*args):

         self._Mode(*args)

     def _Mode(self,*args):
          """

          Control de tipo de url que llega para leer
          :param args: url, identificador, lista de competencias, dataframe

          """
          mode_1 = 'basicos'
          mode_2 = 'competencias.palabratipocomp'
          mode_3 = 'calendarioImplantacion.cronograma'
          mode_4 = 'planificacion.modulos'
          mode_5 = 'planificacion.metodologias'
          mode_6 = 'planificacion.sistemas'
          if len(args)==3:
               mode_url = str(args[0])[str(args[0]).index('actual=menu.solicitud.') + 22:str(args[0]).index('&')]
               if mode_url == mode_1:
                    df_int = self._datos_basicos(args[0],args[1])
                    args[2]['Nombre'] = df_int['Nombre']
                    args[2]['Conjunto'] = df_int['Conjunto']
                    args[2]['Rama'] = df_int['Rama']
                    args[2]['Habilita'] = df_int['Habilita']
                    args[2]['Vinculacion'] = df_int['Vinculacion']
                    args[2]['Condigo de Agencia'] = df_int['Codigo de Agencia']
               if mode_url == mode_3:
                    args[2]['calendario'] = self._datos_calendarios(args[0],args[1])
               if mode_url ==mode_4:
                    args[2]['Modulo']=self._datos_tablas(args[0],args[1])
               if mode_url ==mode_5:
                    args[2]['Metodologia'] = self._datos_tablas(args[0], args[1])
               if mode_url == mode_6:
                    args[2]['Sistema de Formacion'] = self._datos_tablas(args[0], args[1])
          elif len(args)==4:
               mode_url = str(args[0])[str(args[0]).index('actual=menu.solicitud.') + 22:str(args[0]).index('&')]
               if mode_url == mode_2:
                    if args[2]:
                         for tipodecomp in args[2]:
                              nombre_competencia=""
                              if tipodecomp == 'G':
                                   nombre_competencia = "Compentencias Generales"

                              elif tipodecomp == 'T':
                                   nombre_competencia = "Compentencias transversales"

                              elif tipodecomp == 'E':
                                   nombre_competencia = "Compentencias Especificas"

                              args[3][nombre_competencia] = self.datos_competencias(args[0],args[1],nombre_competencia)
          elif len(args)==5:
               args[4]['Universidad']=self.tabla_inicial(args[0], args[1], args[2], args[3],'Universidad')
               args[4]['Estado'] = self.tabla_inicial(args[0], args[1], args[2], args[3],'Estado')

     def _datos_basicos(self,url,id):
          """

          :param url:  url basica de datos primarios; Nombre, agencia, conjunto, Rama
          :param id:   identificador de la titulacion indicada
          :return:     dataframe de los datos asociados al id
          """
          dic={}
          time.sleep(1)
          soup=BeautifulSoup(requests.get(re.sub('codigoin',id,url)).text, 'lxml')

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
          return df_int


     def _datos_calendarios(self, url, id):
          """

          :param url:  url que indica la fecha de inicio de la titulacion
          :param id:   identificador de la titulacion indicada
          :return:     diccionario con la fecha asociada al identificador
          """
          dic={}
          soup = BeautifulSoup(requests.get(re.sub('codigoin', id, url)).text, 'lxml')
          try:
               output = soup.findAll(attrs={"name": "curso_Inicio"})[0]['value']
          except Exception as e:
               output = 0
          dic[id]=output
          return dic


     def datos_competencias(self,url,id,nombre_compt):
          """

          :param url: url asociada a la parte de las tablas de competencias
          :param id: identificador de la titulacion indicada
          :param nombre_compt: clase de competencia que se lee; especifica, general o transversal
          :return: diccionario del id asociado a una lista de competencias
          """
          dic={}
          t_competencias = re.sub('codigoin', id, url)
          if nombre_compt == "Compentencias Generales":
                   t_competencias = re.sub('palabratipocomp', 'generales', t_competencias)
                   t_competencias = requests.get(re.sub('tipodecomp', 'G', t_competencias))
          elif nombre_compt == "Compentencias transversales":
                    t_competencias = re.sub('palabratipocomp', 'transversales', t_competencias)
                    t_competencias = requests.get(re.sub('tipodecomp', 'T', t_competencias))
          elif nombre_compt == "Compentencias Especificas":
                     t_competencias = re.sub('palabratipocomp', 'especificas', t_competencias)
                     t_competencias = requests.get(re.sub('tipodecomp', 'E', t_competencias))

          soup = BeautifulSoup(t_competencias.text, 'lxml')
          try:
               df_sistemaforma = pd.read_html(str(soup.select('table')[0]))[0]
               dic[id] = df_sistemaforma['Denominación'].tolist()
          except Exception as e:
               dic[id] = 'Tabla no encontrada'

          return dic


     def _datos_tablas(self,url,id):
          """

          :param url: url que puede leer sistemas de formacion de titulacion, modulos y metodologias existentes asociados al id
          :param id: identificador de la titulacion indicada
          :return: diccionario del id asociado a una lista de competencias
          """
          dic={}
          soup = BeautifulSoup(requests.get(re.sub('codigoin', id, url)).text, 'lxml')
          try:
               df_modulo = pd.read_html(str(soup.select('table')[0]))[0]
               dic[id] = df_modulo['Denominación'].tolist()
          except Exception as e:
                dic[id] ='No encontrado'

          return dic

     #Creacion de la tabla inicial de la url que se le pasa y guarda nombre, uni,estado.
     def tabla_inicial(self,url_tabla,id,op,cad,col):
          """

          :param url_tabla:  url general donde aparecen todas las titulaciones
          :param id:         id que busco para completar los datos
          :param op:         universidad donde estoy
          :param cad:        numero de tablas maxi
          :param col:        leo columna univer o columna estado
          :return:           diccionario donde se asocia el id a la info guardada
          """
          numtablas=[]
          encontrado=1
          dic={}
          while cad > 0:
               numtablas.append(str(cad))
               cad = cad - 1
          url_tabla = re.sub('universidad', op, url_tabla)
          for i in numtablas:
               soup = BeautifulSoup(requests.get(re.sub('codigotablas', i, url_tabla)).text, 'lxml')
               try:
                    df_tabla = pd.read_html(str(soup.select('table')[0]))[0]
                    for codigoentabla in df_tabla["Código"]:
                         try:
                            if str(codigoentabla) == id[0:7]:
                                 #'Universidad'
                                 dic[id] = df_tabla.loc[df_tabla['Código'] == codigoentabla][col].tolist()
                                # dic2[id] = df_tabla.loc[df_tabla['Código'] == codigoentabla]['Estado'].tolist()

                         except Exception as e:
                              dic[id] = "No encontrado"
               except Exception as e:
                    encontrado=0
          return dic
          #df['Estado']=dic2