# Issues raised about the certified-support-cut work, and their status

This record collects every issue, criticism, request, open question, and
limitation that the internal reviews and completion records raised about the
material for the paper "Certified support cuts for shared nonlinear
expressions and quadratic blocks". For each issue it gives the file that
raised it, the resolution and where that resolution is recorded, the current
status, and what the journal paper must say or do.

It also lists a small number of **new** issues. No review raised them; they
were found while compiling this record and are marked `New`. Each new issue
names the local source or the check that supports it.

All reviews cited here are internal research-agent reviews. None is journal
peer review or formal verification, and the source reports themselves make no
publication-priority claim.

## Conventions

Path abbreviations (all relative to the repository root
`/workspace/minlp-notes`):

- `A/` = `research-20261002-convexification/` (Report A, October 2).
- `B/` = `research-20261003-convexification/` (Report B, October 3).
- `KB/` = `literature/papers/` (local literature knowledge base, read only).
- `notes/`, `results/`, `research-20260922/curve-hulls/` = earlier background.

Status labels:

| Label | Meaning |
| --- | --- |
| Resolved | Defect fixed, or text corrected, and the fix was rechecked by a reviewer. |
| Scoped | Resolved by narrowing the claim or stating a boundary. The limitation itself remains and must appear in the paper. |
| Partial | Some of the issue was addressed; a specific part remains. |
| Open | Not addressed in the source material. |
| New | Not raised in any reviewed file; identified while compiling this record. Always also open unless noted. |

Contribution IDs (C-SUP, C-BERN, ...) and novelty IDs (N1–N6) follow the
paper plan.

## Files read

Report A: `A/reviews/document-review.md`, `A/reviews/integration-review.md`,
`A/reviews/numerical-review.md`, `A/reviews/star-review.md`,
`A/theory/overlap-review.md`, `A/theory/star-audit.md`, `A/PROGRAM.md`,
`A/CLOSEOUT.md`, `A/VERIFICATION.md`, `A/document/COVERAGE.md`,
`A/document/VERIFICATION.md`. Also read because they record review findings
or limits: `A/literature/final-contribution-review.md`,
`A/literature/README.md`, `A/literature/star-overlap.md`,
`A/literature/composition-audit.md`, `A/experiments/experiment-audit.md`,
`A/experiments/README.md`, `A/numerics/contract.md` (limits section),
`A/theory/README.md` (sections 2–3), `A/document/main.tex` (support,
polygon, and limits sections).

Report B: `B/reviews/PLAN.md`, `B/reviews/document-review.md`,
`B/reviews/document-metrics-review.md`, `B/reviews/experiment-review.md`,
`B/reviews/integration-review.md`, `B/reviews/model-review.md`,
`B/reviews/row-rounding-review.md`, `B/reviews/separation-review.md`,
`B/theory/polytope-review.md`, `B/literature/row-proof-review.md`,
`B/literature/final-contribution-review.md`, `B/PROGRAM.md`,
`B/CLOSEOUT.md`, `B/VERIFICATION.md`, `B/document/COVERAGE.md`,
`B/document/VERIFICATION.md`. Also read: `B/literature/README.md`,
`B/literature/aggregation-prior.md`, `B/experiments/protocol.md`,
`B/experiments/post-freeze-changes.md`, `B/experiments/campaign-v2/results.md`,
`B/experiments/campaign-v2/coverage.md`,
`B/experiments/campaign-v2/environment.json`, limits sections of
`B/theory/separation.md`, `B/theory/row-aggregation.md`,
`B/numerics/model-contract.md`, `B/implementation/integration.md`, and
`B/document/{aggregation,foundations,frontier,literature,star,evidence,implementation}.tex`
where cited below.

Background: `notes/review-shared-variable-term-links.md`,
`notes/review-row-hull-theory.md`, `notes/review-composite-univariate-envelopes.md`,
`notes/review-row-hull-code-experiments.md` (verdict section),
`notes/review-minlp-developments-20260922.md` (the later corrective audit),
`research-20260922/curve-hulls/review.txt` and the corrections section of its
`report.md`, the status lines of `results/composite-univariate-envelopes.md`
and `results/shared-variable-term-links.md`, and the topic paragraphs of the
repository `README.md` (lines 8–22, 562–616, 883–895).

## Summary: what remains open or partial

The source reviews closed every correctness finding they raised within their
stated scopes. What remains falls into four groups.

**Attribution gaps that the paper must close (all `New`).**

1. **N3 closure theorem has a classical precedent that no report cites**
   (AGG-5). The statement that all aggregate rows describe exactly the
   projected joint-graph relaxation is a set-level form of the classical
   result that the Lagrangian dual equals the convexified problem
   (Lemaréchal–Renaud 2001, as used in Kerdreux et al. 2023; Udell–Boyd 2016;
   Geoffrion 1974 for integer programs). The `x^2 = 1/4` example is a
   duality-gap example.
2. **Forest McCormick exactness is Padberg (1989), Proposition 8** (OVER-10).
3. **N2 must be positioned against Dey–Khajavirad (2025) and Khajavirad
   (2026)** (OVER-11). Their decomposition results assume that the overlap has
   no "plus loop" (positive square coefficient). The reduced `1/128` witness
   has its only positive square on the shared center `y`. Their exact
   extended formulation for that sign pattern adds the nonedge product `xz`.
   This explains the report's dense-SDP remark and shows that the witness
   tests exactly the hypothesis they impose.
4. **The Report A row-domain polygon example is an RLT consequence**
   (POLY-8). `x^2+2xy+y^2 <= x+y` on `x,y >= 0, x+y <= 1` is the sum of the
   two linearized constraint-factor products; this was checked exactly here.
5. **SCIP 10.0 already has an exact MILP mode** with exact readers, safe
   outward bounds, and VIPR certificates (IMPL-22). N4 and N6 must be
   positioned against it.
6. Minor attributions: the chord correction is the standard linear
   interpolation error bound (BERN-3b); the `d*u = 1` domain witness is the
   Rabinowitsch encoding (IMPL-9b).

**Mathematical scope questions that remain open.**

- Extension of C-STAR from stars to trees with parent–child affine rows
  (STAR-12). Bhathena et al. (2025) is an uncited comparator.
- Automatic choice of the `delta^2/2` family members and of separator
  statistics that close overlap gaps (OVER-4, OVER-5).
- The quoted complexity of the box-only star case must keep its arithmetic
  model (STAR-4, partial).
- The positioning of N5 against the classical treatment of
  non-full-dimensional bodies has not been checked (SEP-9b, new).

**Evidence that a journal referee will ask for.**

- Runs were short (6 s in Campaign A, 30 s in Campaign B), used one primary
  seed, and ran on a shared host. No other solver was compared (EXP-B6,
  EXP-X4).
- The screening certificate accepted only 2 skips in 506 queries (SCR-4).
- The SCIP library version is not recorded in either campaign's environment
  file (EXP-X3, new). The current environment reports SCIP 10.0 with
  PySCIPOpt 6.2.1.
- The exact checks of the reduced overlap certificate, the `delta^2/2`
  family, and the constrained overlap example were run from standard input
  and not saved (OVER-12, partial).
- Single symbolic operations can still overrun the soft discovery deadline
  (IMPL-16, partial).

**Provenance gaps.** The Ballerstein (2013) thesis PDF was not retained
(SUP-10). Vavasis (1990) and Garloff–Jansson–Smith (2003) were checked only at
abstract level (POLY-4, BERN-8).

The adverse computational result is not an open issue. Both reports, all
reviews, and the closeouts agree on it: no additional solves, more summed time
in the cut modes, and native SCIP as the recommended default. The paper must
state it in the abstract and conclusion (EXP-A1, EXP-B1, EXP-B10).

## C-SUP: joint support cuts and final-row validity

