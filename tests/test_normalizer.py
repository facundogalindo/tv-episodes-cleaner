import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from normalizer import normalize_row, parse_air_date, parse_positive_int


def test_parse_positive_int_valid():
    assert parse_positive_int("12") == 12


def test_parse_positive_int_invalid():
    assert parse_positive_int("abc") == 0
    assert parse_positive_int("-5") == 0
    assert parse_positive_int("3.5") == 0
    assert parse_positive_int("") == 0


def test_parse_air_date_valid():
    assert parse_air_date("2024-01-15") == "2024-01-15"


def test_parse_air_date_invalid():
    assert parse_air_date("") == "Unknown"
    assert parse_air_date("not a date") == "Unknown"
    assert parse_air_date("15-01-2024") == "Unknown"


def test_normalize_row_discards_missing_series():
    row = ["", "1", "2", "Pilot", "2024-01-01"]
    assert normalize_row(row, 1) is None


def test_normalize_row_fills_missing_title():
    row = ["Lost", "1", "2", "", "2024-01-01"]
    record = normalize_row(row, 1)

    assert record is not None
    assert record.episode_title == "Untitled Episode"


def test_normalize_row_invalid_numbers_become_zero():
    row = ["Lost", "abc", "-3", "Pilot", "2024-01-01"]
    record = normalize_row(row, 1)

    assert record is not None
    assert record.season_number == 0
    assert record.episode_number == 0


def test_normalize_row_invalid_date_becomes_unknown():
    row = ["Lost", "1", "2", "Pilot", "01/01/2024"]
    record = normalize_row(row, 1)

    assert record is not None
    assert record.air_date == "Unknown"


def test_normalize_row_discards_when_episode_data_is_missing():
    row = ["Lost", "", "", "", ""]
    assert normalize_row(row, 1) is None


def test_normalize_row_cleans_spaces():
    row = ["  Lost  ", " 1 ", " 2 ", "  Pilot  ", " 2024-01-01 "]
    record = normalize_row(row, 1)

    assert record is not None
    assert record.series_name == "Lost"
    assert record.season_number == 1
    assert record.episode_number == 2
    assert record.episode_title == "Pilot"
    assert record.air_date == "2024-01-01"