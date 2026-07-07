"""
Quick pytest suite for PawPal+ core logic.
"""

from pawpal_system import Pet, CareTask


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