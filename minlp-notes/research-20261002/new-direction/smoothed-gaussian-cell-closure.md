# Expected exact quadratic optimization under rational Gaussian-like ambient noise

Date: 2026-10-02. Status: complete proof that passed
[independent review](../reviews/smoothed-gaussian-cell-closure-review.md).
No priority claim is made. This extends the reviewed
[ambient cell-closure theorem](smoothed-ambient-cell-closure.md). Its
new ingredient is a Gaussian-weighted count of local grid events that
depends on the original projected feasible set, rather than the enlarged
auxiliary search box. The finite sampling law below has independent
original coordinates, bounded polynomial-time sampling, and polynomial
encoding length. It approximates a Gaussian; it is not an exact Gaussian.

## 1. Statement and interfaces

Let \(X=\{x:Mx\le b_X\}\) be a nonempty bounded rational polytope,
and let \(F(x)=x^TAx/2+b^Tx+c_0\). Use a supplied rational
decomposition

\[
 P=A+\alpha T^TT\succeq0,\qquad
 \ker P\subseteq\ker T,\qquad
 cI_k\preceq TT^T\preceq I_k,
 \quad 1/2\le c\le1,\quad \alpha>0.                 \tag{1}
\]

The case \(k=0\) is convex QP. Write \(I\) for the rational input
length, including the positive rational noise scale \(\sigma\). The
algorithm computes, from these base data before sampling, a finite
rational law \(\mathcal L\). It then samples every original linear
coefficient independently from \(\mathcal L\), obtaining \(\gamma\),
and returns an exact rational minimizer of
\(F_\gamma(x)=F(x)+\gamma^Tx\).

Put \(\ell_i=\min_X(Tx)_i\), \(u_i=\max_X(Tx)_i\), and
\(C=1+2k\). The expected bit work is at most

\[
 C_0^k(1+H_G)(I+1)^{C_1},\qquad
 H_G=\prod_{i=1}^k\left[
 2+c^{-1/2}(2C+4)+
 \frac{C\alpha(u_i-\ell_i)}{\sigma\sqrt{2\pi}}
 \right],                                               \tag{2}
\]

for absolute constants. Every draw is solved correctly, including atoms
on exceptional hyperplanes; rare draws use an exact fallback. No growth,
uniqueness, genericity, or independent global certificate is assumed.

The [rational spectral normalization](spectral-normalization.md), with
the lower-frame estimate proved in the ambient note, supplies
\(c=63/64\), \(k\) equal to the negative inertia, and
\(\alpha<4\nu\), where
\(\nu=\max\{0,-\lambda_{\min}(A)\}\). Since
\(u_i-\ell_i\le\operatorname{diam}(X)\), (2) has form

\[
 f\!\left(k,\frac{\nu\operatorname{diam}(X)}{\sigma}\right)
 \operatorname{poly}(I).                               \tag{3}
\]

Unlike the uniform-cube ambient bound, its input polynomial has an
absolute exponent independent of \(k\). The target remains the sampled
objective, not the unperturbed objective.

## 2. Gaussian decomposition and local events

Set \(D=(TT^T)^{-1}T\), \(\Pi=I_n-T^TD\),
\(d=D\gamma\), and \(r=\Pi\gamma\). For the continuous proxy
\(\gamma\sim N(0,\sigma^2I_n)\), the random vectors \(d,r\)
are independent: their cross-covariance is zero, and they are jointly
Gaussian. Also

\[
 \operatorname{Cov}(d)=\sigma^2(TT^T)^{-1}.
\]

Define

\[
 W_r(a)=\min_{x\in X}
 [F(x)+r^Tx+\tfrac\alpha2\|a-Tx\|^2],
 \qquad V_\gamma(a)=W_r(a)+d^Ta.
\]

An inner optimizer at \(a\) supplies the global upper model

\[
 W_r(z)\le W_r(a)+\alpha(a-Tx_a)^T(z-a)
                       +\tfrac\alpha2\|z-a\|^2.       \tag{4}
\]

Thus the location bound below uses an actual feasible image \(Tx_a\).
It does not bound an arbitrary piece gradient by a coefficient-height
estimate.

Use any fixed auxiliary rectangle, with nested equal-subdivision grids
as in the ambient theorem. At a level, coordinate steps are \(h_i\),
the longest nominal step is \(h\), and each coordinate having interior
grid points satisfies \(h/2<h_i\le h\). Set
\(B_h=\alpha\sum_i h_i^2/8\). For each deterministic vertex \(v\),
let \(E_v\) consist of all necessary neighboring inequalities

\[
 V_\gamma(v)\le V_\gamma(v\pm h_ie_i)+2B_h             \tag{5}
\]

