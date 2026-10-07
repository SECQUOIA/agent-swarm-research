# Exact mixed box QP through strong-field persistence and random components

Date: 2026-10-02. Status: direct theorem with a
[fresh independent actual-file review](../reviews/strong-field-component-qp-review.md)
finding no substantive gap, and targeted exact checks passing. A
completed [primary-source comparison](../prior-art/strong-field-component-qp-prior.md)
is available. Monotonicity, connected-set counting,
and stationary-face enumeration are standard ingredients. No priority or
practical performance claim is made.

## 1. Result and the noise restriction

Let

\[
 F_0(x)=\tfrac12x^THx+b^Tx+c
\]

have rational symmetric `H` on a bounded mixed product box. An input
matrix may first be replaced by `(H+H^T)/2`. Coordinates are
continuous intervals or native-integer intervals. Round integer bounds
inward, reject empty domains, and substitute fixed coordinates. Write
`I` for the original base input encoding length together with its
polynomial-size preprocessing/substitution data, including a rational
noise half-width `sigma>0`. In particular, `I` counts coordinates that
are later fixed and reinserted in the output. The graph has edge `ij` exactly when
`i!=j` and `H_ij!=0`; let `Delta` be its maximum degree. Isolated
variables can be solved directly as univariate quadratic problems, so
assume the remaining graph has `Delta>=1`. No tree decomposition is
required.

Choose a power of two `M>=2`, and draw independently

\[
 \gamma_i\in\{-\sigma+2\sigma k/(M-1):k=0,\ldots,M-1\}.     \tag{1}
\]

The target is the sampled objective `F_gamma=F_0+gamma^T x`.
Let `ell_i,u_i` be its original effective box bounds, `w_i=u_i-ell_i`,
and compute the exact base derivative interval on the continuous hull:

\[
 m_i=\min_x\partial_iF_0(x),\quad
 M_i=\max_x\partial_iF_0(x),\quad
 R_i=M_i-m_i=\sum_j|H_{ij}|w_j.                              \tag{2}
\]

The symbols `M_i` in (2) are derivative maxima; `M` in (1) is the
number of noise atoms. All quantities in (2) are obtained by independent
endpoint choices in an affine function, with rational arithmetic.

Define

\[
 a_i=\begin{cases}3,&i\text{ continuous},\\
 u_i-\ell_i+1,&i\text{ native integer},\end{cases}
 \qquad
 q_i=\Pr\{\gamma_i\in[-M_i,-m_i]\},\quad
 \beta=\max_i a_iq_i.                                      \tag{3}
\]

Each `q_i` is exactly computable by counting the grid indices in one
rational interval, without listing the noise grid.

**Theorem.** There is an algorithm returning an exact rational global
optimizer and value on every draw. If `4 Delta beta<1`, its expected
bit work is at most

\[
 \operatorname{poly}(I+\log M)
 \left[1+\frac{\sum_i a_iq_i}{1-4\Delta\beta}\right].       \tag{4}
\]

The polynomial exponent is absolute. The algorithm does not assume
growth, uniqueness, a bound on negative inertia, or a bound on integer
dimension. It uses no resampling and no separate exceptional-draw
algorithm. Large unfixed components are solved by the same exact rule
as small ones.

A simple sufficient regime is

\[
 \sigma\ge8\Delta\max_i(a_iR_i),\qquad
 M\ge16\Delta\max_i a_i.                                  \tag{5}
\]

Indeed the uniform finite-grid interval bound gives

\[
 q_i\le\frac{R_i}{2\sigma}+\frac1M,
 \qquad a_iq_i\le\frac1{8\Delta}.                          \tag{6}
\]

Thus (4) is polynomial in the input and sampling bits under (5).
Take the least power of two satisfying its second inequality; its bit
length is polynomial even for binary-encoded integer widths.

