# Focused independent recourse and integer review, round 2

**Decision: V1 is resolved.** The immutable integration-repairs-r1 snapshot clears a positive common denominator of the squarefree root polynomial before coordinate maps, value comparisons, and auxiliary output are constructed. The resulting value resultant is an integer polynomial. The repair preserves the recovered point, value order and equality, common-root contract, and all degree, height, constant-base work and refinement bounds. No further mathematical repair is needed for this finding.

The changed strong-field antecedent and discussion output summary are also correct. The assigned mathematical scope passes, subject to the unchanged pending classical-source identity audit. This focused report closes V1 and its inherited qualifications in final-recourse-integer-sol-r1.md; it does not replace that report's full 47-result review or approve the whole paper for submission.

**Target and provenance.** I read the original manuscript and independent-review briefs, the prior final recourse review, recourse-sol-final author response, integration contract and decisions, review-disposition-final-r1 and reviews/round1-root-repairs.diff. I used scientific TeX only from evidence/snapshots/integration-repairs-r1, captured at 2026-10-06T03:59:42.813203+00:00. Its manifest SHA256 is 154e1311e97d5b858af63b1e45233908a77148e75330e5533a9ab62372542ebe.

All 20 files and line counts match that manifest. Relevant hashes are:

| Frozen file | SHA256 |
| --- | --- |
| sections/02-model.tex | 9fe94874c591d201af37daeae527ee93298baa53fb061db356eb97ebf91571c4 |
| sections/03-counting.tex | ccbe57f1117ed70fea17f6702b9cadbe1155ae5c719c9139ddad8ee6e00a1c0d |
| sections/07-recourse.tex | 6dbb5f51199e261d613afbe67a88b4bd9f8f43dfc3c2fd6bb34a22243f659c6b |
| sections/08-integer.tex | 4a4ec367b1d7076e42ed87f16f3a9d3d3e49d11a7b0ae57680b7c52b6880b3aa |
| sections/10-discussion.tex | b011835c28d33095c9c2c59a72dea31f42b5a5eb36c2d43e528858f04afa8f2a |
| appendices/A-finite-noise.tex | 31b257efb6a6ad8106a06fab5e01b1bc0723b3e2b5e2d34efe8d6a412b7e991f |
| appendices/E-recourse.tex | e3bba43cbcfa9cfd373661b350711c3f890ebb73a9994dc6dfc13fae49676e1f |
| appendices/F-integer.tex | 4ec4e5fbf8907398384e75c4b98f39888d57b603c6389aa398f78c8d58b6ccfd |

I compared this snapshot directly with integrated-mathematical-draft-r1. Section 7 and Appendix E are byte-identical. In Appendix F only the algorithm's denominator-clearance and return wording changed; the entire file from the quotient-algebra lemma to its end is byte-identical. Section 8 differs only in the strong-field antecedent passage. Its preceding text and its suffix beginning with the Bernoulli-probability sentence are byte-identical. The generic fallback statement/explanation in Section 3 and the entire shared-root/fallback proof block in Appendix A are also byte-identical. These comparisons justify carrying forward the previous review of unchanged proof blocks without repeating the 47-result audit.

Later live changes to Appendix F's bad-event definition, Section 8's closing common-root wording and Sections 1/2's companion comparisons are excluded. I did not read live scientific files to verify or approve them.

**Normalization and the genuine cubic example.** Appendix F:57–63 now first forms
\[
P_0=p/G,\qquad A=p'/G,\qquad B_i=b_i/G,
\]
then replaces \(P_0\) by \(P=cP_0\), where \(c\) is a positive integer clearing its coefficient denominators, before setting \(r_i=B_iA^{-1}\bmod P\). Appendix F:68–74 returns the already integral polynomial. Thus the premise of lem:int:values at F:261–283 now supplies \(P\in\mathbb Z[T]\) at the time it asserts the resultant is integral.

