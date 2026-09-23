**Certified convex MINLP: mathematical contract and soundness argument.**

Audited 2026-09-13. This note specifies the result that the implementation must establish. It replaces the incomplete mathematical formulation in the original method note. A proof below is a mathematical proof under explicit hypotheses; it is not a proof that every Python execution satisfies those hypotheses. Current implementation and replay status belong in the repair/replay records, not in the theorem's assumptions.

Formalization update, 2026-09-20: the Lean extension completed on 2026-09-17 covers [49 mathematical obligations](../paper-certified-minlp/formal/COVERAGE.md), including propagation, cut and curvature rules, typed discrete checking, master matching, bound transfer, and primal completion. Its [verification record](../paper-certified-minlp/formal/VERIFICATION.md) reports targeted module builds and an axiom audit. Python execution and benchmark artifacts remain outside the formal coverage.

The certificate establishes a bound for the model reconstructed from the supplied input under the declared exact interpretation. Let `s = 1` for minimization and `s = -1` for maximization, and let `h = s*f`. All proof obligations concern the minimization of `h`. The normalized feasible set is

```
F = { x : x in B0, x_J integral, linear rows hold,
          r_i(x) <= 0 for all nonlinear rows i }.
```

Every function appearing in this definition must be real and defined at the points where it is used. A nonlinear upper row `g <= u` becomes `r = g-u`; a lower row `g >= l` becomes `r = l-g`. The normalized row and `h` must be convex on the domains used for their cuts. Nonlinear equalities and general two-sided nonlinear rows have no such automatic interpretation and are outside the current contract. Affine equalities are allowed.

The exact interpretation fixes each finite binary floating-point leaf to its exact rational value and each integer leaf to that integer. Subsequent algebraic addition and multiplication are exact operations on those leaves. Python computations and Pyomo simplifications performed before the checker receives the tree cannot be recovered: if the user computes `a = 0.1 + 0.2` first, that one resulting floating-point leaf is the input. Similarly, if Pyomo rewrites `x/3` using the floating coefficient `1/3`, the resulting coefficient is interpreted exactly; the original rational division cannot be recovered. By contrast, separately stored coefficients in `0.1*x*x + 0.2*x*x - 0.30000000000000004*x*x` add to `-2^-55`, not zero. Bounds, fixed values, row shifts, objective constants, powers, curvature tests, differentiation, and master construction must use the same interpretation. A loader that executes Python is trusted input construction; it is not a sandbox for adversarial programs. Identity with a GAMS model or original decimal data is a separate equivalence obligation.

Domain checks precede transformations that can hide undefined subexpressions. For example, replacing `x/x` by `1` does not preserve definedness at zero, and `sqrt(x*x)` cannot generally be replaced by `x`. Unsupported functions, nonfinite coefficients, failed domain checks, and failed derivative evaluation produce rejection or no cut. A checker cannot turn them into zero, silently omit them from a required premise, or rely on a solver's numerical feasibility tolerance.

**Preserving feasible points when tightening bounds.**

The checker constructs a rational product box `B` that contains `F`. It starts from the model bounds, exact fixed values, and binary bounds. Each subsequent tightening must follow from previously established bounds and an original linear row. For a row `sum_j c_j*x_j <= u`, let `Rlo` be a lower bound on the sum excluding coordinate `k`. Then

```
c_k*x_k <= u - Rlo.
```

Division by a positive coefficient gives an upper bound; division by a negative coefficient gives a lower bound. For a lower row `sum_j c_j*x_j >= l`, an upper enclosure `Rhi` for the other terms yields `c_k*x_k >= l-Rhi`. Integer upper bounds can be rounded down and integer lower bounds up. Every step preserves each previously feasible integer point. Induction proves `F subset B`, whether or not propagation reaches a fixed point. A finite propagation limit affects strength only. A nonfinite enclosure supplies no finite tightening in that direction. Empty intervals require rejection or a separately justified infeasibility result; they cannot be used as a nonempty box in the cut proof.

