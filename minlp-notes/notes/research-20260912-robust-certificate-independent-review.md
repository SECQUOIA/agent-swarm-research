# Independent review of shared-schedule robust design certificates

Date: 2026-09-12. The support certificate, standardization bound directions,
and efficiency conversion in the [author note](research-20260912-robust-design-certificates.md)
pass independent mathematical review. The complexity paragraph needs the
explicit finite-history transfer and normalization-comparison qualifications
below. These are not defects in the displayed support inequalities. This
review establishes neither priority nor practical performance.

The reviewed input is a nonempty common finite feasible-path family and
positive definite scenario information matrices of common order `p`.
The conclusions concern exactly the supplied finite scenarios. References,
covariances, priors, feasibility restrictions, and single-scenario optima must
refer to the same model and the same feasible family. A reference optimum
over a larger family still gives an upper bound, but an incumbent from that
larger family does not automatically give a lower bound for the required
single-scenario optimum.

## Support certificate

The accepted [finite-history theorem](research-20260912-noisy-markov-memory.md),
Section 3, bounds the data-information term before adding the prior. Thus its
prior-aware consequence is exactly

```text
J_s(P) <= J0_s + A_L,s(P)/(1-delta_s),
A_L,s(P) = sum_(e in P) Q_s,e.
```

This justifies leaving the prior unscaled. A statement only about the total
matrices, `(1-delta_s)J_s<=J_L,s`, would justify the weaker bound
`J_s<=J_L,s/(1-delta_s)`; the sharper prior-aware form uses the separately
established data-information bound. The assumptions `delta_s<1`, PSD arc
matrices, and one graph describing the common decisions are essential.

For each positive definite reference `N_s`, concavity gives, for every
positive definite `X`,

```text
logdet X <= logdet N_s-p+tr(N_s^-1 X).
```

Substitute the prior-aware upper matrix. Logdet is Loewner nondecreasing,
and `tr(N_s^-1 Q_s,e)>=0`. For any nonnegative weights summing exactly to one,
the minimum of the scenario scores is at most their weighted average.
Distributing that average therefore yields exactly the author's intercept
and combined arc weights. Taking one common-path maximum proves the upper
bound for the original discrete objective.

No optimality condition for the references or weights is needed. References
may even come from different proposed mixtures; positive definiteness is the
condition needed by the inequality. Clipping and exactly normalizing numerical
weights is valid provided the resulting sum before normalization is positive.
An all-zero clipped vector needs an explicit valid replacement or rejection.
Negative weights or an approximately unit sum do not satisfy the proof.

If a rational grid size is `h>0`, replacing every combined arc weight `a_e`
by `h ceil(a_e/h)` gives a valid outward score. The longest-path algorithm
must compute an upper bound over every allowed common path. A maximum over
only discovered paths is a lower bound on this price and cannot certify
global optimality. Logarithm enclosures in the intercept must use their upper
endpoints; subtracted uncertain offsets must use lower endpoints.

Because

```text
max_P sum_s w_s a_s(P) <= sum_s w_s max_P a_s(P),
```

separate scenario maximizations are valid but can lose strength. The scalar
example below makes the loss strict. A shared fractional design can propose
references and witnesses for a relaxation. Its average information does not
become the information of an actual feasible common schedule.

## Standardization and efficiency

Write `f_s(P)=logdet J_s(P)` and `b_s*=max_P f_s(P)`. From independently valid
`ell_s<=b_s*<=u_s`, pointwise comparison gives

```text
min_s [f_s(P)-u_s] <= g_*(P) <= min_s [f_s(P)-ell_s].
```

Consequently a true feasible incumbent and lower logdet enclosures give
`L<=g_*(P0)`, while the support formula with offsets `ell_s` gives
`max_P g_*(P)<=U`. Since every `f_s(P)<=b_s*`, replacing `U` by `min(U,0)`
is correct. Reference lower bounds may come from different feasible schedules
for different scenarios; only the robust incumbent must be one common
schedule. All reported exact bounds should satisfy `L<=U`; a violation is an
error to investigate, not a negative optimality gap to display.

