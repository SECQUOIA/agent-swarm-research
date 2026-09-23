# Bounded-range condition-one hardness at the sharp residual scale

Date: 2026-09-02

## Result and scope

The convex-mixture obstruction does leave a sharp escape route.  There is a
linear-size family of standard-form LPs with

- coefficients, right-hand sides, objective coefficients, all feasible primal
  variables, and the relevant dual slack vectors bounded by absolute constants;
- at most four nonzeros per row and three per column;
- one hidden input bit per input-dependent coefficient value;
- a public, strictly positive, coordinatewise-centered infeasible start;
- an exactly scalar reduced Newton matrix at that start and an exactly scalar
  reduced log-barrier Hessian on the whole central path; and
- an exact normalized central-point state and an exact normalized primal
  Newton-direction state whose preparation to constant trace error needs
  \(\Omega(N)\) raw coefficient queries; and
- the same lower bound uniformly for normalized states of arbitrary
  nonnegative points with primal residual at most \(1/(100\sqrt N)\).

The result is not limited to exact states.  Every nonnegative point with
absolute residual at most \(1/(100\sqrt N)\) has a constant correct-parity
margin in its normalized amplitude state, so preparing such a state also
needs \(\Omega(N)\) raw queries.  Conversely, an explicit average of the
\(N\) single-bit-neighbor central points has the opposite output parity and
residual exactly \(2/\sqrt N\).  Since \(\|b\|_2=\sqrt2\), both bounds are at
relative scale \(\Theta(N^{-1/2})\).  This matches the exponent in
`2026-09-02-convex-mixture-local-input-obstruction.md` and pins down the
threshold up to constants.

Tuning the hidden length therefore gives the worst-case accuracy curve
\(\Omega(\min\{P,\epsilon^{-2}\})\). Because \(\|b\|_2=\sqrt2\), the same
exponent holds for relative residual. This curve is a family
reparameterization, not accumulating hardness within one fixed instance.

The hard output requires a linear public copy plateau.  For this construction,
if the plateau has \(K=o(N)\) nodes, exact target states for two inputs of
opposite parity have trace distance \(o(1)\).  Hence no one-copy, constant-bias
parity reduction is possible.  The important distinction from the robust
gain construction is therefore:

\[
 \boxed{\text{state hardness needs only }K=\Theta(N)\text{ bounded copies,}
 \quad\text{not }\Theta(\sqrt N)\text{ dynamic range}.}
\]

This is a unit-height specialization and conceptual sharpening of the exact
central secant construction in
`2026-09-02-exact-central-plateau-newton-direction.md`.  The specialization is
substantive for the resource theorem: removing the gain prefix simultaneously
makes the raw coefficients bounded and the entire, unpreconditioned reduced
geometry condition one.  It necessarily gives up the earlier robust-residual
claim at constant relative error, but retains robustness at the sharp
\(N^{-1/2}\) relative scale.

## 1. The bounded family

Let \(N\ge2\), \(K=16N\), and

\[
                       P=N+K+1=17N+1.
\tag{1}
\]

The hidden input is \(\sigma=(\sigma_1,\ldots,\sigma_N)\in\{\pm1\}^N\).
There are four nonnegative variables \((u_i,v_i,h_i,t_i)\) at each node
\(i=0,\ldots,P-1\).  Write

\[
                  d_i=u_i-v_i,\qquad q_i=u_i+v_i.
\]

The equality constraints are

\[
\begin{aligned}
 d_0&=1,\\
 d_i-\sigma_i d_{i-1}&=0 &&(1\le i\le N),\\
 d_i-d_{i-1}&=0 &&(N<i<P),\\
 h_0&=1,\\
 h_i-h_{i-1}&=0 &&(1\le i<P),\\
 q_i+t_i-2h_i&=0 &&(0\le i<P).
\end{aligned}
\tag{2}
\]

Use the public objective

\[
 c^Tx=\sum_{i=0}^{P-1}
 \left[\frac{43}{36}(u_i+v_i)+h_i+t_i\right].
\tag{3}
\]

The matrix has \(3P\) rows and \(4P\) columns.  A transition row has four
nonzeros, a cap row has four, an internal \(h\)-propagation row has two, and
the two anchor rows have one.  Each \(u_i\) or
\(v_i\) column occurs in at most two difference rows and one cap row.  Each
\(h_i\) column occurs in at most two propagation rows and its cap row, and
each \(t_i\) column occurs once.  Thus row sparsity is four and column sparsity
is three.
The largest matrix entry is two, and every input-dependent coefficient is one
of \(\pm1\) and depends on a single \(\sigma_i\).  A sparse value-oracle query
is simulated with at most one sign-oracle query.  The support, \(b\), and
\(c\) are public.

The difference rows have full rank on the \((u,v)\) variables.  The anchored
\(h\)-propagation block has full rank on the \(h\) variables, and the cap rows
then have pivots in the \(t\) variables.  Hence \(A_\sigma\) has full row rank
\(3P\).

Define the prefix products

\[
 \tau_0=1,\qquad
 \tau_i=\prod_{j=1}^i\sigma_j\ (1\le i\le N),\qquad
 \tau_i=\tau_N\ (i>N).
\tag{4}
\]

Exact feasibility is equivalent to

\[
 d_i=\tau_i,\qquad h_i=1,\qquad t_i=2-q_i,qquad 1\le q_i\le2.
\tag{5}
\]

Strict feasibility holds by taking every \(q_i\in(1,2)\).  On the feasible
set, the local objective is

\[
 \frac{43}{36}q_i+1+(2-q_i)=3+\frac7{36}q_i.
\tag{6}
\]

Consequently the unique optimum has \(q_i=1\) at every node.  At each node
exactly one of \(u_i,v_i\) is zero.  The positive reduced cost of that zero
variable is \(7/18\), an absolute constant.  The \(3P\) positive columns are
independent: a null vector is a linear combination of the disjoint vectors

