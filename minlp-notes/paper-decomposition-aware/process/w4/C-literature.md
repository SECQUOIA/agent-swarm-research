# C-literature: literature and novelty review (W4)

Paper: "Decomposition-aware global optimization: certified coordinate grids, conditional
recourse, and structural limits" (`paper-decomposition-aware/`, sources `main.tex`,
`sections/*.tex`; PDF `/tmp/dpaper/out/main.pdf`). Reviewer key: C-literature. Date: 2026-10-03.
No file in `sections/`, `main.tex`, `macros.tex` or `references.bib` was edited. Check scripts are
in `process/w4/checks/C-literature-*.py`.

## Verdict

No critical issue. The central novelty statement (intro.tex:109-112, related.tex:54-56: no
earlier `f(p,kappa) poly(I+q)` certified approximation or `f(p,kappa) poly(I)` exact algorithm for
nonconvex or mixed-integer box QP) survives an independent search (Section 4). The closest works
remain Bhathena et al. (convex QP with indicators, treewidth plus margin, volume growth and
condition numbers), Del Pia-Khajavirad (forests exact, treewidth two strongly NP-hard), Khajavirad
(structural classes), Bienstock-Munoz (`poly(1/eps)`) and the cluster-problem literature. All
citations I checked against primary sources say what the paper attributes to them; the arXiv and
Crossref metadata of the 53 entries I checked are correct.

There is one major issue. The closest classical antecedent of the paper's central mechanism, the
proximity-scaling algorithm of Hochbaum and Shanthikumar (1990), is described only as an algorithm
"logarithmic in the domain size for ... integer programs". That algorithm also solves continuous
separable convex problems to accuracy eps with `log2(B/2eps)` grids whose size does not depend on
eps. Its totally unimodular specialization, together with Meyer (1977), uses the same grid
integrality as Lemma `lem:tu-round`. A paragraph comparing it with Section 8 existed before W3,
was deleted from `rem:tu-bm` to keep one place per comparison, and was never added to
`related.tex`. The minor issues are imprecise attributions (Bajaj-Hasan vs Hasan 2018, the
Turing-model status of Vavasis 1992, the "open complexity from dimension four" wording for
Burer-Natarajan-Willemsen), missing sources for two standard constructions in Section 9, missing
related work in four places (exact SOS certificates, LP optimal-face identification, certified
Lipschitz optimization, decision-diagram MINLP/fixed-dimension MIQP), one locator, and
bibliography hygiene.

## 1. Findings

### Major

**C-literature-1. Hochbaum-Shanthikumar proximity scaling (and Meyer 1977) is the closest
classical antecedent of accuracy-independent grids and of the TU grid rounding, but the paper
mentions it only as an integer method.**
Locations: related.tex:113-116 (only mention), related.tex:141-143, related.tex:203-207,
constraints.tex:652-680 (`rem:tu-bm`), growth.tex:177-178.

*What is wrong.* The paper's main mechanism is a sequence of stages with a fixed number of grid
nodes per coordinate in a window that shrinks around the current solution, with `O(log(1/eps))`
stages (abstract; Lemma `lem:states`; Theorem `thm:tu-states` for TU coupling). Hochbaum and
Shanthikumar (J. ACM 37(4):843-862, 1990) do exactly this for separable convex objectives over
`{Ax >= b}`. They keep a box that contains an optimum, put a grid of `O(n Delta)` points on each
variable (`Delta` bounds the subdeterminants of `A`), solve the piecewise-linear grid problem by
LP, and halve the box using a proximity theorem. For the continuous problem this gives an
eps-accurate solution in `log2(B/2eps) * T(8n^2 Delta, m, Delta)` (Theorem 1.1; overview in
Section 1.3; proximity in Theorems 3.3 and 3.7-3.8; TU specialization in Theorem 4.3). This is the
proximity-scaling template, with proximity where the paper uses growth. The paper describes the
work only as "algorithms logarithmic in the domain size for linear and separable convex integer
programs" (related.tex:113-116). It also closes the adaptive-discretization paragraph with "None
of these methods certifies a given accuracy with a number of states independent of that accuracy"
(related.tex:141-143). The sentence is true for the methods of that paragraph, but a reader will
apply it to the field, and Hochbaum-Shanthikumar guarantee such a count for their class. They do
not produce a checkable certificate.

