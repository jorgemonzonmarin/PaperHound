import reflex as rx
import logging

from datetime import datetime

from ..backend.query_state import QueryState
from ..backend.topic_state import TopicState
from ..backend.questions_state import QuestionState
from .scripts import procesar_papers as pp
#from .scripts.procesar_papers import procesar_articulos, verificar_y_reprocesar, PAPERS_A_ANALIZAR, TOPIC, QUESTIONS
from .scripts.search_and_save_papers import search_and_save_papers

# from .rx_procesar_papers import RunInThreadState
from .run_in_thread import run_in_thread

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
                queries_list = queries_state.queries  # ⚡ Ahora retorna una lista de Python
                # 🔹 Registrar la lista para depuración
                logging.info(f"Queries obtenidas: {queries_list}; tipo {type(queries_list)}")

                # 🔹 Llamar a la función con la lista nativa
                search_and_save_papers(queries=queries_list)
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
                output_path = f"articulos_filtrados_{fecha_actual}.csv"

            # Ejecutar funciones de procesamiento
            procesamiento_completado = await run_in_thread(pp.procesar_articulos(csv_path=pp.PAPERS_A_ANALIZAR, output_path=output_path))
            verificacion_completada = await run_in_thread(pp.verificar_y_reprocesar(output_path))
            
            #run_in_threaded_state = self.get_state(RunInThreadState)
            #
            #await run_in_threaded_state.run_procesar_articulos()
            #await run_in_threaded_state.run_verificar_y_reprocesar()

            
            logging.info("Procesamiento finalizado")
            
            # Actualizar el estado a completado
            #rx.cond(RunInThreadState.tasks) not None:
            #last_task = RunInThreadState.tasks[-1]
            #if last_task.status == "Complete":
            #    logging.info("Procesamiento completado exitosamente.")
            #    self.status = "Completed ✅"
            #else:
            #    logging.error(f"Error en el procesamiento: {last_task.status}")

            async with self:
                self.status = "Procesando"
            
        
        except Exception as e:
            async with self:
                logging.error(f"Error durante el procesamiento: {e}")
                self.status = "Error ❌"
        
        self.set()  # Actualizar UI nuevamente
