# S5a lead audit notes

Internal lead notes, not an independent reviewer brief. Do not provide these findings to the five stage reviewers before their independent reports.

## Mathematics read before author freeze

The lead read the abstract monotone polynomial-root theorem in full, the correlated-cycle resistance theorem, the correlated polynomial-law theorem, the dense convex-polynomial extension, both convex-maximization results, and the associated source assessments. The central contracts are consistent: fixed-breakpoint dense laws, uniform strict-passivity promises, exact local algebraic values with rational original profiles, and additive sums without a common growing algebraic field. The exact root theorem's uniform separation argument applies across all vertex-piece polynomials; the final rational LP must return a vertex, and successive coordinate minimization stays on faces of the original polytope, preserving its common bit bound.

The stronger few-measurement result for independent polynomial-law cycle polytopes appears to follow from the same rational directions and exact endpoint witnesses. The author is assessing it and will flag it as a new extension for explicit review. Its finite-set clause must remain separate; exact capacity clipping is not freely available for finite coefficient choices.

## Direct primary-source checks

- Agrawal and Boyd, *Disciplined quasiconvex programming* (2020): read sections 2.1, 2.3, and 3, including the quasilinear convex-combination inequalities and the bracketed feasibility-bisection method. These are established antecedents, not the exact polynomial-root vertex-recovery statement. [Author-hosted published PDF](https://web.stanford.edu/~boyd/papers/pdf/dqcp.pdf).
- Megiddo (1979): read the complete section 2 theorem and proof, PDF pages 2–4, printed pages 415–417. Its exact ratio optimization theorem uses an addition/comparison algorithm and parametric simulation; it cannot be invoked for an arbitrary bit-polynomial LP implementation without checking those hypotheses. The current separation-and-bisection proof supplies its own arithmetic argument. [Author copy](https://theory.stanford.edu/~megiddo/pdf/rational.pdf).
- Onn and Rothblum: read the local original PDF pages 4–6 and 8, including Lemmas 2.1–2.4, Algorithm 2.5, Theorem 2.6, and the explicit distinction between rational oracle time and the real-data variant. The normal-fan/zonotope mechanism is classical. Separately refined algebraic endpoint lengths and rational original-network witnesses are the application-specific implementation requirements.
- Aßmann et al.: read local original PDF pages 20–22, especially Proposition 4.9, Lemma 4.10, and Proposition 4.11. Their scalar cycle inequality conversion and preservation of polyhedral parameter domains directly precede the quadratic capacity LP. The manuscript must credit this explicitly.
- Mignotte's factor bound was checked in the primary research article *A new bound on cofactors of sparse polynomials*, Theorem 1.2, which attributes the inequality to Mignotte's 1974 Theorem 2. The original 1974 proof has not been read in this pass. [Exact displayed theorem](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/new-bound-on-cofactors-of-sparse-polynomials/2CADDB77D2E5CBFB7B803CCCAC49D2FD).

A fresh bounded search for monotone polynomial-root polytope optimization and convex cactus resistance design did not reveal a matching combined theorem. This is not evidence of exhaustive priority. A fresh CiteSeer retrieval of the Ferrez–Fukuda–Liebling manuscript timed out. Fukuda's primary publication list confirms the 2005 EJOR record; it links to the publisher. This pass does not claim to have read its full paper. The detailed geometric comparison can rely on Onn–Rothblum's inspected full proof.

## Current-draft proof audit

The lead read the full 743-line draft before its final validation pass. The uniform root separation, exact target interpolation, global-capacity LP directions, stored-endpoint surrogate bounds, perspective extension, Max-Cut realization, and new polynomial-law measurement extension were checked directly. One minor output-contract omission was sent to the author before freeze: the independent-cycle and measurement theorems must explicitly reject infeasible capacity filters before promising optimizing scenarios. Their proofs already supply the emptiness decision. No other mathematical issue was found in this pass. Final frozen changes and validation still require inspection.

The lead subsequently inspected every final source correction, including the infeasibility statements and grammar, and the new diagnostic's explicitly defined second passive cycle. All 15 build-input hashes and all nine check-script hashes match their successful manifests. The complete author report and check outputs were read. Frozen section SHA-256 is `85ea7d7942ab63a9a94d4a91dd10b9e3b30b736982a4f58c6a2af52007807295`.

## Review-stage source improvement

Reviewers r3 and r4 independently located a readable Ferrez–Fukuda–Liebling author manuscript. The lead checked its title-page revision date, April 29, 2004, and read Section 3, PDF pages 4–6, including the fixed-rank factorization setting, zonotope reduction, Theorems 3.1–3.2, Corollary 3.3, and arrangement duality. It explicitly credits the earlier Allemand et al. result. Thus the fixed-rank mechanism has now been checked beyond an abstract. The final bibliography should link this version and replace the stale access-gap comment. [Author manuscript](https://www.cs.mcgill.ca/~fukuda/download/paper/qpzono040429.pdf).
