# Independent review of exact-penalty encoding lower bounds

Date: 2026-09-25. The constructions were supplied by the parent research agent.
This reviewer independently derived their dual values and checked their
regularity and encoding claims. A fresh subagent separately searched for prior
overlap.

**Verdict:** both constructions are correct. The one-binary construction is the
stronger main example. The two-binary construction is a useful symmetric
companion with optimal multiplier zero. Their strongest defensible contribution
is a restricted, multiplier-robust exact-penalty obstruction; repeated squaring
and its numerical-size pathology are established prior art.

## Common chain

For $n\ge1$, take $a\in[0,1]^n$, $y\in[-1,1]$, and impose
\[
a_1\ge\frac14,\qquad a_{i+1}\ge a_i^2\quad(1\le i<n).
\]
Then $a_i\ge2^{-2^i}$, so
\[
a_n\ge\delta_n:=2^{-2^n}>0.
\]
Equality throughout the chain attains this lower bound. Every nonlinear native
inequality has the convex form $a_i^2-a_{i+1}\le0$.

For each construction below, the objective is $-q$, the primal equality is
$y=0$, and the augmented relaxation is
\[
L_\rho(\lambda)=\min_X\{-q+\lambda y+\rho|y|\},\qquad
D_\rho=\sup_{\lambda\in\mathbb R}L_\rho(\lambda),\qquad \rho\ge0.
\]
Bounds make the native set compact. The minimum exists.

## Main construction: one binary

Let $q\in\{0,1\}$ and add the single native inequality
\[
y\ge a_n-2(1-q).
\]
Write $\delta=\delta_n$. The projected native sets are exactly
\[
Y_0=[-1,1],\qquad Y_1=[\delta,1].
\]
The chain proves necessity, and its minimal point attains every value in these
intervals. Indeed, at that point the lower bound for $q=0$ is $\delta-2<-1$.

Primal feasibility forces $q=0$; $a_i=3/8,y=0,q=0$ is feasible. Hence
$P_n^*=0$. Direct minimization over the intervals gives
\[
L_\rho(\lambda)=
\min\{0,\rho-|\lambda|,-1+\delta(\rho+\lambda),-1+\rho+\lambda\}.
\]

The native points $(q,y)=(0,-1)$ and $(1,\delta)$ have relaxation values
$\rho-\lambda$ and $-1+\delta(\rho+\lambda)$. Averaging them with respective
weights $\delta/(1+\delta)$ and $1/(1+\delta)$ cancels the multiplier.
The primal-feasible point also gives a zero upper bound. Thus every multiplier
satisfies
\[
L_\rho(\lambda)\le
\min\left\{0,\frac{2\rho\delta-1}{1+\delta}\right\}.
\]

For $0\le\rho\le1/(2\delta)$, choose
\[
\lambda_\rho^*=\frac{1+\rho(1-\delta)}{1+\delta}.
\]
Then $\lambda_\rho^*\ge\rho\ge0$. The $q=0$ minimum is
$\rho-\lambda_\rho^*$, attained at $y=-1$, and the $q=1$ minimum is
$-1+\delta(\rho+\lambda_\rho^*)$, attained at $y=\delta$.
These expressions agree and equal $(2\rho\delta-1)/(1+\delta)$.
For $\rho\ge1/(2\delta)$, the choice $\lambda=\rho$ gives $q=0$ minimum zero
and $q=1$ minimum $-1+2\rho\delta\ge0$. Therefore
\[
\boxed{
D_\rho=\min\left\{0,\frac{2\rho\delta_n-1}{1+\delta_n}\right\},\qquad
\rho_n^*=\frac1{2\delta_n}=2^{2^n-1}.
}
\]

This proves that optimizing over all real multipliers does not remove the
large penalty requirement.

### Value exactness and minimizer sets

At the threshold, value exactness forces
$\lambda=\rho=1/(2\delta_n)$. Indeed, both displayed adverse witness values must
be nonnegative, so $\lambda\le\rho$ and
$\lambda\ge1/\delta_n-\rho=\rho$. Both witnesses then tie with primal optima.
Thus minimizer-set exactness fails at the threshold.

