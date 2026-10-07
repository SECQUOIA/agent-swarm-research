#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
G="${HOME}"/.local/opt/gams/gams54.3_linux_x64_64_sfx/gams
cd "${_PUBLIC_REPO}"/research-20260929/publication/reviews/lit-control-r1/gms
for N in 10 100 500 1000; do $G dtoc5.gms --N=$N --c=1 --solver=ipopt lo=0 threads=1 o=dtoc5_${N}_1.lst > /dev/null 2>&1; done
for T in 10 40 100 400; do $G optc.gms --T=$T --D=0.05 lo=0 threads=1 o=optc_${T}.lst > /dev/null 2>&1; done
for t in 0 1e-6 1e-5; do timeout 900 $G lv.gms --tol=$t lo=0 threads=1 o=lv_$t.lst > /dev/null 2>&1; done
$G dtoc5.gms --N=50000 --c=4 --solver=ipopt lo=0 threads=1 reslim=1500 o=dtoc5_50000_4.lst > /dev/null 2>&1
$G dtoc5.gms --N=50000 --c=1 --solver=ipopt lo=0 threads=1 reslim=1500 o=dtoc5_50000_1.lst > /dev/null 2>&1
$G optc.gms --T=50000 --D=0.2 lo=0 threads=1 reslim=1500 o=optc_50000_02.lst > /dev/null 2>&1
$G optc.gms --T=50000 --D=0.05 lo=0 threads=1 reslim=1500 o=optc_50000_005.lst > /dev/null 2>&1
echo ALLDONE
