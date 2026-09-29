# Prior-art audit: nonconvex Hessian-span certificates

Date: 2026-09-27. Scope: the feasible-point certificate and boxed-value
claims in [the nonconvex note](nonconvex-hessian-span-frontier.md).
This audit found a shorter proof of the feasible-point claim from an
established sampling theorem. It did not find a publication explicitly
stating the resulting polyhedral corollary. These are different findings.

**Assessment.** The feasible-point RUR bound, NP membership for fixed
Hessian span, and small feasible-point radius should be presented as
corollaries of Grigoriev--Pasechnik and an elementary face argument. They
do not require a new perturbation or elimination theorem. The boxed
optimal-value and finite-infimum claims require separate arguments;
the face argument below does not settle their priority.

## A face lemma that preserves feasibility

Let \(P\subseteq\mathbb R^r\) be a nonempty polyhedron and

\[
V=\{w:F_1(w)=\cdots=F_h(w)=0\}.
\]

The following geometric argument does not require the \(F_j\) to be
quadratic. Suppose \(P\cap V\ne\varnothing\). Among all nonempty faces
of \(P\) meeting \(V\), choose one, \(F\), of minimum dimension. Include
\(P\) itself among its faces.

Every point of the relative boundary of \(F\) lies in a proper face of
\(F\), which is also a face of \(P\). Minimality therefore gives

\[
V\cap\operatorname{relbd}F=\varnothing.                 \tag{1}
\]

Choose a connected component \(C\) of
\(V\cap\operatorname{aff}F\) which meets \(F\). Then

\[
C\cap F=C\cap\operatorname{relint}F.
\]

This set is nonempty. It is closed in \(C\), because \(F\) is closed,
and open in \(C\), because the relative interior is open in
\(\operatorname{aff}F\). Connectedness gives \(C\subseteq F\).
Thus **at least one entire connected component of the restricted variety
lies in the polyhedron**.

The argument uses connectedness, not a choice of paths or sample points.
It applies to unbounded polyhedra and polyhedra with lineality. Their
face lattices are finite, so a minimum dimension exists. An affine-space
polyhedron has empty relative boundary and causes no exception. A
zero-dimensional face is handled directly.

If the polyhedron has rational input of length \(N\), an independent
subset of its active input rows gives equations for
\(\operatorname{aff}F\). Rational Gaussian elimination provides a chart

\[
w=w_0+Bu
\]

with polynomial coefficient bit lengths. One need not compute or certify
which face is minimal in order to establish existence of a short feasible
witness.

This corrects a tempting but different argument: an arbitrary active face
at a minimum-norm point need not have property (1). The ellipse-cap
counterexample in the nonconvex note refutes that different argument.
It does not refute the minimum-dimension face construction.

## The established sampling theorem and its consequence

