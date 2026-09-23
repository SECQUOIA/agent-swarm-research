# PSD column packing shares full product-ball slack rows

Status: Proved; literature-screened; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the stated global-selection and barrier scopes

## Result

Let

\[
                 C=(B_2^s)^b,\qquad s\geq3,\quad b\geq2,
 \qquad M=(S^{s-1})^b,\qquad n=b(s-1).                    \tag{1}
\]

Its polar extreme slack rows are

\[
                         S_a(x,z)=1-x_a^Tz,
              \qquad a\in[b],\quad x\in M,\quad z\in S^{s-1}. \tag{2}
\]

Suppose they have globally labelled \(C^1\) real-PSD factors

\[
 S_a(x,z)=\sum_{i=1}^L
       \operatorname{tr}\bigl(X_i(x)Y_i^a(z)\bigr),
 \qquad X_i(x),Y_i^a(z)\in\mathbb S_+^{r_i},\quad
 2\leq r_i\leq R.                                         \tag{3}
\]

Then the full product contact, not any one row separately, gives the strict
capacity law

\[
 \boxed{\displaystyle
   \sum_{i=1}^L\left\lfloor{r_i^2\over4}\right\rfloor
      \geq b(s-1)+1.}                                      \tag{4}
\]

If the primal factors in (3) are selected boundary points in the closure
of one strictly feasible affine lift slice, its restricted standard product
log-determinant barrier also obeys

\[
\boxed{\displaystyle
      \nu_{\rm std,slice}
       \geq
       b\left\lceil{s-1\over R-1}\right\rceil
       +{\bf1}_{(R-1)\mid(s-1)}.}                          \tag{5}
\]

The first term is a pointwise no-sharing law for *nullity directions*:
at every simultaneous product extreme,

\[
             \boxed{\displaystyle
             \sum_i\operatorname{nullity}X_i(x)\geq b.}    \tag{5a}
\]

Retaining the rank of each source metric strengthens this pointwise law to

\[
 \sum_i\operatorname{nullity}X_i(x)
       \geq b\left\lceil{s-1\over R-1}\right\rceil.         \tag{5b}
\]

Unlike the Lorentz case, PSD factors can genuinely share different polar
extreme rows.  For any integers \(p,c\geq1\) with \(p+c\leq R\), there is
a polynomial full-slack lift in which one order-\((p+c)\) PSD block packs
up to \(c\) coordinate groups, possibly from \(c\) different source balls,
and carries up to \(pc\) mixed-curvature dimensions.  Put

\[
 H=b\left\lceil{s\over p}\right\rceil,\qquad
 L_{\rm pack}=\left\lceil{H\over c}\right\rceil.            \tag{6}
\]

The construction uses \(L_{\rm pack}\) PSD factors, has total boundary
nullity \(H\), and its restricted standard log-determinant has exact
parameter

\[
                         \boxed{\nu_{\rm pack}=H.}          \tag{7}
\]

Choosing \(p=\lfloor R/2\rfloor\), \(c=R-p\) makes

\[
 L_{\rm pack}=O\!\left({bs\over R^2}+{b\over R}+1\right),
 \qquad
 \nu_{\rm pack}=O\!\left({bs\over R}+b\right).              \tag{8}
\]

In the ceiling-free regime \(R=O(s)\) and \(R^2=O(bs)\), this
asymptotically matches all three capacity-ledger scales: factor count
\(bs/R^2\), ambient normal parameter \(bs/R\), and cone-coordinate
dimension \(bs\).  The additive terms in (8) are necessary when the cap
exceeds one of the problem dimensions.  Thus higher-rank PSD blocks
invalidate Lorentz-style factor disjointness, but their sharing is
quantitatively limited by the single support-space capacity \(p(r-p)\).

