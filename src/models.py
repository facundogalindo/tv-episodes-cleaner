from dataclasses import dataclass


@dataclass
class EpisodeRecord:

    series_name: str
    season_number: int
    episode_number: int
    episode_title: str
    air_date: str
    original_index: int
    corrected: bool = False


@dataclass
class ProcessStats:

    total_input_records: int = 0
    total_output_records: int = 0
    discarded_entries: int = 0
    corrected_entries: int = 0
    duplicates_detected: int = 0