Exponentiation is increasing and `p>0`. Thus

```text
E_*(P0) >= exp(L/p),
E_*(P0)/max_P E_*(P) >= exp((L-U)/p).
```

The second denominator is the optimum of the robust standardized objective,
not a product or average of individually optimized efficiencies. The formulas
are rigorous consequences of the rational log bounds. Ordinary floating-point
exponentials are display values unless enclosed independently.

A change `J_s -> T_s J_s T_s^T` adds the same scenario-specific constant
`2 log|det T_s|` to both `f_s(P)` and `b_s*`, provided priors and all information
terms transform consistently. Standardization cancels that constant. A common
transformation adds one constant to the raw maximin objective and preserves
its maximizers; unrelated scenario transformations need not do so.

## Explicit fixed-scenario approximation recipe

The accepted [PSD approximation-set theorem](research-20260912-dag-psd-approximation-set.md)
applies to rational additive PSD matrices on an explicitly encoded DAG.
For already additive scenario information, use block matrices
`diag(Q_1,e,...,Q_q,e)` and the analogous block prior. A spectral factor `a`
for a representative then holds in each block separately. Every determinant
root gains a factor at least `a`; taking a minimum after any fixed positive
normalization preserves this factor. This is a direct corollary.

For noisy finite-history design, true information `J_s(P)` is generally not
additive on the chosen history graph. Apply the set theorem to
`diag(J_L,1(P),...,J_L,q(P))` instead. If the memory error is at most `delta`
in every scenario and the set accuracy is `eta`, transfer from the target's
true matrix to its surrogate, then to its representative, then back to true
information. Every target path has one representative satisfying simultaneously

```text
J_s(P_hat) >= a J_s(P),
a = (1-eta)(1-delta)/(1+delta).
```

The corresponding upper factor is `(1+eta)(1+delta)/(1-delta)`. Taking the
largest required calendar window gives one common graph. A polynomial-size
graph in the original input requires the accepted full-block assumptions:
fixed contraction and noise-ratio bounds, rational supplied sensitivities,
and permitted restrictions that have a polynomial graph representation.
It does not follow for arbitrary dense scenario covariance matrices merely
because their number and information dimension are fixed.

The existence of a representative does not by itself give an objective
comparison procedure using unknown standardizers. The following procedure
uses the same approximation set `C` and exact rational determinants:

```text
D_s* = max_(all P) det J_s(P),
d_s  = max_(P in C) det J_s(P),
P_hat in argmax_(P in C) min_s det J_s(P)/d_s.
```

The `D_s*` define the target but are not computed. Positive definiteness gives
`d_s>0`, and the simultaneous approximation property gives
`a^p D_s*<=d_s<=D_s*`. All comparisons in the last line are rational. In
particular no exact comparison of logarithms or determinant roots is needed.
Let `E(P)=min_s (det J_s(P)/D_s*)^(1/p)` and define `E_C(P)` using `d_s`
instead. Then `E(P)<=E_C(P)<=E(P)/a`. A representative of an optimal robust
path has true efficiency at least `a max_P E(P)`. Maximizing `E_C` in `C`
therefore gives

```text
E(P_hat) >= a E_C(P_hat) >= a^2 max_P E(P).
```

Thus unknown normalization costs a second factor in this simple procedure.
For an additive graph, take `eta=epsilon/2` and `delta=0`. For the accepted
finite-history model, take `eta=epsilon/4` and choose a window with
`delta<=epsilon/8`, or full history with `delta=0`. Then
`a>=1-eta-2delta>=1-epsilon/2`, so `a^2>=1-epsilon`. This yields an FPTAS
for standardized D-efficiency when `q,p` and the memory promises are fixed.
Exact true determinants for the polynomial-size output set can be computed
from the supplied rational covariance model in polynomial time.

The exponent depends on total information dimension `qp`; this is not a
dimension-independent fixed-parameter algorithm. Fixed-offset criteria also
need computable normalizers and an appropriate objective comparison method
for a Turing complexity claim. The practical tangent/hull method does not
construct this set and does not inherit its FPTAS guarantee.

