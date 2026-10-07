#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../../../../.." && pwd)"
# Review r1: build two comparison binaries in /tmp/r1chk without touching $HOME/build-scip/selection.
#   scip-pristine-lapack : nlhdlr_quadratic.c from the 10.0.3 tarball (unpatched)
#   scip-nocapture       : patched nlhdlr_quadratic.c with the SCIPcaptureRow block removed
# Both are compiled with the C flags of build-lapack and linked with build-lapack's link line, replacing only the
# nlhdlr_quadratic object. The same procedure applied to the patched source gives an object byte-identical to
# build-lapack/scip/src/CMakeFiles/scip.dir/scip/nlhdlr_quadratic.c.o (and likewise for build-debugsol).
set -e
SEL="${HOME}"/build-scip/selection
S=$SEL/scipoptsuite-10.0.3
B=$SEL/build-lapack
PATCH="${_PUBLIC_REPO}"/research-20261001/scip-set-selection/patch/scip-10.0.3-setrule.patch
GCC="${HOME}"/miniconda3/envs/scipbuild/bin/gcc
W=/tmp/r1chk
mkdir -p $W && cd $W
tar xzf "${HOME}"/build-scip/scipoptsuite-10.0.3.tgz scipoptsuite-10.0.3/scip/src/scip/nlhdlr_quadratic.c
mkdir -p a/scip/src/scip && cp scipoptsuite-10.0.3/scip/src/scip/nlhdlr_quadratic.c a/scip/src/scip/
(cd a && patch -p1 < $PATCH)
python3 - <<'EOF'
s = open('/tmp/r1chk/a/scip/src/scip/nlhdlr_quadratic.c').read()
old = """            SCIP_CALL( SCIPcaptureRow(scip, row) );
            nlhdlrdata->cutrows[nlhdlrdata->ncutrows++] = row;"""
assert s.count(old) == 1
open('/tmp/r1chk/nq_nocapture.c', 'w').write(s.replace(old, "            (void) row;"))
EOF
FLAGS="-DSCIP_STATIC_DEFINE -I$B/scip -I$S/scip/src -I$S/scip/src/amplmp/include -I$S/soplex/src -I$S/zimpl/src -I$S/papilo/src -I$S/ug/src -I$S/gcg/src -I$S/scip/src/nauty -I$B/soplex -O3 -DNDEBUG -std=c99 -ffp-contract=off -D_XOPEN_SOURCE=600"
cd $B/scip/src
$GCC $FLAGS -o $W/nq_patched.o -c $S/scip/src/scip/nlhdlr_quadratic.c
cmp $W/nq_patched.o CMakeFiles/scip.dir/scip/nlhdlr_quadratic.c.o && echo "patched object identical to build-lapack object"
$GCC $FLAGS -o $W/nq_pristine.o -c $W/scipoptsuite-10.0.3/scip/src/scip/nlhdlr_quadratic.c
$GCC $FLAGS -o $W/nq_nocapture.o -c $W/nq_nocapture.c
for v in pristine nocapture; do
  CMD=$(sed "s#CMakeFiles/scip.dir/scip/nlhdlr_quadratic.c.o#$W/nq_$v.o#; s#-o ../../bin/scip#-o $W/scip-$v-bin#" CMakeFiles/scip.dir/link.txt)
  bash -c "$CMD"
done
mv $W/scip-pristine-bin $W/scip-pristine-lapack; mv $W/scip-nocapture-bin $W/scip-nocapture
ls -la $W/scip-pristine-lapack $W/scip-nocapture
