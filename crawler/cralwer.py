import asyncio
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import requests
from xml.etree import ElementTree

async def crawl_sequential(urls: List[str]):
    """_summary_

    Args:
        urls (List[str]): _description_
    """
    
    # Browser configuration for imitating the user using headless browser
    browser_config = BrowserConfig(
        headless=True,
        # For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    
    # crawler config can return data differently as well, how about making it directly return data as vectors and/or chunks?
    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )
    
    # Create the crawler (opens the browser)
    crawler = AsyncWebCrawler(config=browser_config)
    
    # block execution until browser is spawned
    await crawler.start()
    
def get_urls_from_sitemap(sitemap_url: str) -> List[str]:
    """
    Fetches all URLs from a sitemap.xml file (if available).
    Returns:
        List[str]: List of URLs
    """
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        root = ElementTree.fromstring(response.content)
        
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        return urls
    except Exception as e:
        print(f"Failed to fetch URLs from sitemap: {e}")
        return []

async def main():
    urls = get_urls_from_sitemap()
    if urls:
        print(f"Found {len(urls)} URLs to crawl")
        await crawl_sequential(urls)
    else:
        print("No URLs found to crawl")

if __name__ == "__main__":
    asyncio.run(main())