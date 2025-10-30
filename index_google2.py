from io import BytesIO
import os
import traceback
import requests
import json
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import lxml.etree as ET
from tqdm import tqdm

KEY_FILE_PATH = "/path/to_credentials"


def get_pages(site: str) -> list[str]:
    resp = requests.get(f"{site}/sitemap")
    data = resp.content
    xml = ET.parse(BytesIO(data))
    all_res = xml.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    # .replace("/MR_Wiki/", "/MR_WIKI/")
    all_urls = list(map(lambda x: x.text, all_res))
    return all_urls


def post_google_url(url: str) -> requests.Response:
    credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE_PATH, scopes=["https://www.googleapis.com/auth/indexing"]
    )
    authorized_session = AuthorizedSession(credentials)

    req_data = {"url": url, "type": "URL_UPDATED"}

    resp = authorized_session.post(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        data=json.dumps(req_data),
        headers={"content-type": "application/json"},  # API expects JSON content type
    )
    if resp.status_code == 200:
        pass
        # print(f"URL {url} submitted successfully: {resp.json()}")
    else:
        print(
            f"Failed to submit URL {url}. Status code: {resp.status_code}, Response: {resp.text}"
        )

    return resp


def index_all(base_site: str):
    all_urls = get_pages(base_site)
    all_urls = list(filter(lambda x: x.find("/Research/") < 0, all_urls))
    all_urls = list(
        filter(lambda x: x.find("/MedProcessTools%20Library/") < 0, all_urls)
    )

    # Filter
    for url in tqdm(all_urls):
        try:
            resp = post_google_url(url)

            if resp.status_code == 200:
                pass
            else:
                print("error")
                print(resp.content)
                break
        except:
            traceback.print_exc()
            break


if __name__ == "__main__":
    SITE = "https://medial-earlysign.github.io/MR_Wiki"
    # store_indexed = os.path.join(os.environ["HOME"], "google_index.csv")
    all_pages = index_all(SITE)