Applying bounds derived using integrality to the continuous relaxation is safe for this certificate: the inclusion needed is for original mixed-integer feasible points. Every accepted cut must still be valid over the entire box on which its supporting inequality is claimed. Original or outward-rounded numerical solver bounds may supply a larger domain for curvature; they must not exclude the exact box relied upon by the checker.

**Safe affine underestimation, including unbounded coordinates.**

Consider one normalized row

```
r(x) = g(x) + ell*x + c.
```

Let `D` be a convex domain containing all original feasible points relevant to this row, and let `z in D intersect B`. Assume `g(z)` is finite and a finite vector `p` has been justified such that

```
g(x) >= g(z) + p*(x-z)             for every x in D intersect B.  (1)
```

Here `*` between vectors is a dot product. A valid subgradient provides (1). Convexity and a finite gradient provide it when the differentiability/domain hypotheses of the supporting-hyperplane inequality hold. Convexity on a closed box and membership of `z` alone do not establish existence of a finite gradient. For instance, `-sqrt(x)` on `[0,1]` is convex but has no finite supporting slope at zero. The current symbolic-gradient route must abstain at unsupported nonsmooth or singular points; no general subgradient oracle is assumed.

Precisely, convexity of `g` on `D intersect B` gives (1) if, for every `x in D intersect B`, the right derivative at zero of `theta -> g(z + theta*(x-z))` exists and equals `p*(x-z)`. A differentiable extension near `z` suffices. Finite coordinate derivatives alone do not: `-sqrt(x*y)` on the nonnegative quadrant has zero derivatives along both axes at the origin, but the zero vector fails the support inequality at `(1,1)`. The support implications, the one-variable counterexample, and the axis-derivative and failed-support facts for the two-variable example are proved in [Support.lean](../paper-certified-minlp/formal/CertifiedMinlp/Support.lean). The symbolic differentiation implementation must supply derivatives with the stated segment meaning; their finite interval evaluation does not establish that premise by itself.

Choose any rational slope vector `a`, define `phi(z) = r(z)-a*z` and `d = p+ell-a`, and set

```
W_j = sup { d_j*(z_j-y) : y in B_j }.
```

For every coordinate, the exact cases are:

| Coordinate interval `B_j` | Condition for finite `W_j` | Value |
| --- | --- | --- |
| `[L_j,U_j]`, both endpoints finite | none | `max(d_j*(z_j-L_j), d_j*(z_j-U_j))` |
| `[L_j,+infinity)` | `d_j >= 0` | `d_j*(z_j-L_j)` |
| `(-infinity,U_j]` | `d_j <= 0` | `d_j*(z_j-U_j)` |
| the entire real line | `d_j = 0` | `0` |

If a listed sign condition fails, the supremum is positive infinity. There is then no finite bound obtainable by this supporting-plane calculation. This does not prove that the nonlinear row has no finite affine underestimator; a different point or stronger nonlinear argument may work. A fixed coordinate `L_j=U_j=z_j` contributes zero. Fixed variables may be eliminated exactly before differentiation, but absent that elimination the evaluator must still return valid finite derivative data.

If all `W_j` are finite and the rational intercept satisfies

```
b <= phi(z) - sum_j W_j,                                      (2)
```

then `a*x+b <= r(x)` for every `x in D intersect B`. Consequently `a*x+b <= 0` is a valid relaxation of the row there.

Proof: (1) and the affine terms give `r(x)-a*x >= phi(z)+d*(x-z)`. The definition of `W_j` gives `d_j*(x_j-z_j) >= -W_j` coordinate by coordinate. Summing and applying (2) proves the result. No minimizer of `phi`, boundedness of `B`, Slater condition, integer optimality, or optimal linearization point is required.

