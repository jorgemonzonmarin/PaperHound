import os
import sys

import logging
import requests

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
sys.path.insert(0, project_root)

from template_web.backend.scripts.bbdd_papers.filter import filter_valid_results

# CrossRef: Límite de consultas por minuto.

CROSSREF_SEARCH_URL = "https://api.crossref.org/works"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

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

def get_paper_info_crossref(title):
    url = "https://api.crossref.org/works"
    params = {"query": title, "rows": 1}
    response = requests.get(url, params=params)
    data = response.json()
    
    if "message" in data and "items" in data["message"] and data["message"]["items"]:
        return data["message"]["items"][0].get("abstract")
    return None

if __name__ == "__main__":
    query = '("foam detection" OR "foam monitoring") AND (sensor OR "measurement system") AND (oil OR "industrial process") AND (precision OR reliability)'
    fetch_crossref_articles(query)
    # Ejemplo de uso
    title = "Deep learning for time-series forecasting"
    paper_info = get_paper_info_crossref(title)
    print(paper_info)
