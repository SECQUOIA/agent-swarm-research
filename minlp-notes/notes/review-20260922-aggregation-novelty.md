# Independent review of the aggregation counterexample

Date: 2026-09-22. Reviewer: `aggregation_novelty_review`, independently assigned
to assess the proof's scope, significance, and closest prior results. The
reviewed draft is `research-20260922-aggregation-frontier.md`, specifically its
construction with `r >= 6` and its elementary Gram-matrix proof of HHC. This
review does not cover later changes unless stated explicitly.

The main construction passes this review. It gives an affirmative example for
Blekherman–Dey–Sun Conjecture 3.1 under the definitions in the source. I found
no prior resolution in the sources examined. That is limited discovery
evidence, not proof of priority. The likely original contribution is the
combination of HHC and infinite necessity for **good** aggregations. The
semidefinite convex hull of the associated closed set is already a consequence
of established quadratic matrix programming results.

## Proof and assumption audit

I checked the HHC construction algebraically. Its common-nullspace dimension
bound is sufficient: stacking `B` and `Z` gives a matrix of rank at most `2k`,
so `r >= 3k` provides the required `k` orthonormal rows. The correction
`Y=D^(1/2)U` preserves the hyperplane because `BU^T=0`, preserves the cross
terms because `ZU^T=0`, and has `YY^T=D`. The vector-valued Cauchy–Schwarz
argument proves `D` is PSD. The `s=0` branch also works, including zero mixing
weights. No assumed definiteness or independence of the output forms is
silently used. This establishes every hyperplane image, not merely the full
quadratic image or one selected hyperplane.

The classification of good multipliers also holds. A negative eigenvalue of
the two-by-two leading matrix is repeated `r` times, which excludes it under
the BDS inertia requirement. Conversely, PSD of that matrix gives a convex
aggregate and a strictly negative constant term. Strict negativity on all
finite convex combinations follows directly from Jensen's inequality. Thus
the note correctly identifies **all** good multipliers, including coordinate
rays, rather than only a convenient subfamily.

The Gram matrices used for the witnesses are positive definite throughout the
stated interval. Weighted AM–GM gives precisely the stated equality ray.
Selecting a missing ray therefore yields a point satisfying every member of
an arbitrary finite list strictly while failing another valid strict
aggregate. This argument does not require the optional hull formula or the
BDS exact-aggregation theorem. Only the HHC assertion is needed to match the
conjecture's hypothesis.

There is a slightly stronger immediate conclusion: any exact representation
of the **open** hull by strict good aggregations must include every witness
ray in the continuum. Omitting even one leaves its witness in the
intersection. Consequently no countable family suffices. This observation is
about strict inequalities; it should not be transferred to the closed hull
without a new argument. A countable dense family of non-strict valid
inequalities can have different behavior.

The failure of PDLC is correctly checked using arbitrary signed multipliers,
as the definition requires. The two ball Hessians have a positive definite
sum in the original variables, but their **homogenized** matrices do not.
Confusing these two distinct definiteness conditions would incorrectly
suggest a contradiction with the literature.

No counterexample or missing assumption was found in these arguments. This is
a mathematical review, not machine verification, and does not certify a sharp
dimension threshold or any stronger formulation lower bound.

## Closest literature and what the construction adds

### Blekherman–Dey–Sun: the target conjecture

