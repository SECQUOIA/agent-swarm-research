# Component-solver numerical budget: independent Sol review R3

**Adjudication.** Luna's concern does not show that the numerical solver base or strong-field theorem is false. An unspecified fixed absolute multiplicative constant \(A\) in the elementary routines is absorbed into the global prefactor \(C_d\). It is not raised once per coordinate and need not be folded into \(c_d\). The claimed base \(c_d=2^{10000D}\) can be retained.

The frozen proof nevertheless needs a narrow completion: its invocation of an exponent-100 routine bound should have an explicit elementary operation ledger, and its word “input length” must include requested refinement precision numerically. A binary encoding of a requested \(q\) cannot support a runtime polynomial in \(\log q\) for writing \(q\)-bit irrational-root enclosures. The theorem already charges \(\operatorname{poly}_d(H+q)\), so this is a repair to the proof convention, not the theorem.

Below I give a degree/height/precision ledger, independent of the asymptotic computational exponents in BPR or Mehlhorn–Sagraloff–Wang, that supplies the required bound. It is deliberately loose. A universal bound \(A(\ell+2)^{40}\) suffices for the elementary calls; the frozen exponent 100 then follows. The existing outer \(U^{5010}\) bound and numerical base survive. No optimizer, common-root, or lattice argument is contradicted.

My R1/R2 acceptance of the compact explicit-budget paragraph should therefore be qualified by this proof completion. I do not recommend deleting the numerical base merely because the prefactor \(A\) is unprinted. If the root prefers not to integrate this elementary ledger, the safe alternative is a fixed effective solver base without the displayed 10000 formula, as specified below.

**Immutable target.** Scientific source reads were restricted to evidence/snapshots/isolated-root-proof-r1, captured at 2026-10-06T04:23:50.845160+00:00. Its manifest has 20 TeX files and one bibliography file; all 21 entries and line counts match. Manifest SHA256: 82bcd7e3082f297b53a10fcee701d9f94cfa082d1251618e244f5c1db0b50136.

| Principal file | SHA256 |
| --- | --- |
| appendices/F-integer.tex | 7720acea2407b43cc60844522197094936d3572373ed0759ac2f7611112d69e2 |
| sections/08-integer.tex | b88b511b7201f75c12a4f51d9e39725d5dee823c80ee8981e8cdf1e5b8d6461c |
| sections/03-counting.tex | 28141913b9357189bace34ee2f3e5ee19fd9d04fdfdfcbdaab9edeb375f4c7c8 |

I read BRIEF.md, independent-review-brief.md, the prior complete/R1/R2 recourse reviews and recourse-sol-final author response. I inspected the actual solver, mixed comparison, strong-field weight and finite-tail constant passages. A direct comparison with integration-repairs-r1 confirms that the solver and budget proof are unchanged. Appendix F's only later change is the explicit inside-interval bad-event definition; Section 8's only change is the closing common-root scope. Neither affects the budget. The new isolated-root proof elsewhere in this snapshot is outside this focused assignment.

**Why the unprinted \(A\) is not the issue.** The budget lemma lem:int:budget at F:332–340 states
\[
C_d\,2^{10000Dk}(H+q+1)^{10000}.
\]
Its prefactor expressly depends on fixed \(d\). If a primitive has work at most \(A(\ell+2)^{100}\), and \(\ell\le C_dU^{50}\), then all fixed factors, including \(A\) and powers of the height-ledger constants, become a new prefactor depending only on \(d\). They do not change the exponent of \(U\), hence do not change the displayed dimension base.

For a component \(C\), a bound of the form
\[
K_d\,c_d^{|C\cap C_{\rm cont}|}
       \prod_{i\in C\cap C_{\rm int}}N_i\,P_d(I+b+q)
\]
is summed over components. The fixed factor \(K_d\) and polynomial factor are outside that sum. The geometric connected-set argument weights a continuous site by \(c_d\) and an integer site by \(N_i\); it does not weight each site by \(K_dc_d\). Thus an unknown fixed global prefactor does not alter the subcriticality condition or the sufficient scale using \(a_i=c_d\).

