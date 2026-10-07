# Floating-point provenance checks (evidence, not proofs)

All runs single-threaded on 2026-10-01. GAMS 54.3 at
/workspace/local-home/.local/opt/gams/gams54.3_linux_x64_64_sfx/gams.

- dtoc5_coef_check.py -> dtoc5_coef_check.log: damped Newton on the reduced
  DTOC5 chain with dynamics coefficient c*h on y^2 (c=1: Coleman-Liao /
  CUTEst; c=4: QPLIB_8585 / MINLPLib dtoc5). c=1 reproduces Coleman-Liao
  (1993) Table 3 (problem 5) to all printed digits; c=4, N=50000 reproduces
  the MINLPLib value 5.389672119181.
- optcdeg2_coef_check.gms -> optcdeg2_coef_check.log: IPOPT local solves of
  OPTCDEG2 with quadratic damping 0.05*dt (CUTEst SIF) and 0.2*dt
  (QPLIB_8803 / MINLPLib). Damping 0.05 reproduces the SIF SOLTN values for
  T = 10, 40, 100, 400; damping 0.2 at T = 50000 gives 293.8762 (MINLPLib
  primal 293.8760751).
  Command: gams optcdeg2_coef_check.gms --T=<T> --damp=<d> --solver=ipopt lo=0 threads=1
- lukvle10_local_check.gms -> .log: IPOPT and CONOPT from the SIF start
  point, N = 1000 (IPOPT 353.12245 = MINLPLib p1; CONOPT failed).
- lukvle10_tolerance_check.gms -> .log: IPOPT from MINLPLib point p5 with
  every constraint relaxed to |c_j| <= tol. tol = 1e-6 gives 352.23762,
  which prints as 3.52237E+02, the SOLTN value in LUKVLE10.SIF.
  p5start.inc was generated from open-instances/minlplib_sol/lukvle10.p5.sol.

## Added in revision 1 (2026-10-02)

- qplib_camshape_compare.py -> qplib_camshape_compare.log: parses the QPLIB
  camshape copies (QPLIB_2738/2480/2703/3177) and MINLPLib camshape100/200/
  400/800 GAMS files (stored in ../sources/qplib/camshape_copies/), matches
  every row by monomial support and sense, and reports the largest relative
  coefficient and bound differences (all <= 2.5e-10). It then evaluates the
  MINLPLib p1 point and the QPLIB solution point in both models with exact
  rational arithmetic on the printed decimals (objective row excluded from
  the violation). Data comparison, not a proof about optimal values.
  Command: python3 qplib_camshape_compare.py <minlplib.gms> <qplib.gms> <minlplib.p1.sol> <qplib.sol>
- qplib_dtoc5_optcdeg2_identity.log: diff of MINLPLib dtoc5.gms / optcdeg2.gms
  against QPLIB_8585.gms / QPLIB_8803.gms with comment lines removed. The
  only differences are the solve statement and a redundant "Positive
  Variables" line for two variables that both files fix at 0.
- mittelmann_values_vs_certified.py -> .log: printed values from the 2026
  Mittelmann cnconv logs minus our certified optima (decimal arithmetic).
