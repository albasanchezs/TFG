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
import os.path as path
import os
import ssl
import stat
import subprocess
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import pyarrow.parquet as pq
import pyarrow as pa

if __name__ == '__main__':

     configuracion = configparser.ConfigParser()
     configuracion.read('inconfig.cfg')
     ubicacion = '.\\pdf_output\\'
     opciones=[]


     #Inicializacion
     opciones = datos_generales.universidades(opciones)
     competencias=[configuracion['competencias']['url'],configuracion['competencias']['tipo']]
     principal=configuracion['principal']['url']
     lista = [configuracion['basico']['url'],configuracion['calendario']['url'],configuracion['modulo']['url'],configuracion['metodologia']['url'],configuracion['sistemaforma']['url']]

     #Proceso de lectura
     for op in opciones:
          if open("Titulaciones2.txt", 'r').read().find("-" + op + "-") == -1:
               list = datos_generales.creacion_tablas(configuracion['principal']['url'], op)
               for i in list[0]:
                    if open("Identificadores2.txt", 'r').read().find("-" + i + "-") == -1:

                         df_id = datos_web.datos_web.control(lista, i, competencias, principal, op, list[1],
                                                                  configuracion['pdf']['url'], ubicacion)
                         
                         print(df_id)
                         if path.exists('Data.parquet'):

                              df = pd.read_parquet('Data.parquet')
                              # concatenar:
                              dfs = [df, df_id]
                              df_concat = pd.concat(dfs,ignore_index=True)
                              df_concat.astype(str).to_parquet('Data.parquet')
                         else:
                              df_id.astype(str).to_parquet('Data.parquet')

                         u = open("Identificadores2.txt", mode="a")
                         u.write("-" + i + "-")
                         u.close()
                    else:
                         print("Id Existe")
               f = open("Titulaciones2.txt", mode="a")
               f.write("-" + op + "-")
               f.close()
          else:
               print("existe")
          print(op)

     #print(pd.read_parquet('data.parquet'))
