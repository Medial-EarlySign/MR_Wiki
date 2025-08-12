import asyncio
import httpx
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin, urlparse
import pandas as pd
import time

pointer_to_page = dict()
crawled_pages = dict()
max_crawled_pages = 500

def get_page_re(url: str, retries: int = 3) -> str | None:
    """Fetch a page with retries for common HTTP and system errors."""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()  # Raise an error for bad responses
            return response.text
        except Exception as e:
            #print(f"Attempt {attempt + 1} failed for {url}, error: {str(e)}")
            if attempt < retries - 1:
                time.sleep(1)
            else:
                print(f"Failed to fetch {url} after {retries} attempts: {e}")
    return None


async def get_page(url: str, retries: int = 3) -> str | None:
    """Fetch a page with retries for common HTTP and system errors."""
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(url)
                if response.status_code == 200 or response.status_code == 301:
                    return response.text
                else:
                    print(f"Non-200 status code {response.status_code} for {url}")
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
        await asyncio.sleep(1)  # Backoff between retries
    return None


async def crawl_page(url: str, limiter: asyncio.Semaphore) -> None:
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
    print(f"crawling: {url}")
    #html_content = await get_page(url)
    html_content = get_page_re(url)
    if not html_content:
        crawled_pages[url] = 0
        return
    else:
        crawled_pages[url] = 1
    # await process_page(html_content)

    # extract all relative or same-domain URLs
    soup = BeautifulSoup(html_content, "html.parser")
    base_domain = urlparse(url).netloc
    urls = []
    for link in soup.find_all("a", href=True):
        href: str = link["href"] # type: ignore
        absolute_url = urljoin(url, href)
        absolute_url = absolute_url.split("#")[0]  # remove fragment
        if absolute_url in crawled_pages:
            continue
        if urlparse(absolute_url).netloc != base_domain:
            continue
        urls.append(absolute_url)
        pointer_to_page[absolute_url] = url
    # print(f"  found {len(urls)} new links")
    # ensure we don't crawl more than the max limit
    _remaining_crawl_budget = max_crawled_pages - len(crawled_pages)
    if len(urls) > _remaining_crawl_budget:
        urls = urls[:_remaining_crawl_budget]

    # schedule more crawling concurrently
    async with limiter:
        await asyncio.gather(*[crawl_page(url, limiter) for url in urls])


async def main(start_url, concurrency=10):
    """Main function to control crawling."""
    limiter = asyncio.Semaphore(concurrency)
    try:
        await crawl_page(start_url, limiter=limiter)
    except asyncio.CancelledError:
        print("Crawling was interrupted")


if __name__ == "__main__":
    start_url = "http://localhost:8000"  # Change this to your starting URL
    asyncio.run(main(start_url))
    df = pd.DataFrame.from_dict(crawled_pages, orient="index", columns=["status"])
    df_sources = pd.DataFrame.from_dict(
        pointer_to_page, orient="index", columns=["source"]
    )
    df = df.join(df_sources)
    df.reset_index(inplace=True)
    print(df[df['status']==0])
    breakpoint()
