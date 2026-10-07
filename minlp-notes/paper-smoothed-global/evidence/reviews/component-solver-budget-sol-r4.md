**Component-solver budget: focused actual-integration review R4**

Reviewer: Sol. Date: 2026-10-06. Target: the immutable snapshot `evidence/snapshots/final-literature-integrated-r2/`. This report reviews the actual integrated elementary proof of the numerical solver budget and its inherited uses. It does not replace the previous complete recourse/integer review or approve unrelated changes in this snapshot.

**Decision: PASS for the assigned mathematical scope.** The actual proof of `lem:int:budget` supplies the routine accounting missing in R3. The numerical choice \(c_d=2^{10000D}\) remains valid, including mixed comparisons and its use as the continuous-site weight in the strong-field theorem. The unprinted absolute implementation factor belongs in the global prefactor, not in that site weight. I found no new mathematical blocker in the integrated proof. Classical source identification and other manuscript scopes retain their separate review requirements.

**Frozen evidence and comparison.** The SHA256 of `manifest.json` is

`628f762d433e2b4cd82b309b88a1699a0d71bcb22dcc377d8f2963430b342515`.

All 21 TeX/Bib entries match their recorded hashes. Principal files actually read or compared have the following hashes.

| File | SHA256 |
| --- | --- |
| appendices/F-integer.tex | da70a07e15c758f4c3e40854cbddf970065424ac2c8de410366097bff026078d |
| sections/08-integer.tex | b88b511b7201f75c12a4f51d9e39725d5dee823c80ee8981e8cdf1e5b8d6461c |
| sections/02-model.tex | b2ee85b74131bf95659b085dbfe7976e63746acfccfe1500eb060e088891c8ca |
| sections/03-counting.tex | 28141913b9357189bace34ee2f3e5ee19fd9d04fdfdfcbdaab9edeb375f4c7c8 |
| sections/07-recourse.tex | 6dbb5f51199e261d613afbe67a88b4bd9f8f43dfc3c2fd6bb34a22243f659c6b |
| appendices/E-recourse.tex | e3bba43cbcfa9cfd373661b350711c3f890ebb73a9994dc6dfc13fae49676e1f |
| sections/10-discussion.tex | 6785b08b9a945ce467e425af244e1f9b5202d5d4dcc3bacf9a8ba44f01b652a6 |

A direct comparison against `isolated-root-proof-r1` shows that Appendix F changes only its opening source qualifier, the elementary routine proof, and the mixed-comparison prefactor sentence. Sections 02, 03, 07, 08 and 10 and Appendix E are byte-identical. The rest of Appendix F, from its native-integer subsection through the end, is byte-identical; that suffix has SHA256 `494215274fb7dff24369c7972cbfe61c941f5c9af5610aff3aa91bbf1c1aaf8d`. Changes in the introduction, quadratic section, Appendices A/C and references are outside this focused scope.

The unchanged normalization/return/quotient block, extracted from step (3) through just before the Puiseux-field definition, has SHA256 `b1d03b176fd7f6cc0bdea4edf79a6c22c9a9da97dad473cb9236aa1d18ea8fcf`. The unchanged budget statement has SHA256 `ae37702dd8a8c17e873b57fc8b922884e445a454757f47e2f98530a95214db1e`. The unchanged outer ledger has SHA256 `0a3199a857e09f234cc66477688437c72841b7a456c72f02b109ce982f78e58d`. These are block hashes, not full-file hashes.

I reread the original BRIEF and independent-review brief and used my previous full, normalization and budget reports for the established scope boundary. The verdict below follows from the frozen proof and independent operation/height checks, not an author response or a build result.

**The primitive budget is now correctly specified.** At F:362–369 the proof defines \(L\) as combined dense arithmetic-data length, including endpoints and interpolation nodes, and \(\ell=2+L+q_{\rm req}\), with requested precision entering as a number. This repairs the binary-encoding ambiguity. The theorem continues to charge work polynomially in \(H+q\); it does not claim work polynomial in \(\log q\). Input polynomial counts, degrees, coefficient lengths, node counts and endpoint lengths are bounded by this dense budget. Replacing \(\ell\) by a fixed multiple of \(\ell\) for a two-polynomial product changes only an absolute factor.

**The new elementary accounting is sufficient.** I checked each stage in F:371–429, including the looser exponent 30 for determinant, inverse and interpolation stages.

Integer multiplication and division have quadratic schoolbook cost, and Euclidean integer gcd has at most a linear number of divisions in operand bit length. Thus cubic cost is a valid envelope for reduced rational arithmetic. Clearing denominators gives coefficient heights at most \(K\ell^2\). Sylvester minors of order \(O(\ell)\) then have \(K\ell^3\)-bit height. Primitive Euclidean remainders are proportional to the nonzero subresultants, including when degrees drop by more than one. Dividing by positive contents preserves the signed remainder sequence needed for Sturm counts. The loose \(K\ell^4\) primitive height and \(K\ell^6\) rational-division intermediate length are sufficient; at most \(K\ell^3\) coefficient operations give \(K\ell^{21}\) bit work. The same denominator/leading-coefficient control applies to exact quotients and squarefree extraction.

