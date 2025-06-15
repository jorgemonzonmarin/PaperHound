import logging
import requests
import xml.etree.ElementTree as ET
from .filter import filter_valid_results

ARXIV_SEARCH_URL = "http://export.arxiv.org/api/query"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def fetch_arxiv_articles(query, max_results=10):
    results = []
    params = {"search_query": f"ti:{query}", "start": 0, "max_results": max_results}
    try:
        logging.info(f"🔍 Buscando en ArXiv para '{query}'")
        response = requests.get(ARXIV_SEARCH_URL, params=params, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                title = entry.find("atom:title", ns).text
                link = entry.find("atom:id", ns).text
                if title:
                    results.append({"query": query, "titulo": title, "revista": "ArXiv", "doi": link})
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error en ArXiv: {e}")
    return filter_valid_results(results)

def get_paper_info_arxiv(title):
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": f"ti:{title}", "start": 0, "max_results": 1}

    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entry = root.find("atom:entry", ns)
    print(entry)
    if entry is not None:
        return {
            "title": entry.find("atom:title", ns).text,
            "abstract": entry.find("atom:summary", ns).text,
            "link": entry.find("atom:id", ns).text
        }
    return None

if __name__ == "__main__":
    query = '("foam detection" OR "foam monitoring") AND (sensor OR "measurement system") AND (oil OR "industrial process") AND (precision OR reliability)'
    fetch_arxiv_articles(query)
    title = "Deep learning for time-series forecasting"
    paper_info = get_paper_info_arxiv(title)
    print(paper_info)
