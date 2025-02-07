import pytest

def calculate_times(race_hours, race_minutes, race_seconds, srs):
    total_time_seconds = race_hours * 3600 + race_minutes * 60 + race_seconds
    srs_time_seconds = int(total_time_seconds) * float(srs[1])
    
    srs_hours = int(srs_time_seconds // 3600)
    srs_minutes = int((srs_time_seconds % 3600) // 60)
    srs_seconds = int(srs_time_seconds % 60)

    return (srs_hours, srs_minutes, srs_seconds)

def test_1():
    result = calculate_times(0, 0, 0, [None, 1])
    assert result == (0, 0, 0)

def test_2():
    result = calculate_times(1, 30, 0, [None, 1.5])
    assert result == (2, 15, 0)

def test_3():
    result = calculate_times(1, 30, 0, [None, 2])
    assert result == (3, 0, 0)

def test_4():
    result = calculate_times(1, 30, 0, [None, 2.5])
    assert result == (3, 45, 0)

def test_5():
    result = calculate_times(1, 30, 0, [None, 3])
    assert result == (4, 30, 0)
