# 📚 Borrowed Beans Task Management

## 📖 Project Overview

This project provides a lightweight task management backend for the Data Platform team at **Borrowed Beans**. It helps organize, prioritize, and allocate weekly engineering tasks using an effort-based planning model. The core logic includes a Knapsack-based allocation algorithm and validations to ensure task consistency.

Built with **FastAPI**, **SQLite**, and **Docker**, the system supports both manual and bulk task creation, and enables optimal weekly task selection based on available effort.

---

## 🚀 Features

- ✅ Add tasks via manual **form input** or **bulk upload (JSON file only)**
- ✅ Filter tasks by team
- ✅ Task prioritization based on `priority` and `updated_timestamp`
- ✅ Allocate tasks weekly using a **0/1 Knapsack algorithm** (more details in app/utils)
- ✅ Frontend UI using HTML + JS (Fetch API)
- ✅ Validations to prevent bad data entry:

  - ✔️ Effort must be in the Fibonacci sequence (dynamically generated)
  - ✔️ No future `updated_timestamp` allowed
  - ✔️ No duplicates (same name, team, and timestamp)
  - ✔️ Duplicates blocked **within JSON file** and **against database**

- ✅ Logging for task creation and allocation
- ✅ Dockerized with support for containerized DB + backend
- ✅ GitHub Actions CI/CD for running tests and pushing image to Docker Hub

---

## 🛠️ Setup Instructions

### ▶️ Local Setup

```bash
# Clone the repo
git clone https://github.com/squiz8/borrowed-beans-task-planner.git
cd borrowed-beans-task-planner

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app locally
fastapi dev app/main.py
```

Access: [http://localhost:8000](http://localhost:8000)

---

### ▶️ Run from DockerHub

```bash
# Pull from DockerHub
docker pull devsquiz/borrowed-beans-task-planner:latest

# Run using Docker Compose
docker compose up
```

> ℹ️ The app uses an internal SQLite DB which is recreated each run for testing/demo purposes.

Access: [http://localhost:8000](http://localhost:8000)

---

## ✅ Testing

This project supports **unit** tests using `pytest`.

### ▶️ Run All Tests

```bash
pytest tests/
```

### 🧪 Unit Tests

Located in `tests/test_fibonacci.py`, `tests/test_knapsack.py`, and `tests/test_validators.py`:

#### What we test:

- 🔁 Fibonacci sequence is generated dynamically and capped at 100
- 🎒 Knapsack respects effort limits and selects optimal task set
- 🧼 Validation catches:

  - Future timestamps
  - Duplicates in file

---

## 📁 Dataset

Two datasets provided for evaluation:

### `dataset_1.json` (Clean Sample)

Used to simulate a first-time upload with valid tasks and expected allocation results.

### `dataset_2.json` (Validation Trigger Sample)

Includes:

- ✅ A valid new task
- ❌ Task with future timestamp
- ❌ Duplicate task (in file and DB)
- ❌ Invalid effort not in Fibonacci sequence

> These datasets allow for thorough API testing during review.

---

## 🛠️ Suggestions for Future Enhancements (AWS-Focused)

If this app were to grow beyond MVP and be deployed in a real-world scenario, here are some AWS-based suggestions:

- 🧱 **Use PostgreSQL via Amazon RDS**  
  Switch from SQLite to Amazon RDS with PostgreSQL for a fully managed, scalable database with backups, security, and monitoring.

- ☁️ **Deploy the backend with AWS ECS (Fargate)**  
  Containerize and deploy the FastAPI app using ECS Fargate — a serverless option for running containers without managing infrastructure.

- 🖥️ **Rebuild the UI and host with S3 + CloudFront**  
  Convert the HTML UI to React or Vue, and host it as a static site using S3 (with caching via CloudFront for speed).

> ✨ These AWS-based upgrades are optional — but would bring the project closer to real production architecture.
