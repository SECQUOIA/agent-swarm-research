# Residual-certified checkpoint-span recycling

Status: Proved conditional module  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on mathematics; not an unconditional quantum advantage  
Question: Can low-dimensional Newton-ray structure remove repeated QLS and
tomography calls even when one-ray projective variation is unbounded?

## Exact rank theorem

For a sequence \(H_tz_t=f_t\), let \(\psi_t=z_t/\|z_t\|\). Retain prior
checkpoint rays and, at each round, minimize the current relative residual over
their span. If the minimum exceeds the acceptance threshold, solve once and
append the exact new ray. If

\[
 \dim\operatorname{span}\{\psi_t:t\geq1\}=r,
\]

then at most \(r\) refreshes occur. Every rejection appends a linearly
independent ray. The bound is sharp for \(H_t=I,f_t=e_t\).

This requires no smoothness, projective-variation bound, or comparison between
different \(H_t\)'s: every stored vector is re-evaluated under the current
operator. The repository's cycling counterexample has a three-dimensional
solution span, so exact span recycling resolves it after at most three solves
despite divergent one-ray refresh counts.

## Robust numerical-rank theorem

Normalize

\[
 M_t=(\|z_t\|/\|f_t\|)H_t,qquad \|M_t\|\leq B.
\]

Let checkpoint tomography error be \(\xi\), residual minimization and testing
each have additive error \(\eta/8\), and put

\[
 d_r=\inf_{\dim S=r}\sup_t\operatorname{dist}(\psi_t,S),qquad
 \Delta=\eta/(2B)-\xi>0.
\]

If

\[
 d_r+\xi<\frac{\Delta^{2-1/r}}{2r},
\]

then at most \(2r-1\) refreshes occur. A rejection forces innovation greater
than \(\Delta\); \(2r\) such columns have QR volume greater than
\(\Delta^{2r-1}\). But proximity to one \(r\)-space bounds that volume by
\((2r)^r(d_r+\xi)^r\), a contradiction.

With a stable \(\ell_1\) representation constant \(\Lambda\) for each ray in
the exact checkpoint basis, the sharper condition \(B\Lambda\xi\leq\eta/2\)
restores the exact \(R\leq r\) bound and permits linear, rather than quadratic,
inverse-\(\eta\) tomography scaling.

Holomorphic dependence on a Bernstein ellipse gives

\[
 d_r\leq\frac{2W\chi^{-(r-1)}}{\chi-1},
\]

and hence logarithmic numerical rank. Strict complementarity alone does not
give uniform \(\chi\): separable quadratic programs with distinct reduced
costs have distinct complex branch points and can have full-dimensional ray
span.

## Implementation and limitation

Materializing \(R\) checkpoint images and solving the small least-squares
problem costs roughly
\(O(R\,\mathrm{mv}(H_t)+D_tR^2+R^3)\) per test. Quantum coherent residual
tests add image-amplification and coefficient-conditioning factors and can be
worse than a classical scan. Feasible OSS span combinations preserve affine
primal and dual feasibility, and admit implicit coordinate representations,
but cone-scaling access still must be built.

Classical reduced-basis and recycling Krylov methods receive the same rank
benefit. The apparently new contribution is the QIPM checkpoint-ray refresh
theorem and its robustness boundary, not an unconditional quantum speedup.

## Rank alone does not make certification cheap

Take a two-system sequence with \(H_0=H_1=I_D\), \(f_0=e_0\), and

\[
 f_1=e_0+\sum_{i=1}^{D-1}a_ie_i,\qquad |a|\in\{0,1\}.
\]

The exact solution rays have rank at most two and \(\kappa=B=1\), but the best
residual from \(\operatorname{span}\{e_0\}\) is zero on the all-zero input and
\(1/\sqrt2\) on a uniquely marked input. Any correct refresh test across a
threshold between these values solves unique search, requiring
\(\Omega(\sqrt D)\) quantum and \(\Omega(D)\) randomized coefficient queries.
The uniform-index RHS preparation amplitude is \(\Theta(D^{-1/2})\), exactly
locating the missing cost. Small checkpoint rank must be paired with favorable
RHS/residual access; it cannot by itself make certification
\(\operatorname{poly}(r,\log D)\).

Even rank one does not reduce explicit output. With repeated \(H=I\) and a
hidden sign vector
\(f_b=D^{-1/2}((-1)^{b_1},\ldots,(-1)^{b_D})\), amplitude-state preparation
uses one phase query, but a classical vector of \(\ell_2\) error below \(1/4\)
reveals almost all signs and costs \(\Omega(D)\) queries and writes.
