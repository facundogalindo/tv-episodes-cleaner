from typing import Dict, List, Tuple

from models import EpisodeRecord
from normalizer import normalize_for_compare


def make_duplicate_keys(record: EpisodeRecord) -> List[Tuple]:


    normalized_series = normalize_for_compare(record.series_name)
    normalized_title = normalize_for_compare(record.episode_title)

    return [
        ("rule_1", normalized_series, record.season_number, record.episode_number),
        ("rule_2", normalized_series, 0, record.episode_number, normalized_title),
        ("rule_3", normalized_series, record.season_number, 0, normalized_title),
    ]


def record_quality_score(record: EpisodeRecord) -> Tuple[int, int, int, int]:


    has_valid_air_date = 1 if record.air_date != "Unknown" else 0
    has_known_title = 1 if record.episode_title != "Untitled Episode" else 0
    has_valid_numbers = 1 if record.season_number > 0 and record.episode_number > 0 else 0

    return (
        has_valid_air_date,
        has_known_title,
        has_valid_numbers,
        -record.original_index,
    )


class DisjointSet:


    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1


def deduplicate_records(records: List[EpisodeRecord]) -> Tuple[List[EpisodeRecord], int]:


    if not records:
        return [], 0

    dsu = DisjointSet(len(records))
    seen_keys: Dict[Tuple, int] = {}

    for index, record in enumerate(records):
        for key in make_duplicate_keys(record):
            if key in seen_keys:
                dsu.union(index, seen_keys[key])
            else:
                seen_keys[key] = index

    groups: Dict[int, List[int]] = {}

    for index in range(len(records)):
        root = dsu.find(index)
        groups.setdefault(root, []).append(index)

    final_records: List[EpisodeRecord] = []
    duplicates_detected = 0

    for group_indexes in groups.values():
        group_records = [records[i] for i in group_indexes]
        best_record = max(group_records, key=record_quality_score)
        final_records.append(best_record)
        duplicates_detected += len(group_records) - 1

    final_records.sort(
        key=lambda record: (
            normalize_for_compare(record.series_name),
            record.season_number,
            record.episode_number,
            normalize_for_compare(record.episode_title),
            record.original_index,
        )
    )

    return final_records, duplicates_detected