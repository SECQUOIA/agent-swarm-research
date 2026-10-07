# Review evidence

## Central positive result

The frozen initial manuscript and supporting files were reviewed by five fresh
Codex reviewers and a fresh Claude session with one Fable and three Opus
reviewers. The scope was the count and enumeration arguments, spectral
treewidth specialization and bit complexity, literature claims, writing, and
supporting checks. These were internal adversarial reviews, not external
peer review.

The accepted findings were localized. The manuscript now defines the noisy
branches `F_A` explicitly and uses them in dictionary construction and optimizer
recovery; a scalar active-zero example checks that omitting the noise changes
the selected bit. The abstract expectation theorem requires measurable oracle
selection and deterministic handling of remaining ties. The revision also
specifies the noise grid endpoints, states the separator argument in both
cases, clarifies factor ownership and the dynamic-programming induction, uses
“coordinate slices,” and adds classical citations where the ingredients are
used. Bibliographic metadata and the repository source paths were checked.

The finite count tests were strengthened with atomic ties and a family attaining
the bound exactly. The earlier finite checks were valid; the new cases improve
their diagnostic coverage and do not correct a counterexample to the lemma.

The lead rejected automatic computation of the supplied spectral bounds and a
fully expanded polynomial exponent as unnecessary for the stated theorem.
Reuse of symbols within separate local scopes was not judged a correctness
defect. The accepted changes preserve the proof method and theorem scope.
Their verification consists of direct inspection and the targeted checks
recorded in `validation.md`; the full review round was not repeated for these
localized fixes.

The algorithm remains a complexity construction, without a measured practical
speedup. The checks in this stage did not implement the complete spectral treewidth
algorithm; the final-integration section below records its later implementation.
Finite checks do not prove asymptotic claims. The novelty statement remains limited
to the specific hypotheses and output proved in the manuscript.

## Negative results and representation limits

Five fresh Codex reviewers and a fresh Claude session with one Fable and
three Opus reviewers examined the frozen stage-2 increment against the
stage-1 commit `02abbb9b4053acd9da081a9b746050ce4be942b9`. The target
included the hardness and message-size sections, star appendix, exact
checker, integration text, bibliography, and evidence records. These were
internal adversarial reviews. No accepted finding identified a defect in a
mathematical theorem or proof.

The accepted changes correct attribution and make existing scope explicit.
Das–Kempe's predictor-only bandwidth graph is now distinguished from their
response-inclusive tree graph. The literature comparison adds the
multi-period factorizable-matrix result of Lee–Gómez–Atamtürk and Çivril's
general sparse-approximation hardness, credits Gaubert et al. for established
approximation power laws, and acknowledges Choi et al.'s exponential-star
observation. The star contribution is restricted to its stronger order,
weight, conditioning, and row-normalization statement. Conference metadata
were added for Lee–Raghavendra–Steurer, retaining author-version theorem
locators.

The revision states the complexity assumption and the joint scaling of
linear costs and penalties; it makes no bounded-penalty scaling claim.
It displays the residual identity behind the existing unit-penalty gap,
defines the additive constant, and avoids reusing the noise-grid symbol.
The deterministic message lower bound, boundary-cost convention, and
matching pruning exponent are explicit. Statements about combining
hardness restrictions and transferring a face obstruction to an epigraph
now describe what these proofs establish, rather than asserting an
impossibility. The coverage map retains the unit-diagonal hypothesis.

The lead rejected a proposed precise perturbation scale at which all
message supports would remain indispensable: the submitted argument does
not establish that threshold. The manuscript instead states the
unperturbed result and its consistency with an expected smoothed bound.
It also avoids treating a dense inverse in one scalar projection as a
proof against every block reformulation. No general theorem scope changed.

All accepted fixes were localized attribution, wording, or display of
existing algebra. Under the build skill's minor-fix exception, the lead
selected direct inspection and the scoped validation recorded in
`validation.md`, rather than another full review round. This does not
replace the cumulative manuscript review. Claude inspected the PDF through
text extraction only; a Codex reviewer also performed visual inspection.
The stage-1 proofs served as context in this round, rather than receiving
a new complete review.

## Supporting moments, geometry, and recursive algorithms

Five fresh Codex reviewers and a fresh Claude session with one Fable and
three Opus reviewers completed review of the frozen stage-3 increment
against `9a527b06`, with the surrounding manuscript as context. The target
included the new moment, geometry, and recursive appendices, the short star
refinement, integration text, primary-source comparisons, exact checker, and
evidence records. All review work was read-only. These were internal
adversarial reviews, not external peer review.

The accepted findings were localized assumptions, wording, and attribution.
The loop count now explicitly concerns compact components of the tie set in
the square's interior, excluding arcs that meet the boundary. The recursive
bit bounds explicitly require rational supplied diagonal-dominance bounds
and include their encodings in the input length. The invariant gradient
bound is stated on its box, and the continuous block proof explains why
finite pairs of distinct support polynomials are almost surely different.
The spectral application of the planar theorem identifies its half-width
as `M=R` and uses `L=L_2`.

The recursive appendix directly credits Bhathena et al.'s established
parametric recursion and pruning. It states that the block-size-two/tree
case is already solved deterministically on arbitrary trees and that this
smoothed diagonal-dominance estimate gives no improvement there. Its
particular expected bound combines the invariant box with noise count and
moment control; the text does not claim that the invariant box alone
replaces the structured-graph work's assumptions. The comparison with the
spectral theorem now states the stronger hypotheses and explicit block
estimates without comparing an arithmetic bound to a bit bound.

