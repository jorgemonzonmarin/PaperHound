import logging

from scholarly import scholarly
from .filter import filter_valid_results

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

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

if __name__ == "__main__":
    query = '("foam detection" OR "foam monitoring") AND (sensor OR "measurement system") AND (oil OR "industrial process") AND (precision OR reliability)'
    for result in fetch_scholar_articles(query): logging.info(result)