# Exact sparse optimization for affine-state polynomial-actuator dynamics

Date: 2026-10-02. Status: complete proof that passed
[independent completed-text review](../reviews/smoothed-polynomial-actuator-dynamics-review.md).
No novelty claim.

Stable scalar dynamics with polynomial control response admit a direct
extension of the [sparse polynomial box theorem](smoothed-sparse-polynomial.md)
when state costs are affine. A backward recurrence eliminates all dependent
states. Conditioning on their noise leaves independent linear noise on the
free variables, and the reduced polynomial retains its degree and sparse
factor scopes. The resulting algorithm handles continuous and native integer
controls and returns an exact feasible trajectory implicitly on every draw.

This is a specific reduction, not a general constrained semiconcavity claim.
Even the invariant dynamics \(s_{t+1}=u_t^2\) can give a conditional bag
value \(-|\gamma_{u_t}|\sqrt{s_{t+1}}\), which has no finite upper
curvature bound at zero. The present reduction avoids such predecessor
fibers. The [explicit obstruction](../reviews/stable-dynamics-bag-obstruction.md)
also shows why feasible endpoint rounding needs a separate argument.

## 1. Model and exact-output statement

For a horizon \(H\ge1\) and \(t=0,\ldots,H-1\), impose

\[
 s_{t+1}=a_t s_t+g_t(u_t),\qquad |a_t|\le a<1.             \tag{1}
\]

The rational data specify nonempty bounded closed state intervals \(I_t\),
an initial state interval \(I_0\), and bounded closed control intervals
\(U_t\). The initial state
is continuous; a fixed initial value is also allowed. Each control is
continuous or a native integer variable. Round integer endpoints inward
first and report infeasibility if a control domain is empty. All subsequent
claims assume these domains are nonempty. Every \(g_t\) is an explicit
rational univariate polynomial of degree at most a fixed \(d\ge1\).
Assume the box-invariance condition

\[
 a_t I_t+g_t(\operatorname{hull}U_t)\subseteq I_{t+1}.     \tag{2}
\]

There are no further state, terminal, path, or control constraints.
In particular, (2) makes all dependent-state interval constraints
redundant after forward simulation. Invariance can be checked in
polynomial bit time at fixed degree: extrema of each univariate \(g_t\)
occur at rational endpoints or roots of its derivative, and comparison
with the required rational interval endpoints uses univariate algebra.

Write \(z=(s_0,u_0,\ldots,u_{H-1})\) for the free variables. The objective is

\[
 F_0(s,u)=q(z)+\sum_{t=1}^H c_t s_t,                    \tag{3}
\]

where \(q=\sum_B q_B\) has explicit rational polynomial factors of fixed
degree at most \(d\). Supply a tree decomposition with largest bag size
\(p\), such that every factor's entire variable scope is contained in one
bag. Thus the relevant graph is the primal interaction graph, not the
bipartite incidence graph. Unary terms may be placed in any bag containing
their variable. A term \(c_0s_0\), if present, belongs to \(q\).
No decomposition of the original equality graph is needed for this reduction.

For a supplied rational \(\sigma>0\), independently perturb every original
state and control coefficient by the same finite uniform grid in
\([-\sigma,\sigma]\):

\[
 F_\gamma=F_0+\sum_{t=0}^H\gamma_{s_t}s_t
                  +\sum_{t=0}^{H-1}\gamma_{u_t}u_t.     \tag{4}
\]

The common power-of-two grid size \(M\) is chosen from the base data
before any coefficients are sampled. Its logarithm is polynomial in
the base input length \(I\).

Substitute fixed free variables. Let \(n\) remain, let \(w_i\) be their
widths, and put \(W=\sum_i w_i\), \(w_{\max}=\max_iw_i\). The case
\(n=0\) is direct exact forward evaluation. For \(n>0\), the construction
below supplies a base-only uniform coordinate-curvature bound \(L>0\).
Noise on substituted fixed free variables contributes a known additive
constant. Carry it separately and add it back to objective values; omit it
from the optimization formulas below.
The expected bit work is

