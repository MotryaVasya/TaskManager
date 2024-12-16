import psycopg2

def add_task(conn, name, description, priority, start_date, finish_date):
    """Добавляет новую задачу в базу данных."""
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO Tasks (Name, Description, Priority, Start_Date, Finish_Date)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (name, description, priority, start_date, finish_date))
            conn.commit()
            print("Задача успешно добавлена.")
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении задачи: {e}")

def update_task(conn, task_id, name=None, description=None, priority=None, start_date=None, finish_date=None):
    """Обновляет существующую задачу."""
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE Tasks SET"
            updates = []
            values = []

            if name:
                updates.append("Name = %s")
                values.append(name)
            if description:
                updates.append("Description = %s")
                values.append(description)
            if priority:
                updates.append("Priority = %s")
                values.append(priority)
            if start_date:
                updates.append("Start_Date = %s")
                values.append(start_date)
            if finish_date:
                updates.append("Finish_Date = %s")
                values.append(finish_date)

            if not updates:
                print("Нет полей для обновления.")
                return

            sql += " ,".join(updates) + " WHERE Id = %s"
            values.append(task_id)
            cursor.execute(sql, values)
            conn.commit()
            if cursor.rowcount > 0:
              print(f"Задача с ID {task_id} успешно обновлена.")
            else:
               print(f"Задача с ID {task_id} не найдена")
    except psycopg2.Error as e:
        print(f"Ошибка при обновлении задачи: {e}")

def delete_task(conn, task_id):
    """Удаляет задачу из базы данных."""
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM Tasks WHERE Id = %s"
            cursor.execute(sql, (task_id,))
            conn.commit()
            if cursor.rowcount > 0:
               print(f"Задача с ID {task_id} успешно удалена.")
            else:
                print(f"Задача с ID {task_id} не найдена")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении задачи: {e}")

def get_all_tasks(conn):
    """Получает все задачи из базы данных"""
    try:
        with conn.cursor() as cursor:
           sql = "SELECT Id, Name, Description, Priority, Start_Date, Finish_Date FROM Tasks"
           cursor.execute(sql)
           tasks = cursor.fetchall()
           return tasks
    except psycopg2.Error as e:
        print(f"Ошибка при получении задач: {e}")
        return None