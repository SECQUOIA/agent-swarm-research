# One-step Newton hardness for the linear-volume plateau-gain LP

Date: 2026-09-02

## Main result

The linear-volume plateau-gain LP in
`2026-09-02-linear-size-robust-gain-parity-lp.md` admits a public, exactly
centered, strictly positive infeasible start from which one algebraic full Newton correction
with target \(\widehat\mu=\mu_0/2\) reaches a feasible, dual-feasible point
that is exactly on the fixed-\(\mu_1\) central path on every plateau node.
Only the \(O(\log N)\)-node gain prefix uses different public local
complementarity parameters. Consequently:

- the updated primal amplitude state is \(O(N^{-1/2})\)-close to the true
  fixed-\(\mu_1\) central state; and
- the exact Newton-direction state has constant parity-decoding bias and
  therefore needs \(\Omega(N)=\Omega(P)\) coefficient queries;
- the same linear lower bound holds for every normalized approximate-direction
  state whose full-step update is nonnegative and has fixed
  right-hand-side-relative primal Newton residual.

This upgrades the quadratic-volume parallel-path Newton theorem to linear LP
dimension, at the polynomial dynamic range \(H=\Theta(\sqrt N)\).

A stronger public-right-hand-side theorem for the full stacked KKT direction,
including a residual-robust exactly preconditioned interface and offline--online
query accounting, is proved in
[2026-09-02-linear-plateau-full-kkt-lower-bound.md](2026-09-02-linear-plateau-full-kkt-lower-bound.md).

## Plateau-gain notation

There are \(P=17N+1\) nodes. Let
\[
 T=\left\lceil\frac12\log_2N\right\rceil,\qquad
 H_i=2^{\min\{i,T\}},\qquad H=2^T,
\]
and \(K=16N\) plateau-copy nodes. Exact feasibility fixes
\[
 d_i=H_i\tau_i,\qquad h_i=H_i,\qquad
 q_i+t_i=2H_i,
\tag{1}
\]
where \(\tau_i\) is the appropriate prefix product and equals endpoint parity
on the \(K\) output nodes.

Write
\[
 q_i=H_i+z_i,\qquad 0<z_i<H_i.
\]
For a local complementarity parameter \(\mu_i>0\), stationarity in the one
local null direction is
\[
 \frac1{\mu_i}
 =\frac1{2H_i+z_i}+\frac1{z_i}-\frac1{H_i-z_i}.
\tag{2}
\]
The primal coordinates are
\[
 L_i=H_i+\frac{z_i}{2},\qquad
 S_i=\frac{z_i}{2},\qquad
 h_i=H_i,\qquad t_i=H_i-z_i.
\tag{3}
\]
The \(L_i,S_i\) positions are swapped according to \(\tau_i\).

Fix once and for all
\[
 \mu_1=\frac1{16}.
\tag{4}
\]
Let \(z_H\) solve (2) at scale \(H\) and parameter \(\mu_1\), and put
\[
 q_H=H+z_H,\quad
 L_H=H+z_H/2,\quad S_H=z_H/2,
\]
\[
 R_*=\frac{\mu_1q_H^2}{L_HS_H}.
\tag{5}
\]

## Matching the gain prefix to one common secant

For a scale \(G\ge1\), let \(\mu_G(z)\) be the reciprocal of the right side
of (2), on the interval where that right side is positive, and define
\[
 R_G(z)
 =\frac{\mu_G(z)(G+z)^2}
        {(G+z/2)(z/2)}.
\tag{6}
\]
As \(z\downarrow0\),
\[
 R_G(z)\longrightarrow2G.
\tag{7}
\]
As \(z\) approaches the local analytic-center root where the right side of
(2) vanishes, \(R_G(z)\to+\infty\). Moreover, at every positive \(z\),
\(\mu_G(z)>z\), because the two non-\(1/z\) terms in (2) have negative
sum. Hence
\[
 R_G(z)>
 \frac{4(G+z)^2}{2G+z}>2G,
\]
where the last inequality is equivalent to
\(3Gz+2z^2>0\).

These solutions are in fact unique. With \(r=z/G\), direct simplification gives
\[
 \frac{R_G(z)}G
 =\frac{4(1+r)^2(1-r)}{2-2r-3r^2},
 \qquad
 0<r<r_{\rm ac}:=\frac{\sqrt7-1}{3}.
\]
After removing the positive squared denominator, its derivative has numerator
\[
 4+2r-r^2+4r^3+3r^4>0\qquad(0<r<r_{\rm ac}<1).
\]
Thus \(R_G\) is strictly increasing from \(2G\) to \(+\infty\).

