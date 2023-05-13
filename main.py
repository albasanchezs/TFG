import errno
import time
import configparser
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import pyarrow
import fastparquet
import tabula as tb
from tabula import read_pdf
import datos_web
import datos_generales
import openpyxl
import os.path as path
import os
import logging

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import pyarrow.parquet as pq
import pyarrow as pa

if __name__ == '__main__':

     configuracion = configparser.ConfigParser()
     configuracion.read('inconfig.cfg')
     ubicacion = '.\\pdf_output\\'
     logging.basicConfig(filename='logfile.log', level=logging.INFO)

     #Initialization
     opciones = datos_generales.universidades([])
     competencias = [configuracion['competencias']['url'],configuracion['competencias']['tipo']]
     principal = configuracion['principal']['url']
     lista = [configuracion['basico']['url'],configuracion['calendario']['url'],configuracion['modulo']['url'],configuracion['metodologia']['url'],configuracion['sistemaforma']['url']]
    
        
     # Read existing data from files
     with open("Titulaciones2.txt", 'r') as f:
          titulaciones = f.read()
     with open("Identificadores2.txt", 'r') as f:
          identificadores = f.read()

     # Processing data
     for op in opciones:
          if f"-{op}-" not in titulaciones:
               list = datos_generales.creacion_tablas(configuracion['principal']['url'], op)
               for i in list[0]:
                    if f"-{i}-" not in identificadores:
                         df_id = datos_web.datos_web.control(lista, i, competencias, principal, op, list[1],
                                                        configuracion['pdf']['url'], ubicacion)

                         print(df_id)

                         if path.exists('Data_example.parquet'):
                             df = pd.read_parquet('Data_example.parquet')
                             # concatenar:
                             dfs = [df, df_id]
                             df_concat = pd.concat(dfs,ignore_index=True)
                             df_concat = df_concat.rename_axis('id').reset_index()
                             df_concat.set_index('id', inplace=True)
                             df_concat.astype(str).to_parquet('Data_example.parquet')
                         else:
                             df_id.astype(str).to_parquet('Data_example.parquet')

                         with open("Identificadores2.txt", mode="a") as f:
                            f.write(f"-{i}-")
                    else:
                         logging.info(f"Identifier {i} already exists in file Identificadores2.txt for {op}")
               with open("Titulaciones2.txt", mode="a") as f:
                  f.write(f"-{op}-")
                  logging.info(f"Added title {op} to file Titulaciones2.txt")
          else:
               logging.info(f"Title {op} already exists in file Titulaciones2.txt")
          print(op)

     #df=pd.read_parquet('Data_example.parquet')
     #print(df)



