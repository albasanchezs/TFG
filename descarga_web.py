import pandas as pd

import datos_web
import datos_generales
import main
import errno
import time
import tabula
import contractions
from tabula import read_pdf
from bs4 import BeautifulSoup
import requests
import re
import pdfplumber

# 3. descarga y lectura de documentos de la web

# Descargas de los planes de estudio con nombre identificador usado para la busqueda de informacion anteriormente en formado pdf
# en la ubicacion:

def descarga_pdf(url_pdfs, id, ubicacion,df):
    time.sleep(1)
    encontrado=0
    descargas = requests.get(re.sub('codigoin', id, url_pdfs))
    soup_pdfs = BeautifulSoup(descargas.text, 'lxml')
    try:
       doc = soup_pdfs.findAll(class_='pdf')
       enlace_pdf = doc[0]['href']
       with open(ubicacion + str(id) + ".pdf", "wb") as file:
          file.write(requests.get(enlace_pdf).content)
       des_text(url_pdfs, id, ubicacion, df)
       des_tabla(id, ubicacion, df)

    except Exception as e:
            encontrado=1


def curves_to_edges(cs):
    edges = []
    for c in cs:
        edges += pdfplumber.utils.rect_to_edges(c)
    return edges


def limpieza(text):
    page_text = re.sub('(http[s]?:\/\/|www\.)[^\s]+', '', text)
    page_text = re.sub("r'https://\S+|www\.\S+'", '', page_text)
    expanded_text = contractions.fix(page_text).lower()
    return expanded_text

def des_text(url_pdfs, id, ubicacion,df):
    dic={}
    total_text=""
    try:
        pdf_file = ubicacion + str(id)+".pdf"
        pdfinstance = pdfplumber.open(pdf_file)
        pdf = pdfplumber.open(pdf_file)

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
                    return (h_mid >=x0 and (h_mid < x1) and (v_mid > top) and (v_mid < bottom))
               return not any(obj_in_bbox(__bbox) for __bbox in bboxes)
           #Esto sería el texto
           page_text = p.filter(not_within_bboxes).extract_text()
           total_text += limpieza(page_text)
        dic[id]=total_text
    except Exception as e:
            dic[id] = "No encontrado"

    df['Texto']=dic
def des_tabla(id, ubicacion,df):
    dic={}
    lista_tabla = []
    try:
      df=read_pdf(ubicacion + str(id) + ".pdf", pages="all", multiple_tables=True, encoding='latin-1')
      for u in range(len(df)):
         lista_tabla.append(df[u].to_numpy().transpose().tolist())
         dic[id] = lista_tabla
    except Exception as e:
          dic[id] = "No encontrado"
    df['Tabla']=dic
