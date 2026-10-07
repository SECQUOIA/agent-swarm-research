# Pilot: native SCIP on the deterministic path family

Run on 2026-10-03 with `code/minlp_solver_lab/.venv/bin/python` (PySCIPOpt 6.2.1,
SCIP 10.0), one thread, on the shared host. No cut separator was involved.

## The Proposition 6.1 instance (`pilot_obstruction_root.py`)

Minimize t subject to t >= D(x,y,z) on [0,1]^3, node limit 1.

| Setting | Root dual bound | Types after presolve |
|---|---:|---|
| SCIP defaults | 0.0078125 (= 1/128) | x, z binary; y, t continuous |
| Strong branching disabled (`branching/fullstrong/priority=-1e6`, `branching/relpscost/sbiterquot=0`, `branching/relpscost/initcand=0`) | -0.0558927 | same |

SCIP's presolve changes the types of x and z to binary (D is concave in each
of them). The root cut loop alone reaches -0.0559; root strong branching on
the binary leaves then closes the gap.

## n copies coupled by sum y_i <= 0.9 n (`pilot_native.py`)

| n | Status | Nodes | Seconds | Root dual | Optimum n/128 |
|---:|---|---:|---:|---:|---:|
| 2 | optimal | 5 | 0.05 | -0.182066 | 0.015625 |
| 5 | optimal | 13 | 0.10 | -0.540764 | 0.039062 |
| 10 | optimal | 45 | 0.21 | -0.609502 | 0.078125 |
| 20 | optimal | 121 | 0.46 | -1.452655 | 0.156250 |
| 40 | optimal | 459 | 2.22 | -2.924419 | 0.312500 |
| 80 | optimal | 1660 | 9.16 | -5.863025 | 0.625000 |
| 160 | optimal | 1055 | 18.63 | -11.321115 | 1.250000 |

The root bound decreases roughly linearly in n, while the optimum increases;
SCIP closes the gap by branching.
