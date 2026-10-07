# Lattice and admissible-class chapter

Owned files: `sections/lattice.tex`, `appendices/lattice-proofs.tex`, and this report. Both manuscript files are finished. Independent final review is accepted in `REVIEW-MANUSCRIPT-LATTICE-R1.md`, with no unresolved mathematical or readability issue and matching finished-file hashes. No other manuscript files or research sources were edited.

The chapter follows `BRIEF.md`, `AUTHORING-CONVENTIONS.md`, `ARCHITECTURE-DECISION.md`, `INCOMING-AUDITS.md`, `ISSUES.md`, the full class-number/source-map and scope portions of `AUDIT-DISCRETE.md`, and the integer map in `ARCHITECTURE.md`. The root decision supersedes the architecture's older proof-status and novelty summaries. The primary mathematical source is `research-20260928b/bb-complexity/integer-core/relaxation-intrinsic-bounds.md` (IC), with `research-20260928b/reviews/integer-core-recheck.md` and the corresponding original review read for relevant repairs.

## Claim, source, and manuscript proof map

| Result | Exact scope and cost | Source | Manuscript statement and proof |
|---|---|---|---|
| Projected relaxation and required integer set | Fixed proper convex extended-real projected value function; P records preserved integer points, separately from feasible F | IC Section 1.1, Definitions 1.1–1.2, Lemma 1.3 | `lattice:projection`, `lattice:tree-definition`; completed-run argument immediately after definition |
| Admissible class lower bound | Every P-covering convex-piece tau certificate has at least kappa_tau(P) leaves; counts leaves rather than solves | IC Definition 1.4, Lemma 1.5, Theorem 1.6 | `lattice:class-definition`, `lattice:graph-bound`, `lattice:count-bound`, `lattice:class-number`; main-text lower-bound proof |
| Exact semantic attainment | Finite nonzero class number; arbitrary convex sets, possibly nonclosed; root may be any convex set containing P; internal children cover only P intersect parent | IC Lemma 1.7a and Theorem 1.7 | `lattice:class-number`, `lattice:hemispace`; complete proof `app:lattice:semantic` |
| Finite-P polyhedral certificate | Replace each node S by conv(S intersect P); preserves P-points, coverage, and bounds; no efficient construction/checking claim | IC Theorem 1.7(c)(i), recheck Section 1 | Final paragraph of attainment proof, `app:lattice:semantic`; explicit main-text cost caveat |
| Cuts and feasibility reductions | P-valid convex integer-space cuts preserve the original leaf lower bound; cuts valid only for feasible points preserve kappa(F), not automatically kappa(P) | IC Theorem 1.8(a,b) | `lattice:operations`; `app:lattice:operations` |
| Incumbent removals | Current-set-certified convex removals give kappa<=L+S; one pass at each node yields /(2n+1), binary iterated rounded fixing yields /(n+1) | IC Theorem 1.8(c), recheck Section 4 | `lattice:removal-hypothesis`, `lattice:augmented-count`, `lattice:operations`; complete chain/drop-empty-leaf proof |
| Integer boundary accounting | Rounded lower removal ends at ell'-1, retained domain starts at ell'; no shared retained integer boundary | IC examples after Theorem 1.8; audit integer-boundary finding | OBBT paragraph following `lattice:operations` |
| Pure ILP versus projected MILP descriptions | Pure ILP kappa<=m+1, infeasible <=m; rational projected sublevel q-row description gives <=max(q,1) | IC Proposition 2.1 | `lattice:linear`, complete main proof |
| Compact MILP with 2^n classes | l1 objective represented with 2n rows; eps<1/2; every binary pair conflicts, sign halfspaces attain | IC Example 2.1a, recheck Section 2 | Example following `lattice:linear`, complete main proof |
| Quadratic variable-branching separation | Odd-n parity quadratic on binaries; eps<1/4; kappa=2, three-node sum split, exact binomial leaf count for proper free-variable branching | IC Proposition 2.4 | `lattice:jeroslow`, complete main proof |
| Lattice-free facet interpretation | Finite convex phi on R^n; nonempty open strict sublevel; class number equals enclosing lattice-free facet number | IC Theorem 2.2(a) | `lattice:facet-number`; `app:lattice:facets`; standard maximal lattice-free polyhedron theorem stated as external input |
| Haar moments and scale estimates | Haar unimodular L and uniform torus target; n>=2; E count=V and Var count=V | IC Lemmas 3.1–3.3 | `lattice:siegel` (named standard external input), `lattice:unfolding`, `lattice:moments`, scale estimates in `app:lattice:cvp-proof` |
| Deterministic cap occupancy | tau>0, R²<=tau+lambda1²/2; at most n+1 class points in open ball | IC Theorem 3.5 proof | `lattice:cap`, `app:lattice:cap-proof`; self-contained nearest-hull-point and affine-dependence proof |
| Haar class lower bound | Explicit q=eps/g_n² and delta; R_-²=1.5(1-delta)²-q>1; all bases, all P-covering convex-piece trees | IC Theorem 3.5, sharpened direct tolerance bookkeeping | `lattice:cvp`, `lattice:cvp-lower`; full proof |
| Haar class upper bound | Explicit near/far halfspace cover; fixed-q upper exponent .5 log2(2-q); certificate existence, not split-tree algorithm | IC Proposition 3.6(b), corrected/refined angular choice | `lattice:cvp-upper`, `lattice:cvp-exponents`, `lattice:sphere-cover`; full new tolerance-dependent proof |
| Haar midpoint clique lower bound | rho<4/3, rho[(1-delta)²-q]>1; unconditional close-pair count with event-only domination of nonconflicts | IC Theorem 3.4, recheck algebra | `lattice:cvp-clique`, `app:lattice:clique-proof`; complete moment/integral/deletion proof |
| Curvature versus exact block hull | Orthogonal two-feature blocks; global diminishing-return inequality and sum Delta+eps<min deficit; unique optimum when all Delta>0 | IC Theorem 4.4 and Theorem 4.3 proof | `lattice:curvature-gadget`; complete proof `app:lattice:gadget` |
| Uniform rational unique-optimum family | Fixed lambda1, u=(1,0), v=(3/5,4/5); response scales and perturbations with polynomial denominators; fixed eps range | `AUDIT-DISCRETE.md`, final optional completion | `lattice:rational-family`; full continuity and sum-gap proof |
| C1 one-path criterion | Root box P reset; known feasible incumbent; singleton projected tightness at threshold; proper branches; strict-best-bound variant additionally recovers original feasible optimum at singleton | IC Lemma 5.1, Proposition 5.2; tightened generic-relaxation assumptions from fresh review | `lattice:C1`, `lattice:path`, complete main proof and probing/count comparison |