| ID | Raised in | Issue | Resolution and record | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| SUP-1 | `A/reviews/document-review.md`; `A/literature/README.md` ("distinctions"); `B/reviews/separation-review.md` | An exact support oracle for a given direction is not a complete separation algorithm. A finite set of generated cuts is an outer approximation, and the absence of a violated cut does not show hull membership. | Stated in A `main.tex` after Prop. "Support and complete hull description" and in B `foundations.tex`. | Scoped | State it next to the support proposition. Keep "exact support", "certified lower bound", and "separation" as distinct terms. |
| SUP-2 | `A/reviews/document-review.md`; `A/reviews/numerical-review.md` ("Coefficient semantics and export") | The final-row proposition must apply to the exact values of the coefficients actually submitted, not to the ideal direction before rounding. | Implemented: coefficients are converted to binary64 and then read as exact rationals; the right-hand side is rounded down and checked exactly. Tests include subnormals and a rational whose binary64 value differs. | Resolved | State the proposition for exported binary64 coefficients read as dyadic rationals. Note that rounding an already proved rational row without rechecking does not meet the contract. |
| SUP-3 | `A/literature/final-contribution-review.md` (correction 2); `B/literature/final-contribution-review.md` (table row 1) | The research README said the method certifies "the support value". The general arithmetic paths certify only a lower bound, and a successful cut is not an exact support optimum in every path. | README wording corrected and confirmed by the reviewer. | Resolved | Say "certified lower bound on the support value" except for the exact quadratic oracles (C-POLY, C-STAR). |
| SUP-4 | `A/reviews/document-review.md`; A `main.tex` | Support over a continuous superset is valid for a mixed-integer graph but need not describe its hull. | Stated in A `main.tex`. | Scoped | Repeat the statement where integer variables appear. |
| SUP-5 | `A/reviews/numerical-review.md` (trust boundaries); `A/numerics/contract.md`; `A/theory/star-audit.md`; `B/theory/polytope-review.md`; `B/reviews/separation-review.md`; `B/reviews/integration-review.md` (certification boundary); `A/literature/README.md` | Replay shares the producer's exact arithmetic and geometry routines. It is an independently executable check, not an independently implemented or formally verified checker. Python, SymPy, python-flint/Arb, and the PySCIPOpt expression interface are trusted. | Stated in all component reviews and in both reports. Independent diagnostics (analytic fixtures, KKT face enumeration, whole-interval checks, MaxCut enumeration) reduce but do not remove this gap. | Scoped (permanent) | Give a trust-base paragraph. Do not call replay an independent proof checker. Separate the independent diagnostics from producer/replay agreement. |
| SUP-6 | `A/reviews/numerical-review.md` | A support certificate is conditional on the caller's affine rows being valid restrictions of the model. | Report B binds rows to the source model through the affine-bound certificate (C-IMPL). | Resolved in B | Make the binding of domain rows part of the certificate statement. |
| SUP-7 | `A/reviews/numerical-review.md` | The in-process sample cache is trusted state; changing its graph or domain while reusing it would be unsound. Serialized evidence takes a stricter path. | Stated as a trust boundary. | Scoped | Either describe the cache as untrusted proposal state or omit it from the certified path. |
| SUP-8 | `A/literature/README.md`; `A/literature/composition-audit.md`; `B/document/literature.tex` | Simultaneous graph convexification and separation from linear combinations are established: Ballerstein (2013), Liers et al. (2021, Prop. 1 and Sec. 3), Tawarmalani (2010), He–Tawarmalani (2021 Thm 6, 2022 Thm 4 and Cor 7, 2024 Prop 28), Zhu–He–Tawarmalani (2026 Thm 7–8), Li et al. (2026). | Both reports cite these and make no first-method claim. | Scoped | Cite with locators. Present C-SUP as the certified implementation of an established principle. |
| SUP-9 | `A/literature/README.md` (Garloff–Smith); `B/literature/aggregation-prior.md` | A numerical proposal followed by rigorous validation of an affine lower bound has a direct precedent (Garloff and Smith 2008, Sec. 5). Safe rounding with bound corrections has precedents (Cook et al. 2009; Eifler–Gleixner 2024). | Cited in both reports. | Scoped | N4 can claim only the combined contract: exported-coefficient semantics, whole-domain certificate, safe rounding after elimination, and replay bound to the source model. |
| SUP-10 | `A/literature/README.md`; `A/literature/sources/MANIFEST.md` | The Ballerstein thesis PDF was not retained; the institutional download returned HTTP 429. Its Chapter 5 details rely on an earlier repository note. | Provenance recorded; Liers et al. corroborates the general hull characterization only. | Open (provenance) | Obtain the thesis and cite exact chapter locators, or cite only what Liers et al. attribute to it. |
| SUP-11 | `A/literature/composition-audit.md`; `A/literature/README.md` | The earlier audit `notes/shared-variable-terms-literature.md`, Sec. 2.4, wrongly said that the He–Tawarmalani abstracts omit vectors of outer functions. | That paragraph was corrected in Report A. | Resolved | Do not reuse older first-method wording from background notes. |
| SUP-12 | `notes/review-minlp-developments-20260922.md` ("Shared-variable terms") | The background note claimed that the joint epigraph hull equals the intersection of individual epigraph hulls. The pair `x^2, sqrt(x)` on `[0,1]` disproves it. | Background note corrected. | Resolved (background) | If epigraphs motivate the paper, use the corrected statement. Keep graph hulls and one-sided (hypograph or epigraph) hulls distinct, as He–Tawarmalani (2022) requires. |

## C-BERN: Bernstein enclosures, elementary functions, curvature correction

| ID | Raised in | Issue | Resolution and record | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| BERN-1 | `A/reviews/numerical-review.md` ("Finding and resolution") | The producer accepted `max_depth=300` while replay rejected depth above 256. Example: feature `x` on `[0,1]`, row `x >= 2^-270`, target `2^-271` gave a valid 543-cell proof that replay rejected. | Budgets now require integers with `max_depth <= 256` and `max_cells <= 1,000,000`, matching the checker. A regression test covers it. | Resolved | Nothing beyond stating the certificate budgets if they are described. |
| BERN-2 | `A/reviews/numerical-review.md`; `B/document/foundations.tex` (after Prop. "Partition certificate") | Validity needs complete closed-cell coverage, including endpoints. An omitted end interval or a cache key without its domain is unsound. | Replay starts from the trusted domain and rejects omitted branches, altered bounds, and false exclusions (A `COVERAGE.md`). | Resolved | State the coverage premise in the partition proposition. |
| BERN-3 | `A/reviews/numerical-review.md` ("Combined scalar and second derivative"); `A/reviews/document-review.md` | The chord correction needs an upper bound `M` on the second derivative, the `max(0,M)` clamp, and a twice-differentiable scalar on the cell. A nonsmooth `|x|` example shows that an endpoint-only bound would be invalid. | Sign and clamp verified; analytic checks include `exp(x)-x` (one-cell bound `1-e/8`). Unsupported or singular derivatives disable the correction. | Resolved | State the hypotheses as in B `foundations.tex` eq. (chord-correction). |
| BERN-3b | New | The chord bound `min p >= min{p(a),p(b)} - max{0,M}(b-a)^2/8` is the standard linear-interpolation error bound. Neither report attributes it. | — | New | Cite a standard numerical-analysis source and present it as a known lemma used inside the certificate. |
| BERN-4 | `A/reviews/numerical-review.md` ("Elementary intervals and domains") | Domains must be kept for zero-weight features, tiny endpoint slivers (a peak `2^-300` from an endpoint), and rational endpoints such as `log` at `1+2^-200`. | Every original feature is evaluated on the whole cell before simplification. There is no continuity-based sliver omission. | Resolved | Mention these regression classes in the C-BERN description. |
| BERN-4b | `notes/review-composite-univariate-envelopes.md` (findings 1–9); `results/composite-univariate-envelopes.md` (status and limits) | The older composite-univariate handler had a latent local/global cut-flag bug, did not certify that `g` is defined on certified pieces, could hang, assumed continuity on endpoint slivers, guarded floating-point values with a fixed relative shift instead of directed rounding, and was called "exact certified". | The fixes are recorded in the experiment record. Report A treats the handler as a foundation and does not relabel its results as certified (A `COVERAGE.md`, last paragraph). | Resolved (background) | If the paper cites the earlier handler, say that its cuts were not rigorously certified. Use it as motivation for C-BERN, not as evidence. |
| BERN-5 | `A/reviews/numerical-review.md` | The elementary path trusts Arb's outward `lower()`/`upper()` rounding (python-flint 0.9.0 documentation) and exact `fmpq` input. | Stated as a trusted dependency. | Scoped | Name python-flint/Arb and the version in the trust base; cite Johansson (2017). |
| BERN-6 | `A/document/COVERAGE.md`; `A/numerics/contract.md`; `A/document/integration.tex` | Scope caps: the Bernstein path covers one or two variables, at most 1,024 tensor coefficients, and degree at most 32 per variable. Discovery caps total degree at 8 (one variable) and 4 (pairs). Elementary expressions have one free variable. | Stated in Report A. | Scoped | State these caps. Do not describe C-BERN as general multivariate. |
| BERN-7 | `A/numerics/contract.md` ("Remaining limitations") | Interval dependence can make strict domain validation inconclusive; subdivision budgets then give no cut. Certificates store the subdivision tree and can be large. | Stated. | Scoped | Report refusals and certificate size as costs. |
| BERN-8 | `A/literature/README.md` | Bernstein enclosure and monotone subdivision are classical (Garloff–Smith 2008; Garloff–Jansson–Smith 2003). The 2003 paper was checked at abstract level only. | Cited in both reports. | Partial (provenance) | Cite. Read the 2003 full text before citing specific results. |

