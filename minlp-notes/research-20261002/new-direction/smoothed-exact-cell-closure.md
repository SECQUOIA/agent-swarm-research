# Exact expected work from algebraic closure of smoothed cells

Date: 2026-10-02. Status: complete derivation with targeted exact checks and
a [fresh independent review](../reviews/smoothed-exact-cell-closure-review.md).
No publication-priority claim is made.

The direct expected-cell bound can be made exact under one fixed rational
perturbation law. The extra operation is to recognize cells on which the
convex-QP value function has one quadratic formula, and solve those cells
exactly. An unresolved cell forces the perturbation close to one of finitely
many fixed hyperplanes. A same-draw exact fallback covers all such events,
including atoms, without resampling or a growth assumption.

## 1. Model and conclusion

Let \(X=\{x\in\mathbb R^n:Mx\le d\}\) be a nonempty bounded
rational polytope with \(m\) input inequalities. Let

\[
 F(x)=\tfrac12x^TAx+b^Tx+c,
 \qquad P=A+\alpha T^TT\succeq0,
 \qquad T\in\mathbb Q^{k\times n},\quad \alpha>0,
\]

where all data are rational. Assume \(n,k\ge1\),
\(\|T\|_2\le1\), and

\[
 \ker P\subseteq\ker T.                                      \tag{1}
\]

The [rational negative-space normalization](spectral-normalization.md)
provides these conditions with \(k=n_-(A)\),
\(2\nu\le\alpha<4\nu\), where
\(\nu=\max\{0,-\lambda_{\min}(A)\}>0\). Its residual is positive
definite on \(\operatorname{range}(A)\), with kernel \(\ker A\),
and \(T\) vanishes on that kernel. The convex case needs only one
exact convex-QP solve.

Fix a rational \(\sigma>0\). Section 5 chooses a power of two
\(N\), using only this base input, with polynomially many binary
digits. Sample \(\xi_1,\ldots,\xi_k\) independently and uniformly
from the same fixed grid

\[
 \left\{-\sigma+\frac{2\sigma j}{N-1}:
                  j=0,\ldots,N-1\right\}.                      \tag{2}
\]

The algorithm returns an exact rational optimizer and value of
\(F_\xi(x)=F(x)+\xi^TTx\) for **every draw**. It uses the same draw
in its cell search and its exact fallback. Let
\(\ell_i=\min_X(Tx)_i\), \(u_i=\max_X(Tx)_i\), and

\[
 w_i=u_i-\ell_i+2\sigma/\alpha,
 \qquad
 H_{\rm grid}=\prod_{i=1}^k
 \left[3+\frac{(1+2k)\alpha w_i}{2\sigma}\right].          \tag{3}
\]

If \(I\) is the base rational input length, its expected bit work is
at most

\[
 C^k(1+H_{\rm grid})(I+1)^C                              \tag{4}
\]

for an absolute constant \(C\), enlarged if necessary. Thus it is
expected polynomial time at every fixed \(k\) when the displayed
numerical ratios are polynomially bounded. With normalized negative
inertia this also has the form

\[
 f\left(k,1+\frac{\nu\operatorname{diam}(X)}{\sigma}\right)
 (I+1)^C.                                                   \tag{5}
\]

This is noise aligned with the supplied factor: the original coefficient
perturbation is \(T^T\xi\), generally correlated and of low-dimensional
support. No claim about independent noise in all original coefficients is
made. The target is the sampled objective, not the unperturbed optimum.
The theorem has no restriction to one or two negative directions.

## 2. Smooth recourse and polynomial extraction of a quadratic piece

Define on all of \(\mathbb R^k\)

\[
 W(a)=\min_{x\in X}
 \left[F(x)+\tfrac\alpha2\|a-Tx\|^2\right].                 \tag{6}
\]

Its inner problem has Hessian \(P\) and linear coefficient
\(b-\alpha T^Ta\). If two inner optimizers differ by \(v\), convex
quadratic equality gives \(Pv=0\). By (1), \(Tv=0\). Consequently
all inner optimizers have the same image \(Tx\), and the envelope is
continuously differentiable, with

\[
 \nabla W(a)=\alpha(a-Tx(a)).                               \tag{7}
\]

