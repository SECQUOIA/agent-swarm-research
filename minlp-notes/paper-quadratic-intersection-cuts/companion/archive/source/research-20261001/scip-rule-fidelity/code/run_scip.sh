#!/bin/bash
# Run the instrumented SCIP binary on one instance and write the intersection-cut dump.
# Usage: run_scip.sh INSTANCE_FILE OUTDIR TIMELIMIT [SETTINGS]
set -u
BIN="${HOME}"/build-scip/fidelity/build/bin/scip
f=$1; out=$2; tl=$3; set=${4:-$(dirname "$0")/intercuts_on.set}
name=$(basename "$f"); name=${name%.*}
mkdir -p "$out"
rm -f "$out/$name.jsonl" "$out/$name.jsonl.gz"
SCIP_INTERCUT_DUMP="$out/$name.jsonl" timeout $((tl * 3 + 120)) "$BIN" \
  -c "set load $set set limits time $tl read $f optimize display statistics quit" \
  > "$out/$name.log" 2>&1
echo "$name exit $?" >> "$out/exitcodes.txt"
gzip -f "$out/$name.jsonl" 2>/dev/null
