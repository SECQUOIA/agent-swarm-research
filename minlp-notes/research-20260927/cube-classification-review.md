# Independent review of the strict cube extreme-ray classification

Date: 2026-09-27. Reviewer: `cube_classification_review`, independent of the
construction. Reviewed files: [classification](cube-strict-extreme-classification.md),
[frontier note](cube-frontier.md), and the earlier
[five-contact family and exposed-ray proof](../research-20260925/three-positive-disjoint-counterexample.md).

**Verdict.** The classification is correct under its stated strict assumptions.
I found no remaining proof gap. The corrected treatment of the six-cycle is
essential: that pattern is feasible and nonextreme. The result is a useful
partial extreme-ray classification, with originality still qualified. It does
not prove completeness of the augmented disjoint-support certificate cone.

## Proof audit

The cone consists of all polynomials of degree at most two nonnegative on the
closed three-cube. Its ambient vector space has dimension ten. The assumptions
are positive diagonal quadratic coefficients, strictly negative two-by-two
principal minors, and strictly positive values at every vertex.

The reduction to edge contacts is sound. Every cube point is in the relative
interior of its unique minimal face. At a local minimum on a face with at least
two free coordinates, the restricted Hessian must be positive semidefinite.
Any two free coordinates contradict the strict minor assumption. This argument
applies to every zero, since a zero of a nonnegative polynomial is a global
minimum. Positive vertex values then place all zeros in edge interiors.

For an edge with positive endpoint roots `s_a,s_b` and curvature `d_i^2`, the
edge-slack identity in the note is exact. The necessity of `s_a+s_b>=d_i` can
also be seen by evaluating at `t=s_a/(s_a+s_b)`: the squared term vanishes and
the remaining term has the sign of `(s_a+s_b)^2-d_i^2`. This avoids an implicit
sufficiency-only reading of the identity.

The contact-count argument uses the full cone, rather than a cone restricted
to a fixed Hessian signature. With at most four contacts, the homogeneous
value-and-tangential-derivative conditions have a solution space of dimension
at least two. An independent perturbation has a double root on each contact
edge. Both perturbation signs retain positive edge curvatures, positive vertex
values, and negative principal minors for sufficiently small magnitude. The
remaining edges have a positive minimum and stay nonnegative by compactness.
The same Hessian argument therefore proves nonnegativity everywhere. No inward
normal-derivative constraints are missing from this argument: the global
minimum reduction supplies the needed control away from the edges.

The three-on-a-face exclusion gives
`Q_12=d_2(2h-d_1)` with `0<h<d_1`, contradicting
`|Q_12|>d_1*d_2`. The complementations used in putting three contacts in that
position preserve the diagonal coefficients and the signs of the principal
determinants. The star argument also holds: chords between the three axis
contacts force each residual mixed coefficient to be nonnegative, and the
strict minors make it positive. Every other edge has at least two positive
coordinates in its interior and therefore cannot contain a zero.

I independently checked the exhaustive graph step without importing the
author's checker, orbit table, labels, or three stated slack identities.
The [independent checker](checks/cube_classification_independent_review.py)
uses a different vertex encoding, discovers every equality between sums of
three edge-slack coefficient rows, and closes all 792 five-edge sets under
the resulting implications. After the face and star exclusions, exactly 24
sets retain five contacts and 24 sets force six contacts. The first group is
one symmetry orbit, namely the five-contact family pattern. The second group
closes to the six-cycle orbit. Independently computed cube symmetries give 24
orbits before these exclusions. This verifies that the finite enumeration
has not omitted an admissible five-edge pattern.

For the surviving family pattern, the first two contacts give the bottom
constant and linear coefficients. At either lower endpoint of a contacted
vertical edge, positivity of the endpoint value fixes the positive square-root
branch, so the recovered vertical roots have the signs claimed in the note.
The three vertical derivative equations then give the displayed mixed and
linear coefficients. The last remaining mixed coefficient follows from the
bottom value at `(1,1,0)`. The sign deduction for `k` is valid: the chord gives
`k(2D+k)>0`, while the interior-root condition gives `k>-D` and `D>0`, excluding
the branch `k<-2D`.

I also rechecked the earlier converse and exposedness proof. Its nonnegative
identity proves validity, the strict parameters imply all three negative
principal minors and positive vertex values, and its contact equations force
any nonnegative quadratic vanishing at the five contacts to be a nonnegative
multiple of the family member. The coefficient comparison explicitly covers
the zero multiple. Thus summing the five evaluation functionals exposes the
ray in the full cone. The classification does not assume in advance that an
extreme ray has exactly five contacts; choosing any five after the count
argument is legitimate.

## Independent recheck of the six-cycle correction

With `L=h-d_1*x-d_2*y+d_3*z`, the six-cycle equations give exactly

\[
p=L^2+2K T,\qquad T=z+xy-xz-yz.
\]

