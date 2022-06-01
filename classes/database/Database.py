import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from sqlite3 import Connection, Cursor, connect
from typing import Union, List
from classes.database.Column import Column


@dataclass
class Database(ABC):
    path: Union[str, Path] = None
    filename: str = None
    extension: str = None
    db_path: Union[str, Path] = None
    _tablenames = []
    _connection: Connection = None
    _cursor: Cursor = None

    def connect_existing_database(self, db_path) -> None:
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()

    def create_database_file(self, path, filename, extension) -> None:
        self.path = path
        self.filename = filename
        self.extension = extension
        self.db_path: Union[str, Path] = f"{self.path}/{self.filename}.{self.extension}"

        with open(self.db_path, "w") as f:
            f.write("")

    def establish_connection(self) -> None:
        self._connection = connect(self.db_path)
        self._cursor = self._connection.cursor()

    @staticmethod
    def create_table(tablename: str, columns: List[Column], pk: Column = None) -> str:
        """

        :param tablename: Name of the table
        :param columns: List of Column objects
        :param pk: Primary key ("col_name", "type")
        :return: string representation of sql statement to create the table
        """
        stmt = f"""
                      CREATE TABLE IF NOT EXISTS {tablename} (
                      {f"{pk.column_stmt}" if pk else ""},
                      {Database.dynamic_table_columns_create(columns)}
                      )
                      """
        return stmt

    @staticmethod
    def dynamic_table_columns_create(columns: List[Column]):
        stmt = " ".join([f"{col.column_stmt},"
                         if not col == columns[-1] else col.column_stmt for col in columns])
        return stmt

    @abstractmethod
    def do_populate(self, *args: Union[str, int, float]) -> None:
        pass

    def clear_table(self, table: str) -> None:
        self._cursor.execute(f"DELETE FROM ?", (table,))

    def drop_table(self, table: str) -> None:
        self._cursor.execute("DROP TABLE ?", (table,))

    def query_all(self, table: str) -> List[tuple]:
        return self._cursor.execute(f"SELECT * FROM {table}").fetchall()

    @property
    def cursor(self):
        return self._cursor

    @property
    def connection(self):
        return self._connection
