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
    name="Create a dictionary",
    param_names={"num": "Number to be added", "list_num": "List with numbers"},
    unpack_output=["trevisani", "test", ("num", int)],
)
def create_dict() -> Dict[str, Any]:
    return {"trevisani": list(range(10)), "test": True, "num": 99}
