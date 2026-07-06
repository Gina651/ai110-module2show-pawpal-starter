# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
**a. Initial design**

My initial UML design included four main classes: Owner, Pet, CareTask, and Scheduler. These classes are connected through simple ownership relationships: an Owner owns Pets, each Pet needs CareTasks, and the Scheduler plans for the Owner by organizing and ordering CareTasks.

- What classes did you include, and what responsibilities did you assign to each?

The Owner class represents the app user. It stores the owner’s available time, preferences, and list of pets. The Pet class represents an individual animal and stores its own list of care tasks. The CareTask class represents one care responsibility, such as feeding, walking, medication, or an appointment. It stores the task title, duration, priority, and recurring status. The Scheduler class handles the algorithmic logic by building a time-constrained plan and explaining the plan in plain language.
The three core actions I identified are: adding a pet profile with basic details, scheduling care tasks for a pet, and viewing today’s prioritized tasks across all pets with urgent or overdue tasks shown first.

Add a pet to my profile with basic details (name, species, breed, birthdate)
Schedule a task for a pet (feeding, walk, medication, appointment), including recurring tasks
View today's prioritized tasks across all my pets, with urgent/overdue items surfaced first

**b. Design changes**

- Did your design change during implementation?

Yes. After reviewing my pawpal_system.py with AI, I updated the design by removing the separate Scheduler.tasks list. Instead, the build_plan() method now gathers tasks directly from self.owner.pets.

- If yes, describe at least one change and why you made it.

The original Scheduler.tasks list duplicated information that was already stored within each Pet object. Maintaining two copies of the same data could lead to inconsistencies if one list was updated but the other was not. By retrieving tasks directly from owner.pets, the design uses a single source of truth, making the code simpler, more reliable, and easier to maintain.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
