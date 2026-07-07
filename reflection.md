# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design included four main classes: Owner, Pet, CareTask, and Scheduler. These classes are connected through simple ownership relationships: an Owner owns Pets, each Pet needs CareTasks, and the Scheduler plans for the Owner by organizing and ordering CareTasks.

- What classes did you include, and what responsibilities did you assign to each?

The Owner class represents the app user. It stores the owner’s available time, preferences, and list of pets. The Pet class represents an individual animal and stores its own list of care tasks. The CareTask class represents one care responsibility, such as feeding, walking, medication, or an appointment. It stores the task title, duration, priority, and recurring status. The Scheduler class handles the algorithmic logic by building a time-constrained plan and explaining the plan in plain language.
The three core actions I identified are: adding a pet profile with basic details, scheduling care tasks for a pet, and viewing today’s prioritized tasks across all pets with urgent or overdue tasks shown first.

**b. Design changes**

- Did your design change during implementation?

Yes. After reviewing my pawpal_system.py with AI, I updated the design by removing the separate Scheduler.tasks list. Instead, the build_plan() method now gathers tasks directly from self.owner.pets.

- If yes, describe at least one change and why you made it.

The original Scheduler.tasks list duplicated information that was already stored within each Pet object. Maintaining two copies of the same data could lead to inconsistencies if one list was updated but the other was not. By retrieving tasks directly from owner.pets, the design uses a single source of truth, making the code simpler, more reliable, and easier to maintain.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler considers several constraints when generating a daily plan, including the owner's available time, each task's priority, scheduled time, completion status, and whether a task is recurring. These constraints help ensure that the most important tasks are completed first while staying within the owner's available time.

- How did you decide which constraints mattered most?

I decided that priority and available time were the most important constraints because they have the greatest impact on a pet's daily care. Essential tasks such as feeding, medication, and walks should be scheduled before lower-priority activities whenever time is limited.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

One tradeoff my scheduler makes is that it only detects conflicts when two tasks are scheduled at the exact same time. It does not check whether task durations overlap. For example, a 20-minute walk starting at 8:00 and a 15-minute task starting at 8:10 would overlap in real life, but my scheduler would not identify them as a conflict because their start times are different

- Why is that tradeoff reasonable for this scenario?.

This tradeoff is reasonable for this project because checking for exact time matches is simple, efficient, and easy to understand. Implementing full overlap detection would require calculating start and end times for every task and comparing time intervals, which would make the algorithm more complex. Since the goal of this version is to catch the most common scheduling mistakes, detecting exact-time conflicts provides a practical and beginner-friendly solution.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used my AI coding assistant differently across phases: for brainstorming class structure in Phase 1, for generating method skeletons and later full implementations in Phases 2–4, and for reviewing my own code for gaps (like the missing pet_name back-reference on CareTask, or the duplicate task list on Scheduler). The most effective prompts were specific and scoped — asking it to review one attached file for a particular kind of problem ("missing relationships or bottlenecks") got much more useful feedback than vague requests like "make this better."

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One AI suggestion I chose not to follow was keeping a separate task list inside the Scheduler. Although this approach would have worked, it created two sources of truth for the same data. Instead, I had the Scheduler retrieve tasks directly from Owner.get_all_tasks(). I verified this design by writing a test to confirm that the scheduler correctly retrieved tasks from each pet without maintaining its own copy.
Using separate chat sessions per phase (design, implementation, testing) helped keep feedback focused — a chat session dedicated to testing gave sharper edge-case suggestions than one that was also juggling UI questions.

The main thing I learned about being the "lead architect": AI is very good at generating plausible-looking code quickly, but it doesn't know which tradeoffs matter for my specific design (like whether exact-time conflict detection was good enough, or whether recurrence belonged on Pet vs. CareTask). Those calls stayed mine to make AI could implement either option well, but only I could decide which one fit the system I was building.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested several core behaviors of the system, including task completion, adding tasks to a pet, sorting tasks by time, filtering tasks, recurring task creation, conflict detection, and overall scheduler behavior. I also tested both normal scenarios and edge cases, such as tasks scheduled at the same time.
These tests were important because they verified that the main features of the scheduler worked correctly and continued to behave as expected after changes were made. Automated tests also helped identify issues early and gave me confidence that new features did not break existing functionality.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am very confident that my scheduler works correctly because all eleven automated tests passed successfully. The tests cover the most important features, including scheduling, sorting, filtering, recurring tasks, and conflict detection.

- What edge cases would you test next if you had more time?

If I had more time, I would add tests for overlapping task durations instead of only exact time matches, multiple recurring tasks across several days, owners with multiple pets and large task lists, and situations where the available time is not enough to complete every task.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The part of the project I am most satisfied with is building the scheduling system step by step. Starting with a UML diagram and gradually turning it into a working application helped me understand how good software architecture supports later implementation. I was also pleased with the automated test suite because it confirmed that the main features worked correctly.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve the conflict detection algorithm to identify overlapping task durations instead of only exact time matches. I would also expand the Streamlit interface to allow users to edit or delete tasks, manage multiple pets more easily, and display recurring tasks on a calendar-style schedule.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One of the most important lessons I learned is that AI is a powerful development tool, but it works best when guided by thoughtful human decisions. AI helped me brainstorm designs, generate code, explain concepts, and debug problems, but I still needed to evaluate its suggestions, choose the best approach, and ensure the final system matched the project requirements. Designing software is not just about writing code; it is about making thoughtful architectural decisions, validating those decisions through testing, and using AI as a collaborative tool rather than relying on it to make every design decision.