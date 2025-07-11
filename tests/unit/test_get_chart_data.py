import pytest
from app.charts.get_chart_data import get_max_data_points


def describe_get_max_data_points():
    def test_one_day():
        assert get_max_data_points("1d") == 24

    def test_unknown_string():
        assert get_max_data_points("abc") == 0

    def test_empty_input():
        assert get_max_data_points(None) == 0

    def test_fails_without_argument():
        with pytest.raises(Exception):
            get_max_data_points()