For the R1 counterexample \(f(y)=y^3-3y\) on \([-3/2,3/2]\), the normalized full-face equation is
\[
y^3+(3z/4)y^2-3z/4=0.
\]
Its leading characteristic coefficient is \(p=(3/4)(T^2-1)\), and the monic gcd is \(G=1\). Taking the positive common denominator \(c=4\) gives \(P=3(T^2-1)\). The recovered coordinate and value maps remain \(r_y=T\) and \(r_f=-2T\), but now
\[
\operatorname{Res}_T(3(T^2-1),W+2T)=3(W^2-4)\in\mathbb Z[W].
\]
The root \(\theta=1\) still denotes the unique box minimizer and its value \(-2\). The other finite limit, \(\theta=-1\), still denotes the feasible point of value \(2\). The previous rational resultant \((3/4)(W^2-4)\) is therefore replaced by an integer polynomial with exactly the same distinct value roots and order.

**Recovery, values and comparisons.** Over the field \(\mathbb Q\), the principal ideals \((P_0)\) and \((cP_0)\) coincide. This is the quotient ideal used by the algorithm; no equality of ideals over \(\mathbb Z[T]\) is required. A nonzero scalar does not change the roots, multiplicities or degree. The gcd screening condition remains valid, and \(A\) is invertible modulo the new \(P\) precisely when it was invertible modulo \(P_0\).

The unique rational remainder of degree below \(\deg P\) is unchanged under multiplication of the divisor by a nonzero scalar. Hence the coordinate maps \(r_i\) and the value map \(r_f=f(r)\bmod P\) are unchanged. The recovery identities at good projected limits, candidate membership tests, and selection of the same feasible least-value candidate all remain valid. The repair does not scale \(A\) or \(B_i\); it need not do so because it changes only the modulus by a unit of \(\mathbb Q[T]\).

With \(h\in\mathbb Z[T]\) and nonzero integer \(q_0\), both input polynomials of \(\operatorname{Res}_T(P,q_0W-h)\) now have integer coefficients, so its Sylvester determinant belongs to \(\mathbb Z[W]\). It is nonzero for the same product-form reason proved in F:274–283. If \(e=\deg_T(q_0W-h)\), normalization changes the old resultant by the nonzero factor \(c^e\). Thus its real roots, squarefree root set and isolatable selected value are unchanged. Constant value maps, repeated value roots and ties pose no extra case.

Exact comparison still isolates the squarefree part of the product of two value polynomials and identifies the represented values among its roots. Normalization introduces no sign, equality or root-pairing change. The optimizer coordinates and value still share the same selected root; the value polynomial is auxiliary comparison data rather than a separate choice of optimizer.

**Degree, height, work and inherited theorems.** Write \(\delta=\deg P_0\) and let \(\tau\) bound its rational coefficient lengths before normalization. There are at most \(\delta+1\) coefficients. Choosing the product of their positive denominators gives
\[
\log_2 c\le(\delta+1)\tau+O(\delta+1).
\]
Multiplying the coefficients by \(c\) has polynomial bit work and resulting height polynomial in \(\delta\) and \(\tau\), with absolute exponents. It does not raise the degree. An implementation can use this product directly; the proof needs neither a large search for a denominator nor a minimal polynomial.

The previously proved bounds already control \(\delta\le(D-1)^k\) independently of input coefficient and refinement bits, and \(\tau\) by a fixed polynomial in the quotient dimension and coefficient length. Consequently normalization retains \(c_d^k\operatorname{poly}_d(H+q)\) construction/refinement bounds and the separate degree bound. Its fixed polynomial operations fit the explicit ledger in F:332–370: the prior ledger has ample slack for multiplying at most polynomially many bounded-length integers. It introduces no \(H^k\), noise-dependent degree, product of component fields, or new precision-dependent base factor.

The resultant height remains polynomial in the degree and normalized coefficient lengths. Root separation and derivative allowances therefore remain inside the same fixed-polynomial budget. The positive denominator is computed before the value routines, and is covered by the fixed solver implementation used to choose fallback budgets and strong-field weights before sampling. There is no circular dependence on a newly chosen law.

All former V1 qualifications now close as follows:

