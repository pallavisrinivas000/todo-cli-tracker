import sqlite3
from typing import List
import datetime
from model import Todo


# Establish a connection to sqlite 
conn = sqlite3.connect("todo.db")

# Intialise a cursor for db
cursor= conn.cursor()

#Create a todo table with needed columns

def create_todo_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS todo(
                   task text,
                   category text,
                   date_added datetime,
                   date_completed datetime,
                   status integer,
                   position integer
    )""")

create_todo_table()

def insert_todo(todo: Todo):
    cursor.execute('select count(*) from todo')
    count = cursor.fetchone()[0]
    print(f"The count of rows in table tdod is count={count}")
    # where to add the new entry
    todo.position=count
    with conn:
        cursor.execute('INSERT INTO todo VALUES(:task, :category, :date_added, :date_completed, :status, :position)',
                       {'task': todo.task, 'category': todo.category, 'date_added': todo.date_added,
                        'date_completed': todo.date_completed, 'status': todo.status, 'position': todo.position})
        # why this format of insertion into table?
        # To mitigate sql injection

def get_all_todo():
    cursor.execute('select * from todo')
    results = cursor.fetchall()
    todos =[]
    for result in results:
        todos.append(Todo(*result))
    return todos

def delete(position):
    cursor.execute('select count(*) from todo')
    count = cursor.fetchone()[0]

    with conn:
        cursor.execute('delete from todo where position=:position', {'position': position})

def update_todo(position: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
            cursor.execute('UPDATE todo SET task = :task, category = :category WHERE position = :position',
                      {'position': position, 'task': task, 'category': category})
        elif task is not None:
            cursor.execute('UPDATE todo SET task = :task WHERE position = :position',
                      {'position': position, 'task': task})
        elif category is not None:
            cursor.execute('UPDATE todo SET category = :category WHERE position = :position',
                      {'position': position, 'category': category})

def complete_todo(position: int):
    with conn:
        cursor.execute('UPDATE todo SET status = 2, date_completed = :date_completed WHERE position = :position',
                  {'position': position, 'date_completed': datetime.datetime.now().isoformat()})
    