A particularly transparent specialization takes \(p=s\) and \(c=b\).
Whenever \(R\geq s+b\), the entire product of \(b\) balls has a
**one-factor** \(\mathbb S_+^{s+b}\) lift with a polynomial full-slack
factorization.  Its standard barrier has ambient parameter \(s+b\) but
exact restricted parameter \(b\).  In view of (5a), this is optimal among
all restricted standard product log-determinants in the stated globally
selected class.  Thus the failure of factorwise no-sharing is not marginal:
one PSD support can serve every polar extreme row at once, while spending
one private nullity direction per row.  More generally, packing every group
into one block gives the
one-factor order

\[
             r_{\rm one}^{\rm pack}
                =\min_{1\leq p\leq s}
                   \left\{p+b\left\lceil{s\over p}\right\rceil\right\}.
                                                                    \tag{8a}
\]

There is a stronger intrinsic statement for the transparent \(p=s,c=b\)
slice.  Its optimal parameter is exactly \(b\) even among arbitrary coupled,
non-logarithmically-homogeneous self-concordant barriers.  The completion
fiber over a projected point \(W\in(B_2^s)^b\) is bounded, so exact partial
minimization would turn any \(\vartheta\)-barrier on the lift into a
\(\vartheta\)-barrier on the product body.  A projected \(b\)-cube forces
\(\vartheta\geq b\), and the restricted barrier above attains equality.
This argument works without \(b\leq s\); see the
[arbitrary-coupled one-block theorem](2026-09-04-one-block-psd-packing-coupled-barrier.md).

The lower bound (4) forces any one-factor globally selected lift to have
\(\lfloor r^2/4\rfloor\geq b(s-1)+1\).  Thus (8a) provides a concrete
upper frontier to compare with the capacity lower bound, rather than merely
aggregating \(b\) direct LMIs block-diagonally.

Across all capped lifts, the standard restricted-barrier optimum is exact:

\[
\boxed{\displaystyle
 \nu_{\rm std,slice}^{\min}
   =b\left\lceil{s\over R-1}\right\rceil.}                \tag{8b}
\]

The strengthened lower bound retains the full rank of every source metric
in the private-quotient argument; see
[Private curvature closes every nondivisible PSD product-ball
cap](2026-09-04-psd-product-ball-private-curvature-frontier.md).
The upper bound uses \(p=R-1,c=1\).  Nondivisible residues are exact by
the private-curvature theorem.  In a divisible residue
\(s-1=q(R-1)\) with \(q\geq2\), compact saturated-label closures,
top-eigenline spectral projectors, and a relative-top-class contradiction
force the same grouped-Schur value; see
[The divisible gap closes beyond the one-channel
case](2026-09-04-psd-product-ball-divisible-topclass.md).  The final
\(q=1\), \(s=R\geq3\) residue is closed by
[sequential range compression](2026-09-04-q1-sequential-range-compression-closure.md):
fix one source contact at a time, quotient every PSD block by all earlier
dual contact ranges, and reapply the one-ball order-\(s\) obstruction.
Each source adds at least two new range dimensions, so one simultaneous
contact has total nullity at least \(2b\).  All three results passed
independent hostile audits.
In particular, the exact large-cap answer is

\[
                     \nu_{\rm std,slice}^{\min}=b
                     \qquad(R\geq s+1).                    \tag{8c}
\]

The arbitrary-coupled statement above concerns the fixed order-\((s+b)\)
one-block slice.  Equation (8b), by contrast, is the complete optimum for
the restricted standard product log-determinant over every capped
globally bi-\(C^1\) PSD lift in the stated class.

## 1. One support differential must serve every slack row

At a simultaneous diagonal contact, set

\[
 Y_i^\Sigma(x)=\sum_{a=1}^bY_i^a(x_a),\qquad
 p_i=\operatorname{rank}X_i(x),\qquad
 q_i=\operatorname{rank}Y_i^\Sigma(x).                    \tag{9}
\]

Every term in every zero slack row is nonnegative.  Hence
\[
 X_i(x)Y_i^a(x_a)=0\quad\text{for all }a,
 \qquad X_i(x)Y_i^\Sigma(x)=0,
\]
and therefore

\[
                              p_i+q_i\leq r_i.              \tag{10}
\]