For the TU extension: Lemma `lem:tu-round` writes a feasible point as a convex combination of
feasible grid points of its cell, using integrality of the cell polytope of a TU system with
aligned right-hand side (Hoffman-Kruskal). Meyer, "A class of nonlinear integer programs solvable
by a single linear program", SIAM J. Control Optim. 15(6):935-946 (1977), and Hochbaum-Shanthikumar
(Algorithm 4.2, Theorem 4.3) use the same integrality to solve separable convex problems with TU
constraints by piecewise-linear interpolation on an aligned grid. related.tex:203-207 credits only
Hoffman-Kruskal and dependent rounding.

*History.* Before W3, `rem:tu-bm` ended with a correct comparison
(`process/w3/sections-before-w3/constraints.tex:840-847`). The tu group deleted it (W2 F11, "one
place per comparison") and proposed an optional sentence for `related.tex`
(`process/w3/reports/tu.md:139-145`). That sentence was never added, so the comparison is now
missing.

*Fix.* Replace related.tex:113-116 ("Proximity and scaling ... EisenbrandEtAl2025}.") by:

> Proximity and scaling give algorithms logarithmic in the domain size for linear and separable
> convex integer programs \cite{CookGerardsSchrijverTardos1986,HochbaumShanthikumar1990,
> GranotSkorinKapov1990,HunkenschroderEtAl2026,EisenbrandEtAl2025}. The scaling algorithm of
> Hochbaum and Shanthikumar is the closest classical analogue of our stages: at each scale it
> optimizes on a grid of $O(n\Delta)$ points per variable, where $\Delta$ bounds the
> subdeterminants of the constraint matrix, inside a window around the previous solution, and a
> proximity theorem lets it halve the window; for continuous separable convex problems this gives
> accuracy $\varepsilon$ with $\log_2(B/2\varepsilon)$ grids whose size does not depend on
> $\varepsilon$ \cite[Theorems~1.1 and~3.3]{HochbaumShanthikumar1990}. Here the objective is
> nonseparable and nonconvex, the window comes from growth instead of proximity, and the grid
> problems are solved by dynamic programming over a tree decomposition.

In related.tex:203-205, after the Hoffman-Kruskal sentence, add:

> For separable convex objectives over totally unimodular constraints, piecewise-linear
> interpolation on an aligned grid is exact because the linear program has integral vertices
> \cite{Meyer1977,HochbaumShanthikumar1990}; Lemma~\ref{lem:tu-round} uses the same integrality to
> round mean-preservingly for nonseparable, nonconvex objectives.

New entry (Crossref-verified):
```
@article{Meyer1977,
  author  = {Meyer, R. R.},
  title   = {A class of nonlinear integer programs solvable by a single linear program},
  journal = {SIAM Journal on Control and Optimization},
  volume  = {15}, number = {6}, pages = {935--946}, year = {1977},
  doi     = {10.1137/0315059}
}
```
Optionally qualify related.tex:141-143 with "... with a number of states independent of that
accuracy for nonconvex objectives".

### Minor

**C-literature-2. "leave the complexity open from dimension four on" is incorrect for fixed
dimension.** related.tex:188-191.
For every fixed `n`, box QP is solvable in (strongly) polynomial time by enumerating the `3^n`
faces and solving a linear system on each (Del Pia-Khajavirad, p. 1, citing Vavasis 1990 and Del
Pia-Dey-Molinaro 2017). The open question in BNW footnote 2 is whether continuous submodular box QP
is polynomial when `n` is part of the input. recourse-cuts.tex:152-155 states this correctly ("the
complexity of that class is open"). Fix: "... give a four-variable gap, and leave open whether the
problem is polynomial-time solvable when the dimension is part of the input
\cite[footnote~2]{BurerNatarajanWillemsen2026v3} (for each fixed dimension it is, by enumerating
faces \cite{Vavasis1990})".

**C-literature-3. The edge-concave underestimator is attributed to Bajaj-Hasan 2020 instead of
Hasan 2018.** grids.tex:45-49 (also intro.tex:53-57).
Hasan, J. Glob. Optim. 71(4):735-752 (2018) introduced the edge-concave underestimator obtained by
"subtracting a positive quadratic expression such that all non-edge-concavities in the original
function is overpowered", with a vertex-polyhedral envelope (abstract, RePEc). Bajaj-Hasan 2020
apply it to black-box functions with "a global upper bound on the diagonal Hessian elements" and
evaluate it at the vertices (AIChE 2018/2019 abstracts; the full text is paywalled). grids.tex
credits the construction to Bajaj-Hasan. Fix (grids.tex:45-48): "For a single cell this is the
vertex bound of Bajaj and Hasan \cite{BajajHasan2020}, who evaluate at the vertices the
edge-concave underestimator of Hasan \cite{Hasan2018}, built from an upper bound on the diagonal
Hessian entries; we use one bound $L_i$ per coordinate."

**C-literature-4. Vavasis 1992 is listed with Turing-model results although its algorithm is not
one.** related.tex:43-44.
Del Pia (arXiv:2607.29386, p. 2) writes that the algorithm of Vavasis 1992 "relies on a
simultaneous diagonalization of two matrices which ... cannot be carried out on a Turing machine
... our result is thus new already for p = 0". In a paper that counts bit operations, the sentence
"for QP with a fixed number of negative eigenvalues \cite{Vavasis1992}" therefore overstates the
source. Fix: "... for QP with a fixed number of negative eigenvalues (\cite{Vavasis1992} in a model
with exact real arithmetic; in the bit model \cite{DelPia2026Jacobi}), ...". The later sentence
(related.tex:48-52) on why `1/eps` cannot become polylogarithmic is correct for both papers
(Vavasis 1992, Section 6; Del Pia 2026, p. 2).

**C-literature-5. Two standard constructions in Section 9 are not attributed where they are used.**
limits.tex:286-288; limits.tex:374-376; intro.tex:214-217.
(a) Prop. `prop:lbwidth` uses "the standard box formulation of maximum independent set" without a
source. The identity `alpha(G) = max_{x in [0,1]^n} sum_i x_i - sum_{ij in E} x_i x_j` is in
Abello, Butenko, Pardalos, Resende, J. Glob. Optim. 21(2):111-137 (2001), doi
10.1023/A:1011968411281. Add the citation after "maximum independent set".
(b) Prop. `prop:lbproduct` encodes multicolored clique as a constraint problem with `k` variables
of domain size `N_0` and treewidth `k-1`. This is the standard source of `n^{o(k)}` lower bounds
under ETH (Chen et al. 2006; Cygan et al., Theorem 14.21, both cited in the appendix). For general
binary CSPs, Marx, "Can you beat treewidth?", Theory Comput. 6:85-112 (2010), doi
10.4086/toc.2010.v006a005, shows the analogous bound in terms of treewidth. The intro lists "the
rETH bound" as new without saying what is new. Fix: after limits.tex:374-376 add "The encoding is
the standard reduction from multicolored clique to constraint problems of width $k$ with domain
size $N_0$ \cite{ChenEtAl2006}; what is new is a quadratic encoding with a unique minimizer, by
isolation, and $\kappa$ polynomial in $N_0$." Optionally cite Marx (2010) there.

**C-literature-6. Exact rational SOS certificates and the current state of exact MIP are missing
from the certificate paragraph.** related.tex:90-97.
The paper's certificates are exact-rational, checkable lower bounds for a nonconvex continuous
problem. The closest existing certificates of that kind are rational sum-of-squares certificates:
Peyrl and Parrilo, Theor. Comput. Sci. 409(2):269-281 (2008), doi 10.1016/j.tcs.2008.09.025;
Kaltofen, Li, Yang and Zhi, ISSAC 2008, pp. 155-164, doi 10.1145/1390768.1390792. For exact MIP,
the current reference with certificate output is Eifler and Gleixner, Math. Program.
197(2):793-812 (2023), doi 10.1007/s10107-021-01749-5. Fix: after "...our certificates use exact
rational arithmetic instead." add: "For polynomial objectives, rational sum-of-squares
certificates give exact lower bounds \cite{PeyrlParrilo2008,KaltofenEtAl2008}; they certify a
relaxation value, whereas the path certificate certifies $\OPT$ itself to accuracy $2^{-q}$."
Optionally add EiflerGleixner2023 next to CookKochSteffyWolter2013.

**C-literature-7. The snapping recovery has a classical LP antecedent that is not cited.**
related.tex:150-153; exact.tex:186-196 (Algorithm `alg:rec`).
REC fixes the coordinates within `tau` of a bound and solves the stationarity system on the
rest. Once the gap is below a threshold set by the encoding length, the active set is identified
and an exact solution follows. For LP this is optimal-face identification: Ye, Math. Program.
57:325-335 (1992), doi 10.1007/BF01581087; Mehrotra and Ye, Math. Program. 62:497-515 (1993), doi
10.1007/BF01585180. Fix: in related.tex:150-152 add "and identifying the optimal face once the gap
is below an encoding-length threshold is classical for linear programming \cite{Ye1992,
MehrotraYe1993}; Lemma~\ref{lem:snap} does this for box QP with set growth in place of LP
duality."

**C-literature-8. The modern certified-evaluation result for Lipschitz optimization is missing.**
related.tex:110-113.
Perevozchikov (1990) is cited for `O(log(1/eps))` evaluations; I checked the claim against the
Math-Net.Ru abstract: `O(ln eps_0^{-1})` when `r = 1`. Bachoc, Cesari and Gerchinovitz, NeurIPS 34
(2021), pp. 24180-24192 (arXiv:2102.01977), show that the optimal number of evaluations needed to
find and certify an eps-optimal point of a Lipschitz function is, up to constants,
`int dx/(f* - f(x) + eps)^d`. This is the sharp, certified form of the same phenomenon and is
logarithmic in `1/eps` when growth matches the smoothness. Fix: append "; Bachoc, Cesari and
Gerchinovitz characterize the number of evaluations needed to certify accuracy $\varepsilon$
\cite{BachocCesariGerchinovitz2021}".

**C-literature-9. Related work on DP over partitioned continuous domains, and on fixed-dimension
MIQP, is incomplete.** related.tex:122-143; related.tex:40-42.
(a) Decision-diagram methods for MINLP are dynamic programs over partitioned continuous domains
that give relaxation bounds and are refined by spatial branching: Davarnia, Kiaghadi and Qiu,
J. Glob. Optim. 96 (2026), doi 10.1007/s10898-026-01635-4; Davarnia and van Hoeve, Math. Program.
187:111-150 (2021), doi 10.1007/s10107-020-01475-4. They belong in the adaptive-discretization
paragraph, and the paragraph's last sentence still holds for them.
(b) related.tex:40-42 lists only approximation schemes in fixed dimension. Exact algorithms exist
for integer QP in the plane (Del Pia and Weismantel, SODA 2014, pp. 840-846, doi
10.1137/1.9781611973402.62) and, in a September 2026 preprint, for MIQP in every fixed dimension
(Ari and Hildebrand, arXiv:2609.18266v2). Add one clause.
Both items are optional additions; neither changes a novelty statement.

**C-literature-10. The Schlesinger-Flach locator is incomplete.** recourse-balanced.tex:41-43.
"Threshold encodings, and the reduction ... to one minimum cut, are classical
\cite[Section~4]{SchlesingerFlach2006}". In TR TUD-FI06-01 the threshold ("K to 2") encoding is
Section 3, and the min-cut construction is Section 4 (table of contents, p. 1). Fix:
`\cite[Sections~3--4]{SchlesingerFlach2006}`.

**C-literature-11. Bibliography and source hygiene.** references.bib:215, 1215;
sections/appendix-smoothed.tex:74.
(a) Two provenance comments, which do not print, sit above the wrong entries. Above
`Khajavirad2026PolyBox` (an arXiv preprint) is "W3: Crossref (title, author, year, series);
series volume 13 from publisher and catalogue records", which is the comment of the deleted
`Kearfott1996` (NOIA vol. 13). Above `BhathenaEtAl2026Graphs` (arXiv, no DOI) is "Crossref (R7
audit of cited DOIs, W2)". W3 reported the comments as realigned. (b) `sections/appendix-smoothed.tex`
is not included anywhere (`appendix.tex` does not input it), and it cites `BeierVocking2004` and
`RoglinVocking2007`, which are not in `references.bib`. Delete the file or add the entries if it
is ever included.

