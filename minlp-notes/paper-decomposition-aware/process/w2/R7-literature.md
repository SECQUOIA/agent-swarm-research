# R7 — Literature and novelty review

Manuscript: "Decomposition-aware global optimization: certified coordinate grids, conditional
recourse, and structural limits" (`paper-decomposition-aware/`, PDF `build/main.pdf`, 99 pages).
Reviewer role: literature and novelty. Date: 2026-10-03. No paper file was edited.

## Verdict

No critical issue. None of the main results is anticipated by work I could find, and the central
novelty statement (related.tex:30-33: no earlier `f(p,kappa)poly(I+q)` approximation or
`f(p,kappa)poly(I)` exact algorithm for nonconvex or mixed-integer box QP) survived the search
described below. The citations I checked against primary sources are correct, including theorem
numbers. The problems are about attribution and the reference list:

1. The compiled bibliography prints all 10 arXiv preprints without an arXiv number or URL,
   including the most-cited reference (Del Pia–Khajavirad, 11 citations). It also prints internal
   notes ("Proceedings page range not checked", "Version 1, September 28, 2026; first posted ...").
2. Two results are presented as new without naming their closest antecedent at the point of use:
   - the path-of-affine-equalities hardness (Prop. `lim:prop:constraints`) is the subset-sum chain
     of Bienstock–Muñoz, Appendix A;
   - the endpoint optimal-set theorem (Thm. `thm:endpointset`, Cor. `cor:facecsp`) contains
     Rosenberg's face criterion.
3. The contributions list claims as new two things that Section 3 itself calls classical
   (min-marginal filtering and the path certificate), and it claims "the lower bounds and
   limiting examples of Section 9" as a whole.
4. The closest MINLP analogues of "grids re-centred on the incumbent plus bound tightening" are
   missing: AMP (Nagarajan et al. 2019) and Gupte–Koster–Kuhnke (2022).

All of these are text fixes. Proposed wording is given below.

## 1. Citation checks against primary sources

"KB" means the local full text in `literature/papers/<slug>/fulltext.md`. "PDF" means the local
`original.pdf`, extracted with pdftotext.

