# Claim-level literature comparison

This is a bounded comparison of the manuscript's claims with primary sources
read for this paper. It is not a complete publication search or priority
clearance. A source not found, not retrieved, or not read is not evidence that
a claim is new. The comparison uses the manuscript's stated models and counts:
certificate pieces, tree leaves/nodes, relaxation evaluations, propagation
rounds, and oracle queries are kept separate.

The targeted review processed three discovery rounds. R1 had 58 deduplicated
candidate records: 40 packages were created (30 with open text and 10
metadata-only), 16 were rejected, and 2 matched existing packages. Twenty-nine
of the 30 open R1 packages were read; the remaining package,
`dechter2007-and-or-search-spaces-for`, contains a Mateescu dissertation
rather than the cataloged journal article and is excluded from citation. R2
had 19 candidates: 13 packages were created (11 open and read; 2
metadata-only), and 6 were rejected. The round-2 reader checked all eleven
readable sources and verified display equations against originals where
extraction omitted them. As a lead spot-check, I compared the notes with
page-marked full text for Bachoc (2021), Lin (2017), Kannan–Barton (2018),
and PWE (2015) in R1, and McCoy–Tropp (2014), Wainwright (2009), Basu et al.
(2010), and Skenderi (2021) in R2; the reported claim locators and limits
matched. R3's sole candidate was HJL (1991), already present as a
metadata-only KB package. Publisher/Crossref identity was confirmed, but the
PDF redirected to the abstract and no open copy was found; the abstract's
iteration description is not used as a verified theorem. Thus R3 yielded no
new source the lead would cite, and the targeted search stopped at operational
saturation under this claim scope and cutoff, not at a completeness or
priority conclusion.

Before the BB lead received the shared-KB lock/pause notice, the direct
absolute-path `lit.py check` exited 0 with `KB_CHECK=ok`,
`UNREAD=171`, and `READ_UNCITED=752` across the KB. These are the pre-intake
counts, not the central lead's post-intake final counts. No KB write, ingest,
deduplication, index mutation, or check was run after the lock/pause notice;
the shared reusable lead owns archiving the three round manifests and the
post-intake integrity check.

## Spatial B&B, local clusters, and instance-dependent rates

The inspected cluster literature already establishes that local curvature,
relaxation order, and prefactors control boxes retained near minimizers. Du and
Kearfott's Theorem 1 and Corollary 1 treat interval B&B with midpoint pruning,
a positive-definite Hessian near an unconstrained minimizer, and an interval
extension of order \(\alpha\): for \(\alpha<2\) an unbounded cluster may
occur, at \(\alpha=2\) a bounded cluster larger than one may occur, and for
\(\alpha>2\) the local cluster disappears for sufficiently small boxes except
at a boundary minimizer (printed pp. 6–8; `[[du1994-the-cluster-problem-in-multivariate]]
p.6-8`). Those are bounds on retained local boxes under that algorithm and
model, not the manuscript's general minimum adaptive-tree certificate
characterization. Wechsung, Schaber, and Barton analyze a unique unconstrained
nondegenerate minimum with a centered fixed-width covering construction; their
second-order prefactor condition \(K\leq\lambda_1/8\) yields one covering box,
while their fixed-alpha alphaBB estimate is conservative and does not prove
that the small-prefactor regime always holds (printed pp. 1–5, 8–9;
`[[wechsung2014-the-cluster-problem-revisited]] p.1-5`, `p.8-9`).

Kannan and Barton (2017) extend cluster analysis to constrained optimization.
Definition 8 and Lemmas 1–3 distinguish boxes around optimal feasible points,
infeasible boxes, and objective-dominated infeasible boxes; later bounds depend
on feasible-direction growth and infeasibility growth (printed pp. 5–8,
13–22, 34–41; `[[kannan2017-the-cluster-problem-in-constrained]]
p.5-8`, `p.13-22`, `p.34-41`). This is important prior work on convergence
order, prefactors, and constrained clustering. It does not give the paper's
repeated fixed-incumbent objective-cutoff OBBT contraction or the all-adaptive-
tree covering lower bounds.

