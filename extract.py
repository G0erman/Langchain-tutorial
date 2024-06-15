import os
import requests

from dotenv import load_dotenv

load_dotenv()

URL_PDF = os.getenv("URL_PDF")
FILE_PATH = os.getenv("FILE_PATH")


def download_pdf(url: str, path: str) -> None:
    if is_pdf_downloaded(path):
        print(f"File already exists: {path}")
        return
    response = requests.get(url)
    with open(path, "wb") as f:
        f.write(response.content)


def is_pdf_downloaded(path: str) -> bool:
    return os.path.exists(path)


if __name__ == "__main__":
    download_pdf(URL_PDF, FILE_PATH)