## C-SCREEN: convex-combination screening certificate

| ID | Raised in | Issue | Resolution and record | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| SCR-1 | `A/reviews/document-review.md`; `A/reviews/numerical-review.md` | The screen excludes violations **strictly greater** than the threshold; equality can occur. The topic overview said "below" instead of "at most". | Overview corrected; equality case tested. | Resolved | State the strict inequality exactly. |
| SCR-2 | `A/reviews/document-review.md`; `A/reviews/numerical-review.md`; `A/document/COVERAGE.md` | The norms must be paired correctly: scaled L1 distance with coordinatewise normal bounds, and scaled infinity distance with a sum bound. Normalizations must match. | Verified in review. | Resolved | State both pairings and the normalization. |
| SCR-3 | `A/reviews/numerical-review.md`; `A/reviews/integration-review.md` | Graph samples must be exactly feasible; interval-valued samples use the worst residual. The trusted evaluator must reject points that violate other nonlinear restrictions. A positive tolerance proves neither hull membership nor original feasibility. | Implemented: exact row checks, clipped weights renormalized exactly. | Scoped | State these premises. Do not describe a skipped block as being in the hull. |
| SCR-4 | `A/reviews/document-review.md` ("Final empirical assessment"); `A/experiments/README.md` | In Campaign A the screen produced only **2 accepted skips in 506 queries**. The `no_cache` ablation changes screening, exchange, repeat checks, and caching together, so it cannot isolate the screen's effect. | Reported, not changed. | Open (usefulness) | Report 2/506. Present the screen as a sound but rarely effective tool, or move it out of the main contributions. Do not cite `no_cache` as screen evidence. |
| SCR-5 | `A/literature/final-contribution-review.md` | The bound is standard convex-combination geometry plus Hölder's inequality. | Attributed. | Scoped | Make a modest claim: a checkable skip condition. |
| SCR-6 | `A/document/COVERAGE.md` | The integration screens only source polynomials. | Stated. | Scoped | State it. |

## C-AGG: original-variable aggregation cuts and closure

| ID | Raised in | Issue | Resolution and record | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| AGG-1 | `B/literature/row-proof-review.md`; `B/literature/final-contribution-review.md` (clarification 1) | The equality extension of the closure theorem needed explicit continuity of the equality features `h`. Shared coordinates between block and model variables needed an explanation (duplicate, then identify). | Both added to `B/theory/row-aggregation.md` and `B/document/aggregation.tex` (Thm "Closure of the direct-row interface"); reviewer inspected the revised text. | Resolved | Keep the continuity hypothesis and the duplication remark. |
| AGG-2 | `B/literature/row-proof-review.md`; `B/literature/final-contribution-review.md` (clarification 2); `B/reviews/document-review.md` | The rounding correction mathematically needs only a one-sided bound per changed coefficient (lower bound if `Delta_j > 0`, upper if `Delta_j < 0`, none if zero). The exporter requires both finite bounds for any changed coefficient. | Both statements documented; the conservative rule was checked as consistent with the theorem. | Resolved | State the theorem with the one-sided condition and describe the implementation rule separately. |
| AGG-3 | `B/literature/aggregation-prior.md`; `B/CLOSEOUT.md`; `B/document/frontier.tex`; `B/reviews/document-review.md` | The closure of all aggregate rows is the projected joint-graph relaxation, not the hull of the feasible set. Example: on `[0,1]`, `x^2 = 1/4` has feasible set `{1/2}`, but `x = 1/4` passes every direct cut. | Proved and reviewed; described as a property of the relaxation, not a missing implementation step. | Scoped (permanent) | State the example. Note that native propagation may resolve it and that putting the equality into the support domain changes the oracle problem. |
| AGG-4 | `B/literature/aggregation-prior.md`; `B/document/literature.tex` | The aggregation formula is weak Lagrangian duality (Boyd–Vandenberghe Secs. 5.1–5.2). Related prior work: aggregation hulls (Dey–Muñoz–Serrano 2022; Blekherman–Dey–Sun 2024); Lagrangian variable bounds in OBBT (Gleixner et al. 2017); grouped quadratic terms (Misener–Floudas 2012). | Cited. | Scoped | Cite. Extra strength comes only from jointly minimizing the nonlinear aggregate; combining already linear rows adds nothing. |
| AGG-5 | New | The closure theorem (N3) restates, at the level of sets, the classical result that the Lagrangian dual of a nonconvex problem equals its convexified problem. Local sources: `KB/kerdreux2023-stable-bounds-on-the-duality` Sec. 2.2 (PDF p. 3), which uses Lemaréchal and Renaud (2001), Th. 2.11; `KB/udell2016-bounding-duality-gap-for-separable` p. 4 and App. A ("the convexified problem is the dual of D"). Geoffrion (1974) gives the integer-programming form. Neither report nor any review cites these. The `x^2 = 1/4` example is a duality-gap instance. | — | New | Cite these sources, after checking the primary texts (Lemaréchal–Renaud and Geoffrion are not in the local KB). Present N3 as a self-contained characterization of this cut interface with affine remainders, not as a new duality result. |
| AGG-6 | `B/document/COVERAGE.md`; `B/implementation/integration.md` | The bounded practical multiplier search need not find all useful cuts. Finding no cut does not show hull membership. | Stated. | Scoped | State it. |
| AGG-7 | `B/document/COVERAGE.md`; `B/literature/aggregation-prior.md` | The bounds used in the rounding correction need independent model provenance. Rounding can erase a tiny separation. Bounds valid only below a node give local cuts, and objective cutoffs restrict validity. | Provenance comes from the affine-bound certificate (C-IMPL). Only global root cuts are inserted. A lost separation causes refusal. | Resolved / Scoped | State that only globally valid bounds are used and that lost separation leads to refusal. |
| AGG-8 | `B/reviews/document-review.md`; `B/reviews/document-metrics-review.md` | `B/PROGRAM.md` presented graph-auxiliary reformulation as the established cause of Campaign A's losses. Campaign A's reformulation control also solved 19, like baseline, so the counts do not isolate that cause. | Wording changed to "used in the earlier approach" and verified. | Resolved | Do not claim that original-variable cuts fix a cause identified in Campaign A. |

## C-POLY: exact quadratic support on bounded rational polytopes

