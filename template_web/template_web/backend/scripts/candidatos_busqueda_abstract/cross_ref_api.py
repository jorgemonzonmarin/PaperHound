import requests

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
    # Ejemplo de uso
    title = "Deep learning for time-series forecasting"
    paper_info = get_paper_info(title)
    print(paper_info)
