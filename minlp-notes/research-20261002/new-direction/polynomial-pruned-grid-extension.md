# Pruned coordinate grids for explicit rational polynomial factors

Date: 2026-10-02. Status: passed a
[fresh independent review](../reviews/polynomial-pruned-grid-review.md)
of the completed extension to the actual
[pruned-grid theorem](pruned-coordinate-grid.md). A
[focused prior-art comparison](../prior-art/polynomial-pruned-grid-prior.md)
is available. No priority or polynomial implementation claim is made.

The pruned-grid approximation theorem extends to fixed-degree, explicitly
encoded rational polynomial factors. For a purely native-integer box, the
same approximation algorithm also discovers an exact optimum: refine the
certified objective gap below the common rational spacing of all objective
values. No quadratic-program reconstruction is needed.

The extension requires an independently checked upper-curvature bound on the
full continuous box. It does not provide exact continuous output, and it does
not infer positive quadratic growth from uniqueness of a polynomial minimum.

## 1. Input and curvature verification

Fix a numerical degree bound \(d\ge2\), raising a smaller bound to two. Let

\[
 F(x)=\sum_t f_t(x_{V_t})
\]

be given by explicit monomial lists with rational coefficients and degree at
most \(d\). A supplied tree decomposition has \(N\) bags of size at most
\(p\), and each factor scope is contained in its assigned bag. The feasible
set is a bounded rational product box; each coordinate is continuous or a
native integer. Round integer endpoints inward, reject empty domains, and
substitute fixed coordinates. These operations preserve degree and have
polynomial bit cost. Check the decomposition and factor assignments.

Let \(H\) be the full continuous hull of the resulting mixed box. Accept a
rational \(L>0\) only after verifying

\[
                   \partial_{ii}F(x)\le L
                    \qquad(x\in H,\ i=1,\ldots,n).                 \tag{1}
\]

This includes fractional points between integer labels. Checking (1) only
at feasible integer points is insufficient for the rounding argument.

Here is a concrete polynomial-time curvature check for this input model.
Differentiate the explicit factors twice in coordinate \(i\). Bound each
resulting monomial by rational interval arithmetic on \(H\), multiply by its
signed coefficient, and sum the upper endpoints over all factors. Call the
result \(\widehat L_i\). Accept \(L\) if
\(L\ge\max_i\widehat L_i\). Interval arithmetic may overestimate the
curvature, but every accepted bound is valid; fixed degree makes its work
and rational bit lengths polynomial in the input. If the computed maximum
is positive it can itself be used as \(L\). If every computed upper bound
is nonpositive, separate concavity permits exact endpoint DP with at most
two labels per coordinate, without a growth assumption.

Thus (1) need not be an unchecked promise. This particular check need not
accept every valid sharp bound. Any sharper independently verified bound
may be used, with its verification cost included. All conditioning claims
below concern the bound actually accepted, not the smallest possible
curvature bound. An alternative curvature certificate must have polynomial
verification work, and its length is included in the input. Let \(I\)
include the accepted rational \(L\) and the explicit input; computing it by
the procedure above enlarges the original encoding only polynomially.

For the running-time guarantee, assume an unknown unique optimizer \(x^*\)
and an unknown \(g>0\) such that

\[
 F(x)-F(x^*)\ge g\|x-x^*\|^2\quad(x\in X),
 \qquad \kappa=\max\{1,L/g\}.                                  \tag{2}
\]

The curvature check and certificate verifier do not use \(g\).

**Result.** For fixed \(d\), the algorithm returns a rational feasible
point, a rational lower bound on the original problem, and a certificate
of gap at most \(2^{-q}\), in

\[
                         f_d(p,\kappa)(I+q+1)^C                 \tag{3}
\]

bit operations. The polynomial exponent is independent of \(p\) and
\(\kappa\). If all coordinates are native integers, it discovers an exact
optimum and certifies its value in \(f_d(p,\kappa)(I+1)^C\) bit operations.
Validity of either certificate does not depend on (2).

## 2. The lower bound and interval filtering are not quadratic arguments

Use exactly the grids and unary corrections of the pruned-grid theorem:

