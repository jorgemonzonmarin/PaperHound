import requests

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

# Ejemplo de uso
title = "Deep learning for time-series forecasting"
paper_info = get_paper_info_openalex(title)
print(paper_info)
