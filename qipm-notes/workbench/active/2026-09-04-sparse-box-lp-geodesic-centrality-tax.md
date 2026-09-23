# A sharp centrality tax on a row-one-sparse box LP

Status: Standalone candidate theorem; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated fixed-barrier bounded-movement model

## Main conclusion

There is an explicit family of separable box LPs
\[
 \min_{x\in\mathbb R^r}-\sum_{i=1}^r\sigma_iw_ix_i,
 \qquad -1\le x_i\le1,                                      \tag{1}
\]
with two one-sparse inequalities per variable and dyadic positive weights,
for which the standard restricted logarithmic barrier
\[
                  F(x)=-\sum_{i=1}^r\log(1-x_i^2)             \tag{2}
\]
has exact self-concordant barrier parameter \(\nu=r\).  At the chosen
accuracy \(\epsilon=r2^{-A_r}=\exp[-\Theta(r)]\), every sequence of exact
central points joined by forward \(R\)-Dikin chords needs
\[
                 \Theta_R(r\log r)                            \tag{3}
\]
chords.  The shortest unrestricted feasible path to the same first accurate
central point needs only
\[
                 \Theta_R(r\sqrt{\log r})                     \tag{4}
\]
chords.  Thus exact centrality imposes a sharp
\(\Theta_R(\sqrt{\log r})\) discrete tax even on an LP whose constraint
matrix has row sparsity one and column sparsity two.

More strongly, take any feasible sequence starting at the analytic center,
ending at an actually \(\epsilon\)-accurate point, and remaining within a
fixed metric radius of arbitrarily labeled centers.  The same lower bound
holds, with no assumed progress or monotonicity of the labels.  It therefore
applies to every fixed Newton-decrement neighborhood
\(\lambda\le\beta<1/2\).  This is a fixed-standard-barrier bounded-movement
theorem, not an unrestricted LP iteration, runtime, or query lower bound.
All distances and chords here use the restricted *primal* barrier metric.
They do not by themselves compare primal--dual central tracking with a
primal--dual noncentral shortcut.

Hidden objective signs give a same-instance output separation: a normalized
central or shortcut checkpoint state takes one clean sign-oracle query from
a public amplitude state, whereas constant-coordinate-accuracy classical
output takes \(\Theta(r)\) quantum or randomized sign queries.  These are
simultaneous max-type statements, never a product.

## 1. Dyadic multiscale weights and input size

Use the exact rational profile
\[
 h_j={1\over j\lceil\sqrt j\rceil},\qquad
 H_i=\sum_{j=1}^{i-1}h_j,\qquad
 \bar a_i=4r(\log2)H_i.                                      \tag{5}
\]
Thus \(h_j=\Theta(j^{-3/2})\), uniformly in \(j\).  Round the
*cumulative* rational sums, not their increments:
\[
 A_i=\lfloor4rH_i\rfloor,
 \qquad a_i=A_i\log2,qquad w_i=2^{-A_i}.                    \tag{6}
\]
Then \(A_i\) is a nondecreasing, exactly polynomial-time constructible
integer sequence, \(A_1=0\), and
\[
 e_i:=a_i-\bar a_i\in(-\log2,0].                              \tag{7}
\]
The signs \(\sigma_i\in\{-1,1\}\) may be public or hidden.  The constraint
matrix of (1) has \(2r\) rows, one nonzero per row and two per column; every
constraint coefficient has magnitude one.

In the conventional binary numerator/denominator encoding of rationals,
\(2^{-A_i}=1/2^{A_i}\) uses \(\Theta(A_i)\) bits.  Since
\(A_i=\Theta(r)\) for every \(i\ge2\), the explicit objective has total
bit length \(L=\Theta(r^2)\).  The accuracy
\[
                   \epsilon_r=r2^{-A_r}                       \tag{8}
\]
has \(\log(1/\epsilon_r)=\Theta(r)\) and \(\Theta(r)\) ordinary rational
bits.  A mantissa--exponent sparse oracle stores each \(A_i\) in only
\(O(\log r)\) bits, but that is a different succinct input model and must
charge arithmetic on numbers with exponent \(\Theta(r)\).

