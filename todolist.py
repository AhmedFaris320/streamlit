import streamlit as st

st.title("To-Do List App")

# Initialize the task list in session state
if "tasklist" not in st.session_state:
    st.session_state["tasklist"] = []

# Input for new task
task = st.text_input("Enter a new task", "")

# Add task button
if st.button("Add Task"):
    if task:
        st.session_state["tasklist"].append(task)

# Display tasks with checkboxes for completion
completed_tasks = []
for i, task in enumerate(st.session_state["tasklist"]):
    if st.checkbox(f"{i+1}. {task}", key=f"task_{i}"):
        completed_tasks.append(i)

# Remove completed tasks
for i in sorted(completed_tasks, reverse=True):
    st.session_state["tasklist"].pop(i)

st.write("Tasks completed:")
st.stop()