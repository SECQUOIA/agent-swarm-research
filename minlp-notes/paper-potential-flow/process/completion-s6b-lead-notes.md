# Stage 6b lead audit notes

Internal lead record; keep from independent reviewers until their reports are submitted.

The author is preparing a focused main narrative, principal results/proof ideas, model and output contracts, comparison tables, worked examples and original TikZ diagrams. All accepted technical sections01–11 will remain byte-identical and be included after an appendix break. This is a sound way to improve reading order without disturbing the accepted proofs. Anonymous manuscript, no fictional metadata or external submission. A standalone archive must preserve relative paths and compile/run saved exact checks from a temporary extraction outside the repository.

## Fresh corpus audit

The lead compared the complete main/worktree inventories:43promoted results,173potential-flow notes,73Python modules, and the full308-file direct dependency inventory. Every file exists in both trees and is byte-identical. No newer development needs import. The machine-readable record is `completion-s6b-lead-corpus.json`, including11direct dependencies outside the potential-flow filename pattern. Coverage must map the mathematical developments, distinguish auxiliary diagnostics and historical reviews, and state why unrelated AC-power-flow material is only context.

The legacy `verification/check_coverage.py` hardcodes the obsolete A00–A08 scaffold and deleted07-open-problems source. The author is authorized to update its A assumptions or provide a simple clearly documented A-only replacement. Paper B sources remain untouched. No two-paper build CLI should be used.

## Claims to check against full technical statements

- Exact threshold/value comparison, rational additive interval, rational original optimizing parameters, and possibly irrational physical states are different outputs. Exact scenario recovery can be easy while exact scalar comparison remains SRS-hard.
- Fixed rank per block, fixed global rank, fixed support and nomination dimension are distinct. An N^O(r) algorithm is not automatically FPT. The unrestricted nomination dimension already causes weighted-potential hardness on trees.
- Independent coefficient boxes/finite choices differ from within-cycle polytopes and global correlated polytopes. Global correlation can make a cactus flow region curved and nonconvex; this does not contradict the independent-interval cactus convex-region theorem.
- Coordinatewise extrema and universal robust capacity validation differ from existential simultaneous feasibility and full attainable-region convexity. Safe finite-to-interval objective hulls do not solve discrete flow realization.
- Fixed-law polynomial and uncertain quadratic cases must not be conflated in the scalar higher-block extension. Dense degree can grow where proved; fixed rational exponent families do not cover arbitrary binary-encoded exponents.
- The weighted O(rp) face reduction and scalar higher-block compiler are complete. Only the precisely stated several-parameter unrestricted higher-block sum remains an external extension. Do not inherit stale unresolved status from old notes.
- Closed operating filters can require algebraic scenarios, and exact feasible rational coefficients can fail on ordinary capacity instances. Conditional strict-margin rational recovery must remain conditional. By contrast, the independent cactus design theorems do supply original rational profiles even when their physical flows are algebraic.
- Global resistance-polytope dissipation MAX is the proved concave-maximization/convex-optimization case; dissipation MIN has the separate strong hardness. Classical concavity and cubic duality are credited, not claimed new. Do not import conductance-investment results into arbitrary resistance polytopes.
- S6a sharpness is over a conserved quadratic error set; exact endpoint compatibility proves scenario optimality, not rational physical state/value. The original-instance pipeline is narrower than the generic exact verifier and does not implement every abstract accuracy-bit algorithm.

## Prior-work safeguards

The official2026overview was freshly downloaded and is identical to the local original; printedp10 still raises cactus MPD complexity. State the additive resolution and restricted exact SRS equivalence precisely, not a complete exact classification of arbitrary cactus nominations. Prior switches/installed arcs/conductance costs are different models. Hasler–Wang1993 remains unread; no unrestricted first envelope/endpoint claim. Classical energy, electrical confluence, convex duality, real algebraic computation, approximation and zonotope methods require credit. Source locators and caution about Klimm2026Thm13 are in the literature screen and earlier lead notes; the author has been explicitly told not to cite its unverified hardness proof as established.

No stage6b acceptance or reviewer dispatch has occurred yet. The author must finish and freeze before five independent reviewers are dispatched. Stage7 remains a separate mandatory full-manuscript cycle.

## Lead full main-narrative audit before author freeze

Read the actual abstract, full introduction, all six narrative files, conclusion, main and macros. Checked main theorem/table scopes against the accepted technical statements, including finite rank-three NP membership, single-cycle weighted NP membership, fixed global rank, continuous-law envelopes and the correlated hardness absolute gap. No change to an accepted technical theorem is proposed. Required two wording repairs: the introductory block localization concerns only free nominations; the integrated envelope verifier accepts curvature witnesses rather than the separate support-dual format. Requested explicit separation of disconnected deterministic verification from the connected numerical/envelope implementation, bibliographic identification of the unavailable Hasler–Wang source, and narrow supported originality wording. The author reports the first repairs complete; final frozen text remains to be checked.

Read all standalone README, build wrapper, replay and package scripts. Extracted archive build and both replay modes remain required at author freeze and independent review. Read current contribution/literature synthesis. The lead audit is not a substitute for either the stage five-reviewer gate or the whole-manuscript five-reviewer gate.

