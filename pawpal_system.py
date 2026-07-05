"""
PawPal+ Logic Layer
--------------------
Backend classes for the PawPal+ pet care management system.

This is the "skeleton" phase: class names, attributes, and empty method
stubs derived from the Phase 1 UML diagram. Implementation logic will be
filled in during later phases.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum


class TaskType(Enum):
    FEEDING = "feeding"
    WALK = "walk"
    MEDICATION = "medication"
    APPOINTMENT = "appointment"


@dataclass
class Task:
    task_id: str
    pet_id: str
    task_type: TaskType
    due_datetime: datetime
    is_recurring: bool = False
    recurrence_interval: timedelta | None = None
    priority: int = 0
    is_complete: bool = False

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        raise NotImplementedError

    def reschedule(self, new_datetime: datetime) -> None:
        """Change the due date/time of this task."""
        raise NotImplementedError

    def generate_next_occurrence(self) -> "Task":
        """If recurring, create the next Task instance based on recurrence_interval."""
        raise NotImplementedError


@dataclass
class Pet:
    pet_id: str
    name: str
    species: str
    breed: str
    birthdate: date
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task for this pet."""
        raise NotImplementedError

    def get_upcoming_tasks(self) -> list[Task]:
        """Return this pet's incomplete tasks, sorted by due date."""
        raise NotImplementedError


@dataclass
class Owner:
    owner_id: str
    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a new pet to this owner's profile."""
        raise NotImplementedError

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet from this owner's profile by id."""
        raise NotImplementedError

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across every pet this owner has."""
        raise NotImplementedError


@dataclass
class Scheduler:
    owners: list[Owner] = field(default_factory=list)

    def get_todays_tasks(self) -> list[Task]:
        """Return all tasks due today across all owners/pets."""
        raise NotImplementedError

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by priority (and/or due date)."""
        raise NotImplementedError

    def detect_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Return pairs of tasks that are scheduled too close together for the same pet."""
        raise NotImplementedError

    def get_overdue_tasks(self) -> list[Task]:
        """Return incomplete tasks whose due_datetime has already passed."""
        raise NotImplementedError