Differentiate the \(b\) slack rows simultaneously.  On
\[
 T_xM=\bigoplus_aT_{x_a}S^{s-1},
\]
the direct sum of their mixed forms is the nondegenerate pairing

\[
 G_x(u,v)=\sum_{a=1}^b\langle u_a,v_a\rangle.              \tag{11}
\]

The contribution of factor \(i\) is

\[
 H_i(u,v)=
 -\operatorname{tr}\!\left(
 dX_i(x)u\,
 \sum_a dY_i^a(x_a)v_a\right).                            \tag{12}
\]

In bases adapted to
\(\operatorname{Ran}X_i\perp\operatorname{Ran}Y_i^\Sigma\),
only the off-diagonal \(p_i\times q_i\) derivative block contributes.
Consequently

\[
 \operatorname{rank}H_i\leq p_iq_i
 \leq\left\lfloor{r_i^2\over4}\right\rfloor.               \tag{13}
\]

Taking ranks in (11)--(12) first gives

\[
                         n\leq\sum_i
                         \left\lfloor{r_i^2\over4}\right\rfloor. \tag{14}
\]

The same calculation explains why counting a separate \(p_iq_i^a\) for
every row would be wrong.  All rows use the same pointwise support-rotation
block in
\(\operatorname{Hom}(\operatorname{Ran}X_i,\ker X_i)\), whose dimension is
\(p_i(r_i-p_i)\).  If the rank is locally constant, this is precisely the
differential of the Grassmannian range map.  Rank constancy is not needed
for the pointwise bound (13); it will follow from saturation before the
global map in Section 2 is used.  PSD sharing exists, but this common target
prevents multiplying one block's capacity by \(b\).

There is nevertheless an exact no-sharing law at the level of kernel
directions.  Put

\[
 U_{ia}=\operatorname{Ran}Y_i^a(x_a)\subseteq
 E_i:=\ker X_i(x),\qquad
 U_{i,-a}=\sum_{d\neq a}U_{id},                            \tag{14a}
\]

and define the private dimension

\[
 d_{ia}=\dim\left(U_{ia}/(U_{ia}\cap U_{i,-a})\right).     \tag{14b}
\]

The cylindrical zero identity
\[
                         X_i(x)Y_i^d(x_d)=0
\]
holds while every block \(x_a\), \(a\neq d\), varies freely.
Differentiating shows that the off-diagonal support derivative in block
\(a\) annihilates \(U_{id}\).  Therefore the block-\(a\) curvature channel
factors through the private quotient in (14b), and

\[
                 \operatorname{rank}H_i^a\leq p_i d_{ia}. \tag{14c}
\]

For fixed \(i\), choose a complement
\(P_{ia}\subseteq U_{ia}\) of \(U_{ia}\cap U_{i,-a}\).
The subspaces \(P_{ia}\) are jointly independent: if
\(\sum_av_a=0\), then
\(v_a\in U_{ia}\cap U_{i,-a}\), hence \(v_a=0\).
Consequently

\[
                         \sum_a d_{ia}\leq\dim E_i.         \tag{14d}
\]

For every source row \(a\), its sphere metric is nondegenerate, so (14c)
forces \(d_{ia}>0\) for at least one factor \(i\).  Summing (14d) over
factors proves (5a).  A whole PSD factor can share rows by splitting its
kernel; a single kernel direction cannot be productive for two rows.

## 2. Equality is excluded by full-slack injectivity

Assume equality in (14).  Rank saturation gives fixed balanced ranks
\[
 p_i+q_i=r_i,\qquad
 p_iq_i=\left\lfloor r_i^2/4\right\rfloor                  \tag{15}
\]
for every positive-capacity factor at every point.  These ranks are
globally constant.  For odd \(r_i\), a change would have to interchange
the two balanced values; at a transition one rank would drop while its
complementary rank increased, contradicting lower semicontinuity of both
matrix ranks and \(p_i+q_i=r_i\).  Connectedness then fixes the choice.
Constant-rank PSD families have \(C^1\) range maps, so define

