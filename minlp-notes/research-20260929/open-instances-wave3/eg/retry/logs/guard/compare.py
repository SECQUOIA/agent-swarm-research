"""Compare each guard rerun log with the original run log, line by line, after removing the
timing fields ('(12s)', 't 245s', 'time 274s') and the final 'guard check:' line.
Then print the guard counts.  Run from retry/:  python3 logs/guard/compare.py"""
import re

PAIRS = [("A", "int_1e-9"), ("B", "int_ni_1e-9"), ("C", "int9_final"), ("H", "int9_ni3")]
PAIRS += [("D", f"disc_p{k}") for k in (0, 1)] + [("E", f"disc9_p{k}") for k in (0, 1)]
PAIRS += [("I", f"disc9_ni3_p{k}") for k in (0, 1)] + [("G", f"disc2_9_p{k}") for k in range(8)]


def norm(path):
    out = []
    for line in open(path):
        if line.startswith("guard check:"):
            continue
        line = re.sub(r"\(\d+s\)", "", line)
        line = re.sub(r" t \d+s$", "", line.rstrip("\n"))
        line = re.sub(r"time \d+s", "time", line)
        out.append(line)
    return out


for run, base in PAIRS:
    a, b = norm(f"logs/{base}.log"), norm(f"logs/guard/{base}_guard.log")
    same = a == b
    g = [l for l in open(f"logs/guard/{base}_guard.log") if l.startswith("guard check:")]
    t0 = re.search(r"time (\d+)s", open(f"logs/{base}.log").read())
    t1 = re.search(r"time (\d+)s", open(f"logs/guard/{base}_guard.log").read())
    print(f"run {run} {base}: {len(a)} lines, identical apart from timings: {same}; "
          f"time {t0.group(1) if t0 else '?'} s -> {t1.group(1) if t1 else '?'} s")
    if not same:
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print(f"   first difference at line {i + 1}:\n   orig  {x}\n   rerun {y}")
                break
        else:
            print(f"   lengths differ: {len(a)} vs {len(b)}")
    print("   " + (g[0].strip() if g else "no guard line (run not finished?)"))