For example, continuity follows by taking convergent subsequences of
optimizers in the compact set \(X\), and uniqueness of their images;
the derivative follows from the upper and lower comparison inequalities
for the attained minimum in (6). Also
\(W(a)-\alpha\|a\|^2/2\) is concave, so its full quadratic upper
model has curvature \(\alpha\).

At any rational query \(a\), the following polynomial-time procedure
returns a quadratic polynomial \(q_J\) and a closed rational polyhedron
\(R_J\) containing \(a\), such that \(W=q_J\) on \(R_J\).
All possible formulas and regions depend only on the base data.

First obtain an exact convex-QP optimizer \(x_0\), and put
\(g_0=Px_0+b-\alpha T^Ta\). Its complete optimal set is the polytope

\[
 X\cap\{x:P(x-x_0)=0,\quad g_0^T(x-x_0)=0\}.              \tag{8}
\]

Indeed, convex optimality gives \(g_0^T(x-x_0)\ge0\) on \(X\),
and the objective difference is this quantity plus the nonnegative
quadratic term. Choose a vertex \(x\) of (8), using rational linear
programming. This is polynomial even when the polytope is lower-dimensional;
lexicographically optimizing all coordinates is one possible construction.

The restriction of \(P\) to the tangent space of the original active
face at \(x\) is positive definite. Otherwise a nonzero null tangent
\(v\) permits both small displacements \(x\pm tv\) within that face.
First-order optimality annihilates \(v\), so both displacements remain
in (8), contradicting that \(x\) is a vertex of (8).

Find nonnegative multipliers on the active original rows, representing
\(-Px-b+\alpha T^Ta\) as their conic combination. Such multipliers
exist by the normal-cone formula for a polyhedron, including a
lower-dimensional one. Rational linear feasibility finds them. Eliminate
dependence among rows in their positive support, preserving nonnegative
coefficients, until that support is independent. Extend it by additional
active rows to a basis \(J\) of the full active row space, giving each
added row zero multiplier. All these steps take polynomial rational work.

Write \(r=|J|\le n\). The matrix

\[
 K_J=\begin{pmatrix}P&M_J^T\\M_J&0\end{pmatrix}             \tag{9}
\]

is nonsingular, because its constraint rows are independent and \(P\)
is positive definite on their common kernel. For a variable \(z\in
\mathbb R^k\), solve the affine system

\[
 K_J\binom{x_J(z)}{\lambda_J(z)}
 =\binom{-b+\alpha T^Tz}{d_J}.                             \tag{10}
\]

Define

\[
 R_J=\{z:Mx_J(z)\le d,\quad\lambda_J(z)\ge0\}.             \tag{11}
\]

At the queried point, (10) reproduces \(x\) and its nonnegative
multipliers, so the point belongs to \(R_J\). Throughout this region,
convex KKT sufficiency makes \(x_J(z)\) an exact inner optimizer.
Substitution into (6) gives a quadratic \(q_J\), and differentiation
of (10) gives

\[
 q_J(z)=\tfrac12z^TH_Jz+p_J^Tz+e_J,
 \qquad H_Jz+p_J=\alpha(z-Tx_J(z)).                        \tag{12}
\]

This gradient agrees with \(\nabla W\) throughout \(R_J\), even
when that region has empty interior. Its formula is obtained algebraically,
not by differentiating only along the region.

There are at most \(2^m\) possible row subsets \(J\). Each region
has at most \(m+n\) defining inequalities. Empty regions are harmless;
zero defining rows can be ignored. No enumeration of these regions is
required by the search. Redundant input rows and multiplier lineality do
not affect the nonsingular basis selected above.

## 3. A base-only bound on piece curvature

Choose a positive integer \(D\) clearing the denominators of all entries
in \(P,M,b,d,\alpha T^T\). Let \(C_0\ge1\) bound the absolute
values of the resulting integral entries, and set

\[
 U=(2n)!C_0^{2n},\qquad H_0=\alpha(1+nkU).                 \tag{13}
\]

Both are computable and have polynomial encoding length. Cramer's rule
on (10), after multiplying both sides by \(D\), shows that every
constant or linear coefficient of \(x_J(z)\) has magnitude at most
\(U\): its denominator is a nonzero integer determinant, and its
numerator is a determinant of order at most \(2n\), with entries
bounded by \(C_0\). Thus (12) and \(\|T\|_2\le1\) give

\[
 \|H_J\|_2\le H_0                                        \tag{14}
\]

