# Certified nonlinear and mixed-integer recourse with few nonconvex directions

Date: 2026-10-02. Status: mathematical derivation with independent review.
This extends the [quadratic reduction](negative-inertia-qp.md) to
certified approximate convex recourse. The concrete specialization below
covers separable quartic objectives with a low-rank negative quadratic
term on mixed continuous-integer product boxes. The number of integer
coordinates is unrestricted, and interval endpoints are binary encoded.
No claim of publication priority is made.

## What changes beyond quadratic programming

The fixed-domain lifting and growth argument do not require a quadratic
convex part. The exact rational optimizer oracle does. Replacing that
oracle by certified intervals preserves the controlled subdivision count
if its accuracy improves proportionally to the square of the mesh size.
The resulting theorem gives certified approximation, not exact rational
optimization. It does not assume that arbitrary convex optimization has
a polynomial-bit algorithm.

Let \(X\) be a nonempty compact set and let \(G\) be continuous
on \(X\). Write

\[
 F(x)=G(x)-\frac\alpha2\|Tx\|^2,\qquad \alpha>0,
 \tag{1}
\]

where the supplied rational matrix \(T\) has \(r\) rows and
\(\alpha\) is rational. A rational box containing \(TX\)
is supplied or computed by a separate certified procedure. Constant
coordinates may be removed. Suppose all optimizers have the same image
\(t^*\), and

\[
 F(x)-F^*\ge g_T\|Tx-t^*\|^2,\qquad g_T>0.
 \tag{2}
\]

Define

\[
 Q(a,x)=G(x)-\alpha a^TTx+\frac\alpha2\|a\|^2,
 \qquad W(a)=\min_{x\in X}Q(a,x).
 \tag{3}
\]

The feasible set of this inner minimization is fixed. When \(X\)
and \(G\) are convex, this is a convex optimization problem. The
identities below also hold for nonconvex \(X\); the separate oracle
contract then becomes decisive. As in the quadratic proof,

\[
 Q(a,x)=F(x)+\frac\alpha2\|a-Tx\|^2,
 \quad \min W=F^*,\quad
 W(a)-F^*\ge g_W\|a-t^*\|^2,
 \quad g_W=\frac{g_T\alpha}{2g_T+\alpha}.
 \tag{4}
\]

Also \(W(a)-\alpha\|a\|^2/2\) is concave. Neither a smooth
value function nor a unique inner optimizer is needed. Continuity on
compact \(X\) ensures the minima used here are attained.

## The certified oracle contract

For rational \(a\) and rational tolerance \(\eta>0\), the
oracle must return rational \(l,u\) and a represented feasible
witness \(x\in X\) satisfying

\[
 l\le W(a)\le Q(a,x)\le u,
 \qquad u-l\le\eta.
 \tag{5}
\]

In particular \(F(x)\le u\). This is stronger than returning an
approximate objective value without a certified lower bound or feasible
witness. Witness representation and feasibility certification are part
of the contract; they are not automatic for an arbitrary convex set.
All complexity claims below explicitly charge this oracle's cost.

## Refinement with inexact values

Use nested isotropic cells of maximum side length
\(h_j=s2^{-j}\), as in the quadratic theorem. Put

\[
 \delta_j=\frac{r\alpha h_j^2}{8},
 \qquad \eta_j=\min(1,\delta_j).
 \tag{6}
\]

Evaluate the corners of every cell generated at the current level with
tolerance \(\eta_j\). A reused corner needs a sufficiently accurate
certificate at this level. Old incumbents remain valid without another
oracle call; one need not reevaluate all historical corners.
If \(r=0\), or every projection coordinate is constant, one inner
oracle call at the fixed projection and target tolerance suffices.

For a cell \(B\), let \((l_v,u_v,x_v)\) denote its corner
certificates, and set

\[
 L_B=\min_{v\in\operatorname{vert}(B)}l_v-\delta_B,
 \qquad \delta_B=\frac\alpha8\sum_i\operatorname{width}_i(B)^2.
 \tag{7}
\]

Concavity in (4) makes \(L_B\) a valid lower bound for \(W\)
on \(B\). Keep the smallest upper certificate \(U\) seen so
far and its original-feasible witness. Retain precisely the cells with
\(L_B<U\), using the final incumbent after every corner call at
that level has completed. If none remain, the incumbent is exact. Otherwise
the incumbent and retained lower bounds certify

\[
 L:=\min\bigl(U,\min_{B\text{ retained}}L_B\bigr)
 \le F^*\le F(x_{\mathrm{inc}})\le U,
 \qquad U-L\le\delta_j+\eta_j\le2\delta_j.
 \tag{8}
\]

Indeed, a corner minimizing \(l_v\) supplies
\(U\le u_v\le l_v+\eta_j=L_B+\delta_B+\eta_j\).
Pruned regions remain irrelevant when the incumbent improves.