Since \(H_i\le H\) and \(R_*>2H\), continuity gives, for every gain-prefix
scale \(H_i<H\), a unique public \(z_i\in(0,H_i)\) such that
\[
 R_{H_i}(z_i)=R_*.
\tag{8}
\]
Set \(\mu_i=\mu_{H_i}(z_i)\). On every
plateau node \(H_i=H\), use
\[
 z_i=z_H,\qquad \mu_i=\mu_1.
\tag{9}
\]
All these quantities depend only on \(N\) and the public gain profile, not on
the hidden signs.

At every node,
\[
 R_*=\frac{\mu_iq_i^2}{L_iS_i},
\qquad
 \frac{\mu_i}{R_*}=\frac{L_iS_i}{q_i^2}<\frac14.
\tag{10}
\]

## Public exactly centered start

Let
\[
 \alpha=\frac32,\qquad
 \mu_0=\frac{R_*}{\alpha^2}=\frac{4R_*}{9},
\qquad
 C=\frac{R_*}{\alpha}=\frac{2R_*}{3},
\qquad
 \widehat\mu=C-\mu_0=\frac{\mu_0}{2}.
\tag{11}
\]

For the signed pair at node \(i\), set
\[
 u_i^0=v_i^0=a_i:=\frac{q_i}{\alpha}=\frac{2q_i}{3},
\qquad
 s_{u,i}^0=s_{v,i}^0=b_i:=\frac{\mu_0}{a_i}.
\tag{12}
\]

For each public target coordinate \(x\in\{H_i,H_i-z_i\}\), let \(\lambda_i\)
be the smaller positive root of
\[
 \mu_i \lambda^2-C\lambda+\mu_0=0,
\tag{13}
\]
and initialize that coordinate by
\[
 x^0=\lambda_i x,\qquad s^0=\frac{\mu_0}{x^0}.
\tag{14}
\]
Use (14) separately for \(h_i\) and \(t_i\); their roots use the same
\(\mu_i\), so in fact their scale factor is the same.

Equation (10) makes the discriminant in (13) strictly positive:
\[
 C^2-4\mu_0\mu_i
 =\frac{4R_*}{9}(R_*-4\mu_i)>0.
\]
After division by \(R_*\), (13) is
\[
 \frac{\mu_i}{R_*}\lambda^2-\frac23\lambda+\frac49=0.
\]
Since \(0<\mu_i/R_*<1/4\), its smaller root obeys
\[
 \frac23<\lambda_i<\frac43.
\tag{15}
\]
The polynomial-range claim can be made quantitative. Equation (2) at the
plateau and \(\mu_1=1/16\) imply
\[
 \frac{15}{256}\le z_H<\frac1{16},
 \qquad 2H<R_*<\frac52H.
\]
Also, positivity of the right side of (2) implies
\(z_i<r_{\rm ac}H_i\), while (10) gives
\(0<\mu_i<R_*/4<5H/8\). Equations (12), (14), and (17) then show that
every primal or slack coordinate used here lies between inverse-polynomial
and polynomial bounds (indeed, the largest magnitude is \(O(H)\)). Thus the
whole initialization is public, strictly positive, polynomially bounded, and
exactly centered:
\[
 x_j^0s_j^0=\mu_0
\quad\text{for every coordinate }j.
\tag{16}
\]
Take \(y^0=0\). Primal and dual infeasibility are allowed.

More explicitly, all three Newton right-hand sides are public. At the start,
every signed difference is \(d_i^0=u_i^0-v_i^0=0\), so the hidden transition
coefficients multiply zero in \(b-Ax^0\). Since \(y^0=0\), the dual residual is
\(c-s^0\), and the complementarity residual follows from (16). The only hidden
input to the Newton system is therefore in the coefficient matrix \(A\), not in
the start or right-hand side. Exact evaluation of the public algebraic numbers
is free in this coefficient-query statement; a gate-complexity version would
have to specify their finite-precision preparation cost.

## Feasible dual endpoint

Let \(x^1\) be the feasible point (3), with pair orientation determined by
\(\tau_i\), and define
\[
 s_j^1=\frac{\mu_i}{x_j^1}
\quad\text{on every coordinate belonging to node }i.
\tag{17}
\]
This endpoint is complementary with a node-dependent \(\mu_i\), and is
exactly complementary at the fixed \(\mu_1\) on the plateau.

It is also dual feasible. Indeed, in the local null direction the slack
stationarity condition is
\[
 \frac{s_{u,i}^1+s_{v,i}^1}{2}-s_{t,i}^1=1.
\tag{18}
\]
Substituting (3) and (17), equation (18) is exactly (2). Hence
\(W^\top(c-s^1)=0\) for the full input-independent null basis \(W\).
Because the equality matrix has full row rank,
\[
 c-s^1\in\operatorname{range}(A^\top),
\]
so there is a unique \(y^1\) with
\[
 A^\top y^1+s^1=c.
\tag{19}
\]