## 2. Exact restricted barrier parameter

For one coordinate, \(f(t)=-\log(1-t^2)\) satisfies
\[
 f'(t)={2t\over1-t^2},\qquad
 f''(t)={2(1+t^2)\over(1-t^2)^2},\qquad
 {f'(t)^2\over f''(t)}={2t^2\over1+t^2}<1.                   \tag{9}
\]
The supremum of the last ratio is one as \(|t|\uparrow1\).
The sum (2) is standard self-concordant, and its squared gradient dual norm
is the sum of the coordinate ratios in (9).  Hence it is an \(r\)-barrier,
and simultaneous approach to a vertex proves that no smaller parameter
works:
\[
                         \boxed{\nu_F=r}.                     \tag{10}
\]
The standard slack-space LP log barrier has nominal degree \(2r\); (10) is
the exact parameter after restricting it to the box variables.  These two
numbers must not be conflated.

## 3. Central path and first accurate point

Changing variables \(u_i=\sigma_ix_i\) is a barrier isometry, so take all
signs positive in the geometry.  Put
\[
 q(z)={z\over1+\sqrt{1+z^2}},\qquad s=\log\eta.                \tag{11}
\]
The exact center of \(F(x)-\eta\sum_iw_ix_i\) is
\[
                   u_i(s)=q(e^{s-a_i}).                       \tag{12}
\]
Its objective error from the boundary optimum is
\[
 E(s)=\sum_iw_i[1-q(e^{s-a_i})].                              \tag{13}
\]
Let \(T=A_r\log2=a_r\).  Since \(z[1-q(z)]\le1\),
\[
                         E(T)\le re^{-T}=\epsilon_r.           \tag{14}
\]
The rounding bound (7) changes every tail \(T-a_i\) from
\(4r(\log2)\sum_{j=i}^{r-1}h_j\) by less than \(\log2\).
Consequently, all but
\(O(\sqrt r)\) indices have \(T-a_i\ge1\).  At \(s=T-1\), these coordinates
have \(z_i=e^{s-a_i}\ge1\), and
\[
 E(T-1)\ge e^{-(T-1)}(2-\sqrt2)[r-O(\sqrt r)]
                         >re^{-T}=\epsilon_r                  \tag{15}
\]
for all sufficiently large \(r\), because \(e(2-\sqrt2)>1\).
Thus the first accurate central log-parameter satisfies
\[
                         T-1<s_\epsilon\le T.                 \tag{16}
\]

## 4. Exact metric and optimal noncentral schedule

Define
\[
 \varrho(t)=\int_0^t{\sqrt{2(1+v^2)}\over1-v^2}\,dv,
 \qquad 0\le t<1.                                             \tag{17}
\]
Because (2) is a product metric, the change of variables
\(y_i=\varrho(|x_i|)\) makes every fixed-orthant radial submanifold
Euclidean.  In particular,
\[
 d_F(0,x)^2=\sum_i\varrho(|x_i|)^2.                           \tag{18}
\]
The globally shortest path from zero to the first accurate center is
linear in \(y\):
\[
 x_i(u)=\sigma_i\varrho^{-1}
       \!\left(u\varrho(q(e^{s_\epsilon-a_i}))\right),
 \qquad0\le u\le1.                                           \tag{19}
\]
It is strictly feasible and ends at exactly the same center.  If its length
is \(D_\epsilon\), standard self-concordant chord comparison gives, for
every fixed \(0<R<1\),
\[
 {D_\epsilon\over-\log(1-R)}
 \le T_R^{\rm unrestricted}
 \le\left\lceil{D_\epsilon\over\log(1+R)}\right\rceil.       \tag{20}
\]

The dyadic rounding changes every \(T-a_i\) by only \(O(1)\).  For
\(z=e^b\ge1\), the elementary bounds
\(1/(1+z)\le1-q(z)\le1/z\), together with
\[
 \log{1\over1-t}\le\varrho(t)
       \le\sqrt2\log{1\over1-t},                              \tag{21a}
\]
show that \(\varrho(q(e^b))=\Theta(1+b)\).  The same quantity is bounded
above and below by positive constants for \(-1\le b\le0\).  Moreover, the
unrounded tails obey
\[
 \bar a_r-\bar a_i
 =4r(\log2)\sum_{j=i}^{r-1}h_j
 =\Theta\!\left(r(i^{-1/2}-r^{-1/2})\right).                 \tag{21b}
\]
Summing their squares, using the first \(r/16\) indices for the lower
bound, gives \(\Theta(r^2\log r)\).  Equations (7) and (16) change each
terminal exponent by only \(O(1)\), so
\[
                         D_\epsilon=\Theta(r\sqrt{\log r}).   \tag{21}
\]
This proves (4).

## 5. Discrete central and Newton-neighborhood lower bounds

For two centers, their exact distance is the Euclidean increment of their
\(\varrho\)-coordinate vectors.  Whenever the lower parameter lies in
\([a_j,a_{j+1})\), the first \(j\) coordinate velocities are at least
\[
                       v_0=\sqrt{1-1/\sqrt2},                 \tag{22}
\]
and hence
\[
                   d_F(x(s),x(t))\ge v_0\sqrt j\,|t-s|.       \tag{23}
\]
Fix a metric tube radius \(\zeta\ge0\).  Consider feasible iterates \(z_k\)
and arbitrary real labels \(s_k\) satisfying
\[
 z_0=0,\qquad d_F(z_k,x(s_k))\le\zeta,\qquad
 \|z_{k+1}-z_k\|_{z_k}\le R,                                 \tag{23a}
\]
and suppose the actual final iterate is \(\epsilon_r\)-accurate.  A
transition then implies
\[
 d_F(x(s_k),x(s_{k+1}))
             \le C_{R,\zeta}:=2\zeta-\log(1-R).              \tag{24}
\]
Put \(D=C_{R,\zeta}/v_0\).  From (5)--(7) and
\(\lceil\sqrt j\rceil\le2\sqrt j\),
\[
 a_{j+1}-a_j\ge4r(\log2)h_j-\log2
              \ge {2r\log2\over j^{3/2}}-\log2.             \tag{25}
\]
Therefore, for
\[
 J=\left\lfloor
   \left({2r\log2\over4D+\log2}\right)^{2/3}
   \right\rfloor,                                             \tag{26}
\]
the first \(J\) threshold gaps are at least \(4D\).  The clipped progress
potential
\[
 \Phi(s)=\int_{a_1}^{\min\{\max\{s,a_1\},a_{J+1}\}}
                 \sqrt{\#\{i:a_i\le v\}}\,dv                \tag{27}
\]
changes by only \(O_{R,\zeta}(1)\) per transition.  Its required total
change is
\[
 \begin{aligned}
 \sum_{j=1}^J\sqrt j\,(a_{j+1}-a_j)
 &=4r(\log2)\sum_{j=1}^J\sqrt j\,h_j
    +\sum_{j=1}^J\sqrt j\,(e_{j+1}-e_j)\\
 &=\Theta(r\log r),\qquad e_i=a_i-\bar a_i,                  \tag{28}
 \end{aligned}
\]
because \(\sqrt j\,h_j=\Theta(1/j)\), while summation by parts and
\(|e_i|<\log2\) bound the second sum by \(O(\sqrt J)\).

There are no hidden endpoint-label assumptions.  Work in the sign-corrected
coordinates \(u_i=\sigma_i z_i\).  Actual final accuracy and \(w_1=1\)
give \(u_{K,1}\ge1-\epsilon_r\), since every objective-gap summand is
nonnegative.  Coordinate contraction of the product \(\varrho\)-metric and
the terminal tube condition imply
\[
 \varrho(q(e^{s_K}))
 \ge\varrho(1-\epsilon_r)-\zeta
 \ge T-\log r-\zeta.                                         \tag{28a}
\]
The scalar central coordinate obeys
\[
\varrho(q(e^s))\le {1\over\sqrt2}+\max\{s,0\},              \tag{28b}
\]
because its derivative in \(s\) is at most one and its value at zero is at
most \(1/\sqrt2\).  For the latter bound, the squared velocity is
\(1-(1+e^{2s})^{-1/2}\le e^{2s}/2\) on \(s\le0\), and integration from
the analytic-center limit \(s=-\infty\) gives the claim.  Thus
\(s_K\ge T-\log r-\zeta-1/\sqrt2>a_{J+1}\) for large \(r\), since
\(T-a_{J+1}=\Theta_{R,\zeta}(r^{2/3})\).  At the start,
\(d_F(0,x(s_0))\le\zeta\).  If \(s_0>0\), the first central coordinate has
\(\varrho\)-velocity at least \(v_0\), so \(s_0\le\zeta/v_0\).  Hence the
initial clipped potential is only \(O_\zeta(1)\), whereas the terminal
potential is the full quantity (28).  Consequently every sequence (23a)
needs
\[
                         K=\Omega_{R,\zeta}(r\log r).          \tag{29}
\]
Nonmonotonicity cannot help, since total absolute potential change dominates
net progress.  Central-arclength partitioning and the universal
\(O(\sqrt{\log r})\) central-to-geodesic distortion give the matching
upper bound, proving (3).

For the local centrality function
\(f_s(x)=F(x)-e^s\sum_iw_i\sigma_ix_i\), standard
self-concordance gives
\[
 \lambda_{f_s}(y)\le\beta<1/2
 \quad\Longrightarrow\quad
 d_F(y,x(s))\le\zeta_\beta:=\log{1-\beta\over1-2\beta}.       \tag{30}
\]
Indeed, with \(t=\|y-x(s)\|_y\), global lower Hessian comparison gives
\(t\le\lambda/(1-\lambda)\), and upper comparison integrates to
\(-\log(1-t)\).  Substitution of \(\zeta_\beta\) into (29) proves the
fixed Newton-neighborhood version directly from the actual start and output;
no separate progress condition on \((s_k)\) is needed.

## 6. Raw sign queries and output contracts

Let a clean sign oracle act as
\(O_b|i,z\rangle=|i,z\oplus b_i\rangle\), with
\(\sigma_i=(-1)^{b_i}\).  Exact coefficient access to
\(c_i=-\sigma_i2^{-A_i}\) is equivalent up to constant query overhead.
An approximate value oracle needs absolute error below
\(2^{-A_r-1}=\exp[-\Theta(r)]\), so its worst-case value precision is
\(\Theta(r)\) bits.

For a central or radial checkpoint with public magnitudes \(y_i>0\), exact
preparation of the public state \(\|y\|_2^{-1}\sum_iy_i|i\rangle\), followed
by one phase-kickback query with target \(|-\rangle\), gives
\[
                      {1\over\|y\|_2}\sum_i\sigma_iy_i|i\rangle. \tag{31}
\]
The public amplitude table, finite-precision gates, and every requested
copy are separate costs.  At the terminal center, (16) and \(a_i\le T\)
give \(y_i>q(e^{-1})\).  Thus any classical vector satisfying
\[
              \max_i|\widetilde x_i-\sigma_iy_i|
                            <q(e^{-1})/2                       \tag{32}
\]
reveals all \(r\) signs.  Such full output costs \(\Theta(r)\) quantum or
randomized raw queries: read-all is an upper bound and parity gives the
linear lower bound.  The optimum value \(-\sum_iw_i\) and every checkpoint
objective value are public, so no scalar-output query lower bound exists.

## 7. QIPM relevance and limits

This LP makes the geometric conclusion stronger and the algorithmic caveat
clearer.

- It is a literal sparse LP, not merely a matrix-cone slice.  The exact
  centrality tax and Newton-neighborhood lower use the ordinary restricted
  box log barrier.
- Its Newton matrices are diagonal.  Once the weights are read or their
  public table is loaded, classical central points and the noncentral path
  cost \(O(rB)\) arithmetic for scalar precision \(B\).  There is no sparse
  linear-system bottleneck for a QLS algorithm to improve.
- The shortcut is a direct separable feasible path, not a primal--dual IPM:
  it does not maintain complementarity or a central-neighborhood invariant.
  Generic equality constraints destroy the coordinate product metric.
- For logarithmically homogeneous cone barriers, Nesterov--Todd prove that
  every feasible primal--dual central-path segment is
  \(\sqrt2\)-geodesic: its length is at most \(\sqrt2\) times the endpoint
  distance in the *combined* primal--dual product metric.  That does not
  contradict the present primal centrality tax: the metrics and comparison
  paths differ.  The lower bound transfers to a bounded full-step method
  only when primal feasibility, its neighborhood, and its step contract
  project to (23a) in this restricted primal metric.  Conversely, the
  primal radial shortcut (19) supplies no dual-feasible trajectory to the
  central dual endpoint, so its \(\Theta(r\sqrt{\log r})\) count need not
  survive after dual feasibility and dual motion are charged.  No
  primal--dual \(\sqrt{\log r}\) separation is claimed.
  In fact, this gives a decisive constant-factor obstruction.  For any two
  finite central endpoints, let \(\widehat L_{\rm CP}\) and
  \(\widehat d\) be their central arclength and distance in the combined
  metric.  Then
  \[
       \widehat d\le\widehat L_{\rm CP}\le\sqrt2\,\widehat d. \tag{33}
  \]
  Arclength partitioning and the two self-concordant chord comparisons imply
  \[
  T_{\rm central}^{\rm arc}\le
       \left\lceil{\widehat L_{\rm CP}\over\log(1+R)}\right\rceil,
  \qquad
  T_{\rm arbitrary}^{\star}\ge
       {\widehat L_{\rm CP}\over
        \sqrt2[-\log(1-R)]}.                                  \tag{34}
  \]
  Here the arbitrary paths join the same two endpoints in the full combined
  cone interior and every counted transition is a forward \(R\)-Dikin
  chord in that product metric.  In particular, including the ceiling,
  \[
  T_{\rm central}^{\rm arc}
  \le {\sqrt2[-\log(1-R)]\over\log(1+R)}
          T_{\rm arbitrary}^{\star}+1.                         \tag{34a}
  \]
  Thus the ratio away from the zero- or one-step regime is bounded solely
  by \(R\), not by \(r\).  This is a direct consequence of the classical
  Nesterov--Todd theorem, not a new
  geometric result.  It proves that the growing tax established here is
  intrinsically primal unless the algorithmic contract uses a different
  projected metric or does not charge the full dual trajectory.
- A QIPM asked only for one normalized state sees the one-query law (31),
  while explicit classical output sees (32).  Neither fact multiplies the
  movement count.  Requiring a trajectory, repeated state copies, or full
  output gives different resource contracts.
- The neighborhood lower is output-driven: analytic-center initialization,
  actual objective accuracy, and a fixed metric or Newton-decrement tube
  force the reference labels to cross the hard threshold range.  Label
  progress and monotonicity are not extra assumptions.

In terms of conventional input length \(L=\Theta(r^2)\), the sharp counts
are \(\Theta_R(\sqrt L\log L)\) central versus
\(\Theta_R(\sqrt{L\log L})\) unrestricted.  This translation is descriptive:
the family is separable and directly solvable, so it is not an end-to-end
quantum speedup or a lower bound for unrestricted LP algorithms.

## Audit checklist

- Check that cumulative dyadic rounding preserves monotonic thresholds,
  the first-accurate window, the harmonic progress lower bound, and the
  two-sided endpoint distance.
- Check exact \(\nu_F=r\), distinct from the \(2r\) slack count.
- Check conventional rational versus succinct exponent input lengths.
- Check the conversion of actual endpoint accuracy and \(z_0=0\) into full
  clipped label progress, and the Newton-decrement tube constant.
- Do not transfer the primal shortcut comparison to a combined primal--dual
  metric without constructing and charging a dual trajectory.
- Keep state preparation, full readout, movement, and arithmetic separate.

## Independent hostile audit

The audit verified cumulative dyadic rounding, conventional and succinct
input lengths, the exact restricted parameter \(\nu_F=r\), the first-
accurate window, the two-sided endpoint distance, and the rounded harmonic
progress calculation.  It corrected the sparsity description to row
sparsity one and column sparsity two and made explicit that the clipped
terminal interval lies before \(T-1\).

A second audit verified the endpoint-driven strengthening in Section 5.
Actual objective accuracy makes every coordinate gap nonnegative and forces
the first sign-corrected coordinate above \(1-\epsilon_r\).  Contraction of
the product metric, the scalar lower bound
\(\varrho(1-\epsilon_r)\ge\log(1/\epsilon_r)\), and (28b) then force
\(s_K>a_{J+1}\).  Conversely, \(z_0=0\) and the initial tube bound make the
clipped starting potential \(O_\zeta(1)\).  The pair-distance estimate is
symmetric in arbitrary labels, so nonmonotonicity cannot evade the lower
bound.  The Newton-decrement conversion supplies the required fixed tube
without adding a reference-progress hypothesis.  No substantive defect was
found in the strengthened statement.

A third audit verified the uniformly constructible rational profile in
(5)--(7).  Integer square roots, exact rational summation, multiplication by
\(4r\), and flooring are polynomial-time operations; no comparison with an
irrational half-integer remains.  The bounds
\[
 {1\over2j^{3/2}}\le h_j\le {1\over j^{3/2}}
\]
preserve the finite-tail law, first-accurate window, early threshold gaps,
harmonic progress, and two-sided endpoint distance.  Cumulative flooring
contributes one bounded error \(e_i\in(-\log2,0]\) per threshold rather than
an accumulated rounding error.  It also verified \(A_i=\Theta(r)\) for
every \(i\ge2\), \(A_r=\Theta(r)\), and conventional input length
\(L=\Theta(r^2)\).  No substantive correction was needed.

A fourth audit checked the primal--dual scope against Nesterov--Todd's 2002
theorem.  Their \(\sqrt2\)-geodesic comparison concerns feasible central
paths in the combined product metric of a logarithmically homogeneous
primal--dual cone pair.  The present theorem concerns the restricted primal
box metric.  Projection transfers its lower bound only under the explicitly
stated primal-feasibility, neighborhood, and step contracts, while the
primal radial shortcut supplies no dual-feasible path to the central dual
endpoint.  Accordingly, no primal--dual centrality separation is claimed.

A fifth audit checked (33)--(34a).  For finite feasible primal--dual central
endpoints under a logarithmically homogeneous cone barrier,
Nesterov--Todd give
\(\widehat d\le\widehat L_{\rm CP}\le\sqrt2\widehat d\).
Self-concordant chord comparison gives the two bounds in (34), and retaining
the ceiling yields (34a).  The arbitrary comparison path may move anywhere
in the combined cone interior; imposing primal--dual feasibility only
restricts that class further.  The conclusion does not apply to the
restricted primal barrier alone or to infinite boundary endpoints.