## 2. Novelty statements checked

| Statement | Location | Assessment |
|---|---|---|
| No earlier `f(p,kappa) poly(I+q)` certified approximation or `f(p,kappa) poly(I)` exact algorithm for nonconvex or mixed-integer box QP | intro.tex:109-112; related.tex:54-56 | Survives (Section 4). Hochbaum-Shanthikumar (separable convex), Bhathena et al. (convex with indicators), Eiben et al. (bounded domains), Ari-Hildebrand (fixed dimension) do not cover the class. "To the best of our knowledge" is appropriate. |
| Node-separable correction reproduces the Bajaj-Hasan vertex bound; best cellwise bound by one tree DP | intro.tex:53-60; grids.tex:42-53; related.tex:74-77 | Correctly framed as an observation. No source with the grid-wide node-unary form was found. Attribution detail: C-literature-3. |
| DP, min-marginals, OBBT filter and checkable certificate are classical; "only new element is that its input is Q"; "all interval bounds of a stage come from one pair of message passes" | grids.tex:185-189, 292-296 | Accurate. |
| Global, non-asymptotic form of the cluster phenomenon | related.tex:105-109 | Accurate relative to the cluster literature (Wechsung et al. Table 1: one box iff prefactor <= lambda_1/8, checked in the local full text). Hochbaum-Shanthikumar is missing as an antecedent: C-literature-1. |
| "None of these methods certifies a given accuracy with a number of states independent of that accuracy" | related.tex:141-143 | True for the methods of that paragraph; see C-literature-1. |
| Expanding-box chain, unique-minimizer hardness (refining DPK Remark 2), rETH bound, moment obstruction new; others adapt standard constructions | intro.tex:214-217 | Plausible; no prior source found for these statements. DPK Remark 2 checked (weak NP-hardness via `{s_{i-1}, s_i, x_i}` bags). The rETH bound reuses the standard clique-to-CSP template: C-literature-5. |
| Running-sum Subset Sum encoding credited to Bienstock-Munoz and Cifuentes-Parrilo; "what we add is a unique minimizer and the growth constant" | limits.tex:621-626 | Correct (DPK, p. 25, describes both antecedents the same way). |
| Parametric QP, cut representations and threshold encodings classical; contribution is curvature and growth accounting | intro.tex:242-246; recourse-convex.tex:263-265; recourse-balanced.tex:41-46 | Accurate. |
| Optimal-set description combines Rosenberg with zero-residual labelings; new: strictly concave coordinates, mixed boxes, factored form | intro.tex:282-288; optsets.tex:458-474 | Accurate (Rosenberg credited; WJW 2005 and Werner 2007 credited). |
| Diagonal certificate classical; what is used is invariance | intro.tex:292-294; optsets.tex:530-535 | Accurate. |
| TU extension "narrower class but exactly feasible" vs Bienstock-Munoz | intro.tex:264-268; constraints.tex:652-680 | Accurate (BM Theorems 4 and 15 checked). Missing Hochbaum-Shanthikumar/Meyer: C-literature-1. |
| Footnote: our kappa unrelated to DPK Lemma 20 (a result of Khajavirad) | setting.tex:103-106 | Correct: DPK Lemma 20 is labelled "([22])", and [22] is arXiv:2604.25033. |

