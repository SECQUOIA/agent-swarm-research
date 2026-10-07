#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Run one reproduction command and record wall/CPU/peak RSS and machine load.
#
# usage: run.sh ID CWD MODE 'COMMAND STRING'
#   MODE clean : run inside a private mount namespace in which the main tree
#                /workspace/minlp-notes is replaced by an empty directory,
#                so the command can only see the clean worktree (and ~/.cache).
#   MODE plain : run normally (used only for network downloads and bookkeeping).
# Output: logs/ID.log (stdout+stderr), logs/ID.time (/usr/bin/time -v),
#         one JSON line appended to logs/runs.jsonl.
# Environment inside: OMP/OPENBLAS/MKL_NUM_THREADS=1, PYTHONDONTWRITEBYTECODE=1.
OUT="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/water-audit
MAIN="${_PUBLIC_REPO}"
EMPTY=/tmp/wa_empty
ID=$1; CWD=$2; MODE=$3; CMD=$4
L=$OUT/logs
mkdir -p "$L" "$EMPTY"
T0=$(date +%s.%N); D0=$(date -Is); LA0=$(cat /proc/loadavg); UP0=$(uptime)
if [ "$MODE" = clean ]; then
  /usr/bin/time -v -o "$L/$ID.time" unshare --user --map-root-user --mount bash -c \
    'mount --bind "$1" "$2" && cd "$3" && export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 && eval "$4"' \
    _ "$EMPTY" "$MAIN" "$CWD" "$CMD" > "$L/$ID.log" 2>&1
  RC=$?
else
  /usr/bin/time -v -o "$L/$ID.time" bash -c \
    'cd "$1" && export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 && eval "$2"' \
    _ "$CWD" "$CMD" > "$L/$ID.log" 2>&1
  RC=$?
fi
T1=$(date +%s.%N); D1=$(date -Is); LA1=$(cat /proc/loadavg); UP1=$(uptime)
python3 - "$L" "$ID" "$CWD" "$MODE" "$CMD" "$RC" "$T0" "$T1" "$D0" "$D1" "$LA0" "$LA1" "$UP0" "$UP1" <<'EOF'
import json, sys
L, ID, CWD, MODE, CMD, RC, T0, T1, D0, D1, LA0, LA1, UP0, UP1 = sys.argv[1:]
t = {}
try:
    for ln in open(f"{L}/{ID}.time"):
        if ":" in ln:
            k, v = ln.strip().rsplit(":", 1) if "Elapsed" not in ln else ln.strip().split(": ", 1)
            t[k.strip()] = v.strip()
except FileNotFoundError:
    pass
def num(k):
    try:
        return float(t[k])
    except (KeyError, ValueError):
        return None
rec = dict(id=ID, cwd=CWD, mode=MODE, command=CMD, exit=int(RC), start=D0, end=D1,
           wall_s=round(float(T1) - float(T0), 2),
           cpu_s=round((num("User time (seconds)") or 0) + (num("System time (seconds)") or 0), 2),
           user_s=num("User time (seconds)"), sys_s=num("System time (seconds)"),
           peak_rss_mb=round((num("Maximum resident set size (kbytes)") or 0) / 1024, 1),
           loadavg_start=LA0, loadavg_end=LA1, uptime_start=UP0, uptime_end=UP1,
           log=f"logs/{ID}.log", time_file=f"logs/{ID}.time")
open(f"{L}/runs.jsonl", "a").write(json.dumps(rec) + "\n")
print(json.dumps(rec))
EOF
