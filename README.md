# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Add owner and pet information through the Streamlit UI.
- Add care tasks with title, duration, priority, time, and recurrence.
- Generate a time-constrained daily care plan.
- Sort tasks chronologically by scheduled time.
- Filter tasks by pet name and completion status.
- Detect scheduling conflicts when tasks share the same time.
- Automatically create the next occurrence for daily or weekly recurring tasks.
- Verify core behavior with an automated pytest suite.


## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:


```
Today's plan (45 minutes available):
  - Morning walk (20 min, priority: high)
  - Give medication (5 min, priority: high)
  - Feed breakfast (10 min, priority: medium)
Total time used: 35 minutes.
```
## 🧪 Testing PawPal+

### Run the test suite

```bash
# Run the full test suite
python3 -m pytest

# (Optional) Run with coverage
pytest --cov
```

### What the tests cover

- Task completion updates the task status.
- Adding a task increases a pet's task count.
- Tasks are sorted in chronological order.
- Daily recurring tasks automatically create the next occurrence.
- Conflict detection identifies tasks scheduled at the same time.
- Scheduler filtering works correctly.
- Core scheduling behaviors function as expected.

### Sample test output

```text
=============================== test session starts ===============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/gina-mar/Desktop/Work/codepath/Paypal/ai110-module2show-pawpal-starter
collected 11 items

tests/test_pawpal.py ...........                                            [100%]

=============================== 11 passed in 0.01s ================================
```
### Confidence Level

⭐⭐⭐⭐⭐ (5/5)

The automated test suite verifies the core functionality of the PawPal+ system, including task management, scheduling, sorting, filtering, recurring tasks, and conflict detection. Based on the passing test results, I am confident that the application's primary features work as intended.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| **Sorting** | `Scheduler.sort_by_time()` | Sorts all tasks chronologically using the `time` field in `"HH:MM"` format. |
| **Filtering** | `Scheduler.filter_tasks(pet_name=None, completed=None)` | Filters tasks by pet name and/or completion status. Passing `None` skips that filter. |
| **Recurring Tasks** | `Pet.complete_task(task)` and `CareTask.generate_next_occurrence()` | Marks a task as complete and automatically creates the next daily or weekly occurrence by advancing the due date with `timedelta`. |
| **Conflict Detection** | `Scheduler.detect_conflicts()` | Detects tasks scheduled at the same time and returns warning messages instead of stopping the program. |

## 📸 Demo Walkthrough

**Main UI features:** add an owner and pet, add care tasks with a title,
duration, priority, time, and optional recurrence, view all tasks sorted
chronologically, filter by completion status, see conflict warnings, and
generate a time-constrained daily plan.

**Example workflow:**
1. Enter an owner name and how many minutes are available today.
2. Add a pet (name, species).
3. Add several tasks with different times and priorities — including two
   at the same time, to see conflict detection in action.
4. Review the sorted task table and any conflict warnings.
5. Click "Generate schedule" to see the final prioritized plan.

**Key Scheduler behaviors shown:** chronological sorting, status
filtering, conflict warnings for double-booked times, and a
priority-first, time-budget-constrained plan.

**Sample CLI output** (from `python main.py`):

```
=== All tasks sorted by time ===
  08:00 - Bella: Morning walk
  08:00 - Whiskers: Feed breakfast
  12:00 - Whiskers: Clean litter box
  18:00 - Bella: Give medication

=== Filter: Bella's tasks only ===
  Give medication
  Morning walk

=== Filter: incomplete tasks only ===
  Bella: Give medication
  Bella: Morning walk
  Whiskers: Feed breakfast
  Whiskers: Clean litter box

=== Conflict detection (before completing anything) ===
  ! Conflict at 08:00 — Bella: Morning walk, Whiskers: Feed breakfast

=== Completing Bella's daily walk (recurring) ===
  Original task complete: True
  New occurrence auto-created for: 2026-07-08

=== Today's Plan (with warnings) ===
Today's plan (60 minutes available):
  - Give medication (5 min, priority: high)
  - Morning walk (20 min, priority: high)
  - Feed breakfast (10 min, priority: medium)
  - Clean litter box (15 min, priority: low)
Total time used: 50 minutes.

Warnings:
  ! Conflict at 08:00 — Bella: Morning walk, Whiskers: Feed breakfast
```

*(Note: the recurring task's new date will match tomorrow relative to
whenever you actually run it — the date above reflects the day this demo
was run.)*
