# Source inventory: quadratic aggregation consequences

Inventory date: 2026-09-22. This is a pre-completion scope and semantic review,
not a report of successful Lean verification.

## Authorized source scope

The user authorized the recommended follow-up work. For topic 28 the source
is [the quadratic aggregation note](../../../results/quadratic-aggregation-trivial-hull-certificate.md):
Corollaries 1 and 4, Lemma 4, the two recommended boundary examples, and the
exact SDP characterization in Corollary 3. The independently recommended
infinite aggregation construction belongs to a separate later package.
The full hull-description theorem behind Corollary 2 and the classical
general criteria behind Corollary 5 were explicitly deferred. Proving a
two-form convexity result needed for actual HHC of the examples does not
by itself bring all of Corollary 5 into scope.

The completed [topic 27](../27-quadratic-aggregation/README.md) supplies the
main certificate equivalence, its HHC specialization, and supporting
lemmas. Its frozen claims and historical checks describe that earlier
scope. New consequences must have their own declaration coverage and
verification evidence. The note's blanket statement that all corollaries
and examples are unverified should change only after the corresponding new
claims pass their checks.

The first boundary example is the closed system with empty strict system
in Section 4. Its role here is to disprove the closed-system equivalence
without strict feasibility. The additional discussion of nonempty interior,
absence of BDS-good aggregations, and Remark 2.24 supports a different
assertion and is not needed for that counterexample. The second boundary
example is the two-inequality slab in Section 7: even under HHC, globally
convex aggregations and the Shor projection can strictly exceed the hull.
These are distinct from the example in Section 5 without HHC and the
empty-Shor example following Lemma 4.

## Interfaces that must preserve the source meaning

The closed feasible set uses weak inequalities. Neither its convex hull
nor the strict set's convex hull is silently replaced by its closure. A
nontrivial PSD quadratic is unbounded above, but a nonzero linear term
also matters when the quadratic block vanishes. Both cases are required
for the proper closed sublevel set used in Corollaries 1 and 4.

The Shor projection quantifies a symmetric matrix `X` subject to
`[1 x^T; x X]` PSD and the lifted linear inequalities. A covariance variable
`Y=X-xx^T` is a useful implementation, but its equivalence to the block PSD
condition must be proved. Likewise, the nonnegativity of the pairing of
two PSD matrices must be a theorem, not an assumption supplied to the final
interface. Convexity of the projection is needed to infer `conv(S)⊆P` from
`S⊆P`; set inclusion alone is insufficient.

The meaning of "every convex certificate is trivial" is that every
nonzero nonnegative weight vector with PSD quadratic aggregate has zero
quadratic and linear aggregates. It does not say its constant vanishes.
At a strict feasible point, its constant is strictly negative. The zero
weight vector can be added harmlessly when describing the dual cone.

Lemma 4 has no AHC or HHC assumption. Its PSD-image-plus-orthant cone can
fail to be closed. A proof may identify its closure by dual inequalities,
but closure membership alone does not produce a feasible Shor witness.
The source repairs this using a strict feasible point and the quadratic
midpoint identity: an interior cone element plus a closure element lies
in the interior. An alternative separation argument is acceptable if it
actually proves feasibility and does not assume cone closedness. No
strictly feasible SDP lift is supplied as an additional input.

For Corollary 3 the normalized feasible set is compact because it is a
closed subset of the simplex. It may be empty. When nonempty, the signed
linear objectives attain finite real maxima. Both signs for every
independent symmetric-matrix or vector coordinate vanish exactly when all
coefficient pairs vanish. If an implementation first uses all matrix
entries, it must still justify the source's smaller coordinate count and
the symmetry reduction. This is an exact mathematical characterization,
not a numerical decision algorithm or verified complexity bound.

Both examples assert HHC. A function parameter whose type merely assumes
HHC does not formalize a counterexample under HHC. The implementation must
prove convexity of every actual homogeneous hyperplane image. The closed
example reduces to a two-dimensional span of forms; the slab example
already has only two forms. A fully proved Dines theorem is one possible
route, while an explicit image calculation also suffices.

## A simpler exact proof of Lemma 4

The implementation can avoid introducing the closure cone altogether. Fix
`x` and suppose there is no PSD `Y` with all residuals
`f_i(x)+⟨A_i,Y⟩` strictly negative. The convex translated PSD image is then
disjoint from the open negative orthant. Open-set separation gives
`lambda≥0`, `lambda≠0`, such that

```
0 ≤ sum_i lambda_i f_i(x) + ⟨A_lambda,Y⟩    for every PSD Y.
```

Taking `Y=0` makes the first term nonnegative. Taking arbitrarily large
positive multiples of `vv^T` proves `v^T A_lambda v≥0` for every `v`, hence
`A_lambda` is PSD. If every convex certificate is trivial, its quadratic
and linear parts vanish. Strict feasibility at any fixed `x0` then gives
`c_lambda<0`, contradicting the first-term inequality at `x`.

Thus every fiber even admits a PSD covariance slack with strict residuals.
This proof uses neither closedness of the translated image nor attainment
of an SDP optimum. It is a valid strengthening of the source conclusion;
the strict slack is derived from the original hypotheses, not an added
premise. The final verification record must identify the actual proof route
and avoid claiming that the source's separate cone-closure identity was
formalized if it was not needed.

## Related paper and documentation

The [paper formal account](../../../paper-quadratic-aggregation/sections/90-formal-verification.tex)
currently states the completed eleven-module, 178-declaration topic 27
scope and excludes consequences and examples. Its
[supplement guide](../../../paper-quadratic-aggregation/FORMAL-VERIFICATION.md)
also records the coordinator's independent stage 2 rerun and a later
portable-source packaging obligation. The paper has concurrent author
changes: the formal account now refers to the mathematical proof in
`sections/02-certificate.tex`, while its process status is being developed
separately. Do not overwrite those changes or infer paper-stage acceptance
from completion of Lean checks.

After verification, update the source note and the paper's formal account
with exact new coverage and remaining exclusions. Keep the topic 27 counts
identified as its core package's counts and report new package counts
separately. Add the new modules, coverage, toolchain information, audit,
and actual logs to any portable-source packaging obligation. Rebuild the
standalone supplement only after coordinating with the manuscript author;
record the checked file fingerprints so evidence remains attributable to a
specific snapshot. Paper stage review and Lean semantic review remain
distinct processes.

## Completion review

Map every frozen claim to actual declarations and inspect the resulting
headline types for hidden hypotheses. Review the block/covariance bridge,
the nonclosed-cone step, objective attainment and infeasibility, exact
counterexample coefficients, and actual HHC. Reject custom axioms or
unfinished proofs. Record warning-free targeted builds, transitive axiom
checks, kernel replays, and targeted documentation checks as their actual
results; do not attribute these local checks to CI.