Bachoc, Cesari, and Gerchinovitz provide the closest inspected
instance-dependent certification comparison outside spatial B&B. Their
certified DOO rule has query complexity controlled by near-optimal-set packing
numbers (Proposition 1, Theorem 1, pp. 5–10); their lower bound counts black-box
function evaluations under a global Lipschitz oracle and degenerates at the
boundary \(L=\operatorname{Lip}(f)\) (`[[bachoc2021-instance-dependent-bounds-for-zeroth]]
p.5-10`). It is not a lower bound on B&B nodes or work for a relaxation
oracle. Daskalakis, Diakonikolas, and Yannakakis prove a genuine competitive
ratio for the Chord algorithm, but the model is a two-objective Pareto curve,
the benchmark is the minimum size of an \(\epsilon\)-convex Pareto set, and the
resource is weighted-sum oracle calls (pp. 2–3, 11, 21, 32;
`[[daskalakis2016-how-good-is-the-chord]] p.2-3`, `p.11`, `p.21`, `p.32`).
These differences prevent treating it as an existing spatial-B&B node theorem.

Hansen, Jaumard, and Lu (1991) is the identified one-dimensional Piyavskii
global-search predecessor. Its primary full text was not recovered in this
review. Bachoc et al. describe the earlier one-dimensional certificate
integral in their introduction (pp. 2–3), but that secondary account does not
verify HJL's detailed iteration theorem or node/ query convention. The paper
therefore does not claim or cite a directly verified HJL theorem. The 2018
Kannan–Barton convergence-order article was read for context, but no key or
page-specific theorem claim is used: the only located copy is the typeset
version of record. The separate 2017 constrained-cluster article is the cited
and fully inspected comparison.

## McCormick faces, alphaBB, propagation, and branching

McCormick's factorable convex/concave estimators and consistency under
subdivision are foundational relaxation inputs (1976, pp. 1, 25–27;
`[[mccormick1976-computability-of-global-solutions-to]] p.1`, `p.25-27`).
Rikun gives exact multilinear envelope formulas and face structure (1997,
pp. 1, 8–10; `[[rikun1997-a-convex-envelope-formula-for]] p.1`, `p.8-10`).
Adjiman, Dallwig, Floudas, and Neumaier establish the alphaBB separable
quadratic shift; their Theorem 2.1 requires \(H_f(x)+2\operatorname{diag}(\alpha)\)
to be positive semidefinite throughout the box (Part I, pp. 1–9;
`[[adjiman1998-a-global-optimization-method-bb]] p.1-9`). These are the
named-relaxation antecedents. They do not state the paper's exact
face-characterization or resulting adaptive node-count theorem. The
manuscript's novelty is limited to its stated face hypotheses and proved
counting results; the source audit makes no global priority claim.

Schichl, Markót, and Neumaier give a local fixed-scale cluster estimate for
interval overestimation and validated exclusion regions around Karush–John
points (Theorem 5 and Corollary 4; printed pp. 5–6, 14–18;
`[[schichl2014-exclusion-regions-for-optimization-problems]] p.5-6`,
`p.14-18`). Their exclusion region identifies critical points and does not
itself enforce an objective cutoff or yield an end-to-end tree bound. Belotti,
Cafieri, Lee, and Liberti formulate FBBT as a monotone deflationary interval
operator whose limit is the greatest fixed point; Theorem 4.1 treats its
linear-relaxation limit, and examples show that convergence may be
non-finite (pp. 7–16; `[[belotti2012-on-feasibility-based-bounds-tightening]]
p.7-16`). This is a propagation/fixed-point antecedent, not the manuscript's
cutoff-dependent expression-graph node characterization or cost transfer to
propagation rounds.

The manuscript's branching comparison is also narrower than an unrestricted
priority statement. Its one-dimensional minimizer rule is proved for the
paper's quadratic-gap model and information class. The closest inspected
competitive source, the Chord algorithm, has a different oracle, objective,
and count as described above. The HJL primary comparison remains unavailable.
Practical minimizer/incumbent-point branching and safe clamp comparisons in
the project notes are not used to claim a universal competitive guarantee.

## RLCT and analytic sublevel asymptotics

Lin (2017) supplies analytic asymptotic tools, not B&B results. Corollary 2.6,
Lemma 2.4, and Theorem 2.10 treat analytic integrands on compact semianalytic
domains and include boundary contributions (arXiv version, pp. 7–11;
`[[lin2017-ideal-theoretic-strategies-for-asymptotic]] p.7-11`). The facewise
application must be made on the closed root box or face in its affine hull:
the restricted analytic gap need only be nonnegative on that domain. A
linear boundary gap such as \(m=x\) on \([0,1]\) changes sign outside the box,
so an open-neighborhood nonnegativity assumption would be unjustified. Lin's
Example 2.8 (p. 9) also shows that boundary-domain choices can change the
learning coefficient. The manuscript's ordinary RLCT pair applies to a
nonzero restriction with a zero; a face on which the gap is identically zero
uses the manuscript's separate covering-scaling convention, not an ordinary
RLCT pole pair. The analytic exponent itself is classical; the paper applies
it to its node-count characterization and does not claim the RLCT machinery as
new.

