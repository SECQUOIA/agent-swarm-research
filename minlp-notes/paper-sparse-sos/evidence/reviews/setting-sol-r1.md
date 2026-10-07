# Independent setting and notation review, round 1

Date: 2026-10-05. Reviewed `sections/02-setting.tex` (477-line version), `macros.tex` (76-line version), and `evidence/ARCHITECTURE.md`. The review concerns mathematical definitions, finite conic duality, degree accounting, sparse coefficient identification, and compatibility with `evidence/AUDIT-RECOURSE.md`. Authored TeX was not edited. No experiments or literature searches were conducted.

The setting passes review on its central mathematics. The sparse zero-decomposition lemma is sufficient for the scalar quotient, the box moment feasible sets are compact, and the arcsine family establishes the finite SDP Slater condition. The resulting equality of moment and certificate values and boundary certificate attainment are valid for these box-only hierarchies. The private-degree-two hierarchy is also consistent with the recourse audit, including its slightly stronger row-dependent degree allowance. The repairs below concern precision and edge cases; none defeats the paper's central theorem chain.

## Required repairs

### R1. State the precise total-degree cone in the size/comparison paragraph

Severity: moderate. Location: `sections/02-setting.tex`, lines 457–476, especially lines 471–474.

The moment-matrix size comparison is correct, but the sentence saying that a total-degree hierarchy “allows products of private constraints” is too broad. Arbitrary products of distinct constraint generators are available in a full preordering. An ordinary quadratic module does not automatically contain them. Total-degree lifting and full-preordering positivity are separate choices.

The sentence about “higher shared degree for a given matrix size” also obscures the degree distinction. At equal order, both domains allow pure shared degree `2r`; the rectangular domain additionally retains shared degree `2r` in mixed monomials of private degree two, giving joint total degree up to `2r+2`. The total-degree domain instead permits high private degrees and mixed terms whose combined degree is at most `2r`. The smaller matrix in the rectangular formulation arises from fixing the private degree, not from a universally comparable shared-degree maximum at equal matrix size.

Suggested repair:

> The rectangular hierarchy keeps private degree at two while retaining shared degree up to `2r` in mixed moments. A total-degree hierarchy retains all joint moments of degree up to `2r`, including higher private degrees. If it uses a full preordering, it also permits products of distinct private constraint generators. The two truncated formulations are not compared by inclusion here; lower bounds for both are supplied by actual local measures.

If the authors want to retain an explicit noninclusion claim, specify the total-degree full preordering, the local generator list, and the equal order used in the comparison. The safe statement “we do not rely on an inclusion” is enough for every audited theorem. The distinction is mandated by `evidence/ARCHITECTURE.md`, lines 166–176, and by `AUDIT-RECOURSE.md`, Sections 1 and 4.

### R2. Complete the odd-degree interval-positivity proof

Severity: minor proof gap, straightforward repair. Location: `sections/02-setting.tex`, lines 305–318, especially lines 313–315.

The lemma assumes `deg p <= 2k`, but the odd-degree proof considers only `deg p=2k-1`. A smaller odd degree, such as degree one with `k=3`, is also permitted. The theorem remains correct; the argument needs an additional index or an explicitly padded odd-degree statement.

Use `deg p=2j-1 <= 2k-1`. The odd Markov–Lukács representation has `tau_+`, `tau_-` sums of squares of degree at most `2j-2`. The displayed endpoint identity then gives `sigma_0` of degree at most `2j <= 2k` and `sigma_1` of degree at most `2j-2 <= 2k-2`. For even degree `2j <= 2k`, the ordinary even representation can likewise be padded to the stated bound. Zero and constant polynomials are handled separately if needed.

Also specify the range of `k` or define the negative-degree SOS cone. At `k=0`, a nonnegative constant has representation `sigma_0=p`, `sigma_1=0`, but `sos_{-2}` is currently undefined. Defining every negative-degree SOS cone as `{0}` makes the statement uniform. This is useful because the Jackson kernel can have `m=1`, so its interval certificate can have degree zero.

