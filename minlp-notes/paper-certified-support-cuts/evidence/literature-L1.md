# Literature lane L1: joint convexification, composite and multi-term relaxations, original-variable relaxations

Lane date: 2026-10-03. Claims served: C-SUP, C-AGG (novelty candidate N3),
C-POLY, and general positioning. Findings relevant to other candidates
(N2, N4, N6) are reported where this lane's sources bear on them.

## 1. Main conclusions

1. **C-SUP is classical in its mathematics.** The support-function
   description of the hull of a vector graph, and cut separation through
   linear combinations, are due to Ballerstein (2013, as attributed by
   Liers et al. 2021 and Mertens 2019) and are developed by Tawarmalani
   (2010), Liers et al. (2021), He and Tawarmalani (2021, 2022, 2024), and
   Zhu, He and Tawarmalani (2026). Do not present Prop. support as new.
   Prop. round's principle also has a direct precedent. Neumaier and
   Shcherbina (2004, §7, p. 294) state that cut-selection calculations
   "need not be safeguarded since the bounds are valid for the s actually
   used, independent of its construction". Liers et al. (2021, p. 25)
   mention "safe rounding of coefficients" without details. No source in
   this lane combines a joint support cut for a vector of functions with a
   whole-domain certificate for the exact exported binary64 coefficients.
2. **N3 (the closure theorem for C-AGG) is anticipated in substance.**
   It is the projection form of a known result: the Lagrangian dual of a
   nonconvex program equals a "convexified" program. In that program the
   graph of (variables, objective, constraints) is convexified and the
   dualized constraints are then imposed on the hull, that is, in
   expectation. Sources:
   - Lemaréchal and Renaud (2001), abstract-level;
   - Feltenmark and Kiwiel (2000), abstract;
   - Nowak (2005), Lemmas 3.3 and 3.5 and relaxation (3.14), read in full
     text;
   - Falk (1969), metadata level;
   - Geoffrion (1974), the integer-programming form "dual = optimization
     over conv(X) ∩ {dualized rows}".

   The x²=1/4 example is an instance of the classical Lagrangian duality
   gap: convexifying and then intersecting is weaker than intersecting and
   then convexifying. What remains defensible is narrow:
   - the set-level statement for the specific "direct rows with affine
     remainders" interface, including equality features;
   - a short self-contained proof that needs no constraint qualification
     on a compact domain;
   - explicit use as the closure of a cut family in original variables.

   The paper must cite this duality literature. Reports A and B currently
   cite only Boyd and Vandenberghe for this inference.
3. **The original-variable interface of C-AGG has many precedents.** These
   include:
   - Lagrangian cuts in original block variables (Nowak 2005, §7.1.3–7.1.4,
     p. 93);
   - Lagrangean cuts from decomposed subproblems (Karuppiah and Grossmann
     2008);
   - Lagrangian/duality range reduction and cuts in BARON (Tawarmalani and
     Sahinidis 2004, §4, p. 15–17);
   - surrogate aggregation of nonlinear rows in SCIP (Müller et al. 2022);
   - Lagrangian variable bounds (Gleixner et al. 2017);
   - EC&R aggregation hulls (Davarnia, Richard and Tawarmalani 2017);
   - aggregation hulls for quadratics (Dey, Muñoz and Serrano 2022;
     Blekherman, Dey and Sun 2024; Xu and Pokutta 2026);
   - reduced-space McCormick relaxations (Tsoukalas and Mitsos 2014;
     Bongartz and Mitsos 2017; Najman, Bongartz and Mitsos 2021).

   A referee will also point to Tawarmalani and Sahinidis (2005, Thm. 1,
   p. 227). It shows that, with the same linearization points, outer
   approximation of a lifted (decomposed) formulation is tighter than
   direct outer approximation in original variables. Eliminating auxiliary
   variables therefore needs a justification beyond strength.
4. **Using constraints to restrict the support domain is a known remedy.**
   Report B's remark (put x²=1/4 inside the support domain) and Report A's
   polygon example (convexify the row-constrained domain) have direct
   precedents:
   - Zhu, He and Tawarmalani (2026): factorable programming ignores linking
     constraints (p. 2); Theorem 8 (p. 23) gives convergence to conv of the
     graph over a domain defined by g(x) ≤ 0;
   - Wu, Muts, Nowak and Hendrix (2025): Proposition 1 (p. 419) shows that
     aggregating blocks across a coupling constraint never weakens and can
     strictly tighten the convex-hull relaxation;
   - Nowak (2005, (3.12)–(3.13)): block convex hulls include the block's
     nonlinear constraints;
   - Rikun (1997, p. 435 footnote): x₁x₂ on {0 ≤ x₁ ≤ x₂ ≤ 1} already has
     a non-polyhedral envelope;
   - Locatelli and Schoen (2014); Anstreicher and Burer (2010, Thm. 7).

   Report A's explicit numeric example remains a useful illustration, not
   a new principle.
5. **For N2 this lane found qualitative precedent, not the paper's
   witness.** Tawarmalani (2010) Example 3.8 (p. 14–15) shows that
   envelopes built from different convex-combination representations are
   weaker than the simultaneous hull. Corollary 3.10 (p. 16) glues two
   functions sharing a variable u when their envelope certificates have
   equal marginal distributions of u on all sets A ⊆ U. This is a
   full-marginal gluing result for envelopes, separate from Lasserre's
   (2006) sparse-moment gluing and stated directly for MINLP hulls. Liers et al. (2021, p. 29) note that decomposing a high-degree
   junction gives only a relaxation of the simultaneous hull. He and
   Tawarmalani (2024, §7.2) note that intersecting individual hulls fails
   in general. This lane found no source with the paper's
   matched-first-and-second-moment witness (gap 1/128) or its
   δ²/2 family.

## 2. Method and read scope

- **Local KB.** I searched `literature/index.md` and
  `papers/*/fulltext.md` (grep for Tawarmalani, Ballerstein,
  simultaneous convexification, Lagrangian, aggregation, McCormick,
  multilinear, reduced space, and related terms). I read the cited
  passages in the KB `fulltext.md` files; page locators `p.N` refer to
  KB page markers.
- **Local read-only copies.** He and Tawarmalani 2021 and 2022 PDFs from
  `research-20261002-convexification/literature/sources/` were extracted
  to `/tmp` with `pdftotext -layout`. Nothing in the research folders was
  modified.
- **Open web copies, downloaded to `/tmp` only:**
  - Nowak's habilitation (HU Berlin edoc; the basis of the 2005
    Birkhäuser book);
  - Mertens' dissertation (TU Dortmund Eldorado);
  - Kerdreux, Colin and d'Aspremont (arXiv:1712.08559v3);
  - a 2012 TU Dortmund colloquium notice for D. Michaels.
- **Metadata.** Crossref API records for DOIs. Abstracts came from
  Crossref, publisher or arXiv pages, or search snippets, as marked per
  entry.
- **Not accessed.**
  - The Ballerstein thesis: ETH Research Collection returned an
    "Access Restricted (scraping)" page; I did not try to bypass it.
  - The full texts of Lemaréchal and Renaud 2001, Falk 1969, Geoffrion
    1974, Feltenmark and Kiwiel 2000, Karuppiah and Grossmann 2008,
    Bao et al. 2015, Misener and Floudas 2012 and 2014, Smith and
    Pantelides 1999, Bongartz and Mitsos 2017, Najman et al. 2021,
    Khajavirad and Sahinidis 2012, and Crama 1993.

  Statements about these are marked abstract-level or secondary.
- No theorem number is given unless I saw it in the text I read, or I
  mark it as reported by a named secondary source.

## 3. Works by topic

Each entry gives the full citation, the read scope, what the work
establishes, and how it relates to our claims.

### 3.1 Simultaneous convexification of vectors of functions

**[Tawarmalani2010]** M. Tawarmalani. *Inclusion certificates and
simultaneous convexification of functions.* Optimization Online
manuscript 2722, September 5, 2010.
https://optimization-online.org/wp-content/uploads/2010/09/2722.pdf.
KB `tawarmalani2010-inclusion-certificates-and-simultaneous-convexification`.

