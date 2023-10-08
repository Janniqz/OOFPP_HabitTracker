from datetime import datetime, timedelta, date
from typing import Optional

from sqlalchemy import func, String, Integer, Enum, CheckConstraint, select, Select, desc, exists
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
    streak: Mapped[int] = mapped_column(Integer(), default=0, nullable=False)
    highest_streak: Mapped[int] = mapped_column(Integer(), default=0, nullable=False)
    creation_date: Mapped[Optional[datetime]] = mapped_column(default=datetime.now(), server_default=func.current_timestamp(), nullable=False)

    def __repr__(self) -> str:
        return f'Habit(id={self.habit_id!r}, name={self.name!r}, periodicity={self.periodicity!r}, creation_date={self.creation_date!r})'

    def update(self, session: Session, new_name: Optional[str] = None, new_periodicity: Optional[Periodicity] = None) -> bool:
        """
        Updates the habit with new name and/or periodicity.

        :param session: The SQLAlchemy session object.
        :param new_name: New name for the habit.
        :param new_periodicity: New periodicity for the habit.

        :returns bool: True if changes were made, False otherwise.
        """
        changes_made = False
        if new_name is not None and new_name != self.name:
            self.name = new_name
            changes_made = True
        if new_periodicity is not None and new_periodicity != self.periodicity:
            self.periodicity = new_periodicity
            changes_made = True

        if changes_made:
            session.commit()

        return changes_made

    def delete(self, session: Session) -> None:
        """
        Deletes the current Habit object from the database.

        :param session: The SQLAlchemy session object.

        :returns: None
        """
        session.delete(self)
        session.commit()

    def complete(self, session: Session) -> Optional[tuple[HabitEntry, bool]]:
        """
        Complete a habit by creating a new entry in the HabitEntry table.

        :param session: The SQLAlchemy session object.

        :returns: Created HabitEntry
        """
        statement: Select
        statement = (select(HabitEntry.completion_date)
                     .where(HabitEntry.habit_id.is_(self.habit_id))
                     .order_by(desc(HabitEntry.completion_date))
                     .limit(1))

        last_completion: datetime
        last_completion = session.scalar(statement)

        streak_broken = False

        # If there is no previous streak, this is the first time the Habit is completed
        if last_completion is None:
            self.streak = 1
        else:
            streak_validity = self.__check_streak_validity(last_completion)

            # Check if we already completed the Habit in the current period
            if streak_validity is None:
                return None

            # Check if we passed the "Break Date" for our current Streak
            if streak_validity:
                self.streak += 1
            else:
                self.streak = 1
                streak_broken = True

        # If the current Streak is higher than the current highest one, update the highest streak
        if self.streak > self.highest_streak:
            self.highest_streak = self.streak

        new_entry = HabitEntry(habit_id=self.habit_id)

        session.add(new_entry)
        session.commit()

        return new_entry, streak_broken

# region Class Methods

    @classmethod
    def create(cls, session: Session, habit_name: str, periodicity: Periodicity) -> 'Habit':
        """
        Creates a new habit object and saves it to the database.

        :param session: The SQLAlchemy session object.
        :param habit_name: Desired name for the new habit.
        :param periodicity: Desired periodicity for the new habit. Either daily or weekly.

        :returns Habit: Created Habit
        """
        new_habit = cls(name=habit_name, periodicity=periodicity)

        session.add(new_habit)
        session.commit()

        return new_habit

    @classmethod
    def get(cls, session: Session, habit_id: Optional[int] = None, habit_name: Optional[str] = None) -> Optional['Habit']:
        """
        Retrieves a Habit from the database based on the given ID / Name.

        :param session: The SQLAlchemy session object.
        :param habit_id: ID of the habit to retrieve. Takes precedence over habit_name.
        :param habit_name: Name of the habit to retrieve.

        :returns Habit: Retrieved Habit
        """
        statement = select(cls).where(cls.habit_id.is_(habit_id).__or__(cls.name.is_(habit_name))).limit(1)

        target_habit = session.scalar(statement)
        if target_habit is None:
            return None

        return target_habit

# endregion

# region Helpers

    def __check_streak_validity(self, last_completion: datetime) -> Optional[bool]:
        """
        Checks if the current Habit streak is still active.
        If the Habit has already been completed in the current period, returns None.

        :param last_completion: Date of the Last completion

        :returns bool: True if the streak is still active, False otherwise.
        """
        current_date = date.today()
        last_completion_date = last_completion.date()

        break_date: date
        if self.periodicity is Periodicity.Daily:
            # If we already completed the Habit today, don't do anything
            if last_completion_date == current_date:
                return None

            break_date = last_completion_date + timedelta(days=2)
        else:
            last_completion_week = last_completion_date.isocalendar().week
            current_week = current_date.isocalendar().week

            # If we already completed the Habit this week, don't do anything
            if last_completion_week == current_week:
                return None

            days_until_monday = 7 - last_completion_date.weekday() if last_completion_date.weekday() > 0 else 0       # Get the number of days till Monday
            break_date = last_completion_date + timedelta(days=days_until_monday + 7)                                 # Add another week

        return current_date < break_date

    @classmethod
    def exists(cls, session: Session, habit_name: str) -> bool:
        """
        Checks if a Habit with the given name exists.

        :param session: The SQLAlchemy session object.
        :param habit_name: Name of the Habit to check for.

        :returns bool: True if Habit exists, False otherwise.
        """
        return session.query(exists().where(cls.name == habit_name)).scalar()

# endregion