## Frozen-stage lead audit additions

Verified every43 frozen stage file,23 manuscript input,63 archive payload and archive/PDF hash. Independently extracted the final archive outside the checkout; complete A-only build and all18 exact replay commands passed. Rechecked every distributed payload hash after execution: unchanged. Retained in completion-s6b-lead-checks.json. Rendered and read pages1,9,11,15,16,37,41; diagrams/table/contents/appendix transition are readable.

Read fresh official Dagstuhl Ajdarow et al. ICALP2025 metadata and original HTML introduction and Section5 lower-bounds paragraph (DOI10.4230/LIPIcs.ICALP.2025.138). The source explicitly retains open polynomial-time/NP status for SRS, supporting the narrow new status citation; no broader theorem comparison used.

Lead finding L1 (minor, to consolidate after all five reports): main Theorem5.1, narrative/04-weighted.tex lines19–22, says fixed positive asymmetric quadratic laws, omitting rational coefficients that are explicit in technical TheoremG.1 and the corresponding J results. Add positive rational fixed coefficients; make c in Q^V explicit instead of the grammatically ambiguous “with rational 1^T c=0.” This preserves the intended proved binary-input model and does not change a proof or algorithm. No edit during reviewer freeze.

Lead finding L2 (minor notation clarification): narrative04 lines82–83 use O(rp) and n^{O(rp)} for the weighted face theorem without locally redefining r, while Model2 and the immediately preceding global-rank comparison use r for total rank. Technical G.2 explicitly fixes a positive bound r>=1 on maximum block rank. State a local r0>=max{1,r_max} and use O(r0 p), also align the introduction phrasing, so trees and per-block versus global rank are unambiguous. Figure2 uses O(r_B) for a selected block; if its scope stays general, qualify that it depicts a cyclic selected block and that bridge cases are handled directly, as AppendixC explicitly does. No mathematical change is needed.

Lead finding L3 (minor model hypothesis): narrative01 balanced-box display states only ell,u in Q^V, then nonemptiness iff sum ell<=0<=sum u. Explicitly add ell<=u coordinatewise. Without it ell=(1,-1),u=(0,0) satisfies both sum tests but defines an empty set. Technical preliminaries already use valid intervals and algorithmic results require nonempty boxes; this is a main-definition omission, not a failed optimization theorem.

Related minor model convention: main rank definition should set the empty maximum to zero for the one-vertex graph, matching technical preliminaries lines385–389. The main model explicitly includes the one-vertex case. Add the same short convention alongside the rank definitions.

## Full independent reports read by lead

R5 read in full (tool returned4804tokens, untruncated), SHA256 f579f974c990f7319b3f1889a0cf11e33d7cab8c303af2151e6dae7855b01e7e. No major findings. R5-1 agrees with lead L3, valid minor ordered-bound omission. R5-2 valid minor stale coverage wording: fixed-core row still planned; historical18-section checker count lacks current13 included; “A05,no appendix” obsolete. Lead inspected actual locations and accepted technical usage. Optional single-reference final bibliography page and theorem page breaks are layout preferences, not required defects; rendered pages readable. All build/exact18/numerical28/repackage/source/PaperB/literature integrity evidence documented. Remaining four reports pending.

R3 read in full (4491tokens, untruncated), SHA256 dad2204f33487f8868f8202e30dfcd720eb0503adfd08cebf3af59accf09f211. No major findings. R3-m1 valid minor: root reread actual sharper sensitivity proof at AppendixI lines680–770; it regularizes, differentiates, integrates and passes to limit, unlike the preceding finite circulation estimate. Main narrative05 proof description must say regularized electrical sensitivity and limiting argument. R3-m2 duplicates valid stale fixed-core coverage description. All exact18/scientific28/repackage/build/source integrity evidence recorded. Reports R1,R2,R4 remain pending.

R1 read in full (5754tokens, untruncated), SHA256 14281d21c3128ee15ebf549f4ae99b4504746675331d186df4b8ef86ba2bc0c6. No major findings. R1-1 duplicates valid ordered-bound main-model omission. Extensive original primary/source/package/integrity checks reported; no further required findings.

R2 read in full (5021tokens, untruncated), SHA256 1194789b7d438e198eb956e6f175bc7366e51f794b6082be0c52d6d6c1c6ef22. No major findings. R2-1 duplicates lead L2, valid positive per-block rank convention. Root verified the supplied path counterexample exactly: w=(-1,1), x=(t,t-1), W=-t^2-(1-t)^2, unique interior max t=1/2 at global rank0. R2-2 duplicates valid stale fixed-core coverage row. All standalone replays/build/packaging/integrity pass.

Four full reports now read: R1,R2,R3,R5. R4 remains pending; no corrections or acceptance before it finishes.

R4 read in full (5749tokens, untruncated), SHA256 a84b4903ab2c4aab6719a0cad8e9a91c3146b4b14c4188c3c7c5e39ac4bc5d26. Valid minor factual source-provenance notice: root independently checked exact originalINP header and hash. No legal conclusion/license-version inference adopted. All five full reports now read; complete adjudication written and separate /root/s6b_fix assigned. No major issue; final scientific review remains pending.