Prior cluster work covers special local growth mechanisms. In particular,
Kannan–Barton (2017, Lemma 10 and Corollary 4, pp. 34–41) give fixed-width
upper estimates for linear growth along a constrained feasible direction.
The paper's RLCT transfer concerns adaptive-tree lower and upper counts,
degenerate/non-isolated optimal sets, and facewise analytic exponents under
its stated hypotheses. This comparison is bounded to the read sources; the
search failure reported in the earlier RLCT note is not used as novelty
evidence.

## Sparse regression and the PWE theorem audit

Pilanci, Wainwright, and El Ghaoui (2015) provide a Boolean formulation,
necessary-and-sufficient interval-relaxation certificate (Corollary 2), and a
random-design claim (Theorem 2). The printed theorem uses iid design entries
\(X_{ij}\sim N(0,1)\), iid *per-entry* noise \(N(0,\gamma^2)\), ridge
\(\rho=\sqrt n\), and asserts exactness with probability at least
\(1-2e^{-c_1n}\) under
\(n>c_0(\gamma^2+\|w^*_S\|^2)\log(d)/w_{\min}^2\) (journal pp. 71–72;
KB extraction pp. 9–10; Appendix 7.1, printed p. 81 onward, KB pp. 19–21;
`[[pilanci2015-sparse-learning-via-boolean-relaxations]] p.9-10`, `p.19-21`).
The independent correction audit checks the source's Corollary 2 KKT threshold
and gives a fixed-\((d,k)\) counterexample under this exact printed
per-entry-noise model: the planted support is optimal with probability
tending to one, but the interval-relaxation exactness probability tends to
\([1-2\bar\Phi(w_{\min}/\gamma)]^{d-k}<1\) (recorded with full derivation
in `REVIEW-PWE-R1.md`, especially its normalization table and finite-
dimension construction). That contradicts Theorem 2's probability claim
under the source's stated assumptions. The audit does not supply a repaired
high-dimensional theorem and does not transfer the contradiction to a
shrinking total-noise model \(N(0,\gamma^2 I/n)\). The paper states this as a
precise contradiction under the printed assumptions; it does not call the
published theorem valid or assert unsupported corrected constants.

Other inspected sparse-regression sources establish distinct comparisons.
Xie and Deng (2018, Theorems 1–3, pp. 8–15) prove formulation equivalence
and strength statements for sparse ridge models, not a random phase transition
(`[[xie2018-scalable-algorithms-for-the-sparse]] p.8-15`). Dong, Chen, and
Linderoth (2015, Theorems 1 and 3 and the SDP discussion, pp. 6–13) analyze
perspective/SDP strength and exactness, not B&B complexity or a planted
Gaussian threshold (`[[dong2015-regularization-vs-relaxation-a-conic]]
p.6-13`). Atamtürk and Gómez (2019, Proposition 1 and its rank-one case,
pp. 10–12; Proposition 2 and Theorem 2, pp. 13–14) give rank-one quadratic
convexification and its exact-hull special case. Their 2020 paper, Proposition
2 (p. 3) and Section 3.1 (p. 4), gives safe indicator-screening rules for
cardinality-constrained ℓ₀ regression using a perspective-relaxation solution
and an incumbent upper bound; it also describes dynamic use within B&B. These
are formulation and screening results, not a random-design phase transition
or an asymptotic node-count rate, and neither is the 2015 PWE paper
(`[[atamturk2019-rank-one-convexification-for-sparse]] p.10-14`,
`[[atamturk2020-safe-screening-rules-for-l0]] p.3-4`). Wainwright
(2009, Theorem 1 and uniform-Gaussian case, pp. 8–9) proves the Lasso's
support-recovery threshold under covariance incoherence, tuning, and minimum-
signal assumptions; its constant-2 scale is not an information-theoretic
optimal-decoder result and is not a B&B certificate threshold
(`[[wainwright2009-sharp-thresholds-for-high-dimensional]] p.8-9`).

## Binary least squares, MIMO, and cone geometry