For a continuous/binary model, every `a_i<=3`; the sufficient condition
is `sigma>=24 Delta max_i R_i` and `M>=48 Delta`. This is a material
strong-noise condition on the entire derivative variation, including
diagonal curvature and neighbor effects. It is not the weaker regime
of the [sparse smoothed theorem](sparse-bag-cell-smoothed-miqp.md), and
does not give a treewidth-free guarantee for arbitrary noise strengths.
For large native-integer intervals, (5) also scales with their numerical
label counts. Those costs have not disappeared; the stronger noise
makes expensive enumeration sufficiently rare.

## 2. Certified coordinate persistence

Call coordinate `i` bad when the event in (3) occurs. Otherwise:

- If `gamma_i>-m_i`, its derivative is strictly positive throughout
  the full continuous box, so every global optimizer has `x_i=ell_i`.
- If `gamma_i<-M_i`, its derivative is strictly negative throughout
  that box, so every global optimizer has `x_i=u_i`.

These conclusions also hold for native integers by monotonicity between
successive labels. They hold independently of all other noise values
and all later choices. Assign every nonbad coordinate to its certified
bound. Equality cases remain bad; no finite-grid atom is discarded.

The bad events depend only on their respective noise coefficients and
the fixed base data. They are therefore independent Bernoulli events,
with the exactly specified probabilities `q_i`. This independence would
not follow for an adaptive test whose interval depended on other noise;
such tests are unnecessary for the theorem.

After substituting the certified coordinates, the remaining quadratic
splits over the connected components of the bad induced subgraph. There
are no cross terms between two different components. Optimize them
separately and combine their solutions with the fixed bounds. This
produces a global optimizer of the original sampled problem, since every
global optimizer survived the substitutions.

## 3. Exact work on a component

For a component `C`, enumerate its integer labels and, for each continuous
coordinate, one of three states: original lower bound, free, or original
upper bound. There are at most

\[
                           A(C)=\prod_{i\in C}a_i             \tag{7}
\]

configurations. In a configuration, substitute all fixed coordinates.
If the free continuous Hessian is nonsingular, solve its stationary
linear system and retain the solution if it lies in the prescribed box.
The empty free set is included. Evaluate every retained point exactly
and take the least objective value. Testing all KKT signs is not needed:
every retained point is feasible, so an extra stationary saddle cannot
lower the answer below the true optimum.

At least one global optimum is enumerated, including for degenerate
quadratics. Fix an optimal integer assignment and choose a continuous
global minimizer with the smallest number of coordinates strictly
between their bounds. On its free face, stationarity holds and the
restricted Hessian is PSD. If it were singular, a nonzero null vector
would preserve the objective along a line from this minimizer until a
coordinate reaches a bound. This contradicts minimality of its free
face. Thus this Hessian is nonsingular, unless the free set is empty.
No genericity assumption is used.

Each rational solve, feasibility test, and objective comparison has bit
work polynomial in `I+log M`, with an absolute exponent. Substitution
of integer labels and pinned bounds preserves polynomial encoding
length. Cramer's rule on a stationary system of order at most the input
dimension bounds every candidate's encoding length by the same type
of polynomial. This argument includes nonoptimal candidates.
Consequently component work is at most

\[
                   A(C)\operatorname{poly}(I+\log M).        \tag{8}
\]

Its returned optimizer and value have polynomial binary length on every
draw, not merely in expectation. Univariate components can instead be
solved directly by checking endpoints and the continuous stationary
point or its nearest integer labels; this only improves (8).

## 4. Expected component cost

For a fixed vertex `v`, the number of connected vertex sets of size `k`
containing `v` is at most

\[
                         (4\Delta)^{k-1}.                    \tag{9}
\]

For a direct proof, give each such set a deterministic rooted ordered
spanning tree. There are at most `4^(k-1)` rooted ordered tree shapes,
and at most `Delta^(k-1)` choices of neighbor labels along its edges.
Permitting repeated labels only enlarges this count. The canonical
tree encodes its original vertex set, so this is an upper bound.

