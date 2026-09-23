# Linear-size Newton-state hardness with an exactly condition-one reduced path

Date: 2026-09-02

## Main theorem

There is a fixed-pattern standard-form LP family with \(P=17N+1\) nodes,
\(4P\) nonnegative variables, and \(3P+O(\log N)\) independent equalities
such that:

1. every constraint coefficient has magnitude at most two, and row and column
   sparsity are at most four;
2. the family is bounded, strictly primal-dual feasible, and has a unique,
   nondegenerate, strictly complementary optimum;
3. the complete reduced primal log-barrier Hessian has condition number
   **exactly one at every point of the central path**;
4. a sign-independent, strictly positive, complementarity-centered infeasible
   start has one exact standard Newton correction whose full endpoint is the
   genuine global \(\mu_1=1/16\) central point;
5. the reduced Newton matrix at that start also has condition number exactly
   one; but
6. preparing the normalized original-primal Newton direction to trace error
   \(1/100\) requires \(\Omega(N)=\Omega(P)\) raw sparse coefficient queries.

Moreover, the robust theorem from the underlying gain--plateau family remains
true: preparing a state of any nonnegative point with relative equality
residual at most \(1/100\) costs \(\Omega(P)\), with no objective or centrality
promise. The same linear lower bound holds for the normalized state of any
approximate direction whose full-step update is nonnegative and has that
residual.

The construction removes the last \(O(\log N)\) curvature outliers from
`2026-09-02-exact-central-plateau-newton-direction.md`.  It does so by adding
one public equality at each small-scale gain-prefix node.  These rows eliminate
the corresponding local null directions; they do not reveal or constrain the
hidden parity orientation.

## 1. Construction

Start with the feasible set in
`2026-09-02-linear-size-robust-gain-parity-lp.md`.  Write

\[
 T=\left\lceil\frac12\log_2N\right\rceil,
 \qquad H_i=2^{\min\{i,T\}},\qquad H=2^T,
\]

and use \(K=16N\) output-copy nodes, so \(P=N+K+1=17N+1\).
At node \(i\), put

\[
 d_i=u_i-v_i,\qquad q_i=u_i+v_i.
\]

The original equalities are

\[
\begin{aligned}
 d_0&=1,&d_i-g_i a_i d_{i-1}&=0,\\
 h_0&=1,&h_i-g_i h_{i-1}&=0,\\
 &&q_i+t_i-2h_i&=0,
\end{aligned}
\tag{1}
\]

where \(g_i=H_i/H_{i-1}\in\{1,2\}\), the first \(N\) labels are
\(a_i=\sigma_i\), and all later labels are one.  Thus exact feasibility fixes

\[
 d_i=H_i\tau_i,\qquad h_i=H_i,
\tag{2}
\]

with \(\tau_i\) the corresponding prefix product.

For each of the \(T\) nodes \(i<T\), add the **public rigidification row**

\[
 q_i-\frac54h_i=0.
\tag{3}
\]

Use the uniform public objective

\[
 \min\sum_i\left[(1+w)(u_i+v_i)+h_i+t_i\right],
 \qquad w=\frac7{36H}.
\tag{4}
\]

Only the two previous-node entries in a signed propagation row depend on the
input, and both contain the same one-bit label \(a_i\).  No other coefficient
depends on the input.
The rational numbers \(5/4\) and \(w\) have \(O(\log N)\)-bit exact
representations.

### Size, sparsity, and rank

The old matrix has \(3P\) independent rows and the public orthonormal null
basis

\[
 W_i=\sqrt{\frac23}
 \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right),
 \qquad 0\le i<P.
\tag{5}
\]

