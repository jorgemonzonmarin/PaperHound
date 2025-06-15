def filter_valid_results(results):
    return [paper for paper in results if paper.get("titulo") and paper["titulo"] != "No disponible"]