# Literature lane L2: sparse quadratic hulls, gluing, stars and moments

Date: 2026-10-03. Lane focus: sparse quadratic and polynomial convex hulls,
decomposition and gluing of local hulls, low-dimensional quadratic hulls,
tree/star/forest quadratic programs, parametric QP, and moment theory.
Claims examined: C-STAR (N1), C-OVER (N2), and the hull and complexity
parts of C-POLY.

This is a targeted search. It is not a proof that no anticipating work
exists. "Read" means that I read the cited passage in full text: the local
KB `fulltext.md`, or a lawful preprint downloaded to `/tmp/l2lit/` and
converted with `pdftotext`. "Abstract-level" means that I saw only the
metadata, abstract, or another paper's description. Page numbers refer to
the version I read. They are preprint pages unless stated otherwise.

## 1. Main findings

1. **N2 (pair-hull obstruction) is partly anticipated.** The phenomenon
   itself is known. On a path, with the running intersection property,
   exact local blocks glued on finitely many shared moments can fail to
   give the joint hull or a tight sparse relaxation. The known mechanism is
   that the separator's truncated moments do not determine its marginal.
   Prior explicit path examples exist:
   - Nie and Demmel (2008/09), Example 3.5. It is unconstrained, quartic,
     and its gap is numerical.
   - Nie, Qu, Tang and Zhang (2026), Example 6.7. It is box-constrained and
     quartic. The sparse moment-SOS hierarchy is never tight at any order,
     although the dense hierarchy is tight.
   - Lasserre (2006), Thm. 3.7, and Fantuzzi and Fuentes (2025), Thm. 1.1.
     Both need extra rank (flatness) conditions on the clique overlaps for
     finite gluing.
   - Kojima, Kim and Arima (2026), Sec. 3.3. Overlaps with off-diagonal
     entries create a product obstruction.
   - Dey and Khajavirad (2026), Cor. 1. Its decomposition needs a separator
     without a "plus loop".
   - Burer, Natarajan and Willemsen (2025), p. 46. They observed
     numerically that RLT bounds on zero-pattern pairs are "not always"
     redundant.

   I found no prior example with all of the following properties:
   - degree two, with exact pair hulls that include the squares;
   - the unit-cube path `x-y-z`;
   - the exact rational gap 1/128, an explicit witness, and an explicit cut
     with no `xz` coordinate;
   - the `delta^2/2` family.

   This combination appears new within the search. The paper should present
   it as a minimal explicit degree-2 instance of a known mechanism, cite the
   works above, and place it in their terminology (Section 4.2).
2. **N1 (constrained stars, all signs) is fully anticipated in the box case
   and not anticipated, within the search, with center–leaf affine rows.**
   - Del Pia and Khajavirad (2026), Thm. 1, solve box QP on forests with
     any signs in `O(n^2)` operations, strongly polynomially.
   - Dey and Khajavirad (2026), Thm. 1, Cor. 3 and Thm. 2, give explicit SOC
     hull formulations for stars whose plus-loop center has no plus-loop
     neighbors. These formulations can be exponential in the degree.
   - Bienstock and Muñoz (2018), Thm. 4, give only an epsilon-approximate
     LP for the same structural class with constraints.

   I found no polynomial exact algorithm for nonconvex star QPs whose affine
   rows couple the center with single leaves. An expert will, however, see
   it as a direct application of nonserial dynamic programming and
   one-parameter parametric scalar minimization. The claim should be stated
   as a modest, explicitly scoped extension.
3. **The hull parts of C-POLY are classical.** Exact low-dimensional
   quadratic hulls are due to Anstreicher and Burer (2010), Thms. 3, 6 and 7.
   Anstreicher (2012), Thm. 1 and Cor. 1, shows that convexifying the
   quadratic form over the linear-constraint region dominates separate
   envelopes. Report A's row-domain example is an RLT constraint-factor
   product (Sherali–Adams). Del Pia and Khajavirad (2026), Thm. 3, prove a
   stronger hardness result than the MaxCut reduction: strong NP-hardness
   for box QP at treewidth two.

## 2. Search record

- KB: `grep -i` over `literature/index.md` (about 1,330 lines) for the
  authors and topics named in the lane brief. This found Lasserre, Waki,
  Anstreicher, Burer, Letchford, Del Pia, Khajavirad, Bienstock, Padberg,
  Bemporad, Locatelli, Azuma and Kojima, plus "forest", "tree", "star",
  "acyclic", "chordal", "block-clique", "completely positive", "moment",
  "parametric quadratic" and "arrowhead". `grep -l` over
  `papers/*/fulltext.md` searched for "block-clique", "local consistency",
  "marginal polytope" and "arrowhead".
- KB full texts read: Lasserre 2006; Waki et al. 2006 (report version);
  Anstreicher–Burer 2010 (2007 preprint); Burer–Letchford 2009;
  Anstreicher–Puges 2025; Padberg 1989; Dey–Khajavirad (arXiv 2508.18435);
  Khajavirad 2026 (arXiv 2601.18545v2); Del Pia–Khajavirad 2026 (arXiv
  2609.35595v1); Kojima–Kim–Arima 2026; Azuma et al. 2023;
  Bienstock–Muñoz 2018; Burer–Natarajan–Willemsen 2025; Bemporad et al.
  2002 (Thms. 2 and 4); Locatelli 2015 (technical report, Sec. 5);
  Khajavirad 2011 thesis (Ch. 5, arrowhead decomposition). The KB records
  for Del Pia–Khajavirad 2018 and 2021 were read at abstract level.
- Online, read: Grimm–Netzer–Schweighofer (arXiv math/0611498);
  Nie–Demmel (arXiv math/0606476v3); Laurent's survey (CWI updated
  version, 6 Feb 2010); Nie–Qu–Tang–Zhang (arXiv 2406.06882v3);
  Fantuzzi–Fuentes (arXiv 2502.01410v3); Anstreicher 2012 (Optimization
  Online preprint, 28 Jul 2010).
- Online, partial or abstract-level: Kim–Kojima–Toh 2020 (ar5iv HTML via
  WebFetch summary); Bonami–Günlük–Linderoth 2018 (IBM abstract);
  Moré–Vavasis 1990 (abstract); Bose et al. (arXiv abstract); Vorob'ev 1962
  (Math-Net abstract).