| ID | Raised in | Issue | Resolution and record | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| POLY-1 | `B/theory/polytope-review.md` ("Candidate completeness", "Implementation review") | Boundedness is essential. An API that accepts arbitrary rows must establish or enforce finite bounds. A heuristic cutoff in subset enumeration cannot return an exact optimum or emptiness. | The implementation uses finite rational box bounds. Exceeding the work budget raises `EnumerationLimitError` instead of returning a truncated minimum. | Resolved | State boundedness as a hypothesis and the budget-refusal behavior. |
| POLY-2 | `B/theory/polytope-review.md`; `B/literature/final-contribution-review.md` | Complexity is `O(N(d^3+md))` rational operations with `N = sum_{k<=d} C(m,k)`, which is polynomial only for fixed `d`. Bit complexity is polynomial for fixed `d` through Gaussian-elimination size bounds. | Stated in the reports. | Scoped | State both the operation count and the bit-complexity argument, and that the method is not polynomial in `d`. |
| POLY-3 | `B/document/frontier.tex`; `B/literature/README.md`; `B/theory/polytope-review.md` | Unrestricted dimension is NP-hard (MaxCut reduction on `[0,1]^n`). General QP hardness is also classical (Vavasis 1990; Pardalos–Vavasis 1991). | Proof given in the report; Karp (1972) cited. | Resolved | Keep the proof short and cite the classical QP hardness results. |
| POLY-4 | `B/literature/final-contribution-review.md`; `B/literature/README.md` | Face enumeration for QP is classical: Murty (1997 Internet edition, Sec. 2.9, pp. 163–166), crediting Mueller and Murty. This was added after review. Vavasis (1990) was checked only at abstract and metadata level. | Murty added to report and bibliography; Vavasis limitation recorded. | Partial (provenance) | Present C-POLY as a checked rational realization of classical face enumeration. Read Vavasis before citing anything beyond NP membership. |
| POLY-5 | `B/theory/polytope-review.md` | Replay recomputes the whole enumeration with the producer's implementation. | Independent diagnostics (40 cases, analytic optima, exhaustive MaxCut) supplement it. | Scoped | Include in the trust-base paragraph. |
| POLY-6 | `A/literature/final-contribution-review.md` (correction 1); `A/literature/README.md` | Anstreicher–Burer (2010) Theorem 7 concerns triangulated **polytopes**, not arbitrary polyhedra. The polygon hull is a direct specialization of their results; exact stationary-point enumeration is the simpler implementation, not a new hull theorem. | Literature section corrected. | Resolved | Attribute the 2D polygon case to Anstreicher–Burer. |
| POLY-7 | `A/document/main.tex`; `A/reviews/document-review.md` | The polygon bound `O(m^3)` is an operation count, not a runtime bound. Rational numbers grow. | Stated. | Scoped | State the arithmetic model. |
| POLY-8 | New (checked here) | Report A's row-domain example (on `x,y >= 0`, `x+y <= 1`: `x^2+2xy+y^2 <= x+y` and `xy <= 1/4`, which the box hull intersected with the row misses) has no attribution and no review discusses it. The first inequality is exactly the sum of the linearized RLT constraint-factor products `(1-x-y)x >= 0` and `(1-x-y)y >= 0`. The half-mass point at `(0,0)` and `(1,1)` violates each product by `1/2` and the sum by `1`. `xy <= 1/4` follows once `X11 >= x^2` is added (the triangle hull is DNN by Anstreicher–Burer Cor. 4). | Exact SymPy/`Fraction` check run for this record (see "Checks run"). | New | If the paper keeps the example, attribute it to RLT/DNN. Note that SCIP's native RLT separation may already capture it, and do not present it as strength beyond RLT. |
| POLY-9 | `A/reviews/document-review.md`; `A/reviews/numerical-review.md` | The polygon proof must cover the singular positive-semidefinite case and degenerate (segment, singleton, empty) domains. | Checked; covered by the line-to-boundary argument and fixtures. | Resolved | Nothing beyond including the singular case in the proof. |
| POLY-10 | `B/document/implementation.tex` | The deployed wrapper uses the polytope oracle only up to dimension 4, with 2,000 subsets per calculation in the callback; an unmet limit gives no cut. | Stated. | Scoped | Distinguish the theorem from the deployed limits. |

## C-STAR: quadratic stars with center–leaf affine rows

| ID | Raised in | Issue | Resolution and record | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| STAR-1 | `A/reviews/document-review.md` | The first draft omitted the hypothesis that objective and row coefficients are rational. | Added to the model definition and to the gain corollary; reviewer read the corrected text. | Resolved | Keep the rationality hypothesis. |
| STAR-2 | `A/reviews/star-review.md` ("Merge gain and binding") | The gain equivalence needs the assembled domain to be exactly the set of simultaneous pair memberships `(y,x_i) in P_i`, including every center restriction. A center restriction imposed only after computing the pair minima would break it. | Assumption made explicit in `A/theory/README.md` Sec. 3. | Resolved | State the assumption in the gain corollary. |
| STAR-3 | `A/reviews/star-review.md` | The gain condition concerns the complete minimizing sets. Their center projections need not be intervals; comparing one selected minimizer per pair is not enough. | The implementation computes the gain by exact support, avoiding the shortcut. | Resolved | Phrase the corollary with full minimizer sets and give the compactness argument. |
| STAR-4 | `A/reviews/star-review.md` ("Complexity") | The `O(k^2)` bound for the box-only case counts rational arithmetic operations. Dense exponent tuples, zero entries, sorting, and serialization need not take quadratic elementary operations. The reviewer asked that the arithmetic convention be kept when the bound is quoted. | `A/theory/star-audit.md` confirms the `O((k+m+1)^3)` operation bound. `B/document/star.tex` states only "polynomial in the supplied row counts and number of leaves". | Partial | State the operation model with the bound, and give the bit-length argument from `A/reviews/star-review.md` and `A/theory/star-audit.md`. |
| STAR-5 | `A/reviews/star-review.md`; `A/theory/star-audit.md` | Polynomial bit complexity must be justified, not inferred from the operation count. | Justified: breakpoints solve affine equations, there is no repeated nonlinear composition, and stationary points solve linear equations. | Resolved | Include the argument; "polynomial time" needs it. |
| STAR-6 | `A/reviews/document-review.md` ("Final implementation claim assessment") | The integration text said discovery checked the affine-row center structure. In fact, candidates come from the quadratic graph, and the oracle later refuses unsupported stars, such as one with a leaf–leaf row. | Text corrected to separate candidate discovery from the oracle's eligibility check. | Resolved | Describe the discovery and eligibility steps separately. |
| STAR-7 | `A/reviews/star-review.md`; `A/theory/star-audit.md` | Replay binds normalized rational input (zero terms omitted, row order kept), not a model file or expression tree. Binding to model variables and the actual SCIP coefficients is the integration's job. | Clarified in the note. | Scoped | Link the C-STAR certificate to the C-IMPL binding. |
| STAR-8 | `A/theory/star-audit.md`; `A/reviews/star-review.md` | Sampled checks at three interior points per piece do not prove correctness on the whole interval. | Complemented by whole-interval checks: 88 cases, 786 intervals, 7,063 exact comparisons, independent projection. The proof carries the universal claim. | Resolved (as evidence) | Present both audits as distinct evidence, not as a proof. |
| STAR-9 | `A/literature/star-overlap.md`; `B/document/star.tex` | The box-only star is a special case of Del Pia–Khajavirad's forest DP (arXiv 2609.35595v1, Thm 1, `O(n^2)`). Piecewise-affine parametric QP responses are classical (Bemporad et al. 2002). Khajavirad (2026) and Locatelli (2015) are related. The extension still uses classical parametric optimization, and its scope difference alone does not prove novelty. | Cited; no priority claim. | Scoped | Restrict N1 to center–leaf rows plus all curvature signs, with an explicit rational partition. Make no first-result claim without a priority search. |
| STAR-10 | `A/theory/README.md`; `A/document/COVERAGE.md`; `B/document/COVERAGE.md` | Rows coupling two leaves destroy conditional independence. The implementation rejects them. Integer restrictions are not enforced. | Stated; the polytope oracle covers small unions. | Scoped | State the class boundary. |
| STAR-11 | `A/reviews/document-review.md`; `A/CLOSEOUT.md`; `A/experiments/README.md` | The gain diagnostic does not choose normals or predict runtime. In Campaign A, native SCIP already solved the star case quickly and automatic star merging added cost. | Reported. | Scoped (negative) | Report it. |
| STAR-12 | Partly `B/document/star.tex` ("does not repeatedly nest piecewise messages along a tree"); otherwise New | Extending the class to trees with parent–child affine rows (depth greater than one) is not studied. Del Pia–Khajavirad's forest DP (box only) and Bhathena et al. (2025, `KB/bhathena2025-a-parametric-approach-for-solving`: parametric DP over trees for convex QP with indicators) are natural comparators. Bhathena et al. is not cited. | — | Open | State that the result is for stars. Note the tree case as an open question, and compare with both papers. |

## C-OVER: pair hulls glued on shared moments

