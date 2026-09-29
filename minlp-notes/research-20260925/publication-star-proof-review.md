# Fresh publication-readiness proof review: star moment gaps

Date: 2026-09-25.

**Conclusion: the quantitative theorem passes this independent audit.**
I found no substantive proof gap in the real or rational constructions in
[the accuracy lower bound](star-subset-accuracy-lower.md), their
[uniformly conditioned foundation](star-uniform-condition-subset-gaps.md),
or the general original-epigraph transfer in
[the moment-gluing note](tree-indicator-moment-gluing.md). This review
checks mathematics and scope. It does not establish publication novelty,
optimality of the rate, or a lower bound for other formulations.

## Precisely which relaxation is separated

Every subset has its own PSD pattern matrices. The only common moments
across different subsets are the center matrix `M` and the single-leaf
matrices `M_i`. In particular, pair-pattern marginals from two overlapping
larger subsets need not agree. The gap theorem therefore does not apply
automatically to overlap-consistent hierarchies.

Arbitrary PSD pattern matrices describe closed scalar second-moment
compatibility: a nonzero `diag(0,r)` has no finite scalar measure with that
mass. The explicit local witnesses avoid this issue. Their pattern
matrices can all be positive definite and hence have actual scalar-law
realizations. Thus the claimed gap also survives requiring actual finite
local laws, even though the displayed SDP uses closed moment cones.

For any positive definite `[[p,s],[s,r]]`, use mass `p` and a two-point
conditional law with mean `s/p` and variance `r/p-(s/p)^2`. This realizes
that matrix. Combining these measures over patterns gives the prescribed
center and indicator moments; the conditional leaf completion then also
gives each prescribed leaf mean. Different subsets may use different
center laws, exactly as the specified relaxation permits.

## Geometry and every-subset feasibility

I checked the self-contained planar criterion in
[the Specker-family note](star-hierarchy-specker-gap.md): the effects
`(I+u_i dot sigma)/2` have a common PSD parent exactly when
`conv{+u_i,-u_i}` has perimeter at most four. Necessity follows by
containing that polygon in the zonotope from a parent decomposition;
sufficiency follows from the polygon's planar zonotope decomposition.
The factors two and four in those arguments agree. Perimeter of a
segment means twice its length.

For the real construction, a subset with angular span `s` and `m` points
has perimeter

```
4 [sum_j sin(d_j/2) + cos(s/2)].
```

Concavity in the gaps, monotonicity in `s` on the stated short arc, and
monotonicity of `u sin(beta/u)` bound every subset of at most `k`
directions, including nonconsecutive subsets. Its derivative is
`integral_0^(beta/u) t sin(t) dt`. The stated lower integral bound and
integration from `k-1` to `2k-1` give the inverse-square perimeter
deficit. The separate `k=1` argument is valid and avoids dividing by
`k-1`. The asymptotic constant in the note describes the certificate
only; it is not an upper estimate for the actual hull gap.

I commissioned a separate narrow audit of the rational geometry. It
independently confirmed that deleting an opposite pair only merges
surviving angular gaps, that the adjacent gaps have sum at most pi, and
that the stated deletion-loss identity remains valid when two directions
become a segment. Thus each of the at least `k` deletions costs at least
`ell`, for every required subset. The same argument proves `U>=4` and
handles `k=1` without an exception. The rational short- and closing-edge
tangents also remain rational for asymmetric subsets.

Strict perimeter slack gives finite local realizations. One can obtain
positive pattern matrices directly, without the auxiliary noise parameter
used in the proof: decompose the scaled polygon as `sum_j[-h_j,h_j]`, use
the rank-one effects

```
(||h_j|| I + h_j dot sigma)/2,
(||h_j|| I - h_j dot sigma)/2,
```

and distribute the positive residual
`(1-sum_j ||h_j||) I` uniformly over all patterns. Each vertex is a signed
sum of the generators, which determines the corresponding binary outcomes.
This yields exactly the required marginals and positive definite pattern
matrices. The new finite checker below implements this construction with
exact rational arithmetic.

## Original-variable gap and normalization

The decisive step is the affine cut in the original epigraph variables,
rather than incompatibility of auxiliary matrices alone. Write
`w_i=b_i^2/d_i`, `W=sum_i w_i`, `C=sum_i c_i`,
`a=1+W/2`, and `gamma=1-W/2`. At a binary support `S`, subtracting the
active-leaf completed squares from the claimed cut leaves

```
[(2+h_z) X^2 - 2 h_x X + 2-h_z]/2,
```

where `(h_x,h_z)=sum_i(2Z_i-1)(c_i,-w_i)`. The signed-sum norm bound
`h_x^2+h_z^2<=4` makes this scalar quadratic nonnegative. Thus the cut
is valid on every original feasible point, including a zero center
indicator. Its affine continuity proves validity on the closed convex
hull. No assumption about closedness of a lifted projection is needed.