| Citation in paper | Claim in paper | Source checked | Result |
|---|---|---|---|
| DelPiaKhajavirad2026, Thms 1–3 (related.tex:11-14; intro.tex:27-31; limits.tex:32-36) | Strongly polynomial on forests; strongly NP-hard at treewidth two with bounded integer data; quartic strongly NP-hard on paths | KB + PDF: Thm 1 (O(n²), forests), Thm 2 (quartic, path), Thm 3 (tw 2, ‖Q‖max≤5, ‖c‖∞≤4) | Correct |
| DelPiaKhajavirad2026, Remark 2 (limits.tex:40-43) | Simple weak-NP-hardness reduction, refined in Prop. `lim:prop:unique` | PDF p.25: objective (U s_n−T)² + Σ(U s_i−U s_{i−1}−a_i x_i)² + Σ x_i(1−x_i), bags {s_{i−1},s_i,x_i} | Correct; the attribution is accurate |
| DelPiaKhajavirad2026, (20)–(24) (Remark `lim:rem:dk`, limits.tex:180-223) | ℓ=⌈log₂2B⌉, D=2^ℓ, 5ℓ+2 variables, max diagonal 10, Ψ(y′)=D⁻², ‖y′−v*‖²≥2ℓ, Ψ(fractional)=q/B | PDF pp.21-24; exact check `checks/r7_dpk_remark.py` (B=3,4,5,8,16,32) | All numbers reproduced exactly (PASS) |
| DelPiaKhajavirad2026, "tractable classes ... eliminate the continuous components" (related.tex:14-17) | — | KB Thms 4–6, Sec. 4 | Consistent with the paper's V⁺/V⁻ split |
| BajajHasan2020, Thm 1 (grids.tex:41-42; related.tex:45-47) | Vertex bound from an upper bound on the Hessian diagonal | Crossref metadata verified (Optim. Lett. 14(4):1011–1026). Full text paywalled; only the AIChE abstract was reachable. The provenance comment for this entry (now misplaced above `Neumaier2004`, references.bib:1821) also says "abstract" | Plausible, not verified. Theorem number and the Θ ↔ L_i/2 convention are unconfirmed (see m1) |
| BienstockMunoz2018, Thm 4 (related.tex:24-25), Thms 4 and 15 (constraints.tex:815) | LP of size O((2π/ε)^{ω+1} n log(π/ε)) with scaled tolerances; 1/ε dependence cannot be removed unless P=NP | KB: Thm 4 (p.2), Thm 15, App. A (pp.24-25) | Correct |
| KolmogorovZabih2004 (related.tex:141-142; recourse-cuts.tex:122; recourse-balanced.tex:83) | Pairwise binary energies with regular (submodular) terms are minimized by one cut | KB: Thm 4.1, Lemma 3.2 | Correct; no theorem number is cited |
| LuoSturm2000, Thm 3.3 (exact.tex:252; optsets.tex:584) | Error bound dist(x,S) ≤ c\|g(x)\|^{1/2} for a quadratic on a polytope; gives set growth | KB: main result Thm 3.3 (pp.11-12) | Correct. Related.tex:115-116 overstates it (m6) |
| Vavasis1990 (related.tex:110-111; optsets.tex:236-238; constraints.tex:540) | Rational QP has a minimizer of polynomial size; the stationary-face argument follows Vavasis | KB (IPL) and w1 reading of TR 90-1099, Sec. 2 | Correct. The attribution is missing where the lemma is proved (m7) |
| DelPiaDeyMolinaro2017 (optsets.tex:239-241) | MIQP in NP, unbounded integers | KB | Correct |
| Mangasarian1988 (recourse-convex.tex:513-514) | All optimizers of a convex QP have the same gradient | Known content of Lemma 1 / Cor. 1 | Correct for convex quadratics |
| Khajavirad2026PolyBox (related.tex:15; 145) | Endpoint/binary reduction and elimination of continuous components | arXiv abstract (v1 2026-04-27, v2 2026-08-19) | Correct. No in-section pointer at Thm `thm:cv` (m16) |
| Cluster problem (growth.tex:243-251; related.tex:87-91) | Box count near a nondegenerate minimizer is independent of the tolerance, local, asymptotic, can be exponential in n and conditioning | KB: Du–Kearfott Thm 1 and Cor. 1; Kannan–Barton Thm 3 and Remark 5; Wechsung et al. Table 1 (one box if prefactor ≤ λ₁/8) | Correct in related.tex. growth.tex:248 says the count "is" exponential (m2) |
| Bhathena et al. (related.tex:17-21) | Exact parametric DPs on trees and bounded-treewidth graphs, with complexity depending on a margin and on conditioning | KB: Trees (MP 218:291–336) is O(n²) with no margin or conditioning; Graphs (arXiv 2603.02103) is linear in n for fixed treewidth, margin, volume growth and κ₂, κ∞ | The sentence merges the two results (m3) |
| DelPia2023 (related.tex:25-27) | Approximation for MIQP "with a fixed number of negative eigenvalues" | KB: fixed rank(H) and fixed number of integer variables | Imprecise (m5) |
| GrotschelLovaszSchrijver1988 (5.1.9), (6.4.12), (6.4.9), Lemma (6.5.15) | Continued fractions; LP in polynomial time; separation ⇔ optimization; basic dual solution | KB full text | All four locators correct |
| DvijothamEtAl2017, Thm 2 (related.tex:64) | Interval DP on trees, approximately feasible and superoptimal, poly(1/ε) | KB: Thm 2 (Constraints version) | Correct |
| BurerNatarajanWillemsen2026v3: Thm 1, Ex. 4, fn. 2 (recourse-balanced.tex:168-170) | SDP exact for n≤3; gap at n=4; complexity open for n≥4 | KB | Correct. Prop. 1 there is Kim–Kojima Thm 3.1, matching the KimKojima2003 citation |
| LiWuQuan2015 (optsets.tex:530-531) | Box-multiplier global optimality conditions for box QP | Semantic Scholar abstract (box-constrained QP conditions) | Appropriate |
| MulmuleyVaziraniVazirani1987 (appendix-lbproduct.tex:2) | Isolation lemma | Standard | Correct |

## 2. Novelty statements and how they hold up