If \(U>F^*\), a cell containing \(t^*\) survives. Its
upper-curvature inequality guarantees a corner with
\(W(v)\le F^*+\delta_j\), so
\(U\le F^*+\delta_j+\eta_j\). The same bound is immediate
when \(U=F^*\). A retained cell's corner minimizing \(l_v\)
therefore satisfies

\[
 W(v)\le l_v+\eta_j
 <F^*+2(\delta_j+\eta_j)
 \le F^*+4\delta_j.
 \tag{9}
\]

Growth puts that corner within
\(h_j\sqrt{r\alpha/(2g_W)}\) of \(t^*\). The lattice
packing bound consequently permits at most

\[
 2^r\bigl(\sqrt{2r\kappa_W}+4\bigr)^r,
 \qquad \kappa_W=\alpha/g_W=2+\alpha/g_T,
 \tag{10}
\]

retained cells at every level. Generating children and evaluating their
corners only multiplies this bound by a function of \(r\).
Neither pruning nor stopping needs the unknown growth constant.

## Oracle calls, precision, and bit complexity

For target gap \(\varepsilon\), it suffices to choose \(J\)
with \(2\delta_J\le\varepsilon\). Thus the number of oracle
calls is at most

\[
 f(r,\alpha/g_T)(J+1),\qquad
 J=O\!\left(1+\log_+\frac{r\alpha s^2}{\varepsilon}\right).
 \tag{11}
\]

With rational supplied data of bit length \(I\) and
\(\varepsilon=2^{-q}\), the required corner bit lengths and
\(\log_+(1/\eta_j)\) are \(O(I+q+1)\). If the oracle has
a uniform polynomial bit bound in its instance size, corner encoding
length, and requested precision, the complete algorithm has bit bound
\(f(r,\alpha/g_T)\operatorname{poly}(I+q+1)\).
Without that oracle bound, (11) is an oracle-call theorem only.

Full-vector growth \(g\) at a unique optimizer is sufficient:
the same proof gives
\(\kappa_W=2+\alpha\|T\|_2^2/g\). Unlike the quadratic
case, uniqueness alone need not imply quadratic growth. For example,
\(x^4\) on \([-1,1]\) has a unique minimizer but no positive
quadratic-growth constant at zero.

## A concrete nonlinear family with a polynomial-bit oracle

Let \(X=\prod_i[\ell_i,u_i]\) be a rational box and let

\[
 G(x)=\sum_{i=1}^n
       \left(\lambda_i x_i^4+\frac{\mu_i}{2}x_i^2+b_ix_i+c_i\right),
 \qquad \lambda_i,\mu_i\ge0,
 \tag{12}
\]

with rational coefficients. Let \(T\) and \(\alpha>0\) be
rational. The inner objective (3) separates into convex univariate
quartics with shifted linear coefficients
\(b_i-\alpha(T^Ta)_i\). Its certified oracle can be implemented
using rational bisection alone:

1. If the derivative at the lower endpoint is nonnegative, choose that
   endpoint exactly. If the derivative at the upper endpoint is
   nonpositive, choose the upper endpoint exactly.
2. Otherwise bracket a derivative root and bisect using exact rational
   derivative signs. For \(B_i=\max(|\ell_i|,|u_i|)\), the
   second derivative is bounded by
   \(M_i=12\lambda_i B_i^2+\mu_i\).
3. If the final root bracket has width \(w_i\), its rational
   midpoint \(z_i\) has objective error at most \(M_iw_i^2/8\).
   This follows from Taylor's theorem at a stationary minimizer and
   \(|z_i-x_i^*|\le w_i/2\). Continue until that error is at
   most \(\eta/n\).

The vector \(z\) is box-feasible. Exact rational evaluation gives
\(u=Q(a,z)\), and subtracting the sum of the coordinate error
bounds gives \(l\). These satisfy (5). Coordinates solved at an
endpoint contribute zero error. If \(M_i=0\), the objective is
linear and an endpoint rule already applies. The number of bisections,
integer sizes, and rational evaluations are polynomial in the original
input, the encoding length of \(a\), and
\(\log_+(1/\eta)\). This establishes a polynomial-bit oracle
for this family without invoking an unspecified general convex solver.

### Arbitrarily many integer coordinates

Now restrict any subset of the coordinates to integers. Its feasible
integers have lower and upper bounds
\(L_i=\lceil\ell_i\rceil\), \(U_i=\lfloor u_i\rfloor\),
requiring \(L_i\le U_i\). The feasible set remains compact, and
the oracle still separates by coordinate. For an integer coordinate,
write \(\phi_i\) for its shifted convex quartic and consider

\[
 \Delta_i(k)=\phi_i(k+1)-\phi_i(k).
\]