in coordinates where both neighbors exist. This event is defined for
every ambient draw, even if its auxiliary optimizer is outside the
rectangle. It is used only as an upper bound on retained-cell events
for the bounded finite law.

Fix \(r\). The two inequalities in coordinate \(i\) restrict
\(d_i\) to an interval \(I_i(r)\) of length at most

\[
 \alpha h_i+4B_h/h_i\le C\alpha h_i.                   \tag{6}
\]

Combining (5) with (4) gives the additional necessary condition

\[
 |d_i+\alpha(v_i-(Tx_v)_i)|
 \le\alpha h_i/2+2B_h/h_i\le C\alpha h_i/2.
\]

Consequently the allowed set is contained in the deterministic interval

\[
 J_i(v)=\alpha[\ell_i-v_i,u_i-v_i]
            +[-C\alpha h_i/2,C\alpha h_i/2].           \tag{7}
\]

The interval \(I_i(r)\) itself need not be contained in (7); the event
lies in their intersection. This distinction is sufficient below.

## 3. A weighted lattice count independent of the auxiliary width

Let \(\phi_s\) be the one-dimensional centered Gaussian density of
standard deviation \(s=\sigma/\sqrt c\). For any subset \(Q\) of
\(t\) coordinates, the marginal density of \(d_Q\) obeys

\[
 p_Q(z)\le c^{-t/2}\prod_{i\in Q}\phi_s(z_i).           \tag{8}
\]

Indeed its covariance eigenvalues lie between \(\sigma^2\) and
\(\sigma^2/c\): the determinant prefactor is at most
\((2\pi\sigma^2)^{-t/2}\), and the inverse covariance is at least
\(cI_t/\sigma^2\). Independence from \(r\), followed by integration
over the allowed coordinate intervals, now gives

\[
 \Pr(E_v)\le c^{-t/2}\prod_{i\in Q}
 \min\{1,C\Delta_i\sup_{z\in J_i(v)}\phi_s(z)\},
 \qquad \Delta_i=\alpha h_i.                           \tag{9}
\]

The outer factor in (8) is not silently moved inside a minimum; (9)
follows from the dominating product density itself.

For a one-dimensional lattice of spacing \(\Delta>0\), and a core
interval \([A,B]\) of width \(W\), one has

\[
 \sum_{z\text{ on the lattice}}
 \min\{1,C\Delta\sup_{y\in[A-z-C\Delta/2,
                                  B-z+C\Delta/2]}\phi_s(y)\}
 \le CW\phi_s(0)+2C+4.                                \tag{10}
\]

To verify this for every mesh size, first consider nodes in
\([A-C\Delta/2,B+C\Delta/2]\). There are at most
\(W/\Delta+C+2\), and each contributes
\(\min(1,C\Delta\phi_s(0))\). Their total is at most
\(CW\phi_s(0)+C+2\). On either remaining tail, the summand is
a decreasing function of distance from that interval. The lattice sum
is at most its first term plus its integral divided by \(\Delta\),
and hence at most

\[
 1+\Delta^{-1}\int_0^\infty
             \min(1,C\Delta\phi_s(t))\,dt\le1+C/2.
\]

This proves (10). Keeping the minimum with 1 is essential on coarse
meshes.

Apply (10) to \(A=\alpha\ell_i\), \(B=\alpha u_i\), and
the lattice of \(\alpha v_i\). Each finite coordinate grid is a
subset of that lattice. Its two endpoint choices require no local
inequality; each contributes 1. Summing (9) over interior-coordinate
subsets and all grid vertices proves

\[
 \sum_v\Pr_{\rm Gauss}(E_v)\le H_G                    \tag{11}
\]

with (2), because
\(c^{-1/2}\phi_s(0)=1/(\sigma\sqrt{2\pi})\).
Unrefined coordinates have only two endpoints and satisfy the same
bound. In particular (11) is uniform in the location and width of the
fixed rectangle. The Gaussian proxy need not place all its optimizers
inside that rectangle.

## 4. A polynomial-time finite rational Gaussian approximation

The following elementary sampler avoids exact Gaussian quantiles. Given
an integer \(p\ge1\), it produces a rational \(Z_p\), has bounded
polynomial running time in \(p\), and satisfies

\[
 |Z_p|\le p+20,
 \qquad\sup_t|\Pr(Z_p\le t)-\Phi(t)|\le2^{-p}.         \tag{12}
\]

All random choices use independent fair bits. Its law is fixed and
finite, although an explicit list of its exponentially many masses is
unnecessary.

