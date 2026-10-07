# Exact smoothed optimization with separable mixed recourse

Date: 2026-10-02. Status: complete argument that passed
[fresh independent review](../reviews/smoothed-mixed-separable-closure-review.md)
and a [second review](../reviews/smoothed-mixed-separable-review.md), with
targeted exact checks. No publication-priority claim is made.

The cell-closure method extends to mixed product boxes with arbitrarily
many integer coordinates when convex recourse separates. Neighbor
inequalities certify integer winners without enumerating integer labels.
The value function may be nonsmooth: every optimal witness supplies the
global quadratic upper model required by the proof.

## 1. Model and conclusions

Let \(X=\prod_iX_i\), where each coordinate is a compact rational
interval or its intersection with the integers. Round integer endpoints
inward, reject empty domains, and remove fixed coordinates. Each
\(\phi_i\) is a continuous convex univariate function given by an explicit
finite list of quadratic pieces with rational coefficients and rational
breakpoints, covering the entire coordinate interval. Zero curvature is allowed.
Consider

\[
 F(x)=\sum_{i=1}^n\phi_i(x_i)-\frac\alpha2\|Tx\|^2,
 \qquad \alpha>0,\quad T\in\mathbb Q^{k\times n}.           \tag{1}
\]

The total bit length \(I\) includes all pieces, rational breakpoints,
binary endpoints, and a
positive rational noise scale \(\sigma\). The case \(k=0\) separates
and is solved directly. Below \(k\ge1\).

Under the base-chosen finite aligned law in section 5, the algorithm returns
an exact optimizer of \(F(x)+d^TTx\) for every draw, with expected bit work

\[
 C^k(1+H_{\rm aligned})(I+1)^C,\qquad
 H_{\rm aligned}=\prod_{j=1}^k
 \left[3+\frac{(1+2k)\alpha w_j}{2\sigma}\right],           \tag{2}
\]

where \(w_j=\operatorname{range}_X(Tx)_j+2\sigma/\alpha\).
The number of integer coordinates is not a parameter. This is FPT in
\(k\) and a bound on \(\alpha w_j/\sigma\). No uniqueness or
quadratic-growth assumption is imposed.

With full-row-rank \(T\), \(\|T\|\le1\), and the different finite law
in section 6, independent noise in every original coefficient also gives
exact output on every draw and expected polynomial work at fixed \(k\)
under the displayed numerical bounds. The current ambient bound has
powers of \(n\) depending on \(k\), so it does not establish FPT.

These statements cover product domains and a supplied separable residual.
They do not cover arbitrary coupling constraints or a general dense convex
residual. The target is the sampled objective.

## 2. Scalar recourse supplies global polyhedral regions

Write \(t_i\) for column \(i\) of \(T\). With an arbitrary residual linear
coefficient \(r\), recourse separates:

\[
 \begin{aligned}
 W_r(a)&=\min_{x\in X}
 \left[F(x)+r^Tx+\frac\alpha2\|a-Tx\|^2\right]\\
 &=\frac\alpha2\|a\|^2+
 \sum_i\min_{x_i\in X_i}[\phi_i(x_i)-\lambda_i x_i],
 \qquad \lambda_i=\alpha t_i^Ta-r_i.                     \tag{3}
 \end{aligned}
\]

For an integer coordinate, put
\(\Delta_i(z)=\phi_i(z+1)-\phi_i(z)\). Convexity makes these forward
differences nondecreasing. A feasible integer \(z\) is a global minimizer
of its scalar problem exactly when

\[
 \Delta_i(z-1)\le\lambda_i\le\Delta_i(z),                  \tag{4}
\]

omitting a missing neighbor at a domain endpoint. Summing forward
differences proves sufficiency. Binary search for the first forward
difference at least \(\lambda_i\), or selection of the upper endpoint if
none exists, finds a minimizer in \(O(1+\log N_i)\) comparisons, where
\(N_i\) is the number of allowed integers. Listed piece evaluation is
polynomial in the bit lengths. This includes zero curvature and long ties.

