# Mathematical review of supplement S1.1–S1.5

**Verdict: revision required for this area: one major proof-description issue and three minor corrections. No blocker or counterexample to a displayed optimal value, lower bound, upper bound, or certificate gap was found.** The analytic arguments are sound in the cases checked. In particular, the Gibbs implementation uses a valid Hessian construction; issue 1 concerns the supplement's incomplete and potentially incorrect description of that construction. The conclusions remain subject to the arithmetic and implementation trust assumptions stated in the paper.

Scope: `sections/B0-families.tex` through `sections/B5-small.tex`, with the referenced model statements and proofs in `04-split.tex`, `05-other.tex`, and the lnts proof in `G-proofs-split.tex`. I also consulted the built supplement, dossiers, earlier reviews, decision register, and certificate implementations. I did not edit the paper or make a commit.

1. **major — Specify the Gibbs Hessian matrices and the arithmetic of their minimization.**

   **Location:** `sections/B5-small.tex:148` (also the arithmetic description at line 150).

   **Problem:** The second-order bound uses “the two end-point matrices of the ... interval Hessian” without defining those matrices or proving the quadratic-form inequality. The ordinary componentwise lower and upper endpoint matrices do not provide the claimed bound. The statement that the quadratics are minimized “exactly” also misdescribes the implementation: it evaluates their closed-form minima in outward-rounded mpmath interval arithmetic.

   **Evidence:** Consider the symmetric interval matrix with diagonal entries in `[1,3]` and off-diagonal entries in `[0,1/2]`. Its ordinary endpoint matrices are

   ```text
   Hlo = [[1, 0],   [0,   1]],
   Hhi = [[3, 1/2], [1/2, 3]].
   ```

   Both are positive definite. The admissible matrix `H = [[1,1/2],[1/2,1]]` is also positive definite, but for `z=(1,-1)` the three quadratic forms are respectively `2`, `5`, and `1`. Thus `z^T H z >= min(z^T Hlo z, z^T Hhi z)` is false. With linear term `g=(1,-1)`, the minimum of `g^T z + z^T H z/2` is `-2`, whereas the smaller minimum from the two ordinary endpoints is `-1`.

   The actual implementation, `research-20260929/reviews/wave2-small-verification/gibbs_bb.py:115–129`, correctly uses the **lower ends of both diagonal entries in both matrices**, and varies only the off-diagonal entry between its two endpoints. It encloses `D(c) - g^T Q^{-1}g/2` using mpmath intervals. I found no error in that implementation's endpoint argument.

   **Concrete fix:** Define

   ```text
   a = lower(H11), e = lower(H22),
   Q- = [[a, lower(H12)], [lower(H12), e]],
   Q+ = [[a, upper(H12)], [upper(H12), e]].
   ```

   State and prove that, for every displacement `z` and every admissible symmetric Hessian `H`,

   ```text
   z^T H z >= min(z^T Q- z, z^T Q+ z).
   ```

   The diagonal terms are bounded below independently; the off-diagonal term is linear in `H12` and therefore minimized at one of its endpoints. When both `Q-` and `Q+` are positive definite, taking the smaller of their unconstrained quadratic minima gives a valid lower bound on the box. Describe the computation as **closed-form minima enclosed in outward-rounded interval arithmetic**, including the interval treatment of the centre value and gradient. This supplies the missing proof without changing the certificate.

2. **minor — The lnts coefficient mutation tests model validation, not the root sign.**

   **Location:** `sections/B1-lnts-lukvle10.tex:89`.

   **Problem:** The sentence says that either shifting the bracket or changing an acceleration constant by `10^-40` makes the sign test fail. The recorded coefficient mutation is rejected before any root-sign computation.

   **Evidence:** `development/reviews/code/sol-lnts-review/verify.py:291–295` changes the first coefficient string `100` and calls `inspect_osil(...)`. Its model-template assertion rejects the altered file. The shifted-bracket controls at lines 296–299 separately call `sign_certificate(...)`. The recorded checks therefore establish two different failures.

   **Concrete fix:** Write: “Shifting the final bracket by ±`10^-55` fails the sign test; changing one acceleration coefficient by `10^-40` fails the model-structure assertion.” Do not claim a recomputed sign failure for the perturbed model unless that test is actually performed.