This distinction also applies to label enumeration: the number of labels is a multiplicative factor on solver calls, while a fixed implementation prefactor remains outside. The mixed comparison routine uses two value polynomials of degree \(O((D-1)^k)\), not a field of product degree. Its primitive-call ledger fits the same numerical base. The sentence at F:381–382 about enlarging \(c_d\) can be clarified to say that the explicit budget already includes mixed comparisons and only its global prefactor is enlarged.

**A precise routine-budget convention.** Fix dense representations for the univariate polynomials used by this solver. Let \(L\) be the combined encoded length of a primitive's rational arithmetic data, including rational interval endpoints and interpolation nodes, and let \(q_{\rm req}\) be its largest requested precision as a number. Use
\[
\ell=2+L+q_{\rm req}.
\]
Operations with no requested refinement take \(q_{\rm req}=0\). Equivalently one can pass a common budget bounding all degrees, coefficient/endpoint bit lengths, data counts, and numeric requested precision; dense data length is a polynomial in such a budget.

In the solver's outer ledger, \(\ell\le C_dU^{50}\) still holds: the requested precisions are already bounded by \(O_d(U^{25})\). This convention repairs the literal binary-input ambiguity without changing the theorem's \(\operatorname{poly}_d(H+q)\) contract.

A simple witness to the ambiguity is a request for a non-point rational isolator of \(\sqrt2\) of width \(2^{-q}\). Its endpoint denominators require \(\Omega(q)\) bits up to a constant factor. A request whose numeric value is \(q=2^m\) cannot be answered in \(\operatorname{poly}(m)\) work merely because \(q\) has \(O(m)\) encoded bits. The existing outer theorem makes no such claim.

**Elementary univariate accounting.** The following implements the required calls with an absolute exponent. Constants in this paragraph depend on fixed arithmetic programs, not on \(d\), dimension, coefficient height or requested precision. Let \(K\) denote such a fixed constant, enlarged a finite number of times.

Integer addition, multiplication, exact division and gcd can be implemented by schoolbook arithmetic and Euclidean remainders. On \(B\)-bit integers multiplication and long division cost \(O(B^2)\). Euclidean gcd makes at most \(O(B)\) divisions, so the deliberately loose bound \(O(B^3)\) suffices. Rational arithmetic reduces numerator and denominator by this gcd. All ensuing bounds may therefore use cubic integer cost.

After clearing input denominators, univariate degrees are at most \(\ell\), and coefficient heights are at most \(K\ell^2\). The denominator product itself has this bound even under the weaker convention that only each coefficient's height, rather than total data length, is bounded by \(\ell\). Hadamard's bound gives at most \(K\ell^3\) bits for a minor of a Sylvester-type matrix of order at most \(2\ell\).

Use primitive Euclidean remainders, retaining their signs by dividing only by positive contents. The algebraic subresultant identities say that each nonzero primitive remainder is proportional to the corresponding subresultant; its coefficients are, up to a common factor, minors of these Sylvester matrices. Defective degrees skip zero subresultants. This is an algebraic identity used for height control, rather than an appeal to an unspecified algorithmic exponent. In particular all primitive remainder, gcd, and signed Sturm polynomials have coefficient heights at most \(K\ell^4\).

These sequences can be generated by ordinary rational long division followed at each step by positive primitive normalization. There are at most \(\ell+1\) remainders and at most \(K\ell^3\) coefficient operations in total. Within one division, common denominators and powers of the divisor's leading coefficient bound intermediate rational lengths by \(K\ell^6\). Each operation then costs at most \(K\ell^{18}\), so \(K\ell^{21}\) bit work bounds the full sequence. Clearing contents does not increase this bound. Exact quotients and squarefree parts use the same divisions; a common power of the leading coefficient, rather than unrelated coefficient denominators, supplies their denominator bound.

