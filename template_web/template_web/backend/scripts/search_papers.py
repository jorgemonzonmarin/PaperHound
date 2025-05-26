import time
import logging
import requests
import xml.etree.ElementTree as ET
from scholarly import scholarly

SCOPUS_API_KEY = "28ed61df3b550a39c575b5270b49f254"
SCOPUS_SEARCH_URL = "https://api.elsevier.com/content/search/scopus"
OPENALEX_SEARCH_URL = "https://api.openalex.org/works"
ARXIV_SEARCH_URL = "http://export.arxiv.org/api/query"
CORE_SEARCH_URL = "https://api.core.ac.uk/v3/search/works"
CROSSREF_SEARCH_URL = "https://api.crossref.org/works"
HEADERS = {"X-ELS-APIKey": SCOPUS_API_KEY, "Accept": "application/json"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def filter_valid_results(results):
    return [paper for paper in results if paper.get("titulo") and paper["titulo"] != "No disponible"]

# Nota: Algunas de estas APIs tienen límites diarios de uso.
# OpenAlex: Ilimitado pero con límite de velocidad.
# CORE: Puede requerir API Key.
# CrossRef: Límite de consultas por minuto.

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

def fetch_scholar_articles(query, max_results=10):
    results = []
    try:
        logging.info(f"🔍 Buscando en Google Scholar para '{query}'")
        search_query = scholarly.search_pubs(query)
        for i, result in enumerate(search_query):
            if i >= max_results:
                break
            title = result["bib"].get("title")
            journal = result["bib"].get("venue", "Google Scholar")
            doi = result.get("pub_url", "No disponible")
            if title:
                results.append({"query": query, "titulo": title, "revista": journal, "doi": doi})
    except Exception as e:
        logging.error(f"❌ Error en Google Scholar: {e}")
    return filter_valid_results(results)

def fetch_openalex_articles(query, max_results=10):
    results = []
    params = {"filter": f"display_name.search:{query}", "per_page": max_results}
    try:
        logging.info(f"🔍 Buscando en OpenAlex para '{query}'")
        response = requests.get(OPENALEX_SEARCH_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for paper in data.get("results", []):
                title = paper.get("display_name")
                doi = paper.get("doi", "No disponible")
                if title:
                    results.append({"query": query, "titulo": title, "revista": "OpenAlex", "doi": doi})
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error en OpenAlex: {e}")
    return filter_valid_results(results)

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

def fetch_crossref_articles(query, max_results=10):
    results = []
    params = {"query": query, "rows": max_results}
    try:
        logging.info(f"🔍 Buscando en CrossRef para '{query}'")
        response = requests.get(CROSSREF_SEARCH_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for paper in data.get("message", {}).get("items", []):
                title = paper.get("title", [None])[0]
                doi = paper.get("DOI", "No disponible")
                if title:
                    results.append({"query": query, "titulo": title, "revista": "CrossRef", "doi": doi})
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error en CrossRef: {e}")
    return filter_valid_results(results)

def search_papers(queries, max_results=10):
    all_results = []
    for query in queries:
        logging.info(f"🔎 Procesando query: {query}")
        all_results.extend(fetch_scopus_articles(query, max_results=max_results))
        all_results.extend(fetch_scholar_articles(query, max_results=max_results))
        all_results.extend(fetch_openalex_articles(query, max_results=max_results))
        all_results.extend(fetch_arxiv_articles(query, max_results=max_results))
        all_results.extend(fetch_crossref_articles(query, max_results=max_results))
    return all_results

if __name__ == "__main__":
    queries = [
        '("foam detection" OR "foam monitoring") AND (sensor OR "measurement system") AND (oil OR "industrial process") AND (precision OR reliability)',
        '("foam detection" OR "bubble control") AND (sensor OR "monitoring system") AND (evaporation OR oil) AND industrial',
        '("foam detection" OR "foam monitoring") AND (sensor) AND ("water evaporation" OR "oil processing") AND (industrial OR process)',
        '("foam detection" OR "foam formation") AND (sensor OR "sensor technology") AND (ultrasonic OR optical OR "time of flight")',
        '("foam formation" OR "foam control") AND ("industrial process" OR "oil treatment") AND ("sensor-based detection")',
        '("foam detection" OR "bubble formation") AND ("sensor system") AND (precision OR reliability) AND industrial',
    ]
    
    for query in queries:
        logging.info(f"🔎 Procesando query: {query}")
        results = search_papers([query], max_results=5)
        
        for result in results:
            logging.info(f"📄 {result['titulo']} - {result['revista']} - {result['doi']}")