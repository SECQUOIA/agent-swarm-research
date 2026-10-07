<!-- Written to disk by the root from the structured return value of agent 'author:primal-powerflow' (the harness blocks subagents from writing report files). Status: complete; minor-review fixes applied 2026-10-03. -->

All three instances have proofs of exactly feasible points. The full report is on disk. Independent review r1 verified the enclosures and gaps with its own OSIL reader and interval code.

# Exactly feasible primal points for powerflow0030p, powerflow0039p, powerflow0039r

## 1. Results

For each instance, a computer-assisted proof shows that an exactly feasible point of the cached OSIL model exists in a stored box of radius 1e-45. Enclosure endpoints are rounded outward at 22 decimals. Gaps are (upper end of the enclosure − our dual), computed in exact rationals and rounded up.

| instance | point file | free / fixed variables | objective enclosure | our dual | gap (abs) | gap (rel. to dual) |
|---|---|---|---|---|---|---|
| powerflow0030p | points/powerflow0030p.json | 222 / 14 | [576.8934134703742598676683, 576.8934134703742598676684] | 576.8934122988004 | <= 1.171573860e-6 | <= 2.030833e-9 |
| powerflow0039p | points/powerflow0039p.json | 262 / 20 | [41869.0515113202038027683844, 41869.0515113202038027683845] | 41869.05148485014 | <= 2.6470063803e-5 | <= 6.32211e-10 |
| powerflow0039r | points/powerflow0039r.json | 270 / 12 | [41869.0515113209830932768581, 41869.0515113209830932768582] | 41869.05148327243 | <= 2.8048553094e-5 | <= 6.69912e-10 |

Points to note:
- The optimal value of each instance therefore lies rigorously in [dual, upper end of the enclosure]. For 0030p this is [576.8934122988004, 576.8934134703742598676684].
- Each dual bound lies below the lower end of its enclosure. This is a consistency check that any valid dual bound must pass.
- **Comparison with MINLPLib's p1** (p1's objective evaluated at 50 digits). p1 violates rows by up to 2.1e-13 (0030p), 1.2e-12 (0039p) and 7.9e-12 (0039r). Our exactly feasible points have objectives above obj(p1) by 2.87e-12, 4.64e-12 and 1.83e-10.
- The summary's gaps (2.0e-9, 6.3e-10 and 6.7e-10 relative) are unchanged at the displayed precision.
- The summary's sentence that "no exactly feasible point was constructed" for powerflow0030p/0039p/0039r is now out of date.

**What each point is.**
- **Fixed variables** are exact rationals. There are three kinds:
  - variables fixed by single-variable equality rows (reference angle or reference f = 0, and fixed or zero flows at buses with one branch);
  - variables at an active single-variable bound row, set exactly to that bound:
    - 0030p: x29 = 21/20;
    - 0039p: x30–x36 and x38 = 53/50; Pg x264, x266, x267, x269, x270 at their upper bounds; Qg x273 = 7/5 at its lower bound;
    - 0039r: the same six generator bounds. p1 violates x269 <= 5.8 (e362) by 9e-14, x266 <= 6.52 (e359) by 4e-14 and x267 <= 5.08 (e360) by 3e-14. It also violates voltage rows e307, e309–e313 and e315 by 2.0e-14–6.7e-14.
  - the remaining degrees of freedom, kept at p1's decimal values. Column-pivoted QR chose them:
    - 0030p: x225, x227, x228, x232–x236;
    - 0039p and 0039r: x263, x265, x268, x271, x282.
- **Free variables.** The file stores a 60-digit centre c. The point x* is the unique solution of the stored square system S in [c − 1e-45, c + 1e-45]. The Krawczyk image confines it to about 6e-57 of c.
- **The square system S** contains every equality row that does not fix a single variable. It also contains each active multi-variable inequality row, as an equality at its active side:
  - 0030p: line limits e208 and e211;
  - 0039r: voltage rows e307–e313 and e315 (e² + f² = 1.06²);
  - 0039p: none.

## 2. Method

**1. construct.py (floating point; not part of the proof).**
- Start from p1 (open-instances-wave3/sol/<name>.p1.sol; missing entries are 0).
- Find the active set with cutoff slack < 1e-9. The separation is clean: active slacks in absolute value are at most 1.7e-16 (0030p), zero at p1's stored decimals (0039p), and 6.8e-13 (0039r). In 0039r, e363 has slack 6.8e-13 and e386 has slack 2.1e-13, and the next smallest are 4.3e-4, 1.08e-3 and 2.3e-3.
- Fix variables as described in Section 1.
- Run a simplified Newton iteration at 70 digits with a float64 LU factorization. The residual fell to about 1e-68 in 4 steps.
- Condition numbers of the Jacobian: 1.0e4, 2.0e4 and 5.0e4.
- The free variables moved from p1 by at most 1.4e-14, 2.5e-13 and 7.8e-12.

