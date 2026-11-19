#!/usr/bin/env python3
"""Illustrative arithmetic, not an official competition scorer or ML reproduction."""
import json
import math
from pathlib import Path


def cold_nmae(windows):
    weighted_sum, count = 0.0, 0
    for actual, predicted in windows:
        if len(actual) != len(predicted) or len(actual) not in [24, 7, 2]:
            raise ValueError('Expected paired windows of length 24, 7 or 2')
        mean = sum(actual) / len(actual)
        if mean <= 0:
            raise ValueError('This illustrative implementation assumes positive true mean')
        weighted_sum += sum(abs(a - p) / mean * (24 / len(actual)) for a, p in zip(actual, predicted))
        count += len(actual)
    if not count:
        raise ValueError('Empty predictions')
    return weighted_sum / count


def region_rmse(errors_by_region):
    if not errors_by_region or any(not errors for errors in errors_by_region.values()):
        raise ValueError('Nonempty regions required')
    return sum(math.sqrt(sum(e * e for e in errors) / len(errors))
               for errors in errors_by_region.values()) / len(errors_by_region)


def binary_auc(labels, scores):
    if len(labels) != len(scores) or any(y not in [0, 1] for y in labels):
        raise ValueError('Paired binary labels and scores required')
    pos = [s for y, s in zip(labels, scores) if y == 1]
    neg = [s for y, s in zip(labels, scores) if y == 0]
    if not pos or not neg:
        raise ValueError('Both classes required')
    return sum((p > n) + .5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))


def examples():
    windows = [([100.] * 24, [110.] * 24), ([2400.] * 7, [2640.] * 7), ([16800.] * 2, [18480.] * 2)]
    errors = {'west': [0.] * 9, 'midwest': [2.], 'south': [2.], 'northeast': [2.]}
    flat = [v for values in errors.values() for v in values]
    return {
        'provenance': 'illustrative; synthetic inputs; arithmetic only; not an official scorer',
        'cold_same_10pct_relative_error_three_windows': cold_nmae(windows),
        'bloom_macro_region_rmse': region_rmse(errors),
        'bloom_pooled_rmse': math.sqrt(sum(e * e for e in flat) / len(flat)),
        'auc_tie_half_credit': binary_auc([1, 0], [.5, .5]),
        'auc_before_monotonic_transform': binary_auc([1, 0, 1, 0], [.8, .1, .6, .6]),
        'auc_after_monotonic_transform': binary_auc([1, 0, 1, 0], [s ** 3 for s in [.8, .1, .6, .6]]),
    }


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    output = root / 'docs/metric_examples.json'
    output.write_text(json.dumps(examples(), indent=2) + '\n')
    print(output.relative_to(root))
