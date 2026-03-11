import csv
from pathlib import Path
from typing import List

from models import EpisodeRecord


def read_csv_rows(input_path: Path) -> List[List[str]]:

    rows: List[List[str]] = []

    with input_path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)

        for row in reader:
            rows.append(row)

    if not rows:
        return []

    # Detect if first row is header
    header = [col.strip().lower() for col in rows[0]]

    expected_header = [
        "series name",
        "season number",
        "episode number",
        "episode title",
        "air date",
    ]

    if header[:5] == expected_header:
        return rows[1:]

    return rows


def write_clean_csv(output_path, records):
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)

        writer.writerow([
            "SeriesName",
            "SeasonNumber",
            "EpisodeNumber",
            "EpisodeTitle",
            "AirDate"
        ])

        for r in records:
            writer.writerow([
                r.series_name,
                r.season_number,
                r.episode_number,
                r.episode_title,
                r.air_date
            ])