## One standard Newton correction

### Theorem 1

From the public start \((x^0,y^0,s^0)\), the unique infeasible-start Newton
correction with centering target
\(\widehat\mu=\mu_0/2\) is
\[
 (\Delta x,\Delta y,\Delta s)
 =(x^1-x^0,y^1-y^0,s^1-s^0).
\tag{20}
\]
Thus one full step reaches the feasible, dual-feasible endpoint above and is
exactly on the fixed-\(\mu_1\) central path throughout the plateau.

### Proof

Primal and dual feasibility of the endpoint give the two linear Newton
equations. For complementarity, first consider a signed pair. From (10)--(12),
\[
 a_i^2=\frac{\mu_0L_iS_i}{\mu_i}.
\tag{21}
\]
Consequently the two possible target coordinates have the same cross term:
\[
 b_iL_i+a_i\frac{\mu_i}{L_i}
 =b_iS_i+a_i\frac{\mu_i}{S_i}
 =b_iq_i=C.
\tag{22}
\]
For an \(h\) or \(t\) coordinate, (13)--(14) give
\[
 s^0x^1+x^0s^1
 =\frac{\mu_0}{\lambda_i}+\mu_i \lambda_i=C.
\tag{23}
\]
Thus every coordinate satisfies the common secant identity
\[
 s_j^0x_j^1+x_j^0s_j^1=C.
\]
Using (16),
\[
 S^0\Delta x+X^0\Delta s
 =(C-2\mu_0)\mathbf1
 =(\widehat\mu-\mu_0)\mathbf1.
\tag{24}
\]
This is the standard complementarity Newton equation with
\(\widehat\mu=\mu_0/2\). Full row rank and positivity make the normal matrix
\(A(S^0)^{-1}X^0A^\top\) SPD, proving uniqueness. \(\square\)

## Proximity to the true fixed-\(\mu_1\) central state

Let \(x^{\rm cen}(\mu_1)\) be the genuine global central point. The constructed
endpoint \(x^1\) agrees with it on every node \(i\ge T\), including the whole
length-\(16N\) output plateau. They differ only on the \(T=O(\log N)\) gain
nodes.

All primal coordinates at a scale \(H_i\) are \(O(H_i)\), and
\[
 \sum_{i<T}H_i^2<\frac{H^2}{3}.
\]
Meanwhile, the \(K=16N\) output nodes alone contribute at least
\(16NH^2\) to the squared norm of either central primal point. Therefore
\[
 \frac{\|x^1-x^{\rm cen}(\mu_1)\|_2}
      {\|x^{\rm cen}(\mu_1)\|_2}
 =O(N^{-1/2}).
\tag{25}
\]
The normalized amplitude states have the same
\(O(N^{-1/2})\) Euclidean-distance bound.

Within the symmetric public-pair initialization ansatz used here, exact global
centrality in one step is obstructed: the common pair secant is
\[
 q_i\sqrt{\frac{\mu_0\mu_1}{L_iS_i}},
\]
which varies with the public gain scale \(H_i\). The local \(\mu_i\) values
in (8) equalize this secant while confining the departure from
fixed-\(\mu_1\) centrality to \(O(\log N)\) low-mass nodes. This calculation
is an obstruction for that ansatz, not an impossibility theorem for every
public initialization.

## Exact Newton-direction state

For every node, (12) and (3) give, up to the hidden swap,
\[
 \Delta L_i=\frac{2H_i-z_i}{6},
\qquad
 \Delta S_i=-\frac{4H_i+z_i}{6}.
\tag{26}
\]
Using \(0<z_i<H_i\),
\[
 \frac{H_i}{6}<\Delta L_i<\frac{H_i}{3},
\qquad
 \frac{2H_i}{3}<|\Delta S_i|<\frac{5H_i}{6}.
\tag{27}
\]
For \(h,t\), (15) gives
\[
 |\Delta h_i|\le\frac{H_i}{3},
\qquad
 |\Delta t_i|\le\frac{H_i}{3}.
\tag{28}
\]
Hence the total squared direction norm per node is at most
\[
 \frac{37}{36}H_i^2.
\tag{29}
\]
The correct-minus-incorrect squared pair mass is at least
\[
 (\Delta S_i)^2-(\Delta L_i)^2
 =\frac{H_i(H_i+z_i)}{3}
 \ge\frac{H_i^2}{3}.
\tag{30}
\]

