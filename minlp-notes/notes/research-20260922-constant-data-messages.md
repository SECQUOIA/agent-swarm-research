# Exact and approximate scalar messages with a fixed coefficient alphabet

Date: 2026-09-22. Status: independently derived strengthening of
[the first scalar-message construction](research-20260922-message-complexity.md).
The coordinator and a separate reviewer proposed replacing its varying control
coefficients by a constant. This note checks that replacement, proves a sharper
approximation result, and gives a matching lower bound for pruning original
support quadratics. Priority remains unsettled. General exponential growth of
quadratic dynamic-programming representations is established background.
The [fresh independent review](review-20260922-constant-data-messages.md)
checked the exact formulas, the state-indicator lift, and both sides of the
pruning-accuracy theorem without finding a mathematical defect.

The strengthening removes small input coefficients as an explanation for the
exact representation lower bound. A fixed, time-homogeneous stage cost already
creates exponentially many indispensable quadratic formulas. The same example
also admits a precise, horizon-independent tradeoff between pruning and additive
accuracy. Neither conclusion is a lower bound for arbitrary optimization
algorithms.

## Model and exact support values

Fix a rational number \(0<\theta\le1/10\). For every horizon \(n\ge1\), define

\[
 V_n(t)=\min\left\{
 \sum_{i=1}^n(x_i^2-2x_i+z_i)
 +\sum_{i=1}^n(s_i-\theta s_{i-1}-\theta x_i)^2:
 x_i(1-z_i)=0,\ z_i\in\{0,1\},\ s_0=0,\ s_n=t
 \right\},\qquad t\in[0,1].                              \tag{1}
\]

States and controls are real and otherwise unconstrained. On a feasible
support, the first summand is \((x_i-z_i)^2\). Put

\[
 W_n=\sum_{j=0}^{n-1}\theta^{2j},\qquad
 c_z=\sum_{i=1}^n\theta^{n-i+1}z_i,\qquad
 D_z=W_n+\sum_{i=1}^n\theta^{2(n-i+1)}z_i.
\]

**Proposition 1.** The exact message is

\[
 V_n(t)=\min_{z\in\{0,1\}^n}q_z(t),\qquad
 q_z(t)=\frac{(t-c_z)^2}{D_z}.                            \tag{2}
\]

**Proof.** For fixed \(z\), write \(e_i=x_i-z_i\) and
\(r_i=s_i-\theta s_{i-1}-\theta x_i\). Inactive coordinates have
\(e_i=0\). Iterating the recurrence gives the single equality

\[
 t-c_z=\sum_i\theta^{n-i+1}e_i+\sum_i\theta^{n-i}r_i.     \tag{3}
\]

Conversely, any \((e,r)\) satisfying this equality and the inactive-coordinate
restrictions reconstructs feasible states. The objective is
\(\sum_i e_i^2+\sum_i r_i^2\). Cauchy--Schwarz gives (2), with equality at

\[
 e_i=\frac{t-c_z}{D_z}\theta^{n-i+1}z_i,\qquad
 r_i=\frac{t-c_z}{D_z}\theta^{n-i}.
\]

This also proves attainment. \(\square\)

The usual Bellman recursion uses the same stage cost at every step:

\[
 V_i(t)=\min_{u,x,z:\ x(1-z)=0,\ z\in\{0,1\}}
 \{V_{i-1}(u)+x^2-2x+z+(t-\theta u-\theta x)^2\},
\]

where \(V_0(0)=0\) and \(V_0(u)=+\infty\) for \(u\ne0\).

## Exact exponential growth from constant data

Define

\[
 C_\theta=\frac{1+\theta^2}{1-\theta^2}<2.
\]

Every denominator is in \([1,C_\theta]\), and every center belongs to
\([0,\theta/(1-\theta)]\subset[0,1]\). The centers are distinct. More
precisely, their minimum separation is \(\theta^n\). To check this, let
\(k\) be the smallest power at which two digit strings differ. If \(k=n\),
the difference is \(\theta^n\). If \(k<n\), its absolute value is at least

\[
 \theta^k-\sum_{j=k+1}^n\theta^j
 \ge \theta^k\frac{1-2\theta}{1-\theta}
 \ge\theta^n,
\]

because \((1-2\theta)/(1-\theta)\ge\theta\) on the specified range.
Two strings differing only at power \(n\) attain this separation.

At \(t=c_z\), only \(q_z\) is zero. It is uniquely minimal throughout
\(|t-c_z|\le\theta^n/3\), intersected with \([0,1]\): its value is at most
\(\theta^{2n}/9\), whereas every other value is at least
\(4\theta^{2n}/(9C_\theta)\), which is larger.

