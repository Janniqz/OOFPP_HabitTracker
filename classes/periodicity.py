from enum import Enum
from typing import Optional


class Periodicity(Enum):
    Daily = 1
    Weekly = 2

    @staticmethod
    def from_str(value: str) -> Optional['Periodicity']:
        """
        Converts a string value to a Periodicity enum value.

        :param value: Input String

        :returns Periodicity: Converted Periodicity
        :raises NotImplementedError: Invalid Input String
        """
        if value is None:
            return None

        if value.lower() in ('d', 'daily'):
            return Periodicity.Daily
        elif value.lower() in ('w', 'weekly'):
            return Periodicity.Weekly
        else:
            raise NotImplementedError