For $\rho>\rho_n^*$, choosing $\lambda=\rho$ still leaves native $q=0,y<0$
points tied at zero. To get equality of minimizer sets, choose instead
$\lambda=\rho_n^*$. Then $\rho>|\lambda|$ and
$\rho+\lambda>1/\delta_n$. Every native $q=0,y\ne0$ point and every native
$q=1$ point has strictly positive relaxation value. The relaxation minimizers
are exactly the primal minimizers.

## Companion construction: two binaries and symmetry

Add a second binary $b$ and replace the one-binary coupling inequality by
\[
y\ge a_n-(1-q)-2(1-b),\qquad
y\le-a_n+(1-q)+2b.
\]
For $q=1,b=0$, one has $y\le-a_n\le-\delta_n$; for $q=1,b=1$,
one has $y\ge a_n\ge\delta_n$. Primal feasibility again forces $q=0$,
and $P_n^*=0$.

The two native points using the minimal chain and
$(q,b,y)=(1,0,-\delta_n),(1,1,\delta_n)$ yield
\[
L_\rho(\lambda)\le
\min\{0,-1+\rho\delta_n-|\lambda|\delta_n\}
\le\min\{0,-1+\rho\delta_n\}.
\]
At $\lambda=0$, all native $q=0$ points have nonnegative objective,
and every $q=1$ point has objective at least $-1+\rho\delta_n$.
These bounds are attained, so
\[
\boxed{D_\rho=L_\rho(0)=\min\{0,-1+\rho\delta_n\}.}
\]

The projected native sets are $[-1,1]$ for $q=0$ and
$[-1,-\delta_n]\cup[\delta_n,1]$ for $q=1$. Consequently, writing
$t=\rho-|\lambda|$,
\[
L_\rho(\lambda)=
\begin{cases}
\min\{0,-1+\delta_n t\},&t\ge0,\\
-1+t,&t<0.
\end{cases}
\]
Thus fixed-multiplier value exactness occurs exactly when
$\rho\ge2^{2^n}+|\lambda|$.
The smallest optimized-dual penalty is $2^{2^n}$.
At the threshold, infeasible witnesses tie with feasible optima; any strictly
larger penalty at $\lambda=0$ gives equality of minimizer sets.

## Regularity and the motivating paper's assumptions

Both formulations have affine objectives and convex quadratic native
inequalities. Their entire continuous relaxations are convex; integrality
is the only nonconvexity. Coefficients come from a fixed finite rational set.

In every primal-feasible binary slice, set $a_i=3/8,y=0$.
Every nonlinear inequality has strict slack
\[
\frac38-\left(\frac38\right)^2=\frac{15}{64}.
\]
All displayed nonconstant affine inequalities in the continuous variables
have slack at least $1/8$. Binary bounds become constant conditions after
fixing binaries and are not asserted to be strict.

The $q=1$ slices are primal-infeasible. They nevertheless have native strict
points: $a_i=3/8,y=1/2$ in the one-binary construction, and
$a_i=3/8,y=(2b-1)/2$ in the symmetric construction.
The same slack bounds apply. The tiny quantity is the distance of an
equality-infeasible integer fiber to $y=0$, not the displayed native Slater
margin.

