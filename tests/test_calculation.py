from calculator.calculation import Add

def test_add_returns_sum_of_two_numbers():
    add = Add(10, 5)
    result = add.get_result()
    assert result == 15

def test_add_handles_negative_numbers():
    first = Add(-4, 1)
    result = first.get_result()
    assert result == -3

def test_add_handles_decimals():
    first = Add(0.5, 0.25)
    assert first.get_result() == 0.75

def test_two_instances_are_independent():
    first = Add(10, 5)
    second = Add(100, 50)
    assert first.get_result() == 15
    assert second.get_result() == 150
    