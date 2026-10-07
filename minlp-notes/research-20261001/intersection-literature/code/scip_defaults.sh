#!/bin/bash
# Record SCIP 10.0.3 source facts about quadratic intersection cuts (read-only grep) and
# the defaults reported by PySCIPOpt.
SRC="${HOME}"/build-scip/scipoptsuite-10.0.3/scip
echo "== CHANGELOG section headers (line numbers)"; grep -n "^@section RN\(1000\|900\|800\) " $SRC/CHANGELOG
echo "== CHANGELOG lines on quadratic intersection cuts"; grep -n -i "intersection cut\|separation via intersection\|sepa_interminor\|nlhdlr/quadratic/useintersectioncuts" $SRC/CHANGELOG
echo "== nlhdlr_quadratic.c defaults and sub-SCIP switch"
grep -n "define DEFAULT_USEINTERCUTS\|define DEFAULT_USESTRENGTH\|define DEFAULT_USEMONOIDAL\|define DEFAULT_USEBOUNDS\|define DEFAULT_NCUTSROOT\|define DEFAULT_NCUTS \|SCIPgetSubscipDepth(scip) > 0\|@author" $SRC/src/scip/nlhdlr_quadratic.c
grep -n -A1 "If we are in a subSCIP we don't want to separate intersection cuts" $SRC/src/scip/nlhdlr_quadratic.c
echo "== sepa_interminor.c default"; grep -n "define SEPA_FREQ\|define DEFAULT_" $SRC/src/scip/sepa_interminor.c | head -8
echo "== PySCIPOpt"
python3 -c "
import pyscipopt as ps
m = ps.Model(); print('SCIP', m.version() if hasattr(m,'version') else '', 'PySCIPOpt', ps.__version__)
for p in ['nlhdlr/quadratic/useintersectioncuts','nlhdlr/quadratic/usestrengthening','nlhdlr/quadratic/usemonoidal','nlhdlr/quadratic/useboundsasrays','nlhdlr/quadratic/sparsifycuts','separating/interminor/freq']:
    print(p, '=', m.getParam(p))
"
