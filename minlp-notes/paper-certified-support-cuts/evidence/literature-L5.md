# Literature lane L5: separation versus optimization, SCIP's nonlinear machinery, and how to evaluate a cut separator

Prepared 2026-10-03 for the paper "Certified support cuts for shared nonlinear
expressions and quadratic blocks". This lane covers C-SEP (candidate novelty N5)
and C-EXP. It also touches N4 and N6 where the same sources apply.

## How the sources were read

Read scope uses three labels:

- **Full text**: I read the cited passages myself, either in the local KB
  (`literature/papers/<slug>/fulltext.md`, with page markers) or in an open PDF
  downloaded during this lane.
- **Abstract**: only the abstract, the publisher record, or a search snippet.
- **Metadata**: bibliographic data only. The content statement is standard
  background and was not re-read here.

Theorem, section, and page numbers are given only where I read the passage.
Page numbers follow the pagination of the version read. That version is named
when it is a preprint.

## Main findings

1. **N5 is largely anticipated. It cannot be claimed as the first complete
   positive-tolerance separation without a full-dimensionality assumption.**
   - Grötschel, Lovász, and Schrijver's book (1988), Theorem (4.4.7), printed
     p. 117, solves weak separation from a weak optimization oracle "for every
     convex body". No outer radius, inner radius, or center is needed. The
     current draft (`sections/07-separation.tex`, lines 142-150) says the
     equivalence "assumes an explicit inner ball". That is wrong for this
     theorem. The precise limitation is different:
     - In GLS, a "convex body" is compact *and full-dimensional* (printed p. 53).
     - All weak problems refer to the eroded set S(K,-eps) (Problems
       (2.1.10)-(2.1.14), printed pp. 50-51). For a lower-dimensional hull,
       S(K,-eps) is empty, so the weak problems carry no information.
     - The almost-separating hyperplane in WSEP need only be valid on
       S(K,-delta), not on all of K.

     C-SEP differs in three ways: the returned cut is exactly valid on the
     whole set, the near-hull outcome is a distance certificate, and the set
     may be lower-dimensional.
   - **Gilbert's nearest-point algorithm already delivers the C-SEP output
     contract, with oracle counts independent of dimension.** Brierley,
     Navascués, and Vértesi (arXiv 1609.05011, 2016/2017) define WSEP as follows
     (p. 2): given r and delta, either return s in S with ||r-s|| < delta, or
     return c with c·r > max_S c·s. That is a point of S within delta, or an
     exactly valid strictly separating hyperplane. They solve it with Gilbert's
     (1966) algorithm using a linear optimization oracle for an arbitrary convex
     set S, with no full-dimensionality or inner-ball assumption. The cost is
     O(D^2/delta^2) oracle calls when the point is within delta/2, and
     O(D^4/delta^4) for the separating case (eq. (19) and the text after it,
     pp. 9-10; stopping rule in Appendix B, pp. 28-29). D is the diameter.
     By contrast, the C-SEP normal grid needs (N+1)^k directions with
     N >= 2R/(eps-delta), which is exponential in the feature dimension k.
     For k > 4 a Gilbert/Frank-Wolfe fallback over the same exact support
     oracle has a better worst-case bound.
     The C-SEP pieces map onto standard tools:
     - The exact rational support of C-POLY can serve as the oracle; with a
       rational line search the iterates stay rational.
     - A delta-approximate support oracle is covered by the inexact
       linear-subproblem analysis of Frank-Wolfe (Jaggi 2013, abstract-level).
     - The cone coordinates J only require truncating the cone at max{q_j, u_j}.
   - **The practical C-SEP loop is the local-cuts / Fenchel-cut separation
     scheme.** Chvátal, Cook, and Espinoza (2013), Section 2, pp. 173-175:
     - Separation of x* from P by column generation over oracle points. LP (5)
       normalizes ||a||_1 = 1. Its dual (6) is an L-infinity distance problem.
     - Algorithm 1 (p. 175): solve the restricted LP, call the optimization
       oracle on its dual direction, then either add the returned point or
       return the cut.
     - Their Section 5 (pp. 185-186) runs this in full rational arithmetic
       (exact LP solver) so that cuts are valid. Coefficients are capped at
       320 bits.
     - Boyd's Fenchel cutting planes (1994) are credited there as the origin.

     The C-SEP implementation (numerical LP over samples, rational convex
     combination certificate, exact support for the dual direction) is the
     same scheme with the L1/L-infinity roles swapped. The distance identity of
     Lemma `distance` is standard minimum-norm duality, and LP (5)/(6) is its
     finite-point case.
   - Bienstock, Chen, and Muñoz (2020) Theorem 3.4 gives a finite algorithm over
     the rationals. Using 1-norm cut problems and a distance oracle, it produces
     a polyhedron within eps + lambda of conv(P ∩ S) in Hausdorff distance.
     This is a different oracle and target, but the same finite, rational,
     tolerance-based completeness idea.
   - The barycentric rational domain net S_M is the image, under the vertex
     map, of the regular simplex grid used by de Klerk, Laurent, and Parrilo
     (2006). Their PTAS minimizes fixed-degree polynomials over that grid.

   **What N5 can still claim:** one stated and implemented rational contract
   for polynomial graphs over rational polytopes. Its parts are:
   - cone coordinates for inequality slack;
   - four statuses with distinct evidence requirements: `cut` needs a
     whole-domain lower bound, while `within_tolerance` needs feasible graph
     points;
   - exact feasibility of domain samples on equality-constrained (zero-volume)
     polytopes;
   - binary64 export that records whether separation survives rounding.

   It should be presented as a careful assembly of classical tools. A Gilbert
   or Frank-Wolfe completion should be cited, and preferably offered, as the
   dimension-independent alternative to the grid.

2. **SCIP's 1/128 root bound on the overlap witness comes from documented
   presolve and branching logic, not from a hull-strength relaxation.**
   - PySCIPOpt refuses a nonlinear objective and requires an epigraph
     reformulation. SCIP itself supports only linear objectives: the SCIP
     Optimization Suite 8.0 report, Section 4.2.7, pp. 29-30, says "min f(x)
     becomes min z s.t. f(x) <= z".
   - Expanded, D(x,y,z) = (y-1/4-x/2)^2 + (y-5z/8)^2 + x(1-x) + z(1-z) has
     coefficient -3/4 on x^2 and -39/64 on z^2. In the constraint D <= t, each
     of x and z:
     - appears in only one constraint;
     - has no objective coefficient and bounds [0,1];
     - enters only through a negative square plus terms of degree one in it.
   - SCIP's "Implicit Discreteness" presolve (SCIP Optimization Suite 8.0
     report, Section 4.2.7, pp. 28-29, citing Hansen, Jaumard, Ruiz, Xiong
     1993) therefore restricts x and z to {0,1} and changes their type to
     binary. The same step is described in Bestuzheva et al. (JOGO 2025),
     Section 2.2.1, pp. 8-9.
   - In the SCIP 10.0.2 source (`cons_nonlinear.c`, `presolveSingleLockedVars`)
     the step is controlled by `constraints/nonlinear/checkvarlocks`
     (default `'t'`). Its docstring reads: "presolving method to fix a variable
     x_i to one of its bounds if the variable is only contained in a single
     nonlinear constraint g(x) <= rhs (>= lhs) if g() is concave (convex) in
     x_i. If a continuous variable has bounds [0,1], then the variable type is
     changed to be binary."
   - My targeted runs (Section "Checks run") reproduce root dual 1/128 by
     default. The bound changes as follows when one component is switched off:

     | Setting | Root dual bound |
     |---|---:|
     | Default | 1/128 |
     | `checkvarlocks='d'` | about -1.16e-4 |
     | Probing presolve off | -0.079 |
     | Root propagation off | -0.032 |
     | Quadratic nonlinear handler off | -0.022 |
     | All separators off | unchanged (1/128) |

     The pilot in `experiments/pilot-native.md` also shows that disabling
     root strong branching gives -0.0559.

   So the 1/128 root bound combines the binary upgrade with probing, strong
   branching, and quadratic propagation on the two new binaries. The optimum,
   1/128, is attained at x = z = 1, y = 11/16. The paper must not present this
   bound as evidence that SCIP's LP relaxation already contains the joint hull.
   If the instance is used to illustrate native strength, set
   `checkvarlocks='d'` or alter the instance so that D is not concave in x and z.

3. **C-EXP is underpowered by community standards.** Expected practice:
   - MIPLIB 2010, Section 5.4, pp. 118-121: use permuted copies, robust
     statistics, performance profiles, and inferential statistics, and verify
     correctness on permutations.
   - SCIP 8 papers: 4 permutations, or 2 extra permuted runs.
   - SCIP 10 report: 5 seeds per MINLP instance.
   - Vigerske and Gleixner: Wilcoxon signed-rank test and the primal-dual
     integral.

   Campaign B used one seed, with seed-one repeats on 6 models. Its
   final-bound counts (better/worse) are 2/7 for `all` and 2/4 for `auto`; at
   the root they are 1/3 for `all`. A two-sided sign test gives p ≈ 0.18,
   0.69, and 0.63 respectively, so none of these differences can be told apart
   from noise. The robust finding is "no additional solves". The bound and
   timing asymmetries should be called descriptive, and the paper should cite
   the variability literature for that. The MINLPLib FAQ also says its dual
   bounds must not be used to rank solvers. Campaign B uses archived bounds only
   as conflict flags, which matches that guidance.

