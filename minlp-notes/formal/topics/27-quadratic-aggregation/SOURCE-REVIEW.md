# Independent source inventory: quadratic aggregation

Inventory date: 2026-09-22. This is a source and scope review before completed
Lean implementation. It is not a verification verdict.

## Sources and scope

The primary source is
[Aggregation certificates for a trivial convex hull of a quadratic system](../../../results/quadratic-aggregation-trivial-hull-certificate.md),
specifically Sections 1–3: the definitions, Theorem 1, Lemmas 1–3, and the HHC
specialization. These are the package recommended immediately before the
user authorized verification. The [frozen claims](CLAIMS.md) record their full
substance. They do not include every consequence elsewhere in the same note.

The [original review record](../../../notes/review-quadratic-aggregation-certificate.md)
reports favorable proof audits, followed by corrections to ancillary claims.
The [September 22 corrective audit](../../../notes/review-minlp-developments-20260922.md)
retained the main proof but rejected the assertion that globally convex
aggregations imply every valid linear inequality. Formalizing existence of
one nontrivial convex aggregation must not restore that stronger assertion.
These earlier reviews are evidence about a written argument, not Lean checks.

The related `paper-quadratic-aggregation/` directory was already untracked
when this inventory began. At that time it contained only
[PROCESS.md](../../../paper-quadratic-aggregation/PROCESS.md) and
[process/root-investigation.md](../../../paper-quadratic-aggregation/process/root-investigation.md).
The process record says stage 1 is in progress; no manuscript theorem text
was present to reconcile. The investigation file proposes a smaller SDP
characterization, an example separating asymptotic convexity from HHC, and
Shor-closure refinements. Those proposals are not part of this frozen scope.
Existing manuscript work must be preserved, and a formal-verification update
must distinguish this package from the manuscript's separate review stages.

Other related documentation is the aggregation entry in the
[repository README](../../../README.md), the September 21 research entry in
[notes/log.md](../../../notes/log.md), and the
[numerical-check README](../../../code/quadratic_aggregation/README.md).
The numerical checks exercise examples and mostly known two-form cases; they
do not verify the general theorem. The formal topic index and recommended
topic plan need to record topic 27 while preserving queued topics 22–26.

No new literature or novelty assessment is made in this inventory. The
source identifies its HHC specialization with BDS Conjecture 3.3; checking
the formal theorem against the source statement is distinct from establishing
novelty or confirming all bibliographic claims.

## Semantic requirements

The input system uses real symmetric quadratic parts and real linear and
constant coefficients, with finitely many strict inequalities in finite
dimension. Strict feasibility is essential for negativity of a limiting
trivial certificate. The hull is the ordinary convex hull; no closure is
inserted. The source assumes `n,m>=1`; proving a more general dimension or
index formulation is harmless if it specializes to that setting.

A certificate has nonnegative weights that are not all zero. Its PSD
condition concerns only the quadratic block. Nontriviality means the
quadratic or linear block is nonzero; a negative constant alone is trivial.
Normalization to the simplex is derived, not an extra assumption on the
source coefficients. The homogeneous form is evaluated on `(x,t)` with the
cross term `2t b_i·x` and constant term `c_i t^2`.

HHC concerns every linear hyperplane in the homogeneous space. The weaker
hypothesis only needs arbitrarily large good levels for each nonzero normal.
An implementation may use unbounded good levels instead of a prescribed
strictly increasing sequence, but it must prove the source hypothesis gives
its version and prove the HHC specialization. Supplying certificate weights
on those levels in place of convex image hypotheses would leave the central
separation obligation unproved.

The cone `P=cone{(A_i,b_i)}` is closed because it has finitely many generators.
It is not legitimate to infer closedness merely because it is the linear
image of the closed nonnegative orthant: linear images of arbitrary closed
cones need not be closed. Under absence of nontrivial certificates its
intersection with `D={(A,b):A PSD}` is exactly `{0}`. The unconstrained `b`
coordinate in `D` is essential to the meaning of nontriviality.

