import pytest
from datetime import time


def sort_list(result_list):
    result_list.sort(key=lambda x: x[1])
    return result_list


def test_1():
    result_list = [["boat_1st", time(1, 30, 0), "othertime"],
                   ["boat_2nd", time(2, 0, 0), "othertime"],
                   ["boat_3rd", time(3, 0, 0), "othertime"]
                   ]
    sorted_list = sort_list(result_list)
    first = sorted_list[0]
    second = sorted_list[1]
    third = sorted_list[2]

    assert first[0] == "boat_1st" 
    assert second[0] == "boat_2nd" 
    assert third[0] == "boat_3rd" 