[Grigoriev--Pasechnik, *Polynomial-time computing over quadratic maps I:
sampling in real algebraic sets*](https://arxiv.org/pdf/cs/0403008),
Theorem 1.2, handles a quadratic map
\(Q:\mathbb R^r\to\mathbb R^h\) and a polynomial \(p\) of degree
\(d\). It computes real univariate representations meeting every connected
component of \(\{u:p(Q(u))=0\}\). The degrees are
\((dr)^{O(h)}\); for integer coefficients, output coefficient bit lengths
are bounded by the same factor times the input bit size. The theorem
allows nonhomogeneous quadratics and imposes no smoothness or compactness
condition. The primary statement and its representation conventions on
pages 2--3 were inspected directly.

Apply this theorem to the restricted equations
\(Q_j(u)=F_j(w_0+Bu)\), after clearing denominators, with

\[
p(Y)=\sum_{j=1}^hY_j^2.
\]

Here \(d=2\). By the face lemma, one of the returned samples lies in
\(F\). Its rational affine image is therefore feasible in the original
polyhedron. The total representation length is \(N^{O(h+1)}\), including
all coordinates. It describes every coordinate in one field of that
degree bound.

The source uses a Thom encoding for the real root and rational coordinate
functions with a common denominator coprime to the root polynomial.
To obtain the representation used in the manuscript, take the squarefree
part, compute the denominator inverse modulo that polynomial, and isolate
the selected real root by a rational interval. Standard univariate
arithmetic and root separation keep degree and total bits polynomial in
the original representation size. A root or height bound then gives a
feasible point of magnitude at most \(2^{N^{O(h+1)}}\).

For the manuscript's system, its rational Hessian-basis lift turns all
original quadratic inequalities into affine rows plus precisely \(h\)
quadratic equations. Applying the preceding result proves the claimed
feasible-point bound. The case \(h=0\) is rational polyhedral feasibility.
An NP verifier receives a single resulting RUR and checks every original
row by univariate sign determination. It does not receive a claim about
the minimum face, and need not check one.

There is also a direct nondeterministic interpretation: guess active affine
rows defining the successful chart, run the sampling procedure, and test
its samples against every original inequality. An incorrect guess can be
rejected. Exponentially many possible faces obstruct deterministic
enumeration, while each fixed-face sampling problem has polynomial size
for fixed \(h\).

This is mathematical subsumption by an established theorem plus a short
geometric lemma. It is not evidence that anyone previously published this
exact NP corollary. A responsible novelty statement can claim the explicit
corollary or the parameter interpretation, subject to further searching;
it should not present the feasible-point result as a new general
algebraic-certificate technique.

## Comparison with the closest sources

- [Bienstock--Del Pia--Hildebrand, *Complexity, exactness, and rationality
  in polynomial optimization*](https://arxiv.org/abs/2011.08347), published
  in 2023: the primary introduction, pages 2--3, distinguishes one
  quadratic inequality plus arbitrary affine inequalities from fixed
  numbers of quadratic constraints alone. It explicitly says the cited
  few-quadratic analyses do not apply to two quadratics plus arbitrary
  affine rows. Its Theorem 3.6 supplies near-feasible rational certificates
  in fixed ambient dimension. This is useful context, but the introduction
  neither rules out the face corollary above nor establishes its novelty.
  Its focus on rational witnesses must not be confused with exact algebraic
  witnesses. The repository's complete primary text was read.

- [Del Pia--Dey--Molinaro, *Mixed-integer quadratic programming is in
  NP*](https://arxiv.org/abs/1407.4798), Theorem 1 and Corollary 2:
  one rational quadratic inequality and arbitrary rational affine rows
  admit a small rational mixed-integer feasible witness when feasible.
  This extends the earlier continuous result of Vavasis. It permits an
  unbounded integer domain, which the current nonconvex claim does not.
  Conversely, Hessian span one permits opposite quadratic inequalities
  defining an equality and can force irrational continuous coordinates.
  Thus the two statements have different strengths. The primary theorem
  and the adjacent limitations were read; Vavasis's 1990 paper itself was
  not retrieved in this audit.

- [Nie--Ranestad, *Algebraic degree of polynomial
  optimization*](https://arxiv.org/abs/0802.1233), Theorem 2.2 and
  Corollary 2.5: the generic KKT degree is a product of constraint degrees
  times a complete homogeneous symmetric polynomial in the shifted
  degrees. For a quadratic objective and \(s\) quadratic equalities in
  \(r\) variables, this gives \(2^s\binom rs\). Their nongeneric extension
  assumes a zero-dimensional KKT system. After an affine chart this
  explains the familiar polynomial degree when \(s\) is fixed. The
  statements do not provide the required uniform coefficient-bit bound
  for arbitrary degenerate input. The primary theorem, proof, and
  inequality corollary were inspected in the local source copy.

- [Safey El Din--Schost, *Bit complexity for multi-homogeneous polynomial
  system solving. Application to polynomial
  minimization*](https://arxiv.org/abs/1605.07433), Theorem 1 and
  Proposition 4: degree and height bounds are already available for a
  common parametrization of the nonsingular roots of a square system.
  Other components can be singular or positive dimensional. For the
  quadratic KKT multidegrees \((2,0)^s,(1,1)^r\), the degree coefficient
  is \(2^s\binom rs\), and the height expression is polynomial in the input
  for fixed \(s\). Theorem 16's minimization application assumes genericity.
  Consequently, regular-system degree and height estimates are substantial
  prior tools, while preserving feasible limiting branches through
  degeneracy remains a separate obligation. The primary definitions and
  Theorem 1 were read here; an independent subauditor also checked
  Proposition 4 and the optimization hypotheses.

- [Jeronimo--Perrucci--Tsigaridas, *On the minimum of a polynomial function
  on a basic closed semialgebraic set and
  applications*](https://arxiv.org/abs/1112.0544), Theorem 1: compact
  connected components admit explicit algebraic degree and nonzero-value
  separation bounds without genericity. The stated bound uses ambient
  dimension and a common degree bound. Its deformation increases degrees
  of affine rows to the common degree, so the displayed theorem does not
  give a fixed-nonlinear-count improvement when affine rows are numerous.
  The introduction also explains the extension to compact minimizer sets.
  The primary theorem and comparison with Nie--Ranestad were read. No
  claim is made that every possible refinement of that proof was excluded.

- [El Hilany--Tsigaridas, *Bounds on the infimum of polynomials over a
  generic semi-algebraic set using asymptotic critical
  values*](https://arxiv.org/abs/2407.17093), Theorem 1: its constrained
  nonattainment result assumes a closed connected set whose defining
  subsets give smooth complete intersections. The bounds are exponential
  in ambient dimension, rather than polynomial for fixed Hessian span.
  This does not directly imply the proposed unrestricted finite-infimum
  refinement. The primary definition of a complete semialgebraic set and
  Theorem 1 were read. This comparison does not independently verify the
  newer manuscript's finite-infimum argument.

The child auditor also checked the 2025 paper
[Elliott--Giesbrecht--Gillot--Safey El Din--Schost](https://arxiv.org/abs/2508.20607):
its component-sampling results assume a radical ideal and a smooth complete
intersection. These do not improve on the applicability of the older
Grigoriev--Pasechnik theorem needed here. That paper was not read directly
by this audit's author, so this observation is recorded as an independent
reviewer's report rather than an additional first-hand source check.

## What remains separate

The face proof only finds some feasible point. A face of minimum dimension
among faces meeting an optimizer may have relative-boundary points that
are feasible at a larger objective value. The component of the original
variety containing the optimizer can then leave the face. Unrestricted
optimization on that component does not necessarily give the constrained
optimum.

Accordingly, this audit does not derive the boxed optimal-value height
theorem or its unbounded finite-infimum extension from the face lemma.
The latter claims must retain separate proofs and comparisons with
coefficient-sensitive critical-point and asymptotic-value results. A small
feasible witness is also not a short certificate that a proposed feasible
point is globally optimal.

The established feasible-point corollary is useful for exact validation,
small-radius reductions, and bounded-integer MINLP certificates. It gives
no deterministic polynomial-time method for nonconvex feasibility, which
is already NP-hard with one concave quadratic inequality on a box. Its
practical value would require methods for finding a successful face or
producing manageable algebraic witnesses; the existence proof does not
provide those methods.

## Review and verification record

The audit author discovered the minimum-face argument while searching for
prior results. The root agent and an independent subauditor reconstructed
it separately, including unboundedness, lineality, zero-dimensional faces,
the common-field output, and the failure of the naive objective extension.
This is independent mathematical review, not a formal proof.

Primary sources were read from the local literature collection and the
open links above. Searches included fixed numbers of quadratic constraints
with arbitrary affine rows, NP membership of QCQP, quadratic-map sampling,
algebraic degree, multihomogeneous height bounds, and recent infimum
results. Search results were used to locate primary texts; unsuccessful
searches were not treated as novelty evidence.

Targeted command actually run: an inline `python` document check over this
note and `nonconvex-prior-sources/README.md`. It checked final newlines,
trailing whitespace, control characters, and relative Markdown links:
two documents and two local links passed. No project-wide checks or CI
status were consulted. No numerical experiment is needed for the
topological face argument; computations on examples would not establish
it.
