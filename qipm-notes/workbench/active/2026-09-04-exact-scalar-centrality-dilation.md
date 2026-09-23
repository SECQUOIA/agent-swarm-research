# Exact scalar centrality dilation for the spectral interval

Status: Main theorem independently hostile-audited; rational enclosure
proved and mechanically checked at research closure
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High for the exact variational constant and the rational
bounds; uniqueness of its maximizer remains open; targeted literature
screen complete

## Result

Put
\[
 b(x)=-\log(1-x^2),\qquad
 \rho(x)=\int_0^x {\sqrt{2(1+t^2)}\over1-t^2}\,dt,
 \qquad p(y)=b'(\rho^{-1}(y)).                                  \tag{1}
\]
The exact uniform scalar dilation needed to compare an optimal
accuracy-sublevel endpoint with the corresponding central endpoint is
\[
 \boxed{
 c_\star=\max_{y>0}{p^{-1}(yp'(y))\over y}.}                    \tag{2}
\]
Here \(p^{-1}\) is the functional inverse.  This maximum exists and obeys
the fully analytic enclosure
\[
       \boxed{{68743\over50000}=1.37486<c_\star
                    <{69\over50}=1.38
                    <\kappa_0=1.391010896\ldots,}               \tag{3}
\]
where \(\kappa_0\) is the earlier certified root of
\(\log[\kappa_0(\kappa_0-1)]+2-\kappa_0=0\).
The last strict comparison is also elementary.  The root function has
derivative \(1/a+1/(a-1)-1>0\) on \((1,2)\), while at \(a=69/50\)
\[
 \log[a(a-1)]+2-a
 =-\log{2500\over1311}+{31\over50}<0,
\]
because, with \(z=1189/3811\),
\(\log(2500/1311)=\log((1+z)/(1-z))>2z>31/50\).

Consequently, the sharp scalar constant, rather than the sufficient
constant \(\kappa_0\), gives
\[
 \boxed{
 L_{\rm CP}(\epsilon)
       \le c_\star\Gamma_rL_{\rm opt}(\epsilon)
       <{69\over50}\Gamma_rL_{\rm opt}(\epsilon).}             \tag{4}
\]
The first inequality is exact for the coordinatewise comparison argument:
no smaller uniform coordinate dilation can replace \(c_\star\).  This does
not assert that \(c_\star\Gamma_r\) is the optimal global arclength ratio;
the worst scalar dilation and worst prefix-norm distortion need not occur
in the same instance.

High-precision evaluation of the elementary formula below locates a
maximizer at
\[
 x\approx0.9012017365,\qquad y\approx2.4538667417,
 \qquad c_\star\approx1.37486420044.                            \tag{5}
\]
These decimals are numerical guidance only.  The proof below does not use
them, and it does not prove that this stationary point is unique.

## 1. Elementary one-variable representation

Set
\[
                  v={\sqrt2x\over\sqrt{1+x^2}}\in(0,1).
\]
The substitution \(x=\tan\theta\), followed by
\(u=\sin\theta\), evaluates the apparently non-elementary integral in
(1):
\[
 \begin{aligned}
 Y(v):=\rho(x)
   &=2\operatorname{artanh}v
       -\sqrt2\operatorname{artanh}{v\over\sqrt2},\\
 P(v):=p(Y(v))
   &={v\sqrt{2-v^2}\over1-v^2},\\
 A(v):=p'(Y(v))
   &={\sqrt{2-v^2}\over1-v^2},\\
 Y'(v)&={2\over(1-v^2)(2-v^2)}.                                \tag{6}
 \end{aligned}
\]
The inverse of \(P\) is
\[
                  P^{-1}(q)=\sqrt{1-{1\over\sqrt{1+q^2}}}.
\]
Thus, with
\[
 W(v)=\sqrt{1-{1\over\sqrt{1+Y(v)^2A(v)^2}}},
\]
equation (2) becomes the completely elementary compactified maximum
\[
                       c_\star=\max_{0<v<1}C(v),\qquad
 C(v)={Y(W(v))\over Y(v)}.                                     \tag{7}
\]

The Taylor expansion at zero gives \(Y(v)=v+v^3/2+O(v^5)\), hence
\(C(v)\to1\) as \(v\downarrow0\).  As \(v\uparrow1\),
\(Y(v)=\log(1/(1-v))+O(1)\), while
\(1-W(v)=\Theta((1-v)/Y(v))\).  Therefore
\[
              Y(W(v))=Y(v)+\log Y(v)+O(1),
              \qquad C(v)\longrightarrow1.                    \tag{8}
\]
Since \(p\) is strictly convex and \(p(0)=0\),
\(yp'(y)>p(y)\) for \(y>0\), so \(C(v)>1\).  Extending \(C\) by one at
both endpoints proves that its maximum exists and lies in the interior.

For possible future work on uniqueness, every stationary point obeys one
explicit equation.  Since
\[
 A'(v)={v(3-v^2)\over(1-v^2)^2\sqrt{2-v^2}},
\]
differentiating (7) and using \(P'(W)=A(W)Y'(W)\) gives
\[
 \boxed{
 Y(v)\bigl[Y'(v)A(v)+Y(v)A'(v)\bigr]
   =Y(W(v))Y'(v)A(W(v)).}                                      \tag{9}
\]
Numerics show one root of (9), the point in (5), but no analytic
one-root proof is claimed here.

## 2. Elasticity identity

Let \(x=\rho^{-1}(y)\) and define
\[
 E(y)={yp'(y)\over p(y)},\qquad
 K(y)={y^2(1-x^2)\over2x^2(1+x^2)}.                            \tag{10}
\]
Direct differentiation gives
\[
              {dE\over d\log y}=E-K,\qquad E\ge1.             \tag{11}
\]
Moreover,
\[
 B(x)=\sqrt2x\sqrt{1+x^2\over1-x^2},
 \qquad K=(\rho/B)^2.
\]
The elementary derivative comparison \(\rho(x)\le B(x)\), strict for
\(x>0\), gives \(K<1\).  Explicitly, with \(u=x^2\),
\[
 {B'(x)\over\rho'(x)}={1+2u-u^2\over(1+u)\sqrt{1-u}}>1,
\]
because the difference of the squared numerator and denominator is
\(u(3+3u-3u^2+u^3)>0\).  Hence, for \(t>1\) (with equality at \(t=1\)),
\[
                    E(ty)>1+t(E(y)-1).                          \tag{12}
\]
Integrating \(d\log p/d\log y=E\) from \(y\) to \(ay\) yields the general
bound
\[
 \log{p(ay)\over yp'(y)}
   >h_1(E):=\log a+(a-1)(E-1)-\log E.                           \tag{13}
\]

For the large-elasticity regime a stronger estimate is available.  By
concavity of the square root,
\[
 \rho(x)\le\sqrt2\,D(x),\qquad
 D(x)={3\over2}\operatorname{artanh}x-{x\over2}.               \tag{14}
\]
At \(x=4/5\), \(D=(3/2)\log3-2/5<2497/2000\).  The last strict inequality
follows from \(\log3<1099/1000\); the degree-six exponential Taylor sum
at \(1099/1000\) already exceeds three.  Therefore
\[
 E(4/5)\le {D(4/5)\sqrt{41}\over4}<2,                           \tag{15}
\]
where the final exact check is
\(2497^2\cdot41<64\cdot2000^2\).  Since (11) makes \(E\) increasing,
\(E(y)>2\) implies \(x>4/5\).

For \(x\ge4/5\), (14) gives
\[
 K\le G(x):={D(x)^2(1-x^2)\over x^2(1+x^2)}.                  \tag{16}
\]
The inequalities
\[
 D(x)\ge x(1+x^2/2),\qquad
 D'(x)={1+x^2/2\over1-x^2}
\]
imply
\[
 {1\over2}(\log G)'\le-{x\over1+x^2}<0.                       \tag{17}
\]
Thus \(G\) is decreasing, and exact rational arithmetic gives
\[
 G(x)\le G(4/5)
 <\left({2497\over2000}\right)^2{225\over656}
 ={56115081\over104960000}<{107\over200}.                     \tag{18}
\]
Consequently, throughout every multiplicative ray \(ty\), \(t\ge1\),
starting at a point with \(E(y)>2\), one has \(K(ty)<107/200\).  Integrating
(11) now gives, for \(t>1\) (with equality at \(t=1\)),
\[
 E(ty)>{107\over200}
      +t\left(E(y)-{107\over200}\right),                       \tag{19}
\]
and hence
\[
 \log{p(ay)\over yp'(y)}
 >h_{107/200}(E)
 :={107\over200}\log a
 +(a-1)\left(E-{107\over200}\right)-\log E.                   \tag{20}
\]

## 3. Rational certificate for \(69/50\)

Take \(a=69/50\).  If \(1\le E\le2\), then \(h_1\) is decreasing and
\[
 h_1(E)\ge h_1(2)=\log{69\over100}+{19\over50}>0.              \tag{21}
\]
Indeed,
\[
 e^{19/50}>1+{19\over50}+{(19/50)^2\over2}
 ={7261\over5000}>{100\over69}.
\]

If \(E>2\), the convex function in (20) has its minimum at
\(E=50/19\).  At that point
\[
 h_{107/200}(E)
 =\log{19\over50}+1
  +{107\over200}\left(\log{69\over50}-{19\over50}\right).    \tag{22}
\]
For \(0<z<1\), the positive series
\[
 \log{1+z\over1-z}=2\sum_{j\ge0}{z^{2j+1}\over2j+1}
\]
gives, with \(r=31/69\) and \(s=19/119\),
\[
 \begin{aligned}
 \log{19\over50}
 &>-2\left(r+{r^3\over3}+{r^5\over5(1-r^2)}\right)
   =-{9064603453\over9362506500},\\
 \log{69\over50}
 &>2\left(s+{s^3\over3}\right)
   ={1628072\over5055477}.                                    \tag{23}
 \end{aligned}
\]
Substitution in (22) leaves the exact positive margin
\[
 h_{107/200}(50/19)
 >{255839420916449\over315546241820670000}>0.                  \tag{24}
\]
Equations (13) and (20)--(24) prove
\[
                         p((69/50)y)>yp'(y),\qquad y>0.         \tag{25}
\]
Applying the increasing inverse \(p^{-1}\) proves (3).
The comparison with the earlier root is analytic as well.  If
\(g(a)=\log[a(a-1)]+2-a\), then \(g\) is strictly increasing on
\((1,2)\), and, with \(z=1189/3811\),
\[
 \log{2500\over1311}
 =2\sum_{j\geq0}{z^{2j+1}\over2j+1}
 >{2378\over3811}>{31\over50}.
\]
Thus \(g(69/50)=\log(1311/2500)+31/50<0=g(\kappa_0)\), proving
\(69/50<\kappa_0\) without using its decimal approximation.

## 4. A rational lower certificate and maximizer enclosure

The elementary function \(Y\) has the positive rational series
\[
 Y(z)=\sum_{k\geq0}{(2-2^{-k})z^{2k+1}\over2k+1}.              \tag{26}
\]
If \(S_N(z)\) is the sum through \(k=N\), then
\[
 S_N(z)<Y(z)<
 S_N(z)+{2z^{2N+3}\over(2N+3)(1-z^2)},\qquad 0<z<1.           \tag{27}
\]
Thus evaluations at rational \(z\) have exact rational enclosures.

Take
\[
 v_0={3787\over4000},\qquad
 w_0={9797031\over10^7},\qquad
 a_0={68743\over50000}.
\]
Using (27) and rational square-root enclosures, verified by squaring,
gives
\[
\begin{aligned}
 Y(w_0)-a_0Y(v_0)
  &>{2071874360571\over250000000000000000}>0,\\
 Y(v_0)A(v_0)-w_0A(w_0)
  &>{2049519399569150216498389
       \over40000000000000000000000000000}>0.                 \tag{28}
\end{aligned}
\]
One set of intermediate enclosures producing (28) is
\[
\begin{gathered}
 {2453756741730599\over10^{15}}<Y(v_0)
 <{12268783708653\over5\cdot10^{12}},\\
 {134943211257327\over4\cdot10^{13}}<Y(w_0)
 <{421697535179147\over125\cdot10^{12}},\\
 A(v_0)>{405367307458211\over4\cdot10^{13}},\qquad
 A(w_0)<{25381942601625079\over10^{15}}.
\end{gathered}
\]
For example, summing (26) through \(N=1200\) makes its tail bound
more than sufficient for both inequalities.  Since \(P(z)=zA(z)\) is
strictly increasing, the second inequality says \(w_0<W(v_0)\).
The first inequality and monotonicity of \(Y\) then give
\[
 C(v_0)={Y(W(v_0))\over Y(v_0)}>a_0.                          \tag{29}
\]
This proves the lower half of (3) without using the decimals in (5).

The same certificate localizes every maximizer.  For \(r>1\), put
\[
 q_r={r-1\over r+1}.
\]
The positive series
\[
 \log r=2\sum_{j\geq0}{q_r^{2j+1}\over2j+1}
\]
has the same tail bound as (27), with \(z=q_r\).  Exact rational
evaluation through \(j=200\) gives
\[
\begin{aligned}
 h_1(2)
  &>{2589087717927\over40000000000000000}>0,\\
 h_{107/200}(571/250)
  &>{2011885403423\over100000000000000000}>0,\\
 h_{107/200}(773/250)
  &>{8579961311243\over500000000000000000}>0,                \tag{30}
\end{aligned}
\]
where the functions \(h_k\) in (13) and (20) use \(a=a_0\).
On \(1\leq E\leq2\), \(h_1\) is decreasing, so the first line of
(30) makes (13) positive.  On \(E>2\), \(h_{107/200}\) is convex,
decreases up to \(E=1/(a_0-1)\), and increases thereafter.  The other
two lines and (20) therefore show that \(C(v)>a_0\) is possible only if
\[
                         {571\over250}<E(v)<{773\over250}.     \tag{31}
\]

Equation (11) makes \(E\) strictly increasing.  Since in the \(v\)
coordinate \(E(v)=Y(v)/v\), (27) gives the exact endpoint checks
\[
\begin{aligned}
 {571\over250}{4611\over5000}-Y(4611/5000)
   &>{159652343530451\over200000000000000000}>0,\\
 Y(9701/10000)-{773\over250}{9701\over10000}
   &>{19492543073837\over250000000000000000}>0.              \tag{32}
\end{aligned}
\]
Every global maximizer has \(C(v)=c_\star>a_0\), so (31)--(32) prove
the certified enclosure
\[
             \boxed{{4611\over5000}<v_\star<{9701\over10000}}.
                                                                    \tag{33}
\]
Since \(x=v/\sqrt{2-v^2}\), exact squaring also gives
\[
                         \boxed{{43\over50}<x_\star<{943\over1000}}.
                                                                    \tag{34}
\]
These intervals contain every maximizer; they do not prove that the
maximizer or the root of (9) is unique.

## 5. Composition with the central-path comparison

Let \(y_i^\star\) be the radial coordinates of the exact closest point in
the objective-accuracy sublevel, and let \(\lambda\) be its KKT multiplier.
At central parameter \(\eta=\lambda/2\), the transformed central
coordinates satisfy
\[
                 p(y_i^{\rm c})=y_i^\star p'(y_i^\star).       \tag{35}
\]
Convexity gives \(p(y_i^\star)\le y_i^\star p'(y_i^\star)\), so
\(y_i^{\rm c}\ge y_i^\star\); this center is already accurate.  Definition
(2) gives the matching upper bound
\[
                         y_i^{\rm c}\le c_\star y_i^\star.     \tag{36}
\]
The first accurate central endpoint occurs no later and is coordinatewise
no larger.  Its exact distance from zero is consequently at most
\(c_\star\|y^\star\|_2=c_\star L_{\rm opt}(\epsilon)\).  Composing with
the audited same-endpoint inequality
\(L_{\rm CP}\le\Gamma_r d_\phi(0,X)\) proves (4).

The same proof is unchanged for common-scale Jordan spectral intervals.
For unequal positive scale weights, the factor multiplying (35) is common
to both KKT systems and cancels after choosing \(\eta=\lambda/2\).  Thus the
previous constant two in the weighted comparison can also be replaced by
\(c_\star<69/50\), without changing its weighted prefix factor.

## Scope and open point

The exact constant (2) is the best uniform scalar dilation.  Formula (7)
makes it elementary and (9) gives a necessary stationary equation.
Equations (33)--(34) rigorously localize every maximizer but do not count
the roots of (9).  A proof that (9) has exactly one root in \((0,1)\)
would certify the numerical value in (5) as the unique global maximum;
that uniqueness is not needed for (3)--(4) and is not claimed.  The global
best constant multiplying \(\Gamma_r\) may be smaller than \(c_\star\),
because the two comparison steps can have incompatible equality cases.

### Targeted primary-source screen (2026-09-04)

Nesterov--Nemirovski,
[*Primal Central Paths and Riemannian Distances for Convex
Sets*](https://doi.org/10.1007/s10208-007-9019-4), Example 5.1, explicitly
uses the same box barrier
\(-\sum_i\log(1-x_i^2)\) and computes local barrier quantities to compare
their refined short-step bound with the usual dimension-dependent bound.
Their main bounded-domain theorem gives an \(O(\nu^{1/4})\)
central-path/geodesic comparison.  It does not state the scalar endpoint
KKT matching in (35), optimize a uniform coordinate dilation, or give the
constant \(c_\star\).

Nesterov--Todd,
[*On the Riemannian Geometry Defined by Self-Concordant Barriers and
Interior-Point Methods*](https://doi.org/10.1007/s102080010032), Section
6.2, compute an exact Euclidean metric coordinate and geodesics for a
hypercube equipped with the different scalar barrier
\(-\log\cos\tau\).  Their product-distance rule is a direct antecedent of
the coordinatewise distance reduction, but neither that example nor the
general product theorem contains the accuracy-sublevel/central-endpoint
dilation problem here.  Papa Quiroz--Oliveira's nonstandard hypercube
barrier likewise has an explicit diagonal Riemannian metric but a different
scalar profile and purpose.

The elementary integral in (6), inverse formula, and one-variable maximum
should not carry a broad novelty claim independently.  The targeted search
did not locate the variational constant
\(\sup_y p^{-1}(yp'(y))/y\), the numerical value in (5), or its use as the
sharp uniform scalar factor between closest accuracy-sublevel points and
central endpoints for this barrier.  The safe label is **candidate exact
constant refinement inside the local spectral-interval comparison**.  It
is not a new general Riemannian-distance theorem or a proof that
\(c_\star\Gamma_r\) is globally sharp.  This was a targeted screen through
2026, not an exhaustive novelty or priority determination.

## Audit targets

1. Recheck the elementary transform (6)--(7) and both endpoint limits.
2. Recheck the elasticity identity (11), including the strict inequalities.
3. Recheck the threshold implication \(E>2\Rightarrow x>4/5\), monotonicity
   of \(G\), and all integer arithmetic in (15), (18), and (21)--(24).
4. Recheck the KKT scale \(\eta=\lambda/2\) and the composition in
   (35)--(36).
5. Do not infer uniqueness of the numerical stationary point or global
   sharpness of \(c_\star\Gamma_r\).
6. Independently reproduce the rational series and square-root
   enclosures in (26)--(34).

## Independent audit record

An independent hostile audit rederived the transform (6)--(7), both
compactification limits, and the identity
\(dE/d\log y=E-K\) with \(K=(\rho/B)^2<1\).  It separately checked
\(E>2\Rightarrow x>4/5\), monotonic decrease of \(G\), and both integrated
elasticity bounds.  The rational and logarithmic-series arithmetic in
(21)--(24) reproduces the positive margin
\[
 {255839420916449\over315546241820670000}.
\]
Finally, it verified that the endpoint and central KKT systems coincide at
\(\eta=\lambda/2\), including cancellation of unequal positive scale
weights.  No numerical uniqueness assumption enters the theorem.  The
audit returned **PASS** with no correction.

A further independent hostile audit returned **PASS after one
non-substantive strict-endpoint correction**.  Equations (12) and (19) are
strict for \(t>1\), while at \(t=1\) their two sides are equal; all stated
applications integrate over \(1<t\leq69/50\), so the correction changes no
bound.  The audit checked the transform and inverse in (6)--(7), both
endpoint limits and interior attainment, the exact elasticity identity,
the two comparison regimes, and monotonicity of \(G\).  Exact rational
recomputation reproduced every fraction in (15), (18), and (21)--(24),
including the positive margin
\(255839420916449/315546241820670000\).  An independent 80-digit numerical
maximization gave
\(x=0.9012017365086009\ldots\),
\(y=2.4538667416590275\ldots\), and
\(C=1.3748642004415517\ldots\), consistent with (5).  Finally, the audit
rederived \(\eta=\lambda/2\) and verified coordinatewise cancellation of
the common-scale and weighted Jordan factors before composition with the
corresponding prefix constants.  It found no proof of uniqueness beyond
the necessary stationary equation (9), and the note correctly does not
claim uniqueness.  The audit also supplied the one-term positive-series
certificate following (25), making \(69/50<\kappa_0\) analytic rather than
dependent on the displayed decimal approximation.

At research closure, the new rational enclosure was checked separately
against 80-digit evaluations of the elementary functions.  The strict
margins underlying (28) are positive, with
\[
 C(3787/4000)-68743/50000
   =0.0000042001612699\ldots .
\]
The endpoint elasticity values satisfy
\[
 E(4611/5000)=2.2831343941\ldots<571/250,\qquad
 E(9701/10000)=3.0920803733\ldots>773/250,
\]
and the exact algebraic map \(x=v/\sqrt{2-v^2}\) puts the two endpoints
strictly outside \(43/50<x<943/1000\) in the required directions.
Together with the displayed positive-series remainder bounds, this
mechanically checks (26)--(34).  No uniqueness claim was added.  This was
an internal closure check, not a third independent proof audit.
