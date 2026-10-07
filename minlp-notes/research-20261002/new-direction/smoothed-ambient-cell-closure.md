# Exact cell closure under independent noise in every original coefficient

Date: 2026-10-02. Status: complete extension that passed
[independent review](../reviews/smoothed-ambient-cell-closure-review.md).
No priority claim is made. This note extends the
[reviewed factor-noise closure theorem](smoothed-exact-cell-closure.md)
using a volume estimate and a finite-grid discrepancy argument. It does
not condition on a residual perturbation and then assume the remaining
factor coefficients stay independent.

## 1. Model and noise decomposition

Use the rational quadratic and bounded rational polytope from the closure
theorem:

\[
 X=\{x\in\mathbb R^n:Mx\le b_X\},\qquad
 F(x)=\tfrac12x^TAx+b^Tx+c,
\]

with \(m\) input inequalities, and supplied rational data

\[
 P=A+\alpha T^TT\succeq0,\quad
 T\in\mathbb Q^{k\times n},\quad
 1\le k\le n,\quad \alpha>0,
\]

such that \(T\) has full row rank,
\(\|T\|_2\le1\), and \(\ker P\subseteq\ker T\).
Write \(I\) for the base rational input length, including a positive
rational noise scale \(\sigma\). The convex case \(k=0\) requires
only a convex-QP solve.

The perturbed objective is now

\[
 F_\gamma(x)=F(x)+\gamma^Tx,
\]

No uniqueness or quadratic-growth assumption is imposed on its optimizer.
Every original coefficient \(\gamma_i\) is independently
uniform on one common rational grid in \([-\sigma,\sigma]\).
The grid size is chosen from the base data in section 6, before sampling,
and is not tied to requested accuracy or rational-value reconstruction.

Define the rational matrices

\[
 D=(TT^T)^{-1}T,\qquad \Pi=I_n-T^TD,
\]

and decompose each draw as

\[
 d=D\gamma,\qquad r=\Pi\gamma,\qquad
 \gamma=T^Td+r,\qquad r\in\ker T.                       \tag{1}
\]

The coordinates of \(d\) generally are dependent, even after
conditioning on \(r\). This dependence is retained in the proof.

Let \(\ell_i=\min_X(Tx)_i\),
\(u_i=\max_X(Tx)_i\), and set

\[
 s_i=\sigma\sum_{j=1}^n|D_{ij}|,\qquad
 A_{\rm aux}=\prod_{i=1}^k
 [\ell_i-s_i/\alpha,\ u_i+s_i/\alpha].                   \tag{2}
\]

These are base-only rational quantities. Put
\(w_i=u_i-\ell_i+2s_i/\alpha>0\) and
\(s=\max_iw_i\). Define

\[
 W_r(a)=\min_{x\in X}
 \left[F(x)+r^Tx+\tfrac\alpha2\|a-Tx\|^2\right],
 \qquad V_\gamma(a)=W_r(a)+d^Ta.                         \tag{3}
\]

The inner problem is a convex QP. The kernel assumption gives a unique
image \(Tx\) across all inner optimizers and hence
\(\nabla W_r(a)=\alpha(a-Tx(a))\). Also
\(W_r(a)-\alpha\|a\|^2/2\) is concave. Completing the square gives

\[
 \min_{a\in A_{\rm aux}}V_\gamma(a)
 =\min_{a\in\mathbb R^k}V_\gamma(a)
 =\min_XF_\gamma-\frac{\|d\|^2}{2\alpha}.               \tag{4}
\]

Each exact inner witness transfers an auxiliary certificate to an original
feasible certificate without increasing its gap, as in the factor-noise
theorem. The domain (2) is fixed before the draw.

## 2. A volume lemma for dependent factor coefficients

For this section alone, let \(\gamma\) be continuously uniform on
\([-\sigma,\sigma]^n\). Choose any rational basis matrix \(V\)
for \(\ker T\), so

\[
 S=[T^T\ V]\quad\hbox{is invertible},\qquad
 \gamma=S(d,\eta),\quad r=V\eta.
\]

