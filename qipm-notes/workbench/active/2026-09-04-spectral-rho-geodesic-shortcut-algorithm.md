# A constructive shortest-path shortcut for low-rank spectral-ball objectives

Status: Exact narrow algorithm proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the geometric algorithm; deliberately limited QIPM claim

## Main conclusion

For the unconstrained support problem
\[
       \min_{\|X\|_{\rm op}\le1}-\langle C,X\rangle,
       \qquad \phi(X)=-\log\det(I-XX^*),                         \tag{1}
\]
an accessible compact SVD of the rank-\(r\) objective does turn the new
distance variational theorem into a constructive algorithm.  One scalar
water-filling search produces the globally closest interior
\(\epsilon\)-accurate endpoint.  Linear interpolation in exact radial
metric coordinates is a globally shortest feasible path.  For any fixed
Dikin radius \(0<\theta<1\), arclength partitioning uses
\[
 \boxed{
 T_{\rm geo}\le
  \left\lceil{L_{\rm opt}(\epsilon)\over\log(1+\theta)}\right\rceil,
 \qquad
 T_{\rm any}\ge
  {L_{\rm opt}(\epsilon)\over-\log(1-\theta)}.}                 \tag{2}
\]
Thus the construction is optimal up to a constant depending only on
\(\theta\) among all feasible sequences that start at the analytic center,
end \(\epsilon\)-accurately, and use forward \(\theta\)-Dikin chords in
the fixed standard barrier metric.

This is a genuine algorithm for (1), but it is not a generic IPM or QIPM
variation.  The SVD already solves (1) directly, the path abandons
centrality, and generic affine constraints destroy the singular-coordinate
reduction.  Quantum preparation of a checkpoint additionally requires a
singular-vector transform or loaded amplitude data; its cost is not bounded
by (2).

There is also a sharp same-endpoint statement.  Instead of water filling,
take the first \(\epsilon\)-accurate central point and follow the radial
geodesic directly to it.  Compared with arclength partitioning of the
central arc to that same endpoint, this reduces the number of certified
bounded-Dikin checkpoints by at most \(O(\sqrt{\log r})\), and an audited
sparse diagonal family attains \(\Theta(\sqrt{\log r})\).  For the stronger
choice \(T_0=r\), the separation holds not only for two arclength
partitions: every forward-bounded sequence of exact central points needs
\(\Theta_R(r\log r)\) chords, whereas the unrestricted same-endpoint
geodesic needs \(\Theta_R(r\sqrt{\log r})\).  The lower bound remains valid
for iterates within any fixed Riemannian distance of reference centers.  On
the explicit multiscale family, analytic-center initialization and actual
\(\epsilon\)-accurate output force the reference parameters across the hard
range; no label-progress or monotonicity assumption is needed.
In particular, the tube hypothesis follows from the standard
Newton-decrement neighborhood \(\lambda\le\beta<1/2\), with an explicit
radius depending only on \(\beta\).

The same sparse multiscale instance also supports an exact oracle/output
separation.  Hiding independent signs on its public diagonal weights leaves
all movement laws unchanged.  Every normalized central or radial-checkpoint
state is then exactly one raw sign query away from a public amplitude state,
whereas a constant-coordinate-accuracy classical terminal matrix reveals
all \(r\) signs and needs \(\Theta(r)\) quantum or randomized queries.  The
state, movement, and readout statements are simultaneous max-type resource
bounds, never a product.

## 1. Exact endpoint and radial coordinates