On an output \(u\)-coordinate report \(-1\), on an output \(v\)-coordinate
report \(+1\), and return a fair sign elsewhere. Since all \(K=16N\) output
nodes have scale \(H\), while
\[
 \sum_iH_i^2<
 \left(17N+\frac43\right)H^2,
\tag{31}
\]
the ideal direction-state decoder has bias at least
\[
 \frac{K H^2/3}
 {2(37/36)\sum_iH_i^2}
 >
 \frac{96N}{37(17N+4/3)}
 >\frac17
\qquad(N\ge2).
\tag{32}
\]

### Theorem 2 (linear-dimension direction-state lower bound)

Any coherent sparse-coefficient-query algorithm whose unconditional reduced
output density operator \(\rho\) satisfies
\[
 D_{\rm tr}\!\left(\rho,
 |\Delta x/\|\Delta x\|_2\rangle
 \langle\Delta x/\|\Delta x\|_2|\right)\le\frac1{100}
\]
for the Newton correction in Theorem 1 makes
\[
 \boxed{\Omega(N)=\Omega(P)}
\]
LP coefficient queries. The same holds for a heralded branch of fixed
success probability after charging constant repetition.

The fixed decoder retains constant bias after trace error \(1/100\), and
three independent repetitions already amplify its one-copy success probability
above \(2/3\). Bounded-error quantum parity requires \(\Omega(N)\) hidden-sign queries.
Every sparse row, column, position, or value query to the LP is simulated by
at most one hidden-sign query. Row and column sparsity remain at most four,
and all LP coefficients remain in \(\{-2,-1,0,1,2\}\).

### Output-model audit

The density operator in Theorem 2 may be mixed and is the unconditional output
of an arbitrary CPTP implementation. Under the squared-fidelity convention, its
trace-distance premise can be replaced by

\[
 \langle\Delta x/\|\Delta x\|_2|\rho|
 \Delta x/\|\Delta x\|_2\rangle\ge\frac{9999}{10000}.
\tag{33}
\]

For a heralded preparation using \(Q\) queries per trial and succeeding with
probability \(p\), repetition of the entire trial gives the precise tradeoff

\[
 \frac Qp=\Omega(N).                                    \tag{34}
\]

Thus \(p=\Omega(1)\) recovers Theorem 2. A postselected model that does not charge
the inverse success probability is outside the theorem. For an unheralded physical
ensemble, suppose a classical internal event of probability \(\theta\) has a
conditional output satisfying the trace premise, while the other branches are
arbitrary. The good branch has decoder success greater than
\(1/2+1/7-1/100=443/700\). Hence the unconditional decoder still has success above
one half, and can be amplified, whenever \(\theta>350/443\). No conclusion follows
from an unspecified smaller good-branch probability because bad branches may be
adversarial.

The normalized-state contract is projective. If a nonzero approximate vector
\(v\) satisfies, for some nonzero real scale \(\lambda\),

\[
 \|v-\lambda\Delta x\|_2
 \le\frac{|\lambda|}{200}\|\Delta x\|_2,                \tag{35}
\]

then its normalized pure state is within Euclidean, and therefore trace, distance
at most \(1/100\) of the exact direction ray. This follows from the elementary
bound

\[
 \left\|\frac v{\|v\|_2}-
 e^{i\phi}\frac{\Delta x}{\|\Delta x\|_2}\right\|_2
 \le 2\frac{\|v-\lambda\Delta x\|_2}
 {|\lambda|\|\Delta x\|_2},                             \tag{36}
\]

where \(e^{i\phi}=\lambda/|\lambda|\). Consequently Theorem 2 also lower-bounds
an amplitude encoding of such a vector, and a fortiori an explicit classical
vector with this guarantee. Merely approximating the norm of \(\Delta x\) is not
enough; the direction ray must also be accurate.

### Direction state versus update state

A bare density operator for the direction cannot in general be converted to the
updated state. The states of \(\Delta x\) and \(-\Delta x\) are identical, whereas
\(x^0+\Delta x\) and \(x^0-\Delta x\) are generally different. Thus no CPTP map on
the direction density operator alone can implement vector addition with the public
offset.

With a stronger, phase-referenced preparation interface, the conversion is cheap
on this family. The norms of \(x^0,\Delta x,x^1\) are public because changing the
input only swaps each \((u_i,v_i)\) pair. A controlled preparation with a fixed
phase convention, followed by the standard two-term linear-combination
postselection, prepares the ray of \(x^0+\Delta x=x^1\) with probability

\[
 \frac{\|x^1\|_2^2}{2(\|x^0\|_2^2+\|\Delta x\|_2^2)}
 >\frac{18}{293}.                                       \tag{37}
\]

