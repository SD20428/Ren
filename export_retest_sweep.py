"""Export exact constrained parameter sweeps for both diagnostic tests."""

import csv
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'retest_parameter_sweep_sum180.csv'
PREVALENCES = ('1.0',)
N = D(100000)
HUNDRED = D(100)
EXPORT_FIELDS = (
    'prevalence_percent', 'sample_size',
    'sensitivity1_percent', 'specificity1_percent',
    'sensitivity2_percent', 'specificity2_percent',
    'first_tp', 'first_tn', 'first_fp', 'first_fn',
    *(f'{target}_{metric}' for target in ('positive_only', 'negative_only', 'all')
      for metric in ('TP', 'TN', 'FP', 'FN')),
)


def combinations():
    for tenths in range(810, 991):
        sensitivity = D(tenths) / 10
        yield sensitivity, D(180) - sensitivity


def rows():
    scenario = 0
    for prevalence in PREVALENCES:
        p = D(prevalence) / HUNDRED
        for se1, sp1 in combinations():
            d_pos = p * se1 / HUNDRED
            h_pos = (1-p) * (1-sp1/HUNDRED)
            d_neg = p * (1-se1/HUNDRED)
            h_neg = (1-p) * sp1/HUNDRED
            pos, neg = d_pos+h_pos, d_neg+h_neg
            for se2, sp2 in combinations():
                scenario += 1
                row = dict(scenario_id=scenario, prevalence_percent=prevalence,
                    sensitivity1_percent=se1, specificity1_percent=sp1,
                    sensitivity2_percent=se2, specificity2_percent=sp2,
                    sample_size=N, first_tp=N*d_pos, first_fn=N*d_neg,
                    first_fp=N*h_pos, first_tn=N*h_neg,
                    first_positive_cancer_percent=HUNDRED*d_pos/pos,
                    first_negative_cancer_percent=HUNDRED*d_neg/neg,
                    positive_only_retested=N*pos,
                    positive_only_not_retested=N*neg,
                    positive_only_total_tests=N*(1+pos),
                    negative_only_retested=N*neg,
                    negative_only_not_retested=N*pos,
                    negative_only_total_tests=N*(1+neg),
                    all_retested=N, all_total_tests=2*N)
                total = D(0)
                for code, d1, h1, positive2 in (
                    ('pp',d_pos,h_pos,True), ('pn',d_pos,h_pos,False),
                    ('np',d_neg,h_neg,True), ('nn',d_neg,h_neg,False)):
                    d2=d1*(se2/HUNDRED if positive2 else 1-se2/HUNDRED)
                    h2=h1*(1-sp2/HUNDRED if positive2 else sp2/HUNDRED)
                    branch=d2+h2
                    total += branch
                    row.update({f'{code}_path_percent':HUNDRED*branch,
                        f'{code}_count':N*branch,
                        f'{code}_cancer_count':N*d2,
                        f'{code}_non_cancer_count':N*h2,
                        f'{code}_cancer_percent':HUNDRED*d2/branch})
                # Retested people use their second result; others retain the first.
                for target in ('positive_only', 'negative_only', 'all'):
                    totals = dict(TP=D(0), TN=D(0), FP=D(0), FN=D(0))
                    for code in ('pp', 'pn', 'np', 'nn'):
                        first_positive = code[0] == 'p'
                        retested = (target == 'all' or
                            (target == 'positive_only' and first_positive) or
                            (target == 'negative_only' and not first_positive))
                        final_positive = code[1] == 'p' if retested else first_positive
                        totals['TP' if final_positive else 'FN'] += row[f'{code}_cancer_count']
                        totals['FP' if final_positive else 'TN'] += row[f'{code}_non_cancer_count']
                    assert sum(totals.values()) == N
                    row.update({f'{target}_{key}': value for key, value in totals.items()})
                assert total == 1
                yield row


def export():
    count = 0
    with OUTPUT.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = None
        for row in rows():
            row = {key: row[key] for key in EXPORT_FIELDS}
            if writer is None:
                writer = csv.DictWriter(handle, fieldnames=list(row))
                writer.writeheader()
            writer.writerow({k: format(v, '.10f').rstrip('0').rstrip('.')
                if isinstance(v, D) and v != v.to_integral_value()
                else str(v) for k,v in row.items()})
            count += 1
    assert count == len(PREVALENCES) * 181 * 181
    print(f'{OUTPUT.name}: {count:,} scenarios')


if __name__ == '__main__':
    export()