For a continuous coordinate with \(s_i\) positive-length listed intervals,
there are at most \(2s_i+1\) scalar states:

- On a piece \(p x^2/2+b x+c\) with \(p>0\), use the affine response
  \(x=(\lambda_i-b)/p\), valid for derivative values between the piece's
  two endpoints.
- At a knot \(v\), use the constant response \(x=v\), valid when
  \(\phi'_{i,-}(v)\le\lambda_i\le\phi'_{i,+}(v)\). At the two domain
  endpoints replace the missing derivative by \(-\infty,+\infty\).

These states cover all parameters. A flat interval requires no free state:
at its slope value a knot is also optimal. Searching the listed states
takes polynomial time. Continuity, nonnegative piece curvature, and ordered
one-sided derivatives are checkable by rational arithmetic.

Select one optimal state in every coordinate at the query. Their at most
two affine inequalities per coordinate define a closed polyhedron
\(R_J(r)\) on which all selected scalar responses remain globally
optimal. Constant integer labels, constant knots, and affine continuous
responses therefore combine into a globally valid recourse formula

\[
 W_r(a)=q_J(a;r)=\tfrac12a^TH_Ja+p_J(r)^Ta+e_J(r)
       \quad(a\in R_J(r)).
                                                               \tag{5}
\]

Let \(\mathcal F_J\) be the free positive-curvature coordinates, with
selected curvatures \(p_{i,J}>0\). Direct substitution gives

\[
 H_J=\alpha I-\alpha^2\sum_{i\in\mathcal F_J}
                       \frac{t_it_i^T}{p_{i,J}},
 \qquad \nabla_a q_J(a;r)=\alpha(a-Tx_J(a,r)).             \tag{6}
\]

The Hessian and region normals are independent of \(r\); region offsets
and \(p_J(r)\) are affine in \(r\). Equation (6) is an algebraic
branch identity, including on a lower-dimensional region. It does not
claim differentiability of the full mixed value function.

## 3. Every active witness gives the required upper model

For any query \(v\) and any optimal full witness \(x_v\), feasibility of
that same witness at every other auxiliary parameter gives

\[
 W_r(v+h)\le W_r(v)+\alpha(v-Tx_v)^Th+\frac\alpha2\|h\|^2.
                                                               \tag{7}
\]

For \(V(a)=W_r(a)+d^Ta\), put \(g_v=\alpha(v-Tx_v)+d\).
Taking \(h=-g_v/\alpha\) yields

\[
 \|g_v\|^2\le2\alpha[V(v)-\min_{\mathbb R^k}V].            \tag{8}
\]

This holds for every optimal witness, including integer ties and continuous
knots. For the extracted branch, \(g_v=H_Jv+p_J(r)+d\). Thus it replaces
the smooth-gradient step in the reviewed closure proof.

Square completion remains valid for the actual mixed feasible set:

\[
 W_r(a)+d^Ta=
 \min_{x\in X}\left[F(x)+(r+T^Td)^Tx+
 \frac\alpha2\|a-Tx+d/\alpha\|^2\right]
 -\frac{\|d\|^2}{2\alpha}.                              \tag{9}
\]

Enlarge each coordinate range of \(TX\) by the support bound for
\(d_j/\alpha\). The resulting fixed box contains all auxiliary global
minima, so its minimum agrees with the whole-space minimum used in (8).
An exact recourse witness transfers auxiliary certificates to feasible
original mixed points without increasing their gap.

## 4. Piece counts, curvature, closure, and fallback

Let \(\mathcal I,\mathcal C\) be the integer and continuous coordinates.
The total number of possible scalar-state combinations is at most

\[
 R=\prod_{i\in\mathcal I}N_i
       \prod_{i\in\mathcal C}(2s_i+1).                   \tag{10}
\]

This is an analysis count, not an oracle enumeration. Its logarithm is
polynomial in \(I\). Let \(r_i^+\) be the largest reciprocal of a positive
piece curvature for continuous coordinate \(i\), or zero if none exists.
Then the base-only rational bound

\[
 H_0=\alpha+\alpha^2\sum_{i\in\mathcal C}r_i^+\|t_i\|^2    \tag{11}
\]

