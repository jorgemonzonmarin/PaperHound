import logging
import requests
from .filter import filter_valid_results

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

def get_paper_info(title):
    url = "https://api.crossref.org/works"
    params = {"query": title, "rows": 1}  # Busca el paper más relevante
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    
    if "message" in data and "items" in data["message"] and data["message"]["items"]:
        paper = data["message"]["items"][0]
        return {
            "title": paper.get("title", ["No title found"])[0],
            "abstract": paper.get("abstract", "No abstract available"),
            "doi": paper.get("DOI", "No DOI found")
        }
    return None

if __name__ == "__main__":
    query = '("foam detection" OR "foam monitoring") AND (sensor OR "measurement system") AND (oil OR "industrial process") AND (precision OR reliability)'
    fetch_crossref_articles(query)
    # Ejemplo de uso
    title = "Deep learning for time-series forecasting"
    paper_info = get_paper_info(title)
    print(paper_info)