- Metadata checked through Crossref: Drew–Johnson 1998, Grone et al. 1984,
  Vandenberghe–Andersen 2015, GNS 2007, Nie–Demmel, NQTZ, Laurent 2009,
  Azuma et al. 2022 and 2023, Dey–Khajavirad 2026.
- Not accessed: Karlin–Studden 1966 and Krein–Nudelman 1977 (books);
  Drew–Johnson full text; Pardalos–Vavasis 1991; Sherali–Adams 1990;
  Bertelè–Brioschi 1972; Santana–Dey 2020. They are listed for
  bibliographic completeness only.
- Web queries included:
  - "intersection of convex hulls overlapping quadratic blocks … path …
    counterexample";
  - "sparse SDP relaxation box QP chordal … loses McCormick … nonedge";
  - "Drew Johnson completely positive completion block-clique";
  - "sparse moment relaxation extraction rank one overlaps … gluing fails";
  - "nonconvex QP star graph center leaves linear constraints coupling …
    polynomial";
  - "arrowhead Hessian nonconvex QP box polynomial";
  - "single linking variable … piecewise quadratic value function";
  - "signed measure orthogonal to Chebyshev system sign changes".

## 3. Works, grouped by topic

Every entry states what the work establishes and how it relates to our
claims. "Anticipates" uses none, partial or full.

### 3.1 Sparse moment and SOS hierarchies, and gluing of measures

**[Lasserre2006]** J. B. Lasserre. Convergent SDP-relaxations in polynomial
optimization with sparsity. *SIAM J. Optim.* 17(3):822–843, 2006.
DOI 10.1137/05064504X. Read: full Optimization Online preprint (KB).
- Running intersection property (1.3), p. 3.
- Thm. 3.6, p. 9: the sparse hierarchy converges under Assumptions 3.1–3.2.
- Thm. 3.7, p. 10: finite exactness and extraction need flatness on each
  clique and `rank M_s0(y, I_jk) = 1` on every overlap.
- Proof of 3.6, p. 15: equal marginals follow from equality of all
  moments, by moment determinacy on compacts.
- Lemma 6.3, p. 18 (two blocks) and Lemma 6.4, p. 20 (RIP family): glue
  measures whose marginals are consistent.

Relation: this is the source for C-OVER's "full-marginal gluing" remedy.
Thm. 3.7's rank-one overlap condition is exactly what fails in our witness:
the separator moment matrix `[[1,1/2],[1/2,5/16]]` has rank 2. Lasserre
does not give an explicit failure example. Anticipates N2: partial (the
mechanism, not the instance).

**[Vorobev1962]** N. N. Vorob'ev. Consistent families of measures and their
extensions. *Theory Probab. Appl.* 7(2):147–163, 1962. DOI 10.1137/1107014.
Read: abstract-level (Math-Net). The abstract states that regularity
(acyclicity) of the complex is necessary and sufficient for every
consistent family of measures to extend. Relation: the classical gluing
theorem behind "full marginals glue on trees". Cite it next to Lasserre for
the remedy subsection. Anticipates: none.

**[WakiEtAl2006]** H. Waki, S. Kim, M. Kojima, M. Muramatsu. Sums of squares
and semidefinite program relaxations for polynomial optimization problems
with structured sparsity. *SIAM J. Optim.* 17(1):218–242, 2006.
DOI 10.1137/050623802. Read: Research Report version (KB).
- Defines the correlative sparsity pattern (csp) graph and the
  chordal-extension clique relaxations (Secs. 3.3–3.4).
- p. 4: sparse relaxations are "not guaranteed" to match dense ones in
  general. For QOPs, order-1 sparse equals order-1 dense.
- Sec. 3.5, p. 11: the unconstrained quadratic case.

Relation: the standard sparse SDP that C-OVER compares against. Our
witness relies on box RLT products existing only on edges. A nonedge
McCormick product is not part of the csp-respecting relaxation. Hence no
conflict with the "sparse = dense for QOPs" statement. Anticipates: none.

**[GrimmNetzerSchweighofer2007]** D. Grimm, T. Netzer, M. Schweighofer. A note
on the representation of positive polynomials with structured sparsity.
*Arch. Math.* 89(5):399–403, 2007. DOI 10.1007/s00013-007-2234-z.
arXiv math/0611498. Read: full preprint.
- Lemma 3, pp. 2–3: under RIP, if `f = f_1+...+f_r` is positive on `K^n`,
  then `f = h_1+...+h_r` with every `h_j > 0` on its block. The proof
  shifts a polynomial `p` on the separator that approximates the
  continuous min-marginal `h(y) = min_x f_1(x,y) - eps/2`.
- Thm. 4 and Cor. 5, pp. 3–4: the sparse Putinar representation, the
  result of Lasserre, Kojima and Muramatsu.

Relation: the dual mechanism of N2. Identifying only `(y, y^2)` restricts
the separator function `p` to `span{1, y, y^2}`. GNS need arbitrary-degree
`p` (Section 4.2). Anticipates N2: partial (mechanism).

**[NieDemmel2009]** J. Nie, J. Demmel. Sparse SOS relaxations for minimizing
functions that are summations of small polynomials. *SIAM J. Optim.*
19(4):1534–1558, 2008/09. DOI 10.1137/060668791. arXiv math/0606476.
Read: v3 preprint, 5 Oct 2007.
- Thm. 3.3, p. 8: if the optimal local moment matrices have representing
  measures and RIP holds, the sparse bound equals the dense SOS bound.
- Remark 3.4 and Example 3.5, p. 8: RIP alone is not sufficient. With
  `f = [x1^4 + (x1 x2 - 1)^2] + [x2^2 x3^2 + (x3^2 - 1)^2]` on the path
  `x1-x2-x3`, they find numerically `f_sparse ≈ 5e-5 < f_sos ≈ 0.8499`.
- Cor. 3.6, p. 8: equality holds for quadratic `f_i` under RIP.

Relation:
- Example 3.5 is a prior explicit path example of a gap between sparse
  gluing and the joint relaxation. It is unconstrained and of degree 4, and
  the gap is numerical rather than an exact hull gap.
- The proof of Thm. 3.3 says that equal overlap moment submatrices make the
  local measures' marginals "consistent" and then applies Lasserre's Lemma
  6.4. Our witness shows that this inference fails in general: two local
  measures, equal `E y` and `E y^2`, different `y`-marginals, and no global
  measure.
