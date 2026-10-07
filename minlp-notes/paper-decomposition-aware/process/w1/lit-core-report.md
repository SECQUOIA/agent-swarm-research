# lit-core report: prior work for certified grids, filtering, conditioned complexity and exact output

Date: 2026-10-03. Scope: the literature positioning of the report's
Sections 1-5 (`research-20261002-decomposition/document/main.tex`): the
corrected-grid lower bound, min-marginal filtering, the accuracy-independent
state bound and `f(p,kappa) poly(I+q)` theorem, and exact rational output.
Detailed locators are in `lit-core.md`; checked BibTeX in `lit-core.bib`;
paper-ready statements and proofs in `lit-core-proofs.tex`.

## Verdict

No source found invalidates a main claim. The main theorem — a certified
algorithm for rational mixed-integer box QPs with running time
`f(p,kappa) poly(I+q)`, and exact output in `f(p,kappa) poly(I)`, without
knowing the growth constant — was not found in the literature after
searches with many phrasings (log in `lit-core.md`, Sec. 9). It can be
presented as new with "to our knowledge".

The ingredients are not new, and the report currently understates this.
Three attributions are missing and one is substantive:

1. The per-cell lower bound behind the "unary interpolation correction" is
   the edge-concave vertex bound of Bajaj and Hasan (Optim. Lett. 2020,
   Theorem 1), with the alphaBB separation constant. The report's
   contribution there is the node-separable form, which I prove equals the
   best cell bound over the whole product grid (new Proposition
   `prop:lc-cellwise`).
2. Accuracy-independent box counts under second-order bounds and quadratic
   growth are the known "cluster problem" phenomenon of branch and bound
   (Du-Kearfott 1994; Neumaier 2004; Wechsung et al. 2014; Kannan-Barton
   2017), and exponential rates under matched growth are known in optimistic
   optimization (Munos 2011). The report's version is global,
   non-asymptotic and treewidth-parameterized; that is the novelty.
3. The rational-height lemma reproduces Vavasis's 1990 argument, and the
   filter is optimality-based bounds tightening/probing computed by
   min-marginals.

I also add a complexity-theoretic complement: unless P = NP, no algorithm
achieves `poly(I+q)` at treewidth two (Proposition `prop:lc-necessity`), so
some conditioning parameter is necessary; NP-hardness reductions at
treewidth two must produce non-unique or super-polynomially ill-conditioned
instances (Corollary `cor:lc-illconditioned`). With the ETH remark
(`rem:lc-eth`), both parameters of `f(p,kappa)` are shown to be necessary.

## Issues and fixes

Severity: critical = invalidates a main claim; major = wrong or missing
statement needing a real fix; minor = easily fixed.