- *Read scope:* full text, pp. 1–6 and 12–17.
- *Establishes:*
  - p.1: the example 2z₁+z₂ ≤ 3x for {z₁ ≤ x/y, z₂ ≤ xy, (x,y) ∈ [1,2]²},
    which individual envelopes do not imply.
  - p.2: the "convex extensions" literature finds "inequalities in the
    original variables that separate the convex hull" by convex
    optimization.
  - Thm 2.1, p.3: a domain point can be excluded when a convex combination
    over other points dominates it.
  - Cor 2.6, p.5: identical support functions give identical closed
    convex hulls.
  - Cor 2.7, p.5: a vector of multilinear functions over a product of
    compact convex sets is convexified from extreme points.
  - Def 3.4, p.12: inclusion certificate.
  - Thm 3.6, p.13: composition through independent certificates.
  - Example 3.8, p.14–15: x/y and xy convexified separately versus
    simultaneously; explicit gap ½(x^U−x^L)(y^U−y^L).
  - Cor 3.9, p.15: a common certificate realizing every individual
    envelope gives the simultaneous hull.
  - Cor 3.10, p.16: gluing h₁(u,v) and h₂(u,w) when the u-marginals of
    their certificates agree on every set A ⊆ U.
  - Remark 3.11, p.16.
- *Relation:* Core prior art for C-SUP. Cor 3.10 and Example 3.8 bear
  directly on N2. Its "inclusion certificate" is a measure, not a
  numerical validity certificate; the paper must distinguish the two
  terms.

**[Ballerstein2013]** M. Ballerstein. *Convex Relaxations for
Mixed-Integer Nonlinear Programs.* Doctoral thesis, ETH Zürich,
Diss. ETH No. 21024, 2013. DOI 10.3929/ethz-a-009959194. Also printed by
Cuvillier Verlag, Göttingen. KB `ballerstein2013-…` (not retrieved).

- *Read scope:* not accessed (ETH access restriction). Secondary sources:
  Liers et al. 2021, Prop. 1, p.6, and Mertens 2019, Prop. 3.13, p.28,
  which cites "[Ballerstein, 2013, Cor. 5.25]".
- *Establishes (secondary):* for compact convex D and continuous
  g: D→ℝ^m, conv graph(g) equals the intersection over α of
  {(x,z): αᵀz ≥ vex_D[αᵀg](x)}. Mertens (p.18) adds that Ballerstein
  applies this to multiple univariate convex functions and identifies
  combinations that are not required.
- *Relation:* The origin of C-SUP's Prop. support for vector graphs.
  C-SUP does not require convex D, but that is a trivial extension.

**[Mertens2019]** N. Mertens. *Relaxation Refinement for Mixed-Integer
Nonlinear Programs with Applications in Engineering.* Dissertation,
Fakultät für Mathematik, TU Dortmund, 2019 (defense 15.11.2019).
https://eldorado.tu-dortmund.de/bitstream/2003/38410/1/Dissertation_Mertens.pdf.

- *Read scope:* full-text passages, printed pp.18, 25–28.
- *Establishes:*
  - Example 3.10, pp.25–27: on x ∈ [0,1]³ with x₂ = x₁², x₃ = x₁³,
    individual convexification is weaker than the hull.
  - Prop. 3.13, p.28: Ballerstein's characterization.
- *Relation:* Secondary attribution for Ballerstein. It is the
  dissertation version of Liers et al. 2021.

**[LiersEtAl2021]** F. Liers, A. Martin, M. Merkert, N. Mertens,
D. Michaels. *Solving mixed-integer nonlinear optimization problems using
simultaneous convexification: a case study for gas networks.* Journal of
Global Optimization 80(2):307–340, 2021. DOI 10.1007/s10898-020-00974-0.
KB `liers2021-solving-mixed-integer-nonlinear-optimization`; author
revision dated Sept. 16, 2020.

- *Read scope:* full text, pp.1–9, 25, 29–30, 36.
- *Establishes:*
  - Prop. 1, p.6: Ballerstein's characterization.
  - Separation problem (SP), pp.6–7: over the unit ball of multipliers
    α, convex but nonsmooth (Prop. 2); a negative value suffices to
    separate.
  - Prop. 3, p.8: cut construction from a supporting hyperplane of
    vex_D[αᵀg].
  - Application: envelopes of linear combinations of bivariate quadratic
    absolute-value functions.
  - p.25: a subgradient method with "safe rounding of coefficients"; the
    appendix pseudocode on p.36 has a "Numeric rounding" step. Cuts are
    precomputed and added to BARON.
  - p.29: decomposing degree d>3 junctions yields only a relaxation.
  - p.30: envelopes of arbitrary combinations are "very difficult",
    calling for consistent approximations.
- *Relation:* Direct precedent for C-SUP's separation logic. Our
  difference: we need only a certified lower bound on the support for one
  final direction, not the envelope vex_D[αᵀg]. This answers the need
  stated on p.30, but only for the supported grammar. Their "safe
  rounding" is unspecified, so our exact final-row certificate is a
  stronger and specified contract.

**[HeTawarmalani2021]** T. He, M. Tawarmalani. *A new framework to relax
composite functions in nonlinear programs.* Mathematical Programming
190(1–2):427–466, 2021 (online July 13, 2020).
DOI 10.1007/s10107-020-01541-x.

- *Read scope:* full text (local publisher PDF), abstract and §5,
  printed pp.457–458.
- *Establishes:* §5 treats a vector of outer functions θ over polytope P.
  Lemma 7 gives conv(Θ^P) as a projection. Theorem 6 (p.458): separation
  for conv(Θ^P) is polynomial given a polynomial separation oracle for
  conv(Θ^Q). §5.2 covers facet generation.
- *Relation:* Vector/simultaneous composite convexification precedes
  C-SUP. The oracle is an input there; we supply concrete certified
  support bounds for specific classes.

**[HeTawarmalani2022]** T. He, M. Tawarmalani. *Tractable relaxations of
composite functions.* Mathematics of Operations Research
47(2):1110–1140, 2022. DOI 10.1287/moor.2021.1162. Author manuscript:
https://par.nsf.gov/servlets/purl/10382117.

- *Read scope:* full text (local author manuscript), §3.3, pp.20–21.
- *Establishes:* Theorem 4: if the concave envelopes of θ_k over Q share
  a triangulation, the simultaneous hypograph hull equals the
  intersection of the individual hulls. Corollary 7: this holds for
  concave-extendable supermodular θ_k, with facet generation in
  O(κ d n log d).
- *Relation:* A structural condition under which joint support adds
  nothing over individual hulls. The paper should state that its joint
  cuts help only outside such classes.

**[HeTawarmalani2024]** T. He, M. Tawarmalani. *MIP relaxations in
factorable programming.* SIAM Journal on Optimization 34(3):2856–2882,
2024. DOI 10.1137/22M1515537; arXiv:2310.07168. KB
`he2024-mip-relaxations-in-factorable-programming`.

- *Read scope:* full text of the KB arXiv copy. Its numbering is §7.2,
  Prop. 7.4, Cor. 7.5, Remark 4.3. Report A's audit cites arXiv v3 as
  Prop. 28, Cor. 29, Remark 11.
- *Establishes:*
  - Remark 4.3, p.9: MICP relaxation for the graph of a vector of
    composite functions.
  - §7.2, pp.21–22: vectors of composite functions; "individually
    convexifying the hypograph of θ_k∘F does not yield the simultaneous
    convex hull"; the supermodular exception.
  - Cor. 7.5: vector multilinear outer functions.
- *Relation:* Positioning for C-SUP and N2. Cite with version-specific
  numbering.

**[ZhuHeTawarmalani2026]** H. Zhu, T. He, M. Tawarmalani.
*Axis-aligned relaxations for mixed-integer nonlinear programming.*
arXiv:2603.18458v1, March 19, 2026. KB
`zhu2026-axis-aligned-relaxations-for-mixed`.