At the candidate means and cost its residual is exactly
`2-eta P/2=-Delta`. Its epigraph coefficient is one, so the true height
exceeds the candidate cost by at least `Delta`, and exceeds the relaxed
infimum by at least as much.

I checked the normalization inequalities independently:

- For the real arrow matrix, the two nontrivial eigenvalues have trace
  below three and determinant `1-sqrt(3)/2>1/8`. This gives the stated
  strict spectral bounds `1/24` and `3`.
- For the rational matrix, the normalized arrow matrix has determinant
  `1/13` and trace `38/13<3`. Congruence by leaf scalings in `[1,2)`
  gives strict bounds `1/39` and `12`.
- The rational slope bound implies `|c_i|/w_i<8`, and the rotated point
  bound gives `11/416<=z_i<1/2`. The dyadic edges satisfy
  `b_i^2>=w_i`, proving the mean-norm bound.
- A true finite law with center zero and active leaf values `y_i/z_i`
  has cost `sum_i d_i y_i^2/z_i`, bounded by `T_0` in the real case and
  `1584/13<122` in the rational case. Candidate costs are at least the
  positive Schur complement. These statements justify division by the
  true height in the relative-gap assertion.
- Singleton compatibility gives `0<=r_i<=v`, hence every relaxed cost
  is at least `(a-W)v>=0`.

Consequently the additive and relative `Omega(k^-2)` conclusions hold
for `N=2k` leaves with all the stated simultaneous bounds. They imply
a necessary order `Omega(epsilon^-1/2)` for uniform accuracy of this
specific relaxation. They supply neither a matching sufficient order
nor a computational complexity bound.

The rational encoding argument is also sound: local rational coordinates,
weights, and edge data have `O(log N)` bits; the polygon perimeter and
noise level have `O(N log N)` bits by a product-denominator estimate;
each original mean has `O(N log N)` bits. The resulting sparse nonzero
data use `O(N^2 log N)` bits. Enumerating all subsets is unnecessary to
construct the instance. The supporting scalar atoms need not be rational.

## General transfer and exact full-parent optimization

The general transfer proof uses a closed full-compatibility set, whose
closedness follows from `0<=G_S<=M` and finitely many patterns. Strong
separation is therefore applicable. Its supportwise recession directions
give the sign restrictions needed after complementing leaf indicators.
The small perturbation preserving the separating gap makes every edge
weight positive and the Schur complement strictly positive. Conditional
square completion then gives the stated strict original-epigraph gap.
Positive definiteness bounds all second moments along bounded-cost
sequences, which makes its closed-hull argument valid even when the
approximating means and indicator masses vary.

I also independently checked the existing consequence being incorporated
into the main moment note: for fixed center mean and interior leaf masses,
minimizing the full-parent objective gives the ordinary and closed convex
hull height, and it attains that height by a finite law. This holds for
general positive leaf diagonals `d_i`, with
`gamma=a-sum_i b_i^2/d_i>0`.

For existence, a constant center and independent indicators give a feasible
parent. The inequality `F>=gamma v` bounds center second moments on a
finite sublevel. PSD inequalities bound all selected moments and parent
matrices, so closedness and continuity give a minimizer. If a minimizing
pattern had a nonzero zero-mass matrix `diag(0,r)`, removing it would
preserve all masses and first moments and decrease the objective by

```
(a - sum_{i in S} b_i^2/d_i) r >= gamma r > 0.
```

That contradicts minimality. Every nonzero optimal pattern therefore has
positive mass and a finite two-atom realization. Conditional leaf
completion realizes the minimum as an actual finite convex combination.
The bounded-parent subsequence argument proves the same lower bound for
the closed hull. This conclusion does not provide a compact formulation:
it retains one matrix per full indicator pattern.

## Targeted verification and its limits

I ran:

```text
python research-20260925/check_star_subset_accuracy.py
python research-20260925/check_star_subset_accuracy_review.py
python research-20260925/check_publication_star_parents.py
```

All passed. The first checks five rational instances and 852 subpolygon
inequalities exactly. The second checks eight generic support identities
and the candidate-cut identity symbolically, plus 4,706 real-family
subsets in floating point. I wrote the third independently; it constructs
215 exact local laws for `k=1,...,4`, represented by 1,964 positive
definite rational pattern matrices, and checks every total and marginal
exactly. It does not import the author's geometric construction functions.

The separate rational-geometry reviewer ran an independent inline
`Fraction` calculation covering 20,415 deletion comparisons for all
nonempty subsets with `N=2,...,11`, and quantitative subset bounds for
`k=1,...,5`; all passed. These finite computations challenge the formulas
and their implementations. The displayed geometry, cut, and compactness
arguments establish the all-order claims. No Lean verification, new
literature search, project-wide verification, or CI inspection was part
of this proof audit.