4. **A null or negative end-to-end result for a valid new cut family is common
   and well documented in SCIP practice.** This supports reporting C-EXP
   honestly:
   - Minor cuts hurt circle-packing instances (SCIP 8.0 report, Section 4.10,
     p. 54).
   - Intersection cuts and edge-concave cuts are disabled by default
     (Bestuzheva et al., Sections 2.3.5-2.3.6, pp. 12-13). Intersection cuts
     are still off by default in SCIP 9.0 (report, Section 3.2.2, p. 10).
   - Tighter gradient cuts are disabled (same paper, Section 2.4.2, p. 15).
   - Nonconvex perspective cuts are detrimental on hard instances (Bestuzheva,
     Gleixner, Vigerske 2023, conclusion p. 21).
   - RLT cuts for implicit products are slightly slower overall, and filtering
     hurts the hardest MINLP subset (Bestuzheva, Gleixner, Achterberg 2025,
     Section 5).
   - The flower separator lost performance on continuous products and keeps
     them disabled (SCIP 10 report, Section 3.5, pp. 18-19).
   - A PySCIPOpt SONC relaxator raised the shifted mean time from 25.29 s to
     123.04 s while improving 6 root bounds (Bestuzheva, Völker, Gleixner,
     arXiv 2304.12145, p. 18).
   - Oracle cuts tail off early (Bienstock, Chen, Muñoz, Section 6.3).
   - Local cuts are "far from conclusive" (Chvátal, Cook, Espinoza, p. 196).

## Works

### A. Separation, optimization, and oracle-based cuts

**A1. Grötschel, Lovász, Schrijver (1988).** *Geometric Algorithms and
Combinatorial Optimization*. Algorithms and Combinatorics 2, Springer, Berlin.
DOI 10.1007/978-3-642-97881-4. A second corrected edition appeared in 1993.
KB `grotschel1988-geometric-algorithms-and-combinatorial-optimization`.
- Read scope: full text of Sections 2.1 and 4.1-4.4. The KB PDF page equals
  the printed page plus 12.
- Establishes:
  - The weak problems WOPT, WVIOL, WVAL, WSEP, WMEM are defined through
    S(K,eps) and S(K,-eps) ((2.1.10)-(2.1.14), printed pp. 50-51).
  - A "convex body" is compact and full-dimensional (printed p. 53).
  - Figure 4.1 and Section 4.1 (printed pp. 102-104) summarize which
    implications need an outer radius R and which need an inner radius r and
    a center a0. The text notes that "Most of the results also hold for
    bounded convex sets, as the proofs show" (printed p. 103).
  - Theorem (4.2.2): WSEP gives WVIOL for circumscribed bodies (printed
    p. 105). Corollary (4.2.7): WSEP gives WOPT (printed p. 106).
  - Theorem (4.3.2), the Yudin-Nemirovskii result: WMEM gives WVIOL for
    centered bodies.
  - Theorem (4.4.4): WVAL gives WSEP for circumscribed bodies (printed p. 116).
    Part II of its proof lifts K to conv(K×{0} ∪ S(e_{n+1},1/2)), which is
    centered whatever the dimension of K.
  - **Theorem (4.4.7): WOPT gives WSEP in oracle-polynomial time "for every
    convex body"**, with no radius needed (printed p. 117).
  - Section 4.5 shows that the remaining assumptions cannot be weakened.
- Relation:
  - This is the definitive polynomial-time oracle equivalence, in
    log(1/eps) and the encoding length.
  - Its weak-problem semantics differ from C-SEP: the cut is valid only on
    the eroded set, and full dimension is part of the definition.
- Claims: C-SEP (N5).
- Anticipates: partial (N5). The equivalence itself is anticipated; the exact
  whole-set validity and the lower-dimensional semantics are not.

**A2. Grötschel, Lovász, Schrijver (1981).** "The ellipsoid method and its
consequences in combinatorial optimization." *Combinatorica* 1(2):169-197.
DOI 10.1007/BF02579273. Corrigendum: *Combinatorica* 4 (1984) 291-295.
- Read scope: not re-read here. The ZIB PDF is a scanned image without a text
  layer. Report B's audit inspected pp. 171-178, Theorem 3.1, and the
  inner/outer ball assumptions on p. 172.
- Establishes: polynomial equivalence of weak optimization and weak
  separation in its encoded convex-body model (Theorem 3.1, per Report B).
- Relation: the paper should cite both the 1981 paper and the book's Theorem
  (4.4.7). It should state the full-dimensional "convex body" definition and
  the eroded-set semantics, not an inner-ball requirement, as the reason the
  weak framework does not deliver C-SEP's contract.
- Claims: C-SEP (N5).
- Anticipates: partial (N5).

**A3. Karp, Papadimitriou (1982).** "On linear characterizations of
combinatorial optimization problems." *SIAM J. Comput.* 11(4):620-632. Also
FOCS 1980 and MIT LCS TM-154.
- Read scope: metadata. The journal fields are from memory; the FOCS and TM
  versions were confirmed online.
- Establishes: an independent optimization/separation equivalence, and the
  consequence that NP-hard problems have no tractable linear description
  unless NP = co-NP.
- Relation: a standard co-citation with GLS for the equivalence.
- Claims: C-SEP.
- Anticipates: none.

**A4. Bienstock, Chen, Muñoz (2020).** "Outer-product-free sets for polynomial
optimization and oracle-based cuts." *Math. Program.* 183(1-2):105-148.
DOI 10.1007/s10107-020-01484-3. arXiv 1610.04604. KB
`bienstock2020-outer-product-free-sets-for`.
- Read scope: full text of Sections 3 and 6.3, Optimization Online preprint
  pagination.
- Establishes:
  - From an oracle for the distance to a closed set S, the ball
    B(x, d(x,S)) is S-free and yields intersection cuts (Section 3.1,
    pp. 7-8).
  - The master cut problem MC is solved by Benders-style decomposition, with
    a fixed-precision adjustment lambda (pp. 8-9).
  - Theorem 3.3: the infinite-rank closure is contained in conv(P ∩ S_lambda).
  - Theorem 3.4: a finite algorithm works over the rationals with 1-norm cut
    problems and returns a polyhedron within eps + lambda of conv(P ∩ S) in
    Hausdorff distance (p. 10).
  - Computations (Section 6.3, pp. 25-29): oracle-ball and strengthened
    oracle cuts "exhibit early tailing off behaviour" and close modest gaps.
    The 2×2 + OA combination is stronger on GLOBALLib, and OA alone is
    strongest on BoxQP.
- Relation:
  - Precedent for finite, rational, tolerance-based oracle cut algorithms.
  - The oracle differs: distance to a nonconvex S versus support of F(P).
  - The target differs: a whole relaxation versus per-query separation.
  - Its tailing-off evidence parallels our weak runtime results.
- Claims: C-SEP (N5), C-EXP.
- Anticipates: partial (N5: finite rational eps-completeness of an oracle cut
  loop).

**A5. Chvátal, Cook, Espinoza (2013).** "Local cuts for mixed-integer
programming." *Math. Program. Comput.* 5(2):171-200.
DOI 10.1007/s12532-013-0052-9.
- Read scope: full text of Sections 2, 5, and 6 (open PDF via ZIB OPUS-MPC).
- Establishes:
  - Separation of x* from a rational polyhedron P = conv{g_i} + cone{r_i}
    given only an optimization oracle (Section 2, pp. 173-175).
    - LP (5) maximizes violation subject to ||a||_1 = 1. Its dual (6) is
      min s subject to x* = Σλ_i g_i + Σμ_i r_i + w with |w| ≤ s, an
      L-infinity distance.
    - Formulations (7) and (8) are the variants used in practice.
    - Algorithm 1 (p. 175) does column generation with the oracle: an
      unbounded (8) proves x* ∈ P; otherwise the oracle validates the cut or
      returns a new point or ray.
  - Credits Boyd's Fenchel cutting planes (p. 174).
  - "Precision" (Section 5, pp. 185-186): oracle or LP error can produce
    invalid cuts. They build a full rational implementation with an exact LP
    solver and accept only cuts whose coefficients fit in 320 bits.
  - Section 6: experiments on 488 MIPLIB instances (floating point) and 36
    instances (rational). The rational closed gaps are 33.5-36.1%, and the
    authors call these "far from conclusive" (p. 196).
- Relation:
  - The closest algorithmic precedent for the C-SEP practical loop (LP over
    samples, exact support of the dual direction, add the point or return the
    cut).
  - Also for exact rational validity of oracle cuts (N4, partial).
  - Differences: polyhedral and finite targets rather than nonlinear graph
    hulls; no binary64 export; no source-model replay.
- Claims: C-SEP (N5), C-SUP/N4, C-EXP.
- Anticipates: partial (N5 practical loop; N4 exact validity of oracle cuts).

**A6. Boyd (1994).** "Fenchel cutting planes for integer programs."
*Oper. Res.* 42(1):53-64. DOI 10.1287/opre.42.1.53. See also Boyd (1995),
"On the convergence of Fenchel cutting planes in mixed-integer programming,"
*SIAM J. Optim.* 5(2):421-435 (metadata from memory).
- Read scope: abstract.
- Establishes: cutting planes generated from the ability to optimize a linear
  function over the integer hull, without knowing its facets.
- Relation: the origin of separation via optimization oracles in practice.
- Claims: C-SEP.
- Anticipates: partial (oracle-based separation principle).

