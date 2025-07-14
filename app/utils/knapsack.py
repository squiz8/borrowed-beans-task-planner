from app.utils.logger import logger

def knapsack(tasks, max_effort):
    """
    Implements a 0/1 Knapsack algorithm to select the optimal set of tasks within the given effort limit.

    Each task's `effort` is treated as both its weight and its value — we want to maximize the total effort
    used without exceeding the `max_effort` (weekly capacity).

    Tasks are then sorted by priority and timestamp to reflect business rules.

    Args:
        tasks (List[Task]): List of task objects to choose from.
        max_effort (int): The maximum effort capacity available.

    Returns:
        List[Task]: Optimally selected and sorted list of tasks that fit within the effort constraint.
    """
    logger.info(f"Knapsack started: {len(tasks)} tasks, budget = {max_effort}")
    n = len(tasks)

    # Step 1: Build DP table (2D matrix)
    # dp[i][w] = max effort used by selecting from first i tasks with total weight limit w
    dp = [[0 for _ in range(max_effort + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        effort = tasks[i - 1].effort
        for w in range(1, max_effort + 1):
            if effort > w:
                dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = max(dp[i - 1][w], effort + dp[i - 1][w - effort])

    # Step 2: Backtrack to find the selected tasks
    w = max_effort
    selected_tasks = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            task = tasks[i - 1]
            selected_tasks.append(task)
            w -= task.effort

    logger.info(f"Knapsack selected {len(selected_tasks)} tasks: {[t.name for t in selected_tasks]}")

    # Step 3: Sort by priority (high > medium > low), then by updated_at (earlier first)
    priority_order = {"high": 0, "medium": 1, "low": 2}
    selected_tasks.sort(key=lambda t: (priority_order[t.priority.lower()], t.updated_at))

    return selected_tasks
