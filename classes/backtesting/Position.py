from dataclasses import dataclass
from typing import Union


@dataclass
class Position:
    price: Union[float, int]
    quantity: Union[float, int]
    date: str
    leverage: int = 1
    valid_leverages = [1, 2, 5, 10, 20]
    index: bool = False

    def __post_init__(self):

        if self.price < 0:
            raise PositionValueError(self.price, "Price must be > 0")

        if self.leverage == 20 or self.leverage == 10 and not self.index:
            raise LeverageError(self.leverage, "Invalid Leverage for non index")


# for data in dates:
#     Position(price=df['Close'].loc[date], quantity=120, leverage=1)


class LeverageError(Exception):
    def __init__(self, value: int, message: str):
        self.value = value
        self.message = message
        super().__init__(message)


class PositionValueError(Exception):
    def __init__(self, value: int, message: str):
        self.value = value
        self.message = message
        super().__init__(message)