No norm bound on this complement is needed.
Fix a subset \(Q\subseteq\{1,\ldots,k\}\), with \(|Q|=t\).
For each \(i\in Q\), let \(I_i(\eta)\) be a measurable interval,
depending arbitrarily on \(\eta\), of length at most \(L_i\).
Then

\[
 \Pr\{d_i\in I_i(\eta)\ (i\in Q)\}
 \le \frac{\prod_{i\in Q}L_i}{(2\sigma)^t}
 \sum_{\substack{K\subseteq\{1,\ldots,n\}\\|K|=t}}
       |\det((T^T)_{K,Q})|                              \tag{5}
\]

and consequently

\[
 \Pr\{d_i\in I_i(\eta)\ (i\in Q)\}
 \le\prod_{i\in Q}\frac{\sqrt n\,L_i}{2\sigma}.         \tag{6}
\]

For \(t=0\), the empty products and determinant sum equal one.

**Proof.** Change coordinates by \(S\), integrate over all coordinates
except \(d_Q\), and bound each remaining fiber by
\(\prod_{i\in Q}L_i\). The integration domain is contained in the
projection of \(S^{-1}[-\sigma,\sigma]^n\) onto those remaining
\(n-t\) coordinates. The volume of this projected parallelotope,
viewed as a zonotope, is

\[
 (2\sigma)^{n-t}
 \sum_{|J|=n-t}|\det((S^{-1})_{Q^c,J})|.
\]

Multiply by the transformed density \(|\det S|/(2\sigma)^n\).
The complementary-minor identity gives

\[
 |\det S|\,|\det((S^{-1})_{Q^c,J})|
 =|\det(S_{J^c,Q})|.
\]

This proves (5): the complement cancels. Cauchy--Schwarz and
Cauchy--Binet bound the determinant sum by

\[
 \sqrt{\binom nt}\sqrt{\det(T_QT_Q^T)}
 \le n^{t/2},
\]

using \(\|T\|_2\le1\). This proves (6). QED.

## 3. Expected local grid counts with continuous ambient noise

Use the fixed nested equal-subdivision grids on (2), with
\(h_j=s2^{-j}\), coordinate subdivisions \(m_{ij}\), and actual
steps \(h_{ij}=w_i/m_{ij}\le h_j\). As before, a refined coordinate
has \(h_j/2<h_{ij}\le h_j\); an unrefined coordinate has only
its two endpoints. Put

\[
 B_j=\frac\alpha8\sum_i h_{ij}^2.
\]

At a deterministic level-\(j\) grid node \(v\), define the local
event \(E_v\) by all neighboring comparisons in interior coordinates:

\[
 V_\gamma(v)\le V_\gamma(v\pm h_{ij}e_i)+2B_j.           \tag{7}
\]

Every globally \(2B_j\)-near-optimal grid node satisfies this event.
For fixed residual \(r\), comparison in coordinate \(i\) restricts
\(d_i\) to an interval depending only on \(r\), of length at most

\[
 \alpha h_{ij}+4B_j/h_{ij}
 \le(1+2k)\alpha h_{ij}.                               \tag{8}
\]

Apply (6) to the interior-coordinate subset, then sum over the full
deterministic grid. The product expansion gives

\[
 \sum_v\Pr_{\rm cont}(E_v)\le H_{\rm amb},\qquad
 H_{\rm amb}=\prod_{i=1}^k
 \left[2+\frac{(1+2k)\alpha\sqrt n\,w_i}{2\sigma}\right].
                                                               \tag{9}
\]

This uses an upper bound on each local event, not independence among the
factor coefficients. The random recourse function \(W_r\) causes no
problem because its value depends on the residual coordinate \(\eta\)
alone.

## 4. Exact closure and fixed ambient exceptional hyperplanes

The exact piece extraction and cell-closure algorithm are unchanged from
the factor-noise theorem, applied to the base linear coefficient \(b+r\).
For every nonsingular active basis \(J\), the inner optimizer has form

\[
 x_J(a,r)=X_Ja+Y_Jr+z_J.
\]

There are at most \(R=2^m\) such bases. Their critical regions are
given by at most \(m+n\) inequalities, affine jointly in \((a,r)\).
The quadratic-piece gradient is

