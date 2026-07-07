"""
PawPal+ Logic Layer
--------------------
Backend classes for the PawPal+ pet care management system.

Four core classes: Owner, Pet, CareTask, Scheduler.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

# Maps priority labels to numeric weights (higher = more urgent)
_PRIORITY_WEIGHTS = {"high": 3, "medium": 2, "low": 1}

# Maps a recurrence frequency label to how far the next occurrence is pushed
_FREQUENCY_DELTAS = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


@dataclass
class CareTask:
    """A single care activity for a pet (e.g. feeding, walk, medication)."""

    title: str
    duration_minutes: int
    priority: str
    time: str = "09:00"  # scheduled time in "HH:MM" (24-hour) format
    due_date: date = field(default_factory=date.today)
    frequency: str | None = None  # None, "daily", or "weekly"
    is_complete: bool = False
    pet_name: str = ""  # set automatically by Pet.add_task()

    def priority_weight(self) -> int:
        """Convert this task's priority label into a numeric weight for sorting."""
        return _PRIORITY_WEIGHTS.get(self.priority.lower(), 0)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_complete = True

    def generate_next_occurrence(self) -> CareTask | None:
        """
        If this task recurs, return a new CareTask representing the next
        occurrence (same details, due_date pushed forward). Returns None
        for one-off tasks.
        """
        if self.frequency not in _FREQUENCY_DELTAS:
            return None

        return CareTask(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            time=self.time,
            due_date=self.due_date + _FREQUENCY_DELTAS[self.frequency],
            frequency=self.frequency,
            is_complete=False,
            pet_name=self.pet_name,
        )


@dataclass
class Pet:
    """An individual pet and the care tasks it needs."""

    name: str
    species: str
    breed: str
    age: int
    tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a new care task for this pet, tagging it with this pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def complete_task(self, task: CareTask) -> None:
        """
        Mark a task complete. If it recurs, automatically schedule its next
        occurrence so recurring tasks never have to be re-created by hand.
        """
        task.mark_complete()
        next_task = task.generate_next_occurrence()
        if next_task is not None:
            self.add_task(next_task)


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

    def sort_by_time(self, tasks: list[CareTask] | None = None) -> list[CareTask]:
        """
        Return tasks sorted chronologically by their "HH:MM" time string.
        Zero-padded HH:MM strings sort correctly as plain strings, so no
        datetime parsing is needed for same-day comparisons.
        """
        tasks = tasks if tasks is not None else self._all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[CareTask]:
        """
        Return tasks filtered by pet name and/or completion status.
        Pass None for either argument to skip that filter.
        """
        tasks = self._all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.is_complete == completed]
        return tasks

    def detect_conflicts(self) -> list[str]:
        """
        Lightweight conflict detection: group incomplete tasks by their
        scheduled time, and flag any time slot with more than one task as
        a conflict. Returns warning strings instead of raising, so the
        caller can display them without the program crashing.
        """
        warnings: list[str] = []
        by_time: dict[str, list[CareTask]] = {}
        for task in self._all_tasks():
            if task.is_complete:
                continue
            by_time.setdefault(task.time, []).append(task)

        for time_slot, tasks_at_time in by_time.items():
            if len(tasks_at_time) > 1:
                names = ", ".join(f"{t.pet_name}: {t.title}" for t in tasks_at_time)
                warnings.append(f"Conflict at {time_slot} — {names}")
        return warnings

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

        conflicts = self.detect_conflicts()
        if conflicts:
            lines.append("")
            lines.append("Warnings:")
            lines.extend(f"  ! {w}" for w in conflicts)

        return "\n".join(lines)