- *Read scope:* full text, pp.2–6, 20–25; summary of §5.2.
- *Establishes:*
  - p.2: factorable programming "ignores interdependencies among
    variables induced by linking constraints".
  - Definition 7 and Theorem 7, p.20: the simultaneous hull of several
    multilinear functions over a bounded axis-aligned region is the hull
    of corner evaluations.
  - Algorithm 3 and Lemma 3, p.22: outer approximation of
    {g(x) ≤ 0} ∩ box, converging in Hausdorff distance.
  - Theorem 8, p.23: under Lipschitz assumptions, the polyhedral
    relaxations converge to conv(G) for a graph over a constrained
    domain.
  - Prop. 9, p.24: cardinality bound.
  - §5.2: root-bound study on 619 MINLPLib instances.
- *Relation:* Strongest recent precedent for C-POLY's
  "row-constrained domain" message and for convergent joint hulls. It
  uses floating-point QuickHull with no final-row certification, so it
  does not anticipate N4.

**[HeLiuTawarmalani2023]** T. He, S. Liu, M. Tawarmalani.
*Convexification techniques for fractional programs.* arXiv:2310.08424,
2023. KB `he2024-convexification-techniques-for-fractional-programs`.

- *Read scope:* full text, §5.1, pp.18–19.
- *Establishes:* Corollary 5 and Proposition 4: exact simultaneous hulls
  of {x^p, x^{-q}} and of {1/(x−r_i)} via the moment hull (SDP),
  "to simultaneously relax fractions and powers instead of … separately".
- *Relation:* Exact joint hulls for vectors of univariate functions in
  C-SUP's grammar (powers, reciprocals). C-SUP's cutting-plane route
  differs (Bernstein/ball bounds, single directions), but the hull theory
  exists.

**[DavarniaRichardTawarmalani2017]** D. Davarnia, J.-P. P. Richard,
M. Tawarmalani. *Simultaneous convexification of bilinear functions over
polytopes with application to network interdiction.* SIAM Journal on
Optimization 27(3):1801–1833, 2017. DOI 10.1137/16M1066166. KB
`davarnia2017-…`; the KB file is the authors' 2016 dissertation.

- *Read scope:* dissertation chapter, pp.16–20.
- *Establishes:* The EC&R procedure aggregates equalities and polytope
  inequalities with nonnegative multipliers, cancels bilinear terms, and
  relaxes the rest. Theorem 2.1: all EC&R inequalities, plus the base
  ones, describe conv(S) for bilinear functions over polytope × simplex.
- *Relation:* Aggregation of original rows giving an exact hull, and a
  contrast to N3. EC&R reaches conv(S); our aggregation closure is only
  the graph relaxation.

**[DavarniaKiaghadiQiu2026]** D. Davarnia, M. Kiaghadi, J. Qiu.
*A graphical framework for global optimization of mixed-integer nonlinear
programs.* Journal of Global Optimization, 2026.
DOI 10.1007/s10898-026-01635-4; arXiv:2409.19794. KB
`davarnia2026-a-graphical-framework-for-global`.

- *Read scope:* pp.16–17 and the summary.
- *Establishes:* Decision-diagram outer approximations with a separation
  oracle that yields linear cuts. Remark 3.1 (pp.16–17) convexifies the
  intersection of several constraints simultaneously.
- *Relation:* Another original-space joint-constraint convexification.
  No validity contract for floating point is described in the passages I
  read.

**[LiEtAl2026]** T. Li, D. Ovalle, B. Póczos, C. Laird, I. Grossmann,
J. Peña. *Efficient convexification of Kolmogorov–Arnold networks with
polynomial functional forms via a continuous Graham scan approach.*
arXiv:2604.03871v1, April 4, 2026. Not in KB; the KB entry
`li2026-on-strong-valid-inequalities-for` is a different paper.

- *Read scope:* abstract on arXiv. Theorem-level content is from Report A's
  composition audit.
- *Establishes:* Exact envelopes of univariate polynomials via bitangents,
  combined componentwise for KANs.
- *Relation:* Scalar envelopes; joint cuts keep cross-output
  dependencies.

**[XuPokutta2026]** L. Xu, S. Pokutta. *Joint-range inequalities for
nonconvex QCQPs.* arXiv:2608.03318, August 5, 2026. KB
`xu2026-joint-range-inequalities-for-nonconvex`.

- *Read scope:* full text, pp.1–6, and the summary of pp.10–34.
- *Establishes:* Project-then-lift cuts. Two base inequalities, possibly
  aggregated (p.4), are projected to the joint range of two quadratics.
  The paper gives the closed convex hull of the nonconvex range
  intersected with the simplicial cone in closed form, an SDP
  representation in the convex case (Thm. 7), and secant
  mixed-joint-range cuts.
- *Relation:* Aggregation plus joint convexification in an image space,
  and "intersect then convexify" in two dimensions. It is related to
  C-AGG and N3 but works on ℝⁿ ranges with S-lemma geometry, not
  bounded-domain support with certification.

### 3.2 Lagrangian duality, aggregation, and the primal characterization (N3)

**[Falk1969]** J. E. Falk. *Lagrange multipliers and nonconvex
programs.* SIAM Journal on Control 7(4):534–545, 1969.
DOI 10.1137/0307039.

- *Read scope:* metadata and a search snippet only.
- *Establishes (snippet):* The Lagrangian bound for a nonconvex program
  is at least as sharp as the program built from convex envelopes of all
  its functions.
- *Relation:* Early primal/dual comparison. Cite for N3.

**[Geoffrion1974]** A. M. Geoffrion. *Lagrangean relaxation for integer
programming.* Mathematical Programming Study 2:82–114, 1974.
DOI 10.1007/BFb0120690.

- *Read scope:* metadata. The theorem is stated in secondary form by Dey
  and Xu (2026, p.8) and Dey, Meunier and Moran (2025, abstract and HTML).
- *Establishes:* For finite X or integer points of a rational polyhedron,
  the Lagrangian dual equals min over conv(X) ∩ {dualized rows}.
- *Relation:* C-AGG's closure is this statement applied to the lifted
  graph X = graph(g) over compact D, with the rows y + Lz ≤ b dualized.

**[LemarechalRenaud2001]** C. Lemaréchal, A. Renaud. *A geometric study
of duality gaps, with applications.* Mathematical Programming
90(3):399–427, 2001. DOI 10.1007/PL00011429.

- *Read scope:* abstract, plus a secondary statement in Kerdreux, Colin
  and d'Aspremont (arXiv:1712.08559v3, §2.2), who cite "Th. 2.11". That
  number is not verified by me.
- *Establishes (abstract):* For a nonconvex problem, the authors build "a
  convex problem having the same dual", involving "a convexification in
  the product of the three spaces containing respectively the variables,
  the objective and the constraints".
- *Relation:* This anticipates N3 most directly at the value level. Our
  closure is the set-level, projected form.

**[FeltenmarkKiwiel2000]** S. Feltenmark, K. C. Kiwiel. *Dual
applications of proximal bundle methods, including Lagrangian relaxation
of nonconvex problems.* SIAM Journal on Optimization 10(3):697–721, 2000.
DOI 10.1137/S1052623498332336.

- *Read scope:* Crossref abstract, plus the reproduction of their
  relaxation in Nowak (3.14), p.32.
- *Establishes:* Applied to Lagrangian relaxation of nonconvex programs,
  bundle methods "find solutions to relaxed convexified versions". The
  dual-equivalent relaxation is a mixture: min Σ z_j f(w_j) s.t.
  Σ z_j g(w_j) ≤ 0 with w_j ∈ G and z in the simplex.
- *Relation:* The mixture form is exactly "constraints imposed in
  expectation" (our x²=1/4 discussion).

**[Nowak2005]** I. Nowak. *Relaxation and Decomposition Methods for Mixed
Integer Nonlinear Programming.* International Series of Numerical
Mathematics 152, Birkhäuser, Basel, 2005. DOI 10.1007/3-7643-7374-1.
Read as the open habilitation, Humboldt-Universität zu Berlin, 2004:
https://edoc.hu-berlin.de/18452/14614.