| Statement | Location | Assessment |
|---|---|---|
| (i) Node-separable form of the vertex bound; best cellwise bound by tree DP | intro.tex:145-148 | Supported. The single-box bound is Bajaj–Hasan, the α constant is from αBB, and edge-concavity from Tardella/Meyer–Floudas/Hasan. All are cited in grids.tex:41-47. No source with the grid-wide node-unary form was found. |
| (i) "... together with min-marginal filtering and the path certificate" | intro.tex:147-148 | Overclaimed. grids.tex:149-153 and 226-230 say the DP and min-marginals are classical, the filter is OBBT, and the certificate follows VIPR logic (M3). |
| (ii) Accuracy-independent grid bound; f(p,κ) algorithms; no knowledge of g | intro.tex:149-154; related.tex:30-33 | Supported. The closest prior works are the cluster-problem analyses (local, asymptotic, dimension-exponential), Bhathena–Graphs (convex indicator QP, exact, treewidth plus margin, volume growth and κ), and proximity–scaling (separable convex). Bhathena–Graphs should be named as the nearest "treewidth + conditioning" result (m3). |
| (iii) Integration of value functions, certified responses, cut oracles | intro.tex:155-158 | Supported as composition. Each ingredient is attributed in remarks (recourse-convex.tex:429-431; recourse-cuts.tex:119-133; recourse-balanced.tex:79-85, 166-178), except Khajavirad's elimination at Thm `thm:cv` (m16). |
| (iv) TU extension and several minimizers | intro.tex:159-160 | TU: well attributed (constraints.tex:153-154, 805-848). Several minimizers: Rosenberg's face criterion is not named at Thm `thm:endpointset`/Cor. `cor:facecsp` (M2). |
| (v) "the lower bounds and limiting examples of Section 9" | intro.tex:161-163 | Too broad. Prop. `lim:prop:constraints` is the Bienstock–Muñoz chain (M1). Prop. `prop:lbwidth` is the standard embedding of independent set. Prop. `lim:prop:oracle` and Prop. `prop:oraclebarrier` adapt classical hidden-well/bump arguments (the paper says so, limits.tex:230-231, 544-545). The expanding-box chain, `lim:prop:unique` (attributed refinement of DPK Remark 2), `prop:lbproduct` and `lim:prop:moments` are new as far as I found. |
| (vi) Exact-arithmetic implementation with independent checker | intro.tex:164-166 | Fine as a contribution. Rigorous global optimization (interval methods, safe bounds) and exact MIP are not mentioned at all (m11). |
| "To our knowledge, no earlier result gives ... f(p,κ)poly(I+q) ... f(p,κ)poly(I) for nonconvex or mixed-integer box QPs" | related.tex:30-33 | Survives the search (Section 4). Bhathena–Graphs is close in spirit but solves a different class: convex objective with indicator constraints, unbounded x. |
| "classical" labels | grids.tex:149; optsets.tex:236, 440, 530-533; recourse-mixed.tex:49; recourse-cuts.tex:119; recourse-convex.tex:429, 513; appendix-boundary.tex:78; limits.tex:230, 544 | All justified. The sources behind appendix-boundary.tex:78 and limits.tex:544 should be cited (m8, m9). |

## 3. Findings

### Major

**M1. Prop. `lim:prop:constraints` repeats the Bienstock–Muñoz subset-sum chain without citing it.**
Location: limits.tex:550-583; contributions item (v), intro.tex:161-163; summary bullet
limits.tex:25-26; intro.tex:134-135.
Bienstock–Muñoz [SIOPT 28 (2018), App. A, eq. (26), arXiv v15 pp.24-25] encode subset sum as a
constrained polynomial problem whose intersection graph has treewidth two: the running sums
M S y_i = M a_i x_i + M S y_{i−1}, y_n = 1, with x_j(1−x_j)=0. They use it to show that the
dependence on 1/ε cannot be improved unless P=NP. The paper's chain y_{i+1}=y_i+(a_i/B)x_i,
y_0=0, y_{n+1}=1, with binary x, is the same construction. The additions are the dummy item x_0,
the lexicographic objective, uniqueness, and the growth constant at κ=1. DPK Remark 2 and
Cifuentes–Parrilo [SIDMA 30 (2016), Ex. 1] (subset sum for quadratic systems on a path, cited by
DPK) are further antecedents. The proposition has no citation except Garey–Johnson. Contribution
(v) presents Section 9 as new as a whole.
Fix: after limits.tex:568, add: "The running-sum encoding of Subset Sum is that of Bienstock and
Muñoz \cite[Appendix~A]{BienstockMunoz2018}; see also \cite[Example~1]{CifuentesParrilo2016}.
What we add is a unique minimizer and the growth constant, so that $\kappa=1$." Replace intro
item (v) by: "(v) the expanding-box chain (Proposition~\ref{lim:prop:messages}), unique-minimizer
hardness at bag size three with explicit growth (Proposition~\ref{lim:prop:unique}, a refinement
of \cite[Remark~2]{DelPiaKhajavirad2026}), the rETH bound on the exponent of $\kappa$
(Proposition~\ref{prop:lbproduct}) and the finite-order moment obstruction
(Proposition~\ref{lim:prop:moments}); the remaining statements of Section~\ref{sec:limits} adapt
standard constructions."