For example, the upper two tangential derivative equations give
`Q_12+Q_13=d_1(d_2-d_3)` and
`Q_12+Q_23=d_2(d_1-d_3)`. Defining `K=Q_12-d_1*d_2` yields the other two
mixed coefficients, and a vertical derivative gives `ell_z=2h*d_3+2K`.
The lower-axis chord forces `K>=0`; the strict `(1,2)` minor forces `K>0`.

The identity

\[
T=z(1-x)(1-y)+xy(1-z)
\]

proves nonnegativity. Although the two products on the right have degree
three, their sum is the degree-two polynomial `T`, so the decomposition is
inside the stated quadratic cone. The two nonzero summands are nonproportional
because only the square has positive constant term.

An exact strict-regime witness is

\[
(\tfrac12-x-y+z)^2+z+xy-xz-yz.
\]

Its diagonal coefficients are one, its mixed matrix entries are
`(3/2,-3/2,-3/2)`, and every two-by-two principal determinant is `-5/4`.
Its vertex values are `1/4` or `13/4`. It vanishes at the midpoints of the
six edges in the cycle. Thus a proposed exclusion of the cycle as infeasible
would be false even away from every stated degeneracy. The independent
checker confirms this witness, the symbolic double-root equations for both
patterns, and the triangle identity exactly. At illustrative rational
parameters it also gives contact-system rank nine for the family and rank
eight for the cycle; those sample ranks are not substituted for the proofs
covering all parameters.

## Scope, importance, and literature audit

The hypotheses are substantive. They do not merely remove isolated or singular
parameter choices: positive definiteness of a two-coordinate principal
submatrix is itself an open condition outside the theorem. Vertex contacts and
singular principal submatrices are also excluded. One cannot infer that an
arbitrary polynomial satisfying the strict assumptions decomposes into extreme
rays that satisfy them. In particular, completeness of a certificate cone
cannot be deduced by considering only these rays or by asserting that all
other cases are limits without a separate argument.

The established consequence is that searching for additional extreme rays
within this strict regime cannot improve on the symmetry copies of the earlier
family. This sharply narrows the next structural question. It gives no new
tractability result, formulation-size bound for the full hull, or demonstrated
solver benefit. A full classification or an exact characterization of the
remaining extreme rays could support a stronger completeness theorem; the
present theorem alone does not provide it.

I inspected the following primary sources or explicitly identified portions:

- Burer and Letchford, *On Nonconvex Quadratic Programming with Box
  Constraints*, Section 6, especially Lemma 8 and Proposition 10; the
  [local full-text extract](../research-20260925/extreme-prior-sources/burer-letchford-2009.txt)
  and [publisher record](https://doi.org/10.1137/080729529) were examined.
  Their classification separates convex, concave, and indefinite valid
  inequalities; boundary recursion is already present there. That Section 6
  classification is not the contact-pattern extreme-ray classification proved
  here. This distinction does not establish priority beyond the inspected text.
- Anstreicher and Burer, *Computable representations for convex hulls of
  low-dimensional quadratic forms*, [Theorem 7 and the immediately following
  cube example](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf).
  The exact formulation over a triangulated three-dimensional polytope already
  enforces every valid quadratic on the cube. The new classification is more
  explicit about this subset of rays, but weaker in hull completeness.
- Khajavirad, *Tight semidefinite programming relaxations for sparse
  box-constrained quadratic programs*, [version 2, Section 3 and the end of
  Section 6](https://arxiv.org/html/2601.18545v2). The inspected version still
  states the three-positive-loop exactness question. The earlier repository
  counterexample addresses that question; the present classification adds a
  converse only in its strict regime. It does not resolve the completeness of
  adding every family block.
- Hildebrand, *Minimal zeros of copositive matrices*,
  [arXiv record and abstract](https://arxiv.org/abs/1401.0134v4).
  Only the record and abstract were examined in this review. They identify
  adjacent established theory about minimal zeros and irreducibility. No
  assertion of nonequivalence with all results in that paper is based on this
  abstract-only inspection.

Additional searches used `"extreme rays" "quadratic" "cube" nonnegative`,
`"nonnegative quadratic" "box" "extreme"`,
`"quadratic polynomials" "cube" "zeros" extreme`, and variants involving
copositivity, Hildebrand, and five box-quadratic zeros. They identified no
matching theorem, but their sparse results do not establish novelty. Priority
remains unproved; the manuscript should retain its qualified claims.

## Verification record

These targeted commands were actually run and passed:

```sh
python research-20260927/check_cube_strict_extreme_classification.py
python research-20260927/checks/cube_classification_independent_review.py
```

The first checks the author's explicit orbit table and three slack identities.
The second independently checks the finite classification, symbolic contact
identities, an exact cycle witness, and two illustrative contact-system ranks.
The calculus and perturbation arguments, all-parameter coefficient recovery,
and exposedness proof were reviewed mathematically; they were not formalized
in Lean. Neither script establishes novelty or the full cube-cone completeness
claim. No project-wide checks or CI inspection were performed.
