"""
PawPal+ Logic Layer
--------------------
Backend classes for the PawPal+ pet care management system.

Four core classes: Owner, Pet, CareTask, Scheduler.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Maps priority labels to numeric weights (higher = more urgent)
_PRIORITY_WEIGHTS = {"high": 3, "medium": 2, "low": 1}


@dataclass
class CareTask:
    """A single care activity for a pet (e.g. feeding, walk, medication)."""

    title: str
    duration_minutes: int
    priority: str
    recurring: bool = False
    is_complete: bool = False

    def priority_weight(self) -> int:
        """Convert this task's priority label into a numeric weight for sorting."""
        return _PRIORITY_WEIGHTS.get(self.priority.lower(), 0)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_complete = True


@dataclass
class Pet:
    """An individual pet and the care tasks it needs."""

    name: str
    species: str
    breed: str
    age: int
    tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a new care task for this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    """The app user, who manages one or more pets."""

    name: str
    minutes_available: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a new pet to this owner's profile."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[CareTask]:
        """Return every task across all of this owner's pets."""
        all_tasks: list[CareTask] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Scheduler:
    """The 'brain' that organizes and prioritizes tasks across an owner's pets."""

    owner: Owner

    def _all_tasks(self) -> list[CareTask]:
        """Pull tasks live from the owner's pets (single source of truth)."""
        return self.owner.get_all_tasks()

    def build_plan(self) -> list[CareTask]:
        """
        Build a prioritized plan of incomplete tasks that fits within the
        owner's available time. Tasks are chosen by priority first (high to
        low), then filled in until minutes_available is used up.
        """
        candidates = [t for t in self._all_tasks() if not t.is_complete]
        candidates.sort(key=lambda t: t.priority_weight(), reverse=True)

        plan: list[CareTask] = []
        minutes_left = self.owner.minutes_available
        for task in candidates:
            if task.duration_minutes <= minutes_left:
                plan.append(task)
                minutes_left -= task.duration_minutes
        return plan

    def explain(self) -> str:
        """Return a human-readable explanation of the current plan."""
        plan = self.build_plan()
        if not plan:
            return "No tasks fit into today's available time."

        lines = [f"Today's plan ({self.owner.minutes_available} minutes available):"]
        minutes_used = 0
        for task in plan:
            minutes_used += task.duration_minutes
            lines.append(
                f"  - {task.title} ({task.duration_minutes} min, "
                f"priority: {task.priority})"
            )
        lines.append(f"Total time used: {minutes_used} minutes.")
        return "\n".join(lines)