**M2. The endpoint optimal-set result does not name Rosenberg's face criterion where it is stated.**
Location: optsets.tex:334-358 (Thm `thm:endpointset`), 373-394 (Cor. `cor:facecsp`), remark at
optsets.tex:440-446; abstract.tex:31-33; intro.tex:116-120.
Rosenberg [RAIRO 6(V2) (1972), Lemma and Prop. 1, p.96] characterizes the optimal set of a
multilinear function on a box as the union of the faces all of whose vertices are optimal. That
is the content of Cor. `cor:facecsp`(ii) for H_ii=0. The zero-residual (reparameterization)
description of all optimal labelings is Wainwright–Jaakkola–Willsky 2005 and Werner 2007,
Thm 4. The related work names both (related.tex:169-172). The remark next to the theorem,
however, credits only endpoint optimality and DPK and says the identity "records what these
ingredients give for the entire optimal set". A reader of Section 8, or of the abstract, will
take the face description to be new. The new content is the extension to strictly concave
diagonals and mixed boxes and the factored, tree-structured form with its counting and
projection consequences.
Fix: replace optsets.tex:440-446 by: "Endpoint optimality for nonpositive diagonals is classical,
and for multilinear functions Rosenberg characterized the optimal set as the union of faces whose
vertices are all optimal \cite{Rosenberg1972}; Del Pia and Khajavirad use endpoint optimality to
separate binary-valued from continuous variables \cite{DelPiaKhajavirad2026}. Zero-residual
descriptions of all optimal labelings of discrete problems are standard
\cite{WainwrightJaakkolaWillsky2005,Werner2007}. Theorem~\ref{thm:endpointset} combines these
facts; what is new is the treatment of strictly concave coordinates and mixed boxes and the
factored description on the decomposition, which Corollary~\ref{cor:facecsp} turns into a
tree-structured constraint problem."

**M3. Contribution (i) claims as new what Section 3 calls classical.**
Location: intro.tex:145-148 vs grids.tex:149-153 and 225-230.
Item (i) lists "min-marginal filtering and the path certificate" as new. grids.tex says the
min-marginals are classical two-pass message passing, removing intervals is optimality-based
bound tightening, and the certificate's logic is that of checkable branch-and-bound
certificates. This is the most visible novelty statement in the paper, and it contradicts the
section it summarizes.
Fix: "(i) the node-separable form of the vertex lower bound, which makes the best cellwise bound
over a product grid computable by dynamic programming on a tree decomposition; its coordinate
min-marginals give interval bounds for optimality-based filtering from one pair of message passes,
and the stage grids form a certificate checked by recomputation (Section~\ref{sec:grids});"

**M4. The closest MINLP analogues of incumbent-centred adaptive grids are missing.**
Location: related.tex:55-69 ("Dynamic programming with coarse states") and 35-53.
The paper's algorithm rests on grids graded around the current corrected minimizer, filtered by
bound tightening, with a bounded number of nodes per coordinate. Two lines of MINLP work do
something close in practice, and an MP/SIOPT referee will expect them:
- Nagarajan, Lu, Wang, Bent, Sundar, "An adaptive, multivariate partitioning algorithm for global
  optimization of nonconvex programs", J. Glob. Optim. 74(4):639–675 (2019),
  doi:10.1007/s10898-018-00734-1. It refines piecewise-McCormick partitions around the current
  relaxation and local solutions, combined with sequential OBBT (KB: Alg. 1 and 4, pp.9-13).
- Gupte, Koster, Kuhnke, "An adaptive refinement algorithm for discretizations of nonconvex
  QCQP", SEA 2022, LIPIcs 233, Art. 24, doi:10.4230/LIPIcs.SEA.2022.24. It re-centres a
  fixed-size discretization on the previous MILP solution; it is a heuristic (KB pp.5-8). See
  also Koster–Kuhnke, Optim. Eng. 20:497–542 (2019).

