from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import time

def crawl_with_selenium():
    url = 'https://jateng.bps.go.id/id/statistics-table/1/MjY2NSMx/banyaknya-desa-kelurahan-menurut-keberadaan-penyandang-disabilitas--2021.html'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    table = soup.find('table')
    if table is None:
        print("Masih tidak menemukan tabel. Coba tambah waktu sleep.")
        return
    
    df_raw = pd.read_html(str(table))[0]
    
    df_raw.columns = df_raw.iloc[4]
    df_clean = df_raw[5:].reset_index(drop=True)

    print("Data sudah dibersihkan:")
    print(df_clean.head())
    
    client = MongoClient("mongodb://localhost:27017/")
    db = client["selvoi_db"]
    collection = db["penyandang_disabilitas"]
    collection.delete_many({})
    collection.insert_many(df_clean.to_dict(orient="records"))

    print("Data berhasil disimpan ke MongoDB.")

if __name__ == "__main__":
    crawl_with_selenium()