\[
 W_i=\sqrt{\frac23}
 \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right),
\tag{7}
\]

and a nonzero coefficient on \(W_i\) changes the zero member of the pair.
Thus the optimum is primal nondegenerate, dual nondegenerate, and strictly
complementary.  Every feasible primal coordinate lies in \([0,3/2]\).

## 2. A common exact central point and scalar central geometry

Set

\[
                         \mu_1=\frac1{16}.
\tag{8}
\]

At each node define, up to the hidden swap of the first two coordinates,

\[
 x_i^1=\left(\frac98,\frac18,1,\frac34\right),
 \qquad s_i^1=\frac{\mu_1}{x_i^1}
 =\left(\frac1{18},\frac12,\frac1{16},\frac1{12}\right).
\tag{9}
\]

Here the larger pair member is \(u_i\) when \(\tau_i=+1\) and \(v_i\) when
\(\tau_i=-1\).  Feasibility follows from (5).  The only stationarity equation
along the local null direction is

\[
 \frac{7}{36\mu_1}
 =\frac1{q+1}+\frac1{q-1}-\frac1{2-q}.
\tag{10}
\]

At \(q=5/4\), both sides equal \(28/9\).  Hence
\(W^T(c-s^1)=0\), so full row rank gives a unique \(y^1\) with
\(A^Ty^1+s^1=c\).  Therefore (9) is the genuine global \(\mu_1\)-central
point.

For arbitrary \(\mu>0\), the right side of (10) is strictly decreasing from
\(+\infty\) to \(-\infty\) on \((1,2)\).  Its unique solution \(q(\mu)\) is
the same at every node and is independent of the orientation \(\tau_i\).
The vectors (7) are an orthonormal basis of \(\ker A\).  Since all local
central coordinates agree up to swapping \(u,v\),

\[
       W^T\nabla^2 f_\mu(x(\mu))W=\gamma(\mu)I_P
\tag{11}
\]

for a public scalar \(\gamma(\mu)>0\).  Thus the unpreconditioned reduced
central Hessian has condition number exactly one on the whole central path.
At (9), in the convention
\(\nabla^2f_\mu=\mu X^{-2}\),

\[
                         \gamma(\mu_1)=\frac{182}{243}.
\tag{12}
\]

This is not merely a condition-number normalization.  Bounded degree and
bounded entries give

\[
 \|A\|_\infty\le5,\qquad \|A\|_1\le4,
 \qquad \|A\|_2\le\sqrt{20}.
\tag{13}
\]

Thus the usual sparse-access block encoding can use constant normalization.

## 3. One exact Newton correction from public data

At every node use the public start

\[
 x_i^0=\left(\frac56,\frac56,\frac{20}{27},\frac59\right),
 \qquad
 s_i^0=\left(\frac{10}{27},\frac{10}{27},\frac5{12},\frac59\right),
 \qquad y^0=0.
\tag{14}
\]

It is strictly positive, independent of \(\sigma\), and satisfies

\[
             x_j^0s_j^0=\mu_0:=\frac{25}{81}
\tag{15}
\]

in every coordinate.  It is intentionally primal and dual infeasible.  In
the standard infeasible-start system

\[
\begin{aligned}
 A\Delta x&=b-Ax^0,\\
 A^T\Delta y+\Delta s&=c-A^Ty^0-s^0,\\
 S^0\Delta x+X^0\Delta s
   &=\widehat\mu\mathbf1-X^0s^0,
\end{aligned}
\tag{16}
\]

take

\[
                        \widehat\mu=\frac{25}{162}=\frac{\mu_0}{2}.
\tag{17}
\]

All three right-hand sides are public.  In particular \(d_i^0=0\), so hidden
transition signs multiply zero in \(b-Ax^0\).  The primal residual consists
only of fixed public anchor, reference, and cap values.

For either pair orientation and for each of the other two coordinates,
direct substitution gives the common secant identity

\[
                         s_j^0x_j^1+x_j^0s_j^1=\frac{25}{54}.
\tag{18}
\]

Equations (15), (17), and (18) imply

\[
 S^0(x^1-x^0)+X^0(s^1-s^0)
 =\left(\widehat\mu-\mu_0\right)\mathbf1.
\tag{19}
\]

Primal and dual endpoint feasibility supply the other two equations in (16).
The normal matrix is positive definite because \(A\) has full row rank and
\(x^0,s^0>0\).  Therefore the unique Newton correction is

\[
          (\Delta x,\Delta y,\Delta s)
          =(x^1-x^0,y^1-y^0,s^1-s^0),
\tag{20}
\]

and a full step lands exactly at the global central point (9).

The actual reduced Newton matrix at the start is also scalar:

\[
             W^T(X^0)^{-1}S^0W=\frac{22}{27}I_P.
\tag{21}
\]

Thus neither a growing reduced condition number nor block-encoding
normalization explains the state-generation lower bound below.  The hidden
work is the affine feasible translation: solving the signed difference rows
loads all prefix products into the original primal coordinates.

The public start and the public right-hand sides in (16) are repeated
constant-size blocks.  In the standard address/arithmetic circuit model they
can be prepared in \(\operatorname{polylog}P\) gates and with no hidden-sign
queries.  Any setup that queries or stores hidden prefixes is instead charged
to the raw coefficient oracle.

## 4. Linear raw-query lower bounds

### Theorem 1 (bounded-range exact-state separation)

Give the algorithm coherent sparse position/value access to \(A_\sigma\), with
all public data and (14) free.  Count every use of a value oracle or its inverse,
including uses made while constructing advice, QRAM, a block encoding, a
preconditioner, or an affine-offset/recovery oracle.  For the LP (2)--(3):

1. \(A_\sigma\) has constant row and column sparsity, constant entry bound,
   constant sparse block-encoding normalization, and full row rank;
2. its full reduced central Hessian has \(\kappa_{\rm red}=1\) for every
   \(\mu>0\), and its reduced Newton matrix at the public start also has
   condition number one;
