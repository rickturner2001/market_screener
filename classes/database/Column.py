from abc import ABC
from dataclasses import dataclass
from enum import Enum


class ColumnType(Enum):
    Null = 0
    Integer = 1
    Float = 2
    Text = 3


@dataclass
class Column(ABC):
    label: str
    col_type: str = ""
    nullable: bool = False
    unique: bool = False
    attribute: str = ""
    valid_attributes = ["", "primary_key", "secondary_key"]

    @property
    def column_stmt(self) -> str:
        return f"""{self.label} {self.col_type} {self.attribute_string() if self.attribute else ''}{' NOT NULL' if not self.nullable else ''}{' UNIQUE' if self.unique else ''}"""

    def validate_column_attribute(self):
        if not self.attribute.lower() in self.valid_attributes:
            raise ColumnAttributeError(self.attribute, "Invalid attribute field")

    def attribute_string(self) -> str:
        stmt = " ".join(f"{word.upper()}" if not word == self.attribute.split("_")[-1]
                        else word.upper() + ' ' for word in self.attribute.split("_")
                        )
        return stmt


class DefaultColumn(Column):
    pass


@dataclass
class IntegerColumn(Column):
    def __post_init__(self) -> None:
        self.validate_column_attribute()
        self.col_type = ColumnType(1).name.upper()


@dataclass
class FloatColumn(Column):
    def __post_init__(self) -> None:
        self.validate_column_attribute()
        self.col_type = ColumnType(2).name.upper()


@dataclass
class TextColumn(Column):
    def __post_init__(self) -> None:
        self.validate_column_attribute()
        self.col_type = ColumnType(3).name.upper()


class ColumnAttributeError(Exception):
    """Exception for invalid attributes for column class"""

    def __init__(self, attr: str, msg: str) -> None:
        self.attr = attr
        self.msg = msg
        super().__init__(msg)
