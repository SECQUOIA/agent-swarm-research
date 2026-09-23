# SCIP 10 exact mode + VIPR certificate toolchain (build record, 2026-09-12)

Prefix: `/home/sgusev/.local/opt/scip-exact` (binaries in `bin/`: `scip`, `soplex`, `viprchk`, `viprchk_parallel`, `viprttn`, `viprcomp`, `viprincomp`, `vipr2html`).
Build trees and test files: `/home/sgusev/build-scip/` (`scipoptsuite-10.0.3/`, `build-suite/`, `vipr/`, `build-vipr/`, `test/`).

## Versions

- SCIP 10.0.3 (GitHash d409edf9f6), SoPlex 8.0.3, from `https://scipopt.org/download/release/scipoptsuite-10.0.3.tgz` (latest release tag on GitHub at build time: v10.0.3).
- VIPR: `https://github.com/scipopt/vipr` commit `30f2951d` (2025-10-29), certificate format 1.0 (spec files `cert_spec_v1_0.md`, `cert_spec_v1_1.md` in the repo).
- Linked libraries (from `scip -v`): GMP 6.3.0, MPFR 4.2.2, Boost 1.85.0, Readline 8.3, ZLIB 1.3.2, CppAD, Nauty 2.8.8, sassy 2.1, TinyCThread.
- Toolchain: conda-forge gcc/g++ 16.2.0, cmake 4.4.3, make (conda env `scipbuild`).

## Prerequisites

System (Ubuntu 24.04 under WSL2) has cmake 3.28, gcc 13.3, make, zlib1g-dev, but not `libgmp-dev`, `libmpfr-dev`, `libboost-dev`, `libreadline-dev`, and `sudo` needs a password (`apt-get` failed non-interactively). Fallback used:

```
mamba create -y -n scipbuild -c conda-forge cmake gmp mpfr boost-cpp zlib readline ncurses gcc gxx make tbb-devel
mamba install -y -n scipbuild -c conda-forge patchelf   # for the RPATH fix below
```

The installed binaries depend on the conda env's shared libraries (`libgmp`, `libgmpxx`, `libmpfr`, `libreadline`, `libz`, `libstdc++`) via RPATH, so `/home/sgusev/miniconda3/envs/scipbuild` must not be deleted. System Python and the repo's uv environment were not touched.

## SCIP/SoPlex configure and build

```
P=/home/sgusev/miniconda3/envs/scipbuild
PREFIX=/home/sgusev/.local/opt/scip-exact
cd /home/sgusev/build-scip && mkdir build-suite && cd build-suite
CC=$P/bin/gcc CXX=$P/bin/g++ $P/bin/cmake ../scipoptsuite-10.0.3 \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$PREFIX \
  -DCMAKE_PREFIX_PATH=$P -DCMAKE_INSTALL_RPATH="$PREFIX/lib;$P/lib" -DCMAKE_BUILD_RPATH="$P/lib" \
  -DEXACTSOLVE=ON -DGMP=ON -DMPFR=ON -DBOOST=ON -DLPS=spx -DLPSEXACT=spx \
  -DPAPILO=OFF -DIPOPT=OFF -DZIMPL=OFF -DGCG=OFF -DUG=OFF -DAMPL=OFF -DREADLINE=ON -DZLIB=ON -DSHARED=ON
make -j8 scip libscip && make -j8 install
```

Notes:
- The SCIP 10 option is `EXACTSOLVE` (AUTO/ON/OFF; needs GMP, MPFR, Boost >= 1.68) plus `LPSEXACT=spx`. Configure output confirms: "Building SCIP with support for exact solving mode using exact LP solver SoPlex."
- `make install` stripped the conda lib dir from the RPATH of the *executables* (kept it in `libscip.so` and `libsoplexshared.so`), so `scip` failed with `libgmpxx.so.4: cannot open shared object file`. Fixed with:
  `for f in $PREFIX/bin/scip $PREFIX/bin/soplex; do $P/bin/patchelf --set-rpath "$PREFIX/lib:$P/lib" $f; done`
- Installed: `bin/scip`, `bin/soplex`, `lib/libscip.so.10.0.3`, `lib/libsoplexshared.so.8.0.3`, `lib/libsoplex.a`, `lib/libsoplex-pic.a`, cmake configs in `lib/cmake/{scip,soplex}`.

## VIPR build

VIPR's CMake has no install target; binaries were copied. `viprcomp` (completer) needs SoPlex + Boost + zlib and is found through the installed `soplex-config.cmake`; `viprchk_parallel` needs TBB (from conda; otherwise it downloads oneTBB).

```
cd /home/sgusev/build-scip && git clone https://github.com/scipopt/vipr.git && mkdir build-vipr && cd build-vipr
CC=$P/bin/gcc CXX=$P/bin/g++ $P/bin/cmake ../vipr/code -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="$PREFIX;$P" -DCMAKE_BUILD_RPATH="$PREFIX/lib;$P/lib" -DVIPRCOMP=ON
make -j8
cp viprchk viprchk_parallel viprttn vipr2html viprcomp viprincomp $PREFIX/bin/
```

## Verified command sequence

Parameters (from `scip/doc/xternal.c`, page EXACT, and `grep '"exact/' src/scip/*.c`): `exact/enable` (must be set before `read`), `certificate/filename`, `certificate/maxfilesize`; advanced ones under `exact/` (`safedbmethod`, `cutmaxdenom`, `lpinfo`, ...).

