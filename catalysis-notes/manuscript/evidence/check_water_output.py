"""Reproduce the manuscript's reported-output proxy from factual source arrays.

Run: python manuscript/evidence/check_water_output.py
Data provenance and limitations: stage1-water.md and water-source-series.json.
"""
import bisect
import json
from pathlib import Path


def at(points, t):
    i = max(0, min(len(points) - 2, bisect.bisect_right([p[0] for p in points], t) - 1))
    (t0, x0), (t1, x1) = points[i:i + 2]
    return x0 + (x1 - x0) * (t - t0) / (t1 - t0)


def integral(a, b, start=25, stop=585):
    knots = sorted({start, stop} | {t for t, _ in a + b if start < t < stop})
    total = 0
    for left, right in zip(knots, knots[1:]):
        # Simpson's rule is exact for the quadratic product of linear interpolants.
        mid = (left + right) / 2
        total += (right - left) / 6 * (
            at(a, left) * at(b, left) + 4 * at(a, mid) * at(b, mid)
            + at(a, right) * at(b, right))
    return total


if __name__ == '__main__':
    series = json.loads(Path(__file__).with_name('water-source-series.json').read_text())['series']
    reference = integral(series['reference_conversion'], series['reference_selectivity'])
    promoted = integral(series['promoted_conversion'], series['promoted_selectivity'])
    print(json.dumps({'reference_feed_carbon_hours': reference,
                      'promoted_feed_carbon_hours': promoted,
                      'ratio': promoted / reference,
                      'ratio_charging_5pct_PDVB': promoted / reference / 1.05}, indent=2))
