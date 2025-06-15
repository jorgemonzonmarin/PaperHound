import time
import asyncio
import logging
import dataclasses
import reflex as rx
from datetime import datetime
from .scripts import procesar_papers as pp

def quick_blocking_function():
    time.sleep(0.5)
    return "Quick task completed successfully!"


def slow_blocking_function():
    time.sleep(3.0)
    return "This should never be returned due to timeout!"


@dataclasses.dataclass
class TaskInfo:
    result: str = "No result yet"
    status: str = "Idle"


class RunInThreadState(rx.State):
    tasks: list[TaskInfo] = []

    @rx.event(background=True)
    async def run_quick_task(self):
        """Run a quick task that completes within the timeout."""
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        output_path = f"articulos_filtrados_{fecha_actual}.csv"
    
        async with self:
            task_ix = len(self.tasks)
            self.tasks.append(
                TaskInfo(status="Running quick task...")
            )
            task_info = self.tasks[task_ix]

        try:
            result = await rx.run_in_thread(
                pp.procesar_articulos(csv_path=pp.PAPERS_A_ANALIZAR, output_path=output_path)
            )
            async with self:
                task_info.result = result
                task_info.status = "Complete"
        except Exception as e:
            async with self:
                task_info.result = f"Error: {str(e)}"
                task_info.status = "Failed"
    
    @rx.event(background=True)
    async def run_procesar_articulos(self):
        """Run a quick task that completes within the timeout."""
        print("Iniciando el procesamiento de artículos...")
        rx.console_log("Iniciando el procesamiento de artículos...")
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        output_path = f"articulos_filtrados_{fecha_actual}.csv"
    
        async with self:
            task_ix = len(self.tasks)
            self.tasks.append(
                TaskInfo(status="Running quick task...")
            )
            task_info = self.tasks[task_ix]

        try:
            result = await rx.run_in_thread(
                pp.procesar_articulos(csv_path=pp.PAPERS_A_ANALIZAR, output_path=output_path)
            )
            async with self:
                task_info.result = result
                task_info.status = "Complete"
        except Exception as e:
            async with self:
                task_info.result = f"Error: {str(e)}"
                task_info.status = "Failed"

    @rx.event(background=True)
    async def run_verificar_y_reprocesar(self):
        """Run a slow task that exceeds the timeout."""
        logging.info("Iniciando el reprocesamiento de artículos...")
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        output_path = f"articulos_filtrados_{fecha_actual}.csv"

        async with self:
            task_ix = len(self.tasks)
            self.tasks.append(
                TaskInfo(status="Running slow task...")
            )
            task_info = self.tasks[task_ix]

        try:
            # Run with a timeout of 1 second (not enough time)
            result = await asyncio.wait_for(
                rx.run_in_thread(
                    pp.verificar_y_reprocesar(output_path)
                ),
                timeout=1.0,
            )
            async with self:
                task_info.result = result
                task_info.status = "Complete"
                
        except asyncio.TimeoutError:
            async with self:
                # Warning: even though we stopped waiting for the task,
                # it may still be running in thread
                task_info.result = (
                    "Task timed out after 1 second!"
                )
                task_info.status = "Timeout"
        except Exception as e:
            async with self:
                task_info.result = f"Error: {str(e)}"
                task_info.status = "Failed"


def run_in_thread_example():
    return rx.vstack(
        rx.heading("run_in_thread Example", size="3"),
        rx.hstack(
            rx.button(
                "Run Quick Task",
                on_click=RunInThreadState.run_quick_task,
                color_scheme="green",
            ),
            rx.button(
                "Run Slow Task (exceeds timeout)",
                on_click=RunInThreadState.run_slow_task,
                color_scheme="red",
            ),
        ),
        rx.vstack(
            rx.foreach(
                RunInThreadState.tasks.reverse()[:10],
                lambda task: rx.hstack(
                    rx.text(task.status),
                    rx.spacer(),
                    rx.text(task.result),
                ),
            ),
            align="start",
            width="100%",
        ),
        width="100%",
        align_items="start",
        spacing="4",
    )