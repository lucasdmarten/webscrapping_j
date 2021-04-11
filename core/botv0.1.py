from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import datetime
from selenium.webdriver.firefox.options import Options
import os

options = Options()
options.add_argument('--headless')

def get_data(articles, page):
    dfs=[]
    
    for j in range(len(articles)):
        
        # METADATA
        info = articles[j].find_all('h2', {'class':'entry-title'})[0].text.split()
        name = info[3]
        hour = info[4][:-2]
        date = info[-1]
        objDate = datetime.datetime.strptime( (date + " " + hour), '%d/%m/%Y %H:%M' )        

        # DATA
        tds = articles[j].find_all('td')
        keys = ['1°','2°','3°','4°','5°','6°','7°']
        PREMIO = []
        RESULTADO = []
        GRUPO = []
        for i in range(len(tds)-3):
            n=i                                   
            for key in keys:                
                if key in tds[i]:
                    PREMIO.append(str(tds[n].text))
                    RESULTADO.append(int(tds[n+1].text))
                    GRUPO.append(int(tds[n+2].text))                                        
                elif len(tds) == 22:                    
                    m=0
                    while m < len(tds[:-1]):                    
                        PREMIO.append(str(tds[m].text))
                        RESULTADO.append(int(tds[m+1].text))
                        GRUPO.append(tds[m+2].text.split()[0])                        
                        m += 3
                    break
            n+=3
        # CREATE DATAFRAME
        df = pd.DataFrame({
            "DATA": objDate,
            "NOME": name,
            "PREMIO": PREMIO,
            "RESULTADO": RESULTADO,
            "GRUPO": GRUPO
        }).drop_duplicates()
        print("##"*10)
        print("PAGINA {}, TABELA {}".format(page, j))
        print("\n\n")
        print(df)
        print("\n\n")
        print("##"*10)
        df.to_csv('./data/tabela_{}_{}.csv'.format(page, j))
        dfs.append(df)

    return dfs

page=0
while True:
    try:
        driver = webdriver.Firefox(options=options)
        if page == 0:
            driver.get("https://resultadosemponto.com/")
        elif page > 0:
            driver.get("https://resultadosemponto.com/page/{}".format(int(page)))
        url = driver.current_url
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')   
        articles = soup.find_all('article')
        dfs = get_data(articles,page)
        page += 1
    except:
        page+=1
        pass