The repaired degree bounds match the univariate certificates used in `AUDIT-RECOURSE.md`, Sections 2, 4, and 5, and in the supplied `active-region-fresh-review.md`, lines 28–42. No change to the later kernel or commutator constants is needed.

### R3. Make the order-zero and all-empty-continuous conventions explicit

Severity: moderate integration boundary. Locations: `sections/02-setting.tex`, line 18, lines 113–128, lines 145–147, and line 414; `evidence/ARCHITECTURE.md`, lines 80–85.

The setting assumes `w=max_b |B_b| >= 1` and defines box cones and hierarchies only for `r >= 1`. The accepted finite-state extension explicitly includes empty continuous bags and an all-discrete case exact at order zero. These are compatible with the central proofs, but they require stated conventions somewhere before being used. If all continuous bags are empty, the current width assumption is violated; if the order is zero, the current definitions do not apply.

The simplest repair is either:

1. Define `w=max(1,max_b |B_b|)` as in the source recourse notes, allow `r=0` where the objective belongs to the moment domain, and omit negative-degree localizers; or
2. Preserve the positive-width, positive-order box conventions here, and state explicitly in the finite-state section that it extends the definitions to empty continuous bags and order zero by empty products and constant-only cones. Use a guarded width such as `max(1,max_b |B_b|)` in every parameter formula for that case.

Either option is mathematically sound. The first is more uniform; the second may require fewer edits. Do not silently apply formulas that divide by `w` when the unguarded continuous width is zero. The recourse source uses `max(1,max_b k_b)` and naturally includes entirely private problems with no shared coordinates, so the same convention also restores full agreement with that source class.

This is an integration request, not a recommendation to expand the theorem scope beyond the already accepted architecture.

### R4. Qualify affine box normalization for degenerate intervals

Severity: minor factual precision. Location: `sections/02-setting.tex`, lines 29–31.

“Any product of compact intervals” includes singleton intervals. An invertible coordinatewise affine map cannot send a singleton onto `[-1,1]`. Say “any product of nondegenerate compact intervals,” or first eliminate fixed coordinates and then normalize the remaining intervals. Eliminating fixed coordinates may reduce bags and degrees, so the existing “preserves bags” sentence should apply only after the nondegeneracy qualification.

### R5. Specify that multi-indices include zero

Severity: minor notation ambiguity. Locations: `macros.tex`, line 29; `sections/02-setting.tex`, line 71.

The macro `N` denotes `mathbb N` without a convention, while `alpha in N^B` must include zero coordinate indices and the all-zero index. Define `N={0,1,2,...}` or use `N_0` for multi-indices. This keeps the constant-coefficient and empty-product conventions explicit.

## Correct central arguments

### Sparse identities and the coefficient quotient

Locations: `sections/02-setting.tex`, lines 37–54, 170–173, 183–193, and 285–292.

The zero-decomposition lemma is correct. At a leaf, a coordinate outside the parent separator occurs nowhere else by running intersection. A monomial containing such a coordinate cannot be canceled by another bag polynomial, so its coefficient is zero. The leaf polynomial is therefore a separator polynomial, and adding it to its parent preserves the degree while removing the leaf. This identifies the kernel of the local-polynomial summation map with signed edge-separator differences.

A minor proof-detail improvement is to call the reduced structure a tree of the remaining bags satisfying running intersection. It may no longer cover the original coordinate set if a leaf owned some coordinates; those now-unused coordinates can be dropped. The induction itself does not require positive width or coverage of unused coordinates.

The paragraph extending edge consistency to arbitrary intersecting bags is also correct. Every coordinate in their intersection is present on every bag of the path; thus every polynomial in the intersection variables of the agreed degree can be transferred along that path.

The weak-duality proof correctly assigns the constant `-lambda` to one bag and applies the zero-decomposition lemma. It does not assume that a sum of local expectations is automatically a global expectation. The use of separator consistency is the needed justification.

