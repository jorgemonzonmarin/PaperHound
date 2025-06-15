import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def get_paper_info_semantic(title):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "fields": "title,abstract",
        "limit": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    logging.debug(data)

    if "data" in data and data["data"]:
        paper = data["data"][0]
        return {
            "title": paper.get("title", "No title found"),
            "abstract": paper.get("abstract", "No abstract available"),
            "doi": paper.get("doi", "No DOI found")
        }
    return None

if __name__ == "__main__":
    title = "Deep learning for time-series forecasting"
    paper_info = get_paper_info_semantic(title)
    print(paper_info)

