# Adversarial review: error-bound transfer and cluster attribution

Date: 2026-09-22. Reviewer: independent `review_error_transfer` agent.
Reviewed [the transfer note](research-20260922-error-bound-transfer.md),
[the existing cluster result](../results/cluster-free-branch-and-bound-constrained-minima.md),
its earlier review, and the current README entry. The author files were not
edited in this review.

**Verdict.** The projection theorem, spatial corollary, packing bound, and
Hölder extension are correct under the stated assumptions and the standard
convention that boxes are closed bounded rectangles and `w(Z)` is their
largest side length. Define that convention explicitly in the transfer note.
The main needed correction to the existing result is attribution and
significance, not withdrawal of its mathematical conclusions. The transfer
note appropriately identifies classical exact-penalty growth as the core
principle. Its branch-and-bound use remains a useful application whose
publication novelty has not been established.

## Proof audit

For Theorem 1, a nearest feasible point exists because `F` is nonempty and
closed in finite-dimensional space. Compactness of `F` is unnecessary: a
minimizing sequence for distance can be restricted to a bounded ball. With
`d=dist(z,S)` and `e=dist(z,F)`, the inclusion `S subset F` gives `e<=d<=rho`.
Any selected projection satisfies `dist(y,S)<=d+e<=2rho`. Thus neither the
feasible growth assumption nor the Lipschitz inequality is used outside its
specified neighborhood. Nonuniqueness of the projection causes no issue.

The displayed inequality `d_y^2>=d^2-3rho e` follows from
`|d_y-d|<=e` and `d_y+d<=3rho`. It preserves the original feasible growth
coefficient `a`; there is no unmentioned reduction of that coefficient.
The final residual coefficient has the correct sign. One could improve
`3rho` to `2rho`, using `d_y>=d-e>=0` and
`(d-e)^2>=d^2-2rho e`, but this is an optional constant improvement, not a
correction or significant new result.

The corollary takes an infimum of a pointwise inequality; it requires neither
attainment nor convexity. Relaxed infeasible boxes are allowed. Crucially,
the projection need not belong to the box. Projecting onto `F intersect Z`
would invalidate the intended application and exclude empty feasible boxes.

The compact-neighborhood Lipschitz remark is sound. If a function is `C^1`
near compact `S`, choose a sufficiently small closed neighborhood of `S`
inside its differentiability domain and bound its gradient on a somewhat
larger compact neighborhood. Nearby pairs can be joined by segments in that
larger neighborhood; function boundedness handles pairs separated by a fixed
positive distance. Convexity of the neighborhood of `S` is not needed.

The MFCQ-to-uniform-error-bound passage over compact `S` is sound by finite
covering. This argument requires the constraint system to include any active
domain bounds, or an error bound expressly relative to an exact ambient
domain. The transfer note already states this qualification.

The SOSC argument is correct for a **fixed KKT multiplier** whose Lagrangian
Hessian is positive on every nonzero vector of the actual critical cone.
Along a feasible sequence with bounded quadratic growth ratio, the limiting
normalized direction satisfies the linearized constraints. The ratio bound
forces nonpositive first objective derivative; KKT forces nonnegative first
objective derivative. The limiting direction is therefore critical.
Complementarity and feasibility give `f(y)-f* >= L(y)-L(z*)`; Taylor expansion
then gives the contradiction. This establishes growth with any coefficient
strictly below `gamma/2`, including the old result's `gamma/4`.

Strict complementarity is not needed in this argument. Positivity merely on
the subspace that annihilates all active gradients is insufficient without
strict complementarity: the old quartic example correctly establishes that
narrower warning. It does not show strict complementarity is necessary for
the mixed distance/width conclusion under ordinary SOSC.

## Counting, exponents, and examples

Theorem 2 is correct. Every unfathomed box lies within distance
`sqrt(C/a) delta` of `S`; assigning it to a radius-`delta` covering center
places the whole box in a cube of side
`2(sqrt(C/a)+1+sqrt(n))delta`. Dividing its volume by `(delta/2)^n` gives
exactly the stated bound. Disjoint interiors suffice because rectangle
boundaries have zero volume. Compactness of both sets supplies the closest
pair used in the proof. The positive-tolerance cutoff follows from the
strict fathoming inequality, including equality `C delta^2=eps`.

The covering-number qualification about Minkowski dimension is essential and
correct. Finite upper Minkowski dimension alone does not give a covering
bound with that exact exponent. Compact embedded `C^1` manifolds do have the
claimed covering estimate. For the grid example, take meshes that divide the
domain, such as dyadic meshes. There are order `delta^(-s)` boxes meeting
`S`, and the deliberately shifted convex objective gives the asserted lower
bound on each. This demonstrates sharpness within the relaxation-error
assumptions, not inevitable behavior of tight relaxations.