Hansen, Hassibi, Dimakis, and Xu (2009) use the square real model
\(y=\sqrt{\mathrm{SNR}/N}Hs+v\), iid standard-normal \(H\) and \(v\), and
\(s\in\{-1,1\}^N\). Lemma IV.2 states vanishing ML error for
\(\mathrm{SNR}>2\ln N\), but the accompanying proof is explicitly only a
sketch (pp. 2, 5). Hassibi et al. (2014, Lemma IV.2) state the sufficient
condition \(\mathrm{SNR}>2\ln N+f(N)\) for any \(f(N)\to\infty\) in the same
square-real model (pp. 3, 5); their separate MCMC analysis leaves polynomial
mixing in dimension open (pp. 1–2, 7). Neither source proves a tall-system
extension or the paper's all-node certificate event. Keep these distinct from
Hu and Lu (2020): their box-constrained least-squares decoder is sign-rounded
under \(A_{ij}\sim N(0,1/p)\), sampling ratio \(\delta\), and noise variance
\(\sigma_p^2\). Proposition 1 uses
\(\alpha_p=(\delta_p-1/2)/(2\sigma_p^2\log p)\) and gives perfect recovery
when \(\alpha_p\to\alpha_*>1\), under assumptions A.1–A.5 (printed pp. 3–5;
`[[hu2020-the-limiting-poisson-law-of]] p.3-5`).

For the square single-wrong-fixing comparison, set \(p=N-1\), \(M=N\),
\(\delta_N=N/(N-1)\), and \(\beta_N=(N+1)/(N-1)=2\delta_N-1\). With
\(\rho_0=(1+\varepsilon)4\log N/(2\beta_N-1)\) and
\(\sigma_N^2=1/\rho_0\), Hu–Lu's parameter is
\(\alpha_N=(1+\varepsilon)(N+1)/(N+3)\to1+\varepsilon\). Also
\(\sigma_N^2\log^2N\to\infty\), \(\sigma_N^2\) is bounded, and the sampling
ratio tends to one, so the cited assumptions apply to this one-decoder
comparison. This supports the box-decoder recovery input for that sequence;
it does not provide a union bound across B&B nodes. The manuscript's new
all-node C1 result uses its self-contained sign-orbit coefficient-tail proof,
so there is no remaining Hu–Lu dependency for that step.

The Gaussian-cone antecedents are standard but narrower than the application.
McCoy and Tropp's Theorem 3.1 and Corollary 3.2 give the fixed-cone master
Steiner formula and chi-square mixture (pp. 4–5;
`[[mccoy2014-from-steiner-formulas-for-cones]] p.4-5`). Hug and Schneider's
Corollary 4.3 gives expected intrinsic-volume weights for Cover–Efron cones
under its general-position hypothesis (pp. 8, 10, 13;
`[[hug2016-random-conical-tessellations]] p.8`, `p.10`, `p.13`). Together
with the relevant parity identity these explain the aggregate binomial
face-dimension law for Gaussian generators. They do not state the manuscript's
fixed-vector labelled-face sign-orbit tail, simultaneous upper-box inactivity,
or B&B all-node certificate threshold. The paper limits its application-level
contribution to those finite sign-orbit/all-node steps; it does not claim the
classical conic projection law as new.

## Integer class number and structural comparisons

Dey, Dubey, and Molinaro (2023) give a strong general-split B&B lower-bound
mechanism. Their cross-polytope Proposition 3 and the set-covering argument
in Section 6 (printed pp. 14, 17–18) use pairwise midpoint conflict and
leaf-capacity bounds in an abstract integer-split tree
(`[[dey2023-lower-bounds-on-the-size]] p.14`, `p.17-18`). The manuscript
credits and reuses that mechanism. Its semantic class number counts arbitrary
admissible convex-hull classes in the specified projected relaxation model
and identifies the minimum leaf count for the stated semantic-tree class;
that is the claim being made, not a blanket new version of the Dey lower
bound. Kaibel and Weltge's hiding sets prove exponential *formulation*
complexity for integer programs without auxiliary variables (Section 4,
Definition 1 and Proposition 7, p. 9); this is not itself a B&B tree-size
result (`[[kaibel2015-lower-bounds-on-the-sizes]] p.9`).

The full-dimensional maximal lattice-free polyhedron input is sourced to
Basu, Conforti, Cornuéjols, and Zambelli (2010), Theorem 2, which gives a
cylinder \(P+L\) with at most \(2^{\dim P}\) facets and a lattice point in
the relative interior of each facet (author version p. 2; proof pp. 8–9;
`[[basu2010-maximal-lattice-free-convex-sets]] p.2`, `p.8-9`). The
full-dimensional/rational-affine-space hypotheses matter; the general
classification also contains an irrational-hyperplane case. The manuscript
uses the full-dimensional \(2^n\) case only. It does not cite Doignon's
unretrieved 1973 primary text separately.

