"""R5-impl: read-only scan of campaign-v3 records for implementation facts.

Counts cut methods, polytope fallbacks, separator statistics and allowance
overruns per part and mode. Single-threaded, streaming, no writes.
"""
import collections
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "experiments"


def scan(path):
    methods = collections.Counter()
    skipped = collections.Counter()
    stats = collections.defaultdict(collections.Counter)
    overruns = collections.defaultdict(list)
    statuses = collections.Counter()
    star_cuts = collections.Counter()
    configs = collections.defaultdict(set)
    nonquad_fail = collections.Counter()
    with open(path) as handle:
        for line in handle:
            if not line.strip():
                continue
            r = json.loads(line)
            mode = r.get("mode")
            statuses[(mode, r.get("status"))] += 1
            cfg = r.get("config")
            if cfg:
                configs[mode].add(json.dumps(cfg, sort_keys=True))
            for cut in r.get("cuts") or []:
                st = cut.get("support_stats", {})
                methods[(mode, st.get("method"))] += 1
                if "polytope_skipped" in st:
                    skipped[mode] += 1
            sep = r.get("separation")
            if sep:
                for key, value in sep.items():
                    if isinstance(value, bool):
                        stats[mode][key] += int(value)
                    elif isinstance(value, (int, float)):
                        stats[mode][key] += value
                if cfg:
                    budget = min(cfg["max_separation_seconds"],
                                 cfg["separation_budget_fraction"] * r["time_limit"])
                    overruns[mode].append((sep["callback_seconds"] - budget, r.get("name"),
                                           sep["discovery_seconds"], budget))
    return methods, skipped, stats, overruns, statuses, configs


def main(parts):
    for part in parts:
        path = BASE / part / "records.jsonl"
        methods, skipped, stats, overruns, statuses, configs = scan(path)
        print("=" * 20, part)
        print("statuses", dict(statuses))
        print("methods", dict(methods))
        print("polytope_skipped", dict(skipped))
        for mode, counter in stats.items():
            keep = {k: round(v, 3) for k, v in counter.items()}
            print("stats", mode, keep)
        for mode, values in overruns.items():
            values.sort(reverse=True)
            over = [v for v in values if v[0] > 0.05]
            print("overrun", mode, "runs", len(values), ">0.05s:", len(over),
                  "max:", [(round(a, 3), n, round(d, 3), round(b, 3)) for a, n, d, b in values[:3]])
        for mode, cfgs in configs.items():
            print("configs", mode, len(cfgs))


if __name__ == "__main__":
    main(sys.argv[1:] or ["v3/runs/partA-full", "v3/runs/partA-root", "v3/runs/partB"])
