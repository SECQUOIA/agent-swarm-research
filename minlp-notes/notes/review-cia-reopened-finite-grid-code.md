# Independent review: finite-grid theorem and computational certificates

Reviewed 2026-09-07 by the independent `review_finite_code` agent. Scope: [the finite-grid note](cia-reopened-finite-grid.md), its LP formulation, rational certification, witness reconstruction, and comparison with the original CIA objective. The [review code](../code/cia_reopened/check_finite_grid_review.py) was written separately from the author's implementation.

## Mathematical review

The ten-variable region theorem is correct as written. I checked the following points specifically.

- The schedule identity includes constant controls through endpoint switches. Directly computing every absolute cumulative coordinate discrepancy agrees with the identity on rational test controls.
- Replacing the final mode by a largest-total mode other than the initial mode cannot increase the omitted maximum: the new omitted mode has no larger total than the old omitted mode that becomes selected. The final deficit also decreases.
- Weak cutoff inequalities are sufficient for adversarial witnesses, including ties. An early switch has final deficit at least E, while a late switch has initial deficit at least E. No numerical strict-feasibility decision is needed.
- For E>T/3, at most two totals exceed E. The two cases m2≤E and m2>E supply exactly the stated constraints. Averaging modes 3 through n preserves monotonicity, weighted sums, and the ordering relative to m2.
- The lower cutoff index cannot be zero: that would make the largest-total constant schedule have error at most E. Upper cutoff indices exist because E and all totals are nonnegative.
- The limit argument uses finitely many regions and bounded endpoint data. This covers the supremum without assuming that a strict feasibility region is closed.
- In the F=T/3 construction, a=b and u3=m3 are harmless. The sum constraints force coincident endpoint states whenever a=b or b=N. The explicit baseline construction satisfies all constraints for every n≥3.
- The fixed number of variables and constraints gives a polynomial bit-complexity algorithm for rational grid data and binary-encoded n. A witness represented by its three component types has the same compact description; expanding all n rows necessarily takes at least n operations.

## LP certificate audit

For `solve_certified`, HiGHS solves min cᵀx with c=−e_E, Ax≤b and Bx=d, with free x. The reconstructed multipliers satisfy y≤0 and Aᵀy+Bᵀz=c. Hence cᵀx≥bᵀy+dᵀz for every feasible point. Exact primal feasibility and exact equality of these objectives prove optimality. The code checks all these conditions with rational arithmetic.

For `certify_region_upper`, the signs are reversed as required: y≥0 and Aᵀy+Bᵀz=e_E imply E≤bᵀy+dᵀz. The checked right side is at most the proposed global bound. This applies even to an empty region. In particular, the global conclusion never depends on trusting a floating-point infeasibility classification. A mistakenly skipped nonempty region could not conceal a larger optimum if this certificate passes.

The fixed denominator cap in floating-point rational reconstruction is a limitation of the LP prototype, not a soundness flaw: failed reconstruction raises an exception instead of certifying an incorrect answer. Before subsequent author changes, `minimax(100000000,[0,1])` raised `AssertionError`, whereas n≤10⁷ in the same test passed. The mathematical LP theorem remains valid. This observation motivated distinguishing a general exact arithmetic algorithm from a certificate-producing numerical prototype.

## Independent original-objective checks

The reviewer implementation constructs every distinct schedule with zero or one switch and computes the maximum absolute cumulative discrepancy at every original grid endpoint, using `Fraction` arithmetic. It does not use the author's three-term schedule identity. It also reconstructs phase witnesses independently and checks the stated LP constraints directly, without the author's row builder.

A separate MILP models the original max–min–max problem: every schedule receives a disjunction over signed cumulative coordinate discrepancies. It uses all switch and terminal times, where each coordinate's discrepancy attains its extrema by monotonicity. It neither uses the cutoff-region theorem nor averages mode groups. Ordering final totals is a valid relabeling symmetry reduction. MILP upper bounds are floating-point cross-checks, not rational proof certificates.

The review run and resulting case table are recorded below after final validation.

Validation command:

```bash
python code/cia_reopened/check_finite_grid_review.py
```

All checks passed. The small original-disjunction MILPs attained the following values, with matching numerical global upper bounds (agreement with exact values better than 10⁻⁷):