- We do not claim that Thm. 3.3's conclusion is false. For degree 2 its
  conclusion follows from PSD completion, as in Cor. 3.6. The journal
  version was not checked.

Anticipates N2: partial.

**[Laurent2009]** M. Laurent. Sums of squares, moment matrices and
optimization over polynomials. In M. Putinar, S. Sullivant (eds.),
*Emerging Applications of Algebraic Geometry*, IMA Vol. Math. Appl. 149,
Springer, 2009, pp. 157–270. DOI 10.1007/978-0-387-09686-5_7.
Read: updated CWI version, 6 Feb 2010, Sec. 8.1.
- Lemma 8.6 and Cor. 8.7, p. 124 of the updated version: under RIP with
  quadratic data, sparse and dense order-1 moment and SOS values coincide.
  The proof uses PSD completion (Grone et al.).
- Example 8.8, pp. 124–125: Waki's degree-4 example, sparse 0 versus dense
  0.84986.
- Thm. 8.9: the sparse Putinar theorem of GNS.

Relation: the standard reference for "sparse = dense for quadratics". It
lets the paper state precisely that our gap needs box RLT and exact local
hulls (each pair is QPB_2 = SDP+RLT), not the Shor relaxation alone.
Anticipates N2: partial (degree-4 analogue).

**[NieQuTangZhang2026]** J. Nie, Z. Qu, X. Tang, L. Zhang. A characterization
for tightness of the sparse moment-SOS hierarchy. *Math. Program.*
215:369–405, 2026 (online 2025). DOI 10.1007/s10107-025-02223-2.
arXiv 2406.06882. Read: v3 preprint.
- Thm. 3.1, pp. 7–8: tightness at order `k` holds iff `f - f_min` splits
  into a sum `sum_i (f_i + p_i)` with `sum_i p_i + f_min = 0` and each part
  in its clique's truncated ideal plus quadratic module.
- Thm. 3.5, p. 11: extraction under RIP plus overlap flat truncation.
- Assumption 4.1: polynomial interfaces `p_i` with block-nonnegative parts.
- Example 6.7, p. 20: `x1^2 + (x1 x2 - 1)^2 + (x2 x3)^2 + (x3 - 1)^2` on
  `[-1,1]^3`, cliques `{1,2}` and `{2,3}`. The sparse hierarchy is never
  tight, because the required interface `p1(x2) = -(x2^2+1)^{-1}` is not a
  polynomial. The dense hierarchy is tight.

Relation: the closest prior art for N2.
- It proves an exact path counterexample with RIP, compact box, and the
  min-marginal argument.
- Differences: their example is quartic. The failure is at every degree
  and is caused by a non-polynomial message. Their relaxations use SOS
  certificates, not exact local hulls.
- Our example is quadratic, with exact pair hulls. Its failure comes only
  from truncating the interface to degree 2. A lane computation (Section 5)
  suggests that a cubic interface already closes the gap.

Anticipates N2: partial. It must be cited as the general characterization.

**[FantuzziFuentes2025]** G. Fantuzzi, F. Fuentes. Finite convergence and
minimizer extraction in moment relaxations with correlative sparsity.
arXiv 2502.01410, v3, 6 Jul 2026. Read: full preprint, Secs. 1, 3 and 5.3.
- Thm. 1.1, p. 2: a solution of the truncated correlatively sparse moment
  problem. It needs RIP, clique flat extension (1.4a), and overlap flatness
  (1.4b). Lemma 3.3, p. 7: (1.4b) gives a unique overlap measure, hence
  consistent marginals.
- p. 3: they say prior sparse analyses "implicitly rely" on such results.
- Sec. 5.3: an example without RIP (the triangle with atoms `±1`) where
  local unique measures exist but no global measure does.
- p. 3: the measure in (1.7) on cliques `{1,2}`, `{2,3}` shows that sparse
  moments determine only marginals.

Relation: our witness complements their RIP-necessity example. RIP holds,
but overlap flatness (1.4b) fails (rank 2 versus rank 1), and gluing fails.
They give no such RIP example, so the overlap condition is shown to be
needed. Anticipates N2: partial (framework).

**[GroneEtAl1984]** R. Grone, C. R. Johnson, E. M. Sá, H. Wolkowicz. Positive
definite completions of partial Hermitian matrices. *Linear Algebra Appl.*
58:109–124, 1984. DOI 10.1016/0024-3795(84)90207-6. Read: metadata, and the
statement as quoted in Kojima et al. 2026, Lemma 2.1(i), p. 6, and in
Laurent 2009, Lemma 8.6. A partial PSD matrix with a chordal pattern has a
PSD completion iff all its specified clique blocks are PSD. Relation: this
is why R contains a dense PSD completion. Our witness's completion is
unique, with `Cov(x,z) = 1/5`, and violates `xz <= x`. Anticipates: none.

**[VandenbergheAndersen2015]** L. Vandenberghe, M. S. Andersen. Chordal graphs
and semidefinite optimization. *Found. Trends Optim.* 1(4):241–433, 2015.
DOI 10.1561/2400000006. Read: metadata only. Standard survey for chordal
decomposition and PSD completion. Cite it for background. Anticipates: none.

**[DrewJohnson1998]** J. H. Drew, C. R. Johnson. The completely positive and
doubly nonnegative completion problems. *Linear Multilinear Algebra*
44(1):85–92, 1998. DOI 10.1080/03081089808818550. Read: metadata only.
The statement is known through Kim–Kojima–Toh 2020, Lemma 2.2: every
partial CP (DNN) matrix with pattern G is CP (DNN) completable iff G is a
block-clique graph. Relation: in homogenized form our pair cliques
`{1,x,y}` and `{1,y,z}` share two indices, so the pattern is not
block-clique. CP completion, the hull-type analogue of PSD completion, is
not guaranteed. This is a conceptual precedent for N2, in the orthant/CP
setting rather than the box-graph-hull setting. Anticipates N2: partial
(conceptual).

