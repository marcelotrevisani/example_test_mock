from random import randint
from typing import Any, Dict

from arca import mark_component


@mark_component(
    name="Sum 2 numbers",
    param_names={"num_1": "Input Number 1", "num_2": "Input 2"},
)
def sum_num(num_1: int, num_2: int) -> int:
    """Sum two numbers.

    :param num_1: First Number
    :param num_2: Second Number
    :return: Return the result of the sum of two numbers.
    """
    return num_1 + num_2


@mark_component(
    name="Create even and odd number",
    param_names={"num": "Number to be added", "list_num": "List with numbers"},
    unpack_output=[("even", int), ("odd", int)],
)
def create_even_odd_numbers():
    """Create two integer numbers, one even and one odd number."""
    rand_num = randint(0, 9999)
    even_num = rand_num if rand_num % 2 == 0 else rand_num + 1

    rand_num = randint(0, 9999)
    odd_num = rand_num if rand_num % 2 == 1 else rand_num + 1
    return {"even": even_num, "odd": odd_num}
