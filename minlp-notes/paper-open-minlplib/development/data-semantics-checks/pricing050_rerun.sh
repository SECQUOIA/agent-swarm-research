#!/bin/bash
# Re-run a /tmp copy of the verifier's v_pricing050.py (about 20 s) with an appended block that
# saves its own exactly feasible point and counts zero bases of power(x, 3) terms.
# usage: bash pricing050_rerun.sh <repo-root> <scratch-dir> <log-dir>
set -e
REPO=$1; W=$2; L=$3; R=$REPO/research-20260929
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
rm -rf "$W"; mkdir -p "$W/reviews" "$L"
cp -r "$R/reviews/wave2-small-verification" "$R/reviews/open-instances-verification" "$W/reviews/"
cd "$W/reviews/wave2-small-verification"
cat >> v_pricing050.py <<'PY'

# ---- data-semantics audit addition (/tmp copy only)
p3vars = sorted({j for tl in terms for (j, a, g, p) in tl if p == 3})
z3 = [m["names"][j] for j in p3vars if xd[j] == 0]
zall = [m["names"][j] for j in range(N) if xd[j] == 0]
with open(os.path.join(common.HERE, "logs", "pricing050_own_point.txt"), "w") as fo:
    for j in range(N):
        fo.write(f"{m['names'][j]} {xd[j].numerator}/{xd[j].denominator}\n")
print("AUDIT: zero coordinates", len(zall), "; zero coordinates inside power(x,3) terms:", len(z3), z3)
PY
python3 v_pricing050.py > "$L/pricing050_rerun.log" 2>&1
cp logs/pricing050_own_point.txt logs/pricing050.json "$L/"
diff <(python3 -m json.tool "$R/reviews/wave2-small-verification/logs/pricing050.json") <(python3 -m json.tool logs/pricing050.json) \
  && echo "rerun pricing050.json identical to the stored log" | tee -a "$L/pricing050_rerun.log"
tail -3 "$L/pricing050_rerun.log"
