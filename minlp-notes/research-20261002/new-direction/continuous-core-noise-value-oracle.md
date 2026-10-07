# A lazy continuous core-noise value oracle in arbitrary core dimension

Date: 2026-10-02. Status: fresh independent actual-file
[review passed](../reviews/continuous-core-noise-value-review.md);
targeted exact checks passed. This is a direct continuous-noise counterpart of the
[finite-law value theorem](core-only-noise-value-oracle.md), with a
different input model. It makes no publication-priority claim.

One fixed continuous uniform perturbation, represented by persistent
independent bitstreams, admits certified value evaluation at every
precision in arbitrary core dimension. Expected work has the usual
core-dimension and curvature/noise factors. No growth promise,
residual strong convexity, or algebraic fallback is needed. The result
concerns a random-real objective accessed through its coefficient bits;
it does not replace a theorem about one finite rational sampled instance.

## 1. Model and statement

Fix the polynomial degree `d`. Let `F_0(v,z)` be an explicit rational
polynomial on `[0,1]^k times [0,1]^m`, with verified bounds

\[
 \partial_{v_i v_i}F_0\le L\quad(1\le i\le k),\qquad
 \nabla^2_{zz}F_0\succeq0
                  \quad\hbox{throughout the product box},       \tag{1}
\]

where `L>=0` and the noise half-width `sigma>0` are rational. Include
the polynomial, dimensions, bounds, convexity certificates and their
verification costs in base input size `I`, as in the
[convex recourse theorem](smoothed-polynomial-box-recourse.md).
Arbitrary polynomial convexity recognition is not an uncharged step.

For each core coordinate take an independent stream of fair bits
`B_i1,B_i2,...`, and define one coefficient

\[
 U_i=\sum_{r\ge1}B_{ir}2^{-r},\qquad
 \gamma_i=\sigma(2U_i-1),\qquad
 F_\gamma(v,z)=F_0(v,z)+\gamma^Tv.                            \tag{2}
\]

These coefficients are independent continuous uniforms on
`[-sigma,sigma]`. The streams are fixed for all subsequent queries;
revealing further bits does not resample the coefficients. All-zero,
all-one, and dyadic-ambiguity streams still define valid objectives.
Correctness below holds for every bitstream, including these
probability-zero cases.

**Theorem.** For every requested integer `q>=0`, a finite computation
returns a rational feasible point `(v_q,z_q)` and rational bounds
`a_q,U_q` such that

\[
 a_q\le f_\gamma^*\le F_\gamma(v_q,z_q)\le U_q,
 \qquad U_q-a_q\le2^{-q}.                                   \tag{3}
\]

The bounds and point are correct for the same objective (2) at every
query. The upper bound need not equal the generally irrational
objective at that point. Only `O(k(I+q))` stream bits are needed per
query, counting previously revealed bits once when they are reused.
For `k>=1` and `L>0`, expected bit work and expected complete proof-record
length are at most

\[
 \left(2^k+8^k
       \left[2+\frac{(1+k)L}{2\sigma}\right]^k\right)
                         \operatorname{poly}_d(I+q).          \tag{4}
\]

The polynomial exponent is independent of `k`. The dependence on
`L/sigma` is numerical, not just through its bit length. The finite
answer and used coefficient prefixes have polynomial length in
`I+q` on every draw; the full cell trace has the expected bound (4).
There is also one finite-expected random work factor bounding all
query precisions at once, as shown in Section 5.

This is an exact optimal-value Cauchy oracle relative to the persistent
random tape. It promises neither distance to an optimizer nor
convergence of the feasible points to a selected optimizer. A finite
input string does not encode a typical coefficient in (2).

## 2. Finite prefixes give honest objective intervals

Let `m_i(b)` be the integer encoded by the first `b` bits of stream `i`.
For `b=0`, set `m_i(0)=0`. Every completion of that prefix satisfies

\[
 \underline\gamma_i(b)=\sigma(2m_i(b)2^{-b}-1)
 \le\gamma_i\le
 \overline\gamma_i(b)=\sigma(2(m_i(b)+1)2^{-b}-1).           \tag{5}
\]

The interval width is `2sigma 2^-b`. Both endpoints are rational.
These intervals are nested as bits are revealed.

Assume `k>=1` and `L>0`. At dyadic level `j`, use

\[
 h_j=2^{-j},\qquad e_j=kLh_j^2/8.                            \tag{6}
\]

Choose the least integer `b_j>=0` satisfying

\[
                    k\sigma 2^{-b_j}\le e_j/4.             \tag{7}
\]

This choice depends only on base data and the level, and
`b_j=O(I+j)`. The sequence is nondecreasing. A level always uses its
prescribed prefix length even if a previous, finer query has already
revealed more bits. This convention gives one canonical refinement
process for all query precisions.

At each rational core corner `v`, solve the unchanged convex residual
problem `min_z F_0(v,z)` to certified interval width `e_j/2`:

\[
 \ell_v^0\le V_0(v)\le u_v^0=F_0(v,z_v),\qquad
                       u_v^0-\ell_v^0\le e_j/2.             \tag{8}
\]