**Theorem 2.** Every finite exact representation of \(V_n\) on \([0,1]\)
as a minimum of polynomial functions contains at least \(2^n\) distinct
polynomials. Every finite piecewise polynomial representation also needs at
least \(2^n\) distinct polynomial formulas.

**Proof.** Each \(q_z\) agrees with \(V_n\) on an ordinary open interval,
including a one-sided subinterval for the zero center. On that interval the
finitely many differences between representing polynomials and \(q_z\) have
zeros covering the interval. At least one difference is identically zero,
since a nonzero polynomial has only finitely many roots. Distinct centers
give distinct quadratics. The same argument applies to any finite piecewise
polynomial representation. \(\square\)

This is a count of necessary formulas, rather than candidate formulas before
dominance pruning. It permits arbitrary polynomial degrees. It does not
exclude short recursive or other symbolic representations.

Before conditioning the terminal state, the continuous quadratic matrix
\(K\), in the order \((x_1,s_1,\ldots,x_n,s_n)\), satisfies

\[
 (1-3\theta)I\preceq K\preceq(1+3\theta+2\theta^2)I.       \tag{4}
\]

Indeed, its nonzero off-diagonal entries are \(-\theta\) and \(\theta^2\).
Control diagonals and nonterminal state diagonals are \(1+\theta^2\);
the terminal state diagonal is one. The largest absolute off-diagonal row
sum is \(3\theta+\theta^2\), so Gershgorin proves (4). Its graph is a
bandwidth-two chain of triangles sharing individual state vertices, with an
initial pendant edge, maximum degree four, and pathwidth and treewidth two
for \(n\ge2\). The recurrence contraction coefficient is \(\theta\).

For fixed \(\theta\), every entry of \(K\), every linear coefficient, and
every indicator penalty belongs to a finite rational alphabet independent of
\(n\). There are \(O(n)\) nonzero coefficient entries. This gives an
\(O(n)\)-length description in the natural ordered chain representation;
an explicit sparse matrix format storing every row and column index can use
\(O(n\log n)\) bits. A dense matrix format costs more. The statement about
fixed coefficients does not depend on these encoding conventions. The small
scales \(\theta^n\) arise through propagation, not through tiny input data.

## Unit penalties on every continuous variable

An indicator of penalty one can also be attached to each state. Set
\(y_0=4\) and consider the objective

\[
 H=\sum_i(x_i^2-2x_i+z_i)
 +\sum_i[y_i-\theta y_{i-1}-\theta x_i-4(1-\theta)]^2
 +\sum_i\zeta_i,                                        \tag{5}
\]

with only the indicator constraints
\(x_i(1-z_i)=y_i(1-\zeta_i)=0\). The first residual simplifies to
\(y_1-\theta x_1-4\). Condition its message on \(y_n=4+t\), for
\(t\in[0,1]\).

**Proposition 3.** This conditional message is \(n+V_n(t)\).

**Proof.** Given \(z\), let \(s_0^z=0\) and
\(s_i^z=\theta s_{i-1}^z+\theta z_i\ge0\). Write
\(e=x-z\) and \(d=y-4\mathbf1-s^z\). The residual squares, including
the control squares, form \((e,d)^TK(e,d)\). If \(k\) state indicators
are zero, their \(d_i\le-4\), so (4) gives

\[
 H\ge n-k+16(1-3\theta)k\ge n+10.2k.
\]

An all-on state assignment with \(x=z=0\), \(y_i=4\) for \(i<n\),
and \(y_n=4+t\) costs \(n+t^2\le n+1\). Thus every optimum has
all state indicators on. Substitution \(s=y-4\mathbf1\) now proves the
claim. \(\square\)

The expanded continuous linear coefficients in (5) have magnitude at most
eight and belong to a fixed finite alphabet. The objective's additive constant
is at most \(16n\); it can be omitted without changing its optimizers or the
number of message formulas. Thus the construction has fixed local data and
unit penalties even in the pure indicator model. The terminal equality is
used to define a conditional message, not to claim that the unconditioned
model has additional coupling constraints.

## Horizon-independent approximation by pruning

For \(0\le m\le n\), call the first \(n-m\) bits the omitted prefix and
the last \(m\) bits the retained suffix. Define their maximum contributions

\[
 \delta_{n,m}=\sum_{j=m+1}^n\theta^j
 \le\frac{\theta^{m+1}}{1-\theta},\qquad
 \beta_{n,m}=\sum_{j=m+1}^n\theta^{2j}
 \le\frac{\theta^{2m+2}}{1-\theta^2}.                     \tag{6}
\]

Empty sums vanish. All retained formulas remain original support formulas;
in particular their common denominator contribution remains \(W_n\), not
\(W_m\). Approximations here remove support choices, not early residuals.