Here is a construction with deliberately loose constants. Put
\(K_p=p+20\), \(e_p=2^{-(p+20)}\). Choose a power of two \(N_p\)
whose equally spaced grid on \([-K_p,K_p]\) has mesh
\(\Delta_p\le e_p/K_p\). Propose one uniform grid node \(z\).
Compute a dyadic number \(w(z)\in[0,1]\) with

\[
 |w(z)-\exp(-z^2/2)|\le e_p/K_p,
\]

using a fixed common dyadic denominator. Accept the proposal with exact
probability \(w(z)\): if the common denominator is \(2^q\), use
\(q\) fair bits. Make at most
\(L_p=\lceil16K_p(p+20)\rceil\) independent attempts. Return the
first accepted node, or 0 if all attempts fail.

The acceptance probability is at least \(1/(16K_p)\): at least a
\(1/(4K_p)\) fraction of this fine grid lies in \([-1,1]\), where
the approximate weight is at least \(1/4\). Thus the failure mass is
at most \(\exp(-(p+20))\le e_p\). Conditional on accepting, the
node distribution is exactly proportional to \(w(z)\), including
when acceptance occurs before the finite cap.

For completeness, elementary Riemann-sum estimates suffice for (12).
The function \(f(z)=\exp(-z^2/2)\) is bounded by 1 and is
1-Lipschitz. The integral over \([-K_p,K_p]\) exceeds 1.
Rectangle sums for any initial subinterval, allowing its last partial
cell and the endpoint node, differ from the integral by at most
\(2K_p\Delta_p+2\Delta_p\). Normalizing both measures changes
their distribution functions by at most \(10K_p\Delta_p\).
Replacing grid weights by \(w\) changes distribution functions by
at most \(10K_p(e_p/K_p)=10e_p\); these bounds follow by bounding
the total unnormalized mass error and using the normalizing integral
lower bound. Gaussian truncation beyond \(K_p\) contributes at
most \(e_p\), and capped rejection contributes at most \(e_p\).
The total is at most \(22e_p<2^{-p}\).

Weight computation is polynomial bit work. One explicit method uses
\(t=z^2/2\), reduces the argument to \(u=t/2^s\le1/2\),
approximates \(e^{-u}\) by its alternating Taylor series, and squares
\(s\) times with dyadic rounding and clamping to \([0,1]\).
Here \(s=O(\log K_p)\); \(O(p+\log K_p)\) precision bits,
with the additional \(s\) guard bits, suffice. Taylor remainders
decrease geometrically on \([0,1/2]\), and squaring on \([0,1]\)
amplifies error by at most 2. This also gives a deterministic rule for
every weight, so the construction defines one law rather than an
accuracy-dependent random numerical oracle.

Scale the output by rational \(\sigma\). The resulting coordinate
law has Kolmogorov distance at most \(2^{-p}\) from
\(N(0,\sigma^2)\), support in
\([-\sigma(p+20),\sigma(p+20)]\), and polynomial encoding length.

## 5. Base-only choice of support and precision

Reuse the following base-only constants from the ambient closure proof:
\(R_b=2^m\) bounds the number of critical bases,
\(B=\max(2,R_b)\) bounds the fallback's exponential factor,
\(K_b=R_b(m+n+1)\) bounds exceptional hyperplanes, \(H_0\) bounds
all critical-piece Hessian norms, and

\[
 C_{\rm sec}=[2(2k+1)R_b+1](8k+2)
\]

bounds the number of interval components of each local event on every
line parallel to an original coefficient axis. Their logarithms have
polynomial base-input size; importantly \(H_0\) excludes sampled
coefficient denominators.

For a trial support multiplier \(R_s=2^t\), use the fixed box

\[
 A_{R_s}=\prod_i[\ell_i-s_i/\alpha,u_i+s_i/\alpha],
 \qquad s_i=R_s\sigma\sum_j|D_{ij}|,
\]

and let \(s=\max_i(u_i-\ell_i+2s_i/\alpha)\). Every draw with
\(\|\gamma\|_\infty\le R_s\sigma\) has an auxiliary optimizer
in this box. Choose the least \(J\ge0\) such that

\[
 s2^{-J}\le\frac{\sigma}{4kK_bB(\alpha+H_0)},           \tag{13}
\]

and put \(Q_{\rm all}=(J+1)(2^J+1)^k\). Choose the least positive
integer \(p\) such that

\[
 2^p\ge\max\{8nK_bB,\ 2nC_{\rm sec}Q_{\rm all}\}.     \tag{14}
\]

Starting at \(t=0\), increase \(t\) until \(2^t\ge p+20\).
Fix the first successful \(R_s,J,p\), then sample all coefficients
independently using section 4. This is a deterministic base-data budget
calculation, before any random draw. It does not query a precision bound
that depends on the eventual sampled denominators.

