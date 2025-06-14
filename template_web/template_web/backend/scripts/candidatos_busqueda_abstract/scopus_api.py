import requests

API_KEY = "28ed61df3b550a39c575b5270b49f254"

def get_paper_info_scopus(title):
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {"X-ELS-APIKey": API_KEY, "Accept": "application/json"}
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

    title = "Deep learning for time-series forecasting"
    paper_info = get_paper_info_scopus(title)
    print(paper_info)