| # | Severity | Issue | Fix (verified) |
|---|---|---|---|
| M1 | major | Abstract, Sec. 1 and Lemma 3.1 (`lem:round`) present "a unary interpolation correction makes finite-state DP a valid continuous lower bound" without prior art. The per-box inequality `F >= min_vertices F - (L/8) sum Delta_i^2` under an upper bound on diagonal Hessian entries is Bajaj-Hasan 2020 Thm 1 (edge-concave underestimator; Hasan 2018; vertex polyhedral envelopes, Tardella 2004, Meyer-Floudas 2005; separation constant of alphaBB, Adjiman et al. 1998 p. 1141). | Cite these. Replace the claim by: the node-separable correction computes `min_C beta(C)` over all cells of the product grid in one tree DP (Prop. `prop:lc-cellwise`(b)); proof is complete in the fragment and checked exactly on 240 random instances (`checks/lit_core_cell_equivalence.py`). Optionally replace the randomized proof by the deterministic one (part (a)). |
| M2 | major | Sec. 4 ("Why filtering removes the accuracy exponent", `sec:rate`) gives no comparison with the branch-and-bound cluster problem, where second-order bounds and a nondegenerate minimizer already give tolerance-independent box counts (locally, exponential in `n`). A referee from global optimization will raise this. | Add the paragraph "Accuracy-independent work under growth" (fragment, Sec. `sec:lc-related`) and state the difference: global non-asymptotic contraction; coordinatewise hulls with `K = O(sqrt(kappa) log n)` per coordinate and `K^p` per bag instead of `(C sqrt kappa)^n` boxes; bit-complexity statement. |
| M3 | major | Lemma 5.1 (`lem:height`) is Vavasis's argument (TR 90-1099, Sec. 2: optimizer with most active constraints, positive definite reduced Hessian, Edmonds), restated by Del Pia-Dey-Molinaro 2017 Thm 3; Lemma 5.2 (uniqueness implies growth) is standard second-order QP theory (Contesse 1980) plus compactness; continued-fraction reconstruction is GLS 1988 Thm 5.1.9. The report cites Vavasis only in the bibliography, without attribution in the text. | Attribute in the text ("the proof follows Vavasis [..]"), keep the explicit constants (they are needed for the bit bound), and present Lemma 5.2 as standard. Present Theorem 5.3 (`thm:exact`) as a corollary that composes classical tools with Theorem 4.4 (`thm:approx`). |
| M4 | major | Proposition 3.2 (`prop:filter`) and the "certificate" paragraph read as a new filtering principle. The rule is optimality-based bounds tightening / aggressive bounds tightening (Belotti et al. 2009 Sec. 4.3), branch-and-reduce (Ryoo-Sahinidis 1996; Puranik-Sahinidis 2017 pp. 11-14), cost-based filtering and dead-end elimination (incl. continuous rotamers, Gainza et al. 2012); min-marginals by two passes (Wainwright et al. 2005 Sec. V.A; Kohli-Torr 2006); history certificates as in VIPR (Cheung et al. 2017). | Cite and state that the filter is classical; the new content is the localization lemma (retained hull radius `O(sqrt(n kappa) h)`). |
| M5 | major | Missing comparison with dynamic programming over coarse continuous states with optimistic costs: coarse-to-fine DP (Raphael 2001, incl. a continuous version with convergence under a unique optimum) and interval convex max-product (Peng et al. 2011). Both obtain valid DP lower bounds for continuous problems from cells and refine adaptively. | Add the paragraph "Dynamic programming with coarse states" (fragment). Difference: those methods bound each cell or superstate pair by problem-specific minimization or interval evaluation and have no rate; the corrected grid uses one global curvature constant, node-unary terms, and a growth-based state bound. |
| m1 | minor | The retention test `min{m_i(a), m_i(a^+)} <= U` can be sharpened at no cost to `min_v (m_i(v)+d_i(v)) - L Delta_i(I)^2/8 <= U` (Prop. `prop:lc-cellwise`(c)). It keeps both properties used by Lemma 4.2 (`lem:localize`). | Optional; Remark `rem:lc-cellwise` gives the argument. |
| m2 | minor | A single `L = max_i max(H_ii,0)` is used. Coordinate-specific `L_i` work verbatim; coordinates with `H_ii <= 0` then need only their two endpoints, which recovers the Del Pia-Khajavirad endpoint reduction inside the grid method. | Remark `rem:lc-coordinate-L`; checked exactly (per-coordinate mode of the check script). |
| m3 | minor | Del Pia-Khajavirad use `kappa` (their Lemma 20) for a different quantity. | Footnote if both are discussed. |
| m4 | minor | The report's positioning against Bienstock-Muñoz omits that they prove the `1/eps` dependence cannot be made polylogarithmic in their constrained model unless P = NP (preprint p. 2 and App. A); Vavasis 1992 and Del Pia 2026 make the same point for fixed negative inertia. This is the natural foil for the report's `log(1/eps)` rate. | One sentence plus Prop. `prop:lc-necessity`. |
| m5 | minor | Bhathena et al. already parameterize an exact treewidth DP by conditioning (convex indicator QP). Any claim "first conditioning-parameterized treewidth algorithm" must be restricted to nonconvex or mixed-integer box QPs. | Wording in the related-work draft. |
| m6 | minor | Internal notes: Kohli-Torr DOI in `prior-art/minmarginal-prior.md` is wrong (correct: 10.1007/11744047_3); "Kuhn" should be "Kuhnke" (Gupte et al. 2022); Beach et al. 2022 vs 2024 author lists; Peng et al. official ICML title; Vavasis 1990 full text is in fact available (Cornell TR 90-1099). | Use `lit-core.bib`. Research files were not edited. |

## Classical versus new