**A7. Applegate, Bixby, Chvátal, Cook (2001).** "TSP cuts which do not conform
to the template paradigm." In *Computational Combinatorial Optimization*,
LNCS 2241, pp. 261-303. DOI 10.1007/3-540-45586-8_7.
- Read scope: abstract.
- Establishes: local cuts via mapping to small spaces and an optimization
  oracle. Validity is safeguarded with integer representations (as described
  in A5, p. 185).
- Relation: precedent for oracle cuts with exact validity safeguards.
- Claims: C-SEP, N4.
- Anticipates: partial.

**A8. Gilbert (1966).** "An iterative procedure for computing the minimum of a
quadratic form on a convex set." *SIAM J. Control* 4(1):61-80.
DOI 10.1137/0304007.
- Read scope: metadata. The publisher page returned 403. The algorithm's use
  of a linear optimization (support) oracle and its O(1/√k) convergence are
  as described in A9.
- Establishes: the nearest-point iteration for a compact convex set using
  only its support (contact) function.
- Relation: the base of a dimension-independent eps-separation completion.
- Claims: C-SEP.
- Anticipates: partial (N5).

**A9. Brierley, Navascués, Vértesi (2016; v2 2017).** "Convex separation from
convex optimization for large-scale problems." arXiv:1609.05011. A journal
version was not found.
- Read scope: full text (arXiv v2): definitions (p. 2), Section 3 complexity
  (pp. 8-10), Appendix B (pp. 28-29).
- Establishes:
  - WSEP is defined as either s ∈ S with ||r - s|| < delta, or c with
    c·r > max_S c·s (p. 2).
  - The problem is reduced to weak minimum distance (WDIST) and solved by
    Gilbert's algorithm with a strong linear optimization oracle over an
    arbitrary convex set.
  - If d* ≤ delta/2, then k = O(D^2/delta^2) oracle calls suffice (eq. (19)).
    Otherwise a witness is found after O(D^4/delta^4) calls (p. 9-10).
  - Any iterate with d_k·d'_k > 0 certifies r ∉ S (Appendix B).
  - The call count does not depend on the dimension n.
- Relation:
  - **Anticipates the C-SEP answer contract** (point within tolerance, or
    exactly valid strict cut).
  - Needs no full dimension or inner ball.
  - Has a better worst-case oracle count than the C-SEP grid when k > 4.
  - Works in Euclidean rather than L1 norm, and in floating point rather than
    rational arithmetic.
  - Has no cone coordinates and no domain-net analysis for approximate
    support.
- Claims: C-SEP (N5).
- Anticipates: largely anticipates the mathematical core of N5. It does not
  anticipate the rational, implemented contract for polynomial graphs with
  cone slack and exact domain feasibility.

**A10. Ioannou, Travaglione, Cheung (2006).** "Convex separation from
optimization via heuristics." arXiv:cs/0603089.
- Read scope: abstract.
- Establishes: a polynomial-time Turing reduction from weak separation to weak
  optimization for full-dimensional convex sets, using analytic centers.
- Relation: an intermediate reference between GLS and A9.
- Claims: C-SEP.
- Anticipates: none beyond A1.

**A11. Frank, Wolfe (1956).** "An algorithm for quadratic programming."
*Naval Res. Logist. Q.* 3(1-2):95-110. DOI 10.1002/nav.3800030109.
- Read scope: metadata.
- Relation: the conditional-gradient method. Applied to min ||z - q||^2 over
  conv F(P) with an exact support oracle, its duality gap gives a
  within-tolerance point or a separating direction.
- Claims: C-SEP.
- Anticipates: partial.

**A12. Jaggi (2013).** "Revisiting Frank-Wolfe: projection-free sparse convex
optimization." *Proc. 30th ICML*, PMLR 28(1):427-435.
- Read scope: abstract.
- Establishes: duality-gap certificates and primal-dual convergence that
  remain valid with approximately solved linear subproblems.
- Relation: covers the delta-approximate support case of C-SEP (polynomial
  graphs).
- Claims: C-SEP.
- Anticipates: partial.

**A13. Wolfe (1976).** "Finding the nearest point in a polytope." *Math.
Program.* 11:128-149. DOI 10.1007/BF01580381. Also **Gilbert, Johnson, Keerthi
(1988)**, "A fast procedure for computing the distance between complex objects
in three-dimensional space," *IEEE J. Robot. Autom.* 4(2):193-203,
DOI 10.1109/56.2083.
- Read scope: metadata.
- Relation: finite-point and support-mapping nearest-point algorithms that
  decide separation or eps-proximity. GJK is the standard engineering form.
- Claims: C-SEP.
- Anticipates: partial.

**A14. Kalantari (2015).** "A characterization theorem and an algorithm for a
convex hull problem." *Ann. Oper. Res.* 226(1):301-349.
DOI 10.1007/s10479-014-1707-2. arXiv 1204.1873.
- Read scope: abstract.
- Establishes: the Triangle Algorithm and distance duality for membership of p
  in conv(S) of a finite set. It returns an eps-approximate point or a
  separating hyperplane, in O(mn ln(1/eps))-type bounds per the abstract.
- Relation: the same dichotomy for finite point sets.
- Claims: C-SEP.
- Anticipates: partial.

**A15. Lee, Sidford, Vempala (2018).** "Efficient convex optimization with
membership oracles." *Proc. COLT 2018*, PMLR 75:1292-1294. arXiv 1706.07357.
- Read scope: abstract.
- Establishes: optimization with Õ(n^2) membership and evaluation calls, and
  faster reductions among the five GLS oracles.
- Relation: modern oracle-complexity context; the bodies are assumed
  well-bounded.
- Claims: C-SEP.
- Anticipates: none.

**A16. Kelley (1960).** "The cutting-plane method for solving convex
programs." *J. SIAM* 8(4):703-712. DOI 10.1137/0108053. Also **Cheney,
Goldstein (1959)**, "Newton's method for convex programming and Tchebycheff
approximation," *Numer. Math.* 1:253-268.
- Read scope: metadata.
- Relation: the C-SUP/C-AGG solver loop (choose a direction, add a supporting
  cut, re-solve) is a Kelley-type outer approximation in the lifted space.
- Claims: C-SEP, C-EXP.
- Anticipates: none.

**A17. Drori, Teboulle (2016).** "An optimal variant of Kelley's cutting-plane
method." *Math. Program.* 160(1-2):321-351. DOI 10.1007/s10107-016-0985-7.
arXiv 1409.2636.
- Read scope: full text of the Introduction (arXiv v2, p. 1).
- Establishes: per the authors, "the Kelley method suffers from very poor
  performance, both in practice and in theory". They cite Nemirovsky and
  Yudin, *Problem Complexity and Method Efficiency in Optimization*, Wiley
  1983, and attribute the cause to unstable subproblem solutions.
- Relation: the citable statement of Kelley's poor worst-case complexity. It
  explains tailing off in unregularized cut loops.
- Unverified: Nesterov, *Introductory Lectures on Convex Optimization*
  (Kluwer/Springer 2004), may contain a Kelley lower-bound example in a
  section titled "Kelley method"; its location was not verified.
- Claims: C-EXP, C-SEP.
- Anticipates: none.

**A18. de Klerk, Laurent, Parrilo (2006).** "A PTAS for the minimization of
polynomials of fixed degree over the simplex." *Theor. Comput. Sci.*
361(2-3):210-225.
- Read scope: abstract and snippet.
- Establishes: minimizing a fixed-degree polynomial over the regular grid
  Δ(n,r) = {x ∈ Δ : rx ∈ Z^n} gives a PTAS with explicit error bounds. This
  extends Bomze and de Klerk (2002) for quadratics.
- Relation: S_M in C-SEP's Lemma `domain-net` is the image of Δ(s,M) under
  the vertex map. That is a known approximation device; C-SEP's Lipschitz
  error bound is cruder than the degree-based bounds here.
- Claims: C-SEP (N5).
- Anticipates: partial (domain net).

**A19. Chen, Luedtke (2022).** "On generating Lagrangian cuts for two-stage
stochastic integer programs." *INFORMS J. Comput.* 34(4):2332-2349.
DOI 10.1287/ijoc.2022.1185. KB `chen2022-on-generating-lagrangian-cuts-for`.
- Read scope: KB summary only.
- Establishes: normalized separation of Lagrangian cuts through an MIP
  optimization oracle, with delta-relative stopping.
- Relation: modern oracle separation with an explicit tolerance contract.
- Claims: C-SEP.
- Anticipates: none.

**A20. Lodi, Tanneau, Vielma (2023).** "Disjunctive cuts in mixed-integer
conic optimization." *Math. Program.* DOI 10.1007/s10107-022-01844-1.
arXiv 1912.03166. KB `lodi2023-disjunctive-cuts-in-mixed-integer`.
- Read scope: KB summary only.
- Establishes: normalization choices for cut-generating conic programs and
  their dual distance interpretations, including ill-posed cases.
- Relation: background for the C-SEP choice of L1 distance and
  L-infinity-normalized normals.
- Claims: C-SEP.
- Anticipates: none.

### B. SCIP's nonlinear relaxation machinery

