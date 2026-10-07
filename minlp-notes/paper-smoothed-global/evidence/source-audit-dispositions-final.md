# Source-contract dispositions

This record connects the Luna source audits to the final manuscript. It is an
integration record, not an additional literature search. All literature work
was assigned to GPT Luna with maximum reasoning. The one serialized `$lit`
owner records source intake and KB checks separately in the final literature
audit and handoff. The scientific source target is
`snapshots/final-submission-r4/`; all 20 TeX files equal the independently
reviewed `final-literature-integrated-r2/` files.

| Source contract | Final disposition |
| --- | --- |
| Renegar, Part III, Theorem 1.1 | The primary theorem supports the block-sensitive format, height and bit-work bounds. The manuscript uses a fixed admissible effective constant, without claiming that its numerical value was extracted from the published asymptotic bound. |
| Kozlov–Tarasov–Khachiyan; Del Pia | Luna checked the exact rational convex-QP interface and Del Pia's exact fixed-integer-dimension MIQP theorem. The latter pinpoint is explicitly to arXiv v2, Theorem 3; the bibliography also identifies the published article. Rational point-height control uses the manuscript's continuous-slice polishing argument. |
| Grötschel–Lovász–Schrijver | The checked weak separation/optimization statements permit a point in an outer neighborhood and comparison with the eroded set. Appendix C explicitly repairs feasibility and the objective comparison rather than silently treating weak optimization as exact optimization. Oracle answer lengths and bit costs are charged. |
| Hochbaum–Shanthikumar | The primary theorem supplies the arithmetic/value-oracle TU algorithm. Appendix F adds rational fixed-degree evaluation and exact LP operations to obtain the stated bit-work interface. |
| Basu–Lerario | The tube bound is tied to the checked 2021 arXiv v1, not to an unread later journal version. The manuscript proves the finite-grid covering step separately. |
| Basu–Pollack–Roy | Luna directly checked Weak Bézout, real-root isolation, sign determination, separation, subresultants, and the Puiseux field/constant-term facts in the primary second-edition text. |
| Mehlhorn–Sagraloff–Wang | The checked arXiv v2, Theorem 5 gives complex disks and refinement. The final prose distinguishes this result from BPR's real intervals, gcd and sign operations. It does not attribute all exact univariate routines to the fast disk algorithm. |
| Fulton | The inaccessible refined component-degree locator is no longer a proof dependency. Appendix C now proves the needed nonsingular-root bound directly, cites the verified BPR Weak Bézout theorem, and keeps Fulton as general background. |
| Ding; Patrinos–Sarimveis | The checked global correspondence and piecewise-quadratic value/solution statements are used with their qualification on uniqueness and regularity. They are not asserted to give a polynomial bound on all parametric regions. The read technical-report version is identified. |
| Pardalos–Vavasis | The primary title/abstract supports hardness with one negative eigenvalue. The introduction no longer adds an unverified bounded-polytope qualifier. |
| Rouillier; Cox–Little–O'Shea | Full-text access limits are recorded. Rouillier is used for the introductory RUR comparison, not an unverified complexity theorem. Appendix F spells out the leading monomials and quotient basis used in its own construction; no invented textbook pinpoint is given. |
| Evans–Gariepy; Federer; Rockafellar and other classical books | Where a primary full text was unavailable, the audit preserves metadata-only status. Standard background facts retain general citations without invented theorem/page locators. Their source packages are not described as read. |
| Local companions | The final introduction precisely credits cubic and supplied-convexifier recourse results, the existing quartic obstruction, growth-conditioned decomposition bounds, indicator-penalty noise, and output-interface limitations. Those results are not relabelled as new. |

Two source-audit findings required additional proof work. The new Appendix C
proof treats any finite set of nonsingular zeros, deforms the equations to
coordinate powers, and compares homogeneous quotient dimensions. The
independent isolated-root review passed that proof, including degenerate
and positive-dimensional ambient zero sets. The explicit Appendix F solver
budget now includes the elementary arithmetic, subresultant, determinant,
isolation and refinement ledger; the focused R4 review passed its numerical
base and inherited strong-field use. Neither proof is justified by extracting
an unspecified constant from a classical polynomial-time statement.

The principal source evidence is `literature-preliminary.md`,
`bibliography-assembly-luna.md`, and the three
`classical-*-source-audit-luna.md` files. The independent proof evidence is
`reviews/isolated-root-proof-independent-sol-r1.md` and
`reviews/component-solver-budget-sol-r4.md`. The master literature audit
records discovery rounds, source intake outcomes and remaining access gaps.

The three unpublished companions have no supplied author or date. Their
references therefore retain exact titles, the date description `undated`, and the description
“Unpublished companion manuscript.” Removing optional sort keys avoids
printing each short title as an author substitute. Standard `plainnat`
reports three expected missing-author/key sorting warnings; these do not
represent missing citations, unidentified titles, or invented authors. Spelling
out `undated` also avoids a doubled terminal period from `plainnat`'s date
suffix when numeric natbib citations suppress disambiguation letters.
