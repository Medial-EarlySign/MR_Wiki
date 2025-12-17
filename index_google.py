#!/usr/bin/env python

from io import BytesIO, StringIO
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
import urllib.parse
import glob
from zipfile import ZipFile


def filter_pages(url: str) -> bool:
    if url.find("/Archive/") > 0:
        return False
    if url.endswith("/LICENCE.html") or url.endswith("/CONTRIBUTING.html"):
        return False
    return True


def sort_page_key(url: str):
    if url.find("/MR_Wiki/index.html") > 0:
        return 0
    elif url.find("/Models/") > 0:
        return 1
    elif url.find("/Installation/") > 0:
        return 2
    elif url.find("/Tutorials/") > 0:
        return 3
    elif url.find("/Infrastructure%20Library/Medial%20Tools/") > 0:
        return 4
    elif url.find("/Infrastructure%20Library/") > 0:
        return 5
    elif url.find("/Research/") > 0:
        return 6
    else:
        return 7


def get_pages(site: str) -> list[str]:
    resp = requests.get(f"{site}/sitemap")
    data = resp.content
    xml = ET.parse(BytesIO(data))
    all_res = xml.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    # .replace("/MR_Wiki/", "/MR_WIKI/")
    all_urls = list(map(lambda x: x.text, all_res))
    # Remove:
    all_urls = list(filter(lambda x: filter_pages(x), all_urls))
    all_urls = sorted(all_urls, key=sort_page_key)

    return all_urls


def get_already_indexed_pages(driver: webdriver.Chrome, site: str) -> pd.DataFrame:
    site_strip = urllib.parse.quote(site, safe=[])
    driver.get(
        f"https://search.google.com/search-console/index/drilldown?resource_id={site_strip}&pages=ALL_URLS"
    )
    wait = WebDriverWait(driver, 30)
    # div[role="button" aria-label="EXPORT"]
    element_locator = (By.CSS_SELECTOR, "div[role='button'][aria-label='EXPORT']")
    export_button = wait.until(EC.visibility_of_any_elements_located(element_locator))
    export_button = driver.find_element(element_locator[0], element_locator[1])
    export_button.click()

    time.sleep(1)
    csv_down = driver.find_element(By.CSS_SELECTOR, "span[aria-label='Download CSV']")
    csv_down.click()
    time.sleep(5)

    home = os.path.expanduser("~")
    downloadspath = os.path.join(home, "Downloads")
    list_of_files = glob.glob(
        downloadspath + r"/*.zip"
    )  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    with ZipFile(latest_file, "r") as zip_object:
        with zip_object.open("Table.csv") as file_in_zip:
            content = file_in_zip.read().decode("utf-8")
    df_indexed = pd.read_csv(StringIO(content))
    df_indexed["URL"] = df_indexed["URL"].apply(
        lambda x: x.replace("\n", "").replace(" ", "%20")
    )
    os.remove(latest_file)
    return df_indexed


def get_already_indexed_pages_multiple(driver: webdriver.Chrome, sites: list[str]):
    df = pd.concat(
        [get_already_indexed_pages(driver, site) for site in sites], ignore_index=True
    )
    return df


def index_page(
    driver: webdriver.Chrome, base_site: str, index_url: str, REINDEX: bool
) -> str:
    final_status = 'unknown'
    base_site = base_site.strip("/")
    driver.get(f"https://search.google.com/search-console?resource_id={base_site}")

    wait = WebDriverWait(driver, 30)

    element_locator = (
        By.CSS_SELECTOR,
        f"input[type='text']",
    )
    search_box = wait.until(EC.visibility_of_any_elements_located(element_locator))
    # Find the element with aria-label='Inspect any URL in ..'
    search_box = list(
        filter(
            lambda x: x.get_attribute("aria-label").startswith("Inspect any URL in"),
            search_box,
        )
    )
    assert len(search_box) == 1, f"Found {len(search_box)} search elements"
    search_box = search_box[0]

    search_box.send_keys(index_url + "\n")
    time.sleep(3)
    is_indexed = (
        len(driver.find_elements(By.XPATH, "//div[text() = 'Page is indexed']")) > 0
    )
    
    if is_indexed:
        final_status = 'indexed'
    if is_indexed and not (REINDEX):
        return final_status
    indexing_div_stats = driver.find_elements(By.XPATH, "//div[text() = 'Page indexing']/../div")
    indexing_div_stats = list(filter(lambda x: x.text != 'Page indexing',indexing_div_stats))
    is_duplicate_issue = False
    if len(indexing_div_stats) > 0:
        indexing_div_stats = indexing_div_stats[0]
        status = indexing_div_stats.text
        is_duplicate_issue = status.find("Duplicate, Google chose different canonical than user") >= 0
        final_status = status
    if is_duplicate_issue and not (REINDEX):
        return 'duplicate'
    
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
    if quata_limit:
        final_status = 'quota'
    return final_status


def index_all(
    base_site: str, reindex: bool, use_cache_file: bool = True
) -> dict[str, bool]:
    BASE_CACHE_PATH = os.path.join(os.environ["HOME"], "google_index.csv")
    all_urls = get_pages(base_site)
    options = Options()
    hm_folder = os.environ["HOME"]
    options.add_argument(rf"--user-data-dir={hm_folder}/snap/chromium/common/chromium")
    options.add_argument(r"--profile-directory=Default")
    #options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    read_urls_df = get_already_indexed_pages(driver, base_site)
    read_urls = set(read_urls_df["URL"].unique())
    if use_cache_file:
        if os.path.exists(BASE_CACHE_PATH):
            use_cache_file = True
            read_urls_df = pd.read_csv(BASE_CACHE_PATH, sep="\t", names=["URL"])
            read_urls_df = read_urls_df.drop_duplicates(ignore_index=True)
            read_urls = read_urls.union(set(read_urls_df["URL"].unique()))

    all_pages = {}
    for url in tqdm(all_urls):
        try:
            if url in read_urls:
                print(f"Skip url {url}")
                continue
            final_status = index_page(driver, base_site, url, reindex)
            all_pages[url] = final_status
            quata_limit = final_status == "quota"
            if not (quata_limit):
                read_urls.add(url)
                if use_cache_file:
                    with open(BASE_CACHE_PATH, "a") as fw:
                        fw.write(f"{url}\n")
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
    all_pages = index_all(SITE, REINDEX)
    all_pages = pd.DataFrame.from_dict(
        all_pages, orient="index", columns=["was_indexed"]
    ).reset_index()
    all_pages.rename(columns={"index": "url"}, inplace=True)
    all_pages.to_csv("~/google.csv", index=False)
