import pandas as pd
import ollama
#from transformers import pipeline
import os
import re
from datetime import datetime
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


PAPERS_A_ANALIZAR = r"C:\Users\JorgeMonzonMarin\GDI PROYECTOS Y MONTAJES, S.A\TESIS-Jorge - Documentos\Memoria\Papers\Sensor_espuma\lista_papers\2025-03-03_Papers_encontrados.csv"
NUM_PREGUNTAS = 13

TOPIC = """The comparative evaluation of sensors for foam detection in water 
        evaporation processes in oil within the steel and metallurgical industry, 
        with a focus on process control and industrial instrumentation."""

QUESTIONS = """
            1. Does the paper analyze water evaporation processes in oil within the steel and metallurgical industry or a similar industry?
            2. Does the study evaluate foam detection in these processes?
            3. Are sensor technologies such as ToF, ultrasonic, LIDAR, or level sensors mentioned or compared?
            4. Does the paper present experimental results or simulations on foam detection in industrial environments?
            5. Does it analyze the accuracy, reliability, or response time of sensors in foam detection?
            6. Does the paper mention both controlled and uncontrolled operating conditions?
            7. Is the focus of the paper related to automation, process control, or industrial instrumentation?
            8. Does the paper specifically mention the steel and metallurgical industry?
            9. Does the paper include a quantitative comparison of different sensors for foam detection?
            10. Are the data presented obtained in a real industrial environment or under similar conditions?
            11. Does the paper propose improvements or innovations in foam detection compared to existing technologies?
            12. Do the authors have academic or industrial affiliations relevant to the topic?
            13. Has the paper been published in a reputable journal or conference related to sensors, process control, or industrial engineering?
            """

def create_dataframe(questions_count=NUM_PREGUNTAS):
    """Crea un DataFrame con columnas estándar y tantas preguntas como sea necesario."""
    columns = ["Titulo", "DOI"] + \
              [f"{i+1}. explained" for i in range(questions_count)] + \
              [f"{i+1}. summary" for i in range(questions_count)] + \
              ["Revista", "Respuesta" , "Abstract"]
    
    df = pd.DataFrame(columns=columns)
    return df

def preguntar_ollama(prompt):
    answer = ollama.chat(model="deepseek-r1:8b", messages=[{"role": "user", "content": prompt}])
    return answer

def crea_prompt(titulo, abstract, preguntas=QUESTIONS):
    
    text = f"""
    You are an advanced AI designed for structured and precise information processing. Your responses must be highly synthesized, strictly ordered, and formatted exactly as instructed. Your primary objective is to generate well-structured lists with precise formatting, avoiding any unnecessary text, reordering, or alternation of list types.
    I am conducting a systematic review that investigates {TOPIC}. I have run my ScienceDirect search and would like you to assist with screening by title and abstract.
    
    Carefully analyze the provided text and respond **strictly** according to the following instructions. **Any deviation from the required format will be considered incorrect.**

    ### **Response Format (MANDATORY)**
    You must generate **TWO DISTINCT LISTS** in the specified format:  

    #### **1. Explained List**  
    - Each item must be formatted as: `{{question_number}}. explained {{answer}} - {{justification}}`  
    - The answer must be **'Yes'**, **'No'**, or **'Not Determined'**.  
    - A **brief but clear justification** must follow the answer, separated by a hyphen (-).  
    - Example:  

    1. explained Yes - The abstract explicitly discusses the use of ToF sensors for foam detection.
    2. explained No - The paper focuses on general fluid dynamics without mentioning foam detection.


    #### **2. Summary List**  
    - Each item must be formatted as: `{{question_number}}. summary {{answer}}`  
    - The answer must be **only** 'Yes', 'No', or 'Not Determined'.  
    - **No additional text, justification, or explanation** is allowed in this list.  
    - Example:  

    1. summary Yes
    2. summary No


    ### **Important Rules (STRICT COMPLIANCE REQUIRED)**
    1. **Do not merge the lists.** The two lists must be clearly separated.  
    2. **Do not alternate between explained and summary responses.** The entire **Explained List** must come first, followed by the **Summary List**.  
    3. **Do not add extra text, commentary, or formatting.** The response must strictly follow the described structure.  
    4. **If the abstract does not provide enough information to answer a question, respond with 'Not Determined'.**  
    5. **Any failure to follow this structure will be considered incorrect.**

    ### **Paper Details**
    - **Title:** '{titulo}'  
    - **Abstract:** '{abstract}'
    - **Qestions:** '{preguntas}'

    Now, **strictly follow the instructions and generate the two required lists.**

"""
    return text
    #return "\n".join([f"{pregunta}\n{texto}" for pregunta in preguntas])