controls \(\|H_J\|\) for every state. Its encoding length is polynomial.
Tiny positive unary curvature affects the cutoff through \(\log H_0\).

At every queried corner extract (5). If a returned region contains the
whole cell, minimize its quadratic plus the auxiliary tilt exactly on the
cell and close it. Containment follows from testing the region inequalities
at all corners. The local solve uses the existing \(3^k\)-face stationary
enumeration, including descent from singular optimal faces.

Unresolved cells use the usual corner lower bound and refinement. A retained
cell has a \(2B_j\)-near-optimal corner. The active-vector estimate (8)
then gives the same fixed-hyperplane obstruction as the
[exact closure theorem](smoothed-exact-cell-closure.md): an invertible
branch Hessian maps a violated region hyperplane to a nearby gradient-image
hyperplane; a singular Hessian has a proper affine gradient image.
At most \(2n\) inequalities define each region, so at most

\[
 K=R(2n+1)                                               \tag{12}
\]

fixed hyperplanes are needed. Their factor-space tube radius is
\(\sqrt{k}(\alpha+H_0)h_j\). Zero defining rows cannot be violated
elsewhere in a cell containing the query. Ties and lower-dimensional
regions require no additional assumption.

An exact fallback enumerates integer assignments and choices of a listed
piece for every continuous coordinate. On each resulting continuous box,
enumerate the faces of its rational quadratic objective and solve
nonsingular free stationarity systems, including vertices. Some optimum
has positive definite restricted Hessian on its smallest optimal face:
otherwise a null direction reaches a smaller optimal face. This finds the
exact optimum, including flat faces and ties, in
\(B\operatorname{poly}(I+L)\) bit work, where \(L\) is the sampled
coefficient bit length and

\[
 B=\max\left\{2,\ \prod_{i\in\mathcal I}N_i
                         \prod_{i\in\mathcal C}3s_i\right\}.
                                                               \tag{13}
\]

Thus \(R\le B\) and \(\log B\) is polynomial in the base input.

## 5. A fixed aligned-noise law

Set \(r=0\), use auxiliary widths \(w_j\) from (2), and put
\(s=\max_jw_j\). Choose the least \(J\ge0\) with

\[
 s2^{-J}\le\frac{\sigma}{2kKB(\alpha+H_0)},
\]

then the least power of two \(M\) satisfying
\[
 M\ge\max\{2,2^J,2KB\}.                                  \tag{14}
\]

Independently sample each \(d_j\) from
\(\{-\sigma+2\sigma q/(M-1):q=0,\ldots,M-1\}\).
Run closure through \(J\), then apply the fallback to the same draw if
unresolved cells remain. All choices precede sampling and
\(J+\log M=\operatorname{poly}(I)\).

The reviewed hyperplane argument bounds fallback probability by \(1/B\).
The finite-noise local counting lemma bounds expected survivors at every
level by \(2^kH_{\rm aligned}\). Scalar recourse, extraction, and closure
have polynomial bit cost per processed cell, with a factor depending only
on \(k\). These facts prove (2), including the fallback's expected cost.
Every draw returns an exact answer; no exceptional draw is rejected.

## 6. Independent ambient noise

For full-row-rank \(T\) with \(\|T\|\le1\), decompose original noise as
\[
 D=(TT^T)^{-1}T,\qquad d=D\gamma,\qquad r=\gamma-T^Td.
\]

The residual term preserves separability. In (3), only the scalar tilt
\(\lambda_i=\alpha t_i^Ta-r_i\) changes. The state count, base-only
Hessian bound, and affine-offset property therefore remain valid.
The [ambient-noise proof](smoothed-ambient-cell-closure.md) applies:
its volume argument uses semiconcavity; its exceptional-tube argument now
uses (8); its scalar-section argument uses the finite critical regions.
Each region still meets an ambient-coordinate line in an interval and
has a quadratic value formula there, including at integer ties.

