# Current manuscript delivery after scientific-framing revision

The complete 33-page anonymous paper is `../main.pdf`; its standalone LaTeX
source package is `../certified-minlp-paper-source.tar.gz`. The title remains
**Checkable Lower Bounds for Convex Mixed-Integer Nonlinear Optimization
through Rational Outer Approximations**.

The revision implements all five recommended presentation changes:

| Recommendation | Delivered change |
|---|---|
| State the research problem first | Abstract and introduction identify nonlinear-cut validity and exact master/model binding before the implementation inventory |
| Make the contribution explicit and bounded | Early contribution subsection states the concrete interface and conditional soundness, retaining established prior attribution |
| Abstract organized around scientific results | Problem, method, guarantee, principal 203/289 replay result, exact local proof-check findings and practical significance replace run/repair bookkeeping |
| Experiments organized around questions | Section 6 presents capability, failure mechanisms and costs; Appendix B retains protocols, complete production accounting and separate V1/V2/V3 repairs |
| Distinguish contribution and supporting evidence | Method, empirical findings, validation and reusable artifacts have distinct roles; conclusion synthesizes the scientific lessons |

The mathematical proofs, reference entries, generated tables, checker code,
formal proofs and experimental archives remain unchanged. Earlier 161-test,
Lean and numerical verification evidence remains applicable; it was not rerun
for a prose-only revision. Current source extraction/build and PDF/bibliography
matching passed. `final-delivery-checks.json` identifies the current artifacts.
The prior delivery summary and checks are preserved under
`clarity-revision/pre-revision-*`.

All three new sequential gates are accepted. Each received five independent
reviews; all three valid R1 minor findings were corrected by a separate agent
and inspected before R2. R2 and the final full-manuscript R3 review were clean.
No unresolved valid finding remains. Review records and coordinator decisions
are in `clarity-revision/`.

The core and bulk artifacts retain their earlier identities; see
`../supplement/README.md` for reproduction. No public upload, commit or journal
submission was made during this revision. The manuscript's supported scope
and the journal's editorial acceptance decision remain distinct.
