# A dual-completion tax on a sparse box LP

Status: Candidate exact synthesis; independently hostile-audited, targeted literature screen complete  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the calculation; novelty priority remains provisional

## Main conclusion

The dyadic multiscale box LP from
[A sharp centrality tax on a row-one-sparse box LP](2026-09-04-sparse-box-lp-geodesic-centrality-tax.md)
has sharply different movement laws in its restricted primal metric and in
the standard primal--dual metric of its sparse orthant formulation.

Write the box by nonnegative slacks
\[
 u_i=1+x_i,\qquad v_i=1-x_i,\qquad u_i+v_i=2,
 \qquad i=1,\ldots,r.                                      \tag{1}
\]
Every equality row has two nonzeros and every slack column has one.  Use the
standard logarithmically homogeneous barrier
\[
 \mathcal F(u,v)=-\sum_{i=1}^r(\log u_i+\log v_i),
 \qquad \nu=2r.                                             \tag{2}
\]
On the affine slice (1), this is the restricted box barrier
\[
 F(x)=-\sum_i\log(1-x_i^2)                                  \tag{3}
\]
up to an additive constant.  Let \(w_i=2^{-A_i}\),
\(T=A_r\log2=\Theta(r)\), and
\(\epsilon_r=re^{-T}=\exp[-\Theta(r)]\), exactly as in the companion
construction.  Start at the finite primal--dual central point with
\(\eta_0=1\), and set the terminal gap threshold to
\(2\epsilon_r=2re^{-T}\).  The exact central point at
\(\eta_1=e^T\) attains this threshold.

For every fixed \(0<R<1\), the optimal numbers of forward \(R\)-Dikin
chords obey
\[
 \begin{array}{c|c}
 \text{geometry and endpoint contract}&\text{optimal chord count}\\ \hline
 \text{restricted primal, arbitrary path}
     &\Theta_R(r\sqrt{\log r})\\
 \text{restricted primal, exact central path}
     &\Theta_R(r\log r)\\
 \text{combined primal--dual, arbitrary feasible gap output}
     &\Theta_R(r^{3/2})\\
 \text{combined primal--dual, exact central path}
     &\Theta_R(r^{3/2}).
 \end{array}                                                \tag{4}
\]
The restricted-primal rows use the fixed endpoints \(x(0)\) and \(x(T)\).
The arbitrary combined-metric row instead minimizes over all strictly
feasible primal--dual endpoints of gap at most \(2\epsilon_r\).
The two combined-metric rows have the same order because an elementary
dual-slack log-distance argument lower-bounds distance to the **entire**
feasible gap sublevel, while the constant-speed central path supplies a
matching route.  The new point of (4) is the exact sparse
multiscale comparison: requiring a feasible primal--dual gap certificate,
rather than only the primal endpoint, raises the optimal movement by
\[
 {\Theta(r^{3/2})\over\Theta(r\sqrt{\log r})}
       =\Theta\!\left(\sqrt{r/\log r}\right).               \tag{5}
\]
It also raises movement relative to primal central tracking by
\(\Theta(\sqrt r/\log r)\).  Thus the dual variables do more than remove
the primal \(\sqrt{\log r}\) centrality tax: for this formulation they
introduce a larger polynomial completion cost.

With ordinary rational encoding, the input length is \(L=\Theta(r^2)\).
The three scales in (4) become
\[
 \Theta(\sqrt{L\log L}),\qquad
 \Theta(\sqrt L\log L),\qquad
 \Theta(L^{3/4}),                                           \tag{6}
\]
respectively.  This is a bounded-movement theorem for a named formulation
and metric.  It is not by itself a runtime or quantum-query lower bound.

## 1. Exact central speed allocation