3. the unique standard Newton correction (20) lands at the exact central point
   (9); and
4. producing an unconditional state within trace distance \(1/100\) of either
   the normalized primal correction (25) or the normalized central primal
   state requires \(\Omega(N)=\Omega(P)\) raw coefficient queries.

Items 1--3 were proved above.  The next two subsections prove item 4.

### 4.1 Exact Newton-direction state

Up to the hidden pair swap, the primal direction block is

\[
       \Delta x_i=\left(\frac7{24},-\frac{17}{24},
                         \frac7{27},\frac7{36}\right).
\tag{22}
\]

With the first slack coordinate paired with the larger primal coordinate, the
corresponding exact dual-slack direction is

\[
       \Delta s_i=\left(-\frac{17}{54},\frac7{54},
                         -\frac{17}{48},-\frac{17}{36}\right).
\tag{22a}
\]

The squared norm of the primal direction block (22) is

\[
 D=\frac{16139}{23328},
\tag{23}
\]

and the larger-minus-smaller squared pair mass is \(5/12\).  On an output
plateau node, report \(-1\) on measuring its \(u\) coordinate, \(+1\) on
measuring its \(v\) coordinate, and a fair sign on every other outcome.  The
advantage over random guessing on the ideal normalized state is

\[
 \beta_\Delta
 =\frac{K(5/12)}{2DP}
 >\frac14.
\tag{24}
\]

The reported sign equals \(\tau_N=\prod_{i=1}^N\sigma_i\) with that advantage.
Trace distance \(1/100\) reduces it by at most \(1/100\).  Since bounded-error
quantum parity requires \(\Omega(N)\) sign-oracle queries, every algorithm
whose unconditional output is within trace distance \(1/100\) of

\[
                         |\Delta x/\|\Delta x\|_2\rangle
\tag{25}
\]

uses \(\Omega(N)=\Omega(P)\) raw sparse-coefficient queries.  A heralded
contract has the same consequence after charging repetition by its success
probability.

### 4.2 Exact central-point state

Each block in (9) has squared norm \(91/32\), and its oriented pair has
larger-minus-smaller squared mass \(5/4\).  On the plateau, now report \(+1\)
on \(u\), \(-1\) on \(v\), and a fair sign elsewhere.  This decoder has
advantage

\[
                  \beta_{\rm cen}=\frac{20K}{91P}>\frac15.
\tag{26}
\]

Therefore preparing \(|x^1/\|x^1\|_2\rangle\) to trace distance \(1/100\)
also requires \(\Omega(N)=\Omega(P)\) raw coefficient queries.  The same
argument applies to the exact optimum state; this note emphasizes the
central/Newton contracts because approximate feasibility is where the
mixture obstruction applies.

These are input-oracle lower bounds, not gate lower bounds for a supplied
block encoding.  They charge construction of any input-dependent QRAM,
prefix gauge, affine-offset oracle, preconditioner, or recovery map.  If such
a compiled object is supplied for free, it already contains the hard prefix
information and the theorem does not apply.  The equality multiplier \(y^1\)
and its Newton correction are not bounded coordinatewise in this formulation:
the signed-chain dual recurrence can accumulate \(\Theta(P)\).  The theorem is
for the normalized primal central or primal-direction state, not for a
normalized concatenation of \((\Delta x,\Delta y,\Delta s)\), in which the
dual block could dominate.

### 4.3 Full-KKT dead end: unit primal scale becomes dual accumulation

It is tempting to combine the unit-height idea with the full-direction theorem
in
[2026-09-02-linear-plateau-full-kkt-lower-bound.md](2026-09-02-linear-plateau-full-kkt-lower-bound.md).
The resulting calculation is instructive, but it does **not** strengthen that
theorem.  In its LP, set every height and gain to one while retaining the
propagated reference rows, the objective block \((2,2,1,1)\), the public start
\(x^0=s^0=\mathbf1,y^0=0\), and a public centering target
\(\theta\in[0,1]\).  For \(j=0,\ldots,P-1\), the exact direction is

\[
\begin{aligned}
 \Delta x_{u_j}&=\frac{-4+3\tau_j}{6},&
 \Delta x_{v_j}&=\frac{-4-3\tau_j}{6},&
 \Delta x_{h_j}&=0,&
 \Delta x_{t_j}&=\frac13,\\
 \alpha_j&=\frac{\tau_j(P-j)}2,&
 \beta_j&=\frac{(11-9\theta)(P-j)}3,&
 \gamma_j&=\frac43-\theta,&
 \Delta s&=(\theta-1)\mathbf1-\Delta x.
\end{aligned}
\tag{26a}
\]

Here \((\alpha,\beta,\gamma)\) are the multipliers of the difference,
propagated-reference, and cap rows.  The right-hand side remains public:
every hidden coefficient multiplies the zero public difference
\(u_i^0-v_i^0\).  The canonical symmetric three-block KKT matrix and its
two-block elimination both have maximum absolute row and column sum five.
The magnitude-weighted sparse construction therefore gives an exact block
encoding with normalization five; one call or inverse call is simulated by
one hidden-sign query.

The normalized full state is still parity-hard.  On the \(K=16N\) public-copy
suffix put

\[
 A_S=\frac14\sum_{\ell=1}^K\ell^2,
 \qquad r=\frac{\beta_j}{|\alpha_j|}
       =\frac{2(11-9\theta)}3\in\left[\frac43,\frac{22}3\right].
\tag{26b}
\]

The fixed observable that swaps the \(\alpha_j\) and \(\beta_j\) coordinates
on that suffix has signed numerator \(2rA_S\).  Moreover,

\[
 \frac{\sum_j\alpha_j^2}{A_S}
 \le\left(\frac{P}{K}\right)^3
 \le\left(\frac{35}{32}\right)^3,
 \qquad
 \frac{\|\Delta x\|^2+\|\Delta s\|^2+\|\gamma\|^2}{A_S}<\frac14.
\tag{26c}
\]

