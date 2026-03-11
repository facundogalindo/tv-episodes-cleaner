from pathlib import Path

from models import ProcessStats


def write_report(report_path: Path, stats: ProcessStats) -> None:
    """
    Writes the markdown report with processing statistics
    and a brief explanation of the applied rules.
    """

    content = f"""# Data Quality Report

## Summary
- Total number of input records: {stats.total_input_records}
- Total number of output records: {stats.total_output_records}
- Number of discarded entries: {stats.discarded_entries}
- Number of corrected entries: {stats.corrected_entries}
- Number of duplicates detected: {stats.duplicates_detected}

## Deduplication Strategy
Two records were considered duplicates when they matched at least one of the following criteria:

1. Same normalized Series Name, Season Number, and Episode Number
2. Same normalized Series Name, Episode Number, and normalized Episode Title
3. Same normalized Series Name, Season Number, and normalized Episode Title

Normalization for comparison means:
- trimming leading and trailing spaces
- collapsing multiple internal spaces
- converting text to lowercase

When duplicate records were found, the program kept the best one using this priority:
1. Valid Air Date over "Unknown"
2. Known Episode Title over "Untitled Episode"
3. Valid Season Number and Episode Number over missing values
4. If still tied, the first record encountered in the input file was kept

## Corrections Applied
The following correction rules were applied during processing:

- Missing Series Name -> record discarded
- Missing or invalid Season Number -> 0
- Missing or invalid Episode Number -> 0
- Missing Episode Title -> "Untitled Episode"
- Missing or invalid Air Date -> "Unknown"
- Records with missing Episode Number, Episode Title, and Air Date were discarded
"""

    report_path.write_text(content, encoding="utf-8")