## Proof simplifications that preserve the theorem

The shortest route uses one compactness argument and no simplex limit.
Fix `x0` in the strict feasible system. Every nonzero nonnegative aggregation
satisfies

```
c_lambda < -x0^T A_lambda x0 - 2 b_lambda·x0.
```

In the nonnegative hyperplane restriction, replace `c_lambda` by this upper
bound. This preserves nonnegativity because its multiplier
`(alpha·x)^2/s^2` is nonnegative. For `rho=norm(A_lambda,b_lambda)>0`, divide
the resulting inequality by `rho`. Its constant coefficient is now bounded
above by a continuous function of the normalized pair on the compact unit
section of the coefficient cone. Both perturbations therefore vanish as
`s` tends to infinity along a convergent subsequence of the normalized pairs.
The limit has PSD quadratic part and norm one, contradicting `P∩D={0}`.
When `rho=0`, strict feasibility instead gives `c_lambda<0`, which immediately
contradicts the hyperplane inequality at any `x` with `alpha·x!=0`.

This argument does not assert boundedness of `c_lambda/rho`; only a bounded
upper replacement is used. The simplex-limit step in the source is an
internal route to the same contradiction, not a separate conclusion of
Theorem 1 or Lemmas 1–3. Q09 records both routes so the scope retains all
advertised mathematical conclusions without requiring an unused proof step.

An alternative simplification also avoids eigenvalues and the formula for
distance to the PSD cone. After the source's simplex subsequence gives
eventual `c_k<0`, put
`p_k=(A_k,b_k)` and `rho_k=norm(p_k)`. If `rho_k=0`, evaluate the hyperplane
inequality at a vector on which the supporting normal is nonzero to get an
immediate contradiction. Otherwise `p_k/rho_k` belongs to the compact unit
section of `P`. Pass to a convergent subsequence with limit `p` of norm one.

Drop the nonpositive constant term from the restricted quadratic inequality
and divide by `rho_k`. For every fixed `x` this yields

```
0 <= x^T (A_k/rho_k) x
     + (2/s_k) (alpha·x) ((b_k/rho_k)·x).
```

The normalized linear coefficients are bounded, so the second term tends
to zero. Hence the quadratic part of `p` is PSD, putting `p` in `P∩D={0}`,
contrary to `norm(p)=1`. This proves the source's contradiction without a
spectral decomposition. Lemma 3 remains a separate frozen source claim even
if this alternative proof no longer needs its numerical constant.

The easy direction can also avoid eigenvectors. A nonzero PSD symmetric
form has a vector with strictly positive quadratic value; otherwise
polarization makes the form zero. Evaluation on scalar multiples of that
vector is a quadratic with positive leading coefficient. If the quadratic
part is zero, a nonzero linear functional is unbounded above. These facts
give properness of the strict sublevel set exactly as the source requires.

Lemma 2 does not need a sign change of `(x,t)`: for any `t!=0`, dividing the
homogeneous inequality by `t^2>0` proves `x/t` is feasible, and the hyperplane
equation gives `alpha·(x/t)=s`. The `t=0` case still requires Lemma 1.

Lemma 3 itself needs closedness and the cone scaling property but no
convexity. Its source assumes both that `P` is closed and that it is finitely
generated; finite generation is only needed to establish closedness in the
application. A formal statement for arbitrary closed cones is therefore a
valid strengthening, with the finite-generation application proved separately.

## Completion review requirements

The final semantic review must inspect the actual headline types and their
dependencies, verify the matrix-to-form bridge if needed, and reject any
new assumption that encodes the conclusion or an unproved proof step.
Every frozen claim requires a declaration mapping. Verification records
must separate targeted Lean builds and axiom checks from numerical sanity
checks, historical reviews, and unobserved CI. No completion is asserted here.
