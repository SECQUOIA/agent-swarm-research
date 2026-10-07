# Core-only noise with strongly convex interior recourse

Date: 2026-10-02. Status: independently reviewed; targeted checks passed. This is a restricted core-only-noise counterpart
of the [polynomial recourse theorem](smoothed-polynomial-box-recourse.md).
It removes residual noise under explicit additional recourse assumptions;
it does not solve the extension to arbitrary residual optimal fibers.

## 1. Assumptions and exact output

Let `F_0` be an explicitly represented rational polynomial of fixed degree
`d` on `[0,1]^n`. Supply a core `C` of size `k>=1`, residual coordinates
`R`, rational `L,mu>0`, and checkable certificates that

\[
 \partial_{ii}F_0\le L\quad(i\in C),\qquad
 \nabla^2_{RR}F_0\succeq\mu I
                  \quad\hbox{on the full unit box}.           \tag{1}
\]

For every fixed core point `v`, require that the unique residual minimizer
`s(v)` be interior to the original residual box. This is a **supplied,
verified structural premise**, not a free recognition oracle. One simple
sufficient certificate is a rational `beta>0` with, uniformly over the
remaining coordinates,

\[
 \partial_iF_0< -\beta\ \text{ on }z_i=0,
 \qquad \partial_iF_0>\beta\ \text{ on }z_i=1,
                          \qquad i\in R.                    \tag{2}
\]

Other tractable certificates of qualitative interiority are allowed.
Their verification costs and lengths, those for (1), and `mu` are counted
in base input length `I`. The algorithm does not use a quantitative
distance from `s(v)` to the residual bounds. In particular, the certificate
in (2) is sufficient, not a numerical slack parameter in the theorem.

Sample independent linear noise **only in the core** from one finite law

\[
 \gamma_i\text{ uniform on }
 \{-\sigma+2\sigma j/(M-1):0\le j<M\},\quad i\in C,
 \qquad F_\gamma(v,z)=F_0(v,z)+\gamma^Tv.                     \tag{3}
\]

There is a base-computable power of two `M`, with
`log M=poly_d(I)`, for which exact implicit optimization on every draw
has expected bit work and expected output/proof-record size

\[
 8^k\left[3+\frac{(1+k)L}{2\sigma}\right]^k
                  \operatorname{poly}_d(I).                  \tag{4}
\]

Usual output is a globally certified strongly convex rational patch,
with possibly fixed original **core** bounds. Its constrained minimizer
specifies the exact optimizer and value, and admits `q`-bit evaluation
in `poly_d(I+q)` time. A rare unresolved draw uses exact real-algebraic
fallback on that same draw. Exceptional output size and evaluation cost
may be large, with polynomial expected contribution. As in the predecessor,
the full pruning trace has an expected size bound, not a per-draw compact
bound. Subsequent expected evaluation work is `poly_d(I+q)` after global
validity has been established.

The exponential factor uses the original core curvature `L`; it does not
charge large mixed derivatives or `1/mu` as numerical parameters. Their
binary encodings and their effect on the cutoff precision are included
in the polynomial factor. This is not a uniform bound independent of
their input lengths.

If `R` is empty, use the predecessor's same core-corner algorithm with
direct polynomial evaluation and no residual slab calls; its count is
exactly (4). If `k=0`, the whole problem is strongly convex and its original
box and certificate already provide exact implicit output. Remove fixed
coordinates before invoking the main statement.

## 2. The projected value and a quantitative growth lift

Write

\[
 V_0(v)=F_0(v,s(v)),\qquad V_\gamma(v)=V_0(v)+\gamma^Tv.
\]

Choose a rational coefficient bound

\[
 M_1\ge\max\{1,\max_i\sum_j\sup|\partial_{ij}F_0|\},
 \qquad H=M_1/\mu.                                         \tag{5}
\]

Strong convexity and the variational inequalities for the two residual
minimizers give

\[
                  \|s(v)-s(w)\|_2\le H\|v-w\|_2.             \tag{6}
\]

Indeed, the residual gradient is strongly monotone with modulus `mu`,
while its change with the core is bounded by the cross-Hessian operator
norm, which is at most `M_1`. The fixed residual domain permits direct
comparison. Interiority is not needed for (6).

Suppose a sampled value function has point growth `g_V>0` at its unique
core optimizer `a_C`. Set `a_R=s(a_C)` and

\[
          g_F=\min\{g_V/(1+2H^2),\mu/4\}.                    \tag{7}
\]

Strong convexity of each conditional residual problem gives

