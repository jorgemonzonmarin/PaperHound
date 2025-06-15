import csv
import reflex as rx
from pathlib import Path
from typing import List, Dict

class Item(rx.Base):
    """The item class."""

    pipeline: str
    status: str
    workflow: str
    timestamp: str
    duration: str

class DynamicTableState(rx.State):
    """State for managing a generic table with unknown columns."""

    items: List[Dict[str, str]] = []  # List of dictionaries where keys are column names
    columns: List[str] = []  # Dynamically detected column names

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page
    
    selected_file: str = ""  # ⬅ Nuevo campo

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[Dict[str, str]]:
        """Filters and sorts items based on user input."""
        items = self.items

        # Sort items based on selected column
        if self.sort_value and self.sort_value in self.columns:
            items = sorted(
                items,
                key=lambda item: str(item.get(self.sort_value, "")).lower(),
                reverse=self.sort_reverse,
            )

        # Filter items based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(item.get(col, "")).lower()
                    for col in self.columns
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 0
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> List[Dict[str, str]]:
        """Returns the current page of items."""
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def prev_page(self):
        """Go to the previous page."""
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        """Go to the next page."""
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        """Go to the first page."""
        self.offset = 0

    def last_page(self):
        """Go to the last page."""
        self.offset = (self.total_pages - 1) * self.limit

    def load_entries(self):
            """Carga los datos usando el archivo seleccionado."""
            try:
                filepath = Path(f"assets/papers_filtrados/{self.selected_file}")
                with filepath.open(encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    filtered_fieldnames = [f for f in reader.fieldnames if 'Titulo' in f or 'summary' in f]
                    filtered_rows = [{k: row[k] for k in filtered_fieldnames} for row in reader]
                    self.items = filtered_rows
                    self.columns = filtered_fieldnames
                    self.total_items = len(self.items)
            except Exception as e:
                print(f"Error loading file {self.selected_file}: {e}")
                self.items = []
                self.columns = []
                self.total_items = 0


    def toggle_sort(self, column: str):
        """Toggles sorting for a given column."""
        if column in self.columns:
            self.sort_value = column
            self.sort_reverse = not self.sort_reverse