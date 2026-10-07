# Expected exact optimization with sparse monotone implicit constraints

Date: 2026-10-02. Status: completed; independent proof reviews and targeted
exact checks passed under the stated global graph premises. This extends the
[sparse polynomial box theorem](smoothed-sparse-polynomial.md) to
constraints with a global, locally computable parameterization.
It makes no claim for arbitrary coupled constraints or publication priority.

## 1. Model and conclusion

Let \(t\in X\) be retained coordinates in a bounded rational mixed product
box, and let \(y_j\in V_j=[\ell_j,u_j]\), \(j=1,\ldots,m\), be dependent
continuous coordinates. Native integers occur only among the retained
coordinates. Round integer bounds inward, reject empty domains, and
substitute fixed retained coordinates. A singleton dependent interval
can also be substituted: the global brackets below force its equation
to vanish at that value throughout the real retained hull. Impose
\[
 q_j(t_{S_j},y_j)=0,\qquad j=1,\ldots,m.                    \tag{1}
\]
Each equation is an explicit rational polynomial of fixed degree and
depends on its own dependent coordinate only. Supply valid rational
bounds and brackets for every retained vector in the real hull and every
dependent value in its full interval:
\[
 \partial_yq_j(t,y)\ge\alpha_j>0,\qquad
 q_j(t,\ell_j)\le0\le q_j(t,u_j).                          \tag{2}
\]
Consequently there is a unique root \(y_j=\psi_j(t_{S_j})\) in \(V_j\)
for every real retained vector. Write \(\Psi=(\psi_j)_j\).
The feasible set is exactly \(\{(t,\Psi(t)):t\in X\}\).
There are no additional constraints.

