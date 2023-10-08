from datetime import datetime
from typing import Optional

from sqlalchemy import func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from classes.orm.base import Base


class HabitEntry(Base):
    __tablename__ = "habit_entry"

    habit_entry_id: Mapped[int] = mapped_column(Integer(), name='id', primary_key=True, autoincrement=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey('habit.id', ondelete='CASCADE'))
    completion_date: Mapped[Optional[datetime]] = mapped_column(default=datetime.today(), server_default=func.current_timestamp())

    def __repr__(self) -> str:
        return f'HabitEntry(id={self.habit_id!r}, habit_id={self.habit_id!r}, completion_date={self.completion_date!r})'