After changing signs isometrically, take the objective
\(-\sum_iw_ix_i\).  Put \(s=\log\eta\) and
\[
 q(z)={z\over1+\sqrt{1+z^2}}.
\]
The primal projection of the exact central path is
\[
                 x_i(s)=q(e^{s-a_i}),\qquad a_i=-\log w_i. \tag{7}
\]
For clarity, the standard-form costs of \((u_i,v_i)\) are
\((-w_i/2,w_i/2)\).  If \(\alpha_i,\beta_i>0\) are the corresponding dual
slacks, dual feasibility and central complementarity read
\[
                 \beta_i-\alpha_i=w_i,\qquad
                 u_i\alpha_i=v_i\beta_i=e^{-s}.
\]
Thus the convention here is \(\eta=e^s=1/\mu\), and the central duality gap
is \(\sum_i(u_i\alpha_i+v_i\beta_i)=2re^{-s}\).
The general primal--dual speed-splitting identity for a
\(\nu\)-logarithmically homogeneous barrier says
\[
 \|\dot z_{\rm P}(s)\|_{\rm P}^2+
 \|\dot z_{\rm D}(s)\|_{\rm D}^2=\nu,                      \tag{8}
\]
where the dot is \(d/ds\).  Direct scalar differentiation gives the sharper
coordinate formula
\[
 \begin{aligned}
 q_{\rm eff}(s)
   &:=\|\dot z_{\rm P}(s)\|_{\rm P}^2\\
   &=\sum_{i=1}^r\left(1-{1\over
                 \sqrt{1+e^{2(s-a_i)}}}\right),\\
 \|\dot z_{\rm D}(s)\|_{\rm D}^2
   &=2r-q_{\rm eff}(s),\\
 \|(\dot z_{\rm P}(s),\dot z_{\rm D}(s))\|_{\rm PD}^2
   &=2r.                                                     \tag{9}
 \end{aligned}
\]
Indeed, the squared restricted-Hessian speed of one coordinate is
\[
 {2(1+x_i^2)\over(1-x_i^2)^2}\dot x_i^2
       =1-{1\over\sqrt{1+(\eta w_i)^2}}.                    \tag{10}
\]
Equation (8) then supplies the dual identity.  Notice the structural
asymmetry
\[
                    0\le q_{\rm eff}(s)\le r,
 \qquad \|\dot z_{\rm D}(s)\|_{\rm D}^2\ge r.              \tag{11}
\]
Even after every primal coordinate has become active, the equality
constraints leave at least one unit of dual radial speed per box
coordinate.

Integrating the last line of (9) over \(0\le s\le T\) gives the exact
combined central arclength
\[
                  \widehat L_{\rm CP}=\sqrt{2r}\,T
                         =\Theta(r^{3/2}).                  \tag{12}
\]
The terminal primal point is actually \(\epsilon_r\)-accurate because
\[
 \sum_iw_i[1-q(e^{T-a_i})]\le re^{-T}=\epsilon_r.           \tag{13}
\]
The terminal primal--dual gap is exactly
\[
                         {2r\over e^T}=2\epsilon_r.         \tag{14}
\]

## 2. Exact combined bounded-movement order

Let \(\widehat d\) denote Riemannian distance in the product of the primal
and conjugate-dual barrier metrics, let \(z^c(s)\) denote the exact
primal--dual center, and let
\[
 \mathcal G_T=\{z:\ z\text{ is strictly primal--dual feasible and }
                         \operatorname{gap}(z)\le2\epsilon_r\}.
\]
At the initial center, the dual equations above give
\[
 {1\over\alpha_i^0}+{1\over\alpha_i^0+w_i}=2.
\]
Because \(0<w_i\le1\) and the left side is decreasing in \(\alpha_i^0\),
\(\alpha_i^0\ge1/\sqrt2\).  At any \(z\in\mathcal G_T\), weak duality and
the standard-form equations give
\[
 \operatorname{gap}(z)
   =\sum_i(u_i\alpha_i+v_i\beta_i)
   =\sum_i(2\alpha_i+v_iw_i).
\]
All terms are nonnegative, so \(\alpha_i\le\epsilon_r\) for every \(i\).
The dual orthant metric is Euclidean in the log coordinates.  Projecting a
product path onto only its \(\alpha\)-coordinates therefore proves
\[
 \widehat d\bigl(z^c(0),z\bigr)
 \ge\left(\sum_i\log^2{\alpha_i^0\over\alpha_i}\right)^{1/2}
 \ge\sqrt r\left[T-\log r-\tfrac12\log2\right]_+.          \tag{15}
\]
Taking the infimum over \(z\in\mathcal G_T\) preserves the final bound.
For a standard self-concordant metric, a forward chord satisfying
\(\|z_{k+1}-z_k\|_{z_k}\le R<1\) has Riemannian length at most
\(-\log(1-R)\).  Therefore every path, even one allowed to leave the
primal--dual feasible affine spaces between its endpoints, needs at least
\[
 N_{\rm PD}^\star
 \ge {\sqrt r\,[T-\log r-\tfrac12\log2]_+
        \over-\log(1-R)}.                                   \tag{16}
\]
Here only the initial point and the final strictly feasible gap certificate
are prescribed; the final point need not be central.  Restricting intermediate
points to the primal--dual feasible affine spaces only narrows the admissible
class.