The local full text and the
[author PDF](https://www2.isye.gatech.edu/~sdey30/HHC.pdf) were examined for
Definition 2.1, Theorem 2.8, Theorem 2.17, and Conjecture 3.1. The conjecture
asks for a quadratic system satisfying HHC whose hull has no finite good
aggregation description. The source's sufficient finiteness theorem requires
the additional PDLC condition for triples. The reviewed construction meets
the conjecture and fails PDLC, so it is consistent with that theorem.

### Wang–Kılınç-Karzan: the closed hull is already covered

[On semidefinite descriptions for convex hulls of quadratic programs](https://arxiv.org/html/2403.04752v2),
Section 4.1 and Assumption 1 (also inspected in v1, Appendix B.2), gives convex hull exactness for quadratic matrix
programs with replication width at least the number of constraints and a
positive definite nonnegative combination of the leading quadratic matrices.
For the present **closed** set, take zero objective, three constraints,
replication width `r`, and sum the two ball Hessians to obtain `I_(2r)`.
Therefore the established theorem applies for `r >= 3`. It allows linear
terms too. Its assumptions concern leading matrices, not BDS's homogenized
PDLC. Its conclusion establishes SDP exactness, not HHC of every homogeneous
hyperplane restriction or necessity of infinitely many good aggregations.
The older eigenvalue-multiplicity results are thus weaker comparators than
this 2024 result. The open hull needs an additional argument; simply replacing
all non-strict inequalities by strict ones is not a general inference.

### Brun–Sun–Watson: inner products over balls already arise in an application

[Modeling Adversarial Wildfires for Power Grid Disruption](https://arxiv.org/html/2603.18473v1),
Section 3.2.1, Corollary 1, applies Wang–Kılınç-Karzan to obtain the exact Shor
hull of the inner-product **hypograph** over two Euclidean balls in dimension
at least two. The paper develops mixed-integer conic wildfire models and
additional SOC relaxations. This is a concrete application connection, but
does not establish solver gains from the present counterexample. Fixing a
hypograph level after convexification need not commute with taking the
convex hull, so their corollary alone is not a proof of the fixed-level hull.
The general quadratic matrix theorem above supplies the relevant comparison.
There is no basis for claiming that convexifying an inner product over balls
is itself new here.

### Dey–Muñoz–Serrano: infinite necessity predates HHC

The local published full text of
[On obtaining the convex hull of quadratic inequalities via aggregations](https://doi.org/10.1137/21M1428583),
Proposition 2.8 and Section 7.4, was examined. It already gives a bounded
two-dimensional example requiring infinitely many **valid** aggregations.
Its aggregation family does not impose the BDS inertia condition; the paper
explicitly discusses this distinction. Thus neither the broad phenomenon of
infinite necessity nor a proof based on continuously varying active
aggregations is new. The present example supplies HHC and the restrictive
good-aggregation property simultaneously.

For clarity, the older example has defining forms

```
g1(x,y)=x²-1,
g2(x,y)=y²-1,
g3(x,y)=-(x-1)²-(y-1)²+1.
```

An independent check shows why it does not settle the HHC conjecture. Restrict
its homogenization to the hyperplane `y=0`. Its image coordinates are

```
(x²-t², -t², -x²+2xt-t²).
```

The images of `(x,t)=(1,0)` and `(0,1)` are `(1,0,-1)` and `(-1,-1,-1)`.
Their midpoint `(0,-1/2,-1)` would force `x²=t²=1/2` and `xt=0`, an
impossibility. Thus this system fails HHC.

There is also a terminology trap in the later topological preprint. Its
Example 3.10 restates this example using the phrase “good aggregations.”
That wording should not be used to erase the inertia distinction. The older
paper's displayed family, parameterized by `a in (0,1)`, is

```
lambda=(a²,(1-a)²,a²-a+1).
```

Its leading matrix is `diag(a-1,-a)`, which has two negative eigenvalues;
its homogenization therefore has at least two negative eigenvalues. This
family is not permissible under BDS's definition. I did not investigate all
consequences of this discrepancy for the later preprint and make no claim
about its published correction history.

### Dey–Han–Wang: another aggregation operation

[Aggregation of Bilinear Bipartite Equality Constraints and its Application to Structural Model Updating Problem](https://arxiv.org/html/2410.14163v1),
Theorem 2, and the local 2026 published full text were examined. The example
is `xy1=xy2=1/2` in `[0,1]^3`. It requires infinitely many intersections of
convex hulls of aggregated equalities while retaining the box. Multipliers
are signed, and each aggregated set is convexified before intersection.
This is a different operation from intersecting BDS good quadratic
sublevel sets. In particular, replacing equalities by two strict inequalities
does not produce the same feasible set. The paper supplies relevant
background and cautions against broad first-infinite-aggregation claims,
but it does not state a resolution of the HHC conjecture.

### Blekherman–Dunbar: the four-aggregation result retains PDLC

[The open arXiv version](https://arxiv.org/html/2405.18282v1), Theorem 1.4,
requires PDLC, nonempty interior, `S=cl(int(S))`, and no points at infinity;
it bounds by four the good aggregations defining the closed hull. Its
discussion addresses BDS Conjecture 3.2, not Conjecture 3.1. The
[publisher page](https://epubs.siam.org/doi/10.1137/24M1668445) confirms the
2025 publication but did not expose the published theorem text. The
[2025 thesis search excerpt](https://etd.library.emory.edu/downloads/2j62s637x?locale=en),
Theorem 5.0.5, omits no-points-at-infinity while retaining PDLC and the
interior assumptions. Direct thesis access failed, so I did not verify that
stronger statement in full context. Neither displayed statement covers the
present example because PDLC fails. The candidate's determinant also has
repeated factors, so smooth-spectral-curve results cannot be applied without
checking their hypotheses.

## Novelty search and remaining uncertainty

Searches included the exact conjecture, HHC with “infinite,” “counterexample,”
“2025,” “2026,” and “Kronecker,” plus quadratic matrix programming,
eigenvalue multiplicity, inner products over balls, and joint numerical
ranges. I checked the current publication lists of
[Dey](https://www2.isye.gatech.edu/~sdey30/publications_topic.html) and
[Dunbar](https://alex-dunbar.github.io/). I found no announced resolution of
Conjecture 3.1. These are incomplete discovery channels.

The search also located the primary joint-numerical-range papers
[Li–Poon](https://cklixx.people.wm.edu/poon-1.pdf) and
[Gutkin–Jonckheere–Karow](https://doi.org/10.1016/j.laa.2003.06.011).
Only their definitions/abstract-level criteria were inspected in this pass,
so they do **not** constitute a completed equivalence audit for the general
HHC lemma. Their focus on numerical ranges with normalization or frame
constraints should not be confused with all real linear hyperplane
restrictions of the unnormalized homogeneous map. Equivalence to a known
matrix-factorization or numerical-range theorem remains a residual novelty
question for that lemma.

The plausible publication claim is therefore an explicit resolution of the
stated BDS conjecture, with an elementary sufficient HHC construction and an
explicit continuum of necessary rays. I would not describe this as a new
general SDP exactness theorem, an impossibility of finite conic formulation,
or a demonstrated algorithmic improvement. It is a clear structural result
about the limits of quadratic aggregation. A short research note appears
plausible if priority checks hold; its depth and broader solver consequences
should be assessed separately from the fact that it answers a named
conjecture.

## Verification record

This review used targeted `cat`, `sed`, and `rg` reads of the candidate and
the three local aggregation papers, primary-source web reads, and algebraic
checks written above. No project-wide checks or CI inspection were run. A
small web-text extraction initially failed because `bs4` was unavailable;
the replacement used `requests` and the standard `re` module successfully.
No numerical experiments or Lean verification were performed by this
reviewer. No manuscript authored by the parent agent was edited.

## Addendum: independent recheck of the stronger `r >= 2` HHC proof

After completing the preceding review, the parent requested an independent
check of the substantive strengthening in
`review-20260922-infinite-aggregation.md`, section “Independent stronger HHC
lemma for two columns.” I checked that proof separately. It is valid and
allows the main example to use four original variables (`u,v in R²`).

Here are the potentially delicate points and their resolutions. For every
PSD matrix `G` of order two and every `r>=2`, a matrix `U` with `U^TU=G`
has a factorization `U=Q G^(1/2)` with `Q^TQ=I_2`. In the singular case,
extend the partial isometry from the range of `G` to two orthonormal
columns. Conversely every such `Q` gives the required Gram matrix.

For the hyperplane `tr(P^TU)+s*t=0`, maximization of the linear functional
over these factors gives

```
M(G)=||P G^(1/2)||_*,
M(G)^2=tr((P^TP)G)+2 sqrt(det(P^TP)) sqrt(det G).
```

The SVD maximum is attained. Replacing a maximizing `Q` by `Q R(theta)`
for a planar rotation from `I_2` to `-I_2` preserves its orthonormal columns
and hence preserves `G`. The functional varies continuously from `M(G)`
to `-M(G)`. Its entire attainable range is therefore the interval between
these extremes, even for `r=2`, where the full orthogonal group is
disconnected. Connectedness of that group is unnecessary.

It follows that the attainable pairs `(G,T)=(U^TU,t²)` on the hyperplane
are exactly `G PSD, T>=0, s²T<=M(G)²`. The variational formula for
`sqrt(det G)` in the other review is correct on both positive definite and
singular matrices, so the right-hand side is concave. This set of pairs is
convex. Applying the displayed linear map to the three quadratic outputs
proves HHC. If `s=0`, the range interval contains zero for every `G`; if
`P=0`, the formula reduces to `s²T<=0`. Both degenerate hyperplanes are
handled correctly.

This approval is for the stronger HHC argument itself. The direct two-point
midpoint hull proof still assumes `r>=3`; in dimension two, the ordinary
hull formula uses BDS's aggregation theorem unless another independent
construction is supplied. The novelty comparison should now mention that
the general QMP theorem's generic replication threshold `r>=3` does not
alone certify this particular four-variable fixed-level hull.
