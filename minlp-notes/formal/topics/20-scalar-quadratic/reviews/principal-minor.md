# Independent review: principal minor of actual rank

Date: 2026-09-20. Reviewer: independent source-review agent.
Reviewed module:
[PrincipalMinor.lean](../../../Formal/QuadraticPrecision/PrincipalMinor.lean).

Verdict: **PASS** for the principal-minor portion of R2. The final theorem
uses the actual matrix rank and requires only a real Hermitian matrix
(equivalently a real symmetric matrix) on an arbitrary finite index type.
It does not assume a principal minor, diagonalization certificate, positive
definiteness, distinct eigenvalues, or positive rank. The affine slice and
lift transfer portions of R2 require separate assembly and are not claimed
by this module.

`charpoly_coeff_nullity_ne_zero` partitions the eigenvalue *indices* into
zero and nonzero eigenvalues. Thus repeated eigenvalues retain their
correct multiplicities. Mathlib's spectral rank theorem identifies the
number of nonzero indices with `H.rank`; its characteristic polynomial
factorization is over all indices. Splitting that product writes the
characteristic polynomial as a product of nonzero-root factors times
`X^(card n - rank H)`. The coefficient at the latter exponent is the
constant coefficient of the nonzero-root product, which is nonzero.
No cancellation between positive and negative eigenvalues invalidates
this product argument.

`exists_principal_minor_rank` applies the characteristic-coefficient
identity with `k = H.rank`, justified by the actual rank upper bound.
That identity sums the determinants of the principal submatrices indexed
by the finite subsets of cardinality `k`. A nonzero coefficient forces
the sum to be nonzero, so one determinant is nonzero. The selected
submatrix uses the same subtype inclusion on both indices, making it a
principal submatrix with exactly the required size.

Rank zero is included without an extra premise: the nonzero-eigenvalue
product is empty, its constant coefficient is one, and the selected
finite set has cardinality zero. Its principal minor is the empty matrix,
whose determinant is one. The argument also applies when the original
index type itself is empty. I additionally checked a direct client
specialization deriving that the selected set is empty whenever
`H.rank = 0`.

## Targeted checks actually run

From `formal/`, with `PATH="$HOME/.elan/bin:$PATH"` and
`LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.QuadraticPrecision.PrincipalMinor
lake env lean /tmp/Topic20PrincipalMinorReview.lean
```

Both commands passed. The second temporary review file imported only the
module, printed axioms for both declarations, and checked the rank-zero
client specialization. Both axiom lists were exactly
`[propext, Classical.choice, Quot.sound]`.

Reviewed source SHA-256:
`d572aaf4b0d2920a362513b0b00ef4f78e329df2cf778000cdb494a6793905e5`.
No proof source was changed. No project-wide build or CI inspection was
performed. The temporary client check is corroboration of the boundary
interface; the general theorem itself proves the result for every rank.
