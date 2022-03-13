
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import pyautogui, sys
from xlsxwriter import Workbook
from selenium.webdriver.common.by import By


def DataCSV(msg_part_1 , msg_part_2, df ):
    index_a = msg_part_1.find(']')
    index_b = msg_part_1.find(',')

    msg_registro = [ ( msg_part_1[index_a+2:] , msg_part_1[index_b+2:index_a] , msg_part_1[1:index_b] , msg_part_2 ) ]
    dfNew=pd.DataFrame(msg_registro, columns = ['Enviado por ...' , 'Fecha', 'Hora','Mensaje'])
    df = pd.concat([df, dfNew])
    #df=df.append(dfNew,ignore_index=True)
    
    return df



def ScrollMaximo(driver):
    primer_texto = "Los mensajes están cifrados de extremo a extremo. Nadie fuera de este chat, ni siquiera WhatsApp, puede leerlos ni escucharlos. Haz clic para obtener más información."
    list_sistema = []
    cont = 1
    while ( not(primer_texto in list_sistema) ):
        pyautogui.scroll(+10000)
        
        cont = cont + 1
        msgs_sistema = WebDriverWait(driver,120).until(lambda driver:driver.find_elements(by=By.XPATH, value='.//div[@aria-label="Lista de mensajes. Presiona la tecla de flecha hacia la derecha en un mensaje para abrir su menú contextual."]//div[@class="_2wUmf V-zSs focusable-list-item"]'))
        for msg_sistema in msgs_sistema:
            try:
                msg = msg_sistema.find_element(by=By.XPATH, value='.//span[@dir="ltr"]').text
                if ( not(msg in list_sistema) ):
                    list_sistema.append(msg)
            except:
                pass
    
    print("Hemos hecho un scroll . . . " , cont)
    #print("#################\n")
    #print(list_sistema)
    #print("\n#################\n")

def ScrapearMsg(driver , list_msg ,contacto ):
    msgs_contac = WebDriverWait(driver,120).until(lambda driver:driver.find_elements(by=By.XPATH, value='.//div[@aria-label="Lista de mensajes. Presiona la tecla de flecha hacia la derecha en un mensaje para abrir su menú contextual."]//div[@tabindex="-1"]'))
    #msgs_contac = WebDriverWait(driver,120).until(lambda driver:driver.find_elements_by_xpath('.//div[@aria-label="Lista de mensajes. Presiona la tecla de flecha hacia la derecha en un mensaje para abrir su menú contextual."]//div[@tabindex="-1"]'))

    data = pd.DataFrame()
    for msg in msgs_contac:
        try:  
            try :
                #msg2 = msg.find_element_by_xpath('.//div[@class="copyable-text"]')
                #msg3 = msg2.get_attribute("data-pre-plain-text")
                #msg1 = msg.find_element_by_xpath('.//span[@dir="ltr"]').text

                msg2 = msg.find_element(by=By.XPATH, value='.//div[@class="copyable-text"]')
                msg3 = msg2.get_attribute("data-pre-plain-text")
                msg1 = msg.find_element(by=By.XPATH, value='.//span[@dir="ltr"]').text


                list_msg.append(msg3 + ' ---> '+ msg1)
                data = DataCSV(msg3 , msg1, data )
            except:
                try :
                    #msg2 = msg.find_element_by_xpath('.//div[@class="_2jGOb copyable-text"]')
                    #msg3 = msg2.get_attribute("data-pre-plain-text")
                    #msg1 = msg.find_element_by_xpath('.//span[@dir="ltr"]').text

                    msg2 = msg.find_element(by=By.XPATH, value='.//div[@class="_2jGOb copyable-text"]')
                    msg3 = msg2.get_attribute("data-pre-plain-text")
                    msg1 = msg.find_element(by=By.XPATH, value='.//span[@dir="ltr"]').text


                    list_msg.append(msg3 + ' ---> '+ msg1)
                    data = DataCSV(msg3 , msg1, data )
                except:
                    #msg1 = msg.find_element_by_xpath('.//span[@dir="ltr"]').text
                    #msg4 = msg.find_element_by_xpath('.//div[@class="Nm1g1 _22AX6"]//div')
                    #msg5 = msg4.get_attribute("data-pre-plain-text")

                    msg1 = msg.find_element(by=By.XPATH, value='.//span[@dir="ltr"]').text
                    msg4 = msg.find_element(by=By.XPATH, value='.//div[@class="Nm1g1 _22AX6"]//div')
                    msg5 = msg4.get_attribute("data-pre-plain-text")

                    
                    list_msg.append(msg5 + ' ---> '+ msg1)
                    data = DataCSV(msg5 , msg1, data )
        except:
            pass

    #print("hola mundo\n")
    print(data)


def main():

    driver = webdriver.Chrome('C:\driver_Chrome\chromedriver.exe')
    driver.get('https://web.whatsapp.com/')

    time.sleep(20)

    contactos = []
    cont = 0
    x = 250
    y = 400
    maximo = 1

    data_final = [[] for i in range(maximo)]

    while ( len(contactos) < maximo ):

        inicio = time.time()

        t = 0.0001
        pyautogui.click(x, y)
        time.sleep(t)

        #nombre_contac = WebDriverWait(driver,120).until(lambda driver:driver.find_elements_by_xpath('.//div[@class="_21nHd"]'))
        nombre_contac = WebDriverWait(driver,120).until(lambda driver:driver.find_elements(by=By.XPATH, value='.//div[@class="_21nHd"]'))
        #contacto = nombre_contac[0].find_element_by_xpath('.//span[@dir="auto"]').text
        contacto = nombre_contac[0].find_element(by=By.XPATH, value='.//span[@dir="auto"]').text
        
        if ( not(contacto in contactos)):
            print("\n##########------------##########")
            print(contacto,'  ',cont)
            
            contactos.append(contacto)

            pyautogui.moveTo(x+300, y,0.5)

            ScrollMaximo(driver)

            ScrapearMsg(driver , data_final[cont],contacto)

            cont = cont +1
                
            pyautogui.moveTo(x,y,0.5)
            pyautogui.scroll(-60)
        
        else :
            time.sleep(t)
            y = y + 10
            pyautogui.scroll(-20)

            if ( y > 430 ):
                #pyautogui.scroll(-80)
                if (  (len(contactos) > maximo-5) and ( len(contactos) < maximo ) ):
                    y = y + 20
                else:
                    y = 400

        fin = time.time()

        print("El tiempo de este contacto es : ",fin-inicio,"seg ")
        print("\n##########------------##########")

        time.sleep(1)
        
    driver.close()


main()