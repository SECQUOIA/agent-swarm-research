# Independent review of piecewise recourse curvature

Date: 2026-10-03. Scope: the mathematical statements in
[piecewise-curvature.md](piecewise-curvature.md), read independently of
the author's derivation. This is research-agent review, not external
peer review. No publication-priority or solver-performance assessment is
made here.

**Verdict:** no substantive mathematical gap found in the stated
certificate theorem, its composition with the existing sparse solver
theorem, the finite positive-definite construction, or the separating
family. The certificate-size parameter and implementation limitations
are necessary parts of the claims.

## Coverage and replay

The adopted BSP convention is sufficient: start with a full-dimensional
box, accept only splits with two full-dimensional children, and keep
both closed children. Induction on the tree proves that the closed leaves
cover the box, including intersections of several splitting
hyperplanes. A parameter on a splitting hyperplane may be evaluated in
either subtree; both have a containing closed leaf. Consequently there
is no missing lower-dimensional parameter stratum.

The rational dual inequality has the correct signs. If
`G^T w=-c`, `w>=0`, and `h^T w<=c0`, then on `Gv<=h`,

```text
c0+c^T v = c0-w^T Gv >= c0-w^T h >= 0.
```

The converse follows from LP duality on the nonempty bounded leaf.
Using this representation in the recognition LP stays linear even when
`c0,c` contain unknown selector coefficients. Rational stationarity and
quadratic complementarity coefficient checks suffice because each leaf
has interior. Exact PSD checking and all of these algebraic checks take
polynomial bit time in the supplied certificate encoding.

An implementation should remove zero-normal tautological inequalities
before demanding a point strict in every displayed inequality. A
full-dimensional polyhedron may contain a redundant `0<=0` row. This is
an input-normalization detail, not a failure of the full-dimensional-leaf
contract. The scalar constructor's implementation is reviewed separately
from this proof-level coverage argument.

## Curvature across interfaces

The proof uses more than continuity, as it must. After subtracting the
common parameter quadratic, each value factor is the infimum of affine
functions of its parameter and is concave. On every coordinate line its
derivative jumps can therefore only be downward. The common quadratic
does not change a derivative jump. After subtracting half the proposed
piecewise diagonal upper bound times the squared coordinate, the
ordinary second derivative on each open piece is nonpositive and every
join remains a downward jump. This proves coordinatewise concavity.

A line lying in one or several BSP faces is also covered. Restricting
the finite leaf closures to the line gives finitely many closed
intervals. On overlaps, certified values agree because they are values
of the same conditional optimization problem. On a nontrivial overlap
the two restrictions are therefore the same univariate polynomial. The
derivative-jump argument remains valid.

A useful singular adversarial case is `min_{-1<=y<=1} y v=-|v|`.
Its two constant affine selectors have piece Hessian zero, yet the
value has a downward kink at zero. The claimed bound correctly gives
coordinate curvature zero; an argument requiring differentiability
would fail on this valid input. In contrast, the continuous piecewise
affine function `|v|` has the same zero piece Hessians and an upward
kink, and would refute a proof based on continuity alone. The
concave-infimum step excludes precisely that error.

Summing the local coordinate upper bounds and the direct quadratic
diagonal is valid without enumerating the global overlay. Taking a
maximum separately for each block can overestimate the curvature but
cannot underestimate it.

## Sparse complexity and exact output

The filtered-grid proof uses coordinatewise upper semiconcavity for
independent rounding, exact rational factor values for the tree tables,
and growth for contraction and the state count. It does not require
differentiability of the reduced factors. The new finite-leaf evaluator
therefore meets that interface. A tree traversal, rational quadratic
evaluation, and affine lift cost polynomially in the explicit package
size `S`; no implicit exponential overlay is used. Rational values from
different pieces do not require a common denominator across all leaves:
each selected DP value sums only an input-sized number of factor values.