The paper's last sentence there ("None of these methods comes with a state count independent of
the accuracy") stays true for both, and it is the point to make.
Fix: add to related.tex after line 68: "In mixed-integer nonlinear programming, adaptive
partitioning refines piecewise relaxations around the current relaxation solution and combines
them with optimality-based bound tightening \cite{NagarajanEtAl2019}, and discretizations of a
fixed size can be re-centred on the previous solution \cite{GupteKosterKuhnke2022}; these are
practical methods without a bound on the number of partition points."

**M5. The compiled bibliography prints arXiv preprints without identifiers and leaks internal notes.**
Location: references.bib `@misc` entries at lines 279, 303, 443, 672, 696, 731, 978, 1358, 1381,
1558; Bach2018Isotonic (line 76); rendered as references [45] etc. on PDF pp.82-86
(`build/main.bbl`:64, 247, 351, 512, 608, 677, 683).
`plainnat` ignores `eprint`/`archivePrefix`. As a result, DelPiaKhajavirad2026,
BhathenaEtAl2026Graphs, BienstockChen2024, BurerNatarajanWillemsen2026v3, DelPia2026Jacobi,
DongLuo2018, GomezHan2025, Khajavirad2026PolyBox, Khajavirad2026SparseSDP and Lokshtanov2015
appear as title and year only, with no way to locate them. For example: "[45] Alberto Del Pia
and Aida Khajavirad. Treewidth and the complexity of box-constrained quadratic programs, 2026.
Version 1, September 28, 2026." Internal notes are also printed: "Proceedings page range not
checked" (Bach 2018), "first posted 2025", "Online March 18, 2026; preprint arXiv:2505.22212".
Fix: give every `@misc` a `howpublished = {arXiv:2609.35595}` (and so on), or a `url`, or
switch to a style that prints `eprint`. Delete the bookkeeping notes; keep only "arXiv:XXXX,
version N" where the version matters (BNW v3). For Bach2018Isotonic, check the NeurIPS 31
page range in the proceedings, or omit pages without a note.

### Minor

**m1. Bajaj–Hasan Theorem 1 is verified only at abstract level.** grids.tex:41-46; related.tex:45-47.
The full text was not reachable here or in w1. The w1 memo says "the exact constant convention
of the paper was not checked". Bajaj–Hasan use one global bound on the Hessian diagonal; the
paper uses per-coordinate L_i. Fix: confirm Thm 1 and its Θ convention in the published version.
Then write "with a single bound $\max_iL_i$; the per-coordinate form is immediate".

**m2. growth.tex:247-248 says the cluster count "is ... exponential in the dimension and in the conditioning".**
Wechsung–Schaber–Barton show a single box suffices when the second-order prefactor is at most
λ₁/8 (KB, Table 1, p.8). related.tex:90 correctly says "can be". Fix: "That count is local and
asymptotic, and it can be exponential in the dimension and in the conditioning of the Hessian."

**m3. Bhathena et al. are summarized imprecisely, and the nearest "treewidth + conditioning" result is not singled out.** related.tex:17-21, 30-33.
The tree paper is an O(n²) algorithm with no margin or conditioning. The graph paper is linear
in n for fixed treewidth, margin, volume growth and condition numbers κ₂, κ∞ (KB, Thm 1 and the
paragraph after Cor. 1). Fix: "Bhathena et al.\ give an $O(n^2)$ parametric dynamic program on
trees \cite{BhathenaEtAl2026Trees} and, on graphs of bounded treewidth, one whose running time is
linear in $n$ for fixed width, margin, volume growth and condition numbers
\cite{BhathenaEtAl2026Graphs}; this is the closest treewidth-and-conditioning result we know, for
a convex objective with indicator constraints." Keep the "To our knowledge" sentence after it.

**m4. The integer-QP sentence mixes parameters, and a 2026 result is missing.** related.tex:22-23.
Lokshtanov 2015 parameterizes by the number of variables plus the coefficient bound, not by
treewidth. Ganian–Ordyniak 2018 is about ILP. Herrmann, "Integer quadratic programming is
W[1]-hard parameterized by the number of variables", arXiv:2608.17818 (Aug. 2026), shows that
f(n)|I|^{O(1)} is impossible (separable concave objective, linear constraints). Fix: "For
integer QP, bounded treewidth gives fixed-parameter tractability together with bounded domains
\cite{EibenEtAl2019}; parameterized by the number of variables, bounded coefficients are also
needed \cite{Lokshtanov2015}, and without them the problem is W[1]-hard \cite{Herrmann2026}; see
\cite{GanianOrdyniak2018} for ILP."

