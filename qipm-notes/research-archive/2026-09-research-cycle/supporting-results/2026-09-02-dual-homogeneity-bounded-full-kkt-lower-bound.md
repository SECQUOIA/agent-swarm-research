# Dual homogeneity lifts primal hardness to a bounded full KKT direction

Date: 2026-09-02

## Main result

Positive scaling of all dual data is a classical exact symmetry of a
primal--dual Newton system.  It leaves the primal correction unchanged and
scales the multiplier and slack corrections.  Applying this symmetry with
\(\lambda=1/P\) to the bounded-range parity LP gives a linear-size sparse LP
whose complete Newton direction

\[
                 w=(\Delta x,\Delta y,\Delta s)\in\mathbb R^{11P}
\]

has every coordinate bounded by an absolute constant and
\(\|w\|_2=\Theta(\sqrt P)\).  Nevertheless, preparing its normalized state to
trace distance \(1/100\) requires \(\Omega(P)\) raw coefficient queries.  The
same lower bound holds for calls to the explicit canonical sparse block
encoding of either the \(11P\)-dimensional Newton matrix or its
\(7P\)-dimensional two-block elimination.  Both block encodings have exact
normalization five, and their right-hand sides are public.

The price is explicit.  Objective coefficients, positive slacks, and the
target complementarity are \(\Theta(1/P)\).  Although the reduced Newton
condition number remains one, the smallest singular value of the canonical
full KKT matrix is \(O(1/P)\), so its unpreconditioned condition number is
\(\Omega(P)\).  This is a bounded-coordinate theorem, not a simultaneous
constant-scale and constant-conditioned theorem.

The underlying primal feasible set and exact secant Newton step are in
[2026-09-02-bounded-range-exact-only-condition-one-hardness.md](2026-09-02-bounded-range-exact-only-condition-one-hardness.md).
Here the public height equalities are independently pinned rather than
propagated along the path.  That choice makes the height multipliers local and
is essential to the strongest full-state norm bound.  The full-state decoder
is new here.  The homogeneity lemma applies beyond this particular family.

## 1. Dual-homogeneity transfer lemma

Consider a standard-form LP and a strictly positive infeasible-start Newton
system

\[
\begin{aligned}
 A\Delta x&=b-Ax^0,\\
 A^T\Delta y+\Delta s&=c-A^Ty^0-s^0,\\
 S^0\Delta x+X^0\Delta s
   &=\widehat\mu\mathbf1-X^0s^0.
\end{aligned}
\tag{1}
\]

Assume that \(A\) has full row rank.  For any \(\lambda>0\), leave
\((A,b,x^0)\) fixed and make the dual scaling

\[
 (c,y^0,s^0,\widehat\mu)
 \longmapsto
 (\lambda c,\lambda y^0,\lambda s^0,
  \lambda\widehat\mu).
\tag{2}
\]

### Lemma 1 (exact dual homogeneity)

If the unique solution of (1) is
\((\Delta x,\Delta y,\Delta s)\), then the unique solution after (2) is

\[
              (\Delta x,\lambda\Delta y,\lambda\Delta s).
\tag{3}
\]

If \((x(\mu),y(\mu),s(\mu))\) is a primal--dual central point for the
unscaled LP, then

\[
       (x(\mu),\lambda y(\mu),\lambda s(\mu))
\tag{4}
\]

