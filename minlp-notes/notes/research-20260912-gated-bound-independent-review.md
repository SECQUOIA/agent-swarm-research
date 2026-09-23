# Independent review of the gated-information bounds

Date: 2026-09-12. **Verdict: the matrix inequalities and design guarantees
pass.** The sharpness example needs a small domain repair if every feasible
information matrix is required to be positive definite. The statistical
interpretation should also state the Gaussian assumption already present in
the linked source audit. Neither issue changes the derived constants.

This review independently checks
[the bounds note](research-20260912-gated-information-bounds.md), including
arbitrary feasible families, a common positive semidefinite prior, singular
selections, the direction of optimization bounds, covariance scaling, and the
rank refinement. It assesses mathematical validity, not publication priority.
No author file or literature record was edited, and no literature index check
was run.

| Claim | Finding |
| --- | --- |
| `M(S) <= G(S) <= alpha M(S)` | Correct for `0 < m <= M` and `J0 >= 0`. |
| D-efficiency and trace-information factor `1/alpha` | Correct when the gated selection optimizes the corresponding criterion over the same family. |
| Trace-inverse approximation factor `alpha` | Correct for positive definite information, with minimization in both models. |
| Three-observation sharpness and rational approximation | Correct after resolving the zero-information second singleton; an explicit positive replacement preserves sharpness. |
| Positive diagonal rescaling invariance | Correct when both covariance and sensitivities are transformed. |
| Rank-refined logdet loss | Correct, including with a singular positive semidefinite prior when total information is positive definite. |
| A global gated logdet upper bound bounds the marginal optimum | Correct; it does not require the condition-number bound. |

For the statistical interpretation, the note should repeat the assumption
`Y = mu(theta) + epsilon`, with `epsilon ~ N(0,R)` and parameter-independent
`R`. Then `F` is the sensitivity of the mean, and the displayed marginal
matrix is the exact Fisher information at the specified parameter, plus the
common prior information. Known covariance alone does not determine Fisher
information for an arbitrary noise distribution. Alternatively, the matrices
can be defined as generalized least-squares information, with all the matrix
conclusions unchanged. The source audit already makes the Gaussian assumption
explicit, so this is a clarification of the bounds note's standalone scope.

The spectral assumption should explicitly read `0 < m <= M`, rather than
only `mI <= R <= MI`. Positive definiteness of `R` does not itself force a
user-supplied lower bound `m` to be positive. The equal-endpoint case `m=M`
is valid and gives `alpha=1` and equality of the two models.

To verify the lower comparison and rank claim together, partition the
covariance for a proper nonempty selection as

```text
R = [[A,B],[B^T,C]],
H = C - B^T A^{-1} B > 0.
```

Block inversion gives

```text
(R^{-1})_SS - A^{-1} = A^{-1} B H^{-1} B^T A^{-1} >= 0,
G(S)-M(S) = F_S^T A^{-1} B H^{-1} B^T A^{-1} F_S.
```

Thus the discrepancy is positive semidefinite and its rank is at most
`rank(B)`. It vanishes exactly when `B^T A^{-1} F_S=0`. No positive
definiteness of the prior is needed. Selecting all observations gives equality
directly; selecting none gives the common prior, under the natural empty-data
convention.

For the upper comparison, every eigenvalue `t` of `R` obeys
`(t-m)(M-t) >= 0`. Dividing by `t>0` proves

```text
R + Mm R^{-1} <= (M+m)I.
```

Compression therefore gives

```text
K = (R^{-1})_SS <= ((M+m)I-A)/(Mm).
```

The final step is valid despite possible noncommutation of `A` and `K`:
it compares a function of `A` with another function of `A`. For each
eigenvalue `t>0` of `A`,

```text
t(M+m-t) <= (M+m)^2/4,
((M+m)I-A)/(Mm) <= alpha A^{-1}.
```

Congruence and the common prior then give

```text
G <= J0 + alpha F_S^T A^{-1}F_S
  = alpha M - (alpha-1)J0 <= alpha M.
```