| ID | Raised in | Issue | Resolution and record | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| OVER-1 | `A/reviews/document-review.md`; `A/theory/README.md` Sec. 3; `B/literature/final-contribution-review.md` | The witness is not a dominance claim over dense SDP/RLT. The saturated pair covariances force `Cov(x,z) = 1/5`, so `E[xz] = 3/5 > E[x] = 1/2`, which violates the nonedge McCormick bound. | Stated in both reports. | Scoped | Say that dense PSD plus the nonedge product excludes the witness. Compare against complete pair hulls, not only McCormick. |
| OVER-2 | `A/theory/overlap-review.md`; `A/reviews/document-review.md` | The constrained example survives only *separate block interval propagation*. Global presolve combining both rows deduces `x = z = 0`. | Qualified in the note and report. | Scoped | Keep the qualifier. |
| OVER-3 | `A/theory/overlap-review.md` ("An explicit missing cut ...") | The gap `1/128` scales with the objective; its size is not a bound on the effect of missing separator consistency. | Stated. | Scoped | Give the gap with its normalization, or describe it only as strict and exact. |
| OVER-4 | `A/theory/overlap-review.md` (family (4)) | For the `delta^2/2` family, automatic choice of `a,b,c,d` and the cost of detecting useful members remain open; no novelty or computational advantage is claimed. | — | Open | Present the family as an explicit construction. State that detection is open. |
| OVER-5 | `A/theory/overlap-review.md` ("One extra separator statistic") | Adding `E[q^2]` with `q = y(1-y)` closes the constrained example, but there is no automatic rule for finding such statistics. | — | Open | State this as an open question if the remedy is mentioned. |
| OVER-6 | `A/theory/overlap-review.md`; `A/literature/README.md`; `B/reviews/document-review.md` | Gluing with full separator marginals under running intersection is established (Lasserre 2006, Lemmas 6.3–6.4). It needs conditional kernels on standard Borel spaces. Finitely many shared moments suffice only when they determine the separator law. | Attributed and scoped. | Scoped | Attribute to Lasserre. Do not present the gluing theorem as new. |
| OVER-7 | `A/theory/overlap-review.md`; `B/reviews/document-review.md` | Coordinate means do not determine the joint law of a multi-variable binary separator. | Stated. | Scoped | Keep this distinction in the special cases. |
| OVER-8 | `A/literature/README.md` (Tawarmalani 2010) | Inclusion certificates (Def. 3.4, Cor. 3.9) already explain compatibility through representing measures; individual hulls need not combine into the joint hull. | Cited. | Scoped | Credit the general phenomenon. N2's contribution is the explicit quantitative witness for full two-sided pair graph hulls. |
| OVER-9 | `A/CLOSEOUT.md`; `A/experiments/README.md` | The obstruction gave no runtime benefit in the solver experiment. | Reported. | Scoped | Separate the mathematical result from solver evidence. |
| OVER-10 | New | McCormick exactness for pure bilinear forests is classical: Padberg (1989), Proposition 8, `QP^G = QP^G_LP` iff `G` is acyclic (`KB/padberg1989-the-boolean-quadric-polytope-some`, PDF p. 23). Neither report cites it. | — | New | Cite Padberg and present the forest case only as a consistency check. |
| OVER-11 | New | Dey–Khajavirad (2025, arXiv 2508.18435; `KB/dey2025-a-second-order-cone-representable`) prove decomposability of the sign-oriented lifted set across a complete separator **with no plus loops** (Cor. 1, PDF p. 9). They also prove an exact SOC description when the plus-loop nodes form a stable set; the proof adds products among the neighbors of each plus-loop node (Thm 2, PDF p. 20). Khajavirad (2026; `KB/khajavirad2026-tight-semidefinite-programming-relaxations-for`) uses the same decomposition (Lemma 4, PDF p. 6; Thm 5, PDF p. 23). The reduced witness (3) has square coefficients `(0, 2, 0)` for `(x, y, z)` (checked here). So only the separator `y` carries a plus loop, and their construction adds exactly the nonedge product `xz`. The witness therefore shows that the no-plus-loop hypothesis cannot simply be dropped for pair decomposition. A text search of their full texts found no equivalent path example; Dey–Khajavirad list necessity of the stable-set condition as open (PDF p. 27). Report A cites Khajavirad (2026) only for Theorems 5–6 in the star context. | Search and check run for this record. | New | Cite both papers. Frame N2 as quantifying the failure of pair decomposition when the separator has a positive square coefficient, and relate the dense-SDP remark (OVER-1) to their construction. Confirm that neither paper contains an equivalent example before claiming novelty. |
| OVER-12 | `A/theory/overlap-review.md` ("Targeted verification") | The exact checks of the witness moments, the reduced certificate (3), the constrained example, and the separator moments were run as `python -` scripts on standard input and not saved. The merged-star `1/128` mechanism is replayable (`A/experiments/star-mechanism.json`, `A/experiments/check_star_mechanism.py`). | Partly saved. | Partial | Save a rerunnable exact check script for every displayed overlap claim in the paper's `verification/` folder. |

## C-SEP: complete positive-tolerance separation

| ID | Raised in | Issue | Resolution and record | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| SEP-1 | `B/reviews/separation-review.md` | The normal grid must cover the whole normal box, including its boundary; testing only corners is not enough. Example: for `F(x) = (x, x^2)` on `[0,1]`, the query `(3/10, 2/25)` is at L1 distance `1/100`, and no normal in `{-1,0,1}^2` separates it. | Tested. | Resolved | Use the example to motivate the grid. |
| SEP-2 | `B/reviews/separation-review.md` | A near-hull verdict needs upper support bounds (feasible graph points), while a cut needs a lower bound over the whole domain. A failed or budget-exhausted search is not a distance certificate. | Encoded in the statuses and in replay. | Resolved | State the four statuses with their evidence requirements. |
| SEP-3 | `B/reviews/separation-review.md` | Thin or lower-dimensional domains need the exact barycentric rational net. Filtering a floating-point grid is not enough. | Implemented; tested on `x+y = 1/3`. | Resolved | State that full-dimensionality is not assumed. |
| SEP-4 | `B/reviews/separation-review.md` | With cone coordinates `J`, the target set becomes the hull plus the cone, and the distance contribution is `max(F_j - q_j, 0)`. | Implemented; replay binds `J`; a negative cone coefficient is rejected even when the header is forged. | Resolved | State the cone variant. |
| SEP-5 | `B/reviews/separation-review.md`; `B/reviews/document-review.md` | An exact rational separating cut need not survive binary64 export (a gap smaller than the least positive binary64 value). The export records availability and whether it still separates. | Implemented. | Scoped | Distinguish rational separation from exported separation. |
| SEP-6 | `B/reviews/separation-review.md` ("Findings resolved during review") | Six implementation defects: wrong argument order in the quadratic replay call; SymPy floats narrowed through binary64; `x * x**(-1)` accepted as one (domain loss at `x = 0`); an eager normal mesh allocated before the budget check; recursion-depth limits; `None` certificates raising an error. | All fixed; 21 independent tests pass. | Resolved | Optionally mention the domain-loss regression as an example of why source syntax is checked before simplification. |
| SEP-7 | `B/reviews/separation-review.md`; `B/theory/separation.md`; `B/literature/README.md` | Complete mode is finite but not polynomial: the normal net has `(N+1)^m` points, the domain net up to `C(M+k-1, k-1)`, and the cost in the tolerance is not polynomial in its bit length. Budgets count cardinality, not wall-clock time or face enumeration. | Stated. | Scoped | State the costs explicitly. |
| SEP-8 | `B/reviews/separation-review.md`; `B/literature/final-contribution-review.md` | `within_tolerance` is L1 distance in feature (and slack) coordinates, not in original model variables. | Stated. | Scoped | State the coordinate system and normalization of the tolerance. |
| SEP-9 | `B/literature/README.md`; `B/document/literature.tex`; `B/literature/final-contribution-review.md` | The weak optimization/separation equivalence of Grötschel–Lovász–Schrijver (1981, Thm 3.1) is algorithmically stronger under its inner/outer-ball assumptions. The finite-net construction is a direct elementary proof, not a polynomial-time substitute. | Stated. | Scoped | Limit N5 to an explicit finite algorithm with stated output semantics and no full-dimensionality assumption. |
| SEP-9b | New | The GLS book treats some non-full-dimensional bodies, for example well-described polyhedra and bodies with a known affine hull. The claim "without full-dimensionality" has not been checked against that treatment. | — | New | Check GLS (1988) before presenting the absence of a full-dimensionality assumption as a distinguishing feature. |
| SEP-10 | `B/reviews/separation-review.md`; `B/reviews/document-review.md`; `B/document/implementation.tex` | The solver callback uses a separate capped support wrapper, not the complete fallback. | Stated. | Scoped | Do not present callback results as complete separation. |
| SEP-11 | `B/reviews/separation-review.md` | Source-syntax validation cannot recover a domain restriction removed before the caller built the expression. | Stated. | Scoped | Include in the trust base. |
| SEP-12 | New (supporting) | Del Pia–Khajavirad (2026) show that quartic minimization over the unit box is strongly NP-hard even when the interaction graph is a path (`KB/pia2026-treewidth-and-the-complexity-of`, p. 18 per the KB summary). | — | New (optional) | Cite in the frontier discussion to explain why exponential costs for polynomial graphs are expected in general. |

## C-IMPL: source-faithful SCIP implementation