## Exact examples and limitations

With two scalar scenarios, prior one, and two feasible paths having
information `(4,1)` and `(1,4)`, both individual scenario optima are four.
Either integer path has standardized efficiency `1/4`. The equal mixture has
information `(5/2,5/2)` and relaxed efficiency `5/8`.

At references `N_1=N_2=5/2` and equal scenario weights, the combined arc price
is `3/5`; the weighted sum of separate arc maxima is `6/5`. The shared
certificate improves the log upper bound by exactly `3/5`, giving
`U=log(5/8)` for the standardized problem. Nevertheless the true optimum is
`log(1/4)`. Every tangent/scenario-weight certificate of this family also
bounds the equal fractional mixture, so improving those witnesses alone
cannot close this gap. This is an explicit hull limitation even at zero
memory error, rather than a numerical failure.

Reversing either normalization direction can invalidate a certificate. With
one scalar scenario and feasible information values one and four, use the
valid reference bounds `ell=log 1` and `u=log 8`. Subtracting `ell` in the
incumbent lower bound for information one would report zero, above its true
standardized score `-log 4`. Subtracting `u` in an otherwise exact optimal
support upper bound would report `log(4/8)<0`, below the true robust optimum
zero.

The second factor in the same-set normalization recipe can be attained.
Let `a=3/4` and use the scalar two-scenario family containing

```text
C = {(3/4,1/10), (1/10,1), (3/8,3/8), (9/32,3/8)},
additional paths = {(1/2,1/2), (1,1/10)}.
```

Every path has a representative in `C` within simultaneous factors
`[3/4,5/4]`. True scenario maxima are `(1,1)`, while the set maxima are
`(3/4,1)`. The last path in `C` maximizes the in-set-normalized objective,
with a tie, but its true robust efficiency relative to the optimum is
`(9/32)/(1/2)=9/16=a^2`. Therefore the generic recipe cannot claim a single
factor `a` for every allowed choice of maximizing representative.

The [independent exact checker](../code/research_20260912/review_robust_certificate_theorem.py)
imports no optimization or certificate-generator code. It forms dense
rational observation covariances for three scenarios, including negative
correlation, and enumerates all 20 schedules choosing three of six times.
It checks 60 scenario/schedule prior-aware memory comparisons and 300 shared
support and standardization comparisons using 15 simplex points, including
zero scenario weights. Separate rational logarithm series enclose all logs.
The exact examples above and three finite-memory loss-constant cases also
pass. The [saved report](../code/research_20260912/results/robust-certificate-theorem-independent-review.json)
records the reviewed source hash and checker hash. These fixtures supplement
the proof and preserve failure examples; they are not a solver benchmark.

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_robust_certificate_theorem.py
```

Missing robust-design primary-source coverage was sent to the sole literature
writer. No new literature claim is made in this independent proof review.

## Subsequent exact implementation review

The new [exact certifier](../code/research_20260912/certify_robust_design.py)
also passes independent review. No implementation correction was required.
The reviewed source SHA-256 is
`ef2c5a153b4983197869c75942cfdcb3446816e508ffa10a8aef0e1371063873`.
This implementation supports nonempty scalar stationary AR(1)-plus-nugget
scenario models with rational data, SPD priors, and one common cardinality.
The scenarios may have different covariance parameters. Its numerical
proposal generator currently uses common covariance parameters; the exact
checker also exercises different scenario covariances.

The certifier clips proposed scenario weights and normalizes them exactly,
rejecting zero positive mass. It recomputes every individual scenario
certificate using that scenario's own stored data, so supplied numerical
objective labels never become standardizing constants. Every tangent is
symmetrized, rounded to rationals, and checked for positive definiteness.
Its inverse, prior trace, weighted coefficient matrix, and all final log
bound directions agree with the reviewed formula.

The combined price sums outward scenario arc scores and uses one shared
count/history DP. Pattern reuse by relative history ages is valid for the
stationary covariance model. The explicit cap rejects excessive state
counts before allocating the graph. Empty and full selections pass the
tested valid-window cases. A coefficient grid whose conditional variance
floor is zero is rejected, as required by the accepted interval scorer.

The [implementation checker](../code/research_20260912/review_robust_certificate_implementation.py)
forms exact dense selected covariance inverses independently of the scalar
filter. It represents DP histories as tuples of actual calendar indices,
independently of the certifier's bit masks. This separate graph implementation
uses the already reviewed `IntegerIntervalScores` component for arc values;
it is a check of shared-path integration, not a fresh implementation of
that component. Exhaustive small-case bounds use directly computed dense
information, and independent rational log enclosures check the saved
incumbent intervals.

The [saved implementation review](../code/research_20260912/results/robust-certificate-implementation-independent-review.json)
records ten independent tuple-history prices, 22 dense incumbent/reference
checks, 36 enumerated common-schedule bounds, five weight-clipping cases,
three log-grid variants (`1`, `3`, and `10^16`), 15 malformed-input rejections,
and six invalid or insufficient grid/cap rejections. It also confirms that
altering numerical reference objective labels and the fixed offsets leaves
the true-standardized certificate unchanged when witnesses are held fixed.

Both saved benchmark certificates replay exactly after excluding timing
fields, with input, implementation, and dependency hashes checked. The
independent tuple-history DP also reproduces both maximizing integer prices
and their selected paths. Dense calculations validate each robust incumbent
and each individual-reference incumbent. The certified standardized log gaps
are:

| Candidates | Exact standardized log gap |
|---:|---:|
| 48 | `8525235239/1000000000000` |
| 96 | `16642464577/1000000000000` |

These are rigorous gaps for the saved rational sensitivity tables and
stipulated covariance models. The review does not certify the underlying
exponential mean formula as exact input or validate the noise model against
measurements. It also does not establish that the continuous hull is solved
globally; an arbitrary validated support witness suffices for the reported
upper bound.

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_robust_certificate_implementation.py
```

