from pathlib import Path

from deduplicator import deduplicate_records
from file_handler import read_csv_rows, write_clean_csv
from models import ProcessStats
from normalizer import normalize_row
from report import write_report


def main() -> None:
    input_path = Path("../data/input/episodes.csv")
    output_csv_path = Path("../data/output/episodes_clean.csv")
    report_path = Path("../data/output/report.md")

    stats = ProcessStats()
    normalized_records = []

    raw_rows = read_csv_rows(input_path)

    for index, raw_row in enumerate(raw_rows, start=1):
        stats.total_input_records += 1

        record = normalize_row(raw_row, index)

        if record is None:
            stats.discarded_entries += 1
            continue

        if record.corrected:
            stats.corrected_entries += 1

        normalized_records.append(record)

    final_records, duplicates_detected = deduplicate_records(normalized_records)

    stats.duplicates_detected = duplicates_detected
    stats.total_output_records = len(final_records)

    output_csv_path.parent.mkdir(parents=True, exist_ok=True)

    write_clean_csv(output_csv_path, final_records)
    write_report(report_path, stats)

    print("Process completed successfully.")
    print(f"Input records: {stats.total_input_records}")
    print(f"Output records: {stats.total_output_records}")
    print(f"Discarded entries: {stats.discarded_entries}")
    print(f"Corrected entries: {stats.corrected_entries}")
    print(f"Duplicates detected: {stats.duplicates_detected}")


if __name__ == "__main__":
    main()