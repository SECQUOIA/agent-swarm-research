# Endpoint dynamic programming describes every optimal face

Date: 2026-10-02. Complete derivation for coordinatewise concave quadratic
objectives. The endpoint algorithm and Bellman reparameterization are
classical. The result here records their exact full-set certificate on mixed
boxes. Review and diagnostics are in [README.md](README.md).

Let \(F(x)=x^TQx+b^Tx+c\) on a nonempty rational mixed box
\(X=\prod_i X_i\), where \(X_i=[\ell_i,u_i]\) or the integer points
of that interval. Round integer bounds inward, substitute fixed variables,
and assume every remaining diagonal coefficient \(Q_{ii}\le0\).
Let a supplied factor-tree decomposition have \(N\) bags of size at most
\(p\). No optimizer or growth constant is supplied.

**Result.** In \(2^{O(p)}\operatorname{poly}(I)\) bit work, endpoint
dynamic programming computes the exact optimum, an attaining endpoint
assignment, and a compact rational polynomial description of the entire
optimal set. The descriptor may represent exponentially many faces without
enumerating them. The conclusion also covers arbitrarily large integer
intervals: their interior labels are never enumerated.

## 1. Endpoint reduction and Bellman residuals

Each coordinate restriction is concave, so replacing one coordinate by a
minimizing endpoint cannot increase the objective. Repeating this over all
coordinates proves that at least one global optimizer is an endpoint
assignment. Both endpoints are feasible for every integer coordinate after
the preprocessing. This proves equality of the continuous/mixed and binary
endpoint minimum.

Root the decomposition. Write \(B_t\) for a bag and
\(S_t=B_t\cap B_{\mathrm{parent}(t)}\) for its parent separator, empty
at the root. Assign each original factor to one containing bag and call
their sum \(\phi_t\). For endpoint labels, compute exact messages

\[
 m_t(v_{S_t})=\min_{v_{B_t\setminus S_t}}
       \left[\phi_t(v_{B_t})+\sum_{c\text{ child of }t}m_c(v_{S_c})\right].
                                                                    \tag{1}
\]

The root message is the scalar \(f^*\). Define the rational residual table

\[
 r_t(v_{B_t})=\phi_t(v_{B_t})+
       \sum_c m_c(v_{S_c})-m_t(v_{S_t})\ge0.                       \tag{2}
\]

For each global endpoint assignment \(v\), every nonroot message cancels
once positively and once negatively, giving

\[
                      F(v)-f^*=\sum_t r_t(v_{B_t}).               \tag{3}
\]

The exact recurrence and all nonnegativity claims can be checked from
tables of at most \(2^p\) entries per bag. Combining children by addition
does not cause exponential dependence on node degree. Standard traceback
returns an attaining endpoint assignment, proving upper-bound attainment.

## 2. Interpolation identifies the entire optimal set

For \(x\in X\), put

\[
 w_i^{\ell}(x_i)=\frac{u_i-x_i}{u_i-\ell_i},\qquad
 w_i^u(x_i)=\frac{x_i-\ell_i}{u_i-\ell_i},\qquad
 W_t(v;x)=\prod_{i\in B_t}w_i^{v_i}(x_i).
\]

These nonnegative weights are the probabilities of independent endpoint
rounding with mean \(x\). The rounding is an analysis device even when
\(x_i\) is an interior integer label. Its variance is
\((x_i-\ell_i)(u_i-x_i)\), while every cross-term expectation is
unchanged. Taking expectations in (3) yields the exact identity

\[
 F(x)-f^*=
    \sum_t\sum_{v\in\{\ell,u\}^{B_t}}r_t(v)W_t(v;x)
       -\sum_iQ_{ii}(x_i-\ell_i)(u_i-x_i).                       \tag{4}
\]

Every summand in (4) is nonnegative throughout the full box. Consequently
\(x\) is optimal if and only if it is mixed feasible and satisfies

\[
 \begin{aligned}
 (x_i-\ell_i)(u_i-x_i)&=0 &&\text{whenever }Q_{ii}<0,\\
 \prod_{i\in B_t}
 \begin{cases}u_i-x_i,&v_i=\ell_i,\\x_i-\ell_i,&v_i=u_i\end{cases}
 &=0 &&\text{whenever }r_t(v)>0.
 \end{aligned}                                                   \tag{5}
\]

Positive denominators were removed in (5). At most \(N2^p+n\) polynomial
zero constraints occur, each in factored form with degree at most \(p\)
(degree two for the first group). Checking a proposed rational point needs
only these products, the original bounds, and integrality. No polynomial
expansion or union-of-faces enumeration is necessary.

The second line is important when a diagonal is zero: an interior
coordinate can belong to an optimum only if every endpoint assignment in
its independent-rounding support is optimal. Retaining a coordinate merely
because each of its endpoints occurs somewhere among optimal corners is
unsound. In (4), this support condition is enforced locally by nonnegative
Bellman residuals, with running intersection ensuring their global identity.

For example, \(F(x,y)=x+y-2xy\) on \([0,1]^2\) has two optimal
corners \((0,0),(1,1)\), and all four coordinate endpoints occur in
some optimum. Its two positive endpoint residuals give
\(x(1-y)=0\) and \((1-x)y=0\). These exclude every other point;
neither the full square nor the diagonal segment is optimal.

If a variable has negative diagonal curvature, (5) excludes every interior
real or integer label. If its diagonal is zero, the same local support
conditions allow all appropriate continuous or integer interior values.
Purely free coordinates and the zero objective are therefore handled
without any refinement or artificial positive growth parameter.

## 3. Size, interpretation, and limitations

All endpoint table evaluations use rational coefficients and endpoints of
input-bounded length. A common denominator for the quadratic endpoint
evaluations has polynomial bit length in \(I\); every message is a sum
of original assigned factors, so repeated elimination does not multiply
denominators. Residuals and their exact signs have the same polynomial
bit bound. Construction and verification cost
\(2^{O(p)}\operatorname{poly}(I)\).

For continuous boxes, (5) describes a union of coordinate faces. Its number
of components can be exponential even at bag size two: a sum of independent
copies of \(x+y-2xy\) has two optimum corners per copy. Adding free
coordinates gives exponentially many positive-dimensional components.
The polynomial system remains linear in the number of copies. For a mixed
box, intersect the same face description with the specified integer lattice.

This class does not include positive-diagonal tilted flat directions such
as \((x-y)^2\). The [diagonal-certificate class](unknown-growth-diagonal-class.md)
handles some such cases by a different method. Neither theorem solves the
general arbitrary-optimal-set unknown-growth problem.

## 4. Primary comparison

The endpoint reduction is explicit in Del Pia and Khajavirad,
[Treewidth and the complexity of box-constrained quadratic programs](https://arxiv.org/abs/2609.35595),
including the treatment of nonpositive diagonal variables. The min-sum
recurrence is standard tree dynamic programming; see Dechter,
[Bucket elimination: A unifying framework for reasoning](https://ics.uci.edu/~csp/r48b.pdf).
Tree reparameterizations and their exactness also have substantial prior
development; see Wainwright, Jaakkola, and Willsky,
[MAP estimation via agreement on trees](https://willsky.lids.mit.edu/publ_pdfs/179_pub_IEEE.pdf).

Thus finding one endpoint optimum and expressing nonnegative Bellman
residuals are not new mechanisms. Equation (4) combines them with exact
quadratic endpoint variance to record a compact certificate for every
continuous or mixed optimizer, including the strict-diagonal exclusions.