is the central point of the scaled LP at complementarity
\(\mu'=\lambda\mu\).  In particular, the entire primal central trajectory is
unchanged after reparametrizing \(\mu\).

**Proof.**  The first equation of (1) is unchanged.  The second and third
equations, including their coefficient blocks \(S^0\) and right-hand sides,
are multiplied by \(\lambda\) when (3) is substituted.  Thus (3) is a
solution.  Positivity and full row rank make the usual Newton normal matrix
positive definite, so the solution is unique.  For a central point, substitute
(4) in

\[
 Ax=b,\qquad A^Ty+s=c,\qquad Xs=\mu\mathbf1.
\]

The last two equations are multiplied by \(\lambda\), while the first is
unchanged.  This proves (4). \(\square\)

There is also a direct output-interface consequence.  Suppose a norm-one
observable \(O_x\) supported on the primal block has parity-signed expectation
at least \(\delta\) in \(|\Delta x/\|\Delta x\|\rangle\).  Extend it by zero
to the full coordinate space.  If

\[
 \lambda^2(\|\Delta y\|^2+\|\Delta s\|^2)
 \le C\|\Delta x\|^2,
\tag{5}
\]

then its expectation in the full state (3) has the same sign and magnitude
at least \(\delta/(1+C)\).  Thus any primal-state query lower bound transfers
to the normalized full KKT state whenever \(C=O(1)\).  This statement concerns
the target state itself and does not assume a particular linear-system
algorithm.

## 2. The scaled bounded secant family

Let \(N\ge2\), \(K=16N\), and \(P=17N+1\).  At node
\(i=0,\ldots,P-1\), use nonnegative variables \((u_i,v_i,h_i,t_i)\) and put
\(d_i=u_i-v_i\), \(q_i=u_i+v_i\).  With hidden signs only on the first
\(N\) transitions, impose

\[
\begin{aligned}
 d_0&=1,\\
 d_i-\sigma_i d_{i-1}&=0 &&(1\le i\le N),\\
 d_i-d_{i-1}&=0 &&(N<i<P),\\
 h_i&=1 &&(0\le i<P),\\
 q_i+t_i-2h_i&=0 &&(0\le i<P).
\end{aligned}
\tag{6}
\]

Call this matrix \(A_\sigma^{\rm pin}\).  It has \(3P\) full-rank rows and
\(4P\) columns, row sparsity at most four, column sparsity at most three, and
maximum entry magnitude two.  Its maximum absolute row and column sums are
five and three.  The support and right-hand side are public, and one value
query uses at most one hidden-sign query.

The equalities (6) define exactly the same feasible set as the
propagated-height formulation in the cited bounded-range note: both force
every \(h_i=1\).  They therefore have the same primal optimum, primal central
path, and exact primal secant correction.  The representation change is
legitimate for a full-direction lower bound because (6) itself is a sparse LP
input family.  It does change the equality multiplier coordinates, as any
change of row basis may.

Use the public primal start

\[
 x_i^0=\left(\frac56,\frac56,\frac{20}{27},\frac59\right),
 \qquad
 \bar s_i^0=\left(\frac{10}{27},\frac{10}{27},
                         \frac5{12},\frac59\right),
\tag{7}
\]

and the unscaled objective block is

\[
                  \bar c_i=\left(\frac{43}{36},
                  \frac{43}{36},1,1\right).
\tag{8}
\]

Take \(y^0=0\), \(\lambda=1/P\), and set

\[
 c=\lambda\bar c,\qquad s^0=\lambda\bar s^0,
 \qquad \mu^0=\lambda\frac{25}{81},
 \qquad \widehat\mu=\lambda\frac{25}{162}.
\tag{9}
\]

All these data are public.  Their rational descriptions use \(O(\log P)\)
bits.  Since the public pair difference at the start is zero, every hidden
transition coefficient still multiplies zero in \(b-A_\sigma x^0\).  Hence
all three Newton right-hand sides are independent of \(\sigma\).

Lemma 1 and the exact secant construction show that the primal correction is
unchanged.  Up to the hidden swap of the first pair, its node block is

\[
 \Delta x_i=\left(\frac7{24},-\frac{17}{24},
                         \frac7{27},\frac7{36}\right).
\tag{10}
\]

The unscaled slack correction, with the first coordinate paired with the
larger primal coordinate, is

\[
 \Delta\bar s_i=\left(-\frac{17}{54},\frac7{54},
                    -\frac{17}{48},-\frac{17}{36}\right),
 \qquad \Delta s=\lambda\Delta\bar s.
\tag{11}
\]

Let \((\alpha,\beta,\gamma)\) denote the difference-row, height-fixing-row,
and cap-row multipliers.  Writing
\(\tau_j=\prod_{i=1}^j\sigma_i\), stationarity at the endpoint gives the
unscaled values

\[
 \bar\alpha_j=\frac29\tau_j(P-j),\qquad
 \bar\beta_j=\frac{133}{48},\qquad
 \bar\gamma_j=\frac{11}{12},
 \qquad
 \Delta y=\lambda(\bar\alpha,\bar\beta,\bar\gamma).
\tag{12}
\]

For completeness, subtracting the two pair stationarity equations gives
\(B_\sigma^T\bar\alpha=(2/9)\tau\), whose backward recurrence yields the first
formula.  The \(t\) equation gives \(\bar\gamma=1-1/12=11/12\), and the
\(h\) equation gives
\(\bar\beta=1+2\bar\gamma-1/16=133/48\).

Equations (10)--(12) show coordinatewise that

\[
 \|\Delta x\|_\infty\le\frac{17}{24},\qquad
 \|\Delta y\|_\infty\le\frac29,
 \qquad \|\Delta s\|_\infty\le\frac{17}{36P}.
\tag{13}
\]

Thus the full direction is genuinely bounded, rather than merely normalized
after allowing a large dual block.

## 3. Norm and parity decoder

The exact squared primal norm per node is

\[
                     D=\frac{16139}{23328}.
\tag{14}
\]

Put

\[
 E=\frac{86657}{186624}=\|\Delta\bar s_i\|^2,
 \qquad
 C_y=\left(\frac{133}{48}\right)^2
       +\left(\frac{11}{12}\right)^2
       =\frac{19625}{2304}.
\tag{15}
\]

Using \(\sum_{\ell=1}^P\ell^2=P(P+1)(2P+1)/6\), (11)--(12) give

\[
 \|\Delta y\|^2+\|\Delta s\|^2
 =\frac{4}{81P^2}\sum_{\ell=1}^P\ell^2
   +\frac{C_y+E}{P}
 <\frac{P}{40}
 \quad(P\ge35).
\tag{16}
\]

Therefore

\[
 DP\le\|w\|^2<\left(D+\frac1{40}\right)P<\frac34P.
\tag{17}
\]

On every one of the \(K\) public-copy nodes, let a fixed diagonal observable
report \(+1\) on the \(v\) coordinate, \(-1\) on the \(u\) coordinate, and
zero elsewhere.  The signed squared-mass difference per copy node is
\(5/12\), with sign
\(p_N=\prod_{i=1}^N\sigma_i\).  By (17), its expectation in \(|w/\|w\|\rangle\)
has the parity sign and magnitude greater than

\[
          \frac{(5/12)K}{(3/4)P}
          =\frac{5K}{9P}
          \ge\frac{32}{63}>\frac12.
\tag{18}
\]

A state at trace distance \(1/100\) changes the induced measurement
probabilities by at most \(1/100\), leaving constant parity bias.  Bounded-error
quantum parity needs at least \(N/2\) sign-oracle queries.  Since
\(P=17N+1\), preparing the normalized full direction to this trace error
requires \(\Omega(P)\) raw sparse-coefficient queries.  This proves the stated
full-state lower bound.

## 4. Canonical block-encoding interface

At the scaled public start, order the standard three-block Newton matrix as

\[
 M_\lambda^{(3)}=
 \begin{pmatrix}
 0&(A_\sigma^{\rm pin})^T&I\\
 A_\sigma^{\rm pin}&0&0\\
 \lambda\bar S^0&0&X^0
 \end{pmatrix}.
\tag{19}
\]

Its maximum absolute row sum and maximum absolute column sum are both five:
the cap rows of \(A_\sigma^{\rm pin}\) attain five, while every other block row or
column is smaller.  Put \(y'=-\Delta y\).  Eliminating \(\Delta s\) and
multiplying the dual equation by minus one gives

\[
 M_\lambda^{(2)}\binom{\Delta x}{y'}
 =\binom{(X^0)^{-1}r_c-r_d}{r_p},
 \quad
 r_p=b-A_\sigma^{\rm pin}x^0,\quad
 r_d=c-s^0,\quad
 r_c=\widehat\mu\mathbf1-X^0s^0,
\]

where the two-block matrix is

\[
 M_\lambda^{(2)}=
 \begin{pmatrix}
 (X^0)^{-1}\lambda\bar S^0&(A_\sigma^{\rm pin})^T\\
 A_\sigma^{\rm pin}&0
 \end{pmatrix},
\tag{20}
\]

which has the same maximum absolute row and column sum five.  The standard
magnitude-weighted sparse state construction therefore gives exact block
encodings of (19) and (20) with normalization

\[
                             \alpha=5.
\tag{21}
\]

All nonzero positions and all entries except the signed transition values are
public.  A call to either explicit block encoding, its adjoint, or its
controlled version can be simulated using one coherent sign-oracle query,
with arbitrary-input and failure subspaces included in the simulation.
Concretely, use the row/column state-pair construction in equations (23)--(24)
of
[2026-09-02-linear-plateau-full-kkt-lower-bound.md](2026-09-02-linear-plateau-full-kkt-lower-bound.md),
replace its denominator six by five, and put the single local hidden sign in
the same phase oracle.  This fixes the complete unitary, including its failure
subspaces.
Right-hand-side state preparation uses no sign queries.  For (19), the target
is the normalized full direction from Section 3.  For (20), the target is
the normalized two-block solution
\(w_2=(\Delta x,y')=(\Delta x,-\Delta y)\).  It has the same primal
coordinates and
\[
 \|w_2\|^2=\|\Delta x\|^2+\|\Delta y\|^2
 \le \|w\|^2<\frac34P.
\]
Consequently the observable in (18) has magnitude greater than \(1/2\) in
either target state.  Hence an algorithm that prepares the corresponding
solution state using \(q\) calls to either canonical block encoding would
yield a parity algorithm using at most \(q\) sign queries.  Thus

\[
                             q\ge N/2=\Omega(P).
\tag{22}
\]

As usual, (22) charges construction of any input-dependent advice,
preconditioner, prefix gauge, QRAM, or recovery map.  It is not a lower bound
relative to an arbitrary input-dependent block encoding or recovery oracle
supplied for free, because such an oracle may already contain every prefix
product.

## 5. The inverse-scale price

The scaled central endpoint occurs at

\[
                     \mu_1'=\frac1{16P}.
\tag{23}
\]

All its positive slack coordinates and all objective coefficients are
\(\Theta(1/P)\); the primal point and feasible region are unchanged.  The
reduced Newton matrix at the public start is

\[
 W^T(X^0)^{-1}S^0W
 =\lambda\frac{22}{27}I_P.
\tag{24}
\]

Its spectral condition number is still exactly one, but its absolute scale is
\(\Theta(1/P)\).

For this fixed primal endpoint, the inverse scale is necessary in the
canonical signed-row representation.  Write its oriented pair as
\((x_u,x_v)=(9/8,1/8)\) when \(\tau_j=+1\), with the coordinates swapped when
\(\tau_j=-1\).  At complementarity \(\mu\), its pair slacks satisfy

\[
 s_{u_j}-s_{v_j}=-\frac{64}{9}\mu\tau_j.
\]

Subtracting the two stationarity equations and solving the signed-incidence
backward recurrence therefore gives the exact multiplier

\[
 \alpha_j=\frac{32}{9}\mu\tau_j(P-j),
 \qquad
 \|\alpha\|_\infty=\frac{32}{9}\mu P.
\tag{25}
\]

At \(\mu=1/16\), this reduces to the unscaled formula
\(\bar\alpha_j=(2/9)\tau_j(P-j)\).  Thus, along the dual-homogeneity ray that
keeps this constant-ratio primal endpoint fixed, bounded multiplier
coordinates require \(\mu=O(1/P)\), while constant \(\mu\) forces
\(\Theta(P)\) accumulation.  This necessity is instance- and
representation-specific: rescaling or changing the equality rows changes the
multiplier coordinates.

The canonical full matrices expose the same price as a small singular value.
For (20), take a unit \(z\in\ker A_\sigma^{\rm pin}\).  Then

\[
 \left\|M_\lambda^{(2)}\binom z0\right\|
 =\lambda\|(X^0)^{-1}\bar S^0z\|
 \le\lambda.
\tag{26}
\]

For (19), use

\[
 v=\left(z,0,-\lambda(X^0)^{-1}\bar S^0z\right).
\]

The primal-feasibility and complementarity output blocks vanish, while the
dual output block has norm at most \(\lambda\); also \(\|v\|\ge1\).  Hence

\[
 \sigma_{\min}(M_\lambda^{(2)})\le\lambda,\qquad
 \sigma_{\min}(M_\lambda^{(3)})\le\lambda.
\tag{27}
\]

Both matrices have largest singular value at least one, so their canonical
unpreconditioned condition numbers are \(\Omega(1/\lambda)=\Omega(P)\).
This condition statement is representation-dependent and can change under
preconditioning.  The raw-query theorem does not depend on it: the fixed
primal coordinates of the requested state still contain parity, and any
input-dependent preconditioner and recovery operation is charged.

The order is sharp for these raw matrices.  Let \(B_\sigma\) be the pinned
signed bidiagonal matrix in the difference equations.  Prefix-sign row and
column gauges show that it has the same singular values as the all-positive
pinned incidence matrix.  Since \(B_+^{-1}\) is the cumulative-sum matrix,
\[
 \sigma_{\min}(B_\sigma)=\Theta(P^{-1}),
 \qquad \|B_\sigma\|=\Theta(1).
\tag{28}
\]
After the orthogonal sum/difference change in each pair, a bounded local
column transformation replaces every cap expression by a private
coordinate.  It reduces \(A_\sigma^{\rm pin}\), up to transformations with
constant condition number, to the direct sum of
\(\sqrt2B_\sigma\), the identity height pins, and the identity cap rows.
Consequently
\[
 \sigma_{\min}(A_\sigma^{\rm pin})=\Theta(P^{-1}),
 \qquad \|A_\sigma^{\rm pin}\|=\Theta(1),
\tag{29}
\]
uniformly in the hidden signs.

Write
\[
 (X^0)^{-1}\bar S^0=E,\qquad
 \frac49I\preceq E\preceq I.
\]
Congruence of (20) by
\(\operatorname{diag}(E^{-1/2},I)\), whose condition number is at most
\(3/2\), gives
\[
 \begin{pmatrix}\lambda I&C^T\\C&0\end{pmatrix},
 \qquad C=A_\sigma^{\rm pin}E^{-1/2}.
\tag{30}
\]
For each singular value \(s\) of \(C\), the paired eigenvalues are
\[
 \frac{\lambda\pm\sqrt{\lambda^2+4s^2}}2,
\tag{31}
\]
and the null space of \(C\) contributes eigenvalue \(\lambda\).
Equations (29)--(31), with \(\lambda=1/P\), show that the smallest absolute
eigenvalue is \(\Theta(P^{-1})\) and the largest is \(\Theta(1)\).
The constant-conditioned congruence preserves these asymptotic singular
bounds, so
\[
 \boxed{\kappa_2(M_\lambda^{(2)})=\Theta(P).}
\tag{32}
\]

The same is true for (19).  Set
\(D=\lambda(X^0)^{-1}\bar S^0\) and change slack variables by
\(\Delta s'=\Delta s+D\Delta x\).  After scaling the complementarity block
by \((X^0)^{-1}\), subtracting it from the dual block leaves the direct sum
of (20), up to a sign, and an identity slack block.  These row and column
transformations have condition bounded by an absolute constant because
\(X^0\) and \((X^0)^{-1}\) are bounded and \(\|D\|\le1\).  Therefore
\[
 \boxed{\kappa_2(M_\lambda^{(3)})=\Theta(P).}
\tag{33}
\]

Since the canonical block-encoding normalization is exactly
\(\alpha=5\) and both raw matrix norms are \(\Theta(1)\), their
normalization-aware inverse parameter is also
\[
       \alpha\|M_\lambda^{-1}\|=\Theta(P).
\tag{34}
\]
Thus the lower bound is not independent of the full-system condition or
inverse scale.

There are two related precision effects.  First, the public values
\(\lambda c,\lambda s^0,\mu^0,\widehat\mu\) need
\(\Theta(\log P)\) bits for exact rational representation.  This costs no
hidden-input query in the stated exact value-oracle model.  Second, the dual
and complementarity sectors of the unnormalized Newton right-hand side have
norm \(\Theta(\lambda\sqrt P)\), while its primal-feasibility sector has
norm \(\Theta(\sqrt P)\).  Their relative amplitude is therefore
\(\Theta(\lambda)=\Theta(P^{-1})\).  Dropping those small public sectors can
change the solution by a constant because
\(\|M_\lambda^{-1}\|=\Theta(P)\).  A generic stable QLS implementation must
therefore resolve the block encoding and normalized right-hand side to
operator/state error \(O(P^{-1})\), or prepare them exactly as the canonical
construction does.  Polynomial/QSVT inversion must likewise resolve a
\(\Theta(P^{-1})\) singular gap and has degree \(\Theta(P)\), up to
logarithmic accuracy factors.

## 6. Scope and comparison

### 6.1 Literature and novelty boundary

Scale invariance is not a novelty claim.  Tunçel,
[*Primal-Dual Symmetry and Scale Invariance of Interior-Point Algorithms for
Convex Optimization*](https://doi.org/10.1287/moor.23.3.708), develops the
broader conic theory of primal--dual symmetry and invariant variable
scalings.  In the present LP setting, multiplying the objective, dual
variables, dual slacks, and complementarity parameter by one positive scalar
is the elementary specialization obtained by substitution in the
primal--dual central and Newton equations.  Lemma 1 records that
specialization and its effect on all three blocks of the Newton direction; it
should not be advertised as a new homogeneity principle.

The exact normalization in Section 4 is likewise not a new generic
block-encoding result.  It is the state-preparation-pair/q-norm construction
of Gilyén et al.,
[*Quantum singular value transformation and
beyond*](https://arxiv.org/abs/1806.01838), specialized to a matrix whose
maximum absolute row and column sums are both five; compare the classical-data
resource treatment of Clader et al.,
[*Quantum resources required to block-encode a matrix of classical
data*](https://doi.org/10.1109/TQE.2022.3231194).  What matters here is that
the specialization fixes the complete unitary oracle, has normalization five,
and uses only one local hidden-sign query per call or adjoint call.  It does
not establish that five is the minimum normalization over all possible access
models or input-dependent encodings.

Published QIPMs use quantum linear solvers for normal-equation, orthogonal-
subspace, nullspace, or related Newton formulations and then generally use
tomography for classical updates.  Representative examples are Kerenidis--
Prakash,
[*A quantum interior point method for LPs and
SDPs*](https://arxiv.org/abs/1808.09266); Augustino et al.,
[*Quantum interior point methods for semidefinite
optimization*](https://arxiv.org/abs/2112.06025); Mohammadisiahroudi et al.,
[*An inexact feasible interior point method for linear optimization with high
adaptability to quantum computers*](https://arxiv.org/abs/2307.14445) and
[*Improvements to quantum interior point method for linear
optimization*](https://arxiv.org/abs/2310.07574); Wu et al.,
[*A quantum dual logarithmic barrier method for linear
optimization*](https://arxiv.org/abs/2412.15977); Wu--Yang--Terlaky,
[*A preconditioned inexact infeasible quantum interior point method for linear
optimization*](https://arxiv.org/abs/2412.11307); and Mohammadisiahroudi et
al.,
[*Optimal scaling quantum interior point method for linear
optimization*](https://arxiv.org/abs/2512.04510).  These are algorithmic upper
bounds.  Their scale choices and Newton reformulations do not give a
raw-coefficient oracle lower bound for one normalized complete KKT direction,
and no theorem in them matches the simultaneous public-right-hand-side,
bounded-coordinate, constant-normalization properties here.  Binkowski,
[*Practical lower bounds for hybrid quantum interior point methods in linear
programming*](https://arxiv.org/abs/2604.24362), gives empirical
instance-by-instance runtime exclusions, not a worst-case query lower bound of
this form.

Generic QLSP lower bounds do contain the same linear exponent on other hard
matrix families.  In particular, Orsucci--Dunjko,
[*On solving classes of positive-definite quantum linear systems with
quadratically improved runtime in the condition
number*](https://arxiv.org/abs/2101.11868), Wang--Zhang,
[*Tight quantum depth lower bound for solving systems of linear
equations*](https://arxiv.org/abs/2407.06012), and Mori et al.,
[*Sparsity-dependent complexity lower bound of quantum linear system
solvers*](https://arxiv.org/abs/2601.16697v2), rule out treating the
\(\Omega(P)\) exponent, parity propagation, or solution-state decoding as new
in isolation.  They do not supply this standard-form LP, its public centered
infeasible start and public Newton right-hand side, or the homogeneity
transfer from a primal state to a bounded full KKT state.  The present matrix
also has unpreconditioned condition number \(\Theta(P)\), so the result is
compatible with condition-number-dependent QLSP bounds rather than a
constant-condition contradiction.

The defensible apparent novelty is therefore the conjunction and transfer:
a classical dual scaling is chosen so that the hard primal correction is
unchanged, the accumulated multiplier block no longer dominates or has large
coordinates, and a fixed primal-supported observable retains constant bias in
the normalized full direction.  Together with the explicit LP and oracle
completion, this yields an \(\Omega(P)\) raw-query lower bound for a bounded-
coordinate full KKT direction.  The observable dilution bound (5) is an
elementary norm argument; its use for this LP/QIPM output contract, rather
than the inequality itself, is the contribution.  The targeted primary-source
search found no exact prior theorem with this conjunction.  That is evidence
of apparent novelty, not proof of priority.

### 6.2 Remaining scope

This result closes one gap between the two earlier parity families:

- the bounded-range theorem had constant primal coordinates and condition-one
  reduced geometry, but deliberately claimed only a primal state because the
  canonical equality multiplier accumulated to \(\Theta(P)\);
- the gain-plateau full-KKT theorem proved a full-state lower bound, but its
  exact direction contained growing multiplier coordinates; and
- dual homogeneity suppresses those coordinates without changing the hard
  primal correction, yielding a complete bounded \(11P\)-coordinate target.

The independently pinned representation has
\(\|b\|_2=\sqrt{P+1}=\Theta(\sqrt P)\), whereas the propagated-height
representation has only two nonzero anchor entries and \(\|b\|_2=\sqrt2\).
The sharp \(\Theta(N^{-1/2})\) relative-residual theorem in the bounded-range
note uses the latter representation.  The full-direction result here does not
inherit that residual theorem: it is an exact Newton-direction state lower
bound for the equally sparse pinned formulation.

The improvement is paid for by inverse-polynomial dual scale.  It therefore
does not prove that a full Newton state remains hard when primal variables,
dual slacks, reduced costs, complementarity, and the full KKT singular scale
are all bounded below by constants.  Establishing or ruling out that stronger
simultaneous regime remains open.
