import time
import logging
import requests
import xml.etree.ElementTree as ET

from .candidatos_busqueda_abstract.xarvy import fetch_arxiv_articles
from .candidatos_busqueda_abstract.scopus_api import fetch_scopus_articles
from .candidatos_busqueda_abstract.cross_ref_api import fetch_crossref_articles
from .candidatos_busqueda_abstract.open_alex_api import fetch_openalex_articles
from .candidatos_busqueda_abstract.google_schoolar import fetch_scholar_articles

CORE_SEARCH_URL = "https://api.core.ac.uk/v3/search/works"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def search_papers(queries, max_results=10):
    all_results = []
    for query in queries:
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