**[KimKojimaToh2020]** S. Kim, M. Kojima, K.-C. Toh. Doubly nonnegative
relaxations are equivalent to completely positive reformulations of
quadratic optimization problems with block-clique graph structures.
*J. Global Optim.* 77(3):513–541, 2020. DOI 10.1007/s10898-020-00879-y.
arXiv 1903.07325. Read: partial (ar5iv HTML through a WebFetch summary).
DNN equals CPP for QOPs whose aggregated and correlative sparsity is a
block-clique graph. Lemma 2.2 gives the CP/DNN completion characterization.
Relation: block-clique overlaps (single nodes) are where local-to-global
works for these cones. Our overlap is `{homogenizing index, y}`.
Anticipates: partial (conceptual).

**[KojimaKimArima2026]** M. Kojima, S. Kim, N. Arima. Local-to-global
exactness of SDP relaxations for sparse QCQPs. arXiv 2606.21823, 2026.
Read: full text (KB), pp. 1–14 and 20–24.
- Clique-wise reformulation; Lemma 2.1, p. 6: PSD and rank-one chordal
  completion.
- Thm. 3.2, pp. 11–12: if every induced local sub-SDP is exact, the global
  SDP is exact.
- Sec. 3.3, pp. 12–13: when cliques share more than one node, consistency
  includes off-diagonal entries. Local rank-one solutions must then satisfy
  "nontrivial product relations". They therefore assume block-clique
  overlaps.
- p. 4: linear terms are added through a normalized diagonal entry.

Relation: with linear terms, our path homogenizes to cliques `{0,x,y}` and
`{0,y,z}`. The overlap `{0,y}` carries the off-diagonal entry `X_0y = E y`.
This is precisely the case they exclude. Their subject is rank-one SDP
exactness, not convex hulls, and they give no hull-gap instance.
Anticipates N2: partial (structural).

**[AzumaEtAl2022] / [AzumaEtAl2023]**
- G. Azuma, M. Fukuda, S. Kim, M. Yamashita. Exact SDP relaxations of
  quadratically constrained quadratic programs with forest structures.
  *J. Global Optim.* 82(2):243–262, 2022. DOI 10.1007/s10898-021-01071-6.
  Read: metadata, and the statement as given in AzumaEtAl2023, Prop. 2.4.
- Azuma et al. Exact SDP relaxations for quadratic programs with bipartite
  graph structures. *J. Global Optim.* 86(3):671–691, 2023.
  DOI 10.1007/s10898-022-01268-3. Read: KB full text, Secs. 1–3.

They give SDP exactness for homogeneous QCQPs whose aggregated sparsity
graph is a forest (with feasibility-system conditions) or bipartite.
Relation: linear terms need `x0`, which makes star objectives with linear
terms non-bipartite (triangles `x0-y-x_i`). They therefore do not cover
C-STAR. Anticipates: none.

**[BoseEtAl2015]** S. Bose, D. F. Gayme, K. M. Chandy, S. H. Low.
Quadratically constrained quadratic programs on acyclic graphs with
application to power flow. *IEEE Trans. Control Netw. Syst.* 2(3):278–287,
2015. arXiv 1203.5599. Read: abstract only. Polynomial-time SDP solution of
acyclic QCQPs under a technical condition. Optional for C-STAR related
work. Anticipates: none known.

### 3.2 Hulls of box quadratic programs, dense and sparse

**[AnstreicherBurer2010]** K. M. Anstreicher, S. Burer. Computable
representations for convex hulls of low-dimensional quadratic forms.
*Math. Program.* 124:33–43, 2010. DOI 10.1007/s10107-010-0355-9.
Read: Feb 2007 preprint (KB).
- Thm. 3: the simplex. Cor. 4, p. 5: triangles and tetrahedra (DNN).
- Thm. 6, p. 7: `QPB_2 = PSD + RLT`. p. 8: an `n = 3` box counterexample
  (−53 versus about −53.004).
- Thm. 7, p. 9: triangulated polytopes with `n <= 3`.

Relation:
- C-POLY's 2-D polygon hull and its vector projection are direct
  specializations.
- Thm. 6 is what makes each block of C-OVER's R equal to "pair SDP+RLT".
  Hence R ⊇ proj(dense SDP + all-pairs RLT) ⊇ H, and our witness shows
  that the first inclusion is strict.

Anticipates: full for the hull representations, none for the overlap
instance.

**[BurerLetchford2009]** S. Burer, A. N. Letchford. On nonconvex quadratic
programming with box constraints. *SIAM J. Optim.* 20(2):1073–1089, 2009.
DOI 10.1137/080729529. Read: author PDF (KB).
- Thm. 1: extreme points of QPB_n.
- Prop. 5: BQP_n is a projection of QPB_n.
- Thms. 4–5: which BQP facets are QPB facets.
- Prop. 10: validity of indefinite inequalities reduces recursively to
  faces with a fixed coordinate.

All results concern dense QPB_n. Relation: background for C-OVER (squares
make the continuous problem differ from BQP). Prop. 10 is a precedent for
the endpoint argument in C-STAR's nonconvex leaves. Anticipates: none.

**[Anstreicher2012]** K. M. Anstreicher. On convex relaxations for
quadratically constrained quadratic programming. *Math. Program.*
136(2):233–251, 2012. DOI 10.1007/s10107-012-0602-3. Read: Optimization
Online preprint, 28 Jul 2010.
- Thm. 1, p. 4: the convex envelope of `x^T Q x + c^T x` on the
  linear-constraint region F equals the minimum over the convex hull C of
  `(1,x)(1,x)^T`, `x ∈ F`.
- Cor. 1, p. 5: convexifying the range of the quadratic form dominates
  replacing each function by its envelope.

Relation: a direct precedent for joint (vector) quadratic convexification
over the row-constrained domain. It covers Report A's observation that
convexifying the row domain beats box hull ∩ row. Anticipates: partial
(C-SUP and C-POLY motivation).

**[AnstreicherPuges2025]** K. M. Anstreicher, D. Puges. Extended triangle
inequalities for nonconvex box-constrained quadratic programming. arXiv
2501.09150, 2025. Read: KB full text, introduction and Sec. 2. New valid
inequalities for dense QPB_3, generated from the six-simplex disjunctive
representation; the paper also gives an SOC strengthening. Relation:
dense-only background, needed to show awareness of QPB_3 work. Our cut has
no `xz` coordinate. Anticipates: none.