Convexity makes \(\Delta_i\) nondecreasing. Binary search for
the first \(k\in\{L_i,\ldots,U_i-1\}\) with
\(\Delta_i(k)\ge0\). If one exists, that \(k\) is an exact
integer minimizer; if none exists, choose \(U_i\). A singleton
interval needs no search. The search uses
\(O(1+\log(U_i-L_i+1))\) exact rational evaluations. A concise
optimality certificate is the chosen integer together with the two
available neighbor signs: \(\Delta_i(k-1)\le0\) when
\(k>L_i\), and \(\Delta_i(k)\ge0\) when \(k<U_i\).

Integer coordinates contribute zero oracle error. Apply the preceding
derivative bisection only to continuous coordinates and add their error
bounds. Quartic evaluation at a binary-encoded integer has polynomial
bit cost, even when the interval contains exponentially many integers.
Thus the full mixed recourse oracle retains a uniform polynomial bit
bound. Convexity of the feasible set is not used in (4) or (7)--(10).

Combining (11) and (12), separable convex quartics with a supplied
rank-at-most-\(r\) negative quadratic term on these mixed product
boxes admit certified global approximation in
\(f(r,\alpha/g_T)\operatorname{poly}(I+q+1)\) under (2).
The ambient dimension, including the number of integer coordinates,
appears only in the polynomial factor. Dense low-rank interactions
through \(T\) are allowed. This is a structured MINLP result: the
integer domains need not be enumerated, while continuous inner
minimizers may be irrational. Separability is needed for the recourse,
not for the original objective, whose negative quadratic term can couple
every pair of variables.

### Exact optimization when all coordinates are integer

If every coordinate is integer, expand (1) and choose a common positive
denominator \(D\) for its rational coefficients. The product of
their denominators suffices and has polynomial bit length. Every feasible
objective value lies in \(D^{-1}\mathbb Z\). Run the algorithm
until the certified gap is strictly less than \(1/D\). Its stored
integer witness must then be globally optimal, because

\[
 0\le F(x_{\mathrm{inc}})-F^*\le U-L<1/D.
\]

Its exact objective can be evaluated rationally. Choosing
\(q=\lceil\log_2 D\rceil+1\) requires only polynomial
additional accuracy bits. Consequently the pure integer specialization
has exact running time
\(f(r,\alpha/g_T)\operatorname{poly}(I)\) under (2).
There is no need to reconstruct auxiliary coordinates. The proof applies
even though the stored upper certificate bounds the joint objective:
it also bounds the original witness value by (5).

For example, \(F(x)=x^4-x^2\) on \([0,1]\) fits (12) with
\(T=1\) and \(\alpha=2\). Its unique optimizer is
\(x^*=1/\sqrt2\), and

\[
 F(x)-F^*=(x-x^*)^2(x+x^*)^2
          \ge\tfrac12(x-x^*)^2.
\]

Thus its nonconvexity-to-growth ratio is bounded, but no exact rational
optimizer exists. The approximation theorem has the right output
contract; the quadratic theorem's rational reconstruction does not
extend unchanged. This example illustrates the output distinction,
not a difficult benchmark.

## Scope

The concrete MINLP result requires a product domain and separable convex
recourse. General linear constraints connecting the integer coordinates
would destroy that elementary oracle, and are not covered by its
polynomial-bit proof. Other fixed-domain recourse classes can use the
oracle-call theorem only after establishing the certificate contract and
their own cost bounds. No exact rational-optimizer claim is made when
continuous quartic coordinates remain.

The main safeguards are substantive: certified lower bounds, feasible
witnesses, precision improving with the mesh, and quantitative projected
growth. Omitting any of them is not justified by the proof. No claim is
made for an arbitrary convex function presented only by a numerical
evaluation routine.

## Verification

An independent reviewer checked the inexact-value inequalities, the
retained-cell count, the continuous and integer quartic oracles, and
pure-integer exact recovery. The review identified the
need to require attainment and to reevaluate only corners used at the
current level, rather than every historical corner; both are explicit
above. It also required pruning against the completed level's incumbent
and direct treatment of a constant projection, both now explicit.

The targeted command
`python research-20261002/new-direction/check_approximate_recourse.py`
passed using exact Python rational arithmetic:

- 100 integer oracle cases matched exhaustive optimization on small
  integer intervals, including affine and quadratic degeneracies.
- A mixed two-variable quartic with a dense rank-one interaction and an
  irrational continuous optimizer passed ten levels, 82 oracle calls,
  and every per-level objective interval and mesh-error check.
- A pure integer quartic over \(2^{40}+1\) feasible integers returned
  the exact optimizer after 41 levels and 166 oracle calls. Its final
  certificate gap was strictly below its objective lattice spacing
  \(1/3\), as required by the recovery argument.

These checks exercise the oracle certificates and approximate-value
refinement; the mathematical arguments establish the general bounds.
The scoped command
`git diff --check -- research-20261002/new-direction/approximate-convex-recourse.md research-20261002/new-direction/check_approximate_recourse.py`
passed, as did a targeted `python - <<'PY'` check of whitespace,
paired mathematical delimiters, and local file references.
No project-wide checks or CI inspection were performed.
