import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def get_paper_info_semantic(title):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": title, "fields": "abstract", "limit": 1}
    response = requests.get(url, params=params)
    data = response.json()
    
    if "data" in data and data["data"]:
        return data["data"][0].get("abstract")
    return None

if __name__ == "__main__":
    title = "Deep learning for time-series forecasting"
    paper_info = get_paper_info_semantic(title)
    print(paper_info)