3. **minor — The lukvle10 certificate gap is not exactly the sum of search tolerances.**

   **Location:** `sections/B1-lnts-lukvle10.tex:314`.

   **Problem:** “The remaining gap equals the summed branch-and-bound tolerances” asserts an equality that neither the proof nor the stored numbers establish. The upper certificate is a separately defined rational-seed trajectory. The search incumbents are interval upper bounds for separate pair/window points. Logging and the explicit `10^-18` reductions also contribute to the assembled lower certificate.

   **Evidence:** My exact recomputation from the stored multiplier vector and logged lower bounds gives

   ```text
   B = 352.23802540507845570173654781696532154455780982971...
   ```

   The sum of the logged incumbent-minus-lower-bound differences, with multiplicities, is `1.41716658194e-9`. The upper end of the rational-seed objective enclosure minus `B` is `1.4171669291347231...e-9`. They differ by approximately `3.47e-16`. This is immaterial to the valid `1.42e-9` gap, but rules out the literal numerical equality. No exact identity between the summed incumbents and the rational-seed objective is proved.

   **Concrete fix:** Say that the certified gap is **dominated by**, or **agrees to the reported precision with**, the summed search errors. Preserve the qualification that global optimality of the rational-seed point is not proved.

4. **minor — Exclude the fixed capital variable from the etamac margin statement.**

   **Location:** `sections/B5-small.tex:308`.

   **Problem:** “Every bound holds with margin at least `0.047`” cannot include the fixed variable `K1`.

   **Evidence:** The OSIL file fixes `K1 = 12.32657617084` by equal lower and upper bounds. Its margin to both bounds is zero. The recomputed point has minimum margin approximately `0.04735` among the other finite variable bounds. The code explicitly excludes `K1` from that minimum in `development/dossiers/small-checks/r2/etamac_point.py`.

   **Concrete fix:** Say “Every nonfixed variable satisfies its finite bounds with margin at least `0.047`; `K1` equals its fixed value exactly.”

**Checks and findings.** All executions took place under `/tmp/sol-math-supp1/`, using copied code and inputs. Numerical libraries were limited with `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`, and at most two single-process computations ran concurrently. No repository script was run in place. These are targeted local checks, not CI results; I did not inspect CI.