Conversely, partition the exact central arc into pieces of length at most
\(\log(1+R)\).  The lower chord comparison
\(d(z,z')\ge\log(1+\|z'-z\|_z)\) makes every resulting forward chord
an \(R\)-Dikin chord.  Hence
\[
 N_{\rm PD}^{\rm CP}
 \le\left\lceil{\sqrt{2r}\,T\over\log(1+R)}\right\rceil.   \tag{17}
\]
Since \(T=\Theta(r)\), equations (12), (16), and (17) prove both combined
rows of (4), including
constant-factor optimality of central tracking even when the competitor may
choose any finite strictly feasible endpoint in the whole target gap
sublevel.

## 3. Comparison with the restricted primal geometry

The companion box theorem proves, from the exact coordinate flattening
\[
 \rho(x)=\int_0^x{\sqrt{2(1+t^2)}\over1-t^2}\,dt,           \tag{18}
\]
that the restricted primal distance between the projections of the same
two finite central endpoints is
\[
 d_F(x(0),x(T))=\Theta(r\sqrt{\log r}).                     \tag{19}
\]
That theorem is stated from the analytic center.  Replacing it by \(x(0)\)
changes the distance by only \(O(1)\): \(a_1=0\), while
\(a_i=\Theta(r)\) for \(i\ge2\), so the initial \(\rho\)-vector has bounded
norm.  The companion theorem ends at its first accurate parameter
\(s_\epsilon\in(T-1,T]\); the remaining central segment has length at most
\(\sqrt r\,(T-s_\epsilon)\le\sqrt r\), which is lower order than
\(r\sqrt{\log r}\).  The exact primal central arclength on
\(0\le s\le T\) is
\[
 \int_0^T\sqrt{q_{\rm eff}(s)}\,ds=\Theta(r\log r),         \tag{20}
\]
because deleting the negative-\(s\) tail changes the audited length by only
\(O(1)\), while replacing \(s_\epsilon\) by \(T\) changes it by at most
\(\sqrt r\).  Endpoint distance and the two chord comparisons prove the
arbitrary-path row and the central-path upper bound.  The matching
\(\Omega_R(r\log r)\) central-path lower bound is the companion theorem's
discrete threshold-potential argument; prepending the \(O(1)\)-length
negative-\(s\) central tail transfers it from the analytic center to
\(x(0)\), and its endpoint-driven form applies because \(x(T)\) is actually
\(\epsilon_r\)-accurate.

Combining (9), (12), and (20) makes the mechanism explicit.  The primal
speed is a soft count of objective scales already visible at precision
\(e^{-s}\); the missing squared speed is carried by the dual projection.
For the multiscale weights, integrating the soft count gives the harmonic
\(r\log r\) primal length, whereas the full product curve has the fixed
speed \(\sqrt{2r}\) throughout the entire \(T=\Theta(r)\) log-accuracy
window.

## 4. Scope and novelty boundary

The constant product-speed identity and \(\sqrt2\)-geodesicity are
classical consequences of Nesterov--Todd's primal--dual barrier geometry.
The exact scalar activity formula is also recorded in
[Exact primal--dual speed splitting](2026-09-04-primal-dual-speed-splitting-product-ball-counterexample.md).
The candidate contribution here is their combination with the explicit
dyadic sparse multiscale LP to give all four sharp movement laws (4), the
polynomial primal-versus-completed separation (5), and the ordinary-input
translation (6).  The targeted literature screen recorded in the companion
ledger did not locate this exact synthesis, but it was not exhaustive and
does not establish priority.

This theorem has several strict limits.

- The lower bound requires a finite strictly feasible **primal--dual gap
  certificate** of gap at most \(2\epsilon_r\).  It does not prescribe the
  central dual endpoint; that endpoint supplies the matching upper bound.
  A contract asking only for a primal solution does not pay (16).
