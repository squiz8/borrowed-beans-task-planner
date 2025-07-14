def generate_fibonacci_up_to(max_val: int):
    """
    Generate a list of Fibonacci numbers up to a specified maximum value.

    Args:
        max_val (int): The upper limit for the generated Fibonacci sequence.

    Returns:
        List[int]: A list of Fibonacci numbers not exceeding max_val.

    Example:
        generate_fibonacci_up_to(21) -> [1, 2, 3, 5, 8, 13, 21]
    """
    fibs = [1, 2]
    while fibs[-1] + fibs[-2] <= max_val:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs