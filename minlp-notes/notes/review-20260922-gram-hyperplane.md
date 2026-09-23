# Independent adversarial review of the sharp Gram-map HHC theorem

Date: 2026-09-22. Reviewed independently from the proof in
[the Gram-map note](research-20260922-gram-hyperplane.md). Scope: the full
map `(X,t) -> (XX^T,t²)`, its exact hyperplane image, the sharp threshold,
and the stated literature and significance boundaries.

**Verdict:** no mathematical error found. The theorem and image formula
are correct with the scalar exception as stated. This is a proof review,
not formal verification or certification of novelty. Its best present role
is a sharp structural lemma supporting the aggregation construction; its
classical ingredients should not be promoted as new matrix analysis.

## Exact attainability and degeneracies

The main potential failure was replacing an attainable set by its closure,
or silently assuming that the orthogonal group is connected. Neither occurs.

Fix `G PSD`, with rank `s`, and `r>=k`. In an eigenbasis of `G`, the last
`k-s` rows of any factor `X` with `XX^T=G` vanish. Normalize its first `s`
rows by the positive eigenvalue square roots. These rows are orthonormal in
`R^r`; completing them to `k` orthonormal rows is possible because `r>=k`.
Undoing the eigenbasis change proves `X=G^(1/2)Q`, `QQ^T=I_k` even for
singular `G`. This includes `G=0`.

For `C=G^(1/2)B`, its rectangular SVD reduces the linear functional on
these factors to `sum_j s_j R_jj` on a subset parametrized by `R in O(k)`.
The entire fiber is compact, and the elementary diagonal-entry bound gives
the attained endpoints `±sum_j s_j`. Compactness alone would not fill the
gap between the endpoints; the component argument is essential.

For every `k>=2`, a cyclic permutation without fixed points has zero
diagonal. Negating one row preserves zero diagonal and changes its
determinant. Thus each determinant component of `O(k)` contains a zero of
the functional. Each component is connected, and a continuous real-valued
function on it has interval image. The component containing `I` therefore
supplies `[0,M]`; the component containing `-I` supplies `[-M,0]`, where
`M=sum_j s_j`. This remains true when `k` is odd, when these endpoints lie
in different components. When `k` is even they lie in the same component,
which only simplifies the argument. Zero singular values do not affect it.

Consequently every interior value, both endpoints, and zero are actually
attained. There is no limiting factor construction here. For `k=1,r>=2`,
the corresponding sphere is connected, so the same conclusion follows.

For `T>=0`, choosing `t=sqrt(T)` requires the trace value `-beta*sqrt(T)`.
The interval argument gives exactly

```
beta² T <= [tr((G^(1/2)BB^T G^(1/2))^(1/2))]².
```

The following edge cases check against the original equations:

- If `B=0` and `beta!=0`, then `t=0`, and the formula forces `T=0`.
- If `beta=0`, each Gram matrix admits a factor orthogonal to `B`, so
  arbitrary `T>=0` is permitted. This would fail for one-dimensional square
  factors, which explains why the scalar exception cannot be suppressed.
- If `G^(1/2)B=0`, the linear functional vanishes on the entire fiber, and
  the displayed inequality correctly requires `beta²T=0`.
- `B=0,beta=0` does not define a proper hyperplane. The formula remains
  valid for the full domain, but this extra degenerate case is not needed
  for the HHC quantifier.

For `k=r=1`, a hyperplane has a generator `(a,b)`, and its image is
`{lambda*(a²,b²): lambda>=0}`. This verifies HHC directly. The example
`x+t=0` correctly refutes the general inequality formula in that case.

## Concavity and the singular limit

The product-of-traces argument proves precisely the required *separate*
concavity. It does not rely on the false inference that squaring a
nonnegative concave function preserves concavity.

For any positive definite `Z`, weighted Frobenius Cauchy--Schwarz gives
`F_H(G)<=tr(GZ)tr(HZ^(-1))`. For positive definite `G,H`, the stated
`Z=G^(-1/2)(G^(1/2)HG^(1/2))^(1/2)G^(-1/2)` satisfies `ZGZ=H`.
Cyclicity of trace gives both traces equal to
`tr((G^(1/2)HG^(1/2))^(1/2))`, so equality follows.