This also verifies that adding the prior does not reverse or enlarge the
factor. The cited paper states the matching normalized-positive-map inequality
in its opening equation; coordinate compression is such a map. The attribution
is appropriate. [Moradi, Furuichi, and Heydarbeygi, *New Refinement of the
Operator Kantorovich Inequality*, Eq. (1)](https://www.mdpi.com/2227-7390/7/2/139).
The publisher's indexed text was available; direct page retrieval returned
HTTP 429. The proof above supplies the independent mathematical check.

Singularity cannot occur in only one of the two information matrices. Since
both covariance factors are positive definite,

```text
ker M(S) = ker G(S) = ker J0 intersect ker F_S.
```

Consequently, restricting a feasible family to selections with positive
definite information restricts both models identically. For logdet and
trace-inverse optimization, this restricted family must be nonempty. Another
consistent convention is to assign singular matrices logdet value `-infinity`
and trace-inverse cost `+infinity`, while requiring at least one positive
definite feasible selection. Replacing inverses by pseudoinverses would be a
different criterion and is not needed here. Trace-information maximization
itself remains defined for all positive semidefinite matrices; when its
optimum is zero, its inequality form remains valid but an efficiency ratio
`0/0` is undefined.

The objective comparisons use a separate gated optimizer for each criterion.
Writing `d_X(S)=logdet X(S)`, the D-optimal guarantee follows from

```text
d_M(S_G) >= d_G(S_G)-p log(alpha)
         >= d_G(S_M)-p log(alpha)
         >= d_M(S_M)-p log(alpha).
```

Exponentiation and the `p`th root give precisely `1/alpha`; a determinant
ratio without the root has lower bound `alpha^{-p}`. An additive gated
logdet suboptimality of `delta>=0` adds `delta` to this loss bound.

For trace information, write `t_X(S)=trace X(S)` and let the two selections
maximize their respective trace objectives. Then

```text
t_M(S_G) >= t_G(S_G)/alpha
         >= t_G(S_M)/alpha
         >= t_M(S_M)/alpha.
```

For inverse trace, inversion reverses Loewner order and gives

```text
(1/alpha)M(S)^{-1} <= G(S)^{-1} <= M(S)^{-1}.
```

With `a_X(S)=trace(X(S)^{-1})` and the two selections minimizing their
respective objectives,

```text
a_M(S_G) <= alpha a_G(S_G)
         <= alpha a_G(S_M)
         <= alpha a_M(S_M).
```

These proofs use only pointwise inequalities and optimality over the common
family. They require no budget structure, cardinality rule, inclusion
monotonicity, or independence between selections. They also hold for any
choice among tied global optima.

The phrase “gate-optimal design” should make this criterion-specific meaning
explicit. A selection maximizing gated logdet is not automatically covered
by the trace or inverse-trace guarantee. For example, with `R=I`, hence
`alpha=1`, designs with information `diag(100,1/100)` and `diag(4,4)` have
determinants `1` and `16`, but traces `100.01` and `8`. D-optimality selects
the smaller trace. Likewise, between `diag(100,1/4)` and `diag(4,4)`,
D-optimality selects the first, whose inverse trace is `4.01`, exceeding
the second's `0.5`. Both examples can be realized with rational sensitivity
rows and the two feasible coordinate pairs of a four-observation experiment.
These examples identify an interpretation to exclude; they do not contradict
the intended three separate guarantees.

The original sharpness witness correctly computes marginal information
`(1,0,b^2)` and gated information `(alpha,0,b^2)`. However, its second
singleton has zero information, so its logdet and inverse are outside the
note's stated positive definite domain unless an extended-value convention
is supplied. The smallest repair that retains all three singleton selections
is

```text
F = [1,1/2,b]^T.
```

For the same covariance, the values become

```text
marginal: (1,1/4,b^2),
gated:    (alpha,alpha/4,b^2).
```

All three are positive, and `1<b^2<alpha` still makes observation 1 the
unique gated optimizer and observation 3 the unique marginal optimizer.
The true D-efficiency and trace-information ratio are `1/b^2`; the
inverse-trace cost ratio is `b^2`. Thus their limiting values are respectively
`1/alpha` and `alpha`. More precisely, the efficiency guarantee is sharp
as an infimum, while the logarithmic loss `log(b^2)` is sharp as a supremum
`log(alpha)`. At `b^2=alpha`, the bound is attained if a gated tie is resolved
in favor of observation 1, but the strict sequence avoids any reliance on
tie-breaking.

For every fixed rational `rho` in `(0,1)`, rational `b` values are dense in
`(1,sqrt(alpha))` and can approach the upper endpoint from below. Hence both
`R` and the repaired `F` can remain rational throughout the sequence.
For example, `rho=3/5` gives `alpha=25/16`; rational `b` can approach `5/4`
from below. Rational `rho` values can also approach one. Each covariance in
that sequence remains strictly positive definite, while `alpha` diverges.
No singular limiting covariance is used as a feasible instance. This proves
the absence of a covariance-independent positive D-efficiency or
trace-information guarantee in the stated class.

If sharpness is wanted separately for every information dimension `p`, take
`p` independent copies of the repaired witness and a feasible family
consisting of the set of all first observations and the set of all third
observations. Give each copy sensitivity only in its corresponding parameter.
The covariance condition number is unchanged. The two relevant marginal
matrices are `I_p` and `b^2 I_p`, and their gated matrices are `alpha I_p`
and `b^2 I_p`. The D-optimal loss approaches `p log(alpha)`, and the
D-efficiency approaches `1/alpha` in each dimension.

Diagonal covariance scaling is also exact. For positive diagonal `D`, write
`D_S` for its selected block. Then

```text
(DRD)_SS = D_S R_SS D_S,
((DRD)^{-1})_SS = D_S^{-1}(R^{-1})_SS D_S^{-1},
(DF)_S = D_S F_S.
```

Substitution cancels the diagonal factors in both information matrices.
The prior is unchanged. Taking `D_ii=1/sqrt(R_ii)` therefore allows the
factor to use the correlation matrix's spectral condition number. This
normalization need not minimize the condition number, and the note does not
claim it does. The proof specifically uses preservation of coordinate
subsets; a general transformation that mixes observation coordinates would
not provide the same selection invariance. Cross-covariance rank is preserved
by this diagonal scaling as well.

For the logdet refinement, when `M(S)>0`, define

```text
E = M(S)^{-1/2}(G(S)-M(S))M(S)^{-1/2}.
```

Then `E>=0`, its rank is at most `q_S=min(p,rank(R_ST))`, and
`I+E <= alpha I`. The generalized eigenvalues of `(G,M)` are the eigenvalues
of `I+E`, so at least `p-q_S` are exactly one and the others lie in
`[1,alpha]`. Summing their logarithms gives the displayed bound (4).
In the optimization proof, it suffices to bound the discrepancy at `S_G`:

```text
optimal marginal logdet - logdet M(S_G)
    <= logdet G(S_G) - logdet M(S_G)
    <= q_{S_G} log(alpha).
```

The stated uniform `min(p,r)` bound follows immediately. In particular,
zero cross-covariance rank makes the two objectives equal, including their
optimizers up to ties.

Rank one does not improve the worst-case multiplicative inverse-trace factor
below `alpha`. For any `p>=2`, use the repaired three-observation covariance,
put all observation sensitivities in the first parameter, and use the common
prior `J0=diag(0,L,...,L)` with `L>0`. At the gated and marginal optimizers,
the true matrices are respectively `diag(1,L,...,L)` and
`diag(b^2,L,...,L)`. Their inverse-trace cost ratio is

```text
(1+(p-1)/L)/(1/b^2+(p-1)/L).
```

All singleton information matrices are positive definite, and the uniform
cross-covariance rank is one. Letting `L` grow and then `b^2` approach
`alpha` makes the ratio approach `alpha`. This verifies the intended limit
of the rank refinement. A more precise replacement for “does not give a
dimension-free improvement” is “rank one can still approach the full
multiplicative factor alpha for trace-inverse cost,” since the original
factor is already independent of dimension.

The global-bound contract has the correct maximization direction:

```text
max_S logdet M(S) <= max_S logdet G(S) <= U_G.
```

A feasible selected design with positive definite marginal information
provides the lower bound by direct evaluation. Thus `U_G-logdet M(S)` is
a valid absolute marginal optimality gap when both supplied values are
valid bounds. The pointwise lower comparison alone proves this statement;
the factor `alpha` is unnecessary. A globally valid relaxation upper bound
for the gated maximum is sufficient, even without finding a global gated
optimizer. A feasible gated objective value or a local solver's estimate
does not supply that upper-bound guarantee. If a solver instead minimizes
negative logdet, its valid lower bound must be negated to obtain `U_G`.
Objective normalization, the prior, and the feasible family must agree
between the reported bounds and the stated matrices. The author's remarks
about solver tolerances correctly distinguish this mathematical implication
from a claim of certified numerical arithmetic.

Independent executable checks used the available Python environment with
NumPy, SciPy, SymPy, and exact rational arithmetic. The repaired rational
example `rho=3/5`, `b=6/5` gave marginal values `(1,1/4,36/25)`, gated values
`(25/16,25/64,36/25)`, and covariance determinant `16/25` exactly. Exact
diagonal invariance passed for all seven nonempty subsets under
`D=diag(2,1/3,5)`.

A separate seeded numerical check generated 100 covariance and sensitivity
instances, with 2–7 observations, 1–4 parameters, condition numbers
`1`, `3`, `20`, and `10000`, and prior ranks ranging from zero to full rank.
It checked both Loewner inequalities and diagonal invariance on 4,092
selections, and generalized eigenvalue and rank-refined logdet bounds on
3,675 positive definite selections. It also checked the three separately
optimized criteria and the global upper-bound direction on 400 sampled
feasible families. All checks passed with floating-point tolerances, including
a scaled Loewner tolerance of `2e-9` and an absolute logdet tolerance of
`2e-7`.
Exact rational evaluations of the rank-one inverse-trace construction for
`p=1,2,10,100` approached `alpha=1.5625` as predicted. These computations
are finite corroboration; the derivations above establish the universal
claims.

Reviewed source snapshot, before subsequent author revisions:

```text
ace91772212531de3e4d5b1e7417cbb28caf573053fe239ff1adb079a58db1f7  notes/research-20260912-gated-information-bounds.md
```
