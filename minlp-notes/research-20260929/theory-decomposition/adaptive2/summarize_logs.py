"""Tables of adaptive-matching.md, Sections 8.3-8.4, built from the GR logs.

  python3 summarize_logs.py

For every completed run (a SUMMARY line) it prints: size, size per bag, stages, processed boxes,
largest number of leaves split per bag per stage, zloc = max_t |z^t - x*_{V_t}|_inf / W_j by stage,
and the last value of gap/((bags) W_j^2). Unfinished runs are listed with their stages so far.
"""
import re
import sys

FILES = [
    "logs/tree_zero_eps1e-4.log",
    "logs/tree_random_eps1e-4.log",
    "logs/tree_zero_b062_eps1e-3.log",
    "logs/tree_zero_b062_eps1e-3_theta16.log",
    "logs/gr_path_b088_eps1e-3.log",
    "logs/gr_path_b088_eps1e-3_theta32.log",
]


def main():
    for f in FILES:
        try:
            lines = open(f).read().splitlines()
        except FileNotFoundError:
            continue
        print("==", f)
        cur = []
        for line in lines:
            if line.startswith("j="):
                cur.append(line)
            elif line.startswith("SUMMARY"):
                m = dict(re.findall(r"(\w+)=([^\s]+)", line))
                size_key = "m" if "m" in m else "n"
                zl = [float(re.search(r"zloc=([^\s]+)", l).group(1)) for l in cur]
                gc = re.search(r"gap/\((?:m|n)-1\)W\^2=([^\s]+)", cur[-1])
                sp = [int(re.search(r"split=(\d+)", l).group(1)) for l in cur if "split=" in l]
                print("%s=%s theta=%s done=%s stages=%s size=%s per_bag=%s processed=%s max_split=%s "
                      "zloc_by_stage=%s max_zloc_from_stage3=%.2f gapconst_last=%s" % (
                          size_key, m[size_key], m["theta"], m["done"], m["stages"], m["size"],
                          m["size_per_bag"], m["processed"], max(sp) if sp else 0,
                          [round(z, 1) for z in zl], max(zl[3:]) if len(zl) > 3 else max(zl),
                          gc.group(1) if gc else "?"))
                cur = []
        if cur:
            zl = [float(re.search(r"zloc=([^\s]+)", l).group(1)) for l in cur]
            print("  unfinished run: %d stages, zloc_by_stage=%s" % (len(cur), [round(z, 1) for z in zl]))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