The objective \(F_0(t,y)\) is a sum of explicit rational polynomial
factors of fixed degree. A supplied tree decomposition covers every
objective factor and every constraint scope \(S_j\cup\{y_j\}\).
Replace every dependent coordinate in a bag by its retained support.
Write \(p'\) for the largest resulting bag size. If original bags have
size \(p\) and \(|S_j|\le k\), then \(p'\le p\max(1,k)\).
Running intersection is preserved: each added subtree for a dependent
variable using \(t_i\) meets the original \(t_i\) subtree at a constraint
bag. Assign each dependent-noise unary term to such a bag.

Perturb all coordinates independently from one common finite uniform grid
of half-width \(\sigma>0\):
\[
 F_{\gamma,\eta}(t,y)=F_0(t,y)+\gamma^\top t+\eta^\top y.
 \qquad
 G_{\gamma,\eta}(t)=G_\eta(t)+\gamma^\top t,\quad
 G_\eta(t)=F_0(t,\Psi(t))+\eta^\top\Psi(t).                 \tag{3}
\]
Conditioning on \(\eta\) preserves the original independent linear noise
\(\gamma\) in retained coordinates.

Supply \(L>0\) such that \(\partial_{ii}G_\eta\le L\) throughout the
real retained box, uniformly for \(\eta\in[-\sigma,\sigma]^m\).
Let \(I\) include the explicit input, decomposition, and valid bounds
used here. These are input premises. Independently checkable global
certificates require verifiable proofs of (2) and the derivative bounds,
or their derivation by elementary monomial estimates. Arbitrary
polynomial positivity is not silently checked in polynomial time. Count
the length of supplied bound proofs in \(I\), and require their
verification to take polynomial time in that augmented encoding.

Let \(n\ge1\) be the number of remaining retained coordinates, \(w_i\)
their widths, and \(w_{\max}=\max_iw_i\). A base-computed power of two
\(M\), with \(\log M=\operatorname{poly}(I)\), gives an algorithm that
returns an exact implicit global optimizer on every draw from
\[
 \{-\sigma+2\sigma a/(M-1):a=0,\ldots,M-1\},
\]
with expected bit work
\[
 C_0^{p'}\left[4+\frac{(1+n)Lw_{\max}}{2\sigma}\right]^{p'}
                  \operatorname{poly}(I).                \tag{4}
\]
Polynomial exponents may depend on the fixed original degrees.
No growth, uniqueness, or strict-complementarity premise is supplied.
This is fixed-width expected polynomial work under polynomial numerical
bounds on the displayed ratio. It is not FPT in width or polynomial in
the binary encoding of arbitrary integer widths alone.

The usual output is a verified strongly convex retained-coordinate
patch and the graph equations selecting its dependent coordinates.
Exceptional draws use exact algebraic fallback. The compact successful
descriptor has polynomial length; its global pruning record has the
expected bound (4). Numerical output consists of coordinate enclosures
and feasible implicit points: rational retained coordinates together
with their unique scalar-root equations. Rational ambient feasibility
is not promised. Even one cubic equality can force irrational dependent
coordinates. If no retained coordinate remains, solve the independent
scalar roots directly and evaluate the fixed implicit feasible point.

## 2. Polynomial precision local oracles

At a rational retained query, exact-sign rational bisection solves every
scalar equation to any specified precision. Store rational brackets
\(q_j(t,a)\le0\le q_j(t,b)\). These are checkable using polynomial
evaluation and the global monotonicity premise.

Implicit differentiation gives derivatives through order three.
For example, \(\psi_i=-q_i/q_y\). If \(A_j\ge1\) bounds all relevant
partials of \(q_j\) through order three, safe entry bounds are
\[
 P_1=A_j/\alpha_j,\qquad
 P_2=A_j(1+P_1)^2/\alpha_j,\qquad
 P_3=A_j[(1+P_1)^3+3(1+P_1)P_2]/\alpha_j.                 \tag{5}
\]
Their numerical magnitudes can be large, but their encoding lengths
are polynomial. Use the known denominator floor \(\alpha_j\) in
interval division. Polynomial monomial bounds and these formulas give
uniform rational bounds
\[
 M_1\ge\max\{1,\max_i\sum_k\sup|\partial_{ik}G_\eta|\},
 \quad
 T\ge\max\{1,\max_i\sum_{j,k}\sup|\partial_{ijk}G_\eta|\}.   \tag{6}
\]
Bag values, gradients, and Hessians therefore admit certified rational
approximations in polynomial precision cost. The
[oracle interface](implicit-graph-oracle-interface.md) supplies the
detailed bit and certificate argument.

Curvature is measured after substitution. Ambient diagonal curvature
alone does not suffice: \(y=t\), \(F_0=Hty\) has zero ambient diagonal
curvature but retained curvature \(2H\). Dependent linear noise can
also contribute retained curvature.

## 3. Certified approximate DP and expected cell counts

Use the nested mixed cells and separator-key DP of the box theorem on
the retained box and expanded bags. Let \(h_j=s2^{-j}\), with \(s\) the
least power-of-two integer at least \(\max(1,w_{\max})\).
Integer cells become singleton labels below unit scale.
Sequential mean-preserving endpoint rounding gives true-objective error
\[
                         E_j=nLh_j^2/8.                  \tag{7}
\]
It preserves every bag whitelist and any specified bag cell.

Let \(N\) count cost-owning bags. Evaluate each allowed bag row by a
rational lower cost \(\ell_B\le f_B\le\ell_B+\delta_j\), where
\(D_j=N\delta_j\le E_j\). Refine reused rows each level.
Let \(m_j^-\) be the exact rational DP minimum of these lower costs.
Its recovered implicit feasible witness has upper value
\(m_j^-+D_j\). Maintain the best such upper bound \(U_j\).
For a cell, let \(q_C^-\) be the minimum lower-cost min-marginal over
its corners, and retain it precisely when
\[
                         q_C^- - E_j\le U_j.              \tag{8}
\]
Fixed-cell rounding proves this lower bound; every global optimizer
survives. Moreover,
\[
 f^*\le U_j\le m_j^-+D_j\le f^*+E_j+D_j,
 \quad
 G_{\gamma,\eta}(\text{witness}_C)
 \le q_C^-+D_j\le f^*+4E_j.                                \tag{9}
\]
These are single globally consistent retained-grid witnesses, with
exact implicit dependent roots. All DP comparisons are rational.

Condition on \(\eta\) and retained noise outside a bag. Recourse
minimizes over a fixed original retained mixed box, so its infimum
preserves coordinate upper curvature \(L\).
At comparison spacing \(a_i=h_j\) for continuous coordinates and
\(a_i=\max(1,h_j)\) for integers, (9) confines each regular coefficient
to an interval of length at most \(La_i+8E_j/a_i\).
There are at most three exceptional nodes per coordinate.
The finite-grid interval mass is length divided by \(2\sigma\), plus
\(1/M\). Thus for \(j\le J\), \(M\ge2^J\), the expected qualifying bag
count is at most
\[
 H_B=\prod_{i\in B}
             \left[4+\frac{(1+n)Lw_i}{2\sigma}\right].     \tag{10}
\]
Corner incidences, children and child corners add a constant to the
power \(p'\). Separator-key minima avoid products of adjacent table
sizes. Consequently per-level expected work is
\(C_0^{p'}\sum_BH_B\) times polynomial bit overhead. The bounds are
uniform in \(\eta\), so averaging over it is valid. No conditioning on
previous pruning decisions is used.

## 4. Exact closure with certified derivative approximations

Intersect the retained coordinate hulls. Fix integers only from singleton
hulls. For a rational midpoint \(c\) and largest half-width \(r\),
compute a gradient approximation with entry errors
\(\epsilon_g\le\tau/8\). A strict sign in
\[
 \widehat g_i+[-(M_1r+\epsilon_g),M_1r+\epsilon_g]           \tag{11}
\]
forces the corresponding original continuous retained endpoint.
This rule is not applied to integers.

After all integers and certified continuous bounds are substituted,
record and remove any singleton continuous hull coordinate as well.
Let \(C\) be the remaining retained box, recomputing its midpoint
and radius after these restrictions. Compute a symmetric rational
Hessian approximation with operator error \(\epsilon_H\le g_0/8\).
Accept if
\[
                \widehat H-(Tr+\epsilon_H+g_0)I\succ0.    \tag{12}
\]
This proves uniform reduced Hessian at least \(g_0I\) on \(C\).
The box contains every global optimizer, so its unique constrained
minimizer is globally optimal. Equations (1) specify its dependent
coordinates uniquely. These tests are sound without a growth promise.

For stopping analysis only, suppose the unique retained optimizer has
point growth at least \(g_0\), and all active continuous retained
gradients have magnitude greater than \(\tau\).
Set \(A=2+nL/g_0\). Equation (9) gives witness distance at most
\(h_j\sqrt{nL/(2g_0)}\), and every retained coordinate lies within
\(Ah_j\) of its optimal value. Therefore
\[
 h_j\le\min\{1/(4A),\tau/(4M_1A),g_0/(4TA)\}               \tag{13}
\]
fixes all integers and all active retained bounds. The gradient error
from its optimal value is at most \(2M_1r+2\epsilon_g\le3\tau/4\).
The remaining original-interior face has reduced Hessian at least
\(2g_0I\) by two-sided Taylor expansion. The matrix in (12) is at least
\((g_0-2Tr-2\epsilon_H)I\succeq g_0I/4\).
No full ambient Hessian or generic constrained LICQ claim is needed.

## 5. Finite-law growth and active-gradient tails

Growth is measured in retained coordinates. Conditional on \(\eta\),
the universal linear-tilt tail applies to (3).
Write Graph for retained mixed-box membership, dependent bounds, and (1).
The good-growth event has the two-block formula
\[
 \exists(t,y)\ \forall(t',y'):\quad
 \operatorname{Graph}(t,y)\ \wedge
 \left[\neg\operatorname{Graph}(t',y')\ \vee\
 F_{\gamma,\eta}(t',y')-F_{\gamma,\eta}(t,y)
                       \ge\varepsilon\|t'-t\|^2\right].   \tag{14}
\]
Native integer membership adds label disjunctions but no quantified
blocks. Degree is fixed and the two block sizes are \(O(n+m)\).
The [reviewed finite-tail argument](polynomial-finite-noise-tails.md)
therefore gives a base \(C_{\rm tail}=2^{\operatorname{poly}(I)}\),
uniform in thresholds, all fixed real \(\eta\), and coefficient heights:
\[
 \Pr\{g_*<\varepsilon\mid\eta\}
 \le W\varepsilon/\sigma+2nC_{\rm tail}/M,\quad W=\sum_iw_i.
                                                               \tag{15}
\]

For active-gradient tails, fix integer retained labels, an original
continuous retained face, and one active retained coordinate \(i\).
Condition on \(\eta,\gamma_{-i}\). Let \(u\) be its \(k\) free
retained coordinates and define
\(\mathcal L=F_{\gamma,\eta}+\sum_j\lambda_jq_j\).
The polynomial system
\[
                    q=0,\quad\mathcal L_y=0,\quad
                    \mathcal L_u=0                       \tag{16}
\]
has \(k+2m\) unknowns and is independent of \(\gamma_i\).
Dependent interval bounds remain branch selectors but need no
multipliers: (2) makes them redundant after parameterization.

Here \(q_y\) is diagonal and invertible. Let
\(C_q=[q_u\ q_y]\) and \(Z=[I;-q_y^{-1}q_u]\).
The bordered KKT matrix has blocks
\([H_{\mathcal L},C_q^\top;C_q,0]\).
A kernel vector has \(v=Z\,du\), then
\(Z^\top H_{\mathcal L}Z\,du=H_{\rm reduced}du=0\).
At positive-growth optimizers the reduced Hessian is positive definite;
hence \(du=v=0\), and \(q_y^\top\) forces the remaining multiplier
component to vanish. The KKT root is nonsingular over both real and
complex numbers, even if other components have positive dimension.

Take \(D=\max\{2,d_F,\max_j\deg q_j\}\), where \(d_F\) bounds
the original objective degree. Each multiplier term has degree at most
its constraint degree. This gives at most \(D^{k+2m}\)
nonsingular roots by Bezout. At each fixed root the active derivative
is \(\gamma_i+b\). Thus, writing \(R_Z\) for the number of native
retained label assignments and \(n_c\) for the continuous dimension,
\[
 K=\max\{1,n_c3^{n_c}R_ZD^{n_c+2m}\},\qquad
 \Pr\{g_*>0,\ \text{some active retained gradient has magnitude}
        \le\tau\mid\eta\}\le K(\tau/\sigma+1/M).           \tag{17}
\]
This is an intersection event, not conditioning on positive growth.
The active event is empty when \(n_c=0\).

## 6. Uniform sampling budget and exact exceptional output

Apply the [lexicographic fallback](polynomial-exact-fallback.md) to the
original polynomial graph domain, adding (1) and dependent intervals to
its domain formula. Compactness supplies a canonical optimizer.
Every coordinate and the value have two-block singleton formulas.
The bit bound remains \(B\operatorname{poly}(I+b+q)\), with a base-only
\(B=2^{\operatorname{poly}(I)}\) and sampled coefficient length \(b\).
The reduced algebraic function is not treated as an explicit polynomial
in this invocation.

Before sampling any coefficient choose
\[
 \rho=1/(4B),\quad g_0=\rho\sigma/(2W),\quad
 \tau=\rho\sigma/(2K).                                    \tag{18}
\]
Take the first level \(J\) satisfying (13), then a power of two
\[
 M\ge\max\{2,2^J,4nC_{\rm tail}/\rho,2K/\rho\}.             \tag{19}
\]
All derivative bounds, section counts, KKT degrees and fallback format
bounds are uniform in \(\eta\). Realized dependent coefficients affect
only polynomial height factors. Hence \(J,\log M=\operatorname{poly}(I)\).
One does not treat a sampled \(\eta\) as a new base input and choose
its own noise law.

Equations (15)--(17) bound failure of closure by \(J\) by \(1/(2B)\),
conditional on every \(\eta\), hence unconditionally.
Every failure is solved on the same draw by the exact graph-domain
fallback. Its expected work and output size are polynomial. Summing
(10) over levels and bags proves (4).

## 7. Computational meaning and exact feasibility

On a successful rational retained patch, use rational bounds
\(|G|\le V\) and \(\|\nabla G\|_2\le G_1\).
The capped epigraph is \(G(x)\le t\le V+2\).
For a rational \(x\in C\), obtain a value interval \([\ell,u]\) of
width at most \(\epsilon/2\) and a rational gradient approximation
with infinity error
\(\beta=\epsilon/(2\max(1,\operatorname{diam}_1C))\).
Convexity gives the valid affine underestimate
\[
 \ell+\widehat g^\top(z-x)-\beta\operatorname{diam}_1C
                         \le G(z),\qquad z\in C.          \tag{20}
\]
If it separates the query, normalize its rational normal and return
a strong separator. Otherwise \(G(x)-t\le\epsilon\), proving
\(\epsilon\)-nearness to the capped epigraph.
Outside-box and above-cap queries have exact rational separators.
This is a polynomial-bit weak separation oracle.

Apply the [GLS epigraph repair](convex-patch-evaluation.md), including
erosion control and rational clipping. The resulting retained point
is exactly feasible. Its objective is algebraic, so obtain a rational
upper value with error at most half the requested gap and allocate
the other half to weak optimization. Strong convexity then gives
retained accuracy with polynomial dependence on \(\log(1/g_0)\).

The chart has a rational Lipschitz bound of polynomial encoding length
from (5). It converts retained accuracy to ambient coordinate accuracy.
A rational retained point together with the unique roots (1) is an
exactly feasible implicit original point. The fallback similarly
refines and clips retained coordinates, identifies native integer
labels exactly, and reattaches their graph roots. A reduced-gradient
bound determines sufficient precision for any requested objective gap.
It never rounds dependent coordinates independently while claiming
exact equality feasibility.

Successful patch evaluation costs \(\operatorname{poly}(I+q)\).
Exceptional algebraic evaluation has a base-exponential factor paid
for by the same rare budget. Expanded minimal polynomials and exact
comparison against an arbitrary rational threshold are not promised.

## 8. Dynamics example and limitations

Take state anchors \(s_t\in[-1,1]\), native binary mode anchors \(z_t\),
and dependent controls \(u_t\in[-2,2]\), with
\[
             s_{t+1}=s_t/4+u_t+u_t^3+z_t/2.              \tag{21}
\]
For every allowed pair of states and every real \(z_t\in[0,1]\),
the control equation has derivative at least one and endpoint values
bracketing zero. Fixed initial or terminal states can be substituted.
Stage polynomial costs may depend nonlinearly on states, modes and
controls. Original stage bags have size four; retained stage bags have
size three. The cubic inverse is generally irrational at rational
grid points, so approximate DP and implicit output are necessary for
this proof.

The premise is global solvability in selected coordinates, not merely
local regularity at an unknown optimum. Extra constraints that destroy
the retained product domain, dependent integer restrictions, and
multiple inverse branches are excluded. The
[affine-constraint barrier](constrained-smoothing-barrier.md) explains
why unrestricted sparse coupled constraints cannot inherit the box rate.
The [polynomial graph corollary](smoothed-polynomial-graph-constraints.md)
and [affine-state actuator theorem](smoothed-polynomial-actuator-dynamics.md)
give complementary reductions with rational polynomial evaluations.
The actuator theorem uses affine state costs to preserve unary control
scopes at arbitrary forward depth; direct substitution into the present
chart framework need not preserve that sharper width bound.

## Review and verification

Independent completed-text reviews passed for the
[oracle interface](../reviews/implicit-graph-oracle-review.md),
[finite tails and KKT argument](../reviews/implicit-graph-tail-kkt-review.md),
[full composition](../reviews/implicit-graph-composition-review.md), and
[composition and significance](../reviews/smoothed-implicit-graph-composition-review.md).
The [focused prior-art comparison](../prior-art/implicit-monotone-actuator-prior.md)
distinguishes existing implicit elimination and validated global search
from this quantitative finite-noise composition. It makes no priority claim.

The author ran

```text
python research-20261002/new-direction/check_smoothed_implicit_graph.py
```

The [exact checker](check_smoothed_implicit_graph.py) and
[saved results](smoothed-implicit-graph-check-results.json) cover a
zero-perturbation two-stage cubic-actuator instance with two native binary modes, maximum
retained bag size three, and a known off-grid optimum. Five refinement
stages checked 296 rational lower-cost min-marginals against brute force,
82 consistent witnesses with certified true gap at most \(4E_j\),
120 cell removals preserving the optimum, and 18 rounding atoms.
It certified 81 full-real-hull root brackets, exercised 326 nonpoint root
brackets in value computations, and separately checked 18 value refinements
with nonzero dependent-coordinate noise. After fixing the modes, rational interval
bounds certified that the true algebraic reduced Hessian is at least
\(2I\) on the retained patch. No exact comparison of algebraic sums was
used. An independent actual-code inspection passed without rerunning the
same diagnostic. These finite examples do not test noisy pruning paths,
the generic GLS/fallback routines, or an expected-work bound.

The tail reviewer separately ran the
[KKT diagnostic](../reviews/check_implicit_graph_tail_kkt_review.py):
36 exact bordered-matrix identities, a nonlinear graph case, and 16
finite-law active-gradient strip cases passed. Author document checks
covered local links, whitespace, paired math delimiters, sequential
equation tags and Python syntax for these new artifacts. No index,
project-wide verification or CI inspection was part of this work.
