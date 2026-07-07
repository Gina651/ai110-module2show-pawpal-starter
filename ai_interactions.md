# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**
**What task did you give the agent?**

I asked the agent to add a third algorithmic capability beyond sorting, filtering, and conflict detection. Specifically, I wanted to implement priority-then-time scheduling and a "next available slot" finder. I also asked it to update the CLI demo (`main.py`) to showcase every algorithmic feature using professional formatting with the `tabulate` library and emoji status indicators, without breaking any existing tests.
**What did the agent do?**

- Modified `pawpal_system.py` by adding `Scheduler.sort_by_priority_then_time()` and `Scheduler.find_next_available_slot()`.
- Updated `build_plan()` to use priority-then-time scheduling.
- Rewrote `main.py` to display formatted task tables using the `tabulate` library and emoji status indicators.
- Added a demo for `find_next_available_slot()`.
- Added three new tests to `tests/test_pawpal.py`.
- Ran the full test suite after each change to verify nothing broke.


**What did you have to verify or fix manually?**

The agent's first version of find_next_available_slot() only checked for gaps between existing tasks it missed the case where the first available gap is after the last task of the day but still before day_end. I added the missing final check (end_of_day - cursor >= duration_minutes) after the main loop, and added test_find_next_available_slot_returns_none_when_fully_booked specifically to confirm the function correctly returns None instead of an invalid time when no gap of the requested length exists anywhere in the day. I verified the fix by manually tracing the algorithm against a fully-booked 07:00–21:00 day before trusting the test result.


---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

This stretch feature was not attempted. I used a single AI coding assistant throughout the project, so I did not perform a comparison between multiple AI models or prompting strategies.