The reverse implication in the Slater proof is valid: for a global certificate `f-lambda=sum_b q_b`, put `p_1=f_1-q_1-lambda` and `p_b=f_b-q_b` for `b>1`. Their sum is zero, so the separator potentials supplied by the lemma give a finite conic dual point with objective `lambda`. The bag-normalization scalars need only sum to `lambda`; assigning it all to one bag is sufficient.

### Compactness of finite box moment families

Locations: `sections/02-setting.tex`, lines 245–263.

For a monomial square `x^{2alpha}` with `|alpha| <= r`, the singleton box localizer tested at `x^{alpha-e_i}` yields `L(x^{2alpha}) <= L(x^{2(alpha-e_i)})`. Iteration bounds it between zero and one. Every monomial of degree at most `2r` splits into two monomials of degree at most `r`; the moment-matrix Cauchy–Schwarz inequality then bounds its absolute moment by one. This uses ordinary-module constraints only, so it covers the preordering as well.

There are finitely many moment coordinates, closed PSD constraints, and closed linear equalities. Point evaluations give nonemptiness. The normalized feasible set is therefore compact and the moment optimum is attained. No representing-measure assumption or strict feasibility is used in this compactness proof.

### The finite box Slater argument and boundary attainment

Locations: `sections/02-setting.tex`, lines 265–301.

The arcsine family has exact product marginals on all separators. Every present localizing matrix is positive definite: for a nonzero polynomial in its monomial basis, its square times the relevant product of box generators is strictly positive on some open subset of the open bag box, where the arcsine measure has positive density. An absent negative-degree localizer should not be counted as a matrix. Empty bags have a one-element constant basis and cause no failure of positive definiteness when permitted by the conventions.

This gives a strictly feasible primal in the affine equality space. Redundant separator equalities, including agreement of constants already normalized in every bag, do not invalidate the Slater condition. The finite conic primal has finite optimal value by compactness. The standard finite SDP duality theorem therefore gives zero gap and an attained dual optimum.

The proof identifies that dual with the polynomial certificate cone, rather than silently appealing to an unspecified sparse dual. Consequently the claims

\[
 \lambda_r^{\rm mod}=\rho_r^{\rm mod},\qquad
 \lambda_r^{\rm pre}=\rho_r^{\rm pre},\qquad
 f-\rho_r^{\rm mod}\in\sum_b M_r(B_b),\qquad
 f-\rho_r^{\rm pre}\in\sum_b P_r(B_b)
\]

are all supported for the box-only finite hierarchies. This is stronger than the strict-slack certificate existence proved for recourse by the order-unit argument; the distinction is essential. Private fibers can be lower dimensional, so the arcsine strict-feasibility construction must not be carried over to recourse without an additional proof.

The explanatory paragraph at lines 298–301 correctly distinguishes boundary attainment for a finite SDP from existence of exact nonnegative polynomial separator functions in an infinite-dimensional local-measure problem. The quadratic sparse sharpness example has positive finite gaps, so its lack of an exact separator is compatible with attained finite SDP certificates at their lower values.

Source request sent to root: ask Luna to record the exact finite conic duality theorem in `bental2001-lectures-modern-convex` that gives equality and dual attainment from primal strict feasibility and finite value, including affine equalities and PSD constraints. The cited mathematical implication is correct. This review does not independently retrieve the cited book.

### Chebyshev definitions and moment bounds

Locations: `sections/02-setting.tex`, lines 58–108 and 207–243; `macros.tex`, lines 40–55.

The scalar coefficient budgets are consistent with the recourse matrix budget and with the decomposition-dependent constants. Counting only the nonconstant Chebyshev coefficients in `C_b` makes `C_f` vanish precisely when every local polynomial is constant, even if nonconstant terms cancel in the global sum. This dependence on the chosen decomposition is stated correctly. The inequalities `A <= d^2 C_f`, oscillation `<= 2 C_b`, coefficient norm submultiplicativity, and the weighted product inequality are correct. For the weighted product inequality, averaging the plus and minus frequencies cancels the mixed frequency products, leaving `sum_i(alpha_i^2+beta_i^2)`; no missing factor two is needed.

