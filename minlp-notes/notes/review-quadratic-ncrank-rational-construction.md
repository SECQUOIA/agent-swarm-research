# Independent review: rational construction at the noncommutative-rank rate

Date: 2026-09-05. Reviewer: binary_formulation_review.
Target: [the promoted rational result](../results/quadratic-ncrank-rational-construction.md),
reviewed before promotion at `notes/quadratic-ncrank-rational-construction.md`.
Conclusion: PASS. No required correction found.

The imported constructive theorem was checked directly in Ivanyos,
Qiao, and Subrahmanyam's February 2018 manuscript,
[arXiv:1512.03531v6](https://arxiv.org/pdf/1512.03531), Theorem 1.5,
printed page 7. It gives the maximal shrinking witness and explicitly
bounds the rational intermediate and output encoding sizes. Lemma 5.3,
printed page 16, states field-extension invariance of noncommutative
rank. Thus the rational shrinking witness has the complex-field rank
used in the main precision theorem. An arithmetic-operation count alone
would have been insufficient, but the cited source provides the needed
bit bound.

The rational-basis construction is valid. The subspaces Z, W, and R are
mutually orthogonal even when their individual rational bases are not
orthonormal. Thus T is rational and invertible, HZ lies in W, and the
ZZ and ZR congruence blocks vanish. The dimension identity is about
subspaces and does not require normalized bases.

The fixed sequence of rational nullspace, intersection, inverse, and
coordinate-bound computations preserves polynomial encoding length by
standard determinant bounds. The exact enclosing intervals have
positive width because the original box has positive widths and each
row of T inverse is nonzero. Translation and diagonal normalization
preserve the zero quadratic blocks. Coefficient C has polynomial
encoding length even if its numerical magnitude is large.

The dyadic offset b=max(0,ceil(log2(C/4))) is computable by exact
integer comparisons and is polynomial in the input length. Depth K
on W and ceil(K/2) on R ensures every residual product width is at
most 2^(-K). The error C 2^(-K)/4 is at most 2^(-k). The binary count
is at most (r/2)k+(r/2)b+n/2; the last terms are polynomial in the
input size. The main theorem's binary product and residual envelopes
contain the exact graph and introduce no other integer coordinates.

The row count is polynomial in the data dimensions and linear in the
depth. Each dyadic coefficient has length O(k+poly(s)), so total output
length and construction time are polynomial in s+k. This measures time
polynomial in the precision depth k, as explicitly stated, rather than
polynomial in the binary encoding length of k. The conclusion does not
claim that optimizing the constructed MILP is polynomial time.

The pre-existing `code/quadratic_rank/check_shrunk.py` independently
checks twenty rational nonorthogonal congruences, including all needed
zero blocks and dimension identities. These exact checks passed and
are compatible with the rational construction; the general argument
and imported theorem remain the basis of the result.

## Added uniform lower bound: PASS

The subsequent quantitative lower section was independently checked.
GGOW2020 Theorem 2.18, journal page 251, applies to unnormalized
integer Kraus matrices and gives capacity at least r^(-2r), with no
entry-magnitude hypothesis. Clearing denominators by D changes the
restricted capacity by D^(2r), so its original value is at least
D^(-2r)r^(-2r). This determinant scaling is correct.

If E is the product of all endpoint denominators, the principal slice
volume is at least E^(-1). Substituting these bounds into the reviewed
finite covariance bound, and using omega_r^(2/r)<=4, gives exactly

```
epsilon >= [16D(r+2)sqrt(mr)E^(2/r)]^(-1) 2^(-2p/r).
```

Taking logarithms yields the stated uniform lower overhead. The total
logarithms of the denominator products are bounded by the input length.
The resulting two-sided polynomial-input-size overhead is therefore
valid against arbitrary real convex lifts, as claimed.

The proposed principal compression search is also valid: every current
Hermitian principal pencil of rank r and order larger than r has an
invertible principal r-submatrix, so some deletion retains rank r.
Polynomially many exact nc-rank calls locate one. No new algebraic
algorithm is being claimed.
