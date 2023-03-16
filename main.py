import errno
import time
import configparser
import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import lxml
import urllib.request
from itertools import chain
from collections import defaultdict
import PyPDF2
import aspose.words as aw

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

def tabla_inicial(url_uni,cad,lis_titulo,lis_estado,identificadores,dic1,dic2):
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
                         #lis_titulo.append(df_tabla.loc[df_tabla['Código']==codigoentabla]['Universidad'].tolist())
                         #lis_estado.append( df_tabla.loc[df_tabla['Código'] == codigoentabla]['Estado'].tolist())

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

def creacion_tablas(url_tabla,lis_titulo,lis_estado,dic1,dic2):
     identificadores =[]
     opciones = []
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
          tabla_inicial(url_uni,cad,lis_titulo,lis_estado,creacion_identificadores(cad, url_uni),dic1,dic2)
          #identificadores += creacion_identificadores(cad,url_uni)
          print('Aqui ha pasado a la otra universidad')
     return identificadores

#2. Datos de la web importantes:

#Datos basicos

def datos_basicos(url_basicos,identificadores):
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
     return df


#Descripcion de competencias dado el tipo de competencias que quieres.Dado 1,2 o las 3 competencias va leyendo y crea columnas en funcion de ellas.


def datos_competencias(url_competencias,identificadores,df_final,list_ident):
     dic = {}
     nombre_competencia = ""
     #identificadores = creacion_tablas(url_tablas, lis_titulo, lis_uni, lis_estado)
     for tipodecomp in list_ident:
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

#3. descarga y lectura de documentos de la web

#Descargas de los planes de estudio con nombre identificador usado para la busqueda de informacion anteriormente en formado pdf
#en la ubicacion:

def descarga_pdf(url_pdfs,identificadores,ubicacion):
     for i in identificadores:
         descargas=requests.get(re.sub('codigoin',i,url_pdfs))
         soup_pdfs=BeautifulSoup(descargas.text,'lxml')
         try:
             inputTag = soup_pdfs.findAll(class_='pdf')
             enlace_pdf = inputTag[0]['href']
             with open(ubicacion+str(i)+".pdf","wb") as file:
                  file.write(requests.get(enlace_pdf).content)
                  print('descargando archivos')
         except Exception as e:
              print('aqui no existe ese archivo')



#Lee todas las paginas del  pdf que encuentra: Pero no las guarda en ninguna parte.
def paso(pdf_file):
     read_pdf =PyPDF2.PdfReader(pdf_file)
     number_of_pages =len(read_pdf.pages)
     
     #     #Aqui solo lee la primera pagina de todos los documentos pero no los ugarda
     #     page = read_pdf.pages[0]
     #     page_content = page.extract_text()
     #     print(page_content)
     
     import pdb; pdb.set_trace()
     for u in range(number_of_pages):
          page= read_pdf.pages[u]
          print(page.extract_text())

#pasa a la funcion 'paso' cada identificador con la idea de ir guardandolo (pero no se guarda completo)
def creacion_df(url_pdfs,identificadores):
     # descarga_pdf(url_pdfs,identificadores)
     for i in identificadores:
          try:
               pdf_file = "C:\\Users\\asanchezsanc\\Desktop\\personal\\Proyectonuevo\\des_pdfs\\" + str(i) + ".pdf"
               print(paso(pdf_file))
          except Exception as e:
               print('aqui no existe ese archivo')

#Pasa el pdf a un texto plano pero no entero, lo resume a una pagina.

def pasar_txt(url_pdfs,identificadores,ubicacion):
     descarga_pdf(url_pdfs, identificadores,ubicacion)
     for i in identificadores:
          try:
               pdf = aw.Document(ubicacion + str(i) + ".pdf")
               # Extrae y guarda texto en un archivo TXT
               pdf.save(ubicacion+str(i)+".txt")
          except Exception as e:
               print("No existe")
def leer_txt(url_pdfs,identificadores,ubicacion,df_final):
     pasar_txt(url_pdfs,identificadores,ubicacion)
     for i in identificadores:
          try:
               archivo = open(ubicacion+str(i)+".txt",mode='rb')
               texto = archivo.read()
               dic[i] = texto
               archivo.close()
          except Exception as e:
               print("No convertido")
     df_final['Contenido'] = dic

