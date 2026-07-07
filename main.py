"""
PawPal+ Demo Script
--------------------
CLI-first verification: exercises Owner, Pet, CareTask, and Scheduler
before wiring anything up to a UI.
"""

from pawpal_system import Owner, Pet, CareTask, Scheduler


def main() -> None:
    owner = Owner(name="Gina", minutes_available=45, preferences=["mornings"])

    bella = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Tabby", age=2)

    owner.add_pet(bella)
    owner.add_pet(whiskers)

    bella.add_task(CareTask(title="Morning walk", duration_minutes=20, priority="high"))
    bella.add_task(CareTask(title="Give medication", duration_minutes=5, priority="high"))
    whiskers.add_task(CareTask(title="Feed breakfast", duration_minutes=10, priority="medium"))
    whiskers.add_task(CareTask(title="Clean litter box", duration_minutes=15, priority="low"))

    scheduler = Scheduler(owner=owner)

    print(scheduler.explain())


if __name__ == "__main__":
    main()