[Lefebvre–Schmidt, revised December 15, 2025](https://optimization-online.org/wp-content/uploads/2024/07/exact-penalty-for-minlp-1.pdf),
Definition 1, concerns zero gap for the augmented dual optimized over its
multiplier. Assumptions 1–4 and Assumption 5's feasible-slice Slater or
infeasibility alternative all hold here. Theorem 14 supplies finite exact
penalties for fixed multipliers but no rational-size bound, so there is no
contradiction.

Their conclusion asks whether polynomial-size penalties known for MIQP extend
to quadratically constrained problems. These examples refute the general
extension to convex mixed-integer QCQP with variable continuous dimension and
ordinary rational encoding. They do not settle fixed total dimension. The
public repository page checked on this date identifies December 15, 2025 as
the latest revision.

## Encoding qualifications

The main threshold $2^{2^n-1}$ has $2^n$ binary digits, and the companion
threshold $2^{2^n}$ has $2^n+1$. Every larger rational penalty $p/s$,
with positive integer denominator, requires at least as many numerator digits:
$p\ge s\rho_n^*\ge\rho_n^*$.

There are $O(n)$ nonzero constant-size rational coefficients. A conventional
sparse representation including variable indices uses $O(n\log n)$ bits.
Penalty size is exponential in dimension and superpolynomial in this input
length. Dense encodings also have polynomial length in $n$. Avoid claiming
exponential size in total input length without specifying the encoding.

This is ordinary numerator/denominator binary encoding. A symbolic power,
arithmetic circuit, or floating-point encoding with a binary exponent can name
the threshold compactly. The result is not a lower bound for every numerical
representation.

The residual is normalized as $y$, and the penalty norm is fixed as $|y|$.
The threshold changes under residual or norm scaling. These examples do not
rule out useful reformulations or cuts. In particular, the valid inequality
$q=0$ resolves the constructed primal immediately; the result supplies no
computational-hardness theorem for solving these instances.

## Prior overlap and qualified significance

Repeated squaring is classical.
[Pataki–Touzov](https://arxiv.org/html/2103.00041) reproduces Khachiyan's convex
quadratic chain and discusses related large certificates.
The numerical-size mechanism itself is not new.

[Bienstock–Del Pia–Hildebrand](https://arxiv.org/html/2011.08347), Section 6,
Example 4, gives a bounded nonconvex QCQP with constant objective advantage at
doubly exponentially small infeasibility. A large ordinary norm-penalty lower
bound follows immediately by dividing the advantage by the violation; that
penalty consequence is an inference, not their stated theorem.
Other constraints are nonconvex, and they do not analyze freely optimized
augmented-Lagrangian multipliers. Example 3 records the classical chain.

Care is needed with that source's displayed approximate vector.
Its $d_1=1/2,d_i=2^{-2^i}$ for $i\ge2$ gives
$d_1^2-d_2=3/16$ when $N\ge3$. Replacing it by
$d_i=2^{-2^{i-1}}$ for $i<N$, with $d_N=0$, repairs the chain and gives
last residual $2^{-2^{N-1}}$. The doubly exponential conclusion survives.
The fresh reviewer independently checked the same typo in arXiv PDF v5,
printed page 27, Example 6.2, and checked the repair with exact fractions for
$N=3,4,5$. It is not just an HTML conversion issue.

The fresh reviewer also identified
[Beck–Bienstock–Schmidt–Thürauf (2023)](https://doi.org/10.1007/s10957-023-02238-9),
which uses a compact convex quadratic chain to demonstrate bilevel sensitivity
under small violations while retaining Slater regularity, and
[Gu–Ahmed–Dey, Theorem 11](https://arxiv.org/html/1907.00920), which gives the
positive polynomial-size exact-penalty boundary for convex quadratic objectives
over rational mixed-integer polyhedra. Quadratic native constraints are outside
that positive result.

The defensible provisional contribution is the adaptation to bounded convex
mixed-integer QCQP, one binary, one normalized linear equality, small
coefficients, quantitative native Slater points, and freely optimized
multipliers. No source examined by this review explicitly proves that
restricted statement. An unsuccessful search does not establish novelty.
Any publication should prominently acknowledge the prior chain examples.

The useful theoretical distinction is between regularity of feasible integer
fibers and separation of infeasible fibers from the linking equality.
Practical value would require exploiting this distinction in relaxations,
scaling, or certificates. No computational speedup is proved.

## Targeted checks actually run

Both exact checks were first executed inline with Python's fractions.Fraction,
then saved together in parametric-penalty-review-check.py and rerun using:

~~~sh
python research-20260925/parametric-penalty-review-check.py
~~~

For each variant, $n=1,\ldots,10$ and five penalties below, at, and above the
threshold were combined with eight multipliers. The checks use native interval
endpoints and zero where applicable. The two-binary check also verifies chain
endpoints and uniform strict margins. The one-binary check verifies its
maximizing multiplier, balanced-witness identity, threshold bit count, and
strict exactness inequalities. Result: 400 exact rational checks per variant,
800 total, all passed.

The audit checks arithmetic and finite cases; the independent proofs above
establish all dimensions and multipliers. The two-witness argument is especially
important because a lower bound only at multiplier zero would not establish
the main claim. No Lean proof was attempted in this review. No project-wide
verification or CI checks were run.
