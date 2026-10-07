# Final mathematical review: admissible integer classes

Review began: 2026-10-05. Final disposition: 2026-10-06. Reviewer owns this
evidence report only. Review scope is
`sections/lattice.tex` and `appendices/lattice-proofs.tex`; no manuscript file
was edited. This is an independent mathematical review of the saved manuscript,
not acceptance of a source-note audit as proof.

## Disposition

**Accepted under the stated relaxation, certificate, operation, and probability
hypotheses. No unresolved mathematical or readability issue remains in the
reviewed chapter and appendix.** The main arguments and complete appendix have
been read, and every reported repair has been reread and verified. The author
sent a finished-version notice after the final citation additions, and the
saved file hashes below were independently checked against that notice.

Bibliographic verification belongs to the Luna literature lead and root; this
reviewer did not browse or perform literature research. The final standard-input
citations and their theorem locators were checked against the supplied Luna
evidence. This is mathematical manuscript approval for the recorded source
versions, not a claim of journal acceptance or of independently completed
global integration checks.

Narrow final attribution refresh, 2026-10-06: the prose following
`lattice:count-bound` now credits the branch-and-bound midpoint/leaf-occupancy
mechanism to Dey, Dubey, and Molinaro alone. A separate sentence credits
Kaibel and Weltge for a related hiding-set obstruction to small formulations.
This matches the integer comparison in the completed `evidence/LITERATURE.md`:
Kaibel--Weltge's result concerns formulation complexity without auxiliary
variables and is not being cited as a branch-and-bound tree-size theorem.
The accepted mathematical disposition is unchanged. Only this attribution
change and the saved source hashes were checked; unchanged proofs were not
reviewed again.

## Proof scope examined

| Statement / proof labels | Scope and assessment |
|---|---|
| `lattice:tree-definition`, `lattice:class-definition`, `lattice:class-number`, `app:lattice:semantic` | The benchmark is the least number of admissible convex classes covering the explicitly required integer set P. Fractional coverage is not required. Routing produces admissible leaf classes. Exact binary attainment uses a full hemispace induction, including lower-dimensional boundary recursion and nonclosed sets. The final split covers the remaining P-points, which need not cover the remaining fractional set. The root may vary; kappa=1 at a prescribed larger root is explicitly qualified. For finite P, replacing convex node sets S by conv(S intersect P) preserves their integer points and coverage while shrinking bounds. |
| `lattice:graph-bound`, `lattice:count-bound` | Pairwise midpoint and segment conflicts and finite-set occupancy give valid lower bounds. Counting now excludes the undefined empty-set/zero-denominator quotient and states that zero occupancy prevents a finite cover. |
| `lattice:operations`, `app:lattice:operations` | Cuts preserving required node integer points retain the original-phi class lower bound. Cuts valid only for feasible points require P=F. Sequential removals are tested on the current effective set and give kappa <= leaves + certified pieces. The binary empty-node accounting, one-pass 2n budget, root-only pass, and actual-change counting for general iterated integer tightening are complete. Enumeration conversion explicitly requires certified omitted tails. |
| `lattice:linear`, compact projected MILP example | Violated integer rows give the pure ILP cover; projected rational sublevel rows give the MILP cover. The short 2n-row absolute-value epigraph formulation has exactly 2^n classes for epsilon<1/2. The proof does not infer complexity from formulation length alone. |
| `lattice:jeroslow` | The quadratic parity instance has two admissible sum classes and a three-node split certificate. Every proper binary variable tree has the binomial leaf count, proved by the two count states and Pascal recurrence. This does not assert the same separation for arbitrary split trees. |
| `lattice:facet-number`, `app:lattice:facets` | For finite convex phi, the strict sublevel is open. Closed halfspace covers and full-dimensional lattice-free enclosing polyhedra have the same minimum size, with empty strict sublevel treated separately. The external maximal lattice-free polyhedron theorem is stated with the hypotheses actually used. Its 2^n conclusion and the compact-neighborhood constrained variant are valid. |
| `lattice:siegel`, `lattice:moments`, `app:lattice:cvp-proof` | The external Siegel formula states Haar probability, unimodular covolume one, n>=2, and the nonzero-vector sum normalization. Torus unfolding derives mean V and variance V for the joint lattice-target law, including deterministic close-pair moments. No Poisson or independence assumption is made. |
| `lattice:cap`, `app:lattice:cap-proof`, lower part of `lattice:cvp` | The compact hull of the finite sampled class has an attained minimum norm, avoiding a closure or attainment gap. The outer cap is contained in an open ball of radius at most lambda_1/sqrt(2); strict obtuseness gives at most n+1 points by affine dependence. The optimum, shortest-vector, and count events are combined by a union bound. |
| `lattice:sphere-cover`, upper part of `lattice:cvp` | The appendix gives the full spherical-net construction, cap-mass lower bound, probabilistic cover, uniform inward-angle loss, and finite-small-dimension adjustment. Near points and distant halfspaces share exponential base sqrt(1+(1+delta)^2-q). Tau<=0 is handled separately by one class. |
| `lattice:cvp-exponents` | For deterministic q_n=epsilon_n/g_n^2 tending to q_0<1/2, the valid bounds are one-half log_2(3/2-q_0) and one-half log_2(2-q_0). The limits 0.29248... and 1/2 require q_n=o(1). Slowly vanishing delta_n and gamma_n make all failure probabilities vanish. There is no claim that an exact 1/2 exponent survives fixed positive relative tolerance. |
| `lattice:cvp-clique`, `app:lattice:clique-proof` | The unconditional fixed-distance close-pair count dominates nonconflicting pairs only on the optimum event; it is not conditioned before applying moments. The lens containment, radial monotonicity condition rho>=2/n, integration, deletion, and limiting parameter choices are complete. Its 0.20752... lower exponent is distinguished from the stronger occupancy lower bound. |
| `lattice:curvature-gadget`, `app:lattice:gadget` | The perspective projection and dual convexity formula, common affine minorant, original optimality/uniqueness, feasible midpoint clique, stronger block-epigraph hull root exactness, and uniform rational family are all proved. Global cross-block diminishing returns and the sum of asymmetric gaps are controlled uniformly in k. Polynomial encoding and fixed positive absolute tolerance range follow from the explicit rational family. |
| `lattice:C1`, `lattice:path` | The generic path statement requires the incumbent/search convention, singleton projected bound, root-contained P, and a singleton feasible-extension hypothesis in the no-incumbent variant. All are now explicit and have been verified. They directly yield the at-most-2n+1 class cover, because every one-sided class and the singleton have bound at least U-epsilon>=OPT-epsilon. C1 is expressly sufficient and does not characterize all small trees. The two-class quadratic example correctly has n+1 variable leaves and 2n+1 nodes. |