Indeed, per node \(\|x^0_i\|_2^2<64H_i^2/9\), (29) gives
\(\|\Delta x_i\|_2^2<37H_i^2/36\), and
\(\|x^1_i\|_2^2\ge H_i^2\). The reverse subtraction succeeds with probability
greater than \(4/209\), using
\(\|\Delta x_i\|_2^2>4H_i^2/9\) and
\(\|x^1_i\|_2^2<9H_i^2/2\). Hence exact direction and exact update preparations
are equivalent up to constant overhead only under this coherent phase-referenced
interface, not under the density-output contract alone.

## Robust residual theorem for the direction state

The full Newton endpoint \(x^1\) is exactly feasible. More strongly, a fixed
primal Newton residual suffices for hardness of the **direction** state, provided
the full-step update remains in the nonnegative orthant.

### Theorem 3 (residual-accurate direction-state lower bound)

Suppose an algorithm outputs an unconditional density operator \(\rho\) for which
there is a nonzero direction \(\widetilde{\Delta x}\) whose update

\[
 \widetilde x=x^0+\widetilde{\Delta x}\ge0
\]

satisfies the primal Newton residual

\[
 \frac{\|A\widetilde x-b\|_2}{\|b\|_2}\le\frac1{100},
\tag{38}
\]

and

\[
 D_{\rm tr}\!\left(\rho,
 |\widetilde{\Delta x}/\|\widetilde{\Delta x}\|_2\rangle
 \langle\widetilde{\Delta x}/\|\widetilde{\Delta x}\|_2|\right)
 \le\frac1{100}.                                        \tag{39}
\]

Then the algorithm makes \(\Omega(N)=\Omega(P)\) coefficient queries. Any
additional dual-residual, complementarity, objective, or neighborhood promise can
be imposed simultaneously without weakening the implication, because the proof
does not use it. This sentence does not assert that the displayed full step meets a
particular algorithm's neighborhood or acceptance rule.

### Proof

On a plateau node let \(\lambda_H\) be the public scale factor in (14). Since
\(R_*>2H\), the coefficient \(\delta=\mu_1/R_*\) is below \(1/(32H)\le1/32\).
The polynomial in (13), divided by \(R_*\), is positive at zero and at
\(\lambda=3/4\) has value

\[
 \frac9{16}\delta-\frac1{18}<0.
\]

Thus its smaller root obeys

\[
 \frac23<\lambda_H<\frac34.                             \tag{40}
\]

Write \(\widetilde d=\widetilde u-\widetilde v\) and
\(\widetilde q=\widetilde u+\widetilde v\). The robust decoder estimates for the
gain LP, applied to (38), give on every plateau node

\[
 \tau_i\widetilde d_i>\frac{37}{40}H,\qquad
 \frac{37}{40}H<\widetilde h_i<\frac{43}{40}H,\qquad
 \widetilde q_i,\widetilde t_i<\frac{433}{200}H.         \tag{41}
\]

Here the last constant uses the cap residual and \(H\ge1\). At the public start,

\[
 q_i^0=\frac43(H+z_H),\qquad h_i^0=\lambda_H H,\qquad
 t_i^0=\lambda_H(H-z_H),\qquad 0<z_H<\frac1{16}.        \tag{42}
\]

Nonnegativity gives \(\widetilde q_i\ge|\widetilde d_i|\). Combining
(40)--(42) yields

\[
 |\widetilde q_i-q_i^0|<\frac56H,\qquad
 \frac7{40}H<\widetilde{\Delta h}_i<\frac{49}{120}H,\qquad
 |\widetilde{\Delta t}_i|<\frac{77}{50}H.              \tag{43}
\]

Since the start has zero pair difference,

\[
 \widetilde{\Delta u}_i^2+\widetilde{\Delta v}_i^2
 =\frac{(\widetilde q_i-q_i^0)^2+\widetilde d_i^2}{2}.
\]

Equations (41)--(43) bound the squared direction norm on every plateau node by
less than \(16H^2/3\). On the \(i<T\) prefix, the general estimates
\(\|\widetilde x_i\|^2<11H_i^2\) and
\(\|x_i^0\|^2<64H_i^2/9\), together with
\(\sum_{i<T}H_i^2<H^2/3\), suffice. Hence, for \(N\ge2\),

\[
 \|\widetilde{\Delta x}\|_2^2<100NH^2.                 \tag{44}
\]

It remains to use phase information that the computational-basis decoder in
Theorem 2 did not need. Put

\[
 |g_i\rangle=\frac{|u_i\rangle-|v_i\rangle}{\sqrt2},
 \qquad
 O=\bigoplus_{i\in S}
 (|h_i\rangle\langle g_i|+|g_i\rangle\langle h_i|).
\tag{45}
\]

