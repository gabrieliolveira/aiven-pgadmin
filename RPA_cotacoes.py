import datetime
import time
from selenium.webdriver.chrome.options import Options
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

## Pegando cotação dólar site

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu") 

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.google.com/search?q=cotacao+dolar&rlz=1C1GCEU_pt-BRBR1077BR1077&oq=cotacao&gs_lcrp=EgZjaHJvbWUqBwgBEAAYgAQyCQgAEEUYORiABDIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIMCAYQABhDGIAEGIoFMgcIBxAAGIAEMgcICBAAGIAEMgcICRAAGIAE0gEIMTkwN2owajeoAgCwAgA&sourceid=chrome&ie=UTF-8")

time.sleep(2)

dolar = driver.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').text
dolar = dolar.replace(',', '.')
float(dolar)
current_date = datetime.datetime.now().date() 
current_time = datetime.datetime.now().time()

driver.close()

conexao = psycopg2.connect(
        dbname='dbcotacoes_xqci', 
        user='postgresss', 
        password='WHRyNdc6SxGCU1xqN6AY9oaSVJXM0270', 
        host='dpg-cr8q71l6l47c73bncnb0-a.oregon-postgres.render.com', 
        port='5432'
    )
cursor = conexao.cursor()
cursor.execute("CALL inserir_cotacao_dolar(%s, %s, %s);", (current_date, current_time, dolar))
conexao.commit()

cursor.close()
conexao.close()
