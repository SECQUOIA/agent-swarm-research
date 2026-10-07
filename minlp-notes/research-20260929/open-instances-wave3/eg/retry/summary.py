"""Collect the certified values of the runs from their logs: every piece must report
done=True (no open boxes); the instance bound is the minimum over the pieces of a run,
together with the 'previous theta_min/forced_min' of any checkpoint it resumed from.

    python3 summary.py
"""
import re

RUNS = {
    "A eg_int_s 1e-9 (fast, order 2)": ["int_1e-9"],
    "B eg_int_s 1e-9 (interval, order 2)": ["int_ni_1e-9"],
    "C eg_int_s 1e-9 (fast, final)": ["int9_final"],
    "H eg_int_s 1e-9 (interval, final)": ["int9_ni3"],
    "D eg_disc_s 1e-6 (fast, order 2)": ["disc_p0", "disc_p1"],
    "E eg_disc_s 1e-9 (fast, final)": ["disc9_p0", "disc9_p1"],
    "I eg_disc_s 1e-9 (interval, final)": ["disc9_ni3_p0", "disc9_ni3_p1"],
    "F eg_disc2_s 1e-6 (stage 2 and split pieces)": ["disc2_p0_r", "disc2_p3_r"] +
        [f"disc2_p{p}s{k}_r" for p in (1, 2) for k in range(3)],
    "G eg_disc2_s 1e-9 (fast, final)": [f"disc2_9_p{k}" for k in range(8)],
}
# stopped stage-2 runs of eg_disc2_s parts 1 and 2: only the closed part recorded in the
# checkpoints they resumed from (stage 1) and in their own 600-iteration checkpoints counts
PREV_ONLY = {"F eg_disc2_s 1e-6 (stage 2 and split pieces)": ["disc2_p1_r", "disc2_p2_r"]}
for run, pieces in RUNS.items():
    vals, done, prev, boxes = [], True, [], 0
    for p in PREV_ONLY.get(run, []):
        r = re.search(r"previous theta_min ([-0-9.e]+) forced_min (\S+)", open(f"logs/{p}.log").read())
        prev.append(min(float(r.group(1)), float(r.group(2))))
    for p in pieces:
        t = open(f"logs/{p}.log").read()
        m = re.search(r"B&B: done=(\w+) processed (\d+)", t)
        done &= m is not None and m.group(1) == "True"
        boxes += int(m.group(2)) if m else 0
        c = re.search(r"certified lower bound np.float64\(([-0-9.e]+)\)", t)
        vals.append(float(c.group(1)))
        r = re.search(r"previous theta_min ([-0-9.e]+) forced_min (\S+)", t)
        if r:
            prev.append(min(float(r.group(1)), float(r.group(2))))
    lb = min(vals + prev)
    print(f"{run}: pieces {len(pieces)}, all done {done}, boxes {boxes}, bound {lb!r}")