Example that needs the LP and branching (`/home/sgusev/build-scip/test/knap.lp`):

```
Maximize
 obj: 10 x1 + 13 x2 + 8 x3 + 7 x4 + 9 x5
Subject To
 c1: 11 x1 + 15 x2 + 9 x3 + 8 x4 + 12 x5 <= 27
Binaries
 x1 x2 x3 x4 x5
End
```

```
export PATH=/home/sgusev/.local/opt/scip-exact/bin:$PATH
scip -c "set exact enable TRUE" -c "set certificate filename knap.vipr" \
     -c "read knap.lp" -c "optimize" -c "display solution" -c "quit"
#   SCIP Status : problem is solved [optimal solution found];  Solving Nodes : 11
#   Exact Primal Bound : 23   Exact Dual Bound : 23
#   closing certificate file (wrote approx. 0.0 MB)      -> writes knap.vipr and knap.vipr_ori
viprcomp knap.vipr            # "Completed 10 out of 85 ... Completion of File successful!" -> knap_complete.vipr
viprchk  knap_complete.vipr   # "Successfully checked solution for feasibility."
                              # "Successfully verified optimal value range [-23, -23]."   (internally minimizes -obj)
viprttn  knap_complete.vipr   # optional tightening; writes knap_complete.vipr.opt (45 of 85 derivations kept)
viprchk  knap_complete.vipr.opt   # "Successfully verified optimal value range [-23, -23]."
viprchk  knap.vipr_ori        # "Successfully verified." (feasibility of the best solution in the original problem, DER 0)
vipr2html knap_complete.vipr  # writes knap_complete.vipr.html
```

Findings about the tools:
- `viprchk` on the raw `knap.vipr` reports "Verification failed": with cutting-plane separation on (default), SCIP writes incomplete ("weak") derivations, exactly as the SCIP docs state; `viprcomp` must run first. This is the same order SCIP's own ctest uses (`scip/check/CMakeLists.txt`, tests `MIPEX-*-viprcomp` then `-vipr`; pass regex `Successfully verified|Infeasibility verified`).
- `viprttn` exits with status 255 even on success; judge it by the presence of the `.opt` file and a subsequent `viprchk`. It also prints a benign "non-ascending indices" warning on the tightened file.
- `viprchk` exit status is 0 on success and 255 on failure.
- Helper used for the runs: `/home/sgusev/build-scip/test/run_chain.sh <file.lp> <tag> [extra -c settings]`.

## Failure: certificate for a root-node-only instance

The tiny requested instance (`gap.lp`: min x+y s.t. 2x+2y >= 3, x,y binary; LP bound 1.5, optimum 2) is solved by SCIP exact mode correctly (Exact Primal/Dual Bound 2), but with default settings the root node is closed by domain propagation plus the trivial heuristic **without any LP solve** (`primal LP ... 0` calls). The written certificate contains the bound derivations x >= 1 and y >= 1 (`GlobalBound_8`, `GlobalBound_12`) but no final derivation of the objective bound x + y >= 2, so both `viprchk gap.vipr` and `viprchk gap_complete.vipr` end with:

```
Failed to derive lower bound.
Proved:      ( 1 ) t_y >= 1 ( 1 )
Instead of:  ( 1 ) t_x + ( 1 ) t_y >= 2 ( 2 )
Verification failed.
```

Cause (from source): `scip/src/scip/solve.c` `applyBounding()` only prints the pseudo-objective dual bound when `focusnode->number != 1`, and the exact-mode cutoff path at solve.c:4498 did not fire here. Turning off the trivial heuristic alone (`set heuristics trivial freq -1`) does not help. Workaround that works: force the root LP by disabling heuristics:

```
scip -c "set exact enable TRUE" -c "set certificate filename gap.vipr" -c "set heuristics emphasis off" \
     -c "read gap.lp" -c "optimize" -c "quit"
viprchk gap.vipr             # "Successfully verified optimal value range [2, 2]."  (no viprcomp needed: no cuts)
```

Conclusion: for benchmark use, always run `viprcomp` then `viprchk` and treat "Verification failed" as a real signal; trivially small instances that never solve an LP can produce unverifiable certificates in 10.0.3 (worth reporting upstream).

## Input-format findings (exact parsing)

`SCIPrationalSetString` (`scip/src/scip/rational.cpp`) converts decimal strings to exact fractions (`0.1` -> `1/10`, exponents handled) and accepts `a/b`. Both the LP and MPS readers use it in exact mode:

- LP file with `0.1 x + 0.1 y >= 0.15` -> certificate CON line `C0 G 15/100 2 0 1/10 1 1/10` (exact, not the binary double).
- LP file with `1/10 x + 1/10 y >= 3/20` -> `C0 G 3/20 2 0 1/10 1 1/10` (fraction syntax accepted in `.lp`).
- MPS (fixed format) with `0.1` / `0.15` -> `C0 G 3/20 2 0 1/10 1 1/10`, verified end to end (`viprchk`: "Successfully verified optimal value range [2, 2]", run with heuristics off because of the root-node issue above).

Propagation-derived bounds in the certificate use floating-point-safe rounding of activities (e.g. `2251799813685247/45035996273704960` in place of 1/20), which is valid (weaker) and checks fine.