The condition `b <= inf(r(x)-a*x)` is equivalent to global affine underestimation on the specified domain. It is only sufficient for the weaker implication `r(x)<=0 => a*x+b<=0`. For example, on `[-1,1]`, the row `r(x)=x<=0` implies `2*x<=0`, although `2*x<=x` fails at positive points. Neither condition is necessary for obtaining a useful MINLP lower bound through other methods.

**A fully rational sufficient test from enclosures.**

Suppose rigorous interval evaluation gives a finite rational lower bound `v <= phi(z)` and finite rational intervals `[dlo_j,dhi_j]` containing the actual `d_j`. Since `z in B`, the following rational quantities bound `W_j` from above:

| Coordinate interval | Acceptance condition | Conservative upper bound `What_j` |
| --- | --- | --- |
| `[L_j,U_j]` | `dlo_j <= dhi_j` | `max(dhi_j*(z_j-L_j), dlo_j*(z_j-U_j))` |
| `[L_j,+infinity)` | `dlo_j >= 0` | `dhi_j*(z_j-L_j)` |
| `(-infinity,U_j]` | `dhi_j <= 0` | `dlo_j*(z_j-U_j)` |
| the entire real line | `dlo_j = dhi_j = 0` | `0` |

The finite-interval formula follows because `z_j-L_j >= 0` and `z_j-U_j <= 0`. These signs also justify the half-line formulas. Thus accepting only `b <= v-sum_j What_j` proves (2). Direct outward interval evaluation of the same expression is also sound if its final lower endpoint is read exactly and all intermediate enclosures are valid. Loss of dependency between `phi(z)` and `d` can weaken the result but cannot invalidate this conservative calculation.

For an upper-unbounded coordinate the producer can choose `a_j` no greater than a rigorous lower bound on `p_j+ell_j`; for a lower-unbounded coordinate it can choose `a_j` no smaller than a rigorous upper bound. On a free coordinate it needs an exactly known slope. In an objective epigraph row, the new variable has exact coefficient `-1`, so choosing its cut coefficient as `-1` makes its residual slope zero. The checker verifies the supplied slopes directly; producer rounding choices and precision are not evidence of validity. An insufficient enclosure causes refusal, even when the unknown true residual has the desired sign.

All variables in `r` are included in the calculation. An omitted slope means exactly zero, not an omitted residual term. The point must supply all needed coordinates. Unknown variables, ambiguous names, unsupported coordinates, reversed intervals, and nonfinite endpoints are malformed evidence. The final intercept may be rounded downward to shorten its encoding. Rounding to nearest is insufficient without a separate error allowance.

**Transfer from a rational master to the original problem.**

Use an exact affine objective if `h` is affine. Otherwise introduce a free real variable `t`, take master objective `t`, and generate safe cuts for `h(x)-t<=0`. Include exact original linear rows, justified box bounds, integrality, and any accepted cuts. Auxiliary variables introduced for constants or other purposes require explicit constraints and a checked extension map. They cannot alias model variables. Additional master constraints require their own validity argument.

For every `x in F`, define the extension `E(x)` by preserving `x` and setting `t=h(x)` if necessary. Set any objective-constant variable to one. The safe-cut result and box preservation show that `E(x)` is master feasible. Its objective is exactly `h(x)`.

Suppose the discrete proof establishes the semantic statement

```
master_objective(y) >= L          for every master-feasible y, (3)
```

for finite rational `L`. Applying (3) to `E(x)` proves `h(x)>=L` for every `x in F`. Hence `L <= inf_{x in F} h(x)`, with the empty-set infimum understood as positive infinity. The infimum need not be attained. For original minimization the result is a lower bound `L`; for original maximization it is an upper bound `-L`. An exactly affine objective constant must be included once, with the correct sign.

A proof that the master is infeasible instead implies that `F` is empty. An unbounded master, no finite proof bound, or checker failure supplies no finite MINLP certificate. A weak relaxation may fail to certify a finite bound even for a well-behaved bounded MINLP.