| Family | Mathematical and model checks | Recomputed evidence |
|---|---|---|
| lnts | OSIL bounds, dynamics and objective spot checks; forward weights and reflection; scalar-root uniqueness, feasibility and support inequality; strict suboptimality argument | Independent integer/Fraction root brackets for all four sizes, with optimum enclosure widths about `1.37e-64`; all four 40-decimal displays agree |
| lukvle10 | Free-variable model and power trees; partial-Lagrangian coefficients, three-pair window, differentiability, coercive-box lemma and interval search argument | Exact assembly of the logged bound; all 35 logged boxes satisfy the coercivity conditions with the exact binary64 multipliers, with minimum margin over the logged incumbent plus 1 exceeding `2.95e-6` |
| dtoc5 | Independent parsing and checking of every OSIL dynamics row, variable bound and objective term; sign convention, terminal multiplier override, squares, attainment and SDP argument | Every row of the copied rational point holds exactly; independent `B256` evaluation and completed-square loss check give gap at most `7.205103440638...e-43`, confirming both displayed ends and `7.21e-43` |
| optcdeg2 | OSIL row/bound/constant spot checks; telescoping, state enclosure, elimination of position, control endpoints/vertex, Sturm coverage and quartic error bound | Copied exact enclosure and minimization programs reproduce `293.87607509587509237940` as the truncated bound; 11,596 quartic calls, 7,785 minimum brackets, no interior-control piece, largest bracket allowance `9.49576e-29` |
| camshape | Stored constants and row form; Green recurrence, Sturm comparison, Lipschitz envelope, feasibility case split, uniqueness, perturbation and deficit arguments | Independent exact checks of K1–K6 and every row/bound at the envelope for all four sizes; n=100 optimum `-4.284147121746743803441007134034135707...`, denominator 28,165 digits |
| chain | Polyline bijection, length/objective weights, summation by parts, catenary inequality and equality conditions, Weierstrass construction/uniqueness, boundary and end-window arguments | Copied record implementation rerun for chain50: 36,689 boxes, 36 excluded, zero unresolved; certified binary64 target safely displays as `5.0722614939828627` |
| catmix | All bilinear OSIL rows and objective checked independently for all four sizes; positive cone, projective value functions, chord minorants, DP induction, Dinkelbach signs, loss accumulation and coefficient transport | Independent exact simulation and generic evaluation of every row for the stored catmix100 controls; objective `-0.048069432030959562924734533987703146...`; changing c to 9a raises it by `1.18150e-17` |
| hvycrash | OSIL mapping and row spot checks; elimination identities, nonzero denominators, backward existence induction and tolerance bound | Independent exact A, D and kappa; cosine Taylor upper bound `-0.856881557497...`; total angle-drop bound `0.3829739902447...` |
| ex6_2_5/7 | OSIL amounts, balances, phase separability, scaling residuals, Gibbs inequality and mass-balance bound; inspection of the interval Hessian method | Copied exact symbolic/scaling checks and primal evaluations reproduce residuals 0 and `(0,0,5e-14)`, the ideal-phase positive minimum, both bound assemblies and primal enclosures |
| etamac | OSIL row/bound spot checks and template inspection; boundedness recursion, power-mean majorant, exponent identities and convex tangent inequality | Independent exact degree excess `207070707070707/(5*10^29)`; copied triangular-point evaluation confirms objective and `2.57652e-15` gap |
| pricing050 | Maximization direction checked directly in OSIL; demand-row signs and Lagrangian direction; univariate derivatives and window/exclusion argument | 78/94/77 terms with powers 1/2/3; exact multiplier assembly; copied minimization and primal check reproduce upper bound `-1813.82907845197305774994594623` and primal objective `-1813.8290784519730769` |
| pindyck | OSIL state bounds and recurrence templates; implicit uniqueness, polytope inclusion, Hessian differentiation, matrix criterion, strong-concavity bound and local-interiority uniqueness argument | Copied checker verifies exact coverage and all six stored Hessian leaves; copied interval Newton/gradient evaluation reproduces J, its `1.40e-46` enclosure width and localization radius `3.687216e-13` |

**Targeted commands actually run.** Each command below used the thread limits stated above; outputs are retained in the scratch directory. Copied-program paths were changed only to use copied inputs and scratch outputs.

```text
python /tmp/sol-math-supp1/check_models.py
python /tmp/sol-math-supp1/exact_checks.py
python /tmp/sol-math-supp1/exact_checks.py skip-lnts
python /tmp/sol-math-supp1/dtoc5_exact.py
python /tmp/sol-math-supp1/luk_sum.py
python /tmp/sol-math-supp1/catmix_exact.py

# In /tmp/sol-math-supp1/tree/research-20260929/reviews/bangbang-verification:
python v_states.py
python v_qcal_exact.py

# In /tmp/sol-math-supp1/tree/research-20260929/reviews/cops-verification:
python v_chain_bnb.py 1e-14 50

# In /tmp/sol-math-supp1/small:
python gibbs_check.py
python etamac_point.py
python pricing_check.py

# In /tmp/sol-math-supp1/pindyck:
python verify_own_leaves.py
python primal_check.py
```

The first `exact_checks.py` execution completed the lnts checks and the n=100 camshape feasibility checks, then stopped at Python's default integer-to-string digit limit while printing the camshape denominator length. I disabled that presentation limit in the scratch program and reran the remaining checks; they passed. This did not change the arithmetic or conclusions.

**Limits of this review:** I did not rerun the complete lukvle10 search trees, the full catmix DP runs, the other three chain end-window searches, the Gibbs simplex searches, the etamac dual refinement, or the LP state-range construction for pindyck. Their relevant algorithms, stored evidence and analytic validity arguments were inspected. The pindyck leaf replay checks the stored root box and partition; it does not independently regenerate the LP proof that the box contains the state map. The exact optima of the rounded QPLIB camshape copies and the tabulated perturbation/deficit numbers were checked at the level of the general theorem and existing evidence, not independently regenerated. These limits should not be read as additional issues or as full independent reproduction of every computer-assisted certificate.