if __name__ == '__main__':
     #url de prueba
     url_tabla_uc3m = 'https://www.educacion.gob.es/ruct/listaestudios?codigoEstado=&consulta=1&d-1335801-p=3&ambito=&codigoTipo=&descripcionEstudio=&codigoRama=&codigoEstudio=&situacion=&buscarHistorico=N&action:listaestudios=Consultar&actual=estudios&codigoSubTipo=&codigoUniversidad=036'

     lis_titulo = []
     lis_uni = []
     lis_estado = []
     dic={}
     #df_prueba = pd.DataFrame()
     ubicacion= "C:\\Users\\asanchezsanc\\Desktop\\personal\\Proyectonuevo\\des_pdfs\\" #intentar que esta carpeta este dentro del proyecto
     """
     dic1={}
     dic2={}
     configuracion = configparser.ConfigParser()
     configuracion.read('inconfig.cfg')
     #PRUEBAS:
     identificadores = creacion_tablas(url_tablas, lis_titulo, lis_estado,dic1,dic2)
     #df_prueba['Universidad'] = dic1
     #df_prueba['Estado'] = dic2
     #print(creacion_tablas(url_tablas,lis_titulo,lis_uni,lis_estado)) #Funciona
     df_prueba=pd.concat([datos_basicos(url_basicos,identificadores),df_prueba])

     df_prueba['Universidad'] = dic1
     df_prueba['Estado'] = dic2

    # df_prueba['Universidad'] = lis_titulo
    # df_prueba['Estado'] = lis_estado
     datos_competencias(url_competencias, identificadores, df_prueba, list_ident)
     print('2')
     datos_calendarios(url_calendario, identificadores, df_prueba)
     #datos_modulo(url_modulos,identificadores, df_prueba)
     #print(df_prueba)
     #datos_metodologia(url_metodologia,identificadores, df_prueba)
     #print(df_prueba)
    # datos_sistemas(url_sistemaforma, identificadores, df_prueba)
     leer_txt(url_pdfs,identificadores,ubicacion,df_prueba)
     df_prueba.to_excel('Prueba2.xlsx')
     print('Terminado')
     identificadores = creacion_tablas(url_tablas, lis_titulo, lis_estado, dic1, dic2)
     descarga_pdf(url_pdfs, identificadores, ubicacion)
     """
     #Forma para guardar tablas y texto plano.
     import pdfplumber
     import pdfplumber

     pdf_file = "C:\\Users\\asanchezsanc\\Desktop\\personal\\Proyectonuevo\\des_pdfs\\25001202020020501.pdf"
     pdfinstance = pdfplumber.open(pdf_file)
     pdf = pdfplumber.open(pdf_file)
     pdf_text = []


     def curves_to_edges(cs):
          edges = []
          for c in cs:
               edges += pdfplumber.utils.rect_to_edges(c)
          return edges


     for i in range(len(pdf.pages)):
          p = pdf.pages[i]

          ts = {
               "vertical_strategy": "explicit",
               "horizontal_strategy": "explicit",
               "explicit_vertical_lines": curves_to_edges(p.curves) + p.edges,
               "explicit_horizontal_lines": curves_to_edges(p.curves) + p.edges,
          }
          bboxes = [table.bbox for table in p.find_tables(table_settings=ts)]


          def not_within_bboxes(obj):
               def obj_in_bbox(_bbox):
                    v_mid = (obj["top"] + obj["bottom"]) / 2
                    h_mid = (obj["x0"] + obj["x1"]) / 2
                    x0, top, x1, bottom = _bbox
                    return (h_mid >= x0 and (h_mid <= x1) and (v_mid > top) and (v_mid < bottom))

               return not any(obj_in_bbox(__bbox) for __bbox in bboxes)


          # print(page_text)
          # page_text = p.filter(not_within_bboxes).extract_text().splitlines()

          # Esto sería el texto
          page_text = p.filter(not_within_bboxes).extract_text()

          # Esto serían las tablas
          # page_table=pdf_text.extend(page_text)
          # print(p.extract_table())

#argparse