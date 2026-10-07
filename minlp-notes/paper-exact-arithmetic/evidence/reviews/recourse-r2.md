# Recourse manuscript review, round 2

Reviewed the repaired actual Section 10 and Appendix I on 2026-10-05.
I read the entire round-one review and author response
`authoring/repair-recourse-r1.md`, then checked every listed repair in
the manuscript. Independent delegated reviews checked the changed
fallback/QP/coupled interfaces and the fiber/lattice/completion
interfaces. The full analytic chain reconstructed in round one is
unchanged except for the local corrections described here.

All round-one findings are resolved. The author's additional rational
fallback bound and integer precision changes are valid. Three further
local contract/edge issues found during this review were repaired by
root and reread in the final files. No unresolved internal mathematical,
algorithmic, or output-contract finding remains in the assigned scope.
V1–V5 and RQ1–RQ4 retain their unconditional statements under their
printed promises; no selected-core oracle assumption was introduced.

Final reviewed SHA-256 hashes:

- `sections/10-recourse.tex`: `b70d6f940a2df502ce61b5e4168ce1d7a3dadf59ced7244a17ea90e1299543b4`
- `appendices/I-recourse.tex`: `f4c21d1ad36fac74449315f3b4a20c4c1652e41e50797e657796c8b0e526d155`

## Verification of the round-one repairs

Locations below refer to these final versions. Every row is resolved.

| Repair | Actual location and verification |
| --- | --- |
| Rational higher-degree error constant | I:1407–1416 uses the integer exponent `ceil((D-1)/2)`. The coefficient vector has at most `(n+1)^(D-1)` entries, so the new factor majorizes its Euclidean norm. It leaves the uniform modulus valid and makes the supplied constant rational. |
| Rational fiber error constant | I:1517–1534, shifted by the new empty-residual branch, uses `m` as a rational upper bound for `sqrt(m)/2` in the gradient-row estimate and in Gamma. The transverse and Hoffman inequalities remain valid, and Gamma is at least 1 with polynomial encoded length. |
| Arbitrary tolerance encoding | I:47–51 counts `<eta>`, matching the shared convex-value lemma. Actual call bounds appear at I:409–411 (cells), I:973–975 (joint convexity), I:1452–1456 (supplied convexifier), and I:1904–1906 (cubic completion). All tolerances are short structured rationals; replacing logarithmic accuracy by encoded length preserves the stated work bounds. |
| Thin residual QP | I:1047–1070 reduces the rational fiber to its affine hull. The zero-dimensional branch returns its rational point. Otherwise the reduced polytope has nonempty interior, so convexity forces the constant symmetric restricted Hessian `B'^T A_zz B'` to be positive semidefinite. Exact QP then returns a rational residual optimizer; LP reduction and reconstruction are charged. |
| Unit-box lattice approximation | Main:463–464 requires `hat a in [0,1]^r`. I:1670 onward applies the monomial Lipschitz estimate to both points in that box; the actual base stage clips, and I:1862–1864 explains that clipping cannot increase coordinate error. |
| Zero restricted Hessian | I:1515–1520 separates `H_A=0`, where the kernel is all of the residual space and Pi=0, from the positive-eigenvalue branch. The undefined eigenvalue is never used in the zero branch. The gradient-row/Hoffman argument still handles affine fibers. |
| Optimal-slice necessity | I:1373–1379 defines the reduced optimal set first. Optimality gives E=0 and hence the rational-row equations. Conversely those equations imply E=0. The subsequent Hoffman application therefore uses the established equality of sets. |
| Strict outer ball | I:1276–1281 uses `R_0=1+sum m_j` and proves strict containment in the open outer ball. It also records the closed inner ball. The reflection at I:1337 now lies strictly inside the inner ball. |
| Symmetric quadratic matrix | I:988–989 explicitly assumes symmetry; I:1030–1032 chooses A as the constant symmetric Hessian. Tangent stationarity, the denominator bound, and continued-fraction recovery retain their valid hypotheses. |
| Sampled coefficient length | I:29–32 proves `b<=L+2 log_2 M`. Multiplying numerator and denominator of sigma by integers of magnitude less than the power of two M adds at most `log_2 M` to each encoded component; reduction cannot increase that length. |
| Las Vegas complexity qualifier | Main:31–34 and the degree-four proof at the end of I explicitly require expected polynomial running time. The finite law is sampled with polynomially many fair coins. |
| Product-box scope | Main:25–30 and :611–620 distinguish residual convexity on product boxes from supplied convexifiers on coupled polytopes. The full-point summary also retains the cubic/global-convexity alternatives of the actual theorem. |
| Supplied rational margin lengths | Main:347–357 declares delta and mu rational. I:1536–1538 counts their encoded lengths; I:1879–1882 proves the certified values have polynomial length before computing Gamma. No hidden arbitrary-real input is passed to a bit algorithm. |
| Earlier incumbent witness | I:863–866 says that the witness can come from a level at most J and computes the lower bound from its value. The existing refinement invariants still give the value and selected-core certificate. |
| Finite growth threshold | I:736–740 and :748–759 state and prove the inequality for every finite `0<t<=g`, including the single-core case with infinite g. Every algorithmic caller uses the finite threshold g_0. |
| Original-coordinate map bound | I:1385–1386 uses `B_F=max{1,sum absolute entries}`. This majorizes the operator norm and meets the lower bound required for the computed Gamma. |

