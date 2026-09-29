# Independent audit of the binary-leaf star theorem

Date: 2026-09-27. Reviewer: a fresh delegated investigator. Reviewed
[the star-hull note](binary-leaf-star-hull.md) independently, including its
clipping reductions and the passage from objective exactness to hull equality.
This is a positive proof audit with qualified novelty findings, not a claim that
all possible prior formulations have been excluded.

## Proof assessment

I found no gap in either theorem as stated. The important restrictions are that
there is only one continuous square retained in the hull, and that the
optimization theorem allows no positive leaf square coefficient. The proof
does not extend automatically to arbitrary continuous leaves or prescribed
leaf–leaf products.

The delicate part is subtracting RLT products while preserving the true
minimum. It is not enough that the subtracted products are nonnegative. The
note supplies the additional required argument, and it is correct:

1. For the lower correction, the reduced hinge function agrees with the
   original objective on the interval above the threshold. Below it, the
   corrected hinge function equals `a t² + c`, which is at least the original
   minimum because the original endpoint value is `c`.
2. The identity `sum(lambda_i) = b` makes the cancellation exact. For a changed
   leaf, the new breakpoint is precisely the common threshold; an unchanged
   leaf has breakpoint at least that threshold. At the threshold the hinge
   identities remain valid, including ties.
3. Since the threshold is strictly below one, each changed coefficient still
   satisfies `0 < e_i < k_i'`. Thus the hypotheses needed for the complemented
   correction remain available.
4. The complemented correction subtracts `gamma_i (1-t)y_i` in the original
   coordinates. It leaves the original center linear coefficient unchanged,
   decreases both the leaf linear coefficient and its interaction magnitude
   by `gamma_i`, and gives `sum(k_i') - b = 2a`. The strict bound
   `gamma_i < e_i` is correct.
5. The final inequalities put the unconstrained center minimizer inside the
   interval for every binary leaf vector. Only after this fact has been
   established can the minimum of the eliminated binary quadratic be
   identified with the box minimum. Its mixed coefficients are nonpositive,
   so the common-threshold binary rounding argument applies.

The square identity (9) has the correct signs: expanding the square creates
positive leaf-square and leaf–leaf terms, the multilinear eliminated
polynomial cancels the mixed terms, and the added diagonal RLT products
cancel the leaf squares. Negative original leaf curvature is also handled
with the correct sign, because
`d y² = d y + (-d)y(1-y)` for `d <= 0`.

Zero interactions, leaves with fixed optimal response, endpoint ties, a
nonpositive center coefficient, and an empty leaf set are all covered. In the
empty-set case an out-of-interval center minimizer triggers one of the endpoint
certificates; otherwise the final argument is simply completion of one square.

The support-function argument is sound. For a retained-coordinate affine
functional, every leaf is affine. Therefore a binary leaf minimizer exists.
Compactness gives separation without a closure issue. There is no need to
identify a single threshold correction that works for every objective: the
representation is fixed, and objective-dependent certificates establish all
its support values.

## A slightly stronger projection statement

The same proof shows that imposing the binary-leaf diagonal equalities is
optional when only the stated coordinates are retained:

\[
\operatorname{proj}_{(\mu_t,X_{tt},\mu_y,X_{ty})}(S_m)=H_m.
\]

Indeed, Theorem 2 proves exact support values on the full relaxation itself,
not just its binary-leaf face. This does not require another mathematical
ingredient. The binary face remains useful when gluing local distributions.

The geometric counterpart is also simple. Given a deterministic continuous
leaf vector and center `t`, replace every leaf by a Bernoulli variable with
that leaf's success probability. This preserves the center, its square, all
leaf means, and the center–leaf products. Consequently allowing continuous
leaves in the defining set does not change this particular projected hull.

This strengthening does not validate all auxiliary moments. A concrete
counterexample uses three leaves with means `1/2`, diagonal moments `1/2`,
and each off-diagonal moment `1/8`; set the center and all its moments to zero.
The leaf covariance matrix has diagonal `1/4` and off-diagonal `-1/8`, so its
eigenvalues are `0, 3/8, 3/8`. All RLT inequalities hold. A Bernoulli
realization would nevertheless have `sum(y_i) = 3/2` almost surely, since
that sum has mean `3/2` and variance zero. This is impossible for three binary
variables. Projection is therefore an essential qualification.