Full-vector growth descends to the retained vector by evaluating it at a
conditional optimizer. Original uniqueness implies retained uniqueness.
For exact output, using the original rational QP's coordinate and value
height bounds is the correct step. It avoids treating a piecewise
function as a single quadratic. Once the certified value interval
isolates the original optimum value, premature coordinate
reconstruction cannot cause false acceptance: the lifted point must be
original-feasible and have exactly that isolated value. The existing
doubling-accuracy and capped unknown-growth arguments then give the
stated parameterized bound.

If all reduced coordinate bounds are nonpositive, separate concavity
indeed puts at least one optimum at a retained box vertex. Endpoint DP
and a certified private lift are exact and do not need growth. This
does not assert that every original optimizer has endpoint retained
coordinates.

The theorem measures complexity in `S`, which includes the entire
partition. It neither bounds the number of pieces by the original QP
encoding nor solves the unrestricted width-plus-negative-curvature
problem. These qualifications are stated correctly in the note.

## Recognition and finite construction

The central-gradient affine-selector proof extends from a box to any
full-dimensional bounded polyhedron. An affine feasible coordinate
attaining a bound at an interior parameter is constant; a one-signed
affine gradient vanishing there is identically zero. All central
optimizers have the same gradient because their differences are in the
kernel of the PSD Hessian. The proposed fixed pattern is therefore
necessary for every affine selector, including selectors passing through
degenerate central optimal faces. Its KKT conditions are also
sufficient. The dualized global sign tests yield a polynomial-size LP.

For positive-definite `C`, every free principal submatrix is invertible.
Each of the `3^m` bound/free patterns supplies a rational affine response
and finitely many affine KKT inequalities. Their nonconstant boundary
hyperplanes form an arrangement with at most the stated number of
full-dimensional cells. An interior point of a final leaf has an
optimal pattern. Its nonzero affine inequalities cannot change sign in
that leaf interior, since every relevant hyperplane is in the
arrangement. Their weak versions hold on the closure. This proves that
one valid pattern labels the whole closed leaf, including all boundary
points. Impossible constant inequalities must simply reject their
pattern. The stated exponential cost and restriction of the automatic
constructor to positive-definite blocks are appropriate.

## Separating family

An independent exact symbolic check verified all three responses,
reduced values, and the expansion in equation (10). The private
gradients on the three regions are respectively

```text
(1-4z, 0),
(0, 0),
(0, M(2z-1)/(M+1)).
```

They have the required lower-bound signs, and no unlisted upper-bound
transition occurs on `[0,3/4]`. The values have second derivatives
`8`, `0`, and `2M/(M+1)`. The response slopes change, so uniqueness of
the private response rules out a globally affine selector on the full
attachment interval.

For the growing family, the expansion gives
`t^2+M r^2+s^2+u/5`; `u>=0` permits dropping the last term. The displayed
elementary estimates imply the claimed `1/36` growth in `(t,u,w)`.
Also `-v^2+3v-tv>=v^2` throughout the given box. Adding nonnegative path
penalties preserves full-vector growth and proves the stated unique
optimizer and value.

The base `(z,v)` Hessian has eigenvalues `+sqrt(5),-sqrt(5)`; all omitted
square and path terms are PSD. Thus `nu<=sqrt(5)`. The `v` principal
subspace is strictly negative since the path Laplacian eigenvalues are
at most four and `eta=1/16`. The restriction to `v=0` is PSD. These two
subspace arguments show that the negative inertia is exactly `m`.
The constant-`v` direction has Rayleigh quotient `-2`, giving `nu>=2`.
The direct and reduced diagonal-curvature bounds, residual bag-size
bound, and `3^m` nonempty overlay cells also check.

This is a valid separation from the two cited methods on the fixed
supplied partition. It is not a hardness example: the explicit
nonnegative growth identity already identifies its optimum. The note
makes that limitation clear.

## Checks performed

Reviewed the full new proof, the existing sparse-convex-value-factor
composition, and the existing affine-selector recognition proof. Ran a
small exact SymPy calculation expanding the family, substituting all
three selectors, differentiating their values, checking their private
gradients, and asserting the growth identity. It passed. This was a
targeted mathematical check, not a benchmark or a project-wide test.

