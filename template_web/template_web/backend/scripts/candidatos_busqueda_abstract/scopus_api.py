import requests
import logging

from .filter import filter_valid_results

SCOPUS_API_KEY = "28ed61df3b550a39c575b5270b49f254"
SCOPUS_SEARCH_URL = "https://api.elsevier.com/content/search/scopus"
HEADERS = {"X-ELS-APIKey": SCOPUS_API_KEY, "Accept": "application/json"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def fetch_scopus_articles(query, max_results=10):
    results = []
    params = {"query": query, "apiKey": SCOPUS_API_KEY, "count": max_results, "field": "dc:title,prism:doi"}
    try:
        logging.info(f"🔍 Buscando en Scopus para '{query}'")
        response = requests.get(SCOPUS_SEARCH_URL, params=params, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for paper in data.get("search-results", {}).get("entry", []):
                title = paper.get("dc:title")
                doi = paper.get("prism:doi", "No disponible")
                if title:
                    results.append({"query": query, "titulo": title, "revista": "Scopus", "doi": doi})
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error en Scopus: {e}")
    return filter_valid_results(results)

def get_paper_info_scopus(title):
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {"X-ELS-APIKey": SCOPUS_API_KEY, "Accept": "application/json"}
    params = {"query": f"TITLE({title})", "count": 1}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if "search-results" in data and "entry" in data["search-results"] and data["search-results"]["entry"]:
        paper = data["search-results"]["entry"][0]
        return {
            "title": paper.get("dc:title", "No title found"),
            "abstract": paper.get("dc:description", "No abstract available"),
            "doi": paper.get("prism:doi", "No DOI found"),
            "link": paper.get("link", [{}])[0].get("@href", "No link available")
        }
    return None

if __name__ == "__main__":
    query = '("foam detection" OR "foam monitoring") AND (sensor OR "measurement system") AND (oil OR "industrial process") AND (precision OR reliability)'
    title = "Deep learning for time-series forecasting"
    
    fetch_scopus_articles(query)
    paper_info = get_paper_info_scopus(title)
    print(paper_info)