| Modes | Grid | Exact LP value |
|---:|---|---:|
| 3 | 0,1 | 2/3 |
| 3 | 0,1,2 | 3/4 |
| 3 | 0,1,2,3 | 1 |
| 4 | 0,1 | 3/4 |
| 4 | 0,1,2 | 3/4 |
| 5 | 0,1,2 | 4/5 |
| 3 | 0,1/5,2/3,1 | 4/9 |
| 4 | 0,2/7,1 | 13/28 |
| 5 | 0,1/4,3/2 | 19/20 |

Together with n=5 on 0,1,…,9, the rational audit covered 148 regions: 30 primal/dual-certified feasible optima and 118 regions classified numerically infeasible but nevertheless covered by exact global upper certificates. Of the feasible optimum witnesses, 23 had cutoff ties and 26 had coincident phase endpoints. Every feasible primal was checked against the explicit mathematical constraints, reconstructed independently, and evaluated against all original schedules with exact arithmetic. For n=5,N=9, the exact global value was 17/5; all 90 region upper bounds and all six feasible region witnesses passed.

An additional 100 generated rational controls, over n=3,…,6 and one through five nonuniform intervals, gave exact agreement between direct cumulative-coordinate enumeration and the author's schedule identity.

The direct MILP initially exposed numerical solver failures on some symmetric instances, without producing contradictory optima. The review formulation now orders total allocations and selects exactly one active disjunct per schedule, both without changing the feasible adversarial controls up to mode relabeling. The successful tests used HiGHS with presolve disabled. The rational LP certificates and direct rational schedule evaluations provide the exact mathematical checks; these MILPs provide an independent formulation cross-check.

## Review of the final explicit formula implementation

The author subsequently replaced the default numerical LP computation with [a separate standard-library implementation](../code/cia_reopened/minimax.py) of equations (2)–(7). I checked every arithmetic expression against the stated formula, the family selection and pair admissibility tests, and both compressed witness constructions. There is no floating-point conversion in this implementation. The optional LP audit remains in `finite_grid_research.py` as `minimax_lp`.

The final review command passes all preceding tests and adds:

- Exact agreement between the explicit formula and rational-certified LP solutions on 99 cases: 48 unit grids with n=3,…,8 and N=1,…,8; 50 random rational nonuniform grids with seed 160907, n=3,…,10, and one through seven intervals; and the documented n=9 nonuniform counterexample to the incomplete formula.
- Explicit validation of every returned compressed witness against the original LP constraints, using the reviewer's separate constraint checker.
- Direct original-error evaluation of the formula witnesses using compressed component multiplicities. This enumerates constant schedules and every ordered pair of component types, distinguishing two different modes of the same type from a single constant mode. It evaluates the original signed cumulative discrepancies at every grid time.
- Twenty-four extreme exact-arithmetic cases, with n as large as 10¹⁰⁰+7, grid denominators above 10³⁰, horizon numerators above 10⁵⁰, and endpoints separated by 2/10⁴⁰ around T/3. Every compressed witness passes the original-error check. All single-interval cases also match the independently known exact value (n−1)T/n.

The previous n=10⁸ rational reconstruction failure is therefore resolved for the default solver; it remains only a documented limit of the optional numerical LP audit. Baseline equality cases now return an explicit witness. Expanding all n modes is intentionally unnecessary in these extreme tests.

**Conclusion:** I found no correctness defect in the finite-grid theorem, final rational formula implementation, or accepted LP certificates. The final formula agrees with the separate LP characterization, independent original-objective optimization on small cases, and exact original schedule evaluation of the constructed witnesses. The companion mathematical review examines the elimination proof in greater algebraic detail. Novelty assessment is outside this code review.

## Final public-input validation review

A final narrow change replaced public-input assertions in `minimax.py` with explicit exceptions and rejected floating-point or Boolean inputs. The formula and witness construction were unchanged. I reviewed the input checks and ran:

```bash
python -O code/cia_reopened/check_finite_grid_review.py --validation-only
```

All 18 invalid-input cases raised the expected exception with Python assertions disabled. These cover noninteger or Boolean mode counts, mode counts below three, missing endpoints, a nonzero initial endpoint, repeated/decreasing/negative endpoints, Boolean/floating-point endpoints, malformed rational strings, and unsupported endpoint objects. Four valid cases using integer endpoints, rational strings, mixed `Fraction`/integer endpoints, and extreme exact arithmetic returned their independently specified exact values and witnesses. The public input contract therefore remains enforced under `python -O`. Internal proof-audit assertions still run only in normal Python mode, as expected.
