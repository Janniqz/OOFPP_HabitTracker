from datetime import datetime
from typing import Optional, Tuple

from sqlalchemy import func, Integer, ForeignKey, Row
from sqlalchemy.orm import Mapped, mapped_column, Session, Query

from classes.orm.base import Base


class HabitEntry(Base):
    __tablename__ = "habit_entry"

    habit_entry_id: Mapped[int] = mapped_column(Integer(), name='id', primary_key=True, autoincrement=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey('habit.id'))
    streak: Mapped[int] = mapped_column(Integer(), nullable=False)
    completion_date: Mapped[Optional[datetime]] = mapped_column(default=datetime.today(), server_default=func.current_timestamp())

    def __repr__(self) -> str:
        return f"Habit(id={self.habit_id!r}, habit_id={self.habit_id!r}, streak={self.streak!r}, completion_date={self.completion_date!r})"

    @staticmethod
    def get_current_streak(session: Session, habit_id: int) -> Optional[Row[Tuple[int, Optional[datetime], int]]]:
        """
        Retrieves the current streak information for a habit.

        Contains the following fields:
        - streak: The last streak number.
        - latest_date: The date of the last completion. Can be None if there have been no completions.
        - count: The total number of entries with the same streak number.
        """
        statement = None    # type: Query | None
        statement = (session.query(HabitEntry.streak,                                                   # Last Streak Number
                                   func.max(HabitEntry.completion_date).label('latest_date'),           # Last Streak Completion Date
                                   func.count(HabitEntry.habit_id).label('count'))                      # Total Number of Entries with this Streak Number
                     .filter(HabitEntry.habit_id == habit_id)
                     .group_by(HabitEntry.streak))
        return statement.one_or_none()
