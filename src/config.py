# Configuration settings for the e-kartoteka downloader
import os
BASE_URL = "https://e-kartoteka.pl/"
DOWNLOAD_PATH = "./files/"
TIMEOUT = 10  # seconds

def get_download_url(resource_id: str) -> str:
    """Constructs the download URL for a given resource ID."""
    return f"{BASE_URL}download/{resource_id}"

def get_headers() -> dict:
    """Returns the headers to be used in HTTP requests."""
    authorization = os.getenv("EKARTOTEKA_AUTHORIZATION")
    cookie = os.getenv("EKARTOTEKA_COOKIE")
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Authorization": authorization,
        "Cookie": cookie,
        # "Content-Type": "application/json; charset=utf-8"
    }