The moment Cauchy–Schwarz lemma is correct provided the functional is defined on the displayed products. For formal completeness it could say that the domain contains the span of `Gpq`, but all later finite-degree applications already check this domain requirement.

The Chebyshev telescoping proof uses singleton box generators with square degrees at most `|alpha|-1`. It is valid under the ordinary module. The restriction `|alpha| <= r` is retained explicitly, and the warning at lines 240–243 correctly directs higher frequencies to the later half-degree lemma. The commutator proof must continue to use that stronger lemma, not this simpler one.

### Junction-tree gluing

Locations: `sections/02-setting.tex`, lines 328–365.

The standard Borel-space assumption supports regular conditional kernels. In a parent-before-child ordering, running intersection gives `B_b intersect U_k = B_b intersect B_parent`, so adjoining each conditional kernel preserves old marginals and realizes the new bag law. Null separator events cause no difficulty because the kernel is only specified almost everywhere with respect to the common separator law; any measurable version gives the same required marginals. Empty separators yield independent products. The finite union of null infeasibility events proves concentration on all local constraints simultaneously.

This is exactly the scalar law gluing needed in the recourse proofs. It does not imply gluing of private matrix-valued pseudomoments; the recourse argument first turns each private block into a Borel decision function of its shared coordinates.

## Compatibility of the recourse definitions with the audited theorems

Locations: `sections/02-setting.tex`, lines 373–445; `evidence/ARCHITECTURE.md`, lines 194–200; `AUDIT-RECOURSE.md`, Sections 1–3, 5, and 7.

The recourse model uses real affine fiber data, private variables disjoint across bags, polynomial shared objective coefficients, and pointwise PSD private Hessian matrices on the entire shared box. These are the correct mathematical ingredients. The full augmented matrix `H_b` need not be PSD, and no matrix-SOS certificate of the PSD condition is imposed. That distinction is stated correctly.

The model definition does not globally assume complete recourse; it defines the property for later theorems to assume. That is acceptable, but the displayed minimum and the statement `rho_rec <= f*` require a nonempty original feasible set, or an explicit extended-value convention. The smallest clarification is to say that the optimization problem is considered when its feasible set is nonempty, and that the quantitative theorems below impose complete recourse. Fixed-domain theorems additionally need each fixed private polytope nonempty. There is no need to impose full-dimensionality or strict feasibility.

The shared/private degree domain is stated precisely: total shared degree at most `2r` and total private degree at most two. The degree of an objective coefficient can be up to `2r` merely to define the hierarchy. The quantitative kernel proofs later need the stronger `d <= r`; that must remain in their theorem statements. The setting's weaker domain-membership condition is appropriate and is not itself a rate hypothesis.

The row-dependent allowance in (R2) is correct. If a row of `E_b` vanishes, the row contributes no shared degree and the square allowance `r-|I|` is valid. A nonzero row contributes shared degree one, and the allowance `r-|I|-1` yields shared degree at most `2r-1`. Private degree stays at most one in either case. This hierarchy coincides with the fixed-domain source hierarchy when all rows are fixed and is at least as strong as the source affine hierarchy, which conservatively reserves one degree for every row.

All source upper bounds remain valid: a feasible manuscript moment family is feasible for the weaker source affine conditions, or the source proof applies directly with the stronger fixed-row allowance. Every source lower bound supplied by an actual local measure also remains valid because the stronger local tests are pointwise nonnegative on that measure's support. This is a valid comparison between degree variants of the same rectangular formulation, not a comparison with the separate total-degree hierarchy.