**The discrete proof obligation and solution-derived cutoffs.**

The master encoded in the discrete certificate must equal the master whose inclusion was proved. Check its variable bijection, integrality indices, objective and sense, coefficients, constant treatment, row directions and right-hand sides, and bounds. Equivalent positive row scaling is harmless. Equality can also be multiplied by a negative number; an inequality needs its direction reversed. A proof about a presolved model is insufficient without either the original-model identity or a verified presolve map.

Parsing and matching only the problem section does not establish (3). All inference rules, reference indices, branch assumptions, assumption discharge, solution vectors, final conclusion, and declared result must also be checked. A process exit status or success phrase is operational evidence only; the checking program and interface remain part of the software soundness argument.

Solution-derived cutoff rows need special care. In minimization, a checked feasible master solution of value `U` allows the proof to reason under the cutoff `objective<=U`. That cutoff is not true at every feasible point. It cannot be added as an unconditional original constraint, and it cannot be justified by an empty solution section.

Here is a direct way to recover (3) without assuming attainment. Check every solution used, and let `Umin` be their smallest objective value. Require the proposed finite lower bound `L` to satisfy `L<=Umin`. If there were a master-feasible point `y` with objective below `L`, it would satisfy every such solution cutoff. Induction through valid linear-combination, rounding, and branch-discharge steps therefore makes the chosen assumption-free lower-bound constraint true at `y`, a contradiction. If no solution cutoff is used, the same argument omits `Umin` entirely. A more permissive proof interface may establish an equivalent semantic guarantee, but it must supply that argument explicitly. An infeasibility claim cannot rely on excluding points through an incumbent cutoff.

A checked feasible master solution need not satisfy the original nonlinear constraints. Its value therefore does not certify an original MINLP upper bound. A nonlinear incumbent certificate requires exact integrality and bounds, exact linear feasibility, rigorous satisfaction of every nonlinear row and its domain, and an outward objective enclosure. For minimization, combining such a feasible upper bound `U` with `L` proves a gap at most `U-L`; equality proves exact optimality only when all these premises hold. Floating-point closeness to a recorded incumbent proves neither assertion.

**Implementation obligations and limits of the claim.**

The checker implements the contract only insofar as these components are correct: model loading and exact expression reconstruction; domain and curvature rules; symbolic differentiation or any subgradient rules; outward interval arithmetic and exact endpoint conversion; rational bound propagation; rational master serialization and identity parsing; the complete discrete proof checker; and the code that combines their verdicts. Their shared use by producer and checker does not remove them from the trusted computing base. Numerical OA, NLP solves, slope proposals, SCIP search, and proof completion need not be trusted when their outputs are fully replayed against this contract.

The repaired implementation uses a narrower sufficient domain contract than the general lemma: original expression domains are checked over the declared variable box, including domain bounds and exact fixed values. It does not infer missing domain restrictions from nonlinear constraints. Its cut evaluator accepts finite supported symbolic derivatives, without a general subgradient mechanism. Perspective recognition is disabled until curvature can be established on the actual ratio domain. These restrictions can reject mathematically valid models or cuts; they do not enlarge the theorem's claim.

This is a soundness result for accepted evidence, not a completeness or complexity result. It promises no finite termination, polynomial certificate size, recognition of every convex function, or exact optimum for every admissible model. Basic lower-bound checking does not require a new nonlinear solver, general nonconvex support, or an end-to-end proof assistant implementation.

The completed Lean development proves the mathematical cut and transfer rules and the soundness of typed reference checkers for discrete proofs and rational quadratic matrices. It does not verify Python parsing, expression translation, interval-library execution, VIPR input handling, the Python discrete checker, or benchmark files. The [coverage map](../paper-certified-minlp/formal/COVERAGE.md) lists the precise theorems and their remaining assumptions. The primary-work comparison and the separate scopes of Why3 and CakeML verification are recorded in [the literature audit](certified-minlp-literature-audit.md).