## Mathematical repairs and fresh developments

The written model permits only integer coverage at internal nodes. The final two leaves of the hemispace chain cover the remaining required integer points, not necessarily all remaining fractional points. Children are intersected with their parent, so their nesting and convexity are explicit. The root is allowed to vary; the kappa=1 case uses a class-enclosing root, and the fixed-continuous-root caveat is explicit. No efficient constructive tree algorithm or polynomial checking cost is asserted.

The hemispace proof includes the weak-separation boundary case and the induction on the boundary hyperplane. It does not assume a strict hyperplane separator exists for arbitrary nonclosed convex sets. The finite-P hull replacement is shown to preserve every node's P-points exactly.

Removal chains are built only after normalizing node sets to their effective sets. Feasible-point cuts preserve the F bound; the chapter does not claim invariance of a larger P after deletion of infeasible integer points. Binary tightening counts only genuine rounded removals of remaining binary values. The emptying removal replaces the run's empty retained leaf. General iterated integer tightening counts actual bound changes and retains the possible final +1 emptying change in the width estimate.

The exact Jeroslow count uses branches that fix a free binary variable to 0 or 1, avoiding the source's looser wording about not repeating a fixed variable.

The class-cap proof minimizes norm over the finite near-subset's compact hull, avoiding any unnecessary global-hull attainment assumption. Strict negativity comes from the open outer ball. The obtuse-vector cardinality proof uses an affine dependence of n+2 vectors.

The Haar midpoint proof defines an unconditional close-pair surrogate M and computes its mean through unfolding/Siegel. On the good optimal-radius event, this surrogate dominates all nonconflicting pairs. This avoids a hidden conditional-moment assumption in the source's phrasing.

Fresh read-only subagent checks independently confirmed the semantic/operation/Jeroslow proofs and the Haar cap/moment/clique/covering calculations. The Haar checker found a correction to IC Conjecture 3.7: for fixed positive q=eps/g_n², the same covering method gives upper exponent .5 log2(2-q)<.5. The source's fixed-q exponent-.5 conjecture is therefore excluded. The manuscript gives the complete corrected tolerance-dependent upper proof, with lower .5 log2(1.5-q) for q<.5. Its vanishing-q exponents remain .29248 lower and .5 upper. The supporting agent reconstructed all steps without browsing or experiments.

Independent final reviewer `review_lattice_final` identified two generic-relaxation C1 edge cases, now repaired: projected tightness is required at the known incumbent for singleton pruning, and the no-initial-incumbent variant explicitly assumes that singleton processing recovers a feasible optimal continuous extension. The subsection resets P to the root box's integer points. The occupancy quotient also now states its nonempty-positive-denominator condition, with zero occupancy implying infinite class number.