for every possible nonsingular basis, whether or not its critical region
is full-dimensional. Large \(H_0\) affects only the number of stages
and sampling bits through its logarithm. It is not a numerical multiplier
in (4).

## 4. Exact closure of a cell

Use the fixed auxiliary box

\[
 A_{\rm aux}=\prod_i[\ell_i-\sigma/\alpha,
                          u_i+\sigma/\alpha].             \tag{15}
\]

Completing the square shows that the global minimum on this box of
\(V_\xi(a)=W(a)+\xi^Ta\) equals its minimum on all of
\(\mathbb R^k\), and equals
\(\min_XF_\xi-\|\xi\|^2/(2\alpha)\). Every auxiliary evaluation
has an attaining original feasible witness, as in the
[smoothed cell theorem](smoothed-semiconcave-cells.md).

Use exactly its nested equal subdivisions: \(s=\max_iw_i\),
\(h_j=s2^{-j}\), and coordinate interval sizes
\(h_{ij}=w_i/m_{ij}\le h_j\), with \(m_{ij}\) the least sufficient
power of two. The common cell correction is

\[
 B_j=\frac\alpha8\sum_i h_{ij}^2\le\frac{k\alpha h_j^2}8.
                                                               \tag{16}
\]

At every processed cell, evaluate its corners and extract their regions
(11). If any extracted region contains the entire cell, then
\(V_\xi=q_J+\xi^Ta\) everywhere on that cell. Containment is checked
by linear inequalities at its corners. Exactly minimize this quadratic
on the cell, update the incumbent, and mark the cell closed.

This exact box solve needs at most \(3^k\) face choices. For each face,
fix the corresponding coordinates to endpoints and solve the free
stationarity equations when the restricted Hessian is nonsingular;
include vertices as zero-dimensional faces and keep feasible solutions.
A global minimizer on a smallest-dimensional box face has positive definite
restricted Hessian, unless the face is a vertex: a null direction would
reach a lower-dimensional face at the same value. Therefore one of these
candidates is globally optimal on the cell. No definiteness test is
needed to retain the other feasible candidates. Their rational arithmetic
has polynomial bit complexity per face.

For an unresolved cell use the ordinary lower bound
\(L(C)=\min_{v\text{ corner}}V_\xi(v)-B_j\). After all cells at that
level update the incumbent \(U_j\), retain the unresolved cells with
\(L(C)\le U_j\). A closed cell has its exact local minimum recorded;
a discarded cell has a valid lower bound above the incumbent. Subdivide
only the retained unresolved cells. If none remain, the incumbent is an
exact global optimum. This stopping test is sound for every draw.

The usual invariant persists. If an optimal cell was closed, the incumbent
is already exact. Otherwise an optimal cell is processed at the current
level, and its corners give \(U_j-\min V_\xi\le B_j\). Each retained
unresolved cell has a corner \(v\) with

\[
 V_\xi(v)-\min V_\xi\le2B_j.                             \tag{17}
\]

Closure only reduces the ordinary survivor count. Its extra corner basis
extraction and \(3^k\) exact face solves have polynomial bit cost times
this dimension factor.

## 5. Fixed hyperplanes control the exceptional draws

For any \(v\in\mathbb R^k\), the full quadratic upper model and the
trial point \(v-\nabla V_\xi(v)/\alpha\) imply

\[
 \|\nabla V_\xi(v)\|^2
 \le2\alpha[V_\xi(v)-\min_{\mathbb R^k}V_\xi].             \tag{18}
\]

The analysis trial point need not belong to (15); the global minima over
the box and the whole space agree. For the corner in (17), this gives
\(\|H_Jv+p_J+\xi\|\le\alpha\sqrt{k/2}\,h_j\).

Extracted \(R_J\) does not contain this cell, or the algorithm would
have closed it. If \(H_J\) is nonsingular, a nonzero defining row of
(11) is violated somewhere in the cell. Its boundary hyperplane lies
within distance \(\sqrt{k}h_j\) of \(v\). Its image under the
invertible affine map \(z\mapsto-H_Jz-p_J\) is a fixed affine
hyperplane. By (14) and (18), \(\xi\) lies within distance

\[
 \eta_j=\sqrt{k}(\alpha+H_0)h_j                           \tag{19}
\]

