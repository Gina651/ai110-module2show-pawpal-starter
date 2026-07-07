import streamlit as st

from pawpal_system import Owner, Pet, CareTask, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ — a pet care planning assistant. Add a pet, add some
care tasks, and generate a time-constrained schedule for the day.
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

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    # UI action -> logic layer: build a real CareTask, not a plain dict
    st.session_state.tasks.append(
        CareTask(title=task_title, duration_minutes=int(duration), priority=priority)
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "title": t.title,
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
                "complete": t.is_complete,
            }
            for t in st.session_state.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates a plan using Scheduler.build_plan() and explains it.")

if st.button("Generate schedule"):
    # Wire the UI inputs into real Owner / Pet / Scheduler objects
    pet = Pet(name=pet_name, species=species, breed="", age=0)
    pet.tasks = st.session_state.tasks

    owner = Owner(name=owner_name, minutes_available=int(minutes_available))
    owner.add_pet(pet)

    scheduler = Scheduler(owner=owner)
    st.text(scheduler.explain())