The constructor and checker were reviewed separately after that proof
review. Their results follow. No CI status or logs were inspected.

## Scalar implementation review

Read [scalar_piecewise.py](scalar_piecewise.py) and
[check_piecewise.py](check_piecewise.py), then independently ran

```sh
python3 -B research-20261002-decomposition/completion/theory/piecewise-recourse/check_piecewise.py
```

The initial run passed five separating-family blocks, 485 analytic
response checks, 900 interpolation inequalities, 540 growth inequalities,
20 random positive-definite blocks, 1,980 feasible-value comparisons,
65 singular-kink checks, and 10 invalid-input rejections.

The constructor enumerates active patterns and restricts their affine
KKT conditions to exact rational intervals. Keeping only intervals of
positive length does not lose isolated parameter values: the closures
of neighboring valid intervals cover them. The final interval partition
is ordered, has no gaps or overlaps except shared endpoints, and is
replayed before return. The implementation's exponential pattern budget
and positive-definiteness requirement are explicit.

The verifier does not call the constructor or solve a QP. It checks PSD,
ordered exact coverage, affine stationarity, all coefficients of the
complementarity products, primal and multiplier signs at interval
endpoints, and the value polynomial. Affine signs at both endpoints
establish the signs everywhere in an interval. The KKT identity then
proves the conditional minimum at every parameter, not just sampled
points. The maximum twice-quadratic coefficient is the claimed
coordinate curvature. Boundary value agreement is checked as well,
although it also follows from KKT optimality.

Independent probes beyond the author's checker passed:

- All 15,625 symmetric three-by-three matrices with entries in
  `{-2,-1,0,1,2}`, comparing the Schur-complement PSD test against the
  exact signs of all seven nonempty principal minors.
- Two valid singular affine certificates: a zero first PSD pivot with a
  positive second pivot, and a rank-one Hessian with nonzero off-diagonal
  entries.
- Ten additional malformed certificates, covering booleans, floating
  coefficients including NaN, incorrect dimensions or value length,
  empty intervals, and multiplier/response mutations. All were rejected.
- Three nonsymmetric or indefinite private Hessians. All were rejected
  by automatic construction.
- An empty-private-block certificate: construction, verification, and
  evaluation gave the exact retained quadratic and its curvature.

One small API defect was found in the last case: `Block.objective`
computed the empty quadratic sum as Python integer zero divided by two,
which produced a floating result. This did not affect certificate
construction, verification, or `evaluate`, whose values remained exact.
The author fixed the sum, added exact coordinate normalization and a
dimension check, and added durable regressions. I inspected that fix and
reran the displayed checker successfully. The final run preserves all
the earlier successful counts, increases invalid-input rejections to
14, adds four empty-private exact-output checks, and checks one
cooperative constructor-budget interruption. The objective helper now
returns a `Fraction` in the empty-private case and rejects floating or
wrong-dimension input. No unresolved implementation defect was found in
this review.

This code implements scalar-attachment construction and replay. It does
not implement the general-polytope affine-selector LP or the general BSP
constructor. Integration into a sparse solver is outside this component
review and requires its own integration checks. The mathematical theorem
has broader scope than this tested component.

### Serialization and budget callback follow-up

Reviewed the subsequent `pack_pieces`/`unpack_pieces` additions and the
verifier budget callback, then reran the same targeted command. It
passed six serialization round trips, 14 malformed-serialization
rejections, and two budget-interruption checks, with the previous
mathematical counts unchanged. Encoding uses exact rational strings;
decoding requires the exact field set, vector containers, and integer or
rational-fraction inputs, rejecting floats and booleans. Decoding is
explicitly separate from mathematical certificate verification.

Additional independent probes rejected a Boolean substitution in each
of the nine record fields and rejected a schema-valid but false value
polynomial at the subsequent verification step. A callback also stopped
verification during a piece check, rather than only at entry. No defect
was found in these additions. Budget checks are cooperative; this review
does not claim they preempt an individual rational arithmetic operation.
