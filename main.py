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
import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook



if __name__ == '__main__':

     configuracion = configparser.ConfigParser()
     configuracion.read('inconfig.cfg')
     ubicacion = '.\\pdf_output\\'
     opciones=[]
     #opciones = datos_generales.universidades(opciones)

     op = '036'
     id='25029222013071801'

     competencias=[configuracion['competencias']['url'],configuracion['competencias']['tipo']]
     principal=configuracion['principal']['url']
     cad=6
     lista = [configuracion['basico']['url'],configuracion['calendario']['url'],configuracion['modulo']['url']]
     df=pd.DataFrame()

     for op in opciones:
         list = datos_generales.creacion_tablas(configuracion['principal']['url'], op)
         for i in list[0]:
            df_id=pd.DataFrame()
            df = datos_web.datos_web.control(lista, df_id, competencias, principal, op, list[1], configuracion['pdf']['url'], ubicacion)
            print(df_id)
            df=pd.concat([df_id,df])
            # Guardado y leido en parquet
            df.to_parquet('data.parquet')
            print(pd.read_parquet('data.parquet'))


     """
            # Guardado en una tabla de excel 
            df.to_excel('Prueba.xlsx')
     """
#print(pd.read_parquet('data.parquet').iloc[2])