- *Read scope:* full-text passages, habilitation pages 30–33, 83–84,
  93–97.
- *Establishes:*
  - Lemma 3.2, pp.30–31: the dual of a block-separable MINLP equals the
    dual of its extended (epigraph-lifted) reformulation.
  - Lemma 3.3, p.31: under a CQ, the dual equals min{cᵀx+c₀ :
    x ∈ conv(G), Ax+b ≤ 0}.
  - Lemma 3.4, pp.31–32: dual relaxations dominate convex-underestimator
    relaxations.
  - (3.14) and Lemma 3.5, pp.32–33: the Feltenmark–Kiwiel mixture
    relaxation.
  - §7.1.3, p.93: Lagrangian cuts a_k(μ)ᵀx_{J_k} ≥ D_k(μ), with
    D_k(μ) = min over the block set G_k.
  - §7.1.4, p.93: "deeper cuts" from a certified lower bound of
    Σ_{k∈K} L_k over a super-block.
  - §7.1.6, p.94: the Tawarmalani–Sahinidis Lagrangian cut.
  - Observation 7.3, p.97.
  - §6.2, pp.83–84: Bernstein–Bézier convex-hull-property lower bounds,
    used in MINLP since Nowak 1996.
- *Relation:* Anticipates the substance of N3. It also anticipates
  C-AGG's cut family in original block variables. The difference is in
  which constraints are dualized: Nowak dualizes linear coupling rows and
  keeps block nonlinear constraints in G_k; C-AGG dualizes nonlinear rows
  and supports over the box D. Its §6.2 is also relevant to C-BERN.

**[Lemarechal2001survey]** C. Lemaréchal. *Lagrangian relaxation.* In
M. Jünger, D. Naddef (eds.), Computational Combinatorial Optimization,
LNCS 2241, pp.112–156, Springer, 2001. DOI 10.1007/3-540-45586-8_4.

- *Read scope:* metadata only.
- *Relation:* Standard reference for "dual = convexified primal". Cite if
  a textbook-style source is wanted.

**[DeyMeunierMoran2025]** S. S. Dey, F. Meunier, D. Morán Ramírez.
*Geoffrion's theorem beyond finiteness and rationality.* arXiv:2510.10966v1,
October 13, 2025.

- *Read scope:* abstract, plus a tool summary of the HTML statements
  (Example 1.1, Prop. 1.1 Slater, Thm 1.2 local polyhedrality, Thm 1.3
  n ≤ 2, Thm 1.4 single rational row). I did not read the full text.
- *Establishes:* Geoffrion's conclusion can fail when X is neither finite
  nor rational-polyhedral; the paper gives sufficient conditions.
- *Relation:* The paper should state that its closure theorem is
  set-level on a compact domain. In that setting, compactness of the
  convex graph hull also gives value equality by a minimax argument (my
  reasoning, to be proved in the paper if used). The pathologies there
  come from non-closed conv(X).

**[DeyXu2026]** S. S. Dey, J. Xu. *Asymptotically tight Lagrangian dual of
smooth nonconvex problems via improved error bound of Shapley–Folkman
Lemma.* arXiv:2601.19003, 2026. KB
`dey2026-asymptotically-tight-lagrangian-dual-of`.

- *Read scope:* p.8.
- *Establishes:* Restates the primal characterization of the Lagrangian
  dual (Theorem 2, attributed to Geoffrion and to Hiriart-Urruty and
  Lemaréchal) and notes the regularity required, citing Lemaréchal and
  Renaud.
- *Relation:* Secondary confirmation for N3 positioning. It also shows
  that the duality gap of separable problems shrinks with the number of
  blocks.

**[TawarmalaniSahinidis2004]** M. Tawarmalani, N. V. Sahinidis. *Global
optimization of mixed-integer nonlinear programs: a theoretical and
computational study.* Mathematical Programming 99(3):563–591, 2004.
DOI 10.1007/s10107-003-0467-6. KB
`tawarmalani2004-global-optimization-of-mixed-integer`.

- *Read scope:* full text, pp.4–7 and 15–17.
- *Establishes:*
  - §3, pp.4–7: recursive factorable relaxation with auxiliary variables.
  - §4.1, pp.15–17: duality-based range reduction through a homogenized
    Lagrangian subproblem inf_x l(x,y₀,y). Cuts y₀u₀+yu+inf_x l ≤ 0 in
    the image space can be reused across nodes.
  - p.17: any relaxation of an NP-hard Lagrangian subproblem gives a
    weaker valid bound.
- *Relation:* Lagrangian cuts over (f(x), g(x)) images in BARON, a
  precedent for C-AGG's "a lower bound suffices, exact minimum not
  needed".

**[TawarmalaniSahinidis2002]** M. Tawarmalani, N. V. Sahinidis.
*Convexification and Global Optimization in Continuous and Mixed-Integer
Nonlinear Programming.* Nonconvex Optimization and Its Applications 65,
Kluwer, 2002. DOI 10.1007/978-1-4757-3532-1. KB
`tawarmalani2002-convexification-and-global-optimization-in`.

- *Read scope:* Ch. 5, printed pp.151–153 (KB pages 173–175).
- *Establishes:* Lagrangian relaxation through perturbation functions.
  Thm 5.5: p*(y) = −inf_x l(x,y). Domain reduction uses support functions
  of the image set U.
- *Relation:* Convex-analytic foundation that BARON uses; cite with the
  2004 paper.

**[KaruppiahGrossmann2008]** R. Karuppiah, I. E. Grossmann. *A Lagrangean
based branch-and-cut algorithm for global optimization of nonconvex
mixed-integer nonlinear programs with decomposable structures.* Journal
of Global Optimization 41(2):163–186, 2008.
DOI 10.1007/s10898-007-9203-8.

- *Read scope:* AIChE 2006 abstract only.
- *Establishes:* Cuts derived from global optima of Lagrangean-decomposed
  subproblems, added to convex relaxations.
- *Relation:* A process-systems precedent for "certified subproblem lower
  bound gives a cut in original variables".

**[MullerEtAl2022]** B. Müller, G. Muñoz, M. Gasse, A. Gleixner,
A. Lodi, F. Serrano. *On generalized surrogate duality in mixed-integer
nonlinear programming.* Mathematical Programming 192(1–2):89–118, 2022.
DOI 10.1007/s10107-021-01691-6. KB
`muller2022-on-generalized-surrogate-duality-in`.

- *Read scope:* full text, pp.89–91; summary pp.8 and 27.
- *Establishes:* Definitions 1–2: surrogate relaxations aggregate
  nonlinear constraints with λ ≥ 0 into a single nonconvex row. The
  surrogate dual is at least as strong as the Lagrangian dual. An
  algorithm and SCIP experiments on MINLPLib are given.
- *Relation:* Aggregation of original nonlinear rows in SCIP. It keeps
  the aggregated row nonconvex, whereas C-AGG produces certified linear
  cuts. Surrogate ≥ Lagrangian also means the C-AGG closure is no
  stronger than the surrogate dual for a fixed objective (my inference
  from their (4)–(5)).

**[GleixnerEtAl2017]** A. M. Gleixner, T. Berthold, B. Müller,
S. Weltge. *Three enhancements for optimization-based bound tightening.*
Journal of Global Optimization 67(4):731–757, 2017.
DOI 10.1007/s10898-016-0450-4. KB
`gleixner2017-three-enhancements-for-optimization-based`.

- *Read scope:* via Report B's audit; not re-read in this lane.
- *Relation:* Lagrangian variable bounds in original variables, which
  are redundant for the generating LP.

**[DeyMunozSerrano2022]** S. S. Dey, G. Muñoz, F. Serrano. *On obtaining
the convex hull of quadratic inequalities via aggregations.* SIAM Journal
on Optimization 32(2):659–686, 2022. DOI 10.1137/21M1428583;
arXiv:2106.12629. KB `dey2022-on-obtaining-the-convex-hull`.

