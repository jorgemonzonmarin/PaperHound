import reflex as rx
import logging
import os 
from datetime import datetime

from ..backend.query_state import QueryState
from ..backend.topic_state import TopicState
from ..backend.questions_state import QuestionState
from .scripts import procesar_papers as pp
#from .scripts.procesar_papers import procesar_articulos, verificar_y_reprocesar, PAPERS_A_ANALIZAR, TOPIC, QUESTIONS
from .scripts.search_and_save_papers import search_and_save_papers

# from .rx_procesar_papers import RunInThreadState
from .run_in_thread import run_in_thread
import threading
import asyncio

papers_filepath = None  # Variable global para almacenar la ruta del archivo de artículos encontrados

class ProcessingState(rx.State):
    """Estado para gestionar la ejecución del procesamiento de artículos."""
    
    status: str = "Ready"  # Estado inicial
    
    @rx.event(background=True) 
    async def start_processing(self):
        async with self:
            """Inicia el procesamiento de artículos y actualiza el estado."""
            self.status = "Processing..."
            self.set()  # Actualizar UI
            
            try: 
                logging.info("Iniciando la búsqueda de artículos")

                # 🔹 Obtener queries como lista de Python desde el backend
                #queries_list = QueryState.questions_text_for_process
                queries_state = await self.get_state(QueryState) 
                queries_list = queries_state.queries  
                # 🔹 Registrar la lista para depuración
                logging.info(f"Queries obtenidas: {queries_list}; tipo {type(queries_list)}")

                # 🔹 Llamar a la función con la lista nativa
                papers_filepath = search_and_save_papers(queries=queries_list) #FIXME: Incluir la función en un hilo para evitar bloqueos
                
            except Exception as e:
                logging.error(f"Error durante la búsqueda: {e}")
                self.status = "Error ❌"
        
        try:
            async with self:
                logging.info("Iniciando el procesamiento de artículos...")
                
                # Generar el nombre del archivo de salida
                topic_state = await self.get_state(TopicState) 
                pp.TOPIC = topic_state.topic[0]
                
                questions_state = await self.get_state(QuestionState) 
                questions_list = questions_state.questions  # ⚡ Ahora retorna una lista de PythonQUESTIONS_LIST
                pp.QUESTIONS = '\n'.join(questions_list)
                
                fecha_actual = datetime.now().strftime("%Y-%m-%d")
                current_dir = os.path.dirname(os.path.abspath(__file__))
                path_file = os.path.join(current_dir, '..', '..', 'assets', 'papers_filtrados')
                logging.info(current_dir)
                
                output_file = f"{fecha_actual}_articulos_filtrados.csv"
                filtered_papers_filepath = os.path.join(path_file, output_file)
            # Ejecutar funciones de procesamiento
            procesamiento_ready = threading.Event()
            def procesar_articulos_thread():
                try:
                    procesamiento_completado = pp.procesar_articulos(csv_path=papers_filepath, output_path=filtered_papers_filepath)                
                except Exception as e:
                    logging.error(f"Error en el procesamiento de artículos: {e}")
                else:
                    procesamiento_ready.set() 
            
            threading.Thread(target=procesar_articulos_thread, daemon=True).start()

            while not procesamiento_ready.is_set():
                logging.debug("El procesamiento todavía no ha terminado...")
                await asyncio.sleep(10.0)  

            verificacion_ready = threading.Event()
            def verificar_articulos_thread():
                try:
                    verificacion_completada = pp.verificar_y_reprocesar(filtered_papers_filepath)                
                except Exception as e:
                    logging.error(f"Error en la verificación de artículos: {e}")
                else:
                    verificacion_ready.set() 
            
            threading.Thread(target=verificar_articulos_thread, daemon=True).start()

            while not verificacion_ready.is_set():
                logging.debug("La verificación todavía no ha terminado...")
                await asyncio.sleep(10.0)

            logging.info("Procesamiento finalizado")

            async with self:
                self.status = "Procesessing completed ✅"
            
        except Exception as e:
            async with self:
                logging.error(f"Error durante el procesamiento: {e}")
                self.status = "Error ❌"
        
        self.set()  # Actualizar UI nuevamente
