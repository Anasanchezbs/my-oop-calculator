import math

import pytest

from calculator.inputs import read_csv_values


def write(tmp_path, text):
    path = tmp_path / "data.csv"
    path.write_text(text)
    return path


def test_reads_the_value_column(tmp_path):
    path = write(tmp_path, "value\n10\n20\n30\n")
    assert read_csv_values(path) == [10, 20, 30]


def test_other_columns_are_ignored(tmp_path):
    path = write(tmp_path, "label,value\na,1\nb,2\n")
    assert read_csv_values(path) == [1, 2]


def test_missing_value_column_is_rejected(tmp_path):
    path = write(tmp_path, "x\n1\n")
    with pytest.raises(ValueError, match="named value"):
        read_csv_values(path)


def test_empty_file_is_rejected(tmp_path):
    path = write(tmp_path, "")
    with pytest.raises(ValueError):
        read_csv_values(path)


def test_header_only_file_gives_no_values(tmp_path):
    path = write(tmp_path, "value\n")
    assert read_csv_values(path) == []


def test_missing_file_is_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_csv_values(tmp_path / "nope.csv")


def test_empty_cell_comes_back_as_nan(tmp_path):
    path = write(tmp_path, "value,label\n10,a\n,b\n")
    values = read_csv_values(path)
    assert values[0] == 10
    assert math.isnan(values[1])