| Result or inherited use | Focused R2 status |
| --- | --- |
| lem:int:values | Verified literally, including the integer-resultant assertion. |
| thm:int:solver | V1 resolved; common-root output and fixed-base degree/work bounds preserved. |
| cor:int:mixed-solver | Value order/equality, winner selection and re-isolation preserved. |
| thm:int:native | Whole-slice completion and label-enumeration fallback inherit the corrected routine. |
| cor:int:native-implicit | Ordinary patch unchanged; algebraic fallback inherits the corrected routine. |
| thm:int:flow-interior and thm:int:flow-boundary | Exact chart tests, derivative/minimum comparisons and whole-slice completion inherit the corrected routine. |
| cor:int:bilinear, thm:int:tu and cor:int:tu-ineq | Algebraic completion inherits the correction; sampler and certificate proofs are unchanged. |
| thm:int:strong-field | Each nonquadratic component's auxiliary value polynomial is integral; weighted work and joint refinement are unchanged. |
| lem:int:cost and lem:int:budget | Normalization is within the existing proved work/height bounds. |

The quadratic rational branches require no new normalization argument. The lattice theorem never calls this algebraic component routine and is unchanged. The continuous recourse theorems use the distinct generic shared-root fallback, whose statement and proof are unchanged and already integral. No new comparison of sums of unrelated component values is claimed.

**Other assigned changed passages.** Section 8:614–623 now expressly calls a coordinate bad when its sampled coefficient lies inside the closed interval defining \(q_i\), so the strict derivative-sign test leaves it unpinned. That event depends only on the coordinate's own independent ambient coefficient and on the pre-draw derivative enclosure. Its probability is exactly the stated \(q_i\). Endpoints are included because a strict sign certificate may fail there. This correctly separates the unpinned event from its pinning complement and agrees with the unchanged weighted component proof. It does not recompute enclosures after pinning or assume conditional independence of selected components.

Section 10:83–95 correctly distinguishes compact ordinary descriptors, base-exponential bounds on fallback outputs on every draw, expected proof/output sizes under their work bounds, and the per-draw parameter bounds for small-core algebraic output. It retains one common root per component and a symbolic total value sum. No efficient exact comparison for unrelated algebraic sums is inferred.

I also read the changed envelope premises and their fresh shared-interface R2 review. Section 2:193–199 explicitly charges evaluation of the integer envelope before sampling; Section 3:689–702 requires a positive integer-valued monotone envelope evaluable in a fixed polynomial in its magnitude and encoded supplied bound; Appendix A:704–715 charges that cost. Since the supplied \(K\) is counted in \(I\), the evaluation work is bounded by \((1+F(K))^{c_F}\operatorname{poly}(I)\). Substitution of the new sampled height retains a fixed polynomial exponent and the supplied-\(K\) factor. Appendix A:805–821 chooses an envelope with this property for the explicit flow/TU powers.

These new premises are consistent with the recourse sampler contracts and do not change the old actual-core versus supplied-bound qualification. The accompanying model passages retain sampled-bit and refinement costs rather than canceling them with the fallback multiplier. The focused envelope proof has independent approval in shared-root-universal-independent-sol-r2.md. I found no conflict in its application here.

**Actual checks and remaining scope.** I used scoped cat, rg, sed, and nl with sed to read the specified evidence and frozen changed passages. A Python script verified SHA256 and line counts for all 20 manifest files and generated unified differences for the assigned scientific interfaces. A second scoped comparison checked all seven unchanged whole-file or proof-block comparisons stated above; all passed. The cubic resultant, quotient-ideal argument, modular recovery and degree/height/work effects were checked analytically. The report-only final check verifies whitespace, control characters, paired math delimiters, cited manifest hashes and the listed inherited result labels.

No experiment, literature research, delegation, scientific source edit, build, project-wide check, CI inspection or commit was performed. This review authors only final-recourse-integer-sol-r2.md.

There is no remaining mathematical blocker in this focused repair scope. Classical-source identities remain with the assigned literature lead. The later live wording/comparison additions need the final publication snapshot check and are not approved here.

