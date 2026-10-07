#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
# Review r2: stock binary identity. Writes to stdout.
set -u
SEL="${HOME}"/build-scip/selection
W=/tmp/r2chk; mkdir -p $W; rm -rf $W/tar; mkdir $W/tar
tar xzf "${HOME}"/build-scip/scipoptsuite-10.0.3.tgz -C $W/tar
echo "== tarball sha256"; sha256sum "${HOME}"/build-scip/scipoptsuite-10.0.3.tgz
echo "== source tree used by build-lapack vs tarball (differences)"; diff -rq $W/tar/scipoptsuite-10.0.3 $SEL/scipoptsuite-10.0.3
echo "== stock handler source vs tarball"; cmp $W/tar/scipoptsuite-10.0.3/scip/src/scip/nlhdlr_quadratic.c $SEL/revision-r1-stock/nlhdlr_quadratic.c && echo identical
echo "== link command: tokens differing from build-lapack link.txt"
python3 - <<PY
import shlex
a=shlex.split(open('$SEL/build-lapack/scip/src/CMakeFiles/scip.dir/link.txt').read())
b=shlex.split(open('$SEL/revision-r1-stock/link-argv.txt').read())
print(len(a), len(b), [(x, y) for x, y in zip(a, b) if x != y])
PY
echo "== objects/static libs newer than benchmark binary"; find $SEL/build-lapack \( -name '*.o' -o -name '*.a' \) -newer $SEL/build-lapack/bin/scip
echo "== ldd benchmark vs stock"; diff <(ldd $SEL/build-lapack/bin/scip | awk '{print $1,$3}') <(ldd $SEL/revision-r1-stock/scip-stock | awk '{print $1,$3}') && echo identical
echo "== disassembly of stock handler object vs review-r1 pristine object (/tmp/r1chk/nq_pristine.o)"
if [ -f /tmp/r1chk/nq_pristine.o ]; then
  diff <(objdump -d --no-show-raw-insn /tmp/r1chk/nq_pristine.o | tail -n +4) <(objdump -d --no-show-raw-insn $SEL/revision-r1-stock/quadratic-stock.o | tail -n +4) && echo "identical instructions (objects differ only in embedded source paths)"
fi
echo "== stock log headers/settings vs logs/full scip logs"
cd "${_PUBLIC_REPO}"/research-20261001/scip-set-selection/logs
for d in full_stock full; do echo "-- $d"; for f in $d/*.scip.*.log; do sed -n '/^user parameter/,/^read problem/p' $f | grep ' = ' | sed 's/permutationseed = [12]/permutationseed = X/'; done | sort | uniq -c; done
diff <(sed -n 1,30p full/nvs17.scip.s1.log) <(sed -n 1,30p full_stock/nvs17.scip.s1.log) && echo "nvs17 s1 first 30 lines identical (version, GitHash, libraries, parameters)"
