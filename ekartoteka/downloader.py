import requests
import json
import unicodedata
import pandas as pd


def download_file(url: str, destination: str, headers) -> None:
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(response.text)


def sanitize_filename(filename: str) -> str:
    """Sanitize the filename to ensure it is valid for the filesystem."""
    return (
        unicodedata.normalize("NFKD", filename)
        .replace(" ", "_")
        .replace(":", "_")
        .replace("/", "_")
    )


def save_json(data: dict, filename: str) -> None:
    """Save JSON data to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def json_to_csv(uchwaly: dict, filename: str) -> None:
    """Convert uchwały data to a CSV file."""
    df = pd.DataFrame(uchwaly)
    df.to_csv(filename, index=False, encoding="utf-8", sep=";")