**2. certify.py (the proof).** It reads only the point JSON and the OSIL file. It uses mpmath iv at 80 digits and compares interval endpoints exactly as Fractions.
- **(a) Structure.** The free and fixed variables partition the variables, |S| = #free, and every side used is valid.
- **(b) Krawczyk test.** K = c − C F(c) + (I − C J(X))(X − c), where:
  - C is a float64 inverse;
  - F(c) is enclosed in intervals, with the fixed variables enclosed from their exact rationals;
  - J(X) comes from forward-mode interval differentiation of the OSIL expression trees.

  K lies inside the open box for every component, with max |K − c|/r <= 5.4e-12. The Krawczyk inclusion gives existence (Moore 1977). Uniqueness follows separately because ||I − C J(X)||∞ < 1: a check of the stored boxes gives upper bounds 1.930e-12, 2.855e-12 and 5.376e-12 (`logs/minor_review_check.log`). If F(x) = F(y) = 0 in the convex box X, the mean-value matrix A belongs to J(X) and x − y = (I − C A)(x − y); the strict contraction forces x = y. The same bound makes C A invertible and hence makes C nonsingular. This supplies the needed argument without an unverified theorem number in Neumaier's book.
- **(c) Every OSIL row is checked.** Each row is either in S, checked exactly in rationals (all its variables fixed and the row linear), or checked by an interval enclosure over X. The script asserts that every equality row is in S or exact.

| instance | rows | in S | exact | interval | smallest interval margin |
|---|---|---|---|---|---|
| 0030p | 555 | 222 | 23 | 310 | 4.30e-4 at e215 |
| 0039p | 657 | 262 | 39 | 356 | 1.08e-3 at e346 |
| 0039r | 473 | 270 | 23 | 180 | 2.29e-3 at e306 |

  The models have no variable bounds and no integer variables; the script asserts both.
- **(d) Objective** enclosed over X.

**3. scip_check.py (evidence only).** SCIP 10's own OSIL reader loads each model, and checkSol on the original problem at feastol 1e-9 accepts all three centres (rounded to double). SCIP's objectives are 576.8934134703743, 41869.0515113202 and 41869.051511320984. This guards against a parsing error in our reader.

**4. Negative tests** (on a copy in /tmp, since deleted). Each altered point was rejected as intended:
- A centre coordinate moved by 1e-8: Krawczyk fails, and SCIP also rejects the point.
- Fixed voltage x29 raised 1e-12 above its bound (then construct and certify re-run): certify stops with "row e300 fails exactly", while SCIP still accepts the point.
- Row e208 removed from S: the structure check fails.
- e208 used at the wrong side: certify fails.

**5. Radius 1e-30.** The test also passes at this radius, with the same enclosures (logs/certify_r1e-30.*.log).

## 3. What is proved, and the assumptions

**Proved.** For each instance there is a point with these properties:
- its fixed coordinates are the stored rationals, and its free coordinates lie in the stored box;
- it satisfies every OSIL constraint exactly;
- the model has no bounds or integrality to check;
- its objective lies in the stated enclosure.

The rigorous gap to our dual is at most the stated value.

**Numerical only** (none of it enters the proof): the construction, the SCIP check, and the condition numbers.

**Assumptions.**
- mpmath 1.3.0 iv encloses +, −, ×, /, sin, cos and the conversion of decimal strings and integers correctly.
- Python Fraction arithmetic is exact.
- osilx.py, the verification review's OSIL reader, parses the files correctly. Its dependency is `research-20260929/reviews/open-instances-verification/osilx.py`, SHA-256 `4bcdc1d830bd3fc0392756f10b3e5daccbce218198543e402158a24cf986a465` (checked for this revision). The SCIP cross-check and r1's independent reader support the reading.
- pfmodel.py supports exactly the node types used (sum, product, square, sin, cos, number, variable); any other node raises an error.
- The dual bounds are the summary's displayed values. This track did not re-check them.

**Reproducibility.** Re-running construct.py can change centre digits beyond about 1e-60, because the float corrections depend on BLAS threading. This happened once for 0030p. The certificate is the stored file. SHA-256 of the stored files:
- 0030p: 4b0635996f6a303f02773ba37d1f47d141656cc5d48444f4663fc32fd9f45c12
- 0039p: acef65dac3106ce204a569674a699036d5ecb975431d9c64059c4b13285e50b2
- 0039r: e851cfb4fcd5c0fd704d0c17630c3f90a99e97aa93bde9e36acd3df5ec091fed

