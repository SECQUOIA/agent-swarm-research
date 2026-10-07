# Report (lit-ext): prior work for conditional recourse, constraints, optimal sets and structural limits

Date: 2026-10-03. Companion files: `lit-ext.md` (related-work memo with locators),
`lit-ext.bib` (verified bibliography), `lit-ext-proofs.tex` (statements and complete proofs of
the classical facts the paper should state, one new theorem and one corollary, and a draft
related-work section), `checks/` (exact-arithmetic checks listed at the end).

## Verdict

No source found invalidates a main claim of the paper. Several extension results are, however,
presented with too little attribution, and two of them are close to specific older results that
the report does not cite:

- The optimal-set identity for coordinatewise concave box QPs is Rosenberg's 1972 face criterion
  (for multilinear functions) combined with the classical zero-residual description of
  tree-structured discrete optima. It must be presented as such.
- The convex value-factor construction is closest to Khajavirad's 2026 elimination of
  positive-diagonal components into value functions of their neighbors (arXiv:2604.25033), which is
  not cited at all. The differences (continuous gridded neighbors, curvature certificate, growth)
  are real and should be stated.

Everything else is correctly scoped as composition, but some citations should change (list below).
The audit also produced one new, fully proved result that fits the paper's story well: the
corrected-grid algorithm does not need a tree decomposition when the quadratic is balanced
(submodular after sign changes); one minimum cut per value replaces the messages, giving
polynomial dependence on n, kappa, I and q without any width parameter (Theorem
"Balanced box quadratics without a width parameter" in `lit-ext-proofs.tex`).

## Issues

Severity scale: critical (invalidates a main claim), major (a proof gap, a wrong statement, or a
missing attribution that changes the novelty claim), minor (wording, constant or citation fix).

