from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse


def extract_body_text(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        body = soup.find('body')
        if body:
            return body.get_text(separator='\n').strip().replace('\n', '')
        else:
            return "No body tag found in the HTML."
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch {url}: {e}"
    
def crawl(url):
    visited_urls = set()
    to_visit_urls = [url]
    all_found_urls = set()

    while to_visit_urls:
        current_url = to_visit_urls.pop(0)
        if current_url not in visited_urls:
            try:
                page = requests.get(current_url)
                soup = BeautifulSoup(page.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(current_url, href)
                    if urlparse(full_url).netloc == urlparse(current_url).netloc:
                        if full_url not in visited_urls and full_url not in to_visit_urls:
                            to_visit_urls.append(full_url)
                        all_found_urls.add(full_url)
            except requests.exceptions.RequestException as e:
                print(f"Failed to crawl {current_url}: {e}")
            visited_urls.add(current_url)

    return sorted(all_found_urls)

def extract_all_data(base_url):
    all_urls = crawl(base_url)
    data_from_links = {}

    for url in all_urls:
        body_text = extract_body_text(url)
        data_from_links[url] = body_text
    return data_from_links

def extract_query_tag(url,tag):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        queryText = soup.find(tag)
        if queryText:
            return queryText.get_text(separator='\n').strip().replace('\n', '')
        else:
            return "No query tag found in the HTML."
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch {tag} in {url}: {e}"

