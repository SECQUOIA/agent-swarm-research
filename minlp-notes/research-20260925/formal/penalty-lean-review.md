Independent adversarial review of `PenaltyEncoding.lean`, 2026-09-25.

The formal statements correctly establish the two optimized augmented-dual
formulas and their zero-gap thresholds for the stated native constraints.
I found no incorrect constraint, hidden substantive hypothesis, or misuse of
real infima or suprema. This review concerns the formal core and its
correspondence to [the research note](../parametric-exploration.md); it is not
a fresh literature or novelty audit.

The reviewed source is [PenaltyEncoding.lean](PenaltyEncoding.lean), SHA-256
`f42d98e8997e65f77a5573886673b00d823bd0aa1aa3f08d560ee4b5b780d72d`.
I read the definitions and proofs directly before checking compilation. I
did not edit that source.

The index translation is essential. The Lean parameter is any natural
number `k`; the paper dimension is `n = k + 1`. Thus `k = 0` represents
the valid one-coordinate chain, not an empty chain. Lean coordinate `a i`
corresponds to paper coordinate `a_(i+1)`. The recursion starts at
`delta 0 = 1/4`; `delta_closed` proves
`delta k = (1/2)^(2^(k+1))`, exactly the paper's final lower bound.
The step constraint uses `i < k`, so it imposes precisely the `k` links
between `k + 1` coordinates. It does not add a link after the final
coordinate.

`Point.a` and `OnePoint.a` have type `Nat → Real`. Only coordinates from
zero through `k` occur in feasibility and objectives. Restricting a Lean
point to those coordinates gives a paper point with identical objective;
any finite paper point can be extended arbitrarily after `k` to give a
Lean point with the same objective. Thus the objective-value sets coincide.
This correspondence is a manual audit, not a separately proved Lean
theorem. The full Lean feasible set has an unrestricted infinite tail, so
it should not be called a compact finite-dimensional feasible set.
Neither dual proof relies on such a compactness assertion.

For the symmetric companion, `Feasible` contains both binary conditions,
both bounds on `y`, every chain bound and link, and exactly the two native
linking inequalities in the note. For the one-binary construction,
`OneFeasible` removes the sign variable and the upper linking inequality,
and uses `a k - 2*(1-q) ≤ y`. In both structures the binary variables have
real type, but the explicit disjunction `q = 0 ∨ q = 1` (and likewise for
`b`) gives exactly the required two values. No continuous relaxation of a
binary variable is substituted in the dual. The equality `y = 0` is
intentionally absent from native feasibility and appears as an assumption
in the primal-objective lemmas. Both Lagrangians use the actual objective
`-q`, the unrestricted real multiplier term `lam*y`, and the unscaled
absolute-value penalty `rho*|y|`.

The chain lower bound is derived from the native inequalities; it is not
assumed as a premise of either main theorem. The positive chain witness
and the zero, positive-residual, and negative-residual points are checked
against full native feasibility. In particular, the negative witness in
the one-binary model is `(q,y) = (0,-1)`, whereas the symmetric negative
witness has `(q,b,y) = (1,0,-delta k)`. Confusing those witnesses would
change the penalty threshold by a factor of two; the formalization keeps
them distinct.

The only explicit numerical hypothesis of `dual_eq`, `one_dual_eq`, and
their threshold theorems is `0 ≤ rho`. The multiplier ranges over all real
numbers, without a bound or sign restriction. For the one-binary lower
bound, the proof chooses
`(1 + rho*(1-delta k))/(1+delta k)` and proves its nonnegativity.
That multiplier works for every nonnegative penalty. Above the threshold,
the note instead chooses `lam = rho`; these are different valid
maximizers, so this difference does not change the theorem.

The real `sInf` and `sSup` definitions require an audit because their
behavior on unbounded or empty sets would not represent the intended
optimization problem. Here that issue is handled explicitly:

| Obligation | Formal evidence and reason |
| --- | --- |
| Every inner objective-value set is nonempty | `values_nonempty` and `one_values_nonempty` exhibit the feasible zero-objective point. |
| Every inner objective-value set is bounded below | `values_bddBelow` and `one_values_bddBelow` prove the bound `-1 - |lam|` using `q ≤ 1`, `|y| ≤ 1`, and `rho ≥ 0`. |
| The outer value set is nonempty | `Set.range_nonempty` applies because the multiplier domain is all reals. |
| The outer value set is bounded above | `inner_upper` and `one_inner_upper` bound every multiplier's value by the respective claimed dual value; each dual proof also constructs `BddAbove`. |
| The claimed lower bound is attained in multiplier space | `inner_zero` uses multiplier zero for the symmetric model; `one_inner_at_multiplier` uses the displayed multiplier for the one-binary model. |

The upper bounds come from actual feasible witnesses. The lower bounds
apply to every native feasible point, not merely a finite list of
endpoints or a sampled relaxation. For the one-binary proof, the weighted
identity cancels the multiplier with positive weight `delta k`; if the
negative witness exceeds the proposed average, the positive witness lies
below it. The matching lower proof handles both signs of `oneValue` and
both binary assignments. This establishes the full optimized dual rather
than a bound for one chosen multiplier.

`primal_objective` and `one_primal_objective` prove that every native point
with `y = 0` has objective zero. The respective feasible zero witnesses
also have `y = 0`. These results together establish the original optimum
zero, although no separately named primal minimum or infimum is defined.
`exact_threshold` and `one_exact_threshold` characterize **zero duality
gap**. They do not assert that every penalized optimizer satisfies the
linking equality. At the threshold, the displayed nonzero-residual
witnesses tie at objective zero. The note's distinction between value
exactness and solution-set exactness is therefore necessary.

`reciprocal_delta` and `one_threshold_size` identify the real numerical
thresholds. The formal file does not prove binary-digit counts, rational
encoding bounds, sparse model size, superpolynomial growth in input
length, or the fixed-additive-accuracy corollaries. Those require the
note's additional arguments. It also does not formalize convexity,
finite-dimensional compactness, Slater points and their uniform margins,
the full projected feasible sets, the optional inner-value formula at
every multiplier, fractional-penalty variants, literature assumptions,
novelty, solver complexity, or practical benefit. The inner optimization
is defined with an infimum; attainment at every arbitrary multiplier is
not a separate formal theorem. The formalized equalities and witnesses
are sufficient for the claimed dual formulas without that extra theorem.

I independently ran this targeted command from
`paper-certified-minlp/formal`, whose toolchain and mathlib dependency are
pinned to version `v4.33.1`:

```bash
lake env lean /workspace/minlp-notes/research-20260925/formal/PenaltyEncoding.lean
```

It exited with status zero and no warnings. The nine printed transitive
axiom sets, covering the chain identity, both primal-objective results,
both dual formulas, both thresholds, and the one-binary threshold size,
were exactly `[propext, Classical.choice, Quot.sound]`. Direct source
inspection and a targeted `rg` scan found no `sorry`, `admit`, custom
`axiom`, `unsafe`, `native_decide`, or `implemented_by` declaration. The
scan's exit status one means no matches. These checks provide kernel
checking under the installed Lean and imported mathlib environment;
they are not an independent proof-assistant replay, an audit of all
mathlib source, or a guarantee that the formal statement captures every
claim in the research note. No project-wide build or CI inspection was
run.
