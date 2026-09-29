# Independent review of the sparse quadratic PSD approximation proposal

Date: 2026-09-27. This review reconstructs the argument from its statement,
checks exact small instances, and compares relevant local and external work.
The proof is sound under the qualifications below. External novelty remains
unresolved. The normalization and matrix-cover method already exist in this
repository; the sparse quadratic consequences must be identified as an
application or extension of that method.

## 1. Reviewed model and conclusions

Let `D=diag(d_i)>0`, `U` be a rational `n by r` matrix, and `b` be rational.
The rank parameter `r` is fixed, and `Q=D+UU^T`. An indicator support `S`
means `x_i=0` outside `S`; selected coordinates may also equal zero.
This last convention matters when activation costs are negative.

Put

```text
g(S) = b_S^T Q_SS^(-1) b_S,
B = sum_i b_i^2/d_i,
f(S) = lambda(S)-g(S).
```

For every rational `0<epsilon<1`, the proposed construction yields a
finite set of actual supports such that each target `S` with `g(S)>0`
has a representative `T` satisfying

```text
lambda(T) <= lambda(S),
(1-epsilon)g(S) <= g(T) <= (1+epsilon)g(S).
```

The upper bound follows from the same matrix sandwich, although the
minimization application only needs the lower bound. The representative
depends on the cost vector used by the dynamic program. The set is not
automatically reusable after changing that vector.

Together with the support of all negative-cost coordinates, this proves

```text
f(output) <= OPT + epsilon g(S*) <= OPT + epsilon B
```

for every optimal support `S*`. This is an additive fully polynomial
approximation scheme. Calling this statement alone a multiplicative
FPTAS would be incorrect: the penalized objective can be negative or
arbitrarily close to zero.

The number of states and bit complexity are polynomial in encoded input
length and `1/epsilon` for fixed `r`. Independence of numerical norms or
condition numbers means no additional numerical-magnitude dependence
beyond their encoding length. It does not mean independence of the bits
needed to write very large or very small input numbers.

## 2. Proof reconstruction and vulnerable steps

Write `p=r+1`, `a_i=(u_i,b_i)`, `W_i=a_i a_i^T/d_i`, and

```text
K_S = diag(I_r,0) + sum_(i in S) W_i.
```

The Schur complement of its first `r` coordinates is exactly `g(S)` by
the Woodbury identity. The first principal block is positive definite,
so `K_S` is positive definite exactly when `g(S)>0`. Equivalently, this
holds exactly when some selected `b_i` is nonzero. This is simpler than
a general singular PSD cover: only full rank and zero gain need handling.

For a positive-gain target support, choose a maximum-volume basis of
`p` factor vectors from `a_i/sqrt(d_i)`, `i in S`, and the first `r`
coordinate vectors. The square roots occur only in the proof. If `V`
is its square basis matrix, determinant replacement gives
`|(V^(-1)v)_j|<=1` for each target factor `v` and basis coordinate `j`.
For the rational matrix `A=VV^T`, this yields

```text
tr(A^(-1) W_i) <= p,
tr(A^(-1) e_j e_j^T) <= p.
```

Every basis is enumerated, so the algorithm need not compute a
maximum-volume basis. It must force every selected item owner of an
anchor factor into its returned support. Fixed coordinate factors are
already present. This gives `K_T >= A` in every retained state of a
completed branch.

A rational LDL decomposition `A=L diag(t_j)L^T`, followed by dyadic
scales `s_j` with `1<=s_j^2 t_j<4`, gives

```text
R=diag(s_j)L^(-1),
I <= RAR^T < 4I.
```

For every admitted item, `tr(A^(-1)W_i)<=p` implies
`tr(RW_iR^T)<4p`; this follows by expressing the factor in coordinates
of `A^(1/2)`. Thus every transformed item entry has magnitude below
`4p`. The resulting entry bound is independent of the conditioning of
the untransformed matrices.

Round each upper-triangular item entry downward to the mesh
`delta=epsilon/(2pn)`, including negative entries. Do not round the common
prior. Keep the exact least activation cost for each vector of sums of
these integer labels. The processing index and forced-item rule complete
the state. Replacing a partial support by a cheaper support with the
same labels preserves all remaining item choices; no spectral argument
is required at intermediate stages.

