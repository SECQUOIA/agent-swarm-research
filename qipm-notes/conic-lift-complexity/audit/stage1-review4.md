# Stage 1 independent review 4

Scope: complete current `main.tex`, both included section files, bibliography, and `audit/source-map.md`. I did not read other review reports. Main emphasis: novelty and literature, scope and coverage, and an independent mathematical reading.

## Verdict

**No major issue found in the completed Stage 1 mathematics.** The proof chain from whole-slice certificates to regular minimum-rank selectors, complementary Peirce channels, and the all-simple-cone attaining lift is coherent. I recommend proceeding after the minor corrections below. This verdict does not certify the later candidate results listed in the plan.

## Minor corrections

1. **State the main theorem's exclusions in the abstract.** `main.tex`, sentence beginning “For a fixed repeatable dictionary”: the asserted formula currently appears to include the interval and a dictionary of rays. The actual theorem assumes `s >= 2` and positive capacity `B`, and the final paragraph explicitly establishes that the interval has frontier one rather than zero. Remedy: say “For `s >= 2` and a finite repeatable dictionary containing a non-ray simple symmetric cone ...”. This is an abstract-scope correction; it does not affect the proved theorem.

2. **Make the polar degree comparator precise.** `sections/01-foundations.tex:28–29` describes Fawzi–Safey El Din only as “Algebraic-boundary degree supplies another kind of lower bound”. Their Theorem 1 specifically uses the least degree of a nonzero polynomial vanishing on the **polar boundary** and obtains `rank_psd(C) >= sqrt(log_2 d)`. Their Section 5 also gives a product-block count consequence. Remedy: add “of the polar body” and, if expanding the comparison, distinguish their degree-based product-block bound from this manuscript's local curvature bound. Local source: `literature/papers/fawzi2018-a-lower-bound-on-the/paper.md`, verified-findings entries for Theorem 1 and pp. 8–9; primary source https://arxiv.org/abs/1705.06996. The present wording is broad rather than false, so this is minor.

3. **Clarify the numerical resources in the introduction before the abstract resource language grows.** `sections/01-foundations.tex:2–7` speaks of number and size of factors, rank certificates, and barrier parameters without stating which resource the first theorem optimizes. Add a short sentence distinguishing (i) factor count under a dimension cap; (ii) total ambient Jordan rank; (iii) support-wise minimum certificate rank; and (iv) the standard barrier after restriction. Later portions already distinguish these correctly. This will prevent readers from importing a cone-count interpretation into the rank frontier, especially since Fawzi–Parrilo uses a different resource. A compact theorem table can be deferred to the planned final introduction.

## Mathematical checks performed

- Free-variable elimination: the kernel of the equality projection must have zero output because it generates an entire feasible line; consequently the output descends to cone coordinates. The minimal-face reduction then produces relative Slater feasibility. The dual multiplier signs in the whole-slice certificate identity are correct.
- The minimum rank exists without compactness because feasible total ranks are integers in a finite set. Semialgebraic choice can select minimum rank even when minimum-norm choice does not do so. The dense-open regular locus supports the required separate-variable differentiation.
- The universal `m-2` argument uses two-sided derivatives and the rank of the pairing between `b^perp` and `a^perp`; its kernel is exactly the line through `a`. A zero primal or dual point forces the associated two-sided derivative to vanish by pointedness.
- In the Jordan argument, only `V_ij` with `i` in primal support and `j` in dual support can pair; differentiating complementarity yields the positive Gram formula with coefficient `mu_j/lambda_i`. Zero ranks and non-strict complementarity cause no gap.
- The norm-tree count has exactly `s` leaves, factors of dimensions `b_i+2`, and total dimension `s-1+2k`. Its standard ambient rank is `2k`; the text correctly declines to identify that with the restricted barrier parameter.
- In the Peirce perspective, the trace normalization gives `t=||w||^2/2`, then `P(w)c=tk`, and the two-dimensional determinant is `delta z-||w||^2`. The quadratic representation proof avoids associative octonionic multiplication. The coefficient of the half-Peirce term in the rank-one completion and its tail trace are consistent.
- The attaining lift's whole-slice coefficient comparison forces a positive common tail trace at every non-north-pole support. Thus **all** certificates have at least one rank in every block, including supports where some groups vanish. At the exceptional pole a single positive primitive component supplies rank one. Extra half-Peirce components outside the coordinate groups do not invalidate the lower bound.
- The capacity per unit certificate rank `a(r-1)` is correctly distinguished from maximum local factor capacity `a floor(r^2/4)`. Minimal-face reduction cannot increase the former; rank-two Albert faces have the stated spin capacity.

## Literature and novelty assessment

The current precise and qualified novelty statement is supportable by the sources checked; none of these sources establishes this support-fiber minimax theorem. This is a targeted check, not proof of priority.

- Gouveia–Parrilo–Thomas, https://arxiv.org/abs/1111.3164 and DOI 10.1287/moor.1120.0575: proper lift/slack factorization and cone-family rank. The manuscript attributes these correctly and does not confuse their family rank with support-wise certificate rank.
- Fawzi–Parrilo, https://arxiv.org/abs/1311.2571: fixed-size PSD products, exponential factor counts for cut/correlation polytopes. The manuscript's one-sentence characterization matches the primary abstract and the repository's detailed source notes. It is an appropriate comparator, not evidence for the present formula.
- Fawzi–Safey El Din, https://arxiv.org/abs/1705.06996: polar algebraic degree, as described above.
- Kummer, https://arxiv.org/abs/1506.07699 and DOI 10.1137/15M1030789: direct spectrahedral descriptions of the ball; primary abstract gives `r >= n/2` and stronger special-dimensional results. The source-map correctly plans comparison and distinguishes direct spectrahedra from projected lifts. Include this comparison in the final literature synthesis, as already planned.
- The Gowda–Sznajder all-EJA Schur-complement source is particularly useful to support the exceptional-cone construction; the manuscript proves its specialized formulas rather than merely citing them.
- A fresh online search for combinations of conic lifts, curvature, Euclidean ball, certificate rank, and Lorentz-factor count located no prior statement matching the claimed exact invariant. The relevant 2026 La Piana–Müller-Hermes paper (DOI 10.1016/j.laa.2026.03.012) concerns positive maps factoring through Lorentz cones and operator-ideal norms, not the whole-slice certificate fiber objective. Its presence in the source ledger is sufficient at this stage; it need not be forced into the introduction.

One useful final-synthesis contextual comparison is Helton–Nie's positive-curvature **sufficient conditions for existence** of semidefinite lifts. Their subject is distinct from the present quantitative lower bounds. The primary survey at https://mathweb.ucsd.edu/~helton/BILLSPAPERSscanned/HNpreptA.pdf, Section 3, describes the curvature conditions. This is an optional contextual addition, not a missing prerequisite or a major novelty concern.

## Coverage plan assessment

The source map is appropriately exhaustive at the file level and explicitly marks source status as unverified. Its main distinctions are essential and correct: generic versus global selectors; whole-row versus selected-contact factorizations; restricted versus ambient barriers; and geometric movement versus query cost. Stage 3 honestly identifies the bounded narrow-cap divisible seam rather than treating a navigation note's “proved” status as authority.

The map is a prospective routing ledger, not yet a theorem-to-source coverage proof. At integration, replace each relevant source's prospective routing with a final disposition: theorem/corollary/appendix locator, subsumed result, or rejected/limited result with reason. This is already implicit in the ledger's stated policy and should be carried out before the final five-reviewer cycle. I found no Stage 1 coverage omission that needs to block the next stage.
