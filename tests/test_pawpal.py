"""
Automated test suite for PawPal+ core logic.

Covers happy paths (sorting, filtering, recurrence, conflict detection)
and edge cases (empty task lists, non-recurring completion, weekly
recurrence, no-match filters).
"""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, CareTask, Scheduler


# --- Basic behaviors -------------------------------------------------

def test_mark_complete_changes_status():
    """Calling mark_complete() should flip is_complete to True."""
    task = CareTask(title="Feed", duration_minutes=10, priority="high")
    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase that pet's task count by 1."""
    pet = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    assert len(pet.tasks) == 0

    pet.add_task(CareTask(title="Walk", duration_minutes=20, priority="medium"))

    assert len(pet.tasks) == 1


# --- Sorting -----------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    """Tasks added out of order should come back sorted by time."""
    pet = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    pet.add_task(CareTask(title="Dinner", duration_minutes=10, priority="medium", time="18:00"))
    pet.add_task(CareTask(title="Breakfast", duration_minutes=10, priority="medium", time="08:00"))
    pet.add_task(CareTask(title="Lunch", duration_minutes=10, priority="medium", time="12:00"))

    owner = Owner(name="Gina", minutes_available=60)
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    sorted_tasks = scheduler.sort_by_time()

    assert [t.title for t in sorted_tasks] == ["Breakfast", "Lunch", "Dinner"]


def test_sort_by_time_on_empty_task_list():
    """Sorting when there are no tasks at all should return an empty list, not error."""
    owner = Owner(name="Gina", minutes_available=60)
    pet = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    owner.add_pet(pet)  # pet has no tasks
    scheduler = Scheduler(owner=owner)

    assert scheduler.sort_by_time() == []


# --- Filtering -----------------------------------------------------------

def test_filter_tasks_by_pet_name():
    """Filtering by pet_name should only return that pet's tasks."""
    owner = Owner(name="Gina", minutes_available=60)
    bella = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Tabby", age=2)
    bella.add_task(CareTask(title="Walk", duration_minutes=20, priority="high", time="08:00"))
    whiskers.add_task(CareTask(title="Feed", duration_minutes=10, priority="medium", time="08:00"))
    owner.add_pet(bella)
    owner.add_pet(whiskers)
    scheduler = Scheduler(owner=owner)

    result = scheduler.filter_tasks(pet_name="Bella")

    assert len(result) == 1
    assert result[0].title == "Walk"


def test_filter_tasks_by_nonexistent_pet_returns_empty():
    """Filtering by a pet name that doesn't exist should return an empty list."""
    owner = Owner(name="Gina", minutes_available=60)
    pet = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    pet.add_task(CareTask(title="Walk", duration_minutes=20, priority="high"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    assert scheduler.filter_tasks(pet_name="Ghost Dog") == []


# --- Recurrence -----------------------------------------------------------

def test_completing_daily_task_creates_next_day_occurrence():
    """Marking a daily task complete should auto-create a task due 1 day later."""
    pet = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    today = date.today()
    task = CareTask(
        title="Morning walk", duration_minutes=20, priority="high",
        time="08:00", due_date=today, frequency="daily",
    )
    pet.add_task(task)

    pet.complete_task(task)

    assert task.is_complete is True
    new_tasks = [t for t in pet.tasks if t is not task]
    assert len(new_tasks) == 1
    assert new_tasks[0].due_date == today + timedelta(days=1)
    assert new_tasks[0].is_complete is False


def test_completing_weekly_task_advances_by_seven_days():
    """A weekly task's next occurrence should be due_date + 7 days, not 1."""
    pet = Pet(name="Whiskers", species="Cat", breed="Tabby", age=2)
    today = date.today()
    task = CareTask(
        title="Clean litter box", duration_minutes=15, priority="low",
        time="12:00", due_date=today, frequency="weekly",
    )
    pet.add_task(task)

    pet.complete_task(task)

    new_task = next(t for t in pet.tasks if t is not task)
    assert new_task.due_date == today + timedelta(weeks=1)


def test_completing_non_recurring_task_creates_no_new_task():
    """A one-off task (no frequency) should not spawn a new occurrence."""
    pet = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    task = CareTask(title="Vet visit", duration_minutes=30, priority="high", frequency=None)
    pet.add_task(task)

    pet.complete_task(task)

    assert len(pet.tasks) == 1  # no new task was added
    assert task.is_complete is True


# --- Conflict detection -----------------------------------------------------------

def test_detect_conflicts_flags_duplicate_time():
    """Two tasks at the exact same time should be flagged as a conflict."""
    owner = Owner(name="Gina", minutes_available=60)
    bella = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Tabby", age=2)
    bella.add_task(CareTask(title="Walk", duration_minutes=20, priority="high", time="08:00"))
    whiskers.add_task(CareTask(title="Feed", duration_minutes=10, priority="medium", time="08:00"))
    owner.add_pet(bella)
    owner.add_pet(whiskers)
    scheduler = Scheduler(owner=owner)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_detect_conflicts_no_warning_for_different_times():
    """Tasks at different times should not be flagged as conflicts."""
    owner = Owner(name="Gina", minutes_available=60)
    pet = Pet(name="Bella", species="Dog", breed="Labrador", age=4)
    pet.add_task(CareTask(title="Walk", duration_minutes=20, priority="high", time="08:00"))
    pet.add_task(CareTask(title="Dinner", duration_minutes=10, priority="medium", time="18:00"))
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner)

    assert scheduler.detect_conflicts() == []