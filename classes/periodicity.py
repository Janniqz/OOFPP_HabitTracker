from enum import Enum


class Periodicity(Enum):
    Daily = 1
    Weekly = 2

    @staticmethod
    def from_str(value: str) -> 'Periodicity':
        """
        Converts a string value to a Periodicity enum value.

        :param value: Input String

        :returns: Converted Periodicity
        :raises NotImplementedError: Invalid Input String
        """
        if value.lower() in ('d', 'daily'):
            return Periodicity.Daily
        elif value.lower() in ('w', 'weekly'):
            return Periodicity.Weekly
        else:
            raise NotImplementedError