For two final supports with the same key, each matrix-entry difference
has absolute value below `n delta`. This remains valid when the two
supports have different cardinalities: each sum of floor residuals lies
in `[0,n delta)`. Consequently

```text
||K'_T-K'_S||_2 <= p n delta <= epsilon,
K'_S >= I,
(1-epsilon)K'_S <= K'_T <= (1+epsilon)K'_S,
```

where `K'_S=RK_SR^T`. The choice of mesh has a spare factor of two.

An arbitrary congruence changes the distinguished Schur-complement
coordinate. It is essential to use the common transformed affine vector
`c=R e_p`:

```text
g(S) = min_(c^T w=1) w^T K'_S w.
```

Taking the last-coordinate Schur complement of `K'_S` without transforming
this constraint would be wrong. The variational formula directly transfers
the two Loewner inequalities to the displayed bounds on `g`.

For zero-gain optimal supports, let `N={i:lambda_i<0}`. Then
`lambda(N)<=lambda(S)` for every support and `g(N)>=0`, so
`f(N)<=f(S)` whenever `g(S)=0`. Thus the proposed fallback is valid even
if it has positive gain. If `B=0`, it is exact.

There are at most `(n+r)^p` branches. For fixed `p`, each of the
`p(p+1)/2` integer coordinates has `O(p^2 n^2/epsilon+n)` possible
values. Exact rational cost addition and comparison have polynomial bit
complexity. Fixed-dimensional inverses, LDL factors, powers of two, and
integer floors also have polynomial bit complexity. Tiny pivots enlarge
bit lengths, not the range of rounded state coordinates.

## 3. Stronger budget and ridge consequences

**One exact budget.** Replace the stored activation cost by an exact
nonnegative rational cost `c(S)`. Retain states with `c(S)<=C`, where
`C>=0` may be binary encoded. For every feasible target, its representative
costs no more and remains feasible. Maximizing gain over the retained
feasible supports therefore gives

```text
g(output) >= (1-epsilon) max_(c(S)<=C) g(S).
```

This is a genuine deterministic FPTAS for budgeted gain at fixed rank.
No budget expansion into a pseudo-polynomial graph is necessary. The
empty support handles a zero optimum. A cardinality state adds at most
`n+1` values and preserves cardinality exactly. For an upper cardinality
bound the same empty fallback works. For exact cardinality `k`, first
check the cost of the `k` cheapest items; that supplies a feasible
fallback if every feasible support has zero gain.

The single stored cost cannot simultaneously preserve an independent
budget `c` and an arbitrary penalized objective `lambda`. Such a claim
would need an additional argument. Likewise, multiple exact binary-encoded
budgets do not follow from keeping one minimum scalar label.

**Positive ridge-loss objective.** Suppose the linear term has the form
`b=Uy` for a rational response vector `y`. The fixed-support optimum of

```text
||U^T x-y||^2 + x^T D x
```

is

```text
ell(S) = y^T [I_r + sum_(i in S) u_i u_i^T/d_i]^(-1) y.
```

Apply the two-sided PSD-cover argument directly to the `r`-dimensional
information matrix in this formula. The prior is now positive definite.
It yields `ell(T)<=ell(S)/(1-eta)`. With nonnegative activation costs
stored exactly, the same representative satisfies

```text
lambda(T)+ell(T) <= [lambda(S)+ell(S)]/(1-eta).
```

Taking `eta=epsilon/(1+epsilon)` gives a multiplicative `(1+epsilon)`
FPTAS for this positive penalized ridge objective. With a stored budget
cost instead, it gives a budgeted residual-minimization FPTAS. The
response alignment `b=Uy` is a substantive restriction: a relative
gain approximation for general unrelated `b` does not automatically
give relative accuracy for a shifted residual objective.

## 4. Prior work and significance assessment

