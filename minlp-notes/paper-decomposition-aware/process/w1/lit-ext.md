# Related-work memo (lit-ext): conditional recourse, constraints, optimal sets, structural limits

Audit date: 2026-10-03. Scope: the extension results of the report
`research-20261002-decomposition/document/extensions.tex` (sections "Negative curvature",
"A complete reduction for certified affine convex recourse", "Changing active sets without
explicit value-function pieces", "Local pieces can preserve curvature cancellation", "The precise
conditional-recourse interface", "An exact cut oracle for a large nonconvex residual", "A complete
extension for integral TU fibers", "Nonunique TU minima", "Compact descriptions of nonunique optimal
sets", "Polynomial boundary output with an explicit margin") and the limits discussed there.
Bibliography: `lit-ext.bib` (keys below). Proofs of the classical facts the paper should state, and
of the new corollary found in this audit, are in `lit-ext-proofs.tex`.

## How the sources were checked

- "Read" means the statement was checked in the primary text during this audit (local knowledge
  base `literature/papers/<slug>/fulltext.md`, or an open primary PDF downloaded to a scratch
  directory). Page numbers are PDF pages unless "printed p." is given.
- "Ledger" means the locator comes from the 2026-10-02 source ledger
  (`research-20261002-decomposition/literature/source-ledger.md`) and was not re-opened.
- "Secondary" means the statement was checked only through another paper that quotes it (named).
- "Metadata only" means authors, title, venue, year, volume and pages were checked (Crossref, arXiv
  API, or DOAJ) but the text was not read. No theorem number or page is attributed to such a source.
- Searches: arXiv/Crossref/Semantic Scholar APIs and web search with several phrasings per topic
  (for example "affine optimal response parametric QP whole box", "convex value function concave
  in linear parameter", "submodular quadratic box polynomial", "continuous submodular minimization
  discretization", "optimal set multilinear box faces", "box QP global optimality diagonal
  multiplier", "solution set convex quadratic constant gradient", "dependent rounding totally
  unimodular", "PSD completion chordal", "regularization path exponential"). Failed searches do not
  establish novelty.

## Summary table

| Contribution in the report | Closest prior (key) | Relation | Threat |
| --- | --- | --- | --- |
| (1a) Affine convex recourse: exact PSD/KKT identity, reduced Hessian, metric growth transfer, reduced curvature parameter | BemporadEtAl2002 Thms 2, 4; SpjotvoldTondelJohansen2005/2007; PatrinosSarimveis2011; Schur complement / condensing | Fixed-active-set affine maps and quadratic values are classical; the paper adds the global-on-box certificate, unchanged factor scopes, growth transfer in the induced metric and the parameter L_red/g | low for the composition, high for the ingredients |
| (1b) Recognizing a globally affine selector by one central QP and one LP | Mangasarian1988 Lemma 1, Cor. 1 (constant gradient on optimal sets); Bemporad critical-region LP; Spjotvold et al. (PSD mp-QP) | Equivalent to "one critical region covers the whole parameter box", including singular C; constant-gradient fact is Mangasarian's | medium |
| (1c) Curvature across a certified partition (no global overlay) | DelPiaKhajavirad2026 (concave kinks of value functions, Lemmas 1--2, p.5); value-function concavity (MangasarianRosen1964, FiaccoKyparisis1986); semiconcavity under infima (CannarsaSinestrari2004) | The bound max_r (H_r)_jj follows from concave kinks plus piecewise quadratic structure; not stated elsewhere in this form as far as found | low-medium |
| (2) Convex value factors with changing active sets | Khajavirad2026PolyBox Thm 1 and proof pp. 8--10; DelPiaKhajavirad2026 Thms 4--6; BhathenaEtAl2026 | Khajavirad eliminates positive-diagonal continuous components into value functions of their (binary) neighbors; the paper keeps continuous gridded neighbors and uses concavity to bound curvature | medium (must be cited; currently missing) |
| (3a) Graph-cut residual oracle for coordinatewise-concave, switch-submodular residuals | Rosenberg1972; Ivanescu1965; PicardRatliff1975; Padberg1989 Props 9--10; BorosHammer2002; KolmogorovZabih2004; Harary1953; BNW v3 pp.2--3 | The residual class (after switching) is "DR-submodular", classically solvable by endpoints + one cut; the paper adds the certified box-stable contract and composition with core search | high for the oracle, low for the composition |
| (3b) Mixed submodular recourse (concave endpoints + PSD continuous block) with greedy-base certificate | GomezHan2025 Lemma 1/Thms 1--3; BuntonTabuada2022 Thm 4, Cor 6; Topkis1978; IwataFleischerFujishige2001 p.765 (credits Cunningham1985) | Same mechanism (partial minimization preserves submodularity, SFM, extreme-base certificates); different variable interface | medium-high |
| (3c) Smoothed count of retained core cells | SpielmanTeng2004; BeierVocking2004/2006; RoglinVocking2007; MulmuleyVaziraniVazirani1987; KelnerNikolova2007 | Same anti-concentration-plus-certification pattern; continuous conditional-value cell count is different | low |
| (3d) NEW in this audit: balanced box QPs solved by the corrected-grid algorithm with a cut oracle, poly(n, kappa, I, q), no width | SchlesingerFlach2006 Sec. 4; Ishikawa2003; Hochbaum2001; Bach2018Isotonic Sec. 4.3; Bach2019; AxelrodLiuSidford2020; KimKojima2003; BNW v3 | Cut representation of ordered-label submodular problems is classical; combining it with growth-filtered geometric grids gives log(1/eps) dependence, which the checked sources do not state | low (to the best of our knowledge) |
| (4) TU fibres: correlated corner rounding, filtered grids, exact recovery, union of retained cells | HoffmanKruskal1956 (via ChervetGrappeRobert2018 Thm 4.4 p.11); GandhiEtAl2006; ChekuriVondrakZenklusen2010; BienstockMunoz2018 Thm 4; proximity papers | Box integrality and marginal-preserving rounding are classical; the growth-filtered, exactly feasible, accuracy-independent state bound is not found | low-medium |
| (5a) Endpoint optimal-set identity (coordinatewise concave mixed-box QP) | Rosenberg1972 Lemma and Prop. 1 (p. 96); Werner2007 Thm 4; WainwrightJaakkolaWillsky2005 Prop. 1 | Rosenberg characterizes all optimal points of multilinear box problems as unions of faces with optimal vertices; the paper adds strictly concave coordinates, mixed boxes and a factored certificate | high for the idea (must cite Rosenberg) |
| (5b) Diagonal Lagrangian certificate, its invariance, full optimal set, unknown-growth discovery | LiWuQuan2015 Cor. 2; BeckTeboulle2000 Thm 2.3; JeyakumarRubinovWu2006; Mangasarian1988; LuoSturm2000 | Certificate and invariance are classical (zero-gap multipliers certify every optimum); discovery by untrusted conditioning guesses is the only added step | high for certificate, low for the discovery procedure |
| (6) Boundary active-face discovery with margin B_gamma | Hansen1980; HansenWalster2004; ArayaTrombettoniNeveu2010 Def. 3, Prop. 1 p.2; BurkeMore1988; Wright1993; FacchineiFischerKanzow1998; Garloff1986 | Sign tests and active-set identification are classical; the precision term for reaching the identification region from a certified global enclosure is the added part | medium |
| (7) Limits: conditional-moment obstruction, DPK conditioning, path complexity | Khajavirad2026SparseSDP Thm 3 p.9, Thm 6 p.24; GroneEtAl1984 (via VandenbergheAndersen2015 Thm 10.1); Lasserre2006; SheraliAdams1990; WainwrightJordan2008; MairalYu2012; GartnerJaggiMaria2012; Murty1980; DelPiaKhajavirad2026 Thms 2--3 | The obstructions are specific to the paper's interfaces; the literature supplies the context a referee expects | low |

## 1. Affine and piecewise-affine convex recourse, condensation, value functions

**Report claims.** (i) If private blocks y_t (C_t PSD, box bounds) admit affine primal and
multiplier maps satisfying KKT on the whole attachment box, then
f(y,z) - q_t(z) = (1/2)(y - ybar)'C(y - ybar) + lambda'(y - l) + mu'(u - y) >= 0, the reduced
objective has Hessian A + B'CB + B'D + D'B, original growth transfers in the metric
I + sum E'B'BE, and the main algorithm runs with L_red/g. (ii) Existence of such a selector is
decided by one central QP and one LP. (iii) With a certified partition into regions each with its
own affine response, the reduced coordinate curvature is max_r (H_r)_jj, with no global overlay.

**Prior work (read).**
- BemporadEtAl2002: Theorem 2, p.6 (printed p.8): for H strictly positive definite and linearly
  independent active constraints, the optimizer and multipliers are affine on the critical region.
  Theorem 4, p.8 (printed p.10): optimizer continuous piecewise affine, value convex piecewise
  quadratic. Section 4.1.1, pp.7--8: degeneracy handled by choosing r independent constraints.
  Their parameter enters the constraints after the substitution z = U + H^{-1}F'x, which needs
  H nonsingular. The report's blocks have parameter in the linear term and possibly singular C.
- TondelJohansenBemporad2003: Definition 2 (LICQ) p.2, Theorem 2 p.3 (active set across a facet),
  Section 5 pp.5--6 (degenerate facets, LP of Theorem 4). Strict convexity is assumed.
- SpjotvoldTondelJohansen2005 (ACC paper read, p.1): convex mp-QP with possibly nonunique
  solutions; choosing the minimum-norm solution gives a unique affine optimizer on each region and
  a unique polyhedral partition; journal version SpjotvoldTondelJohansen2007 (metadata only).
- PatrinosSarimveis2011 (author report version, 22 pp.): objective "merely convex", solution map
  multivalued (p.20); Proposition 4, p.6 (argmin of convex PWQ polyhedral); Theorem 6, p.14
  (adjacent critical regions); Corollary 2, p.17 (critical-region graph connected).
- Mangasarian1988 (journal scan read): Lemma 1, printed p.21: the gradient of a convex objective is
  constant on the solution set; Corollary 1, printed p.22: polyhedral description of the solution
  set of a convex QP. This is exactly the fact the report uses ("all central minimizers have the
  same gradient") in the affine-selector recognition.
- Schur complement / condensation: Zhang2005Schur (metadata), BockPlitt1984, JerezKerriganConstantinides2012,
  Axehill2015 (metadata only). Fill-in under elimination: RoseTarjanLueker1976 (metadata only).
- Low-rank negative curvature with convex recourse by spatial branching: Vavasis1992 (KB, pp.1--7),
  LuoBaiLimPeng2019 (KB, pp.1--3, 10--11): already use "project onto few nonconvex directions,
  minimize the convex rest" with inverse-polynomial accuracy dependence.
- Affine policies in robust optimization (BertsimasIancuParrilo2010, metadata only) is a different
  question (worst case over uncertainty), but a referee may ask about it.

**Relation and novelty statement.** The affine and piecewise-affine optimal responses, their
critical regions, and the identity behind (i) are classical mp-QP facts. What the checked sources
do not contain is the use of a *global* (whole-box or region-wise) response certificate to bound
the upper coordinate curvature of the reduced objective, while keeping factor scopes, together
with the induced-metric growth transfer, so that a growth-conditioned sparse global algorithm
applies with L_red/g instead of L/g. Proposed wording: "Fixed-active-set responses are classical
in multiparametric quadratic programming [BemporadEtAl2002, TondelJohansenBemporad2003,
SpjotvoldTondelJohansen2007, PatrinosSarimveis2011]; we use them only as certificates for a global
upper curvature bound of the reduced objective." For (ii): "The recognition test is the statement
that one critical region contains the parameter box; the constant-gradient property of convex
optimal sets [Mangasarian1988] makes the test a single LP even for singular blocks." No priority
claim for (ii) is warranted. For (iii) the defensible claim is the global curvature bound
without overlaying the partitions of different blocks (proof in `lit-ext-proofs.tex`,
Corollary "Curvature across a certified partition", which is cleaner than the report's proof).

**Threat:** high for ingredients, low for the composition (1a, 1c), medium for (1b).

**Referee-expected citations:** BemporadEtAl2002, TondelJohansenBemporad2003,
SpjotvoldTondelJohansen2007, PatrinosSarimveis2011, Mangasarian1988, Benders1962/Geoffrion1972
(value-function decomposition), Vavasis1992, LuoBaiLimPeng2019, a condensing reference.

## 2. Convex value factors with changing active sets

**Report claim.** For private blocks with fixed feasible polytopes, psi_t(v) = min_y
{(1/2)y'C_t y + y'D_t v + c_t'y} is concave, so the reduced coordinate curvature is that of q_0;
each value query is an exact convex QP [KozlovTarasovKhachiyan1980]; exact output uses the height of
the original QP.

**Prior work (read).**
- Khajavirad2026PolyBox (arXiv:2604.25033v2, read): Theorem 1, p.4: box QP solvable in polynomial
  time if the graph obtained by deleting positive-diagonal components and making their
  neighborhoods N(C) cliques has O(log|V|) treewidth and each component has small "PSD-deletion"
  parameter kappa_C. Lemma 1, p.7: nonpositive-diagonal variables can be taken binary.
  Proposition 2, p.7 (attributed to Vavasis1990): a minimizer with the maximum number of bound
  coordinates has a positive definite reduced Hessian. Lemma 2, pp.7--8: enumeration over
  PSD-deletion sets. Proof of Theorem 1, pp.8--10: each component C is replaced by the value
  function psi_C(z) = min_{x_C} f_C(x_C, z) evaluated at all binary neighbor labels z, then
  binary DP. Remark 4, p.6, compares with SOC/SDP formulations.
- DelPiaKhajavirad2026 (read): p.2 endpoint observation; Theorem 4, p.27 (logarithmic treewidth of
  the binary part, a polynomial oracle for each continuous component, constant rank of the
  coupling); Theorem 5, p.35 (restates Khajavirad2026PolyBox); Theorem 6, p.35 (combination).
- Concavity in linearly entering parameters: MangasarianRosen1964 and FiaccoKyparisis1986
  (metadata only; the fixed-feasible-set concavity condition is stated, with these citations, in
  Fiacco and Kyparisis's 1987 NASA conference paper, p.3, read). Rockafellar1970 Theorem 5.5
  (metadata only).
- BhathenaEtAl2026 (ledger): exact parametric DP for convex QP with indicators on structured
  graphs, with margin and conditioning assumptions.
- Benders1962, Geoffrion1972: value functions of subproblems as the object of optimization.

**Relation and novelty statement.** Khajavirad's elimination is the closest prior: it eliminates
continuous convex (or nearly convex) components into value factors of a small neighbor set and
then runs exact DP. The report's version differs in three ways: (a) the neighbors (retained
coordinates) are continuous and gridded, not binary and enumerated; (b) concavity of the value
factor in its linearly entering parameter is what keeps the corrected grid a valid lower bound;
(c) the number of retained coordinates may be large, controlled by growth-filtered grids. Proposed
wording: "Eliminating convex components into value functions of their neighbors is used for exact
box QP by Khajavirad [Khajavirad2026PolyBox] and Del Pia and Khajavirad [DelPiaKhajavirad2026]
with binary neighbors; we keep continuous neighbors and use the concavity of such value factors
[MangasarianRosen1964, FiaccoKyparisis1986] to retain the curvature certificate." The report
currently does not cite Khajavirad2026PolyBox; this must be fixed (issue I1 in the report).

**Threat:** medium.

## 3. Graph-cut residual oracles, submodular certificates, continuous submodularity, smoothing

**Report claims.** (a) For a fixed core, a residual with nonpositive diagonal and signs s with
c_ij s_i s_j <= 0 is minimized at endpoints by one min cut, with flow certificate, stable under
subboxes. (b) A mixed residual (concave endpoint coordinates + PSD continuous block, submodular
after reversal) gives a submodular endpoint set function; certificate by a convex combination of
greedy bases and exact convex-QP values. (c) Corner search on core cells with a smoothed expected
count. (d) Exact output via a value-denominator bound D_0.

**Prior work (read unless stated).**
- Endpoint reduction: Rosenberg1972, Lemma and Proposition 1, p.96 (multilinear case, and the face
  structure of the optimal set); DelPiaKhajavirad2026 p.2; Khajavirad2026PolyBox Lemma 1 p.7.
- Binary submodular quadratic by min cut: Ivanescu1965 (metadata), PicardRatliff1975 (metadata;
  Padberg1989 p.24, printed p.162, attributes the q >= 0 case to it), KolmogorovZabih2004 Lemma 3.2
  and Theorem 4.1, p.4 (printed p.150), construction p.5 (printed p.151), Section 7 related work
  p.11 (printed p.157); BorosHammer2002 (metadata). Switching: KZ footnote 5, p.5, credits Gortler
  et al.; Padberg1989 Proposition 10 (bipartite case), printed p.162; Harary1953 (balance;
  metadata); HammerHansenSimeone1984 (complementation; metadata).
- Continuous quadratic submodular minimization: BurerNatarajanWillemsen2026v3 pp.2--3 (DR-submodular
  case reduces to binary SFM, citing Staib--Jegelka Prop. 1.1 and Padberg Prop. 10; Kim--Kojima SDP
  exact when c <= 0; Axelrod et al. pseudo-polynomial), Table 1 p.3, footnote 2 p.3 (complexity for
  n >= 4 open), Proposition 1 p.7 (= KimKojima2003 Thm 3.1), Theorem 1 p.12 (SDP exact for n <= 3),
  Example 4 p.14 (gap at n = 4). Bach2019 (arXiv v2): Theorem 1 p.12, Theorem 2 p.13, discretization
  Section 5 pp.27--28. Bach2018Isotonic Section 4.3, p.5: with bounded second derivatives a uniform
  grid of k points has error n^2 L_2^2/(2k^2), giving O(eps^{-5/2}) function accesses.
- Ordered labels: SchlesingerFlach2006 (TU Dresden report, read): abstract p.1, submodularity
  w.r.t. label order Section 2.2 pp.3--4, MinCut construction Section 4 p.13. Hochbaum2001 (read):
  abstract, printed p.686: nonconvex deviation with convex separation solvable by a min cut on a
  graph with nU nodes; nonconvex separation NP-hard. Ishikawa2003 (metadata only).
- Partial minimization and submodularity: GomezHan2025 v2 (read; PDF title page order Gomez, Han):
  Proposition 1 (Topkis) p.11, Lemma 1 = Topkis1978 Theorem 4.2, p.12, Theorem 1 p.12, Theorem 2
  p.14, Remark 1 p.14 (Theorems 1--2 hold for nonconvex submodular f, but evaluation is then hard),
  Theorem 3 p.15 (PSD Q, G/G- bipartite, strongly polynomial via sign changes). BuntonTabuada2022
  (read): Theorem 4 p.9 (Topkis 1998 Thm 2.7.6), Corollary 6 p.11, Section 4.2 pp.11--12.
- Certificates for SFM: IwataFleischerFujishige2001 (read): Lemma 2.1, p.5 (printed p.765), the
  convex-combination-of-extreme-bases certificate credited to Cunningham [1984; 1985], p.5;
  greedy rule (2.2), p.6 (printed p.766), credited to Edmonds 1970 and Shapley 1971.
  GrotschelLovaszSchrijver1988 (ledger: Thm 6.4.9, Lemma 6.5.15).
- Smoothing: SpielmanTeng2004 (arXiv version read, definition of smoothed complexity p.9);
  BeierVocking2004 (KB): Theorem 1 p.3, generalized Isolating Lemma p.3, Theorem 3 p.4;
  RoglinVocking2007 (KB): Theorem 1 p.5; KelnerNikolova2007 (prior audit: Thm 2.9);
  MulmuleyVaziraniVazirani1987 (metadata; discrete uniform weights).
- Del Pia--Khajavirad core/residual organizations: Theorems 4--6 (above).

**Relation and novelty statement.** (a) The residual class is exactly the class of quadratics that
become DR-submodular after switching; its polynomial solvability by endpoints and one cut is
classical (Rosenberg; Picard--Ratliff; Padberg; KZ; BNW pp.2--3). The report already says "the cut
reduction is classical"; it should cite the switching/balance sources and BNW's summary, and say
that the contribution is the box-stable certified oracle and its composition with core search.
(b) The mixed oracle is the Gomez--Han/Bunton--Tabuada mechanism (Topkis partial minimization +
SFM) with a different interface (endpoint-concave coordinates instead of indicators); the
greedy-base certificate is Cunningham's. Defensible novelty: exact rational certificate contract
and box stability, not the tractable class. (c) The smoothed count differs from the discrete
winner-gap literature because it counts near-optimal continuous core cells; cite the smoothed
analysis lineage and MVV for discrete uniform weights.

**New in this audit (3d).** The corrected-grid algorithm needs only an exact oracle for the grid
minimum and coordinate min-marginals of Q = F - D. For a *balanced* quadratic (signs sigma with
sigma_i sigma_j H_ij <= 0; no condition on diagonals or linear terms), one min cut per value
provides this oracle on arbitrary nonuniform grids (threshold encoding; SchlesingerFlach2006
Section 4, Ishikawa2003). Hence, under unique-point growth, a certified 2^{-q} approximation in
(n kappa (I+q+1))^{O(1)} bit operations and exact output in (n kappa (I+1))^{O(1)}, with no
width parameter (Theorem "Balanced box quadratics without a width parameter" in
`lit-ext-proofs.tex`). Relation: BNW v3 leave the complexity of continuous submodular box QP open
for n >= 4; KimKojima2003 need a sign condition on c; Bach2018Isotonic/Bach2019/AxelrodLiuSidford2020
are polynomial in 1/eps. The new statement is polynomial in log(1/eps) and in kappa; it does not
settle BNW's question because kappa can be exponential in the input length. Novelty statement: "To
the best of our knowledge, a growth-conditioned algorithm for continuous submodular quadratics with
polynomial dependence on log(1/eps) has not been stated; the cut representation itself is
classical." Finite support: exact checks in `checks/` (see report).

**Threat:** high for (a); medium-high for (b); low for (c) and (3d).

## 4. TU fibres, correlated rounding, proximity, constrained sparse approximation

**Report claims.** Dyadic cell fibres of TU systems with integral data are integral; any feasible
point is a convex combination of feasible cell corners (correlated mean-preserving rounding with
error n_c L h^2/8 under a full Hessian bound); filtered grids with retained-label bound
5 + 2 sqrt(n_c kappa); exact recovery; union-of-cells variant for finite optimal projections.

**Prior work.**
- HoffmanKruskal1956: TU iff {x: Ax <= b} integral for all integral b. Checked as restated in
  ChervetGrappeRobert2018 (arXiv v1, read), Theorem 4.4, p.11, whose reference [30] gives the
  bibliographic data. The published version of that preprint is ChervetGrappeRobert2021 (Math.
  Prog. 188, different title; metadata only). Schrijver1986 Chapter 19 (metadata only).
- Marginal-preserving rounding under hard constraints: GandhiEtAl2006, ChekuriVondrakZenklusen2010
  (metadata only).
- Proximity between continuous and integer optima (different question): CookGerardsSchrijverTardos1986,
  GranotSkorinKapov1990 (metadata only; HochbaumShanthikumar1990 p.10 uses "Theorem 1 of Granot and
  Skorin-Kapov"), HochbaumShanthikumar1990 (KB): Theorems 1.1--1.2, p.5; proximity sections pp.2--10.
- BienstockMunoz2018 (KB): Theorem 4, p.2 (polynomial-size LP approximations for bounded
  intersection-graph width with scaled feasibility and objective tolerances); Theorem 7 (network
  version) cited p.1.
- LuoSturm2000 (KB; ledger: Theorem 3.3, pp.11--12; theorem numbers are lost in the local text
  extraction, the polytope statement is on p.11): quadratic error bound on a polytope, giving
  existential set growth toward the optimal set.

**Relation and novelty statement.** Box integrality and rounding by convex combinations of
integral points are classical; the rounding needs only Hoffman--Kruskal plus Caratheodory
(proof in `lit-ext-proofs.tex`, Lemma "Corner rounding in a dilated TU fibre"). Bienstock--Munoz
cover broader constrained models but only with scaled feasibility tolerances. The added result is
an exactly feasible, growth-filtered grid algorithm with an accuracy-independent retained-state
bound and exact recovery, for TU continuous fibres. Proposed wording: "Integrality of the cell
fibres is the Hoffman--Kruskal theorem; unlike the LP approximations of Bienstock and Munoz, which
apply to general bounded-width polynomial constraints with scaled tolerances, the TU extension is
exactly feasible." The report correctly notes it is XP in width (factor n_c^{p/2}), not FPT.

**Threat:** low-medium.

## 5. Optimal-set descriptions and Lagrangian certificates

**Report claims.** (a) For x'Qx + b'x with Q_ii <= 0 on a mixed box, an interpolation identity
F(x) - OPT = sum_t sum_v r_t(v) W_t(v;x) - sum_i Q_ii (x_i - l_i)(u_i - x_i) gives a factored
description of all optimizers with at most N 2^p + n equations. (b) The diagonal certificate
(H + D PSD at a KKT point) gives the full optimal set and is passed at every optimum if at one;
combined with untrusted conditioning guesses it discovers an optimum without g.

**Prior work (read unless stated).**
- Rosenberg1972 (numdam scan read), Lemma and Proposition 1, printed p.96: for a polynomial linear
  in each variable on a box, the set of minimizers is the union of the faces C whose vertices are
  all minimizers over the vertex set. This is (a) without the strictly concave terms and without
  the factorization.
- Werner2007 (author version read): Section III-D "trivial problems" and Theorem 4, p.6: after an
  optimal equivalent transformation, optimal labelings are the solutions of the CSP of maximal
  (zero-residual) elements; on trees this is exact. WainwrightJaakkolaWillsky2005 Proposition 1
  (tree agreement), p.6 (printed p.3702). Kolmogorov2006 (metadata). Dechter1999 (ledger: Thm 11).
- LiWuQuan2015, Corollary 2, Section 3.2, eq. (14) (ledger; the publisher blocked automated
  re-access on 2026-10-03): box multipliers with grad F(s) + diag(lambda)(2s - l - u) = 0 and
  H + 2 diag(lambda) PSD imply global optimality.
- BeckTeboulle2000 (read): Theorem 2.3, p.4 (sufficient condition [SC] for {-1,1}^n,
  lambda_min(Q) e >= XQXe + Xb), Theorem 2.4 p.5, Remark 2.6 p.6.
- JeyakumarRubinovWu2006 (secondary: HuyJeyakumarLee2006, Proposition 2.1, p.441, read): necessary
  and sufficient condition for separable box QP and sufficient conditions via quadratic
  underestimators. Pinar2004 (metadata only).
- Mangasarian1988 (read; see Section 1), BurkeFerris1991 and JeyakumarLeeDinh2004 (metadata only):
  solution sets of convex programs and Lagrangian characterizations of them.
- LuoSturm2000 (see Section 4): existence of set growth.

**Relation and novelty statement.** (a) is Rosenberg's face criterion, extended to strictly concave
coordinates (which must sit at endpoints) and mixed boxes, combined with the zero-residual
description of tree reparameterizations. The report presents it as "the displayed identity
records their full-set certificate" but does not cite Rosenberg; it must (issue I2). A cleaner
statement and proof are in `lit-ext-proofs.tex` (Proposition "Face criterion"). (b) The
certificate is LWQ's Corollary 2 (with earlier relatives); the full-set description and the
invariance are the classical fact that a multiplier certifying zero duality gap certifies every
optimal solution (Proposition "Diagonal Lagrangian certificate" in `lit-ext-proofs.tex`). The
report's "classical box Lagrangian sufficient condition of Li, Wu, and Quan" should become "the box
Lagrangian sufficient condition [LiWuQuan2015, Cor. 2]; see also [BeckTeboulle2000,
JeyakumarRubinovWu2006]". Defensible novelty: only the discovery procedure under untrusted growth
guesses and its exact acceptance.

**Threat:** high for both ingredients; low for the discovery procedure.

## 6. Monotonicity, interval methods and active faces

**Report claim.** Inside a certified retained box of half-width r with Hessian row-sum bound M, the
test d_iF(c) - M r > 0 fixes a lower bound (Araya et al. cited); with strict complementarity margin
gamma, all active coordinates are found at r <= gamma/(4M); a strongly convex patch is then
certified; total work f_d(p, kappa) poly(I + B_gamma).

**Prior work.** ArayaTrombettoniNeveu2010 (KB): Definition 3 and Proposition 1, p.2
(monotonicity-based interval extension). The monotonicity test of interval global optimization:
Hansen1980, HansenWalster2004 (metadata only). Bernstein bounds: Garloff1986 (metadata only).
Active-set identification under strict complementarity or error bounds: BurkeMore1988, Wright1993,
FacchineiFischerKanzow1998 (metadata only).

**Relation and novelty statement.** The sign test is the classical monotonicity test; the
identification threshold r <= gamma/(4M) is an elementary instance of active-constraint
identification. The added part is the explicit precision term B_gamma for reaching this region from
a certified global enclosure, and the convex-patch certificate. The report should cite Hansen's
monotonicity test and one active-set-identification reference, and keep this result in an appendix.

**Threat:** medium.

## 7. Structural limits

**Report claims.** (i) Convex energy and convex-recourse envelopes keep positive energy but do not
bound separator states; (ii) a four-variable, width-two family with nu/g = 44 where matching three
separator moments and even a global PSD completion do not repair a constant gap; (iii) Del Pia--
Khajavirad's width-two hardness construction has nu/g >= 4B; (iv) exponential complete messages are
inherited from earlier work.

**Prior work.**
- DelPiaKhajavirad2026 (read): Theorem 1 p.4 (forest QP in O(n^2) operations), Theorem 2 p.18
  (quartic on a path strongly NP-hard), Theorem 3 p.20 (box QP strongly NP-hard at treewidth two,
  ||Q||_max <= 5, ||c||_inf <= 4).
- Khajavirad2026SparseSDP (arXiv:2601.18545v2, KB): Theorem 3, p.9 (RLT-augmented LMIs),
  Theorem 5 p.23, Theorem 6 p.24 (polynomial-size SDP formulations under graph conditions).
  DeyKhajavirad2026 (metadata only; SOC-representable class). The report cites the Optimization
  Online URL; the arXiv v2 (Feb 12, 2026) is the same version and is preferable.
- GroneEtAl1984: chordal patterns guarantee PSD completions; checked as quoted in
  VandenbergheAndersen2015 (read), Theorem 10.1, printed p.356, "[108, theorem 7]".
- Moment relaxations and sparsity: Lasserre2001, Lasserre2006, WakiEtAl2006 (KB), Laurent2009
  (metadata only). Local versus global consistency: SheraliAdams1990 (KB), WainwrightJordan2008
  (metadata only).
- Parametric complexity: MairalYu2012 (KB: exactly (3^p + 1)/2 segments in the worst case, p.1;
  ledger: Theorem 1, p.5 of the ICML PDF), GartnerJaggiMaria2012 (metadata from DOAJ; arXiv
  0903.4817), Murty1980 (KB).

**Relation and novelty statement.** The obstructions are about the report's own interfaces and
are correctly scoped there. A referee will expect the context: PSD completion is automatic on
chordal patterns (so a PSD completion existing is unsurprising), local consistency of low-order
moments does not imply a joint measure (the continuous analogue of the local-versus-marginal
polytope gap), and complete parametric descriptions can be exponential (Murty, Mairal--Yu,
Gartner--Jaggi--Maria). The Del Pia--Khajavirad conditioning remark is new as far as found and
should be in the main text because it explains why the conditioned theorem does not contradict
width-two hardness.

**Threat:** low.

## Corrections to citations currently in `references.bib` of the report

1. Khajavirad2026SparseSDP: cite arXiv:2601.18545 (v2, 2026-02-12), not the Optimization Online URL.
2. ChervetGrappeRobert2018: the theorem used is Hoffman--Kruskal; cite HoffmanKruskal1956 for it
   and, if the preprint is kept, also its published version ChervetGrappeRobert2021 (new title).
3. GomezHan2025: the PDF lists "Andres Gomez and Shaoning Han" (arXiv metadata lists Han first);
   keep the PDF order. No journal version found.
4. IwataFleischerFujishige2001 is cited for the greedy-base certificate; the certificate is credited
   there to Cunningham (1984, 1985) and the greedy rule to Edmonds (1970). Add Cunningham1985 and
   Edmonds1970.
5. KolmogorovZabih2004 alone is cited for the cut reduction; add Ivanescu1965 (Hammer),
   PicardRatliff1975, BorosHammer2002 and, for switching, Harary1953/HammerHansenSimeone1984 or
   Padberg1989 Prop. 10.
6. BemporadEtAl2002 is cited for fixed-active-set recourse with possibly singular C; Bemporad's
   Theorem 2 assumes H positive definite and LICQ. Add SpjotvoldTondelJohansen2007 and
   PatrinosSarimveis2011 for the PSD case.
7. LiWuQuan2015 is called "classical"; it is a 2015 statement of a condition with earlier relatives
   (BeckTeboulle2000, JeyakumarRubinovWu2006).
8. ArayaTrombettoniNeveu2010 is cited for "standard monotonicity propagation"; add Hansen1980 or
   HansenWalster2004 for the monotonicity test in interval global optimization.
9. Vavasis1990 remains unread here; Khajavirad2026PolyBox Proposition 2 (p.7) attributes to it the
   minimum-face positive-definiteness argument used in the report's height lemma. The report's
   self-contained proof should stay; the citation can be attributed through that statement.

## Source access log

Read in primary text in this audit: Khajavirad2026PolyBox, DelPiaKhajavirad2026,
Khajavirad2026SparseSDP, BemporadEtAl2002, TondelJohansenBemporad2003 (garbled extraction; theorem
numbers and pages only), SpjotvoldTondelJohansen2005, PatrinosSarimveis2011 (report version),
Mangasarian1988, KolmogorovZabih2004, Padberg1989, BurerNatarajanWillemsen2026v3, GomezHan2025,
BuntonTabuada2022, IwataFleischerFujishige2001, Hochbaum2001, SchlesingerFlach2006, Bach2018Isotonic,
Bach2019 (arXiv), Rosenberg1972, Werner2007 (author version), WainwrightJaakkolaWillsky2005,
BeckTeboulle2000, HuyJeyakumarLee2006, ChervetGrappeRobert2018, VandenbergheAndersen2015,
BeierVocking2004, RoglinVocking2007, SpielmanTeng2004 (arXiv), ArayaTrombettoniNeveu2010,
HochbaumShanthikumar1990, BienstockMunoz2018, MairalYu2012, LuoSturm2000 (extraction lost theorem
numbers).

Secondary only: FiaccoKyparisis1986 and MangasarianRosen1964 (Fiacco--Kyparisis NASA CP 1987, p.3),
CannarsaSinestrari2004 (Kunisch--Vasquez-Varas, arXiv:2602.07770, pp.4--5), Topkis1978 (Gomez--Han
p.12), Topkis1998 (Bunton--Tabuada p.9), JeyakumarRubinovWu2006 (Huy--Jeyakumar--Lee p.441),
KimKojima2003 and StaibJegelka2020 (BNW v3 pp.2--3, 7), HoffmanKruskal1956 (Chervet et al. p.11),
GroneEtAl1984 (Vandenberghe--Andersen p.356), PicardRatliff1975 (Padberg p.162), GranotSkorinKapov1990
(Hochbaum--Shanthikumar p.10).

Ledger only (not re-opened): LiWuQuan2015 (Springer blocked automated access), Dechter1999,
GrotschelLovaszSchrijver1988, KozlovTarasovKhachiyan1980, BhathenaEtAl2026.

Metadata only: Ishikawa2003, PicardRatliff1980, Ivanescu1965, HammerHansenSimeone1984, Harary1953,
BorosHammer2002, Schrijver2000, Cunningham1985, Edmonds1970, Lovasz1983, AxelrodLiuSidford2020,
Zhang2000, SojoudiLavaei2014, SpjotvoldTondelJohansen2007, SpjotvoldEtAl2006, BockPlitt1984,
JerezKerriganConstantinides2012, Axehill2015, Zhang2005Schur, RoseTarjanLueker1976, Rockafellar1970,
BurkeFerris1991, JeyakumarLeeDinh2004, Pinar2004, BertsimasIancuParrilo2010, GandhiEtAl2006,
ChekuriVondrakZenklusen2010, CookGerardsSchrijverTardos1986, ChervetGrappeRobert2021, Schrijver1986,
Hansen1980, HansenWalster2004, Garloff1986, BurkeMore1988, Wright1993, FacchineiFischerKanzow1998,
GroneEtAl1984, Laurent2009, WainwrightJordan2008, GartnerJaggiMaria2012, DeyKhajavirad2026,
MulmuleyVaziraniVazirani1987, Kolmogorov2006, Vavasis1990, BeierVocking2006.

Not accessible: Ishikawa2003 full text (IEEE), Fiacco--Kyparisis 1986 full text (Springer),
Li--Wu--Quan 2015 (Springer blocked automated download this time), Picard--Ratliff 1975/1980
(Wiley; the 1974 report is restricted at Polytechnique Montreal), Grone et al. 1984 (Elsevier
blocked), Topkis 1978 (INFORMS). These are cited only through the statements listed above.