Consequently its expectation in the normalized full direction has the parity
sign and magnitude at least

\[
 \frac{2r}
 { (35/32)^3(1+r^2)+1/4 }>0.203.
\tag{26d}
\]

Thus this unit-height specialization also gives an \(\Omega(P)\) raw-query,
and hence canonical-block-encoding-query, lower bound for a constant-error
full-direction state.  But it fails the desired bounded-direction property:

\[
 \max_j\{|\alpha_j|,|\beta_j|\}=\Theta(P),
 \qquad \|\Delta y\|_2=\Theta(P^{3/2}),
 \qquad \|\Delta x\|_2+\|\Delta s\|_2=\Theta(\sqrt P).
\tag{26e}
\]

The accumulation is structural for the canonical signed-path rows.  Let
\(B_\sigma d=(d_0,d_1-\sigma_1d_0,\ldots)\).  At any public pair-symmetric
start with common positive pair coordinates \(x_0,s_0\), subtracting the
\(u\)- and \(v\)-dual equations and the corresponding complementarity
equations gives

\[
 B_\sigma^T\alpha=\frac{s_0}{2x_0}\tau,
 \qquad
 \alpha_j=\frac{s_0}{2x_0}\tau_j(P-j).
\tag{26f}
\]

Hence unit primal scale trades the gain-prefix dynamic range for a linearly
accumulating equality multiplier.  Multiplier coordinates depend on row
scaling, so (26f) is a diagnosis of this canonical formulation, not a
representation-invariant impossibility theorem.  It explains why the bounded
primal statement of Theorem 1 does not automatically extend to a bounded
normalized concatenation of all Newton variables.  Since the earlier
full-KKT theorem already proves \(\Omega(P)\) hardness with constant
coefficients and constant block-encoding normalization, (26a)--(26f) are a
dead-end audit rather than a new stronger lower bound.

There is one controlled escape: scaling all dual data by \(1/P\) leaves the
hard primal correction unchanged and suppresses the accumulated multipliers.
It produces a bounded full direction at the price of \(\Theta(1/P)\) slacks
and a canonical full-KKT condition number \(\Omega(P)\); see
[2026-09-02-dual-homogeneity-bounded-full-kkt-lower-bound.md](2026-09-02-dual-homogeneity-bounded-full-kkt-lower-bound.md).

## 5. Why the copy plateau is still necessary here