\[
 \nabla W_r(a)=H_Ja+p_J(r),
\]

where \(H_J=\alpha(I-TX_J)\) is independent of \(r\) and
\(p_J(r)\) is affine in \(r\).

A base-only bound \(\|H_J\|_2\le H_0\) is obtained by Cramer's
rule using only \(P,M,\alpha T^T\): these determine the matrix
and the right-hand-side coefficients for the response to \(a\).
Explicitly, choose a positive denominator \(D_0\) clearing these
entries, let \(C\ge1\) bound their scaled integer magnitudes, and put

\[
 U=(2n)!C^{2n},\qquad H_0=\alpha(1+nkU).
\]

Every coefficient of \(X_J\) has magnitude at most \(U\), by
Cramer's rule on a nonsingular integral KKT system of order at most
\(2n\). The perturbed linear coefficient affects only the constant
part of the KKT right-hand side. Do not include its sampled denominators
when choosing this curvature bound. The resulting \(H_0\) has
polynomial encoding length, independently of the eventual noise-grid size.

A retained unresolved cell at level \(j\) has a near-optimal corner.
The smooth global upper model, together with (4), gives the same gradient
bound as before. The unclosed-region argument then forces \(d\)
within distance

\[
 \tau_j=\sqrt k(\alpha+H_0)h_j                           \tag{10}
\]

of one of at most

\[
 K=R(m+n+1)                                             \tag{11}
\]

factor-coordinate hyperplanes. Their normals are fixed, and their offsets
depend affinely on \(r\). This includes singular piece Hessians through
their proper affine gradient images. A defining region row that is zero
in \(a\) cannot be the row violated elsewhere in a cell containing
its queried point, so no zero-normal exception is introduced.

Each such condition lifts to a fixed ambient hyperplane. More explicitly,
write its normalized equation as

\[
 u^Td+v^Tr+c_0=0,\qquad\|u\|=1.
\]

After (1), its ambient normal is
\(L=D^Tu+\Pi^Tv\). Because \(DT^T=I_k\) and
\(\Pi T^T=0\), we have \(TL=u\), hence
\(\|L\|\ge1\) from \(\|T\|_2\le1\).
The factor tube in (10) is therefore contained in the ambient Euclidean
\(\tau_j\)-tube about this fixed hyperplane.

For independently uniform ambient coordinates on an \(N\)-point grid,
conditioning on all but a largest normal coordinate bounds this event by
\(\sqrt n\tau_j/\sigma+1/N\). Consequently

\[
 \Pr_N\{\text{retained unresolved cell at level }j\}
 \le K\left[
 \frac{\sqrt{nk}(\alpha+H_0)h_j}{\sigma}+\frac1N
 \right].                                             \tag{12}
\]

These hyperplanes remain fixed as ambient noise varies; only their
factor-coordinate description has residual-dependent offsets.

## 5. Uniform section complexity of the local events

The event \(E_v\) in (7) has a bounded number of interval components
on every line parallel to an original noise coordinate. This avoids
analyzing the nonconvex global optimum as a function of the noise.

Fix every ambient coefficient except one, denoted \(t\). Then both
\(r\) and \(d\) are affine in \(t\). At any fixed auxiliary query
\(a\), each active-basis critical region for the inner convex QP
intersects this line in an interval, possibly empty, a point, or unbounded.
Its value formula is quadratic in \(t\). These at most \(R\)
intervals cover the whole real line: at every parameter an optimal-set
vertex supplies a nonsingular active basis. Values agree whenever regions
overlap.

The at most \(2R\) finite endpoints therefore partition the line into
open intervals on which one quadratic formula is valid. No pairwise
comparison of candidate value polynomials is needed.

If \(v\) has \(t_v\le k\) interior grid coordinates, its local
event uses at most \(2t_v+1\le2k+1\) such query values. Their
combined finite endpoints number at most \(2(2k+1)R\). Between
successive endpoints, the event is a conjunction of \(2t_v\)
quadratic weak inequalities. At most \(4t_v\) distinct roots split
that interval into sign-constant intervals and individual root points.
An identically zero polynomial imposes no additional split.

