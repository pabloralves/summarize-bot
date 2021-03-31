# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 12:56:35 2021


Entrenamiento de idiomas adicionales va en:
C:\Program Files\Tesseract-OCR\tessdata
Por ahora hay eng y spa

@author: Pablo
"""

import pdf2image
import pytesseract
from pytesseract import Output, TesseractError
import os


def delete_ppms(PATH):
  for file in os.listdir(PATH):
    if '.ppm' in file or '.DS_Store' in file:
      try:
          print('Eliminando',PATH + file)
          os.remove(PATH + file)
      except FileNotFoundError:
          print('Errpr eliminando')
          pass


def pdf_a_texto(pdf_original,lang_pdf):
    
    print('Convirtiendo pdf ',pdf_original)
    images = pdf2image.convert_from_path(pdf_original)
    print('Debug: Hay',len(images),' imágenes, una por página')

    #lang_pdf = 'eng' #TODO: Detectar idioma
    texto = ""

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


    for pagina in range(0,len(images)):
        print('Debug: pag',pagina)
        texto_pagina = pytesseract.image_to_string(images[pagina], lang=lang_pdf)
        texto += texto_pagina
        
    print('Debug: NO Limpiando archivos locales del servidor')
    #delete_ppms(PATH)
    print('Debug: Retornando texto')
    return texto


def pdf_a_texto_old(PATH,nombre_pdf,lang_pdf):
    
    pdf_path = PATH + nombre_pdf
    print('Debug: Convirtiendo ',pdf_path,' a imagenes')
    
    images = pdf2image.convert_from_path(pdf_path)
    print('Debug: Hay',len(images),' imágenes, una por página')

    #lang_pdf = 'eng' #TODO: Detectar idioma
    texto = ""

    for pagina in range(0,len(images)):
        print('Debug: pag',pagina)
        texto_pagina = pytesseract.image_to_string(images[pagina], lang=lang_pdf)
        texto += texto_pagina
        
    print('Debug: Limpiando archivos locales del servidor')
    delete_ppms(PATH)
    print('Debug: Retornando texto')
    return texto