Let the same construction have an arbitrary plateau length \(K\), so
\(P=N+K+1\).  Let \(\sigma'\) be obtained from \(\sigma\) by flipping only
\(\sigma_N\).  The two inputs have opposite parity.  Their target blocks are
identical before node \(N\), while the pair orientation is swapped at node
\(N\) and on all \(K\) plateau nodes.

For the central block, its squared norm is \(91/32\), its inner product with
the swapped block is \(59/32\), and the difference is exactly one.  Hence

\[
 \left\langle\frac{x^1_\sigma}{\|x^1_\sigma\|},
                  \frac{x^1_{\sigma'}}{\|x^1_{\sigma'}\|}\right\rangle
 =1-\frac{32(K+1)}{91P}.
\tag{27}
\]

For the direction block, the squared norm is \(D\); swapping the first two
coordinates reduces its inner product by
\((7/24+17/24)^2=1\).  Therefore

\[
 \left\langle\frac{\Delta x_\sigma}{\|\Delta x_\sigma\|},
                  \frac{\Delta x_{\sigma'}}{\|\Delta x_{\sigma'}\|}\right\rangle
 =1-\frac{K+1}{DP}.
\tag{28}
\]

For pure states, trace distance is
\(\sqrt{1-|\langle\psi|\phi\rangle|^2}\).  If \(K=o(N)\), (27)--(28) give
trace distance \(o(1)\) even though the parities are opposite.  No measurement
on one constant-error copy can output parity with uniform constant bias on
both inputs: opposite correct answers with bias \(\epsilon\) require output
distributions at total-variation distance at least \(2\epsilon\).

Thus a one-copy parity reduction for this unit-height family needs
\(K=\Omega(N)\).  Conversely, (24) and (26) show that \(K=16N\) suffices.
This is an information-theoretic necessity for this target-state family, not
a universal theorem about all exact central-state encodings.

## 6. A sharp-order robust threshold

The exact-state theorem has a nontrivial robust extension, but only at a
vanishing absolute residual.  No objective, dual, or centrality promise is
needed.

### Theorem 2 (robust state hardness at absolute residual \(N^{-1/2}\))

Let \(x\ge0\) be any nonzero vector for the unrigidified LP (2) satisfying

\[
                       \|A_\sigma x-b\|_2
                       \le \frac1{100\sqrt N}.
\tag{29}
\]

Then the fixed plateau-coordinate measurement described below recovers
\(\tau_N\) from \(|x/\|x\|_2\rangle\) with advantage greater than \(1/15\).
Consequently, any quantum algorithm whose unconditional output is within
trace distance \(1/100\) of the normalized amplitude state of some such
\(x\) uses \(\Omega(N)=\Omega(P)\) raw sparse-coefficient queries.  The same
conclusion holds if the ideal output is any classical mixture of normalized
states of legal vectors satisfying (29).

#### Proof

Write the full residual as \(e=A_\sigma x-b\).  Let \(e_i^d\) denote its
difference-row coordinates, starting with the anchor row.  Define

\[
 r_i=\tau_i d_i.
\]

The anchor and transition equations give the exact telescoping identity

\[
 r_i-1=\sum_{j=0}^i\tau_j e_j^d.
\tag{30}
\]

For every node, including the final plateau node,

\[
 |r_i-1|
 \le\sqrt{i+1}\,\|e^d\|_2
 \le\sqrt P\,\|e\|_2
 \le\frac{\sqrt{18}}{100}<\frac1{20}.
\tag{31}
\]

Here \(P=17N+1\le18N\) for \(N\ge2\).  Thus every output node satisfies the
uniform signed margin

\[
                         \tau_Nd_i=r_i>\frac{19}{20}.
\tag{32}
\]

It remains to ensure that unrelated coordinates cannot swamp this signal in
the normalized state.  Put \(\eta=1/(100\sqrt N)<1/100\).  Let \(e_i^h\)
denote the anchored \(h\)-chain residuals.  They telescope just as the
difference rows do:

\[
 |h_i-1|\le\sum_{j=0}^i|e_j^h|
 \le\sqrt P\,\|e^h\|_2<\frac1{20}.
\tag{33}
\]

Each cap residual coordinate has magnitude at most \(\eta\).  Since \(x\ge0\),

\[
 q_i+t_i\le2h_i+\eta\le\frac{211}{100},
 \qquad h_i<\frac{21}{20}.
\tag{34}
\]

Therefore each four-coordinate block obeys

\[
\begin{aligned}
 u_i^2+v_i^2+h_i^2+t_i^2
 &\le (u_i+v_i+t_i)^2+h_i^2\\
 &=(q_i+t_i)^2+h_i^2<6,
\end{aligned}
\tag{35}
\]

and hence \(\|x\|_2^2<6P\).

On measuring an output node, report \(+1\) on its \(u\) coordinate and
\(-1\) on its \(v\) coordinate; return a fair sign on all other outcomes.
Nonnegativity gives \(q_i=u_i+v_i\ge|d_i|\).  By (32), its signed squared-mass
gap is

\[
 \tau_N(u_i^2-v_i^2)=\tau_Nd_iq_i
 =r_iq_i\ge r_i^2>\left(\frac{19}{20}\right)^2.
\tag{36}
\]

The ideal decoder's advantage over random guessing is consequently at least

\[
 \frac{K(19/20)^2}{2\|x\|_2^2}
 >\frac{361K}{4800P}
 \ge\frac{361\cdot32}{4800\cdot35}
 >\frac1{15},
\tag{37}
\]

where \(K/P=16N/(17N+1)\ge32/35\).  Trace distance \(1/100\) decreases the
advantage by at most \(1/100\), leaving a fixed positive constant.  Applying
the measurement to the algorithm's output therefore computes parity with
bounded error.  The quantum parity lower bound gives \(\Omega(N)\) raw
queries.  Since every legal pure state has the same signed lower bound (36),
the argument is unchanged for a classical mixture of legal amplitude states.
\(\square\)

Only the \(d\)-anchor and \(h\)-anchor entries of the public right-hand side
are nonzero, so

\[
                         \|b\|_2=\sqrt2.
\tag{38}
\]

Thus (29) is a relative-residual requirement of order \(1/\sqrt N\):
explicitly,

\[
 \frac{\|A_\sigma x-b\|_2}{\|b\|_2}
 \le\frac1{100\sqrt{2N}}.
\tag{39}
\]

This is stronger than the constant-relative-residual contracts usually used
for robust QIPM updates.  It is nevertheless the correct asymptotic threshold
for this bounded-height chain.

### 6.1 Accuracy-dependent worst-case curve

The threshold can be inverted into a two-parameter query lower bound. This is
a reparameterization of Theorem 2, not a theorem that one fixed instance
reveals new information at successively finer accuracies.

Let \({\cal F}_{\le P}\) contain all families (2) whose hidden chain has length
\(L\), whose output plateau has length \(16L\), and whose total node count
\(17L+1\) is at most \(P\). The algorithm may choose any nonzero \(x\ge0\) in
the promised residual tube, but must output an unconditional state within trace
distance \(1/100\) of \(|x/\|x\|_2\rangle\).

**Corollary 3 (accuracy curve).** In the nontrivial range where the right side
is larger than an absolute constant,

\[
 Q_{\rm abs}(P,\epsilon)
 =\Omega\!\left(\min\{P,\epsilon^{-2}\}\right)            \tag{C1}
\]

under \(\|Ax-b\|_2\le\epsilon\), and

\[
 Q_{\rm rel}(P,\eta)
 =\Omega\!\left(\min\{P,\eta^{-2}\}\right)               \tag{C2}
\]

under \(\|Ax-b\|_2/\|b\|_2\le\eta\). In particular, for
\(0<\eta\le1\), (C2) implies the weaker proposed curve
\(\Omega(\min\{P,\eta^{-1}\})\).

For (C1), take

\[
 L=\left\lfloor
 \min\left\{\frac{P-1}{17},\frac1{10^4\epsilon^2}\right\}
 \right\rfloor.                                           \tag{C3}
\]

Apart from the irrelevant regime \(L<2\), this is
\(\Theta(\min\{P,\epsilon^{-2}\})\), and
\(\epsilon\le1/(100\sqrt L)\). Theorem 2 gives
\(\Omega(L)\) raw queries.

For (C2), use \(\|b\|_2=\sqrt2\) and take

\[
 L=\left\lfloor
 \min\left\{\frac{P-1}{17},\frac1{2\cdot10^4\eta^2}\right\}
 \right\rfloor.                                           \tag{C4}
\]

Then

\[
 \eta\|b\|_2=\sqrt2\eta\le\frac1{100\sqrt L},          \tag{C5}
\]

so Theorem 2 again applies. This normalization is important: because only the
two anchors contribute to \(b\), the relative exponent is two, not one.

The active instance has \(4(17L+1)\) nonnegative variables and
\(3(17L+1)\) equalities, with row sparsity four and column sparsity three.
Thus replacing node budget \(P\) by scalar-variable dimension \(n\) changes
only constants in (C1)--(C2).

#### Exact-dimension padding without state dilution

The at-most-\(P\) convention is the clean unit-height statement. Naively adding
unit-height public nodes to reach exactly \(P\) is not sound: their normalized
mass can swamp the \(\Theta(L)\) hard plateau. Exact dimension can instead be
obtained with strictly positive small-scale dummy blocks.

Let \(P_h=17L+1\), \(M=P-P_h\), and \(\delta=1/P\). For each dummy node add
\((u,v,h,t)\ge0\), set \(d=u-v\), \(q=u+v\), and impose

\[
 d=0,\qquad h=\delta,\qquad q+t-2h=0,
 \qquad q-\frac54h=0.                                    \tag{C6}
\]

Give these variables the same public positive objective coefficients as in
(3). The padded LP has exactly \(4P\) variables and
\(3P_h+4M\le4P\) independent equalities.

This square block has the unique strictly positive point

\[
                  (u,v,h,t)=\delta(5/8,5/8,1,3/4).       \tag{C7}
\]

In \((d,h,q,t)\) coordinates, the four dummy rows successively pivot on
\(d,h,q,t\).  Their coefficient matrix is nonsingular.  Thus every dummy block
adds four independent rows and four variables, has no null direction, and the
full padded row rank is exactly

\[
 3P_h+4M=4P-P_h<4P.
\]

The padded nullspace is precisely the active nullspace, so every reduced central
or start Newton matrix is unchanged and retains condition number one.  Strict
primal feasibility is preserved because (C7) is positive.  Strict dual
feasibility follows, as before, from \(y=0,s=c>0\).  At the optimum, all four
dummy variables are positive and their four columns form their own basis block;
choosing the unique dummy equality multipliers with zero dummy slacks preserves
strict complementarity and primal-dual nondegeneracy.  Coefficient magnitude and
row/column sparsity remain at most two and four, respectively, and \(\delta\) has
\(O(\log P)\) bits.

The padding is stable for every approximate output. Let \(a,r,c,k\) be the
four dummy residual vectors in the order in (C6), and let \(E\) be the global
residual. From
\(h=\delta\mathbf1+r\), \(q=5h/4+k\),
\(t=3h/4+c-k\), and
\(u^2+v^2=(q^2+d^2)/2\),

\[
 \|x_{\rm dummy}\|_2^2
 \le\frac{17}{4}\|h\|_2^2+\frac12\|a\|_2^2
       +3\|c\|_2^2+4\|k\|_2^2.
\]

Since \(\|h\|_2^2\le2M\delta^2+2\|r\|_2^2\), this gives

\[
 \|x_{\rm dummy}\|_2^2
 \le\frac{17}{2}\left(M\delta^2+E^2\right).              \tag{C8}
\]

At the selected accuracy, \(E\le1/(100\sqrt L)\) and
\(M\delta^2\le1/P\), so (C8) is \(O(1/L)\). It cannot dilute the
\(\Theta(L)\) hard-output mass.  More explicitly, restricting a padded residual
vector to the active rows gives an active residual of norm at most \(E\), so
(36) supplies \(\Theta(L)\) signed plateau mass and the active-coordinate bound
used in (37) is still \(O(L)\).  Adding the dummy norm (C8) changes that
denominator by only \(O(1/L)\), and the decoder retains constant bias. Moreover,

\[
                 \|b_{\rm pad}\|_2^2=2+M/P^2<3.          \tag{C9}
\]

Replacing the constant \(2\cdot10^4\) in (C4) by \(3\cdot10^4\) therefore
proves the same relative curve for exactly \(P\) nodes: a padded relative promise
gives

\[
 E\le\eta\|b_{\rm pad}\|_2<\sqrt3\,\eta
 \le\frac1{100\sqrt L}.
\]

This padding no longer has unit height on every node: its dummy scale is
\(1/P\). If exact dimension and a constant lower scale on all public blocks are
both required, (C8)--(C9) do not apply. The unpadded class-at-most-\(P\) result
remains purely unit height.

Finally, (C1)--(C2) are worst-case family bounds: the hard chain length \(L\)
depends on the requested accuracy. Their exponents are simply the inversion of
the sharp \(L^{-1/2}\) residual threshold proved in Theorem 2 and Section 7.

Theorem 2 also holds verbatim for the rigidified family in Section 7.1: its
residual norm upper-bounds the residual on the base rows used in the proof,
and its right-hand side still has norm \(\sqrt2\).

## 7. Exact failure above the robust threshold

Fix \(\sigma\).  For each \(j\in[N]\), let \(\sigma^{(j)}\) flip bit \(j\),
and let \(x^{(j)}\) be either its exact central point (9) or its exact optimum.
Set

\[
                          \bar x=\frac1N\sum_{j=1}^N x^{(j)}.
\tag{40}
\]

Every neighbor has parity \(-\tau_N\), so all \(K\) output plateau blocks of
\(\bar x\) retain the common opposite orientation.  Nonnegativity and the
common objective value are preserved by averaging.  Evaluated in the base
matrix \(A_\sigma\), the \(j\)-th neighbor violates only transition row \(j\),
by signed magnitude two: after the flipped edge both adjacent prefix values
have changed sign, so all later transition rows telescope exactly.  The \(N\)
violations occupy distinct rows.  Consequently

\[
                 \|A_\sigma\bar x-b\|_2=\frac2{\sqrt N}.
\tag{41}
\]

For the central-point average, the wrong output also remains visible with
constant bias in the normalized amplitude state.  Every averaged block has
squared norm at most \(91/32\), while each of the \(K\) plateau blocks is the
exact opposite-parity central template.  The decoder from Section 4.2
therefore reports \(-\tau_N\) with advantage at least
\(20K/(91P)>1/5\).

Moreover \(\|b\|_2=\sqrt2\), so the relative residual is
\(\sqrt{2/N}=\Theta(N^{-1/2})\).  Thus even a vanishing-residual nonnegative point with the
exact optimal objective can carry the wrong plateau parity.  This explicit
witness explains why Sections 4.1--4.2 must be stated for the designated exact
central/Newton states, not for all approximately feasible or approximately
optimal points.

Equation (41) proves matching-order tightness.  Theorem 2 forces the correct
output at absolute residual \(c/\sqrt N\) for the explicit constant
\(c=1/100\), whereas the single-flip average has the wrong output at residual
\(2/\sqrt N\).  Hence the \(N^{-1/2}\) exponent, in both absolute and relative
residual, cannot be improved under only nonnegativity and a primal-residual
promise.  The constants are not optimized.
The companion note
[2026-09-02-all-unit-relative-residual-threshold.md](2026-09-02-all-unit-relative-residual-threshold.md)
sharpens the recurrence-only constant to the exact cutoff \(1/\sqrt P\), gives
a zero-signal witness at residual \(1/\sqrt N\), and proves a state theorem at
the larger explicit radius \(1/(16\sqrt N)\).  Those refinements are consistent
with the sharp-order claim here.

### 7.1 Rigidification makes dual feasibility and complementarity exact

There is a stronger version of the preceding failure mode.  Add the public
rows

\[
                         u_i+v_i-\frac54h_i=0
                  \qquad(0\le i<N).
\tag{42}
\]

These homogeneous rows rigidify every non-output \(q\)-mode.  They have three
nonzeros, all coefficients have magnitude at most two, and they increase
maximum column sparsity only from three to four.  The augmented matrix obeys

\[
 \|A_{\rm rig}\|_\infty\le5,
 \qquad \|A_{\rm rig}\|_1\le\frac{21}{4},
 \qquad \|A_{\rm rig}\|_2\le\frac{\sqrt{105}}2,
\]

so its sparse block-encoding normalization is still constant.  It remains
full row rank: (42) kills precisely \(W_0,\ldots,W_{N-1}\), so

\[
             \ker A_{\rm rig}=\operatorname{span}
                 \{W_N,\ldots,W_{P-1}\}.
\tag{43}
\]

The exact center (9), the public start (14), the secant identity, and the
Newton lower bound remain valid.  The added primal residual at the public
start is public.  The reduced matrices are still scalar identities, now on
the \(K+1\) output modes.

Apply the neighbor average (40) to exact \(\mu_1\)-centers of this rigidified
family.  At every output node \(i\ge N\), every single-flip neighbor has the
same opposite-parity block.  Hence \(\bar x_i\) there is exactly that block.
On a rigid prefix node, averaging preserves (42); explicitly,

\[
 \bar d_i=\tau_i\left(1-\frac{2i}{N}\right),
 \qquad \bar q_i=\frac54.
\tag{44}
\]

Thus every coordinate of \(\bar x\) is at least \(1/8\).  Define

\[
                         \bar s=\mu_1\bar X^{-1}\mathbf1.
\tag{45}
\]

Complementarity \(\bar X\bar s=\mu_1\mathbf1\) is exact.  Moreover every vector in
the kernel (43) is supported on an output block where \(\bar x\) equals an
exact central block.  Therefore

\[
                   W_{\rm out}^T(c-\bar s)=0.
\tag{46}
\]

Full row rank now gives \(\bar y\) satisfying

\[
                    A_{\rm rig}^T\bar y+\bar s=c.
\tag{47}
\]

Consequently \((\bar x,\bar y,\bar s)\) has exact positivity, exact dual
feasibility, and exact coordinatewise complementarity at \(\mu_1\), while

\[
             \|A_{\rm rig}\bar x-b_{\rm rig}\|_2=\frac2{\sqrt N}
\tag{48}
\]

and its plateau has the wrong parity.  Thus a robust output contract is still
false even if it demands exact dual feasibility and zero complementarity
residual and allows approximation only in primal feasibility.  The new rows
are homogeneous, so \(\|b_{\rm rig}\|_2=\sqrt2\); the relative primal residual
in (48) is \(\sqrt{2/N}=\Theta(N^{-1/2})\), exactly the scale of Theorem 2.

This wrong parity remains visible with constant bias from the normalized
amplitude state of \(\bar x\).  On every prefix block, (44) gives

\[
 \bar u_i^2+\bar v_i^2
 =\frac12\left(\frac{25}{16}+\bar d_i^2\right)
 \le\frac{41}{32}.
\]

Since \(\bar h_i^2+\bar t_i^2=25/16\), each prefix block has squared norm at
most \(91/32\), while each output block has squared norm exactly \(91/32\).
Thus \(\|\bar x\|_2^2\le(91/32)P\).  The fixed decoder from Section 4.2 has
signed squared-mass gap \(5/4\) on each of the \(K\) plateau blocks, now in
the direction \(-\tau_N\).  Its advantage for that wrong parity is at least

\[
 \frac{K(5/4)}{2\|\bar x\|_2^2}
 \ge\frac{20K}{91P}>\frac15
 \qquad(K=16N,\ N\ge2).
\tag{49}
\]

The obstruction therefore survives a normalized-primal-state output contract
tested by this fixed one-copy observable.

The mechanism has a useful general form.  Suppose selected neighboring exact
centers share one \(\mu\), and \(\ker A_\sigma\) has a basis of
input-independent vectors that also belong to every neighboring kernel and
are supported only on coordinates on which all selected centers have a common
template.  Their primal average \(\bar x\), paired with
\(\bar s=\mu/\bar x\), then has exact complementarity.  On each basis
vector's support, \(\bar s\) equals the common exact-center slack; central
stationarity in any neighboring instance therefore gives
\(c-\bar s\perp\ker A_\sigma\), and exact dual feasibility follows.  This
conclusion is not valid without both the common-kernel and common-template
hypotheses, because reciprocation does not commute with averaging.

## 8. Verification and novelty boundary

The identities above were checked symbolically and by direct numerical KKT
assembly for \(N=2,3,7\), using the propagated \(h\)-chain.  In each case
\(\operatorname{rank}A=3P\), the rigidified rank was \(3P+N\), endpoint and
rigidified-mixture dual residuals were below \(2\times10^{-12}\), primal
identities were exact to machine precision, the secant cross terms agreed to
machine precision, and (21) held exactly up to rounding.

The prefix-parity clock, repeated output interval, and quantum parity lower
bound are standard motifs and are not claimed as new.  In particular,
Wang--Zhang,
[*Tight quantum depth lower bound for solving systems of linear
equations*](https://arxiv.org/abs/2407.06012), and Mori et al.,
[*Sparsity-dependent complexity lower bound of quantum linear system
solvers*](https://arxiv.org/abs/2601.16697v2), use sparse propagation/history
systems to prove QLSP lower bounds.  Mori et al.'s constant-error construction
has growing \(\kappa=\Theta(N)\), and both papers specify a square linear
system whose designated solution state must be prepared.  They do not give a
standard-form LP central point, a public infeasible IPM start and exact Newton
secant, or a reduced log-barrier Hessian equal to a scalar identity.
Orsucci--Dunjko,
[*On solving classes of positive-definite quantum linear systems with
quadratically improved runtime in the condition
number*](https://arxiv.org/abs/2101.11868), likewise prove worst-case sparse-
and block-access QLS output-state lower bounds and structured positive
results.  Those theorems do not imply the present LP-native statement.

Nor is the robust statement in Theorem 2 a residual-form restatement of a
QLSP lower bound.  Standard QLSP output guarantees compare a state with the
designated normalized solution of a supplied square system; a small residual
only implies that comparison after charging the relevant inverse singular
value.  Theorem 2 instead quantifies over **every** nonnegative LP vector in a
specified equality-residual tube, without selecting a unique linear-system
solution or assuming a condition bound for the equality operator.  Somma--
Subaşı,
[*Complexity of quantum state verification in the quantum linear systems
problem*](https://arxiv.org/abs/2007.15698), lower-bound verification of
closeness to a designated QLSP solution state.  That is a different promise
and task from generating a state of any vector in this LP feasible tube.
Li's 2026
[*A residual-based quantum linear system algorithm with dynamic stopping and
applications to elliptic PDEs*](https://arxiv.org/abs/2605.06414) gives an
upper-bound and stopping construction for structured elliptic-PDE systems;
it neither proves a worst-case residual-tube output lower bound nor treats
nonnegative LP witnesses.  Thus these sources do not supply the
\(N^{-1/2}\) threshold in Theorem 2.

The distinction is essential: condition one in (11) and (21) refers to the
Newton/log-barrier operator after restriction to an orthonormal basis of
\(\ker A_\sigma\).  The signed equality operator that constructs the affine
feasible translation, and hence the full KKT matrix, need not have constant
condition number.  Therefore Sections 4.1--4.2 are **not** a
constant-\(\kappa\) lower bound in the standard QLSP input model and should
not be described that way.  Their point is that reduced central conditioning,
sparsity, block-encoding normalization of the raw LP matrix, and bounded
primal coordinates do not by themselves pay for affine-offset state
generation.

Existing quantum optimization lower bounds use different output contracts.
Van Apeldoorn et al.,
[*Convex optimization using quantum
oracles*](https://arxiv.org/abs/1809.00643), and Chakrabarti et al.,
[*Quantum algorithms and lower bounds for convex
optimization*](https://arxiv.org/abs/1809.01731), work with membership,
separation, or function-evaluation oracles.  Apers--Gribling, Theorem 8.4 of
[*Quantum speedups for linear programming via interior point
methods*](https://arxiv.org/abs/2311.03215v3), lower-bound additive optimal-
value approximation for sparse LP data while their algorithms return an
explicit feasible approximate point.  None of these results asks for one
amplitude state of the designated exact central point or first Newton
direction.  Conversely, the present theorem gives no lower bound for their
approximate-value or arbitrary-feasible-point contracts.

The QIPM/QCPM literature is also on the upper-bound side of this boundary.
Kerenidis--Prakash,
[*A quantum interior point method for LPs and
SDPs*](https://arxiv.org/abs/1808.09266), and later inexact QIPMs solve Newton
systems approximately and use tomography to make classical updates.
Augustino et al.,
[*A quantum central path algorithm for linear
optimization*](https://arxiv.org/abs/2311.03977), measure a continuous
ground-state distribution to return classical primal--dual vectors.  These
are not exact amplitude-encoded-primal-state contracts and contain no
matching raw-coefficient lower bound.

The exact secant here is inherited from the earlier local construction cited
above.  The useful apparently new statement is the sharp-residual-scale
resource dichotomy:

1. exact designated central and Newton states can be linearly query-hard with
   bounded LP data, bounded primal range, constant block-encoding
   normalization, and globally condition-one reduced geometry;
2. every nonnegative point at absolute residual \(1/(100\sqrt N)\) still has
   a uniform correct-output amplitude margin and therefore the same linear
   state-preparation lower bound;
3. the family admits an opposite-output point at residual \(2/\sqrt N\),
   exactly as the convex-mixture theorem predicts, so the exponent
   \(N^{-1/2}\) is tight up to constants for this family and output
   observable; after homogeneous rigidification the same point has exact
   dual feasibility and exact coordinatewise complementarity; and
4. constant distinguishability still requires a linear bounded-height copy
   plateau, but no growing coefficient or coordinate magnitude.

The neighbor-average statement in Section 7 is also narrower than a generic
robust-optimization or inexact-IPM fact.  Its specific content is an explicit
bounded-degree LP witness whose nonnegative primal vector has the wrong
plateau output and residual exactly \(2/\sqrt N\); after rigidification it can
simultaneously be paired with exact dual feasibility and exact
\(\bar X\bar s=\mu_1\mathbf1\).  The averaging mechanism is an application of
convexity and local single-bit changes, not a new convexity principle.  No
primary source found in the targeted search states this exact LP/QIPM
conjunction.  This is evidence of apparent novelty, not proof of priority.

The theorem should therefore be advertised as a sharp-residual-scale
amplitude-state oracle separation, not as a general lower bound on solving the
LP, recovering only reduced coordinates, producing points at larger residual,
or solving a supplied constant-condition full KKT system.