\[
 d_i(v)=L\ell_i(v)^2/8,\qquad
 D(y)=\sum_i d_i(y_i),\qquad T(y)=F(y)-D(y).
\]

Here \(\ell_i(v)\) is the largest adjacent grid interval; native-integer
unit intervals are ignored. This convention is valid because they have no
feasible interior integer point.

For any point \(x\) in the current product box, independently round each
coordinate to its enclosing grid endpoints with mean \(x_i\). Conditional
on earlier rounds, (1) and one-dimensional Jensen give

\[
 \mathbb E F(Y)-F(x)\le\frac L2\sum_i\operatorname{Var}(Y_i).
\]

The correction at either endpoint of a genuinely rounded interval of
length \(\Delta\) is at least \(L\Delta^2/8\), which dominates its
\((L/2)\operatorname{Var}(Y_i)\). Consequently

\[
                      \mathbb E T(Y)\le F(x).                   \tag{4}
\]

This is sequential semiconcavity, not cancellation of quadratic cross
terms. It permits arbitrary polynomial interactions inside the supplied
factor scopes.

Exact finite-state DP gives \(b=\min_y T(y)\), a minimizer \(y\), and all
coordinate min-marginals \(m_i(v)=\min_{z:z_i=v}T(z)\). Equation (4) gives
both