## 3. Citation checks (locators and attributed content)

| Citation | Paper's claim | Source checked | Result |
|---|---|---|---|
| DelPiaKhajavirad2026, Theorems 1-3 (related.tex:19) | forests strongly polynomial; quartic on paths strongly NP-hard; treewidth two strongly NP-hard with bounded integers | local PDF text: Thm 1 (p. 4, O(n^2)), Thm 2 (p. 18), Thm 3 (p. 20, ‖Q‖max<=5, ‖c‖inf<=4) | Correct |
| DelPiaKhajavirad2026, Remark 2 (limits.tex:57; intro.tex:216; optsets.tex:647) | simple weak NP-hardness reduction from Subset Sum, bags `{s_{i-1},s_i,x_i}` | text p. 25 | Correct |
| DelPiaKhajavirad2026, Theorem 4 (recourse-cuts.tex:148) | log treewidth and log interfaces of nonpositive-diagonal part, low-rank coupling | Thm 4 (p. 27) and the discussion of its assumptions 1-3 (p. 31) | Correct |
| DelPiaKhajavirad2026, Lemma 20 (setting.tex:104) | integer kappa = rows to delete before principal submatrices are PSD; result of Khajavirad | p. 32 | Correct |
| DelPiaKhajavirad2026, Theorem 3 and (20)-(24) (appendix-lbproduct.tex:11) | bounded-coefficient construction | proof of Thm 3, eqs (19)-(25) present | Locators correct (numbers re-derived in W2) |
| BienstockMunoz2018, Theorem 4 (related.tex:43) and Theorems 4 and 15 (constraints.tex:653) | LP size `O((2pi/eps)^{omega+1} n log(pi/eps))`, scaled violation, eps-dependence not improvable unless P=NP | arXiv v15: Thm 4 (p. 2), Thm 15 (p. 7), Sec. 2.0.3 (p. 9), App. A (p. 24) | Correct (bib note states v15 numbering) |
| DvijothamEtAl2017, Theorem 2 (related.tex:131) | interval DP on trees, approximately feasible, superoptimal, `poly(1/eps)` bound evaluations | Constraints version, Thm 2 (p. 16-17; max degree 3, `n zeta' eps^{-5}` calls) | Correct |
| LuoSturm2000, Theorem 3.3 (exact.tex:267; related.tex:155) | `dist(x,S) <= c |g(x)|^{1/2}` for one quadratic on a polytope | local package notes (p. 11) | Correct |
| GrotschelLovaszSchrijver1988, Section 5.1 and Theorem 5.1.9 (related.tex:151; exact.tex:389) | continued fractions; best approximation in polynomial time | full text: 5.1 "Continued Fractions", (5.1.9) p. 137 | Correct |
| GLS Theorem 6.4.12 (exact.tex:195; constraints.tex:544; appendix-proximal.tex:164) | exact LP in polynomial time | (6.4.12) Khachiyan's theorem | Correct |
| GLS Theorem 6.4.9, Lemma 6.5.15 (appendix-recourse-cuts.tex:228) | separation/optimization; basic dual solution | full text | Correct |
| CyganEtAl2015, Theorem 14.21 (appendix-lbproduct.tex:135) | no `f(k) n^{o(k)}` for Clique under ETH | secondary (arXiv:2311.08988 quotes it) | Correct |
| HornJohnson2013, Theorem 7.8.1 (exact.tex:52) | Hadamard's inequality | secondary only (arXiv:2112.01462 cites "[HJ] Theorem 7.8.1") | Plausible, not checked in the book |
| CifuentesParrilo2016, Example 1.1 (intro.tex:212; limits.tex:625) | Subset Sum for quadratic systems on a path | arXiv v2 p. 2 (W3); DPK p. 25 calls it "Example 1" | Correct for arXiv numbering |
| BurerNatarajanWillemsen2026v3, footnote 2 (recourse-cuts.tex:155) | complexity open for n >= 4 | local text, footnote 2 | Locator correct; wording issue in related.tex: C-literature-2 |
| BurerNatarajanWillemsen2026v3 (related.tex:183-191) | DR-submodular reduces to cuts; SDP exact n<=3; Example 4 gap at n=4 | local text: p. 2, Thm 1, Ex. 4 | Correct |
| SchlesingerFlach2006, Section 4 (recourse-balanced.tex:43) | threshold encodings and min-cut | TR TUD-FI06-01 TOC | Section 3 also needed: C-literature-10 |
| Schrijver1986, Chapter 20 (constraints.tex:322) | TU recognition | chapter title "Recognizing total unimodularity" (from memory) | Correct; Section 19.1 locator (constraints.tex:166) not checked |
| Perevozchikov1990 (related.tex:112-113) | `O(log(1/eps))` evaluations for Lipschitz functions with small near-optimal sets | Math-Net.Ru abstract: `O(ln eps_0^{-1})` if r=1 | Correct |
| BhathenaEtAl2026Trees/Graphs (related.tex:29-35) | `O(n^2)` on trees; linear in n for fixed width, margin, volume growth, condition numbers | arXiv abstract; local text p. 23 (fixed omega, (k,eta), kappa_2, kappa_inf, (delta,gamma)) | Correct |
| Khajavirad2026PolyBox (related.tex:20; recourse-convex.tex:265) | binary restriction of nonpositive-diagonal variables, componentwise elimination of continuous parts | arXiv abstract v2; DPK p. 2 | Correct |
| Vavasis1992; DelPia2026Jacobi (related.tex:44-52) | `poly(1/eps)` for fixed negative inertia; why not polylog | Vavasis local text (Sec. 6, "Dependence of the running time on the parameters"); Del Pia p. 2 | Correct, but see C-literature-4 |
| EibenEtAl2019; Lokshtanov2015; Herrmann2026 (related.tex:36-39) | FPT with bounded domains; FPT in #vars plus coefficients; W[1]-hard in #vars | local text (Thm 8, Thm 13); arXiv abstracts | Correct |
| HochbaumShanthikumar1990 (related.tex:113-116) | logarithmic in domain size for separable convex IP | local text: Thms 1.1, 1.2, 3.3, 4.3 | Correct but incomplete: C-literature-1 |
| WechsungSchaberBarton2014 (related.tex:100-104) | count independent of tolerance with second-order bounds; can be exponential | local text Table 1, p. 8 | Correct ("can be") |
| BajajHasan2020 (grids.tex:45-48; related.tex:68-70) | vertex bound from upper bound on Hessian diagonal | AIChE 2018/2019 abstracts; Crossref | Consistent; see C-literature-3 |

