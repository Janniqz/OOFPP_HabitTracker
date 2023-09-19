from __future__ import annotations
from enum import Enum
from typing import Union

import click


class Periodicity(Enum):
    Daily = 'daily'
    Weekly = 'weekly'

    @staticmethod
    def from_str(value: str) -> Periodicity:
        if value.lower() in ('d', 'daily'):
            return Periodicity.Daily
        elif value.lower() in ('w', 'weekly'):
            return Periodicity.Weekly
        else:
            raise NotImplementedError
