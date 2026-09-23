"""Integrate reported Fang Figure 1 series; no lifetime or economic extrapolation.

Usage: python water_published_output.py /path/to/ft-source.xlsx
Uses only Python standard library. Writes a sibling JSON audit record.
"""
import bisect
import hashlib
import json
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def load_series(path):
    with ZipFile(path) as archive:
        strings = ["".join(node.itertext()) for node in
                   ET.fromstring(archive.read("xl/sharedStrings.xml")).findall("m:si", NS)]
        relations = {node.attrib["Id"]: node.attrib["Target"] for node in
                     ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))}
        sheets = ET.fromstring(archive.read("xl/workbook.xml")).find("m:sheets", NS)
        sheet = next(node for node in sheets if node.attrib["name"] == "Figure 1")
        target = relations[sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]]
        target = target.lstrip("/") if target.startswith("/") else "xl/" + target
        rows = []
        for node in ET.fromstring(archive.read(target)).findall("m:sheetData/m:row", NS):
            row = {}
            for cell in node:
                value = cell.find("m:v", NS)
                if value is None:
                    continue
                column = "".join(filter(str.isalpha, cell.attrib["r"]))
                row[column] = strings[int(value.text)] if cell.attrib.get("t") == "s" else float(value.text)
            rows.append(row)
    pairs = {"reference_conversion": ("A", "B"), "reference_selectivity": ("C", "E"),
             "promoted_conversion": ("G", "H"), "promoted_selectivity": ("I", "K")}
    series = {}
    for name, (time, value) in pairs.items():
        series[name] = [(row[time], row[value] / 100) for row in rows
                        if isinstance(row.get(time), float) and isinstance(row.get(value), float)]
        # The promoted conversion has an exact duplicate (154 h, 44.34527%).
        # Remove identical pairs only; conflicting values at one time still fail.
        series[name] = list(dict.fromkeys(series[name]))
        assert all(a[0] < b[0] for a, b in zip(series[name], series[name][1:]))
        assert all(0 <= value <= 1 for _, value in series[name])
    return series


def interpolate(series, time):
    assert series[0][0] <= time <= series[-1][0]
    index = min(bisect.bisect_right([point[0] for point in series], time) - 1, len(series) - 2)
    t0, v0 = series[index]
    t1, v1 = series[index + 1]
    return v0 + (v1 - v0) * (time - t0) / (t1 - t0)


def integrate_product(first, second, start, stop):
    knots = sorted({start, stop} | {t for t, _ in first + second if start < t < stop})
    total = 0.0
    for left, right in zip(knots, knots[1:]):
        a, b = interpolate(first, left), interpolate(first, right)
        c, d = interpolate(second, left), interpolate(second, right)
        # Exact integral of the product of two linear interpolants.
        total += (right - left) * (a * c + (a * (d-c) + c * (b-a))/2 + (b-a)*(d-c)/3)
    return total


def first_crossing(function, knots):
    for left, right in zip(knots, knots[1:]):
        if function(left) < 0 <= function(right):
            for _ in range(50):
                middle = (left + right) / 2
                if function(middle) < 0:
                    left = middle
                else:
                    right = middle
            return (left + right) / 2
    return None


def main():
    path = Path(sys.argv[1])
    series = load_series(path)
    reference = series["reference_conversion"]
    promoted = series["promoted_conversion"]
    ref_s = series["reference_selectivity"]
    pro_s = series["promoted_selectivity"]
    start = max(points[0][0] for points in series.values())
    stop = min(points[-1][0] for points in series.values())
    ones = [(min(reference[0][0], promoted[0][0]), 1.0), (stop, 1.0)]
    knots = sorted({start, stop} | {t for points in series.values() for t, _ in points if start < t < stop})
    reference_integral = integrate_product(reference, ref_s, start, stop)
    promoted_integral = integrate_product(promoted, pro_s, start, stop)
    difference = lambda t: integrate_product(promoted, pro_s, start, t) - integrate_product(reference, ref_s, start, t)
    # Unknown early selectivity is bounded only by [0,1], without extrapolation.
    early_ref_max = integrate_product(reference, ones, reference[0][0], start)
    early_pro_known = integrate_product(promoted, pro_s, pro_s[0][0], start)
    early_pro_unknown_max = integrate_product(promoted, ones, promoted[0][0], pro_s[0][0])
    early_difference_bounds = [early_pro_known - early_ref_max, early_pro_known + early_pro_unknown_max]
    latest_early_bound_crossing = first_crossing(lambda t: difference(t) + early_difference_bounds[0], knots)
    full_window_ratio_bounds = [
        (promoted_integral + early_pro_known) / (reference_integral + early_ref_max),
        (promoted_integral + early_pro_known + early_pro_unknown_max) / reference_integral,
    ]
    def shifted(points, amount):
        return [(time, max(0.0, min(1.0, value + amount))) for time, value in points]
    # Analyst sensitivity: coherent +/-2 percentage points, not a statistical CI.
    caption_sensitivity_ratios = []
    for direction in [-1, 1]:
        p = integrate_product(shifted(promoted, direction * 0.02), shifted(pro_s, direction * 0.02), start, stop)
        r = integrate_product(shifted(reference, -direction * 0.02), shifted(ref_s, -direction * 0.02), start, stop)
        caption_sensitivity_ratios.append(p / r)
    # A distinct analytic check of the product integration, integral t*t on [0,1].
    assert abs(integrate_product([(0, 0), (1, 1)], [(0, 0), (1, 1)], 0, 1) - 1/3) < 1e-12
    result = {
        "source": "Fang et al. 2026 DOI 10.1038/s41467-026-76571-8, source-data Figure 1",
        "xlsx_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "interpretation": "Integral of reported CO conversion times reported C5+ carbon selectivity; proxy, not independently measured product yield or economics",
        "series_ranges_and_counts": {name: {"first_h": p[0][0], "last_h": p[-1][0], "count": len(p)} for name, p in series.items()},
        "common_observation_window_h": [start, stop],
        "integrated_proxy_feed_carbon_hours": {"reference": reference_integral, "promoted": promoted_integral},
        "promoted_to_reference_ratio_per_catalyst_mass": promoted_integral/reference_integral,
        "promoted_to_reference_ratio_charging_5percent_additive_mass": promoted_integral/reference_integral/1.05,
        "cumulative_proxy_crossing_starting_at_common_window_h": first_crossing(difference, knots),
        "early_difference_2_to_25_h_bounds_feed_carbon_hours": early_difference_bounds,
        "latest_proxy_crossing_after_2_h_under_early_selectivity_bounds_h": latest_early_bound_crossing,
        "ratio_2_to_585_h_under_early_selectivity_bounds_per_catalyst_mass": full_window_ratio_bounds,
        "ratio_2_to_585_h_under_early_selectivity_bounds_charging_additive_mass": [v / 1.05 for v in full_window_ratio_bounds],
        "coherent_2_percentage_point_sensitivity_25_to_585_h_ratio_per_catalyst_mass": caption_sensitivity_ratios,
        "known_limitations": ["Linear interpolation; no statistical uncertainty estimate. Source caption states +/-2% bounds but correlation and replicate information are unavailable", "No observations before 2 h", "No reference extrapolation beyond 592 h", "Selectivity normalization and unclosed carbon not independently corrected", "Source reports matched bed volumes, but no absolute volume, complete quartz inventory or downtime normalization is supplied here", "C5+ includes products with different values"],
    }
    output = Path(__file__).with_name("water_published_output.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
