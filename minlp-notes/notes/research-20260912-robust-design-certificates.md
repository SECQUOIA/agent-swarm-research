# Shared sampling schedules under uncertain kinetic parameters

Date: 2026-09-12. Status: the
[certificate derivation](research-20260912-robust-certificate-independent-review.md)
passed fresh mathematical review. The same fresh reviewer then independently
checked the exact implementation, both saved certificates and the nominal
comparisons. A [separate implementation review](research-20260912-robust-solver-independent-review.md)
also accepted the numerical producer after two boundary fixes. Robust design, scenario scalarization and
log-determinant tangents are established methods. The practical investigation
asks whether the reviewed finite-history oracle can give useful, rigorously
certified schedules when one nominal kinetic model is insufficient.

## Model and normalization

There are finitely many scenarios `s=1,...,q`, each with a known observation
covariance and nominal mean sensitivities. One common feasible schedule `P`
produces positive definite information `J_s(P)` of common dimension `p`.
The first experiments will use the same consecutive-reaction model and three
nominal rate regimes, with a stipulated scalar AR(1)-plus-nugget covariance.
Scenarios represent uncertainty in a nominal model; this finite collection
does not certify a continuous parameter region or global identifiability.

For supplied offsets `c_s`, the fixed-offset objective is

```text
g_c(P) = min_s [log det J_s(P) - c_s].
```

The raw maximin criterion has `c_s=0`. Standardized D-efficiency uses the
unknown individual scenario optima

```text
b_s* = max_P log det J_s(P),
g_*(P) = min_s [log det J_s(P) - b_s*],
E_*(P) = exp(g_*(P)/p).
```

This removes differences in the best achievable information across scenarios.
One common invertible change of parameter coordinates preserves the raw
criterion's optimal schedules. Scenario-dependent transformations can change
the raw criterion; standardization cancels their determinant offsets when
the prior and information are transformed consistently. This is a reason to
report standardized performance, not an assertion that raw maximin is invalid.

## Shared support certificate

Suppose the reviewed finite-history construction gives additive matrices

```text
J_L,s(P) = J0_s + sum_(e in P) Q_s,e,
J_s(P) <= J0_s + sum_(e in P) Q_s,e/(1-delta_s),
0 <= delta_s < 1,  Q_s,e >= 0.
```

Use the same explicit feasible-path graph for every scenario, with a history
long enough for all their local conditionals. Choose any positive definite
tangent references `N_s` and any nonnegative weights `w_s` summing exactly
to one. They need not be optimal dual variables. Log-determinant concavity,
its monotonicity under PSD order, and `min <= weighted average` give

```text
g_c(P) <= sum_s w_s [log det N_s - p
                    + tr(N_s^-1 J0_s) - c_s]
          + sum_(e in P) a_e,

a_e = sum_s w_s tr(N_s^-1 Q_s,e)/(1-delta_s).
```

An exact longest-path price of these scalar arc weights therefore gives a
global upper bound on the original discrete maximin objective. The same
schedule must maximize the combined arc price. Summing separate scenario
maxima is valid but can be weaker. A mixture of schedules can choose useful
references, while its information is not treated as a feasible single
experiment. Every reported lower bound comes from an actual common schedule.

The numerical prototype will optimize a shared mixture using a concave
maximin epigraph and extract nonnegative scenario weights. The certificate
will recompute the bound independently with rational data, rational reference
rounding, outward integer arc scores, and rational logarithm enclosures.
Clipping and normalizing proposed weights is permitted because every point
of the simplex supplies a valid upper bound. Exact validation of the simplex
and positive definite references is part of the certifier.

## Unknown standardizing optima

Suppose independently recomputed certificates give `ell_s <= b_s* <= u_s`.
Then a common incumbent `P0` has the standardized lower bound

```text
L = min_s [lower_logdet J_s(P0) - u_s].
```

In the support formula, replace the subtracted offsets by `ell_s` to obtain
an upper bound `U` for `max_P g_*(P)`. Also use `U=min(U,0)`, since every
scenario-specific optimum dominates every feasible common schedule. This
propagates uncertainty in the standardization instead of silently treating
numerical single-scenario optima as exact constants.

The resulting schedule satisfies

```text
E_*(P0) >= exp(L/p),
E_*(P0)/max_P E_*(P) >= exp(-(U-L)/p).
```

The stored rigorous quantities can be the rational log bounds `L,U`.
Floating-point exponentials are display summaries, not additional exact
inequalities. Exact references and all scenario data must be retained so
the certificate can be reproduced.

## Complexity connection

For a fixed number of scenarios and fixed parameter dimension, apply the
[reviewed PSD approximation-set theorem](research-20260912-dag-psd-approximation-set.md)
to the additive block information `diag(J_L,1(P),...,J_L,q(P))` on the common
finite-history graph. Transfer its sandwich back to the true scenario matrices.
If every memory error is at most `delta` and the set accuracy is `eta`, one
representative simultaneously satisfies `J_s(P_hat) >= a J_s(P)`, where
`a=(1-eta)(1-delta)/(1+delta)`. This gives a factor `a` for each determinant
root and for their minimum after fixed positive normalization.