**m5. Del Pia 2023 assumes fixed rank, not a fixed number of negative eigenvalues.** related.tex:25-27.
Fix: "... for QP with a fixed number of negative eigenvalues \cite{Vavasis1992}, for MIQP with
fixed rank and a fixed number of integer variables \cite{DelPia2023}, and for MIQP with a fixed
number of negative eigenvalues and integer variables \cite{DelPia2026Jacobi}".

**m6. "set-valued error bounds are due to Luo and Sturm" overstates the source.** related.tex:115-116.
Error bounds go back to Hoffman (1952) and Łojasiewicz. Luo–Sturm give the bound for one
quadratic on a polytope. Fix: "growth towards the whole optimal set of a quadratic program over a
polytope follows from the error bound of Luo and Sturm \cite[Theorem~3.3]{LuoSturm2000}."

**m7. Classical lemmas are proved without attribution where they appear.** exact.tex:64-120 (Def.
`def:statpoly`, Lemma `lem:statpoly`), exact.tex:264-287 (Lemma `lem:unique-growth`),
exact.tex:46-57 (Hadamard's inequality).
Vavasis is credited in related.tex:111 and in optsets.tex:235-241, three sections later, but not
at the lemma. Contesse is not cited at the uniqueness lemma. Fix: add before Lemma
`lem:statpoly`: "The argument follows Vavasis \cite[Section~2]{Vavasis1990} (see also
\cite[Theorem~3]{DelPiaDeyMolinaro2017}); we need its explicit constants." Add to Lemma
`lem:unique-growth`: "This is standard second-order theory for quadratic programs
\cite{Contesse1980}." Cite Hadamard's inequality (e.g. Horn–Johnson, *Matrix Analysis*,
Section 7.8) instead of proving it.

**m8. The monotonicity test is credited to a later constraint-programming paper.** appendix-boundary.tex:76-80.
Hansen 1980 and Hansen–Walster 2004 are already in references.bib but not cited; Garloff 1986
(Bernstein bounds) likewise. Fix: "Such monotonicity tests are standard in interval global
optimization \cite{Hansen1980,HansenWalster2004,ArayaTrombettoniNeveu2010}; Bernstein bounds are
due to \cite{Garloff1986}."

**m9. Classical information-based-complexity arguments need a source.** limits.tex:544-545 (Prop.
`prop:oraclebarrier`). Fix: cite \cite{NemirovskiYudin1983} there as at limits.tex:231, or
Novak, *Deterministic and Stochastic Error Bounds in Numerical Analysis*, LNM 1349 (1988).

**m10. The rETH and multicolored-clique sources are incomplete.** appendix-lbproduct.tex:57-61; limits.tex:346.
Chen et al. 2006 prove the clique bound under ETH. rETH is usually cited from Dell, Husfeldt,
Marx, Taslaman, Wahlén, ACM TALG 10(4):21 (2014), doi:10.1145/2635812. The multicolored-clique
form is in Cygan et al., *Parameterized Algorithms* (Springer 2015), Chapter 14. Fix: cite both.

**m11. Missing references a referee would expect.** (Metadata verified on Crossref or arXiv unless noted.)
- Rates for sparse SOS hierarchies. intro.tex:22-25 says the sparse hierarchies of Waki et al. and
  Lasserre have "sizes polynomial in the inverse accuracy". Those papers prove only asymptotic
  convergence. Cite Korda, Magron, Ríos-Zertuche, "Convergence rates for sums-of-squares
  hierarchies with correlative sparsity", Math. Program. 209:435–473 (2025),
  doi:10.1007/s10107-024-02071-6, or drop the clause for the SDP hierarchies. Optionally add
  Wang–Magron–Lasserre, TSSOS, SIOPT 31(1):30–58 (2021).
- Exact tree DP with piecewise-quadratic messages: Kolmogorov, Pock, Rolinek, "Total variation on
  a tree", SIAM J. Imaging Sci. 9(2):605–636 (2016); Kuric, Ahmetspahic, Pock, "Total generalized
  variation on a tree", SIAM J. Imaging Sci. 17(2):1040–1077 (2024). DPK note that the latter has
  exponential worst case for nonconvex terms. This belongs next to Example `ex:chain` and
  Prop. `lim:prop:messages`.