For Hölder error bounds, retain all neighborhood and Lipschitz assumptions
from Theorem 1 while replacing growth and residual exponents. The bound
`L_q=a q(2rho)^(q-1)` is valid for `q>=1`, including `q=1`. Substitution gives
the stated exponent `r=min(beta_f,beta_c theta)` for widths at most one.
If `r<=q`, a tube of radius `R=O(delta^(r/q))` is covered by
`O(R^(-s))` balls of radius comparable to `R`; packing gives
`O(R^(n-s) delta^(-n))`, the first exponent in (5). If `r>=q`, cover at
radius `delta` and pack constantly many boxes per cover ball. This gives the
second bound. Constants need not be sharp. Explicitly importing the original
assumptions in this section would make it more self-contained.

The examples are sound:

- On the nonnegative orthant, `x^2+y^2+4xy>=x^2+y^2`. Its Hessian has
  eigenvalues `6,-2`; repeated constraints violate LICQ, MFCQ holds, and
  nonnegative KKT multipliers must all vanish.
- For `min -x^2` with `x^2<=0`, no linear constraint error bound exists,
  but adding twice the residual gives the penalty `x^2`. Thus the new
  error-bound sufficient condition does not subsume all degenerate variants
  of the old proof; the penalty-growth property does include this example.
- For `f=y^2-x`, `g=x^2`, the point `(w/4,0)` in the stated box satisfies
  `g_Z=0` and has objective `-w/4`. Consequently a bound `L>=-Cw^2` fails
  for every fixed `C` along sufficiently small widths, despite second-order
  pointwise relaxation errors and feasible quadratic growth.
- The corrected old nearby-point example remains useful. Its expanded
  constraint is `q+t^2+s(5b+t-s)`. For the given ranges,
  `5b+t-s>0`, so feasibility requires `q=t=s=0`. The proposed relaxed point
  gives precisely the displayed first-order gap. No argument in the transfer
  note contradicts this example: the two bounds compare different values.

## Direct literature check and scope of the correction

Directly inspected [Anitescu's open preprint](https://optimization-online.org/wp-content/uploads/2004/08/918.pdf),
Sections 1.2–1.3, printed pages 5–6. Equations (1.14)–(1.15) define the
infinity- and one-norm residuals. Equations (1.18)–(1.19) assert quadratic
growth of the corresponding exact penalties, assuming a nonempty KKT
multiplier set and the generalized growth condition (1.16). Under MFCQ,
the text identifies (1.16) with feasible quadratic growth (1.17). The source
expressly attributes the penalty result to Bonnans–Shapiro, Theorem 3.113;
reference [7] identifies their 2000 book. I did not inspect that book theorem.
The smooth NLP setting is specified in Section 1.1. This directly supports
the transfer note's isolated-point prior-art comparison; it does not alone
establish the book theorem's full scope or a published nonisolated-set
branch-and-bound theorem.

The following revisions are justified:

1. In the existing result's status, summary, and literature section, describe
   the mixed bound as an application of established exact-penalty growth.
   Retain the elementary Lagrangian proof as an explicit sufficient-condition
   proof if useful. Its length does not establish novelty.
2. State that LICQ and strict complementarity are sufficient named
   assumptions of that presentation, not essential assumptions of the
   cluster conclusion. Link the broader metric-error-bound/feasible-growth
   version and the still more general penalty-growth formulation.
3. Preserve the distinction between comparison with `f*` and comparison with
   the feasible optimum inside the box. The corrected counterexample
   demonstrates failure of a neighborhood property for one standard scheme;
   it does not settle whether another scheme can have that property.
4. Replace any suggestion that the work resolves the literal Kannan–Barton
   neighborhood question by the precise statement that it supplies a
   sufficient local fathoming estimate under stated assumptions. That
   estimate bypasses the neighborhood property for this application.
5. Supersede the earlier review's statement that strict complementarity was
   shown necessary, and its broad claim to resolve the practical open
   question. The current result already qualifies the first point, but the
   historical review still needs an explicit attribution/scope update.
6. Keep the valid fixed-scale count, its incumbent and shape qualifications,
   and the conditional width-tight reduced-space corollary. Neither this
   prior-art match nor lack of broad solver complexity makes these false.

The absence of a directly located published branch-and-bound statement does
not prove originality. Conversely, a prior penalty-growth inequality is not
evidence that every application, example, or domain-reduction observation in
the repository has already appeared. The defensible status is a useful
application and clarification, with substantive mathematical novelty
unestablished. It is not presently evidence of the major advance sought by
the active research objective.

## Verification record

Inspected the two author files and earlier review with targeted `cat`,
`sed`, and `rg` commands. Accessed the specified Anitescu PDF with web
`open`, `find`, and page-5 `screenshot`. Independently re-derived the proofs
above. Ran one inline `python`/SymPy calculation asserting the orthant
example's eigenvalues, the old corrected example's constraint identity and
objective gap, and the singular-system relaxed-feasible witness. All
assertions passed. These exact checks verify those identities only; they do
not establish general theorems or novelty. No optimization solver experiment,
Lean formalization, CI inspection, or project-wide check was performed.