- The lower bound is for the standard orthant product metric, or algorithms
  whose counted steps obey its bounded-Dikin contract.  It does not cover an
  arbitrary barrier or arbitrary iterate map.
- The standard-form equality matrix is sparse, but objective bit length is
  \(\Theta(r^2)\) under ordinary rational encoding because the dyadic
  exponents are \(\Theta(r)\).
- State-preparation and classical-readout lower bounds from the companion
  note are simultaneous max-type facts.  They must not be multiplied by
  the movement count without a same-instance composition theorem.

## Audit checklist

1. Check the orthant formulation, signs, barrier parameter \(2r\), and
   central projection (7).
2. Verify the activity identity (9), especially the use of the ambient
   orthant barrier rather than the restricted parameter \(r\).
3. Verify the exact terminal objective error and duality gap (13)--(14).
4. Check the elementary dual-slack endpoint bound and both Dikin chord
   constants in (15)--(17).
5. Verify that deleting the analytic-center tail preserves (19)--(20), and
   the three input-length translations in (6).
6. Keep the endpoint, metric, barrier, and nonmultiplication caveats in the
   final statement.

## Independent hostile audit record (2026-09-04)

The standard-form convention was checked directly.  With costs
\((-w_i/2,w_i/2)\), dual slacks obey
\(\beta_i-\alpha_i=w_i\), and complementarity at
\(\eta=e^s=1/\mu\) gives \(u_i\alpha_i=v_i\beta_i=e^{-s}\).
Consequently the central gap is exactly \(2re^{-s}\), while stationarity on
the box slice gives (7).  Differentiating (7) in \(s\) and using the
restricted Hessian gives one-coordinate primal squared speed
\[
 {2x_i(s)^2\over1+x_i(s)^2}
   =1-{1\over\sqrt{1+e^{2(s-a_i)}}}.
\]
The general orthogonal primal--dual speed splitting then gives dual squared
speed \(2r-q_{\rm eff}(s)\) and exact product speed \(\sqrt{2r}\).
Equations (9)--(14), including the factor two in the terminal gap, are
therefore consistent.

The endpoint lower bound was strengthened during audit without relying on
an endpoint-set reading of Nesterov--Todd.  At the initial center,
\(1/\alpha_i^0+1/(\alpha_i^0+w_i)=2\) and \(w_i\le1\), so
\(\alpha_i^0\ge1/\sqrt2\).  At any target of gap at most
\(2\epsilon_r\), the identity
\(\operatorname{gap}=\sum_i(2\alpha_i+v_iw_i)\) forces
\(\alpha_i\le\epsilon_r\).  Exact Euclideanization of the dual orthant
metric by coordinatewise logarithms gives (15), uniformly over every
finite strictly feasible target gap certificate.  Dividing by the
forward-chord length bound \(-\log(1-R)\) proves (16), even if intermediate
interior points leave the feasible affine spaces.  Conversely, partitioning
the finite central arc into arclength at most \(\log(1+R)\) is valid because
\(d(z,z')\ge\log(1+\|z'-z\|_z)\); this proves (17).  Thus the two combined
rows are sharp up to constants depending only on \(R\).

For the restricted primal rows, the companion theorem's first accurate
parameter lies in \((T-1,T]\).  Moving its initial endpoint from the
analytic center to \(x(0)\) changes distance and central arclength by
\(O(1)\); moving its terminal endpoint to \(x(T)\) changes either by at
most \(\sqrt r\).  These terms are negligible relative to
\(r\sqrt{\log r}\) and \(r\log r\).  Endpoint distance plus chord
comparison proves the arbitrary-path row.  The central-path lower row uses
the companion theorem's discrete threshold potential, not arclength alone.

Finally, the ordinary rational input has \(r\) dyadic objective
coefficients with \(\Theta(r)\)-bit denominators, so \(L=\Theta(r^2)\).
Substitution gives respectively
\(\Theta(\sqrt{L\log L})\), \(\Theta(\sqrt L\log L)\), and
\(\Theta(L^{3/4})\).  These are movement counts in the named metrics; they
do not compose multiplicatively with state-preparation or readout queries.
