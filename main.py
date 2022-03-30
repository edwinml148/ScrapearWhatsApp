
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import pyautogui, sys
from selenium.webdriver.common.by import By
import tkinter as tk
import os
import sys


def DataCSV(msg_part_1 , msg_part_2, df ):
    index_a = msg_part_1.find(']')
    index_b = msg_part_1.find(',')

    msg_registro = [ ( msg_part_1[index_a+2:] , msg_part_1[index_b+2:index_a] , msg_part_1[1:index_b] , msg_part_2 ) ]
    dfNew=pd.DataFrame(msg_registro, columns = ['Enviado por ...' , 'Fecha', 'Hora','Mensaje'])
    df = pd.concat([df, dfNew])
    
    return df

def ScrollMaximo(driver):
    primer_texto = "Los mensajes están cifrados de extremo a extremo. Nadie fuera de este chat, ni siquiera WhatsApp, puede leerlos ni escucharlos. Haz clic para obtener más información."
    list_sistema = []
    cont = 1
    while ( not(primer_texto in list_sistema) ):
        pyautogui.scroll(+500)
        time.sleep(0.01)
        
        cont = cont + 1
        msgs_sistema = WebDriverWait(driver,120).until(lambda driver:driver.find_elements(by=By.XPATH, value='.//div[@aria-label="Lista de mensajes. Presiona la tecla de flecha hacia la derecha en un mensaje para abrir su menú contextual."]//div[@class="_2wUmf V-zSs focusable-list-item"]'))
        for msg_sistema in msgs_sistema:
            try:
                msg = msg_sistema.find_element(by=By.XPATH, value='.//span[@dir="ltr"]').text
                if ( not(msg in list_sistema) ):
                    list_sistema.append(msg)
            except:
                pass

def ScrapearMsg(driver , contacto ):
    msgs_contac = WebDriverWait(driver,120).until(lambda driver:driver.find_elements(by=By.XPATH, value='.//div[@aria-label="Lista de mensajes. Presiona la tecla de flecha hacia la derecha en un mensaje para abrir su menú contextual."]//div[@tabindex="-1"]'))

    data = pd.DataFrame()
    for msg in msgs_contac:
        try:

            try :

                msg2 = msg.find_element(by=By.XPATH, value='.//div[@class="copyable-text"]')
                msg3 = msg2.get_attribute("data-pre-plain-text")
                msg1 = msg.find_element(by=By.XPATH, value='.//span[@dir="ltr"]').text
                data = DataCSV(msg3 , msg1, data )
            except:

                try :

                    msg2 = msg.find_element(by=By.XPATH, value='.//div[@class="_2jGOb copyable-text"]')
                    msg3 = msg2.get_attribute("data-pre-plain-text")
                    msg1 = msg.find_element(by=By.XPATH, value='.//span[@dir="ltr"]').text
                    data = DataCSV(msg3 , msg1, data )

                except:

                    msg1 = msg.find_element(by=By.XPATH, value='.//span[@dir="ltr"]').text
                    msg4 = msg.find_element(by=By.XPATH, value='.//div[@class="Nm1g1 _22AX6"]//div')
                    msg5 = msg4.get_attribute("data-pre-plain-text")
                    data = DataCSV(msg5 , msg1, data )
        except:
            pass

    try:
        os.chdir(en1.get())
        print("--> Generando el archivo . . .")
        data.to_csv( (en1.get()+'\{}.csv').format(contacto) , sep=';' , encoding='utf-8-sig' )
    except:
        print("--> La ruta output es incorrecta ...")