**[BonamiGunlukLinderoth2018]** P. Bonami, O. Günlük, J. Linderoth. Globally
solving nonconvex quadratic programming problems with box constraints via
integer programming methods. *Math. Program. Comput.* 10(3):333–382, 2018.
DOI 10.1007/s12532-018-0133-x. Read: abstract-level (IBM record).
BQP cutting planes are effective for box QP. The Chvátal–Gomory closure of
BQP is given by odd-cycle inequalities, whether or not the graph is
complete. The methods are implemented in CPLEX. Relation: the solver
baseline for sparse box QP cuts. Anticipates: none.

**[Padberg1989]** M. Padberg. The boolean quadric polytope: some
characteristics, facets and relatives. *Math. Program.* 45:139–172, 1989.
DOI 10.1007/BF01589101. Read: KB full text.
- Prop. 8, p. 161: the McCormick (linear) relaxation equals BQP^G iff G is
  acyclic.
- Thm. 10, p. 163: for series-parallel G, the nontrivial facets are
  odd-cycle inequalities.

Relation: the binary counterpart of C-OVER's "exactness of McCormick for
pure bilinear forests". The bilinear forest statement in Report B is
Padberg's Prop. 8 combined with the vertex property of multilinear
functions. The paper must attribute it. Anticipates: full for that
sub-statement.

**[DeyKhajavirad2026]** S. S. Dey, A. Khajavirad. A second-order cone
representable class of nonconvex quadratic programs. *Math. Program.*
(online 2026). DOI 10.1007/s10107-026-02364-y. arXiv 2508.18435.
Read: KB full text of the arXiv version.
- Definitions: QP(G) uses sign-oriented squares, `z_ii >= z_i^2` for plus
  loops and `z_ii <= z_i^2` for minus loops.
- Lemma 5, p. 8: minus loops decouple.
- Cor. 1, p. 9: PP(G) is decomposable when the separator is a complete
  hypergraph with no plus loop.
- Prop. 5, p. 11: perspective-RLT inequalities for a plus-loop node and
  `M ⊆ N(i)`.
- Prop. 7 and Cor. 2, pp. 13–15: with `|M| > 2` these are not implied by
  SDP+MC+Tri. For `n = 3` with one square term, SDP+MC+Tri is not an
  extended formulation.
- Thm. 1, p. 17, and Cor. 3, p. 20: an explicit hull for a complete
  (hyper)graph with exactly one plus loop.
- Thm. 2, p. 20: SOC-representable if the plus-loop nodes form a stable
  set. The proof decomposes along `N'(i)`, i.e. a star centered at a
  plus-loop node.
- Lemma 7, p. 23: each plus-loop node is placed in a single bag.
- Prop. 8, p. 25: forests with stable plus loops and logarithmic degrees.
- Sec. 6, p. 27: open questions on whether the stable-set and spread
  conditions are needed.

Relation:
- Our variant `D~` (Report A `overlap-review.md`, eq. (3)) has a plus loop
  only at `y` and no other loops. It shows that PP(path) is not decomposed
  by `{x,y}` and `{y,z}` when the separator `{y}` has a plus loop. So
  Cor. 1's hypothesis "separator without plus loops" cannot be dropped. I
  checked the lifted value 0 and the cube minimum 1/128 exactly (Section 5).
  The paper does not state this explicitly.
- Their decomposition through stars at plus-loop nodes is the structural
  reason why C-STAR's star blocks repair the pair gap.
- Their stars are box-only. Their formulations have `Θ(2^{|M|})` size.

Anticipates: N1 partial (box stars with nonpositive or absent leaf squares
have explicit hulls); N2 partial (they implicitly avoid splitting
plus-loop nodes, but give no witness).

**[Khajavirad2026]** A. Khajavirad. Tight semidefinite programming
relaxations for sparse box-constrained quadratic programs. arXiv
2601.18545v2, Feb 2026. Read: KB full text, Secs. 1–2 and theorem
statements.
- Lemma 4, p. 6: decomposability when the separator is complete and has no
  plus loops (from Dey–Khajavirad).
- Prop. 1, p. 6: extended formulations from connected components of the
  plus-loop subgraph together with their neighbors.
- Thm. 3: RLT-integrated LMIs.
- Thm. 5, p. 23: SDP-representable with `O(2^|V|)` size if there is no
  "connected plus triplet".
- Thm. 6, p. 24: polynomial size under logarithmic treewidth and
  plus-node degree.

Relation: as for Dey–Khajavirad. The full-square version of our D has a
plus loop only at `y`, so Thms. 5 and 6 apply in the box setting. Stars
with plus-loop center and at least two plus-loop leaves fall outside
Thm. 5. That is only a sufficient condition. Anticipates: N1 partial (box
only), N2 partial.

**[DelPiaKhajavirad2018]** A. Del Pia, A. Khajavirad. On decomposability of
multilinear sets. *Math. Program.* 170(2):387–415, 2018.
DOI 10.1007/s10107-017-1158-z. Read: abstract-level (KB). Necessary and
sufficient conditions for decomposing binary multilinear sets along
pairwise intersection hypergraphs. Relation: the binary version of the
decomposition question. In the binary case a single-node separator glues,
because its mean fixes its distribution. That is exactly the property our
continuous witness lacks. Anticipates: none.

**[DelPiaKhajavirad2021]** A. Del Pia, A. Khajavirad. The running intersection
relaxation of the multilinear polytope. *Math. Oper. Res.*
46(3):1008–1037, 2021. DOI 10.1287/moor.2021.1121. Read: abstract-level
(KB). Optional binary background. Anticipates: none.

**[BurerNatarajanWillemsen2025]** S. Burer, K. Natarajan, R. Willemsen. On the
semidefinite representability of continuous quadratic submodular
minimization with applications to pricing and moment problems. arXiv
2504.03996, 2025. Read: KB full text, Thm. 1, p. 12, and conclusion, p. 46.
- Thm. 1: for `n <= 3`, the relaxation SDP + `X <= x e^T` is tight for all
  submodular `(Q, c)`, i.e. `Q_ij <= 0` off the diagonal.
- p. 46: whether RLT bounds on pairs with `Q_ij = 0` can be dropped. They
  report that dropping them "preserves the optimal value in the large
  majority of instances, though not always", and leave a characterization
  open.

