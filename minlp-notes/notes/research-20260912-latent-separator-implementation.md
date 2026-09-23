# Latent-separator design prototype and initial experiments

Date: 2026-09-12. Status: separate numerical prototype; author validation and
[independent theory review](research-20260912-latent-separator-independent-review.md)
passed. A fresh implementation review checked the final repaired source, both
failure-handling regressions, and all 13 saved numerical witnesses. Five exact certificates
are documented separately. No earlier solver core was changed.

The [implementation](../code/research_20260912/latent_separator_design.py) realizes
the construction in the [theory note](research-20260912-latent-separator-design.md).
It models the original selected covariance exactly by introducing latent anchor
variables. Its convex relaxation still has a discrete gap; removing covariance
truncation does not remove that gap. In the first fixed-physical-grid experiments,
the method supplies useful upper bounds quickly at the finer grids, but it does
not reach the target log-determinant gap of 0.01.

## 1. Partition and local pattern matrices

For block size \(b\), the observed blocks are consecutive disjoint intervals
\([jb,\min\{(j+1)b,n\})\), using zero-based indices. Latent anchors are their
right endpoints \(b-1,2b-1,\ldots\), excluding the final observation \(n-1\).
An observation at an anchor belongs only to the block ending there. Its
conditional noise variance is exactly the nugget. The following block uses
that same latent variable only as a conditioning anchor.

An interior block depends on its left and right anchors; an endpoint block
depends on its single adjacent anchor. If \(b\ge n\), there are no anchors
and one observation block. Zero latent variance and zero correlation are handled
directly as independent observations without unnecessary latent anchors.

The implementation uses stable analytic scalar bridge formulas. For latent
variance \(P\), an interior block with anchors \(l<r\), and \(l<t\le r\),
the conditional mean coefficients are
\[
H_{t,l}=\rho^{t-l}\frac{1-\rho^{2(r-t)}}{1-\rho^{2(r-l)}},\qquad
H_{t,r}=\rho^{r-t}\frac{1-\rho^{2(t-l)}}{1-\rho^{2(r-l)}}.
\]
For \(l<i\le j\le r\), the conditional latent covariance is
\[
P\rho^{j-i}
\frac{(1-\rho^{2(i-l)})(1-\rho^{2(r-j)})}{1-\rho^{2(r-l)}}.
\]
At a missing endpoint, omit the corresponding numerator factor and the bridge
denominator. With no endpoints, use the unconditional covariance. Add the nugget
to every observation diagonal. The code evaluates \(1-\rho^{2h}\) through
`-expm1(2*h*log(abs(rho)))`, with explicit zero-distance and zero-correlation
cases. Signed correlations are included.

For each of the \(2^{|B|}\) patterns \(S_B\) in an observed block, store
\[
[F_{S_B},H_{S_B}]^TD_{S_BS_B}^{-1}[F_{S_B},H_{S_B}]
\]
only on the parameter coordinates and the at most two adjacent anchor
coordinates. The pattern count can grow exponentially with \(b\), but its
stored matrix has at most \(p+2\) rows. A complete schedule matrix is assembled
by adding these contributions to \(\operatorname{diag}(J_0,K_{AA}^{-1})\).
The anchor precision is computed directly from scalar Markov transition and
innovation formulas.

## 2. Pricing and correction

For an augmented matrix \(M\), the oracle evaluates
\[
J=M_{\theta\theta}-M_{\theta U}M_{UU}^{-1}M_{U\theta},\quad
G=-M_{UU}^{-1}M_{U\theta},\quad
\nabla f(M)=[I;G]J^{-1}[I;G]^T.
\]
Here \(f(M)=\log\det J\). The exact formulas and concavity are justified in
the theory note; the prototype computes them numerically. The gradient is PSD
and satisfies \(\langle\nabla f(M),M\rangle=p\).

For each block and each possible local cardinality, pricing selects the pattern
with the largest linear score. An exact-count dynamic program then allocates the
global budget across blocks. This is combinatorially exact pricing with
floating-point scores. The upper tangent is
\[
f(M)-p+\langle\nabla f(M),\operatorname{diag}(J_0,K_{AA}^{-1})\rangle
+\max_{|S|=k}\sum_B\langle\nabla f(M),M_B(S_B)\rangle.
\]
Every priced schedule is independently evaluated using the original selected
covariance for its feasible lower bound.

The outer algorithm builds a convex mixture of complete schedule matrices and
uses SLSQP to correct its simplex weights. A feasible mixture remains usable
even if the numerical correction stops before its requested tolerance. A global
upper bound is retained from every completed price. The reported statuses
distinguish closure of the continuous hull from closure of the discrete gap.
The full-selection objective supplies the initial numerical upper bound.

