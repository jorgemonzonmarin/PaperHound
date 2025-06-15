import logging
import requests

from .filter import filter_valid_results

# OpenAlex: Ilimitado pero con límite de velocidad.

OPENALEX_SEARCH_URL = "https://api.openalex.org/works"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

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

def get_paper_info_openalex(title):
    url = "https://api.openalex.org/works"
    params = {"filter": f"display_name.search:{title}", "per_page": 1}

    response = requests.get(url, params=params)
    data = response.json()

    if "results" in data and data["results"]:
        paper = data["results"][0]

        # Procesar el abstract
        abstract_dict = paper.get("abstract_inverted_index", {})
        if abstract_dict:
            # Ordenar las palabras por su posición en el texto
            abstract_words = sorted(
                [(pos, word) for word, positions in abstract_dict.items() for pos in positions]
            )
            abstract_text = " ".join(word for _, word in abstract_words)
        else:
            abstract_text = "No abstract available"

        return {
            "title": paper.get("display_name", "No title found"),
            "abstract": abstract_text,
            "doi": paper.get("doi", "No DOI found"),
            "link": paper.get("id", "No link available")
        }
    
    return None

if __name__ == "__main__":
    query = '("foam detection" OR "foam monitoring") AND (sensor OR "measurement system") AND (oil OR "industrial process") AND (precision OR reliability)'
    fetch_openalex_articles(query)    
    title = "Deep learning for time-series forecasting"
    paper_info = get_paper_info_openalex(title)
    print(paper_info)