Relation: our D has off-diagonal coefficients −1 (`xy`), −5/4 (`yz`) and 0
(`xz`), so it is submodular with `n = 3`. By their Thm. 1, the dense
SDP+RLT-upper relaxation is exact (value 1/128). Our witness shows that
dropping the nonedge bounds `X_xz <= x, z` gives value 0. This is an
explicit rational instance of their "not always". Anticipates N2: partial
(numerical observation of the phenomenon). Strong must-cite.

**[SantanaDey2020]** A. Santana, S. S. Dey. The convex hull of a quadratic
constraint over a polytope. *SIAM J. Optim.* 30(4):2983–2997, 2020. Read:
not accessed (cited in Dey–Khajavirad, ref. [24]). Optional for C-POLY.

**[SheraliAdams1990]** H. D. Sherali, W. P. Adams. A hierarchy of relaxations
between the continuous and convex hull representations for zero-one
programming problems. *SIAM J. Discrete Math.* 3(3):411–430, 1990. Read:
not accessed (standard citation). Together with Sherali–Tuncbilek 1995
(*J. Global Optim.* 7:1–31), it is the attribution for RLT constraint-factor
products. Report A's `x^2 + 2xy + y^2 <= x + y` is
`(x+y)(1-x-y) >= 0`. Anticipates: full for that example.

### 3.3 Tree, star and forest quadratic programs

**[DelPiaKhajavirad2026tw]** A. Del Pia, A. Khajavirad. Treewidth and the
complexity of box-constrained quadratic programs. arXiv 2609.35595v1,
28 Sep 2026. Read: KB full text, Secs. 1–2.6 and the statements of Thms. 3
and 4.
- Thm. 1, p. 4: box QP with forest interaction graph and any signs is
  solved in `O(n^2)` operations, strongly polynomially. The leaf-to-root
  value functions are concave-kinked and piecewise quadratic.
- Sec. 2.5, pp. 16–17: comparison with Bhathena et al. and Kuric et al.
  Breakpoints are generally irrational (common tangents of parabolas) and
  are handled exactly by `O(1)` algebraic comparisons.
- Thm. 2, p. 18: quartic box POP on a path is strongly NP-hard.
- Thm. 3, p. 20: box QP at treewidth 2 is strongly NP-hard.
- Thm. 4, p. 27: a polynomial class through hyperplane arrangements.

Relation:
- Box-only C-STAR is a special case and fully anticipated. On a star the
  breakpoints are rational, because the leaves have no children. That is
  why C-STAR stays in rational arithmetic.
- The paper does not treat linear constraints. Center–leaf rows are
  outside its scope.
- For C-POLY's hardness statement, Thm. 3 (strong, treewidth 2) and Thm. 2
  are stronger than the MaxCut reduction. They should be cited instead of,
  or in addition to, it.

Anticipates N1: full (box), none (rows).

**[BhathenaEtAl2026]** A. Bhathena, S. Fattahi, A. Gómez, S. Küçükyavuz. A
parametric approach for solving convex quadratic optimization with
indicators over trees. *Math. Program.* 218:291–336, 2026.
DOI 10.1007/s10107-025-02222-3. arXiv 2404.08178. Read: abstract-level
(KB record) and Del Pia–Khajavirad's comparison in Sec. 2.5. An `O(n^2)`
parametric dynamic program over trees for `Q ≻ 0` with indicators.
Relation: parametric-cost dynamic programming on trees, convex case only.
Anticipates: none.

**[BienstockMunoz2018]** D. Bienstock, G. Muñoz. LP formulations for
polynomial optimization problems. *SIAM J. Optim.* 28(2):1121–1150, 2018.
DOI 10.1137/15M1054079. arXiv 1501.00288. Read: KB full text, Thm. 4, p. 2,
and Thms. 7 and 15. If the intersection graph of the constraints has
treewidth `ω`, an LP of size `O((2π/ε)^{ω+1} n log(π/ε))` solves the
problem within feasibility tolerance `Fε` and optimality tolerance
`||c||_1 ε` (variables in `[0,1]`). Relation: after the products `y x_i`
are linearized, a star QP with center–leaf rows has small treewidth. So an
epsilon-approximate polynomial-size LP already follows. C-STAR is exact and
rational. Anticipates N1: partial (approximate tractability).

**[Locatelli2015]** M. Locatelli. Convex envelopes of some quadratic
functions over the n-dimensional unit simplex. *SIAM J. Optim.*
25(1):589–621, 2015. DOI 10.1137/140976637. Read: technical report version
(KB), Sec. 5 "Convex envelope over stars". Envelopes on the unit simplex
when the underlying graph is a star with `Q_1j < 0`. Relation: prior star
convexification on a different domain (simplex) and with a different graph
notion. Anticipates: none.

**[MoreVavasis1990]** J. J. Moré, S. A. Vavasis. On the solution of concave
knapsack problems. *Math. Program.* 49:397–411, 1990.
DOI 10.1007/BF01588800. Read: abstract only. Global minimization of a
separable concave function over a box with one linear equality is NP-hard.
Local minimizers are found in `O(n log n)`. Relation: a hardness citation
for C-STAR's scope limit. One affine row coupling several leaves makes even
center-free stars hard. Anticipates: none.

**[PardalosVavasis1991]** P. M. Pardalos, S. A. Vavasis. Quadratic programming
with one negative eigenvalue is NP-hard. *J. Global Optim.* 1:15–22, 1991.
DOI 10.1007/BF00120662. Read: not accessed. Report B's
`exact-support.md` cites it. Optional for the hardness boundary.

**[BerteleBrioschi1972]** U. Bertelè, F. Brioschi. *Nonserial Dynamic
Programming.* Academic Press, 1972. Read: not accessed (classical
attribution). Nonserial dynamic programming on interaction graphs. C-STAR's
elimination of leaves conditioned on the center is an instance.

**[KhajaviradThesis2011]** A. Khajavirad. Convexification techniques for
global optimization of nonconvex nonlinear optimization problems. PhD
thesis, Carnegie Mellon University, 2011. Read: KB full text, Ch. 5,
pp. 108–112. Lagrangian decomposition with copied linking variables for
"arrowhead" (quasi-separable) problems. Relation: dualizing only `y = y'`
(and `y^2 = y'^2`) is exactly the R-type bound of C-OVER, so the overlap gap
is a Lagrangian-decomposition gap. Lane L1/L3 may hold the classical
Guignard–Kim (1987) reference. Anticipates: none.