def ScrapearWhatsApp():
    #print("hola mudno .. .... ",ruta)
    try:
        driver = webdriver.Chrome(en0.get())
        driver.get('https://web.whatsapp.com/')
    except:
        print("--> Error en la ruta del controlador")
        pass
    
    
    time.sleep(30)

    contactos = []
    cont = 0
    x = 250
    y = 400

    v_opt = v.get() 
    if ( v_opt == '2' ):
        cantidad_contactos = int(en2.get())
    else:
        cantidad_contactos_web = WebDriverWait(driver,120).until(lambda driver:driver.find_elements(by=By.XPATH, value='.//div[@aria-label="Lista de chats"]'))
        cantidad_contactos = int(cantidad_contactos_web[0].get_attribute("aria-rowcount"))

    print( "Cantidad de Contactos : " , cantidad_contactos)

    while ( len(contactos) < cantidad_contactos ):
        t = 0.0001
        pyautogui.click(x, y)
        time.sleep(t)

        nombre_contac = WebDriverWait(driver,120).until(lambda driver:driver.find_elements(by=By.XPATH, value='.//div[@class="_21nHd"]'))
        contacto = nombre_contac[0].find_element(by=By.XPATH, value='.//span[@dir="auto"]').text
        
        if ( not(contacto in contactos)):
            print("\n##########------------##########")
            print(contacto,'  ',cont)
            
            contactos.append(contacto)

            pyautogui.moveTo(x+300, y,0.5)

            ScrollMaximo(driver)
            print("--> Scrapeando . . .")
            ScrapearMsg(driver , contacto)
            
            """
            try :
                texto=tex.get()
                print("hola1")
                texto.insert(tk.INSERT, "Hello.....")
                print("hola2")
                texto.pack(fill='x', expand=True)
                print("hola3")
            except:
                print("hya error aca . . .")
            """
            #try :
            #    tex.insert(tk.INSERT, "Hello.....")
            #    tex.pack(fill='x', expand=True)
            #except:
            #    print("hya error aca . . .")
            

            cont = cont +1
                
            pyautogui.moveTo(x,y,0.5)
            pyautogui.scroll(-60)
        
        else :
            time.sleep(t)
            y = y + 10
            pyautogui.scroll(-20)

            if ( y > 430 ):
                if (  (len(contactos) > cantidad_contactos-5) and ( len(contactos) < cantidad_contactos ) ):
                    y = y + 20
                else:
                    y = 400

        time.sleep(1)
        
    driver.close()

def LogicaRutaControlador():
    entrada0 = en0.get()
    try:
        driver = webdriver.Chrome(entrada0)
        lb1_1.configure(text='Ruta valida')
    except:
        lb1_1.configure(bg='red' ,text='Ruta invalida')
    
    lb1_1.pack(fill='x', expand=True)

def LogicaOptionOutput():
    entrada1 = en1.get()

    if ( os.path.isdir(entrada1) ):
        lb2_1.configure(text='Ruta valida')
    else:
        lb2_1.configure(bg='red' ,text='Ruta invalida')

    lb2_1.pack(fill='x', expand=True)

def LogicaOptionScraper():
    v_opt = v.get()

    if ( v_opt == '2' ):
        lb4.pack(fill='x', expand=True)
        en2.pack(fill='x', expand=True)
        en2.focus()
    else:
        lb4.pack_forget()
        en2.pack_forget()
        en2.configure(background='steelblue')


class StdOutRedirect:
    def __init__(self,  text: tk.Text) -> None:
        self._text = text

    def write(self,  out: str) -> None:
        self._text.insert(tk.END,  out)

class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent,  *args, **kwargs)
        self.stdout_text = tk.Text(self,  bg="black",  fg="#38B179",  font=("Helvetica", 8) , height=10, width=60)
        self.stdout_text.pack(padx=10, pady=10, fill='x', expand=True)
        sys.stdout = StdOutRedirect(self.stdout_text)



