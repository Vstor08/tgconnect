import sqlite3
from typing import Optional, Dict

DB_PATH = "commands.db"

class CommandsDB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS commands (
                    name TEXT PRIMARY KEY,
                    command TEXT NOT NULL
                )
            """)
            conn.commit()

    def add_command(self, name: str, command: str) -> bool:
        """
        Добавить новую команду или обновить существующую.
        Возвращает True, если успешно.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO commands (name, command) VALUES (?, ?)
                    ON CONFLICT(name) DO UPDATE SET command=excluded.command
                """, (name, command))
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка добавления команды: {e}")
            return False

    def get_command(self, name: str) -> Optional[str]:
        """
        Получить команду по имени. Вернёт None, если не найдена.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT command FROM commands WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None

    def delete_command(self, name: str) -> bool:
        """
        Удалить команду по имени. Возвращает True, если что-то удалено.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM commands WHERE name = ?", (name,))
            conn.commit()
            return cursor.rowcount > 0

    def list_commands(self) -> Dict[str, str]:
        """
        Вернуть все команды в виде словаря {name: command}
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, command FROM commands")
            rows = cursor.fetchall()
            return {name: command for name, command in rows}