**B1. Bestuzheva, Chmiela, Müller, Serrano, Vigerske, Wegscheider (2025).**
"Global optimization of mixed-integer nonlinear programs with SCIP 8." *J.
Global Optim.* 91(2):287-310. DOI 10.1007/s10898-023-01345-1. arXiv 2301.00587.
KB `bestuzheva2025-global-optimization-of-mixed-integer`.
- Read scope: full text of Sections 2-4 (arXiv v1 pagination).
- Establishes:
  - Section 2.1.2 (pp. 5-7): the extended formulation is attached as
    annotations, and feasibility is checked on the original constraints.
  - Section 2.1.3 (pp. 7-8): nonlinear handlers.
  - Section 2.2.1 (pp. 8-9): a bounded variable that appears in exactly one
    constraint, convex (concave) in it with the matching infinite side,
    becomes binary or gets a bound disjunction, after Hansen et al.
  - Section 2.2.3: the KKT presolver is disabled.
  - Section 2.3.1: quadratic propagation.
  - Section 2.3.2: bilinear terms with LP-projected inequalities (Locatelli;
    Müller et al.).
  - Sections 2.3.3-2.3.4: RLT cuts and 2×2 minor SDP cuts.
  - Section 2.3.5 (p. 12): intersection cuts, "currently disabled by default".
  - Section 2.3.6 (p. 13): edge-concave cuts, disabled.
  - Section 2.4.2 (p. 15): tighter gradient cuts, disabled.
  - Section 3 (pp. 19-24): 200 MINLPLib instances × 5 (4 permutations,
    "Since small changes to an instance can lead to large variations in the
    solver's performance"); correctness via GAMS/Examiner and conflicts with
    MINLPLib bounds; shifted geometric mean with shift 1 s; Dolan-Moré
    profiles.
  - Section 4: many nonlinear features are disabled by default and need
    tuning.
- Relation: the native baseline and its methodology. It is the documented
  source for the root-bound mechanism (Main finding 2) and for disabled cut
  families (Main finding 4).
- Claims: C-EXP, C-IMPL, C-OVER (computational illustration).
- Anticipates: none.

**B2. Bestuzheva, Besançon, Chen, Chmiela, Donkiewicz, van Doornmalen, Eifler,
Gaul, Gamrath, Gleixner, Gottwald, Graczyk, Halbig, Hoen, Hojny, van der Hulst,
Koch, Lübbecke, Maher, Matter, Mühmer, Müller, Pfetsch, Rehfeldt, Schlein,
Schlösser, Serrano, Shinano, Sofranac, Turner, Vigerske, Wegscheider, Wellner,
Weninger, Witzig (2021).** "The SCIP Optimization Suite 8.0." ZIB-Report 21-41,
arXiv:2112.08872. The short version is "Enabling research through the SCIP
Optimization Suite 8.0," *ACM Trans. Math. Softw.* 49(2), 2023 (metadata).
- Read scope: full text of Sections 4.2.7, 4.10, and 4.14 (arXiv v1).
- Establishes:
  - Section 4.2.7 "Implicit Discreteness" (pp. 28-29): non-binary variable,
    finite bounds, zero objective coefficient, in only one constraint;
    polynomial with x only in c_k x^{2k} monomials of equal sign or in
    monomials linear in x; matching infinite side. Then x ∈ {lb, ub}, and the
    type becomes binary for [0,1] bounds. The report says this "has been shown
    to be particularly effective for box-QP instances".
  - Same section (pp. 29-30): "Since SCIP supports linear objective functions
    only, problems with a nonlinear objective function are reformulated ...
    (min f(x) becomes min z s.t. f(x) <= z)".
  - Section 4.10 (p. 54): sepa_minor uses 2×2 principal minors. For circle
    packing, "the minor cuts are not really helpful" and "SCIP's overall
    performance was negatively affected".
  - Section 4.11: rank-1 intersection cuts (sepa_interminor).
  - Section 4.14 (p. 59): classic versus new nonlinear handling on 1678
    MINLPLib instances with two extra permuted runs each. The report notes
    "MINLPLib is not designed to be benchmark set".
- Relation: the authoritative documentation for the 1/128 root-bound
  mechanism and the objective epigraph, plus a precedent for negative cut
  results.
- Claims: C-EXP, C-IMPL, C-OVER.
- Anticipates: none.

**B3. Bolusani, Besançon, Bestuzheva, Chmiela, Dionísio, Donkiewicz, van
Doornmalen, Eifler, Ghannam, Gleixner, Graczyk, Halbig, Hedtke, Hoen, Hojny,
van der Hulst, Kamp, Koch, Kofler, Lentz, Manns, Mexi, Mühmer, Pfetsch,
Schlösser, Serrano, Shinano, Turner, Vigerske, Weninger, Xu (2024).** "The SCIP
Optimization Suite 9.0." ZIB-Report 24-02-29, arXiv:2402.17702.
- Read scope: full text of Sections 2.3 and 3.2.2 (arXiv v2).
- Establishes:
  - Section 2.3 (p. 5): MINLP gains over SCIP 8, mainly on nonconvex
    instances.
  - Section 3.2.2 (p. 10): quadratic intersection cuts remain disabled by
    default (`nlhdlr/quadratic/useintersectioncuts`), and monoidal
    strengthening was added for integer variables.
- Relation: baseline version context and disabled-cut precedent.
- Claims: C-EXP.
- Anticipates: none.

**B4. Hojny, Besançon, Bestuzheva, Borst, Dionísio, Ehls, Eifler, Ghannam,
Gleixner, Göß, Hoen, von Holly-Ponientzietz, van der Hulst, Kamp, Koch, Kofler,
Lentz, Lübbecke, Maher, Meinhold, Mexi, Mohr, Mühmer, Patel, Pfetsch, Reinartz
Groba, Serrano, Shinano, Turner, Vigerske, Walter, Weninger, Xu (2025).** "The
SCIP Optimization Suite 10.0." arXiv:2511.18580. KB
`hojny2025-the-scip-optimization-suite-10`.
- Read scope: full text of Sections 2.1, 2.3, 3.1.8, 3.5, and 10.1.
- Establishes:
  - Section 2.1 (p. 4): 169 MINLPLib instances × 5 seeds; subsets "affected",
    [t,T], and both-solved; shifted geometric means.
  - Section 3.1.8 (p. 10): VIPR certificates for exact MILP.
  - Section 3.5 (pp. 18-19): sepa_flower; handling continuous products
    showed "a performance loss, which is why this is disabled by default".
  - Section 10.1 (pp. 35-36): PySCIPOpt recipes include "requiring an
    epigraph reformulation to add a nonlinear objective".
- Relation: the version used by campaign B (SCIP 10.0.2 with PySCIPOpt 6.2.1,
  per `experiments/campaign-v2/environment.json` and run records). It sets the
  seed-based methodology expectation and offers exact MILP certification as a
  contrast for N4.
- Claims: C-EXP, C-IMPL, N4.
- Anticipates: none.

**B5. Vigerske, Gleixner (2018).** "SCIP: global optimization of
mixed-integer nonlinear programs in a branch-and-cut framework." *Optim.
Methods Softw.* 33(3):563-593. DOI 10.1080/10556788.2017.1335312. The volume
and pages are from memory; the KB records only the DOI. KB
`vigerske2017-scip-global-optimization-of-mixed`.
- Read scope: full text of Sections 2-4 (Optimization Online/ZIB version;
  Section 3.2 on printed pp. 17-18).
- Establishes:
  - Section 3.1: component-impact study on 475 MINLPLib2 instances.
  - Section 3.2: subsets ("solved+≥100s", "diff", ...); primal-dual integral;
    shifted geometric means (shift 1 s for time, 100 for nodes). It defines
    performance variability, says it "looms even larger on mixed-integer
    nonlinear programs", and uses the Wilcoxon signed-rank test with the
    Pratt zero treatment.
  - Section 3.5.2: outer approximation separation has a large impact.
- Relation: the methodological template for evaluating a separator inside
  SCIP.
- Claims: C-EXP.
- Anticipates: none.

**B6. Müller, Serrano, Gleixner (2020).** "Using two-dimensional projections
for stronger separation and propagation of bilinear terms." *SIAM J. Optim.*
30(2):1339-1365. DOI 10.1137/19M1249825. arXiv 1903.05521.
- Read scope: abstract, plus the description in B1, Section 2.3.2.
- Establishes:
  - Valid inequalities for the projection onto (x, y), obtained by
    OBBT-like LPs.
  - Locatelli's envelopes over the projected polytope, and best bounds for
    x, y, and xy.
  - Significant performance gains on MINLPLib in SCIP.
- Relation: native SCIP already exploits row-coupled two-dimensional domains
  for single products. C-POLY and C-AGG must be compared against this, not
  against box McCormick.
- Claims: C-POLY, C-EXP.
- Anticipates: partial (row-domain strengthening for single bilinear terms).

**B7. Bestuzheva, Gleixner, Achterberg (2025).** "Efficient separation of RLT
cuts for implicit and explicit bilinear terms." *Math. Program.*
210(1-2):47-74. DOI 10.1007/s10107-024-02104-0. arXiv 2211.13545. IPCO 2023
version: LNCS 13904. KB `bestuzheva2025-efficient-separation-of-rlt-cuts`.
- Read scope: full text of Section 5 (arXiv pagination).
- Establishes:
  - Section 5.1: 1357 MINLP and 195 MILP instances; MILP runs use 4
    permutations (Table A1); results on "clean" instances only.
  - Section 5.2: explicit RLT is clearly beneficial; implicit products are
    instance-dependent and slightly slower overall.
  - Section 5.3: row marking cuts separation time.
  - Section 5.4: redundancy filtering slows the [1000, timelimit] MINLP
    subset by 10%.
  - Appendix A: per-instance tables showing performance variability.
- Relation: the native RLT baseline, and a template for reporting a separator
  with "affected" subsets.
- Claims: C-EXP, C-POLY (RLT may already capture row-domain products; see
  issue POLY-8).
- Anticipates: none.

**B8. Bestuzheva, Gleixner, Vigerske (2023).** "A computational study of
perspective cuts." *Math. Program. Comput.* 15(4):703-731. KB
`bestuzheva2023-a-computational-study-of-perspective`.
- Read scope: full text of Sections 5-6 (arXiv v1).
- Establishes:
  - p. 15: 186 instances × 5 (4 permutations) "to robustify our results
    against the effects of performance variability", citing Lodi and
    Tramontani.
  - Conclusion p. 21: convex perspective cuts give >20% gains. Nonconvex ones
    "can be detrimental to performance on challenging instances and can lead
    to an increased amount of numerical issues", yet reduce nodes by 5% and
    improve root bounds.
- Relation: the closest precedent for a mixed or negative result for a valid
  new nonconvex cut family in SCIP.
- Claims: C-EXP.
- Anticipates: none.

**B9. Chmiela, Muñoz, Serrano (2023).** "On the implementation and
strengthening of intersection cuts for QCQPs." *Math. Program.*
197(2):549-586. DOI 10.1007/s10107-022-01808-5. IPCO 2021: LNCS 12707,
pp. 134-147. Also **Muñoz, Serrano (2020)**, "Maximal quadratic-free sets,"
IPCO 2020, LNCS 12125, pp. 307-321, DOI 10.1007/978-3-030-45771-6_24; and
**Chmiela, Muñoz, Serrano**, "Monoidal strengthening and unique lifting in
MIQCPs" (IPCO 2023 / preprint; metadata not verified).
- Read scope: abstract, plus B1 Section 2.3.5 and B3 Section 3.2.2.
- Establishes: closed-form intersection cuts from maximal quadratic-free sets
  and Glover-style strengthening, implemented in SCIP's quadratic nonlinear
  handler. Off by default in SCIP 8, 9, and 10 (`useintersectioncuts=False`
  observed in the PySCIPOpt parameter list).
- Relation: the native nonconvex quadratic cut family absent from default
  runs. Any comparison should state that default SCIP does not use it.
- Claims: C-EXP, C-POLY.
- Anticipates: none.

**B10. Achterberg (2009).** "SCIP: solving constraint integer programs."
*Math. Program. Comput.* 1(1):1-41. DOI 10.1007/s12532-008-0001-1.
- Read scope: metadata (from the A5 reference list).
- Relation: the framework citation.
- Claims: C-IMPL, C-EXP.
- Anticipates: none.

**B11. Hansen, Jaumard, Ruiz, Xiong (1993).** "Global minimization of
indefinite quadratic functions subject to box constraints." *Naval Res.
Logist.* 40(3):373-392. DOI 10.1002/1520-6750(199304)40:3<373::AID-NAV3220400307>3.0.CO;2-A.
- Read scope: metadata (from B1 and B2).
- Relation: the source of SCIP's implicit-discreteness reduction behind the
  1/128 root bound.
- Claims: C-OVER (illustration), C-EXP.
- Anticipates: none.

**B12. Bestuzheva, Völker, Gleixner (2023).** "Strengthening SONC relaxations
with constraints derived from variable bounds." arXiv:2304.12145. KB
`gleixner2023-strengthening-sonc-relaxations-with-constraints`.
- Read scope: KB full text of pp. 14 and 18.
- Establishes: a PySCIPOpt relaxator inside SCIP. "SCIP handles nonlinear
  objective functions by reformulating ... into a constraint" (p. 14). The
  shifted mean time rose from 25.29 s to 123.04 s, and root bounds improved
  on 6 instances (p. 18).
- Relation: a PySCIPOpt-based plug-in with valid strength but a negative
  runtime result, the same pattern as C-EXP.
- Claims: C-EXP.
- Anticipates: none.

### C. Test sets and computational methodology

**C1. Bussieck, Drud, Meeraus (2003).** "MINLPLib—a collection of test models
for mixed-integer nonlinear programming." *INFORMS J. Comput.* 15(1):114-119.
DOI 10.1287/ijoc.15.1.114.15159. KB
`bussieck2003-minlpliba-collection-of-test-models`.
- Read scope: KB summary.
- Relation: the test-set citation.
- Claims: C-EXP.
- Anticipates: none.

**C2. Vigerske, MINLPLib web site** (https://www.minlplib.org, snapshot
2026-07-29, git 168bf3d2). KB `vigerske2026-minlplib-a-library-of-mixed`.
- Read scope: KB snapshot.
- Establishes: the FAQ says reported points and dual bounds "must not be
  used to rank solver performance". It also documents the objective-variable
  convention.
- Relation: supports C-EXP's use of archived bounds only as conflict flags.
  The paper should cite the snapshot or version used.
- Claims: C-EXP.
- Anticipates: none.

**C3. Koch, Achterberg, Andersen, Bastert, Berthold, Bixby, Danna, Gamrath,
Gleixner, Heinz, Lodi, Mittelmann, Ralphs, Salvagnin, Steffy, Wolter (2011).**
"MIPLIB 2010." *Math. Program. Comput.* 3(2):103-163.
DOI 10.1007/s12532-011-0025-9.
- Read scope: full text of Sections 3 and 5 (open PDF).
- Establishes:
  - Section 3 (p. 110 ff.): a solution checker using exact arithmetic.
  - Section 5 (p. 115): defines performance variability.
  - Section 5.4 (pp. 118-121): use permutations; averages and geometric
    means "give limited insights"; prefer robust indicators, performance
    profiles, and inferential statistics; "verify this [correctness] on
    several permutations".
  - Fig. 3: solution times over 100 permutations.
- Relation: the standard methodological citation for C-EXP's
  single-seed limitation.
- Claims: C-EXP.
- Anticipates: none.

**C4. Gleixner, Hendel, Gamrath, Achterberg, Bastubbe, Berthold, Christophel,
Jarck, Koch, Linderoth, Lübbecke, Mittelmann, Ozyurt, Ralphs, Salvagnin,
Shinano (2021).** "MIPLIB 2017: data-driven compilation of the 6th
mixed-integer programming library." *Math. Program. Comput.* 13(3):443-490.
DOI 10.1007/s12532-020-00194-3.
- Read scope: full text of Sections 4.7, 5.1, and 5.6 (open PDF).
- Establishes:
  - Section 4.7 (p. 464): independent verification of reported solutions
    against the original model with GMP arbitrary precision. It checks
    feasibility only, "it cannot check optimality".
  - Section 5.1 (p. 467): benchmark-suitability criteria, including
    consistent results.
  - Section 5.6 (p. 478): "performance variability and parallel scalability
    were not captured".
- Relation: precedent for C-EXP's independent original-model evaluator and
  for honest scoping of benchmark limits.
- Claims: C-EXP (N6 partially: checking against the source model).
- Anticipates: none.

**C5. Lodi, Tramontani (2013).** "Performance variability in mixed-integer
programming." In *Theory Driven by Influential Applications*, INFORMS
TutORials in Operations Research, pp. 1-12. DOI 10.1287/educ.2013.0112.
- Read scope: abstract and publisher record. The page range comes from the B8
  reference list.
- Establishes: the roots of variability (platform, row/column permutation,
  neutral changes), misinterpretations from improper benchmark analysis, and
  ways to exploit it.
- Relation: must be cited for C-EXP's single-seed design.
- Claims: C-EXP.
- Anticipates: none.

**C6. Danna (2008).** "Performance variability in mixed integer programming."
Talk, Workshop on Mixed Integer Programming 2008, Columbia University.
- Read scope: metadata (cited in B5 and C3).
- Relation: the origin of the term.
- Claims: C-EXP.
- Anticipates: none.

**C7. Dolan, Moré (2002).** "Benchmarking optimization software with
performance profiles." *Math. Program.* 91(2):201-213.
DOI 10.1007/s101070100263. arXiv cs/0102001. KB
`dolan2002-benchmarking-optimization-software-with-performance`.
- Read scope: KB summary, Sections 2-4.
- Establishes: performance ratios and profiles that keep failures. A single
  problem moves a profile by at most 1/n_p.
- Relation: optional for C-EXP. With 30 models, three modes, and equal solve
  counts, a profile adds little. Cite it if timing is plotted.
- Claims: C-EXP.
- Anticipates: none.

**C8. Bussieck, Dirkse, Vigerske (2014).** "PAVER 2.0: an open source
environment for automated performance analysis of benchmarking data." *J.
Global Optim.* 59(2-3):259-275 (volume and pages from memory).
DOI 10.1007/s10898-013-0131-5. KB `bussieck2014-paver-2-0-an-open`.
- Read scope: KB summary, pp. 4-17.
- Establishes:
  - Failure imputation and filters can change rankings.
  - Examiner checks the original model; solver stopping tests act on the
    presolved and scaled model.
- Relation: supports separating the "solved" definition from the solver
  status, as C-EXP does.
- Claims: C-EXP.
- Anticipates: none.

**C9. Berthold (2013).** "Measuring the impact of primal heuristics." *Oper.
Res. Lett.* 41(6):611-614. DOI 10.1016/j.orl.2013.08.007.
- Read scope: metadata (via B5).
- Relation: the primal(-dual) integral, an alternative to solved counts for
  short time limits.
- Claims: C-EXP.
- Anticipates: none.

**C10. Margot (2009).** "Testing cut generators for mixed-integer linear
programming." *Math. Program. Comput.* 1(1):69-95.
DOI 10.1007/s12532-009-0003-7 (DOI from memory; the metadata were confirmed
online).
- Read scope: abstract.
- Establishes: a methodology for testing the *accuracy* (validity failures
  recorded during random dives toward known feasible solutions) and the
  *strength* (statistical comparison) of cut generators.
- Relation: the standard reference for evaluating a cut separator's
  validity. C-EXP's replay of 165 cuts against the source model and stored
  SCIP rows is a stronger, exact form of the accuracy test. Cite it and
  contrast.
- Claims: C-EXP, N4.
- Anticipates: partial (validity testing of cut generators).

**C11. Dey, Molinaro (2018).** "Theoretical challenges towards cutting-plane
selection." *Math. Program.* 170(1):237-266. DOI 10.1007/s10107-018-1302-4.
arXiv 1805.02782.
- Read scope: abstract.
- Establishes: a review of cut strength, selection issues, and the gap
  between theoretical strength and solver benefit.
- Relation: supports the C-EXP and frontier statement that a valid or
  stronger cut oracle need not reduce runtime.
- Claims: C-EXP.
- Anticipates: none.

**C12. Wilcoxon (1945).** "Individual comparisons by ranking methods."
*Biometrics Bull.* 1(6):80-83. Optional: **Fischetti, Monaci (2014)**,
"Exploiting erraticism in search," *Oper. Res.* 62(1):114-122 (metadata from
memory; verify before citing).
- Read scope: metadata.
- Relation: the statistical tests used in SCIP practice, and erraticism as a
  resource.
- Claims: C-EXP.
- Anticipates: none.

## Novelty assessment for this lane

| Claim | Verdict | Evidence |
|---|---|---|
| N5: finite complete positive-tolerance separation (cut or within-tolerance) for polynomial graphs over polytopes, without full-dimensionality | **Largely anticipated in substance.** Novel only as a specific exact-rational, implemented contract. | A9 gives the same two-outcome contract from a linear optimization oracle on arbitrary convex sets, without full dimension, with dimension-independent O(D^2/δ^2) and O(D^4/δ^4) oracle bounds. A1 Thm (4.4.7) needs no radius for WOPT to WSEP, but works on full-dimensional bodies with eroded-set semantics. A5 gives the column-generation loop with L1 normalization, its L-infinity distance dual, and exact rational arithmetic. A4 Thm 3.4 gives finite rational eps-completeness of an oracle cut scheme. A18 gives the barycentric domain net. |
| N5 sub-claim: the draft says "GLS assumes an explicit inner ball" | **Inaccurate as written.** | A1 Thm (4.4.7), printed p. 117: "for every convex body given by a weak optimization oracle". The correct difference: GLS convex bodies are full-dimensional by definition (printed p. 53), and WSEP cuts need only be valid on S(K,-δ) (printed p. 51). |
| C-SEP practical loop (numerical LP over samples, exact support of the dual direction, rational convex-combination certificate) | **Anticipated** (local cuts and Fenchel cuts). | A5 Algorithm 1 (p. 175), A6, A7. |
| C-EXP null result (no additional solves; native SCIP recommended) | **Consistent with precedent; not a novelty issue.** Must be framed with the variability literature. | B1 Sections 2.3.5-2.4.2, B2 Section 4.10, B3 Section 3.2.2, B4 Section 3.5, B7 Sections 5.2/5.4, B8 p. 21, B12 p. 18, A4 Section 6.3, A5 p. 196, C3 Section 5.4, C5. |
| C-EXP design (single seed, 30 models) | **Below current SCIP practice.** The "worse bound" counts are not significant. | B1 (4 permutations), B2 Section 4.14 (2 permutations), B4 Section 2.1 (5 seeds), B5 Section 3.2 (Wilcoxon). Sign tests: 2 vs 7 gives p ≈ 0.18; 2 vs 4 gives p ≈ 0.69; 1 vs 3 gives p ≈ 0.63. |
| N4 (numerical direction plus exact certificate of the exported row), as seen from this lane | **Partially anticipated.** | A5 Section 5 and A7 (rational and integer validity of oracle cuts); B4 Section 3.1.8 (VIPR for exact MILP); C10 (validity testing). Other lanes cover Cook et al. 2009 and Eifler-Gleixner 2024. |
| N6 (source-faithful import with exact domain witnesses), as seen from this lane | **Not anticipated by these sources.** They only partially cover checking returned points against the source model. | C3 Section 3 and C4 Section 4.7 (GMP checker against the original MPS); C8 Examiner; B1 Section 2.1.3 (feasibility on original constraints). None covers domain witnesses or replay of expression DAGs. |

## Suggested corrections to the current draft (for the section owners)

The lane does not edit section files. These are recommendations:

1. `sections/07-separation.tex`, paragraph "Relation to the ellipsoid method"
   (lines 141-150). Replace "That equivalence assumes an explicit inner ball,
   hence a full-dimensional body" with wording close to this:
   "In the oracle framework of [GLS 1988], weak separation is obtainable from
   weak optimization for every convex body [Thm. (4.4.7)], but convex bodies
   are full-dimensional by definition and the weak problems only constrain
   behaviour on the eroded set S(K,−ε), so a returned hyperplane need not be
   valid on K and lower-dimensional hulls are degenerate inputs."
   Then add:
   "Gilbert's nearest-point algorithm with a linear optimization oracle
   [Gilbert 1966; Brierley, Navascués, Vértesi 2016] already returns either a
   point of the set within δ or an exactly valid strictly separating
   hyperplane, without full-dimensionality and with a number of oracle calls
   independent of the dimension; our finite grid is an elementary alternative
   whose cost is exponential in k, and the exact support of Section 5 can be
   used as its oracle."
   Also cite [Chvátal, Cook, Espinoza 2013, Sect. 2] for the implemented LP
   column-generation loop.
2. Consider either replacing the normal grid in complete mode with a
   Gilbert/Frank-Wolfe iteration, or stating its worst-case comparison
   explicitly. The rational Gilbert step with exact support keeps all
   certificates rational, and the existing `within_tolerance` certificate
   format (a rational convex combination) already fits.
3. If the C-OVER instance D(x,y,z) is used to discuss native SCIP, state the
   documented mechanism: implicit discreteness [SCIP Opt. Suite 8.0 report,
   Section 4.2.7; Bestuzheva et al. 2025, Section 2.2.1; Hansen et al. 1993]
   turns x and z into binaries, and root probing and strong branching then
   reach 1/128. Report the root bound with
   `constraints/nonlinear/checkvarlocks = d` as the relaxation-only
   comparator.
4. In C-EXP, cite C3 Section 5.4, C5, and B5 Section 3.2. State that a single
   seed per job and 30 models cannot resolve small timing or bound effects.
   Present the bound "better/worse" counts as descriptive (include the
   sign-test values or equivalent wording).

## Checks run (targeted, single-threaded, each well under a minute)

- KB reads: `grep` over `literature/index.md` and `papers/*/fulltext.md`;
  `sed` reads of the passages cited above.
- Downloaded open PDFs to `/tmp` and extracted text with `pdftotext`:
  - Chvátal-Cook-Espinoza 2013 (OPUS-MPC);
  - MIPLIB 2010 (OPUS-MPC);
  - MIPLIB 2017 (RWTH open copy);
  - SCIP Optimization Suite 8.0 (arXiv 2112.08872v1);
  - SCIP Optimization Suite 9.0 (arXiv 2402.17702v2);
  - Brierley et al. (arXiv 1609.05011v2);
  - Drori-Teboulle (arXiv 1409.2636v2);
  - GLS 1981 (ZIB; scanned image, no text layer).
- SCIP source: `cons_nonlinear.c` at tag `v10.0.2` from GitHub. I read the
  `checkvarlocks` parameter registration and the `presolveSingleLockedVars`
  docstring.
- SCIP probes with `code/minlp_solver_lab/.venv/bin/python` (PySCIPOpt,
  SCIP 10.0; `parallel/maxnthreads=1`, `lp/threads=1`, `limits/nodes=1`).
  The model was min t s.t. D(x,y,z) <= t on [0,1]^3 with t ∈ [-10,10]. Root
  dual bounds:

  | Setting | Root dual bound |
  |---|---:|
  | Default | 0.0078124990 |
  | `presolving/maxrounds=0` | -0.0001160072 |
  | `constraints/nonlinear/checkvarlocks=d` | -0.0001160072 |
  | `checkvarlocks=b` | -0.0001160072 |
  | `propagating/probing/maxprerounds=0` | -0.0791263559 |
  | `propagating/maxroundsroot=0` | -0.0316395429 |
  | `nlhdlr/quadratic/enabled=False` | -0.0217287816 |
  | `separating/maxroundsroot=0` | 0.0078124990 |
  | Minor, RLT, perspective, convex handler, or restarts off | 0.0078124990 |

  The transformed variable types after default presolve are x and z BINARY,
  y and t CONTINUOUS. After presolve alone, the lower bound of t is -0.3828,
  so the 1/128 is reached during root processing.
  `m.setObjective(nonlinear)` raises "SCIP does not support nonlinear
  objective functions". The scratch scripts were deleted after the runs.
- Sign-test arithmetic, exact binomial with p = 1/2:
  - n = 9, X ≤ 2: 46/512, two-sided 0.180.
  - n = 6, X ≤ 2: 22/64, two-sided 0.688.
  - n = 4, X ≤ 1: 5/16, two-sided 0.625.

No project-wide tests were run, and CI was not inspected. Nothing under
`literature/` or `research-2026100*-convexification/` was modified.

## BibTeX-ready entries

Entries are plain BibTeX. Fields marked `% verify` were not confirmed from a
primary source in this lane.

```bibtex
@book{GrotschelLovaszSchrijver1988,
  author = {Gr{\"o}tschel, Martin and Lov{\'a}sz, L{\'a}szl{\'o} and Schrijver, Alexander},
  title = {Geometric Algorithms and Combinatorial Optimization},
  series = {Algorithms and Combinatorics}, volume = {2},
  publisher = {Springer}, address = {Berlin}, year = {1988},
  doi = {10.1007/978-3-642-97881-4}}
@article{GrotschelLovaszSchrijver1981,
  author = {Gr{\"o}tschel, Martin and Lov{\'a}sz, L{\'a}szl{\'o} and Schrijver, Alexander},
  title = {The ellipsoid method and its consequences in combinatorial optimization},
  journal = {Combinatorica}, volume = {1}, number = {2}, pages = {169--197}, year = {1981},
  doi = {10.1007/BF02579273}}
@article{KarpPapadimitriou1982,
  author = {Karp, Richard M. and Papadimitriou, Christos H.},
  title = {On linear characterizations of combinatorial optimization problems},
  journal = {SIAM Journal on Computing}, volume = {11}, number = {4}, pages = {620--632}, year = {1982}} % verify
@article{BienstockChenMunoz2020,
  author = {Bienstock, Daniel and Chen, Chen and Mu{\~n}oz, Gonzalo},
  title = {Outer-product-free sets for polynomial optimization and oracle-based cuts},
  journal = {Mathematical Programming}, volume = {183}, number = {1--2}, pages = {105--148}, year = {2020},
  doi = {10.1007/s10107-020-01484-3}}
@article{ChvatalCookEspinoza2013,
  author = {Chv{\'a}tal, Va{\v{s}}ek and Cook, William and Espinoza, Daniel},
  title = {Local cuts for mixed-integer programming},
  journal = {Mathematical Programming Computation}, volume = {5}, number = {2}, pages = {171--200}, year = {2013},
  doi = {10.1007/s12532-013-0052-9}}
@article{Boyd1994,
  author = {Boyd, E. Andrew}, title = {Fenchel cutting planes for integer programs},
  journal = {Operations Research}, volume = {42}, number = {1}, pages = {53--64}, year = {1994},
  doi = {10.1287/opre.42.1.53}}
@incollection{ApplegateBixbyChvatalCook2001,
  author = {Applegate, David and Bixby, Robert and Chv{\'a}tal, Va{\v{s}}ek and Cook, William},
  title = {{TSP} cuts which do not conform to the template paradigm},
  booktitle = {Computational Combinatorial Optimization}, series = {Lecture Notes in Computer Science},
  volume = {2241}, pages = {261--303}, publisher = {Springer}, year = {2001},
  doi = {10.1007/3-540-45586-8_7}}
@article{Gilbert1966,
  author = {Gilbert, Elmer G.},
  title = {An iterative procedure for computing the minimum of a quadratic form on a convex set},
  journal = {SIAM Journal on Control}, volume = {4}, number = {1}, pages = {61--80}, year = {1966},
  doi = {10.1137/0304007}}
@misc{BrierleyNavascuesVertesi2016,
  author = {Brierley, Stephen and Navascu{\'e}s, Miguel and V{\'e}rtesi, Tam{\'a}s},
  title = {Convex separation from convex optimization for large-scale problems},
  howpublished = {arXiv:1609.05011 [quant-ph]}, year = {2016}, note = {v2, January 2017}}
@misc{IoannouTravaglioneCheung2006,
  author = {Ioannou, Lawrence M. and Travaglione, Benjamin C. and Cheung, Donny},
  title = {Convex separation from optimization via heuristics},
  howpublished = {arXiv:cs/0603089}, year = {2006}}
@article{FrankWolfe1956,
  author = {Frank, Marguerite and Wolfe, Philip}, title = {An algorithm for quadratic programming},
  journal = {Naval Research Logistics Quarterly}, volume = {3}, number = {1--2}, pages = {95--110}, year = {1956},
  doi = {10.1002/nav.3800030109}}
@inproceedings{Jaggi2013,
  author = {Jaggi, Martin}, title = {Revisiting {Frank-Wolfe}: Projection-free sparse convex optimization},
  booktitle = {Proceedings of the 30th International Conference on Machine Learning},
  series = {PMLR}, volume = {28}, number = {1}, pages = {427--435}, year = {2013}}
@article{Wolfe1976,
  author = {Wolfe, Philip}, title = {Finding the nearest point in a polytope},
  journal = {Mathematical Programming}, volume = {11}, pages = {128--149}, year = {1976},
  doi = {10.1007/BF01580381}}
@article{GilbertJohnsonKeerthi1988,
  author = {Gilbert, Elmer G. and Johnson, Daniel W. and Keerthi, S. Sathiya},
  title = {A fast procedure for computing the distance between complex objects in three-dimensional space},
  journal = {IEEE Journal on Robotics and Automation}, volume = {4}, number = {2}, pages = {193--203}, year = {1988},
  doi = {10.1109/56.2083}} % verify DOI
@article{Kalantari2015,
  author = {Kalantari, Bahman},
  title = {A characterization theorem and an algorithm for a convex hull problem},
  journal = {Annals of Operations Research}, volume = {226}, number = {1}, pages = {301--349}, year = {2015},
  doi = {10.1007/s10479-014-1707-2}}
@inproceedings{LeeSidfordVempala2018,
  author = {Lee, Yin Tat and Sidford, Aaron and Vempala, Santosh S.},
  title = {Efficient convex optimization with membership oracles},
  booktitle = {Proceedings of the 31st Conference on Learning Theory}, series = {PMLR},
  volume = {75}, pages = {1292--1294}, year = {2018}}
@article{Kelley1960,
  author = {Kelley, Jr., James E.}, title = {The cutting-plane method for solving convex programs},
  journal = {Journal of the Society for Industrial and Applied Mathematics}, volume = {8}, number = {4},
  pages = {703--712}, year = {1960}, doi = {10.1137/0108053}}
@article{CheneyGoldstein1959,
  author = {Cheney, E. W. and Goldstein, A. A.},
  title = {Newton's method for convex programming and {Tchebycheff} approximation},
  journal = {Numerische Mathematik}, volume = {1}, pages = {253--268}, year = {1959}}
@article{DroriTeboulle2016,
  author = {Drori, Yoel and Teboulle, Marc}, title = {An optimal variant of {Kelley}'s cutting-plane method},
  journal = {Mathematical Programming}, volume = {160}, number = {1--2}, pages = {321--351}, year = {2016},
  doi = {10.1007/s10107-016-0985-7}}
@book{NemirovskyYudin1983,
  author = {Nemirovsky, A. S. and Yudin, D. B.},
  title = {Problem Complexity and Method Efficiency in Optimization},
  publisher = {Wiley}, address = {New York}, year = {1983}}
@article{deKlerkLaurentParrilo2006,
  author = {de Klerk, Etienne and Laurent, Monique and Parrilo, Pablo A.},
  title = {A {PTAS} for the minimization of polynomials of fixed degree over the simplex},
  journal = {Theoretical Computer Science}, volume = {361}, number = {2--3}, pages = {210--225}, year = {2006}}
@article{BestuzhevaEtAl2025SCIP8,
  author = {Bestuzheva, Ksenia and Chmiela, Antonia and M{\"u}ller, Benjamin and Serrano, Felipe and Vigerske, Stefan and Wegscheider, Fabian},
  title = {Global optimization of mixed-integer nonlinear programs with {SCIP} 8},
  journal = {Journal of Global Optimization}, volume = {91}, number = {2}, pages = {287--310}, year = {2025},
  doi = {10.1007/s10898-023-01345-1}}
@techreport{SCIP80,
  author = {Bestuzheva, Ksenia and Besan{\c{c}}on, Mathieu and Chen, Wei-Kun and Chmiela, Antonia and Donkiewicz, Tim and van Doornmalen, Jasper and Eifler, Leon and Gaul, Oliver and Gamrath, Gerald and Gleixner, Ambros and Gottwald, Leona and Graczyk, Christoph and Halbig, Katrin and Hoen, Alexander and Hojny, Christopher and van der Hulst, Rolf and Koch, Thorsten and L{\"u}bbecke, Marco and Maher, Stephen J. and Matter, Frederic and M{\"u}hmer, Erik and M{\"u}ller, Benjamin and Pfetsch, Marc E. and Rehfeldt, Daniel and Schlein, Steffan and Schl{\"o}sser, Franziska and Serrano, Felipe and Shinano, Yuji and Sofranac, Boro and Turner, Mark and Vigerske, Stefan and Wegscheider, Fabian and Wellner, Philipp and Weninger, Dieter and Witzig, Jakob},
  title = {The {SCIP} {O}ptimization {S}uite 8.0}, institution = {Zuse Institute Berlin},
  type = {ZIB-Report}, number = {21-41}, year = {2021}, note = {arXiv:2112.08872}}
@techreport{SCIP90,
  author = {Bolusani, Suresh and Besan{\c{c}}on, Mathieu and Bestuzheva, Ksenia and Chmiela, Antonia and Dion{\'\i}sio, Jo{\~a}o and Donkiewicz, Tim and van Doornmalen, Jasper and Eifler, Leon and Ghannam, Mohammed and Gleixner, Ambros and Graczyk, Christoph and Halbig, Katrin and Hedtke, Ivo and Hoen, Alexander and Hojny, Christopher and van der Hulst, Rolf and Kamp, Dominik and Koch, Thorsten and Kofler, Kevin and Lentz, Jurgen and Manns, Julian and Mexi, Gioni and M{\"u}hmer, Erik and Pfetsch, Marc E. and Schl{\"o}sser, Franziska and Serrano, Felipe and Shinano, Yuji and Turner, Mark and Vigerske, Stefan and Weninger, Dieter and Xu, Liding},
  title = {The {SCIP} {O}ptimization {S}uite 9.0}, institution = {Zuse Institute Berlin},
  type = {ZIB-Report}, number = {24-02-29}, year = {2024}, note = {arXiv:2402.17702}}
@misc{SCIP100,
  author = {Hojny, Christopher and Besan{\c{c}}on, Mathieu and Bestuzheva, Ksenia and others},
  title = {The {SCIP} {O}ptimization {S}uite 10.0}, howpublished = {arXiv:2511.18580}, year = {2025}}
@article{VigerskeGleixner2018,
  author = {Vigerske, Stefan and Gleixner, Ambros},
  title = {{SCIP}: global optimization of mixed-integer nonlinear programs in a branch-and-cut framework},
  journal = {Optimization Methods and Software}, volume = {33}, number = {3}, pages = {563--593}, year = {2018}, % verify volume/pages
  doi = {10.1080/10556788.2017.1335312}}
@article{MullerSerranoGleixner2020,
  author = {M{\"u}ller, Benjamin and Serrano, Felipe and Gleixner, Ambros},
  title = {Using two-dimensional projections for stronger separation and propagation of bilinear terms},
  journal = {SIAM Journal on Optimization}, volume = {30}, number = {2}, pages = {1339--1365}, year = {2020},
  doi = {10.1137/19M1249825}}
@article{BestuzhevaGleixnerAchterberg2025,
  author = {Bestuzheva, Ksenia and Gleixner, Ambros and Achterberg, Tobias},
  title = {Efficient separation of {RLT} cuts for implicit and explicit bilinear terms},
  journal = {Mathematical Programming}, volume = {210}, number = {1--2}, pages = {47--74}, year = {2025},
  doi = {10.1007/s10107-024-02104-0}}
@article{BestuzhevaGleixnerVigerske2023,
  author = {Bestuzheva, Ksenia and Gleixner, Ambros and Vigerske, Stefan},
  title = {A computational study of perspective cuts},
  journal = {Mathematical Programming Computation}, volume = {15}, number = {4}, pages = {703--731}, year = {2023}}
@article{ChmielaMunozSerrano2023,
  author = {Chmiela, Antonia and Mu{\~n}oz, Gonzalo and Serrano, Felipe},
  title = {On the implementation and strengthening of intersection cuts for {QCQPs}},
  journal = {Mathematical Programming}, volume = {197}, number = {2}, pages = {549--586}, year = {2023},
  doi = {10.1007/s10107-022-01808-5}}
@inproceedings{MunozSerrano2020,
  author = {Mu{\~n}oz, Gonzalo and Serrano, Felipe}, title = {Maximal quadratic-free sets},
  booktitle = {Integer Programming and Combinatorial Optimization (IPCO 2020)}, series = {LNCS},
  volume = {12125}, pages = {307--321}, publisher = {Springer}, year = {2020},
  doi = {10.1007/978-3-030-45771-6_24}}
@article{Achterberg2009,
  author = {Achterberg, Tobias}, title = {{SCIP}: solving constraint integer programs},
  journal = {Mathematical Programming Computation}, volume = {1}, number = {1}, pages = {1--41}, year = {2009},
  doi = {10.1007/s12532-008-0001-1}}
@article{HansenJaumardRuizXiong1993,
  author = {Hansen, Pierre and Jaumard, Brigitte and Ruiz, Michel and Xiong, Junjie},
  title = {Global minimization of indefinite quadratic functions subject to box constraints},
  journal = {Naval Research Logistics}, volume = {40}, number = {3}, pages = {373--392}, year = {1993}}
@misc{BestuzhevaVolkerGleixner2023,
  author = {Bestuzheva, Ksenia and V{\"o}lker, Helena and Gleixner, Ambros},
  title = {Strengthening {SONC} relaxations with constraints derived from variable bounds},
  howpublished = {arXiv:2304.12145}, year = {2023}}
@article{BussieckDrudMeeraus2003,
  author = {Bussieck, Michael R. and Drud, Arne Stolbjerg and Meeraus, Alexander},
  title = {{MINLPLib}---a collection of test models for mixed-integer nonlinear programming},
  journal = {INFORMS Journal on Computing}, volume = {15}, number = {1}, pages = {114--119}, year = {2003},
  doi = {10.1287/ijoc.15.1.114.15159}}
@misc{MINLPLib,
  author = {Vigerske, Stefan}, title = {{MINLPLib}: A library of mixed-integer and continuous nonlinear programming instances},
  howpublished = {\url{https://www.minlplib.org}}, note = {Snapshot 2026-07-29, git 168bf3d2}}
@article{KochEtAl2011MIPLIB2010,
  author = {Koch, Thorsten and Achterberg, Tobias and Andersen, Erling and Bastert, Oliver and Berthold, Timo and Bixby, Robert E. and Danna, Emilie and Gamrath, Gerald and Gleixner, Ambros M. and Heinz, Stefan and Lodi, Andrea and Mittelmann, Hans and Ralphs, Ted and Salvagnin, Domenico and Steffy, Daniel E. and Wolter, Kati},
  title = {{MIPLIB} 2010}, journal = {Mathematical Programming Computation},
  volume = {3}, number = {2}, pages = {103--163}, year = {2011}, doi = {10.1007/s12532-011-0025-9}}
@article{GleixnerEtAl2021MIPLIB2017,
  author = {Gleixner, Ambros and Hendel, Gregor and Gamrath, Gerald and Achterberg, Tobias and Bastubbe, Michael and Berthold, Timo and Christophel, Philipp and Jarck, Kati and Koch, Thorsten and Linderoth, Jeff and L{\"u}bbecke, Marco and Mittelmann, Hans D. and Ozyurt, Derya and Ralphs, Ted K. and Salvagnin, Domenico and Shinano, Yuji},
  title = {{MIPLIB} 2017: data-driven compilation of the 6th mixed-integer programming library},
  journal = {Mathematical Programming Computation}, volume = {13}, number = {3}, pages = {443--490}, year = {2021},
  doi = {10.1007/s12532-020-00194-3}}
@incollection{LodiTramontani2013,
  author = {Lodi, Andrea and Tramontani, Andrea}, title = {Performance variability in mixed-integer programming},
  booktitle = {Theory Driven by Influential Applications}, series = {INFORMS TutORials in Operations Research},
  pages = {1--12}, publisher = {INFORMS}, year = {2013}, doi = {10.1287/educ.2013.0112}}
@misc{Danna2008,
  author = {Danna, Emilie}, title = {Performance variability in mixed integer programming},
  howpublished = {Talk, Workshop on Mixed Integer Programming 2008, Columbia University}, year = {2008}}
@article{DolanMore2002,
  author = {Dolan, Elizabeth D. and Mor{\'e}, Jorge J.},
  title = {Benchmarking optimization software with performance profiles},
  journal = {Mathematical Programming}, volume = {91}, number = {2}, pages = {201--213}, year = {2002},
  doi = {10.1007/s101070100263}}
@article{BussieckDirkseVigerske2014,
  author = {Bussieck, Michael R. and Dirkse, Steven P. and Vigerske, Stefan},
  title = {{PAVER} 2.0: an open source environment for automated performance analysis of benchmarking data},
  journal = {Journal of Global Optimization}, volume = {59}, number = {2--3}, pages = {259--275}, year = {2014}, % verify volume/pages
  doi = {10.1007/s10898-013-0131-5}}
@article{Berthold2013,
  author = {Berthold, Timo}, title = {Measuring the impact of primal heuristics},
  journal = {Operations Research Letters}, volume = {41}, number = {6}, pages = {611--614}, year = {2013},
  doi = {10.1016/j.orl.2013.08.007}}
@article{Margot2009,
  author = {Margot, Fran{\c{c}}ois}, title = {Testing cut generators for mixed-integer linear programming},
  journal = {Mathematical Programming Computation}, volume = {1}, number = {1}, pages = {69--95}, year = {2009},
  doi = {10.1007/s12532-009-0003-7}} % verify DOI
@article{DeyMolinaro2018,
  author = {Dey, Santanu S. and Molinaro, Marco}, title = {Theoretical challenges towards cutting-plane selection},
  journal = {Mathematical Programming}, volume = {170}, number = {1}, pages = {237--266}, year = {2018},
  doi = {10.1007/s10107-018-1302-4}}
@article{Wilcoxon1945,
  author = {Wilcoxon, Frank}, title = {Individual comparisons by ranking methods},
  journal = {Biometrics Bulletin}, volume = {1}, number = {6}, pages = {80--83}, year = {1945}}
```
