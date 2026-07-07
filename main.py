"""
PawPal+ Demo Script
--------------------
CLI-first verification of sorting, filtering, recurring tasks, and
conflict detection added in Phase 4.
"""

from pawpal_system import Owner, Pet, CareTask, Scheduler


def main() -> None:
    owner = Owner(name="Gina", minutes_available=60, preferences=["mornings"])

    bella = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Tabby", age=2)
    owner.add_pet(bella)
    owner.add_pet(whiskers)

    # Tasks added out of order on purpose, to prove sort_by_time() works
    bella.add_task(CareTask(title="Give medication", duration_minutes=5, priority="high", time="18:00"))
    bella.add_task(CareTask(title="Morning walk", duration_minutes=20, priority="high", time="08:00", frequency="daily"))
    whiskers.add_task(CareTask(title="Feed breakfast", duration_minutes=10, priority="medium", time="08:00"))
    whiskers.add_task(CareTask(title="Clean litter box", duration_minutes=15, priority="low", time="12:00", frequency="weekly"))

    scheduler = Scheduler(owner=owner)

    print("=== All tasks sorted by time ===")
    for task in scheduler.sort_by_time():
        print(f"  {task.time} - {task.pet_name}: {task.title}")

    print("\n=== Filter: Bella's tasks only ===")
    for task in scheduler.filter_tasks(pet_name="Bella"):
        print(f"  {task.title}")

    print("\n=== Filter: incomplete tasks only ===")
    for task in scheduler.filter_tasks(completed=False):
        print(f"  {task.pet_name}: {task.title}")

    print("\n=== Conflict detection (before completing anything) ===")
    # Bella's walk and Whiskers' breakfast are both at 08:00 -> should conflict
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  ! {warning}")
    else:
        print("  No conflicts found.")

    print("\n=== Completing Bella's daily walk (recurring) ===")
    walk_task = next(t for t in bella.tasks if t.title == "Morning walk")
    bella.complete_task(walk_task)
    print(f"  Original task complete: {walk_task.is_complete}")
    new_occurrences = [t for t in bella.tasks if t.title == "Morning walk" and not t.is_complete]
    for t in new_occurrences:
        print(f"  New occurrence auto-created for: {t.due_date}")

    print("\n=== Today's Plan (with warnings) ===")
    print(scheduler.explain())


if __name__ == "__main__":
    main()