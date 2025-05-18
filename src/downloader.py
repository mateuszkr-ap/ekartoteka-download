import requests
import unicodedata

def download_file(url: str, destination: str, headers) -> None:
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(response.text)
    
def sanitize_filename(filename: str) -> str:
    """Sanitize the filename to ensure it is valid for the filesystem."""
    return unicodedata.normalize("NFKD",filename).replace(" ", "_").replace(":", "_").replace("/", "_")