\[
 C_0^p\left[4+\frac{(1+n/2)Lw_{\max}}{2\sigma}\right]^p
 \operatorname{poly}_d(I).                              \tag{5}
\]

Every draw returns a global optimizer of (4). The usual exact descriptor
is a certified strongly convex patch in the free variables, together with
the recurrence (1). Exceptional draws use an exact algebraic fallback
for the reduced polynomial box problem. The output supports point and
value approximation, including feasible rational trajectories and certified
objective gaps, in expected \(\operatorname{poly}_d(I+q_{\rm acc})\)
bit work at \(q_{\rm acc}\) requested accuracy bits. Expanded algebraic
coordinates and minimal polynomials of the states are not required.

No uniqueness, growth modulus, LICQ margin, or strict-complementarity
margin is supplied as an input assumption.
The bound is polynomial for fixed \(p\) under polynomial bounds on its
displayed numerical ratios. It is not an FPT statement in \(p\), or a
polynomial bound in the binary encoding of integer widths alone.

## 2. Backward elimination preserves sparse polynomial structure

Condition on the dependent-state coefficients
\(\eta=(\gamma_{s_1},\ldots,\gamma_{s_H})\). Define rational adjoints

\[
 \lambda_H=c_H+\eta_H,\qquad
 \lambda_t=c_t+\eta_t+a_t\lambda_{t+1}
 \quad(t=H-1,\ldots,1).                                 \tag{6}
\]

Repeated substitution of (1) gives the exact identity

\[
 \sum_{t=1}^H(c_t+\eta_t)s_t
 =a_0\lambda_1s_0+\sum_{t=0}^{H-1}\lambda_{t+1}g_t(u_t).
                                                               \tag{7}
\]

Thus the reduced objective is

\[
 Q_\eta(z)+\xi^Tz,\qquad
 Q_\eta(z)=q(z)+a_0\lambda_1s_0+
                \sum_{t=0}^{H-1}\lambda_{t+1}g_t(u_t),  \tag{8}
\]

where \(\xi=(\gamma_{s_0},\gamma_{u_0},\ldots,\gamma_{u_{H-1}})\),
after dropping fixed coordinates and carrying their noise constants separately.
Conditional on \(\eta\), the coordinates of \(\xi\) remain independent
uniform draws on the original common grid. The deterministic offsets in
(8) do not change that law.

The new terms are unary. Consequently (8) preserves the supplied bag
size, has fixed degree at most \(d\), and has polynomial explicit size.
This remains true for native integer controls; (7) is an identity, not
an approximation or a relaxation of their labels.

If \(|c_t|\le C_s\), then for every possible conditioned draw

\[
 |\lambda_t|\le\Lambda:=\frac{C_s+\sigma}{1-a}.           \tag{9}
\]

The rational adjoints have \(\operatorname{poly}(I+b)\) encoding length
when the sampled coefficients have \(b\) bits. The recurrence has only
\(H\) steps and is affine in previous adjoints. Products of the supplied
rational coefficients add denominator bit lengths; they do not repeatedly
square them.

Let \(L_q\ge0\) bound every \(|\partial_{ii}q|\) on the full free-variable
hull, and let \(G_j\) bound all \(|g_t^{(j)}|\) on the control hulls.
Termwise rational monomial bounds provide such numbers. One valid choice is

\[
 L=1+L_q+\Lambda G_2.                                   \tag{10}
\]

Likewise, if \(M_q\) bounds
\(\max_i\sum_j|\partial_{ij}q|\) and \(T_q\) bounds
\(\max_i\sum_{jk}|\partial_{ijk}q|\), take

\[
 M_1=1+M_q+\Lambda G_2,\qquad
 T_3=1+T_q+\Lambda G_3.                                 \tag{11}
\]

These bounds hold for every \(\eta\), independently of \(M\). Fixed-degree
monomial bounds also give uniform value and gradient bounds. Their numerical
magnitudes can be large; their encoding lengths are polynomial in \(I\).
Only the displayed \(L\) enters the grid-count factor in (5).

## 3. One finite law works before conditioning