Bézout coefficients and modular inverses can use the subresultant identities or a consistent Sylvester linear system after the gcd is found. Degree bounds permit at most \(2\ell+O(1)\) unknowns. Solve it with exact pivoting and fraction-free determinants. Cleared entry heights, minor bounds and rational reconstruction give intermediate lengths at most \(K\ell^8\); there are polynomially many determinants of order at most \(2\ell+O(1)\). The resulting bound is below \(K\ell^{25}\) bit operations. This does not require iterating uncontrolled unnormalized extended remainders.

Bareiss elimination for an order-\(n\) integer matrix uses \(O(n^3)\) exact operations; its intermediate entries are minors. For \(n\le\ell\) and input heights at most \(K\ell^2\), these entries have at most \(K\ell^3\) bits. Rational determinants first clear denominators. Resultants are such determinants. A resultant polynomial with the one additional value variable can be obtained at consecutively spaced integer nodes and interpolated. Ordinary Lagrange interpolation has \(O(\nu^2)\) coefficient operations for \(\nu\) nodes; products of at most \(\nu\le\ell\) node differences and coefficient denominators retain polynomial height. These determinant and interpolation routines fit well below \(K\ell^{25}\). Tensor interpolation here has at most three variables, and is a fixed number of successive univariate interpolation operations; dimension does not enter its exponent.

