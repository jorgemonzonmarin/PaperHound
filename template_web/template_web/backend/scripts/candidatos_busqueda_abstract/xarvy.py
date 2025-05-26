import requests
import xml.etree.ElementTree as ET

def get_paper_info_arxiv(title):
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": f"ti:{title}", "start": 0, "max_results": 1}

    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entry = root.find("atom:entry", ns)
    print(entry)
    if entry is not None:
        return {
            "title": entry.find("atom:title", ns).text,
            "abstract": entry.find("atom:summary", ns).text,
            "link": entry.find("atom:id", ns).text
        }
    return None

title = "Deep learning for time-series forecasting"
paper_info = get_paper_info_arxiv(title)
print(paper_info)