## 4. Point file format

Each point file is JSON with these keys:
- instance;
- radius ("1e-45");
- system: a list of {row, side}, where side is lb for equality rows and the active side otherwise;
- fixed: {var: {value: "p/q", reason}};
- free: {var: 60-significant-digit decimal centre}.

The point is the unique solution of S in [centre − radius, centre + radius], with the fixed variables at their rationals.

## 5. Files

All in /workspace/minlp-notes/research-20260929/publication/primal/powerflow/:
- pfmodel.py: OSIL access and forward-mode evaluation for mp or iv;
- construct.py;
- certify.py;
- scip_check.py;
- points/*.json;
- logs/construct.<name>.log, logs/certify.<name>.log, logs/certify_r1e-30.<name>.log, logs/scip_check.<name>.log.

## 6. References

- Krawczyk, Computing 4 (1969) 187–201.
- Moore, SIAM J. Numer. Anal. 14 (1977) 611–615.
- Neumaier, Interval Methods for Systems of Equations (1990), Ch. 5.

## Commands run (from the agent's structured return)

- `Exploration (inline python3 -c, exit 0): summarized the OSIL row structure; listed missing p1 entries; listed the smallest inequality slacks at p1 at 50 digits; tested mpmath iv conversions; tested that pyscipopt reads OSIL`
- `First runs, with numpy's default BLAS threads (briefly about 10 cores, 5 s wall): python3 construct.py powerflow0030p|0039p|0039r (exit 0); python3 certify.py <name> (exit 0, all PROVED); python3 scip_check.py <name> (exit 0, feasible = True)`
- `Negative tests in /tmp/pfneg (since deleted): perturbed centre by 1e-8, fixed bound +1e-12, S row removed, wrong side; each altered point was rejected as intended (AssertionError)`
- `Final runs with OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1, in /workspace/minlp-notes/research-20260929/publication/primal/powerflow: for n in powerflow0030p powerflow0039p powerflow0039r: python3 construct.py $n > logs/construct.$n.log; python3 certify.py $n > logs/certify.$n.log; python3 scip_check.py $n > logs/scip_check.$n.log (all exit 0; each under 5 s)`
- `python3 certify.py <name> 1e-30 > logs/certify_r1e-30.<name>.log for all three (exit 0, PROVED)`
- `After adding a side-consistency assertion to certify.py: python3 certify.py <name> rerun for all three (exit 0, PROVED; the current logs are from this version)`
- `sha256sum points/*.json`

## Open issues (from the agent's structured return)

- Independent review r1 verified all three stored point certificates. The original author checks and SCIP floating-point cross-check are listed above.
- The OSIL parse relies on the reused osilx.py reader. SCIP's independent reader agrees, but only in floating point.
- The early (pre-final) runs used multi-threaded BLAS briefly (about 50 s of user time in total). All final runs were single-threaded.
- open-instances-summary.md still says that no exactly feasible point was constructed for powerflow0030p/0039p/0039r. Integration should update it; this track did not edit it. For valid upper bounds, use primal displays 41869.0515113203 (0039p) and 41869.0515113210 (0039r). The relative gaps stay 6.3e-10 and 6.7e-10 at summary precision.

## Response to review

Review: `../../reviews/primal-powerflow-review-r1.md`. Checked and resolved on 2026-10-03.

| issue | resolution and evidence |
|---|---|
| 1. Missing report and commands | The complete report is on disk, including the per-instance construction, radius checks, SCIP commands and mpmath assumptions. |
| 2. Active-slack bound | Corrected the 0039r maximum to 6.8e-13, with e363/e386 examples; recomputed slacks at stored p1 values. |
| 3. Incomplete p1 violations | Added x266/x267 violations and all seven violated voltage rows; `logs/minor_review_check.log` records them. |
| 4. External reader dependency | Recorded the exact path and verified SHA-256 of osilx.py; no copy or interface change needed. |
| 5. Summary primal displays | Recorded upward displays 41869.0515113203 (0039p) and 41869.0515113210 (0039r); enclosures and relative gaps unchanged. |
| 6. Uniqueness citation | Checked ||I − C J(X)||∞ < 1 on each stored box and gave the mean-value contraction argument. Moore 1977 is cited for existence; no inaccessible theorem number is asserted. |

Targeted check: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/primal/powerflow/minor_review_check.py > research-20260929/publication/primal/powerflow/logs/minor_review_check.log` (from the repository root). Results are in `logs/minor_review_check.log`. No main computation, solver campaign, project-wide verification or CI check was run for this revision.
