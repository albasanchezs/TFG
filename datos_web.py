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
import tabula
import contractions
import pdfplumber
import re
import requests
from bs4 import BeautifulSoup



class datos_web():
    """
         Clase para comprobar que los enlaces a url, lista , id estan correctos
              -extraer datos basicos
              -tablas de competencias,modulo,formacion,metodologia
              -fecha de calendario

    """
    def __init__(self,logger=None):
        self._logger = logger or logging.getLogger(__name__)

    def control(lista, id, competencias, principal, op, max_tabla, pdf, ubicacion):
          df = pd.DataFrame()

          for i in lista:
              datos_web._Mode(i, id, df)
          datos_web._Mode(principal, id, op, max_tabla, df)
          datos_web._Mode(competencias[0], id, competencias[1], df)
          datos_web.dow_pdf(pdf, id, ubicacion, df)

          return df


    def _Mode(*args):
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

          mode_url_to_func = {
              mode_1: datos_web.get_basic_data,
              mode_2: datos_web.get_competencies,
              mode_3: datos_web.get_year,
              mode_4: datos_web.get_info,
              mode_5: datos_web.get_info,
              mode_6: datos_web.get_info,
          }

          if len(args)==3:
               mode_url = str(args[0])[str(args[0]).index('actual=menu.solicitud.') + 22:str(args[0]).index('&')]
               func = mode_url_to_func[mode_url]
               if mode_url == mode_1:
                    df_int = func(args[0], args[1])
                    args[2]['Nombre'] = df_int['Nombre']
                    args[2]['Conjunto'] = df_int['Conjunto']
                    args[2]['Rama'] = df_int['Rama']
                    args[2]['Habilita'] = df_int['Habilita']
                    args[2]['Vinculacion'] = df_int['Vinculacion']
                    args[2]['Condigo de Agencia'] = df_int['Codigo de Agencia']

               if mode_url == mode_3:
                        args[2]['calendario'] = func(args[0], args[1])
                        time.sleep(2)
               if mode_url == mode_4:
                        args[2]['Modulo'] = func(args[0], args[1])
                        time.sleep(2)
               if mode_url == mode_5:
                        args[2]['Metodologia'] = func(args[0], args[1])
                        time.sleep(2)
               if mode_url == mode_6:
                        args[2]['Sistema de Formacion'] = func(args[0], args[1])

               time.sleep(2)
          elif len(args)==4:
               mode_url = str(args[0])[str(args[0]).index('actual=menu.solicitud.') + 22:str(args[0]).index('&')]
               func = mode_url_to_func[mode_url]
               if mode_url == mode_2:
                    if args[2]:
                         for tipodecomp in args[2]:
                              nombre_competencia=""
                              if tipodecomp == 'G':
                                   nombre_competencia = "Compentencias Generales"

                              elif tipodecomp == 'T':
                                   nombre_competencia = "Compentencias Transversales"

                              elif tipodecomp == 'E':
                                   nombre_competencia = "Compentencias Especificas"
                              args[3][nombre_competencia] = func(args[0],args[1],nombre_competencia)
                              time.sleep(6)
          elif len(args)==5:
              args[4]['Universidad'] = datos_web.get_status(args[0], args[1], args[2], args[3], 'Universidad')
              time.sleep(3)
              args[4]['Estado'] = datos_web.get_status(args[0], args[1], args[2], args[3], 'Estado')



    def basico(url,var,id):
        soup = BeautifulSoup(requests.get(re.sub('codigoin', id, url),verify=False).text, 'lxml')
        try:
          out = soup.findAll(attrs={"name": var})[0]['value']
        except Exception as e:
            out = "No encontrado"
            logging.info(f"This data doesn't exist")
        return out

    def get_basic_data(url,id):
          """
          :param url:  url basica de datos primarios; Nombre, agencia, conjunto, Rama
          :param id:   identificador de la titulacion indicada
          :return:     dataframe de los datos asociados al id
          """
          sleep_duration = 4
          time.sleep(4)
          variables = ["denominacion", "conjunto", "rama.codigo", "habilita", "vinculado", "codigoAgencia"]
          data = [datos_web.basico(url, var, id) for var in variables]
          df_int = pd.DataFrame([data], index=[id],
                                columns=['Nombre', 'Conjunto', 'Rama', 'Habilita', 'Vinculacion', 'Codigo de Agencia'])
          return df_int


    def get_year(url, id):
          """

          :param url:  url que indica la fecha de inicio de la titulacion
          :param id:   identificador de la titulacion indicada
          :return:     diccionario con la fecha asociada al identificador
          """
          sleep_duration = 4
          time.sleep(sleep_duration)
          fecha_in = datos_web.basico(url, "curso_Inicio", id)
          return {id: fecha_in}


    def get_competencies(url,id,nombre_compt):
          """

          :param url: url asociada a la parte de las tablas de competencias
          :param id: identificador de la titulacion indicada
          :param nombre_compt: clase de competencia que se lee; especifica, general o transversal
          :return: diccionario del id asociado a una lista de competencias
          """

          competencies = {
              "Compentencias Generales": {"palabra": "generales", "tipo": "G"},
              "Compentencias Transversales": {"palabra": "transversales", "tipo": "T"},
              "Compentencias Especificas": {"palabra": "especificas", "tipo": "E"}
          }
          url_params = competencies.get(nombre_compt)
          t_competencias = re.sub('codigoin', id, url)
          if url_params:
              t_competencias = re.sub('palabratipocomp', url_params["palabra"], t_competencias)
              t_competencias = requests.get(re.sub('tipodecomp', url_params["tipo"], t_competencias), verify=False)
              soup = BeautifulSoup(t_competencias.text, 'lxml')
              soup = BeautifulSoup(t_competencias.text, 'lxml')
          try:
              df_sistemaforma = pd.read_html(str(soup.select('table')[0]))[0]
              info = df_sistemaforma['Denominación'].tolist()
          except Exception as e:
               info = 'No encontrado'
          return {id:info}


    def get_info(url,id):
          """
          :param url: url que puede leer sistemas de formacion de titulacion, modulos y metodologias existentes asociados al id
          :param id: identificador de la titulacion indicada
          :return: diccionario del id asociado a una lista de competencias
          """
          sleep_duration = 4
          time.sleep(sleep_duration)
          soup = BeautifulSoup(requests.get(re.sub('codigoin', id, url),verify=False).text, 'lxml')
          try:
               data = pd.read_html(str(soup.select('table')[0]))[0]
               info = data['Denominación'].tolist()
          except Exception as e:
                info ="No encontrado"

          return {id : info}

     #Creacion de la tabla inicial de la url que se le pasa y guarda nombre, uni,estado.
    def get_status(url_tabla,id,op,max_tabla,col):
          """
          :param url_tabla:  url general donde aparecen todas las titulaciones
          :param id:         id que busco para completar los datos
          :param op:         universidad donde estoy
          :param cad:        numero de tablas maxi
          :param col:        leo columna univer o columna estado
          :return:           diccionario donde se asocia el id a la info guardada
          """
          sleep_duration = 4
          dic = {}
          for i in range(1, max_tabla + 1):
              url = re.sub('codigotablas', str(i), re.sub('universidad', op, url_tabla))
              try:
                  soup = BeautifulSoup(requests.get(url, verify=False).text, 'lxml')
                  df_tabla = pd.read_html(str(soup.select('table')[0]))[0]
                  for codigo in df_tabla["Código"]:
                      try:
                          if str(codigo) == id[0:7]:
                              info = df_tabla.loc[df_tabla['Código'] == codigo][col].tolist()
                              dic[id] = info
                              return {id : info}
                      except Exception as e:
                          return {id : "No encontrado"}
              except Exception as e:
                  print(f"Error while retrieving table {i}: {e}")
          time.sleep(sleep_duration)
          return dic

    def dow_pdf(url_pdfs, id, ubicacion,df):

          """
          Descarga de url donde esta el plan de estudios
          :param id:     id que busco para completar los datos
          :param ubicacion: carpeta del proyecto donde guardo el pdf
          :param df:        guardo lo leido del pdf
          """
          sleep_duration = 2
          soup_pdfs = BeautifulSoup(requests.get(re.sub('codigoin', id, url_pdfs),verify=False).text, 'lxml')
          try:
               doc = soup_pdfs.findAll(class_='pdf')
               enlace_pdf = doc[0]['href']
               with open(ubicacion + str(id) + ".pdf", "wb") as file:
                    file.write(requests.get(enlace_pdf,verify=False).content)
               df['Texto'] = datos_web.des_text(id, ubicacion)
               time.sleep(sleep_duration)
               df['Tabla'] = datos_web.des_tabla(id, ubicacion)
               time.sleep(sleep_duration)

          except Exception as e:
               logging.info(f"pdf does not exist")
          return df

    def des_text(id, ubicacion):
         """
         :param id:     id que busco para completar los datos
         :param ubicacion: carpeta del proyecto donde guardo el pdf
         :return:           dic del texto asociado al documento id
         """
         dic={}
         total_text=[]
         try:
             pdf_file = ubicacion + str(id)+".pdf"
             pdf = pdfplumber.open(pdf_file)

             for i in range(len(pdf.pages)):
                p = pdf.pages[i]

                ts = {
                                "vertical_strategy": "explicit",
                                "horizontal_strategy": "explicit",
                                "explicit_vertical_lines": datos_generales.curves_to_edges(p.curves) + p.edges,
                                "explicit_horizontal_lines": datos_generales.curves_to_edges(p.curves) + p.edges,
                }
                bboxes = [table.bbox for table in p.find_tables(table_settings=ts)]
                def not_within_bboxes(obj):
                    def obj_in_bbox(_bbox):
                         v_mid = (obj["top"] + obj["bottom"]) / 2
                         h_mid = (obj["x0"] + obj["x1"]) / 2
                         x0, top, x1, bottom = _bbox
                         return (h_mid >=x0 and (h_mid < x1) and (v_mid > top) and (v_mid < bottom))
                    return not any(obj_in_bbox(__bbox) for __bbox in bboxes)


                page_text = p.filter(not_within_bboxes).extract_text()
                total_text.append(datos_generales.limpieza(page_text))
             info=total_text
         except Exception as e:
                 info= "No encontrado"
                 logging.info(f"pdf does not exist")
         return {id: info}

    def des_tabla(id, ubicacion):
         """
         :param id:     id que busco para completar los datos
         :param ubicacion: carpeta del proyecto donde guardo el pdf
         :return:            dic de tablas asociadas al documento id
         """
         dic={}
         lista_tabla = []
         try:
           df=read_pdf(ubicacion + str(id) + ".pdf", pages="all", multiple_tables=True, encoding='latin-1')
           for u in range(len(df)):
              lista_tabla.append(df[u].to_numpy().tolist())
         except Exception as e:
               lista_tabla = "No encontrado"
               logging.info(f"pdf does not exist")
         return {id: lista_tabla}


