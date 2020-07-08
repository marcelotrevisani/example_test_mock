from typing import Any

from arca.internals.component_internals import get_all_components


def test_get_all_components():
    assert "sum_num" in get_all_components().keys()


def test_description():
    assert "Sum two numbers." in get_all_components()["sum_num"].description


def test_name():
    assert get_all_components()["sum_num"].func_name == "sum_num"

def test_output():
    out_meta = get_all_components()["create_dict"].output
    assert out_meta[0].name == "trevisani"
    assert out_meta[0].type_hint is Any
    assert out_meta[1].name == "test"
    assert out_meta[1].type_hint is Any
    assert out_meta[2].name == "num"
    assert out_meta[2].type_hint is int


def test_input_list():
    all_input = get_all_components()["sum_num"].input_list
    assert all_input[0].name == "Input Number 1"
    assert all_input[0].var_name == "num_1"
    assert all_input[0].type_hint is int
    assert all_input[0].description == "First Number"
    assert all_input[1].name == "Input 2"
    assert all_input[1].var_name == "num_2"
    assert all_input[1].type_hint is int
    assert all_input[1].description == "Second Number"
