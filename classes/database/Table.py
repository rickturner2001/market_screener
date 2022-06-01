from dataclasses import dataclass
from typing import List
from classes.database.Column import Column


@dataclass
class Table:
    table_name: str
    columns: List[Column]

    def parse_columns_opt(self):
        return " ".join(col.column_stmt + "," if not col == self.columns[-1]
                        else col.column_stmt for col in self.columns)

    @property
    def stmt(self):
        return f"CREATE TABLE IF NOT EXISTS {self.table_name} ({self.parse_columns()})"