- *Read scope:* abstract and p.1–5 summary.
- *Establishes:* With n ≥ 3, the PDLC condition, and a nontrivial hull,
  the three-quadratic hull is an intersection of aggregated inequalities.
  Counterexamples exist for four constraints. Yildiran (2009) gives two
  aggregations for two quadratics.
- *Relation:* Aggregation closure results that reach the true hull under
  hypotheses, a contrast to N3.

**[BlekhermanDeySun2024]** G. Blekherman, S. S. Dey, S. Sun.
*Aggregations of quadratic inequalities and hidden hyperplane
convexity.* SIAM Journal on Optimization 34(1):98–126, 2024.
DOI 10.1137/22M1528215; arXiv:2210.01722. KB
`blekherman2024-aggregations-of-quadratic-inequalities-and`.

- *Read scope:* via Report B's audit.
- *Relation:* Same role as Dey, Muñoz and Serrano.

**[FujieKojima1997]** T. Fujie, M. Kojima. *Semidefinite programming
relaxation for nonconvex quadratic programs.* Journal of Global
Optimization 10(4):367–380, 1997. DOI 10.1023/A:1008282830093.
**[KojimaTuncel2000]** M. Kojima, L. Tunçel. *Cones of matrices and
successive convex relaxations of nonconvex sets.* SIAM Journal on
Optimization 10(3):750–778, 2000. DOI 10.1137/S1052623498336450.

- *Read scope:* search snippets only.
- *Establishes (snippet):* Shor's SDP relaxation is equivalent to the
  relaxation by all convex quadratic valid inequalities obtained from the
  constraints.
- *Relation:* An aggregation-closure equals lifted-relaxation identity in
  the QCQP setting. It is the quadratic analogue of the C-AGG closure
  form.

**[WuMutsNowakHendrix2025]** O. Wu, P. Muts, I. Nowak, E. M. T. Hendrix.
*On the use of overlapping convex hull relaxations to solve nonconvex
MINLPs.* Journal of Global Optimization 91(2):415–436, 2025.
DOI 10.1007/s10898-024-01376-2. KB `wu2025-on-the-use-of-overlapping`.

- *Read scope:* full text, pp.415–420.
- *Establishes:* The convex hull relaxation (CHR) replaces each block's
  nonlinear constraint set by its convex hull; for block-separable models
  it is equivalent to column generation. Prop. 1, p.419: aggregated
  blocks containing a coupling constraint never weaken and can strictly
  tighten the CHR. The method is implemented in Decogo.
- *Relation:* Intersect-then-convexify block hulls. This is the remedy for
  the x²=1/4 limitation and the general form of Report A's
  row-constrained example. It also relates to N2: overlapping block hulls
  are "glued" only through copy constraints.

### 3.3 Factorable, composite, and original-variable (reduced-space) relaxations

**[McCormick1976]** G. P. McCormick. *Computability of global solutions to
factorable nonconvex programs: Part I — Convex underestimating problems.*
Mathematical Programming 10(1):147–175, 1976. DOI 10.1007/BF01580665. KB
`mccormick1976-computability-of-global-solutions-to`.

- *Read scope:* full text, §§1–3 and 5 (KB pp.1–11, 25–27).
- *Establishes:* Factorable functions, composite convex/concave
  estimators, bilinear envelopes, and consistency under subdivision
  (Theorems 1–2).
- *Relation:* Baseline that every joint/termwise comparison starts from.

**[SmithPantelides1999]** E. M. B. Smith, C. C. Pantelides. *A symbolic
reformulation/spatial branch-and-bound algorithm for the global
optimisation of nonconvex MINLPs.* Computers & Chemical Engineering
23(4–5):457–478, 1999. DOI 10.1016/S0098-1354(98)00286-5.

- *Read scope:* metadata only.
- *Relation:* The auxiliary-variable "standard form" (SCIP 8 p.6 calls it
  "Smith Normal Form"). This is the reformulation that Report A's
  campaign used and Report B's direct rows avoid.

**[TawarmalaniSahinidis2005]** M. Tawarmalani, N. V. Sahinidis. *A
polyhedral branch-and-cut approach to global optimization.* Mathematical
Programming 103(2):225–249, 2005. DOI 10.1007/s10107-005-0581-8. KB
`tawarmalani2005-a-polyhedral-branch-and-cut`.

- *Read scope:* full text, pp.225–227 and the theorem list (pp.226–236).
- *Establishes:* §2, Theorem 1 (p.227): for h = g∘f with convex
  components, outer-approximating f and g separately (lifted) is tighter
  than outer-approximating h directly at the same points (S₂(h) ⊆ S₁(h)).
  Theorem 2 extends this to nondifferentiable functions. Automatic
  exploitation of convex subexpressions in BARON.
- *Relation:* A referee will cite this against "original variables
  without auxiliaries". The paper should explain that its closure is
  equal but that finite cut sets can differ.

**[BelottiEtAl2009]** P. Belotti, J. Lee, L. Liberti, F. Margot,
A. Wächter. *Branching and bounds tightening techniques for non-convex
MINLP.* Optimization Methods and Software 24(4–5):597–634, 2009.
DOI 10.1080/10556780903087124. KB
`belotti2009-branching-and-bounds-tightening-techniques`.

- *Read scope:* KB summary and pp.2–7.
- *Establishes:* Couenne's DAG opt-reformulation with auxiliary
  variables, linearization, FBBT/OBBT, and violation-transfer branching.
- *Relation:* Baseline solver architecture.

**[BestuzhevaEtAl2025]** K. Bestuzheva, A. Chmiela, B. Müller,
F. Serrano, S. Vigerske, F. Wegscheider. *Global optimization of
mixed-integer nonlinear programs with SCIP 8.* Journal of Global
Optimization 91(2):287–310, 2025. DOI 10.1007/s10898-023-01345-1;
arXiv:2301.00587. KB `bestuzheva2025-global-optimization-of-mixed-integer`.

- *Read scope:* full text, pp.6–8 and 14 (arXiv v1).
- *Establishes:*
  - p.6: the extended formulation annotates subexpressions with
    auxiliary variables ("Smith Normal Form").
  - p.7: nonlinear handlers decide where to annotate.
  - p.8: extended formulations are stored as annotations on original
    expressions; feasibility is checked on the original constraints;
    branching is on original variables.
  - p.14: convexity handlers avoid auxiliaries for convex subexpressions.
- *Relation:* Native "original-expression" semantics, relevant to the
  C-AGG and C-IMPL positioning.

**[TsoukalasMitsos2014]** A. Tsoukalas, A. Mitsos. *Multivariate McCormick
relaxations.* Journal of Global Optimization 59(2–3):633–662, 2014.
DOI 10.1007/s10898-014-0176-0. Erratum: J. Najman, D. Bongartz,
A. Tsoukalas, A. Mitsos, JOGO 68(1):219–225, 2017,
DOI 10.1007/s10898-016-0470-0. KB `tsoukalas2014-multivariate-mccormick-relaxations`.

- *Read scope:* full text, pp.636–644 (KB pp.4–13).
- *Establishes:* Theorem 2 (printed p.636): multivariate composition. §4
  (pp.641–644): relation to the auxiliary variable method (AVM). The
  original-space bound can match AVM by adding selected variables.
  Minimizing McCormick relaxations by subgradient cutting planes "is
  strongly related to applying generalized Benders decomposition on the
  lower bounding problem defined by AVM". The resulting cuts are in the
  original variables.
- *Relation:* Benders/Lagrangian elimination of auxiliary variables to
  obtain original-variable cuts is the same mechanism as C-AGG's
  elimination. Must cite.

**[BongartzMitsos2017]** D. Bongartz, A. Mitsos. *Deterministic global
optimization of process flowsheets in a reduced space using McCormick
relaxations.* Journal of Global Optimization 69(4):761–796, 2017.
DOI 10.1007/s10898-017-0547-4.

