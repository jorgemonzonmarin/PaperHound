import re
import os
import reflex as rx

class QuestionState(rx.State):
    questions: list[str] = []  # Lista de preguntas introducidas
    input_value: str = ""  # Estado para almacenar el valor del input
    selected_file: str = ""
    _file_options: list[str] = []  # atributo privado interno

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
    
    @rx.var
    def file_options(self) -> list[str]:
        return self._file_options
    
    def load_file_options(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        questions_folder_path = os.path.join(current_dir, "..", "..", "assets", "filtro_preguntas")
        if os.path.exists(questions_folder_path):
            self._file_options = [
                f for f in os.listdir(questions_folder_path)
                if f.endswith(".txt") or f.endswith(".csv")
            ]

    def set_selected_file(self, filename: str):
        self.selected_file = filename

    async def load_questions_from_selected_file(self):
        if not self.selected_file:
            return

        current_dir = os.path.dirname(os.path.abspath(__file__))
        questions_path = os.path.join(current_dir, "..", "..", "assets", "filtro_preguntas", self.selected_file)
        if not os.path.exists(questions_path):
            return

        with open(questions_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            print(f"[LOG] Cargando preguntas desde el archivo: {self.selected_file}")
            print(f"[LOG] Total de líneas leídas: {len(lines)}")

        used_numbers = set()
        for q in self.questions:
            match = re.match(r"^(\d+)", q.strip())
            if match:
                used_numbers.add(int(match.group(1)))

        next_number = 1 if not used_numbers else max(used_numbers) + 1

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            match = re.match(r"^(\d+)\s*(.*)", stripped)
            if match:
                number = int(match.group(1))
                if number not in used_numbers:
                    self.questions.append(stripped)
                    used_numbers.add(number)
            else:
                while next_number in used_numbers:
                    next_number += 1
                question = f"{next_number} {stripped}"
                self.questions.append(question)
                used_numbers.add(next_number)