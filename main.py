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
     df=pd.DataFrame()

     #Proceso de lectura
     for op in opciones:
         if open("Titulaciones.txt", 'r').read().find("-" + op + "-") == -1:
             list = datos_generales.creacion_tablas(configuracion['principal']['url'], op)
             for i in list[0]:
                if  open("Identificadores.txt", 'r').read().find("-" + i + "-") == -1:
                     df_id = datos_web.datos_web.control(lista, i, competencias, principal, op, list[1], configuracion['pdf']['url'], ubicacion)
                     # Guarda datos en CSV:
                     df = pd.concat([df, df_id])
                     if path.exists('output.xlsx'):
                         with pd.ExcelWriter('output.xlsx', mode='a' , engine="openpyxl", if_sheet_exists="overlay") as writer:
                             df.to_excel(writer)
                     else:
                         with pd.ExcelWriter('output.xlsx', mode='w') as writer:
                             df.to_excel(writer)
                     u = open("Identificadores.txt", mode="a")
                     u.write("-" + i + "-")
                     u.close()
                else:
                    print("Id Existe")
             f = open("Titulaciones.txt",mode="a")
             f.write("-"+op+"-")
             f.close()
         else:
             print("existe")
         print(op)





     """
    
            # Guardado y leido en parquet
            df.to_parquet('data.parquet')
            print(pd.read_parquet('data.parquet'))

     """