It is not valid simply to compute a different sampling grid after observing
\(\eta\). A common base-only grid exists for the following reasons.

The [finite-noise tail proof](polynomial-finite-noise-tails.md) bounds the
number of scalar sections by the variable count, degree, and mixed-box
formula. Its quantifier-elimination count is independent of polynomial
coefficient heights. It therefore supplies one
\(C_{\rm tail}=2^{\operatorname{poly}_d(I)}\) uniformly for every
\(Q_\eta\), including real coefficients in intermediate conditional
arguments. For each fixed \(\eta\),

\[
 \Pr_\xi\{g_*<\epsilon\mid\eta\}
 \le W\epsilon/\sigma+2nC_{\rm tail}/M.                 \tag{12}
\]

Here \(g_*=0\) includes tied draws. The active-gradient tail likewise
depends on degree and face counts, not coefficient heights. With \(n_c\)
free continuous variables and \(R_Z\) native integer assignments, set

\[
 K=\max\{1,n_c3^{n_c}R_Z\max(1,d-1)^{n_c}\}.             \tag{13}
\]

The probability, conditional on \(\eta\), of positive growth together
with some active free continuous gradient of magnitude at most \(\tau\)
is at most \(K(\tau/\sigma+1/M)\).

One also needs a uniform fallback budget, rather than substituting sampled
coefficient lengths into its exponential factor. The
[fallback proof](polynomial-exact-fallback.md), sections 3--5, separates
formula dimensions, atom counts, and degree from coefficient height.
Its same two-block canonical-optimizer formulas apply when arbitrary
coefficients of a fixed-degree polynomial vary. For (8), their format is
base-fixed, and denominator clearing gives coefficient lengths
\(\operatorname{poly}_d(I+b)\). Thus one base-only
\(B=2^{\operatorname{poly}_d(I)}\) bounds exact fallback and subsequent
evaluation by

\[
 B(I+b+q_{\rm acc}+1)^{c_d},                            \tag{14}
\]

with a fixed exponent \(c_d\). This is a direct use of that proof's
height bound; it does not require that only linear coefficients vary.

For completeness, the following choice makes the absence of a precision
circle explicit. Set

\[
 \rho=1/(4B),\quad g_0=\rho\sigma/(2W),\quad
 \tau=\rho\sigma/(2K),\quad A=2+nL/g_0.
\]

Let \(s\) be the least power of two at least \(\max(1,w_{\max})\).
Choose the least \(J\ge0\) such that \(h_J=s2^{-J}\) satisfies

\[
 h_J\le\min\{1/(4A),\ \tau/(4M_1A),\ g_0/(4T_3A)\}.
                                                               \tag{15}
\]

Finally choose the least power of two

\[
 M\ge\max\{2,\ 2^J,\ 4nC_{\rm tail}/\rho,\ 2K/\rho\}.    \tag{16}
\]

Every quantity preceding \(M\) is determined by the original base data
and the uniform bounds (9)--(11). Its logarithm has polynomial size.
The eventual sampled denominators appear only in the polynomial height
factor in (14).

For every fixed \(\eta\), (12)--(16) give a bad-growth probability at
most \(\rho\) and an additional active-gradient failure probability at
most \(\rho\). Averaging over \(\eta\) preserves the bound \(2\rho\).
There is no resampling and no conditioning on the occurrence of good growth.

## 4. Sparse search and exact closure

After the sampled adjoint pass, run the sparse polynomial box algorithm
on (8). All of its rounding and bag min-marginal arguments now concern a
product box in the free variables. Every free-grid corner has an exact
feasible forward trajectory by (2). For a fixed \(\eta\), the base
polynomial is fixed and the free linear noise is independent; the theorem's
conditional bag semiconcavity proof applies without an equality fiber.
The uniform derivative bound gives its conditional expected count with
the same \(L\) in (5). Averaging proves that bound for the full original
noise law.

Use (11) and the common \(g_0,\tau,J\) for gradient fixing and convex-patch
closure. The tests are sound on every draw. On the good event they succeed
by level \(J\); otherwise invoke the all-draw fallback for the same reduced
objective. Equation (14) and failure probability at most \(1/(2B)\)
make the expected fallback and evaluation contributions polynomial.
No KKT regularity of the redundant original state bounds is required.

