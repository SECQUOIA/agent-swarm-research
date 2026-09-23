# Stage 4B spectral and chordal author audit

Owned files: sections/09e-spectral-chordal.tex, this audit, and stage4b-spectral-bib.txt. No other repository files edited. The section is 436 lines and compiled alone with the repository macros under qipm, producing six pages without errors or overfull boxes; missing bibliography and cross-section references are expected in the temporary standalone check. Parent performs the integrated bibliography/build.

## Source coverage

- 2026-09-04-spectral-ball-contact-curvature-packing.md: fully incorporated in Proposition prop:spectral-contact and its proof. R/C/H and mixed fields included; tangent rank delta*c−1 includes relative phase. Whole-row assumption is absent here, but global C1 labelled full rows are explicit. Incidence-index typo corrected. No sharp topology or attainment claim.

  First-review correction: the total local rank bound is strengthened from
  m_i-1 to m_i-2. Any active nonzero dual contact vector annihilates the
  primal ray and all primal derivatives, so the rank-detecting direct sum
  lies in an (m_i-1)-dimensional hyperplane. Consequently the unweighted
  sum of capacities is at least the sum of spectral contact ranks. This
  replaces the source's weaker weighted/divided capacity consequences;
  its useful face and incidence inequalities remain. See the separate
  correction audit for the complete validation.
- 2026-09-04-spectral-norm-face-capped-grouping-frontier.md: full face formula, universal theorem specialization, exact two-cap group feasibility, equal-row floor count, heterogeneous strong NP-hardness, storage and displayed-cone exact barriers included. General whole-row theorem referenced as thm:whole-row-caps. Independent real and complex dimensions, including mixed real/complex rows, stated. No inference of a barrier lower bound for arbitrary larger-dimensional attaining cones.
- 2026-09-04-spectral-norm-product-sharing.md: all sharing, ambient/slice barriers, genuine full slack maps, block-star matrix extension, exact reduced-oracle/KKT geometry covered. Its movement theorem belongs to the planned Stage 5 and is deferred explicitly below. R/C barriers stated; no unsupported quaternionic spectral-barrier claim added.
- 2026-09-04-chordal-completion-ball-packing.md: arbitrary graph cone closedness/duality and exact arbitrary-coupled barriers, classical maxdet/clique-separator formula, scalar and matrix leaves, real/complex storage counts, full dual slack maps, regrouping totals, reduced geometry, and precise barrier-evaluation-only arithmetic/storage bounds covered. Ellipsoidal coordinate changes are subsumed by standard affine invariance and do not need a separate theorem.

## Independent mathematical reconstruction

1. Contact gauge: at X=(I,0), u=v=e1, use u*du=0. Off-axis differences have delta(r−1) dimensions; tail delta(c−r); imaginary diagonal delta−1. This includes r=c and r=1. All quaternionic operations use real pairings, avoiding unqualified trace cyclicity.
2. Cross-contact cylinders: each nonnegative summand vanishes, so its first polar derivative vanishes identically along each unrelated primal cylinder. Differentiating this C1 identity proves the mixed cross-row annihilation. Direct-sum and face inequalities use only this identity, not nondegeneracy of the total spectral contact pairing.
3. Whole-row faces: support of nuclear rank h fixes −tI_h, kills cross rectangles, leaves arbitrary complementary contraction. Real codimension delta*h*(r+c−h), smallest at h=1. This supplies universal-theorem lambda=delta(r+c−1) exactly.
4. Ambient barrier lower bound substantially clarified: source only mentioned recession certificates. Draft gives explicit ones for C_r={t>=||xi||infty}: x=(1,(1−epsilon)1), p0=(1,1), pj=(1,1−2ej), aj=bj=epsilon/2, a0=1−r epsilon/2, b0=1−epsilon/2. Then x=sum aj pj and every x−bj pj is boundary. Nesterov bound r+a0/b0 tends to r+1. Direct-sum certificates prove arbitrary coupled-product lower bound; no accidental use of an LH-only polyhedral theorem.
5. Slice: restriction of Hermitian block PSD logdet proves ordinary SC; explicit singular-value gradient norm proves sharp parameter sum ranks; cube section gives arbitrary coupled lower.
6. Completion cone: full diagonals bound every unspecified entry of every PSD completion, so projection is closed. The signed Legendre transform gives maxdet completion, with sign checked explicitly F=−n−logdet Z. Orthant section proves all-barrier lower. Chordal leaf-Schur elimination proves separator formula. All-diagonal hypothesis explicit.
7. Block-star dual map depends only on rank-one Z although written using u,v: bb*/2 invariant under common phase. Could equivalently write diagonal blocks ZZ*, Z*Z and cross −Z. Identity-block restriction preserves exact functions, not merely parameters.
8. Complex orientation correction: adjunction is a fixed real orthogonal signed coordinate change, not just an unsigned index permutation. Reduced-object oracle equivalence is conditional on supplied reduced interfaces and does not identify ambient KKT or compilation cost.