Unknown optimal standardizers require an additional comparison step. For
the computed path set `C`, calculate the positive rational determinants
`d_s=max_(P in C) det J_s(P)` and choose a path in `C` maximizing
`min_s det J_s(P)/d_s`. These are exact rational comparisons. Since
`a^p max_P det J_s(P) <= d_s <= max_P det J_s(P)`, the returned path has
at least `a^2` times optimum standardized D-efficiency. The second factor
accounts for the approximate normalizers; the review gives an example where
it is attained. Taking `eta=epsilon/4` and `delta<=epsilon/8` gives
`a^2>=1-epsilon`. The graph has polynomial size under the previously reviewed
fixed decay and noise-ratio promises, not for arbitrary dense covariances.

This is a direct corollary, not a new robust-design principle. The polynomial
exponent depends on the total matrix dimension `q p`; this observation gives
no efficient implementation for many scenarios.

The practical hull oracle does not enumerate this approximation set. Its
cost per support price grows polynomially with the scenario matrices while
the calendar-history state count is unchanged. A hull gap may remain, and
the numerical prototype must report it rather than imply an FPTAS runtime.

## Planned comparison and limitations

Compare the shared design against schedules optimized at each single
scenario, a completed greedy/exchange search for the common criterion, and
a dense correlated-error relaxation if it provides a useful matched baseline.
Record each schedule's score in every scenario, reference-certificate
uncertainty, design-generation time and certificate time separately.
Include single-scenario reference work in total pipeline costs.

The source audit runs alongside implementation. No new priority or numerical
performance claim is established by this derivation alone.

## Reviewed exact artifacts

The [certifier](../code/research_20260912/certify_robust_design.py) now recomputes
all three individual reference certificates, exact selected information,
the weighted common integer price, and rational log enclosures. It rounds
logarithm bounds outward to a denominator of `10^12`; this limits fraction
size without assuming floating-point logarithm accuracy. The application uses
the same covariance in every scenario, although the certifier computes each
scenario's covariance conditionals and correction independently.

| Candidates | Incumbent source | Standardized log lower | Standardized log upper | Log gap | Certificate time |
|---|---|---:|---:|---:|---:|
| 48 | Completed greedy/exchange | -0.091701377259 | -0.083176142020 | 0.008525235239 | 2.97 s |
| 96 | Shared-path hull proposal | -0.091162249685 | -0.074519785108 | 0.016642464577 | 8.25 s |

These are the exact saved rational bounds, shown in terminating decimals.
The times include three individual-scenario certificates and exclude numerical
design generation. Both use the shared-hull tangent matrices and weights;
the feasible incumbent can come from any valid common schedule. At `p=3`,
the efficiency guarantee relative to the unknown robust optimum is
`exp(-gap/3)`, about 99.716% and 99.447%, respectively. The percentage displays
are numerical summaries of the rigorous log bounds.

The files are `results/robust-kinetic-n48-certificate.json` and
`results/robust-kinetic-n96-certificate.json` under `code/research_20260912/`.
Reproduce the first certificate from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/certify_robust_design.py code/research_20260912/results/robust-kinetic-n48.json code/research_20260912/results/robust-kinetic-n48-certificate.json --selection greedy_exchange
```

For 96 candidates, replace `n48` by `n96` and omit `--selection` to use the
shared-hull incumbent. Exact certification does not depend on numerical
optimizer termination or on the supplied floating-point bound values.

The [nominal comparison](../code/research_20260912/compare_robust_nominal.py)
recomputes each saved central-model schedule from the same exact covariance
and sensitivity data. Independent dense inversions verify its bounds. The
selected schedule's standardized D-efficiency divided by that nominal
schedule's efficiency is at least `exp(x)`, with the exact values

```text
x_48 = 33377973613/1000000000000,
x_96 = 24094612477/3000000000000.
```

Since `exp(x)>=1+x`, these imply improvements of at least 3.33% and 0.80%,
respectively, using only rational comparisons. The corresponding artifacts are
`robust-kinetic-n48-nominal-comparison.json` and its `n96` counterpart. These
are comparisons with the saved central-scenario schedules, not every possible
central-scenario optimum or nominal-design algorithm. The robust objective
still concerns only the explicitly supplied three scenarios.

A subsequently [reviewed dense comparison and polishing step](research-20260912-robust-dense-comparison.md)
improves the 96-candidate incumbent. Its separately reviewed exact standardized
interval is `[-0.086007784227,-0.074519785108]`, with log gap
`0.011487999119`. This gives about 97.173780% worst D-efficiency and about
99.617800% of the unknown robust optimum. These percentage displays derive
from the exact log inequalities. The earlier table deliberately retains the
unpolished results and their original timings.
