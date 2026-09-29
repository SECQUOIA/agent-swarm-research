# Independent review of the copositive-to-box star obstruction

Reviewed on 2026-09-25. The transfer is valid. It disproves universal
exactness of full lifted PSD plus all McCormick/RLT inequalities for
star-supported box quadratics. It is an elementary consequence of an
existing copositive example; no substantial novelty claim is made.

## General transfer, with the missing hypotheses made explicit

Let \(A\in\mathbb S^{n+1}\) be copositive but not a sum of a PSD matrix
and an entrywise nonnegative matrix. Select any index and call it \(0\).
There exists a finite \(U>0\) such that the quadratic

\[
 f(z)=[1;z]^TA[1;z],\qquad z\in[0,U]^n,
\]

has a strict gap in its full PSD plus full RLT relaxation. In particular,
the relaxation is not exact for the interaction graph obtained by
deleting vertex \(0\) from the off-diagonal support graph of \(A\).

To justify separation, the cone
\(\mathcal S_+^{n+1}+\mathcal N^{n+1}\) is closed. Indeed, if
\(A_k=P_k+N_k\to A\), with \(P_k\succeq0\) and \(N_k\ge0\), then
\(0\le(P_k)_{ii}\le(A_k)_{ii}\). PSD bounds the off-diagonal entries
of \(P_k\) by its diagonal entries, so \(P_k\) is bounded. A
convergent subsequence gives a limiting decomposition of the same type.
Finite-dimensional conic separation and self-duality of the two cones
therefore yield

\[
Y\succeq0,\qquad Y\ge0,\qquad A\mathbin\bullet Y<0.
\]

Replace \(Y\), **not \(A\)**, by
\(Y+\varepsilon(I+\mathbf1\mathbf1^T)\), for sufficiently small
\(\varepsilon>0\). This preserves the strict negative objective and
makes \(Y\) positive definite with every entry strictly positive.
Divide by \(Y_{00}>0\), and write the result as

\[
Y=\begin{pmatrix}1&m^T\\m&M\end{pmatrix}.
\]

Every \(m_i\) is now positive. One sufficient common bound is any
\(U\) satisfying

\[
U\ge2\max_i m_i,
\qquad
U\ge\max_{1\le i,j\le n}\frac{M_{ij}}{\min(m_i,m_j)}.
\]

These inequalities give \(0\le m_i\le U\) and, for every pair
including diagonals,

\[
0\le M_{ij}\le U m_i,\quad M_{ij}\le U m_j,\quad
M_{ij}\ge U(m_i+m_j)-U^2.
\]

The last inequality follows because its right side is nonpositive.
Thus \((m,M)\) is feasible for the full box moment relaxation. Its
linearized objective is \(A\mathbin\bullet Y<0\), whereas
copositivity gives \(f(z)\ge0\) for every feasible \(z\). This proves
a strict gap. Existence of a zero with first coordinate one is useful
for identifying the true minimum, but is unnecessary for the gap.

The change of variables \(z=Uw\) maps the example to the unit box.
Explicitly, put \(D=\operatorname{Diag}(1,U,\ldots,U)\). The new
objective matrix and feasible moment matrix are

\[
A'=DAD,\qquad Y'=D^{-1}YD^{-1}.
\]

Their trace pairing is unchanged. Positive diagonal entries and all
off-diagonal zero patterns are preserved. If \(A\) is rational, a
rational witness exists: after the strict perturbation there is an open
neighborhood of feasible negative witnesses, so rational approximation
preserves all strict conditions. Normalization and an integer \(U\)
then preserve rationality. This is an existence statement, not a bound
on encoding length.

## Application and limits

