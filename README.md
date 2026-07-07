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

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```

=============================== test session starts ===============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/gina-mar/Desktop/Work/codepath/Paypal/ai110-module2show-pawpal-starter
collected 2 items

tests/test_pawpal.py ..                                                     [100%]

================================ 2 passed in 0.01s ================================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| **Sorting** | `Scheduler.sort_by_time()` | Sorts all tasks chronologically using the `time` field in `"HH:MM"` format. |
| **Filtering** | `Scheduler.filter_tasks(pet_name=None, completed=None)` | Filters tasks by pet name and/or completion status. Passing `None` skips that filter. |
| **Recurring Tasks** | `Pet.complete_task(task)` and `CareTask.generate_next_occurrence()` | Marks a task as complete and automatically creates the next daily or weekly occurrence by advancing the due date with `timedelta`. |
| **Conflict Detection** | `Scheduler.detect_conflicts()` | Detects tasks scheduled at the same time and returns warning messages instead of stopping the program. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
