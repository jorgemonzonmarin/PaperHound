import requests
import xml.etree.ElementTree as ET

SCOPUS_API_KEY = "28ed61df3b550a39c575b5270b49f254"

def get_paper_info_arxiv(title):
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": f"ti:{title}", "start": 0, "max_results": 1}
    
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entry = root.find("atom:entry", ns)
    
    if entry is not None:
        return entry.find("atom:summary", ns).text
    return None

def get_paper_info_semantic(title):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {"query": title, "fields": "abstract", "limit": 1}
    response = requests.get(url, params=params)
    data = response.json()
    
    if "data" in data and data["data"]:
        return data["data"][0].get("abstract")
    return None

def get_paper_info_scopus(title):
    url = "https://api.elsevier.com/content/search/scopus"
    headers = {"X-ELS-APIKey": SCOPUS_API_KEY, "Accept": "application/json"}
    params = {"query": f"TITLE({title})", "count": 1}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if "search-results" in data and "entry" in data["search-results"] and data["search-results"]["entry"]:
        return data["search-results"]["entry"][0].get("dc:description")
    return None

def get_paper_info_openalex(title):
    url = "https://api.openalex.org/works"
    params = {"filter": f"display_name.search:{title}", "per_page": 1}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if "results" in data and data["results"]:
        paper = data["results"][0]
        abstract_dict = paper.get("abstract_inverted_index", {})
        if abstract_dict:
            abstract_words = sorted(
                [(pos, word) for word, positions in abstract_dict.items() for pos in positions]
            )
            return " ".join(word for _, word in abstract_words)
    return None

def get_paper_info_crossref(title):
    url = "https://api.crossref.org/works"
    params = {"query": title, "rows": 1}
    response = requests.get(url, params=params)
    data = response.json()
    
    if "message" in data and "items" in data["message"] and data["message"]["items"]:
        return data["message"]["items"][0].get("abstract")
    return None

if __name__ == "__main__":
    title = "Deep learning for time-series forecasting"
    
    print("ArXiv:", get_paper_info_arxiv(title))
    print("Semantic Scholar:", get_paper_info_semantic(title))
    print("Scopus:", get_paper_info_scopus(title))
    print("OpenAlex:", get_paper_info_openalex(title))
    print("CrossRef:", get_paper_info_crossref(title))
