import os
import sys
import csv
import logging
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from template_web.backend.scripts.search_papers import search_papers
from template_web.backend.scripts.bbdd_papers.arxiv import get_paper_info_arxiv
from template_web.backend.scripts.bbdd_papers.scopus_api import get_paper_info_scopus
from template_web.backend.scripts.bbdd_papers.open_alex_api import get_paper_info_openalex
from template_web.backend.scripts.bbdd_papers.cross_ref_api import get_paper_info_crossref
from template_web.backend.scripts.bbdd_papers.semantic_schoolar_api import get_paper_info_semantic

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

NOMBRE_CARPETA = "lista_papers"

QUERIES = [
    # 1. Búsqueda general sobre sensores y detección de espuma en evaporación de agua en aceite
    '("Time-of-Flight" OR "ToF" OR "Time of Flight") AND ("ultrasonic sensor" OR "ultrasound sensor" OR "ultrasonics") '
    'AND ("LIDAR" OR "LiDAR") AND ("level sensor" OR "level measurement") AND ("foam detection" OR "foam sensing" OR "bubble detection") '
    'AND ("oil-water evaporation" OR "water evaporation in oil" OR "oil-water separation" OR "oil phase transition")',
    
    # 2. Comparación de sensores con métricas de rendimiento
    '("Time-of-Flight" OR "ToF" OR "Time of Flight") AND ("ultrasonic sensor" OR "ultrasound sensor" OR "acoustic sensor") '
    'AND ("LIDAR" OR "LiDAR") AND ("foam detection" OR "foam monitoring" OR "bubble detection") '
    'AND ("accuracy" OR "precision" OR "response time" OR "reliability" OR "robustness" OR "sensitivity") '
    'AND ("oil-water evaporation" OR "oil-water separation") AND ("industrial process" OR "steel industry" OR "metallurgical industry")',

    # 3. Aplicaciones industriales y procesos en siderometalurgia
    '("Time-of-Flight" OR "ToF" OR "Time of Flight") AND ("ultrasonic sensor" OR "ultrasound sensor") AND ("LIDAR" OR "LiDAR") '
    'AND ("foam detection" OR "foam monitoring" OR "bubble detection") '
    'AND ("industrial process" OR "metallurgical industry" OR "steelmaking" OR "iron and steel industry") '
    'AND ("oil-water evaporation" OR "oil separation in metallurgical processes" OR "oil refining")',

    # 4. Comparación entre sensores para la detección de espuma
    '("sensor comparison" OR "sensor evaluation" OR "sensor benchmarking") AND ("Time-of-Flight" OR "ToF") AND ("ultrasonic sensor" OR "ultrasound sensor") '
    'AND ("LIDAR" OR "laser scanning") AND ("foam detection" OR "bubble detection") AND ("accuracy" OR "response time" OR "reliability") '
    'AND ("oil-water evaporation" OR "industrial process")',

    # 5. Evaluación de sensores en separación de fases
    '("foam detection" OR "foam monitoring" OR "bubble detection") AND ("oil-water separation" OR "phase separation in oil") '
    'AND ("sensor performance" OR "sensor evaluation") AND ("ToF" OR "ultrasonic sensor" OR "LIDAR") '
    'AND ("liquid-liquid separation" OR "multiphase flow")',

    # 6. Modelado y simulación de sensores
    '("sensor modeling" OR "sensor simulation") AND ("ToF" OR "Time-of-Flight") AND ("ultrasonic sensor") '
    'AND ("foam detection" OR "bubble sensing") AND ("oil-water evaporation" OR "industrial application")',

    # 7. Validación experimental en entornos industriales
    '("sensor validation" OR "experimental validation") AND ("Time-of-Flight" OR "ToF") AND ("ultrasonic sensor") '
    'AND ("LIDAR") AND ("foam detection" OR "bubble monitoring") AND ("oil-water evaporation") '
    'AND ("metallurgical process" OR "steel industry")',

    # 8. Evaluación de sensores bajo condiciones operativas variables
    '("sensor performance" OR "sensor reliability") AND ("variable operating conditions" OR "harsh environments") '
    'AND ("foam detection" OR "bubble detection") AND ("ToF" OR "ultrasonic sensor" OR "LIDAR") '
    'AND ("oil-water evaporation" OR "industrial process")',

    # 9. Aplicación de Machine Learning para la detección de espuma
    '("machine learning" OR "artificial intelligence") AND ("sensor fusion") AND ("foam detection" OR "bubble monitoring") '
    'AND ("Time-of-Flight" OR "ultrasonic sensor" OR "LIDAR") AND ("oil-water evaporation" OR "industrial separation process")',

    # 10. Optimización y reducción de errores en sensores
    '("sensor accuracy improvement" OR "error reduction in sensors") AND ("foam detection" OR "bubble detection") '
    'AND ("ToF" OR "ultrasonic sensor" OR "LIDAR") AND ("oil-water evaporation" OR "industrial process")',

    # 11. Aplicaciones de visión artificial en detección de espuma
    '("computer vision" OR "image processing") AND ("foam detection" OR "bubble detection") '
    'AND ("LIDAR" OR "Time-of-Flight") AND ("oil-water separation" OR "phase separation in oil")',

    # 12. Métodos ópticos avanzados en detección de espuma
    '("optical sensing" OR "laser-based detection") AND ("foam monitoring" OR "bubble detection") '
    'AND ("LIDAR" OR "Time-of-Flight") AND ("oil-water separation" OR "industrial fluid measurement")',

    # 13. Uso de sensores en flujos multifásicos
    '("multiphase flow" OR "two-phase flow") AND ("foam detection" OR "bubble detection") '
    'AND ("ultrasonic sensor" OR "ToF" OR "LIDAR") AND ("oil-water interface" OR "oil separation process")',

    # 14. Sensores ultrasónicos de alta frecuencia para la detección de espuma
    '("high-frequency ultrasound" OR "high-resolution ultrasonic sensor") AND ("foam detection" OR "bubble sensing") '
    'AND ("oil-water evaporation" OR "industrial oil separation")',

    # 15. Aplicaciones en refinerías y procesos petroquímicos
    '("oil refining" OR "petrochemical industry") AND ("foam detection" OR "bubble detection") '
    'AND ("ultrasonic sensor" OR "Time-of-Flight" OR "LIDAR")',

    # 16. Implementación de sensores en procesos de evaporación térmica
    '("thermal evaporation" OR "steam-assisted separation") AND ("foam monitoring" OR "bubble detection") '
    'AND ("sensor performance" OR "sensor optimization") AND ("ToF" OR "ultrasonic sensor" OR "LIDAR")'
]

