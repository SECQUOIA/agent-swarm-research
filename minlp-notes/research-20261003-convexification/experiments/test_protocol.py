"""Check frozen experiment contracts, not optimizer implementation details."""
from collections import Counter
import json

from run_campaign import HERE, make_jobs


def test_complete_job_plan_respects_frozen_denominators_and_caps(tmp_path):
    jobs = make_jobs(tmp_path)
    assert len(jobs) == 282
    counts = Counter((j["phase"], j["suite"]) for j in jobs)
    assert counts == {("full", "holdout"): 90, ("full", "diagnostic"): 30,
                      ("full", "synthetic"): 39, ("root", "holdout"): 90,
                      ("root", "synthetic"): 15, ("repeat", "holdout"): 18}
    assert sum(j["worker_timeout"] for j in jobs) == 8565
    assert sum(j["time_limit"] for j in jobs) == 5055
    assert all(j["time_limit"] < j["worker_timeout"] for j in jobs)
    assert all(j["suite"] == "holdout" and j["phase"] == "full" for j in jobs[:90])
    assert {j["mode"] for j in jobs} == {"baseline", "all", "auto"}
    for start in range(0, len(jobs), 3):
        group = jobs[start:start + 3]
        assert len({(j["name"], j["phase"], j["seed"]) for j in group}) == 1
        assert len({j["mode"] for j in group}) == 3


def test_holdout_is_stratified_new_and_ranked():
    selection = json.loads((HERE / "holdout-selection.json").read_text())
    selected = selection["selected"]
    assert len(selected) == 30
    assert not ({r["name"] for r in selected} & set(selection["excluded_names"]))
    assert Counter(r["stratum"] for r in selected) == {
        "convex": 10, "nonconvex_continuous": 10, "nonconvex_integer": 10}
    assert [r["rank"] for r in selected] == sorted(r["rank"] for r in selected)
