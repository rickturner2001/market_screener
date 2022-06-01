from dataclasses import dataclass
from typing import Union
from classes.backtesting.Position import Position


@dataclass
class Wallet:
    balance: Union[float, int]
    positions = []

    def add_funds(self, funds: Union[float, int]):
        self.balance += funds

    def withdraw_funds(self, funds: Union[float, int]):
        if funds <= self.balance:
            self.balance -= funds
        else:
            raise InvalidOperation(funds, "Invalid amount to withdraw")

    def add_position(self, position: Position):
        if position.price <= self.balance:
            self.positions.append(position)
            self.balance -= position.price
        else:
            raise InvalidOperation(position.price, "Insufficient Funds")


class InvalidOperation(Exception):
    def __init__(self, val: Union[float, int], message: str):
        self.val = val
        self.message = message
        super().__init__(message)
