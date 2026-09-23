# Exponentially many necessary quadratics in a scalar indicator message

Date: 2026-09-22. Status: proof and independent rational checks of a proposed
consequence of [the bandwidth-two construction](../results/indicator-quadratic-treewidth-two-hardness.md).
This note was written by a separate research agent asked to challenge the
coordinator's candidate. The exact priority of the restricted construction is
unsettled. Exponential growth of quadratic representations in dynamic
programming is established background, not the novelty claim.

The useful conclusion is specific: even a scalar exact Bellman message for a
uniformly well-conditioned, stable, bandwidth-two indicator quadratic problem
can require exponentially many distinct quadratics. All of them remain
necessary on a fixed bounded parameter interval. The phenomenon persists with
unit indicator penalties and bounded coefficients. Small separators alone do
not make an explicit exact message small.

This is a representation lower bound. It is not an unconditional lower bound
for arbitrary optimization algorithms, and the example becomes easy to
approximate at fixed additive accuracy. The two qualifications are essential.

## Construction and exact formula

Fix a rational number \(0<\theta\le1/10\) and integer \(n\ge1\). Set

\[
 a_i=2^{i-1},\quad M=2^n-1,\quad
 b_i=\frac{a_i\theta^i}{M},\quad
 h=\frac{\theta^n}{M},\quad w_i=\theta^{n-i}.
\]

Thus \(0<b_i\le\theta^i\le\theta\). Define the terminal-state value
function, for \(t\in[0,1]\), by

\[
 V_n(t)=\min\left\{
 \sum_{i=1}^n(x_i^2-2x_i+z_i)
 +\sum_{i=1}^n(s_i-\theta s_{i-1}-b_ix_i)^2:
 \begin{array}{l}
 x_i(1-z_i)=0,\ z_i\in\{0,1\},\\
 x,s\text{ real},\ s_0=0,\ s_n=t
 \end{array}\right\}.                                      \tag{1}
\]

The first term equals \((x_i-z_i)^2\) on the indicator-feasible set.
This identity is not asserted outside that set; the actual continuous
quadratic matrix in (1) does not depend on the indicators. Existence of a
minimum also follows from the formula below, or from coercivity on each
of the finitely many supports.

For \(z\in\{0,1\}^n\), put

\[
 t_z=\sum_iw_ib_iz_i=h\sum_i2^{i-1}z_i,\qquad
 D_z=\sum_iw_i^2+\sum_iw_i^2b_i^2z_i.                       \tag{2}
\]

**Proposition 1.** The exact fixed-support value and overall value are

\[
 q_z(t)=\frac{(t-t_z)^2}{D_z},\qquad
 V_n(t)=\min_{z\in\{0,1\}^n}q_z(t).                        \tag{3}
\]

**Proof.** For a fixed support, define
\(e_i=x_i-z_i\) and \(r_i=s_i-\theta s_{i-1}-b_ix_i\).
When \(z_i=0\), \(e_i=0\) is required. Iterating the state recurrence
gives the single residual constraint

\[
 t-t_z=\sum_{i:z_i=1}w_ib_ie_i+\sum_iw_ir_i.                \tag{4}
\]

Conversely, every pair \((e,r)\) satisfying (4) and the inactive-coordinate
restrictions yields a feasible point: set \(x=z+e\) and reconstruct states
recursively from \(s_0=0\). Equation (4) gives \(s_n=t\).
The fixed-support objective is \(\sum_i e_i^2+\sum_i r_i^2\).
Cauchy--Schwarz gives its lower bound \((t-t_z)^2/D_z\).
Equality is attained by

\[
 e_i=\frac{t-t_z}{D_z}w_ib_iz_i,\qquad
 r_i=\frac{t-t_z}{D_z}w_i.                                \tag{5}
\]

The residual reconstruction just described verifies feasibility of the
equality case, rather than treating Cauchy--Schwarz only as a lower bound.
This proves (3). \(\square\)

The function is a scalar Bellman message in the usual precise sense. With
\(V_0(0)=0\) and \(V_0(u)=+\infty\) for \(u\ne0\), its prefixes obey

\[
 V_i(t)=\min_{u,x,z:\ x(1-z)=0,\ z\in\{0,1\}}
 \{V_{i-1}(u)+x^2-2x+z+(t-\theta u-b_ix)^2\}.             \tag{6}
\]

Here the coefficients of each prefix are inherited from the fixed
\(n\)-period instance; they need not be renormalized for that prefix.

## Every quadratic is necessary

The centers in (2) are exactly

