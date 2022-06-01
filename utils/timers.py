from typing import Callable
import timeit


def compare_functions(regular_func: dict, optimized_func: dict, number: int = 100, verbose=True) -> float:
    """dict -> {name: "", function: func}"""
    func1: Callable = regular_func['function']
    func2: Callable = optimized_func['function']

    regular = timeit.timeit(func1, number=number)
    optimized = timeit.timeit(func2, number=number)

    if verbose:
        print(f"{optimized_func['name']} performed {optimized / regular}x faster than {regular_func['name']}")

    return optimized / regular
