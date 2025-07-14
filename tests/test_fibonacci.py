from app.utils.fibonacci import generate_fibonacci_up_to

def test_fibonacci_returns_base_case_when_limit_is_too_small():
    """Should return base Fibonacci values [1, 2] when the upper limit is less than the next Fibonacci number."""
    fibs = generate_fibonacci_up_to(0)
    assert fibs == [1, 2]

def test_fibonacci_math_integrity():
    """Should ensure Fibonacci sequence values are correct up to 100."""
    fibs = generate_fibonacci_up_to(100)
    for i in range(2, len(fibs)):
        assert fibs[i] == fibs[i - 1] + fibs[i - 2]

