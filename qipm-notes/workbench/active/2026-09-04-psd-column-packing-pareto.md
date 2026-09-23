# Exact Pareto ledger for PSD column packing

Status: Proved; literature-screened; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the fixed-family and proxy scopes stated below

## Result

Let

\[
                         C=(B_2^s)^b,
             \qquad b\geq2,\quad s\geq3.                 \tag{1}
\]

The PSD column-packing lift is described in
[PSD column packing shares full product-ball slack
rows](2026-09-04-psd-column-packing-product-balls.md).  This note solves
the finite resource optimization internal to that construction and
separates five conclusions that are easy to conflate:

1. balanced row and column widths minimize the usual static continuous
   resource ledgers;
2. after multiplying factor count, ambient parameter, or cone dimension by
   the standard short-step multiplier
   \(\sqrt{\nu_{\rm slice}}\), balance is no longer optimal--the cap-active
   continuum optimum is \(p:c=3:2\); and
3. against direct Lorentz lifts, PSD sharing buys factor count, and in a
   many-small-balls regime ambient rank, but never total cone-coordinate
   dimension or restricted barrier parameter when the order cap is absent;
   and
4. every globally selected PSD lift satisfies an exact joint
   factor--boundary-nullity capacity envelope, whose continuous optimum
   produces the general \(p:c=(1+\theta):1\) rule and universal lower
   bounds for \(J_\omega\nu^\theta\) that the packing construction
   asymptotically attains; and
5. among all globally bi-\(C^1\) real PSD factorizations with order cap
   \(R\), not just column packings, the exact minimum standard-slice
   parameter is \(b\lceil s/(R-1)\rceil\). Thus packed factor sharing can
   lower block count, but cannot beat grouped Schur lifts on the iteration
   certificate itself; and
6. if work charges only genuinely free affine coordinates rather than the
   full ambient cone arrays, the exact optimum returns to the unshared
   grouped Schur point. This separates a realistic variable-materialization
   ledger from full-factor serialization.

These are formulation and barrier comparisons.  The proxy optimization
below is not an end-to-end IPM or QIPM runtime theorem.

## 1. An exact two-integer Pareto parameterization

Choose a padded row width \(p\in[s]\).  Splitting every source ball into
groups of at most \(p\) coordinates gives

\[
             h_p=\left\lceil {s\over p}\right\rceil,
             \qquad H_p=b h_p.                            \tag{2}
\]

Here \(H_p\) is both the number of packed columns and the exact parameter
of the restricted standard log-determinant barrier.  Put the \(H_p\)
columns into \(\ell\) nonempty PSD blocks, where
\(1\leq\ell\leq H_p\).  Write

\[
 H_p=q\ell+t,\qquad 0\leq t<\ell,\qquad
 d_r={r(r+1)\over2}.                                      \tag{3}
\]

Balancing the column counts makes \(\ell-t\) blocks contain \(q\)
columns and \(t\) blocks contain \(q+1\) columns.  The resulting exact
ledger is

\[
\boxed{
\begin{aligned}
 L(p,\ell)&=\ell,\\
 G(p,\ell)&=H_p,\\
 r_{\max}(p,\ell)&=p+\left\lceil {H_p\over\ell}\right\rceil,\\
 \nu_{\rm slice}(p,\ell)&=H_p,\\
 \nu_{\rm ambient}(p,\ell)&=p\ell+H_p,\\
 M(p,\ell)&=(\ell-t)d_{p+q}+t d_{p+q+1},\\
 V(p,\ell)&=bs+(\ell-t)d_q+t d_{q+1}.
                                                               \tag{4}
\end{aligned}}
\]

In (4), \(L\) is PSD factor count, \(G\) is group count,
\(r_{\max}\) is maximum matrix order, \(M\) is the total number of cone
coordinates, and \(V\) is the number of free affine scalar coordinates
before imposing the \(b\) source equations: \(bs\) true entries of \(W\), plus the entries of
the free symmetric matrices \(S_\ell\). (Padded zeros and the public
identity blocks are not counted.) Formula (4), followed by ordinary dominance
pruning, is the exact Pareto frontier of the fixed-width column-packing
family.

Indeed, for fixed \((p,\ell)\), maximum block order, \(M\), and \(V\) are
minimized by balanced column counts.  If two counts differ by at least
two, moving one column from the larger to the smaller block does not
increase the maximum and, by strict convexity of \(d_{p+c}\) in \(c\),
lowers both \(M\) and the convex \(S\)-coordinate sum in \(V\). Repeating
reaches a balanced allocation.
The remaining entries of (4) do not depend on the allocation.  Values
\(p>s\) are dominated by \(p=s\), so (4) is a finite exact enumeration.

Under an order cap \(r_{\max}\leq R\), it is enough to enumerate