The loop terminates in polynomial time. There is a computable
\(A_0=\operatorname{poly}(I)\) such that \(J\le A_0+t\),
and (14) gives \(p\le A_1+O(k t+\log(A_0+t+1))\), with
\(A_1=\operatorname{poly}(I)\). Exponential \(2^t\) exceeds this
linear-plus-logarithmic bound at polynomial \(t\) (indeed logarithmic
in suitable polynomial bounds). Every intermediate integer has polynomial
encoding length. The resulting \(J,p\), auxiliary coordinates, sampler
outputs, and exact-QP queries have polynomial encoding length with an
absolute exponent. Equation (12) and \(p+20\le R_s\) guarantee
that every sampled draw fits the fixed box.

## 6. Transfer, closure, and expected exact work

For a union of at most \(C_{\rm sec}\) intervals, changing a scalar
Gaussian law to a law of Kolmogorov distance \(\delta=2^{-p}\)
changes its probability by at most \(2C_{\rm sec}\delta\).
This includes open, closed, unbounded and singleton intervals, by taking
one-sided limits. Replace the independent coordinates one at a time.
The uniform axis-section bound from the ambient proof gives

\[
 |\Pr_{\mathcal L^{\otimes n}}(E_v)
          -\Pr_{\rm Gauss}(E_v)|
 \le2nC_{\rm sec}\delta.
\]

Summing over the deterministic grids through \(J\), (11) and (14)
yield

\[
 \sum_{j=0}^J\sum_{v\in G_j}
        \Pr_{\mathcal L^{\otimes n}}(E_v)
 \le(J+1)H_G+1.                                      \tag{15}
\]

The exact critical-region extraction and cell closure are unchanged.
Every retained unresolved cell has a corner satisfying \(E_v\), each
corner belongs to at most \(2^k\) cells, and each cell has at most
\(2^k\) children. Exact quadratic minimization on a covered cell uses
\(3^k\) faces. The reviewed invariants preserve an optimal cell or
an exact optimal incumbent. Thus (15) bounds expected search work by
(2), including polynomial bit costs.

It remains to pay for the same-draw exact fallback. At the terminal
level, any retained unresolved cell forces the ambient noise into a
\(\tau_J\)-tube around one of \(K_b\) fixed hyperplanes, with

\[
 \tau_J=\sqrt k(\alpha+H_0)s2^{-J}.
\]

The pulled-back hyperplane normals have norm at least 1, as proved in
the ambient note. For the Gaussian proxy, a tube has probability at most
\(2\tau_J/(\sigma\sqrt{2\pi})\le\tau_J/\sigma\).
For the finite law, each axis section of a tube is an interval (or empty
or the whole line). Product telescoping therefore gives the safe bound

\[
 \Pr_{\mathcal L^{\otimes n}}(\text{one tube})
 \le\tau_J/\sigma+2n\delta.                            \tag{16}
\]

Equations (13), (14), (16), and \(\sqrt k\le k\)
bound the total unresolved probability by \(1/(2B)\), hence by
\(1/B\). The fallback costs \(B\operatorname{poly}(I)\), including
the now fixed polynomial sampled bit length, so its expectation is
polynomial. This completes the claimed bound. The factor \(n\) in
(14) affects only logarithmic precision and never enters \(H_G\).
The algorithm does not discard, redraw, or perturb an exceptional sample.

## 7. Scope and verification status

The Gaussian proxy is a proof device for the particular independent
finite law above. This note does not assert a Turing-model exact algorithm
on real Gaussian input, nor an expectation bound for every coarse
Gaussian approximation. The chosen law is independent across original
coordinates and has arbitrarily high base-chosen Kolmogorov accuracy,
while exact correctness holds at every atom.

The exact-QP, active-basis extraction, closure, and fallback interfaces
are the ones already reviewed for ambient noise. Two independent proof
reads found no substantive gap in the weighted count, finite sampler,
or deterministic budget loop. The
[persisted independent review](../reviews/smoothed-gaussian-cell-closure-review.md)
records the complete proof audit.

The targeted diagnostic command

```sh
python research-20261002/new-direction/check_gaussian_cells.py
```

passed 108 weighted-lattice fixtures (including coarse meshes and
zero-width cores), four exact covariance/frame identities, 18 rational
exponential-weight checks, and 12 fully enumerated finite-law distribution
checks. Three exact budget calculations terminated at support exponents
6, 11, and 16; the last used a 1,000-bit curvature bound and selected
33,133 bits of coordinate-law accuracy. These checks diagnose the new
lemmas; they are not an implementation or benchmark of the QP solver.
The enumerable distribution fixtures use small analogues of the sampler
grid, while the theorem samples its finer grid without enumerating it.
No project-wide checks or CI inspection were performed.
