import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from deduplicator import deduplicate_records
from models import EpisodeRecord




def test_deduplicate_keeps_best_record_by_air_date():
    records = [
        EpisodeRecord("Lost", 1, 1, "Pilot", "Unknown", 1),
        EpisodeRecord("Lost", 1, 1, "Pilot", "2004-09-22", 2),
    ]

    final_records, duplicates = deduplicate_records(records)

    assert len(final_records) == 1
    assert duplicates == 1
    assert final_records[0].air_date == "2004-09-22"


def test_deduplicate_keeps_first_if_same_quality():
    records = [
        EpisodeRecord("Lost", 1, 1, "Pilot", "2004-09-22", 1),
        EpisodeRecord("Lost", 1, 1, "Pilot", "2004-09-22", 2),
    ]

    final_records, duplicates = deduplicate_records(records)

    assert len(final_records) == 1
    assert duplicates == 1
    assert final_records[0].original_index == 1