The known-incumbent C1 hypothesis now says U is available whenever a node is processed, including the singleton. The reviewer reread and approved this precision. The tightening counterexample also uses the bounded binary root [0,1], P={0,1}, and closed incumbent cutoff UB=.16, so there is exactly one removed integer point.

## Literature and contribution boundaries

Used stable literature keys supplied by Luna: `deyDubeyMolinaro2023BranchAndBoundLowerBounds` and `kaibelWeltge2015LowerBoundsBranchAndBound`, restricted to midpoint/hiding-set and leaf-occupancy mechanisms. The class-number framework extends those mechanisms from pairwise witnesses to convex-hull admissibility and identifies the exact minimum in a specified semantic tree class. No unrestricted novelty claim is made.

Both named standard inputs now have Luna-verified citations. The full-dimensional maximal lattice-free polyhedron/facet theorem cites `basuConfortiCornuejolsZambelli2010MaximalLatticeFree`: author PDF Theorem 2 p.2, proof pp.8–9, facet bound at most 2^n. The normalized Siegel identity cites `skenderi2021RandomLatticesSiegel`: dissertation Theorem 3.2 p.10, Haar probability, n>=2, all nonzero lattice vectors, nonnegative Borel L1 tests, and no zeta factor; Remark 3.3 supplies the extension of the original Riemann-integrable test class. They are stated explicitly as inputs; the chapter does not purport to prove either standard theorem from its elementary calculations. The original Siegel1945 remains metadata-only and is not represented as inspected. The elementary parity quadratic proof stands on its own, with no claim to have directly inspected the historical Jeroslow original.

Root approved the complete core scope and explicitly excluded three optional original-note topics from this chapter: the Gläser–Pfetsch hard general-split separation, the Kabatiansky–Levenshtein .261241 midpoint upper exponent, and the Reis–Rothvoss-based fixed-dimension split-tree estimate. Their omission is recorded rather than replaced by a guessed citation. The supplied `glaserPfetsch2024SmallDisjunctionTrees` key is a different work from the hard general-split source, arXiv:2308.04320, and has not been substituted. The full class lower bound, Jeroslow variable/split distinction, Haar class/clique lower estimates, stronger-block relaxation separation, and C1 easy criterion do not depend on those exclusions. No optional theorem additions are planned.

## Targeted verification

No experiments were rerun. No literature searches, project-wide checks, CI inspection, commits, or LaTeX builds were performed by this author. Root owns targeted standalone compilation after integration. Verification here consisted of source reads, independent proof reconstruction, read-only supporting proof checks, and a targeted label/reference scan of the two owned TeX files. A small `python3` static parser found 51 unique labels, no missing owned references, and matching environment counts in each file (40/40 and 45/45); it did not run an experiment. Other commands actually run: `pwd`, `rg --files`/`rg -n` on the assigned sources and manuscript evidence, `cat`, `sed -n`, and `apply_patch` to the owned files. These are local author checks, not CI results.

Root's integrated local LaTeX builds reported two typesetting failures in the owned files, both repaired: the C1 display's multiple alignment pairs now use `aligned` instead of `split`, and the sole operator-macro radical now uses `\sqrt{\OPT}`. A targeted `rg` confirmed that all other unbraced radical arguments are ordinary tau symbols. These repairs do not change mathematical claims. Root owns the eventual compilation result; the static source checks above are not represented as a successful build.

After adding the verified citations, a final targeted `python3` reference/key check found 51 unique owned labels, no missing owned references, and all four cited keys present in `references.bib`. `sha256sum` pinned the finished TeX files below. No further TeX edits are planned.

## Concrete remaining integration requests

1. Root retains integrated standalone compilation and final source-package checks. There are no new global macros or bibliography requests.
2. Regression/BLS chapters may cite `lattice:class-number`, `lattice:operations`, `lattice:path`, and `lattice:C1`; the deterministic gadget is owned here as `lattice:curvature-gadget`.
The independent review is closed and accepted for the hashes below. It checked the complete fixed-tolerance correction, all mathematical repairs, the final typesetting corrections, and the citation-only edits against supplied Luna evidence. There are no outstanding author or mathematical-review requests.

Finished TeX SHA-256 hashes:

- `sections/lattice.tex`: `b067147113f270916292a3ec4599dc178305efdf678747d40de8bb98dee5631e`.
- `appendices/lattice-proofs.tex`: `8e3ffdb2e4c16eca503e950c4ff22e45c8068fb9b20c597dc9a47dd6a7ae7221`.
