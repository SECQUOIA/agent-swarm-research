"""Compare the recording logs (logs/rec_disc2_p<k>.log) with the original run-G logs
(open-instances-wave3/eg/retry/logs/disc2_9_p<k>.log): every progress line and the final
B&B and certified-bound lines must agree once the timing fields are removed."""
import os
import re

OUT = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(OUT, "..", "..", "open-instances-wave3", "eg", "retry", "logs")


def lines(path):
    keep = []
    for line in open(path):
        if line.startswith(("  it ", "B&B:", "  certified lower bound")):
            line = re.sub(r"\(\d+s\)", "(Ts)", line)
            line = re.sub(r" t \d+s$", " t Ts", line.rstrip())
            line = re.sub(r"time \d+s", "time Ts", line)
            keep.append(line)
    return keep


allok = True
for k in range(8):
    a = lines(os.path.join(ORIG, f"disc2_9_p{k}.log"))
    b = lines(os.path.join(OUT, "logs", f"rec_disc2_p{k}.log"))
    same = a == b
    allok &= same
    fin = [x for x in b if x.startswith("B&B:")]
    print(f"part {k}: {len(a)} original lines, {len(b)} replay lines, identical apart from timings: {same}")
    print(f"   {fin[0] if fin else 'no final line'}")
    if not same:
        for x, y in zip(a, b):
            if x != y:
                print("   first difference:\n   orig:", x, "\n   rec: ", y)
                break
print("ALL IDENTICAL" if allok else "DIFFERENCES FOUND")
