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

if __name__ == "__main__":
    import pandas as pd
    import logging
    
    logging.basicConfig(level=logging.INFO)
    
    # Cargar el archivo de entrada
    input_path = r"C:\Git_repository\PaperHound\template_web\template_web\backend\scripts\data.csv"
    output_path = r"C:\Git_repository\PaperHound\template_web\template_web\backend\scripts\articulos_filtrados_ordenados.csv"
    
    df = pd.read_csv(input_path)
    
    # Ordenar el DataFrame por la cuenta de 'Yes'

    df = sort_by_yes_count(df)
                
    df.to_csv(output_path, index=False)
    logging.info(f"Reprocesamiento completado. Resultados guardados en {output_path}")