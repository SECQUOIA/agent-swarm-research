# Independent review of positive-update normalization

Date: 2026-09-27. Scope: the rational normalization and exact arithmetic in
[the positive-update note](positive-update-spectral-approximation.md).
This is an independent narrow review, not a review of every theorem or an
external novelty assessment.

## Conclusion and scope of the contribution

The rational LDL normalization is correct under the stated assumptions:
the anchor sum is rational positive definite, every atom is rational PSD,
and the rounding width is a positive rational. Exact normalization,
admission tests, and rounding have polynomial bit complexity in fixed
dimension. No square-root approximation or sum-of-radicals comparison is
needed.

The [2026-09-12 DAG approximation-set note](../notes/research-20260912-dag-psd-approximation-set.md)
already gives a general two-sided spectral approximation set, including
singular matrices, using the same normalization and rounding principle.
The current incremental candidate is minimum-cost selection within each
existing state, which preserves one binary-encoded exact additive budget,
together with the positive-low-rank regression-benefit approximation
application. The normalization is not a new contribution. This review
does not establish external novelty of the incremental candidate.

## Exact normalization and encoding length

Let the rational anchor sum be \(A=L\Delta L^T\succ0\), where \(L\)
is unit lower triangular and \(\Delta\) is positive diagonal. Unpivoted
rational LDL factorization is valid because every leading principal minor
of a positive definite matrix is positive. Its entries and those of
\(L^{-1}\) have polynomial encoding length; determinant formulas for the
pivots and elimination entries give the usual rational-arithmetic bounds.

For each positive rational \(\Delta_i\), choose

\[
k_i=-\lfloor\log_4\Delta_i\rfloor,\qquad s_i=2^{k_i}.
\]

This expression is an exact specification, not a floating-point
calculation. For \(\Delta_i=N/M\), use numerator and denominator bit
lengths to set \(t=\operatorname{bits}(N)-\operatorname{bits}(M)\).
An exact comparison with \(2^t\) gives
\(m=\lfloor\log_2\Delta_i\rfloor\): it is \(t\) if
\(\Delta_i\ge2^t\), and \(t-1\) otherwise. Then
\(k_i=-\lfloor m/2\rfloor\). Negative exponents are represented as
dyadic reciprocals. Their magnitudes are bounded by the encoding length
of \(\Delta_i\), so the resulting rational scales also have polynomial
encoding length.

Set \(S=\operatorname{diag}(s_i)\) and \(R=SL^{-1}\). Directly,

\[
RA R^T=S\Delta S,\qquad I\preceq RA R^T\prec4I.
\]

The needed comparison also follows directly by congruence:

\[
R^TR=L^{-T}S^2L^{-1}\preceq
4L^{-T}\Delta^{-1}L^{-1}=4A^{-1}.
\]

Thus, for each admitted PSD atom \(W\) satisfying
\(\operatorname{tr}(A^{-1}W)\le p\),

\[
\operatorname{tr}(RWR^T)
=\operatorname{tr}(R^TRW)
\le4\operatorname{tr}(A^{-1}W)\le4p.
\]

Every transformed entry has magnitude at most \(4p\), because a PSD
matrix satisfies \(|H_{ij}|\le\sqrt{H_{ii}H_{jj}}\le
\operatorname{tr}(H)\). The admission trace, transformed entries, and
entry divided by the rational rounding width are rational quantities of
polynomial encoding length. Their floors are ordinary exact integer
division, using mathematical floor for negative values. These arguments
do not depend on bounded numerical condition numbers.

If the rounding width is \(\delta=\varepsilon/(pn)\), the accumulated
error bound requires at most \(n\) individually rounded contributions.
The present note rounds only the selectable atoms and leaves the common
prior exact, so the stated bound has the required meaning. Rounding the
prior's atoms separately would require counting them in this bound.

## Retained exact check and actual result

The independent one-off command was run before these artifacts were
written. It invoked `python - <<'PY'` with the exact body now retained in
[positive_update_normalization_review.py](checks/positive_update_normalization_review.py),
followed by the terminating `PY`. The
[JSON record](checks/positive_update_normalization_review.json) contains
that complete executed command and the actual captured output. The
retained script has not been rerun; preservation did not introduce an
additional normalization check.

The command completed with exit code 0 and printed:

```text
Exact rational LDL/dyadic normalization identities verified in 250 SPD cases, dimensions 1 through 5.
```

The check uses only Python `Fraction` arithmetic with seed 731. It creates
50 rational positive definite matrices in each dimension from 1 through
5, verifies positivity of every LDL pivot, constructs the dyadic scales
using exact comparisons, and checks every entry of
\(RA R^T=\operatorname{diag}(s_i^2\Delta_i)\), including the bounds
\(1\le s_i^2\Delta_i<4\).

For reproduction, the equivalent retained-file command is:

```bash
python research-20260927/checks/positive_update_normalization_review.py
```

This equivalent command is provided for reproduction and was not run in
this review. The original here-document command is recorded in full in
the JSON artifact. The finite check supports the arithmetic recipe; it
does not prove the universal identity or bit-complexity bound, test the
full dynamic program, verify the budget refinement, or establish novelty.
No project-wide verification or CI inspection was performed.