| ID | Severity | Location in the report | Issue | Fix (verified) |
| --- | --- | --- | --- | --- |
| I1 | major | extensions.tex, "Changing active sets without explicit value-function pieces"; also "An exact cut oracle..." | Khajavirad, *A polynomial-time solvable class of sparse box-constrained polynomial optimization problems*, arXiv:2604.25033v2, is uncited. Its Theorem 1 (p.4) and proof (pp.8--10) eliminate positive-diagonal continuous components into value functions over neighbor labels, its Lemma 1 (p.7) is the hidden-binary endpoint reduction, and its Lemma 2 (pp.7--8) uses the PSD-deletion parameter. Del Pia--Khajavirad cite it as [22] and restate it as their Theorem 5. | Cite it in the value-factor and cut-residual paragraphs, with the wording proposed in `lit-ext.md` Section 2. The differences were checked against the primary text: binary enumerated neighbors and logarithmic treewidth there; continuous gridded neighbors, concavity-based curvature certificate and growth-conditioned filtering here. |
| I2 | major | extensions.tex, "Compact descriptions of nonunique optimal sets", first result | The identity is presented as recording "their full-set certificate" without citing Rosenberg (1972), whose Lemma and Proposition 1 (printed p.96) characterize the optimal set of a multilinear function on a box as the union of faces whose vertices are optimal. | Cite Rosenberg1972, Werner2007 (Theorem 4) and WainwrightJaakkolaWillsky2005 (Proposition 1). Restate the result as the face criterion of Proposition "Face criterion" in `lit-ext-proofs.tex` (complete proof; exact check `litext_check_optimal_sets.py` part B). New content: strictly concave coordinates, mixed boxes, factored certificate. |
| I3 | minor | same section, second result | Li--Wu--Quan (2015) is called "classical"; earlier related conditions exist (Beck--Teboulle 2000, Theorem 2.3; Jeyakumar--Rubinov--Wu 2006). The invariance across optima and the full-set description are the classical zero-duality-gap/saddle-point facts (Mangasarian 1988 for the convexified Lagrangian). The report's invariance proof is correct but does not mention the case in which an optimum sits at the opposite endpoint. | Use the wording in `lit-ext.md` Section 5 and the proof of Proposition "Diagonal Lagrangian certificate" in `lit-ext-proofs.tex`, which treats that case (the gradient identity gives the same entry). Exact check part A passed. |
| I4 | minor | "An exact cut oracle..." | Only Kolmogorov--Zabih is cited for the cut reduction. The sign-switched class is classical (Ivanescu/Hammer 1965; Picard--Ratliff 1975; Padberg 1989 Props. 9--10, printed p.162; Boros--Hammer 2002; Harary 1953 balance; Hammer--Hansen--Simeone 1984), and Burer--Natarajan--Willemsen v3 (pp.2--3) record that the coordinatewise-concave submodular box QP is polynomial. | Add these citations; state that the contribution is the box-stable certified oracle and its composition with core search. |
| I5 | minor | same section, mixed submodular recourse | The greedy-base certificate is credited to Iwata--Fleischer--Fujishige, who credit it to Cunningham (1984, 1985) and the greedy rule to Edmonds (1970) (IFF p.5, printed p.765). | Cite Cunningham1985 and Edmonds1970 as well. |
| I6 | minor | "A complete reduction for certified affine convex recourse" and "Local pieces..." | Bemporad et al. is cited for fixed-active-set responses with possibly singular C; their Theorem 2 (p.6, printed p.8) assumes H positive definite and linearly independent active constraints. | Add Spjotvold--Tondel--Johansen (2005/2007) and Patrinos--Sarimveis (2011) for PSD blocks; cite Mangasarian (1988, Lemma 1 and Cor. 1) for "all central minimizers have the same gradient". |
| I7 | minor | "A complete extension for integral TU fibers" | Box integrality is attributed to the Chervet--Grappe--Robert preprint, which restates Hoffman--Kruskal (Theorem 4.4, p.11). The preprint was published with a different title (Math. Prog. 188 (2021) 319--349). | Cite HoffmanKruskal1956 (and Schrijver1986); if the preprint is kept, cite the published version. Marginal-preserving rounding: GandhiEtAl2006, ChekuriVondrakZenklusen2010. Proof in `lit-ext-proofs.tex`, Lemma "Corner rounding". |
| I8 | minor | "Polynomial boundary output with an explicit margin" | The sign test is the classical monotonicity test of interval global optimization; active-set identification under strict complementarity is classical in local optimization. Only Araya et al. is cited. | Cite Hansen1980 or HansenWalster2004, and BurkeMore1988 / FacchineiFischerKanzow1998; Garloff1986 for Bernstein bounds. |
| I9 | minor | references.bib | Khajavirad2026SparseSDP uses an Optimization Online URL; arXiv:2601.18545v2 (2026-02-12) is the same version. GomezHan2025 author order: the PDF says Gomez, Han (arXiv metadata lists Han first). Vavasis1990 is unread; Khajavirad's Proposition 2 (p.7) attributes the minimum-face positive-definiteness argument to it. | Replace with entries in `lit-ext.bib`. |
| I10 | minor | "The precise conditional-recourse interface" and value-factor concavity | The semiconcavity and value-function concavity facts are classical; terminology "upper coordinate curvature" should be linked to semiconcavity with linear modulus. | Lemma "Infima preserve concavity and coordinate curvature" in `lit-ext-proofs.tex`, with citations MangasarianRosen1964, FiaccoKyparisis1986 (secondary check), CannarsaSinestrari2004 (secondary check). |
| I11 | minor | "Negative curvature" and "A conditional-moment obstruction" | Context a referee will expect is missing: PSD completion is automatic for chordal patterns (Grone et al. 1984), sparse moment relaxations (Lasserre 2006, Waki et al. 2006), local versus global consistency (Sherali--Adams; Wainwright--Jordan), exponential parametric complexity (Murty 1980; Gartner--Jaggi--Maria 2012). | Add one sentence each (draft in `lit-ext-proofs.tex`, Section E). |
| I12 | minor | smoothed count | The smoothed-analysis lineage is not cited in the extension (only in earlier audits). | Cite SpielmanTeng2004, BeierVocking2006, RoglinVocking2007; MulmuleyVaziraniVazirani1987 for discrete uniform weights. |