The observable is input-independent and \(\|O\|=1\). All nodes in \(S\) have
\(\tau_i=p_N\), so (41), (43), and (44) imply

\[
 p_N\langle\widetilde{\Delta x}/\|\widetilde{\Delta x}\||O|
 \widetilde{\Delta x}/\|\widetilde{\Delta x}\|\rangle
 =\frac{\sqrt2\sum_{i\in S}\widetilde{\Delta h}_i
                    \widetilde d_i}
        {\|\widetilde{\Delta x}\|_2^2}
 >\frac{259\sqrt2}{10000}>\frac1{28}.                  \tag{46}
\]

The two-outcome POVM \((I\pm O)/2\) therefore guesses parity with ideal bias
greater than \(1/56\). Trace error \(1/100\) leaves bias greater than
\(1/56-1/100>0\). Constant repetition and the parity query lower bound prove the
claim. \(\square\)

The mixed, heralded, and postselected interpretations are exactly those in the
output-model audit above. In particular, a heralded implementation obeys
\(Q/p=\Omega(N)\), while free postselection is not covered. Theorem 3 also applies
to an explicit approximate vector satisfying (38): its exact normalized encoding
meets (39) with zero trace error, and an explicit classical output is an even
stronger interface.

### Corollary 4 (robust update state)

Under (38), preparing a state within trace distance \(1/100\) of
\(|\widetilde x/\|\widetilde x\|_2\rangle\) also requires
\(\Omega(N)=\Omega(P)\) coefficient queries. This is the direct robust-plateau
theorem. Theorem 3 is stronger at the Newton interface because its state encodes
the direction \(\widetilde{\Delta x}\), not the updated primal point.

## Why a residual promise alone is insufficient

The nonnegative-update premise in Theorem 3 is essential. This remains true even
if one replaces the primal residual by the residual of the **full** Newton system.
Write that system as

\[
 \mathcal K
 \begin{pmatrix}\Delta x\\ \Delta y\\ \Delta s\end{pmatrix}
 =r,\qquad
 \mathcal K=
 \begin{pmatrix}
 A&0&0\\
 0&A^T&I\\
 S^0&0&X^0
 \end{pmatrix}.                                        \tag{47}
\]

For each output-plateau node define the public unit null vector

\[
 W_i=\sqrt{\frac23}
 \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right),
 \qquad w=\sum_{i\in S}W_i.                              \tag{48}
\]

Then \(Aw=0\), \(\|w\|_2=\sqrt K\), and \(w\) is independent of every hidden
sign. For a public scalar \(M>0\), perturb the exact solution by

\[
 e_x=Mw,\qquad e_y=0,\qquad
 e_s=-(X^0)^{-1}S^0e_x.                                 \tag{49}
\]

The primal and complementarity residual perturbations vanish exactly; the only
full-system residual is the dual block \(e_s\). Directly from (10)--(15), on the
plateau coordinates in the support of \(w\),

\[
 \|(X^0)^{-1}S^0w\|_2\le\frac3H\|w\|_2.                \tag{50}
\]

To make the constants self-contained, stationarity (2) at
\(\mu_1=1/16\) gives \(15\mu_1/16\le z_H<\mu_1\). For example, the pair ratio is
\(s_u^0/u^0=\mu_1/(L_HS_H)\le32/(15H)\); the same formulas
give a ratio below \(3/H\) on \(t\). Explicitly,
\(R_*\le(289/120)H\), hence \(\mu_0\le(289/270)H\), while
\(\lambda_H>2/3\) and \(H-z_H>15H/16\); therefore

\[
 \frac{s_t^0}{t^0}
 =\frac{\mu_0}{\lambda_H^2(H-z_H)^2}<\frac3H.
\]

On the other hand, the cap component of the primal Newton right-hand side at every
output node has magnitude

\[
 q_i^0+t_i^0-2h_i^0=(H+z_H)(4/3-\lambda_H)>\frac7{12}H
\]

by (40). Therefore

\[
 \frac{\|\mathcal K e\|_2}{\|r\|_2}
 \le\frac{36M}{7H^2}.                                   \tag{51}
\]

Choose \(M=H^{3/2}\). Equation (29) and (31) give

\[
 \frac{\|\Delta x\|_2}{M\|w\|_2}=O(H^{-1/2}),
 \qquad
 \left\|
 \frac{\Delta x+Mw}{\|\Delta x+Mw\|_2}
 -\frac w{\|w\|_2}\right\|_2=O(H^{-1/2}).              \tag{52}
\]