The verified
[value-only convex interface](smoothed-polynomial-box-recourse.md)
returns the rational feasible `z_v` and a checkable tangent lower
certificate in polynomial query bit time. Its proof uses convexity,
not a positive Hessian modulus. If `m=0`, evaluate directly.

Define the rational bounds

\[
 \ell_v=\ell_v^0+\underline\gamma(b_j)^Tv,
 \qquad u_v=u_v^0+\overline\gamma(b_j)^Tv.                    \tag{9}
\]

Since `v_i in [0,1]`, (7)--(9) imply, for every completion of the
revealed prefixes,

\[
 \ell_v\le V_\gamma(v)\le F_\gamma(v,z_v)\le u_v,
 \qquad u_v-\ell_v\le e_j.                                 \tag{10}
\]

The residual problem itself never changes with the revealed core
noise: that noise is constant during residual optimization. There is
no need to solve a succession of objectives and identify their
optimizers with an optimizer of a limiting objective.

## 3. Sound refinement and stopping on every stream

Start with the whole core box. At level `j`, generate all dyadic
children of previously retained cells, except that level zero consists
of the original single cell. Query all their corners by (8)--(9).
Shared corners may be queried repeatedly; their multiplicity is at
most `2^k`. Let `U` be the smallest upper bound seen so far and retain
the corresponding rational feasible point. For each generated cell set

\[
                 \mathrm{LB}(C)=\min_{v\in\mathrm{corners}(C)}
                                             \ell_v-e_j.   \tag{11}
\]

After all corner queries, make a second pass retaining precisely the
cells with `LB(C)<=U`, using the final incumbent. Use deterministic
oracle and list rules so a finer query extends the same refinement.

Independent coordinate rounding within a core cell increases the
expected objective by at most `e_j`, with a residual optimizer held
fixed. This follows from (1) and the sum of the rounding variances;
the linear noise adds no curvature. Consequently (11) is a lower
bound on the whole cell for every compatible coefficient vector.
All its global optima are preserved by pruning.

For any compatible noise vector, the cell containing an optimum has
a true corner value at most `f*+e_j`. Equation (10) gives

\[
                   U-f^*\le2e_j.                           \tag{12}
\]

For every current queried corner,
`ell_v>=u_v-e_j>=U-e_j`. Current cell bounds are therefore at least
`U-2e_j`. A previously discarded cell had a lower bound above its
then-current incumbent, which is at least the current `U`; its older
coefficient prefix contains every completion of the current prefix.
Thus the global interval

\[
                            [U-2e_j,U]                     \tag{13}
\]

is valid uniformly over all completions of the used coefficient
prefixes. The stored point has objective at most `U` for every such
completion. A verifier checks a finite statement about this whole
coefficient box; it need not perform exact arithmetic on a random real.

Every retained cell also has a corner whose true conditional value is
at most `U+2e_j<=f*+4e_j`. Choose the corner minimizing that cell's
lower bound to obtain this witness. This statement is pointwise for
the actual coefficient vector (2), regardless of how its approximate
queries affected the search.

For query `q`, stop at the least `J>=0` with `2e_J<=2^-q`.
It satisfies `J=O(I+q)`. Every level has finitely many dyadic cells,
so every query terminates on every stream, even on a stream giving
zero growth or a continuum of optimal cores. No cap, growth test,
or algebraic fallback is used.

## 4. Continuous-noise counting at every level

Fix a level `j` and a deterministic grid node `v`. A necessary condition
for `V_gamma(v)<=f*+delta`, with `delta=4e_j`, is that it beat each
feasible adjacent grid node up to `delta`. For an interior coordinate
these two tests imply

\[
 \frac{V_0(v)-V_0(v+h_je_i)-\delta}{h_j}
 \le\gamma_i\le
 \frac{V_0(v-h_je_i)-V_0(v)+\delta}{h_j}.                    \tag{14}
\]

The interval depends on `V_0` and the fixed node, not on any noise
coefficient. Holding a residual optimizer at `v` fixed proves

\[
 V_0(v-h_je_i)+V_0(v+h_je_i)-2V_0(v)\le Lh_j^2.
\]

Thus (14) has length at most

\[
                    Lh_j+2\delta/h_j=(1+k)Lh_j.             \tag{15}
\]

An empty interval has probability zero. For an interior node coordinate,
the probability of its necessary test is at most
`min(1,(1+k)Lh_j/(2sigma))`. Independence of the actual continuous
coefficients makes these probabilities multiply over interior
coordinates. Boundary coordinates require no test.

Writing `m_j=1/h_j`, summing over all deterministic nodes gives

