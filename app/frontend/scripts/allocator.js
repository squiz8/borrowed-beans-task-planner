function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleString();
}

async function allocateTasks() {
  const effortValue = document.getElementById("effort-input").value.trim();
  const messageDiv = document.getElementById("allocation-message");
  const tableBody = document.getElementById("allocation-body");

  messageDiv.textContent = "";
  tableBody.innerHTML = "";

  if (!effortValue || isNaN(effortValue) || parseInt(effortValue) <= 0) {
    messageDiv.textContent = "Please enter a valid effort number.";
    return;
  }

  const url = `http://127.0.0.1:8000/allocate/?effort=${encodeURIComponent(
    effortValue
  )}`;

  try {
    const response = await fetch(url);
    const allocatedTasks = await response.json();

    if (!Array.isArray(allocatedTasks) || allocatedTasks.length === 0) {
      messageDiv.textContent =
        "No tasks could be allocated within that effort.";
      return;
    }

    allocatedTasks.forEach((task) => {
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
    messageDiv.textContent = "Error allocating tasks: " + error.message;
  }
}
