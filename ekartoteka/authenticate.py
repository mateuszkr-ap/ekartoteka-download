import json
import requests
import os
from pathlib import Path


def load_credentials():
    """Load credentials from secrets.json file."""
    secrets_path = Path(__file__).parent.parent / "secrets.json"
    try:
        with open(secrets_path, "r") as f:
            credentials = json.load(f)
            return credentials.get("username"), credentials.get("password")
    except FileNotFoundError:
        raise FileNotFoundError(f"Credentials file not found at {secrets_path}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in secrets.json")


def authenticate():
    """Authenticate to e-kartoteka.pl and get bearer token."""
    username, password = load_credentials()

    if not username or not password:
        raise ValueError("Username or password missing in secrets.json")

    # API endpoint for authentication
    auth_url = "https://e-kartoteka.pl/api/api-token-auth/"

    # Prepare payload
    payload = {"username": username, "password": password}

    # Send authentication request
    response = requests.post(auth_url, json=payload)

    # Check response
    if response.status_code != 200:
        raise Exception(
            f"Authentication failed with status code {response.status_code}: {response.text}"
        )

    # Extract token
    response_data = response.json()
    token = response_data.get("token")

    if not token:
        raise ValueError("Token not found in response")

    # Save token to file
    token_path = Path(__file__).parent.parent / "token.txt"
    with open(token_path, "w") as f:
        f.write(token)

    print(f"Authentication successful. Token saved to {token_path}")
    return token


if __name__ == "__main__":
    authenticate()
