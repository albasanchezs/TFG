import errno
import time
import configparser
import contractions
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
     dic={}
     df_final = pd.DataFrame()
     ubicacion = '.\\pdf_output\\'
     opciones=[]
     opciones = datos_generales.universidades(opciones)
     print(opciones)
     #for op in opciones:
     #     df_uni = pd.DataFrame()
     #     identificadores = datos_generales.creacion_tablas(configuracion['principal']['url'],df_uni,op)
     """
          datos_web.datos_basicos(configuracion['basico']['url'], identificadores,df_uni)
          print('2')
          time.sleep(1)
          datos_web.datos_competencias(configuracion['competencias']['url'], identificadores, df_uni, configuracion['competencias']['tipo'])
          print('3')
          time.sleep(1)
          datos_web.datos_calendarios(configuracion['calendario']['url'], identificadores, df_uni)
          print('4')
          time.sleep(1)
          datos_web.datos_modulo(configuracion['modulo']['url'], identificadores, df_uni)
          print('5')
          time.sleep(1)
          datos_web.datos_metodologia(configuracion['metodologia']['url'], identificadores, df_uni)
          print('6')
          time.sleep(1)
          datos_web.datos_sistemas(configuracion['sistemaforma']['url'], identificadores, df_uni)
          print('7')
          time.sleep(1)
          descarga_web.des_text(configuracion['pdf']['url'], identificadores, ubicacion, df_uni)
          print('8')
          descarga_web.des_tabla(configuracion['pdf']['url'], identificadores, ubicacion, df_uni)
          
          df_final=pd.concat([df_final,df_uni])
          # Guardado y leido en parquet

          df_final.to_parquet('Data.parquet')
          print(pd.read_parquet('Data.parquet'))
          time.sleep(4)
          print("---------------------------")
          """

     """
     #PRUEBAS
     #identificadores = ['25000482019030501']
     #identificadores = '25000482019030501'
     #descarga_web.des_text(configuracion['pdf']['url'], identificadores, ubicacion, df_prueba)
     #print(df_prueba['Texto'].iloc[0])

     #Guardado y leido en parquet
     df_prueba.to_parquet('data.parquet')
     print(pd.read_parquet('data.parquet'))


     #Guardado en una tabla de excel 
     df_prueba.to_excel('Prueba2.xlsx')

     """
#argparse
# ir metiendo cada universidad una vez hace la lectura
