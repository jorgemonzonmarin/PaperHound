import reflex as rx

class QueryState(rx.State):
    queries: list[str] = []  # Lista de preguntas introducidas
    input_value: str = ""  # Estado para almacenar el valor del input

    def set_input_value(self, value: str):
        """Actualiza el valor del input."""
        print(f"[LOG] Actualizando input_value: {value}")  # ✅ Log corregido
        self.input_value = value
        self.set()  # ✅ Forzar actualización del estado

    def add_question(self):
        """Agrega una nueva pregunta a la lista y actualiza el estado."""
        print(f"[LOG] Intentando agregar pregunta: {self.input_value}")
        if self.input_value and self.input_value.strip():
            self.queries.extend(self.input_value.strip().split(";"))
            print(f"[LOG] Pregunta agregada. Lista actual: {self.queries}")
            self.input_value = ""  # ✅ Limpia el input después de agregar
            self.set()  # ✅ ¡Forzar actualización del estado!
        else:
            print("[LOG] La pregunta estaba vacía o no era válida.")

    def remove_question(self, index: int):
        """Elimina una pregunta de la lista por su índice y actualiza el estado."""
        print(f"[LOG] Intentando eliminar pregunta en índice: {index}")
        if 0 <= index < len(self.queries):
            self.queries.pop(index)
            print(f"[LOG] Pregunta eliminada. Lista actual: {self.queries}")
            self.set()  # ✅ ¡Forzar actualización del estado!
        else:
            print("[LOG] Índice inválido o fuera de rango.")

    @rx.var
    def queries_text(self) -> str:
        """Devuelve todas las preguntas en formato de texto."""
        print(f"[LOG] Generando texto para el área de queries: {self.queries}.")
        return ";".join(self.queries)

    #@rx.var
    def queries_text_for_process(self) -> list[str]:  # ⚡ Ahora retorna una lista de Python
        return rx.foreach(self.queries)