[Drury (2020), “The triangle graph T6 is not SPN”](https://emis.de/ft/34748)
gives a copositive, non-SPN matrix with unit diagonal and support on two
adjacent hubs, each adjacent to four otherwise independent leaves.
Its parameter satisfies \(0<\theta<\pi/6\); both
\((\cos\theta,\sin\theta)=(12/13,5/13)\) and
\((24/25,7/25)\) satisfy this condition. Deleting either hub leaves
the five-variable star \(K_{1,4}\). The paper's zero
\((1,2\cos\theta,1,0,0,0)\) also confirms that, after fixing its
first hub coordinate to one, the true minimum is zero for a sufficiently
large box. Its non-SPN result predates the present investigation.

Applying the transfer proves a five-variable star gap with strictly
positive square coefficients. Because every star is a tree, complementing
selected leaves on the unit box can make every edge coefficient
nonpositive. Full PSD and full RLT are invariant under coordinate
complementation. Hence a submodular star example exists as well, with
the positive square coefficients retained.

Several stronger conclusions do **not** follow:

- This does not prove five variables is the smallest star counterexample.
  In particular, the fact that the five-vertex book graph is SPN would
  only block this orthant-based construction for a four-variable star.
- This does not obstruct arbitrary semidefinite extensions, additional
  nonlinear constraints, or higher moments.
- This does not rule out efficient exact star optimization by eliminating
  leaves and solving the resulting univariate problem.
- This construction concerns the ordinary full PSD plus RLT relaxation.
  It does not by itself defeat an arbitrary fixed family of further
  valid cuts.
- Existence of a strict gap does not supply a useful uniform lower bound
  after coefficient normalization. Large box scaling may make the
  normalized gap small.

The useful conclusion is narrow and clear: graph acyclicity and positive
diagonal curvature do not suffice for this relaxation's exactness, even
on a star. The transfer is a standard conic-separation argument coupled
with finite box scaling, so novelty would need to lie in a stronger
consequence or a genuinely new structural characterization.

[Qiu–Yıldırım (2024), “On exact and inexact RLT and SDP-RLT relaxations
of quadratic programs with box constraints”](https://link.springer.com/article/10.1007/s10898-024-01407-y)
provides general algebraic exactness characterizations. Its Lemma 19 and
Proposition 20 imply, by specialization at the origin, that a homogeneous
copositive quadratic has an exact unit-box SDP-RLT relaxation precisely
when its matrix is SPN. This is a consequence of their characterization,
not the wording of a separately stated theorem. An independent literature
review found no explicit star specialization there. The present transfer
therefore should not be represented as a new general link between
copositivity and box-relaxation gaps.

## Independent audit of the explicit five-variable instance

The construction is recorded in
[star-hull-proof-exploration.md](star-hull-proof-exploration.md). No
mathematical defect was found. The independent command

```text
python research-20260925/check_star_independent_review.py
```

passed. It reads only the literal matrix data from the construction's
check file, then uses separate SymPy calculations rather than its
determinant or polynomial routines. The audit established:

- All 63 principal minors of the six-dimensional integer matrix are
  positive. This independently verifies positive definiteness.
- All box bounds and all RLT inequalities hold strictly, with smallest
  listed RLT slack \(1/250000\).
- The exact relaxed objective is \(-9337/250000\).
- Differentiating the polynomial independently produces the four clipped
  affine leaf minimizers. Their upper bounds are inactive throughout
  \(0\le t\le4\). Their zero crossings partition the interval exactly
  as stated in the construction.
- Direct substitution independently produces all five stated reduced
  quadratics. Their exact interval minima are
  \(0,0,9018009/390625,0,83521/625\), respectively. The exhibited feasible
  zero proves the true minimum is zero.
- Direct symbolic substitution gives exactly the displayed submodular
  unit-box polynomial.

These checks were accompanied by a manual sign review of the five
pieces: two are squares, the middle concave quadratic has its roots
outside its interval, and the first and last pieces have the stated
nonnegative signs. Thus the nonnegativity argument does not depend on
numerical optimization or on accepting the external copositivity proof.

One further exact property follows from the objective matrix: its leaf
block is \(625I_4\), and the scalar Schur complement of that block is
\(-668354/625\). By inertia under congruence, the quadratic matrix has
four positive eigenvalues and exactly one negative eigenvalue. The
unit-box scaling and leaf complements preserve that inertia. This is a
property of the example, not a complexity conclusion.

## Connected-graph corollary audit

Combining the five-variable star example with the existing four-variable
path example rules out universal SDP-RLT exactness on every connected
interaction graph having at least five vertices, even within submodular
quadratics with positive diagonal coefficients.

The graph argument only requires a spanning tree. If its diameter is at
least three, it contains a four-vertex path. Otherwise it is a star,
whose at least four leaves contain \(K_{1,4}\). The subgraph need not be
induced.

To extend either base example, append deterministic zero coordinates to
its feasible moment matrix and add positive squares on the additional
variables. This preserves every full PSD and RLT constraint, the true
minimum zero, and a negative feasible relaxation value \(-g\).

If the objective must have exactly a prescribed graph as its support,
add \(-\delta z_i z_j\) for each of the \(r\) missing required edges.
On the unit box, the new true minimum is at least \(-\delta r\).
The old feasible moment matrix has objective at most \(-g\), because
all its cross moments are nonnegative. For \(r>0\), choosing
\(0<\delta<g/r\) preserves the strict gap; \(r=0\) needs no
perturbation. All new edges are submodular and all diagonal coefficients
remain positive. No conclusion about the four-variable star follows.

## Review record

The proof above was checked independently of the numerical witness
construction. The closedness, strict perturbation, common upper bound,
unit-box scaling, and support preservation were each checked explicitly.
A separate reviewer also found the transfer sound and examined the
Qiu–Yıldırım comparison through a further fresh literature reviewer.
Failure to find the specific star statement in that search does not
establish novelty.

The explicit rational instance and connected-graph corollary passed the
independent audit described above. These checks do not certify novelty,
quantitative solver impact, or any unclaimed extension to arbitrary
additional cuts. No project-wide verification or CI inspection was run.