| ID | Raised in | Issue | Resolution and record | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| IMPL-1 | `A/reviews/integration-review.md` (finding 1) | Deduplicating atoms by SymPy expression merged `x^2` and `sqrt(x)^4`, removing the second domain restriction. | Discovery now deduplicates exact source trees. | Resolved | Use it as an example of domain loss under algebraic equality. |
| IMPL-2 | `A/reviews/integration-review.md` (finding 2) | Native construction can change exact coefficients: `1e16 + 1 - 1e16` evaluated to zero. | Constants are folded only when the exact result is representable, and constructed expressions are compared exactly. | Resolved | Cite as motivation for exact binary64 source semantics. |
| IMPL-3 | `A/reviews/integration-review.md` (finding 3) | Checking each atom is not enough: whole-row cancellation can lose small coefficients. | Complete original rows are checked in every mode; rewritten rows are checked after exact substitution. | Resolved | Describe the whole-row check. |
| IMPL-4 | `A/reviews/integration-review.md` (finding 4) | Logging the requested coefficients does not show which row SCIP received. | The actual row (columns, coefficients, bounds, constant, scope) is read before insertion. Dropped columns and presolve fixings are rejected. | Resolved | Describe replay of the stored SCIP row. |
| IMPL-5 | `A/reviews/integration-review.md` (finding 5) | In direct probes, SCIP removed the domain in `0*sqrt(x)`, `sqrt(x)-sqrt(x)`, and `0*log(x)`. On `[-1,1]`, a baseline minimizing `x` returned `-1`. | Every mode proves all source domain restrictions on the declared box before normalization; unresolved restrictions are refused. | Resolved | Report this as observed SCIP behavior with the exact version and a minimal reproducer (see EXP-X3). Do not call it a SCIP defect without that evidence. |
| IMPL-6 | `A/reviews/integration-review.md` (finding 6) | Finite source sides at or beyond SCIP's infinity value, reversed bounds, wrongly signed infinities, NaNs, and metadata length mismatches. | Refused. | Resolved | Mention briefly. |
| IMPL-7 | `A/reviews/document-review.md`; `A/CLOSEOUT.md`; `A/experiments/experiment-audit.md` | The strict Report A importer refused valid models: three held-out and two historical domain refusals, one row changed by binary64 assembly (`chp_partload`), and one variable-exponent failure (`cvxnonsep_pcon40r`). | Report B admitted all seven historical cases through exact affine bound propagation, domain witnesses, and positive-base variable powers (`B/CLOSEOUT.md`; `B/numerics/model-admission.json`). | Resolved for those cases | Report the admission gain and state the grammar that remains unsupported (IMPL-14). |
| IMPL-8 | `B/reviews/model-review.md` | The first variable-power guard forced every base to be positive. That changes the model, because a negative base with an integer exponent can be valid. | Variable powers now need an independently proved positive base; otherwise `unsupported_variable_power_domain`, which is not an infeasibility claim. | Resolved | State the rule and its refusal semantics. |
| IMPL-9 | `B/reviews/model-review.md` | Domain witnesses `d*u = 1` (projects to `d != 0`) and `d*u = 1, u >= 0` (projects to `d > 0`) are exact over the reals; SCIP still checks them with numerical tolerances. They are recorded even inside zero products and zero powers. | Implemented and audited (`B/reviews/model_binding_audit.py`). | Scoped | State that exactness holds over the reals and not for SCIP's tolerance-based checks. |
| IMPL-9b | New | The `d*u = 1` encoding of `d != 0` is the classical Rabinowitsch trick. | — | New (minor) | Attribute it. |
| IMPL-10 | `B/reviews/model-review.md` | Pure constant rows reached `addCons` as Python Booleans. A row constant moved to the side by binary64 subtraction (`0.01` against side `0.1`) changed the row. | Constant expression objects are used; the original side is kept. | Resolved | Optional detail. |
| IMPL-11 | `B/reviews/integration-review.md` | The actual-row audit allowed two source variables to map to one transformed column, and a NaN upper side could pass an inverted comparison. | Duplicate mappings rejected; an infinite upper side is required explicitly. | Resolved | Optional detail. |
| IMPL-12 | `B/reviews/model-review.md`; `B/reviews/integration-review.md`; `A/reviews/document-review.md` | The binding boundary is the submitted PySCIPOpt expression DAG. SCIP's later simplification, presolve, floating-point feasibility checks, and bounds are not certified. Native construction and runtime capture of the actual row are trusted. The generic expression fallback is not exact SCIP arithmetic. | Stated in all reviews. | Scoped (permanent) | State the boundary precisely in the C-IMPL section and the abstract. |
| IMPL-13 | `B/numerics/model-contract.md`; `B/literature/final-contribution-review.md` | A strict domain can make an infimum unattained. Support on a polynomial extension is valid for original feasible points, but a closeness bound for the extended graph does not certify membership in the original partial graph. | Stated. | Scoped | State it where cancelled expressions are discussed. |
| IMPL-14 | `B/numerics/model-contract.md` | Supported grammar: finite arithmetic, fixed rational powers, positive-base variable powers, and exp/log/sqrt/sin/cos/abs. General power domains and exact global domain inference are not claimed. `B/PROGRAM.md` asked to "support valid variable powers"; only proved-positive bases are supported. | Stated. | Scoped / Partial against the program | State the grammar and the positive-base restriction. |
| IMPL-15 | `B/reviews/integration-review.md` ("Defensive changes"); `B/experiments/post-freeze-changes.md` | Three defensive guards (infinity value for the cut side and the actual lower side; an exception in heuristic exchange-sample evaluation) were completed after the campaign snapshot. | The guard audit found all 123 recorded rows below SCIP's infinity value (largest ratio `8.5e-19`), and none of the four worker errors came from the exchange path. | Resolved for recorded rows | State that the measured implementation is the frozen one. |
| IMPL-16 | `B/reviews/integration-review.md`; `B/reviews/experiment-review.md`; `B/reviews/document-review.md` | Discovery overran its allowance (46 measured overruns) because several symbolic operations ran without time checks. | Deadline checks now run between discovery steps, and unfinished discovery is discarded (`discovery_incomplete`). In the repaired cohort, six overruns remain (largest discovery excess 3.618 ms, callback excess 29.529 ms, total-budget excess 23.611 ms) because single symbolic calls cannot be interrupted. | Partial | Report that the deadline is soft and that single calls are not preemptive. Do not claim a hard time guarantee. |
| IMPL-17 | `B/reviews/integration-review.md`; `B/experiments/post-freeze-changes.md` | Discovery built each polynomial over all model variables, and SymPy's dense constructor hit its recursion depth on `chp_partload` and `waterno2_06` (four worker errors). The repair also found a conversion exception for a term with an exact nonrational coefficient. | Sparse per-term generators were introduced; unsupported terms stay in the nonlinear remainder. Replay got the matching fix. Validated in the separate 75-job cohort. | Resolved | Report the defect, the fix, and that the original failures are kept in the primary results. |
| IMPL-18 | `B/reviews/integration-review.md` | Three offline checker versions exist: frozen `b6e0fe49...`, repair `83ab356a...`, and final `10115390...`. The final version also handles tamper controls for an empty infeasibility row `0 >= 1`. | Archived (`B/reviews/replay-final.py`, `replay-final-provenance.json`). | Resolved | State which checker replays which cohort. |
| IMPL-19 | `B/document/evidence.tex` | Admission does not guarantee that every later separator operation finishes; the four worker failures happened after model construction. | Stated. | Scoped | Do not count worker failures as importer refusals. |
| IMPL-20 | New | No report compares N4/N6 with SCIP 10.0's exact solving mode. That mode reads MPS/LP/CIP/OPB/ZIMPL instances exactly, keeps floating-point bounds as safe outward roundings of exact ones, and logs VIPR certificates, but is restricted to MILP (Hojny et al. 2025, Sec. 3.1, PDF pp. 7–8; `KB/hojny2025-the-scip-optimization-suite-10`). VIPR itself (Cheung, Gleixner, Steffy) is not in the local KB. | — | New | Position the work: exact semantics for MINLP expression DAGs and certified individual cuts, versus an exact end-to-end MILP solve. Cite SCIP 10 and VIPR. |

## C-EXP: computational campaigns