\[
 \Pi:M\longrightarrow
       \prod_{i:q_i>0}\operatorname{Gr}_{p_i}(\mathbb R^{r_i}),
 \qquad
 \Pi(x)=(\operatorname{Ran}X_i(x))_i.                     \tag{16}
\]

If \(d\Pi(x)u=0\), every off-diagonal block in (12) vanishes.
Equation (11) then forces \(u=0\).  Source and target dimensions are both
\(n\), so \(\Pi\) is a local diffeomorphism.

The full family of rows makes \(\Pi\) injective.  If
\(\Pi(x')=\Pi(x)\), then every \(Y_i^a(x_a)\) has range in
\(\ker X_i(x)=\ker X_i(x')\).  Equation (3) gives

\[
                        1-(x_a')^Tx_a=0
                        \qquad\text{for every }a,           \tag{17}
\]

so \(x'=x\).  Compactness and connectedness would therefore make (16) a
diffeomorphism.

This is impossible.  The source \(M\) is simply connected because
\(s-1\geq2\).  Every nontrivial real Grassmannian in (16) has nontrivial
fundamental group: \(\operatorname{Gr}_1(\mathbb R^2)\cong S^1\), and the
higher cases have the standard \(\mathbb Z_2\) obstruction.  The target
product is not simply connected.  Thus equality in (14) cannot occur, and
integrality proves (4).

This argument differs from Lorentz analytic no-sharing.  It permits one PSD
support Grassmannian to receive tangent directions from many source balls;
it only rules out exact total saturation.

## 3. Restricted barrier lower bound

At a selected primal boundary tuple put

\[
                         c_i=\operatorname{nullity}X_i(x).
                                                                    \tag{18}
\]

The boundary-nullity lemma for the standard product log-determinant gives

\[
                         \nu_{\rm std,slice}\geq\sum_i c_i. \tag{19}
\]

For every source \(a\), (14c) and the rank-\((s-1)\) source metric give

\[
 s-1\leq\sum_i p_i d_{ia}
      \leq(R-1)\sum_i d_{ia}.
\]

Summing over sources and applying (14d) proves (5b), and (19) gives the
first term of (5).  If \((R-1)\nmid(s-1)\), this is already the displayed
bound.  In the divisible case, equations (10)--(13) also give

\[
 n\leq\sum_i p_iq_i
   \leq\sum_i p_ic_i
   \leq(R-1)\sum_i c_i.                                   \tag{20}
\]

Write \(s-1=q(R-1)\), so \(n=h(R-1)\) with \(h=bq\).  Suppose
\(\nu_{\rm std,slice}<h+1\).  Applying (5b), (19), and (20) at every
contact fixes the total nullity at \(h\).  Equality forces exactly \(h\) active
order-\(R\) factors with

\[
                         (p_i,q_i,c_i)=(R-1,1,1).           \tag{21}
\]

Their active set is locally, hence globally, constant: nonzero
\(Y_i^\Sigma\) persists locally and keeps \(X_i\) singular, while the fixed
total nullity \(h\) forbids both new singular blocks and further rank drops.
The joint range map is now an injective local diffeomorphism

\[
                  M\longrightarrow(\mathbb {RP}^{R-1})^h, \tag{22}
\]

by exactly the argument in Section 2.  This again contradicts fundamental
groups.  Here every inactive \(X_i\) is positive definite at every contact,
so complementarity forces every corresponding \(Y_i^a\) to vanish; inactive
factors cannot spoil the cross-contact injectivity.  Therefore
\(\nu_{\rm std,slice}\geq h+1\), proving (5).

As a resource ledger, (4) also implies
\[
\begin{aligned}
 L&\geq K_R(n+1),\\
 \sum_i{r_i(r_i+1)\over2}&\geq F_R(n+1),\\
 \nu_{\rm ambient}=\sum_i r_i&\geq V_R(n+1),               \tag{23}
\end{aligned}
\]
where \(K_R,F_R,V_R\) are the exact capacity knapsacks in the
[PSD order-cap ledger](2026-09-04-psd-order-cap-qipm-ledger.md).
These are capacity-only minima; attainment is a separate construction
question.

## 4. A single PSD factor can share many source rows

Fix \(p,c\geq1\), \(p+c\leq R\).  Partition the \(s\) coordinates of every
source ball into \(h=\lceil s/p\rceil\) nonempty groups of size at most
\(p\).  Call the resulting \(H=bh\) groups columns, and pack up to \(c\)
columns into each block \(\ell\).  Let \(c_\ell\leq c\) be its column count.

Pad every group vector to \(x_\gamma\in\mathbb R^p\), place these columns in
\(W_\ell\in\mathbb R^{p\times c_\ell}\), introduce a free symmetric
\(S_\ell\in\mathbb S^{c_\ell}\), and impose

\[
 Z_\ell=
 \begin{pmatrix}
  S_\ell&W_\ell^T\\
  W_\ell&I_p
 \end{pmatrix}\succeq0.                                   \tag{24}
\]

For each source ball \(a\), impose the one affine equation

\[
 \sum_{\gamma:\,a(\gamma)=a}
       (S_{\ell(\gamma)})_{\gamma\gamma}=1.                \tag{25}
\]

Schur complementation says

\[
 Z_\ell\succeq0
 \quad\Longleftrightarrow\quad
 D_\ell:=S_\ell-W_\ell^TW_\ell\succeq0.                    \tag{26}
\]

The diagonal of (26), summed in (25), gives
\(\|x_a\|^2\leq1\).  Conversely, for any point of \(C\), distribute
\(1-\|x_a\|^2\) nonnegatively among its groups and set
\[
 S_\ell=W_\ell^TW_\ell+\operatorname{Diag}(\delta_\gamma).
\]
This proves exact projection; positive distributions give strict
feasibility over the interior.

At a product extreme, every diagonal residual is zero.  A PSD matrix with
zero diagonal is zero, so

\[
                         D_\ell=0,\qquad
                         S_\ell=W_\ell^TW_\ell.             \tag{27}
\]

Thus the boundary fiber is unique and polynomial.  It has
\(\operatorname{rank}Z_\ell=p\) and nullity \(c_\ell\).

The full slack factors are explicit.  For column \(\gamma\) and a polar
point \(z\), let \(\tilde z_\gamma\in\mathbb R^p\) be the padded coordinate
group and put

\[
 v_{\ell,\gamma}(z)=
 \begin{pmatrix}e_\gamma\\-\tilde z_\gamma\end{pmatrix},
 \qquad
 Y_\ell^a(z)={1\over2}
 \sum_{\substack{\gamma\text{ in }\ell\\a(\gamma)=a}}
 v_{\ell,\gamma}(z)v_{\ell,\gamma}(z)^T.                  \tag{28}
\]

With \(X_\ell(x)=Z_\ell\) from (27),
\[
\begin{aligned}
 \operatorname{tr}\!\left(
 X_\ell(x)v_{\ell,\gamma}(z)v_{\ell,\gamma}(z)^T\right)
 &=\|\tilde x_\gamma-\tilde z_\gamma\|^2,\\
 \sum_\ell\operatorname{tr}(X_\ell(x)Y_\ell^a(z))
 &={1\over2}\|x_a-z\|^2
 =1-x_a^Tz.                                                \tag{29}
\end{aligned}
\]

All maps are polynomial.  If one block contains columns assigned to
different source balls, the same PSD factor is productive for all their
polar rows.  This is an explicit counterexample to factorwise no-sharing.

## 5. Exact restricted barrier and resource tradeoff

Fixing the public identity block in (24) gives

\[
 -\log\det Z_\ell=-\log\det D_\ell.                         \tag{30}
\]

This restricted block barrier has exact parameter \(c_\ell\).  One quick
verification uses affine symmetries to move any point to
\((D_\ell,W_\ell)=(I,0)\).  Along a direction \((A,U)\),

\[
 D_\ell(t)=I+tA-t^2U^TU,
\]
so
\[
 F'(0)=-\operatorname{tr}A,\qquad
 F''(0)=\operatorname{tr}(A^2)+2\|U\|_F^2.                \tag{31}
\]

The squared local dual norm of the gradient is therefore \(c_\ell\).
Self-concordance follows by affine restriction of the standard PSD barrier,
and the symmetries make the calculation point-independent.  Products and
the equations (25) give an upper parameter \(\sum_\ell c_\ell=H\).
At a product extreme, (27) and the nullity lemma give the reverse bound.
This proves (7).

The exact construction ledgers are

\[
\begin{aligned}
 L_{\rm pack}&=\left\lceil{H\over c}\right\rceil,\\
 \nu_{\rm std,slice}&=H,\\
 \nu_{\rm ambient}
   &=pL_{\rm pack}+H,\\
 M_{\rm cone}
   &=\sum_{\ell=1}^{L_{\rm pack}}
       {(p+c_\ell)(p+c_\ell+1)\over2}.                     \tag{32}
\end{aligned}
\]

With \(p=\lfloor R/2\rfloor\) and \(c=R-p\), full blocks use the maximum
PSD curvature capacity \(pc=\lfloor R^2/4\rfloor\).  Away from ceilings,

\[
 L_{\rm pack}\sim {bs\over pc},\qquad
 \nu_{\rm ambient}\sim {bs(p+c)\over pc},\qquad
 M_{\rm cone}\sim {R^2\over2pc}\,bs.                       \tag{33}
\]

For balanced \(p,c\), these are respectively
\(\sim4bs/R^2\), \(\sim4bs/R\), and \(\sim2bs\), matching the lower-ledger
scales in (23).  In contrast, taking \(p=R-1,c=1\) minimizes the displayed
restricted parameter to

\[
                   b\left\lceil{s\over R-1}\right\rceil,   \tag{34}
\]

but gives no factor-count sharing.  Equations (32)--(34) expose a genuine
factor-count versus restricted-barrier tradeoff.

The naive lifted Hessian can be dense, but exact auxiliary centering and
Schur elimination are analyzed separately in
[the PSD packing Newton-forest note](2026-09-04-psd-column-packing-newton-forest.md).
For this construction, the marginal barrier is independent of the packing,
and its rank-expanded reduced KKT graph is a forest.  This does not make
dense lifted-coordinate materialization free: Gram matrices, precision,
access, and output must still be charged separately.  Equations (4)--(8)
are formulation and barrier ledgers, not iteration lower bounds or
end-to-end quantum speedups.

## 6. Why bare embedding codimension cannot give \(bs\)

It is natural to ask whether the strict capacity bound (4) can be sharpened
from \(b(s-1)+1\) to \(bs\), matching the balanced column-packing scale.
Support-map injectivity by itself cannot prove such a statement.

Indeed, put \(p=s-1\) and fix \(0<\varepsilon<1\).  Write the second copy
of \(S^p\) as
\[
                         (t,y)\in S^p\subset\mathbb R\times\mathbb R^p.
\]
The map
\[
 \Psi:S^p\times S^p\longrightarrow\mathbb R^{2p+1},\qquad
 \Psi(x,(t,y))=((1+\varepsilon t)x,\varepsilon y)          \tag{35}
\]
is a smooth codimension-one embedding.  Its first component has positive
norm \(1+\varepsilon t\), which recovers \(t\) and \(x\), while the second
recovers \(y\); the differential is injective by the same decomposition.
Geometrically, (35) is the boundary of a small tubular neighborhood of the
standard \(S^p\subset\mathbb R^{2p+1}\).

Composing (35) with an affine chart gives a codimension-one embedding
\[
       S^p\times S^p\hookrightarrow
       \mathbb {RP}^{2p+1}
       =\operatorname{Gr}_1(\mathbb R^{2p+2}).              \tag{36}
\]
The image lies in a contractible chart, so pullbacks of all positive-degree
characteristic classes of the target vanish.  Thus orientability,
Stiefel--Whitney classes, stable tangent data, and generic
support-map-embedding codimension cannot universally exclude \(q=1\).

Equation (36) is not a slack factorization and does not refute the possible
stronger bound \(bs\).  In particular its Grassmannian is unbalanced, while
equality in the maximum-capacity ledger forces balanced support ranks.  It
does show that any \(bs\) theorem must use more than injective immersion:
the cylindrical identities and the arrangement of the row-specific dual
subspaces \(U_{ia}\) are essential.  The private-direction theorem (5a) is
the present rigorous gain from that extra structure.  Whether it also
forces
\[
            \sum_i\left\lfloor r_i^2/4\right\rfloor\geq bs \tag{37}
\]
remains open.

## 7. Literature and novelty boundary

The PSD lift/factorization framework is standard; see Gouveia, Parrilo, and
Thomas, *Mathematics of Operations Research* 38 (2013), DOI
[10.1287/moor.1120.0575](https://doi.org/10.1287/moor.1120.0575).
Fawzi and Parrilo study extension complexity over products of fixed-order
PSD cones in
[*Exponential lower bounds on fixed-size psd rank and semidefinite extension
complexity*](https://arxiv.org/abs/1311.2571).  The shared-principal-block
matrix in (24) is a standard Schur-complement/PSD-completion device; the
foundational completion theorem is due to Grone, Johnson, Sá, and
Wolkowicz, *Linear Algebra and its Applications* 58 (1984), DOI
[10.1016/0024-3795(84)90207-6](https://doi.org/10.1016/0024-3795(84)90207-6).
No novelty is claimed for that matrix-completion device by itself.

A targeted search did not locate the simultaneous full-product curvature
bound (4), the strict injective-Grassmannian argument, the private-nullity
law (5a), or their combination with the exact full-slack and barrier
tradeoff (28)--(34).  Novelty is plausible pending specialist review.

The theorem is deliberately conditional on globally labelled \(C^1\)
full-contact factors.  It does not apply to arbitrary nonsmooth lift
selections.  The barrier statement additionally needs the selected primal
tuple to lie in the closure of the same strictly feasible affine slice.
Neither lower bound is an actual iteration lower bound.

## 8. Independent hostile audit

The auditor rederived the simultaneous mixed-curvature channel using
\(Y_i^\Sigma\), including the possible residual subspace between the primal
and dual ranges.  It verified the rank bound (13), the balanced-rank
constancy argument, full-slack injectivity, and the strict \(+1\) covering
obstruction.  The residue case behind (5) was checked separately, including
local constancy of the active set and disappearance of inactive dual
factors.

The private-nullity proof (14a)--(14d) also passed independently:
cylindrical complementarity makes every other source derivative annihilate
a row's dual range, the private complements are jointly independent, and
each nondegenerate row needs at least one private direction.  Thus (5a) is
not inferred merely from normal-cone dimension.

On the construction side, the audit expanded the Schur complement, checked
strict feasibility and the unique polynomial boundary fiber, and verified
the trace identity (29).  It also computed the local gradient norm of
\(-\log\det(S-W^TW)\) after the affine normalization to \((I,0)\), confirming
the exact block parameter \(c_\ell\) and total parameter \(H\).  The first
draft omitted unavoidable ceiling terms from (8); the displayed bounds now
include them, and the asymptotic scale match is limited to the stated
regime.  The PSD-completion construction is correctly identified as
standard machinery rather than claimed standalone novelty.

Finally, a separate follow-up audit verified the codimension-one embedding
(35)--(36), its differential, its affine-chart characteristic-class
consequence, and the important qualification that it does not settle the
balanced-capacity conjecture (37).  No further mathematical correction was
required.

The arbitrary-coupled one-block strengthening was audited independently.
That audit checked every hypothesis of exact partial minimization on the
relative-open completion slice, boundedness of the fixed-\(W\) fibers for
all \(b,s\), the projected \(b\)-cube when \(b>s\), and the exact
parameter-\(b\) normalization of the restricted log-determinant.  It passed
after correcting only wording that had treated a big-\(O\) short-step
guarantee as a lower bound.