\[
 1\leq p\leq\min\{s,R-1\},\qquad
 \left\lceil {H_p\over R-p}\right\rceil\leq\ell\leq H_p. \tag{5}
\]

In particular, three exact scalar optima are

\[
\boxed{
\begin{aligned}
 L_{\min}(R)
   &=\min_p\left\lceil {H_p\over R-p}\right\rceil,\\
 \nu_{{\rm slice},\min}(R)
   &=b\left\lceil {s\over\min\{s,R-1\}}\right\rceil,\\
 \nu_{{\rm ambient},\min}(R)
   &=\min_p\left\{H_p+p
          \left\lceil {H_p\over R-p}\right\rceil\right\}.
                                                               \tag{6}
\end{aligned}}
\]

The minima range over the \(p\)'s in (5).  The exact cone-dimension
minimum is

\[
 M_{\min}(R)=
 \min_{p}\ \min_{\ell\geq\lceil H_p/(R-p)\rceil}M(p,\ell), \tag{7}
\]

an \(O(sH_1)\) direct enumeration, or faster after grouping intervals on
which \(\lceil s/p\rceil\) and \(\lfloor H_p/\ell\rfloor\) are constant.
Equations (4)--(7), rather than the single choice
\(p=\lfloor R/2\rfloor\), retain all ceiling and final-block effects.
They also give exact discrete short-step-weighted proxy optima without a
new argument.  For example,

\[
\begin{aligned}
 \min L\sqrt{\nu_{\rm slice}}
   &=\min_p \sqrt{H_p}
          \left\lceil {H_p\over R-p}\right\rceil,\\
 \min \nu_{\rm ambient}\sqrt{\nu_{\rm slice}}
   &=\min_p\sqrt{H_p}\left(H_p+p
          \left\lceil {H_p\over R-p}\right\rceil\right),\\
 \min M\sqrt{\nu_{\rm slice}}
   &=\min_p\min_{\ell\geq\lceil H_p/(R-p)\rceil}
          \sqrt{H_p}\,M(p,\ell).                          \tag{7a}
\end{aligned}
\]

Thus (12) below is an interpretable closed-form limit of exact finite
programs, not a replacement for them in small ceiling-sensitive cases.

The free-affine-coordinate ledger has a simpler exact optimum. Put
\[
 p_*=\min\{s,R-1\},\qquad H_*=b\left\lceil{s\over p_*}\right\rceil .
\]
For every \(\theta\geq0\),
\[
\boxed{
 \min_{p,\ell}V(p,\ell)\nu_{\rm slice}(p,\ell)^\theta
       =(bs+H_*)H_*^\theta.}                              \tag{7b}
\]
For fixed \(p\), splitting a column block of sizes \(c_1+c_2\) lowers
\(d_{c_1+c_2}\) by \(c_1c_2\). Hence \(V\) is minimized by
\(\ell=H_p\), one column per block, and equals \(bs+H_p\). The function
\((bs+H)H^\theta\) increases with \(H\), so the largest feasible row width
\(p_*\) is optimal. Smaller widths on the same ceiling plateau can tie it.
In the cap-active branch, the canonical optimum
\(p:c=(R-1):1\) is exactly the grouped Schur construction.

There is a useful exact identity behind (7):

\[
 d_{p+c}=(2p+1)c+{(p-c)(p-c+1)\over2}.                    \tag{8}
\]

Consequently every packing obeys

\[
                  M\geq(2p+1)H_p\geq b(2s+1).             \tag{9}
\]

For fixed \(p\), equality in the first inequality holds exactly when
every block has \(c=p\) or \(c=p+1\) columns.  Thus the dimension-efficient
block aspect ratio is exactly balanced up to one column, even though a
cap or an indivisible remainder can prevent equality.

## 2. A universal joint factor--nullity lower envelope

The same aspect-ratio optimization is forced by the mixed-curvature lower
bound, not only by the construction.  Consider any globally selected
\(C^1\) full-contact factorization of (1) over \(L\) PSD blocks of order at
most \(R\).  At a simultaneous product extreme \(x\), let

\[
                  c_i(x)=\operatorname{nullity}X_i(x),
             \qquad Z(x)=\sum_{i=1}^L c_i(x).              \tag{9a}
\]

The primal rank is at most \(R-c_i\), the complementary dual rank is at
most \(c_i\), and the block's mixed-curvature rank is therefore at most
\(c_i(R-c_i)\).  Since the product contact pairing has rank

\[
                            n=b(s-1),
\]

one obtains the joint inequality

\[
                         n\leq\sum_{i=1}^L c_i(R-c_i).      \tag{9b}
\]

This contains more information than separate lower bounds on \(L\) and
boundary nullity.  Define the exact integer budget envelope