For singular matrices, replacing *both* arguments by `G+epsilon*I` and
`H+epsilon*I` is valid. At each positive definite optimizer, each original
trace is nonnegative and no larger than its regularized counterpart. Their
product therefore has the same ordering. Continuity of the positive square
root gives the desired upper bound on the infimum in the limit. Combined
with the Cauchy--Schwarz lower bound, this proves equality without asserting
existence of a singular-case optimizer.

For fixed `H`, each term of the infimum is linear in `G`. Its infimum is
concave on the PSD cone, so the hypograph inequality with `T>=0` defines a
convex set. This proves convexity of the exact image, including its boundary.

For necessity, the hyperplane `t=0` retains the rank restriction
`rank(G)<=r`. When `r<k`, the two matrices specified in the note have ranks
`r` and `1`, whereas their midpoint has rank `r+1`. Both original matrices
are Gram matrices of `k by r` factors. Thus the counterexample uses actual
points and proves failure of HHC for the full output.

## Prior results and significance

The following primary sources were opened during this review:

- Uhlmann, [On “Partial” Fidelities](https://www.physik.uni-leipzig.de/~uhlmann/PDF/Uh00d.pdf),
  pp. 407–410. Page 408 explicitly states separate concavity of transition
  probability; pp. 409–410 allow unnormalized positive operators and give
  the product formula through equation (14). Page 407 also describes the
  interval of attainable squared purification overlaps. These are direct
  classical antecedents for the analytic core. The note's real orthogonal
  component argument addresses a detail not supplied merely by invoking
  complex purification geometry.
- Blekherman–Dey–Sun, [Aggregations of quadratic inequalities and hidden
  hyperplane convexity](https://arxiv.org/html/2210.01722v2), Definition 2.1
  and Lemma 2.5. The definition uses linear hyperplanes through the origin,
  exactly as the note does. Lemma 2.5 confirms preservation under linear
  transformations of output. The consequence for finitely many repeated
  quadratic forms is therefore a correct application of the full-map
  statement, not a separate new preservation principle.
- Beck, [Convexity Properties Associated with Nonconvex Quadratic Matrix
  Functions and Applications to Quadratic Programming](https://www.tau.ac.il/~becka/22.pdf),
  JOTA 142 (2009), especially Section 3 and Theorem 3.1. This primary full
  text was reached from the author's publication page. Theorem 3.1 proves
  ordinary image convexity for at most `r` real quadratic matrix functions
  of order `r`, allowing affine terms. Its homogenization uses an `r by r`
  matrix variable. This is not the scalar homogenization in the reviewed
  theorem, and the inspected statement does not give arbitrary-hyperplane
  convexity of the full Gram output at `r=k`. A complete equivalence audit
  remains necessary; different hypotheses alone do not prove novelty.

Searches included `"Gram" "hyperplane" "convexity"`, `"quadratic matrix
programming" "convexity" Beck`, `"Gram matrix" "linear constraint" "convex"
fidelity`, and `"quadratic matrix" "hyperplane" convexity`. They did not
identify an exact prior statement. This is limited discovery evidence.
The reviewed note's rotation-matrix source was not independently inspected
in this review, so this review does not certify that source comparison.

The theorem materially strengthens the draft sufficient threshold `r>=3k`
to the optimal `r>=k` for this full map. It also avoids a constraint-count
bound, which can matter when the repeated quadratic family has many forms.
Those are concrete structural benefits. They do not by themselves show a
new general SDP exactness result, a solver speedup, or an efficient finite
description of the original feasible hull. The particularly useful current
application is reducing the replication requirement in the aggregation
counterexample. A standalone substantial-contribution claim for this lemma
would need a stronger prior-art comparison or a consequential new use.

## Verification boundary

I independently reconstructed the singular factorization, interval argument,
variational identity and its boundary limit, scalar exception, and rank
obstruction. No correction to the reviewed proof was required. Repository
checks were limited to reading the two relevant research notes and searching
local literature filenames with `rg --files literature | rg
'beck|quadratic-matrix'`. No numerical test, Lean build, project-wide check,
or CI inspection was run. The elementary finite-dimensional proof is the
evidence for the universal claim; source inspection only informs attribution
and the limits of the novelty assessment.
