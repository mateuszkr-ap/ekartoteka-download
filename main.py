from pathlib import Path
from tqdm import tqdm
from ekartoteka.authenticate import authenticate
from ekartoteka.client import EkartotekaClient
from ekartoteka.downloader import save_json, uchwaly_to_csv

PAGE_SIZE = 100


def main():
    token = authenticate()
    client = EkartotekaClient(token)

    id_ado = client.get_dane_ksiegowe()[0]
    print(f"ID ADO: {id_ado}")
    active_uchwaly = client.get_active_uchwaly(page_size=PAGE_SIZE)
    assert active_uchwaly["count"] < PAGE_SIZE, (
        "Too many active uchwały, please increase PAGE_SIZE"
    )
    save_json(
        active_uchwaly, client.active_uchwaly_location / f"active_uchwaly_{id_ado}.json"
    )
    uchwaly_to_csv(
        active_uchwaly["results"],
        client.active_uchwaly_location / f"active_uchwaly_{id_ado}.csv",
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
        client.uchwaly_archiwalne_location / f"archiwalne_uchwaly_{id_ado}.json",
    )
    uchwaly_to_csv(
        inactive_uchwaly["results"],
        client.uchwaly_archiwalne_location / f"archiwalne_uchwaly_{id_ado}.csv",
    )
    for uchwala in tqdm(
        inactive_uchwaly["results"], desc="Downloading inactive uchwały"
    ):
        client.get_uchwala_file(uchwala, active=False)
    print(f"Archiwalne uchwały saved to {client.uchwaly_archiwalne_location}")


if __name__ == "__main__":
    main()