- Path hardness for polynomial systems: Cifuentes–Parrilo, SIDMA 30(3):1534–1570 (2016) (with M1).
- Polynomial box-QP classes and graph-based exactness, both already in references.bib but not
  cited: Hladík–Černý–Rada, Optim. Lett. 15(6):2331–2341 (2021); Sojoudi–Lavaei, SIOPT
  24(4):1746–1778 (2014). The latter belongs at related.tex:175-176.
- Local versus global consistency: Vorob'ev, "Consistent families of measures and their
  extensions", Theory Probab. Appl. 7(2):147–163 (1962), at related.tex:178-179 and in the
  discussion after Prop. `lim:prop:moments` (limits.tex:665-667).
- Already in references.bib but not cited:
  - De Loera et al. 2008 and Hildebrand–Weismantel–Zemmer 2016 (approximation schemes,
    related.tex:24-30);
  - Pardalos–Vavasis 1991 (the source of the "cannot be polylogarithmic" arguments);
  - Breiman–Cutler, Math. Program. 58:179–199 (1993), the classical deterministic global method
    with second-order information (related.tex:36-37).
- Rigorous and certified global optimization, for Section 10 and the conclusion. The paper
  stresses that floating-point solvers violate tolerances. Cite Neumaier–Shcherbina, "Safe bounds
  in linear and mixed-integer linear programming", Math. Program. 99:283–296 (2004) and an
  interval global-optimization text (Kearfott 1996; Hansen–Walster 2004).
- Solver version: computation.tex:144-145 uses SCIP 10.0 but cites the SCIP 8.0 paper. Cite
  Hojny et al., "The SCIP Optimization Suite 10.0", arXiv:2511.18580 (2025).
- Optional:
  - Bürgisser–Cucker, *Condition* (Springer 2013), for complexity parameterized by a condition
    number;
  - Füllner–Rebennack, "Non-convex nested Benders decomposition", Math. Program.
    196:987–1024 (2022), for the stage-structured models that open the introduction.

**m12. Bibliography hygiene.** references.bib.
- (a) 43 entries are never cited, including duplicates of cited ones: Khajavirad2026Poly vs
  Khajavirad2026PolyBox, Khajavirad2026SDP vs Khajavirad2026SparseSDP, BhathenaEtAl2026 vs
  BhathenaEtAl2026Graphs, ChervetGrappeRobert2018/2021, SpjotvoldTondelJohansen2005 vs
  SpjotvoldEtAl2006.
- (b) The provenance comments sit above the wrong entries, shifted by one. For example,
  "numdam scan read: Lemma and Proposition 1, p. 96" (Rosenberg) is above ChenEtAl2006
  (line 506), "max-separation formula p. 1141" (Adjiman) is above MisenerFloudas2014
  (line 1724), and "Theorem 1 and Property 1" (Bajaj–Hasan) is above Neumaier2004 (line 1821).
  The record of which entries were verified is therefore unreliable.
- (c) Korhonen2021 lacks pages 184–192.
- (d) GartnerJaggiMaria2012 lacks pages 168–195 (checked at jocg.org). Its DOI is not
  registered at Crossref but resolves.
- (e) Edmonds1970 prints as "Edmonds (2003)". Cite the 1970 Calgary proceedings, pp. 69–87,
  with the reprint as a note.
- (f) Topkis1998 carries the DOI of the 2011 e-book edition.
- (g) GomezHan2025: arXiv lists the authors as Han, Gómez. The order in the PDF was reported
  as Gómez, Han; use one consistently and state the source.
- (h) The Crossref audit of the 131 cited entries with a DOI found no other substantive
  mismatch (`checks/r7_bib_audit.py`).

**m13. The conclusion and abstract state the lower bounds more strongly than the propositions prove.**
- conclusion.tex:13-15 says "the dependence on the condition number must be polynomial".
  Corollary `lim:cor:nopolylog` excludes only polylogarithmic dependence.
- abstract.tex:24-25 and intro.tex:130-131 say the exponent "must grow linearly with p".
  Prop. `prop:lbproduct` proves a(p) ≠ o(p).

Fix: "cannot be polylogarithmic in $\kappa$ unless P${}={}$NP, and under rETH its exponent cannot
be $o(p)$."