**Proposition 4.** Retaining only supports with zero omitted prefix gives a
minimum \(R^0_{n,m}\) of \(2^m\) original quadratics satisfying

\[
 0\le R^0_{n,m}(t)-V_n(t)\le2\delta_{n,m}+\beta_{n,m}
 \quad(t\in[0,1]).                                      \tag{7}
\]

**Proof.** Take a support \(z\) attaining \(V_n(t)\), and set its omitted
bits to zero to obtain \(z^0\). The center moves by at most \(\delta_{n,m}\)
and the denominator decreases by at most \(\beta_{n,m}\). Both centers
and \(t\) belong to \([0,1]\), so the squared numerators differ in
absolute value by at most \(2\delta_{n,m}\). Each denominator is at least
one, and the original numerator is at most one. Splitting the change into a
numerator change and a reciprocal-denominator change proves (7).
The lower bound follows because the retained supports form a subset.
\(\square\)

A better rate follows by allowing the omitted prefix to be either all zero
or all one.

**Theorem 5.** Retain those two prefix choices for every suffix. Their minimum
\(R^{\pm}_{n,m}\), using at most \(2^{m+1}\) original quadratics, satisfies

\[
 0\le R^{\pm}_{n,m}(t)-V_n(t)
 \le \frac{\delta_{n,m}^2}{4}+\beta_{n,m}
 \le A_\theta\theta^{2m+2},                              \tag{8}
\]

where

\[
 A_\theta=\frac1{4(1-\theta)^2}+\frac1{1-\theta^2}.
\]