A parallel read-only proof check reviewed the complete Haar-CVP appendix, with
an additional independent check of the sphere-cover lemma. It found no
surviving mathematical defect. This report's reviewer separately checked those
arguments and retains responsibility for the final saved-version disposition.

## Findings and resolution record

| ID | Initial defect / request | Resolution at final review |
|---|---|---|
| LATTICE-PATH-1 | A generic projected phi may underestimate at integer x^circ. C1 alone did not certify its singleton; P was not explicitly restricted to the root box; phi(x^circ)=OPT did not guarantee an arbitrary relaxation optimizer supplied an original feasible incumbent. | Resolved and verified: author added phi(x^circ)>=U-epsilon, reset P to the root integer box, made incumbent availability explicit at every processed node including the singleton, and required singleton processing to obtain a feasible optimal extension in the best-bound no-incumbent variant. |
| LATTICE-COUNT-2 | Counting bound allowed empty S (0/0) or nonempty S with zero admissible occupancy. | Repaired by nonempty S with positive denominator and an explicit no-cover statement for zero occupancy. |
| LATTICE-REMOVAL-3 | The one-node tightening example on all of R removed two nonmergeable integer tails while describing one tail. Its asserted retained singleton also needs cutoff UB rather than UB-epsilon. | Resolved and verified: bounded root [0,1], P={0,1}, closed cutoff UB=0.16, and one upper-bound removal of integer point 1. |
| LATTICE-TYPO-4 | The block-optimality display used literal pi instead of the LaTeX command for pi. | Resolved and verified. |
| LATTICE-SOURCE-5 | Standard external inputs need actual attribution and exact hypotheses: maximal lattice-free polyhedron theorem and Siegel mean theorem. | Resolved: exact inputs are stated, the maximal lattice-free theorem cites Basu et al. (2010), Theorem 2, and Siegel's normalized formula cites Skenderi (2021), Theorem 3.2 and Remark 3.3. Keys and locators match the supplied Luna evidence; the original Siegel 1945 paper is not represented as directly inspected. |
| LATTICE-SCOPE-6 | Midpoint-clique proposition implicitly reused delta, q, and tau introduced locally in the preceding theorem. | Resolved and verified: proposition explicitly states its model, delta in (0,0.1), nonnegative tolerance, q=epsilon/g_n^2, and tau=OPT-epsilon. Formulas and proof are unchanged. |
| LATTICE-ATTRIBUTION-7 | The earlier joint citation could present Kaibel--Weltge's hiding-set formulation lower bound as a branch-and-bound tree-size mechanism. | Resolved and verified in the final attribution refresh: only Dey et al. supports the B&B mechanism sentence; Kaibel--Weltge receives a separate related-formulation sentence, matching the supplied literature ledger. |