For root isolation, first take a primitive squarefree integer polynomial \(p\), of degree \(n\le\ell\) and coefficient height \(\tau'\le K\ell^4\). A Cauchy root bound places every root in the complex disk of radius \(R=2^{\tau'+2}\). The discriminant of \(p\) is a nonzero integer. If \(\zeta,\eta\) are a pair of closest distinct roots, its product formula and the upper bound \(2R\) on the other distances give
\[
1\le |a_n|^{2n-2}|\zeta-\eta|^2
       (2R)^{n(n-1)-2}.
\]
For \(n\ge2\) this proves a strict separation bound \(2^{-S}\) after choosing
\(S=K(n+1)^2(\tau'+1)\le K\ell^6\) with a sufficiently large fixed integer \(K\).
The case \(n=1\) is evaluated directly. No numerical constant from a quoted fast isolation theorem is needed.

Bisect the initial rational interval \([-R,R]\), and subdivide only intervals with at least one real root, according to exact Sturm counts. At any depth at most \(n\) open intervals contain roots; dyadic roots discovered at endpoints or midpoints are recorded once as point intervals. One-sided Sturm variations, computed from the first nonzero derivative at a zero endpoint, handle these cases without a search over all dyadic nodes. At depth \(K(\tau'+S+q_{\rm req}+1)\), distinct roots are separated and every remaining isolator has the requested width. Thus at most \(K\ell^7\) rational variation evaluations suffice, with endpoint bit lengths at most \(K\ell^6\). This bound applies to continued refinement of given isolators as well.

At such a point, homogenized Horner evaluation of a chain polynomial and the endpoint derivative tests use at most \(K\ell^3\) integer operations. Their operands have at most \(K\ell^7\) bits: the coefficient height plus degree times endpoint height bounds numerator growth. Schoolbook multiplication gives at most \(K\ell^{17}\) work per variation evaluation, and hence at most \(K\ell^{24}\) total isolation/refinement work. Allowing rational normalization or a less economical endpoint implementation still leaves a bound below \(K\ell^{30}\).

To determine the sign of a polynomial \(h\) at the stored root of \(p\), gcd membership first decides equality. For a nonzero value, isolate/refine the squarefree part of \(ph\), so that the stored \(p\)-root is separated from all other roots. The sign of \(h\) is then its rational sign inside that interval. The product has degree at most twice the original degree and coefficient height bounded by the sum of the two heights plus a logarithmic summation allowance. The same determinant, separation and bisection ledger applies. Locating two represented values in the squarefree product of their value polynomials also uses this operation, including when the two values agree.

These estimates give the following uniform envelope:

| Elementary stage | Sufficient bit-work envelope |
| --- | --- |
| Integer/rational arithmetic on the bounded intermediate operands | Cubic in operand bit length. |
| Bareiss determinants, exact interpolation and resultants | \(K(\ell+2)^{25}\). |
| Primitive gcd, exact quotient, squarefree and signed Sturm data | \(K(\ell+2)^{25}\). |
| Bézout coefficients and modular inverse | \(K(\ell+2)^{25}\). |
| All-real-root isolation, refinement, sign and two-value comparison | \(K(\ell+2)^{30}\). |
| One fixed collection of these primitive programs | \(A(\ell+2)^{40}\), hence \(A(\ell+2)^{100}\). |

The minor identities and Sturm correctness are classical algebraic facts; the displayed cost exponents follow from the operations above. The proof therefore does not claim that BPR or Mehlhorn–Sagraloff–Wang states the exponent 100, the numerical solver base, or these particular conservative constants.

The universal \(A\) is effective: it is obtained from a finite count of instructions, loop coefficients and elementary integer programs. Its exact numerical value need not be printed because it enters only the prefactor. A chosen implementation fixes an admissible integer upper bound before use; no search over unknown maximal runtime or sampled coefficients is involved.

**Outer dimension and height ledger.** I also checked that this routine completion fits the dimension budget, rather than merely proving some polynomial time. Set \(U=2^{Dk}(H+q+d+2)\). A fixed degree is essential here.

| Solver object | Sufficient bound in \(U\) |
| --- | --- |
| Quotient dimension \(N=(D-1)^r\), memoized monomial count | \(U\). |
| Reduction depth \(R=r(D-2)+1\) | \(O_d(U)\). |
| Normal-form coefficient heights | \(O_d(U^2)\). |
| Number of moment forms | \(O(U^3)\). |
| Moment-form coefficient heights | \(O_d(U^2)\). |
| Determinant interpolation nodes per form/coordinate | \(O_d(U^4)\). |
| Determinant sampled heights; interpolated heights | \(O_d(U^5)\); \(O_d(U^8)\). |
| Squarefree polynomial, modular coordinate data and their final coefficient heights | \(O_d(U^{12})\). |
| Value map, integer value resultant and their coefficient heights | \(O_d(U^{18})\). |
| Root separation, selection, derivative and final refinement precisions | \(O_d(U^{25})\). |
| Combined arithmetic data plus numeric precision of any primitive | \(O_d(U^{50})\). |
| Number of outer primitive calls, including faces and comparisons | \(O_d(U^{10})\). |

There are concrete reasons for these fixed powers. A normal form uses only the common base derivative denominator, raised to at most \(R\); retaining that common denominator bounds determinant and interpolation heights. There are \(O(rN^2)\) forms, \(r\) coordinate derivatives, and \((RN+1)(N+1)^2\) tensor nodes. Multiplying these by at most \(3^k\le2^{Dk}\) faces fits \(O_d(U^{10})\). No Cartesian pairing of scalar field roots occurs in this solver.

Gcd/quotient coefficients have Sylvester-minor heights. Clearing the squarefree polynomial's common denominator multiplies height by at most its degree, still inside \(U^{12}\). The coordinate map can also be viewed as the unique solution of \(Ar_i=B_i\bmod P\), whose linear-system minors supply the same height bound. The value map composes at most \(H\) explicitly listed monomials, each of fixed degree at most \(d\), and reduces them modulo \(P\). A shared denominator for all maps has polynomial height in the coordinate count and \(N\); value substitution and a Sylvester determinant retain the \(U^{18}\) envelope. They do not introduce an exponent of \(H\) depending on \(k\).

The value polynomial has degree at most \(N\); comparison uses a product of two such polynomials and degree at most \(2N\). The crude discriminant separation bound therefore requires at most \(O_d(U^{20})\) bits at the value stage. Derivative bounds for coordinate/value evaluation and the numeric requested \(q\) fit the larger stated \(U^{25}\) precision envelope. Dense coefficient arrays, endpoint lengths and requested precision then fit \(U^{50}\) with large slack.

The helper bound now gives
\[
\text{work}\le C'_dU^{10}\bigl(C_dU^{50}+2\bigr)^{100}
 \le C''_dU^{5010}
 \le C'''_d\,2^{10000Dk}(H+q+1)^{10000}.
\]
The last inequality absorbs \((d+2)^{5010}\) and all fixed program factors into \(C'''_d\). It does not absorb a dimension-dependent factor there. This proves the existing numerical base. The same ledger includes the two-value comparisons in mixed enumeration; substituting integer labels changes only the polynomial data factor.

**Minimal manuscript repair.** Keep the budget lemma and numeric strong-field weight. Immediately before or within its proof:

1. Define the primitive budget as encoded arithmetic data length plus numeric requested precision, and note the \(C_dU^{50}\) bound.
2. Replace the F:357–368 explanation with the elementary counting argument above, or a condensed version giving the minor-height bound, cubic arithmetic cost, discriminant separation, occupied-interval bisection, and the displayed primitive envelopes.
3. Do not claim \(O(\ell^2)\) evaluation points as the justification for the entire routine. The \(O(\ell^7)\)-point conservative bound suffices and is proved here.
4. State that the fixed absolute factor \(A\) is included in the global prefactor \(C_d\); the dimension base comes from the exponent of \(U\). Clarify that the already budgeted mixed comparison needs no later change to that base.

No source should be cited as stating the manuscript's numeric base. Sources support the classical algebraic mechanisms; the local operation ledger supplies this particular bound. A fresh frozen check of the actual integration remains necessary.

If the root elects to omit this accounting, the simplest safe replacement is to fix an effective computable degree-dependent solver base \(c_d\ge1\), with a fixed polynomial exponent and an effective prefactor, obtained from a fully specified implementation and its elementary bounds. Every continuous component uses that same base as \(a_i\); all strong-field sufficient inequalities and fallback budgets use it before sampling. Remove the explicit 10000 formula from the budget lemma, Section 8's solver explanation and the discussion, without changing the theorem forms. Do not leave the old explicit scale while replacing only its proof by an unspecified asymptotic exponent. This fallback is valid but unnecessary if the narrow repair above is adopted.

**Renegar's fixed \(a_{\rm R}\).** The issue at Section 3:457–466 is different. The manuscript expressly says it does not extract a numerical value and fixes one admissible constant for the two-block constructive elimination algorithm. That absolute exponent is used consistently in the base-only format/tail bound and sampler choice. It is not advertised as a particular small numeral.

Given the cited constructive fixed-block degree/format bound, an admissible integer exponent can be fixed in the implementation once, independently of the input. Integer power construction then has the polynomial-logarithmic sampler budget stated in the manuscript. A source theorem with effective algorithms and fixed absolute constants is enough for this existential algorithm claim; publication need not print a numerical value for every fixed coefficient of its bit polynomial.

This still requires the source's actual block-sensitive theorem, format and coefficient-height bounds, not a vague statement that quantifier elimination is computable. Those contracts remain a literature-review responsibility. It would be misleading to claim a specific numerical sampler coefficient without a derivation. The current text does not do that. Its admissible constant is an algorithm constant, rather than an input oracle or a quantity learned from the sampled draw. I find no additional mathematical gap in this paragraph on the specified source-contract issue.

**Checks and decision boundary.** I used scoped cat, rg, sed and nl with sed, and a scoped Python manifest/diff comparison. The 21-entry immutable manifest and principal hashes matched. The relevant budget and solver blocks match R2; the normalization remains before all value routines. No computational experiment or optimization diagnostic was run. The cost, height, discriminant and strong-field arguments in this report were developed analytically. A report-only final check covers final newline, whitespace/control characters, paired math delimiters, cited hashes and required finding/result names.

I authored only this report. No literature search, KB change, delegation, source edit, build, project-wide check, CI inspection or commit was performed.

There is no core contradiction and no need to abandon the strong-field result. The focused publication blocker is the missing explicit routine-accounting convention/proof in the frozen target, which the report supplies for integration. The numeric base is mathematically salvageable with the stated narrow repair. Classical source identities and the fresh post-repair frozen check remain outside this report's approval.
