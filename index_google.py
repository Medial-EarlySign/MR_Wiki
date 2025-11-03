#!/usr/bin/env python

from io import BytesIO
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import lxml.etree as ET
from tqdm import tqdm
import pandas as pd
import time
import os


def sort_page_key(url: str):
    if url.find("/MR_Wiki/index.html") > 0:
        return 0
    elif url.find("/Models/") > 0:
        return 1
    elif url.find("/Installation/") > 0:
        return 2
    elif url.find("/Repositories/") > 0:
        return 3
    elif url.find("/Medial%20Tools/") > 0:
        return 4
    elif url.find("/Infrastructure%20C%20Library/") > 0:
        return 5
    elif url.find("/Python/") > 0:
        return 6
    elif url.find("/Research/") > 0:
        return 7
    else:
        return 8


def get_pages(site: str) -> list[str]:
    resp = requests.get(f"{site}/sitemap")
    data = resp.content
    xml = ET.parse(BytesIO(data))
    all_res = xml.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    # .replace("/MR_Wiki/", "/MR_WIKI/")
    all_urls = list(map(lambda x: x.text, all_res))
    all_urls = sorted(all_urls, key=sort_page_key)

    return all_urls


def index_page(
    driver: webdriver.Chrome, base_site: str, index_url: str, REINDEX: bool
) -> tuple[bool, bool]:
    base_site = base_site.strip("/")
    driver.get(f"https://search.google.com/search-console?resource_id={base_site}")

    wait = WebDriverWait(driver, 30)

    element_locator = (
        By.CSS_SELECTOR,
        f"input[aria-label='Inspect any URL in {base_site}/']",
    )
    search_box = wait.until(EC.visibility_of_element_located(element_locator))

    search_box.send_keys(index_url + "\n")
    time.sleep(3)
    is_indexed = (
        len(driver.find_elements(By.XPATH, "//div[text() = 'Page is indexed']")) > 0
    )
    if is_indexed and not (REINDEX):
        return is_indexed, False

    # live index: 'Test live URL'
    element_locator_live = (
        By.XPATH,
        "//span[text() = 'Test live URL']",
    )
    live_search = wait.until(EC.visibility_of_element_located(element_locator_live))
    live_search.click()
    time.sleep(30)

    element_locator_req_index = (
        By.XPATH,
        "//span[text() = 'Request indexing']",
    )
    index_button = wait.until(
        EC.visibility_of_any_elements_located(element_locator_req_index)
    )

    # Check if URL is in google first: 'Page is indexed'
    is_indexed = (
        len(driver.find_elements(By.XPATH, "//div[text() = 'Page is indexed']")) > 0
    )

    if not (is_indexed) or REINDEX:
        if len(index_button) > 0:
            index_button[0].click()
    time.sleep(10)
    # Search for <span>Quota Exceeded</span>
    quata_limit = (
        len(driver.find_elements(By.XPATH, "//span[text() = 'Quota Exceeded']")) > 0
    )
    return is_indexed, quata_limit


def index_all(base_site: str, reindex: bool, file_index_path: str) -> dict[str, bool]:
    all_urls = get_pages(base_site)
    read_urls = set()
    if os.path.exists(file_index_path):
        with open(file_index_path, "r") as fr:
            read_urls = fr.readlines()
        read_urls = list(map(lambda x: x.strip(), read_urls))
        read_urls = set(list(filter(lambda x: len(x) > 0, read_urls)))
    options = Options()
    hm_folder = os.environ["HOME"]
    options.add_argument(rf"--user-data-dir={hm_folder}/snap/chromium/common/chromium")
    options.add_argument(r"--profile-directory=Default")
    driver = webdriver.Chrome(options=options)
    all_pages = {}
    for url in tqdm(all_urls):
        try:
            if url in read_urls:
                print(f"Skip url {url}")
                continue
            was_indexed, quata_limit = index_page(driver, base_site, url, reindex)
            all_pages[url] = was_indexed
            if not (quata_limit):
                with open(file_index_path, "a") as fw:
                    fw.write(url + "\n")
                read_urls.add(url)
            else:
                print("Quata Limit Reached!")
                break
        except:
            traceback.print_exc()
            all_pages[url] = None
            time.sleep(3)
    return all_pages


if __name__ == "__main__":
    SITE = "https://medial-earlysign.github.io/MR_Wiki"
    REINDEX = False
    store_indexed = os.path.join(os.environ["HOME"], "google_index.csv")
    all_pages = index_all(SITE, REINDEX, store_indexed)
    all_pages = pd.DataFrame.from_dict(
        all_pages, orient="index", columns=["was_indexed"]
    ).reset_index()
    all_pages.rename(columns={"index": "url"}, inplace=True)
    all_pages.to_csv("~/google.csv", index=False)
