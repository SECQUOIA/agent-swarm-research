# Sharp hyperplane convexity of a Gram map with one scalar square

Date: 2026-09-22. Independent proof challenge and literature comparison.

The [fresh adversarial review](review-20260922-gram-hyperplane.md) checked
the full theorem, exact attainment, singular cases, and prior-work scope.
It found no necessary correction. The coordinator separately re-derived
the trace-range and concavity arguments. This is internal proof review,
not formal certification or external peer review.

The main statement below verifies and sharpens the Gram-map construction
proposed in [the aggregation frontier](research-20260922-aggregation-frontier.md).
The dimension threshold is sharp for the full Gram map. The central
concavity identity is classical quantum fidelity theory, not a new matrix
inequality. Whether the resulting sharp HHC formulation is new remains
unsettled; the searches below do not establish novelty.

## Statement

Let `k,r` be positive integers. Define

```
Phi(X,t) = (XX^T,t²),     X in R^(k by r), t in R.
```

Hidden hyperplane convexity (HHC) means that `Phi(L)` is convex for every
linear hyperplane `L` in the domain.

**Theorem.** `Phi` has HHC if and only if `r>=k`.

For `k>=2` and `r>=k`, there is a more precise formula. Write

```
L = {(X,t): <B,X> + beta*t = 0},
H = BB^T,
F_H(G) = [tr((G^(1/2) H G^(1/2))^(1/2))]².
```

Then, including singular `G`, zero `B`, and zero `beta`,

```
Phi(L) = {(G,T): G PSD, T>=0, beta²*T <= F_H(G)}.       (1)
```

The same formula holds for `k=1,r>=2`. For `k=r=1`, HHC still holds,
but (1) need not hold: every hyperplane is a line and its image is a ray.
For example, `x+t=0` has image `{(G,T): G=T>=0}`, whereas the proposed
inequality would incorrectly include every `0<=T<=G`.

Any finite collection of quadratics

```
q_i(X,t) = tr(A_i XX^T) + c_i*t²,    A_i symmetric,
```

therefore has HHC when `r>=k`, without a bound on the number of forms.
This follows by a linear map of the full output. Necessity of `r>=k`
is asserted for the full map, not every smaller collection of forms.

## Proof of the exact image

### The trace range on a Gram fiber

Fix `G PSD`. Since `r>=k`, every factor satisfying `XX^T=G` can be
written as `X=G^(1/2)Q` with `QQ^T=I_k`. For singular `G`, extend the
orthonormal rows in its positive eigenspace to a full orthonormal row
frame; this gives the same factorization.

Let `C=G^(1/2)B`. Take a rectangular singular value decomposition

```
C = U [D 0] V^T,      D=diag(s_1,...,s_k), s_j>=0.
```

For `QQ^T=I`, changing coordinates gives

```
<B,X> = <C,Q> = sum_j s_j*(U^T Q V)_(j,j).
```

Each displayed diagonal entry has absolute value at most one. Hence the
maximum is `M=sum_j s_j`, attained by `Q=U[I_k 0]V^T`. In particular,

```
M = tr((G^(1/2) H G^(1/2))^(1/2)).
```

All values in `[-M,M]` are attained when `k>=2`. To see this without
mistaking `O(k)` for a connected set, restrict to
`Q=U[R 0]V^T`, `R in O(k)`. The functional becomes `tr(DR)`.
Each of the two determinant components of `O(k)` is connected.
Each contains a signed permutation matrix with zero diagonal: take a
cyclic permutation with no fixed points and change one row's sign to
switch determinant. Thus both components contain a point where
`tr(DR)=0`. The component containing `I` has image containing `[0,M]`;
the component containing `-I` has image containing `[-M,0]`.
These may be the same component, which causes no problem. The upper
bound already proved shows that the total range is exactly `[-M,M]`.

For `k=1,r>=2`, the Gram fiber of a positive scalar is a connected
sphere; the zero fiber is a singleton. A linear functional therefore has
the same interval range. This argument fails correctly for `k=r=1`.

For any `T>=0`, choose `t=sqrt(T)`. There exists a factor `X` with
`<B,X>=-beta*t` precisely when `abs(beta)*sqrt(T)<=M`. This proves (1),
including all its degenerate cases.

### Separate concavity of squared fidelity

For fixed `H PSD`,

```
F_H(G) = inf_(Z positive definite) tr(GZ)*tr(H Z^(-1)).  (2)
```

Here is a direct real-matrix proof, including boundary cases. Factor
`H=BB^T` and choose an `X` attaining the Gram-fiber maximum above. For
every positive definite `Z`, Frobenius Cauchy--Schwarz gives

```
M² = <Z^(1/2)X, Z^(-1/2)B>²
   <= tr(GZ)*tr(H Z^(-1)).
```

When `G,H` are positive definite, set

```
K = (G^(1/2) H G^(1/2))^(1/2),
Z = G^(-1/2) K G^(-1/2).
```

Then `ZGZ=H` and both traces in (2) equal `tr(K)`, proving equality.
For general PSD matrices, apply this equality to
`G_e=G+eI`, `H_e=H+eI`, and let `Z_e` be the optimizer just constructed.
Positivity of the traces gives