The result stores the original model data, block size, anchor list, block
assignment, selected schedule, final mixture support, augmented mixture matrix,
and the best tangent witness. The latter contains the Schur matrix, nuisance
minimizer, prior trace, linear price, and priced schedule. This permits a later
rational certificate based on arbitrary \(W\succ0\) and \(G\) without retaining
every numerical pattern matrix.

A preflight workspace estimate includes local pattern arrays, augmented hull
matrices, and covariance evaluation work. It is not a process-RSS guarantee.
All reported runs used one BLAS/OpenMP thread and the existing isolated project
environment. Setup and internal seed evaluation are inside each solver's timer.
The implementation uses dense augmented matrices for simplicity. The nuisance
block remains tridiagonal in these scalar-anchor models, which could be exploited
later if its solve becomes a material cost.

## 3. Author validation

The [saved validation](../code/research_20260912/results/latent-separator-validation.json)
records the reviewed source candidate hash
`ba2d1e2178e0d34b0d67cd5a6b7265ec30f2f4f33f58213e9d65f6794ff28213`.
The tests cover one, two, five, and eight observations; negative, zero, and
positive correlation; zero latent variance; singleton blocks; and a block
covering the entire horizon. They passed:

- 44 complete covariance reconstructions, including anchor precision checks;
- 3,520 selected-subset Schur-information identities;
- 44 directional gradient checks and 44 concavity checks;
- 44 count-DP comparisons with exhaustive enumeration;
- 44 upper-tangent comparisons with the true exhaustive discrete optimum;
- three small full-solver comparisons with an enumerated optimum.

The maximum information discrepancy was about \(7.11\times10^{-15}\), and the
maximum directional derivative discrepancy about \(8.38\times10^{-10}\).
These are author numerical checks, not independent implementation certification.
Even the single-block convex hull can exceed the discrete optimum: the stored
nine-observation example has a gap around 0.94 at that hull. This is an ordinary
information-mixture gap, not an error in the Schur identity.

The [independent implementation review](research-20260912-latent-separator-implementation-independent-review.md)
found one error-handling defect: a failed Schur Cholesky factorization caught
inside the solver was repeated without a guard while preparing the final
diagnostics. For example, four observations with two identical constant features,
\(\rho=0.8\), latent variance 1, nugget \(10^{-16}\), prior \(0.01I\),
budget 2, and block size 1 expose cancellation in the augmented Schur calculation.
The repaired source returns `numerical_linear_algebra_failure`, the feasible
incumbent, and the full-selection numerical upper bound. It leaves unavailable
Schur diagnostics null. It also records elapsed setup time if construction times
out before an oracle is returned.

The frozen repaired source hash is
`6366451ad20c815b6a66675a6eb9be8f7bad34b9db95b469af2c9fc67210184c`.
The [post-repair validation](../code/research_20260912/results/latent-separator-validation-after-numerical-fix.json)
repeats the author checks above successfully at the intermediate repair hash
`15af99d4e20162998fd4164fdddc577fb4f82efcd60bf7007db71350b287502c`.
All experiment timings below remain the original successful runs at the earlier
source hash. The fresh reviewer also checked all 13 saved witnesses. Extreme
conditioning can still produce a `numerical_bound_inconsistency` status. The final
repair handles that status in the same way as a failed factorization: it falls
back to the separately evaluated full-selection numerical upper bound, clears
the tangent witness, and leaves hull value, gap, and information null. For
\(\rho=\operatorname{nextafter}(1,0)\), four constant scalar features, latent
variance 1, nugget and prior \(10^{-8}\), budget 2, and block size 1, the retained
lower and upper values are approximately \(5.0\times10^{-9}\) and
\(7.5\times10^{-9}\). Both failure-status regressions passed an author replay.
The ordinary saved probes have no such inconsistency. Numerical success alone
is not an exact certificate.

## 4. Fixed-physical-grid experiments

The experiments use exactly the fast-kinetics data in
[`fixed_physical_grid_benchmark.py`](../code/research_20260912/fixed_physical_grid_benchmark.py):
three parameters, prior \(0.01I\), latent and nugget variances \(1/800\), and
exactly 16 selected observations. The three grids sample the same physical
covariance with
\(\rho_{48}=(4/5)^4\), \(\rho_{96}=(4/5)^2\), and \(\rho_{192}=4/5\).
No measured experimental residual model is asserted.

Each block-size invocation has its own 30-second cap. These initial runs use an
equally spaced seed. The saved raw lower bounds therefore include only that seed
and the prototype's priced schedules. For comparison below, the earlier shared
greedy schedule is re-evaluated on the exactly matching model and used if better.
The [comparison artifact](../code/research_20260912/results/latent-separator-fixed-physical-comparison.json)
checks exact rational input identity and records hashes. It charges the original
shared setup and greedy cost in its accounted totals. Those totals combine saved
measurements, rather than represent new end-to-end invocations.