- *Read scope:* abstract (search snippet).
- *Relation:* Reduced-space (original-variable) global optimization can
  outperform the equation-oriented full space.

**[NajmanBongartzMitsos2021]** J. Najman, D. Bongartz, A. Mitsos.
*Linearization of McCormick relaxations and hybridization with the
auxiliary variable method.* Journal of Global Optimization
80(4):731–756, 2021. DOI 10.1007/s10898-020-00977-x.

- *Read scope:* Crossref abstract.
- *Establishes:* Linearization points "have to be determined in the
  space of original optimization variables" (Kelley-type, simplex
  vertices, random). First results on hybridizing AVM with McCormick.
- *Relation:* Linear cuts in original variables from nonlinear
  relaxations, a positioning precedent for C-AGG.

**[WilhelmStuber2023]** M. E. Wilhelm, M. D. Stuber. *Improved convex and
concave relaxations of composite bilinear forms.* JOTA 197(1):174–204,
2023. DOI 10.1007/s10957-023-02196-2. KB
`wilhelm2023-improved-convex-and-concave-relaxations`.

- *Read scope:* summary, p.1.
- *Relation:* Reduced-space composite products without auxiliary
  variables.

**[KhajaviradMichalekSahinidis2014]** A. Khajavirad, J. J. Michalek,
N. V. Sahinidis. *Relaxations of factorable functions with
convex-transformable intermediates.* Mathematical Programming
144(1–2):107–140, 2014. DOI 10.1007/s10107-012-0618-8. KB
`khajavirad2012-relaxations-of-factorable-functions-with`.

- *Read scope:* summary, pp.1 and 20–25.
- *Relation:* Recognizing larger intermediates beats expression-tree
  relaxations, a positioning reference for block extraction.

### 3.4 Multilinear, multi-term, and product envelopes

**[Crama1993]** Y. Crama. *Concave extensions for nonlinear 0–1
maximization problems.* Mathematical Programming 61(1–3):53–60, 1993.
DOI 10.1007/BF01582138.

- *Read scope:* metadata, plus Rikun 1997 Remark 1.2 (p.431), which calls
  Rikun's Corollary 1.1 "a generalization of Crama's criterion of the
  equivalence between the standard and the convex envelope approaches".
- *Relation:* Termwise versus joint exactness criterion (when the sum of
  envelopes is the envelope of the sum).

**[Rikun1997]** A. D. Rikun. *A convex envelope formula for multilinear
functions.* Journal of Global Optimization 10(4):425–437, 1997.
DOI 10.1023/A:1008217604285. KB `rikun1997-a-convex-envelope-formula-for`.

- *Read scope:* full text, printed pp.429–436.
- *Establishes:*
  - Theorem 1.1: a polyhedral envelope holds iff the generating set
    equals the vertex set.
  - p.431: Cor. 1.1 (sum of envelopes); Theorem 1.2 (local concavity
    along a line implies polyhedral envelope); Remark 1.3 (general
    multilinear functions over products of polytopes).
  - Theorem 1.4 (p.434): sum rule under a common simplex factor.
  - Theorem 2.1 (p.436): the associated affine functions.
  - Footnote on p.435: on {0 ≤ x₁ ≤ x₂ ≤ 1}, conv x₁x₂ is not
    polyhedral.
- *Relation:* Classical termwise-versus-joint theory. The p.435 footnote
  illustrates that a non-product domain changes the hull (C-POLY).

**[MeyerFloudas2005]** C. A. Meyer, C. A. Floudas. *Convex envelopes for
edge-concave functions.* Mathematical Programming 103(2):207–224, 2005.
DOI 10.1007/s10107-005-0580-9.

- *Read scope:* metadata (cited by Mertens 2019, p.78).
- *Relation:* Vertex-polyhedral envelopes of edge-concave functions.

**[MisenerFloudas2012]** R. Misener, C. A. Floudas. *Global optimization
of mixed-integer quadratically-constrained quadratic programs (MIQCQP)
through piecewise-linear and edge-concave relaxations.* Mathematical
Programming 136(1):155–182, 2012. DOI 10.1007/s10107-012-0555-6.
**[MisenerFloudas2014]** R. Misener, C. A. Floudas. *ANTIGONE: Algorithms
for coNTinuous/Integer Global Optimization of Nonlinear Equations.*
Journal of Global Optimization 59(2–3):503–526, 2014.
DOI 10.1007/s10898-014-0166-2.

- *Read scope:* abstract snippets only.
- *Establishes:* Facets of low-dimensional (n ≤ 3) edge-concave
  aggregations of bilinear and quadratic terms at every node (GloMIQO).
- *Relation:* Grouping of terms into small joint blocks inside a global
  solver, a precedent for block-level joint cuts.

**[MisenerSmadbeckFloudas2015]** R. Misener, J. B. Smadbeck,
C. A. Floudas. *Dynamically generated cutting planes for mixed-integer
quadratically constrained quadratic programs and their incorporation into
GloMIQO 2.* Optimization Methods and Software 30(1):215–249, 2015.
DOI 10.1080/10556788.2014.916287.

- *Read scope:* metadata. Boland et al. (2017, pp.3 and 10) attribute to
  it "Theorem 3.10": McCormick describes the bilinear convex envelope iff
  every cycle has an even number of positive edges.
- *Relation:* Original source for McCormick exactness on forests (C-OVER).

**[BaoSahinidisTawarmalani2009]** X. Bao, N. V. Sahinidis,
M. Tawarmalani. *Multiterm polyhedral relaxations for nonconvex,
quadratically constrained quadratic programs.* Optimization Methods and
Software 24(4–5):485–504, 2009. DOI 10.1080/10556780902883184. KB
`bao2009-multiterm-polyhedral-relaxations-for-nonconvex`.

- *Read scope:* summary, pp.2–19.
- *Establishes:* Theorem 2.4 (pp.5–7): facets of the grouped bilinear
  envelope over a box from an LP over vertices. MUL and COL separation;
  root gap closure in BARON at high separation cost.
- *Relation:* Multi-term joint convexification with LP separation, a
  direct analogue of block-level joint cuts with a cost warning.

**[BaoKhajaviradSahinidisTawarmalani2015]** X. Bao, A. Khajavirad,
N. V. Sahinidis, M. Tawarmalani. *Global optimization of nonconvex
problems with multilinear intermediates.* Mathematical Programming
Computation 7(1):1–37, 2015 (online 2014). DOI 10.1007/s12532-014-0073-z.
IBM report RC25318.

- *Read scope:* abstract (search snippet).
- *Establishes:* Multilinear hull facets by LP; a graph decomposition to
  low-dimensional components; cuts at every BARON node; reported ~60%
  average CPU time reduction.
- *Relation:* The strongest computational counterexample to "joint cuts
  do not pay". The paper's negative campaign result must be framed
  against it.

**[LuedtkeNamazifarLinderoth2012]** J. Luedtke, M. Namazifar,
J. Linderoth. *Some results on the strength of relaxations of
multilinear functions.* Mathematical Programming 136(2):325–351, 2012.
DOI 10.1007/s10107-012-0606-z. KB `luedtke2012-some-results-on-the-strength`.

- *Read scope:* summary with locators pp.2–22.
- *Establishes:* Recursive McCormick is exact for products on [0,u] and
  [−u,u]. Positive-coefficient bilinear termwise envelopes equal the
  hull. Theorem 8 gives the coloring-number bound mcgap ≤ (2−2/χ)·chgap.
  Theorem 10 shows edge removal is monotone.
- *Relation:* Termwise versus joint gap theory, and exactness for
  bipartite positive-weight bilinear graphs.

**[BolandEtAl2017]** N. Boland, S. S. Dey, T. Kalinowski, M. Molinaro,
F. Rigterink. *Bounding the gap between the McCormick relaxation and the
convex hull for bilinear functions.* Mathematical Programming
162(1–2):523–535, 2017. DOI 10.1007/s10107-016-1031-5. KB
`boland2017-bounding-the-gap-between-the`.