```
inf_Z tr(GZ)*tr(H Z^(-1))
 <= tr(GZ_e)*tr(H Z_e^(-1))
 <= tr(G_e Z_e)*tr(H_e Z_e^(-1)) = F_(H_e)(G_e).
```

Continuity of matrix square roots sends the final expression to
`F_H(G)` as `e` decreases to zero. This proves (2) together with the
opposite inequality already obtained. No singular optimizer is assumed.

For fixed `H`, every expression inside the infimum in (2) is a linear
function of `G` with a nonnegative coefficient. Its infimum is concave.
Consequently (1) is convex. This proves HHC for `r>=k`, with the scalar
case `k=r=1` established separately by the line argument.

### Sharpness

If `1<=r<k`, use the hyperplane `t=0`. Its image is

```
{(G,0): G PSD, rank(G)<=r}.
```

Take `G_1=diag(1,...,1,0,...,0)` with `r` initial ones and
`G_2=e_(r+1)e_(r+1)^T`. Each is attainable, but their midpoint has rank
`r+1`, so the image is not convex. This proves necessity.

## Consequences and limits

The proof preserves the whole Gram matrix and the scalar square. It gives
HHC for repeated-block quadratic families even when the number of distinct
quadratic forms exceeds the repetition count. In applications of an
aggregation theorem, that is a structural certificate independent of the
number of constraints. Additional hypotheses of the aggregation theorem
must still be checked; HHC alone is not an assertion that a given closed
feasible set has a finite conic or quadratic convex-hull description.

For `k=2`, the function in (1) reduces to

```
F_H(G) = tr(HG) + 2*sqrt(det(H)*det(G)),
```

recovering the independently verified two-row argument in
[the infinite-aggregation review](review-20260922-infinite-aggregation.md).
For `r=k`, no spare right-kernel directions are available in general;
the trace-range and fidelity proof replaces that dimension-dependent
construction.

The result does not cover arbitrary linear terms `2*t*<D_i,X>` in the
forms. It also does not establish convexity after restriction to
arbitrary codimension-two linear subspaces. Both extensions would need
new reasoning. Neither a numerical algorithm nor a speedup follows
merely from the HHC certificate.

## Literature examined and novelty assessment

Sources opened on 2026-09-22:

- Uhlmann, [On “Partial” Fidelities, Reports on Mathematical Physics 45
  (2000)](https://www.physik.uni-leipzig.de/~uhlmann/PDF/Uh00d.pdf),
  especially pp. 408--410, equations (5), (6), (13), and (14).
  The paper explicitly states separate concavity of transition
  probability, allows positive operators without trace normalization,
  and gives (2) as the full-rank instance of its general formula.
  These are direct prior results for the concavity step. The complex
  purification overlap interpretation is also closely related to the
  Gram-fiber trace calculation; the real orthogonal endpoint issue is
  addressed explicitly above.
- Uhlmann, [Algebra and Geometry in the Theory of Mixed
  States](https://www.physik.uni-leipzig.de/~uhlmann/PDF/Uh91b.pdf),
  equation (24), already records the product-of-traces variational
  identity. The PDF was opened; the searchable indexed equation was
  inspected. The 2000 source gives a clearer accessible comparison.
- Blekherman--Dey--Sun,
  [Aggregations of quadratic inequalities and hidden hyperplane
  convexity, arXiv:2210.01722v2](https://arxiv.org/html/2210.01722v2).
  The HHC definition and its preservation under linear changes of
  output match the usage here. Searches within this source for
  Kronecker structure found no match. This is insufficient to rule out
  an equivalent result elsewhere in the paper or its references.
- Ramachandran--Shu--Wang,
  [Hidden Convexity, Optimization, and Algorithms on Rotation Matrices,
  Mathematics of Operations Research 50 (2025)](https://ir.cwi.nl/pub/35175/35175.pdf),
  especially Lemma 1 and Appendix B. Lemma 1 gives the classical
  singular-value formula for the extremum over `SO(k)`; Appendix B
  relates some rotation-image convexity results to quadratic maps.
  These explain why the trace-range ingredient should not be treated
  as new. The inspected portions do not state the sharp Gram-map HHC
  theorem above. A full equivalence audit is still needed.

Search terms included `fidelity squared concave in each argument`,
`Uhlmann transition probability variational formula`, `Gram hyperplane
convexity`, `quadratic matrix programming hidden convexity`, and
`hidden hyperplane convexity Gram matrix quadratic maps`. No exact prior
statement of the full theorem was identified in these searches. This is
limited discovery evidence, not a novelty claim. The most defensible
current contribution is a sharp HHC formulation and its application to
the aggregation construction; its matrix-analytic ingredients are known.

## Verification performed

This note independently checked the exact trace range, both orthogonal
components for odd square dimensions, singular Gram matrices, zero
hyperplane coefficients, the limiting argument in (2), and the rank
obstruction. The `k=r=1` exception to (1) was identified and isolated.
No numerical tests, Lean build, project-wide checks, or CI inspection
were run for this proof-only note. The proof is mathematical review,
not formal verification. The theorem still warrants a fresh independent
review before publication.