\[
 F_\gamma(v,z)-f^*
 \ge g_V\|v-a_C\|^2+\frac\mu2\|z-s(v)\|^2.
\]

Since

\[
 \|v-a_C\|^2+\|z-a_R\|^2
 \le(1+2H^2)\|v-a_C\|^2+2\|z-s(v)\|^2,
\]

equation (7) proves full point growth with constant `g_F`. Thus core noise
can supply the full localization needed by the predecessor without
perturbing residual coefficients. The residual minimizer is unique here;
this argument is not a statement about arbitrary fibers.

Partial minimization preserves the upper coordinate curvature `L`.
Moreover, at an interior residual solution the implicit-function theorem
gives a smooth selector and the familiar value Hessian

\[
 \nabla^2V_0=F_{CC}-F_{CR}F_{RR}^{-1}F_{RC}.                  \tag{8}
\]

The subtracted matrix is PSD, so a large cross block does not increase
the upper core curvature. Formula (8) explains the parameter, but the
algorithm does not need to construct or symbolically expand the selector.

## 3. Core-noise growth and active-core tails

The continuous uniform growth tail for a continuous function on a compact
unit `k`-box applies directly to `V_0`:

\[
                 \Pr\{g_V<\epsilon\}\le k\epsilon/\sigma.
 \tag{9}
\]

For finite noise, the section-count argument in the
[polynomial tail theorem](polynomial-finite-noise-tails.md) applies with
no extra quantifier alternation. The good projected-growth event is
expressed by

\[
 \exists(a,z_0)\in[0,1]^n\ \forall(v,z)\in[0,1]^n:
 F_\gamma(v,z)\ge F_\gamma(a,z_0)+\epsilon\|v-a\|^2,
 \tag{10}
\]

where the norm uses only the `k` core coordinates. At `v=a`, this also
forces `z_0` to be a conditional minimizer. Consequently (10) is exactly
the projected-growth condition. Its two quantified blocks have size `n`,
and its degree and format have the same bounds as the predecessor.
The same effective argument supplies `C_tail=2^{poly_d(I)}`, independent
of coefficient precision and `epsilon`, such that

\[
 \Pr\{g_V<\epsilon\}
       \le k\epsilon/\sigma+2kC_{\rm tail}/M.                \tag{11}
\]

Only the `k` sampled marginals are replaced in the finite-law comparison.
No assertion about an explicit low-degree expansion of `V_0` is needed.

An active **core** gradient admits a separate tail. Fix an original core
face and one of its active coordinates `i`. All residual coordinates are
interior by assumption. Conditional on the other core noise, stationarity
on the free core coordinates and all residual coordinates is independent
of `gamma_i`, because coordinate `i` is fixed. On a positive projected-
growth draw, (7) and two-sided free directions make this joint free
Hessian positive definite. The root is therefore nonsingular and isolated.

The isolated-root Bezout bound gives at most `D^n` candidates per face,
where `D=max(1,d-1)`, even if other stationary components are singular.
There are at most `3^k` core faces. At each root the remaining active
gradient is `gamma_i+c`, so an interval of length `2tau` and a union bound
give

\[
 \Pr\{g_V>0\text{ and some active core gradient has magnitude}\le\tau\}
 \le K(\tau/\sigma+1/M),\qquad K=\max\{1,k3^kD^n\}.
 \tag{12}
\]

This step uses interiority exactly where the full-ambient theorem used
residual active-gradient noise. There are no residual active coordinates
at any original optimizer and thus no residual gradient tail to pay for.

## 4. Base-only closure and one finite law

Take the same exact algebraic fallback budget `B=2^{poly_d(I)}>=2` as
the polynomial recourse theorem, large enough also for subsequent
coordinate/value refinement. Define before sampling

\[
 \rho=1/(4B),\qquad
 \bar g_V=\rho\sigma/(2k),\qquad
 \tau=\rho\sigma/(2K),\qquad
 g_0=\min\{\bar g_V/(1+2H^2),\mu/4\}.                       \tag{13}
\]

Use certified approximate convex recourse on dyadic core corners with
`eta_j=e_j=kLh_j^2/8`. The predecessor's retained-cell rule gives incumbent
gap at most `2e_j`, a `4e_j`-near-optimal true corner for every retained
cell, and exactly the expected core count appearing in (4). This count
requires only core noise and was already proved after conditioning on
all residual data.

For completeness, let `T>=1` bound the Hessian Lipschitz constant in
infinity norm by coefficient sums, and let `G>=1` bound the core gradient
one-norm on the original domain for all allowed noise. Set