## 4. Searches for prior or overlapping work

Queries (WebSearch, arXiv API, Crossref, local knowledge base `literature/papers`) on:
treewidth or bag size with a condition number for box QP; FPT under quadratic growth; grid DP
lower bounds with an `L h^2/8` correction; certified MINLP and exact-arithmetic checkers;
follow-ups to Del Pia-Khajavirad (Sept. 2026); continuous submodular minimization; ETH and rETH
bounds for integer QP and CSP; edge-concave underestimators; certified Lipschitz optimization.

| Work found | Relation |
|---|---|
| Hochbaum-Shanthikumar 1990; Meyer 1977 | Closest antecedent of accuracy-independent grids and of TU grid integrality: C-literature-1 |
| Bachoc-Cesari-Gerchinovitz 2021 | Certified evaluation counts for Lipschitz functions: C-literature-8 |
| Peyrl-Parrilo 2008; Kaltofen et al. 2008; Eifler-Gleixner 2023 | Exact rational certificates: C-literature-6 |
| Ye 1992; Mehrotra-Ye 1993 | Optimal-face identification in LP: C-literature-7 |
| Davarnia-Kiaghadi-Qiu 2026 (JOGO); Davarnia-van Hoeve 2021 | DD-based MINLP: C-literature-9 |
| Ari-Hildebrand, arXiv:2609.18266 (Sept. 2026); Del Pia-Weismantel 2014 | Exact MIQP in fixed dimension: C-literature-9 |
| Marx 2010; Abello et al. 2001 | Templates of Section 9 lower bounds: C-literature-5 |
| Bagirov-Laha-Martinez-Legaz, arXiv:2608.30611 (Aug. 2026) | DC method for box QP, no complexity claim; not relevant |
| Hasan 2018; Nath Roy-Hasan (separable edge-concave, AIChE 2025) | Single-box underestimators; no grid or DP form |

