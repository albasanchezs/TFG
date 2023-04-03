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
     df_final = pd.DataFrame()
     ubicacion = '.\\pdf_output\\'
     opciones=[]
     opciones = datos_generales.universidades(opciones)
     df = pd.DataFrame()

     for op in opciones:
         op='036'
         list = datos_generales.creacion_tablas(configuracion['principal']['url'], op)
         for i in list[0]:
            i='25029222013071801'
            df_id=pd.DataFrame()
            datos_generales.tabla_inicial(configuracion['principal']['url'],i, df_id, op, list[1])

            datos_web.datos_basicos(configuracion['basico']['url'], i, df_id)
            datos_web.datos_competencias(configuracion['competencias']['url'], i, df_id, configuracion['competencias']['tipo'])
        #comprobar si ya esta guardado el dato si es asi pasar al siguiente mirar el identificador


            """
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