#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
G="${HOME}"/.local/opt/gams/gams54.3_linux_x64_64_sfx/gams
S="${_PUBLIC_REPO}"/research-20260929/publication/solver-runs/gms
for n in $(cat "${_PUBLIC_REPO}"/research-20260929/publication/solver-runs/instances.txt); do
  mkdir -p $n; cd $n; printf 'OSiL\n' > convert.opt
  OMP_NUM_THREADS=1 $G $S/$n.gms NLP=CONVERT MINLP=CONVERT optfile=1 threads=1 lo=2 logfile=c.log o=c.lst trace=c.trc traceopt=3 > /dev/null 2>&1
  echo "$(date -u +%FT%TZ) $n rc=$? $(stat -c %s osil.xml 2>/dev/null)"
  cd ..
done
echo DONE
