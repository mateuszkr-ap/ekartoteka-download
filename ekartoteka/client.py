import requests
from pathlib import Path
from ekartoteka.downloader import download_file, sanitize_filename

BASE_URL = "https://e-kartoteka.pl/api"


class EkartotekaClient:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            # "Content-Type": "application/json"
        }
        self.id_a_do = None
        self.active_uchwaly_location = Path("./files/uchwaly/active")
        self.active_uchwaly_location.mkdir(parents=True, exist_ok=True)
        self.uchwaly_archiwalne_location = Path("./files/uchwaly/archiwalne")
        self.uchwaly_archiwalne_location.mkdir(parents=True, exist_ok=True)
        self.uchwaly_location = self.active_uchwaly_location

    def get_user_data(self):
        """Fetch current user data from the API."""
        url = f"{BASE_URL}/uzytkownicy/uzytkownicy/me/"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_dane_ksiegowe(self):
        """Extract DaneKsiegowe field from user data."""
        user_data = self.get_user_data()
        self.id_a_do = user_data.get("DaneKsiegowe", {})
        return self.id_a_do

    def get_uchwaly(self, page=1, page_size=50, aktywne=1):
        """Fetch active uchwały from the API with pagination.

        Args:
            page (int): Page number (default: 1)
            page_size (int): Number of items per page (default: 10)
        """
        url = f"{BASE_URL}/uchwaly/uchwaly/"
        params = {
            "id_a_do": self.id_a_do,
            "page_size": page_size,
            "page": page,
            "aktywne": aktywne,
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_active_uchwaly(self, page=1, page_size=50, aktywne=1):
        return self.get_uchwaly(page, page_size, aktywne)

    def get_inactive_uchwaly(self, page=1, page_size=50, aktywne=0):
        return self.get_uchwaly(page, page_size, aktywne)

    def get_uchwala_file(self, uchwala, active=True):
        """Fetch uchwała file from the API."""
        url = f"{BASE_URL}/uchwaly/uchwaly/{uchwala['id_uch']}/zalaczniki/"
        params = {"id_a_do": self.id_a_do, "page_size": 1000, "removed": False}
        if active:
            location = self.active_uchwaly_location
        else:
            location = self.uchwaly_archiwalne_location
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        zalaczniki = response.json().get("results", [])
        for i, zal in enumerate(zalaczniki):
            base_url = (
                f"{BASE_URL}/uchwaly/uchwaly/{zal['id_uch']}/zalaczniki/{zal['id']}/"
            )
            download_url = (
                f"{base_url}?id_a_do={self.id_a_do}&pageSize=1000&removed=False"
            )
            name = sanitize_filename(uchwala["Nazwa"]) + f"{i}." + zal["extension"]
            download_file(
                download_url, f"{location.as_posix()}/{name}", headers=self.headers
            )
        return response.json()