of that image. If \(H_J\) is singular, its full affine gradient image
\(-p_J+\operatorname{range}(H_J)\) lies in some fixed affine
hyperplane, and (18) gives the same conclusion without a defining row.
This also covers lower-dimensional critical regions. No irredundant
facet representation is needed.

There are at most

\[
 K=2^m(m+n+1)                                             \tag{20}
\]

hyperplanes needed for this argument. They are determined by the base
problem, independently of the random draw and the mesh. They are proof
devices and need not be constructed or enumerated.

For a fixed affine hyperplane, choose a unit normal and a coordinate whose
normal component has magnitude at least \(1/\sqrt{k}\). Conditional
on the other noise coordinates, membership in its Euclidean
\(\eta\)-neighborhood restricts that coordinate to an interval of
length at most \(2\sqrt{k}\eta\). Under (2), its probability is at
most \(\sqrt{k}\eta/\sigma+1/N\). Hence

\[
 \Pr\{\text{a retained unresolved cell exists at level }j\}
 \le K\left[\frac{k(\alpha+H_0)h_j}{\sigma}+\frac1N\right].
                                                               \tag{21}
\]

Let \(B=\max\{2,2^m\}\). Choose the least integer \(J\ge0\)
with

\[
 s2^{-J}\le\frac{\sigma}{2kKB(\alpha+H_0)},               \tag{22}
\]

then choose the least power of two \(N\) with

\[
 N\ge\max\{2,2^J,2KB\}.                                 \tag{23}
\]

These choices are made **before sampling**, depend only on the base
input, and have \(J+\log_2N=\operatorname{poly}(I)\). Equation
(21) bounds the probability of reaching level \(J\) with unresolved
retained cells by \(1/B\). All atomic events, including exact flatness,
are included in its \(K/N\) term.

## 6. Same-draw fallback and expected bit work

Run the cell algorithm through level \(J\). If unresolved retained
cells remain, run the deterministic exact original-QP fallback on the
**same** \(F_\xi\). The fallback enumerates independent active-row
subsets, solves nonsingular stationary KKT systems, and selects the least
feasible value. As proved in
[the earlier expected exact theorem](expected-smoothed-qp.md), it is always
correct and costs at most \(B\operatorname{poly}(L)\), where \(L\)
is the perturbed input length. It handles ties, flat optimal faces, and
lower-dimensional feasible sets. Its cost does not require a growth bound.

By (23), \(N\ge m_{iJ}\) for every coordinate. The finite-noise
direct counting lemma therefore bounds the expected near-optimal node
count at every level through \(J\) by \(H_{\rm grid}\). An unresolved
retained cell still has the corner (17), so its expected count is at most
\(2^kH_{\rm grid}\). At most \(2^k\) children per survivor are
processed next, with \(2^k\) corner queries and at most \(3^k\)
exact face candidates per processed cell. Thus the expected work before
the fallback obeys (4), including polynomial factors for the \(J+1\)
levels and rational operations.

All corner coordinates have polynomial bit length in \(I+J\). The
noise has \(O(k\log N)\) bits. Exact convex-QP solves, the optimal-face
LP (8), multiplier extraction, and linear algebra consequently have
polynomial bit cost with an absolute exponent. Extracted formulas are
obtained from base KKT matrices, and the local quadratic box problems have
rational data of the same polynomial length. There is no growth of
unrelated denominators across oracle calls.

The fallback contributes expected work at most
\((1/B)B\operatorname{poly}(L)=\operatorname{poly}(I)\).
This proves (4). From \(\|T\|_2\le1\),
\(w_i\le\operatorname{diam}(X)+2\sigma/\alpha\), and normalized
\(\alpha<4\nu\), equation (5) follows.

If the cell search finishes first, take the inner witness corresponding
to its least exact auxiliary value. The square-completion identity gives
an original feasible point with objective no larger than that value plus
\(\|\xi\|^2/(2\alpha)\), which is the original global minimum.
It is therefore an exact rational optimizer. Otherwise use the fallback's
exact rational optimizer. No rational-value isolation threshold or
noise-dependent final mesh is needed.

The potentially large determinant and region counts only determine the
fixed sampling precision and the polynomial number of stages. They do
not multiply the expected cell count. This is why the construction avoids
the accuracy/noise-precision circle and extends beyond the inverse-growth
moment argument restricted to at most two negative directions.