| ID | Raised in | Issue | Resolution and record | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| EXP-A1 | `A/CLOSEOUT.md`; `A/reviews/document-review.md`; `A/literature/final-contribution-review.md` | Campaign A's held-out result is adverse: 19/24 solved for baseline and control versus 18/24 for both cut modes (20 admitted). `genpooling_lee2` was lost in both cut modes. | Reported in the abstract, conclusion, and closeout. | Scoped (negative result) | Report it. Recommend native SCIP as the default. |
| EXP-A2 | `A/CLOSEOUT.md`; `A/experiments/experiment-audit.md` | The synthetic solved-count gain (12 to 13) is matched by the reformulation control, so it cannot be attributed to the cuts. | Reported. | Scoped | Attribute the gain to reformulation. |
| EXP-A3 | `A/experiments/experiment-audit.md`; `A/reviews/document-review.md` | Refusals (`syn15m`, `cvxnonsep_psig30r`, `syn10hfsg`) and the `cvxnonsep_pcon40r` failure (eight worker errors with unknown cut counts) are importer limitations, not SCIP failures. | Kept in the denominators. | Scoped | Keep the 24 denominator and separate selected, admitted, and solved counts. |
| EXP-A4 | `A/experiments/README.md` | On the historical `waterno2_06` diagnostic, the final dual bounds were 26.59 / 21.17 / 7.05 / 2.41 for baseline / control / all / auto, which is much worse in the cut modes. | Reported. | Scoped (negative) | Report it. Reconcile it with any earlier `waterno2` gains the paper cites (EXP-X4). |
| EXP-A5 | `A/experiments/experiment-audit.md`; `A/reviews/document-review.md` | Final dual bounds against baseline: `all` 1 better / 14 tied / 5 worse / 4 unavailable; `auto` 3 / 12 / 5 / 4. Against the control, both modes are 3 / 16 / 1 / 4. Root one-node comparisons: `all` 3 / 15 / 2, `auto` 3 / 14 / 3. All use a `1e-6` scaled tolerance. | Reconciled with raw records. | Scoped | Report the final and root comparisons separately, with the tolerance. |
| EXP-A6 | `A/reviews/integration-review.md`; `A/experiments/experiment-audit.md` | Runs were short (6 s full, 2 s root with one node) on a shared host. The soft budget is not preemptive; two runs exceeded 6 s by more than 0.01 s. | Stated. | Scoped | Label all timing as descriptive. |
| EXP-A7 | `A/experiments/experiment-audit.md` | Population: the metadata predicate `nquadcons + ngennlcons > 0` excludes polynomial-only models. "Held out" means held out from two named campaigns only. | Stated. | Scoped | State the selection rule and the meaning of "held out". |
| EXP-A8 | `A/reviews/document-review.md`; `A/CLOSEOUT.md` | Automatic selection reduced candidate LPs from 1,073 to 323 and callback time from 5.59 s to 3.05 s, without recovering the baseline solve count. The native C sampling kernel was not loaded in solver runs. | Stated. | Scoped | Do not promote work reductions to solver gains. Leave the C kernel out of the contributions. |
| EXP-A9 | `A/experiments/experiment-audit.md` | Harness defects found before the freeze: partial JSON aborting the runner, missing cut logs shown as zero, incomplete source snapshot, solved counts accepting unverified incumbents, missing root-bound reference check, and an overflowing objective (`1e308` times 2) accepted as feasible. | All fixed before the freeze, with regressions. | Resolved | Mention the harness safeguards briefly. |
| EXP-B1 | `B/CLOSEOUT.md`; `B/reviews/document-review.md`; `B/reviews/document-metrics-review.md` | Campaign B: all three modes solved the same 25 of 30 new holdout models. Summed integration and preparation time was 170.57 s for baseline versus 187.02 s and 187.12 s for the cut modes. | Reported. | Scoped (negative) | Report it. Recommend native SCIP as the default. |
| EXP-B2 | `B/reviews/experiment-review.md`; `B/document/evidence.tex` | Final dual bounds: `all` 2 better / 21 tied / 7 worse; `auto` 2 / 24 / 4. On the five common unsolved cases, both cut modes had 0 better, 1 tied, and 4 worse, and **none of those cases received a cut** (for example `graphpart_clique-40`, 438 versus 392), so the losses come from overhead. Both improvements were on models already solved. Median both-solved runtime ratios: 1.87 (`all`), 1.58 (`auto`). | Reported. | Scoped (negative) | Report it. Attribute the losses to discovery and callback overhead (about 24.4 s of discovery across runs). |
| EXP-B3 | `B/experiments/campaign-v2/coverage.md`; `B/document/evidence.tex` | Low coverage: cuts on 7/30 models (`all`) and 3/30 (`auto`). Discovery found no supported blocks in 12 runs; 186 source sides were declined. | Reported; the counters do not isolate causes. | Scoped | Discuss applicability honestly. |
| EXP-B4 | `B/reviews/experiment-review.md`; `B/reviews/integration-review.md`; `B/document/COVERAGE.md` | The 75-job repair cohort was selected by defects (46 overruns and four recursion failures), not by outcomes. It is not a prospective sample. It solved 4/8 holdout and 4/7 diagnostic models in every mode, with no better bounds and worse bounds on `waterno2_06` in both cut modes. | Kept separate from the primary results. | Scoped | Present it as a regression validation. Do not splice it into the 30-model table. |
| EXP-B5 | `B/document/evidence.tex`; `B/reviews/document-metrics-review.md` | The only positive mechanism is constructed: on root-only `simplex_quadratic_vector`, both cut modes reach about `-0.50000002` versus baseline's node-limit `-0.50027374`, against an exact optimum of `-1/2`. | Labeled as a mechanism. | Scoped | Label it as a constructed mechanism. |
| EXP-B6 | `B/experiments/protocol.md`; `B/experiments/campaign-v2/environment.json`; `B/PROGRAM.md` item 5 | Runs used a 30 s budget and seed 0 for primary runs, with seed-1 repeats on only six models. The host was shared (load average about 10.8 on 36 logical CPUs at the start). The program asked for "longer runs and prespecified repeated seeds"; this was met only modestly. | Stated as descriptive. | Open (for a journal) | Either run a longer, multi-seed, independently selected study (which both closeouts say is needed for any performance claim), or present the campaigns as evidence that validity and binding hold at no benefit. |
| EXP-B7 | `B/experiments/protocol.md` | Size filter: at most 120 variables, 180 constraints, and 250,000 OSiL bytes. Large models appear only as diagnostics. | Stated. | Scoped | State the filter. |
| EXP-B8 | `B/reviews/experiment-review.md` | Harness defects before the freeze: implicit binary bounds not checked, missing validation fields passing by default, setup time not charged, partial cut logs not flagged. | Fixed before the freeze. | Resolved | Mention briefly. |
| EXP-B9 | `B/reviews/experiment-review.md` | The emergency-cap arithmetic did not guarantee completion if orchestration overhead grew. | All 282 jobs completed. | Resolved | None. |
| EXP-B10 | `B/reviews/document-review.md`; `B/reviews/document-metrics-review.md` | The abstract omitted the adverse result, the claim map was stale, and one figure was rounded to 23.612 ms instead of 23.611 ms. | Corrected and verified. | Resolved | Put the adverse result in the abstract. |
| EXP-X1 | `B/document/COVERAGE.md`; `B/reviews/document-review.md`; `B/literature/final-contribution-review.md` | The two campaigns use different implementations (auxiliary reformulation versus original-variable cuts) and different populations, so they cannot be pooled. The total of 165 replayed cuts is 123 + 42 records, not unique inequalities. Four original unknown logs remain outside the claim. | Stated. | Scoped | Report the campaigns separately. Keep the unknown logs visible. |
| EXP-X2 | `B/reviews/experiment-review.md`; `A/experiments/experiment-audit.md` | Incumbent checks are numerical residual checks (scaled `1e-5`). Transcendental functions are evaluated in floating point. Reference-bound checks do not certify SCIP's bounds. | Stated. | Scoped | Use "passed numerical original-model checks", not "feasible". |
| EXP-X3 | New | Neither campaign's `environment.json` records the SCIP library version; they record PySCIPOpt 6.2.1 only. The current environment reports SCIP 10.0 with PySCIPOpt 6.2.1 (checked here), but the version used in the archived runs is not directly recorded. | — | New | Confirm the SCIP version from archived logs or binaries and report it, together with host load. |
| EXP-X4 | Partly `A/literature/README.md` ("Baselines"); otherwise New | No other solver is compared, and native SCIP's own RLT, minor, and projection cuts are not ablated. Earlier background work reported large but uncertified Gurobi bound gains on `waterno2` from static root cuts (`results/shared-variable-term-links.md`; `research-20260922/curve-hulls/report.md`), while both SCIP campaigns show worse `waterno2_06` bounds with the new cuts. | — | Open | If the paper cites the earlier `waterno2` results, keep their caveats (BG-3, BG-4) and explain the contrast. A referee will likely ask for at least one stronger baseline. |