## Subsequent nominal-schedule comparison review

The [comparison code](../code/research_20260912/compare_robust_nominal.py)
and both saved nominal comparisons pass independent review. Its claim is
explicitly conditional on an independently verified input certificate. The
review matched each supplied certificate's hash to the certificate already
checked above, then reproduced both comparison artifacts exactly. No code
correction was required.

For a nominal schedule `P_N`, the correct standardized interval is

```text
min_s [lower_logdet J_s(P_N)-u_s]
  <= g_*(P_N)
  <= min_s [upper_logdet J_s(P_N)-ell_s].
```

The implementation uses these directions. If `L_R` is the verified lower
bound for the selected robust schedule and `U_N` is the nominal schedule's
upper bound, then

```text
log(E_*(P_R)/E_*(P_N))
  = (g_*(P_R)-g_*(P_N))/p
  >= (L_R-U_N)/p.
```

The upper bound here concerns the fixed nominal schedule, rather than the
global robust optimum. The unknown scenario standardizers are enclosed for
both schedules with the same verified reference bounds. The code checks
exact agreement of all scenario model data between the numerical record
and certificate, and checks nominal schedule feasibility.

The [independent comparison checker](../code/research_20260912/review_robust_nominal_comparison.py)
recomputes both nominal schedules and both robust schedules from exact dense
covariance inverses in all three scenarios. Independent rational logarithm
enclosures fit inside the reported intervals, and the resulting standardized
intervals separate strictly in the required direction. Both artifacts replay
exactly; four changed-model or infeasible-schedule inputs are rejected. The
[saved review report](../code/research_20260912/results/robust-nominal-comparison-independent-review.json)
records the artifact and implementation hashes.

| Candidates | Proven lower bound on `log(E_*(P_R)/E_*(P_N))` |
|---:|---:|
| 48 | `33377973613/1000000000000` |
| 96 | `24094612477/3000000000000` |

Both rationals are positive, proving strict standardized-efficiency
improvement over the respective saved central-scenario nominal schedule.
This does not compare against every central-scenario optimum or every
possible nominal-design method. The model and finite-scenario limitations
of the original certificates remain in force. Floating exponential summaries
are unnecessary to establish either strict comparison.

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_robust_nominal_comparison.py
```
