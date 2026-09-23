# Independent review: continuous folding core

Date: 2026-09-20. Reviewer: independent source-review agent.
Reviewed modules:
[Folding.lean](../../../Formal/QuadraticPrecision/Folding.lean) and
[FoldingLift.lean](../../../Formal/QuadraticPrecision/FoldingLift.lean).

Verdict: **PASS** for the folding approximation, objective dominance,
projected epigraph characterization, and actual finite affine-system
construction with its size counts. These discharge I3 and I4. The final
part of this review verifies the bridge in `FoldingLift.lean` to the
common binary linear lift model.

The definitions match the source's tent map
`G(t)=min(2t,2(1-t))`. The recursive `foldSum` and `foldObjective` place
successive weights `4^-1, 4^-2, ...` on successive folds. The explicit
sum and iterate theorems verify that correspondence; the recursion is
not a different approximant with the same name.

The error proof uses the exact identity
`t - G(t)/2 + G(t)^2/4 = t^2`. It follows that the approximation error
at depth `n+1` is one quarter of the depth-`n` error evaluated at `G(t)`.
The tent map preserves `[0,1]`, and the depth-zero error `t-t^2` lies
between zero and one quarter. Induction therefore proves both signs and
the exact bound `4^-n/4`, including endpoints and depth zero.

The central relaxed-objective argument is complete. `foldSum_abs_sub`
proves a global Lipschitz bound of one for every finite depth. In a
feasible relaxed sequence, the first coordinate `g_0` satisfies
`g_0 <= G(t)`. Induction bounds the remaining relaxed objective by
`foldSum n g_0`; the Lipschitz estimate bounds any advantage in this
future contribution by `G(t)-g_0`. That advantage cannot exceed the loss
in the first contribution. After division by four this proves
`foldObjective (n+1) g <= foldSum (n+1) t` for every relaxed feasible
sequence. This is a sufficient weak dominance proof; uniqueness of the
maximizing sequence is unnecessary. The exact folding sequence is
separately constructed and proved feasible, with exactly the objective
value `foldSum`.

Consequently `foldEpigraph_iff` identifies the entire projected set at
each `t` in `[0,1]` with
`w >= foldApprox n t - foldError n`. It is stronger than graph-point
feasibility: there is no upper output constraint and every `w >= t^2`
has a feasible lift. The accompanying error theorem controls every
admitted output from below. I checked a client derivation of complete
epigraph containment from this equivalence and the upper approximation
error, as well as the explicit depth-zero boundary `w >= t-1/4`.

The finite constraint list has three inequalities per fold and one
output inequality, totaling `3n+1`, with `n` real auxiliary coordinates.
Its equivalence to the recursive feasibility predicate is proved. The
input interval is a hypothesis of the approximation results and is not
included in that `3n+1` count; an actual globally specified square lift
must impose its two input bounds as well. This constant addition does
not change the advertised linear size.

`foldError_succ` verifies that using depth `L+1` gives
`2^(-2L-4)`, the positive-square bound required in I4. This implements
the manuscript's shifted-interpolant construction. It does not claim
identity with the enhanced depth-`L` formulation used by the older
numerical checker.

## Targeted checks actually run

From `formal/`, with `PATH="$HOME/.elan/bin:$PATH"` and
`LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.QuadraticPrecision.Folding
lake env lean /tmp/Topic20FoldingReview.lean
```

Both commands passed. The temporary review file checked the full-epigraph
and depth-zero client statements and printed axioms for
`foldSum_abs_sub`, `foldApprox_error`, `foldObjective_le`,
`foldEpigraph_iff`, `foldEpigraph_error`,
`foldEpigraphConstraints_iff`, and `foldError_succ`. Every list was
exactly `[propext, Classical.choice, Quot.sound]`.

The source hash was unchanged before and after the checks:
`4e481c33daf8cf940c4227d619e2382c27511b19ae28be625eed7a0032830bc5`.
No proof source was edited. No project-wide verification or CI inspection
was performed.

## Follow-up review: actual finite affine lift

`foldingSystem` has a finite list of real affine maps on
`LiftPoint 1 0 n`, with one original input, one output, `n` continuous
auxiliaries, and zero binary coordinates. Its list includes the two
input bounds, the lower output inequality, and three inequalities per
fold. Recursive substitution into the tail rows is an actual affine-map
composition. The type therefore enforces linearity of every displayed
row; the construction does not merely label an arbitrary predicate a
linear formulation.

`foldingSystem_feasible` proves equivalence between these rows and the
core interval, fold-feasibility, and output predicates. The tuple
projections correctly select continuous auxiliary coordinates, not code
coordinates. `foldingBinaryLift_relaxation` then identifies the actual
existential projection in the common model with the interval restriction
and `FoldEpigraph`. The vacuous binary bounds concern `Fin 0`; they do
not hide integrality requirements on the fold auxiliaries.

`foldingBinaryLift_isEpigraph` supplies the full
`IsEpigraphRelaxation` contract: every `w >= t^2` over `[0,1]` has a
feasible lift, and every projected point lies in that input interval and
satisfies `w >= t^2-foldError n`. There is no upper output row or
implicit bound truncating the epigraph. The common model uses the actual
finite rows to obtain convexity and integer-lift inclusion.

The exact row count is **`3n+3`**, including both input bounds, with
exactly `n` continuous auxiliary coordinates and zero binaries. At depth
zero the three rows are just the two interval bounds and
`w >= t-1/4`. At depth `L+1`, the verified error identity gives
`2^(-2L-4)`, with `L+1` auxiliaries and `3L+6` rows. Thus I4 has an
actual LP of the advertised linear size and error.

Additional targeted checks, from `formal/` with the same environment:

```text
lake build --wfail Formal.QuadraticPrecision.FoldingLift
lake env lean /tmp/Topic20FoldingLiftReview.lean
```

Both passed. An initial client invocation preceded completion of the
module build and reported its missing object file; rerunning after that
successful build passed. The client checked the depth-zero row count,
the actual `HasBinaryEpigraphLift` statement at depth `L+1`, and axioms
for `foldingSystem_rowCount`, `foldingSystem_feasible`,
`foldingBinaryLift_relaxation`, `foldingBinaryLift_isEpigraph`, and
`square_has_zeroBinary_epigraph`. All five axiom lists were exactly
`[propext, Classical.choice, Quot.sound]`.

Reviewed `FoldingLift.lean` SHA-256:
`f9b6833391ce89b93c2661ed3e048288ce8c3de8821901e88f4a202285f7e9ed`.
The current folding core hash is
`da55626d51e9591c71d272339f1da0ac8f6b7cb8becec7639c00a12611111819`;
its only change since the first review is an introductory documentation
comment. Removing that comment reproduces the first reviewed hash.
The bridge build rechecked this core successfully. No proof source was
changed by this review.