For any connected set `S`, the probability that it is an entire bad
component is at most the probability that all its vertices are bad,
namely `product_(i in S) q_i`. Conditions on its exterior can be omitted
for an upper bound. Therefore

\[
\begin{split}
 \mathbb E\sum_{C\text{ bad component}}A(C)
 &\le\sum_{S\text{ nonempty connected}}\prod_{i\in S}a_iq_i\\
 &\le\sum_v\sum_{S\ni v\text{ connected}}\prod_{i\in S}a_iq_i\\
 &\le\sum_v a_vq_v\sum_{k\ge1}(4\Delta\beta)^{k-1}\\
 &=\frac{\sum_v a_vq_v}{1-4\Delta\beta}.                    \tag{10}
\end{split}
\]

The second inequality deliberately overcounts a set once per vertex.
Only independence of the original bad events is used. Combining (8)
with the polynomial preprocessing and graph traversal proves (4).

The exact probabilities in (3) can be much smaller than the bound (6),
for example when the base linear coefficient already pushes a derivative
interval away from the noise support. Condition `4 Delta beta<1` can
therefore certify the expected-work bound beyond the simple sufficient
regime (5). If it fails, the algorithm is still exact, but this theorem
gives no useful expected complexity guarantee.

## 5. Scope, certificates, and further questions

The output is for the sampled objective. Original-objective loss can
still be bounded by `sigma sum_i w_i`, but (5) may make that bound
large. This is a distinct strong-field capability, not a general
improvement over the sparse polynomial theorem's noise dependence.

Each returned solution has a direct global proof record: the derivative
intervals and pinned bounds, the resulting component partition, and the
component stationary-face/label enumerations. A verifier can repeat
these checks within the same realized-work bound. Certificate soundness
does not rely on (5), independence, or the expectation calculation.
Those conditions bound only the expected cost of discovering and checking
the exact answer.

The product domain is essential to both coordinate monotonicity and
component separation. General coupling constraints are not covered.
Extending this mechanism to fixed-degree polynomials requires a component
solver with cost exponential in its dimension with a constant base
depending on degree, and polynomial dependence on new coefficient bits,
or a separately justified probability budget for a more expensive
degenerate fallback. The existing deliberately loose algebraic fallback
bound `2^poly(component size)` is insufficient: exponential component
tails do not generally pay for that cost. No polynomial extension is
asserted here.

## Verification and attribution status

The argument uses standard persistence, elementary random-component
counting, and exact rational QP face enumeration. A focused primary-source
comparison on random-field pinning, percolation, and smoothed component
algorithms is recorded in the linked audit. The
[completed review](../reviews/strong-field-component-qp-review.md)
checks the probability calculation, singular-face completeness,
arithmetic, all-draw output, and strong-noise scope. It requested two
clarifications, now applied: explicit symmetry of the Hessian and an
input-length convention that counts preprocessing and reinserted fixed
coordinates.

The author ran

```sh
python3 -B research-20261002/new-direction/check_strong_field_components.py
```

The [persistent exact checker](check_strong_field_components.py) passed
324 same-draw comparisons between component optimization and exhaustive
whole-instance stationary-face/label enumeration. Fixtures include mixed
domains, indefinite Hessians, offset rational bounds, and finite-noise
threshold equalities. Two additional singular-Hessian fixtures have known
optimal values and nonunique optimizers. The same enumerator is reused
on components and whole instances, so these comparisons test persistence
and separation rather than independently proving the enumerator.

Separately, 96 bad-site patterns on a path, clique, and star were summed
with exact probabilities. All three expected-cost bounds passed,
including unequal integer-label weights and positive endpoint-atom
probabilities. These finite checks do not prove the general connected-set
count. The reviewer read and reran that checker, then independently
checked eight weighted-component expectations, including fixtures with
81-bit integer-label counts. No project-wide checks, CI inspection, or
root-index edits are part of this derivation.