Including all original endpoints as possible isolated components, a safe
uniform bound on the number of interval components is

\[
 C_{\rm sec}=[2(2k+1)R+1](8k+2).                         \tag{13}
\]

For a union of at most \(C_{\rm sec}\) intervals, the probability
under an equally spaced \(N\)-point grid in \([-\sigma,\sigma]\)
differs from continuous uniform probability by at most
\(2C_{\rm sec}/N\). Replace the \(n\) noise coordinates one at a
time and apply this bound to every fixed section. The product-measure
telescoping argument proves

\[
 |\Pr_N(E_v)-\Pr_{\rm cont}(E_v)|
 \le\frac{2nC_{\rm sec}}N.                              \tag{14}
\]

The section bound is uniform in the values of the other coordinates,
including when those coordinates already have the discrete distribution.

## 6. One fixed finite law and the expected exact-work bound

Let \(B=\max\{2,R\}\), the exponential multiplier in the exact
original-QP fallback bound. Choose the least integer \(J\ge0\) with

\[
 s2^{-J}\le
 \frac{\sigma}{2nkKB(\alpha+H_0)}.                       \tag{15}
\]

The rational factor \(nk\) upper-bounds \(\sqrt{nk}\). In
particular \(J\) is determined before sampling and has polynomial
size in \(I\). Every deterministic level grid through \(J\) has
at most \((2^J+1)^k\) nodes. Put

\[
 Q_{\rm all}=(J+1)(2^J+1)^k.
\]

Choose the least power of two \(N\) satisfying

\[
 N\ge\max\{2,\ 2KB,\ 2nC_{\rm sec}Q_{\rm all}\}.       \tag{16}
\]

Sample all original noise coordinates independently and uniformly from

\[
 \{-\sigma+2\sigma j/(N-1):j=0,\ldots,N-1\}.           \tag{17}
\]

Both \(J\) and \(\log N\) are polynomial in the base input
length. In particular (16) is not a requirement that noise precision
exceed an exact-recovery precision depending on that same noise.

Run exact algebraic cell closure through level \(J\). If unresolved
retained cells remain, run the exact original-QP fallback on the same draw.
Validity of closure and fallback is deterministic, so every draw returns
an exact original feasible optimizer.

For the search cost, sum (14) over all deterministic level grid nodes and
all levels. Equations (9) and (16) give

\[
 \sum_{j=0}^J\sum_{v\in G_j}\Pr_N(E_v)
 \le(J+1)H_{\rm amb}+1.                                \tag{18}
\]

Every retained unresolved cell has one corner satisfying \(E_v\), and
each corner belongs to at most \(2^k\) cells. Each retained cell has
at most \(2^k\) children. Corner evaluation, critical-region extraction,
and exact quadratic closure cost a dimension-dependent factor times
polynomial bit work. Their expected total work is therefore

\[
 C_0^k(1+H_{\rm amb})(I+1)^{C_1}                         \tag{19}
\]

for absolute constants, using the exact convex-QP and LP primitives of
the reviewed closure theorem. The base-input bit polynomial includes the
polynomial bounds on \(J\) and \(\log N\).

For the fallback, (12), (15), and (16) give probability at most \(1/B\).
Its deterministic cost is \(B\operatorname{poly}(I+\log N)\),
so its expected contribution is polynomial. This proves (19).

At each fixed \(k\), (19) is polynomial when the displayed numerical
ratios \(\alpha\sqrt n\,w_i/\sigma\) are polynomially bounded.
It is not an FPT statement in \(k\) and a dimension-free curvature
ratio: (9) contains powers of \(n\) whose exponent depends on \(k\).

The [rational negative-space normalization](spectral-normalization.md)
used in the factor-noise theorem supplies the stronger lower bound

\[
 TT^T\succeq\frac{63}{64}I_k.                            \tag{20}
\]

Here is the additional estimate, using that note's notation. Its output
is \(T=U^T\), \(U=R_AB_-\), where \(R_A\) is the orthogonal
projector onto \(\operatorname{range}(A)\) and the rational columns
of \(B_-\) are orthonormal. Each selected column has leakage at most
\(2e/\mu\) outside the negative eigenspace, hence also outside
\(\operatorname{range}(A)\). Since
\(e=\mu^2/(16n\beta)\), \(\mu\le\beta\), and \(k\le n\),

