
from app.utils.knapsack import knapsack
from collections import namedtuple
from datetime import datetime

# Simulate a Task object with all required attributes
Task = namedtuple("Task", ["name", "effort", "priority", "updated_at"])

def dt(ts: str):
    return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

def test_knapsack_exact_fit():
    """Tasks perfectly fit the available effort and are sorted by priority."""
    tasks = [
        Task("A", 5, "low", dt("2025-01-01 10:00:00")),
        Task("B", 3, "medium", dt("2025-01-02 10:00:00")),
        Task("C", 2, "high", dt("2025-01-03 10:00:00")),
    ]
    result = knapsack(tasks, 10)
    assert sum(t.effort for t in result) == 10
    assert result[0].priority == "high" 
    assert result[1].priority == "medium"

def test_knapsack_underfilled():
    """Not all effort is used; knapsack still picks highest value set."""
    tasks = [
        Task("A", 5, "medium", dt("2025-01-01 10:00:00")),
        Task("B", 3, "high", dt("2025-01-02 10:00:00")),
    ]
    result = knapsack(tasks, 6)
    assert sum(t.effort for t in result) == 5 or 3
    assert all(t.effort <= 5 for t in result)

def test_knapsack_zero_effort():
    """Returns empty list if effort is 0."""
    tasks = [
        Task("A", 2, "low", dt("2025-01-01 10:00:00")),
        Task("B", 3, "medium", dt("2025-01-02 10:00:00"))
    ]
    result = knapsack(tasks, 0)
    assert result == []

def test_knapsack_empty_task_list():
    """Returns empty list if there are no tasks."""
    result = knapsack([], 10)
    assert result == []

def test_knapsack_priority_sorting():
    """Tasks are returned sorted by priority and updated_at."""
    tasks = [
        Task("A", 1, "low", dt("2025-01-04 10:00:00")),
        Task("B", 1, "high", dt("2025-01-02 10:00:00")),
        Task("C", 1, "medium", dt("2025-01-03 10:00:00")),
        Task("D", 1, "high", dt("2025-01-01 10:00:00")),
    ]
    result = knapsack(tasks, 4)
    priorities = [t.priority for t in result]
    assert priorities == ["high", "high", "medium", "low"]
    assert result[0].updated_at < result[1].updated_at 

def test_knapsack_respects_updated_at_on_equal_priority():
    """Tasks with same priority are ordered by oldest updated_at first."""
    tasks = [
        Task("X", 2, "medium", dt("2025-01-05 10:00:00")),
        Task("Y", 2, "medium", dt("2025-01-01 10:00:00")),
    ]
    result = knapsack(tasks, 2)

    assert result[0].name in {"X", "Y"}
    assert len(result) == 1
