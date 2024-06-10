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

driver.close()

conexao = psycopg2.connect(
        dbname='dbcotacoes', 
        user='avnadmin', 
        password='AVNS_DgQT5YHAmGpK5QE600Y', 
        host='pg-13f76388-gapettena-cecb.g.aivencloud.com', 
        port='21452'
    )
cursor = conexao.cursor()
print(dolar)
cursor.execute(f'CALL inserir_cotacao({dolar})')
conexao.commit()

cursor.close()
conexao.close()
