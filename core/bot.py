from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import datetime


driver = webdriver.Firefox()
time.sleep(3)
dates =[]
while True:
    time.sleep(3)
    driver.get("https://resultadosemponto.com/")
    openTable = driver.find_element_by_xpath("//h2[@class='entry-title']")
    openTable.click()
    url = driver.current_url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    # TABELA DE DADOS
    tables=soup.find('table')
    # DADOS
    data = tables.text.split()
    # METADADO
    h1=soup.find('h1')
    p=soup.find('p')
    # COLETANDO HORÁRIO E DATA DO JOGO
    date_time_str = h1.text.split()[-1]
    date_time_obj = datetime.datetime.strptime(date_time_str+" "+p.text.split()[-1], '%d/%m/%Y %H:%M')
    if len(dates) == 0:
        print("apendando primeira data")
        dates.append(date_time_obj)
        # COLETANDO NOME DA LOJA
        name = p.text.split()[0]
        # COLETANDO O DADO: 
        n=3
        premio=[]
        resultado=[]
        grupo=[]
        animais=[]
        while n < len(data) - 3:
            premio.append(data[n])
            resultado.append(data[n+1])
            grupo.append(data[n+2])
            animais.append(data[n+3])
            n+=4
        dataframe = pd.DataFrame({
            "DATA": [date_time_obj for x in range(len(premio))],
            "ID": [name for x in range(len(premio))],
            "PREMIO": premio, "RESULTADO": resultado, "GRUPO": grupo, "ANIMAL": animais
        })
        time.sleep(60)
        print(dataframe)
    elif date_time_obj < dates[-1]:  
        print("PEGANDO DADO...")
        print("HORA: {}".format(date_time_obj))  
        dates.append(date_time_obj)
        # COLETANDO NOME DA LOJA
        name = p.text.split()[0]
        # COLETANDO O DADO: 
        n=3
        premio=[]
        resultado=[]
        grupo=[]
        animais=[]
        while n < len(data) - 3:
            premio.append(data[n])
            resultado.append(data[n+1])
            grupo.append(data[n+2])
            animais.append(data[n+3])
            n+=4
        dataframe = pd.DataFrame({
            "DATA": [date_time_obj for x in range(len(premio))],
            "ID": [name for x in range(len(premio))],
            "PREMIO": premio, "RESULTADO": resultado, "GRUPO": grupo, "ANIMAL": animais
        })
        time.sleep(60)
        print(dataframe)
    else: 
        print("não há atualizações")
        time.sleep(60)

        pass