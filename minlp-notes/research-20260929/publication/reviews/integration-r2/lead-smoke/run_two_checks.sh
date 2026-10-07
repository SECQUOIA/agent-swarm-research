#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Integration review r2 (lead rerun of two checks): relocated EG smoke checks in a disposable copy.
# Copies the needed evidence to a fresh mktemp -d tree under /tmp, pins the OSIL by SHA-256,
# and runs the scientific scripts only inside that copy under bubblewrap, with the source
# checkout and the original OSIL cache hidden (tmpfs) and strace recording every open.
# CPU limit: taskset -c 0,1; one BLAS/OpenMP thread. Writes only to the /tmp copy;
# afterwards copies the logs into this agent-repro directory.
set -euo pipefail
SRC="${_PUBLIC_REPO}"
R=$SRC/research-20260929
HERE=$R/publication/reviews/integration-r2/lead-smoke
PY=$(command -v python3)
T=$(mktemp -d /tmp/lead-eg-r2-XXXXXXXX)
echo "disposable copy: $T"
mkdir -p "$T/research-20260929/publication" "$T/research-20260929/reviews" "$T/research-20260929/publication/reviews"
cp -a "$R/publication/eg-recheck" "$T/research-20260929/publication/eg-recheck"
cp -a "$R/reviews/eg-retry-review-checks" "$T/research-20260929/reviews/eg-retry-review-checks"
cp -a "$R/publication/reviews/eg-recheck-r1" "$T/research-20260929/publication/reviews/eg-recheck-r1"
find "$T" -name __pycache__ -prune -exec rm -rf {} +
mkdir -p "$T/osil-cache"
cp -a "$HOME/.cache/minlplib/minlplib/osil/eg_disc2_s.osil" "$T/osil-cache/"
PIN=$($PY -I -c "import json; print(next(r['sha256'] for r in json.load(open('$R/publication/reproduction/inputs/osil-models.json')) if r['name']=='eg_disc2_s'))")
GOT=$(sha256sum "$T/osil-cache/eg_disc2_s.osil" | cut -d' ' -f1)
echo "OSIL sha256 pinned $PIN"
echo "OSIL sha256 copy   $GOT"
[ "$PIN" = "$GOT" ] || { echo "OSIL PIN MISMATCH"; exit 1; }
# checksums of the copied inputs used by the checks, compared with the source files
for f in publication/eg-recheck/rec/rec_disc2_p7.npz publication/eg-recheck/recheck_leaves.py \
         publication/eg-recheck/margin_cert.py reviews/eg-retry-review-checks/indep_cert.py \
         reviews/eg-retry-review-checks/gms_model.py reviews/eg-retry-review-checks/data/eg_disc2_s.gms; do
  a=$(sha256sum "$R/$f" | cut -d' ' -f1); b=$(sha256sum "$T/research-20260929/$f" | cut -d' ' -f1)
  echo "copy identical $f: $([ "$a" = "$b" ] && echo yes || echo NO)"
done

CACHE=$HOME/.cache/minlplib/minlplib
SANDBOX=(bwrap --dev-bind / / --tmpfs "$SRC")
[ -d "$SRC-clean" ] && SANDBOX+=(--tmpfs "$SRC-clean")
SANDBOX+=(--tmpfs "$(dirname "$CACHE")" --ro-bind "$T/osil-cache" "$CACHE/osil")
for k in OMP_NUM_THREADS OPENBLAS_NUM_THREADS MKL_NUM_THREADS RAYON_NUM_THREADS; do SANDBOX+=(--setenv "$k" 1); done
SANDBOX+=(--setenv PYTHONDONTWRITEBYTECODE 1)

run() {  # id cwd args...
  local id=$1 cwd=$2; shift 2
  local start end rc
  echo "== $id: cd $cwd; python3 -B -u $*"
  start=$(date +%s.%N)
  set +e
  taskset -c 0,1 "${SANDBOX[@]}" --chdir "$T/research-20260929/$cwd" -- \
    strace -f -yy -e trace=openat,open -o "$T/$id.strace" \
    timeout 600 "$PY" -B -u "$@" > "$T/$id.log" 2>&1
  rc=$?
  set -e
  end=$(date +%s.%N)
  echo "   exit $rc, wall $(awk -v a=$start -v b=$end "BEGIN{printf \"%.2f\", b-a}") s"
  # successful opens of anything under the source checkout (should be none)
  echo "   successful source-tree opens: $(grep -F "$SRC" "$T/$id.strace" | grep -cE '= [0-9]+(<|$)' || true)"
  echo "   attempted source-tree opens:  $(grep -cF "$SRC" "$T/$id.strace" || true)"
  tail -4 "$T/$id.log" | sed 's/^/   | /'
}

run summary publication/eg-recheck summarize.py
run chunk-subset publication/eg-recheck recheck_leaves.py rec/rec_disc2_p7.npz eg_disc2_s 5.642100574331458 0 1024 smoke-subset.npz

cp "$T"/summary.log "$T"/chunk-subset.log "$T"/ "$HERE/"
mkdir -p "$HERE/smoke-out"
mv "$HERE"/summary.log "$HERE"/chunk-subset.log "$HERE"/ "$HERE/smoke-out/"
cp "$T"/*.strace "$HERE/smoke-out/"
cp "$T/research-20260929/publication/eg-recheck/smoke-subset.npz" "$HERE/smoke-out/"
echo "T=$T" > "$HERE/smoke-out/tmp-dir.txt"