At the same time (51) is \(O(H^{-1/2})\). Hence, for every pair of fixed positive
state and relative-residual tolerances and all sufficiently large \(N\), the
zero-query, input-independent state \(|w/\|w\|\rangle\) is close to the primal
part of a direction having that full-Newton residual. This counterexample concerns
the normalized primal-direction output; no claim about a state encoding the entire
\((\Delta x,\Delta y,\Delta s)\) triple is needed. The perturbation eventually
makes updated \(t\)-coordinates negative, which is exactly why it does not
contradict Theorem 3.

There is a general condition-aware residual statement, but it cannot be replaced
by a fixed conventional relative residual. Let \(\Pi_x\) select the primal
direction block and define

\[
 \Gamma_x=\frac{\|\Pi_x\mathcal K^{-1}\|_2\,\|r\|_2}
                  {\|\Delta x\|_2}.                     \tag{53}
\]

If \(\widetilde z\) satisfies

\[
 \frac{\|\mathcal K\widetilde z-r\|_2}{\|r\|_2}
 \le\frac1{200\Gamma_x},                                \tag{54}
\]

then
\(\|\Pi_x\widetilde z-\Delta x\|_2\le\|\Delta x\|_2/200\),
so (35)--(36) and Theorem 2 give the \(\Omega(P)\) lower bound. Equations
(48)--(52) show why the factor \(\Gamma_x\), or a geometric restriction such as
nonnegativity of the update, is indispensable.

## Scope

The endpoint is not globally central: its \(O(\log N)\) gain-prefix nodes use
public \(\mu_i\neq\mu_1\). This is necessary for an exact common Newton
secant under a public symmetric pair start. The primal endpoint state is
nevertheless \(O(N^{-1/2})\)-close to the true fixed-\(\mu_1\) central state,
and the entire parity-carrying plateau is exactly central.

Theorem 1 is an identity for the standard infeasible-start Newton linear
system, not a claim that a conventional path-following neighborhood or merit
test accepts the full step. Indeed, \(\widehat\mu=2R_*/9=\Theta(H)\), whereas
the actual endpoint products on the plateau equal \(\mu_1=1/16\). The omitted
quadratic term \(\Delta x_j\Delta s_j\) is therefore macroscopic, and the
endpoint is far from a global complementarity neighborhood centered at the
linearized target \(\widehat\mu\). Theorem 3 and Corollary 4 likewise concern a
nonnegative approximately feasible full-step update and, respectively, its
direction or original-primal state. They do not assert IPM acceptance or a global
central-neighborhood guarantee. Without nonnegativity, the construction
(47)--(52) rules out any theorem based only on a fixed conventional Newton-system
relative residual.

The theorem is end to end and preconditioner independent. Any setup,
transformed-RHS, iterative-solve, or recovery implementation producing the
promised original direction/update state has total raw coefficient-query cost
\(\Omega(N)\).

The distinction between a density output and a phase-referenced preparation
oracle is also substantive. The former suffices for every lower bound here but
does not by itself permit direction-to-update addition. The latter permits the
constant-success conversions in (37), with its preparation, postselection, and
inverse-success costs included in the end-to-end query count.

Here, “exactly centered” means the componentwise complementarity identity
\(X^0S^0\mathbf 1=\mu_0\mathbf 1\); the start is deliberately primal and dual
infeasible and is not claimed to lie on a feasible central path. Likewise,
Theorem 1 identifies the exact algebraic Newton correction and shows that its
unit step is positive and feasible at the endpoint. It does not assert that a
particular neighborhood-based infeasible IPM would accept this unit step under
its own line-search rule. The public algebraic start is supplied for free in
the coefficient-query model. A finite-precision gate-cost theorem would also
have to charge for preparing or approximating its public entries.

## Literature and novelty audit

Checked against open primary literature through 2026-09-02. The defensible
novelty claim is the **LP-native interface theorem**: a fixed-pattern,
row-and-column-sparse LP and a sign-independent complementarity-centered
infeasible start for which one actual standard Newton correction has an
\(\Omega(P)\) coefficient-query lower bound as a normalized primal-direction
state. The ingredients around that interface have substantial prior art:

- QIPMs have long used a QLSA to prepare a normalized Newton-direction state
  and tomography to recover a classical update; see Kerenidis--Prakash
  ([arXiv:1808.09266](https://arxiv.org/abs/1808.09266)),
  Casares--Martin-Delgado
  ([arXiv:1902.06749](https://arxiv.org/abs/1902.06749)), and Augustino et al.
  ([arXiv:2112.06025](https://arxiv.org/abs/2112.06025)). These are upper-bound
  and convergence results, not coefficient-query lower bounds for a specified
  Newton iterate.
- Wu--Yang--Terlaky's preconditioned infeasible QIPM starts Algorithm 2 at the
  public uniform point \((\omega_*\mathbf1,0,\omega_*\mathbf1)\), which is
  componentwise complementarity-centered, and solves a transformed Newton
  system by QLSA and tomography
  ([arXiv:2412.11307](https://arxiv.org/abs/2412.11307)). Thus a public centered
  infeasible start is not itself new. Their Theorem 1 is an upper complexity
  bound under QRAM, basis, conditioning, and accuracy assumptions; it does not
  construct a hard one-step direction or prove an oracle lower bound.
- Apers--Gribling Theorem 8.4 proves
  \(\Omega(\sqrt{ndr})\) quantum row queries for the *optimal value* of a tall
  inequality LP to constant additive error
  ([arXiv:2311.03215v3](https://arxiv.org/abs/2311.03215v3)); it refines the
  LP/SDP value lower bound of van Apeldoorn--Gily\'en--Gribling--de Wolf,
  Theorem 29 and Corollary 30
  ([arXiv:1705.01843](https://arxiv.org/abs/1705.01843)). Those contracts do not
  request a Newton-direction state, do not fix a public IPM start, and do not
  imply Theorem 2. Conversely, Theorem 2 is not a stronger optimal-value lower
  bound: it addresses a different output problem and a sparse coefficient
  oracle rather than the tall-LP row oracle.
- Generic QLS lower bounds are the closest technical comparators. Orsucci--
  Dunjko Propositions 6 and 17 give
  \(\widetilde\Omega(\min\{\kappa,D\})\) queries for a designated
  positive-definite QLS solution state, including constant-sparse access
  ([arXiv:2101.11868](https://arxiv.org/abs/2101.11868)). Wang--Zhang prove
  \(\Omega(\kappa)\) query depth for designated QLS solution-state generation
  (Theorem 1 and its block-access corollary,
  [arXiv:2407.06012](https://arxiv.org/abs/2407.06012)). Mori et al. prove
  \(\Omega(\kappa\log(1/\epsilon))\) at constant sparsity (Theorem 1) and
  \(\Omega(\kappa\sqrt{s})\) at constant error (Theorem 2), again for the
  designated inverse state
  ([arXiv:2601.16697v2](https://arxiv.org/abs/2601.16697v2)). None of these
  theorems supplies the LP, the public infeasible IPM iterate, or the Newton
  secant identities required here, so Theorem 2 is not a formal corollary of
  them. It can instead be viewed as a structured KKT/Newton embedding of parity.
- The geometric clock and endpoint-repetition mechanism is not new. Mori et
  al.'s QLS construction uses a geometrically weighted inverse clock and a
  repeated interval carrying the computed parity; Wang--Zhang use the same
  broad inverse-clock strategy. Biased Feynman--Kitaev clocks already realize
  geometric ground-state amplitudes in Caha--Landau--Nagaj, equations
  (18)--(19) ([arXiv:1712.07395](https://arxiv.org/abs/1712.07395)). The new
  claim should therefore not be phrased as invention of plateau amplification;
  the contribution is its robust realization inside a bounded-degree LP
  feasibility system and then inside one bona fide primal--dual Newton step.
- Somma--Subasi prove that verifying a supplied QLS solution state can require
  \(\Omega(\kappa)\) uses of the right-hand-side preparation unitary in the
  worst case ([arXiv:2007.15698](https://arxiv.org/abs/2007.15698)). This is a
  verification/copy-access result, not a lower bound on LP coefficient queries
  needed to generate the Newton state. Dalzell--Li--Su's beyond-condition-number
  solver ([arXiv:2607.07691](https://arxiv.org/abs/2607.07691)) is likewise an
  upper bound for a designated QLS state. Neither collides with the end-to-end,
  raw-coefficient lower bound here.
- Binkowski's “practical lower bounds”
  ([arXiv:2604.24362](https://arxiv.org/abs/2604.24362)) are benevolent
  resource/runtime lower estimates for two hybrid QIPM pipelines on benchmark
  instances. They are not asymptotic oracle lower bounds and do not contain a
  hard Newton-state construction.

No open primary source found in this audit states the combination in Theorems
1--3, including the robust approximate-direction output theorem and its fixed
interference decoder. That is evidence of a narrow novelty gap, not a priority guarantee. The
most important citation and wording discipline is to claim novelty only for
the sparse-LP/public-start/Newton-state combination, not for parity clocks,
centered infeasible initialization, generic \(\kappa\)-dependent QLS hardness,
or quantum LP lower bounds in general.

Status: **proof complete in the fixed-pattern sparse coefficient-query model.**
