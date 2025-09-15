import asyncio
import traceback
import httpx
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin, urlparse
import pandas as pd
import time

pointer_to_page = dict()
crawled_pages = dict()
max_crawled_pages = 5000
allow_external_test = True


def get_page_re(url: str, retries: int = 3) -> tuple[str, str | None]:
    """Fetch a page with retries for common HTTP and system errors."""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()  # Raise an error for bad responses
            return response.url, response.text
        except Exception as e:
            # print(f"Attempt {attempt + 1} failed for {url}, error: {str(e)}")
            if attempt < retries - 1:
                time.sleep(1)
            else:
                print(f"Failed to fetch {url} after {retries} attempts: {e}")
    return url, None


async def get_page(url: str, retries: int = 3) -> tuple[str, str | None]:
    """Fetch a page with retries for common HTTP and system errors."""
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(url)
                if response.status_code == 301:
                    new_url = response.headers.get("Location")
                    absolute_url = urljoin(url, new_url)
                    absolute_url = absolute_url.split("#")[0]
                    url = absolute_url
                    response = await client.get(url)
                if response.text == "":
                    raise httpx.HTTPStatusError(
                        f"Empty response for {url}",
                        request=response.request,
                        response=response,
                    )
                if response.status_code == 200:
                    return url, response.text
                else:
                    print(f"Non-200 status code {response.status_code} for {url}")
        except (httpx.RequestError, httpx.HTTPStatusError, httpx.ReadTimeout) as e:
            traceback.print_exc()
            print(f"Attempt {attempt + 1} failed for {url} {e}")
        await asyncio.sleep(1)  # Backoff between retries
    return url, None


def crawl_page(
    url: str, allow_external_test: bool, start_url: str, limiter: asyncio.Semaphore
) -> None:
    """Crawl a page and extract all relative or same-domain URLs."""
    global crawled_pages
    global pointer_to_page
    if url in crawled_pages:  # url visited already?
        return
    # check if crawl limit is reached
    if len(crawled_pages) >= max_crawled_pages:
        return

    # scrape the url
    crawled_pages[url] = None
    print(f"{len(crawled_pages)} crawling: {url}")
    # url_final, html_content = await get_page(url)
    url_final, html_content = get_page_re(url)
    if not html_content:
        crawled_pages[url] = 0
        if url_final != url:
            crawled_pages[url_final] = 0
        return
    else:
        crawled_pages[url] = 1
        if url_final != url:
            crawled_pages[url_final] = 1

    # extract all relative or same-domain URLs
    html_page = (
        url_final.endswith(".html")
        or url_final.endswith("/")
        or url_final.split("/")[-1].find(".") == -1
    )
    if not html_page:
        return  # skip files that are not HTML pages
    soup = BeautifulSoup(html_content, "html.parser")
    base_domain = urlparse(url_final).netloc
    urls = []
    for link in soup.find_all("a", href=True):
        href: str = link["href"]  # type: ignore
        absolute_url = urljoin(url_final, href)
        absolute_url = absolute_url.split("#")[0]  # remove fragment
        if absolute_url in crawled_pages:
            continue
        if urlparse(absolute_url).netloc != base_domain or not(absolute_url.startswith(start_url)):
            # only test
            if allow_external_test:
                _, html_cont = get_page_re(absolute_url)
                if not html_cont:
                    crawled_pages[absolute_url] = 0
                else:
                    crawled_pages[absolute_url] = 1
                pointer_to_page[absolute_url] = url_final
            continue
        urls.append(absolute_url)
        pointer_to_page[absolute_url] = url_final
    for img in soup.find_all("img", src=True):
        img_url: str = img["src"]  # type: ignore
        absolute_url = urljoin(url_final, img_url)
        if absolute_url in crawled_pages:
            continue
        if urlparse(absolute_url).netloc != base_domain or not(absolute_url.startswith(start_url)):
            continue
        urls.append(absolute_url)
        pointer_to_page[absolute_url] = url_final
    # print(f"  found {len(urls)} new links")
    # ensure we don't crawl more than the max limit
    _remaining_crawl_budget = max_crawled_pages - len(crawled_pages)
    if len(urls) > _remaining_crawl_budget:
        urls = urls[:_remaining_crawl_budget]

    # schedule more crawling concurrently
    for url in urls:
        crawl_page(url, allow_external_test, start_url, limiter=limiter)
    # async with limiter:
    #    await asyncio.gather(*[crawl_page(url, allow_external_test, start_url, limiter) for url in urls])


def main(start_url, concurrency=1):
    """Main function to control crawling."""
    limiter = asyncio.Semaphore(concurrency)
    try:
        crawl_page(start_url, allow_external_test, start_url, limiter=limiter)
    except asyncio.CancelledError:
        print("Crawling was interrupted")


if __name__ == "__main__":
    # start_url = "http://localhost:8000"
    start_url = "https://medial-earlysign.github.io/MR_WIKI"  # Change this to your starting URL
    
    # asyncio.run(main(start_url))
    main(start_url)
    df = pd.DataFrame.from_dict(crawled_pages, orient="index", columns=["status"])
    df_sources = pd.DataFrame.from_dict(
        pointer_to_page, orient="index", columns=["source"]
    )
    df = df.join(df_sources, how="outer")
    df.reset_index(inplace=True)
    print(df[df["status"] == 0])
    df[df["status"] == 0].to_csv("~/res.csv", index=False)
    # breakpoint()
