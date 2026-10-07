#!/bin/sh
# Which vector-library routines numpy 2.5.1 calls for float64 exp and power on this machine (read-only inspection).
SO=$(python3 -c "import numpy._core._multiarray_umath as m; print(m.__file__)")
python3 -c "import numpy; from numpy.lib import introspect as i; print('numpy', numpy.__version__); print(i.opt_func_info(func_name='exp|power', signature='float64'))"
for f in DOUBLE_exp_X86_V4 DOUBLE_power_X86_V4; do
  A=$(nm "$SO" | awk -v f="$f" '$3==f {print $1}')
  echo "== $f at 0x$A: call targets"
  objdump -d --no-show-raw-insn --start-address=0x$A --stop-address=$(printf "0x%x" $((0x$A + 0x700))) "$SO" | grep -o "call .*<[^>]*>" | sed 's/.*</</' | sort | uniq -c
done
