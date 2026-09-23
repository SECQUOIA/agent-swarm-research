# Independent review: Stage 00, round 01, reviewer 4

Reviewer: `paper_reviewer_4`. Date: 2026-09-07.

Verdict: **No major issue found in this preparation stage. Three minor documentation issues should be corrected before acceptance.** This verdict does not certify the candidate theorems, unfinished investigations, or novelty.

## Scope and independence

I read the plan, claim map, notation ledger, LaTeX entry point and preamble, status section, project README, review ledger and templates, build record, and author handoff. I did not read other reviewers' reports or coordinate findings with them. I compared the scope against the final research report, uncertainty working paper, risk-sensitive and finite-precision prior-art audits, numerical verification record, the scalar-to-bulk and generic-fold notes, and the observable-cancellation note.

The principal reviewed source hashes are:

| File | SHA-256 |
|---|---|
| `PLAN.md` | `943457d6888a441c054a0e23b5c3dc69ac0bc6262e71387dc1cf9aca81cdb14a` |
| `claims-map.md` | `aae5c9883aa3de7c81b5a916a76f9c9ea7634ce3ddc93a39597f7663fa8342f6` |
| `notation.md` | `6fbcb755c8306fa62f40554696864fe766268b6115d661d3f98be1c9f2d1739b` |
| `main.tex` | `11f0cd99bd54159fbceec18943ecb3abbf2a5e33c72ff46782189dcc135b5c13` |
| `preamble.tex` | `69757a0786a132d9f837548aadfe1bd55e7503acb870508d66234e2d74e54572` |
| `reviews/stage-00/author-handoff.md` | `6f3628b176d332c6780cb64bc9d20072a5ecbb746a268799c2f7a22490243bf5` |

## Checks performed

The scope captures the current uncertainty package: the uniform baseline, unrestricted predetermined-moment design, critical coefficient, generic folds, local placement required for exact observation, noiseless finite-bin policies, and full-bulk transfer. It correctly treats the two genuinely unfinished sharp limits as investigations rather than proved results. The required self-contained rederivation of deterministic quadratic placement is appropriate; the unrelated traveling-channel and deterministic finite-floor developments need not be included to satisfy this paper's stated topic. The source-dependent cancellation result would be useful context for the nonzero-mean restriction, but extending its general wall-drift theory is not necessary here.

I independently evaluated the candidate constants from the formulas in the map: C0 = 4.64747600940097, Cpl = 6.22282373601989, K1 = 18.3860636501143, Kobs = 22.4046282307491, Kcrit = 2.02233076396939, and Kcoarse = 25.7238273887633. They agree with the documented numbers. The proposed interior crossover has the correct endpoint factors: substituting the local constant at zero gives Kobs; substituting C0 times the one-quarter power gives the prefactor 2^(-3/4) and integrand exponent -7/8, hence Kcoarse. This is a consistency check only, not a proof of the proposed limit. The dimensional response factor in the map is also consistent with rescaling arclength and the surface operator.

The numerical plan identifies the important existing failures: slow asymptotic convergence, trial-versus-optimum confusion, sparse scenario overfitting, and whole-line tail error. It requires independent parameter nodes and lower certificates, rather than merely rerunning the same optimizer. No numerical output is improperly presented as stage-0 evidence of a theorem.

The literature plan appropriately distinguishes new candidate operator-level laws from established allocation, compliance, quantized-decision, and bifurcation arguments. The linked risk-design audit also includes optimized-tolerance work, which should be carried into the Stage 7 literature assessment even though the short inventory does not name it individually. No unsupported absolute novelty claim is made. A fresh primary-source assessment is explicitly future work and is not a defect in a preparation-only stage.

The workflow matches the user's requested sequence, including a separate fixer, five repeat reviewers after any valid major issue, correction of all valid minor issues, and a separate complete-draft audit. The current documents do not falsely claim those future reviews have already happened.

## Findings

### R4-01 — Minor: state the canonical ensemble and zero axial wall drift explicitly

Locations: `claims-map.md`, “Scope and assumptions that must survive every theorem,” and `notation.md`, rows for `kω(s), kc(s)` and `u(y), V`.

The inventory repeatedly uses “the cosine ensemble” and lists its exact constants, but does not itself write the defining rate `kc(s)=(c+cos s)^2`, the circle `s in R/(2πZ)`, and `c uniform on [-2,2]` together. It also gives `V=∫Ωu/(A+KP)` without explicitly saying that the wall has zero axial drift. These conventions can be recovered from the source notes, but a scope and notation ledger should fix them directly. A nonzero wall drift changes the source observable and the mean velocity.

Remedy: add the canonical dimensionless ensemble definition and specify immobile axial wall drift in the scope paragraph or model rows. Stage 1 should derive the model under exactly these conventions. This is a preparation-document omission, not a finding that the future transport derivation is wrong.

### R4-02 — Minor: Gaussian amplitudes conflict with the notation ledger

Locations: `claims-map.md`, L4 row; `notation.md`, `A, P` row.

The ledger explicitly reserves A for bulk area and says to use no other quantity named A. The Gaussian counterexample uses `g=A cos s+B sin s` and `A²+B²` in the same manuscript inventory. This is a local notation inconsistency with an easy correction.

Remedy: use, for example, `ξ1, ξ2` for the independent normal amplitudes and write the bound `J ≥ 2P/(ξ1²+ξ2²)`. Keep the bulk area notation unchanged.

### R4-03 — Minor: clarify when the reviewed snapshot is recorded

Locations: `reviews/stage-00/author-handoff.md`, final paragraph, versus `PLAN.md`, mandatory workflow step 2, and `reviews/README.md`, snapshot instruction.

The handoff says the coordinator will record “the reviewed file snapshot and final acceptance only after the required cycle.” The plan correctly requires freezing the changed files before the five reviews. Deferring the identifying record until after the review/correction cycle makes the audit trail ambiguous, especially if source files change while reports are being returned.

Remedy: record the round's immutable source manifest before review or preserve an explicitly identified initial manifest, and reserve the post-cycle record for the accepted corrected snapshot. If such a manifest has already been recorded outside this folder, link it and adjust the handoff wording. This is an audit-record issue; I found no evidence that different reviewers actually saw different drafts.

## Overall assessment

The stage provides a coherent, appropriately cautious plan with concrete proof obligations. The open problems are not hidden by scope exclusions, and the numerical and literature plans are sufficient at preparation level. After the three minor corrections and the coordinator's check, I see no stage-0 reason to delay Stage 1. The substantive proofs, closure questions, primary-source checks, and publication readiness remain to be established by their assigned stages and final review.
