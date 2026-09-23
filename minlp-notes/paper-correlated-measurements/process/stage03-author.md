# Stage 3 author handoff

Date: 2026-09-13. Status: author complete; five-reviewer gate pending.
Root owns acceptance and PROCESS.md. No agents were spawned by the author.

## Files

- Added `sections/03-approximation.tex`: trace FPTAS and all promised classes,
  exact feasibility and bit complexity; scope/hardness/prior distinction;
  shared rational spectral normalization, DAG cover and full proof; criteria,
  singular contrasts, prior/congruence reuse and true finite-memory transfer;
  represented-matroid theorem and specific qualified contribution comparison.
- Added `appendices/approximation.tex`: complete scalar predecessor reduction
  and complete represented-matroid proof with source and representation limits.
- Added input lines in `main.tex`, bibliography entries in `references.bib`,
  actual-label coverage in `process/coverage.md`, and primary inspection/access
  records in `process/literature.md`.
- Added `verification/stage03/check.py`, exact `results.json`, and build log.
  Test code explicitly imports original audit helpers but never their main
  routines; historical result files and scientific sources are not overwritten.
  Final portable-supplement packaging remains assigned to Stage5.

## Development and corrections

The single shared normalization lemma replaces duplicate DAG/matroid proofs.
It handles exact singular ranges, owner multiplicity, dyadic scaling, signed
floor residuals and bit length; no feasibility oracle is claimed for arbitrary
families. DAG and matroid feasibility are separately proved. The matroid proof
retains original rank during filtering/deletion and gives the full product-grid
interpolation bound, including growing matroid rank.

A useful strengthening developed here is an input-gap cooldown/count product
for the trace FPTAS: history length controls information only; spacing is
tracked separately with g clamped to n+1. This preserves exact constraints
without an exponential dependence on the spacing parameter. The partial-packet
complexity envelope is fully rational, using sqrt(kappa*s)<=s; all algorithms
operate in supplied rational coordinates rather than computing whiteners.

No theorem-level defect was found in the source results. The inherited scalar
priority claim remains withdrawn. The Gaussian-message reduction explicitly
handles the printed inverse/block-order issue by giving positive variance cost
only to a singleton target bag. It is distinguished from a complete rational
implementation of the predecessor's spectral net; our own FPTAS bit proof is
independent and complete.

Root's author-phase read identified wording corrections (r_min notation,
accuracy domain, contained atom ranges, no generic feasibility claim, absent N
in the normalization lemma, and nonzero modular residues). All were accepted
and incorporated before handoff. The final appendix includes exact scope
witnesses rather than unsupported broad exclusions. Bibliographic inspection
corrected Pál Somogyi's name and ESA2026's 18-page extent while drafting.

## Verification

`code/research_20260912/.venv/bin/python paper-correlated-measurements/verification/stage03/check.py`
passed. New elementary checks cover every subset of K3,3 (64 subsets) for the
1/9 hardness separation, 27 exact scalar-reduction accuracy combinations, the
3/5 versus 1/2 local-cost witness, distinct almost-parallel singular ranges,
and finite-memory ratio constants. Two new all-basis DAG fixtures check oblique
rank-deficient ranges, variable-length paths and signed-profile collisions.
Explicitly reused audit helpers additionally replay all 15 adversarial matroid
fixtures and exact interpolation/recovery tests: rank loss, forced-owner
aliases/dependence, rational contraction, q>p, zero information, negative
labels, modular cancellation and finite-field reinterpretation.

These are tiny exact proof stress tests, not empirical runtime evidence for a
large-polynomial algorithm. Root separately verified cooldown/count states
against exhaustive regression evaluation; that evidence is in
`verification/stage03-root` and was not authored here.

The integrated LaTeX build uses `latexmk -pdf -interaction=nonstopmode
-halt-on-error -outdir=build main.tex`. Final log has no undefined citations,
undefined references, overfull/underfull boxes, or LaTeX warnings. The manuscript
still intentionally lacks later-stage sections/abstract/intro; this stage does
not claim the entire submission draft is complete.

## Remaining scope

No unresolved Stage3 mathematical issue is known to the author. The explicit
limitations (fixed p for spectral sets; fixed contraction/noise promises;
complete-packet selection; rational matroid representation; no practical
spectral-set speed claim) are theorem boundaries, not unfinished positive
results. Literature priority is qualified to the specific combined cover.
Unretrieved Onn2010 Chapter6 and Radovilsky2006 full texts are not treated as
negative evidence. Reviewers should inspect this stage and its accepted
interfaces rather than count planned later sections as omissions.