- *Read scope:* full text, pp.1–3 and 10–11.
- *Establishes:* The ratio mcgap/chgap is ≥ √n/4 asymptotically almost
  surely for random signs and ≤ 600√n always. Theorem 4 (p.3, proof
  pp.10–11): Q = conv(B) iff every cycle has even numbers of positive and
  of negative edges; "if G is a forest then Q = conv(B) for every choice
  of coefficients".
- *Relation:* Anticipates the C-OVER sub-claim "McCormick is exact for
  pure bilinear forests". The paper must cite it, together with
  Misener–Smadbeck–Floudas and Luedtke et al.

**[KhajaviradSahinidis2012]** A. Khajavirad, N. V. Sahinidis. *Convex
envelopes of products of convex and component-wise concave functions.*
Journal of Global Optimization 52(3):391–409, 2012.
DOI 10.1007/s10898-011-9747-5.

- *Read scope:* metadata only.

**[KhajaviradSahinidis2013]** A. Khajavirad, N. V. Sahinidis. *Convex
envelopes generated from finitely many compact convex sets.* Mathematical
Programming 137(1–2):371–408, 2013. DOI 10.1007/s10107-011-0496-5. KB
`khajavirad2013-convex-envelopes-generated-from-finitely`.

- *Read scope:* summary, pp.1–16 and 33–35.
- *Establishes:* Exact envelope formulations from finite convex
  generating sets (formulation CX). Closed forms for f(x)g(y) with
  convex f and componentwise concave g. Reported gaps above 70% for the
  standard relaxations. p.55 credits Tawarmalani (2010) for simultaneous
  convexification.
- *Relation:* Exact envelopes of specific products. Background for C-SUP
  and C-POLY.

**[TawarmalaniRichardXiong2013]** M. Tawarmalani, J.-P. P. Richard,
C. Xiong. *Explicit convex and concave envelopes through polyhedral
subdivisions.* Mathematical Programming 138(1–2):531–577, 2013.
DOI 10.1007/s10107-012-0581-4. The KB package
`tawarmalani2013-convex-envelopes-of-products-of` has the wrong title
"Convex Envelopes of Products of Linear Functions over Polytopes"; the DOI
and Crossref give the title above.

- *Read scope:* summary, pp.1–33, of the 2010 preprint.
- *Establishes:* An envelope LP over polyhedral subdivisions;
  supermodular concave-extendable envelopes via Kuhn triangulations;
  disjunctive convex functions.
- *Relation:* The structural basis for He and Tawarmalani (2022)
  Theorem 4.

**[NguyenRichardTawarmalani2018]** T. T. Nguyen, J.-P. P. Richard,
M. Tawarmalani. *Deriving convex hulls through lifting and projection.*
Mathematical Programming 169(2):377–415, 2018.
DOI 10.1007/s10107-017-1138-3. KB `nguyen2018-deriving-convex-hulls-through-lifting`.

- *Read scope:* summary, pp.1–6 and 32–35.
- *Establishes:* x-space convex hulls of monomial covering, packing, and
  equality sets by lifting then projecting semi-infinite families.
- *Relation:* A precedent for "hull in original variables by projection"
  (C-AGG closure style).

### 3.5 Polytope domains and low-dimensional quadratic hulls (C-POLY positioning)

**[AnstreicherBurer2010]** K. M. Anstreicher, S. Burer. *Computable
representations for convex hulls of low-dimensional quadratic forms.*
Mathematical Programming 124(1–2):33–43, 2010.
DOI 10.1007/s10107-010-0355-9. KB
`anstreicher2010-computable-representations-for-convex-hulls`.

- *Read scope:* via Report A's audit (Thms 3, 6, 7).
- *Relation:* Exact quadratic-graph hulls on triangulated polytopes of
  dimension ≤ 3. Report A's polygon result specializes it.

**[LocatelliSchoen2014]** M. Locatelli, F. Schoen. *On convex envelopes
for bivariate functions over polytopes.* Mathematical Programming
144(1–2):65–91, 2014. DOI 10.1007/s10107-012-0616-x. KB
`locatelli2014-on-convex-envelopes-for-bivariate`.

- *Read scope:* summary, pp.1–4.
- *Establishes:* Envelopes over triangles and polygons. A value and
  supporting hyperplane can need up to 3^t three-dimensional convex
  subproblems.
- *Relation:* A precedent for exact two-dimensional polytope envelopes.

**[SantanaDey2020]** A. Santana, S. S. Dey. *The convex hull of a
quadratic constraint over a polytope.* SIAM Journal on Optimization
30(4):2983–2997, 2020. DOI 10.1137/19M1277333. KB
`santana2020-the-convex-hull-of-a`.

- *Read scope:* summary.
- *Relation:* The hull of one quadratic equality over a bounded polytope
  is SOC-representable (possibly with exponential size). This is
  "intersect then convexify" for one row over a polytope.

### 3.6 Numerical validity of cuts (N4 ingredients within this lane)

**[NeumaierShcherbina2004]** A. Neumaier, O. Shcherbina. *Safe bounds in
linear and mixed-integer linear programming.* Mathematical Programming
99(2):283–296, 2004. DOI 10.1007/s10107-003-0433-3. KB
`neumaier2004-safe-bounds-in-linear-and`.

- *Read scope:* full text, printed p.294 (KB p.12).
- *Establishes:* §7: decide cuts in floating point, then "repeat the
  arguments leading to the cuts with rigorous rounding error control".
  The search "need not be safeguarded since the bounds are valid for the
  s actually used, independent of its construction".
- *Relation:* Direct precedent for C-SUP's principle that soundness
  depends only on a bound for the final direction.

**[BorradaileVanHentenryck2005]** G. Borradaile, P. Van Hentenryck.
*Safe and tight linear estimators for global optimization.* Mathematical
Programming 102(3):495–517, 2005 (online 2004).
DOI 10.1007/s10107-004-0533-8.

- *Read scope:* metadata only.
- *Relation:* Floating-point-safe linear relaxations of factorable terms,
  a precedent for safe export of relaxation rows.

**[HojnyEtAl2025]** C. Hojny, M. Besançon, K. Bestuzheva, et al. *The SCIP
Optimization Suite 10.0.* arXiv:2511.18580, 2025. KB
`hojny2025-the-scip-optimization-suite-10`.

- *Read scope:* full text, pp.7–8.
- *Establishes:* An exact solving mode with VIPR certificates and exact
  readers (MPS/LP/CIP/OPB/ZIMPL) "restricted to mixed-integer linear
  programs".
- *Relation:* The exact certification infrastructure stops at MILP. This
  supports the N4/N6 statement that exact MINLP cut certification and
  source-faithful nonlinear import are not native. It also shows that
  exact reading of source data is established practice for linear data.

## 4. Claim-by-claim positioning

### C-SUP

- Prop. support is the support-function (biconjugate) description of
  conv graph. It is attributed to Ballerstein (2013), Liers et al.
  (Prop. 1), and Tawarmalani (2010, Cor. 2.6). Cite Rockafellar's
  *Convex Analysis* for the separation step. Keep the existing text "This
  is classical convex hull duality".
- The direction-search independence of soundness is anticipated in
  principle by Neumaier and Shcherbina (2004, §7).
- What the paper can claim:
  - the certificate is for the exact exported binary64 row of a joint
    vector cut;
  - it covers the whole domain;
  - it holds for a stated elementary grammar.

  Liers et al. mention only unspecified "safe rounding".
- What it cannot claim: a first simultaneous separation method, or exact
  hulls for vectors of univariate powers and reciprocals. He, Liu and
  Tawarmalani give the latter via moment hulls.

### C-AGG and N3

- Validity: weak Lagrangian duality. Cite Boyd and Vandenberghe and
  Geoffrion 1974, plus the Lagrangian-cut lineage: Nowak 2005 §7.1.3–7.1.4;
  Tawarmalani and Sahinidis 2004 §4; Karuppiah and Grossmann 2008.
