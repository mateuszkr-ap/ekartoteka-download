import requests
import unicodedata
import json
import os
from pathlib import Path
import email.header
from config import BASE_URL, DOWNLOAD_PATH, TIMEOUT, get_headers
from downloader import download_file, sanitize_filename

ID_ADO = 31636
ID_KLI = 2347271
def main():
   
    # foldery
    Path("./files/uchwaly/aktywne").mkdir(parents=True, exist_ok=True)
    Path("./files/uchwaly/archiwalne").mkdir(parents=True, exist_ok=True)
    # Aktywne uchwały
    
    req = requests.get(f"https://e-kartoteka.pl/api/uchwaly/uchwaly/?aktywne=1&id_a_do={ID_ADO}&id_kli={ID_KLI}&ordering=-NumerUch&page=1&pageSize=10",headers=get_headers())
    uchwaly_aktywne = [x for x in req.json()["results"]]
    with open("./files/uchwaly/aktywne/aktywne.json", "w", encoding="utf-8") as f:
        json.dump(uchwaly_aktywne, f, ensure_ascii=False, indent=4)
    
    for item in uchwaly_aktywne:
        zalączniki = requests.get(f"https://e-kartoteka.pl/api/uchwaly/uchwaly/{item['id_uch']}/zalaczniki/?id_a_do={item['IdADo']}&pageSize=1000&removed=False",headers=get_headers())
        for zal in zalączniki.json()["results"]:
            download_url = f"https://e-kartoteka.pl/api/uchwaly/uchwaly/{item['id_uch']}/zalaczniki/{zal['id']}/?id_a_do={item['IdADo']}&pageSize=1000&removed=False"
            name = sanitize_filename(item["Nazwa"])+"."+zal["extension"]
            download_file(download_url, f"./files/uchwaly/aktywne/{name}", headers=get_headers())
    
    # Archwalne uchwały
    req = requests.get("https://e-kartoteka.pl/api/uchwaly/uchwaly/?aktywne=0&id_a_do={ID_ADO}&id_kli={ID_KLI}&ordering=-NumerUch&page=1&pageSize=20",headers=get_headers())
    uchwaly = [x for x in req.json()["results"]]
    with open("./files/uchwaly/archiwalne/archiwalne.json", "w", encoding="utf-8") as f:
        json.dump(uchwaly, f, ensure_ascii=False, indent=4)   
    for item in uchwaly:
        zalączniki = requests.get(f"https://e-kartoteka.pl/api/uchwaly/uchwaly/{item['id_uch']}/zalaczniki/?id_a_do={item['IdADo']}&pageSize=1000&removed=False",headers=get_headers())
        for zal in zalączniki.json()["results"]:
            download_url = f"https://e-kartoteka.pl/api/uchwaly/uchwaly/{item['id_uch']}/zalaczniki/{zal['id']}/?id_a_do={item['IdADo']}&pageSize=1000&removed=False"
            name = sanitize_filename(item["Nazwa"])+"."+zal["extension"]
            download_file(download_url, f"./files/uchwaly/archiwalne/{name}", headers=get_headers())
      
    # Dokumenty
    # req = requests.get("https://www.e-kartoteka.pl/api/dokumentynieruchomosci/katalogi/?page=1&pageSize=100&id_a_do={ID_ADO}&_=1747468053433",headers=get_headers())
    # id_rodzin = [x["IdRodz"] for x in req.json()["results"]]
            
if __name__ == "__main__":
    main()