## Program-level requests

| ID | Raised in | Request | Outcome | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| PRG-1 | `A/PROGRAM.md` (deliverable 3) | Give precise limits on composing overlapping block hulls, and keep the obstruction if an extension fails. | Delivered as C-OVER. | Resolved | Present C-OVER as a limit result. |
| PRG-2 | `A/CLOSEOUT.md` ("remaining research boundaries") | Remaining outside Report A: wider overlapping hulls, multivariate elementary functions, arbitrary nonlinear block domains, complete normal separation, permissive domain-preserving compilation, end-to-end certification. | Report B closed complete separation for polynomial graphs (C-SEP) and broadened model admission. Multivariate elementary support, arbitrary domains, and end-to-end certification remain outside. | Partial | State what remains outside in the conclusion. |
| PRG-3 | `B/PROGRAM.md`; `B/reviews/PLAN.md` | The main experiment must wait until source semantics and cut conversion pass review. Review tests must add confidence beyond producer/checker agreement. | Freeze happened after clearance (`B/reviews/integration-review.md`); review tests use analytic optima and independent reconstruction. | Resolved | Describe the review and freeze procedure briefly as part of the evidence standard. |
| PRG-4 | `B/PROGRAM.md` item 4 | Attribute classical optimization and convexification ingredients accurately. | Done in B `literature.tex`, with the gaps listed above (AGG-5, OVER-10, OVER-11, POLY-8, IMPL-20). | Partial | Close those gaps. |
| PRG-5 | `B/CLOSEOUT.md`; `B/literature/README.md` ("How to state completion") | "Complete" means complete for the declared contracts, not that the research area is finished. | Stated. | Scoped | Avoid "complete solution" language outside the stated contracts. |

## Novelty claims N1–N6: what the record supports

| Claim | Supporting record | Limits from the issues above |
| --- | --- | --- |
| N1 (C-STAR with center–leaf rows, all curvature signs) | Proof and two independent audits (STAR-8). | The box case is in Del Pia–Khajavirad; the method is classical parametric QP; there is no priority search; trees are not covered (STAR-9, STAR-12). Claim the explicit class and algorithm only. |
| N2 (pair-hull obstruction and its quantification) | Exact witness, sharp `1/128`, expanded cut, `delta^2/2` family. | Must be positioned against Tawarmalani (2010), Lasserre (2006), Padberg (1989), Dey–Khajavirad (2025), and Khajavirad (2026) (OVER-6, OVER-8, OVER-10, OVER-11). The task text names no additional generalization beyond the `delta^2/2` family. Dense SDP with the nonedge product removes the witness (OVER-1). |
| N3 (closure characterization and gap to feasible hull) | Proof reviewed (AGG-1). | Classical Lagrangian-dual and convexification precedent, not yet cited (AGG-5). The gap example is a duality-gap instance. |
| N4 (certification contract) | Reviewed implementation, replay, and tamper controls. | Garloff–Smith, Cook et al., Eifler–Gleixner, and SCIP 10's exact MILP mode are close precedents (SUP-9, IMPL-20). Claim the combined contract only. |
| N5 (finite complete epsilon-separation) | Proof and 21 independent tests. | Elementary relative to GLS; costs are exponential; the full-dimensionality distinction is unchecked (SEP-7, SEP-9, SEP-9b). |
| N6 (source-faithful import with exact domain witnesses) | Model review: 31 tests plus a metadata audit. | No prior-art comparison exists (IMPL-20). The witness encoding is classical (IMPL-9b). Exactness holds over the reals, not for SCIP's tolerances (IMPL-9). |

## Background reviews (earlier work)

These issues concern earlier repository results that the paper may use as
motivation. They do not affect the validity of C-SUP to C-EXP.

| ID | Raised in | Issue | Resolution | Status | Paper must |
| --- | --- | --- | --- | --- | --- |
| BG-1 | `notes/review-composite-univariate-envelopes.md` | Findings 1–11: a latent local/global cut-flag bug, missing domain checks, possible hangs, a presolved domain not imposed on `x`, a fixed float shift, singular endpoints handled only at 0, inexact standalone enforcement, "exact certified" overclaims, Udell–Boyd versus Aubin–Ekeland attribution, detection gaps. | Addressed according to `results/composite-univariate-envelopes.md` (status line and limits). The note still says "values are floating point with a fixed safety shift". | Resolved (background) | Do not describe the earlier handler's cuts as certified (see BERN-4b). |
| BG-2 | `notes/review-row-hull-theory.md`; `notes/review-row-hull-code-experiments.md`; `notes/review-minlp-developments-20260922.md` | Row hulls: Theorem 2(c) omitted `0 <= z_i <= w y_i`; "weaker otherwise" was false; Kim–Tawarmalani–Richard (2022) had to be checked; the summary numbers were preliminary. In code, a floating-point duplicate-sum bug in `pricing._compress` produced invalid cuts on two-decimal data, and an endpoint-rounding bug could invalidate a pricing bound. | Bugs fixed and affected runs repeated (README lines 594–600). | Resolved (background) | Optionally cite these as concrete cases of floating-point invalid cuts that motivate a posteriori certification of the exported row. |
| BG-3 | `notes/review-shared-variable-term-links.md`; `notes/review-minlp-developments-20260922.md` | Shared-variable links: `pricing050` (a maximization) was misreported as an invalid bound; a volume was wrong (`0.1497` instead of exactly `3/20`); SCIP 10 returned a wrong, setting-dependent optimum on `waterno2_02/03`; the Gurobi bounds are uncertified single runs; `ex8_4_7` Gurobi "optimal" is infeasible by `8.7e-4`; `scan_candidates.txt` is missing. The saved `waterno2_18` point has exact violation `32325/2^49` (about `5.742e-11`). | Note corrected (`results/shared-variable-term-links.md` status). | Resolved (background) | If cited, keep "uncertified" and "single run", give the exact residual, and state the SCIP error as observed for that version and setting. |
| BG-4 | `research-20260922/curve-hulls/review.txt` | Curve hulls: the cuts are exactly valid, but stale artifacts remain. The saved `_06`/`_09` cuts used an earlier scaling (131 of 673 `_06` cuts act on rescaled variables), the seed-0 cut files for `_12/_18/_24` were overwritten, and "7–67" should read "6.7–67". | Corrections section and regenerated runs added to `report.md`. One stale "7–67" remains at `report.md` line 297. | Resolved, one wording residue | If cited, use the regenerated seed-0 runs and "6.7–67". The bounds are uncertified Gurobi output. |
| BG-5 | `README.md` lines 8–22 | The repository overview keeps native SCIP as the default and states that cut certificates do not certify a complete SCIP solve. | Consistent with both closeouts. | Resolved | Keep the same conclusion in the paper. |

## Checks run for this record

These are targeted local checks run while compiling this record. They are not
CI results, and no project-wide verification was run.

1. SCIP library version in the project environment:

   ```sh
   code/minlp_solver_lab/.venv/bin/python -c "import pyscipopt; m=pyscipopt.Model(); m.hideOutput(); print(pyscipopt.__version__, m.version())"
   ```

   Output: `6.2.1 10.0`. This shows the current environment only, not the
   version used in the archived campaigns (EXP-X3).

2. Exact check for POLY-8 and OVER-11, run with SymPy from the same
   environment through standard input. It confirmed:
   - the identity `(x - X11 - X12) + (y - X12 - X22) = x + y - (X11 + 2X12 + X22)`;
   - at the half-mass point (all lifted coordinates `1/2`), each RLT product
     equals `-1/2` and their sum equals `-1`;
   - `max_{t in [0,1]} (t - t^2) = 1/4`;
   - the square coefficients of the reduced overlap certificate (3) are
     `(0, 2, 0)` for `(x, y, z)`.

   Output: `RLT sum equals target: True`, `target at half-mass point: -1 r1: -1/2 r2: -1/2`,
   `max of x - x^2 : 1/4`, `square coefficients x^2,y^2,z^2: 0 2 0`.

3. Text searches with `grep` over `literature/index.md` and selected
   `KB/*/fulltext.md` files (Kerdreux et al. 2023, Udell–Boyd 2016,
   Padberg 1989, Dey–Khajavirad 2025, Khajavirad 2026, Hojny et al. 2025,
   Bhathena et al. 2025, Del Pia–Khajavirad 2026). PDF page locators come from
   the `<!-- page N -->` markers. A search that finds no example is not proof
   that none exists (OVER-11).

No file under `research-2026100*-convexification/` or `literature/` was
modified.