def cargar_datos(csv_path):
    """Carga el CSV y filtra los artículos con abstracts válidos."""
    df = pd.read_csv(csv_path)
    df = df[df["Abstract"] != "Fuente no soportada"]
    return df

def analizar_articulo(titulo, abstract, doi, revista):
    """Utiliza un modelo de lenguaje para responder preguntas sobre el artículo."""
    
    prompt = crea_prompt(titulo, abstract, QUESTIONS)
    respuesta = preguntar_ollama(prompt)
    
    logging.debug(type(respuesta.message.content))
    logging.debug('----------------Respuesta:-----------------')
    logging.debug(respuesta.message.content)
    logging.debug('----------------Dataframe:-----------------')
    
    
    df = process_text(text=respuesta.message.content, title=titulo, abstract=abstract, doi=doi, revista=revista)
    return df

def process_text(title, abstract, doi, text, revista, questions_count=NUM_PREGUNTAS):
    """Procesa el texto y extrae las respuestas para asociarlas a cada columna del DataFrame."""
    explained_matches = re.findall(r'(\d+)\. explained (.*?)\n', text)
    summary_matches = re.findall(r'(\d+)\. summary (.*?)\n', text)
    
    logging.debug("----------------Matches---------------------")
    logging.debug(explained_matches)
    logging.debug(summary_matches)
    
    # Crear el DataFrame
    df = create_dataframe(questions_count)
    
    # Diccionario temporal para almacenar respuestas
    row_data = {col: None for col in df.columns}
    
    logging.debug("Bucle for explained")
    
    for num, explanation in explained_matches:
        column_name = f"{num}. explained"
        logging.debug('Explained:', explanation)
        logging.debug('Column name:', column_name)
        if column_name in df.columns:
            row_data[column_name] = explanation
            logging.debug("Coincidencia en explained")
        else:
            logging.debug("No hay coincidencia en explained")
    
    logging.debug("Bucle for summary")
    
    for num, summary in summary_matches:
        column_name = f"{num}. summary"
        logging.debug('Summary:', summary)
        logging.debug('Column name:', column_name)
        if column_name in df.columns:
            row_data[column_name] = summary.strip()
            logging.debug("Coincidencia en summary")
        else:
            logging.debug("No hay coincidencia en summary")
    
    # Simulación de los metadatos del documento
    row_data["Titulo"] = title
    row_data["DOI"] = doi
    row_data["Abstract"] = abstract
    row_data["Revista"] = revista
    row_data["Respuesta"] = text.replace("\n", " ").replace(",", ";")
    
    # Convertir a DataFrame temporal y concatenar
    temp_df = pd.DataFrame([row_data])
    logging.debug("Temp_df:", temp_df)
    temp_df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, temp_df], ignore_index=True, copy=False, sort=False)
    return df

