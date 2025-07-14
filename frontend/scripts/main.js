document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("task-file");
  const formFields = document.querySelectorAll(
    "#manual-form input, #manual-form select"
  );
  const form = document.querySelector("form");
  const datetimeInput = document.getElementById("updated_timestamp");

  /**
   * FEATURE: Disallow future dates
   * Sets the max attribute of the datetime-local input to the current datetime.
   * This ensures users cannot pick a future timestamp.
   * This can be done in HTML, but setting it dynamically ensures it's always current.
   */

  function getCurrentLocalDatetime() {
    const now = new Date();
    const offset = now.getTimezoneOffset(); // in minutes
    const local = new Date(now.getTime() - offset * 60 * 1000);
    return local.toISOString().slice(0, 16);
  }
  const now = getCurrentLocalDatetime();
  datetimeInput.setAttribute("max", now);

  /**
   * FEATURE: Only one input method allowed — file OR form data
   * This is handled in JavaScript.
   * HTML alone cannot enforce that if one input is filled, the other must be empty.
   * JS disables the form inputs if a file is selected.
   */
  fileInput.addEventListener("change", () => {
    const isFileSelected = fileInput.files.length > 0;
    formFields.forEach((f) => (f.disabled = isFileSelected));
  });

  /**
   * FEATURE: Show feedback messages in the page (success or error)
   */
  function showMessage(message, type = "success") {
    const messageDiv = document.getElementById("response-message");
    messageDiv.classList.remove("d-none", "alert-success", "alert-danger");
    messageDiv.classList.add(
      "alert",
      type === "error" ? "alert-danger" : "alert-success"
    );
    messageDiv.textContent = message;
  }

  /**
   * FEATURE: Submit form OR file to FastAPI
   * - If a file is selected, send it to POST /tasks/file
   * - If form is filled, send data to POST /tasks/
   */
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const isFileSelected = fileInput.files.length > 0;
    // const isManualUsed = Array.from(formFields).some(
    //   (f) => f.value.trim() !== ""
    // );
    const isManualUsed = Array.from(formFields)
      .filter((f) => !f.disabled) // ✅ only check enabled fields
      .some((f) => f.value.trim() !== "");

    console.log("isManualUsed:", isManualUsed);
    console.log("isFileSelected:", isFileSelected);

    // Prevent using both input methods at once
    if (isFileSelected && isManualUsed) {
      showMessage(
        "Please use only one method: upload a file OR fill in the form.",
        "error"
      );
      return;
    }

    // Prevent submitting an empty form
    if (!isFileSelected && !isManualUsed) {
      showMessage("Please provide either a file or form input.", "error");
      return;
    }

    try {
      let response;
      let result;

      if (isFileSelected) {
        // Submit file to FastAPI
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        response = await fetch("http://127.0.0.1:8000/tasks/file", {
          method: "POST",
          body: formData,
        });
      } else {
        // Collect form input data
        const payload = {
          name: document.getElementById("name").value,
          team: document.getElementById("team").value,
          description: document.getElementById("description").value,
          effort: parseInt(document.getElementById("effort").value),
          priority: document.getElementById("priority").value,
          updated_timestamp: document.getElementById("updated_timestamp").value,
        };

        // Submit form data to FastAPI
        response = await fetch("http://127.0.0.1:8000/tasks/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
      }

      // Parse the response
      result = await response.json();

      if (!response.ok) {
        // Error from API
        showMessage(
          "Error: " + (result.detail || "Submission failed"),
          "error"
        );
      } else {
        // Success response
        showMessage("Success: " + JSON.stringify(result), "success");
      }
    } catch (error) {
      // Network or other error
      showMessage("An error occurred: " + error.message, "error");
    }

    // Reset the form and re-enable inputs
    form.reset();
    formFields.forEach((f) => (f.disabled = false));
  });
});