## Primary literature verification and correction

- Critical title correction: https://optimization-online.org/wp-content/uploads/2020/05/7776.pdf is **Towards practical generic conic optimization**, not *Performance enhancements for a generic conic interior point algorithm*. Its Section 4.7 eq4.13 states the spectral barrier. This paper became **Solving natural conic formulations with Hypatia.jl**, INFORMS J. Computing34(5)(2022)2686–2699, DOI10.1287/ijoc.2022.1202. Final metadata verified on author Vielma's publication page https://juan-pablo-vielma.github.io/publications/index_type.html; primary later preprint https://arxiv.org/pdf/2005.01136 Section4.2 p8 records the spectral cone and references the classical NN barrier. Correct key CKV2022natural supplied.
- Complex spectral barrier explicitly verified in Coey's MIT thesis, *Interior point and outer approximation methods for conic optimization*, May2022, primary https://chriscoey.github.io/assets/pdf/phd_thesis.pdf Section2.6.1 printed87 eq2.69. It explicitly treats real/complex rectangular matrices and parameter number-of-rows+1. Thesis title/date inspected on titlepage.
- Nesterov recession certificate stated and verified in Fawzi–Saunderson, primary https://arxiv.org/html/2205.04581v3 Theorem3.9. Journal metadata SIAM J. Optim.33(4)(2023)2858–2884 DOI10.1137/22M1500216 from root's primary metadata check. Section uses this general all-barrier theorem rather than FH/Hildebrand LH-only statements.
- Andersen–Dahl–Vandenberghe primary https://arxiv.org/pdf/1203.2742 Section1.2 eq3 defines the same signed conjugate; section discusses maxdet completion. DOI metadata verified at arXiv record https://arxiv.org/abs/1203.2742. Journal metadata28(3)(2013)396–423 confirmed in root preparation.
- Grone–Johnson–Sa–Wolkowicz publisher page https://www.sciencedirect.com/science/article/pii/0024379584902076 confirms title, authors, LAA58(1984)109–124, DOI and completion/inverse-sparsity statements. Primary original PDF also https://pages.cs.wisc.edu/~nathanae/nonlinproj/grone.pdf.
- Barrett–Johnson–Lundquist publisher page https://www.sciencedirect.com/science/article/pii/0024379589907064 confirms LAA121(1989)265–289 DOI10.1016/0024-3795(89)90706-4 and exact maximal-clique/separator determinant formula.
- Gouveia–Ito–Lourenco2026 is relevant when discussing minimal determinant polynomial degree versus optimal barrier rank. This subsection makes no polynomial-degree claim, so no new citation is needed here. Parent can include it in general literature synthesis.

No priority claim is made for the spectral barrier, completion barrier, separator formula, or their primitive exact parameters. The concrete comparisons and factor-budget applications are proved directly, with no claim that a literature search establishes priority.

## Mandatory movement coverage deferred to Stage 5

The shared-spectral source Section6 has a distinct matrix-valued movement result. Let R=sum r_a, C_a=(I_r,0), ell(X)=sum <C_a,X_a>, Q(X)=prod det(I−X_aX_a*), Phi=−log Q. If R−ell(X)<=epsilon, von Neumann gives sum(1−sigma)<=epsilon; 1−sigma²<=2(1−sigma) and AMGM give Q^(1/R)<=2epsilon/R. Center X=0 has Q=1. Gradient norm bound sqrt R then gives geodesic distance >=[sqrt R log(R/(2epsilon))]_+. m counted feasible chords each starting local norm<=eta<1 per round imply T >= distance/[m log(1/(1−eta))]. The same fixed-slice barrier proves grouping/chordal invariance. Exact central path for maximizing tau ell−Phi is X_a=r(tau)C_a, r=tau/(sqrt(1+tau²)+1), gap R(1−r). All feasible-iterate changes must be charged; result does not imply query/runtime bound or cover unbounded local moves. This theorem is not subsumed merely by scalar-ball movement when r_a>1; Stage 5 must retain it.