def procesar_articulos(csv_path, output_path):
    """Carga los artículos, analiza su relevancia y guarda los resultados en un nuevo CSV."""
    logging.info(f"Cargando datos de {csv_path}")
    logging.info(f"Topic a emplear : {TOPIC}")
    logging.info(f"Preguntas a emplear : {QUESTIONS}")
    df = cargar_datos(csv_path)
    df_respuestas = create_dataframe(questions_count=NUM_PREGUNTAS)
    logging.debug("Cargando modelo de lenguaje...")
    #modelo = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1")
    
    resultados = []
    
    logging.debug("Procesando artículos...")
    for index, row in df.iterrows():
        logging.info(f"Procesando artículo {index}/{len(df)}: {row['Titulo']}")
        titulo, abstract, doi = row["Titulo"], row["Abstract"], row["DOI"]
        df_respuestas_paper = analizar_articulo(titulo=titulo, abstract=abstract, doi=doi, revista=row["Revista"])
        df_respuestas = pd.concat([df_respuestas, df_respuestas_paper], ignore_index=True, copy=False, sort=False)
        df_respuestas.to_csv(output_path, index=False)
        logging.info(f"Avances guardados en: {output_path}")
        
    
    logging.debug("Guardando resultados en output_path")
    #df_resultados = pd.DataFrame(resultados)
    df_respuestas.to_csv(output_path, index=False)
    logging.info(f"Proceso completado. Resultados guardados en {output_path}")

    return True

def sort_by_yes_count(df):
    # Seleccionar columnas que terminan en 'summary'
    summary_cols = [col for col in df.columns if col.strip().endswith('summary')]
    
    # Contar cuántos 'Yes' hay por fila, asegurando que los valores sean strings
    df['Yes Count'] = df[summary_cols].apply(
        lambda row: sum(str(cell).strip() == 'Yes' for cell in row),
        axis=1
    )
    
    # Ordenar el DataFrame por la cuenta de 'Yes'
    sorted_df = df.sort_values(by='Yes Count', ascending=False).reset_index(drop=True)
    
    return sorted_df
    
def verificar_y_reprocesar(output_path, threshold=0.2):
    """Verifica el CSV y reprocesa artículos con más del 20% de respuestas 'summary' como NaN."""
    df = pd.read_csv(output_path)
    needs_reprocessing = []
    for index, row in df.iterrows():
        summary_columns = [col for col in df.columns if col.endswith('. summary')]
        nan_count = row[summary_columns].isna().sum()
        if nan_count / len(summary_columns) > threshold:
            needs_reprocessing.append(index)
            
    while needs_reprocessing:
        for index in needs_reprocessing:
            row = df.loc[index]
            titulo, abstract, doi, revista = row["Titulo"], row["Abstract"], row["DOI"], row["Revista"]
            logging.info(f"Reprocesando artículo {index}/{len(needs_reprocessing)}: {titulo}")
            df_respuestas_paper = analizar_articulo(titulo=titulo, abstract=abstract, doi=doi, revista=revista)
            
            # Actualizar la fila con los nuevos datos
            for col in df_respuestas_paper.columns:
                df.at[index, col] = df_respuestas_paper.at[0, col]
        # Verificar nuevamente si hay artículos que necesitan reprocesarse
        needs_reprocessing = []
        
        for index, row in df.iterrows():
            summary_columns = [col for col in df.columns if col.endswith('. summary')]
            nan_count = row[summary_columns].isna().sum()
            if nan_count / len(summary_columns) > threshold:
                needs_reprocessing.append(index)
    
    df = sort_by_yes_count(df)
                
    df.to_csv(output_path, index=False)
    logging.info(f"Reprocesamiento completado. Resultados guardados en {output_path}")

    return True

if __name__ == "__main__":
    # Uso del script
    
    df = create_dataframe(questions_count=13)
    
    # Generar el nombre del archivo con la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    base_output_path = f"articulos_filtrados_{fecha_actual}.csv"
    output_path = base_output_path

    # Verificar si el archivo ya existe y agregar un sufijo si es necesario
    contador = 1
    while os.path.exists(output_path):
        output_path = f"articulos_filtrados_{fecha_actual}_{contador}.csv"
        contador += 1
        
    procesar_articulos(csv_path=PAPERS_A_ANALIZAR, output_path=output_path)

    verificar_y_reprocesar(output_path)
    
    
