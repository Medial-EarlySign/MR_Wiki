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


def get_pages() -> list[str]:
    resp = requests.get("https://medial-earlysign.github.io/MR_WIKI/sitemap")
    data = resp.content
    xml = ET.parse(BytesIO(data))
    all_res = xml.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    all_urls = list(map(lambda x: x.text.replace("/MR_Wiki/", "/MR_WIKI/"), all_res))
    return all_urls


def index_page(driver: webdriver.Chrome, index_url: str, REINDEX: bool) -> bool:
    driver.get("https://search.google.com/search-console")

    wait = WebDriverWait(driver, 30)

    element_locator = (
        By.CSS_SELECTOR,
        "input[aria-label='Inspect any URL in https://medial-earlysign.github.io/MR_WIKI/']",
    )
    search_box = wait.until(EC.visibility_of_element_located(element_locator))

    search_box.send_keys(index_url + "\n")
    time.sleep(1)

    #live index: 'Test live URL'
    element_locator_live = (
        By.XPATH,
        "//span[text() = 'Test live URL']",
    )
    live_search = wait.until(
        EC.visibility_of_element_located(element_locator_live)
    )
    live_search.click()

    element_locator_req_index = (
        By.XPATH,
        "//span[text() = 'Request indexing']",
    )
    index_button = wait.until(
        EC.visibility_of_element_located(element_locator_req_index)
    )

    # Check if URL is in google first: 'Page is indexed'
    is_indexed = (
        len(driver.find_elements(By.XPATH, "//div[text() = 'Page is indexed']")) > 0
    )

    if not (is_indexed) or REINDEX:
        index_button.click()
    return is_indexed


def index_all(reindex: bool) -> dict[str, bool]:
    all_urls = get_pages()
    options = Options()
    hm_folder = os.environ["HOME"]
    options.add_argument(rf"--user-data-dir={hm_folder}/snap/chromium/common/chromium")
    options.add_argument(r"--profile-directory=Default")
    driver = webdriver.Chrome(options=options)
    all_pages = {}
    for url in tqdm(all_urls):
        try:
            was_indexed = index_page(driver, url, reindex)
            all_pages[url] = was_indexed
        except:
            traceback.print_exc()
            all_pages[url] = None
            time.sleep(3)
    return all_pages


all_pages = index_all(False)
all_pages = pd.DataFrame.from_dict(
    all_pages, orient="index", columns=["was_indexed"]
).reset_index()
all_pages.rename(columns={"index": "url"}, inplace=True)
all_pages.to_csv("~/google.csv", index=False)
