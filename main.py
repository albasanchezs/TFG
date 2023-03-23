import errno
import time
import configparser
from bs4 import BeautifulSoup
import requests
import numpy as np
import re
import lxml
import pandas as pd
import pdfplumber
import pyarrow
import fastparquet
import tabula as tb
from tabula import read_pdf
import datos_web
import datos_generales
import descarga_web
import main

if __name__ == '__main__':
     configuracion = configparser.ConfigParser()
     configuracion.read('inconfig.cfg')
     #url de prueba
     url_tabla_uc3m = 'https://www.educacion.gob.es/ruct/listaestudios?codigoEstado=&consulta=1&d-1335801-p=3&ambito=&codigoTipo=&descripcionEstudio=&codigoRama=&codigoEstudio=&situacion=&buscarHistorico=N&action:listaestudios=Consultar&actual=estudios&codigoSubTipo=&codigoUniversidad=036'
     lis_titulo = []
     lis_uni = []
     lis_estado = []
     dic={}
     df_prueba = pd.DataFrame()
     ubicacion= "C:\\Users\\asanchezsanc\\Desktop\\personal\\Proyectonuevo\\des_pdfs\\" #intentar que esta carpeta este dentro del proyecto
    # ubicacion = '.\\pdf_output\\'
     #identificadores = datos_generales.creacion_tablas(configuracion['principal']['url'],df_prueba)
     #datos_web.datos_basicos(configuracion['basico']['url'], identificadores,df_prueba)
     #datos_web.datos_competencias(configuracion['competencias']['url'], identificadores, df_prueba, configuracion['competencias']['tipo'])
     #datos_web.datos_calendarios(configuracion['calendario']['url'], identificadores, df_prueba)
     #datos_web.datos_modulo(configuracion['modulo']['url'], identificadores, df_prueba)
     #datos_web.datos_metodologia(configuracion['metodologia']['url'], identificadores, df_prueba)
     #datos_web.datos_sistemas(configuracion['sistemaforma']['url'], identificadores, df_prueba)
     #descarga_web.des_tabla(configuracion['pdf']['url'], identificadores, ubicacion, df_prueba)
     identificadores = ['25000482019030501', '25001552019102501', '25000452019040301', '25000482019030501']
     descarga_web.des_text(configuracion['pdf']['url'], identificadores, ubicacion, df_prueba)
     print(df_prueba['Texto'].iloc[0])

     """
     iden='25029222013071801'
     lista=[]
     dic={}
     df_inter=pd.DataFrame()
     df = read_pdf(ubicacion + str(iden) + ".pdf", pages="all", multiple_tables=True, encoding='latin-1')
     for u in range(len(df)):
          lista.append(df[u].to_numpy().transpose().tolist())
     print(lista)
     dic[iden]=lista
     df_prueba['Tabla']=dic
     #df_arr=[df_prueba.values for df_prueba in df]
     print(df_prueba)
     """
     """
     #Guardado y leido en parquet
     df_prueba.to_parquet('data.parquet')
     print(pd.read_parquet('data.parquet'))
     """
     """
     #Guardado en una tabla de excel 
     df_prueba.to_excel('Prueba2.xlsx')
     """

#argparse