If \(r_i\) denotes row (3), then
\(r_i^TW_j=\sqrt{2/3}\,\delta_{ij}\).  Hence the \(T\) new rows are
independent modulo
the old row space.  The augmented matrix \(A'\) has full row rank \(3P+T\),
and

\[
             \ker A'=\operatorname{span}\{W_i:i\ge T\}.
\tag{6}
\]

The new rows have three nonzeros.  An internal prefix \(u,v\), or \(h\)
column occurs in at most two propagation rows, one cap row, and one
rigidification row.  Thus both row and column sparsity remain at most four,
and every constraint coefficient has magnitude at most two.

## 2. Regularity

On each prefix node, (3) fixes \(q_i=5H_i/4\).  On every free node \(i\ge T\),
the feasible interval is \(H\le q_i\le2H\), and the local objective equals

\[
                 wq_i+3H.
\tag{7}
\]

Thus the unique optimum has

\[
 q_i^*=\frac54H_i\quad(i<T),
 \qquad q_i^*=H\quad(i\ge T).
\tag{8}
\]

Every prefix coordinate is then positive.  At each free node exactly one of
\(u_i,v_i\) is zero, according to \(\tau_i\), and its reduced cost is
\(2w=7/(18H)>0\).  There are exactly \(3P+T\) positive optimal variables.
If a null vector is supported on those variables, (6) expresses it as a
combination of free-node \(W_i\)'s, but each such \(W_i\) has a nonzero entry
on that node's zero pair coordinate.  Hence the combination vanishes.  The
positive columns therefore form a nonsingular basis.  This proves primal
nondegeneracy; the positive nonbasic reduced costs and full row rank give dual
nondegeneracy and strict complementarity.

Here “nondegenerate” has the standard-form/simplex meaning: all variables in
the positive \(3P+T\)-column basis are strictly positive, and every nonbasic
reduced cost is strictly positive.  Equivalently, the active dual constraints
are independent and the complementary nonbasic slacks are positive.  The
property holds for each fixed \(N\), but its numerical margin is not uniform:
\(2w=\Theta(N^{-1/2})\).  If a source uses a different conic
nondegeneracy convention, the preceding basis and reduced-cost statements are
the invariant claims.

Choosing \(q_i=5H_i/4\) on every node gives a strictly positive primal point.
The central construction below gives strictly positive dual slacks, so strict
primal-dual feasibility holds.  The caps make the feasible region bounded.

## 3. The entire reduced central path is scalar

All free nodes have the same height \(H\) and objective slope \(w\).  Write

\[
 q_i=H+z(\mu),\qquad i\ge T.
\]

The central stationarity equation is

\[
 \frac{w}{\mu}
 =\frac1{2H+z}+\frac1z-\frac1{H-z}.
\tag{9}
\]

Its right-hand side is continuous and strictly decreasing from \(+\infty\)
to \(-\infty\) as \(z\) runs from \(0\) to \(H\).  It therefore has one
solution in the strictly feasible interval for every \(\mu>0\),
and that solution is identical at every free node.  Prefix coordinates are
fixed by the equalities and contribute no reduced direction.  Therefore, in
the orthonormal basis (6), the reduced Hessian is

\[
 W^T\nabla^2 f_\mu(x(\mu))W=\lambda(\mu)I_{P-T}
\tag{10}
\]

for every \(\mu>0\).  In particular,

\[
 \boxed{\kappa=1\text{ along the complete central path}.}
\tag{11}
\]

This is the unscaled Hessian in the original bounded-coefficient formulation;
no preconditioner or deflation is being hidden.

At \(\mu_1=1/16\), equation (9) has the exact solution \(z=H/4\), because

\[
 \frac1{2H+H/4}+\frac1{H/4}-\frac1{H-H/4}
 =\frac{28}{9H}=\frac{w}{\mu_1}.
\]

Thus the global central primal point, up to the hidden pair swap, is

\[
 x_i^1=H_i\left(\frac98,\frac18,1,\frac34\right)
 \quad(i<T),
 \qquad
 x_i^1=H\left(\frac98,\frac18,1,\frac34\right)
 \quad(i\ge T).
\tag{12}
\]

In other words, the same formula holds with \(H_i\) at every node.  Put
\(s_j^1=\mu_1/x_j^1\).  On the only null directions, those with \(i\ge T\),
equation (9) is exactly \(W^T(c-s^1)=0\).  Equation (6) and full row rank then
give a unique \(y^1\) with

\[
                  (A')^Ty^1+s^1=c.
\tag{13}
\]

Hence (12)--(13) are the genuine common-\(\mu_1\) primal-dual central point.

## 4. One exact Newton correction from a public start

Use the sign-independent start

\[
 x_i^0=H_i\left(\frac56,\frac56,\frac{20}{27},\frac59\right),
 \qquad
 s_i^0=H_i^{-1}\left(\frac{10}{27},\frac{10}{27},
                              \frac5{12},\frac59\right),
 \qquad y^0=0.
\tag{14}
\]

It is strictly positive and

\[
 x_j^0s_j^0=\mu_0:=\frac{25}{81}
\tag{15}
\]

for every coordinate.  It need not be primal or dual feasible; it is a public
complementarity-centered infeasible start.

The associated Newton right-hand sides are public too.  At (14), every signed
difference is zero, so the hidden propagation coefficients multiply zero in
the primal residual.  The reference, cap, and new rigidification residuals
depend only on the public heights.  Since \(y^0=0\), the dual residual is
\(c-s^0\), and (15) fixes the complementarity residual.  Thus only \(A'\), not
the start or any supplied right-hand side, contains the hidden signs.

Let

\[
 \widehat\mu=\frac{25}{162}=\frac{\mu_0}{2}.
\tag{16}
\]

Because \(\mu_0=(x^0)^Ts^0/(4P)\), this is the usual centering target
\(\widehat\mu=\sigma\mu_0\) with \(\sigma=1/2\).  Explicitly, the standard
infeasible-start primal--dual Newton system used here is

\[
\begin{aligned}
 A'\Delta x&=b'-A'x^0,\\
 (A')^T\Delta y+\Delta s&=c-(A')^Ty^0-s^0,\\
 S^0\Delta x+X^0\Delta s
   &=\widehat\mu\mathbf1-X^0s^0 .
\end{aligned}
\tag{15a}
\]

Exactly as in the audited secant calculation of
`2026-09-02-exact-central-plateau-newton-direction.md`, every coordinate obeys

\[
 s_j^0x_j^1+x_j^0s_j^1=\frac{25}{54}.
\tag{17}
\]

Consequently

\[
 S^0(x^1-x^0)+X^0(s^1-s^0)
 =\left(\widehat\mu-\mu_0\right)\mathbf1.
\tag{18}
\]

Endpoint feasibility supplies the first two equations in (15a), and (18)
supplies the third.  Since
\(A'\) has full row rank and \(x^0,s^0>0\), the usual normal matrix is positive
definite.  We have proved:

### Theorem 1 (exact finite Newton secant)

The unique standard infeasible-start Newton correction at (14), with centering
target \(\widehat\mu=\mu_0/2\), is

\[
 (\Delta x,\Delta y,\Delta s)
 =(x^1-x^0,y^1-y^0,s^1-s^0).
\tag{19}
\]

The full step is positive and lands exactly at the global \(\mu_1=1/16\)
central point.  This is an exact algebraic full Newton step, not a claim that a
particular merit-function or neighborhood line search must accept step length
one.  The endpoint parameter \(\mu_1\) differs from the linearized target
\(\widehat\mu\) because the Newton equation omits the quadratic term
\(\Delta X\Delta s\).

The ordinary fraction-to-boundary test does permit the full step.  From
(12), (14), and the corresponding slacks, the largest step preserving
nonnegativity in both primal and slack coordinates is exactly

\[
                    \alpha_{\max}=\frac{20}{17}>1.
\tag{19a}
\]

Thus any fraction-to-boundary rule with safety factor at least \(17/20\)
allows \(\alpha=1\), and the endpoint passes every exact central-neighborhood
test.  A separate merit-function sufficient-decrease rule is algorithm
dependent and is not asserted here.

The reduced primal Newton matrix at the start is also scalar.  For every
free-node basis vector (5),

\[
 W_i^T(X^0)^{-1}S^0W_i=\frac{22}{27H^2},
\tag{20}
\]

so its reduced condition number is exactly one.

### 4.1 The raw OSS and augmented KKT matrices are not condition one

The condition-one result above is genuinely a reduced-primal statement.  It
does not extend to the usual unpreconditioned full systems.

First consider the OSS coefficient matrix at the public start,
\[
 {\cal M}_0=[-X^0(A')^T\ \ S^0W].
\tag{20a}
\]
For an infeasible start one must first choose a particular primal feasibility
correction and shift the OSS right-hand side; this does not change the
coefficient matrix (20a).  At any free plateau node, the column associated
with its cap equality obeys
\[
 \|X^0(A')^Te_{\rm cap}\|_2^2
 =\frac{5675}{1458}H^2.
\]
The column associated with its local null vector obeys
\[
 \|S^0W_i\|_2^2=\frac{550}{2187H^2}.
\]
The largest singular value is at least the norm of the first column and the
smallest singular value is at most the norm of the second.  Therefore
\[
 \boxed{\kappa_2({\cal M}_0)
 \ge \sqrt{\frac{681}{44}}\,H^2=\Omega(P).}
\tag{20b}
\]
This elementary scale separation already rules out a raw OSS
condition-\(O(1)\) strengthening.  The signed propagation path can worsen
conditioning, but is not needed for (20b).

The same issue appears in the canonical eliminated augmented KKT matrix
\[
 {\cal K}_0=
 \begin{bmatrix}
  -(X^0)^{-1}S^0&(A')^T\\
  A'&0
 \end{bmatrix}.
\tag{20c}
\]
For a free-node unit vector \(W_i\),
\[
 \left\|{\cal K}_0\binom{W_i}{0}\right\|_2^2
 =\frac{178}{243H^4},
\]
whereas a cap-multiplier unit vector has image norm \(\sqrt7\).
Consequently
\[
 \boxed{\kappa_2({\cal K}_0)
 \ge\sqrt{\frac{1701}{178}}\,H^2=\Omega(P).}
\tag{20d}
\]
Thus neither the OSS nor this standard KKT formulation inherits the raw
condition-one reduced geometry.

For completeness, the completely uneliminated three-block Newton matrix,
with row blocks ordered as primal feasibility, dual feasibility, and
complementarity, is
\[
 {\cal J}_0=
 \begin{bmatrix}
  A'&0&0\\
  0&(A')^T&I\\
  S^0&0&X^0
 \end{bmatrix}.
\tag{20d'}
\]
Taking
\((\Delta x,\Delta y,\Delta s)=(W_i,0,-(X^0)^{-1}S^0W_i)\)
leaves only the dual-feasibility output
\(-(X^0)^{-1}S^0W_i\), of norm
\(\sqrt{178/243}\,H^{-2}\).  On the other hand, a unit
\(\Delta s_h\) column at a plateau node has image norm at least
\((20/27)H\).  Hence
\[
 \kappa_2({\cal J}_0)
 \ge \frac{20}{27}\sqrt{\frac{243}{178}}\,H^3.
\tag{20d''}
\]
This stronger raw bound is not invariant under eliminating or rescaling
Newton equations, which is why (20d), rather than (20d''), is the cleaner
augmented-KKT comparison.

Exact full-system preconditioning is possible algebraically.  At the
complementarity-centered start, the two OSS column blocks are orthogonal:
\[
 (X^0(A')^T)^T(S^0W)=A'X^0S^0W=\mu_0A'W=0.
\]
Right-preconditioning them by
\[
 R_y=(A'(X^0)^2(A')^T)^{-1/2},\qquad
 R_\lambda=(W^T(S^0)^2W)^{-1/2}
\tag{20e}
\]
makes \({\cal M}_0\operatorname{diag}(R_y,R_\lambda)\) orthogonal and hence
condition one.  Similarly, put
\[
 D_0=(X^0)^{-1}S^0,\qquad G_0=A'D_0^{-1}(A')^T.
\]
Symmetric block preconditioning of (20c) by
\(\operatorname{diag}(D_0^{-1/2},G_0^{-1/2})\) gives
\[
 \begin{bmatrix}-I&B^T\\B&0\end{bmatrix},
 \qquad B=G_0^{-1/2}A'D_0^{-1/2},\qquad BB^T=I.
\tag{20f}
\]
Its condition number is exactly
\(\varphi^2=(3+\sqrt5)/2\).  These are existence statements, not efficient
raw-oracle preconditioners.

Indeed, the difficult factor in (20e) or (20f) is data-dependent and dense.
At the public start the difference-row block decouples from the symmetric
pair, reference, cap, and rigidification blocks.  If
\(R_\tau=\operatorname{diag}(\tau_i)\) is the prefix-sign gauge, its Schur
block has the form
\[
 G_\sigma^{(d)}=R_\tau G_+^{(d)}R_\tau,\qquad
 (G_\sigma^{(d)})^{-1/2}
 =R_\tau(G_+^{(d)})^{-1/2}R_\tau.
\tag{20g}
\]
The all-positive block \(G_+^{(d)}\) is an irreducible tridiagonal Stieltjes
matrix.  Its inverse square root is entrywise strictly positive, for example
from
\[
 G^{-1/2}=\frac2\pi\int_0^\infty(G+t^2I)^{-1}\,dt
\]
and strict positivity of the inverse of an irreducible Stieltjes matrix.
Hence an exact, or sign-resolving, entry-value oracle for
the \((0,j)\) preconditioner entry reveals \(\tau_j\), and an output-copy
entry reveals the final parity.  Such an oracle cannot be granted for free
in the raw coefficient-query model.  A block encoding without entry access
needs a separate quantitative implementation analysis, so no one-query
claim is made for that interface.

The correct strengthened conclusion is therefore:

- the reduced primal Newton solve is raw condition one;
- the raw full OSS and augmented KKT systems have condition
  \(\Omega(P)\);
- ideal full-system preconditioning reduces their condition to one or
  \(\varphi^2\), but moves the hard prefix computation into preconditioner
  construction/application, transformed-RHS preparation, or recovery.

## 5. Direction-state lower bound

At every node, up to the hidden pair swap,

\[
 \Delta x_i=H_i\left(\frac7{24},-\frac{17}{24},
                            \frac7{27},\frac7{36}\right).
\tag{21}
\]

Its squared norm is \(DH_i^2\), where

\[
 D=\frac{16139}{23328},
\]

and the correct-minus-incorrect squared pair signal is \((5/12)H_i^2\).
On the \(K=16N\) output nodes, use the fixed decoder that reports \(-1\) on a
measured \(u\)-coordinate, \(+1\) on a measured \(v\)-coordinate, and a fair
sign elsewhere.  Since

\[
 \sum_iH_i^2<\left(17N+\frac43\right)H^2,
\]

its ideal bias is larger than

\[
 \frac{16N(5/12)}{2D(17N+4/3)}>\frac14
 \qquad(N\ge2).
\tag{22}
\]

### Theorem 2 (condition-one Newton-state hardness)

Any quantum algorithm whose unconditional output is within trace distance
\(1/100\) of

\[
                 |\Delta x/\|\Delta x\|_2\rangle
\tag{23}
\]

makes \(\Omega(N)=\Omega(P)\) raw sparse coefficient queries.  The same holds
for a fixed-probability heralded branch after repetition is charged.

The decoder in (22) retains constant parity bias after the promised trace
error.  Each sparse row, column, position, value, or objective query to the
LP is simulated by at most one hidden-sign query; all new rows and objective
coefficients are public.  Bounded-error quantum parity needs \(\Omega(N)\)
queries.

This is an end-to-end loading/recovery lower bound, not a condition-number
lower bound: the exact reduced solve at the public start is scalar, but the
original-coordinate Newton direction contains the hidden affine translation.
Arbitrary preprocessing, preconditioning, RHS formation, solve, and recovery
are covered when every input-dependent primitive is expanded into raw
coefficient queries.  Free input-dependent advice or a free oracle for the
hidden feasible offset would change the model.

## 6. Robust approximate-feasibility corollary

Let \(b'\) be the augmented RHS.  Every new row has zero RHS, so
\(\|b'\|_2=\sqrt2\), exactly as in the base gain--plateau family.  If
\(x\ge0\), \(x\ne0\), and

\[
 \frac{\|A'x-b'\|_2}{\|b'\|_2}\le\frac1{100},
\tag{24}
\]

then deleting the new residual coordinates gives the same bound for the old
system.  The robust decoder theorem in
`2026-09-02-linear-size-robust-gain-parity-lp.md` applies unchanged.
Therefore preparing a state within trace distance \(1/100\) of
\(|x/\|x\|_2\rangle\) also requires \(\Omega(P)\) coefficient queries, with
no objective, dual, or neighborhood promise.

In particular, exact original-primal central-state preparation is linearly
hard at every prescribed \(\mu>0\), despite (11).  This separates the reduced
barrier geometry from the affine-feasible-offset and original-coordinate
loading tasks as strongly as this family permits.

### Theorem 3 (robust approximate-direction state is linearly hard)

Let an algorithm output an unconditional density operator \(\rho\). Suppose
there is a nonzero direction \(\widetilde{\Delta x}\) whose full-step update

\[
 \widetilde x=x^0+\widetilde{\Delta x}\ge0
\]

satisfies

\[
 \frac{\|A'\widetilde x-b'\|_2}{\|b'\|_2}\le\frac1{100},
 \qquad
 D_{\rm tr}\!\left(\rho,
 |\widetilde{\Delta x}/\|\widetilde{\Delta x}\|_2\rangle
 \langle\widetilde{\Delta x}/\|\widetilde{\Delta x}\|_2|\right)
 \le\frac1{100}.                                       \tag{25}
\]

Then the algorithm makes \(\Omega(N)=\Omega(P)\) raw sparse coefficient
queries.

#### Proof

Deleting the rigidification residual coordinates gives the base gain--plateau
residual bound with the same constant, because \(\|b'\|_2=\sqrt2\). On every
height-\(H\) node, the base robust estimates therefore give

\[
 \tau_i\widetilde d_i>\frac{37}{40}H,\qquad
 \frac{37}{40}H<\widetilde h_i<\frac{43}{40}H,\qquad
 \widetilde q_i,\widetilde t_i<\frac{433}{200}H.        \tag{26}
\]

At the public start (14),

\[
 d_i^0=0,\qquad q_i^0=\frac53H,\qquad
 h_i^0=\frac{20}{27}H,\qquad t_i^0=\frac59H.            \tag{27}
\]

Nonnegativity gives \(\widetilde q_i\ge|\widetilde d_i|\). Consequently,

\[
 |\widetilde q_i-q_i^0|<\frac{89}{120}H,
 \qquad
 \frac{199}{1080}H<\widetilde{\Delta h}_i
 <\frac{361}{1080}H,
 \qquad
 |\widetilde{\Delta t}_i|<\frac{29}{18}H.              \tag{28}
\]

Since

\[
 \widetilde{\Delta u}_i^2+\widetilde{\Delta v}_i^2
 =\frac{(\widetilde q_i-q_i^0)^2+\widetilde d_i^2}{2},
\]

the squared direction norm on each height-\(H\) node is less than

\[
 \frac12\left[\left(\frac{89}{120}\right)^2
              +\left(\frac{433}{200}\right)^2\right]
 +\left(\frac{361}{1080}\right)^2
 +\left(\frac{29}{18}\right)^2
 <\frac{16}{3}.                                        \tag{29}
\]

For the \(i<T\) prefix, the base estimate
\(\|\widetilde x_i\|_2^2<11H_i^2\), the public bound
\(\|x_i^0\|_2^2<9H_i^2/4\), and
\(\|a-b\|^2\le2\|a\|^2+2\|b\|^2\) suffice. Using
\(\sum_{i<T}H_i^2<H^2/3\) and \(P=17N+1\),

\[
 \|\widetilde{\Delta x}\|_2^2
 <\frac{16}{3}PH^2+\frac{53}{6}H^2<100NH^2
 \qquad(N\ge2).                                        \tag{30}
\]

For an output node put

\[
 |g_i\rangle=\frac{|u_i\rangle-|v_i\rangle}{\sqrt2},
 \qquad
 O=\bigoplus_{i\in S}
 (|h_i\rangle\langle g_i|+|g_i\rangle\langle h_i|).
\tag{31}
\]

This observable is fixed, input-independent, and has norm one. Since
\(|S|=16N\) and \(\tau_i=p_N\) on \(S\), (26), (28), and (30) give

\[
 p_N\langle\widetilde{\Delta x}/\|\widetilde{\Delta x}\||O|
 \widetilde{\Delta x}/\|\widetilde{\Delta x}\|\rangle
 =\frac{\sqrt2\sum_{i\in S}\widetilde{\Delta h}_i
                    \widetilde d_i}
        {\|\widetilde{\Delta x}\|_2^2}
 >\frac{7363\sqrt2}{270000}>\frac1{27}.                \tag{32}
\]

The two-outcome POVM \((I\pm O)/2\) guesses parity with ideal bias greater
than \(1/54\). Trace error \(1/100\) leaves positive constant bias. Repetition,
the one-sign-query simulation of every LP query, and the quantum parity lower
bound prove the theorem. \(\square\)

Theorems 2 and 3 permit arbitrary mixed unconditional output. For either theorem,
a heralded implementation using \(Q\) queries per trial and succeeding with probability \(p\) obeys
\(Q/p=\Omega(N)\); in particular, fixed success probability gives the displayed
lower bound. Free postselection is outside the model. The trace premise may also
be replaced by squared fidelity at least \(9999/10000\).

The nonnegative-update condition is necessary for a fixed residual theorem. Let
\(w=\sum_{i\in S}W_i\), so \(A'w=0\) and \(w\) is public. In the full Newton
system, add

\[
 e_x=Mw,\qquad e_y=0,\qquad e_s=-(X^0)^{-1}S^0e_x.
\tag{33}
\]

Only the dual residual changes. On \(S\),
\(\|(X^0)^{-1}S^0w\|\le H^{-2}\|w\|\), while the cap block of the public Newton
right-hand side has norm at least \((20/27)H\sqrt{|S|}\). Choosing \(M=H^2\)
makes the relative full-Newton residual \(O(H^{-1})\) and makes the normalized
primal direction \(\Delta x+Mw\) approach the zero-query public state
\(|w/\|w\|\rangle\). The perturbation drives updated \(t\)-coordinates negative,
so it does not contradict Theorem 3. Thus residual accuracy alone, even for the
full KKT/Newton equations, cannot replace the geometric full-step condition.

## 7. Adaptive preprocessing and multi-iteration accounting

The lower bounds above survive arbitrary preprocessing and reuse across Newton
iterations, but only as a **total** linear bound. They do not multiply by the
number of iterations.

### Corollary 3 (tight adaptive total-query law)

Use the standard hidden-sign oracle, or the fixed-position sparse LP oracle for
\(A',b',c\), with calls to the oracle and its inverse charged equally. Consider
an arbitrary interactive algorithm that:

1. begins with any input-independent classical or quantum advice;
2. performs data-dependent preprocessing and retains unlimited persistent
   classical or quantum workspace;
3. makes any finite, possibly adaptive number \(R\) of Newton, correction,
   refinement, preconditioning, or recovery calls, with intermediate
   measurements and classical control; and
4. implements every input-dependent primitive from the raw coefficient oracle,
   charging every underlying raw call.

Let its worst-case raw-query ledger be

\[
 Q_{\rm prep}+\sum_{t=1}^R
 \bigl(Q_{{\rm form},t}+Q_{{\rm solve},t}+Q_{{\rm recover},t}\bigr)
 +Q_{\rm out}.                                             \tag{A1}
\]

If its final unconditional output is within trace distance \(1/100\) of the
normalized state of any nonzero \(x\ge0\) satisfying (24), then

\[
 Q_{\rm prep}+\sum_{t=1}^R
 \bigl(Q_{{\rm form},t}+Q_{{\rm solve},t}+Q_{{\rm recover},t}\bigr)
 +Q_{\rm out}=\Omega(N)=\Omega(P).                        \tag{A2}
\]

The same bound holds if the final output is the exact original-primal central
state at any fixed or adaptively selected \(\mu>0\), or the normalized
original-coordinate Newton direction (23) for the public start (14). It also
holds for the robust approximate-direction contract (25).

#### Proof

Treat preprocessing, persistent advice, every adaptive phase, and output
formation as one quantum query algorithm. Intermediate measurements may be
purified and deferred and do not affect the total query count. For a final
robust primal state, compose the algorithm with the fixed decoder inherited in
Section 6. For the exact Newton-direction contract, use the decoder (22); for
the robust approximate direction, use the observable decoder (31)--(32). In
every case the composition computes parity with fixed positive bias. Constant
repetition gives standard bounded error with only a constant-factor increase in
(A1). Each sparse LP query is coherently simulated by at most one hidden-sign
query, so quantum parity gives (A2). Exact central states are feasible and hence
are included in (24). No round-independence or fresh-information assumption is
used. \(\square\)

A data-dependent preconditioner, feasible-offset table, compiled block encoding,
or state-preparation circuit is covered when its construction queries the raw
oracle and those setup queries are included in \(Q_{\rm prep}\). Persistent
reusable advice is allowed. If advice is consumed, all queries needed to prepare
the consumed copies must be included in setup or in the consuming phase; it
cannot be cloned for free. By contrast, separately supplying an arbitrary
input-dependent advice state, a hidden feasible-offset oracle, or an
original-primal central-state oracle changes the input model and defeats this
reduction.

### Proposition 4 (static-oracle ceiling)

For this fixed family, all raw coefficient dependence can be cached with exactly
\(N\) sign queries. Query every \(\sigma_i\), compute and store all prefix products
\(\tau_i\), and thereafter answer every sparse coefficient lookup locally. Hence,
for any finite or adaptively chosen number of iterations,

\[
                         Q_{\rm total}=O(N)=O(P).          \tag{A3}
\]

After caching, the algorithm knows the full affine offset (2). The heights,
rigidification rows, objective, null basis (6), scalar central equation (9), and
the reduced Newton matrices are already public. Since arithmetic, circuit size,
and memory access are free in the raw-query model, the cached data suffice to
prepare any desired original-primal central state, the direction (21), or the
exact optimum without further raw queries. They also suffice to simulate every
later raw-oracle call made by an arbitrary QIPM.

Corollary 3 and Proposition 4 prove a tight \(\Theta(P)\) total raw-query law for
either hard final-output contract. In particular, no \(\Omega(RP)\) lower bound
is possible for one fixed instance of this family. Charging setup only once gives
at most the unconditional average consequence \(\Omega(P/R)\) per phase. A true
per-iteration direct sum would require fresh online inputs after committed
outputs, a memory restriction preventing caching, or another charged resource
such as gates, communication, QRAM construction, or consumable advice copies.

The output qualification is essential. Rigidification leaves the null basis and
all reduced central geometry input-independent. Thus a service asked only for
reduced central coordinates, reduced Newton directions, or the known scalar
objective may answer without learning any hidden sign. The linear lower bound is
for recovery/loading into original primal coordinates, not for repeated calls to
the scalar \(\kappa=1\) reduced solve itself.

## 8. Streaming coefficient updates: a valid iteration multiplier

An iteration multiplier becomes valid when each call contains genuinely new
input. The following model keeps the LP dimension, support pattern, public start,
and reduced geometry fixed, but refreshes its signed coefficient block. It is an
online reoptimization theorem, not a trajectory theorem for one static LP.

### Streaming Newton service

Fix \(N\) and \(R\). At round \(t\), after the preceding output has been
committed, a challenger samples a fresh independent block

\[
 \sigma^{(t)}=(\sigma^{(t)}_1,\ldots,\sigma^{(t)}_N)\in\{\pm1\}^N
\]

and exposes the corresponding sparse coefficient oracle for (1). Future blocks
are unavailable. The algorithm starts the round with arbitrary persistent
classical and quantum memory from earlier rounds, but that memory is independent
of \(\sigma^{(t)}\). It may make arbitrary adaptive queries and computations.
Before the next block is released, it must deliver an unconditional state
\(\rho_t\) within trace distance \(1/100\) of the exact original-coordinate
Newton direction (23) for the common public start (14).

Let \(Q_t\) be a fixed worst-case budget for calls to the current raw coefficient
oracle or its inverse. Setup performed after block \(t\) is revealed is included
in \(Q_t\), as are calls used to prepare any classical or quantum advice consumed
in that round. Past memory and intermediate measurements are unrestricted.

### Theorem 5 (streaming condition-one direct sum)

Every streaming Newton service above satisfies

\[
                         \sum_{t=1}^R Q_t
                         =\Omega(RN)=\Omega(RP).          \tag{S1}
\]

The same bound holds if each round instead returns a state of any nonzero
nonnegative point satisfying the robust relative residual contract (24). Every
round has the same fixed sparsity bounds, an exactly scalar reduced Newton matrix
at the public start, and an exactly scalar reduced Hessian along its full central
path.

#### Proof

At the start of round \(t\), fix any possible earlier classical transcript and
let \(\omega_t\) be the algorithm's remaining quantum workspace. Freshness gives
\(\omega_t\) independent of \(\sigma^{(t)}\); a purification of \(\omega_t\) may
therefore be included as arbitrary input-independent advice in Theorem 2. The
fixed measurement (22), applied to \(\rho_t\), computes the parity of
\(\sigma^{(t)}\) with constant bias. Thus the quantum parity lower bound gives

\[
                              Q_t=\Omega(N)               \tag{S2}
\]

for every round and every pre-round workspace. The robust-primal variant uses
the Section 6 decoder instead. Summing (S2) proves (S1). This conditioning
argument is valid with entangled persistent memory because the new classical
block is product with the entire old workspace. \(\square\)

The bound is tight. In each round, query all \(N\) new signs, compute their
prefixes, and prepare (21), a central state, or the exact optimum. This uses
\(O(RN)\) raw queries in total. A compiled resource constructed from the current
block does not improve the asymptotics: its construction queries are part of
\(Q_t\). If it is consumable, enough copies must be prepared and charged; if it
is reusable, it helps only within the current block. Arbitrary persistent memory
cannot predict the independent next block.

### Scope of the multiplier

The causal freshness assumption is indispensable. If all rounds reuse one
\(\sigma\), Proposition 4 caches it in \(N\) queries and (S1) is false. If all
\(R\) blocks are supplied in advance, a different simultaneous direct-sum or
joint-output theorem is needed; the conditional proof above no longer applies.
If future-block advice is supplied for free, freshness is also violated.

Thus (S1) is linear in the total streamed input volume \(RN\). It should not be
described as a superlinear lower bound in the size of one fixed LP, nor as a
standard path-following iteration lower bound. Its QIPM interpretation is a
sequence of coefficient-update/reoptimization calls on one fixed sparse schema.
The exact \(\kappa=1\) geometry shows that even perfect reduced solves do not
remove the need to load each fresh affine orientation into original coordinates.

An earlier abstract online theorem in
`2026-09-02-newton-state-output-interface-lower-bounds.md` proves additivity for
fresh state-preparation oracles of changing diagonal systems. Theorem 5 supplies
a complementary LP-native instantiation: every round is an explicit
bounded-coefficient standard-form LP and an exact infeasible-start Newton
correction to a genuine common-\(\mu\) central point. The conditional direct-sum
argument itself is standard; the useful content is this exact sparse-QIPM
realization.

## 9. Novelty boundary and status

The individual ingredients are established: parity query complexity, endpoint
padding/weighted clocks, public infeasible IPM starts, Newton-state QLSA, and
condition-one diagonal systems.  Apers--Gribling already give a linear sparse-LP
coefficient-query exponent for optimal-value estimation in balanced dimensions.
The apparent new contribution is the conjunction:

> a bounded-coefficient, bounded-row/column-degree, linear-size standard-form
> LP with a public complementarity-centered infeasible start, one exact
> standard Newton correction to a genuine common-\(\mu\) central point, and an
> exactly scalar reduced Newton/central-path geometry, for which the normalized
> exact original-primal Newton direction, every robust approximate-feasible
> primal state, and every direction state whose nonnegative full-step update has
> small relative equality residual nevertheless have linear raw
> coefficient-query complexity.

No claim is made that the full equality normal matrix or KKT matrix is
well-conditioned.  No claim is made that a specific line search accepts the
unit step.  The dynamic range is \(H=\Theta(\sqrt P)\), which the separate
cut--resistance frontier shows is necessary within the broad local signed-graph
class at bounded row scale and linear volume.

### Targeted primary-literature audit (through 2026-09-02)

No exact collision was found for the conjunction in this section. The
defensible novelty is the optimization-specific interface, not any ingredient
in isolation:

- QLSA-based QIPMs already prepare normalized Newton-direction states and use
  tomography to recover classical updates; see Kerenidis--Prakash
  ([arXiv:1808.09266](https://arxiv.org/abs/1808.09266)), Casares--Martin-
  Delgado ([arXiv:1902.06749](https://arxiv.org/abs/1902.06749)), and
  Augustino et al. ([arXiv:2112.06025](https://arxiv.org/abs/2112.06025)).
  These are upper-bound/convergence results and do not lower-bound a specified
  Newton iterate in the raw sparse coefficient model.
- Public complementarity-centered infeasible initialization is also prior art.
  Wu--Yang--Terlaky Algorithm 2 starts at
  \((\omega_*\mathbf1,0,\omega_*\mathbf1)\) and their Theorem 1 upper-bounds
  a preconditioned transformed Newton solve
  ([arXiv:2412.11307](https://arxiv.org/abs/2412.11307)). Mohammadisiahroudi--
  Fakhimi--Terlaky Algorithm 1 and Theorem 4.1 give an earlier inexact
  infeasible QIPM based on a modified normal equation
  ([arXiv:2205.01220](https://arxiv.org/abs/2205.01220)). Neither paper
  constructs one hard exact direction, an exact common-\(\mu\) endpoint, or a
  condition-one reduced path.
- Mohammadisiahroudi et al.'s 2025 review/proposed ``almost-exact'' QIPM makes
  full inexact Newton steps from a strictly dual-feasible point near a center
  and gives iteration and QRAM-query upper bounds in its Theorems 1--4
  ([arXiv:2512.06224](https://arxiv.org/abs/2512.06224)). It neither gives this
  public primal--dual infeasible start nor proves a hard direction-state or
  condition-one-path lower bound.
- Apers--Gribling Theorem 8.4 proves
  \(\Omega(\sqrt{ndr})\) row queries for constant-additive-error LP
  *optimal-value estimation*
  ([arXiv:2311.03215v3](https://arxiv.org/abs/2311.03215v3)), refining van
  Apeldoorn--Gily\'en--Gribling--de Wolf Theorem 29 and Corollary 30
  ([arXiv:1705.01843](https://arxiv.org/abs/1705.01843)). With balanced
  dimensions and constant row sparsity this is already \(\Omega(P)\). Hence
  neither the linear exponent nor sparse-LP query hardness is new here. Their
  contract is an optimal value in a row oracle; it does not supply a public IPM
  start, request a Newton state, or impose scalar reduced central geometry.
- Generic QLS lower bounds do not imply this theorem. Orsucci--Dunjko
  Propositions 6 and 17 give
  \(\widetilde\Omega(\min\{\kappa,D\})\) for a designated positive-definite
  QLS solution state under sparse or block access
  ([arXiv:2101.11868](https://arxiv.org/abs/2101.11868)); Wang--Zhang prove
  \(\Omega(\kappa)\) query depth
  ([arXiv:2407.06012](https://arxiv.org/abs/2407.06012)); and Mori et al.
  Theorems 1--2 prove \(\Omega(\kappa\log(1/\epsilon))\) at constant sparsity
  and \(\Omega(\kappa\sqrt{s})\) at constant error
  ([arXiv:2601.16697v2](https://arxiv.org/abs/2601.16697v2)). Those results
  supply a square linear system and ask for its designated inverse state. They
  do not create this LP, exact Newton secant, common-\(\mu\) endpoint, or
  original-coordinate affine recovery problem. Since the reduced matrices in
  (10) and (20) have \(\kappa=1\), their condition-number lower bounds cannot
  explain Theorem 2. Conversely, this note makes no conditioning claim for the
  full normal or KKT matrices.
- Condition-one state generation is access-model sensitive. For an explicitly
  supplied system \(I z=b\) with a free preparation oracle for \(|b\rangle\),
  the solution state is immediate. Low--Su explicitly separate block-encoding
  queries from initial-state-preparation queries and prove optimal dependence
  on the latter ([arXiv:2410.18178](https://arxiv.org/abs/2410.18178)). Zhao et
  al. note the standard \(\Omega(\sqrt D)\) worst-case cost of exact amplitude
  encoding from an entry-value oracle
  ([DOI:10.1007/s42484-021-00045-x](https://doi.org/10.1007/s42484-021-00045-x)),
  while Lee--Mittal--Reichardt--Špalek--Szegedy give the general adversary
  characterization of query state conversion
  ([arXiv:1011.3020](https://arxiv.org/abs/1011.3020)). These results support
  the need to charge loading, but they do not yield the \(\Omega(P)\) LP theorem.
  Here the reduced scalar solve is easy; the hidden feasible offset and the map
  back to the original primal coordinates are not supplied as free oracles and
  jointly reveal parity.
- The geometric gain and repeated endpoint mechanism has direct prior art in
  the QLS clocks of Mori et al. and Wang--Zhang, and biased Feynman--Kitaev
  clocks already realize geometric amplitudes in Caha--Landau--Nagaj,
  equations (18)--(19)
  ([arXiv:1712.07395](https://arxiv.org/abs/1712.07395)). The rigidification
  rows and the resulting scalar Hessian are elementary. The claim should not
  be framed as a new clock, a new parity lower bound, or a new way to obtain a
  condition-one diagonal system.
- Alternative quantum central-path algorithms do not collide. Augustino et
  al. simulate the nonlinear central-path equations directly
  ([arXiv:2311.03977v2](https://arxiv.org/abs/2311.03977v2)); Gribling--Apers--
  Nieuwboer--Walter obtain condition-number-independent spectral-gap bounds
  using a Laplace--Beltrami Schr\"odinger operator
  ([arXiv:2510.06115](https://arxiv.org/abs/2510.06115)). Neither theorem asks
  for the original-coordinate primal state under this sparse coefficient
  oracle, so neither bypasses Theorems 2 or the robust corollary.
- Somma--Subasi's \(\Omega(\kappa)\) worst-case lower bound concerns verifying
  a supplied QLS solution state using the right-hand-side preparation unitary
  ([arXiv:2007.15698](https://arxiv.org/abs/2007.15698)). Dalzell--Li--Su's
  beyond-condition-number method is a designated-QLS-state upper bound
  ([arXiv:2607.07691](https://arxiv.org/abs/2607.07691)). Binkowski's
  ``practical lower bounds'' are resource/runtime estimates on benchmark QIPM
  instances, not an asymptotic oracle theorem
  ([arXiv:2604.24362](https://arxiv.org/abs/2604.24362)).

For Theorem 3 and the robust feasible-state corollary, the closest lower bounds
still have materially different contracts. Van Apeldoorn--Gily\'en--Gribling--de
Wolf and Chakrabarti--Childs--Li--Wu require a classical approximate optimizer
under membership, separation, or function-evaluation access
([arXiv:1809.00643](https://arxiv.org/abs/1809.00643),
[arXiv:1809.01731](https://arxiv.org/abs/1809.01731)). Apers--Gribling both
return an explicit approximately feasible, approximately optimal point in their
upper bound and prove an optimal-*value* row-query lower bound in Theorem 8.4,
but they do not lower-bound an amplitude encoding of an arbitrary point in a
relative-residual feasible tube
([arXiv:2311.03215v3](https://arxiv.org/abs/2311.03215v3)). Thus the linear
exponent and approximate optimization hardness are not new; the apparently new
contract is that **every** nonnegative approximately feasible update, without an
objective-gap or neighborhood promise, has a direction state carrying parity.

Quantum inexact-IPM papers give upper-bound conditions on approximate Newton
directions rather than lower bounds of this kind. Augustino et al. move Newton
residual into an orthogonal-subspace formulation to preserve feasibility
([arXiv:2112.06025](https://arxiv.org/abs/2112.06025)); Wu--Mohammadisiahroudi--
Augustino--Yang--Terlaky analyze an inexact feasible QIPM and its direction
accuracy ([arXiv:2301.05357](https://arxiv.org/abs/2301.05357)); and
Mohammadisiahroudi--Fakhimi--Wu--Terlaky develop a feasible inexact IPM adapted
to QLSA output ([arXiv:2307.14445](https://arxiv.org/abs/2307.14445)). None
proves a raw coefficient-query lower bound for a mixed state approximating any
direction whose full-step update is nonnegative and relatively feasible.
Theorem 3 should therefore not be described as a generic approximate-QLS lower
bound: it does not supply a designated square linear system, and its
nonnegative-update condition is essential. Equation (33) explicitly shows why
small full-Newton residual alone is insufficient.

The narrow wording supported by this audit is: **an LP-native separation
between exactly scalar reduced Newton/central-path geometry and the raw-query
cost of producing an original-primal direction or robust feasible-point
state.** This is evidence of novelty, not a priority guarantee. Do not call it
the first condition-one QLS lower bound: the hard task includes coefficient-
dependent affine loading/recovery outside the scalar reduced solve.

Corollary 3 is a standard end-to-end oracle-accounting consequence, not a new
direct-product theorem. Proposition 4 records the exact obstruction to such a
claim on a static instance: once all signs are cached, the number of Newton
iterations creates no fresh raw-query cost.

Status: **symbolic proof, direct numerical KKT/rank checks, and an independent
hostile proof audit passed; targeted primary-literature audit found no exact
collision.**

### Independent hostile-audit note

The prefix rigidification does not conflict with strict feasibility or
centrality. At a rigidified node, exact feasibility fixes
\(d_i=\tau_iH_i\), \(h_i=H_i\), and \(q_i=5H_i/4\), so the four primal
coordinates are \(H_i(9/8,1/8,1,3/4)\), up to swapping the pair. They are all
strictly positive; the new row fixes an interior point of the local capped
interval rather than putting an original variable on its boundary.

For centrality, the necessary and sufficient dual-feasibility condition for
\(s=\mu X^{-1}\mathbf1\) is

\[
       c-s\perp\ker A'.
\]

The rigidification rows remove exactly the prefix vectors \(W_i\) from that
kernel. Therefore no scalar stationarity equation is required at a fixed prefix
node; its positive central slacks are absorbed by the corresponding equality
multipliers. Only the free equal-height nodes remain in the kernel, and equation
(9) makes their projected stationarity equations identical. This verifies the
full-path scalar-Hessian claim without treating the fixed coordinates as absent
from complementarity.

Direct dense checks for \(N=2,3,4,5,8\), using alternating hidden signs, found
rank exactly \(3P+T\), zero endpoint primal residual, dual central residual below
\(10^{-11}\), and the secant complementarity identity to machine precision.
These computations are corroboration only; the rank, range, and secant arguments
above are exact.
