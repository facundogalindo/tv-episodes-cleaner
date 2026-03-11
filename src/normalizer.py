import re
from datetime import datetime
from typing import List, Optional

from models import EpisodeRecord


def clean_text(value: str) -> str:
    """
    Removes leading/trailing spaces and collapses multiple spaces into one.
    """
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    return value


def normalize_for_compare(value: str) -> str:
    """
    Used only for comparisons (duplicates).
    """
    return clean_text(value).lower()


def parse_positive_int(value: str) -> int:
    """
    Converts a value to a non-negative integer.
    Invalid or empty values become 0.
    """
    value = clean_text(value)

    if not value:
        return 0

    if not re.fullmatch(r"\d+", value):
        return 0

    return int(value)


def parse_air_date(value: str) -> str:
    """
    Accepts dates in YYYY-MM-DD format.
    Invalid or missing dates become 'Unknown'.
    """
    value = clean_text(value)

    if not value:
        return "Unknown"

    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
        return parsed.strftime("%Y-%m-%d")
    except ValueError:
        return "Unknown"


def normalize_row(raw_row: List[str], row_index: int) -> Optional[EpisodeRecord]:

    row = list(raw_row[:5])
    while len(row) < 5:
        row.append("")

    raw_series, raw_season, raw_episode, raw_title, raw_air_date = row

    series_name = clean_text(raw_series)

    # Series Name is mandatory
    if not series_name:
        return None

    season_number = parse_positive_int(raw_season)
    episode_number = parse_positive_int(raw_episode)

    episode_title = clean_text(raw_title)
    if not episode_title:
        episode_title = "Untitled Episode"

    air_date = parse_air_date(raw_air_date)

    # If episode number, title, and air date are all missing -> discard
    if (
        episode_number == 0
        and episode_title == "Untitled Episode"
        and air_date == "Unknown"
    ):
        return None

    corrected = (
        raw_series.strip() != series_name
        or raw_season.strip() != str(season_number)
        or raw_episode.strip() != str(episode_number)
        or raw_title.strip() != episode_title
        or raw_air_date.strip() != air_date
    )

    return EpisodeRecord(
        series_name=series_name,
        season_number=season_number,
        episode_number=episode_number,
        episode_title=episode_title,
        air_date=air_date,
        original_index=row_index,
        corrected=corrected
    )