No critical issue was found. The mathematical statements checked against their literature sources
(signs, constants and quantifiers in the cut identity, the diagonal certificate identity and its
invariance, the face criterion, TU rounding variance and error, the smoothed interval length
L h_j (1 + k/2), and the growth transfer to the affine response metric) are correct.

## What is classical and what is new

| Result | Classical (closest prior) | New, as far as the checked literature shows | Recommended placement |
| --- | --- | --- | --- |
| Affine convex recourse identity, reduced Hessian | mp-QP (BemporadEtAl2002 Thm 2; SpjotvoldTondelJohansen2005/2007; PatrinosSarimveis2011); Schur complement | Global curvature certificate for the reduced objective with unchanged scopes; induced-metric growth transfer; the L_red versus nu separation | Main text, short proposition (shows that stiff convex energy can be removed exactly) |
| Affine-selector recognition (central QP + LP) | Critical-region LP; Mangasarian1988 constant gradient | Whole-box test including singular C | Remark; proof in an appendix or omit |
| Curvature across a certified partition | Concave kinks (DelPiaKhajavirad2026 p.5); value concavity | The bound max_r (H_r)_jj without global overlay | Main text, together with the value-factor result (one proposition); example f_M as an example environment |
| Convex value factors | Khajavirad2026PolyBox (binary neighbors); MangasarianRosen1964/FiaccoKyparisis1986 | Continuous gridded neighbors with certified curvature | Main text, merged with the previous row |
| Conditional-recourse interface | Semiconcavity under infima (CannarsaSinestrari2004) | The explicit local-error budget statement | Main text (short); it frames the cut oracle |
| Cut residual oracle (concave diagonals) | Rosenberg1972; Ivanescu1965; PicardRatliff1975; Padberg1989; KolmogorovZabih2004; BNW v3 | Box-stable certified contract; composition with core search | Main text as an instance of the interface, one paragraph |
| Mixed submodular recourse | GomezHan2025; BuntonTabuada2022; Topkis1978; Cunningham1985; IwataFleischerFujishige2001 | Interface (endpoint-concave + PSD block), exact certificate contract | Remark with citations; drop the long proof |
| Smoothed core-cell count | Smoothed analysis lineage; isolation lemma | Count of near-optimal continuous core cells under finite uniform noise | Appendix (different model; dilutes the main story) |
| NEW: balanced quadratics without width (and with a supplied core) | Threshold cut encoding (SchlesingerFlach2006; Ishikawa2003); discretization of continuous submodular minimization (Bach2018Isotonic; Bach2019; AxelrodLiuSidford2020) | Growth-conditioned certified algorithm polynomial in n, kappa, I, q for dense balanced QPs; core version removes the nonpositive-diagonal restriction | Main text, as a corollary showing that the method needs an exact grid oracle, not a tree decomposition |
| TU fibres | HoffmanKruskal1956; dependent rounding; BienstockMunoz2018 | Exactly feasible growth-filtered grids with accuracy-independent state count | Main text (the paper's constraint section); union-of-cells variant to an appendix |
| Endpoint optimal set | Rosenberg1972; Werner2007; WainwrightJaakkolaWillsky2005 | Strictly concave coordinates, mixed boxes, factored certificate | Remark or short proposition with attribution |
| Diagonal certificate and discovery | LiWuQuan2015; BeckTeboulle2000; JeyakumarRubinovWu2006; Mangasarian1988; LuoSturm2000 | Discovery under untrusted conditioning guesses with exact acceptance | Remark; appendix for the discovery procedure |
| Boundary active faces | Hansen1980; ArayaTrombettoniNeveu2010; BurkeMore1988; FacchineiFischerKanzow1998 | Explicit precision term B_gamma from a global enclosure | Appendix or drop |
| Conditional-moment obstruction | PSD completion (GroneEtAl1984); moment relaxations | The explicit uniformly conditioned family | Short "limits" subsection; verification details to an appendix |
| DPK hardness has nu/g >= 4B | DelPiaKhajavirad2026 Thm 3 | The conditioning observation | Main text, one paragraph (it positions the main theorem) |

## Open questions in this cluster and what the development produced

1. **Is a tree decomposition essential to the certified grid method?** Resolved for one structure.
   The proofs of the corrected-grid lemmas use the decomposition only to compute the grid minimum
   and min-marginals. For balanced quadratics these are minimum cuts on threshold encodings of the
   grids (Lemma "Grid minimization by one minimum cut"; complete proof). This yields Theorem
   "Balanced box quadratics without a width parameter": certified 2^{-q} approximation in
   (n kappa (I+q+1))^{O(1)} and exact output in (n kappa (I+1))^{O(1)} bit operations under
   unique-point growth, with no width parameter, and Corollary "Balanced after deleting a supplied
   core" (work multiplied by K^k), which removes the report's restriction to nonpositive residual
   diagonals. Evidence: exact checks below, including the report's own solver run with the cut
   oracle substituted in memory on dense indefinite instances with one bag of all variables.
   Limitation: polynomial in kappa, not in log kappa; it does not settle the open complexity of
   continuous submodular box QP for n >= 4 (Burer--Natarajan--Willemsen v3, footnote 2, p.3).
   I did not find an argument that improves the kappa dependence; the retained-label bound
   O(sqrt(kappa) log n) per coordinate is what the analysis gives.
2. **Is the endpoint optimal-set certificate new?** Sharpened negatively. It is Rosenberg's face
   criterion plus reparameterization. The proof in `lit-ext-proofs.tex` is shorter and states the
   criterion in the form a reader will recognize ((a) endpoints for strictly concave coordinates;
   (b) all vertices of the minimal face optimal; (b) equivalent to zero residuals on the projected
   faces).
3. **Is the invariance of the diagonal certificate across optimal components new?** No. It is the
   zero-duality-gap property of the convexified Lagrangian; the full optimal set is a Mangasarian
   polyhedral description. Complete direct proof given, including the opposite-endpoint case.
4. **Is affine-selector recognition known?** Partly. For strictly convex blocks it is the classical
   test that one critical region contains the box. For singular blocks the constant-gradient
   property (Mangasarian 1988) is the key fact; no source stating the whole-box LP test for
   singular blocks was found. Recommendation: keep as a remark without priority claim.
5. **Does the mixed submodular oracle add a tractable class?** No. It is the Gomez--Han /
   Bunton--Tabuada mechanism with a different interface; Gomez--Han's Theorem 3 (p.15) already
   uses sign changes to reach the Stieltjes case. The certificate contract is the contribution.
6. **Closest prior for the TU extension?** None found that is exactly feasible and growth-filtered;
   Bienstock--Munoz is broader but approximate in feasibility. Rounding needs only Hoffman--Kruskal
   and Caratheodory (proof given).
7. Not resolved: whether the growth-conditioned grid method extends to sign-structured
   *polynomials* of higher degree. The threshold encoding turns a cubic term into triple
   interactions of binary threshold variables (and a term such as x_i^2 x_j into products of two
   thresholds of the same chain with one of another). Such binary cubic functions are
   cut-representable when they are regular in the sense of Kolmogorov--Zabih (Theorem 5.3, p.6),
   which imposes sign conditions on every projected pair, not only on the original coefficients.
   I did not determine a natural polynomial class for which this holds for all grids, so no claim
   is made.

Attempts that failed for access reasons (not mathematical): Li--Wu--Quan 2015 (Springer blocked
automated download; the ledger locator is used), Fiacco--Kyparisis 1986, Ishikawa 2003,
Picard--Ratliff 1975/1980, Grone et al. 1984, Topkis 1978 full texts. These are cited only through
the statements recorded in `lit-ext.md`.

## Verification record (targeted, local)

All commands were run from `/workspace/minlp-notes/paper-decomposition-aware/process/w1/checks`
with exact rational arithmetic; each run took under a minute. No project-wide verification or CI
inspection was performed, and these finite checks support but do not replace the proofs.

- `python3 litext_check_balanced_grid_cut.py 300`: PASS. 300 random balanced quadratics
  (n <= 5, random nonuniform grids, arbitrary unary terms): the cut construction of Lemma
  "Grid minimization by one minimum cut" returned the brute-force grid minimum, a minimizer, and
  all min-marginals of one coordinate per instance (3575 grid labels in total).
- `python3 litext_check_optimal_sets.py 300`: PASS. (A) 300 random box QPs with a diagonal
  certificate (including rank-deficient H + D): identity, full-set description and invariance of D
  at all grid points (3202 optimal grid points). (B) 300 random coordinatewise concave box QPs:
  interpolation identity and face criterion at all grid points (589 optimal grid points).
- `python3 -B litext_demo_balanced_solver.py 8 6 strong`, `... 8 6 mild`, `... 3 8 mild`: PASS.
  The report's reference solver `research-20261002-decomposition/solver/certified_grid.py` was
  imported read-only and its `grid_dp` replaced in memory by the cut oracle; dense balanced
  indefinite QPs (lambda_min between -1.95 and -19.5) with a single bag of all variables were
  certified to gap <= 1e-6, and every certified interval contained the optimum computed by
  independent 3^n face enumeration. The largest last-stage grid product was 59049 (n = 8), which a
  single-bag table would have to enumerate; the cut graphs had at most a few dozen nodes.
- LaTeX: `lit-ext-proofs.tex` was compiled in a scratch wrapper with stand-in labels for the main
  paper's references, together with `lit-ext.bib` (pdflatex + bibtex): no undefined citations or
  references, no BibTeX warnings.
- Bibliography: metadata of DOI-bearing entries was checked against Crossref with
  `litext_crossref.py`; arXiv entries against the arXiv API; Gartner--Jaggi--Maria against DOAJ.
  Unverifiable fields (series volume numbers, some page ranges) were removed rather than guessed.
- `litext_findpage.py` was used to attach page locators to statements in local full texts.

Downloaded primary PDFs and the LaTeX test build were kept in a scratch directory outside the
repository and deleted after the audit; they are not part of the outputs.

## Cross-cluster notes

- Rosenberg (1972) and Werner (2007), listed as "not checked" in `optsets-report.md`, were read in
  this audit: Rosenberg's Lemma and Proposition 1 are on printed p.96 of RAIRO 6(V2):95--97
  (numdam scan); Werner's Section III-D and Theorem 4 are on p.6 of the author version. Both
  support the optimal-set attributions above.
- Khajavirad (arXiv:2604.25033v2), recorded at abstract level in `lit-core.md`, was read in full
  here; the locators in `lit-ext.md` Section 2 (Theorem 1 p.4, Lemma 1 and Proposition 2 p.7,
  Lemma 2 pp.7--8, proof pp.8--10) can be reused by that cluster. Its Proposition 2 attributes the
  minimum-face positive-definiteness argument to Vavasis (1990).
- Del Pia--Khajavirad also cite Qiu and Yildirim, *J. Global Optim.* 90 (2024) 293--322, on exact
  RLT and SDP-RLT relaxations of box QPs (reference [33], read in their bibliography only), which
  is relevant to the Shor-exactness remark in `optsets-report.md`.
