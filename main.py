from pathlib import Path
from tqdm import tqdm
from ekartoteka.authenticate import authenticate
from ekartoteka.client import EkartotekaClient
from ekartoteka.downloader import save_json, json_to_csv

PAGE_SIZE = 100

def get_uchwaly(client):
    active_uchwaly = client.get_active_uchwaly(page_size=PAGE_SIZE)
    assert active_uchwaly["count"] < PAGE_SIZE, (
        "Too many active uchwały, please increase PAGE_SIZE"
    )
    save_json(
        active_uchwaly, client.active_uchwaly_location / f"active_uchwaly_{client.id_a_do}.json"
    )
    json_to_csv(
        active_uchwaly["results"],
        client.active_uchwaly_location / f"active_uchwaly_{client.id_a_do}.csv",
    )
    for uchwala in tqdm(active_uchwaly["results"], desc="Downloading active uchwały"):
        client.get_uchwala_file(uchwala, active=True)
    print(f"Active uchwały saved to {client.active_uchwaly_location}")

    inactive_uchwaly = client.get_inactive_uchwaly(page_size=PAGE_SIZE)
    assert inactive_uchwaly["count"] < PAGE_SIZE, (
        "Too many inactive uchwały, please increase PAGE_SIZE"
    )
    save_json(
        inactive_uchwaly,
        client.uchwaly_archiwalne_location / f"archiwalne_uchwaly_{client.id_a_do}.json",
    )
    json_to_csv(
        inactive_uchwaly["results"],
        client.uchwaly_archiwalne_location / f"archiwalne_uchwaly_{client.id_a_do}.csv",
    )
    for uchwala in tqdm(
        inactive_uchwaly["results"], desc="Downloading inactive uchwały"
    ):
        client.get_uchwala_file(uchwala, active=False)
    print(f"Archiwalne uchwały saved to {client.uchwaly_archiwalne_location}")

def get_dokumenty(client):
    folders = client.get_document_folders()["results"]
    for i in folders:
        folder_directory = client.dokumenty_location / i["Nazwa"]
        folder_directory.mkdir(parents=True, exist_ok=True)
        documents = client.get_documents_from_folder(i["IdRodz"], page_size=PAGE_SIZE)
        save_json(
            documents,
            folder_directory / f"dokumenty_{i['Nazwa']}_{client.id_a_do}.json",
        )
        json_to_csv(
            documents["results"],
            folder_directory / f"dokumenty_{i['Nazwa']}_{client.id_a_do}.csv",
        )
        for doc in tqdm(documents["results"], desc=f"Downloading documents from folder {i['Nazwa']}"):
            client.get_document_attachments(doc["id_dok"], folder_directory)
        
   
    
    
def main():
    token = authenticate()
    client = EkartotekaClient(token)
    id_ado = client.get_dane_ksiegowe()
    print(f"ID ADO: {id_ado}")
    print("Getting uchwały...")
    get_uchwaly(client)
    print("Getting dokumenty...")
    get_dokumenty(client)
    print("Done!")




if __name__ == "__main__":
    main()
