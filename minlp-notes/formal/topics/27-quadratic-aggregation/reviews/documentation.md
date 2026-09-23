# Final documentation consistency review

Date: 2026-09-22. Read-only review of topic 27's status, frozen claims,
coverage, review and verification records; the aggregation source note and
historical review record; the aggregation numerical-check README; the root
and formal indices; and the new research-log entry. This reviewer wrote
only this review record and did not change source notes, paper files, or
unrelated concurrent work.

No inconsistency was found in the documented formal scope. All current
status statements identify the completed target as Theorem 1 under
asymptotic hyperplane convexity, its HHC specialization, and Lemmas 1–3.
The recorded twelve obligations, eleven modules, and 178 audited owned
declarations agree across the status documents and observed audit evidence.
The source note's new Section 3.4 accurately describes the implemented
constant-elimination and single-compactness proof.

No stale current claim that this main scope lacks a Lean proof remains in
the selected documentation. The old review's lack-of-formalization statement
is explicitly historical and superseded for the main theorem and lemmas.
The source inventory records the state at the start of work, rather than
pretending that the later completion was already known. The manuscript's
stage-1 process remains separate from completion of this formal package.

The source note, root entry, topic package, numerical-check README, review
record, log entry, and paper section consistently exclude the ancillary
corollaries, examples, numerical software, and literature-priority claims
from the formal verification. They preserve the distinction between
existence of a nontrivial globally convex aggregation and a complete hull
description. Queue identifiers 22–26 retain their prior status.

The verification record describes targeted module builds, the transitive
owned-declaration axiom audit, and individual kernel replays. This agrees
with the verification driver, manifest, successful build log, and explicit
178-declaration audit result inspected in the earlier paper-section review.
The eleven current Lean sources were independently matched to the manifest
in that review. The record does not claim a project-wide local build,
inspection of CI, replay of all Mathlib, or an independently implemented
kernel. The independent cone-separation module is included in the audit.

The paper-build subsection of `VERIFICATION.md` is now complete. The
captured `latexmk` output reports that its target was up to date, the saved
final LaTeX log reports a four-page PDF, and the saved extracted text contains
the theorem, shorter proof, and scope limitations. These support the stated
check of that developing-paper snapshot; they do not certify the rest of
the manuscript.

A final read-only SHA-256 comparison found that the formal-verification
section, setting section, macros, bibliography, and aggregation result note
still match `paper-sources.json`. The concurrently developed `main.tex` and
current PDF have since changed. The recorded four-page build must therefore
be understood as the captured snapshot, not as a claim about the current
state of that separate authoring process. The coordinator was notified;
this review did not overwrite or rebuild the concurrent paper.

Final integration keeps the paper's staged review intact: its main draft
defers the contributed formal section, while `formal-verification.tex`
builds that section with the setting and bibliography as an independent
supplement. `FORMAL-VERIFICATION.md`, the topic README, and the verification
record state this distinction consistently. The wrapper includes exactly
the setting and reviewed formal-verification section, without changing the
main draft's inputs.

The supplement's saved build log reports successful completion, and its
final LaTeX log reports a four-page PDF with no LaTeX or box warnings found
by the focused log search. A separate SHA-256 comparison confirmed that
all six recorded supplement source/PDF files match `supplement-sources.json`.
Every local Markdown link in the supplement README resolves. This supplies
a current, independently buildable artifact of the verified result without
claiming that the paper's separate manuscript stages are complete.

Targeted link check: a local Python script checked all 399 local Markdown
link targets in the eight selected edited external documents and the ten
then-existing Markdown files under topic 27. Every target existed. The
script did not inspect the rest of the repository, and it did not validate
remote URLs or heading anchors. A focused text search also checked the
current-versus-historical wording noted above. No Lean checks or CI queries
were repeated for this documentation review.
