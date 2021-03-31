# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 23:47:34 2021

Based on:
    
    bot template by magnitopic at:
    https://github.com/magnitopic/YouTubeCode/blob/master/Python/TelegramBots/TelegramBot.py

@author: Pablo
"""

# -*- coding: UTF8 -*-
import requests
import datetime

# For debugging: knowing when bot was on and making a fancy tree out of requests
import datetime
import json 

# Back end 
from funcion_resumen_texto import resumelo
from pdf_a_texto_modulo import pdf_a_texto
from txt_a_pdf import escribe_pdf
import os
#import funcion_resumen_texto as fr
import re


#%%
# Bot handling

class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)
            self.file_api_url = "https://api.telegram.org/file/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        #print('\n\nPREVIO: \n\n',resp)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update

    # New method
    def get_pdf_path(self, file_id):
        method = 'getFile'
        params = {'file_id': file_id}
        resp = requests.get(self.api_url + method, params)
        #print('\n\nPREVIO: \n\n',resp)
        result_json = resp.json()['result']
        
        if 'file_path' not in result_json:
            return None                
        else:
            return result_json['file_path']


    def get_pdf_file(self,file_path):
        #print(self.file_api_url + file_path)
        #resp = requests.get(self.file_api_url + file_path)
        return self.file_api_url + file_path


    """
    TODO
    AQUIIIIIIIIIIIIIIIIIIII
    """
    def upload_pdf(self,chat_id,pdf):
        pass
        #method = 'sendPhoto'
        #params = {'chat_id':chat_id,'file_id': file_id}
        #resp = requests.post(self.api_url + method, params)
        


    def get_pdf_file_old(self,file_path):
        #print(self.file_api_url + file_path)
        resp = requests.get(self.file_api_url + file_path)
        return resp.text
#%%
# Get information from the update
        
def get_chat_text(update):
    if 'text' not in update['message']:
        return 'No habia texto!'                
    else:
        return update['message']['text']

def get_chat_name(update):
    if 'first_name' in update['message']:
        return update['message']['chat']['first_name']
    elif 'new_chat_member' in update['message']:
        return update['message']['new_chat_member']['username']
    elif 'from' in update['message']:
        return update['message']['from']['first_name']
    else:
        return "usuario desconocido"

def get_pdf_id(update):
    if 'document' in update['message']:
        #print('hay document')
        if update['message']['document']['mime_type'] == "application/pdf":
            return update['message']['document']['file_id']
    else:
        return None
    
def get_caption(update):
    if 'caption' not in update['message']:
        return None               
    else:
        return update['message']['caption']

def get_pdf_name(update):
    if 'file_name' not in update['message']['document']:
        return None               
    else:
        return update['message']['document']['file_name']    

#%%
# Bot service        
token = 'putYourOwnBotTokenHere' #Given by botfather
resumelo_bot = BotHandler(token) #Your bot's name



def main():
    
    hora_actual = str(datetime.datetime.now())
    print("Sesion abierta a las: "+hora_actual)
   
    log = open("log.txt", "a")
    log.write("\n\nSesion nueva: "+hora_actual)
    
    new_offset = 0
    
    
    while True:
        
        """
        Keeps looking for all updates left unanswered at its url.
        As long as there are updates, it answers them
        """
        
        all_updates=resumelo_bot.get_updates(new_offset)
    
        if len(all_updates) > 0:
            for update in all_updates:
                
                """
                Code for processing each update
                """
                
                # Logs current update
                info_consulta = json.dumps(update, indent = 6)
                log.write(str(info_consulta)+"\n\n")
                print('Consulta:\n',info_consulta,'\n\n')
                
                # Gets update information
                update_id = update['update_id']
                chat_id = update['message']['chat']['id']                
                chat_text = get_chat_text(update)                
                req_chat_name = get_chat_name(update)
                pdf_id = get_pdf_id(update)
            
                # If user sent a pdf file
                if pdf_id is not None:   
                    # We get it
                    pdf_path = resumelo_bot.get_pdf_path(pdf_id)                    
                    if pdf_path is not None:                                                

                        pdf_full_path = resumelo_bot.get_pdf_file(pdf_path)        
                        idioma = get_caption(update)
                        nombre_pdf = str(get_pdf_name(update))

                        if idioma != 'eng' and idioma != 'spa':
                            idioma = 'spa' # Default language

                        
                        #Guardo una copia del pdf en el ordenador
                        print('Guardando una copia del pdf en el pc')
                        log.write('\nGuardando copia de'+pdf_full_path+' en pdfs/'+nombre_pdf+'\n')
                        copia_del_pdf = requests.get(pdf_full_path)
                        with open("pdfs/"+nombre_pdf+".pdf", 'wb') as f:
                            f.write(copia_del_pdf.content) 
                            #f.close()

                        # Log that pdf file was received                                                
                        idioma_log = 'español' if idioma == 'spa' else 'inglés'
                        print('Pasando a texto ',pdf_path,' en ',idioma_log)
                        log.write('\nPasando a texto '+pdf_path+' en '+idioma_log+'\n')

                        # Extract text with OCR and summarize it
                        resumelo_bot.send_message(chat_id, 'Extrayendo texto en '+idioma_log+' de '+nombre_pdf+'.')                        
                        texto = pdf_a_texto(pdf_full_path,idioma)

                        #Guardo una copia del texto en el ordenador
                        print('Guardando una copia del texto en el pc')
                        log.write('\nGuardando copia del texto en un txt')
                        with open("pdfs/"+nombre_pdf+" (texto).txt", 'w') as f:
                            f.writelines(texto) 
                            f.close()



                        resumelo_bot.send_message(chat_id, 'Resumiendo texto.')
                        
                        resumen = str(resumelo(texto)).replace("\n\n","\n")

                        
                        #Guardo una copia del resumen en el ordenador
                        print('Guardando una copia del resumen en el pc')
                        log.write('\nGuardando copia del resumen en un txt')
                        with open("pdfs/"+nombre_pdf+" (resumen).txt", 'w') as f:
                            f.writelines(resumen) 
                            f.close()
                        
                        
                        
                        """
                        #Mando resumen en trozos por debajo del limite de tamaño de la API de telegram
                        resumelo_bot.send_message(chat_id,'Resumen: \n')

                        def chunkstring(string, length):
                            return (string[0+i:length+i] for i in range(0, len(string), length))
                        
                        for chunk in chunkstring(resumen, 3000):
                            resumelo_bot.send_message(chat_id, str(chunk))
                            #print(chunk)
                        
                        resumelo_bot.send_message(chat_id, 'Resumen: \n\n'+resumen+'\n\n Un placer ayudarte, '+req_chat_name+'\n Algo más?')
                        
                        #resumelo_bot.send_message(chat_id, '\nUn placer ayudarte, '+req_chat_name+'\n Algo más?')
                        """

                        
                                                
                        #Devuelvo el PDF:
                        #resumelo_bot.send_message(chat_id, '\nAhora te lo paso resumido en pdf:\n\n')
                        
                        
                        
                        
                        #Genero el PDF
                        path_pdf = "./out/"+nombre_pdf
                        
                        #Elimino caracteres chungos del resumen y titulo
                        #resumen.decode('utf-8','ignore').encode("utf-8")
                        #path_pdf.decode('utf-8','ignore').encode("utf-8")
                        
                        escribe_pdf(resumen,path_pdf)
                        
                        #Abro el mismo pdf para obtener sus bytes:
                        f = open(path_pdf.replace(".pdf","")+" (resumen).pdf",'rb')
                        bytes_pdf = f.read()
                        f.close()
                        
                        #response = {'document':(f.name,bytes_pdf)}
                        #method_name = 'sendDocument'
                        url2 = "https://api.telegram.org/bot"+str(token)+"/sendDocument?chat_id=" + str(chat_id)
                    
                        #resp = requests.post(url=url2,files={'document':bytes_pdf})
                        
                        nombre_pdf = str(nombre_pdf.replace(".pdf","")+" (resumen).pdf")
                        print(nombre_pdf)
                        
                        resp = requests.post(url=url2,files={'document':(nombre_pdf,bytes_pdf)})
                        
                        
                        print('responde: ',resp)
                        
                        resumelo_bot.send_message(chat_id, '\nUn placer.\n\n')
                        
                        
                        #params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
                        #method = 'sendMessage'
                        
                        #resp = requests.post(url2 + method_name, params)
                        
                        
                        
                        #Lo guardo
                        
                        
                        #Lo subo a telegram con direccion local del pdf
                        #status = requests.post("https://api.telegram.org/bot"+str(token)+"/sendDocument?chat_id=" + str(chat_id), files=pdf_resumen)
                        
                        #status = requests.post("https://api.telegram.org/bot"+str(token)+"/sendDocument?chat_id=" + str(chat_id), files=pdf_resumen)
                        
                        #print('Al subirlo me dice: ',status,chat_id)
                        
                        #bot.sendDocument(chat_id=chat_id, document=open(file, 'rb'))
                        
                        #Lo descargo
                        
                        #TODO: Mando algo cualquiera
                        
                        
                        print('FIN')
                        new_offset = update_id + 1
                    else:
                        print('Error leyendo ruta pdf')
                        resumelo_bot.send_message(chat_id, 'Lo siento, no pude encontrar tu archivo!')
                        new_offset = update_id + 1
                     
                    # Paso a siguiente consulta
                    
                    
                # Otherwise we answer text updates    
                else:
                    
                    # Mensaje inicial
                    if chat_text == '/start':
                        resumelo_bot.send_message(chat_id, 'Encantado de verte, '+req_chat_name+'.\n¿Qué quieres que te resuma?')
                        new_offset = update_id + 1
                    
                    # Easter egg
                    elif chat_text == 'lasaña':
                        resumelo_bot.send_message(chat_id, 'Has descubierto mi easter egg, ' + req_chat_name+'.\nLa lasaña me gusta mucho')
                        new_offset = update_id + 1
                    
                    # Warning de texto breve
                    elif len(chat_text) < 20:
                        resumelo_bot.send_message(chat_id, 'Por favor, mándame algo más largo.\nNo acostumbro resumir textos de menos de 20 caracteres.')
                        new_offset = update_id + 1
                    
                    # Resumen de texto
                    else:
                        resumen = str(resumelo(chat_text))
                        
                        resumen = re.sub(r'[^\x00-\x7f]',r'', resumen)
                        #titulo = re.sub(r'[^\x00-\x7f]',r'', titulo)
    
                        
                        print('\nResumen: ',resumen)
                        log.write('\nResumen: '+resumen)
                        
                        resumelo_bot.send_message(chat_id, 'Resumen: \n\n'+resumen+'\n\n Un placer ayudarte, '+req_chat_name+'\n Algo más?')
                        new_offset = update_id + 1


if __name__ == '__main__':
    try:
        print('Iniciando resumelobot.')
        main()
    except KeyboardInterrupt:
        print('Saliendo de resumelobot')
        exit()