# Lista de funciones para obtener abstracts, en orden de preferencia
ABSTRACT_FUNCTIONS = [
    get_paper_info_scopus,
    get_paper_info_semantic,
    get_paper_info_arxiv,
    get_paper_info_openalex,
    get_paper_info_crossref,
]

def get_valid_abstract(title):
    """
    Intenta obtener el abstract de un paper usando varias fuentes, deteniéndose al encontrar uno válido.
    """
    for func in ABSTRACT_FUNCTIONS:
        abstract = func(title)
        if abstract:
            return abstract
    return "No abstract available"

def generate_filename(base_name):
    """
    Genera un nombre de archivo único para evitar sobrescribir.
    """
    filename = f"{base_name}.csv"
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_name}_{counter}.csv"
        counter += 1
    return filename

def save_to_csv(file_path, data):
    """
    Guarda los datos en un archivo CSV de forma progresiva, asegurando que los campos con comas sean manejados correctamente.
    """
    file_exists = os.path.exists(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["Query", "Titulo", "DOI", "Revista", "Abstract"], quotechar='"', quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "Query": data["Query"],
            "Titulo": data["Titulo"],
            "DOI": data["DOI"],
            "Revista": data["Revista"],
            "Abstract": data["Abstract"].replace('\n', ' ')  # Asegurar que no haya saltos de línea
        })

def search_and_save_papers(queries=QUERIES):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_file = os.path.join(current_dir, '..', '..', '..', 'assets', 'papers_encontrados')
    logging.info(current_dir)
    filename = datetime.now().strftime("%Y-%m-%d") + "_Papers_encontrados"
    filename_correct = generate_filename(filename)
    file_path = os.path.join(path_file, filename_correct)
    try: 
        for query in queries:
            logging.info(f"🔎 Procesando query: {query}")
            papers = search_papers([query], max_results=5)
            
            for paper in papers:
                title = paper["titulo"]
                abstract = get_valid_abstract(title)
                
                data = {
                    "Query": query,
                    "Titulo": title,
                    "DOI": paper["doi"],
                    "Revista": paper["revista"],
                    "Abstract": abstract.replace('\n', ' ')  # Remover saltos de línea en el abstract
                }
                
                save_to_csv(file_path, data)
                logging.info(f"✅ Guardado: {title} en {file_path}")
    except Exception as e:
        logging.error(f"Error durante la búsqueda y guardado de papers: {e}")
    finally:
        return file_path

if __name__ == "__main__":
    search_and_save_papers()
