from abc import ABC
from dataclasses import dataclass
from typing import Union

from classes.backtesting.Position import Position


@dataclass
class Fee(ABC):
    position: Position


class OvernightFee(Fee):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    @property
    def fee(self) -> Union[float, int]:
        if self.position.leverage == 1:
            return self.position.quantity * (0.00012 if self.position.date in self.weekdays else 0.00035)
        elif self.position.leverage == 2:
            return self.position.quantity * (0.00023 if self.position.date in self.weekdays else 0.00070)
        elif self.position.leverage == 5:
            return self.position.quantity * (0.00059 if self.position.date in self.weekdays else 0.00176)
        elif self.position.leverage == 10:
            return self.position.quantity * (0.00117 if self.position.date in self.weekdays else 0.00351)
        elif self.position.leverage == 20:
            return self.position.quantity * (0.00234 if self.position.date in self.weekdays else 0.00703)