## Exact targeted calculation

An independent ephemeral Python calculation used `fractions.Fraction` and
`Random(270927)` on 3,000 instances with zero through eight leaves. The
center square coefficient was a positive rational, the center linear
coefficient ranged over positive and negative rationals, each interaction
magnitude was an integer from 2 through 18, and each leaf breakpoint was one
of `1/10,...,9/10`.

The calculation computed the exact minimum by partitioning the center
interval at all leaf breakpoints, then evaluating interval endpoints and each
quadratic stationary point that lay in its interval. It located each clipping
threshold independently by enumerating active breakpoint intervals and solving
the rational threshold equation. After each correction it checked equality of
the exact minima, coefficient restrictions, and the final interval condition
for every binary leaf vector.

The targeted command was `python - <<'PY' ... PY`, executed during this audit.
It finished successfully with:

```text
PASS: 3000 exact-rational clipping instances, m=0..8;
lower_endpoint: 384
lower_shift: 1108
upper_endpoint: 2280
upper_shift: 186
unclipped: 150
```

Counts for a lower shift and a later upper branch can refer to the same
instance. This calculation checks substantial finite families of the delicate
clipping steps using exact arithmetic. It does not prove the arbitrary-input
theorem, verify SDP numerical optimization, or replace the algebraic audit.
No project-wide checks or CI inspection were performed.

## Closest prior formulations

The following comparisons distinguish existence of a conic representation
from polynomial size and from exactness of the particular standard relaxation.