| Item | Classical (with source) | New (to our knowledge) |
|---|---|---|
| Cell lower bound `min_vertices F - L sum Delta^2/8` | Bajaj-Hasan 2020 Thm 1; Hasan 2018; alphaBB separation (Maranas-Floudas 1994; Adjiman et al. 1998); interpolation error of squares in sawtooth relaxations (Beach et al. 2024) | Node-unary form; identity `beta = min_C beta(C)` making one tree DP compute the best cell bound; integer unit intervals; conditional/interval version |
| Finite-grid tree DP, min-marginals, argmin recovery | Bertelè-Brioschi 1972; Lauritzen-Spiegelhalter 1988; Dechter 1999; Aji-McEliece 2000; Wainwright et al. 2005 | none |
| Incumbent-based filtering and history certificate | OBBT/ABT (Belotti et al. 2009), branch-and-reduce, cost-based filtering, DEE, VIPR | Localization of retained coordinate hulls under global growth |
| Tolerance-independent work under growth | Cluster problem (Du-Kearfott; Neumaier; Wechsung et al.; Kannan-Barton); Munos 2011; Perevozchikov 1990 | Global, non-asymptotic, coordinatewise version; `K = O(sqrt(kappa) log n)` per coordinate; `f(p,kappa) poly(I+q)` bit bound for mixed-integer box QP; trial schedule without `g` |
| Not knowing the growth constant | Restarts (Roulet-d'Aspremont 2020); SOO (Munos 2011) | Capped trials that keep the worst-case work bounded |
| Large integer domains at logarithmic cost | Proximity/scaling (Hochbaum-Shanthikumar 1990; Hunkenschröder et al. 2026; Eisenbrand et al. 2025) for separable convex IP | Nonseparable nonconvex objectives on boxes under growth |
| Rational height, continued fractions, value lattice | Vavasis 1990; Del Pia-Dey-Molinaro 2017; GLS 1988 Thm 5.1.9; Kozlov-Tarasov-Khachiyan 1980 | Composition giving exact output in `f(p,kappa) poly(I)` without `g` |
| Necessity of the parameters | Del Pia-Khajavirad 2026 Thm 3; ETH (Impagliazzo-Paturi-Zane 2001) | Prop. `prop:lc-necessity`, Cor. `cor:lc-illconditioned` (short consequences, proved here) |

## Placement

- Prop. `prop:lc-cellwise` (cellwise identity): main text, Section 3, right
  after the definition of the correction. It both attributes the inequality
  and states the contribution precisely. Its part (a) can replace the
  randomized proof of Lemma 3.1; part (c) can replace or sharpen the
  conditional bound `eq:conditional`.
- Remark `rem:lc-coordinate-L`: main text, short remark.
- Prop. `prop:lc-necessity` and Cor. `cor:lc-illconditioned`: main text,
  right after Theorem 4.4 (`thm:approx`), as the lower-bound
  companion; the corollary also replaces the report's informal statement
  that the Del Pia-Khajavirad hardness "does not dominate" the conditioned
  theorem.
- Remark `rem:lc-eth`: one sentence after the corollary, or a footnote.
- Related-work subsection: Section 1 or a dedicated Section 2 of the paper.
  The draft in the fragment is about one and a half pages; trim the DCOP and
  protein-design items first if space is short.
- Lemma 5.2 (uniqueness implies growth): appendix, labelled standard.
- The finite-exact-recovery theorem without uniqueness (report Thm 5.5,
  `thm:generalfinite`)
  has no complexity content and its prior art is the same height
  machinery; appendix or drop (decision belongs to the exact-output cluster).

## Open questions in this cluster and what was attempted

1. **Does prior work already prove a treewidth-plus-conditioning FPT
   result for continuous or mixed box QP?** Searched with about twenty
   phrasings (Google-style web search, arXiv/Optimization Online pages,
   publisher abstracts, Crossref). Not found. Closest: Bhathena et al. 2026
   (convex indicator QP, conditioning, margin, volume growth), Del Pia-
   Khajavirad 2026 (forests exact; width two hard), Khajavirad 2026
   (structural classes), Eiben et al. 2019 (bounded domains), Bienstock-
   Muñoz 2018 (`1/eps`). Result: negative search; supports "to our
   knowledge".
2. **Is a certified grid lower bound of this exact type known?**
   Succeeded in sharpening: the per-cell bound is known (Bajaj-Hasan 2020);
   the node-separable/tree-DP form was not found, and I proved it equals the
   best per-cell bound over the whole product grid (Prop.
   `prop:lc-cellwise`(b)). Exact check: 240 random rational instances with
   nonuniform grids, mixed integer/continuous coordinates, uniform and
   per-coordinate curvature; identities (b), (c) hold exactly and
   random-point validity checks pass.
3. **Is conditioning necessary for a `poly(log 1/eps)` rate at bounded
   width?** Resolved, conditional on P != NP: Prop. `prop:lc-necessity`
   (complete proof from Del Pia-Khajavirad Thm 3 and the rational height
   bound). Consequence (Cor. `cor:lc-illconditioned`): NP-hard width-two
   families must be non-unique or super-polynomially ill-conditioned. This
   explains, rather than merely observes, the earlier internal finding that
   the Del Pia-Khajavirad construction has exponentially large `L/g`.
4. **Is the exponential dependence on `p` necessary?** Yes under ETH, by
   the trivial embedding of maximum independent set as a binary QP with a
   one-bag decomposition (Remark `rem:lc-eth`). Not attempted: a lower bound
   on the dependence on `kappa` at fixed `p` (for example, whether
   `kappa^{Omega(p)}` is necessary). I see no route without a new hardness
   construction that controls growth; this remains open.
5. **Could the cluster-problem literature already imply the main theorem
   by combining box branch and bound with edge-concave bounds?** No: those
   analyses bound boxes in all `n` dimensions jointly, giving counts
   exponential in `n`, and are asymptotic. The coordinatewise hull plus
   tree DP is the step that is not in that literature.

## Verification actually run (targeted, local)

- `python3 checks/lit_core_cell_equivalence.py` → `PASS: 240 random
  instances` (about 5 s). Exact `fractions.Fraction` arithmetic. Supports,
  does not replace, the proof of Prop. `prop:lc-cellwise`.
- LaTeX compile of `lit-core-proofs.tex` inside a stub document with
  `lit-core.bib` (pdflatex + bibtex in `/tmp`): no errors, no undefined
  citations; bibtex reports no warnings.
- Bibliography: 98 entries, no duplicate keys, balanced braces; DOIs checked
  against Crossref, arXiv records against arXiv abstract pages.
- No project-wide verification, no CI inspection, no edits to research or
  literature files.
