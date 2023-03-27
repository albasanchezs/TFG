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

def descarga_pdf(url_pdfs, identificadores, ubicacion):
    for i in identificadores:
        time.sleep(1)
        descargas = requests.get(re.sub('codigoin', i, url_pdfs))
        soup_pdfs = BeautifulSoup(descargas.text, 'lxml')
        try:
            inputTag = soup_pdfs.findAll(class_='pdf')
            enlace_pdf = inputTag[0]['href']
            with open(ubicacion + str(i) + ".pdf", "wb") as file:
                file.write(requests.get(enlace_pdf).content)
                print('descargando archivos')
        except Exception as e:
            print('aqui no existe ese archivo')

def curves_to_edges(cs):
    edges = []
    for c in cs:
        edges += pdfplumber.utils.rect_to_edges(c)
    return edges
"""
def not_within_bboxes(obj,bboxes):
    def obj_in_bbox(_bbox,bboxes):
        v_mid = (obj["top"] + obj["bottom"]) / 2
        h_mid = (obj["x0"] + obj["x1"]) / 2
        x0, top, x1, bottom = _bbox
        return (h_mid >= x0 and (h_mid <= x1) and (v_mid > top) and (v_mid < bottom))

    return not any(obj_in_bbox(__bbox) for __bbox in bboxes)
"""
def limpieza(text):
    page_text = re.sub('(http[s]?:\/\/|www\.)[^\s]+', '', text)
    page_text = re.sub("r'https://\S+|www\.\S+'", '', page_text)
    expanded_text = contractions.fix(page_text).lower()
    return expanded_text
def des_text(url_pdfs, identificadores, ubicacion,df_final):
    dic_text={}
    #dic_table={}
    descarga_pdf(url_pdfs, identificadores, ubicacion)
    for iden in identificadores:
        total_text = ""
       # clear_table = []
        try:

             pdf_file = ubicacion + str(iden)+".pdf"
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
                # print(page_text)
                # page_text = p.filter(not_within_bboxes).extract_text().splitlines()
                #x1 x0 top y bottom suele tener valores de margenes de 25
                #osea hay 25 algo entre el final de la pagina y la letra

                def not_within_bboxes(obj):
                    def obj_in_bbox(_bbox):
                        v_mid = (obj["top"] + obj["bottom"]) / 2
                        h_mid = (obj["x0"] + obj["x1"]) / 2
                        x0, top, x1, bottom = _bbox
                        return (h_mid >=x0 and (h_mid < x1) and (v_mid > top) and (v_mid < bottom))

                    return not any(obj_in_bbox(__bbox) for __bbox in bboxes)
                #Esto sería el texto
                page_text = p.filter(not_within_bboxes).extract_text()
                print(page_text)
                #total_text += limpieza(page_text)
            #    clear_table.append(p.extract_table())
             dic_text[iden]=total_text
            # clear_table.append(p.extract_table())
            # dic_table[iden] = clear_table
        except Exception as e:
            print("no encontrado")
            dic_text[iden] = "No encontrado"
            #dic_table[i] = "No hay tablas"
    df_final['Texto'] = dic_text
   # df_final['Tablas_diferente'] = dic_table


def des_tabla(url_pdfs, identificadores, ubicacion,df_final):
    dic_tabla={}
    for iden in identificadores:
        clear_text = ""
        lista_tabla = []
        try:
            df=read_pdf(ubicacion + str(iden) + ".pdf", pages="all", multiple_tables=True, encoding='latin-1')
            for u in range(len(df)):
                lista_tabla.append(df[u].to_numpy().transpose().tolist())
            dic_tabla[iden] = lista_tabla
        except Exception as e:
            print("no encontrado")
    df_final['Tabla']=dic_tabla

