import streamlit as st

from pawpal_system import Owner, Pet, CareTask, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ — a pet care planning assistant. Add a pet, add some
care tasks, and generate a time-constrained, conflict-checked schedule.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Owner & Pet")
owner_name = st.text_input("Owner name", value="Jordan")
minutes_available = st.number_input(
    "Time available today (minutes)", min_value=5, max_value=480, value=60
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks — these feed directly into the scheduler below.")

# --- Application memory: store CareTask objects, not raw dicts ---------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    task_time = st.text_input("Time (HH:MM)", value="08:00")

frequency = st.selectbox("Recurrence", ["none", "daily", "weekly"])

if st.button("Add task"):
    st.session_state.tasks.append(
        CareTask(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            time=task_time,
            frequency=None if frequency == "none" else frequency,
            pet_name=pet_name,
        )
    )

# --- Build Owner/Pet/Scheduler from current session state ---------------
pet = Pet(name=pet_name, species=species, breed="", age=0)
pet.tasks = st.session_state.tasks
owner = Owner(name=owner_name, minutes_available=int(minutes_available))
owner.add_pet(pet)
scheduler = Scheduler(owner=owner)

st.divider()
st.subheader("All Tasks (sorted by time)")

if not st.session_state.tasks:
    st.info("No tasks yet. Add one above.")
else:
    sorted_tasks = scheduler.sort_by_time()

    # Filtering controls, wired to Scheduler.filter_tasks()
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        status_filter = st.selectbox("Show", ["All", "Incomplete", "Completed"])
    with filter_col2:
        st.caption(f"{len(sorted_tasks)} total task(s)")

    completed_filter = {"All": None, "Incomplete": False, "Completed": True}[status_filter]
    visible_tasks = scheduler.filter_tasks(completed=completed_filter)
    visible_tasks = scheduler.sort_by_time(visible_tasks)

    st.table(
        [
            {
                "time": t.time,
                "title": t.title,
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
                "frequency": t.frequency or "one-off",
                "complete": t.is_complete,
            }
            for t in visible_tasks
        ]
    )

    # Conflict warnings: surfaced with st.warning so they're visually
    # distinct from the plan itself, and shown BEFORE the plan so the
    # owner sees potential problems before deciding what to do about them.
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(f"⚠️ {warning}")
    else:
        st.success("No scheduling conflicts detected.")

st.divider()
st.subheader("Today's Plan")

if st.button("Generate schedule"):
    plan = scheduler.build_plan()
    if not plan:
        st.info("No tasks fit into today's available time.")
    else:
        st.success(f"Built a plan using {sum(t.duration_minutes for t in plan)} of {int(minutes_available)} minutes.")
        st.table(
            [
                {"time": t.time, "title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority}
                for t in plan
            ]
        )
        st.text(scheduler.explain())