### 3.4 Parametric quadratic programming

**[BemporadEtAl2002]** A. Bemporad, M. Morari, V. Dua, E. N. Pistikopoulos.
The explicit linear quadratic regulator for constrained systems.
*Automatica* 38(1):3–20, 2002. DOI 10.1016/S0005-1098(01)00174-1. Read:
author PDF (KB), Thm. 2, p. 6, and Thm. 4, p. 8.
- Thm. 2: for a fixed active set with independent rows, the optimizer and
  multipliers are affine on the critical region (`H ≻ 0`).
- Thm. 4: the optimizer is continuous and piecewise affine, and the value
  is convex and piecewise quadratic.

Relation: the foundation for C-STAR's positive-curvature leaves.
Anticipates: full for that ingredient.

**[TondelEtAl2003]** P. Tøndel, T. A. Johansen, A. Bemporad. An algorithm for
multi-parametric quadratic programming and explicit MPC solutions.
*Automatica* 39(3):489–497, 2003. DOI 10.1016/S0005-1098(02)00250-9.
Read: KB record only. Optional.

### 3.5 Moment spaces and Chebyshev systems

**[KarlinStudden1966]** S. Karlin, W. J. Studden. *Tchebycheff Systems: With
Applications in Analysis and Statistics.* Interscience (Wiley), 1966.

**[KreinNudelman1977]** M. G. Krein, A. A. Nudelman. *The Markov Moment
Problem and Extremal Problems.* Transl. Math. Monogr. 50, AMS, 1977.

Read: neither accessed; no theorem numbers are given here. These are the
standard references for moment spaces of Chebyshev systems and for sign
changes of measures with prescribed moments.

Relation to N2: the two separator `y`-distributions in the witness have
atoms at `0, 1/4, 5/8, 3/4` with signed differences `-1/5, +1/2, -4/5, +1/2`.
The difference measure annihilates `{1, y, y^2}` and has three sign changes.
This is the minimum possible: a polynomial of degree at most 2 with the same
sign pattern would integrate positively. This elementary fact can be proved
in one line in the paper. Cite these books only as general background, not
for a specific theorem.

### 3.6 Fixed-dimension exact support (inherited audit, not re-read)

Murty (1988/1997), *Linear Complementarity, Linear and Nonlinear
Programming*, Sec. 2.9, pp. 163–166, and Vavasis (1990), *Inf. Process.
Lett.* 36(2):73–77, were checked in Report B's audit. I did not re-read
them. Relation: C-POLY's face enumeration is classical. Lane L2 adds
Del Pia–Khajavirad's arrangement method (Thm. 4) as related fixed-rank
tractability.

## 4. Novelty assessment

### 4.1 N1 (C-STAR with center–leaf rows and all curvature signs)

- **Box case: anticipated.** Del Pia–Khajavirad 2026, Thm. 1, cover any
  signs on forests. Dey–Khajavirad 2026, Thm. 1 and Cor. 3, give explicit
  hulls for a complete graph with one plus loop, i.e. stars with plus-loop
  center and leaves without plus loops. Khajavirad 2026, Thms. 5–6, extend
  this.
- **Center–leaf affine rows: no anticipating exact algorithm found.**
  - Bienstock–Muñoz 2018, Thm. 4, gives only epsilon-approximate LPs.
  - The SDP-exactness results (Azuma et al. 2022/2023; Bose et al. 2015;
    Kojima et al. 2026) need sign or structure conditions that linear terms
    break.
  - Locatelli's stars live on the simplex.
- **Expected referee view.** The construction is a routine composition of
  nonserial DP (Bertelè–Brioschi), scalar parametric minimization
  (Bemporad et al. for convex leaves; endpoint comparison for concave
  leaves; Burer–Letchford Prop. 10 style), and a scan over a center
  interval with rational breakpoints.
- **Recommended phrasing.** "We record an exact rational support algorithm
  for quadratic stars whose affine rows each involve the center and at most
  one leaf. In the box case it specializes the forest algorithm of
  [DelPiaKhajavirad2026tw]. Rows coupling two leaves make the problem
  NP-hard even without the center [MoreVavasis1990]." Do not call this a new
  tractable class without that qualification.
- **Gain corollary.** I found no literature. It follows directly from
  compactness and independence of the leaves. Present it as an elementary
  diagnostic.

### 4.2 N2 (pair-hull obstruction and its quantification)

**What is anticipated (mechanism and phenomenon):**
- Gluing needs equal full marginals, and for finite truncations it needs
  overlap flatness or uniqueness: Vorob'ev 1962; Lasserre 2006, Lemma 6.4
  and Thm. 3.7; Fantuzzi–Fuentes 2025, Thm. 1.1 and Lemma 3.3.
- On a path with RIP, sparse relaxations can be strictly weaker than the
  joint problem. Nie–Demmel Example 3.5 is numerical and quartic.
  NQTZ Example 6.7 is exact, quartic, and on a box.
- Sparse tightness is equivalent to a decomposition with separator
  interface polynomials: NQTZ Thm. 3.1; GNS Lemma 3.
- In homogenized or CP form, overlaps of two indices obstruct
  local-to-global arguments: Kojima et al. 2026, Sec. 3.3; Drew–Johnson
  1998 and Kim–Kojima–Toh 2020 (block-clique completion).
- Separators with a plus loop are excluded from decomposition theorems:
  Dey–Khajavirad Cor. 1; Khajavirad Lemma 4.
- Dropping RLT bounds on zero-pattern pairs sometimes changes the SDP-RLT
  value: Burer–Natarajan–Willemsen, p. 46, numerically.

**What appears new (within this search):**
- A degree-2 instance on the unit-cube path `x-y-z`, with exact pair graph
  hulls including all squares (each equal to SDP+RLT by Anstreicher–Burer,
  Thm. 6).
- An explicit witness in R \ H, two-atom local measures, and the exact
  rational gap 1/128.
- The cut (2) using only existing sparse coordinates (no `xz`).
- The variant with a single shared square, which is precisely a failure of
  Dey–Khajavirad Cor. 1 when the separator carries a plus loop.
