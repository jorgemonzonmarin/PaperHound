import reflex as rx
import logging
from datetime import datetime

from ..backend.query_state import QueryState
#from .scripts.procesar_papers import procesar_articulos, verificar_y_reprocesar, PAPERS_A_ANALIZAR
from .scripts.search_and_save_papers import search_and_save_papers

class ProcessingState(rx.State):
    """Estado para gestionar la ejecución del procesamiento de artículos."""
    
    status: str = "Ready"  # Estado inicial
    
    @rx.event
    def start_processing(self):
        """Inicia el procesamiento de artículos y actualiza el estado."""
        self.status = "Processing..."
        self.set()  # Actualizar UI
        
        try: 
            logging.info("Iniciando la búsqueda de artículos")

            # 🔹 Obtener queries como lista de Python desde el backend
            queries_list = QueryState.questions_text_for_process

            # 🔹 Registrar la lista para depuración
            logging.info(f"Queries obtenidas: {queries_list}; tipo {type(queries_list)}")

            # 🔹 Llamar a la función con la lista nativa
            search_and_save_papers(queries=queries_list)
        except Exception as e:
            logging.error(f"Error durante la búsqueda: {e}")
            self.status = "Error ❌"
        
        try:
            logging.info("Iniciando el procesamiento de artículos...")
            
            # Generar el nombre del archivo de salida
            
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            output_path = f"articulos_filtrados_{fecha_actual}.csv"

            # Ejecutar funciones de procesamiento
            #procesar_articulos(csv_path=PAPERS_A_ANALIZAR, output_path=output_path)
            #verificar_y_reprocesar(output_path)

            # Actualizar el estado a completado
            self.status = "Completed ✅"
        
        except Exception as e:
            logging.error(f"Error durante el procesamiento: {e}")
            self.status = "Error ❌"
        
        self.set()  # Actualizar UI nuevamente
