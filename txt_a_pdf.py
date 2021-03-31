# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 20:06:39 2021

@author: Pablo
"""

from fpdf import FPDF
from pathlib import Path
import re

def escribe_header(pdf):
    pdf.cell(200, 10, txt = "Python Pool",  
         ln = 1, align = 'C') 
    pdf.cell(200, 10, txt = "Python Pool",  
         ln = 1, align = 'C')
    return


def guarda_pdf(pdf,path):
    pdf.output("pdf_file_name.pdf")
    


def escribe_pdf(texto,titulo):
    pdf = FPDF()  
    pdf.add_page()
    
    #Elimina caracteres que no son latin-1
    texto = re.sub(r'[^\x00-\x7f]',r'', texto)
    titulo = re.sub(r'[^\x00-\x7f]',r'', titulo)
    
    #result = re.sub(r'[^\x00-\x7f]',r'', text)
    
    #texto = regex.sub(ur'[^\p{Latin}]', u'', 'pepe')
    #titulo = regex.sub(ur'[^\p{Latin}]', u'', titulo)
    
    #Fuente
    pdf.set_font("Arial", size = 15)
    
    # Vacio
    pdf.cell(200, 40, txt = ' ', ln = 1, align = 'C') 
    
    # Titulo
    pdf.cell(200, 10, txt = titulo.replace("./out/","")+ " (resumen)", ln = 1, align = 'C') 
    
    #Espacio
    pdf.cell(200, 15, txt = '', ln = 1, align = 'C') 
    
    
    # Fuente contenido
    pdf.set_font('Arial','',11)

    # Save top coordinate
    top = pdf.y
    
    # Calculate x position of next cell
    offset = pdf.x + 40

    # Contenido    
    pdf.multi_cell(160,8,texto,0,0)
    
    # Reset y coordinate
    #pdf.y = top
    
    # Move to computed offset
    #pdf.x = offset 
    
    #pdf.multi_cell(100,10,texto,1,0)

    #Crea el pdf local
    pdf.output(titulo.replace(".pdf","")+" (resumen).pdf",'F') 
    
    #pdf.set_font("Arial", size = 10)
    #pdf.multi_cell(20,80,texto,0,'J', fill=False)
    
    return
    #return pdf.output("out/"+titulo.replace(".pdf","")+" (resumen).pdf",'F') 

 
#escribe_pdf('en un lugar de la manchaasdahdsdkfjghsñfihgsdfo ighsdñofgihsdñfgihs dñlfghsñdlfkghñsdlkghñsldkfhgñlsdkfhgñlsdkhfgñsldkhgñlsdkhfgñlksdhfgñlksdhgñlskdhfñglkshdfñ','Don Quijote')