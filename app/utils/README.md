## 📁 `utils/` Logic Documentation

This directory contains core utility logic used throughout the backend system. It currently includes:

* 🧠 **`knapsack.py`** — the algorithm used for optimal task allocation.
* 🔢 **`fibonacci.py`** — helper logic for validating acceptable effort values.

---

## 🎒 Task Allocation: The Knapsack Algorithm

### ✅ Problem

We aim to allocate as many tasks as possible within a weekly effort budget. Each task has an `effort` value (like 3, 5, or 8), and we want to:

* Use up the **effort budget efficiently** (maximize usage).
* **Only include complete tasks** (no splitting).
* Sort results by **priority** (High > Medium > Low) afterward.

This is a perfect use case for the **0/1 Knapsack Problem**.

### 🧩 What is the 0/1 Knapsack Problem?

In classic CS terms:

> Given a set of items, each with a weight and value, determine the most valuable subset of items that can be included in a knapsack of limited capacity.

#### How it maps to our use case:

| Knapsack Term | Our Task Context     |
| ------------- | -------------------- |
| Weight        | Task effort          |
| Value         | Task effort          |
| Capacity      | Weekly effort budget |

We want to **maximize the total effort used** without exceeding the effort limit.

---

### 📘 References

* [GeeksforGeeks: 0/1 Knapsack](https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/)
* [Educative: Knapsack in Python](https://www.educative.io/answers/what-is-the-knapsack-problem)
* [MIT OpenCourseWare - Lecture on Knapsack](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-16-dynamic-programming-ii-0-1-knapsack/)

---

### 🧠 What is a DP Matrix?

A **Dynamic Programming (DP) matrix** is a 2D table that helps solve optimization problems by breaking them into smaller subproblems and storing their solutions.

In our solution:

* `dp[i][w]` = the maximum effort that can be filled using the first `i` tasks and effort limit `w`

---

### ✅ Code Snippet: Table Creation

```python
dp = [[0 for _ in range(max_effort + 1)] for _ in range(n + 1)]

for i in range(1, n + 1):
    effort = tasks[i - 1].effort
    for w in range(1, max_effort + 1):
        if effort > w:
            dp[i][w] = dp[i - 1][w]
        else:
            dp[i][w] = max(dp[i - 1][w], effort + dp[i - 1][w - effort])
```

### 🔁 Backtracking to Find Selected Tasks

```python
w = max_effort
selected = []

for i in range(n, 0, -1):
    if dp[i][w] != dp[i - 1][w]:
        selected.append(tasks[i - 1])
        w -= tasks[i - 1].effort
```

---

### ⏱️ Performance

* Time Complexity: `O(n * W)`
* Space Complexity: `O(n * W)`

> ✅ We use a 2D DP matrix so we can backtrack and know which tasks were selected.

#### Why not use a 1D DP array?

While 1D space optimization is possible (`O(W)`), it **doesn't allow clean backtracking**, which we need to know the exact tasks picked. So we trade memory for traceability.

---

## 🔢 Fibonacci Validator

### 📌 Why Fibonacci Efforts?

The business uses a Fibonacci-like scale for estimating task complexity. This keeps effort estimates simple and intuitive: `1, 2, 3, 5, 8, 13, 21, ...`

### ✅ Why Dynamic Fibonacci?

Instead of hardcoding effort values, we dynamically generate the list up to a configurable cap:

```python
def generate_fibonacci_up_to(max_val: int):
    fibs = [1, 2]
    while fibs[-1] + fibs[-2] <= max_val:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs
```

### 📈 Why Cap at 100?

* Effort budgets are unlikely to exceed 100 points.
* 100 is human-readable and gives us values up to 89 (the last Fibonacci <= 100).
* Keeps validation logic simple and bounded.