Other edits define affine rank, specify a smallest admissible power-of-two
CAD noise grid, replace an imprecise higher-gap attribution with the
classical conditioning-method attribution, and remove unexplained historical
language from the manuscript. Research history remains in the coverage map.
The checker now reports how many rank-tail bounds are below one and how many
of those have a nonzero event probability, computed from the actual cases.
No new theorem or broad priority claim was added.

The lead rejected wholesale renaming of locally defined symbols: no
cross-scope defect was identified beyond the planar `M/R` correspondence,
which is now explicit. The reviewers examined the analytic loop/interface,
coarea, genericity, and planar graph arguments as mathematical arguments;
finite checks do not validate those analytic statements or the asymptotic
CAD complexity bounds. The review does not establish practical performance
or verify a complete spectral or recursive implementation.

Under the build skill's minor-fix exception, the lead selected direct
inspection and targeted validation for the accepted localized fixes instead
of another full review round. The commands and results are recorded in
`validation.md`. This decision does not replace the eventual cumulative
manuscript review.

## Final cumulative review

Five new independent Codex reviewers and a fresh successful Claude session
with one Fable and three Opus reviewers examined both the final integration
against `aaa7b5c278501e55e847d0c58a6c67c8ad6a52b4` and the cumulative work
against the original baseline `d29dc99e0c6ecbef474e3add3f64a82cca38e5f7`.
The frozen target included the manuscript, bibliography, reference implementation,
four checkers, PDF, README, and evidence records. The 24-file aggregate digest
was checked as `6cd75677a4cc865258c848c12f494b36e7b9e652650ac7a961178814f96d6188`.
Commit `4eb31ba2` preserves that reviewed snapshot.
An initial Claude attempt exited with status 143 and an empty log, producing
no verdict; only the fresh successful retry is counted as completed review.

The lead's independent adjudication found no substantive defect and accepted
localized attribution, assumption clarity, and diagnostic-coverage changes:

- Name the spectral reference and its valid message-specific bounds and mesh.
- Specify the lifted message's separator and its translated boundary interval.
- Credit Beier–Vöcking's classical bit-class conditioning method and compare
  the closest bicriteria Pareto result of Beier–Röglin–Rösner–Vöcking.
- Independently assert the public coordinate/Lipschitz bounds and exercise a
  nine-point two-dimensional midpoint net in the spectral checker.
- Normalize a source-map path and cross-reference later implementation evidence
  from the historical validation records.

No theorem or reference-algorithm change was required. Under the build skill's
minor-fix exception, the lead chose direct inspection and targeted validation
of these fixes rather than another full review round. Commands and results
are recorded in [validation.md](validation.md). The lead then inspected the
revised TeX, bibliography, checker assertions, and changed-page previews,
and requested no further source changes. This was targeted internal,
non-formal, non-exhaustive review, not external peer review or a guarantee
against all errors. It does not establish practical performance or verify
implemented CAD/recursive SDD solvers. No project-wide checks or CI inspection
were performed.

## Editorial revision of 2026-09-30

An expert in the decision-diagram line of work read the previous version and
said that it was hard to follow, mixed in decision-diagram material, presented
the exponential size of projected-row diagrams on stars as new, mixed central
and minor results, and gave no practical evidence. In response, the author
removed the moment, geometry, and recursion appendices (now in `companion/`),
demoted the decision-diagram star theorem to Remark `rem:dd-star` with
corrected credit to Choi et al. Section 7.2, and added a Discussion section on
practical relevance and open questions. Every section was rewritten for
clarity.

The rewrite was reviewed in two internal rounds (six and then four reviewer
lenses: mathematical fidelity, an indicator-MIQO referee, a smoothed-analysis
referee, prior-work accuracy, and consistency), each finding checked by a
separate verifier before it was applied. No accepted finding identified a
mathematical error. Accepted changes made the numerical-dependence claim
precise (Corollary `cor:magnitude` forces the dependence on `C` relative to
`sigma`), stated that each message is computed directly rather than composed,
reframed the additive certificate (one grid-oracle call already approximates
the original optimum), unified terminology and notation, and added credit to
Beier–Vöcking Theorem 3, Röglin–Teng Lemma 6.1, Fiorini et al., Murty,
Atamtürk–Gómez, Bodlaender, and the open question of Bhathena et al.
(structured graphs, Section 2.2). These were internal reviews, not external
peer review.

## Restructuring of 2026-10-01

The same expert read the revised introduction and said it still assumed
familiarity with Bhathena et al. and with tree-decomposition methods, used
separators and the "minimum over supports" on page one, and read as
AI-written. In response the introduction was rewritten at a high level; a
new Section 2 (Preliminaries, `sections/preliminaries.tex`, formerly
`model.tex`) explains dynamic programming on a chain, tree decompositions
with a figure, how exact dynamic programming combines child messages,
messages and dictionaries, the perturbation, and the proof outline; and a
new Section 3 (`sections/related.tex`) holds the detailed comparisons that
were in the introduction. Every other section received a clarity pass, and
repeated statements were reduced to one home each. Liu, Fattahi, Gómez,
and Küçükyavuz (path case) were added to the credits.

Three internal review rounds (an outsider reader, the expert's
perspective, content preservation, citation accuracy, consistency, and
style) checked the revision, each finding verified before it was applied.
They found one incorrect sentence ("XP in w"), now removed, and no other
mathematical error; the content check against the previous version found
no lost theorem, caveat, or verified citation. These were internal
reviews, not external peer review.