The source-note close-pair dependence pitfall was sent to the author before the
appendix was completed. The saved appendix already uses the correct
unconditional close-pair surrogate, so it is not a surviving manuscript defect.

The author also reported two targeted TeX build presentation repairs: the C1
display's `split` environment was replaced with `aligned`, and the radical
argument for the OPT operator was braced. The affected expressions were
reread; their mathematics is unchanged. This reviewer did not run those builds
and does not report their results as independently performed checks.

## Readability and limitations

The chapter explains its projected relaxation and required integer points
before defining the benchmark. It distinguishes semantic certificate size,
permitted disjunctions, removal pieces, processed nodes, and construction or
checking costs. Main statements are followed by mechanism explanations, while
long complete proofs remain in the appendix. The random-lattice model is
separated from Gaussian-basis and finite experimental observations. The gadget
does not imply a universal algorithmic lower bound. The reviewed chapter is
clear for expert readers after the verified repairs and source attribution;
no claim of journal acceptance is made.

## Versions reviewed and targeted verification

The final mathematical claim set excludes the optional external general-split
hard instance and Kabatiansky--Levenshtein midpoint upper exponent. Root and the
author confirmed that no optional theorem additions were planned after this
review. Complete selected Jeroslow and gadget proofs are included.

| Finished source file | SHA-256 |
|---|---|
| `sections/lattice.tex` | `6f2a698fc11be69addf3d526f3b8c15976a6384ae23778bdff686a1cd68c667c` |
| `appendices/lattice-proofs.tex` | `8e3ffdb2e4c16eca503e950c4ff22e45c8068fb9b20c597dc9a47dd6a7ae7221` |

The hashes were computed from the saved files after the author's finished
notice on 2026-10-06. They include the C1/removal/counting/scope repairs, the
presentation repairs, and the two essential standard-theorem citations.
The section hash was refreshed after the final attribution-only edit on
2026-10-06; its previously accepted hash was
`b067147113f270916292a3ec4599dc178305efdf678747d40de8bb98dee5631e`.
The appendix hash is unchanged.

Read context: `BRIEF.md`, `AUTHORING-CONVENTIONS.md`,
`ARCHITECTURE-DECISION.md`, `ISSUES.md`, the lattice portion of
`AUDIT-DISCRETE.md`, `COVERAGE-FINAL.md`, `INCOMING-AUDITS.md`, and
`LITERATURE-KEYS.md`. Mathematical source reads included the relevant portions
of `research-20260928b/bb-complexity/integer-core/relaxation-intrinsic-bounds.md`
and `research-20260928b/reviews/integer-core-recheck.md`. The final standard-input
citations were checked against the Luna-supplied lane-8 evidence at
`/tmp/lit-bb-complexity.wGZhQj/round-2/lane-8.jsonl`: Basu et al. Theorem 2
states the full-dimensional maximal lattice-free structure, with the
2^dim(P) facet bound recorded on its second PDF page; Skenderi Theorem 3.2
gives the canonical Haar probability, nonzero-vector sum, and nonnegative
Borel L1 test-function normalization, with Remark 3.3 explaining the
extension from the original test class. The shared `LITERATURE.md` was not
present during the original review, but its completed integer comparison was
read for the final attribution refresh. No metadata-only source was independently browsed or
silently treated as this reviewer's primary-text inspection.

Commands actually used were targeted `rg --files`, `rg -n`, `cat`, `sed -n`,
and `nl -ba` reads of those files, and `apply_patch` for this report. The
finished-version checks included these exact local commands:

```text
nl -ba sections/lattice.tex
nl -ba appendices/lattice-proofs.tex
sha256sum sections/lattice.tex appendices/lattice-proofs.tex
sed -n '211,225p' appendices/lattice-proofs.tex
sed -n '243,260p' appendices/lattice-proofs.tex
sed -n '385,417p' references.bib
rg -n "Siegel|Skenderi|Basu|Maximal|Theorem 2|Theorem 3.2|Remark 3.3|maximal" /tmp/lit-bb-complexity.wGZhQj/round-2/lane-8.jsonl
```

The narrow attribution refresh used these additional targeted reads and the
same two-file hash command:

```text
rg -n "Kaibel|Weltge|Dey|hiding|integer|branch-and-bound" evidence/LITERATURE.md
sed -n '238,267p' evidence/LITERATURE.md
sed -n '98,125p' sections/lattice.tex
sha256sum sections/lattice.tex appendices/lattice-proofs.tex
```

No experiments, archived scripts, solvers, builds, project-wide checks, or CI
queries were run by this reviewer. Mathematical checking consisted of manual
proof reconstruction and the independent read-only cross-check described above.