For Bézout coefficients or an inverse, the consistent Sylvester linear system has \(O(\ell)\) unknowns. Exact pivot selection and minor formulas permit the stated polynomial number of fraction-free determinants. With the generous \(K\ell^8\) intermediate-length allowance, \(K\ell^2\) determinants times \(O(\ell^3)\) arithmetic operations times cubic operand cost is at most \(K\ell^{29}\). Hence the displayed exponent 30 is valid. Bareiss determinants and resultants use the same minor-height control. Consecutive-node interpolation adds products of polynomially many node differences. Tensor interpolation here has at most three successive variable stages; the number of lines or grid entries in those stages is charged by dense data length and the outer grid count. “A fixed number” at F:395 refers to these variable stages, not to a constant number of grid evaluations. Their polynomial multiplicity fits the stated loose exponent.

The isolation proof at F:397–420 is elementary and does not need a numerical constant from a fast root-isolation theorem. A primitive squarefree integer polynomial of degree \(n\) and height \(\tau'\) has a nonzero integer discriminant. Its product formula, with all other root distances at most \(2R\), gives the displayed closest-pair inequality and the coarse separation exponent
\[
S=K(n+1)^2(\tau'+1)\le K\ell^6.
\]
The degree-zero and degree-one cases are separate. Only root-occupied intervals are subdivided, so at most \(n\) open intervals at each depth remain. The depth bound includes initial radius, separation and numeric requested precision. Recording roots at dyadic endpoints once and using one-sided Sturm variations handles exact rational roots without loss or double counting. This gives \(K\ell^7\) variation evaluations, rather than visiting all dyadic nodes.

Endpoint heights are at most \(K\ell^6\), and homogenized Horner evaluation and derivative jets have operands at most \(K\ell^7\) bits and at most \(K\ell^3\) integer operations per variation test. Even cubic arithmetic gives exponent \(7+3+21=31\), below the final exponent 40; the written evaluation uses integer arithmetic and quadratic multiplication, giving exponent 24 before the extra normalization allowance. Endpoint normalization is performed once per rational endpoint, not after every Horner multiplication. Even a generic integer gcd at each of the \(K\ell^7\) endpoints has total cost at most \(K\ell^{25}\). The claimed exponent 30 is therefore sufficient. If the Sturm chain is rebuilt after squarefree extraction, Sylvester minors have height at most \(K\ell^5\); rational division has \(K\ell^7\)-bit intermediates and costs at most \(K\ell^{24}\). These allowances remain within the same envelope and the \(K\ell^7\)-bit evaluation bound. There is no repeated application of an unspecified polynomial-time theorem with an uncontrolled exponent.

For signs and equality, F:422–429 expressly uses the product of the two original input polynomials. Its degree is at most \(2\ell\), and its cleared height is at most \(K\ell^2\). Gcd membership detects zero values. Otherwise isolating the squarefree product separates the stored root from roots of the sign polynomial, so a rational point in its isolator has the desired sign. Comparing two represented values locates them in the same squarefree product and decides equality as equality of roots. This avoids both an unrelated-field construction and a compounded input-size substitution from already expanded intermediate representations.

The absolute factor \(A\) in \(A(\ell+2)^{40}\), and hence in the deliberately weaker exponent-100 bound, arises from a fixed finite collection of elementary programs. It is independent of \(d,k,H,q\). No explicit value of \(A\) is needed to prove the stated dimension base: the theorem has a global prefactor \(C_d\).

**The outer ledger and numerical base fit.** F:347–360 is unchanged, but I rechecked it against the actual solver. Write \(U=2^{Dk}(H+q+d+2)\). Quotient dimension and memoized monomial count are at most \(U\). Reduction uses a common derivative denominator raised to at most the reduction depth, not independent denominator multiplication along every path. This gives normal-form height \(O_d(U^2)\). There are \(O(rN^2)\) forms; the three-variable determinant grids have \(O_d(U^4)\) nodes. Common denominators, determinant minors and consecutive-node interpolation fit the sampled/interpolated height allowances \(U^5,U^8\).

Subresultant and linear-system minors give squarefree and coordinate-map heights within \(O_d(U^{12})\), including clearing the denominator of \(P\). A common denominator for all coordinate maps followed by fixed-degree substitution and reduction modulo \(P\) keeps the value map and its resultant within \(O_d(U^{18})\). The value polynomial has degree at most \(N\), and comparison has degree at most \(2N\). Discriminant separation and evaluation derivative bounds fit the larger \(O_d(U^{25})\) precision allowance. Dense data and numeric precision therefore fit \(C_dU^{50}\).

The largest outer product of counts is faces, forms, coordinate determinants and grid nodes, bounded by \(O_d(U^{1+3+1+4})\). Root membership, value construction, comparisons and normal-form arithmetic also fit the asserted \(C_dU^{10}\) primitive-call envelope. These counts do not put a dimension-dependent exponent on \(H\).

Consequently the actual final calculation at F:430–437 is valid:
\[
C'_dU^{10}(C_dU^{50}+2)^{100}
\le C''_dU^{5010}
\le C'''_d2^{10000Dk}(H+q+1)^{10000}.
\]
The last step absorbs only factors depending on fixed \(d\), including \((d+2)^{5010}\), into the prefactor. The use of 30 rather than 25 in the elementary stages stays below 40 and 100 and does not change this calculation. Dimension zero is covered directly; there is no need to absorb a global constant once per coordinate.

**Normalization, output and inherited uses remain sound.** The positive denominator clearing is still before all coordinate and value routines at F:63–66. Scaling \(P\) leaves its roots, squarefreeness and the ideal in \(\mathbb Q[T]\) unchanged. Modular coordinate recovery and \(r_f=f(r)\bmod P\) are unchanged. For the previously identified genuine cubic example, the normalized polynomial is \(P=3(T^2-1)\), the value map is \(-2T\), and the integer resultant is \(3(W^2-4)\). The R2 repair continues to establish the integer-resultant claim. This check is symbolic proof inspection, not an experiment.

The auxiliary value isolator remains separate from the common-root output and determines the value of that same coordinate tuple. Integer normalization changes no ordering or equality decisions. The normalization height is already within the outer ledger. The solver still refines its stored point, its value and its feasible objective-gap witness separately, without using a gap as a distance bound.

The changed mixed proof at F:444–453 now correctly says that comparisons are already budgeted and only the global prefactor is enlarged. Enumeration multiplies work by \(\prod_iN_i\); each comparison uses two degree-\(N\) value polynomials. Substitution increases data length by a polynomial depending only on fixed degree. It does not require a larger continuous-site base.

Section 8:579–611 and F:1052–1071 use the solver base as \(a_i=c_d\) for a continuous site and label count for an integer site. A component cost is
\[
K_d\Bigl(\prod_{i\in C}a_i\Bigr)P_d(I+\log M+q).
\]
The fixed \(K_d\) is outside the sum over components. Therefore it does not enter \(\beta=\max_i a_iq_i\), the connected-set geometric ratio, or the sufficient noise inequalities. The new primitive proof preserves these exact weights and scales. The component output and symbolic global value sum remain unchanged; no exact comparison of unrelated global algebraic sums is introduced. The extra \(q+\lceil\log_2(n+1)\rceil\) component precision has the existing polynomial charge. The unchanged recourse, fallback and finite-law uses retain their proved effective prefactors and base-selected budgets.

| Result/interface in this scope | Status |
| --- | --- |
| `lem:int:budget`, F:335–438 | Verified in the actual integrated proof; R3 blocker resolved. |
| `lem:int:cost` and the numerical budget in `thm:int:solver` | Verified for the changed dependency; statements and output proof unchanged. |
| `lem:int:values`, integer normalization and common-root value identity | Verified unchanged, including the cubic witness. |
| `cor:int:mixed-solver`, F:444–453 | Verified; only a global prefactor is enlarged. |
| `thm:int:strong-field`, Section 8:588–612 and F:1035–1089 | Verified for the changed budget dependency; weights and sufficient scales remain valid. |
| Other inherited recourse/integer proofs in Appendix E/F | Unchanged from previous reviewed blocks; no new budget defect. Their complete proof review is not repeated here. |
| New Appendix C proof and other changed sections | Outside this focused review. |

Appendix F:10–24 now separates the classical real interval/gcd/sign facts from the cited fast complex-disk result. The local numerical ledger does not claim that either source states exponent 100 or the numerical base \(2^{10000D}\). I did no literature research and make no new source-identity verdict.

**Checks actually performed.** I used targeted reads of the briefs, prior budget report, frozen Appendix F and relevant Section 8/10 passages; scoped `rg` searches; a Python SHA256 check of every entry in the named immutable manifest; and direct full-file/block comparisons against the preceding frozen snapshot. One initial optional suffix-marker comparison used a shortened heading that did not occur; I corrected it to the actual native-integer heading and verified the entire suffix. Report-only checks cover hashes, final newline, whitespace/control characters and paired math delimiters. No optimization experiment, delegation, literature/KB work, TeX edit, build, project-wide check, CI inspection or commit was performed. I authored only this report.

There is no remaining mathematical blocker within this focused budget-integration scope. This is a scoped mathematical pass, not a whole-manuscript publication approval.