The private affine bounds are implied at the necessary degree by `(1 +/- y)=((1 +/- y)^2+(1-y^2))/2`, after multiplication by any allowed `w_I s^2`. The quadratic private bounds are still necessary. The source Motzkin unboundedness proposition is written for all orders `r >= 6`; the setting defines that degree-six coefficient objective at orders `r >= 3`. To avoid an unqualified mismatch, line 442 can say “at every sufficiently high order.” Alternatively the source separation construction extends to every `r >= 3`: normalization of the separating functional follows from the scalar box monomial bounds, without testing the degree-six polynomial itself in the order-`r` square basis. This extension is not needed for the paper's central safeguards.

The order-unit proof accepted as `prop:rec-dual` is unaffected by the stronger fixed-row tests: it only uses (R1), (R3), and exact separator consistency. For every rectangular local monomial, factor it as `ab` with both shared factors of degree at most `r`, obtain `1-a^2` and `1-b^2` from box telescoping and (R3), and certify `1 +/- ab=((1-a^2)+(1-b^2)+(a +/- b)^2)/2`. The constant is therefore an interior order unit. The sparse quotient argument extends the scalar zero-decomposition lemma by noting that a monomial containing a private variable has only one owning bag. This gives compact primal moments and certificates at every `lambda < rho_rec`, but does not prove boundary attainment. Section 2 currently avoids claiming recourse boundary attainment, as required.

## SDP size and macros

Locations: `sections/02-setting.tex`, lines 447–463; `macros.tex`, lines 43–74.

The PSD dimensions and moment counts are correct:

\[
 (p_b+1)\binom{r-|I|+v_b}{v_b},\qquad
 \binom{p_b+2}{2}\binom{2r+v_b}{v_b}.
\]

The affine scalar localizer with a nonzero shared row has the smaller dimension `binom(r-|I|-1+v_b,v_b)`; the stated upper bound is valid. Negative degree allowances should mean absent matrices in every size statement, including (R1) if `|I|>r`. The standard total-degree moment matrix has `binom(r+v_b+p_b,r)` rows. The given numerical comparison for `v_b=2`, `p_b=50`, `r=6` is arithmetically correct: `51 binom(8,2)=1428`, versus `binom(58,6)=40475358`.

The contrast is a matrix-dimension comparison at a common integer order, not an accuracy or runtime comparison. The text correctly warns that constants can grow with private dimension and fiber data. The recourse proofs also depend on shared objective degree, row conditioning through Hoffman constants, and projected multiplier regularity constants, so the warning should not be weakened during integration.

The shared macros have the intended mathematical meanings and do not introduce a private/shared degree ambiguity. The vector macro `zy`, hierarchy value macros, kernel/multiplier notation, and polynomial-space macro are compatible with the architecture. There is no need to add a recourse certificate macro merely for symmetry: `prop:rec-dual` can define its scalar value locally if desired. No mathematical defect in the macro file was found beyond the zero convention for `N` noted above.

## Verification and limits

Read-only commands actually run: `nl -ba paper-sparse-sos/evidence/ARCHITECTURE.md`, `nl -ba paper-sparse-sos/sections/02-setting.tex`, `nl -ba paper-sparse-sos/macros.tex`, and the focused reread `nl -ba paper-sparse-sos/sections/02-setting.tex | sed -n '1,225p'`. Review conclusions come from direct mathematical reconstruction and comparison with the existing recourse audit. The displayed size calculation was checked arithmetically; no experiment or SDP solve was run. No source checker, project-wide verification, CI inspection, literature search, or authored TeX edit was performed.

A targeted inline `python3 - <<'PY' ... PY` formatting check reads only this review, verifies the final newline and absence of trailing whitespace, and checks matching display-math delimiters. Its result is recorded in the parent handoff. This is an artifact formatting check, not a proof or CI check.

## Disposition after the setting repairs

Follow-up date: 2026-10-05. This is one focused inspection of the revised 497-line `sections/02-setting.tex`, appended to preserve the original review and its historical locators. All five requested repairs are resolved within the manuscript's stated scope.

