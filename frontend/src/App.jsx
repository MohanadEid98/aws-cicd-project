import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  // =========================
  // GET - Get all tasks
  // =========================
  useEffect(() => {
    fetch("http://127.0.0.1:5000/tasks")
      .then((response) => response.json())
      .then((data) => {
        setTasks(data);
      })
      .catch((error) => {
        console.error("Error fetching tasks:", error);
      });
  }, []);

  // =========================
  // POST - Add new task
  // =========================
  async function addTask() {
    if (!newTask.trim()) return;

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/tasks",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: newTask,
          }),
        }
      );

      const data = await response.json();

      setTasks([...tasks, data]);

      setNewTask("");
    } catch (error) {
      console.error("Error adding task:", error);
    }
  }

async function toggleTask(id) {
  try {
    // Find the current task
    const currentTask = tasks.find(
      (task) => task["task-id"] === id
    );

    // Send the opposite completed value
    const response = await fetch(
      `http://127.0.0.1:5000/tasks/${id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          completed: !currentTask.completed,
        }),
      }
    );

    // Get the updated task from Flask
    const updatedTask = await response.json();

    // Update React UI
    setTasks(
      tasks.map((task) =>
        task["task-id"] === id
          ? updatedTask
          : task
      )
    );

  } catch (error) {
    console.error("Error updating task:", error);
  }
}

 async function deleteTask(id) {
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/tasks/${id}`,
      {
        method: "DELETE",
      }
    );

    const data = await response.json();

    console.log(data);

    setTasks(
      tasks.filter(
        (task) => task["task-id"] !== id
      )
    );

  } catch (error) {
    console.error("Error deleting task:", error);
  }
}
  // Count completed tasks
  const completedTasks = tasks.filter(
    (task) => task.completed
  ).length;

  return (
    <div className="app">
      <div className="container">

        <header>
          <div>
            <p className="eyebrow">TASK MANAGER</p>

            <h1>
              Stay organized.
              <span> Get things done.</span>
            </h1>

            <p className="subtitle">
              Manage your daily tasks in one simple place.
            </p>
          </div>

          <div className="stats">
            <strong>
              {completedTasks}/{tasks.length}
            </strong>

            <span>Tasks completed</span>
          </div>
        </header>

        <div className="add-task">
          <input
            type="text"
            placeholder="What do you need to do?"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                addTask();
              }
            }}
          />

          <button onClick={addTask}>
            + Add Task
          </button>
        </div>

        <section className="tasks">

          <div className="section-header">
            <h2>Your Tasks</h2>
            <span>{tasks.length} total</span>
          </div>

          {tasks.map((task) => (
            <div
              className={`task ${
                task.completed ? "completed" : ""
              }`}
              key={task["task-id"]}
            >

              <button
                className="checkbox"
                onClick={() =>
                  toggleTask(task["task-id"])
                }
              >
                {task.completed ? "✓" : ""}
              </button>

              <span className="task-title">
                {task.title}
              </span>

              <button
                className="delete"
                onClick={() =>
                  deleteTask(task["task-id"])
                }
              >
                Delete
              </button>

            </div>
          ))}

        </section>

      </div>
    </div>
  );
}

export default App;