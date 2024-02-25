import typer
from rich.console import Console
from rich.table import Table
from database import get_all_todo, update_todo, delete, insert_todo, complete_todo  
from model import Todo

# Create instance of both console and typer

console = Console()
app = typer.Typer()


@app.command(help="Add a new task to the tracker")
def add_task(task: str, category:str):
    typer.echo(f"adding a new task={task} to the category={category}")
    todo = Todo(task, category)
    insert_todo(todo)
    show_tasks_table()

@app.command(help="Deleting a task from tracker")
def delete_task(position:int):
    typer.echo(f"deleting a task from position={position}")
    delete(position-1)
    show_tasks_table()

@app.command(help="updating status of a task in tracker")
def update_task(position:int, task:str, category:str):
    typer.echo(f"Updating a task={task} at position={position} under the category={category}")
    update_todo(position-1,task,category)
    show_tasks_table()

@app.command(help="Changing status of task to complete")
def complete_task(position:int):
    typer.echo(f"Changing the status of a task at position={position} to complete")
    complete_todo(position-1)
    show_tasks_table()

@app.command()
def show_tasks_table():
    tasks = get_all_todo()

    console.print("[bold magenta]Todos[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#",style="dim", width=6)
    table.add_column("TODO")
    table.add_column("Category")
    table.add_column("Status")

    for index,task in enumerate(tasks,start=1):
        is_done_str = '✅' if task.status == 2 else '❌'
        table.add_row(str(index),task.task,task.category,is_done_str)
    console.print(table)


if __name__ == "__main__":
    app()