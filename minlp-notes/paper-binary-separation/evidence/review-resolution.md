# Review findings and their disposition

The manuscript was checked analytically by three source auditors, fresh
mathematical referees for the main proofs and the algorithms/gap-zero results,
focused independent class-transfer and gap-zero referees, and an editorial
referee. GPT Luna with max reasoning separately checked the literature and
bibliography. The reports in `../reviews/` are internal reviews, not journal
peer review.

No mistake invalidating the topic was found. The final manuscript incorporates
the following corrections and proof development.

| Finding | Final disposition |
|---|---|
| Source notes relied on precursor identities | Section 2 gives direct cut/correlation/moment/split identities and all normalization factors. |
| Infinite families need polynomial certificate length | Section 5 proves rational quotient, bounded image, and polynomial integer preimage lemmas; it also covers indefinite and singular inputs. |
| A fixed-radius enumeration bound did not establish the stated bit complexity | The rank theorem uses the verified exact CVP theorem, a complete rational Gram embedding, and polynomial normal-form preprocessing. No blanket enumeration bound remains. |
| Support polynomiality differs from rank FPT | Both notions and XP are defined; the support, gonality, and threshold exponents are stated accurately. |
| Strict threshold boundary needed explicit rounding | The admissible squared norm is ceiling of `1/(4ρ)` minus one; equality with the requested violation is not accepted. |
| Primitive domination has an omitted root-sign assumption | The identity holds for every symmetric matrix; its domination conclusion explicitly requires `Y00 ≥ 0`. |
| Binary and general-integer rank-one domains could be confused | The rank-one examples are a separate general-integer subsection. Rank-one Boolean moments are shown to be integral. |
| Duplicate Boros–Hammer data pairs contradicted literal uniqueness | Exact witness lists identify `(w,s)` with `(-w,-s-1)`. |
| Maximum violations were sometimes unconditional in the notes | Every positive maximum is conditional on a cover; no-instances have maximum zero. |
| Hypermetric switching invariance would be false | Switching is stated for the appropriate rounded and gap families; hypermetric coefficient-sum restrictions are explicitly distinguished. |
| Historical facet references had a disputed orientation | The required facets have a direct proof including ambient unused variables; the submission does not rely on the disputed condition. |
| Orthogonal lift needed complete all-positive classification | The proof includes the global-negative case and excludes it because cover coordinates remain negative. |
| Signed coefficients do not make an unbounded-offset family finite | The collective family is called the signed-coefficient family. Its best-offset NP verifier handles every integer parameter. |
| Fixed gonality padding needed the right quantifier | Every promise is for each prescribed fixed cutoff; no binary-encoded padding parameter is treated as constant. |
| Matrix and distance polytope domains were conflated in shorthand | Formal promises state `d ∈ MET(V)` and `Z(d) ∈ relint ELL(V)`. |
| “Rational cut vector” was inaccurate for arbitrary inputs | Gap-zero input is a rational distance vector; cut vectors remain binary vertices. |
| Restricted split hardness could read as difficult evaluation | The proposition explicitly searches for the existence of a violated restricted vector. |
| Rational Gram factors needed a dimensional qualification | Section 5 distinguishes the intrinsic rank dimension from a rectangular rational factor and constructs the latter. |
| Gap-zero nearness needed an encoding qualifier | Polynomial encoding length includes the prescribed rational tolerance; the hard matrix retains one negative eigenvalue. |
| PARTITION reduction was called weak NP-completeness without a matching upper bound | The manuscript states NP-completeness and that this proof does not establish strong hardness. |
| Broad approximation disclaimers omitted a simple raw-value consequence | The new raw-approximation corollary uses the exact zero-or-positive maximum. It distinguishes finite-factor and inverse-polynomial additive accuracy from fixed additive tolerances. A fresh referee checked it. |
| Secondary sources assert hypermetric hardness despite primary open-status statements | Introduction discloses both assertions and their precise families. The novelty claim is qualified and concerns complete proofs with explicit domains and promises. |
| Boros–Hammer issue/DOI was incorrect in the source note | Bibliography uses volume 18, issue 1, pages 245–253, DOI `10.1287/moor.18.1.245`. |
| Global notation reused `W` for a lattice basis | Section 5 now uses `R_Λ`; `W` remains the nonroot vertex set. |
| X3C and parameterized-complexity abbreviations needed definition | X3C, FPT time dependence, and XP time dependence are explained on first use. |
| Final exposition closure identified four local ambiguities | The opening cutoff names the rounded psd family, the common-sphere statement is restricted to positive definite moments, fractional parts and primitive directions are defined, and gap-zero display names are consistent. |
| Discussion repeated scope remarks and writing-process commentary | Final discussion focuses on mathematical implications and the unresolved full-gap question. |
| Initial TeX build caught a double superscript on a primed transpose | Grouped the primed vector. Final build and bibliography have no warnings. |

The raw maximum, quarter-value test, primitive-direction identity, and rational
rank-one formula now have complete proofs in the manuscript. No unsupported
normalization or approximation transfer is used. The exact metric-polytope
promise for gap-zero separation is proved with rational bounds.

The remaining full-gap question at positive semidefinite points is an explicitly
different problem. The manuscript does not leave a claimed theorem dependent on
an unresolved argument. No new experiment was necessary for the theoretical
contributions; no existing experiment was rerun. Targeted document checks are
recorded in `../verification/VERIFICATION.md`.
