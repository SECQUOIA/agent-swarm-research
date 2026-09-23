#!/bin/bash
D=/home/sgusev/repo/minlp-notes/code/minlp_solver_lab
while ! grep -q DONE $D/instances/download.log; do sleep 10; done
RESLIM=${1:-60}; PAR=${2:-7}
for n in $(cat $D/instances/convex_discrete_names.txt); do for s in baron scip dicopt sbb shot antigone gurobi; do echo "$n $s $RESLIM"; done; done | xargs -P $PAR -L 1 $D/baseline/run_one.sh
echo ALLDONE