**m14. Stray reference to "the report".** recourse-balanced.tex:163-164 ("in the cut-based
recourse of the report"). Fix: "in Theorem~\ref{thm:cr-oracle}".

**m15. Notation clash with DPK.** DPK (and Khajavirad, Lemma 20 there) use κ for the number of
rows to delete before all principal submatrices are PSD. Fix: a footnote at
Definition `def:growth` stating that the paper's κ is unrelated.

**m16. Some value-function results lack an attribution at the point of use.** recourse-valuefn.tex:13-36
(Lemma `lem:valuefunction`); recourse-convex.tex near Thm `thm:cv`.
Infima of semiconcave functions are semiconcave (Cannarsa–Sinestrari), and Khajavirad
(arXiv:2604.25033, Thm 1 and its proof) eliminates positive-diagonal components into value
functions of binary neighbours. Both appear only in related.tex. Fix: one sentence at each place,
e.g. "Part (a) is the classical stability of semiconcavity under infima
\cite{CannarsaSinestrari2004}." At Thm `thm:cv`: "Khajavirad \cite{Khajavirad2026PolyBox}
eliminates continuous components into value functions of enumerated binary neighbours; here the
neighbours are continuous and gridded, and what is certified is the curvature of the value
factor."

## 4. Search for recent overlapping work (2025-2026)

Queries were run on the web, on arXiv/Crossref, and in the local knowledge base. They covered:
treewidth or bag size plus condition number for box QP; FPT under quadratic growth;
accuracy-independent discretization with log(1/ε) dependence; grid DP lower bounds with an
L h²/8 interpolation correction and min-marginals; certified exact-arithmetic box-QP solving;
follow-ups to Del Pia–Khajavirad.

| Work found | Overlap |
|---|---|
| Del Pia–Khajavirad, arXiv:2609.35595 (2026-09-28) | Cited; it is the foil. No conditioning parameter. |
| Khajavirad, arXiv:2604.25033v2 (2026-08-19); arXiv:2601.18545v2 | Cited; structural classes and SDP exactness, no conditioning. |
| Bhathena et al., arXiv:2603.02103 (2026) | Cited; treewidth + margin + conditioning, but convex with indicators. See m3. |
| Herrmann, arXiv:2608.17818 (2026-08-18) | Not cited; IQP W[1]-hard by number of variables. Complements the limits; see m4. |
| Del Pia, arXiv:2607.29386 (2026-07-31) | Cited; poly(1/ε) for fixed negative inertia. |
| Burer–Natarajan–Willemsen v3 (2026-08-31) | Cited correctly. |
| Hermelin et al., "Approximating sparse quadratic programs" (arXiv:2007.01252) | Binary ±1 maximization; not relevant. |

No paper was found that gives:
- f(p,κ)poly(I+q) certified approximation or f(p,κ)poly(I) exact solution for nonconvex or
  mixed-integer box QP;
- a node-separable corrected-grid bound on tree decompositions;
- accuracy-independent grid sizes under global growth.

The search cannot prove absence. It supports the paper's "to our knowledge" wording.

## 5. Checks run (targeted, local)

All checks are in `process/w2/checks/`, run with Python 3 and exact `fractions.Fraction` where
arithmetic is involved. Each ran in under 3 minutes, one process at a time.

- `python3 r7_dpk_remark.py`: **PASS**. It rebuilds DPK's (20)–(24) for a=(B,B−1), T=B with
  B ∈ {3,4,5,8,16,32} and confirms:
  - 5ℓ+2 variables, and 5m+7 for B=2^m;
  - Ψ(v*)=0 and Ψ(y′)=1/D²;
  - ‖y′−v*‖² ≥ 2ℓ;
  - maximum Hessian diagonal 10;
  - Ψ at the fractional choice (1/B,1) equals q/B, with the point in the unit box.

  This supports Remark `lim:rem:dk` as a transcription of DPK.
- `python3 r7_bib_audit.py`: compared the 131 cited entries that have a DOI against Crossref
  (title, first author, year, volume, pages). Only cosmetic differences, listed in m12; one DOI
  (JoCG) is not registered at Crossref but resolves.
- `python3 r7_crossref.py ...` and `python3 r7_crossref_title.py ...`: metadata of individual
  entries and of the proposed new references.
- arXiv API: all ten arXiv entries match their arXiv records (titles, authors, versions, dates).
  The only difference is the author order of GomezHan2025.
- Primary-source reading: DPK, Bienstock–Muñoz and GLS from the local PDFs or full texts. Luo–Sturm,
  Kolmogorov–Zabih, Del Pia 2023 and 2026, Bhathena (both), the cluster papers, BNW, AMP and
  Gupte et al. from KB notes and full texts. Li–Wu–Quan and Bajaj–Hasan from abstracts only.

No project-wide verification was run and no CI was consulted.