No work was found that gives an `f(p,kappa) poly(I+q)` or `f(p,kappa) poly(I)` bound for
nonconvex or mixed-integer box QP, a node-separable corrected-grid bound on tree decompositions,
or accuracy-independent grids for nonconvex nonseparable objectives. A search cannot prove
absence; the result supports the paper's "to our knowledge" wording.

## 5. Bibliography metadata checks

* `process/w4/checks/C-literature-crossref.py` compared 40 entries with Crossref (title, first
  author, year, volume, issue, pages): BajajHasan2020, BhathenaEtAl2026Trees, DeyKhajavirad2026,
  NagarajanEtAl2019, CheungGleixnerSteffy2017, HochbaumShanthikumar1990, LuoSturm2000,
  Contesse1980, Vavasis1990, KozlovTarasovKhachiyan1980, CifuentesParrilo2016,
  KolmogorovPockRolinek2016, ChenEtAl2006, LokshtanovMarxSaurabh2018, DellEtAl2014, Korhonen2021,
  Werner2007, WainwrightJaakkolaWillsky2005, Perevozchikov1990, Raphael2001,
  MulmuleyVaziraniVazirani1987, Hasan2018, MeyerFloudas2005, MaranasFloudas1994, AdjimanEtAl1998,
  Bach2019, AxelrodLiuSidford2020, Ishikawa2003, DuKearfott1994, WechsungSchaberBarton2014,
  KannanBarton2017, Neumaier2004, GleixnerEtAl2017, PuranikSahinidis2017, RyooSahinidis1996,
  Rosenberg1972, Tardella2004 (and three without DOI: Munos2011, PengEtAl2011,
  SchlesingerFlach2006). The only differences were cosmetic: accents and the en dash in the
  Contesse, Adjiman and Rosenberg titles, Crossref's "Contesse B." as family name, and article
  numbers 13:1-30 and 21:1-32 in the TALG entries.
