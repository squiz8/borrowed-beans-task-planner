async function loadTasks() {
  const messageDiv = document.getElementById("tasks-message");
  const tableBody = document.getElementById("tasks-body");
  const teamFilter = document.getElementById("team-filter").value.trim();

  messageDiv.textContent = "Loading tasks...";
  tableBody.innerHTML = "";

  let url = "http://127.0.0.1:8000/tasks/filtered";
  if (teamFilter !== "") {
    url += `?team=${encodeURIComponent(teamFilter)}`;
  }

  try {
    const response = await fetch(url);
    const tasks = await response.json();

    if (!Array.isArray(tasks) || tasks.length === 0) {
      messageDiv.textContent = "No tasks found.";
      return;
    }

    messageDiv.textContent = "";
    tasks.forEach((task) => {
      const row = document.createElement("tr");

      row.innerHTML = `
          <td>${task.name}</td>
          <td>${task.team}</td>
          <td>${task.description}</td>
          <td>${task.effort}</td>
          <td>${task.priority}</td>
          <td>${formatDate(task.updated_at)}</td>
        `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    messageDiv.textContent = "Error loading tasks: " + error.message;
  }
}

// Format ISO date to readable format
function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleString(); // e.g., "4/12/2025, 8:01:32 AM"
}

// Sorting utility
function sortTable(colIndex) {
  const table = document.getElementById("tasks-table");
  const rows = Array.from(table.querySelectorAll("tbody tr"));
  const isAsc = table.getAttribute("data-sort-dir") !== "asc";

  rows.sort((a, b) => {
    const valA = a.cells[colIndex].textContent.trim();
    const valB = b.cells[colIndex].textContent.trim();

    // Handle numeric columns like "Effort"
    if (colIndex === 3) {
      return isAsc ? valA - valB : valB - valA;
    }

    // Handle date column (colIndex 5)
    if (colIndex === 5) {
      return isAsc
        ? new Date(valA) - new Date(valB)
        : new Date(valB) - new Date(valA);
    }

    // Default: string sort
    return isAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
  });

  const body = table.querySelector("tbody");
  rows.forEach((row) => body.appendChild(row));
  table.setAttribute("data-sort-dir", isAsc ? "asc" : "desc");
}

// Load tasks on page load
window.addEventListener("DOMContentLoaded", loadTasks);