Let
\[
              C=U\operatorname{Diag}(w_1,\ldots,w_r)V^*,
              \qquad w_i>0.                                    \tag{3}
\]
Define the scalar radial metric coordinate
\[
 \varrho(x)=\int_0^x{\sqrt{2(1+t^2)}\over1-t^2}\,dt,
 \qquad 0\le x<1.                                               \tag{4}
\]
It is strictly increasing and satisfies
\[
       \log{1\over1-x}\le\varrho(x)
       \le\sqrt2\log{1\over1-x}.                               \tag{5}
\]
The exact center-to-point distance theorem says
\[
 d_\phi(0,X)=
       \left(\sum_j\varrho(\sigma_j(X))^2\right)^{1/2}.         \tag{6}
\]
Von Neumann's inequality then reduces the distance to the entire accurate
set to the strictly convex problem
\[
 L_{\rm opt}(\epsilon)=
 \min_{\substack{0\le x_i<1\\
                  \sum_iw_i(1-x_i)\le\epsilon}}
       \left(\sum_i\varrho(x_i)^2\right)^{1/2},
       \qquad0<\epsilon<\sum_iw_i.                              \tag{7}
\]
The unique endpoint has an active constraint and is characterized by one
multiplier \(\lambda>0\):
\[
 2\varrho(x_i^*)\varrho'(x_i^*)=\lambda w_i,qquad
                  \sum_iw_i(1-x_i^*)=\epsilon.                  \tag{8}
\]
Because \((\varrho^2)'\) is strictly increasing from zero to infinity,
each \(x_i^*(\lambda)\) is obtained by a monotone scalar inversion.  The
left side of the constraint in (8) decreases continuously from
\(\sum_iw_i\) to zero as \(\lambda\) increases.  Doubling followed by
bisection therefore finds the unique multiplier.

If \(\epsilon\ge\sum_iw_i\), output the analytic center.  Exact accuracy
\(\epsilon=0\) requires a boundary endpoint at infinite barrier distance
and is excluded.

## 2. The geodesic shortcut algorithm

Put \(\ell_i=\varrho(x_i^*)\),
\(L=(\sum_i\ell_i^2)^{1/2}=L_{\rm opt}(\epsilon)\), and define
\[
 X(s)=U\operatorname{Diag}\left(
       \varrho^{-1}(s\ell_1),\ldots,
       \varrho^{-1}(s\ell_r)\right)V^*,qquad0\le s\le1.       \tag{9}
\]
Every singular value remains in \([0,1)\), so the path is strictly
feasible.  Its endpoint obeys the objective constraint in (7), hence is
\(\epsilon\)-accurate.  Restricting the barrier Hessian to the fixed
singular frame makes the \(\varrho\)-coordinates Euclidean, so (9) has
constant speed \(L\) and length \(L\).  Equation (6) proves that no path
to any accurate endpoint can be shorter.

Choose
\[
 J=\left\lceil{L\over\log(1+\theta)}\right\rceil,qquad
 s_j=\min\left\{{j\log(1+\theta)\over L},1\right\}.             \tag{10}
\]
Each intervening arc has length at most \(\log(1+\theta)\).
For a forward chord from \(Y\) to \(Z\), self-concordant metric comparison
gives
\[
             \log(1+\|Z-Y\|_Y)\le d_\phi(Y,Z).                 \tag{11}
\]
Thus consecutive points in (10) have starting Dikin norm at most
\(\theta\), proving the upper half of (2).  Conversely, any forward
\(\theta\)-Dikin chord has Riemannian length at most
\(-\log(1-\theta)\).  The triangle inequality and the definition of
\(L_{\rm opt}\) prove the lower half.  Notice that this lower bound covers
noncentral paths and arbitrary changes of singular vectors; (9) attains it
within the unavoidable forward/backward self-concordance constants.

### 2.1 Shortcut to the first accurate central endpoint

Let
\[
 q(z)={z\over1+\sqrt{1+z^2}},\qquad
 E(\eta)=\sum_iw_i[1-q(\eta w_i)].                              \tag{12a}
\]
The function \(E\) decreases continuously from \(\|C\|_*\) to zero, so a
second scalar search finds the first accurate central multiplier
\[
                 \eta_\epsilon:\quad E(\eta_\epsilon)=\epsilon. \tag{12b}
\]
Put \(y_i=q(\eta_\epsilon w_i)\) and
\(d_c=(\sum_i\varrho(y_i)^2)^{1/2}\).  Replacing
\(x_i^*,\ell_i,L\) in (9)--(10) by
\(y_i,\varrho(y_i),d_c\) gives a shortest path to that same central
endpoint and uses \(\Theta_\theta(d_c)\) forward-Dikin checkpoints.

If \(L_c\) is the exact central arclength from zero to this endpoint, the
audited decreasing-velocity theorem gives
\[
 d_c\le L_c\le\Gamma_r d_c,qquad
 \Gamma_r^2=\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2
             =1+{1\over4}\log r+O(1).                           \tag{12c}
\]
Thus the radial shortcut saves at most
\(\Theta(\sqrt{\log r})\) relative to the explicit schedule obtained by
partitioning the central arc by constant arclength.  Section 5 proves that
this factor is attained even when the central endpoint is the first one
meeting the requested accuracy.

## 3. Finite precision and arithmetic cost

The cleanest input contract is an **SVD-RAM model**:

- the positive weights \(w_i\) are available as a classical array;
- the compact singular frames \(U,V\) are explicit sparse factors or have
  charged application oracles; and
- monotone scalar functions in (4), (8), and (9) are evaluated to requested
  precision by ordinary reversible or classical arithmetic.

In exact real arithmetic, the construction above is literal.  At finite
precision, solve (8) with target error \(\epsilon/2\), then approximate the
coordinates so that
\(\sum_iw_i|\widetilde x_i-x_i^*|\le\epsilon/2\).  The returned endpoint
is \(\epsilon\)-accurate.  Use an internal chord radius
\(\theta_0<\theta\) and approximate every checkpoint to Dikin error at
most a fixed fraction of \(\theta-\theta_0\); continuity of the local norm
then preserves the advertised \(\theta\)-chord contract.  Required scalar
precision grows only logarithmically with the desired coordinate and
accuracy margins, although it can depend on the weight dynamic range.

If \(B\) doubling/bisection and scalar-inversion iterations suffice, the
endpoint preprocessing uses \(O(rB)\) scalar operations and \(O(r)\)
storage.  Keeping \((\ell_i)_i\) plus \(U,V\) is an implicit path
representation: a checkpoint parameter costs \(O(1)\) storage, one queried
singular value costs the scalar inversion cost, and materializing all \(r\)
singular values costs \(O(rB)\).  A compact rank-factor checkpoint costs
at least its output size; a dense \(p\times q\) matrix costs \(\Omega(pq)\)
entries.  None of these arithmetic or output costs is multiplied into (2)
without an explicit repeated-output contract.

## 4. Quantum checkpoint access is a separate assumption

The normalized checkpoint state is
\[
 |X(s)\rangle={1\over\|x(s)\|_2}
       \sum_{i=1}^r x_i(s)|u_i\rangle|\overline v_i\rangle,
 \quad x_i(s)=\varrho^{-1}(s\ell_i).                            \tag{12}
\]
After an \(O(r)\)-size amplitude table has been built, QRAM-style
state-preparation access to that table plus charged isometries for \(U,V\)
can prepare (12) in polylogarithmic address overhead per copy.  This is an
input/data-structure assumption, not a consequence of low rank or short
movement.  Without the table, a block encoding of \(C\) suggests applying
the composite singular-value map
\[
 w\longmapsto
 \varrho^{-1}\!\left(s\varrho(x^*(\lambda w))\right),           \tag{13}
\]
but a QSVT implementation depends on approximation degree, normalization,
success amplitude, spectral gaps, and the smallest relevant weight.  No
polylogarithmic bound follows from (2).

Nor does one normalized state certify objective accuracy: its Frobenius
normalization removes radial scale, and estimating
\(\langle C,X\rangle\) or producing a classical matrix has separate
readout cost.  The movement count, preprocessing/query complexity, number
of state copies, and output writing are simultaneous resources and are
never multiplied here.

### 4.1 Indexed-weight preprocessing reduces to mean estimation

The multiplier search has a useful exact oracle form, but it does not by
itself yield a new QIPM speedup.  Let
\[
 h(x)=2\varrho(x)\varrho'(x),\qquad
 x(z)=h^{-1}(z),\qquad \mathcal W_\varrho(z)=z[1-x(z)].        \tag{13a}
\]
For \(\gamma>0\), the endpoint equation (8) is equivalently
\[
       \sum_i \mathcal W_\varrho(\gamma w_i)=\gamma\epsilon. \tag{13b}
\]
Here \(\mathcal W_\varrho\) is the displayed exact metric response, not
the Lambert \(W\) function.
The unmultiplied function
\(A(\gamma)=\sum_iw_i[1-x(\gamma w_i)]\) is continuous and strictly
decreasing from \(\|C\|_*\) to zero, so (13b) has exactly one positive
solution.  The apparent solution \(\gamma=0\) created by multiplication
is extraneous.

Suppose a coherent indexed oracle returns \(w_i\le w_{\max}\), and charge
reversible evaluation of \(x(\gamma w_i)\).  For a trial \(\gamma\), the
uniform-index mean
\[
 {A(\gamma)\over rw_{\max}}
 ={1\over r}\sum_i{w_i[1-x(\gamma w_i)]\over w_{\max}}         \tag{13c}
\]
lies in \([0,1]\) and equals \(\epsilon/(rw_{\max})\) at the root.
Relative amplitude estimation and ordinary sampling therefore give a
constant-relative residual test with respective query costs
\[
 O\!\left(\min\left\{r,
       \sqrt{rw_{\max}/\epsilon}\right\}\right),
 \qquad
 O\!\left(\min\left\{r,rw_{\max}/\epsilon\right\}\right),     \tag{13d}
\]
up to confidence, search, and scalar-arithmetic factors.  With a custom
coherent \(\ell_1\)-sampler for \(p_i=w_i/\|C\|_*\), replace
\(rw_{\max}\) in (13d) by \(\|C\|_*\), but charge construction of that
sampler and its normalization.  This is not the usual length-square/SQ
sampler, whose probabilities are proportional to \(w_i^2\) and whose
supplied norm is \(\|C\|_F\).
These fixed-trial laws are precisely relative mean estimation and are tight
by ordinary approximate-counting instances in the nonsaturated regime.

They are not a uniformly conditioned root-estimation theorem.  The exact
logarithmic condition number is governed by
\[
 \alpha_\varrho(\gamma)
 :=-{d\log A(\gamma)\over d\log\gamma}
 ={\sum_i w_i h(x_i)/h'(x_i)\over A(\gamma)},
 \qquad x_i=x(\gamma w_i).                                    \tag{13e}
\]
It can approach zero near the analytic center.  Obtaining relative error
\(\tau\) in \(\gamma\) from residual tests then incurs, locally, an
additional \(1/(\alpha_\varrho\tau)\) quantum or
\(1/(\alpha_\varrho\tau)^2\) randomized factor.  A complete bit-complexity
bound must also charge the bracketing range and reversible evaluation of
\(h^{-1}\).

Once \(\gamma\) is known, a uniform-index controlled rotation prepares
amplitudes proportional to \(x_i=x(\gamma w_i)\) with amplification cost
\[
 O\!\left({x_{\max}\sqrt r\over\|x\|_2}\right),
 \qquad x_{\max}=x(\gamma w_{\max}),                          \tag{13f}
\]
before the separately charged singular-frame isometries.  This cost can
range from constant to \(\Theta(\sqrt r)\).  The custom \(\ell_1\)-sampler
normalization reveals \(\|C\|_*\), making the unconstrained optimum value
itself public;
and an \(\epsilon\)-accurate interior point can be obtained without water
filling by uniformly shrinking the known polar factor.  Consequently the
only generic quantum gain visible in (13c)--(13f) is the standard quadratic
gain for estimating a mean needed by the *closest-endpoint* geometric
contract.  SVD acquisition, dynamic range, checkpoint-state success, and
classical output can dominate it.  We therefore do not promote (13d) as a
QIPM preprocessing advantage.

## 5. Sharp centrality tax at the first accurate endpoint

For \(m=r\) sufficiently large, let \(T_0=r\),
\(\epsilon=re^{-T_0}\), and
\[
 S_r=\sum_{j=1}^{r-1}j^{-3/2},\qquad
 a_i={T_0\over S_r}\sum_{j=1}^{i-1}j^{-3/2},\qquad
 w_i=e^{-a_i}.                                                   \tag{14}
\]
Take \(C=\operatorname{Diag}(w_i)\), with optional zero padding to make
the ambient barrier parameter arbitrarily larger than \(r\).  This is a
one-sparse diagonal objective with a public SVD.

Let \(s=\log\eta\), \(b_i=T_0-a_i\), and let \(s_\epsilon\) be the first
central log-multiplier with error at most \(\epsilon\).  At \(s=T_0\),
\[
 E(e^s)=e^{-s}\sum_i z_i[1-q(z_i)]\le re^{-T_0}=\epsilon,
 \qquad z_i=e^{s-a_i},                                         \tag{15}
\]
because \(z[1-q(z)]\le1\).  At \(s=T_0-1\), all but
\(O(\sqrt r)\) indices have \(b_i\ge1\): if
\(i\le r-K\sqrt r\), the last \(K\sqrt r\) terms in the defining tail
for \(b_i\) give \(b_i\ge K/S_r\).  Choose a fixed \(K>S_r\).  For these
indices \(z_i=e^{b_i-1}\ge1\), and
\[
 z_i[1-q(z_i)]\ge1-q(1)=2-\sqrt2.
\]
Since \(e(2-\sqrt2)>1\), for all sufficiently large \(r\),
\[
 E(e^{T_0-1})
 \ge e^{-(T_0-1)}(2-\sqrt2)[r-O(\sqrt r)]
 >re^{-T_0}=\epsilon.                                          \tag{16}
\]
Hence
\[
                         T_0-1<s_\epsilon\le T_0.              \tag{17}
\]

Truncating the audited harmonic-interval central-length proof at
\(T_0-1\) removes only the last \(O(\sqrt r)\) thresholds.  Therefore
\[
                         L_c(0,s_\epsilon)=\Omega(r\log r).     \tag{18}
\]
Monotonicity and the endpoint-distance estimate at \(T_0\) give
\[
 d_c(0,X(e^{s_\epsilon}))\le d_c(0,X(e^{T_0}))
                              =O(r\sqrt{\log r}).               \tag{19}
\]
The universal upper bound (12c), applied to the same first accurate
endpoint, supplies the reverse ratio.  Thus
\[
 {L_c(0,s_\epsilon)\over d_c(0,X(e^{s_\epsilon}))}
                         =\Theta(\sqrt{\log r}).                \tag{20}
\]
Partitioning the central arc and its same-endpoint radial geodesic by
constant arclength gives explicit bounded-Dikin schedules whose counts have
the same \(\Theta(\sqrt{\log r})\) ratio.  The next theorem shows that the
factor persists for every exact-central bounded-chord schedule, not merely
the arclength partition.

### 5.1 Discrete exact- and near-central chord lower bound

Write \(X(s)\) for the exact center at log-multiplier \(s\), and put
\[
 v_0=\sqrt{1-1/\sqrt2}.
                                                                    \tag{21}
\]
For two centers in their common ordered singular frame, the full ambient
distance is
\[
 d_\phi(X(s),X(t))=
 \left[\sum_i\left(
  \varrho(q(e^{t-a_i}))-\varrho(q(e^{s-a_i}))
                         \right)^2\right]^{1/2}.                 \tag{22}
\]
Indeed, the fixed-frame path linear in the coordinate \(\varrho\) gives
the upper bound.  Conversely, the spectral Hessian inequality used to prove
(6), integrated between arbitrary endpoints, gives the Euclidean distance
between the two ordered \(\varrho\)-singular-value vectors as a lower
bound.  Central singular values have the same ordering at both endpoints,
so no permutation issue occurs.  Thus equality holds even in the full
matrix ball, not only in the diagonal submanifold.

The scalar velocity is
\[
 {d\over ds}\varrho(q(e^{s-a_i}))
 =\sqrt{1-{1\over\sqrt{1+e^{2(s-a_i)}}}}.
                                                                    \tag{23}
\]
It is at least \(v_0\) whenever \(s\ge a_i\).  Hence, if the lower of
\(s,t\) lies in \([a_j,a_{j+1})\), then (22) gives
\[
 d_\phi(X(s),X(t))\ge v_0\sqrt j\,|t-s|.                         \tag{24}
\]
This argument is symmetric in \(s,t\), so it covers both forward and
backward changes of the reference parameter.

Fix a forward chord radius \(0<R<1\) and a Riemannian central-neighborhood
radius \(\zeta\ge0\).  Suppose feasible iterates \(Y_k\) have reference
parameters \(s_k\) satisfying
\[
 d_\phi(Y_k,X(s_k))\le\zeta,qquad
 \|Y_{k+1}-Y_k\|_{Y_k}\le R.                                   \tag{25}
\]
Metric comparison and the triangle inequality imply
\[
 d_\phi(X(s_k),X(s_{k+1}))
 \le C_{R,\zeta}:=2\zeta-\log(1-R).                             \tag{26}
\]
Let \(D=C_{R,\zeta}/v_0\), and, for all sufficiently large \(r\), set
\[
 J=\left\lfloor
       \left({r\over4S_rD}\right)^{2/3}
    \right\rfloor,qquad 1\le J\le r-1.                          \tag{27}
\]
Then every threshold gap among the first \(J\) intervals obeys
\[
 a_{j+1}-a_j={r\over S_rj^{3/2}}\ge4D.                          \tag{28}
\]
Equations (24)--(28) show that one transition crosses at most one such
threshold and changes the clipped progress potential
\[
 \Phi(s)=\int_{a_1}^{\min\{\max\{s,a_1\},a_{J+1}\}}
              \sqrt{\#\{i:a_i\le u\}}\,du                       \tag{29}
\]
by at most \(\sqrt2D\).  If the lower parameter is below \(a_1\), the
first coordinate in (22) instead gives
\(\max\{s,t\}-a_1\le D\) once the upper parameter crosses \(a_1\),
which proves the same bound at the initial edge.  Clipping handles the
terminal edge.

Assume that the reference sequence starts with \(s_0\le a_1=0\) and ends
with \(s_K\ge s_\epsilon\).  Since \(s_\epsilon>r-1>a_{J+1}\) for all
sufficiently large \(r\), its total required progress is
\[
 \Phi(s_K)-\Phi(s_0)
 =\sum_{j=1}^J\sqrt j\,(a_{j+1}-a_j)
 ={r\over S_r}\sum_{j=1}^J{1\over j}
 =\Theta_{R,\zeta}(r\log r).                                   \tag{30}
\]
Nonmonotonicity cannot help, because the sum of the absolute potential
changes dominates the net change.  Therefore (29)--(30) prove
\[
 K\ge {rH_J\over\sqrt2S_rD}
                         =\Omega_{R,\zeta}(r\log r),             \tag{31}
\]
where the asymptotic equality assumes fixed \(R,\zeta\) and sufficiently
large \(r\).
The analytic center is included by the limiting reference \(s_0=-\infty\).
For exact central checkpoints take \(\zeta=0\).  Conversely, (12c), (19),
and central-arc partitioning give \(K=O_R(r\log r)\), so the exact-central
count is \(\Theta_R(r\log r)\).

The distance to the same terminal center has the sharper two-sided order
\[
 d_\phi(0,X(s_\epsilon))=\Theta(r\sqrt{\log r}).                 \tag{32}
\]
For the upper bound, at \(s=r\) put
\(b_i=r-a_i\).  Equations (5) and
\(1-q(e^{b_i})\ge1/(1+e^{b_i})\) give
\(\varrho(q(e^{b_i}))=O(1+b_i)\), while
\(b_i\le2r/(S_r\sqrt{i-1})\) for \(i\ge2\).  Summing squares gives
\(O(r^2\log r)\).  For the lower bound, use
\(s_\epsilon>r-1\),
\(b_i\ge 2r(i^{-1/2}-r^{-1/2})/S_r\), and
\(1-q(z)\le1/z\).  For \(2\le i\le r/16\), these inequalities give
\(\varrho(q(e^{s_\epsilon-a_i}))=\Omega(r/\sqrt i)\), whose squared
sum is \(\Omega(r^2\log r)\).

The unrestricted radial schedule and the general lower half of (2) now
need \(\Theta_R(r\sqrt{\log r})\) chords to this endpoint.  Consequently,
\[
 {\text{minimum exact-central bounded-chord count}\over
  \text{minimum unrestricted same-endpoint bounded-chord count}}
                    =\Theta_R(\sqrt{\log r}).                   \tag{33}
\]
For a general weight profile, (31) is conditional on the stated progress of
the reference labels.  The explicit multiscale family is stronger.  Suppose
\(Y_0=0\) and the actual final iterate is \(\epsilon\)-accurate.  Von
Neumann's inequality and nonnegativity of the paired singular-value gaps,
together with \(w_1=1\), force \(\sigma_1(Y_K)\ge1-\epsilon\).
Singular-value contraction in the barrier metric and the terminal tube give
\[
 \varrho(q(e^{s_K}))\ge\varrho(1-\epsilon)-\zeta
                         \ge r-\log r-\zeta.                 \tag{33a}
\]
The scalar central coordinate satisfies
\[
 \varrho(q(e^s))\le1/\sqrt2+\max\{s,0\}.                    \tag{33b}
\]
Indeed, its derivative is at most one; on \(s\le0\), its squared derivative
is at most \(e^{2s}/2\), whose square root integrates from \(-\infty\) to
zero to \(1/\sqrt2\).  Hence
\(s_K\ge r-\log r-\zeta-1/\sqrt2>a_{J+1}\).  At the start,
\(d_\phi(0,X(s_0))\le\zeta\); if \(s_0>0\), the first coordinate has
\(\varrho\)-velocity at least \(v_0\), so \(s_0\le\zeta/v_0\).  The
initial clipped potential is therefore \(O_\zeta(1)\), while actual endpoint
accuracy forces full terminal progress.  Equation (31) holds for this
family from analytic-center start and actual accuracy, with no separate
endpoint-label or monotonicity hypothesis.

### 5.2 Newton-decrement neighborhoods imply a fixed metric tube

This section converts the geometric tube in (25) into a standard local
centrality condition.  Let \(f\) be a standard self-concordant convex
function with positive-definite Hessian and an attained interior minimizer
\(x_*\), and define
\(\lambda_f(x)=\|\nabla f(x)\|_{x,*}\) and
\(t=\|x_*-x\|_x\).  The global lower Hessian comparison along the segment
from \(x\) to \(x_*\) gives
\[
 -\langle\nabla f(x),x_*-x\rangle
 =\int_0^1 (x_*-x)^T\nabla^2f(x+u(x_*-x))(x_*-x)\,du
 \ge {t^2\over1+t}.                                           \tag{34}
\]
Local Cauchy--Schwarz bounds the left side by \(\lambda_f(x)t\).
Consequently, for \(\lambda_f(x)<1\),
\[
             t\le {\lambda_f(x)\over1-\lambda_f(x)}.          \tag{35}
\]
If \(\lambda_f(x)\le\beta<1/2\), the right side is below one.  Upper
Hessian comparison along the same segment then yields
\[
 d_f(x,x_*)\le-\log(1-t)
 \le \log{1-\beta\over1-2\beta}
 =:\zeta_\beta.                                                \tag{36}
\]

Apply this with
\(f_s(X)=\phi(X)-e^s\langle C,X\rangle\).  Its Hessian metric is exactly
the fixed barrier metric, and its minimizer is the center \(X(s)\).
Therefore any checkpoint sequence satisfying
\[
       \lambda_{f_{s_k}}(Y_k)\le\beta<1/2                     \tag{37}
\]
obeys (25) with \(\zeta=\zeta_\beta\).  Under either the reference-progress
hypotheses used in (30), or the analytic-start and actual-accuracy
hypotheses proved in (33a)--(33b), (31) becomes
\[
 K=\Omega_{R,\beta}(r\log r),
 \qquad
 D={2\zeta_\beta-\log(1-R)\over v_0}.                         \tag{38}
\]
Thus the sharp discrete tax covers the usual fixed
Newton-decrement neighborhoods for every fixed \(\beta<1/2\).  The strict
half threshold is needed by this conversion: at \(\beta\uparrow1/2\),
the guaranteed local displacement reaches one and the upper metric
comparison in (36) diverges.  Equation (38) remains a fixed-standard-barrier
movement theorem.  It is not a generic QIPM runtime or oracle lower bound.

### 5.3 One-query checkpoint states versus linear classical readout

The sharp movement witness can carry hidden sparse data without changing
its geometry.  Let \(b\in\{0,1\}^r\), \(\sigma_j=(-1)^{b_j}\), and replace
(14) by the one-sparse diagonal objective
\[
             C_b=\operatorname{Diag}(\sigma_1w_1,\ldots,
                                      \sigma_rw_r),             \tag{39}
\]
where all magnitudes \(w_j=e^{-a_j}\) are public.  A raw sign oracle
\(O_b:|j,z\rangle\mapsto|j,z\oplus b_j\rangle\) and a sparse coefficient
value oracle for (39) simulate one another with constant query overhead,
provided the latter returns exact values or additive error below
\(w_{\min}/2=e^{-r}/2\).  Thus the coefficient implementation must charge
\(\Theta(r)\) bits of worst-case value precision in this family even though
the number of oracle calls is constant.
All singular values, the optimum value, the first accurate parameter
\(s_\epsilon\), and every scalar checkpoint magnitude are public and
independent of \(b\).

For an exact central checkpoint at parameter \(s\), put
\(y_j(s)=q(e^{s-a_j})\).  For the radial shortcut to a fixed terminal
center, put
\(y_j(u)=\varrho^{-1}(u\varrho(y_j(s_\epsilon)))\).  In either case its
normalized vectorization is
\[
 {1\over\|y\|_2}\sum_{j=1}^r\sigma_jy_j|j,j\rangle.            \tag{40}
\]
Given an exact public preparation of
\(\|y\|_2^{-1}\sum_jy_j|j,j\rangle\), one phase-kickback query to the
standard clean XOR oracle \(O_b\), with its target in \(|-\rangle\), prepares
(40) exactly.  Starting instead from a coefficient-value oracle still costs
only \(O(1)\) calls, but a clean implementation generally uses a second call
to uncompute its value register.  The public amplitude-table construction,
scalar precision, and each requested copy are charged separately; at the
analytic center the zero matrix has no normalized state.

At the first accurate terminal center, (17) and \(a_j\le r\) imply
\[
             y_j(s_\epsilon)>q(e^{-1})>0\quad\hbox{for every }j. \tag{41}
\]
Hence a classical matrix \(\widetilde X\) satisfying
\[
 \max_j|\widetilde X_{jj}-\sigma_jy_j(s_\epsilon)|
                         <{q(e^{-1})\over2}                    \tag{42}
\]
reveals every hidden sign.  Producing such an output with bounded error
uses \(\Theta(r)\) raw queries both quantumly and randomized: reading all
signs is an upper bound, and any successful output computes their parity,
whose bounded-error quantum and randomized query complexities are
\(\Omega(r)\).  Scalar optimum or objective-value output is public here
and has no query lower bound.

Because signs do not affect singular values or the standard-barrier metric,
the very same instance satisfies
\[
 T_{\rm exact\ central}=\Theta_R(r\log r),\qquad
 T_{\rm unrestricted\ same\ endpoint}
                  =\Theta_R(r\sqrt{\log r}),                  \tag{43}
\]
as well as the Newton-decrement-neighborhood lower (38).  Equations
(40)--(43) are a same-instance conjunction: easy normalized checkpoint
states, a sharp \(\sqrt{\log r}\) centrality tax, and hard full classical
readout.  They do not justify multiplying a query cost by a movement count.

## 6. Why this is not yet a QIPM improvement

The shortcut uses more information than a generic IPM step:

1. It knows the complete singular frame and weights, hence also the exact
   boundary optimum \(-\|C\|_*\).  If only the final answer is wanted,
   outputting the polar factor \(UV^*\), or an interior approximation to
   it, is simpler than constructing any path.
2. It explicitly solves the global endpoint problem (7).  Ordinary IPMs
   use local Newton systems because such a global reduction is unavailable.
3. Its intermediate points need not lie in a central neighborhood for any
   objective multiplier.  Standard primal--dual feasibility, complementarity,
   and short-step convergence invariants therefore do not apply.
4. Generic affine constraints couple singular vectors and invalidate both
   von Neumann alignment and the Euclidean radial coordinates.  The method
   extends only to uncoupled spectral blocks, or constraints already reduced
   to the same fixed singular frame.
5. All movement statements use the restricted primal barrier metric.
   Nesterov--Todd's \(\sqrt2\)-geodesic theorem instead uses the combined
   product metric of a logarithmically homogeneous primal--dual cone pair.
   A full primal--dual method inherits the lower bound only when primal
   feasibility and its neighborhood and step contracts project to this
   primal contract.  The primal radial shortcut supplies no dual-feasible
   trajectory to the central dual endpoint, so no primal--dual
   \(\sqrt{\log r}\) separation follows automatically.  Indeed, between
   finite primal--dual central endpoints, Nesterov--Todd's inequality and
   the chord comparisons make arclength-partitioned central tracking
   constant-factor optimal in the combined metric.  A dimension-growing
   tax cannot survive when the entire dual trajectory is charged under that
   contract.
6. In the sparse diagonal witness (14), classical preprocessing, direct
   optimization, and every implicit checkpoint generator cost only
   \(O(rB)\), where \(B\) charges scalar precision and the exponentially
   wide weight range.  There is no end-to-end quantum advantage to explain.

The defensible algorithmic consequence is therefore narrow but exact:
**when a feasible trajectory of bounded standard-barrier Dikin moves is
itself the required contract, SVD water filling plus the radial geodesic is
the optimal movement algorithm up to radius constants.**  It can be used as
a shortcut primitive inside a larger method only when the larger problem
preserves the fixed singular subspace and separately supplies its access,
duality, and output guarantees.  Calling it a general singular-rank-adaptive
QIPM would overstate the result.

## Audit checklist

- Verify the direction of both self-concordant chord inequalities in (11)
  and (2).
- Check that (8) has a unique positive multiplier and strictly interior
  coordinates for every \(0<\epsilon<\|C\|_*\).
- Check the finite-precision safety-margin argument near the boundary.
- For general weights, the near-central theorem is conditional on reference
  progress.  For the explicit multiscale family, analytic-center start and
  actual endpoint accuracy force that progress by (33a)--(33b).
- Do not transfer the primal shortcut comparison to a combined primal--dual
  metric without constructing and charging a dual trajectory.
- Do not turn SVD access or an amplitude table into a free sparse-input
  oracle, and do not multiply movement by readout or preprocessing costs.

## Independent hostile audit

The audit checked the water-filling endpoint, monotone multiplier search,
and strict interiority in (7)--(8).  The fixed-SVD path (9) is feasible and
globally minimizing by the independently audited exact distance theorem.
For the upper move bound, an arc of length \(\log(1+\theta)\) has endpoint
chord norm at most \(\theta\); for the lower bound, a forward
\(\theta\)-Dikin chord has straight-segment length at most
\(-\log(1-\theta)\).  Thus both directions and constants in (2) are
correct.

The finite-precision paragraph uses explicit objective and Dikin-radius
slack and does not claim a uniform strongly polynomial arithmetic bound.
The state-access section charges the singular frames and amplitude table
and keeps movement, state preparation, and readout as separate resources.
The audit also repaired the final paragraph of Section 5: the universal
\(\Gamma_r\) theorem compares a central arc with the distance to its own
endpoint, not with the closest endpoint in an accuracy sublevel.

A further hostile audit established the stronger discrete theorem in
Section 5.1.  It verified the exact shared-frame pair-distance formula,
including the full ambient lower bound and singular-value ordering; the
forward/backward reference-parameter estimate; the fixed-neighborhood
triangle bound; the threshold-gap and clipped-potential accounting; and the
two-sided \(\Theta(r\sqrt{\log r})\) terminal distance.  It also identified
the reference-progress condition needed for a general weight profile.  For
the explicit multiscale family, the later endpoint-driven argument
(33a)--(33b) eliminates that extra hypothesis: analytic-center start and
actual endpoint accuracy force the reference labels across the hard range.

The final audit verified the Newton-decrement conversion (34)--(38),
including the global lower comparison, the strict \(\beta<1/2\) range, and
the exact metric radius.  It also checked the exact
\(\mathcal W_\varrho\) residual, relative mean-estimation laws, root
condition number, and state-preparation success factor in Section 4.1;
the custom coherent \(\ell_1\)-sampler is explicitly distinguished from
ordinary length-square/SQ access.  For the signed construction it checked
the sign isometry, terminal magnitude floor, phase-kickback preparation,
coefficient precision, parity readout lower bound, and preservation of all
movement results.  No movement, preprocessing, state-copy, or readout costs
are multiplied.