\[
 r=\min\{1/8,\tau/(16M_1),g_0/(4T)\},\qquad
 A_0=2+(kL+8)/g_0.
 \tag{14}
\]

Let `J` be the least nonnegative integer for which `h_J=2^-J` satisfies

\[
 h_J\le\min\{r/(4A_0),g_0r^2/(16GA_0)\}.                   \tag{15}
\]

At each level, center the residual patch at the incumbent completion and
evaluate the at most `2|R|` closed excluded slabs to objective accuracy
`g_0r^2/16`. As before, omit a slab whose raw threshold is at or beyond
an original residual endpoint. If its smallest certified lower value
minus the incumbent upper value exceeds `2G diam_inf D_j`, all conditional
optimizers over the retained core hull lie in the patch.

On this contained product box, try strict uniform gradient signs only for
original **core** bounds. Keep every residual coordinate free. If the
remaining box has midpoint `m` and infinity radius `r_Q`, test

\[
                    H_F(m)-(Tr_Q+g_0)I\succeq0               \tag{16}
\]

on all remaining coordinates. This proves a strongly convex exact patch.
Its residual intervals may be clipped by original bounds. There is no
need to demonstrate that the whole patch lies strictly inside those
bounds.

If `g_V>=bar g_V` and all active core gradients exceed `tau` in magnitude,
(7) supplies full growth `g_0`. Every numerical step of the predecessor's
closure proof now applies: the excluded lower gap is at least
`7g_0r^2/16`, the core-Lipschitz comparison is at most `g_0r^2/4`, and
all active core bounds are fixed. All residual coordinates and all
remaining core coordinates are interior at the true optimizer. Hence
their full principal Hessian is at least `2g_0 I` there. Hessian variation
and `r<=g_0/(4T)` prove (16), with slack at least `g_0/2`.

This is why **qualitative** residual interiority suffices. The Hessian
bound at the optimizer uses arbitrarily short two-sided directions, not
a lower bound on their feasible lengths. The certified output may retain
original residual bounds arbitrarily close to its optimizer.

Finally choose the least power of two

\[
 M\ge\max\{2,2^J,4kC_{\rm tail}/\rho,2K/\rho\}.             \tag{17}
\]

Equations (11)--(12) make the two failure probabilities at most `rho`
each. The exact fallback therefore runs with probability at most
`1/(2B)` and has polynomial expected cost. Every accepted patch and every
fallback answer is exact on its actual draw; no draw is resampled.
All thresholds precede `M`, and `J,log M=poly_d(I)`. Certified recourse,
compact tangent lower bounds, derivative tests, and patch evaluation use
the same polynomial-bit algorithms as the predecessor. This proves (4)
and its stated output/evaluation contract.

## 5. Scope and boundaries

This result covers dense coupled nonlinear recourse. For example,
strong diagonal quadratic terms plus a sufficiently small dense convex
quartic term can give a direct certificate of (1), while uniform inward
residual gradients give (2). Conditional minimizers can be implicitly
defined by a coupled polynomial system; an explicit polynomial selector
is not required. Fixing the core does not reduce the residual problem to
independent scalar equations in general.

This is not a generic recognition or discovery theorem for the core,
strong-convexity certificate, or interiority certificate. It also does not
resolve core-only noise with arbitrary flat residual fibers. The
[rotating-fiber obstruction](core-only-noise-rotating-fiber.md) has perfect
projected growth but no full-dimensional jointly convex neighborhood,
so simply weakening (1) to residual PSD breaks the closure argument.
Even strict residual convexity, a unique residual optimizer, and interiority
do not replace a uniform strong-convexity modulus: the same obstruction
note gives a shifted quartic variant with all these weaker properties and
an indefinite full Hessian arbitrarily near its optimizer.
Stable residual faces, quotient representations, and certificates for
the value function itself are separate possible extensions.

## 6. Verification status

The [independent actual-file review](core-only-noise-strong-recourse-independent-review.md)
passed without a substantive correction. It checked the projected-growth
formula, growth lift, isolated-root count, common finite law, and closure
without a residual boundary-distance parameter.

The author ran
`python research-20261002/reviews/check_core_only_strong_recourse.py`.
The [exact rational diagnostic](../reviews/check_core_only_strong_recourse.py)
passed four nonlinear core-only closure fixtures, 14 excluded slabs,
538 recourse bisections, and 27 growth-lift cases. Two fixtures retain a
residual patch clipped at zero while its optimizer is positive and only
of order `2^-400` from that bound. The fixture oracle is a certified scalar
reduction of coupled convex recourse; it is not an implementation of the
general GLS algorithm.

No index edits, project-wide verification, or CI inspection were performed.
