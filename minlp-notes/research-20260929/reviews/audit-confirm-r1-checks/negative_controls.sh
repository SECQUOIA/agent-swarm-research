#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)"
# Negative controls for bound-audit/check_display.py (new) and its first version.
# Works on copies in /tmp; the audit folder is only read.
# The first version is the reviser's copy in /tmp/bound-audit-round1/check_display.py,
# and the pre-revision report is /tmp/bound-audit-round1/audit-report.md.
set -e
BA="${_PUBLIC_REPO}"/research-20260929/bound-audit
T=/tmp/audit-confirm-r1
rm -rf $T; mkdir -p $T/new/logs $T/old/logs
for d in new old; do cp $BA/results.json $T/$d/; cp $BA/logs/cert_socp_*.json $T/$d/logs/; done
cp $BA/check_display.py $T/new/; cp /tmp/bound-audit-round1/check_display.py $T/old/
echo "== new script on the pre-revision report"
cp /tmp/bound-audit-round1/audit-report.md $T/new/audit-report.md; python3 $T/new/check_display.py | tail -1
echo "== first version on the pre-revision report"
cp /tmp/bound-audit-round1/audit-report.md $T/old/audit-report.md; python3 $T/old/check_display.py | tail -1
echo "== new script on the current report"
cp $BA/audit-report.md $T/new/audit-report.md; python3 $T/new/check_display.py | tail -1
mk() { python3 - "$1" "$2" "$BA/audit-report.md" "$T" <<'EOF'
import sys
old, new, src, T = sys.argv[1:]
t = open(src).read()
assert old in t, old
t = t.replace(old, new, 1)
for d in ('new', 'old'):
    open(f'{T}/{d}/audit-report.md', 'w').write(t)
EOF
}
run() { echo "-- $1"; echo "   new:   $(python3 $T/new/check_display.py | tail -1)"; echo "   first: $(python3 $T/old/check_display.py | tail -1)"; }
echo "== controls (unmodified current report: new 'ok 84, failed 8', first 'ok 75, bad 7'; one more failure = caught)"
mk "[508713.7310104, 508713.7310120]" "[508713.7310110, 508719.4912750]"; run "A: sssd22 p4 interval widened to enclose p3 but not p4"
mk "by at least 1.42e-5" "by at least 1.43e-5"; run "B: false 'at least 1.43e-5' for emfl050_3_3"
mk "207.98503480238880…" "207.98503480238881…"; run "C: '…' value rounded up in the last digit"
mk "opt >= 10.40175213162" "opt >= 10.40175213163"; run "D: emfl050_3_3 lower bound 1e-11 too high"
mk "[347691.4104835, 347691.4104845]" "[347691.4104836, 347691.4104845]"; run "E: sssd20 lower end 1e-10 inward"
mk "[18.9136329529, 18.9136329563]" "[18.9136329529, 18.9136329562]"; run "F: Section 8.2 emfl050_5_5 upper end inward"
mk "−983842.2577737, −983842.2577716" "−983842.2577737, −983842.2577717"; run "G: glider100 upper end inward (negative values)"
mk "10729657.585310911…" "10729657.585310912…"; run "H: nd_netgen '…' value rounded up"