* `process/w4/checks/C-literature-arxiv.py`: all 12 arXiv `@misc` entries match the arXiv API
  (title, first author, cited version is the current one where a version is given).
* `process/w4/checks/C-literature-citekeys.py`: every `\cite` key in the included section files is
  in `references.bib`, and every entry is cited. The two missing keys occur only in the unused
  file `appendix-smoothed.tex` (C-literature-11).
* Checked by hand: BienstockMunoz2018 (SIOPT 28(2):1121-1150, with a note on v15 numbering),
  Edmonds1970 (Calgary 1969 proceedings, pp. 69-87, reprint noted), CheungGleixnerSteffy2017
  (LNCS 10328, 148-160), PengEtAl2011 (ICML 2011, 729-736, official title).

## 6. Checks run (targeted, local)

* `python3 process/w4/checks/C-literature-citekeys.py` - cite keys vs bib keys.
* `python3 process/w4/checks/C-literature-crossref.py <keys>` - two runs, 40 entries, 1.5 s
  between queries.
* `python3 process/w4/checks/C-literature-arxiv.py` - one arXiv API query.
* Crossref queries for the BibTeX data proposed above (Meyer 1977, Peyrl-Parrilo, Kaltofen et al.,
  Eifler-Gleixner, Ye, Mehrotra-Ye, Abello et al., Del Pia-Weismantel, Davarnia et al., Marx 2010);
  NeurIPS BibTeX for Bachoc et al.
* Primary-source reading in the local knowledge base: Del Pia-Khajavirad (full text),
  Bienstock-Munoz v15, Dvijotham et al., Grotschel-Lovasz-Schrijver, Hochbaum-Shanthikumar,
  Burer-Natarajan-Willemsen v3, Vavasis 1992, Del Pia 2026, Eiben et al., Bhathena et al.,
  Wechsung et al., Luo-Sturm notes; the Schlesinger-Flach report (downloaded PDF); Math-Net.Ru
  abstract of Perevozchikov.

No project-wide verification was run and no CI was consulted. No paper source file was edited.