\[
 \|(I-R_A)B_-\|_2^2
 \le\frac{4ke^2}{\mu^2}
 \le\frac{k}{64n^2}\le\frac1{64}.
\]

The identity
\(TT^T=I_k-B_-^T(I-R_A)B_-\) proves (20). Consequently
\(\|D\|_2\le2\), \(s_i\le2\sigma\sqrt n\), and

\[
 w_i\le\operatorname{diam}(X)+\frac{4\sigma\sqrt n}{\alpha}.
                                                               \tag{21}
\]

With \(\nu=\max\{0,-\lambda_{\min}(A)\}>0\) and the normalized
choice \(\alpha<4\nu\), this yields

\[
 H_{\rm amb}\le
 \left[2+(1+2k)\left(2n+
       \frac{2\nu\sqrt n\,\operatorname{diam}(X)}{\sigma}
 \right)\right]^k.                                    \tag{22}
\]

Thus the theorem applies with \(k\) equal to the negative
inertia, without a separate factor-conditioning assumption. The powers
of \(n\) still prevent an FPT conclusion in the displayed parameters.

For another supplied factorization, a lower bound
\(\sigma_{\min}(T)\ge c_T>0\) instead gives

\[
 w_i\le\operatorname{diam}(X)+
             \frac{2\sigma\sqrt n}{\alpha c_T},
\]

which makes the numerical dependence explicit. Without such a bound,
formula (2) remains valid and records any ill-conditioning of \(T\)
in the width parameter rather than hiding it.

## 7. Scope and verification status

The target is the exact optimum of the independently perturbed original
objective, under the particular base-chosen finite law (16)--(17).
Arbitrary coarser atomic laws are not covered by the expectation bound.
The algorithm never rejects or resamples an exceptional draw.

The [full independent review](../reviews/smoothed-ambient-cell-closure-review.md)
found no substantive gap in the complementary-minor fiber-volume estimate,
uniform scalar-section bound, finite-grid bookkeeping, or exact-work
conclusion. The reused algebraic closure theorem has its separate
mathematical and exact-rational checks.

The reviewer ran

```sh
python research-20261002/new-direction/check_ambient_noise_review.py
```

It passed 84 complementary-minor identities, 14 ambient-normal checks,
27 exact local-event line sections with 81 finite-grid discrepancy checks,
and 27 exact polygon-area fiber probabilities. These diagnose the new
geometry and probability lemmas; they do not constitute an implementation
of the full ambient solver. Scoped whitespace and local Markdown-link
checks also passed. No project-wide checks or CI inspection were performed
for this extension.

The [focused interface review](../reviews/smoothed-ambient-interface-review.md)
independently approves the normalization, fixed auxiliary domain, rational
coordinate changes, base-only curvature bound, and arithmetic bookkeeping.
It includes exact frame and pulled-back-normal checks; it does not replace
the separate review of the volume and discrepancy arguments.

## 8. Prior-art boundary and solver implications

The [ambient-noise audit](../prior-art/smoothed-ambient-noise-prior.md)
compares the perturbation model and exact-work guarantee with smoothed
low-rank global optimization and discrete winner isolation. The
[parametric-QP audit](../prior-art/smoothed-cell-closure-prior.md)
identifies older value-function reductions and critical-region algorithms.
Those reductions and algebraic ingredients are not claimed as new. The
candidate addition is their use with the volume and finite-grid arguments
above to bound expected exact work under ambient independent noise.
The examined sources do not establish publication priority.

For a solver, the theorem supports searching a low-dimensional nonconvex
parameter space while keeping dense linear constraints inside exact convex
QP solves. It permits growth degeneracy and includes all sampled draws.
The proof does not show that numerical critical-region extraction is fast
or stable in practice, that the fallback is acceptable operationally, or
that this method beats existing solvers. It optimizes the sampled objective.
Shrinking the noise to certify approximation of the original objective
reintroduces inverse-accuracy dependence; no improved worst-case
approximation bound for that objective is established.
