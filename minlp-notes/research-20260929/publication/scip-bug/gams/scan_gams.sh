#!/bin/sh
# usage: scan_gams.sh KEY WITNESS_VALUE SEEDS...   (default SCIP settings + randomization/randomseedshift)
cd "$(dirname "$0")"
k=$1; w=$2; shift 2
for s in "$@"; do
  printf 'randomization/randomseedshift = %s\n' "$s" > seed.opt
  ./run_gams.sh $k.gms ${k}_seed$s seed.opt > /dev/null
  st=$(grep "SCIP Status" logs/gams_${k}_seed$s.log | head -1 | sed 's/.*: //')
  db=$(grep "Dual Bound" logs/gams_${k}_seed$s.log | head -1 | awk '{print $4}')
  pb=$(grep "Primal Bound" logs/gams_${k}_seed$s.log | head -1 | awk '{print $4}')
  nd=$(grep "Solving Nodes" logs/gams_${k}_seed$s.log | head -1 | awk '{print $4}')
  v=$(python3 -c "print('WRONG' if '$st'.startswith('problem is solved [optimal') and float('$db') > $w + 1e-4 else 'ok')")
  echo "$k seed $s: $st dual $db primal $pb nodes $nd $v"
done