| Finding | Disposition | Current locator |
| --- | --- | --- |
| R1: total-degree cone comparison | Resolved. The text distinguishes joint degree from rectangular degree, qualifies private generator products by full-preordering use, and avoids transferring bounds by inclusion. | Lines 490–497 |
| R2: odd-degree interval proof | Resolved. The proof uses `deg p=2j-1`, `1 <= j <= k`, and pads the resulting degrees. The lemma allows `k=0`, constants are covered, and negative-degree SOS cones are `{0}`. | Lines 125–129 and 319–337 |
| R3: order zero and empty continuous bags | Resolved for the chosen scope. The standing positive-width/positive-order assumptions are explicit, and Section 8 is authorized to override them for finite-state models with no continuous coordinates and order zero. | Lines 22–28 |
| R4: degenerate intervals | Resolved. Coordinate normalization is stated for nondegenerate compact intervals, with fixed coordinates eliminated first. Bag and degree preservation refer to the subsequent invertible change on the remaining coordinates. | Lines 38–42 |
| R5: zero multi-indices | Resolved. The text explicitly defines `N={0,1,2,...}` where the multi-index notation is introduced; no macro change is needed. | Lines 81–83 |

The additional nonemptiness clarification is also present: the recourse minimum is defined when the original feasible set is nonempty, and the quantitative theorems are identified as assuming nonempty fixed polytopes or complete recourse (lines 407–417). The omitted-private-bound warning now says “every sufficiently high order” (lines 459–462), matching the source proposition without an unqualified low-order claim.

Zero-dimensional recourse is consistent in the following precise senses. The private model explicitly permits `p_b=0` (lines 393–400). The space `R^0` has one empty vector; the private linear and quadratic terms and private bound tests are empty; the augmented vector consists of its constant coordinate alone. A fiber is that singleton if its scalar row inequalities hold, and is otherwise empty. Complete recourse makes it the singleton at every shared point. The hierarchy, objective, and matrix sizes therefore reduce to their scalar shared counterparts.

An individual empty shared bag `v_b=0` is also permitted as long as some other bag gives the standing `w >= 1`. Its shared polynomial ring is the constants, `E_b` has zero columns, every row has `epsilon_bj=0`, the shared kernel product is one, and its only shared weight is the empty weight. The displayed PSD count reduces to `p_b+1`, each scalar localizer has one row, and the moment count reduces to `binom(p_b+2,2)`. Its coefficient smoothing budget and affine repair contribution are zero. These are the natural empty-vector/product/binomial conventions already used by the source proof. No division by the local bag size is required.

An entirely private model with `n=0` and every shared bag empty has `w=0`, so it remains outside the standing recourse scope at lines 22–28. This exclusion is now explicit and coherent; it is narrower than the supplied recourse notes, which guard their width by `max(1,max_b k_b)`. If the paper later claims to include entirely private models, it must either add that guarded-width convention locally or state the direct exact constant-shared-cost case. Section 8's all-discrete override does not silently extend the recourse scope. This is a scope observation, not an unresolved error in any theorem currently defined under `w >= 1`.

No central duality or degree argument was altered by these repairs. The finite box Slater conclusion remains boundary certificate attainment; the recourse order-unit conclusion remains equality of values and strict-slack certificate attainment only. The independent bibliographic request for the exact cited finite conic duality theorem remains with root/Luna; this follow-up performs no literature verification.

Follow-up read-only commands used focused `nl -ba ... | sed -n ...` ranges of `02-setting.tex`, the number-system range of `macros.tex`, and a scoped `rg -n` for empty/zero-dimensional conventions. The latter reported that `sections/06-recourse.tex` and `sections/07-regularity.tex` were not present at inspection time, so no current manuscript recourse-section text was reviewed here. The disposition concerns the revised setting and the established source/audit contracts. No experiment, source checker, project-wide check, CI inspection, or authored TeX edit was performed.