\[
 b\le\min_{x\in B}F(x),\qquad
 \min\{m_i(a),m_i(b')\}\le F(x)\quad\text{when }x_i\in[a,b'],   \tag{5}
\]

where \(a,b'\) are adjacent grid labels and \(B\) is the current box.
Retaining an interval exactly when its conditional lower bound is at most
the current feasible incumbent \(U\), then taking coordinate hulls, is
therefore sound. Keep \(U\) nonincreasing. Every optimizer and the incumbent
survive; the corrected-grid minimizer also survives and becomes the next
center.

Two directed passes on the supplied tree compute all min-marginals in
\(O(p(N+\#\mathrm{factors})K^p)\) table operations. Factor evaluation cost
is added below. The unary corrections add no graph edges. Neither the
degree nor the number of occurrences of a variable changes this DP rule.

A certificate must include the successful trial's filtering history.
At the first exclusion of any point, (5) proves that its objective exceeds
that stage's incumbent, hence the final incumbent. The last restricted-box
lower bound consequently remains a lower bound for the original box.
Checking only the final restricted DP would be insufficient.

## 3. Contraction, state caps, and unknown growth

Write \(s=\max_i(b_i-a_i)>0\) for the original effective box width and
\(h_j=s2^{-j}\). Use the original geometric steps with
\(\theta=2^{-\mu}\), \(\mu\ge2\). Their mesh inequality is purely geometric.
For any grid assignment \(z\) and current center \(c\), it gives

\[
 D(z)\le\frac L4nh_j^2+
 \frac{L\theta^2}{2}
       \bigl(\|z-x^*\|^2+\|c-x^*\|^2\bigr).                  \tag{6}
\]

The proofs of contraction and retained-interval localization use only (2),
(5), and (6). They therefore retain every constant in Sections 4--5 of
the pruned-grid theorem. In particular, when
\(\theta^2\le1/(8\kappa)\),

\[
 \begin{split}
 \|y_j-x^*\|^2&\le B_0nh_j^2,
       \qquad B_0=\max\{1,4L/(11g)\}\le\kappa,\\
 U_j-b_j&\le F(y_j)-b_j\le 7Lnh_j^2/8.
 \end{split}                                                    \tag{7}
\]

Retained continuous intervals lie within
\(5\sqrt{n\kappa}\,h_j\) of the new center. Native-integer intervals need
the additional physical radius \(1\). Omitting that term would invalidate
the count when a unit interval survives through a good endpoint.
The next stage still has the same cap

\[
               K_\mu=100\,2^\mu\lceil\log_2(n+2)\rceil.        \tag{8}
\]

For \(\varepsilon=2^{-q}\), use the original stage budget

\[
 J=\max\left\{0,
   \left\lceil\tfrac12\log_2
       \frac{7Lns^2}{8\varepsilon}\right\rceil\right\}.          \tag{9}
\]

Compute it by rational comparisons with powers of four. This handles the
initial-stage case \(J=0\) as well. It is \(O(I+q+1)\) with the accepted
\(L\) included in the input.

Restart each trial from the original box. Abort during grid generation
before a coordinate exceeds (8), before allocating its DP tables. Stop
only when the globally certified gap satisfies \(U-b\le\varepsilon\).
The first trial with \(\theta^2\le1/(8\kappa)\) has
\(2^\mu\le6\sqrt\kappa\), never exceeds the cap, and succeeds by stage
\(J\). Earlier trials are sound but may fail to filter; the cap is what
prevents them from paying an accuracy-dependent power \(q^p\).

The absorption
\(\lceil\log_2(n+2)\rceil^p\le(C_0p)^p(n+2)\) and the capped trial
schedule give the same FPT table count as before. No quadratic expansion
has entered this reasoning. Without growth, the sufficiently fine-trial
termination argument in Section 6 of the predecessor still applies, but
it gives no conditioning-dependent FPT rate.

## 4. Polynomial evaluation and the common denominator

After preprocessing, choose a common integer denominator \(D\) for the
explicit coefficients, remaining endpoints, and \(L\). Its bit length is
polynomial in \(I\). For a fixed trial take \(K=K_\mu+1\), allowing the
one extra candidate that can detect an abort. The existing geometric-grid
induction gives a common denominator for every stage-\(j\) coordinate:

\[
                          A_j=D2^{j+\mu K}.                     \tag{10}
\]

The induction depends only on geometric offsets, inherited centers and
endpoints, and integer steps. It is independent of the objective degree;
denominators do not multiply across refinement stages.

A monomial of degree at most \(d\), evaluated at these coordinates, has
denominator dividing \(DA_j^d\). Including the unary corrections, all
factor values and table entries have denominator dividing

\[
                         C_j=8D A_j^{\max\{d,2\}}.              \tag{11}
\]

The original bounded box bounds coordinate magnitudes. Explicit coefficient
lengths and the number of terms then give bit lengths
\(O(d(I+j+\mu K)+\operatorname{poly}(I))\). Messages and min-marginals
are sums, differences, and selections of values with denominator (11);
they do not introduce products of unrelated denominators across bags.
Their numerator bounds add only the input's factor-count allowance.

Evaluating the explicit factors adds polynomial work in their input size,
numerical degree, and these bit lengths per table assignment. Fixed degree
therefore proves (3). Unary-encoded numerical degree also suffices, with
degree charged to the input length. A bare sparse representation with
arbitrarily large binary-encoded exponents does not suffice: for example,
\(x^2-\tfrac12x^{2^k}+y^2\) on \([0,1]^2\) has bounded upper curvature
and growth but exponentially long exact rational values at fixed fractional
grid points. General arithmetic circuits need separate output-size and
comparison guarantees even when their degree is small.

## 5. Exact discovery on native integer boxes

Suppose now that every original coordinate is a native integer. Let \(Q\)
be a common positive denominator of the **original objective coefficients**,
including constants. Taking their least common multiple or product gives
\(\log Q=O(I)\). At every feasible integer point,

\[
                            QF(x)\in\mathbb Z.                 \tag{12}
\]

Substituting fixed integer coordinates preserves this property. This
denominator comes from the original polynomial, not from the grids,
penalties, messages, or refined endpoints.

Choose \(q=1+\lceil\log_2 Q\rceil\) and run the approximation algorithm.
Its accepted incumbent and global lower bound satisfy

\[
                      U-b\le2^{-q}\le1/(2Q)<1/Q.               \tag{13}
\]

If a better integer point existed, (12) would force its value to be at
most \(U-1/Q<b\), a contradiction. Equivalently, rounding the certified
lower bound upward to the value lattice gives
\(\lceil Qb\rceil/Q=U=f^*\). Check the incumbent's original bounds and
integrality, its exact objective value, the common denominator, and the
pruning certificate. These checks prove exact global optimality without
knowing \(g\), reconstructing coordinates, or assuming a rational-height
theorem for continuous polynomial optima.

Here \(q=O(I)\), so (3) gives the claimed exact FPT bound. The algorithm
discovers its incumbent; no proposed optimizer is an input. Every unique
minimum on a finite integer box has some positive \(g\), although it may
be extremely small. With ties, (13) remains a sound exact stopping rule and
general approximation termination still applies; the point-growth FPT
analysis above does not supply a bound for that case.

### A verified growth margin after discovery

For a unique native-integer optimum satisfying (2), compose the exact
discovery algorithm with the reviewed
[polynomial shell certificate](nonlinear-shell-certificate.md), using the
returned optimizer as its proposed point. Its integer coordinates have
polynomial encoding length because they lie in the original bounded box.
The same factors, supplied bags, physical metric, and verified \(L\) apply.
There is no continuous Taylor core in this case.

The shell checks succeed whenever \(\sigma\le g/3\). Starting at
\(\sigma=L/32\) and dividing it by four at each failed trial therefore
returns an independently verified margin satisfying
\[
 F(x)-f^*\ge\sigma\|x-x^*\|^2\quad(x\in X),\qquad
 \frac L\sigma\le\max\{32,12L/g\}.                              \tag{14}
\]
The discovery and shell searches together still take
\(f_d(p,\kappa)\operatorname{poly}(I)\) bit work, without receiving
\(g\). This composition supplies an exact optimizer and value together
with a checked physical growth margin. It adds no new optimization
mechanism beyond the two reviewed algorithms.

## 6. Rational lattices and continuous exact output

The theorem above uses native integer steps. Replacing physical lattice
coordinates by \(x_i=\alpha_i+h_i z_i\) does not preserve the conditioning
parameter automatically. Taking \(h_i=1\) for any unscaled continuous
coordinates, it gives upper curvature at most
\(L\max_i h_i^2\) and a growth lower bound
\(g\min_i h_i^2\). The resulting bound on the ratio can contain
\((\max_i h_i/\min_i h_i)^2\), which is not a parameter-free change.

To retain the physical metric, a rational-lattice extension needs explicit
grid steps

\[
 h_i\max\{1,\lfloor(h_j+\theta t)/h_i\rfloor\},
\]

zero corrections for single-lattice-step intervals, a retained radius
\(h_i+5\sqrt{n\kappa}\,h_j\), and the coordinate-specific counting scale
\(\max\{h_{j+1},h_i\}\). The denominator and floor-operation audit must
then include the lattice data. These are additional proof obligations;
the native-integer statement does not silently implement them.

The objective-spacing part itself extends after the formal substitution
\(x_i=\alpha_i+h_i z_i\): at fixed degree, the resulting explicit rational
polynomial has polynomial encoding length and a common coefficient
denominator \(Q_{\rm lat}\) with polynomial bit length. Once a certified
physical-lattice approximation algorithm is available, a gap below
\(1/Q_{\rm lat}\) suffices for exactness. Fixed continuous coordinates,
if substituted before a remaining integer problem is treated, similarly
require the denominator of that reduced objective.

No exact continuous or mixed continuous/integer output theorem follows
from (12). Even \(F(x)=x^3-6x\) on \([1,2]\) has a unique minimizer
\(\sqrt2\), optimum value \(-4\sqrt2\), valid growth \(g=3\), and upper
curvature \(L=12\). Rational-QP reconstruction cannot simply be reused.
Moreover, uniqueness alone need not give positive polynomial growth:
\(x^4\) on \([-1,1]\) has a unique minimum and no positive quadratic
growth constant. The mixed approximation result retains assumption (2).

## 7. Audit scope

This derivation checked the actual pruned-grid note, the semiconcave
rounding theorem, and the existing mathematical and bit audits. The
quadratic-specific parts replaced here are the easy diagonal-curvature
check, the degree-two evaluation denominator, and the exact-output step.
The QP assertion that uniqueness automatically supplies positive growth
is not carried over to continuous polynomial problems.

The targeted command `python - <<'PY'` checked this document's trailing
whitespace, paired math delimiters, and local links; all passed. No
optimization executable, project-wide check, CI inspection, external search,
or index update was performed. The result here is a mathematical extension,
not a new implementation.