\[
 \{0,h,2h,\ldots,Mh\}=\{0,h,2h,\ldots,\theta^n\}.
\]

At \(t=t_z\), \(q_z(t)=0\), whereas \(q_{z'}(t)>0\) for every
\(z'\ne z\). Thus every support uniquely minimizes at a different point.
Continuity gives a nonempty open interval on which each quadratic alone is
active. At zero, this means an interval open relative to \([0,1]\), which
contains an ordinary open subinterval of positive numbers.

There is also a uniform explicit interval. Define

\[
 C_\theta=\frac{1+\theta^2}{1-\theta^2}<2.
\]

Since \(w_n=1\) and \(b_i\le\theta\),

\[
 1\le D_z\le C_\theta.                                   \tag{7}
\]

If \(|t-t_z|\le h/3\), then

\[
 q_z(t)\le h^2/9,\qquad
 q_{z'}(t)\ge\frac{4h^2}{9C_\theta}>h^2/9\quad(z'\ne z).
                                                                  \tag{8}
\]

These inequalities apply on the intersection of that neighborhood with the
parameter domain. In particular, no support is an artifact that can be
removed by exact dominance pruning on \([0,1]\).

**Theorem 2.** Every finite representation

\[
 V_n(t)=\min_{j=1}^K p_j(t)\qquad(t\in[0,1])              \tag{9}
\]

by polynomial functions contains at least \(2^n\) distinct polynomials.
In particular this holds for arbitrary quadratic polynomials, even if they
are not the quadratics obtained by fixing supports. Every finite piecewise
quadratic representation on intervals likewise uses at least \(2^n\)
distinct quadratic formulas.

**Proof.** Fix an ordinary open interval \(I_z\subseteq[0,1]\) where
\(V_n=q_z\). For each \(t\in I_z\), at least one \(j\) satisfies
\(p_j(t)-q_z(t)=0\). If none of these polynomial differences were
identically zero, each would have only finitely many roots; their finite
union could not cover \(I_z\). Hence some \(p_j\) equals \(q_z\)
identically. The quadratics \(q_z\) are distinct because their unique
zeros are distinct. Apply this argument to every support.
For a finite piecewise representation, at least one interval piece intersects
\(I_z\) in an open interval, so the same polynomial identity argument applies.
\(\square\)

The theorem counts distinct formulas, not merely intervals created by an
unfortunate implementation. It does not exclude a short symbolic expression
with recursion, integer operations, special functions, or optimization calls.

## Conditioning, graph structure, and the unit-penalty lift

Before imposing the terminal boundary, the homogeneous continuous quadratic
form is

\[
 \sum_i x_i^2+\sum_i(s_i-\theta s_{i-1}-b_ix_i)^2=v^TKv,
 \qquad v=(x_1,s_1,\ldots,x_n,s_n).                        \tag{10}
\]

Its off-diagonal entries are \(-b_i\) on \(x_i,s_i\), \(-\theta\)
on \(s_{i-1},s_i\), and \(\theta b_i\) on \(s_{i-1},x_i\).
All other entries vanish. Its graph is the same bandwidth-two chain of
triangles as in the parent result, with maximum degree four and treewidth
and pathwidth exactly two for \(n\ge2\). The triangles share single states.
The terminal boundary is a conditioning operation used to form a message,
not an additional claim about the graph after removing the terminal variable.

An \(x_i\) row has diagonal \(1+b_i^2\) and absolute off-diagonal sum
at most \((1+\theta)b_i\). An internal state row has diagonal
\(1+\theta^2\) and absolute off-diagonal sum at most
\(2\theta+b_i+\theta b_{i+1}\le3\theta+\theta^2\).
The last state row has diagonal one and row sum at most \(\theta+b_n\).
Gershgorin therefore gives

\[
 (1-3\theta)I\preceq K\preceq(1+3\theta+2\theta^2)I,
 \qquad \|K-I\|_2\le4\theta.                             \tag{11}
\]

All continuous principal subproblems inherit these spectral bounds. The
linear state recurrence has contraction coefficient \(\theta\).
The input coefficients have bounded magnitudes and polynomial binary
encoding length for fixed rational \(\theta\), but some are exponentially
small. The exponent \(n\) in the message count is proportional to the number
of variables; no claim of \(2^{\Omega(L)}\) growth in total binary input
length \(L\) is intended.

To put an indicator of penalty one on every state as well, replace the states
by variables \(y_i\) with indicators \(\zeta_i\), set \(y_0=4\), and use

\[
 H=\sum_i(x_i^2-2x_i+z_i)
 +\sum_i[y_i-\theta y_{i-1}-b_ix_i-4(1-\theta)]^2
 +\sum_i\zeta_i,                                        \tag{12}
\]

with only \(x_i(1-z_i)=y_i(1-\zeta_i)=0\) and binary indicators.
The first residual in (12) is \(y_1-b_1x_1-4\), since \(y_0=4\).
For this objective, define the conditional message by fixing
\(y_n=4+t\), \(t\in[0,1]\). The original model before conditioning has
no coupling constraints, all penalties one, and the quadratic matrix (10).

**Proposition 3.** This conditional message equals \(n+V_n(t)\).

**Proof.** For a fixed \(z\), let \(s_0^z=0\) and
\(s_i^z=\theta s_{i-1}^z+b_iz_i\). These states are nonnegative.
Write \(e=x-z\) and \(d=y-4\mathbf1-s^z\). The sum of residual
squares in (12), including the \((x_i-z_i)^2\) terms, is at least
\((1-3\theta)(\|e\|^2+\|d\|^2)\) by (11).
If \(k\) state indicators are off, their states equal zero, so the
corresponding \(d_i\le-4\). Consequently

\[
 H\ge n-k+16(1-3\theta)k\ge n+10.2k.                    \tag{13}
\]

An all-on feasible candidate with \(z=x=0\), \(y_i=4\) for \(i<n\),
and \(y_n=4+t\) has value \(n+t^2\le n+1\). Thus every minimizer
has \(k=0\). Substituting \(s_i=y_i-4\) leaves precisely \(n\) plus
the objective and boundary condition of (1). \(\square\)

In (12), continuous linear coefficients have absolute value at most eight:
write \(h_1=4\), \(h_i=4(1-\theta)\) for \(i>1\); the \(x_i\)
coefficient is \(-2+2h_ib_i\), internal state coefficients are
\(-2h_i+2\theta h_{i+1}\), and the last is \(-2h_n\).
The constant is at most \(16n\). Thus the state-indicator lift does not
explain the message size by large coefficients or tiny indicator penalties.

## Precision limitation and a short approximation

At \(t_z\), removing the corresponding support quadratic from (3) raises
the envelope by at least \(h^2/C_\theta\). Therefore a method restricted
to deleting original support quadratics must keep all of them if it demands
a smaller uniform additive error. This statement concerns deletion alone;
it does not cover constructing new approximating functions.

In contrast, the following two-piece function is a very accurate approximation:

\[
 \widetilde V_n(t)=
 \begin{cases}
 0,&0\le t\le\theta^n,\\
 q_{\mathbf1}(t),&\theta^n\le t\le1.
 \end{cases}                                             \tag{14}
\]

On the first interval, choose a nearest center, whose distance is at most
\(h/2\), and use \(D_z\ge1\) to get \(0\le V_n(t)\le h^2/4\).
On the second interval, the all-ones support has both the largest center
and the largest denominator. For every other support, the nonnegative
distance to its center is larger and its denominator is smaller. Hence
\(V_n=q_{\mathbf1}\) there. Therefore

\[
 0\le V_n(t)-\widetilde V_n(t)\le h^2/4
 \quad\text{for every }t\in[0,1].                        \tag{15}
\]

The function (14) is continuously differentiable at its single breakpoint.
It is a piecewise quadratic approximation, not a minimum of its two formulas
over the entire domain. Even the single quadratic \(q_{\mathbf1}\)
approximates the message from above with uniform error at most \(\theta^{2n}\).
Thus a claim of exponential representation size at fixed additive accuracy
would be false for this family. All exact wells fit inside \([0,\theta^n]\),
and their depth scale is exponentially small.

## Literature examined and the precise contribution boundary

The following openly accessible primary sources were inspected on 2026-09-22.
Source comparisons below distinguish a count of candidate quadratics from a
proof that every one is necessary.

| Source and inspected part | Relevant result and comparison |
| --- | --- |
| Bhathena, Fattahi, Gómez, Küçükyavuz, [A Parametric Approach for Solving Convex Quadratic Optimization with Indicators Over Trees](https://arxiv.org/html/2404.08178v1), Proposition 1, Lemma 3, and the tree algorithm | Gives a quadratic-time exact algorithm on a tree, using conjugates and controlled growth of appropriate pieces. Their discussion explicitly distinguishes retaining the full function from the information needed for optimization. Our graph has triangles. The present theorem concerns an exact conditional message, not the complexity of every possible equivalent optimization representation. |
| Bhathena, Fattahi, Gómez, Küçükyavuz, [Solving Convex Quadratic Optimization with Indicators Over Structured Graphs](https://arxiv.org/html/2603.02103v1), introduction, Definition 5, Lemma 9, Theorem 1 | Develops quadratic parametric messages and exact pruning under a margin bound on nearly optimal supports. This is the closest direct positive theory. The construction here realizes all \(2^n\) support quadratics as necessary on a bounded scalar domain despite bounded conditioning and graph growth. We have not evaluated their exact margin definition on the shifted all-indicator construction, so no claim that a specified margin parameter alone must grow is made. |
| Kuric, Ahmetspahic, Pock, [Total Generalized Variation on a Tree](https://epubs.siam.org/doi/10.1137/23M1556915), §§2 and 5 | Studies continuous messages for piecewise quadratic unary and pairwise costs and gives exponential worst-case complexity for its general nonconvex algorithm. This is relevant existing literature on message growth outside indicator models. Its model permits nonconvex local costs, while our unreduced continuous objective is a single strictly convex quadratic with uncoupled zero indicators. The inspected result is not a theorem about near-identity indicator Hessians or indispensability of this family of support quadratics. |
| McEneaney and Deshpande, [Payoff Suboptimality and Errors in Value Induced by Approximation of the Hamiltonian](https://skoge.folk.ntnu.no/prost/proceedings/cdc-2008/data/papers/1672.pdf), introduction and references 12–15 | Already describes exponential growth with the number of quadratic Hamiltonians and propagation steps in max-plus HJB methods, and pruning as a response. The general phenomenon of quadratic-basis growth is therefore old. The narrow issue here is an explicit lower bound surviving exact pruning under the specified indicator, graph, coefficient, and conditioning restrictions. |
| Lee, Gómez, Atamtürk, [Convexification of multi-period quadratic programs with indicators](https://link.springer.com/article/10.1007/s10107-026-02379-5), introduction, §2, Proposition 8 | Gives polynomial formulations and algorithms for positive definite factorizable or block-factorizable quadratic matrices obtained from its dynamics model. This does not follow merely from stable dynamics. In our scalar construction, eliminating the free internal states leaves continuous quadratic matrix \(I+uu^T/W\), where \(u_i=w_ib_i>0\) and \(W=\sum_iw_i^2\). Its inverse \(I-uu^T/(W+u^Tu)\) has every off-diagonal entry nonzero. For \(n\ge3\) this is not tridiagonal and so is not scalar factorizable, whose inverse is tridiagonal. No contradiction to their scalar theorem follows. A claim concerning all possible block reformulations would require further analysis. |

Searches also used “piecewise quadratic exponential dynamic programming”,
“min-plus quadratic exponential switched systems”, and “curse of complexity”.
The searches do not prove novelty. The lower-bound argument itself is
elementary once the residual encoding is identified. The potentially useful
addition is the simultaneous set of restrictions and the exact-pruning
obstruction, together with its sharp separation from coarse approximation.
This is best treated as a companion theorem explaining the structural hardness
result, not as a new general theory of Bellman complexity.

## Verification and remaining work

The separate reviewer re-derived the residual equality case, checked inactive
coordinates, checked the endpoint intervals, replaced a candidate-count claim
by the stronger polynomial-identity argument, checked the state activation
lift, and established the short approximate representation to challenge broad
algorithmic interpretations.

The targeted command actually run was

```text
python3 code/research_20260922/check_message_complexity.py
PASS: 724 exact support QPs, 124 centers, 248 neighborhood endpoints; n=1..5, theta=1/10,1/20
```

The checker assembles fixed-support least-squares problems directly from the
original residual rows and solves their normal equations by rational Gaussian
elimination. It compares their exact values with (3), checks grid centers and
the omission gap, checks the explicit active-neighborhood endpoints, and checks
the short approximation at grid midpoints and selected exterior points. This
is independent finite-instance evidence for the formula. It does not verify
arbitrary \(n\), literature priority, the all-state activation proof, or a
general algorithmic lower bound. The general mathematical proofs above supply
the first and state activation conclusions. No project-wide or CI checks were
run, and no Lean formalization was attempted because the proof uses only a
single residual constraint, Cauchy--Schwarz, and polynomial identities.

A consequential next step would be an exact characterization of when local
sign structure, quantitative separation, or an alternative message interface
prevents this growth. The present construction suggests testing any proposed
criterion on exponentially close equal-depth wells. Turning such a criterion
into a useful solver guarantee requires further theory; this note establishes
the obstruction, not that positive algorithmic result.
