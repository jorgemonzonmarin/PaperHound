import requests

def get_paper_info_semantic(title):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "fields": "title,abstract",
        "limit": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)

    if "data" in data and data["data"]:
        paper = data["data"][0]
        return {
            "title": paper.get("title", "No title found"),
            "abstract": paper.get("abstract", "No abstract available"),
            "doi": paper.get("doi", "No DOI found")
        }
    return None

title = "Deep learning for time-series forecasting"
paper_info = get_paper_info_semantic(title)
print(paper_info)
