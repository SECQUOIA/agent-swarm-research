# Independent review of the class-transfer proofs

Reviewed `sections/04-classes.tex` against the definitions and core construction in `sections/02-preliminaries.tex` and `sections/03-core.tex`. This review used algebraic derivations, without literature searches or computational experiments.

## Conclusion

No substantive mathematical error found. The hardness transfers, switching identities, direct facet argument, orthogonal extension, exact violation lists, maxima, and common-denominator promises are consistent.

## Checks that determine the conclusion

- **Infinite families (lines 22–58).** On the constructed points, the full rounded-positive-semidefinite violation list has coefficient sum `±1`. Hence enlarging the hypermetric class to gap-1 or rounded-positive-semidefinite inequalities introduces no no-instance violations. The even-sum part of the union of the k-gonal families is excluded by positive definiteness. The gap-1 NP certificate is valid on arbitrary rational inputs: switching to coefficient sum one preserves the quadratic value, and the signed sum one plus odd parity proves gap exactly one after switching back.
- **Complementation identity (lines 69–86).** Substituting `x_g -> 1-x_g` into `(v^T x-s)(v^T x-s-1)` gives `(v'^T x-(s-v_g))(v'^T x-(s-v_g)-1)`. Thus both the sign change and the parameter shift in (bh-switching) are correct. Congruence gives the stated preservation of positive definiteness.
- **Facet lemma (lines 90–135).** For the two tight layers of weights `r` and `r+1`, the swap equations at subset sizes `r-1` and `r` imply equality of all quadratic coefficients. The assumptions `1 <= r <= t-2` guarantee every required subset exists, including the boundary case `t=3,r=1`. The resulting linear and constant coefficients are `-ra` and `r(r+1)a/2`. Varying outside variables eliminates all outside linear, cross, and pair coefficients, so the extension to an arbitrary support is valid.
- **Finite signed families (lines 149–195).** The two equivalent violated data pairs at the base point and their images under complementation are correct. Both have divided-form violation `1/(4N)`. For X3C, `x_i-y_ig = (7-3/2)/N = 11/(2N)`. The maximization over an unrestricted integer parameter is correct: the concave quadratic has its integer maximum at `floor(ell)` (possibly tied), which gives a polynomial-length certificate.
- **Orthogonal lift (lines 256–308).** The new slack is `g_M(z)+(1/(8q))*sum_j w_j(w_j-1)`. Since `g_M=-1/2` exactly on covers, the condition `sum_j w_j(w_j-1)<4q` is exact. The root coefficient and triangle-inequality lower bound imply gonality at least `2q-1`. For pure coefficients, writing `a` and `k` for the numbers of `+1` and `-1` extension coordinates gives `k-a >= m-1` and `k+a <= m`; therefore `a=0` and `k=m` or `m-1`. This yields precisely the two displayed types. Their violations are `(q+2)/(4qN)` and `(q+3)/(4qN)`.
- **Rounded exclusion and switching (lines 275–324).** The extended Schur parameter is `s_M+m/(8q)`, and its scaled value is strictly less than `3/4`. Thus `Y-e_0e_0^T/4` is positive definite. An odd coefficient sum of absolute value at least three forces rounded slack positive. Under the stated switching, an all-positive violator must have all extension coordinates `-1`, giving exactly support `C union U` and violation `(q+2)/(4qN)`.
- **Facets of pure and cut-form cliques (lines 326–337).** Every displayed pure vector has odd support size `2q-1 >= 5`. An all-positive cut clique on an odd support of size `t` gives the Boolean quadric clique parameter `(t-1)/2`, on `t` variables when the root is absent and on `t-1` variables when it is present. Both fall within the proved facet range. Covariance and switching preserve facets.
- **Encoding and promises (lines 339–349).** The common denominator `8qN` clears the base entries and the added `1/(8q)` entries. The moment entries are bounded by one, and positive definite unit-diagonal `Z` gives all distance and switched-distance entries strictly between zero and one. The matrix and dimension growth are polynomial. The bounded-coefficient families have immediate NP certificates.

## Optional small clarification

At lines 314–324 the proof discusses the switched vectors of coefficient sum one. A single sentence could explicitly dispose of their global negatives: an exact cover is nonempty, and its coordinates are positive after the specified switching, so a globally negated vector cannot become all-positive. The present argument already implies this and the exact-list claim is correct.

The description “finite signed-coefficient family” in preliminaries lines 173–174, together with “finite signed families” terminology elsewhere, is potentially misleading. The coefficient alphabet and the number of choices of `(S,T)` are finite, but the parameter `s` is unrestricted, so the displayed family has infinitely many members for fixed `W`. A clearer term is “signed `{0,±1}` Boros--Hammer family” or “restricted signed-coefficient family.” This is a terminology issue only: lines 189–194 correctly prove NP membership despite the unbounded integer parameter.

## Verification performed

Read the three targeted TeX source files with line numbers and rederived the formulas above. No tests, experiments, project-wide checks, or CI inspection were performed.