| Source and material inspected | Established conclusion relevant here | Relation to this result |
| --- | --- | --- |
| Dey–Khajavirad, [arXiv:2508.18435v2](https://arxiv.org/abs/2508.18435v2), local full text, Sections 2, 4, 5; current version verified online | A stable set of positive-loop vertices gives an SOC representation of their sign-directed lifted quadratic hull. Proposition 8 gives polynomial size for forests when every positive-loop degree is `O(log n)`. | Conic representability alone is already known. An arbitrary-degree star or forest SDP formulation adds the removal of that degree condition for this subclass, and identifies the standard SDP–RLT projection. The older formulation is SOC, so one should not claim uniform dominance in computational cost. |
| Khajavirad, [arXiv:2601.18545v2](https://arxiv.org/abs/2601.18545v2), local full text, Introduction and decomposition section; current version verified online | An SDP representation permits positive-loop components of size at most two. Polynomial size follows under treewidth and positive-loop degree bounds. | The star lies within the earlier representable class. The plausible addition is a polynomial-size representation with unbounded star degree, not the existence of an SDP representation. |
| Khajavirad, [A Polynomial-Time Solvable Class of Sparse Box-Constrained Polynomial Optimization Problems](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/26/26T_007.pdf), April 27, 2026, open full text, Theorem 1 and its setup | For box QP, polynomial solvability follows from `tw(G)=O(log n)` and `|C union N(C)|=O(log n)` for each connected positive-diagonal component `C`. The proof fixes nonpositive-curvature coordinates at binary values and eliminates continuous blocks. | The neighborhood condition excludes general high-degree stars and high-degree positive vertices in forests. The hidden-binary reduction is established. This source does not give the asserted standard SDP–RLT projection. |
| Burer–Natarajan–Willemsen, [arXiv:2504.03996v3](https://arxiv.org/abs/2504.03996v3), local full text, Proposition 4 and Appendix A.2; current version verified online | Submodular SDP exactness in dimension at most three; an exactness criterion when all pairwise upper bounds are active and at most one diagonal bound is inactive. | One continuous diagonal by itself is not their stated sufficient condition. The present theorem projects away leaf–leaf products and does not require every pairwise upper bound to be active. Earlier online versions/search extracts asserting arbitrary-dimensional exactness must not be used; version 3 includes a dimension-four counterexample. |

Dey–Khajavirad's hull uses the direction of each quadratic objective
coefficient to impose a square epigraph or hypograph. The bounded moment hull
here retains the exact center-square moment. This difference should be stated
when translating the representation result into their notation. After taking
the required square epigraph, the relevant comparison remains valid.

The natural forest consequence should credit its gluing ingredient:
Dey–Khajavirad Corollary 1 already gives decomposition along complete
separators with no positive loops. In a forest, one can use stars centered at
continuous vertices and binary–binary edge blocks, meeting at singleton
binary separators. The new local star representation removes the exponential
neighborhood expansion in that construction. This audit has not reviewed a
finished forest theorem; it records the applicable prior decomposition result.

## Other terminology checked

The local full-text introduction to Van Vyve's
[*The Continuous Mixing Polyhedron*](https://doi.org/10.1287/moor.1040.0130)
was inspected. Its set couples a common continuous variable, nonnegative
continuous recourse variables, and integer variables through linear covering
inequalities. Its exact cycle-inequality hull is polyhedral. This is a relevant
shared-variable precedent, but no affine reformulation from the retained
second-moment star set was found.

The local full-text introduction and result locators for Atamtürk–Gómez,
[*Submodularity in Conic Quadratic Mixed 0–1 Optimization*](https://doi.org/10.1287/opre.2019.1888),
were inspected. Their basic mixed-binary set is the epigraph of a square root
of a nonnegative affine binary term plus continuous squares. Their exact
general hull treats unbounded nonnegative continuous variables; their bounded
explicit hull is restricted to one binary and one continuous variable. This
does not immediately identify the hull retaining all individual `t y_i`
products.

Qiu–Yıldırım's [general exactness study](https://arxiv.org/abs/2303.06761)
was inspected in the local full text. Its algebraic criteria provide a
framework for exactness certificates. I did not locate a stated structural
star theorem in the examined text. Padberg's Boolean-quadric results and
common-threshold rounding remain established ingredients, not contributions
of the present theorem.

Additional searches combined `one continuous variable`, `binary`, `convex
hull`, `quadratic`, `star graph`, `SDP-RLT`, `one positive diagonal`, `mixing
set`, and `common factor covariance`. They produced related mixed-integer
linearization, indicator-quadratic, mixing, and latent-variable papers, but
no verified equivalent of the star projection. These are limited negative
search findings. A missing search hit does not establish novelty; the claims
should remain qualified until a wider citation audit is completed.

## Significance and remaining limits

The strongest defensible candidate contribution is an exact polynomial-size
description using a familiar degree-two SDP–RLT relaxation for an
arbitrary-degree mixed star, with a possible degree-independent forest
extension. The proof provides explicit certificates of that relaxation's
exactness, and avoids the exponentially many binary leaf assignments used by
the direct disjunctive description.

The scalar star objective is already easy to optimize by sorting breakpoints.
Polynomial-time optimization of the star is therefore not the advance. A
forest algorithm based on messages through binary separators may also be
elementary, so a new tractability claim needs a separate literature check.
The important formulation claim may survive even if such algorithms were
known.

The result can support exact local moment blocks or robust quadratic
certificates. It does not prove that intersecting the hull with application
constraints yields their exact hull, that fixed leaf–leaf moments can be
preserved, that positive leaf curvature is admissible, or that solving these
SDPs improves solver runtimes. Those are separate questions.

## Follow-up: arbitrary submodular graphs with independent positive curvature

The parent investigation subsequently proposed exact SDP–RLT minimization
for every submodular box quadratic whose positive-diagonal vertices form a
stable set, without restricting the graph or its degrees. The proposed route
uses the star hull locally, eliminates the continuous centers, and couples the
remaining binary variables by a common uniform threshold. This is a stronger
objective-exactness statement than the forest consequence, but it is not an
arbitrary-sign graph hull theorem.

An important older tractability result was located during the follow-up.
Fabio Tardella's
[*Connections between continuous and combinatorial optimization problems
through an extension of the fundamental theorem of Linear Programming*](https://doi.org/10.1016/j.endm.2004.03.054)
appeared in Electronic Notes in Discrete Mathematics 17 (2004), 257–262.
The openly available [CTW04 proceedings](https://www.lix.polytechnique.fr/~liberti/ctw04proc.pdf)
contain it on proceedings pages 223–227. I downloaded that PDF and visually
inspected pages 223 and 225 because ordinary text extraction did not recover
the Type 3 font text. Theorem 3 on page 225 already establishes polynomial
minimization of a submodular box function when its residual minimum after
fixing the coordinatewise quasiconcave variables at endpoints is evaluable
in polynomial time.

That theorem applies directly here: the nonpositive-diagonal coordinates
are coordinatewise concave, and the residual positive-diagonal problem is
separable when those vertices form a stable set. Thus polynomial-time
solvability of the proposed stronger class is established by this older
framework. Exactness of the standard degree-two SDP–RLT relaxation is the
plausible additional contribution. The proceedings result does not state that
relaxation theorem.

A related journal article is Tardella,
[*The fundamental theorem of linear programming: extensions and applications*](https://doi.org/10.1080/02331934.2010.506535),
Optimization 60 (2011), 283–301. Its title, author, bibliographic information,
and abstract were verified through the publisher and institutional record;
its full text was not obtained. Consequently this audit cites the exact
theorem from the accessible 2004 proceedings rather than assigning an
unverified theorem number to the journal article.

The recent negative boundary is also relevant. Zhang–Wang,
[*On the Ω(n) SDP relaxation gap for Submodular Box-Constrained Quadratic
Programming*](https://arxiv.org/html/2609.03617v1), September 2026, gives in
equation (5) a four-variable path example with every diagonal positive.
Their Proposition 3 gives a rational gap certificate that survives all cuts
involving only Boolean-quadric coordinates. Their positive vertices contain
the whole path, so this obstruction does not contradict the proposed stable
positive-diagonal condition. The introduction, equation (5), and Proposition
3 were inspected; I did not independently audit that paper's general gap
lower bounds.

Further searches combined `submodular`, `stable set`, `independent set`,
`positive diagonal`, `semidefinite`, `Lovász extension`, and `concave over
modular`. They found the above tractability precedent and relevant
submodular-elimination literature, but no verified equivalent of the proposed
standard-relaxation exactness theorem. Novelty remains qualified.

## Further proof observation: lower RLT bounds may be unnecessary

This observation was sent to the parent and the extension author for a fresh
independent check. It concerns submodular objectives, not the full star moment
hull with arbitrary support directions.

Define the upper-RLT relaxation by

\[
Y=\begin{pmatrix}1&\mu^T\\\mu&X\end{pmatrix}\succeq0,
\qquad X_{ij}\leq\mu_i\quad\text{for every }i,j.
\]

Symmetry includes both upper bounds. Its diagonal inequalities and PSD imply
`mu_i² <= X_ii <= mu_i`, and therefore `0 <= mu_i <= 1`. In the submodular
star case the given proof never needs lower RLT inequalities:

- Negative diagonal replacement uses `y_i(1-y_i)`.
- Fixed-response elimination uses individual box literals and either
  `t(1-y_i)` or `(1-t)y_i`.
- Lower clipping uses `t(1-y_i)`.
- The upper clipping step complements every remaining variable
  simultaneously. This preserves upper RLT, since
  `1-mu_i-mu_j+X_ij <= 1-mu_i` is precisely `X_ij <= mu_j`.
- Completion of squares uses PSD, diagonal upper RLT, and leaf pairwise
  upper bounds in the submodular rounding inequality.

Individual leaf complements are unnecessary when the star is already
submodular. Thus the same algebra proves submodular star objective exactness
for upper-RLT plus PSD. The full moment-hull theorem still needs arbitrary
interaction signs and therefore does not follow for this weaker relaxation.

There is a way to transfer this weaker star exactness to the proposed global
stable-positive theorem without incorrectly demanding local representing
laws. Fix binary means `u` and one eliminated center set function `f_c`.
Let `beta + a^T y` be a supporting affine function of its Lovász extension at
`u`. It is below `f_c` at every binary vector. Thus

\[
q_c(t,y)-a^Ty-\beta\geq0
\]

on the whole box: the polynomial is affine in its leaves, so its minimum
occurs at binary leaves. It is still a submodular star. Upper-RLT star
exactness gives

\[
L(q_c)\geq\beta+a^Tu=f_c^{\mathrm{Lov}}(u).
\]

The common-uniform coupling attains these center bounds simultaneously and
also attains the binary–binary submodular bounds. Therefore the extension's
rounding proof appears to establish exactness of the weaker upper-RLT
relaxation itself. This would match the relaxation studied by
Burer–Natarajan–Willemsen more directly. This observation remains separately
flagged here until another investigator checks its deductions.
