"""1번 양성예측도 실험의 전체 조건 조합을 CSV로 생성한다."""

from __future__ import annotations

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT_FILE = HERE / "diagnostic_parameter_sweep.csv"

PREVALENCE_PERCENTS = (0.25, 0.5, 1.0)
PERCENT_RANGE = range(30, 101)
SAMPLE_SIZE = 1000

FIELDNAMES = (
    "scenario_id",
    "prevalence_percent",
    "sensitivity_percent",
    "specificity_percent",
    "sample_size",
    "diseased",
    "non_diseased",
    "true_positive",
    "false_negative",
    "false_positive",
    "true_negative",
    "positive_tests",
    "negative_tests",
    "ppv_percent",
    "npv_percent",
    "false_positive_rate_percent",
    "false_negative_rate_percent",
)


def calculate(prevalence_percent: float, sensitivity_percent: int, specificity_percent: int) -> dict[str, float]:
    prevalence = prevalence_percent / 100
    sensitivity = sensitivity_percent / 100
    specificity = specificity_percent / 100

    diseased = SAMPLE_SIZE * prevalence
    non_diseased = SAMPLE_SIZE - diseased
    true_positive = diseased * sensitivity
    false_negative = diseased - true_positive
    true_negative = non_diseased * specificity
    false_positive = non_diseased - true_negative
    positive_tests = true_positive + false_positive
    negative_tests = true_negative + false_negative

    return {
        "sample_size": SAMPLE_SIZE,
        "diseased": diseased,
        "non_diseased": non_diseased,
        "true_positive": true_positive,
        "false_negative": false_negative,
        "false_positive": false_positive,
        "true_negative": true_negative,
        "positive_tests": positive_tests,
        "negative_tests": negative_tests,
        "ppv_percent": true_positive / positive_tests * 100,
        "npv_percent": true_negative / negative_tests * 100,
        "false_positive_rate_percent": (1 - specificity) * 100,
        "false_negative_rate_percent": (1 - sensitivity) * 100,
    }


def generate_csv(output_file: Path = OUTPUT_FILE) -> int:
    row_count = 0
    with output_file.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for prevalence_percent in PREVALENCE_PERCENTS:
            for sensitivity_percent in PERCENT_RANGE:
                for specificity_percent in PERCENT_RANGE:
                    row_count += 1
                    writer.writerow(
                        {
                            "scenario_id": row_count,
                            "prevalence_percent": prevalence_percent,
                            "sensitivity_percent": sensitivity_percent,
                            "specificity_percent": specificity_percent,
                            **{
                                key: round(value, 8) if isinstance(value, float) else value
                                for key, value in calculate(
                                    prevalence_percent,
                                    sensitivity_percent,
                                    specificity_percent,
                                ).items()
                            },
                        }
                    )

    return row_count


if __name__ == "__main__":
    rows = generate_csv()
    print(f"{OUTPUT_FILE.name}: {rows:,}개 조건 저장 완료")
