from datetime import datetime
from typing import Optional

from sqlalchemy import func, String, Integer, Enum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, Session

from classes.orm.base import Base
from classes.orm.habit_entry import HabitEntry
from classes.periodicity import Periodicity


class Habit(Base):
    __tablename__ = "habit"
    __table_args__ = (
        CheckConstraint(name='check_habit_name', sqltext='length(name) >= 1'),
        CheckConstraint(name='check_periodicity', sqltext="periodicity IN ('Daily', 'Weekly')")
    )

    habit_id: Mapped[int] = mapped_column(Integer(), name='id', primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    periodicity: Mapped[Periodicity] = mapped_column(Enum(Periodicity), nullable=False)
    creation_date: Mapped[Optional[datetime]] = mapped_column(default=datetime.now(), server_default=func.CURRENT_TIMESTAMP(), nullable=False)

    def __repr__(self) -> str:
        return f"Habit(id={self.habit_id!r}, name={self.name!r}, periodicity={self.periodicity!r}, creation_date={self.creation_date!r})"

    @staticmethod
    def create(session: Session, name: str, periodicity: Periodicity) -> 'Habit':
        """
        Creates a new habit object and saves it to the database.

        :param session: The SQLAlchemy session object.
        :param name: Desired name for the new habit.
        :param periodicity: Desired periodicity for the new habit. Either daily or weekly.

        :returns: Created Habit
        """
        new_habit = Habit(name=name, periodicity=periodicity)

        session.add(new_habit)
        session.commit()

        return new_habit

    def delete(self, session: Session) -> None:
        """
        Deletes the current Habit object from the database.

        :param session: The SQLAlchemy session object.

        :returns: None
        """
        session.delete(self)
        session.commit()

    def complete(self, session: Session) -> HabitEntry:
        """
        Complete a habit by creating a new entry in the HabitEntry table.

        :param session: The SQLAlchemy session object.

        :returns: Created HabitEntry
        """
        new_entry = HabitEntry(habit_id=self.habit_id)

        session.add(new_entry)
        session.commit()

        return new_entry