The repository's
[2026-09-12 DAG PSD approximation-set theorem](../notes/research-20260912-dag-psd-approximation-set.md)
already proves a two-sided relative Loewner cover in fixed dimension
using maximum-volume factor bases, dyadic normalization, signed-entry
rounding, and owner forcing. It handles singular ranges too. Its
[represented-matroid extension](../notes/research-20260912-represented-matroid-psd-approximation-set.md)
provides another existing feasible-family extension. The current method
is not a new matrix approximation construction. Keeping the exact least
cost in each state is the relevant modification for an exact scalar
budget; the Schur complement and ridge identities supply applications.

[Brown, Laddha, and Singh (2024), *Fast algorithms for maximizing the
minimum eigenvalue in fixed dimension*](https://arxiv.org/pdf/2401.14317)
already use guessed subsets, normalization, filtering, and forced
elements. Their matrix-selection schemes under matroid constraints have
an accuracy-dependent exponent, unlike the proposed polynomial
dependence on `1/epsilon`. These ingredients should be credited. Their
read statements do not give this one-budget sparse-quadratic FPTAS.

[Askari, d'Aspremont, and El Ghaoui (2022), *Approximation Bounds for Sparse
Programs*](https://arxiv.org/pdf/2102.06742)
directly study low-rank losses with ridge regularization and sparsity
penalties. Corollary 3.1 gives a feasible objective at most the bidual
value plus `lambda(r+1)`. Thus exploiting low rank and obtaining additive
sparse-ridge guarantees are established. Their displayed bound is not
an arbitrary-accuracy FPTAS, and their displayed penalty is uniform.

[Gao and Li, *A polynomial case of cardinality constrained quadratic
optimization problem*](https://optimization-online.org/wp-content/uploads/2010/09/2721.pdf)
give an exact polynomial algorithm under a different spectral assumption:
the `n-k` largest eigenvalues coincide. This is scalar identity minus a
rank-`k` PSD matrix, rather than scalar identity plus a low-rank PSD matrix.
It does not directly subsume the reviewed class.

A delegated literature audit also inspected
[Vreugdenhil et al. (2021)](https://proceedings.mlr.press/v139/vreugdenhil21a/vreugdenhil21a.pdf),
[Pilanci, Wainwright, and El Ghaoui (2015)](https://people.eecs.berkeley.edu/~elghaoui/Pubs/SparseLearningBoolean.pdf),
and [Xie and Deng (2020)](https://optimization-online.org/wp-content/uploads/2018/06/6652.pdf).
Their low-rank formulations, relaxation-based additive bounds, and
ridge-dependent greedy guarantees are relevant antecedents; the audit
did not identify the present fixed-rank arbitrary-accuracy scheme there.
This bounded search does not prove novelty.

The budgeted gain and positive ridge-loss consequences are stronger
claims than the original additive penalized statement. They identify a
class where binary support selection admits arbitrary requested accuracy
despite large numerical conditioning. The state exponent grows
quadratically in rank and the construction is not yet a practical solver.
A stronger publication case needs a broader direct-priority audit,
careful application positioning, and comparison with established
fixed-dimensional design and multiobjective approximation schemes.

## 5. Exact verification record and limits

Targeted command actually run:

```text
python research-20260927/sparse_psd_review_check.py
```

Final output:

```text
cases=11 nonsingular_support_branches=137 DP_key_collisions=66 target_replacements=20
largest_observed_relative_gain_loss=1/25790417485129681246442840
All exact support, Schur, normalization, rounding, Loewner, cost, budget, and cardinality assertions passed.
```

The checker exhausts small supports, selects each target's maximum-volume
branch, performs the exact rounded-label dynamic program, and checks
Schur identities, normalization, principal-minor PSD tests, transformed
affine vectors, representative costs, budget boundaries, and cardinality
bounds. Cases include signed activation costs, all-zero gains, very large
and very small rational scales, and collisions of rounded states. The
budget case includes a cost of `2^40`, without expanding a budget axis.

A first extension of the checker reused a local variable name and failed
before its assertions; that implementation error was corrected and the
complete command was rerun successfully. The checker is a separate
review artifact, not the production algorithm or a complexity proof.
It verifies finitely many instances, not the universal theorem or external
novelty. No project-wide checks or CI inspection were performed, and no
new Lean formalization was attempted in this review.