| Candidates | Block size | Numerical upper bound | Gap with better available prototype/shared-greedy incumbent | Prototype seconds | Accounted total seconds |
|---:|---:|---:|---:|---:|---:|
| 48 | 4 | 15.096634752 | 0.177390617 | 0.080 | 0.250 |
| 48 | 6 | 15.030050657 | 0.110806521 | 0.074 | 0.244 |
| 48 | 8 | 15.005243601 | 0.079735994 | 0.090 | 0.260 |
| 96 | 4 | 15.247510979 | 0.301848300 | 0.204 | 1.397 |
| 96 | 6 | 15.134837344 | 0.189174665 | 0.194 | 1.387 |
| 96 | 8 | 15.109085513 | 0.163422834 | 0.109 | 1.302 |
| 96 | 12 | 15.051419291 | 0.105756612 | 0.655 | 1.848 |
| 96 | 16 | 15.025970610 | 0.080307931 | 6.956 | 8.149 |
| 192 | 4 | 15.406524064 | 0.453477145 | 0.440 | 3.467 |
| 192 | 6 | 15.321797066 | 0.368750147 | 0.363 | 3.390 |
| 192 | 8 | 15.247511547 | 0.294464628 | 0.349 | 3.376 |
| 192 | 12 | 15.139311161 | 0.186264242 | 1.247 | 4.273 |
| 192 | 16 | 15.110331264 | 0.157284345 | 14.409 | 17.436 |

The larger-block runs for 96 and 192 candidates were run concurrently, with one
thread each. The 4/6/8 probes at those two sizes were also run concurrently.
These are local timings on a shared machine. All runs closed the numerical hull
to within about \(2.2\times10^{-6}\). Several stopped with
`correction_stalled` slightly above the requested \(10^{-6}\) hull tolerance;
their discrete gaps are much larger than that tolerance.

The best saved calendar comparison includes the
[refined transfer reanalysis](../code/research_20260912/results/fixed-physical-grid-refined-transfer.json),
which improved its bounds without another solve. On 48 candidates, its upper
bound is 14.935624533, with gap 0.005971189. On 96 candidates, its upper bound is
14.989863479, with gap 0.037096645, versus the separator block-size-16 upper bound
15.025970610. Thus the calendar method provides the stronger saved upper bound
at both sizes. These reported gaps use each method's own saved incumbents;
the upper bounds permit a direct comparison on the same frozen problem.

On 192 candidates, the earlier calendar construction timed out with upper bound
17.641733002 and no completed surrogate upper bound to refine. Dense OA returned
15.625545906, while separator block size 16 returned 15.110331264. These
comparisons concern the stated implementations and frozen data; they are not
broad solver rankings.

The separate [exact certificate report](research-20260912-latent-separator-certificates.md)
reconstructs rigorous rational bounds from five saved witnesses. Its block-size-16
certificate at 192 candidates has upper bound 15.110331327215 and gap
0.157284408207. Certificate generation took 20.587 seconds in addition to the
17.436 seconds of accounted numerical generation and shared setup/greedy time.
Their sum is about 38.023 seconds. The numerical invocation fits its 30-second
cap; this combined exact-certificate pipeline does not. The analogous 96-candidate
block-size-16 certificate gap is 0.080308032283, with 16.147 seconds of additional
certificate work. These costs are reported separately from the numerical table.

Increasing block size tightened the recorded bounds. The proven monotonicity
requires nested anchor sets, such as block size 4 to 8 to 16, or 6 to 12.
Block sizes 6 and 8 are not nested, so their observed ordering is empirical.
For comparable physical block widths under grid refinement, block size must grow
with the grid density, and enumerating \(2^b\) patterns eventually becomes
expensive. The method currently trades that cost against relaxation strength;
it does not establish a grid-independent approximation guarantee.

The raw files are
[48-candidate probes](../code/research_20260912/results/latent-separator-n48-probe.json),
[96-candidate probes](../code/research_20260912/results/latent-separator-n96-probe.json),
[192-candidate probes](../code/research_20260912/results/latent-separator-n192-probe.json),
[larger 96-candidate blocks](../code/research_20260912/results/latent-separator-n96-larger-blocks.json),
and [larger 192-candidate blocks](../code/research_20260912/results/latent-separator-n192-larger-blocks.json).

Reproduce the small checks and initial probe with:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/latent_separator_design.py --validate
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/latent_separator_design.py --n 48 --blocks 4 6 8 --time-limit 30
```

Use `--n 96` or `--n 192` and `--blocks 12 16` for the larger-block experiments,
with a separate output path to retain the earlier probes. The
[priority audit](research-20260912-latent-separator-priority-audit.md) documents
known Schur-complement, focused-design, and design-oracle ingredients. The scope
here is their structured use for this correlated observation-selection model;
novelty of that combination has not been established. No new literature was
identified in implementing this prototype.