The fallback is needed even after algebraic closure. For example, take
\(X=[0,1]^2\), \(T=(1/2,-1/2)\), \(\alpha=4\),
\(F(x,y)=xy-(x-y)/2\), and \(\sigma=1\). Then \(P=I\).
The endpoint draw \(\xi=1\), present in every grid (2), gives the
target objective \(xy\). Its tilted envelope is constant on
\([-3/4,1/4]\). Two adjacent inner critical regions meet at
\(a=-1/4\), while the fixed auxiliary box is \([-3/4,3/4]\).
The switch has relative position \(1/3\) and never lies on its equal
dyadic meshes. A cell crossing this switch can remain unresolved at every
level, despite its constant objective, because neither extracted region
contains the whole cell. This draw lies on the exceptional hyperplane
\(\xi=1\); its probability is \(1/N\), and the same-draw fallback
solves it exactly. The argument does not assume away such atoms.

## Verification status and limits

The parent researcher independently read the complete derivation and found
no substantive gap in the extraction, curvature bound, hyperplane event,
fixed sampling precision, or expected bit count. The
[fresh adversarial review](../reviews/smoothed-exact-cell-closure-review.md)
also found no substantive gap, including under redundant constraints,
singular residual Hessians, and lower-dimensional critical regions.

The delegated command
`python research-20261002/new-direction/check_smoothed_cell_closure.py`
passed thirteen exact-rational cases over 45 levels and 629 processed
cells. The [diagnostic](check_smoothed_cell_closure.py) recorded 168 exact
closures, 365 ordinary prunes, 96 retained unresolved cells, eight cases
solved by closure, and five same-draw fallbacks. It checked 86 nonsingular
facet-image implications, ten singular-gradient-image implications, 110
active-basis formulas, and 974 query-region and gradient identities.
Fixtures include three negative directions with both axis-aligned and
coupled Hessians, private flat variables, redundant rows, a
lower-dimensional original domain, singular piece Hessians, and a
zero-dimensional critical region.

The independent reviewer ran
`python research-20261002/new-direction/check_exact_cell_closure_review.py`.
That [second diagnostic](check_exact_cell_closure_review.py) passed four
fixtures, with 208 corner queries, 34 exact closures, and 52 retained
unresolved cells. It checked coefficient and curvature bounds, piece
agreement and gradients, cell minima, the incumbent invariant, and the
exceptional hyperplane tubes. It also checked the literal endpoint-atom
example above and showed that dropping (1) can make the envelope
nondifferentiable. This diagnostic enumerates small KKT bases to provide
an independent reference; it is not the proposed polynomial extraction
procedure.

The first checker uses explicit clipped recourse formulas and rational KKT
identities, not the production convex-QP or LP algorithms. Independent
original-box vertex enumeration supplies its reference minima and fallback;
separate concavity makes that enumeration exact on these fixtures. Its
fallback tests use deliberately small stage caps, including one zero cap,
not the potentially much larger theoretical cutoff (22). The tests check
algorithmic invariants and exact outputs, not the expectation theorem by
sampling. A separate inline `python - <<'PY'` check verified twelve levels
of the persistent endpoint-atom example above. Scoped whitespace,
mathematical-delimiter, and local-link checks passed.

The proof uses the existing exact polynomial-time convex-QP theorem and
standard rational LP, not uncertified numerical oracle output. A practical
implementation may use certified numerical methods, but no such numerical
complexity theorem is asserted here.

The finite law (2), with (22)--(23), is essential to this claim. An arbitrary
coarse atomic law can give much larger expected work. The exceptional draws
are never discarded or resampled. Algebraic closure and the fallback remain
valid on them; only the expectation analysis invokes the perturbation law.
No project-wide checks or CI inspection were performed for this note.

## Prior-art boundary and related results

The [focused literature audit](../prior-art/smoothed-cell-closure-prior.md)
identifies Ding's earlier reduction of nonconvex QP to a piecewise-quadratic
parametric convex-QP value function. Convex critical regions, affine
optimizer formulas, and region traversal are also established machinery.
The proposed contribution here is the expected exact bit-work analysis:
the retained-cell count, exceptional-hyperplane argument, fixed finite
sampling law, and exact fallback on the same draw. The search does not
establish priority, and the audit records primary-text access limits.

The separately reviewed [ambient extension](smoothed-ambient-cell-closure.md)
uses independent noise on all original coefficients. Its dependence on the
ambient dimension is weaker than the fixed-parameter bound proved here.