## Additional changes and issues resolved during round two

**Rational fallback G and integer precision.** I:329–337 constructs
`G=max{1,G_f+k sigma}`. Coefficient sums give a rational G_f, and
`||gamma||<=sqrt(k) sigma<=k sigma`, so G is a uniform rational bound.
For `Q=q+1+ceil(log_2(nG))`, coordinate error at most `2^-Q` gives
Euclidean error at most `sqrt(n) 2^(-q-1)/(nG)<=2^-q/(2G)`.
The required ceiling is computed by comparing a rational with powers of
two, without evaluating a transcendental number. Its extra precision has
polynomial base length. The feasible output and objective lower bound
therefore retain their every-draw guarantee. I:1928–1937 similarly uses
`q+ceil(log_2 n)` on full-point rejection. This yields the requested
Euclidean error while preserving the same singleton selector and
base-only fallback work factor.

Three newly noticed local issues were reported to root and resolved:

- I:55–58 now restricts the exact PSD QP tool to nonempty bounded rational
  polytopes. This fixes the formerly unqualified existence assertion;
  every actual call already satisfied those conditions.
- I:1479–1481 handles `m=0` before the fiber constants. The residual set
  consists of the empty vector, all matrix/kernel claims are vacuous,
  and Gamma=1 proves the error bound. Positive residual dimension is
  assumed only for the remaining formulas. This completes the full
  proposition without narrowing its statement.
- Main:477–478 and I:1691–1694 include `<hat a>` in the lattice test and
  construction costs. Exact degree-two monomial evaluation and rational
  rounding now have their input length charged. The rounded basis still
  has O(log T) entry bits. Actual base-stage approximations already have
  polynomial length, so the expected-work theorem is unchanged.

## Preservation of the proof and source interfaces

The all-scale maximum-simplex count, conjugate pushforward measure,
covering estimate, polynomial-size QR event, hybrid finite-law transfer,
retained hull, and cap accounting remain the round-one proved chain.
Growth and fallback use one event and one work factor for all precision
queries. The repaired integer thresholds only strengthen the requested
accuracy. No resampling, almost-sure substitution, or coefficient-height
inflation of the base fallback factor was introduced.

The supplied-convexifier and product-box completions still regularize in
the original norm and approximate the fixed minimum-norm selector.
The rational majorants preserve the effective error exponents and
`O_D(q)+poly_D(L)` precision. Cubic completion remains
`8q+poly(L)` with absolute exponents. Exact quadratic output still
promises some rational residual optimizer with the selected core, as
stated, and the product-box cubic theorem still makes no unconditional
quartic or unsupplied coupled-domain extension.

I:98–103 now separates Renegar's arbitrary-real structural statement
from its integer coefficient-height and bit-work statement. The former
controls scalar sections with other noise values and thresholds fixed
as real coefficients; only denominator-cleared rational data enter the
bit computation. The vetted local `literature-review.md` contract table
confirms that split. The exact LP pinpoint matches the same table and
the shared value proof. Univariate isolation remains an explicitly
integer-polynomial bit contract with an absolute exponent. Bibliography
and classical pinpoint integration are tracked by root and Luna; this
review adds no source-contract request and performs no source research.

## Targeted document checks and final status

The scoped recourse reference check found 70 distinct references, all
resolved, and no duplicate labels defined by these two files. During the
ongoing bibliography integration, six recourse keys were still absent at
the check time: `EvansGariepy2015`, `Hoffman1952`, `Renegar1992QE`,
`Rockafellar1970`, `Schrijver1986`, and `SpielmanTeng2004`. This is the
root-tracked integration work, not a new internal proof finding.

Checks actually run: read-only `cat`, `sed`, `nl`, `rg`, and
`sha256sum`; the inline Python reference/citation document check;
`git diff --check -- paper-exact-arithmetic/evidence/reviews/recourse-r2.md`;
and a scoped text check of this owned review file. The final two checks
passed. Hashes were refreshed after root's three additional fixes.

No manuscript edits, mathematical scripts, experiments, historical
checker reruns, full-manuscript verification, project-wide checks, CI
inspection, or literature browsing were performed. Analytic and
algorithmic acceptance is complete for the assigned recourse scope.