Use fixed auxiliary half-enlargements
\(\sigma\|D_{j,:}\|_1/\alpha\), resulting widths \(w_j\), and
\[
 H_{\rm ambient}=\prod_j
 \left[2+\frac{(1+2k)\alpha\sqrt n\,w_j}{2\sigma}\right],
 \qquad C_{\rm sec}=[2(2k+1)R+1](8k+2).
\]

Choose \(J\) from
\[
 s2^{-J}\le\frac{\sigma}{2nkKB(\alpha+H_0)}
\]
and the least power of two \(M\) at least
\[
 \max\{2,2KB,2nC_{\rm sec}(J+1)(2^J+1)^k\}.               \tag{15}
\]

Sample every original coefficient independently on the same \(M\)-point
grid in \([-\sigma,\sigma]\). Expected work is
\(C^k(1+H_{\rm ambient})(I+1)^C\), with exact output for every draw.
The width formula records conditioning of the supplied factor. General
QP spectral normalization cannot automatically be substituted here:
it need not preserve separability of the residual.

## 7. Why matching integer corner winners is insufficient in general

Take \(z\in[0,1]\), \(y\in\{0,1\}\), and
\[
 F(z,y)=\tfrac12zy+\tfrac78y^2-\tfrac{15}{16}y,
 \qquad \alpha=1,\quad T=(1,1/2).
\]

The convex recourse Hessian is
\(P=\begin{pmatrix}1&1\\1&2\end{pmatrix}\succ0\).
On \(a\in[0,1]\), slice \(y=0\) has response \(z=a\) and value
\(q_0(a)=0\); slice \(y=1\) has response \(z=0\) and value
\[
 q_1(a)=a^2/2-a/2+1/16.
\]
Thus \(y=0\) is the strict winner at both corners but \(y=1\) wins at
\(a=1/2\). The first slice's continuous formula is valid throughout the
cell, yet it is not the mixed global value there. Rescaling to
\(\alpha=4,T=(1/2,1/4)\), cell \([0,1/2]\), gives the same example with
\(\|T\|<1\).

The separable theorem avoids this obstruction by certifying each scalar
winner throughout the cell via (4) and the continuous derivative thresholds.

## 8. Verification status

The reviews found no substantive gap. The second review passed separate exact
checks of 119 integer state equivalences, 17 continuous piece minima,
and 22 active upper-model inequalities. Additional fresh review identified the
need to state rational breakpoints explicitly, as now done in section 1.
Rational polynomial formulas alone would not suffice: on \([0,2]\),
\(\max\{0,x^2-2\}-x\) has its unique minimum at the irrational knot
\(\sqrt2\).

The targeted command actually run was

    python research-20261002/new-direction/check_mixed_separable_closure.py

It passed ten exact-rational cases, 34 levels, 174 processed cells,
34 exact closures, 93 ordinary prunes, and 47 retained unresolved cells.
Six cases finished by closure; four used the same-draw fallback at the
deliberately small test cutoff. Every returned original optimum matched
independent enumeration of integer labels and continuous piece-face
candidates.

Fixtures include five integer coordinates with rank-two coupling, mixed
quadratics, a flat continuous interval, a continuous curvature change,
kinked integer costs, residual linear tilts, and simultaneous integer and
continuous ties. Checks cover 38 facet-image and nine singular-image
implications, plus 25 different active witnesses at the same tie. A domain
with \(2^{40}+1\) integers was searched in 40 neighbor comparisons without
enumerating its labels.

These checks exercise new scalar recourse, region extraction, mixed witness
reconstruction, and algebraic closure. They do not empirically establish
the expectation bound or implement the proof's very fine sampling law.
The geometry and finite-noise arguments reuse the reviewed auxiliary
theorems.

The fresh reviewer also ran the complementary command

    python research-20261002/reviews/check_mixed_separable_sections.py

It passed 24 ambient-coordinate lines, 204 boundary queries, 228 open
intervals, 780 active branches, 1,560 gradient identities, and 912 quadratic
value identities. These checks independently enumerate scalar candidates
and verify line coverage and agreement of overlapping regions at ties.
Scoped whitespace and local-link checks passed. No external search,
project-wide checks, or CI inspection ran.