The usual patch descriptor and the sparse pruning proof record certify a
global optimizer of (8). Equations (1), (2), and (7) transfer that
certificate to the constrained problem exactly. Sparse preprocessing,
the adjoint pass, sampling, and the trajectory recurrence take polynomial
additional bit work. This proves (5) and the all-draw exact claim.

## 5. Feasible trajectory evaluation has polynomial bit cost

The exact free optimizer may be algebraic. Store it in the box theorem's
implicit patch or exceptional algebraic form, and append the rational
recurrence (1). This specifies one common trajectory without requiring a
primitive element or separately expanded state minimal polynomials.

For a feasible rational free point, every state from (1) is rational.
At fixed degree, evaluating \(g_t\) multiplies the control bit length by
at most a constant; the subsequent recurrence is affine in the state.
Across \(H\) steps, rational numerator and denominator lengths therefore
grow only polynomially in \(I\) and the free-point precision. Forward
evaluation gives exact equality feasibility, and (2) gives state-box
feasibility. Native integer labels remain exact.

If \(|g_t'|\le G_1\), the forward map from free variables to the full
trajectory has the safe rational Lipschitz bound

\[
 K_{\rm traj}=1+\frac{1+G_1}{1-a}.                       \tag{17}
\]

Indeed, state differences satisfy
\(|\Delta s_{t+1}|\le a|\Delta s_t|+G_1|\Delta u_t|\);
the geometric convolution has Euclidean operator norm at most \(1/(1-a)\).
Thus an additional \(\lceil\log_2 K_{\rm traj}\rceil\) free-point
accuracy bits suffice for a prescribed full-trajectory error.

The box evaluator returns feasible rational free points and certified
reduced objective gaps. Their exact forward trajectories have the same
objective values and gaps by (7). This proves the claimed evaluation
contract. It avoids the repeated nonlinear state composition that can
produce exponential rational denominators in general stable dynamics.

## 6. Scope and a stateful nonlinear example

On \([-1,1]\), the transition

\[
 s_{t+1}=\tfrac14s_t+\tfrac14u_t+\tfrac18u_t^2
\]

maps the input rectangle into \([-3/8,5/8]\), is genuinely stateful,
and is nonlinear in the control. Continuous or integer controls in the
same hull are allowed. Any explicit fixed-degree polynomial cost
\(\sum_Bq_B(s_0,u_B)\) with the promised free-variable decomposition,
together with affine state costs, fits the theorem. The control costs
may be nonconvex and coupled; they need not be separable.

The restriction to affine state dependence and affine state costs is
substantive. Nonlinear state dynamics generally raise the degree under
elimination. Nonlinear state costs can couple many earlier controls even
when state dynamics are affine. Extra terminal or path constraints can
destroy the free product domain. The theorem makes no claim for those
extensions, or for a general original constraint-graph treewidth bound.

The conditional fiber obstruction at the start shows why this result
cannot be obtained simply by placing nonlinear equalities into the box
algorithm. It instead identifies a class where eliminating those equalities
is exact, sparse, and of controlled degree.

## 7. Verification status

The targeted command

    python research-20261002/new-direction/check_polynomial_actuator_dynamics.py

passed 72 exact-rational adjoint identities and invariant trajectories,
72 trajectory Lipschitz comparisons, 756 denominator-growth checks,
120 native-integer assignments, and 120 exact objective-gap transfers.
These finite checks diagnose the reduction and output map; they do not
implement the sparse optimizer, noise-tail proof, or exact fallback.

The [independent completed-text review](../reviews/smoothed-polynomial-actuator-dynamics-review.md)
found no mathematical or bit-complexity blocker. It checked the conditional
noise law, uniform common grid and fallback budget, coupled sparse costs,
native integer controls, and exact trajectory evaluation. Scoped links and
whitespace checks passed. No external literature search, project-wide
verification, or CI inspection was performed in this workstream.