The normalized lattice expectation is verified from Skenderi's 2021
dissertation, Theorem 3.2 and Remark 3.3 (pp. 10–11 in the dissertation's
pagination; KB source locators pp. 12, 17). For Haar probability on
\(\mathrm{SL}_n(\mathbb R)/\mathrm{SL}_n(\mathbb Z)\), \(n\ge2\), and
nonnegative Borel \(f\in L^1(\mathbb R^n)\), the mean of
\(\sum_{v\in\Lambda\setminus\{0\}}f(v)\) is exactly \(\int f\), with no
zeta factor; primitive vectors have the separate factor \(1/\zeta(n)\).
The original Siegel 1945 paper was not retrieved. This theorem is an explicit
external input, not a proof contribution of the manuscript
(`[[skenderi2021-some-results-concerning-random-lattices]] p.12`, `p.17`).
The paper's quadratic parity example and variable-branching count are proved
in full in the manuscript; per the authors' direction, it is self-contained
and no priority attribution to Jeroslow is made.

For decomposition, Marinescu and Dechter's finite-domain AND/OR B&B has
tree-size bounds in terms of pseudo-tree depth/treewidth (pp. 2–3, 12,
16–18); de Givry, Schiex, and Verfaillie give separator-conditioned BTD+
weighted-CSP bounds (pp. 2–4). Bienstock and Muñoz give approximate LP
formulations for bounded-treewidth polynomial optimization, with explicit
accuracy, degree, and structural-parameter dependence (pp. 1–5, 10–17,
24–25). These are relevant structural precedents but have discrete
finite-domain or approximate-formulation resources, not the manuscript's
fixed continuous node oracle and spatial node count. Langiu et al.'s MUSE-BB
is a closer nonconvex two-stage spatial-decomposition algorithm: it proves
finite \(\epsilon\)-termination for its lower-bounding scheme but gives no
worst-case node-count rate (pp. 5–6, 23–26;
`[[langiu2025-muse-bb-a-decomposition-algorithm]] p.5-6`, `p.23-26`).
These comparisons limit the manuscript's claim to its specified path-
decomposition certificate bound, not decomposition as a general idea.

## Gaussian concentration inputs

The regression tail inequalities are named standard inputs. Laurent and
Massart's Lemma 1, equations (4.3)–(4.4), gives weighted centered
chi-square tails for \(x>0\); the chi-square specialization is checked in
the source (printed pp. 1324–1325; KB locators pp. 24–25;
`[[laurent2000-adaptive-estimation-of-a-quadratic]] p.24-25`). Davidson and
Szarek's Theorem II.13 gives Gaussian singular-value edges in the chapter's
\(N(0,1/d)\) normalization; item 5 of their 2003 corrigendum restores the
missing \(\sqrt d\) scale in the Gaussian tail (2001 printed p. 353; 2003
printed p. 1819; KB locators `[[davidson2001-local-operator-theory-random-matrices]]
p.35`, `p.42`, `[[davidson2003-addenda-and-corrigenda-to-chapter]] p.1`).
Rescaling by \(\sqrt d\) yields the standard-normal matrix inequalities used
in the manuscript. Gordon (1985) is a metadata-only historical source and is
not used as a theorem citation.

## Scope and excluded sources

The final paper makes no universal “first” claim. It states the results under
their proved operation, relaxation, probability, and tree hypotheses, and
credits the mechanism where it overlaps prior work. The inspected sources
support the comparisons above; they do not establish that no other source
states a similar result.

The following identified in-scope primary sources remain unavailable,
unresolved, or unverified at the source-text level. They are not used to
support manuscript theorem details. DOIs link to lawful bibliographic landing
pages; where an author/publisher full-text URL was tried, the reason is given.

