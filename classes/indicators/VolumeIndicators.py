from dataclasses import dataclass
from typing import Union, List, Any

import numpy
import numpy as np
from pandas import Series


@dataclass
class AdvancingVolume:
    volume: Union[Series, List[int]]

    def __post_init__(self) -> None:
        self.data = self.get_advancing_volume()

    def get_advancing_volume(self) -> np.ndarray:
        previous_volumes = np.array([self.volume[i - 1] if not i == 0 else np.nan for i, _ in enumerate(self.volume)],
                                    dtype=np.dtype("float32"))
        return np.array([(current_volume - previous_volume) / current_volume * 100
                         for current_volume, previous_volume in zip(self.volume, previous_volumes)],
                        dtype=np.dtype("float32"))