- Closure theorem: this is the primal characterization of the Lagrangian
  dual, convexify then impose the dualized rows. See Lemaréchal and
  Renaud 2001 (abstract); Feltenmark and Kiwiel 2000; Nowak 2005
  Lemmas 3.3 and 3.5; Geoffrion 1974; Falk 1969.

  The paper's formulation adds two things. It states the identity at set
  level, with a projection to (x, z) and affine remainders. Its proof on
  compact D needs no CQ. Present it as "a known duality fact stated for
  our cut interface", not as a novelty.
- Gap example: standard (duality gap; constraints in expectation, as in
  the Feltenmark–Kiwiel mixture form). Keep it only as an illustration.
- Remedy (constrained support domain): anticipated by Wu et al. 2025,
  Nowak 2005 (3.13), and Zhu et al. 2026 Thm 8.
- Elimination and safe rounding: Eifler and Gleixner (2024), and Cook,
  Dash, Fukasawa and Goycoolea (2009), from Report B's audit.

  Add Tawarmalani and Sahinidis 2005 Thm 1 and Tsoukalas and Mitsos 2014
  §4 to discuss what removing auxiliary variables loses: polyhedral
  tightness at fixed linearization points. They also show what is
  equivalent: Benders projection.

### C-POLY

- Joint support of a quadratic vector is minimization of one quadratic.
  Lane-relevant precedents are Anstreicher–Burer (Thm 7), Locatelli–Schoen
  (polygons), Rikun's non-polyhedral footnote, Santana–Dey, and Zhu et al.
  on linking constraints.
- The general-d enumeration and complexity belong to the quadratic-support
  lane (Murty 1997 face enumeration; Vavasis 1990).
- Report A's "row-constrained domain beats box hull ∩ row" should cite
  Zhu et al. (p.2, Thm 8), Wu et al. (Prop. 1), and Rikun (p.435).

### General positioning

- Joint and multi-term cuts can pay in practice: Bao et al. 2009 and
  2015; Liers et al. 2021; Misener and Floudas.
- Reduced-space methods can pay: Bongartz and Mitsos 2017.
- The paper's negative complete-solve result should be stated against
  these positive precedents and against native SCIP's handlers (SCIP 8).
  It should not be presented as evidence that joint convexification is
  useless.

## 5. Novelty verdicts (this lane)

| Candidate | Verdict | Key evidence |
|---|---|---|
| N3 closure characterization and gap | Anticipated in substance (value-level primal characterization of the Lagrangian dual). The set-level statement for direct rows with affine remainders and no CQ is a modest reformulation. The x²=1/4 gap is a standard duality-gap instance. | Lemaréchal–Renaud 2001 (abstract); Nowak 2005 L3.3/L3.5 and (3.14), pp.31–33; Feltenmark–Kiwiel 2000; Geoffrion 1974; Falk 1969; Dey–Xu 2026, p.8 |
| N4 certification contract (lane view) | Not anticipated as a combination in this lane. Each ingredient has precedent: the direction-independent soundness principle (Neumaier–Shcherbina §7); safe rounding (Liers p.25, unspecified; Eifler–Gleixner); validated affine bounds (Garloff–Smith, other lane). | Liers 2021, pp.25 and 36; Neumaier–Shcherbina 2004, p.294; SCIP 10 exact mode is MILP-only (pp.7–8) |
| C-SUP mathematics | Classical | Ballerstein 2013 via Liers Prop. 1; Tawarmalani 2010 Cor 2.6/3.9; He–Tawarmalani 2021 Thm 6 |
| N2 pair-hull obstruction (lane view) | Phenomenon known qualitatively; full-marginal gluing appears in Tawarmalani 2010 Cor 3.10. The specific 1/128 witness and δ²/2 family were not found. | Tawarmalani 2010, pp.14–16; Liers 2021, p.29; He–Tawarmalani 2024 §7.2 |
| C-OVER forest exactness | Anticipated | Boland et al. 2017 Thm 4; Misener–Smadbeck–Floudas 2015 (Thm 3.10 per Boland); Luedtke et al. 2012 |
| C-POLY row-constrained example | Principle anticipated; the explicit example is illustrative | Zhu et al. 2026, p.2 and Thm 8; Wu et al. 2025 Prop. 1; Rikun 1997, p.435 |
| N6 source-faithful import (lane view) | Partial precedent for the linear part only | SCIP 10 exact readers (MILP), p.8; SCIP 8 original-constraint feasibility checks, p.8 |
| N1, N5 | No anticipating source in this lane. Del Pia–Khajavirad, parametric QP, and Grötschel–Lovász–Schrijver belong to other lanes. | n/a |

## 6. Must-cite list

These are the minimum for a referee in global optimization. Keys refer to
section 3.

- Simultaneous hulls: Tawarmalani2010; Ballerstein2013; LiersEtAl2021;
  HeTawarmalani2021; HeTawarmalani2022; HeTawarmalani2024;
  ZhuHeTawarmalani2026; HeLiuTawarmalani2023.
- Factorable and original-space relaxations: McCormick1976;
  SmithPantelides1999; TawarmalaniSahinidis2002; TawarmalaniSahinidis2004;
  TawarmalaniSahinidis2005; BelottiEtAl2009; BestuzhevaEtAl2025;
  TsoukalasMitsos2014; NajmanBongartzMitsos2021; BongartzMitsos2017.
- Multilinear and multi-term: Rikun1997; Crama1993; BaoSahinidisTawarmalani2009;
  BaoKhajaviradSahinidisTawarmalani2015; LuedtkeNamazifarLinderoth2012;
  BolandEtAl2017; MisenerFloudas2012; MisenerSmadbeckFloudas2015;
  KhajaviradSahinidis2012 or KhajaviradSahinidis2013;
  TawarmalaniRichardXiong2013.
- Lagrangian duality and aggregation: Geoffrion1974; LemarechalRenaud2001;
  Nowak2005; FeltenmarkKiwiel2000; MullerEtAl2022; DavarniaRichardTawarmalani2017;
  DeyMunozSerrano2022; WuMutsNowakHendrix2025.
- Numerical validity: NeumaierShcherbina2004.

## 7. Corrections and flags for the paper team

1. Reports A and B cite only Boyd and Vandenberghe for the aggregation
   inference and present the closure theorem as "self-contained". Add the
   Lagrangian primal-characterization literature (§3.2) and soften the
   novelty language for N3.
2. KB metadata error: `tawarmalani2013-convex-envelopes-of-products-of`
   has the wrong title. Use "Explicit convex and concave envelopes through
   polyhedral subdivisions" (DOI 10.1007/s10107-012-0581-4). I did not
   edit the KB.
3. He and Tawarmalani 2024 numbering differs by version. The KB copy uses
   §7.2, Prop. 7.4, Cor. 7.5, Remark 4.3; arXiv v3 uses Prop. 28,
   Cor. 29, Remark 11. Cite the published version's numbering after
   checking it, or name the version.
4. The KB Davarnia 2017 package is the dissertation. Its page locators are
   dissertation pages, not SIAM pages.
5. Ballerstein 2013 remains not accessed. Attribute the hull
   characterization through Liers et al. Prop. 1 and Mertens Prop. 3.13
   ("Cor. 5.25"), or retrieve the thesis by an allowed route.
6. The 1/128 overlap witness should be positioned against Tawarmalani 2010
   Cor 3.10. That corollary gives exactness when certificate marginals
   agree on all subsets; our witness shows that agreement of first and
   second moments is not enough.

## 8. Checks run (targeted, local)

- `grep` over `literature/index.md` and `literature/papers/*/fulltext.md`
  for lane terms. I read the KB passages cited above.
- `pdftotext -layout` on local read-only copies of He–Tawarmalani 2021 and
  2022, and on downloaded open PDFs (Nowak habilitation, Mertens
  dissertation, Kerdreux et al.), all written to `/tmp` only.
- Crossref API metadata lookups for every DOI listed, and Semantic Scholar
  API title checks.
- arXiv abstract pages for 2604.03871 and 2510.10966.
- No project-wide tests, no CI inspection, and no edits under
  `literature/` or `research-2026100*-convexification/`.
