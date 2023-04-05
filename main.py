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
     ubicacion = '.\\pdf_output\\'
     opciones=[]
     opciones = datos_generales.universidades(opciones)
     
     df = pd.DataFrame()
     op = '036'
     id = '25029222013071801'
     competencias=[configuracion['competencias']['url'],configuracion['competencias']['tipo']]
     principal=configuracion['principal']['url']
     cad=6
     lista = [configuracion['basico']['url'],configuracion['calendario']['url'],configuracion['modulo']['url']]
     df=datos_web.datos_web.primera_parte(lista,id,competencias,principal,op,cad,configuracion['pdf']['url'],ubicacion)
     print(df)

     """
     for op in opciones:
         op='036'
         list = datos_generales.creacion_tablas(configuracion['principal']['url'], op)
         for i in list[0]:
            i='25029222013071801'
            df_id=pd.DataFrame()
            datos_web.datos_web.tabla_inicial(configuracion['principal']['url'],i, op, list[1], df_id)
            datos_web.datos_web.datos_basicos(configuracion['basico']['url'], i, df_id)
            datos_web.datos_web.datos_competencias(configuracion['competencias']['url'], i, df_id, configuracion['competencias']['tipo'])
            print(df_id)

     
            df=pd.concat([df_id,df])
            # Guardado y leido en parquet
            df.to_parquet('data.parquet')
            print(pd.read_parquet('data.parquet'))
     """

     """
            # Guardado en una tabla de excel 
            df.to_excel('Prueba.xlsx')
     """
#print(pd.read_parquet('data.parquet').iloc[2])