\[
 {\cal C}_R(L,z)=
 \max\left\{\sum_{i=1}^Lc_i(R-c_i):
       c_i\in\{0,\ldots,R\},\ \sum_i c_i\leq z\right\},
       \qquad z\in\mathbb Z_{\geq0}.                        \tag{9c}
\]

Put \(m=\lfloor R/2\rfloor\), \(z'=\min\{z,Lm\}\), and write
\(z'=qL+t\), \(0\leq t<L\).  Discrete concavity gives the closed form

\[
\boxed{
 {\cal C}_R(L,z)
  =(L-t)q(R-q)+t(q+1)(R-q-1).}                            \tag{9d}
\]

Indeed, below \(m\) every unit of nullity has nonnegative marginal
capacity and balancing the \(c_i\)'s maximizes their concave sum; above
\(Lm\), every block already attains
\(\lfloor R^2/4\rfloor\).

Let \(\nu\) be the parameter of the standard product log-determinant
restricted to the affine lift slice.  The boundary-vanishing-order lemma
gives \(\nu\geq Z(x)\) at every contact. The private-kernel theorem for
the product rows gives \(Z(x)\geq b\). Under the globally bi-\(C^1\)
hypotheses of the sequential contact-range theorem, the sharp sourcewise
bound is

\[
             Z(x)\geq b\left\lceil{s\over R-1}\right\rceil
             \quad\hbox{at some simultaneous contact}.               \tag{9e0}
\]

Consequently every such lift obeys the exact coupled necessary conditions

\[
\boxed{
       \lfloor\nu\rfloor\geq b\left\lceil{s\over R-1}\right\rceil,
       \qquad
       {\cal C}_R\!\left(L,\lfloor\nu\rfloor\right)
                 \geq b(s-1).}                            \tag{9e}
\]

The first inequality is sharp: grouped real Schur blocks attain it. It is
not obtained by inserting a topological \(+1\) into (9b); it follows from
the separate one-ball contact-range lemma and sequential compression.
The capacity inequality remains a pointwise mixed-curvature constraint.

For \(z\leq LR/2\), Cauchy--Schwarz gives the convenient continuous
relaxation

\[
 n\leq Rz-{z^2\over L},\qquad
 L\geq {z^2\over Rz-n}.                                   \tag{9f}
\]

In the cap-active wide-ball regime where the sharp sourcewise constraint
\(z\geq b\lceil s/(R-1)\rceil\) and source-availability constraints are
slack, parameterize equality by a common nullity \(c=z/L\) and
\(p=R-c\). Minimizing the lower-envelope
proxy \(Lz^\theta\) is then equivalent to maximizing
\(p^{1+\theta}c\), and again gives

\[
                         p:c=(1+\theta):1.                 \tag{9g}
\]

Thus, within that regime, the \(3:2\) rule at \(\theta=1/2\) optimizes the
universal factor--nullity capacity relaxation, not merely the explicit
packing family. Since equality would have \(z=n/p\), the sharp sourcewise
constraint is equivalent to
\[
 p\leq {b(s-1)\over b\lceil s/(R-1)\rceil}.
\]
If the unconstrained optimizer exceeds this bound, the universal
relaxation is boundary-limited instead.
The construction approaches equality when source-group, last-block, and
\(s\) versus \(s-1\) losses are negligible.  Equation
(9e) remains only a necessary formulation/barrier ledger; it does not
assert that every integer point on the envelope is realizable by a lift.

The relaxation gives a sharp universal two-parameter family of proxy
bounds. Define the block-work ledger

\[
                         J_\omega=\sum_{i=1}^Lr_i^\omega.              \tag{9h}
\]

Thus \(J_0=L\), \(J_1=\nu_{\rm ambient}\), and the order cap gives the
exact triangular comparison

\[
 M=\sum_i{r_i(r_i+1)\over2}
   \geq {1+1/R\over2}J_2.                                \tag{9h0}
\]

Fix \(\theta\geq0\) and
\(0\leq\omega\leq2+\theta\), and put

\[
 K_\theta={1+\theta\over2+\theta}
       \left({1\over2+\theta}\right)^{1/(1+\theta)}.
\]

For \(p_i=r_i-c_i\), the order cap and a one-variable maximization give

\[
 p_ic_i
 \leq K_\theta R^{(2+\theta-\omega)/(1+\theta)}
          r_i^{\omega/(1+\theta)}
          c_i^{\theta/(1+\theta)}.                        \tag{9i}
\]

Indeed, after writing \(p_i=xr_i\), the remaining shape factor is
\(x(1-x)^{1/(1+\theta)}\), uniquely maximized at
\(x=(1+\theta)/(2+\theta)\); the remaining scale factor is at most one.
Summing (9i), applying Hölder with conjugate exponents \(1+\theta\) and
\((1+\theta)/\theta\), using (9b), and using
\(\nu\geq z=\sum_i c_i\) yield

\[
\boxed{
 J_\omega\nu^\theta\geq
 {(2+\theta)^{2+\theta}\over(1+\theta)^{1+\theta}}
 {\{b(s-1)\}^{1+\theta}\over R^{2+\theta-\omega}},
 \quad\substack{\theta\geq0,\\0\leq\omega\leq2+\theta}.}       \tag{9j}
\]

For \(\theta=0\), the Hölder step is read in its limiting, elementary
form; (9i) simply sums directly. This case proves that the balanced
\(p:c=1:1\) shape is globally optimal for the static continuous lower
bound. For the short-step exponent \(\theta=1/2\), (9j) becomes

\[
 J_\omega\sqrt\nu\geq
 {25\over6}\sqrt{5\over3}\,
 {\{b(s-1)\}^{3/2}\over R^{(5-2\omega)/2}},
 \qquad0\leq\omega\leq{5\over2}.                       \tag{9k}
\]

It simultaneously lower-bounds factor count, ambient rank, and quadratic
block work, with the unique shape \(p:c=3:2\). Together with (9h0), it
also gives

\[
 M\sqrt\nu\geq
 {25\over12}\sqrt{5\over3}\,
 \left(1+{1\over R}\right)
 {\{b(s-1)\}^{3/2}\over\sqrt R}.                         \tag{9l}
\]

More generally, the equality shape in (9j) is exactly
\(p:c=(1+\theta):1\), and the endpoint \(\omega=2+\theta\) is exactly
where increasing block scale stops improving the bound.

When divisibility permits the stated equality shape and full order-\(R\)
packed blocks, column packing attains (9j) with \(bs\) in place of
\(b(s-1)\). Its ratio to the universal bound is exactly
\((s/(s-1))^{1+\theta}\) for \(J_0\), \(J_1\), and the exact
cone-coordinate ledger: the triangular factor \(1+1/R\) occurs on both
sides by (9h0). Thus these cap-active divisible packings are asymptotically
optimal among all lifts in the globally selected standard-barrier scope
as \(s\to\infty\), even for fixed \(R\). If the sourcewise lower bound in
(9e) is active, the exact integer envelope is stronger than this
continuous family.

## 3. What balance optimizes--and what it does not

Remove ceilings and the last partial block, put \(H=bs/p\), use full
blocks of \(c\) columns, and assume the order cap is active:
\(p+c=R\).  The continuous ledgers are

\[
\begin{aligned}
 H&={bs\over p},\\
 L&={bs\over pc},\\
 \nu_{\rm ambient}&={bsR\over pc},\\
 M&={bsR(R+1)\over2pc}.                                  \tag{10}
\end{aligned}
\]

Each of \(L\), \(\nu_{\rm ambient}\), and \(M\) alone is minimized by
maximizing \(pc\), hence by \(p=c=R/2\).  This is the precise sense in
which balanced column packing is optimal.

The conclusion changes when the iteration certificate is charged.  Let
\(J\) be any one of the three static ledgers in (10), and consider

\[
                         P_\theta=H^\theta J,
                         \qquad \theta\geq0.               \tag{11}
\]

Up to a factor independent of \(p,c\),

\[
                  P_\theta={1\over p^{1+\theta}c}.
\]

Under \(p+c=R\), strict log concavity gives the unique optimum

\[
\boxed{
               {p\over R}={1+\theta\over2+\theta},
       \qquad {c\over R}={1\over2+\theta}.}               \tag{12}
\]

Thus static resources (\(\theta=0\)) select \(p:c=1:1\), while the
standard short-step multiplier \(\sqrt{\nu_{\rm slice}}=\sqrt H\)
selects

\[
                              \boxed{p:c=3:2}.              \tag{13}
\]

This conclusion deliberately excludes the free-coordinate ledger \(V\).
Equation (7b) shows that \(V\nu_{\rm slice}^\theta\) always selects
single-column Schur blocks. Counting the public identity entries inside
each ambient PSD matrix, as \(M\) does, and counting only coordinates that
an affine implementation must update are different cost models.

This is not a small ceiling artifact.  For example, take
\((b,s,R)=(20,30,10)\).  Both candidate packings have no partial source
group or partial PSD block:

\[
\begin{array}{c|ccccc|ccc}
(p,c)&H&L&\nu_{\rm ambient}&M&r_{\max}
 &L\sqrt H&\nu_{\rm ambient}\sqrt H&M\sqrt H\\ \hline
(5,5)&120&24&240&1320&10
 &24\sqrt{120}&240\sqrt{120}&1320\sqrt{120}\\
(6,4)&100&25&250&1375&10
 &250&2500&13750
\end{array}                                                \tag{14}
\]

The balanced choice wins every static column in (14), but the \(3:2\)
choice wins every short-step-weighted proxy.

The same phenomenon has a useful limitation.  If a sequential
implementation spends \(r^\omega\) operations per order-\(r\) block, its
ceiling-free uniform-block proxy is

\[
 H^\theta\sum_jr_j^\omega
  =(bs)^{1+\theta}p^{\omega-2-\theta}
       {(1+c/p)^\omega\over c/p}.                          \tag{15}
\]

If \(\omega<2+\theta\), scale is beneficial, the cap is active, and the
same ratio (12) follows, provided source-width and column-availability
bounds do not bind.  If \(\omega=2+\theta\), scale is neutral and (12)
still minimizes the shape.  If \(\omega>2+\theta\), the upper cap ceases
to bind; lower-size and integrality constraints determine the optimum, so
there is no universal aspect ratio.  In particular, with \(\theta=1/2\), the
\(3:2\) result applies to linear, factor-count, ambient-rank, and quadratic
cone-coordinate proxies, but not automatically to naive dense cubic
matrix algebra.  Nor does it account for the presently unresolved
treewidth and conditioning of a packed Newton system.

## 4. Exact comparison with Lorentz and blockwise Schur lifts

With the same raw order cap \(3\leq R<s+1\), the grouped paraboloid
Lorentz construction has

\[
\begin{aligned}
 h_L&=\left\lceil{s\over R-2}\right\rceil,&
 L_L&=\nu_{L,{\rm slice}}=b h_L,\\
 \nu_{L,{\rm ambient}}&=2b h_L,&
M_L&=bs+2b h_L.                                         \tag{16}
\end{aligned}
\]

Once \(R\geq s+1\), the better direct \(Q_{s+1}\) lift uses one factor
per source and has

\[
       (L_L,\nu_{L,{\rm slice}},\nu_{L,{\rm ambient}},M_L)
                   =(b,b,2b,b(s+1)).                      \tag{16a}
\]

The factor-minimal, cap-saturating blockwise PSD Schur construction has

\[
 h_S=\left\lceil{s\over R-1}\right\rceil,qquad
 L_S=\nu_{S,{\rm slice}}=b h_S,qquad
 \nu_{S,{\rm ambient}}=bs+b h_S.                         \tag{17}
\]

For its exact cone dimension, write \(s=a h_S+t\),
\(0\leq t<h_S\).  Balancing within every source ball gives

\[
 M_S=b\{(h_S-t)d_{a+1}+t d_{a+2}\}.                       \tag{18}
\]

The free-affine-coordinate comparison points in the opposite direction
from full cone dimension. In the grouped branch,
\[
                 V_L=bs+h_Lb,\qquad V_S=bs+h_Sb,           \tag{18a}
\]
before the common \(b\) source equations. Since an order-\(R\) PSD Schur
block carries \(R-1\) source coordinates while the rotated-Lorentz
paraboloid block carries \(R-2\),
\[
                         h_S\leq h_L.
\]
Thus grouped PSD Schur weakly dominates grouped Lorentz in both \(V\) and
restricted parameter under the same raw order cap, strictly whenever the
ceilings differ. This does not contradict the cone-coordinate comparison:
the public identity part of a PSD block is large in \(M\) but absent from
\(V\). After subtracting the \(b\) equations, the direct large-cap branches
both have \(bs\) affine degrees of freedom and restricted parameter \(b\).

Equations (16)--(18) are exact and expose an important modeling issue:
an order-\(R\) Lorentz cone has \(R\) scalar coordinates, whereas
\(\mathbb S_+^R\) has \(R(R+1)/2\).  A raw order-cap comparison therefore
favors PSD packing in factor count without matching input dimension.

In the cap-active, ceiling-free wide-ball regime, the three constructions
have the following leading ledgers:

\[
\begin{array}{c|cccc}
 &L&\nu_{\rm slice}&\nu_{\rm ambient}&M\\ \hline
\text{Lorentz grouped}
  &bs/R&bs/R&2bs/R&bs\\
\text{PSD blockwise Schur, minimum factor count}
  &bs/R&bs/R&bs&bsR/2\\
\text{PSD column pack, }p=c=R/2
  &4bs/R^2&2bs/R&4bs/R&2bs.
\end{array}                                                \tag{19}
\]

Thus column packing trades roughly twice the restricted parameter for an
order-\(R\) reduction in factor count relative to the factor-minimal Schur
point.  It also reduces that point's ambient rank and cone coordinates by
order \(R\).  This is not a comparison with the dimension-minimizing
Schur point: singleton or two-coordinate Schur groups attain total cone
dimension \(3bs\), at the price of many more factors.  Direct Lorentz
grouping still uses about half the packed
construction's restricted parameter, ambient parameter, and total cone
coordinates, but about \(R/4\) times as many factors.  If instead the
per-factor scalar-coordinate cap is matched at \(D\), so a PSD order is
only \(R\asymp\sqrt{2D}\) while a Lorentz factor can have order \(D\),
the cap-active leading terms become

\[
\begin{array}{c|cccc}
 &L&\nu_{\rm slice}&\nu_{\rm ambient}&M\\ \hline
\text{Lorentz}&bs/D&bs/D&2bs/D&bs\\
\text{PSD pack}&2bs/D&\sqrt2bs/\sqrt D&
                    2\sqrt2bs/\sqrt D&2bs.
\end{array}                                                \tag{20}
\]

So the PSD construction has no asymptotic ledger advantage in this
matched-coordinate, cap-active regime.  Its genuine distinctive resource
is cross-source factor sharing.

That distinction is sharp without a cap.  Direct Lorentz lifting uses

\[
       (L,\nu_{\rm slice},\nu_{\rm ambient},M)
                   =(b,b,2b,b(s+1)).                      \tag{21}
\]

Every PSD column packing obeys \(\nu_{\rm slice}=H_p\geq b\) and, by
(9),

\[
                         M\geq b(2s+1)>b(s+1).             \tag{22}
\]

Consequently the direct Lorentz formulation strictly beats every member
of the PSD packing family on both \(M\) and \(\nu_{\rm slice}\), and hence
also on every monotone proxy such as
\(M\sqrt{\nu_{\rm slice}}\).  Cross-source PSD sharing cannot by itself
produce a scalar-work advantage when cone-coordinate processing is the
per-round bottleneck.

But one PSD factor is always possible, with exact minimum order and
ambient parameter within the fixed-width column-packing family

\[
                 r_{\rm one}
                  =\min_{1\leq p\leq s}
                       \left\{p+b\left\lceil{s\over p}\right\rceil\right\}.
                                                               \tag{23}
\]

Moreover,

\[
                    r_{\rm one}<2b\quad\Longleftrightarrow\quad b>s.
                                                               \tag{24}
\]

For if \(\lceil s/p\rceil\geq2\), the expression in (23) is strictly
larger than \(2b\); if it equals one, \(p=s\) is optimal and gives
\(s+b<2b\) exactly when \(b>s\).  Hence, for many low-dimensional source
balls, a one-factor PSD packing improves both factor count and ambient
normal parameter over direct Lorentz lifting, while tying its restricted
parameter at \(p=s\).  It necessarily pays more scalar cone coordinates.
For \(b\leq s\), it can still reduce factor count, but not the ambient
parameter below \(2b\).

### Short-step-weighted comparison at each construction's own optimum

The endpoints in (19) do not optimize every short-step-weighted ledger.
The following divisible benchmark makes the distinction exact. Put
\(A=bs\), ignore only final partial groups, and let a blockwise Schur lift
use source-group width \(g\). Then

\[
 L=\nu={A\over g},\qquad
 \nu_{\rm ambient}=A\left(1+{1\over g}\right),\qquad
 M={A(g+1)(g+2)\over2g}.                                 \tag{24a}
\]

Thus \(L\sqrt\nu\) and \(\nu_{\rm ambient}\sqrt\nu\) decrease strictly
with \(g\), so their Schur optimum uses the largest allowed width
\(g=\min\{s,R-1\}\). In contrast,

\[
 M\sqrt\nu
   =A^{3/2}{(g+1)(g+2)\over2g^{3/2}}.                    \tag{24b}
\]

Among positive integer widths, (24b) has its unique minimum at
\(g=4\), with value \(15A^{3/2}/8\). Indeed, the ratio of the values at
\(g+1\) and \(g\) is at most one exactly when

\[
 g^3(g+3)^2\leq(g+1)^5,
\]

and the difference
\((g+1)^5-g^3(g+3)^2=-g^4+g^3+10g^2+5g+1\) is positive
through \(g=3\) and negative, strictly decreasing, from \(g=4\) onward.
If \(g=4\) is unavailable because \(\min\{s,R-1\}<4\), the best available
width is \(\min\{s,R-1\}\).

This remains globally optimal among heterogeneous Schur groupings in the
divisible case \(4\mid s\). For fixed group count, convexity of
\(d_{g+1}\) makes the widths differ by at most one. On each interval
\(k\leq\bar g\leq k+1\), the balanced average cone cost is the chord
between \(d_{k+1}\) and \(d_{k+2}\). Dividing that chord by
\(\bar g^{3/2}\) has no interior minimum, so the global minimum occurs at
an integer width; the preceding ratio test selects \(g=4\). Thus the
value \(15A^{3/2}/8\) is not merely the best uniform-width choice.

At the column-packing optimum \(p:c=3:2\), taking
\(p=3R/5\), \(c=2R/5\) and assuming the divisions are integral gives

\[
\begin{aligned}
 L\sqrt\nu
   &={25\over6}\sqrt{5\over3}\,{A^{3/2}\over R^{5/2}},\\
 \nu_{\rm ambient}\sqrt\nu
   &={25\over6}\sqrt{5\over3}\,{A^{3/2}\over R^{3/2}},\\
 M\sqrt\nu
   &={25\over12}\sqrt{5\over3}
        \left(1+{1\over R}\right){A^{3/2}\over\sqrt R}.
                                                               \tag{24c}
\end{aligned}
\]

Hence column packing improves all three weighted PSD ledgers by an
order-\(R\) factor over the cap-saturating Schur lift. It also eventually
beats the globally proxy-optimal Schur width \(g=4\) on
\(M\sqrt\nu\). The grouped Lorentz lift, however, has

\[
 M\sqrt\nu={A^{3/2}R\over(R-2)^{3/2}},                   \tag{24d}
\]

so its leading constant is one, versus
\((25/12)\sqrt{5/3}\approx2.69\) for packed PSD blocks. Thus the packed
construction's scalar-coordinate proxy advantage is relative to other
PSD lifts, not to Lorentz modeling. Ceilings are handled by the exact
enumerations (4)--(7), (16)--(18); equations (24a)--(24d) state the clean
divisible/asymptotic comparison.

## 5. QIPM interpretation and novelty boundary

The exact frontier (4)--(7) is useful when a QIPM analysis charges matrix
order, block count, ambient normal parameter, and restricted parameter
separately.  The shift (12)--(14) shows that optimizing a formulation
before multiplying by its iteration certificate can select the wrong
block aspect ratio.  It does **not** show that a \(3:2\) packed lift is the
fastest implementation: the packed Newton graph can have dense
within-block and cross-source coupling, whereas the Lorentz and blockwise
Schur reductions have linear-size tree expansions.

There is an exact iteration baseline against which these proxies must be
read. The
[sequential contact-range theorem](2026-09-04-hermitian-sequential-contact-range-frontier.md)
proves, for every globally bi-\(C^1\) real PSD lift of the full product-ball
slack with order cap \(R\),

\[
            \nu_{\rm std,slice}\geq
              b\left\lceil{s\over R-1}\right\rceil.       \tag{25}
\]

Grouped Schur lifts attain (25). If the factors are genuine affine-slice
dual certificates, the same theorem gives a support objective whose
path-independent log-determinant Dikin-distance coefficient is at least

\[
             \sqrt{b\left\lceil{s\over R-1}\right\rceil}
             \quad\hbox{in front of }\log(1/\epsilon).    \tag{26}
\]

Hence column packing cannot improve the standard-barrier bounded-Dikin
movement coefficient below grouped Schur. Its possible QIPM benefit is confined to
per-step resources such as factor count or matrix-access structure; the
balanced and \(3:2\) conclusions quantify that tradeoff only within the
stated proxy models. Equation (26) is not a quantum query lower bound.

There is one precise setting in which the multiplication is valid. The
[work--movement composition theorem](2026-09-04-psd-packing-work-iteration-composition.md)
shows that the same aggregate dual rank \(Q\) satisfies
\(b(s-1)\leq\sum_ip_iq_i\) and controls the Dikin distance to the
corresponding support objective. Any bounded-Dikin model that explicitly
charges \(J_\omega=\sum_i r_i^\omega\) fresh work per round therefore has
a genuine total-work lower bound equal to the \(\theta=1/2\) case of
(9j), times the accuracy logarithm. Divisible \(3:2\) packing matches it
asymptotically. But a standard QIPM sparse-oracle model does not force this
fresh charge: fixed instance data and normalized KKT directions can be
preprocessed and reused. Thus the conditional theorem does not license
multiplying a one-shot quantum linear-solver lower bound by the movement
count.

The lift/factorization framework is due to Gouveia, Parrilo, and Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://doi.org/10.1287/moor.1120.0575).  Fixed-order PSD
products are studied by Fawzi and Parrilo in
[*Exponential lower bounds on fixed-size psd rank and semidefinite
extension complexity*](https://arxiv.org/abs/1311.2571).  The Schur
complement, product PSD barrier, and convex balancing argument used here
are elementary.  Targeted searches around PSD lifts of products of balls,
block sharing, and restricted barrier parameters did not locate the
cross-source full-slack packing.  The exact Pareto
parameterization, the \(3:2\) short-step-weighted aspect ratio, and the
Lorentz comparison appear not to be stated in the screened open
literature, but novelty remains subject to specialist review.
The two-parameter lower envelope (9j), its exact equality aspect ratio,
and asymptotic attainment by cross-source packing also appear absent from
the screened sources. They are elementary consequences of the new
mixed-curvature and boundary-nullity combination, not a claimed lower
bound for arbitrary barriers or quantum query algorithms.

## 6. Independent hostile audit

The auditor independently rederived the finite ledger (4)--(7), the
dimension identity and lower bound (8)--(9), the continuous proxy optimum
(12), the exact counterexample (14), the Schur ledgers, and the ambient
comparison (24).  A follow-up audit independently verified the pointwise
mixed-curvature inequality (9b), the closed integer envelope (9d) for all
parities of \(R\), the use of \(\lfloor\nu\rfloor\), and the continuous
relaxation (9f).  It also identified the necessary private-nullity
qualification now stated before (9g).

The first audit caught two substantive issues in the first draft.
First, the uncapped Lorentz benchmark had used the grouped-paraboloid
dimension \(s+2\), whereas the direct ball lift is \(Q_{s+1}\); equations
(16a), (21), and (22) now use the correct branch.  Second, the first draft
overstated the \(\omega>2+\theta\) case of (15): the cap is inactive, but
lower-size constraints need not force \(p=c=1\).  The revised statement
makes no universal aspect-ratio claim in that regime.  No correction to
the exact Pareto ledger or the \(3:2\) theorem was needed.

A further audit checked the integration of the sequential contact-range
frontier in (9e0), (9e), and (25)--(26). The same selected simultaneous
contact supplies both the sourcewise nullity lower bound and the pointwise
capacity vector used by \({\cal C}_R\); monotonicity in the integer budget
therefore justifies the two coupled conditions in (9e). The continuous
relaxation correctly imposes
\(p\leq b(s-1)/(b\lceil s/(R-1)\rceil)\) when the sourcewise constraint
is active. Equation (26) uses the exposed aggregate dual rank only when
the row factors are genuine affine-slice certificates and is correctly
stated as a path-distance coefficient, not a query lower bound. No
correction was required.

The latest audit checked the stronger two-parameter family (9h)--(9l).
After \(p_i=xr_i\) and \(c_i=(1-x)r_i\), the exact shape factor
\(x(1-x)^{1/(1+\theta)}\) has its unique maximum at
\(x=(1+\theta)/(2+\theta)\). Hölder then gives
\[
 n\leq K_\theta R^{(2+\theta-\omega)/(1+\theta)}
       J_\omega^{1/(1+\theta)}z^{\theta/(1+\theta)},
\]
and raising to \(1+\theta\), with \(z\leq\nu\), gives precisely the
constant and powers in (9j). The range
\(0\leq\omega\leq2+\theta\) is exactly what makes the residual power of
\(r_i/R\) nonnegative. The limiting \(\theta=0\) case reduces directly to
\(p_ic_i\leq R^{2-\omega}r_i^\omega/4\).

At \(\theta=1/2,\omega=0\), this independently reproduces the
Cauchy--Schwarz derivation from
\(n\leq L\bar c(R-\bar c)\) and \(\nu\geq L\bar c\).
The unique nullity is \(\bar c=2R/5\), and the reciprocal constant is
\[
 {5^{5/2}\over2\,3^{3/2}}
   ={25\over6}\sqrt{5\over3}.
\]
Full-order divisible column packing realizes the equality shape
\(p:c=3:2\), and replacing \(b(s-1)\) by its used capacity \(bs\) gives
the exact factor \((s/(s-1))^{3/2}\). For cone coordinates,
the cap gives \(M\geq(1+1/R)J_2/2\), with equality for the full-order
packed blocks. The triangular factor therefore cancels in the comparison,
so coordinate-work optimality needs only \(s\to\infty\), even at fixed
\(R\). A
dynamic-programming check of the integer envelope covered
\(2\leq R\leq30\) and \(1\leq L\leq14\).

For blockwise Schur groups, the audit verified that minimizing
\((g+1)(g+2)/(2g^{3/2})\) over positive integer widths has the unique
solution \(g=4\), with coefficient \(15/8\). Balancing heterogeneous
widths introduces only linear chords between adjacent integer costs;
dividing each chord by \(\bar g^{3/2}\) has no interior minimum. Hence the
uniform width-four construction is globally optimal when \(4\mid s\) and
the cap permits it. Finally, the audit confirmed that
(9h)--(9l), (12)--(15), and (24a)--(24d) are formulation/work proxies.
Only the separately cited movement theorem supports (26). The terminology
above was tightened from “iteration coefficient” to “bounded-Dikin
movement coefficient.”

The free-coordinate extension (4), (7b) also passed audit. The identity
\(d_{c_1+c_2}=d_{c_1}+d_{c_2}+c_1c_2\) makes complete column splitting
the unique \(V\)-minimizer for fixed \(p\), giving \(V=bs+H_p\).
Monotonicity of \((bs+H)H^\theta\) then selects the minimum attainable
\(H_p\), with exactly the stated ceiling-plateau ties.
