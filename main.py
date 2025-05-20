from pathlib import Path
from ekartoteka.authenticate import authenticate
from ekartoteka.client import EkartotekaClient
from ekartoteka.downloader import save_json

PAGE_SIZE = 100
def main():
    token = authenticate()
    client = EkartotekaClient(token)
    
    id_ado = client.get_dane_ksiegowe()[0]
    print(f"ID ADO: {id_ado}")
    active_uchwaly = client.get_active_uchwaly(page_size=PAGE_SIZE)
    save_json(active_uchwaly, client.active_uchwaly_location / f"active_uchwaly_{id_ado}.json")
    for uchwala in active_uchwaly["results"]:
        client.get_uchwala_file(uchwala, active=True)
    print(f"Active uchwały saved to {client.active_uchwaly_location / f'active_uchwaly_{id_ado}.json'}")
    
    inactive_uchwaly = client.get_inactive_uchwaly(page_size=PAGE_SIZE)
    save_json(inactive_uchwaly, client.uchwaly_archiwalne_location/ f"archiwalne_uchwaly_{id_ado}.json")
    for uchwala in inactive_uchwaly["results"]:
        client.get_uchwala_file(uchwala, active=False)
    print(f"Archiwalne uchwały saved to {client.uchwaly_archiwalne_location / f'inactive_uchwaly_{id_ado}.json'}")
    
    
if __name__ == "__main__":
    
    main()
    
    
    