\[
 \begin{aligned}
 \mathbb E[\#\{v:V_\gamma(v)\le f^*+4e_j\}]
 &\le\left[2+(m_j-1)
       \min\left(1,\frac{(1+k)Lh_j}{2\sigma}\right)\right]^k\\
 &\le H:=\left[2+\frac{(1+k)L}{2\sigma}\right]^k.           \tag{16}
 \end{aligned}
\]

This is the usual coordinate semiconcavity count. The adaptive queries
do not create a conditioning issue: each retained cell has a true
near-optimal witness, and (16) counts all deterministic nodes that
could be such witnesses. No conditional distribution given the
revealed prefixes is used in this count.

Each witness node is incident to at most `2^k` cells. The expected
retained count is at most `2^k H`; at the next level the expected
generated count is at most `4^k H`. Including at most `2^k` corner
queries per cell gives at most `8^k H` expected queries per level,
apart from the first level's `2^k` queries. There is no finite-noise
atom term and no condition relating a mesh to a fixed sampling grid.

## 5. Bit work, common all-precision bound, and certificates

A level-`j` core corner has `O(j)` coordinate bits, and the coefficient
prefixes have `O(I+j)` bits. Substitution into a fixed-degree explicit
polynomial, the residual value solve to error `e_j/2`, and the tangent
certificate all have polynomial query bit cost in `I+j`. Cells can be
generated and filtered in linear list time, with their corner factor
`2^k` explicitly charged. There is no quadratic operation on the list.
Summing (16) through `J=O(I+q)` proves (4).

A common bound for all `q` also follows. Define the canonical infinite
refinement using the prescribed prefixes and deterministic oracle rules.
Let `N_j` be its generated cell count, and set

\[
                        R=\sum_{j\ge0}\frac{N_j}{(j+1)^2}.  \tag{17}
\]

Tonelli's theorem and the preceding count give
`E R<=2(1+4^k H)`, so `R` is finite almost surely. For a fixed
polynomial per-corner cost bound `P_d`,

\[
 \sum_{j=0}^{J}2^kN_j P_d(I+j)
       \le2^kR(J+1)^2P_d(I+J).                             \tag{18}
\]

The right-hand side is one random work factor times a polynomial in
`I+q`, simultaneously for every query precision. This random factor
need not be computed. On the exceptional streams where it is infinite,
each individual finite query still terminates and is correct.

The finite proof record includes coefficient prefixes, convex tangent
certificates, the cell refinement and pruning decisions, and (13).
Its verifier checks bounds for every coefficient completion of those
prefixes under the verified premises (1). The record's expected length
obeys (4). The point and final rational interval alone have polynomial
bit length on every stream. The evaluator can rerun the canonical
refinement at each query or keep its finite completed portion.

## 6. Degenerate cases and significance

For `k=0`, there is no core noise: ordinary convex value evaluation
proves (3). If `L=0` and `k>0`, coordinate endpoint rounding never
increases expected cost. The global optimum is therefore the minimum
of the residual values at the `2^k` core vertices, for every real noise
vector. Solve each residual value to interval width `2^-q/2`, and
reveal enough coefficient bits to make their linear contribution's
interval width at most `2^-q/2`. Taking the minimum lower and upper
endpoints gives (3) in `2^k poly_d(I+q)` deterministic work.

The proof combines established convex value evaluation and the existing
continuous semiconcavity grid count. The extra bookkeeping is that
finite rational calculations certify one persistent random-real
objective, uniformly over unrevealed bits. It is a simpler counterpart
to finite-law results, not a new anti-concentration principle.

The separately reviewed
[all-scale finite-law theorem](all-scale-core-value-oracle.md) now also
handles arbitrary core dimension, using a geometric all-scale bound and
exact fallback while retaining a rational sampled instance. The present
note is a simpler model comparator with no fallback, rather than the
only arbitrary-dimensional value result.

Replacing each stream by one fixed finite rational coefficient would
change the model and remove the atom-free count at sufficiently fine
levels. This note does not make that replacement. Nor does it give
point accuracy for the residual minimizer: the
[Square Root Sum](convex-point-radical-comparison.md) and
[PosSLP](posslp-convex-point-extraction.md) point-output implications
remain compatible with this value-only result.

## Verification status

The exact diagnostic
[check_continuous_core_value.py](check_continuous_core_value.py) uses
dimensions one, two and three, with
`F_0=sum_i(v_i-1/3)^2+(z-v_1/2)^4`. The residual is convex but has
zero Hessian at its optimum. Conditional values and constrained core
minima are known exactly, so the checker can independently verify
the computed lower bounds and retained witnesses.

Endpoint streams, both encodings of dyadic coefficients and repeating
binary streams exercise nested coefficient prefixes. The
[saved results](continuous-core-value-results.json) record 33 levels,
417 generated cells, 63 prefix enclosures, 16,716 corner-completion
checks, 2,466 cell lower-bound checks, 1,390 retained-witness checks,
510 true-noise interval checks and 144 global prefix certificates.
The diagnostic checks coefficient-box vertices against the fixture's
exact value function; this enumeration is not a step of the proposed
algorithm. It is not a stochastic runtime estimate or an implementation
of the general convex solver.

The command actually run was:

```
python research-20261002/new-direction/check_continuous_core_value.py
```

The coefficient-prefix, rounding, counting and common-work-factor
arguments passed the saved
[fresh actual-file review](../reviews/continuous-core-noise-value-review.md).
Scoped local-link, equation-tag, delimiter, whitespace, Python-syntax
and JSON checks also passed, as did scoped `git diff --check`.
No index edits, project-wide checks or CI inspection were used.
