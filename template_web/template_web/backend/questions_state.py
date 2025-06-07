import reflex as rx

class QuestionState(rx.State):
    questions: list[str] = []  # Lista de preguntas introducidas
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
            self.questions.extend(self.input_value.strip().split(";"))
            self.questions = self.questions = sorted(
                [q for q in self.questions if q.strip().split('.')[0].isdigit()],
                key=lambda x: int(x.strip().split('.')[0])
            )
            print(f"[LOG] Pregunta agregada. Lista actual: {self.questions}")
            self.input_value = ""  # ✅ Limpia el input después de agregar
            self.set()  # ✅ ¡Forzar actualización del estado!
        else:
            print("[LOG] La pregunta estaba vacía o no era válida.")

    def remove_question(self, index: int):
        """Elimina una pregunta de la lista por su índice y actualiza el estado."""
        print(f"[LOG] Intentando eliminar pregunta en índice: {index}")
        if 0 <= index < len(self.questions):
            self.questions.pop(index)
            print(f"[LOG] Pregunta eliminada. Lista actual: {self.questions}")
            self.set()  # ✅ ¡Forzar actualización del estado!
        else:
            print("[LOG] Índice inválido o fuera de rango.")

    @rx.var
    def questions_text(self) -> str:
        """Devuelve todas las preguntas en formato de texto."""
        print(f"[LOG] Generando texto para el área de preguntas: {self.questions}")
        return ";".join(self.questions,)