**Proof.** Fix an optimal support \(z\), and let \(z^0,z^1\) be its
zero-prefix and one-prefix variants. Their centers \(c_0,c_1\) bracket
\(c_z\), with \(c_1-c_0=\delta_{n,m}\). Choose the endpoint center
closest to \(t\). If \(t\notin[c_0,c_1]\), its squared distance is no
larger than \((t-c_z)^2\). If \(t\in[c_0,c_1]\), its squared distance
is at most \(\delta_{n,m}^2/4\). In either case the selected numerator
\(N'\) satisfies

\[
 N'\le N+\delta_{n,m}^2/4,\qquad N=(t-c_z)^2\le1.
\]

The selected denominator \(D'\) is at least one and differs from \(D_z\)
by at most \(\beta_{n,m}\). Therefore

\[
 \frac{N'}{D'}-\frac{N}{D_z}
 \le\frac{\delta_{n,m}^2}{4D'}
   +N\frac{D_z-D'}{D'D_z}
 \le\delta_{n,m}^2/4+\beta_{n,m}.
\]

The retained minimum is no larger than this selected formula and is no smaller
than the full minimum. \(\square\)

## Matching accuracy exponent for support pruning

Let \(N_n(\varepsilon)\) be the smallest number of original support
quadratics whose minimum \(R\) satisfies
\(0\le R(t)-V_n(t)\le\varepsilon\) on \([0,1]\). Define

\[
 N_\theta(\varepsilon)=\sup_{n\ge1}N_n(\varepsilon),
 \qquad
 \alpha_\theta=\frac{\log2}{2\log(1/\theta)}.
\]

**Theorem 6.** As \(\varepsilon\downarrow0\),

\[
 N_\theta(\varepsilon)
   =\Theta_\theta\!\left(\varepsilon^{-\alpha_\theta}\right). \tag{9}
\]

**Proof of the lower bound.** For \(n\ge m\ge1\), the \(2^m\) supports
with zero omitted prefix have centers separated by at least \(\theta^m\).
The full message is zero at each center. Any retained quadratic with value at
most \(\varepsilon\) at such a center must have its own center within
\(\sqrt{C_\theta\varepsilon}\). If

\[
 \varepsilon<\frac{\theta^{2m}}{4C_\theta},               \tag{10}
\]

the corresponding neighborhoods of the selected zero points are disjoint.
One retained quadratic can therefore serve at most one selected zero, and
\(N_n(\varepsilon)\ge2^m\).

For sufficiently small \(\varepsilon\), choose

\[
 m=\left\lfloor
 \frac{\log(1/(8C_\theta\varepsilon))}{2\log(1/\theta)}
 \right\rfloor\ge1.
\]

Then (10) holds, and
\(N_\theta(\varepsilon)\ge\tfrac12
(8C_\theta\varepsilon)^{-\alpha_\theta}\).

**Proof of the upper bound.** Choose

\[
 m=\left\lceil
 \frac{\log(A_\theta\theta^2/\varepsilon)}{2\log(1/\theta)}
 \right\rceil\ge0
\]

for sufficiently small \(\varepsilon\). If \(n\le m\), retain every
support. If \(n>m\), use Theorem 5. In either case the required number is
at most
\(2^{m+1}\le4(A_\theta\theta^2/\varepsilon)^{\alpha_\theta}\), proving
(9). \(\square\)

The lower bound in Theorem 6 applies specifically to deletion of original
support formulas. Arbitrary new approximating quadratics, higher-degree
polynomials, or other representations are not covered. Its exponent describes
this constructed family, not all stable indicator dynamic programs.

The exact lower bound and the approximation theorem address different
questions. There are exponentially many exact wells, but propagation makes
late refinements very shallow. Unlike the first construction, all centers
do not shrink into a vanishing interval as \(n\) grows: their maximum tends
to \(\theta/(1-\theta)\). Instead they form progressively finer digit
patterns across a fixed small interval. Coarse pruning remains effective.

## Literature comparison and significance

Primary-source comparisons on 2026-09-22 include:

- Gaubert, McEneaney, and Qu,
  [Curse of dimensionality reduction in max-plus based approximation methods](https://arxiv.org/pdf/1109.5241),
  Section VI, independently inspected by the reviewer: pruning quadratic
  bases under uniform error is already treated as a continuous k-center
  problem. Thus neither the covering interpretation nor a power law for
  quadratic pruning is new. Here the separated binary digit set has covering
  exponent `log(2)/log(1/theta)`; squared-distance error explains the factor
  one half in the accuracy exponent. The model-specific contribution is its
  realization with fixed indicator data and the matching bound despite
  support-dependent denominators.

- Bhathena, Fattahi, Gómez, and Küçükyavuz,
  [A Parametric Approach for Solving Convex Quadratic Optimization with
  Indicators Over Trees](https://arxiv.org/html/2404.08178v1), gives an exact
  quadratic-time tree algorithm. Our graph contains triangles. A lower bound
  for retaining an entire conditional message also does not exclude an
  optimization algorithm using less information.
- The same authors,
  [Solving Convex Quadratic Optimization with Indicators Over Structured
  Graphs](https://arxiv.org/html/2603.02103v1), introduction and its account of
  structural and margin-dependent pruning, is the closest positive theory.
  Fixed graph width, conditioning, and coefficient magnitudes do not themselves
  prevent this example's exact message growth. We have not calculated the
  paper's exact margin parameter for the shifted construction, and claim no
  contradiction with its full hypotheses.

The [earlier message note](research-20260922-message-complexity.md) records
additional inspected sources on exponential growth of quadratic messages,
max-plus approximation, and multi-period indicator convexification. Those
comparisons carry over; this note does not claim that their entire priority
search was independently repeated. Exponential candidate growth, instability
of exact pruning near equal minima, and approximation by forgetting distant
history are established broad ideas. The possible contribution is their
precise simultaneous realization in a scalar, time-homogeneous, uniformly
well-conditioned pure-indicator model with fixed rational data, together with
the explicit matching pruning-accuracy exponent. No unsuccessful search proves
novelty, and the restricted theorem should remain a companion to the structural
hardness result rather than be presented as a new general complexity theory.

For solver theory, the construction gives a concrete stress test for guarantees
based only on graph width, conditioning, bounded local coefficients, or stable
dynamics. A valid general guarantee needs a quantitative distinction between
supports, an approximation allowance, or an interface that avoids storing the
full exact message. The proven approximation bound supplies such a distinction
only for this family. Extending it to useful heterogeneous indicator dynamics
requires further work.

The unconditioned fixed-data objective is easy to optimize: every control
support has a zero-residual trajectory with `x=z`, giving value zero. The
shifted state-indicator version has optimum `n`; the activation bound rules
out an improvement from switching states off. Thus this family establishes
complexity of a conditional message interface, not optimization hardness of
its unconditioned objective. The separate SUBSET SUM reduction is needed
for the hardness claim in the parent result.

## Targeted verification and its limits

The command run for this note was

```text
python3 code/research_20260922/check_constant_data_messages.py
PASS: 180 exact support QPs, 252 centers, 504 active-neighborhood endpoints, 6252 approximation checks; n=1..6, theta=1/10,1/20
```

The checker reuses the direct residual-row QP solver from the earlier check,
which solves rational normal equations independently of (2). It checks the
constant-coefficient formula on every support through horizon four, center
separation and active neighborhoods through horizon six, and both pruning
bounds at all centers, adjacent-center midpoints, and selected exterior
points. These are exact finite-instance checks. They do not prove the general
theorems, continuous-domain bounds, literature priority, or a lower bound for
general algorithms. Those distinctions are addressed by the proofs and
limitations above. No project-wide or CI verification was run. No Lean check
was needed to resolve a remaining proof uncertainty.