- The parametric family with gap `delta^2/2`.
- The comparison that dense SDP plus the nonedge McCormick product removes
  the witness. This matches BNW Thm. 1, since D is submodular with
  `n = 3`.
- An exact counterexample to the inference "equal overlap moment
  submatrices ⇒ consistent marginals" used in the proof of Nie–Demmel
  Thm. 3.3. Do not phrase this as refuting their theorem.

**Not new:**
- "Full-marginal gluing" (Vorob'ev; Lasserre Lemma 6.4).
- "McCormick exact for pure bilinear forests" (Padberg 1989, Prop. 8).
- Finite-support gluing by Vandermonde systems: standard, cite as folklore
  or prove inline.

**Recommended framing:** "minimal explicit degree-2 instance." By Fenchel
duality, the support of R in a direction equals the best split of the
quadratic between the two pairs when the interface `p(y)` is restricted to
`span{1, y, y^2}`. The projections of both pair hulls onto `(E y, E y^2)`
are the same full-dimensional set, so the relative-interior condition
holds. This is the degree-2 truncation of GNS Lemma 3 and NQTZ Thm. 3.1.
Under this view:
- the 1/128 gap is the cost of the quadratic interface restriction;
- NQTZ Ex. 6.7 is the opposite extreme, where no polynomial interface
  works;
- the lane computation in Section 5 suggests that in our example a cubic
  interface already recovers 0.0078124 of the 0.0078125 gap.

The duality statement is my derivation from standard convex duality. The
paper must prove it or omit it.

### 4.3 C-POLY (hull and complexity parts)

- Low-dimensional exact hulls: anticipated by Anstreicher–Burer, Thms. 3,
  6 and 7.
- Row-domain convexification dominating box hull ∩ row: Anstreicher 2012,
  Thm. 1 and Cor. 1, and RLT.
- Hardness: Del Pia–Khajavirad Thm. 3 gives a stronger and more relevant
  statement than the paper's MaxCut proposition.
- The algorithm itself is classical face enumeration (Murty).

The paper should claim only the exact rational implementation, the
degeneracy-complete enumeration argument, and replay.

## 5. Targeted checks run in this lane

All checks were single-threaded and took seconds. They used
`/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python`.
No project-wide tests were run, and CI was not inspected.

1. **Exact rational check of the plus-loop-only variant** `D~ = 2y^2 - y/2
   - xy - (5/4)yz + 1/16 + x/2 + (25/64)z`. At the witness, the lifted value
   is exactly 0. The minimum over the cube is exactly 1/128, at
   `(1, 11/16, 1)`. The pair measures give `E y = 1/2`, `E y^2 = 5/16` on
   both sides, `E xy = 3/8` and `E yz = 1/2`. This confirms that the
   witness separates the sign-oriented Dey–Khajavirad set PP(path),
   because the coefficient of `s_y` is positive and the leaves have no
   square terms.
2. **Interface-degree LP for D (grid upper estimate, not a proof).** I
   maximized `min_y(m1 - p) + min_y(m2 + p)` over polynomials `p` of degree
   `k` on a 4,001-point grid. Here `m1, m2` are the binary-leaf
   min-marginals. The results were about 1.25e-8 for `k = 2`, consistent
   with zero, and about 0.0078125 for `k >= 3`.
3. **Exact check of a rounded cubic interface.** I took
   `p = -171021/200000 y^3 + 257879/250000 y^2 - 331023/1000000 y +
   13987/1000000` and evaluated the minima at all real critical points with
   sympy. The certified bound is `0.00781244 > 0`. So sharing `E[y^3]`
   would almost close the gap for this direction. I did not determine
   whether degree 3 attains exactly 1/128.

These are lane computations, not literature facts.

## 6. Must-cite list for an expert referee

- Lasserre2006
- Vorobev1962
- WakiEtAl2006
- GrimmNetzerSchweighofer2007
- NieDemmel2009
- Laurent2009
- NieQuTangZhang2026
- FantuzziFuentes2025
- GroneEtAl1984
- VandenbergheAndersen2015
- KojimaKimArima2026
- DrewJohnson1998 or KimKojimaToh2020
- AnstreicherBurer2010
- BurerLetchford2009
- Anstreicher2012
- Padberg1989
- DeyKhajavirad2026
- Khajavirad2026
- DelPiaKhajavirad2026tw
- BurerNatarajanWillemsen2025
- BienstockMunoz2018
- BemporadEtAl2002
- Locatelli2015
- MoreVavasis1990
- BonamiGunlukLinderoth2018
- AnstreicherPuges2025

Optional:
- AzumaEtAl2022 and AzumaEtAl2023
- BoseEtAl2015
- BhathenaEtAl2026
- DelPiaKhajavirad2018 and DelPiaKhajavirad2021
- SheraliAdams1990
- SantanaDey2020
- BerteleBrioschi1972
- KarlinStudden1966 and KreinNudelman1977
- Magron–Wang, *Sparse Polynomial Optimization: Theory and Practice*,
  World Scientific, 2023 (not accessed)

## 7. Issues for the paper's text

1. The overlap section should cite NQTZ Ex. 6.7, Nie–Demmel Ex. 3.5,
   Fantuzzi–Fuentes Sec. 5.3, and Lasserre Thm. 3.7 as prior instances and
   conditions. It should then state precisely what is new: degree 2, exact
   pair hulls, rational gap, the cut, and the family.
2. The statement "exactness of McCormick for pure bilinear forests" must
   cite Padberg 1989, Prop. 8. The marginal-gluing remedy must cite
   Vorob'ev 1962 together with Lasserre 2006.
3. C-STAR's attribution paragraph should add Dey–Khajavirad 2026 (star
   hulls), Bienstock–Muñoz 2018 (approximate LP with constraints), and
   Moré–Vavasis 1990 (hardness of rows coupling several leaves).
4. The hardness proposition (MaxCut) should be accompanied by, or replaced
   with, Del Pia–Khajavirad Thm. 3 (strongly NP-hard at treewidth 2).
5. Report A's row-domain example is an RLT product. Attribute it to
   Sherali–Adams/RLT and Anstreicher 2012, Thm. 1.
6. Terminology. Dey–Khajavirad and Khajavirad use sign-oriented squares
   (QP(G)). The paper's H uses square equalities. The witness separates
   both because of D's sign pattern. Say this explicitly when comparing.
