"""
PawPal+ Logic Layer
--------------------
Backend classes for the PawPal+ pet care management system.

Skeleton derived from diagrams/uml_draft.mmd (Phase 1). Four core classes:
Owner, Pet, CareTask, Scheduler. Method bodies are stubs to be implemented
in later phases.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: str
    recurring: bool = False

    def priority_weight(self) -> int:
        """Convert the priority label into a numeric weight for sorting."""
        raise NotImplementedError


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a new care task for this pet."""
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    minutes_available: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a new pet to this owner's profile."""
        raise NotImplementedError

    def add_task(self, task: CareTask) -> None:
        """Add a care task (routed to the appropriate pet, or tracked at owner level)."""
        raise NotImplementedError


@dataclass
class Scheduler:
    owner: Owner
    tasks: list[CareTask] = field(default_factory=list)

    def build_plan(self) -> list[CareTask]:
        """Build a prioritized, time-constrained plan of tasks for the owner."""
        raise NotImplementedError

    def explain(self) -> str:
        """Return a human-readable explanation of how the plan was built."""
        raise NotImplementedError