if __name__ == "__main__":
    root = tk.Tk(className='Scrapeando el WhatsApp')
    root.geometry('400x700')
    #root.resizable(False, False)
    root.configure(background='steelblue')

    ####### TITULO #######
    lb0 = tk.Label(root, text='!! Scrapea tu WhatsApp !!', bg='black', fg='white')
    lb0.pack(padx=10, pady=10, ipadx=10, ipady=5)
    ####### TITULO #######


    ####### BLOKE RUTA DEL CONTROLADOR #######
    fr0 = tk.Frame(root)
    fr0.pack(padx=10, pady=10, fill='x', expand=True)
    
    lb1_0 = tk.Label(fr0, text='Ruta driver :', bg='black', fg='white')
    lb1_0.pack(fill='x', expand=True)
    
    ############# ---------- #############
    fr00 = tk.Frame(fr0)
    fr00.pack(padx=10, pady=10, fill='x', expand=True)
    
    en0 = tk.Entry(fr00)
    en0.pack(fill='x', expand=True, side = tk.LEFT)
    en0.focus()
    boton_0 = tk.Button( fr00, text='Validar', fg="Black", command=LogicaRutaControlador)  
    boton_0.pack(fill='x', expand=True , side=tk.LEFT)
    ############# ---------- #############

    lb1_1 = tk.Label(fr0, bg='green', fg='white')
    ####### BLOKE RUTA DEL CONTROLADOR #######



    ####### BLOKE RUTA OUPUT #######
    fr1 = tk.Frame(root)
    fr1.pack(padx=10, pady=10, fill='x', expand=True)

    lb2_0 = tk.Label(fr1, text='Ruta Ouput :', bg='black', fg='white')
    lb2_0.pack(fill='x', expand=True)

    ############# ---------- #############
    fr11 = tk.Frame(fr1)
    fr11.pack(padx=10, pady=10, fill='x', expand=True)
    
    en1 = tk.Entry(fr11)
    en1.pack(fill='x', expand=True, side = tk.LEFT)
    en1.focus()
    boton_1 = tk.Button( fr11, text='Validar', fg="Black", command=LogicaOptionOutput)  
    boton_1.pack(fill='x', expand=True , side=tk.LEFT)
    ############# ---------- #############

    lb2_1 = tk.Label(fr1, bg='green', fg='white')
    ####### BLOKE RUTA OUPUT #######


    ####### BLOKE DE OPCION MULTIPLE #######
    fr2 = tk.Frame(root)
    fr2.pack(padx=10, pady=10, fill='x', expand=True)
    
    lb3 = tk.Label(fr2, text='Opcion de Scrapear :', bg='black', fg='white')
    lb3.pack(fill='x', expand=True)
    
    v = tk.StringVar(fr2, "0")
    opcion = tk.Radiobutton(fr2,text='Todos los chats', variable = v, value = 1, command=LogicaOptionScraper )
    opcion.pack(fill='x', expand=True , side = tk.LEFT)
    opcion = tk.Radiobutton(fr2,text='Otros', variable = v, value = 2, command=LogicaOptionScraper)
    opcion.pack(fill='x', expand=True , side = tk.LEFT)
    ####### BLOKE DE OPCION MULTIPLE #######



    #######  BLOKE DE CANTIDAD DE CONTACTOS #######
    fr3 = tk.Frame(root)
    fr3.pack(padx=10, pady=10, fill='x', expand=True)
    
    lb4 = tk.Label(fr3, text='Cantidad de contactos :', bg='black', fg='white')
    
    en2 = tk.Entry(fr3)
    #######  BLOKE DE CANTIDAD DE CONTACTOS #######


    #######  BOTON DE SCRAPPER #######
    fr4 = tk.Frame(root)
    fr4.pack(padx=10, pady=10, fill='x', expand=True)

    boton = tk.Button( fr4, text='¡ Empezamos !', bg='white', fg='black', command=ScrapearWhatsApp)  
    boton.pack(fill='x', expand=True)
    #######  BOTON DE SCRAPPER #######


    #######  SALIDA DE COMPILACION #######
    fr5 = tk.Frame(root)
    fr5.pack(padx=10, pady=10, fill='x', expand=True)
    App(fr5).pack(padx=10, pady=10, fill='x', expand=True)
    #######  SALIDA DE COMPILACION #######
    
    root.mainloop()



    