1. Hansen, Jaumard, and Lu (1991), “On the Number of Iterations of Piyavskii's
   Global Optimization Algorithm,” DOI [10.1287/moor.16.2.334](https://doi.org/10.1287/moor.16.2.334).
   No lawful open source was located; the DOI page is subscription access.
   The one-dimensional predecessor is identified through Bachoc et al., but
   its primary theorem was not independently checked.
2. Schöbel and Scholz (2010), “The Theoretical and Empirical Rate of
   Convergence for Geometric Branch-and-Bound Methods,” DOI
   [10.1007/s10898-009-9502-3](https://doi.org/10.1007/s10898-009-9502-3).
   Springer returned an HTML body to the PDF request. No theorem locator is
   used in the paper.
3. Ravutla et al. (2026), “Data-Driven Lipschitz-Informed Convex
   Underestimators for Branch-and-Bound Optimization of Black-Box Functions,”
   DOI [10.1007/s10898-025-01572-8](https://doi.org/10.1007/s10898-025-01572-8).
   The attempted Springer PDF yielded HTML; no theorem claim is used.
4. Khayyal and Kyparisis (1983), “Jointly Constrained Biconvex Programming,”
   DOI [10.1287/moor.8.2.273](https://doi.org/10.1287/moor.8.2.273).
   No lawful full-text copy was located; it is not a source for a manuscript
   claim.
5. Shectman and Sahinidis (1998), “A Finite Algorithm for Global Minimization
   of Separable Concave Programs,” DOI
   [10.1023/A:1008241411395](https://doi.org/10.1023/A:1008241411395).
   No lawful full text was located; the paper does not rely on this source for
   an incumbent-branching theorem.
6. Watanabe (2001), “Algebraic Analysis for Nonidentifiable Learning
   Machines,” DOI
   [10.1162/089976601300014402](https://doi.org/10.1162/089976601300014402).
   No lawful open copy was located. Lin (2017) supplies the analytic input
   actually used.
7. Aoyagi (2005), “Stochastic Complexities of Reduced Rank Regression in
   Bayesian Estimation,” DOI
   [10.1016/j.neunet.2005.03.014](https://doi.org/10.1016/j.neunet.2005.03.014).
   No lawful full text was located; no numerical learning coefficient from
   this source is used in the final manuscript.
8. Siegel (1945), “A Mean Value Theorem in the Geometry of Numbers,” DOI
   [10.2307/1969027](https://doi.org/10.2307/1969027). The primary original
   was not found in open access. The exact needed normalization is cited to
   Skenderi (2021), Theorem 3.2 and Remark 3.3.
9. Jeroslow (1974), “Trivial Integer Programs Unsolvable by Branch-and-Bound,”
   DOI [10.1007/BF01580225](https://doi.org/10.1007/BF01580225). No lawful
   full text was located. The manuscript's parity example is self-contained,
   carries no priority claim, and has no Jeroslow bibliography entry.
10. Jaldén and Ottersten (2005), “On the Complexity of Sphere Decoding in
    Digital Communications,” DOI
    [10.1109/TSP.2005.843746](https://doi.org/10.1109/TSP.2005.843746).
    No lawful primary copy was located; sphere-decoding asymptotics are not
    used as a comparison theorem in the final paper.
11. Gläser and Pfetsch (2024), “On Computing Small Variable Disjunction
    Branch-and-Bound Trees,” DOI
    [10.1007/s10107-023-01968-y](https://doi.org/10.1007/s10107-023-01968-y).
    Springer returned HTML to the PDF request. This is not the different
    hard general-split preprint excluded by the lattice author, and neither
    work is cited for the final class-number claim.
12. Gordon (1985), “Some Inequalities for Gaussian Processes and
    Applications,” DOI
    [10.1007/BF02759761](https://doi.org/10.1007/BF02759761). No open full
    text was located. The exact singular-value bound is supported by
    Davidson–Szarek and its corrigendum.
13. Doignon (1973), “Convexity in Crystallographical Lattices,” DOI
    [10.1007/BF01949705](https://doi.org/10.1007/BF01949705). Springer marks
    the original subscription-only and no lawful open copy was found. Basu et
    al. state the needed lattice-free facet theorem; no independent Doignon
    locator is used.
14. Dechter and Mateescu (2007), “AND/OR Search Spaces for Graphical Models,”
    DOI [10.1016/j.artint.2006.11.003](https://doi.org/10.1016/j.artint.2006.11.003).
    The KB's accessible PDF is a 283-page Mateescu dissertation, not the
    cataloged journal article. The final paper cites the separately read
    Marinescu–Dechter article and does not use this package's theorem
    pagination.

This list reports source-content gaps found in the paper's targeted review;
it is not a complete survey of all related literature. An additional
readable, post-cutoff comparison, Papailiopoulos (2026), is not used as
pre-cutoff prior work: version 1 was posted 16 September 2026, after the
recorded 10 September literature cutoff.
