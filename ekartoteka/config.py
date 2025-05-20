# Configuration settings for the e-kartoteka downloader
from pathlib import Path
BASE_URL = "https://e-kartoteka.pl/"
DOWNLOAD_PATH = "./files/"
TIMEOUT = 10  # seconds

def build_folders(path: str = DOWNLOAD_PATH) -> None:
    """Creates the necessary folders for downloading files."""
    Path("./files/uchwaly/aktywne").mkdir(parents=True, exist_ok=True)
    Path("./files/uchwaly/archiwalne").mkdir(parents=True, exist_ok=True)

def get_download_url(resource_id: str) -> str:
    """Constructs the download URL for a given resource ID."""
    return f"{BASE_URL}download/{resource_id}"