# Targeted open-literature screen: sparse conic QIPM lower bounds and formulation effects

**Screen date:** 2026-09-04
**Status:** targeted, non-exhaustive open-literature check; not a novelty opinion or a systematic review.

This note screens five claim families developed in the September 4 workbench notes, followed by targeted follow-ups on the sharp sharing-cone barriers, product additivity, exposed-rank capacity, and a one-ball regularity premium:

1. fixed-barrier iteration lower bounds for bounded Dikin moves;
2. exposed-dual-rank distance and iteration lower bounds on arbitrary symmetric cones;
3. Lorentz-versus-PSD formulation equivalence after exact fiber minimization;
4. PSD packing of products of Euclidean balls and exact restricted log-determinant barrier parameters; and
5. accuracy-dependent quantum output lower bounds encoded in one Lorentz cone.

The follow-ups check the claimed optimal \(q+1\) barriers on
\(\mathcal H_{q,s}\) and \(\mathcal P_q\), their product behavior, and the
attribution boundary of the symmetric-cone distance and topology results.

The screen used the local literature collection, arXiv title/keyword searches, and publisher or author pages. It emphasizes primary research sources available by the screen date. Terminology varies sharply across self-concordant geometry, extension complexity, matrix completion, and quantum query complexity, so a negative search result should be read only as “no direct collision located in this targeted screen.”

## Executive assessment

| Local claim family | Closest prior art located | Assessment after the screen |
|---|---|---|
| Distance-to-accuracy-set lower bounds for fixed product-ball, norm-tree, and packed-PSD barriers under bounded Dikin chords | Nesterov--Todd's exact bounded-short-step/distance conversion; Nesterov--Nemirovski's distance-to-solution-set benchmark; Todd--Ye and Allamigeon et al. iteration/path-complexity lower bounds | The generic conversion from bounded Dikin moves to a Riemannian-distance lower bound and the use of distance to the whole target set are prior art. No source was located with the same explicit distance formulas for these conic lifts. The claim must remain restricted to the fixed barrier and bounded-local-move model; it is not a lower bound for every IPM or QIPM. |
| Exact spectral-ball distance, objective water filling, and sharp subgeodesicity | Lewis--Sendov's spectral Hessian formula; Nesterov--Todd's self-concordant Riemannian framework; Nesterov--Nemirovski's general (O(\nu^{1/4})) bounded-domain comparison | The Hessian and generic distance machinery are classical. No source was located stating the exact transformed-singular-value distance for \(-\log\det(I-XX^*)\), the exact support-objective water filling and optimal bounded-Dikin move law, or the sharp \(\Theta(\sqrt{\log r})\) same-endpoint/same-accuracy distortion and central-neighborhood round separation. The latter also applies to the conventional fixed Newton-decrement neighborhood by a standard self-concordant conversion. Treat the package as a candidate standard-barrier specialization, not a Bergman-distance identity or generic QIPM runtime theorem. |
| Exposed-Jordan-rank theorem on arbitrary symmetric cones | Permenter's symmetric-cone geodesic IPM; Hauser--Güler barrier classification; Cardoso--Vieira optimal rank parameter; Nesterov--Todd and Nesterov--Nemirovski Riemannian geometry | Principal minors, Peirce compression, standard Jordan logdet geometry, the Dikin-step conversion, and the distance-to-target-set viewpoint are classical. No source was located using a support principal minor with exact covector norm \(\sqrt q\) to give the stated objective-dependent bound in terms of one exposing dual slack's rank. That explicit bound, not the generic iteration conversion, is the candidate contribution. |
| Exact Lorentz/PSD reduction after partial minimization | Classical maximum-determinant positive-definite completion; SOC-to-SDP representation maps | Maximum-determinant fiber centering is established classical machinery. No source located proving the complete package used locally: the particular marginal barrier, the residual KKT direct sum, equality of projected normalized outputs, and exact matched-oracle query equivalence. That package, rather than “SOC and SDP are equivalent,” is the defensible contribution. |
| Exact PSD packing/private-nullity/capacity/restricted-barrier frontier for product balls | PSD-rank and cone-factorization theory; semidefinite extension degree; lower bounds for barriers; Lorentz-cone factorization | No direct theorem with the local joint resource ledger was located. Existing extension measures usually count one largest block or permit arbitrarily many blocks; they do not simultaneously count factor number, contact-channel capacity, selected boundary nullity, and the restricted standard-logdet parameter. |
| One-Lorentz scalar/full-readout lower bounds with easy state output | Nayak--Wu approximate counting; tight expectation-estimation lower bounds for quantum linear systems; general LP/SDP quantum lower bounds | The query exponent is inherited from approximate counting/mean estimation and is not new by itself. No source located compiling it into the stated one-Lorentz, public sparse, well-conditioned, reduced-barrier-one family while also separating scalar/full output from normalized-state output. The contribution should be presented as a conic compilation and separation theorem. |
| One-box signed parity chain with a trivial reduced normalized state | Beals et al. and subsequent exact/bounded-error parity query bounds; elementary signed-path gauge transformations; established QLS output/readout caveats | Parity hardness, global-phase erasure, and path elimination are classical. No direct source was located for their exact conjunction in an equality-constrained barrier-one program: positive optimum \(3\) versus \(1\), fixed-center scalar gap, zero-query one-dimensional reduced state, treewidth-one literal KKT with condition \(\Theta(N)\), and matched raw/sparse/charged-SQ access. Treat this as a compact compiler/counterexample with modest standalone novelty, not a new parity or QLS lower-bound method. |
| Exact \(q+1\) barriers for \(\mathcal H_{q,s}\) and \(\mathcal P_q\) | Nesterov--Nemirovskii spectral-norm cone barrier; Güler and Hildebrand on the infinity-norm cone; chordal max-det completion; Andersen--Dahl--Vandenberghe sparse cone barriers | Both formulas and their \(q+1\) upper bounds are classical specializations. The matching lower bounds follow from classical scalar/orthant sections. Their use in the local sharing frontier may be useful, but the barriers themselves are not new. |
| Exact coupled-barrier parameter \(\nu_{\rm opt}(\prod_\ell\mathcal H_{q_\ell,s_\ell})=\sum_\ell(q_\ell+1)\) | Factorwise spectral-norm barriers; Nesterov's recession-direction lower bound as reproduced by Fawzi--Saunderson | The equality against an arbitrary coupled barrier is a short tensorized-certificate corollary of published machinery. No explicit statement for these block-max cones was located. Treat it as exact accounting with low standalone novelty, not a new lower-bound method. |
| One-ball support-objective premium under a global bi-\(C^1\) contact sheet | General cone-factorization theory; sparse SOCP reformulations; Fawzi's SOC nonrepresentability; Aubrun--La Piana--Müller-Hermes on Lorentz-factorizable positive maps | No source was located with the support-rank statement or its sphere-to-product finite-cover proof. It is a plausible candidate theorem under its narrow regularity and global-labelling assumptions, not an unconditional SOC extension-complexity lower bound and not a statement for every objective. |
| Dimension-only \(\Psi_d(D+1)\) movement bound for arbitrary product-cone dictionaries | Gouveia--Parrilo--Thomas slack factorizations; Fawzi--Parrilo fixed-size PSD block lower bounds; Saunderson short-face-chain obstructions; Nesterov--Todd Riemannian movement | Every ingredient has a classical antecedent. No source was located that combines ordinary slack rank, a factor-dimension cap, an orthant section for a coupled LHSCB, and Nesterov--Todd distance into the exact \(\Psi_d(D+1)\) theorem. Treat it as an apparently unlocated exact synthesis with modest standalone novelty, not a new lift-factorization or Riemannian principle. |
| Hermitian sequential-contact exposed-rank theorem and exact all-field standard-slice frontier | Fawzi--Gouveia--Parrilo--Robinson--Thomas block-triangular PSD-rank compression; PSD/complex-PSD rank; semidefinite extension degree; Kummer's direct ball spectrahedron bound; symmetric-cone logdet barriers | Range compression through the span of factors forced by zero slacks is published prior art. No source was located with the smooth sequential contact selection, the exact \(\delta(R-1)\) capacity and spin exceptions, the rank of one positive weighted exposing sum, or the resulting real/complex/quaternionic restricted-standard-barrier frontier. Candidate derived theorem under its global bi-\(C^1\), labelling, and slice hypotheses; not an unconditional PSD-rank result. |
| Selection-free critical real-PSD sequential theorem | Gouveia--Parrilo--Thomas already construct the convex dual feasible set and choose any certificate; facial reduction gives whole-feasible-set annihilation; Fawzi et al. study PSD-factorization spaces and prove block-triangular common-kernel/range compression; Dawson et al. study size-two uniqueness; Vill studies whole primal PSD fibers | The ingredients “convex certificate fiber,” “every-fiber annihilation by one certificate,” topology of factorization spaces, and PSD compression are not new separately. No source was located combining the rank-one-fiber singleton with an \(S^{s-1}\hookrightarrow\mathbb {RP}^{r-1}\) obstruction and stagewise compression of the **original global** certificate fibers to obtain a positive weighted exposed-rank sum and every-fiber nullity \(2b\). Treat as a candidate exact synthesis only in the proved critical real cap \(r_i\le s\). Unique-certificate norm chains refute the analogous higher-rank exposed-rank statement; their primal vertex seams leave a possible nullity-only extension open. |
| Exact-optimal hyperoctahedral box family and facet-regular tax stability | Standard ball and box barriers; Nesterov--Vial quadratic augmentation; Castro--Cuesta diagonal regularization; Nesterov--Todd metric geometry | No screened source states the exact-\(r\) radial family, its arbitrarily loose sum certificate, or the full-signed-facet regularity theorem preserving the \(\Gamma_r\) tax. Treat both as candidate explicit syntheses, not an all-optimal-barrier theorem. |
| Arbitrary-factor wide-cap Lorentz and Hermitian rigidity | SOC/PSD modelling and factorization; symmetric-cone barrier optimality; face-chain obstructions; invariance of domain and projective-space cohomology | The ingredients are classical, but no screened source gives the factor-count-independent affine-slice parameter theorem. It closes the divisible wide-cap regime for the restricted standard product barrier; narrow-cap bounded cases remain open. |
| All-simple-EJA exposed-rank frontier and same-instance readout boundary | Faraut--Korányi Peirce calculus; Hauser--Güler classification; Cardoso--Vieira ambient optimality; Permenter symmetric-cone IPMs; standard phase-query, Holevo, and rate-distortion bounds | No screened source gives the exact \(\lceil(s-1)/B\rceil\) support-fiber minimax, its Albert/essential-infimum extension, or the rank--movement--state--explicit-output conjunction. Treat as candidate syntheses; movement and readout combine by a maximum and do not imply unrestricted QIPM runtime hardness. |

## 1. Fixed-barrier, bounded-Dikin-move iteration lower bounds

The relevant local notes are:

- [grouped-ball short-step lower bound](2026-09-04-grouped-ball-short-step-iteration-lower-bound.md);
- [norm-tree short-step lower bound](2026-09-04-norm-tree-short-step-iteration-lower-bound.md); and
- [packed-PSD geodesic lower bound](2026-09-04-psd-packing-geodesic-iteration-lower-bound.md).

They lower-bound the number of feasible chords whose lengths are bounded in the local Hessian norm of a **specified restricted standard barrier**. The proof lower-bounds the Riemannian distance from the analytic center to the entire objective-accuracy set, not merely the length or curvature of a chosen central path.

### Closest sources

1. **Nesterov and Todd, “On the Riemannian Geometry Defined by Self-Concordant Barriers and Interior-Point Methods” (2002).**
   [Publisher page](https://doi.org/10.1007/s102080010032) and [author manuscript](https://people.orie.cornell.edu/miketodd/NTRiemann.pdf). Definition 3.1 calls a sequence \(\kappa\)-short-step when every chord has local norm at most \(\kappa<1\). Lemma 3.2 proves \(\rho(x_0,x_N)\leq-N\log(1-\kappa)\), and Corollary 3.2 rearranges this as \(N\geq\rho(x_0,x_N)/[-\log(1-\kappa)]\). This is the direct antecedent for the local notes' generic bounded-Dikin-move conversion, not merely background. Lemma 2.2 also gives the generic barrier-height bound \(\rho(x_0,x_1)\geq |F(x_0)-F(x_1)|/\sqrt\nu\), and Lemma 4.1 gives the \(\ell_2\) product rule for distances. The paper does not give the local notes' closed-form distance from the center to a whole product-ball accuracy level set or the corresponding norm-tree and packed-PSD formulas.

2. **Nesterov and Nemirovski, “Primal Central Paths and Riemannian Distances for Convex Sets” (2008; circulated as a 2003 preprint).**
   [Publisher page](https://doi.org/10.1007/s10208-007-9019-4) and [author manuscript](https://www2.isye.gatech.edu/~nemirovs/FCM_Riem_2008.pdf). This work explicitly treats Riemannian distance from a starting point to a solution set as the natural lower benchmark for short-step methods. Example 1.1 is especially close conceptually: for the standard orthant barrier it shows that a central-path endpoint can be much farther than another point in the same target hyperplane, so central-path length need not equal distance to the target set. With \(\sigma\) denoting Riemannian distance, Theorem 4.1 gives
   \[
     \rho[x(\cdot),t_0,t_1]
     \leq \log2+\nu^{1/4}
       \sqrt{\sigma(x(t_0),x(t_1))
       [\sigma(x(t_0),x(t_1))+\log12]},
   \]
   and removes the \(\log2\) term and replaces \(\log12\) by \(\log3\) when the starting Newton decrement is at least \(1/2\). Corollary 5.1 gives, under its bounded-feasibility assumptions, \(\rho[x(\cdot),0,1]\leq O(1)\nu^{1/4}[\sigma(0,F)+\log\nu]\). Thus the local distinction is not the idea of minimizing over all accurate endpoints; it is the explicit, objective-dependent distance calculation for the named conic lifts and its robustness to inactive fibers.

3. **Todd and Ye, “A Lower Bound on the Number of Iterations of Long-Step Primal-Dual Linear Programming Algorithms” (1996).**
   [Publisher page](https://doi.org/10.1007/BF02206818). This gives an LP lower bound for long-step primal-dual algorithms constrained to a wide neighborhood of the central path. It is a genuine iteration lower bound, but its algorithmic neighborhood model and LP construction differ from the fixed conic-barrier/bounded-chord model in the local notes.

4. **Allamigeon, Benchimol, Gaubert, and Joswig, “Log-Barrier Interior Point Methods Are Not Strongly Polynomial” (2018/2022).**
   [arXiv](https://arxiv.org/abs/1708.01544). This establishes exponential behavior for log-barrier LP central paths using tropical geometry. It addresses strong polynomiality and central-path complexity, not the explicit accuracy-dependent radial distance of one of the fixed sparse conic barriers considered locally.

5. **Allamigeon, Gaubert, and Vandame, “No Self-Concordant Barrier Interior Point Method Is Strongly Polynomial” (2022).**
   [arXiv](https://arxiv.org/abs/2201.02186). This extends the obstruction beyond the logarithmic barrier and constructs LP families with exponentially many path-following iterations in the relevant framework. It is much broader with respect to barrier choice, but is tied to its parametric-LP/path-following notion of progress. It does not subsume an exact product-ball or packed-PSD distance-to-accuracy-set theorem.

6. **Allamigeon, Dadush, Loho, Natura, and Végh, “Interior Point Methods Are Not Worse Than Simplex” (2022).**
   [arXiv](https://arxiv.org/abs/2206.08810). This introduces straight-line complexity: the least number of line segments needed for a piecewise-linear trajectory inside a wide central-path neighborhood. It is close in its use of segmented trajectories, but the admissibility condition is neighborhood membership rather than a local-Hessian length bound, and the target is combinatorial path complexity.

7. **Dahl, Tunçel, and Vandenberghe, “New Complexity Bounds for Primal--Dual Interior-Point Algorithms in Conic Optimization” (2025; revised 2026).**
   [arXiv](https://arxiv.org/abs/2509.10263). This develops improved *upper* bounds using metric properties of self-scaled barriers. It is useful for calibrating the local model against modern conic path-following guarantees, but does not provide the claimed lower bounds.

8. **Augustino, Nannicini, Terlaky, and Zuluaga, “A Quantum Central Path Algorithm for Linear Optimization” (2023).**
   [arXiv](https://arxiv.org/abs/2311.03977). This proposes simulating a nonlinear central-path evolution rather than implementing a succession of Newton/Dikin-bounded classical iterates. It is an important boundary case: a bounded-chord geometric lower bound does not automatically apply to this or to any quantum algorithm whose query trajectory is not represented by the local model.

### Collision assessment and safe statement

No direct source was located for the exact grouped-ball, norm-tree, or packed-PSD distance-to-the-entire-accuracy-set calculation. There is, however, extensive prior work on Riemannian barrier geometry and iteration lower bounds. The local theorem should therefore be described narrowly, for example:

> For the specified restricted standard barrier, any feasible trajectory decomposed into chords of local barrier length at most a fixed constant needs at least the stated number of chords before entering the objective-accuracy set.

It should not be advertised as an unconditional lower bound on IPMs, on all self-concordant barriers, or on arbitrary quantum algorithms.

The independently audited
[sharp spectral-ball subgeodesicity note](2026-09-04-spectral-ball-sharp-subgeodesicity.md)
is a stronger fixed-barrier specialization.  Lewis and Sendov's
[spectral Hessian formula](https://doi.org/10.1137/S089547980036838X)
is the direct antecedent for its Hermitian-dilation calculation, while
Nesterov--Todd supplies the bounded-Dikin conversion and
Nesterov--Nemirovski supplies the general bounded-domain comparison.  The
2026 manifold-IPM framework of
[Hirai--Nieuwboer--Walter](https://doi.org/10.1007/s10208-026-09756-8)
is also adjacent, but treats self-concordance when the base optimization
domain is Riemannian rather than computing this Euclidean barrier-Hessian
matrix-ball metric.  The
candidate contribution is the exact matrix-ball center distance, strictly
convex objective-sublevel water filling, matched optimal arbitrary-move
count, and sharp \(\Theta(\sqrt{\log r})\) continuous and discrete
centrality tax.  Its discrete lower bound starts at the analytic center and
assumes a fixed geodesic-radius neighborhood of labeled exact centers, but permits arbitrary backward moves
of the reference labels and includes a conventional fixed Newton-decrement
neighborhood.  Actual endpoint accuracy itself forces the needed reference
progress, so there is no terminal-label assumption.  It is not an
unconditional lower bound for all IPM neighborhoods.

## 2. Exposed dual rank on arbitrary symmetric cones

The relevant local note is [symmetric-cone exposed-rank Dikin lower bound](2026-09-04-symmetric-cone-exposed-rank-dikin-lower-bound.md). For the standard Jordan barrier on a product of symmetric cones, it associates to an attained exposing dual slack \(s_i\) its support idempotent \(c_i\) and rank \(q_i\), and defines the support-principal-minor potential

\[
  \Phi_s(x)=-\sum_{i:q_i>0}\log\det_{c_i}(P(c_i)x_i).
\]

The proposed key identity is that each support-minor covector has squared dual barrier norm \(q_i\), hence \(\Phi_s\) is globally \(\sqrt Q\)-Lipschitz in the standard barrier metric for \(Q=\sum_iq_i\). Objective accuracy and Jordan AM--GM then give a distance lower bound of the form

\[
 d_F(x^c,\{y:\ell_*-\ell(y)\leq\varepsilon\})
 \geq \left[\sqrt Q\log(\Delta_c/\varepsilon)\right]_+.
\]

The local note also combines this with a product-ball Peirce-capacity argument, forcing \(Q\) to grow for bounded-size symmetric-cone factors.

### Closest sources

1. **Permenter, “A Geodesic Interior-Point Method for Linear Optimization over Symmetric Cones” (2020/2023).**
   [arXiv with full text](https://arxiv.org/abs/2008.08047). This is the closest algorithmic and metric source. It writes the affine-invariant local norm using the quadratic representation, gives the exact symmetric-cone geodesic and distance \(\delta(u,v)=\|\log Q(u^{-1/2})v\|\), and proves a short-step *upper* bound with \(O(\sqrt n)\) dependence on the total Jordan rank \(n\). It also bounds distance/divergence between two centered points using \(n\) and the central-parameter ratio. It does not formulate a support principal minor, an exposed dual-slack rank \(Q\), or a distance from a reference point to the whole \(\varepsilon\)-optimal level set. Its geodesic algorithm updates complementary primal-dual variables and need not decompose its update into the feasible bounded Dikin chords counted locally, so the local lower bound should not be asserted for that algorithm without a separate model reduction.

2. **Hauser and Güler, “Self-Scaled Barrier Functions on Symmetric Cones and Their Classification” (2001/2002).**
   [arXiv](https://arxiv.org/abs/math/0103196). This classifies self-scaled barriers through the irreducible Euclidean-Jordan decomposition. It places the standard Jordan log-determinant in its correct structural family and prevents an exaggerated claim that the local work discovered the symmetric-cone barrier geometry. It does not give an objective-dependent distance lower bound governed by the rank of an exposing slack.

3. **Hauser and Lim, “Self-Scaled Barriers for Irreducible Symmetric Cones” (2001/2002).**
   [arXiv](https://arxiv.org/abs/math/0104020) and [publisher page](https://doi.org/10.1137/S1052623400370953). This proves that self-scaled barriers on an irreducible symmetric cone are, up to the classified transformations, homothetic versions of the universal/Jordan determinant barrier. It concerns classification, not support-minor covector norms or iteration lower bounds.

4. **Cardoso and Vieira, “On the Optimal Parameter of a Self-Concordant Barrier over a Symmetric Cone” (2003/2006).**
   [Open manuscript](https://optimization-online.org/2003/11/774/) and [publisher record](https://doi.org/10.1016/j.ejor.2004.11.027). This proves that the rank of the underlying Euclidean Jordan algebra is the Carathéodory number and hence the optimal barrier parameter for a symmetric cone, using the Güler--Tunçel characterization. That is a minimax statement about the best global barrier parameter of the whole cone. The local theorem instead uses \(Q\), the rank of one selected dual exposing slack, which may be strictly below total cone rank, and proves a concrete distance to an objective-accuracy set for the fixed standard barrier.

5. **Güler and Tunçel, “Characterization of the Barrier Parameter of Homogeneous Convex Cones” (1998).**
   [Open primary-source abstract](https://www.mcs.anl.gov/research/projects/otc/InteriorPoint/abstracts/Guler-Tuncel.html). This identifies the optimal self-concordant barrier parameter of a homogeneous cone with its Siegel-domain rank and Carathéodory number. As with Cardoso--Vieira, it neither selects a proper exposed face through a dual slack nor yields the local \(\sqrt Q\log(1/\varepsilon)\) accuracy-distance bound.

6. **Nesterov and Todd (2002)**, cited in Section 1. Their Definition 3.1, Lemma 3.2, and Corollary 3.2 already contain the exact generic conversion from bounded local-norm chords to a Riemannian-distance iteration lower bound. **Nesterov and Nemirovski (2008)** already use distance from a starting point to a whole solution set as the short-step benchmark. Neither source appears to state the support-principal-minor covector identity or an explicit objective-distance formula controlled by the rank of one exposing slack.

### Collision assessment and safe statement

The determinant, Jordan principal minors/generalized power functions, support idempotents, quadratic-representation Hessian, and Peirce decomposition are classical. The identity \(\|d[-\log\det_c(P(c)x)]\|_{x,*}=\sqrt q\) may therefore be implicit in that algebraic literature even though this screen did not locate it in the optimization literature. The strongest apparently unlocated unit is the first two, objective-specific links in the chain

\[
  \text{support-minor exact norm}
  \Longrightarrow
  \text{dual-slack-rank distance to all \(\varepsilon\)-optimal points}
  \Longrightarrow
  \text{bounded-Dikin movement lower bound},
\]

together with the Peirce-capacity lower bound on \(Q\) for product-ball lifts. The last conversion is Nesterov--Todd's Corollary 3.2 and should not be claimed as new. The local theorem's distinction from existing rank results is that \(Q\) is **objective/exposed-face dependent**, rather than the total Jordan rank or optimal global barrier parameter. Its distinction from Permenter's work is lower versus upper complexity and an explicit rank-sensitive distance to an entire accuracy set versus distance/divergence along the central path.

A cautious statement is:

> For the standard Jordan log-determinant and a fixed attained exposing slack of rank \(Q\), the support-principal-minor potential yields the stated path-independent distance to the whole objective-accuracy set. Consequently, trajectories represented by a bounded number of feasible Dikin-bounded chords per counted round obey the stated lower bound.

This does not cover custom non-self-scaled barriers, infeasible iterates, steps not representable by the counted chords, or arbitrary quantum operations. Specialist review is particularly important for the compression identity used in the support-minor norm and for possible antecedents in generalized-power/Busemann-function literature.

## 3. SOC/PSD lifts after exact fiber minimization

The relevant local note is [PSD/Lorentz reduced-oracle equivalence](2026-09-04-psd-lorentz-reduced-oracle-equivalence.md). For the fixed product-ball lift, it claims that minimizing the PSD log-determinant barrier over the redundant fiber produces the Lorentz marginal

\[
  -h\sum_{a=1}^{b}\log(1-\lVert x_a\rVert_2^2)+bh\log h,
\]

and that the residual Newton/KKT system splits into the Lorentz reduced system plus positive inactive fiber modes. Under a deliberately matched complete access model, the projected normalized solution and the exact query complexity are then identical.

### Closest sources

1. **Grone, Johnson, Sá, and Wolkowicz, “Positive Definite Completions of Partial Hermitian Matrices” (1984).**
   [Publisher page](https://doi.org/10.1016/0024-3795(84)90207-6). This is the key classical collision to acknowledge. For chordal partial matrices it gives positive-definite completion results and characterizes the unique determinant-maximizing completion through zeros in the inverse at unspecified positions. Exact fiber minimization of a log-determinant barrier is therefore not, in itself, a new idea.

2. **Barrett, Johnson, and Lundquist, “Determinantal Formulae for Matrix Completions Associated with Chordal Graphs” (1989).**
   [Publisher page](https://doi.org/10.1016/0024-3795(89)90706-4). This provides determinant formulas for maximum-determinant chordal completions. It is closely related to evaluating the minimized barrier on sparse arrowhead/star fibers.

3. **Sampourmahani, Mohammadisiahroudi, and Terlaky, “On Semidefinite Representations of Second-Order Conic Optimization Problems” (2023/2024).**
   [arXiv](https://arxiv.org/abs/2301.12007). This directly studies mappings between SOCPs and SDP representations. In particular, it explains why a naive arrowhead transformation cannot generally preserve all primal-dual and complementarity relations simultaneously, and constructs admissible maps preserving feasibility, optimality, and optimal partitions. This rules out any broad assertion that arbitrary SOC and PSD primal-dual formulations are automatically interchangeable. It does not analyze the particular maximum-determinant partial minimization, the resulting residual Hessian/KKT direct sum, or matched quantum-oracle query equivalence.

4. **Kerenidis, Prakash, and Szilágyi, “Quantum Algorithms for Second-Order Cone Programming and Support Vector Machines” (2019/2021).**
   [arXiv](https://arxiv.org/abs/1908.06720). This gives an SOCP QIPM whose cost includes condition, accuracy, tomography, and classical-output terms. It illustrates why a formulation comparison must specify access and output models. It does not prove SOC/PSD oracle equivalence after eliminating a redundant PSD fiber.

5. **Augustino, Nannicini, Terlaky, and Zuluaga, “Quantum Interior Point Methods for Semidefinite Optimization” (2021/2023).**
   [arXiv](https://arxiv.org/abs/2112.06025) and [published version](https://doi.org/10.22331/q-2023-09-11-1110). The paper analyzes direct and nullspace formulations, conditioning, feasibility, and tomography in end-to-end SDP QIPMs. These formulation effects are nearby conceptually, but no exact reduction from the local PSD packing to a Lorentz residual oracle is given.

6. **Dalzell et al., “End-to-End Resource Analysis for Quantum Interior-Point Methods and Portfolio Optimization” (2022/2023).**
   [arXiv](https://arxiv.org/abs/2211.12489) and [published version](https://doi.org/10.1103/PRXQuantum.4.040325). This accounts for block encoding, linear-system solution, tomography, and classical reconstruction in an SOCP pipeline. It reinforces that an oracle-equivalence theorem must match data-loading and readout, not only algebraic matrix dimensions. It does not supply the local two-way equivalence theorem.

### Collision assessment and safe statement

The maximum-determinant completion step is classical and must be credited as such. The apparently unlocated statement is the conjunction of:

- the closed-form marginal for this precise product-ball packing;
- a residual KKT decomposition into the Lorentz block and positive inactive modes;
- equality of the projected normalized Newton output; and
- an exact, two-way query simulation under a fully specified matched oracle.

This statement applies only to exact fiber centering and the chosen complete access contract. Approximate centering, a different PSD lift, access to only selected matrix entries, or a cost model that charges preprocessing differently can destroy the equivalence.

## 4. PSD packing of product balls and restricted barrier parameters

The relevant local notes are [PSD column packing of product balls](2026-09-04-psd-column-packing-product-balls.md) and [private-curvature frontier](2026-09-04-psd-product-ball-private-curvature-frontier.md). They track a joint ledger rather than a single lift-size statistic: number of PSD factors, per-factor capacity, selected-boundary private nullity, and the exact self-concordance parameter of the **restricted standard log-determinant barrier**.

### Closest sources

1. **Gouveia, Parrilo, and Thomas, “Lifts of Convex Sets and Cone Factorizations” (2013).**
   [Publisher page](https://doi.org/10.1287/moor.1120.0575). This gives the general equivalence between cone lifts and factorizations of slack operators. It is the right ambient language for PSD and SOC lifts, but does not calculate the local product-ball contact/nullity ledger or its restricted log-determinant parameter.

2. **Fawzi and Parrilo, “Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite Extension Complexity” (2013/2015).**
   [arXiv](https://arxiv.org/abs/1311.2571). This proves lower bounds for lifts over products of fixed-size PSD cones. It is highly relevant to “many small blocks versus larger blocks,” but its hard sets and factorization invariant differ from the product-ball full-contact/private-nullity argument, and it does not study a restricted barrier parameter.

3. **Fawzi, Gouveia, Parrilo, Robinson, and Thomas, “Positive Semidefinite Rank” (2014/2015).**
   [arXiv](https://arxiv.org/abs/1407.4095). This develops PSD rank and the geometry of semidefinite lifts. PSD rank primarily records the size of a PSD lift, whereas the local notes retain the number and sizes of separate factors and the standard-logdet parameter induced after restriction.

4. **Fawzi, “On Representing the Positive Semidefinite Cone Using the Second-Order Cone” (2016/2018).**
   [Publisher page](https://doi.org/10.1007/s10107-018-1233-0). This proves that the (3\times3) PSD cone has no representation by a finite product of second-order cones. It concerns the opposite representation direction and shows that SOC/PSD conversions have genuine structural limits. It does not address how efficiently products of balls can be packed into PSD factors.

5. **Scheiderer, “Second-Order Cone Representation for Convex Sets in the Plane” (2020/2021).**
   [Publisher page](https://doi.org/10.1137/20M133717X). This uses semidefinite extension degree, which minimizes the largest PSD block size while allowing arbitrarily many blocks. The distinction is material: extension degree intentionally forgets the factor count and therefore cannot by itself determine the sum of standard log-determinant parameters or the local capacity/private-nullity frontier.

6. **Hildebrand, “A Lower Bound on the Barrier Parameter of Barriers for Convex Cones” (2012/2014).**
   [Publisher page](https://doi.org/10.1007/s10107-012-0576-1). This supplies general lower bounds on self-concordant barrier parameters for cones. The local quantity is more specialized: it is the exact parameter of a named, restricted standard log-determinant barrier, not the best possible parameter over all barriers for the represented set.

7. **Aubrun, La Piana, and Müller-Hermes, “Factorization Through Lorentz Cones” (2026).**
   [arXiv](https://arxiv.org/abs/2606.27825). This recent work studies when positive maps factor through direct sums of Lorentz cones and classifies several source/target pairs. It is the closest 2026 structural work found involving Lorentz-factor factorizations. It does not appear to count full-contact channels for a fixed product-ball slack map or compute the restricted standard-logdet barrier parameter.

### Collision assessment and safe statement

No direct source was located for the exact private-nullity/capacity theorem or the claimed Pareto frontier for product balls. The main terminology risk is that “PSD packing complexity” can be mistaken for PSD rank, semidefinite extension degree, or psd extension complexity. The paper should define its four resources before making comparisons and should avoid suggesting a lower bound for arbitrary PSD lifts or arbitrary barriers unless separately proved.

A cautious positioning is:

> Existing lift-size measures do not retain all resources that control the standard log-determinant barrier after affine restriction. For the specified full-contact packing class, the theorem computes a sharper joint ledger and its exact restricted-barrier consequence.

## 5. Quantum output/readout lower bounds on one Lorentz cone

The relevant local note is [one-Lorentz constant-barrier value lower bound](2026-09-04-one-lorentz-constant-barrier-value-lower.md). Its family uses one cone \(Q_{2N+1}\), public two-sparse well-conditioned equalities, and reduced barrier parameter one. Depending on the access promise, the target optimum or central scalar inherits quantum query complexity

\[
  \Theta\!\left(\min\{N,C/\varepsilon\}\right),
\]

with the analogous randomized sampling law, while normalized-state preparation is constant-query and sufficiently accurate explicit classical output costs linear queries. The intended result is a separation between geometric/Newton ease and output difficulty.

### Closest sources

1. **Nayak and Wu, “The Quantum Query Complexity of Approximating the Median and Related Statistics” (1998/1999).**
   [arXiv](https://arxiv.org/abs/quant-ph/9804066). This is the primary lower-bound engine. Its approximate-counting/mean-estimation consequences give the relevant accuracy-dependent quantum query law after the hidden bit string is reduced to the conic optimum. The exponent should therefore not be described as a new quantum lower-bound technique.

2. **Brassard, Høyer, Mosca, and Tapp, “Quantum Amplitude Amplification and Estimation” (2000/2002).**
   [arXiv](https://arxiv.org/abs/quant-ph/0005055). Amplitude estimation supplies the matching upper-bound mechanism for estimating the encoded mean. It confirms that tightness comes from the inherited mean-estimation problem, not from an IPM-specific subroutine.

3. **Alase, Nghiem, and Morimae, “Tight Bound for Estimating Expectation Values from a System of Linear Equations” (2022).**
   [Publisher page](https://doi.org/10.1103/PhysRevResearch.4.023237). This gives an end-to-end accuracy-dependent lower bound for extracting a scalar expectation from a quantum linear-system solution, again via mean-estimation ideas. It is a close conceptual precedent for “the state can be available while a scalar statistic remains expensive.” Its input oracle and normalization are those of a linear-system/observable problem, not a one-Lorentz conic program with sparse public constraints.

4. **Brandão and Svore, “Quantum Speed-ups for Solving Semidefinite Programs” (2016/2017).**
   [arXiv](https://arxiv.org/abs/1609.05537). Besides algorithms, this work gives quantum query lower bounds for general sparse SDP solving. The hard instances and parameter dependence concern broad SDP input dimensions; they do not yield the local one-cone, constant-reduced-barrier, accuracy-parametric readout separation.

5. **van Apeldoorn, Gilyén, Gribling, and de Wolf, “Quantum SDP-Solvers: Better Upper and Lower Bounds” (2017/2020).**
   [arXiv](https://arxiv.org/abs/1705.01843). This proves general quantum LP/SDP query lower bounds and near-matching algorithms under specified input models. Those lower bounds are dimension- and constraint-driven worst cases, rather than a compiler into one Lorentz cone with easy normalized state output.

6. **Kerenidis, Prakash, and Szilágyi (SOCP QIPM)** and **Dalzell et al. (end-to-end SOCP analysis)**, cited above. Both make tomography/classical output an explicit part of the resource analysis. Neither gives the local trichotomy among normalized-state output, one scalar value, and a full high-accuracy optimizer on a one-cone family.

7. **Binkowski, “Practical Lower Bounds for Hybrid Quantum Interior-Point Methods in Linear Programming” (2026).**
   [arXiv](https://arxiv.org/abs/2604.24362). This derives hardware-facing runtime lower bounds for hybrid QIPM pipelines and highlights tomography/copy costs, even under favorable iteration assumptions. It is an important recent negative result but has a different scope: LP benchmarks, physical runtime and hybrid reconstruction, rather than oracle-query complexity of a single Lorentz cone.

8. **Garrido et al., “Quantum Algorithms for Second-Order Cone Programming via the Multiplicative Weights Update Method” (2025).**
   [arXiv](https://arxiv.org/abs/2507.14127). This is not an IPM, but it is relevant when stating an algorithm-independent SOCP oracle lower bound: the admissible algorithm class includes quantum SOCP methods outside path following. The local approximate-counting reduction can cover such methods only if its input/output oracle contract matches theirs.

### Collision assessment and safe statement

The lower-bound polynomial in \(1/\varepsilon\) is known from approximate counting, and the broad lesson that readout can erase linear-system speedups is also established. No source was located with all of the local structural promises simultaneously:

- a single Lorentz cone;
- reduced barrier parameter \(1\);
- public two-sparse, well-conditioned equality structure;
- public normalization/raw-norm data;
- constant-query normalized optimizer-state preparation;
- an accuracy-dependent hard optimum or central scalar;
- linear-query sufficiently accurate classical optimizer output; and
- a same-instance bounded-Dikin iteration lower bound.

Thus the potentially publishable unit is the **compiler and separation theorem**, not approximate counting itself. The theorem statement must specify whether the hidden data are available through bit queries, phase queries, state preparation, block encodings, or sample/query access. Giving a stronger state-preparation oracle can reveal the mean implicitly through normalization or amplitudes and invalidate the claimed separation unless the construction explicitly prevents that leakage.

### 5.1 Follow-up: the one-box signed parity chain

The independently audited [boxed parity-chain
note](2026-09-04-boxed-parity-chain-readout-separation.md) gives a smaller
LP-like counterexample with a different purpose.  Its public objective is
\(r_0+2r_N\), its hidden rows are
\(r_m-\sigma_mr_{m-1}=0\), and only \(r_0\in[-1,1]\) is boxed.  Eliminating
the chain changes the objective coefficient to
\(1+2\prod_m\sigma_m\), so the positive optimum is exactly \(3\) or \(1\).
Thus every multiplicative estimate of relative error \(\gamma<1/2\)
computes parity.  At the public central multiplier \(\eta=1\), the two
ordinary primal objective values are \(\sqrt{10}-1\) and \(\sqrt2-1\).

The antecedents are elementary and strong.  Beals, Buhrman, Cleve,
Mosca, and de Wolf, “Quantum Lower Bounds by Polynomials,” FOCS 1998
([arXiv](https://arxiv.org/abs/quant-ph/9802049)), supplies the standard
polynomial-method parity lower bound; the linear randomized parity bound
is classical decision-tree theory.  Signed-path matrices are diagonally
gauge-equivalent to unsigned path incidence matrices, and normalization of
a nonzero one-dimensional real vector erases its sign as a global quantum
phase.  None of these facts is new.

A targeted search did not locate their exact optimization conjunction:

- the affine-slice barrier \(-\log(1-\alpha^2)\) has exact parameter one,
  with \(\sup(\phi')^2/\phi''=1\);
- the reduced Hessian has condition one and every normalized reduced
  optimizer, center, or predictor is the same state \(|0\rangle\);
- raw sign, two-sparse coefficient, coherent row, and charged full-SQ
  access are equivalent up to constant query overhead;
- the literal equality-embedded KKT graph is a path of treewidth one and
  has condition \(\Theta(N)\) at the fixed center, while forward solution
  costs \(O(N)\); and
- the hidden nullspace basis is the prefix-parity state, so the scalar
  reduction is not free preprocessing.

The conservative contribution is this exact conjunction and access-model
counterexample.  It is not a new parity lower bound, not evidence that an
original-coordinate Newton state is free, and not an end-to-end quantum
advantage.  The barrier parameter, query cost, KKT condition, and
\(\Theta(\log(1/\epsilon))\) bounded-movement scale are simultaneous
resources and cannot be multiplied without a temporal direct-product
argument.  Boxing every chain coordinate is a different formulation with
restricted parameter \(N+1\) and fixed-center KKT condition
\(\Theta(N^2)\).

## 6. Second targeted screen: the two sharp sharing-cone barriers

This follow-up checks the exact \(q+1\) barriers in the [bounded face-sharing models note](2026-09-04-bounded-face-sharing-sharp-models.md). It changes the priority assessment: both displayed barrier formulas are classical specializations, although the local note's use of them in the slack-sharing frontier and its elementary matching lower bounds can remain useful.

### 6.1 The block-max cone \(\mathcal H_{q,s}\)

Let

\[
 \mathcal H_{q,s}=\{(t,y_1,\ldots,y_q):t\geq\lVert y_a\rVert_2
 \text{ for every }a\}.
\]

The local barrier is

\[
 F_{\mathcal H}(t,y)
 =-\sum_{a=1}^q\log(t^2-\lVert y_a\rVert_2^2)+(q-1)\log t.
\]

The decisive antecedent is **Nesterov and Nemirovskii, *Interior-Point Polynomial Algorithms in Convex Programming* (1994), Section 5.4.6**, [primary monograph chapter](https://doi.org/10.1137/1.9781611970791.ch5). For the spectral-norm cone

\[
 K_{\rm spec}=\{(t,W):t\geq\sigma_{\max}(W)\},\qquad W\in\mathbb R^{r\times m},
\]

it gives the \((r+1)\)-barrier

\[
 (r-1)\log t-\log\det(t^2I_r-WW^T).
\]

Set \(r=q\), \(m=qs\), and let row \(a\) of \(W\) occupy its own private block of \(s\) columns with entries \(y_a\). Then
\(WW^T=\operatorname{Diag}(\lVert y_1\rVert_2^2,\ldots,
\lVert y_q\rVert_2^2)\) and
\(\sigma_{\max}(W)=\max_a\lVert y_a\rVert_2\). The linear restriction of the spectral-norm cone and barrier is exactly \(\mathcal H_{q,s}\) and \(F_{\mathcal H}\). Hence the formula, its self-concordance, and the \(q+1\) upper bound are not new.

Two further primary antecedents sharpen the boundary:

- **Güler, “Barrier Functions in Interior Point Methods” (1996)**, [publisher page](https://doi.org/10.1287/moor.21.4.860), gives the infinity-norm-epigraph barrier, the \(s=1\) case of the same formula, with parameter \(q+1\).
- **Hildebrand, “A Lower Bound on the Barrier Parameter of Barriers for Convex Cones” (2013)**, [open manuscript](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf) and [publisher page](https://doi.org/10.1007/s10107-012-0576-1), constructs the optimal barrier for the \(\ell_\infty\)-epigraph cone and proves its sharp parameter through a projective lower bound.

The local restriction \(y_a=\xi_a e\) is precisely that \(\ell_\infty\)-epigraph cone, so it combines the classical spectral-norm upper bound with the classical scalar sharp lower bound to give \(\nu_{\rm opt}(\mathcal H_{q,s})=q+1\). The exact block statement may be a useful corollary, and the local derivative calculation is an independent proof, but neither should be presented as a new barrier construction. No source was located that uses this restricted barrier in the same product-ball slack-sharing factor-count/face-dimension comparison.

### 6.2 The shared-perspective cone \(\mathcal P_q\)

Let

\[
 \mathcal P_q=\{(t,u,w):t\geq0,\ w_a\geq0,\ tw_a\geq u_a^2
 \text{ for every }a\}.
\]

This is the PSD-completable partial-matrix cone for the star graph on \(q+1\) vertices: the specified \(2\times2\) clique matrices are
\(\left(\begin{smallmatrix}t&u_a\\u_a&w_a\end{smallmatrix}\right)\).
The classical chordal completion theorem of **Grone, Johnson, Sá, and Wolkowicz, “Positive Definite Completions of Partial Hermitian Matrices” (1984)**, [publisher page](https://doi.org/10.1016/0024-3795(84)90207-6), identifies positivity of all these clique matrices with positive-definite completability in the interior and characterizes the unique maximum-determinant completion.

The clique/separator determinant formulas of **Barrett, Johnson, and Lundquist, “Determinantal Formulae for Matrix Completions Associated with Chordal Graphs” (1989)**, [publisher page](https://doi.org/10.1016/0024-3795(89)90706-4), specialize on the star to

\[
 \det X_{\max\det}
 =\frac{\prod_{a=1}^q(tw_a-u_a^2)}{t^{q-1}}.
\]

Consequently the negative log maximum-determinant completion barrier is exactly

\[
 F_{\mathcal P}(t,u,w)
 =-\sum_{a=1}^q\log(tw_a-u_a^2)+(q-1)\log t.
\]

The modern direct barrier reference is **Andersen, Dahl, and Vandenberghe, “Logarithmic Barriers for Sparse Matrix Cones” (2012)**, [arXiv](https://arxiv.org/abs/1203.2742) and [author manuscript](https://www.seas.ucla.edu/~vandenbe/publications/barriers.pdf). It develops \(-\log\det\) on a sparse PSD cone, its conjugate barrier on the dual PSD-completable cone, and the maximum-determinant completion formulas for gradients and Hessians. Under the star sparsity pattern, its conjugate is \(F_{\mathcal P}\) up to an additive constant, with parameter \(q+1\). In the local notation, the arrow sparse-PSD cone \(\{M(\alpha,\beta,\gamma)\succeq0\}\) is the dual cone and \(\mathcal P_q\) is the completion cone; reversing these conventions would misstate the antecedent.

Thus the formula, the \(q+1\) upper bound, and the Legendre/max-det route are not new. The section \(u=0\) is \(\mathbb R_+^{q+1}\), giving the matching classical orthant lower bound and hence exact optimality. No source was located that isolates this exact optimality as a named theorem for the star completion cone or uses it for the local shared-perspective packing frontier. The defensible contribution is that application and joint resource accounting, not the barrier itself.

### 6.3 Updated symmetric-cone priority boundary

The second pass also found that the generic movement part of the symmetric-cone result has closer antecedents than the original wording suggested. Nesterov--Todd's Definition 3.1, Lemma 3.2, and Corollary 3.2 give exactly the bounded-Dikin-chord-to-distance conversion. Nesterov--Nemirovski's Example 1.1 explicitly shows why the relevant benchmark is distance to the whole target set rather than length of the central path, and its Section 5 uses that benchmark in short-step comparisons.

Accordingly, the candidate new unit is narrower: for the standard Jordan log-determinant, the support-principal-minor potential associated with an attained exposing slack has exact covector norm \(\sqrt Q\), and this yields the explicit objective-dependent lower bound

\[
 d_F(x^c,\mathcal X_\varepsilon)
 \geq [\sqrt Q\log(\Delta_c/\varepsilon)]_+
\]

uniformly over the whole \(\varepsilon\)-optimal set, including unbounded inactive fibers. The dependence on the **rank of the chosen exposing slack**, rather than total Jordan rank, remains the principal distinction from the screened symmetric-cone barrier and geodesic literature. The Dikin-step corollary is an application of Nesterov--Todd, not a separately new conversion theorem.

## 7. Third targeted screen: product additivity, Peirce capacity, and the one-ball premium

### 7.1 Exact product parameter for block-max cones

For any finite collection of block-max cones, the local notes prove

\[
 \nu_{\rm opt}\!\left(\prod_{\ell=1}^g
       \mathcal H_{q_\ell,s_\ell}\right)
 =\sum_{\ell=1}^g(q_\ell+1),                              \tag{S1}
\]

even when a barrier is allowed to couple all product factors. The upper bound is not new: sum the factorwise spectral-norm-cone restrictions described in Section 6.1. The lower bound uses the recession-direction theorem of Nesterov, reproduced with a precise statement as Theorem 3.9 of **Fawzi and Saunderson, “Optimal Self-Concordant Barriers for Quantum Relative Entropies” (2023)**, [publisher page](https://doi.org/10.1137/22M1500216). Embed a parameter-sharp certificate for each \(\mathcal H_{q_\ell,s_\ell}\) in its own direct summand. Joint subtraction remains feasible coordinatewise, each individual threshold subtraction is noninterior in one factor, and certificate values add. This proves (S1) for arbitrary self-concordant barriers, hence in particular for coupled LHSCBs.

This tensorization is the same direct use of published machinery that Fawzi--Saunderson employ for matrix hypograph lower bounds; it is not a new general product theorem. Merely restricting every vector block to one scalar diameter does not by itself prove the sum: a one-group boundary-ray active-facet argument loses a dimension in each other group because the vanished-group facet normals are dependent. The parameter-sharp product certificate is the clean lower-bound route. No explicit statement for products of \(\mathcal H_{q,s}\) was located, and neither the spectral-norm literature nor the sparse PSD-completion literature located in Sections 3 and 6 supplies a smaller coupled barrier. The safe label is:

> Exact derived corollary for the sharing construction; low standalone novelty. Its useful content is that factor bundling does not lower the optimal parameter even if the barrier couples all unchanged ambient factors.

This claim concerns a fixed Cartesian product. Projection to a different aggregate cone can reduce the optimal parameter, so (S1) is not a formulation-independent obstruction.

### 7.2 Exposed support rank and Peirce capacity

The antecedents split cleanly into classical geometry and an apparently unlocated optimization synthesis:

- Nesterov--Todd and Nesterov--Nemirovski already supply the short-step/distance conversion and the distance-to-target-set benchmark, as detailed in Sections 1 and 6.3.
- Permenter uses the standard quadratic-representation metric and total Jordan rank for a geodesic symmetric-cone IPM. Hauser--Güler and Cardoso--Vieira classify self-scaled barriers and identify total cone rank as the optimal global parameter. None of these sources selects the support of an objective's exposing slack.
- Generalized powers, support idempotents, Peirce decompositions, and determinant identities are classical symmetric-cone material. **Lemmens, “Horofunction Compactifications of Symmetric Cones under Finsler Distances” (2022/2023)**, [arXiv](https://arxiv.org/abs/2111.12468) and [publisher page](https://doi.org/10.54330/afm.141190), is nearby modern primary work connecting Jordan faces and horofunction boundaries. Its metrics are the Thompson and Hilbert Finsler metrics, not the Hessian Riemannian metric of the log-determinant barrier, and it gives no objective-accuracy or Dikin-iteration theorem.
- **Aubrun, La Piana, and Müller-Hermes, “Factorization Through Lorentz Cones” (2026)**, [arXiv](https://arxiv.org/abs/2606.27825), studies which positive *linear maps* between proper cones factor through direct sums of Lorentz cones. Its rank and facial arguments do not treat nonlinear primal/dual slack factorizations of a product-ball slack operator, contact mixed derivatives, or the quantitative inequality \(\sum_a(s_a-1)\leq\sum_i a_ip_iq_i\).
- Fawzi's SOC nonrepresentability theorem and semidefinite-extension-degree results concern existence or maximum block size, not the local Peirce curvature delivered per exposed-rank unit.

No primary source was located for either the explicit distance formula

\[
 d_F(x^c,\mathcal X_\varepsilon)
 \geq[\sqrt Q\log(\Delta_c/\varepsilon)]_+
\]

with \(Q\) the rank of one attained exposing slack, or the product-ball capacity implication

\[
 \sum_a(s_a-1)\leq\sum_i a_ip_iq_i\leq\kappa Q.
\]

The support-minor's constant norm is likely classical generalized-power/Busemann geometry and should not be claimed alone. The candidate contribution is the objective-dependent distance formula, its uniformity over inactive fibers, and its coupling to contact-curvature capacity. This remains a targeted negative search result, not a priority opinion; terminology from harmonic analysis and symmetric spaces is a significant residual search risk.

### 7.3 One-ball support-objective premium

For a globally labelled bi-\(C^1\) factorization of the slack operator of \(B_2^N\) over symmetric-cone factors of dimension at most \(d<N+1\), with a fixed global dual-certificate sheet, the local theorem says that some unit support objective has

\[
 Q\geq\left\lceil\frac{N}{d-2}\right\rceil.             \tag{S2}
\]

The only new case beyond the local numerator \(N-1\) is the divisible one: if \(N-1=L(d-2)\), assuming \(Q=L\) for every support objective forces equality in all curvature-capacity inequalities. Active factors then have rank two and maximal allowed dimension, and the joint support map would give a finite covering

\[
 S^{L(d-2)}\longrightarrow(S^{d-2})^L.
\]

For \(L>1\), this contradicts fundamental group when \(d=3\), and intermediate cohomology when \(d>3\). Thus at least one objective has \(Q\geq L+1\). The covering and cohomology facts are standard topology; the literature question is whether this argument has been applied to smooth cone-factorization support sheets.

The closest formulation paper located is **Kobayashi, Kim, and Kojima, “Sparse Second Order Cone Programming Formulations for Convex Optimization Problems” (2008)**, [open primary paper](https://doi.org/10.15807/jorsj.51.241). It compares equivalent SOCP formulations created by auxiliary variables, relates their sparsity to the Schur complement, and recommends formulations with fewer auxiliaries/larger cones. It gives no lower bound under a cone-dimension cap, no globally smooth contact-selection hypothesis, and no support-rank or topological obstruction. Standard Lorentz norm trees are likewise construction precedents, not collisions with (S2).

General lift/factorization theory (Gouveia--Parrilo--Thomas), Fawzi's impossibility of representing \(S_+^3\) by a finite SOC product, and Aubrun--La Piana--Müller-Hermes's Lorentz-factorization property address different questions. None was found to prove (S2), to count the rank of a summed support certificate, or to use a sphere-to-product covering obstruction.

The conservative novelty label is:

> Plausible candidate theorem in the globally labelled bi-\(C^1\), fixed-certificate-sheet model. It is existential in the objective. It is not an unconditional lower bound for arbitrary affine lifts, nonsmooth norm-tree formulations, every boundary objective, arbitrary barriers, or arbitrary QIPMs.

Because the theorem depends critically on turning equality into a global finite covering, publication use should spell out constant active labels, properness/local-diffeomorphism, connected components, and the fixed-sheet hypothesis rather than citing topology informally.

## 8. QIPM landscape check through the screen date

The following primary QIPM sources were also checked for overlap:

- **Augustino, Nannicini, Terlaky, and Zuluaga, “Quantum Interior Point Methods for Second-Order Cone Optimization Problems.”** [Open technical report](https://engineering.lehigh.edu/sites/engineering.lehigh.edu/files/_DEPARTMENTS/ise/pdf/tech-papers/21/21T_009a.pdf). Short-step primal-dual SOCP QIPMs, inexact feasibility, iterative refinement, QRAM assumptions, and condition dependence; no matching lower-bound family located.
- **Wu et al., “A Preconditioned Inexact Infeasible Quantum Interior Point Method for Linear Optimization” (2024; later publication).** [arXiv](https://arxiv.org/abs/2412.11307). Preconditioning and inexact infeasible linear optimization; not the sparse conic packing or readout lower bounds screened here.
- **Mohammadisiahroudi et al., “An Inexact Feasible Quantum Interior Point Method with Optimal Iteration Complexity for Linear Optimization” (2025).** [arXiv](https://arxiv.org/abs/2512.04510). Improved linear-optimization scaling; not a conic formulation or output lower-bound collision.
- **Apers and Gribling, “Quantum Speedups for Linear Programming via Interior Point Methods” (2026).** [SIAM Journal on Computing](https://doi.org/10.1137/25M1736098). Their tall-LP algorithm explicitly outputs a feasible \(\epsilon\)-optimal point in time \(\sqrt n\,\mathrm{poly}(d,\log n,\log(1/\epsilon))\), using quantum spectral approximation and multivariate mean estimation. This is an algorithmic upper bound in its row-access model, not a sparse product-cone movement or readout lower bound.
- **Mohammadisiahroudi et al., “Quantum Interior Point Methods: A Review of Developments and an Optimally Scaling Framework” (2025/2026).** [arXiv](https://arxiv.org/abs/2512.06224). Besides reviewing feasible/infeasible QIPMs, iterative refinement, preconditioning, QLSAs, and tomography, it proposes an almost-exact LP framework under QRAM assumptions and analyzes the dense \(m=O(n)\) regime. It does not state a formulation-universal geometric lower bound.
- **Binkowski, “Practical Lower Bounds for Hybrid Quantum Interior Point Methods in Linear Programming” (2026).** [arXiv](https://arxiv.org/abs/2604.24362). This is the nearest paper using the words “lower bounds” for QIPMs: it derives rigorous hardware-runtime floors for specified hybrid QLSA/IPM pipelines and compares them empirically with HiGHS on benchmark instances. Its conclusion is a practical exclusion result under explicit implementation and hardware assumptions, not an oracle query lower bound, an output-information lower bound, or a self-concordant movement theorem.

These papers also caution against treating the number of Newton steps as the full quantum complexity. Data access, condition numbers, state preparation, tomography, precision, feasibility restoration, and iterative refinement may dominate.

## 9. Recommended claim language and verification priorities

### Claim language

- Use “we did not locate a direct antecedent in a targeted open-literature search through 2026-09-04,” not “this is the first” or “this is known to be new.”
- Call the iteration results **model-specific geometric lower bounds** and name the fixed barrier, starting point, feasibility requirement, and local-step cap.
- For the symmetric-cone theorem, distinguish exposed dual rank from total Jordan rank and from the optimal barrier parameter. Credit the Jordan/principal-minor identities as classical and claim, at most, the objective-distance/iteration application.
- Credit maximum-determinant completion for the partial-minimization principle. Isolate the new candidate as the exact reduced KKT/output/oracle theorem.
- Distinguish the local packing ledger from PSD rank, semidefinite extension degree, and minimum barrier parameter over all barriers.
- Credit Nayak--Wu/mean estimation for the query exponent. Present the one-Lorentz result as a structure-preserving reduction plus output-separation theorem.
- Treat both \(q+1\) sharing-cone barriers as classical specializations. Claim only the new packing/slack-sharing consequences that survive a separate priority check.
- Describe exact additivity for products of \(\mathcal H_{q,s}\) as a tensorized-certificate corollary of Nesterov's published theorem, not as a new barrier lower-bound technique.
- State the one-ball \(Q\geq L+1\) premium only with the global bi-\(C^1\), fixed-certificate-sheet, dimension-cap, and existential-objective hypotheses.
- For the Hermitian sequential-contact result, credit Fawzi--Gouveia--Parrilo--Robinson--Thomas Theorem 2.10 for the PSD range-compression motif. Isolate the candidate contribution as smooth contact selection, the exact field-dependent capacity/exception arithmetic, one weighted aggregate exposing rank, and the restricted-standard-slice consequence.
- State every quantum lower bound together with its input oracle, output type, success probability, precision convention, and whether preprocessing or advice is allowed.

### Highest-priority follow-up checks

1. Ask a specialist in chordal completion/sparse SDP barriers whether the precise residual KKT direct-sum identity is already implicit in multifrontal or clique-tree barrier elimination results.
2. Search cone-factorization terminology beyond “packing,” especially *PSD cone rank*, *block-PSD rank*, *semidefinite extension degree*, *factor-width cones*, and *Lorentz cone rank*.
3. Formalize two simulations for every oracle-equivalence statement. An algebraic equality of reduced systems is insufficient when one formulation makes index maps, normalizers, or fiber centers costly.
4. Stress-test the one-Lorentz lower bound under stronger QRAM/state-preparation access. Determine exactly which extra scalar (normalization, success amplitude, or preparation cost) leaks the Hamming weight.
5. Separate an exact-central-path claim from a finite-precision QIPM claim. Approximate fiber centering can introduce residual modes whose conditioning or required precision changes the cost.
6. Search the harmonic-analysis and nonpositively-curved-geometry literature for generalized-power or Busemann functions whose Riemannian gradients have constant norm; such a result could anticipate the support-minor lemma even if it has not been used as an IPM lower bound.

## Bottom line

The targeted screen found no exact match for the narrow combined theorems in the local notes, but it substantially narrows what can responsibly be claimed:

- fixed-barrier distance formulas may be new calculations, while barrier geometry and IPM iteration lower bounds are not new;
- the exposed-rank symmetric-cone theorem appears distinct from known total-rank barrier-parameter and central-path-distance results, while all of its Jordan-algebra ingredients are classical;
- maximum-determinant fiber minimization is classical, while the complete reduced-KKT and matched-query equivalence was not located;
- lift-size theory is mature, while the proposed four-resource product-ball packing ledger was not located; and
- approximate-counting readout lower bounds are classical, while the promised one-Lorentz sparse compilation and simultaneous state/scalar/full-output separation was not located;
- the two displayed \(q+1\) sharing-cone barriers are classical spectral-norm and chordal-completion specializations; only their exact role in the local joint resource frontier remains a candidate contribution;
- their coupled product parameter is an immediate certificate-tensorization corollary with low standalone novelty;
- the exposed-rank/Peirce-capacity synthesis and the one-ball support-objective premium were not located, but their priority remains tentative and their narrow regularity and fixed-barrier hypotheses are essential.

These are promising candidate contributions, not certified novelty claims. A publication should retain the narrow hypotheses and add expert/citation-index review before asserting priority.

## 10. Fourth targeted screen: dimension-only arbitrary product-cone movement

The local theorem in
[dimension-only arbitrary-cone primal--dual movement](2026-09-04-dimension-only-arbitrary-cone-primal-dual-movement.md)
starts from an exact lift of a full-dimensional compact body in
\(\mathbb R^D\) over a product \(\prod_iK_i\), assumes only
\(\dim K_i\leq d\), and proves

\[
 \nu\geq\Psi_d(D+1),\qquad
 \Psi_d(h)=2\lfloor h/d\rfloor+
             \min\{h\bmod d,2\}.
\]

It then inserts this parameter bound into a Nesterov--Todd primal--dual
distance estimate. The targeted screen separated four antecedent layers.

1. **Slack factorization and ordinary rank.** Gouveia, Parrilo, and
   Thomas, “Lifts of Convex Sets and Cone Factorizations,” *Mathematics of
   Operations Research* 38 (2013), Theorem 2.4
   ([arXiv](https://arxiv.org/abs/1111.3164),
   [publisher](https://doi.org/10.1287/moor.1120.0575)), establish the
   proper-lift/slack-factorization equivalence. After minimal-face
   reduction, the local factorization is an application of that direction
   relative to the operational face. Rank \(D+1\) of the normalized slack
   operator and \(D+1\leq\sum_i\dim K_i\) are elementary affine/bilinear
   rank consequences, not new cone-rank theory.

2. **Orthant sections and barrier charge.** Restriction to a linear
   section is standard self-concordant-barrier calculus. Every
   two-dimensional proper cone is linearly equivalent to
   \(\mathbb R_+^2\), and the sharp orthant parameter is classical; nearby
   primary lower-bound sources include Güler--Tunçel's homogeneous-cone
   characterization and Hildebrand's projective lower-bound theorem
   ([open manuscript](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf),
   [publisher](https://doi.org/10.1007/s10107-012-0576-1)). The useful
   detail in the local proof is to take a single product section
   \(\mathbb R_+^{r+2q}\). It therefore bounds a barrier that couples the
   factors and does not assume additivity of optimal barrier parameters.

3. **Dimension-capped lift obstructions.** Fawzi and Parrilo
   ([arXiv](https://arxiv.org/abs/1311.2571)) study products of fixed-size
   PSD cones and prove exponential block-count lower bounds for the cut
   polytope. Saunderson
   ([arXiv](https://arxiv.org/abs/1902.06401), Theorem 1.4) rules out
   finite product lifts by cones with short face chains for neighborly
   source cones. These are the closest product/dimension-cap results
   located. They are family- and structure-specific lift-complexity
   theorems, not a universal barrier-parameter or Dikin-movement theorem
   for every full-dimensional compact body. Lee--Yue's sharp
   \(n\)-self-concordance theorem for the universal barrier
   ([arXiv](https://arxiv.org/abs/1809.03011)) runs in the other direction:
   it is a dimension-only upper bound on a barrier for an arbitrary
   domain.

4. **Primal--dual movement.** Nesterov and Todd
   ([author manuscript](https://people.orie.cornell.edu/miketodd/NTRiemann.pdf),
   [publisher](https://doi.org/10.1007/s102080010032)) already give the
   bounded-short-step conversion in Definition 3.1, Lemma 3.2, and
   Corollary 3.2. Their Theorem 5.1(c), product geometry, and Theorem 5.2
   contain the central-point/gap Riemannian ingredients from which the
   local endpoint-set bound is extracted. Thus the local theorem's
   Riemannian factor and chord denominator are applications, not new
   geometric principles.

Exact-phrase, concept, and citation-neighborhood searches did not locate a
primary source explicitly performing the remaining integer synthesis

\[
 D+1\leq r+dq,\qquad \nu\geq r+2q
 \quad\Longrightarrow\quad
 \nu\geq\Psi_d(D+1),
\]

or feeding it into Nesterov--Todd distance for arbitrary product-cone
lifts, including products of Euclidean balls. The defensible status is
therefore **apparently unlocated derived theorem with modest standalone
novelty**. Its value is breadth and exact residue accounting, not a new
lower-bound technique. The screen is targeted and non-exhaustive, so no
priority claim is warranted.

The exclusions are material: the parameter lower bound concerns a
coupled LHSC barrier on the operational **product cone**, not an arbitrary
barrier on the affine slice or projected body; the movement corollary
requires a primal--dual gap endpoint and bounded Dikin chords; and neither
statement is a quantum query lower bound or an obstruction to
unrestricted long steps.

## 11. Fifth targeted screen: Hermitian sequential contact and standard-slice frontier

The audited theorem in
[Hermitian sequential-contact range frontier](2026-09-04-hermitian-sequential-contact-range-frontier.md)
uses globally labelled bi-\(C^1\) factorizations of product-ball slack by
products of \(H_+^{r_i}(\mathbb F)\), \(r_i\leq R\), for
\(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\). It chooses one contact
per source ball and proves the additive lower bound

\[
 \sum_i\operatorname{rank}_{\mathbb F}
 \left(\sum_a\lambda_aY_i^a(u_a)\right)
 \geq\sum_a\kappa_{\mathbb F,R}(s_a)
 \qquad(\lambda_a>0),
\]

then derives the matching restricted-standard-logdet barrier frontier.
The closest primary sources divide into four groups.

### 11.1 A direct methodological antecedent

Theorem 2.10 of Fawzi, Gouveia, Parrilo, Robinson, and Thomas,
“Positive Semidefinite Rank,” *Mathematical Programming* 153 (2015)
([arXiv](https://arxiv.org/abs/1407.4095),
[publisher](https://doi.org/10.1007/s10107-015-0922-1)), proves

\[
 \operatorname{rank}_{\rm psd}
 \begin{pmatrix}P&0\\Q&S\end{pmatrix}
 \geq \operatorname{rank}_{\rm psd}(P)+
      \operatorname{rank}_{\rm psd}(S),
\]

with equality for a block-diagonal matrix. Its proof takes the span of the
column-factor ranges paired with the zero block, places the corresponding
row factors in the orthogonal complement, and compresses the two diagonal
subproblems onto complementary subspaces. This is a direct antecedent for
the linear-algebraic idea in the local sequential compression. The
compression/telescoping motif is therefore not new by itself.

The claims differ in their mathematical outputs. The published theorem
has a finite block-triangular matrix and lower-bounds the order of one real
PSD factorization. The local product-ball slack is an infinite smooth
cylindrical family rather than a presented block-triangular matrix. The
local proof must choose contacts sequentially, show that previous contact
ranges remain in the kernel under every future-coordinate variation,
invoke a sharp field-dependent one-ball lemma in each quotient, and
produce a **single simultaneous contact** whose positively weighted dual
sum has large rank. Ordinary PSD rank does not record that exposed rank.

### 11.2 PSD-rank and extension-complexity measures

Gouveia--Parrilo--Thomas
([publisher](https://doi.org/10.1287/moor.1120.0575)) supply the basic
lift/factorization correspondence. Fawzi--Parrilo
([arXiv](https://arxiv.org/abs/1311.2571)) prove block-count lower bounds
for products of fixed-order real PSD cones on specific hard polytopes.
Fawzi's SOC-rank obstruction
([publisher](https://doi.org/10.1007/s10107-018-1233-0)) also decomposes a
product-cone factorization into summands and exploits zero patterns. None
of these sources was found to select smooth simultaneous support contacts
or count the rank of their weighted summed exposing certificates.

Semidefinite extension degree minimizes the largest real PSD block and
allows any finite number of blocks. Scheiderer's formulation
([arXiv](https://arxiv.org/abs/2004.04196),
[publisher](https://doi.org/10.1137/20M133717X)) makes this distinction
explicit. This measure intentionally loses the number of blocks, their
contact ranks, and the restricted product-logdet parameter, so even the
fact that Euclidean balls are SOC-representable does not collide with the
local capped-block additive frontier.

Kummer's “Two Results on the Size of Spectrahedral Descriptions”
([arXiv](https://arxiv.org/abs/1506.07699),
[publisher](https://doi.org/10.1137/15M1030789)) is the closest ball-specific
matrix-size lower bound: a direct real LMI for the \(N\)-ball needs order
at least \(N/2\), with stronger cases at certain dimensions. It excludes
projections and products of smaller cones and says nothing about exposed
dual rank or a restricted barrier, so neither theorem implies the other.

Fawzi--Safey El Din's convex-body PSD-rank bound
([arXiv](https://arxiv.org/abs/1705.06996),
[publisher](https://doi.org/10.1137/17M1142570)) uses the algebraic degree
of the polar boundary; it is weak on a quadratic ball and does not count
capped blocks. Soh--Varvitsiotis
([publisher](https://doi.org/10.1007/s10107-023-02015-6)) treat
finite-matrix factorizations over general symmetric cones, and
Brown--Pashkovich--Tunçel
([arXiv](https://arxiv.org/abs/2501.03025)) treat normalization of cone
factorizations. Neither was found to contain the continuous
contact-capacity, simultaneous exposed-rank, or restricted-barrier
statement screened here.

### 11.3 Field dependence

The 2015 PSD-rank paper discusses real and complex Hermitian PSD rank, and
Bogart, Gouveia, and Torres
([arXiv](https://arxiv.org/abs/2110.08158),
[publisher](https://doi.org/10.1142/S0219498824500257)) develop complex
PSD-minimality for low-dimensional polytopes. Their invariant is minimum
matrix order, not the real tangent-channel capacity
\(\delta pq\), the per-block capacity \(\delta(R-1)\), or the rank of a
summed support certificate. Quaternionic Hermitian PSD cones are standard
symmetric cones, but no primary optimization paper was located that
develops a quaternionic PSD-rank/lift invariant in parallel with complex
PSD rank and combines it with these exact constants. The identities
\(H_+^2(\mathbb R)\cong Q_3\),
\(H_+^2(\mathbb C)\cong Q_4\), and
\(H_+^2(\mathbb H)\cong Q_6\), as well as the associated projective-space
geometry, are classical symmetric-cone facts; only their exact use in the
frontier is a candidate contribution.

### 11.4 Barrier boundary

The Jordan log-determinant and the fact that total Jordan rank is the
optimal parameter on a full symmetric cone are classical; see Cardoso--Vieira
([open manuscript](https://optimization-online.org/wp-content/uploads/2003/11/774.pdf),
[publisher](https://doi.org/10.1016/j.ejor.2004.11.027)) and the earlier
Güler--Tunçel characterization. Affine restriction preserves
self-concordance, the ball barrier \(-\log(1-\lVert x\rVert^2)\) has
gradient parameter one under the convention used here, and summing factor
barriers gives the standard upper bound. These facts do not optimize the gradient parameter of the standard
product log-determinant after restriction to an arbitrary lifted affine
slice. No screened source gives the exact sum
\(\sum_a\kappa_{\mathbb F,R}(s_a)\), its residue arithmetic, or exactly
the three direct order-two spin exceptions.

The resulting conservative assessment is:

> The PSD range-compression proof pattern is prior art. No primary source
> was located with the sharp field-uniform one-ball contact lemma, the
> sequential simultaneous-contact theorem for a positive weighted dual
> sum, or the exact all-field standard-slice barrier frontier. Treat these
> as candidate derived results under the stated global bi-\(C^1\), finite
> labelling, order-cap, genuine-certificate, and common-slice assumptions.

This conclusion is a targeted negative search, not a priority opinion.
The theorem is not additivity of ordinary PSD rank, not a lower bound on
semidefinite extension degree, not a statement for unlabelled/nonsmooth
lifts, and not a lower bound for custom barriers or quantum queries.

## 12. Sixth targeted screen: selection-free affine PSD compression

The relevant local result is
[Affine PSD lifts need no selected contact sheets in the real one-channel
regime](2026-09-04-affine-psd-sequential-compression-without-selections.md).
For an arbitrary finite relative-Slater affine real-PSD lift of
\((B_2^s)^b\) with block orders at most \(s\), it constructs genuine
pure-row dual certificates whose every positive weighted sum has rank at
least \(2b\).  Every lift fiber at their simultaneous contact has nullity
at least \(2b\).  This gives both the exact restricted standard-logdet
parameter \(2b\) and the corresponding exposed-rank metric coefficient
\(\sqrt{2b}\), without selected primal or dual sheets.

The basic lift--slack-factorization correspondence is classical; see
Gouveia, Parrilo, and Thomas,
[*Lifts of Convex Sets and Cone Factorizations*](https://doi.org/10.1287/moor.1120.0575).
Their Theorem 2.4 proof already constructs, for each polar support
functional, a nonempty convex dual feasible set and defines the dual factor
by choosing **any** normalized point in it.  The resulting affine identity
holds for every point in the lifted slice.  Thus the certificate fiber and
the fact that a fixed zero-slack certificate annihilates every primal lift
over its exposed contact are antecedents, not new parts of the local result.
Fixed-block PSD extension lower bounds are also established, notably in
Fawzi and Parrilo,
[*Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite
Extension Complexity*](https://arxiv.org/abs/1311.2571).  Those works do
not track the rank of an attained support-certificate fiber, simultaneous
row contacts, every-fiber boundary nullity, or a restricted standard
barrier.

Fawzi, Gouveia, Parrilo, Robinson, and Thomas,
[*Positive Semidefinite Rank*](https://doi.org/10.1007/s10107-015-0922-1),
are the direct methodological boundary.  Proposition 6.1 uses the SDP
feasible set of all valid factors on one side to select low-rank members.
Section 7 studies the full space of finite PSD factorizations and proves a
homeomorphism to nested PSD-cone images in a dimension-tight case, as well
as connectedness at ordinary rank three/PSD rank two.  Theorem 2.10 proves
block-triangular additivity by spanning factor ranges, placing that span in
common kernels, and compressing to orthogonal subspaces.  Therefore the
range-compression algebra in the local proof is prior art.  Its unlocated
part is the compact convex-fiber dichotomy over a continuum of supports and
the recursive preservation of original global certificates.

Dawson, Hoşten, Kubjas, and Metsälampi,
[*Uniqueness of size-2 positive semidefinite matrix
factorizations*](https://arxiv.org/abs/2410.18891) (v2, 2026), use local and
global rigidity to characterize when one finite rank-three matrix has a
unique size-two factorization up to \(GL(2)\).  This is close prior art for
factorization uniqueness, but it neither studies a support-indexed convex
dual fiber nor derives a sphere-to-projective-space obstruction.  Vill,
[*Integrating Spectrahedra*](https://doi.org/10.1007/s00454-025-00719-4),
uses all compact primal PSD fibers and measurable sections to build a fiber
body and transfer face/normal-cone information.  It is a direct whole-fiber
spectrahedral comparator, but not an extension-complexity theorem about
dual certificate rank; it explicitly leaves dual/KKT-certificate fiber-body
questions for future work.

Targeted primary-source searches for spectrahedral lifts, dual-certificate
continuity, factorization-space topology, minimal faces, semidefinite
extension degree of balls, and projective support maps found no direct
collision.  The apparently unlocated synthesis is:

1. if all certificates in one convex fiber have total rank one, their
   average forces one common block and range;
2. strict-feasibility normalization makes that fiber a singleton and its
   closed graph makes the rank-one branch continuous;
3. support coefficients make the resulting sphere-to-projective-space map
   injective, contradicting covering dimension or invariance of domain; and
4. compressing the **global** row-certificate fibers, rather than selecting
   duals only after facial reduction, preserves genuine pure-row identities
   and makes the rank increments telescope.

The field and regularity boundary is substantive.  A binary
\(\mathbb S_+^2\) norm chain for \(B_2^s\) has a unique support certificate
whose total rank is at most \(s-1\) for every direction, below the smooth
real-order-two value \(s\).  Thus unique fibers, semialgebraicity, and
generic analyticity do not make the higher-rank exposed-rank theorem
automatic.  The independently audited companion
[exact PSD2 theorem](2026-09-04-selection-free-psd2-product-ball-exposed-rank.md)
also proves the matching lower bound: over all finite affine real PSD2
lifts of \(\prod_dB_2^{s_d}\), the exact minimax rank of a favorable positive
aggregate of genuine row-support certificates is \(\sum_d(s_d-1)\).  Its local
one-ball argument uses only semialgebraic generic \(C^1\) strata, while
compression of the original global certificate fibers makes the rank
increments additive.  No source located in this screen states this exact
support-certificate minimax law.  On the primal side, two
\(H_+^2(\mathbb C)\cong Q_4\) blocks give the norm-tree lift
\((t,a)\in Q_4,(1,t,b)\in Q_4\) of \(B_2^5\), with generic total nullity
two.  At the seam, however,
the first primal block is a vertex of nullity two and the second has
nullity one, recovering total three.  The quaternionic two-\(Q_6\) lift of
\(B_2^9\) behaves the same way.  These semialgebraic Slater examples show
that generic smooth strata cannot prove a nullity theorem, but they do not
refute one: the missing primal nullity appears exactly where normalized
contact sheets cease to be differentiable.  The safe novelty label is presently
**candidate selection-free critical-real affine-lift theorem; exact
synthesis not located**, including its exposed-rank strengthening.  This is
not a claim that certificate fibers, factorization-space topology, or range
compression themselves are new.  The unconditional higher-rank exposed-rank
extension is false; an every-fiber nullity/standard-barrier extension remains
open.

The independently audited [arbitrary-cap Lorentz
extension](2026-09-04-selection-free-exposed-rank-premium-counterexample.md)
sharpens the same boundary for one ball.  Under factor-dimension cap \(d\),
the exact affine-lift quantity
\(\inf_{\mathcal L}\max_v\min_{Z\in\mathcal D_{\mathcal L}(v)}
\operatorname{rank}_JZ\) is
\(\lceil(s-1)/(d-2)\rceil\).  The grouped norm-chain certificate is unique,
and both the unique primal boundary fiber and dual certificate are globally
Lipschitz semialgebraic selections.  Hence uniqueness, bi-Lipschitz
regularity, and generic analyticity still do not recover the smooth
premium.  The restricted standard barrier on that explicit chain has exact
parameter \(2\lceil(s-1)/(d-2)\rceil-1\).
For heterogeneous product balls, sequential compression of the original
pure-row certificate fibers and independent chains also give the exact
favorable-aggregate minimax
\(\sum_a\lceil(s_a-1)/(d-2)\rceil\).  This is distinct from, and does not
settle, the minimum rank over the full aggregate-objective certificate
fiber.

The independently audited [rotated-Lorentz perspective
counterexample](2026-09-04-rotated-lorentz-fiberwise-nullity-counterexample.md)
closes the proposed every-fiber strengthening negatively.  With
\(q=\lceil(s-1)/(d-2)\rceil\), every boundary fiber has a completion of
nullity \(q\), and every support-certificate fiber has maximum rank \(q\).
At the exceptional pole, however, the fiber is a simplex whose vertices
have nullity \(2q-1\), making the restricted standard barrier parameter
exactly \(2q-1\).  The formulation is an elementary rotated-SOC
perspective; the candidate new point is the exact three-way separation of
minimum fiber nullity, maximum exposed rank, and restricted barrier
parameter, not the perspective construction itself.

The independently audited [selection-free Lorentz standard-barrier
theorem](2026-09-04-selection-free-lorentz-standard-barrier-cap.md)
nevertheless closes the unrestricted affine-lift barrier frontier in every
nondivisible cap case and for every unbounded lift.  Its new ingredient is
a two-scale recession formula: recession Jordan rank and boundary nullity
in the complementary face contribute additively to the restricted gradient
parameter.  In the remaining bounded divisible regime, a compact
non-singleton fiber with minimum nullity \(r\) must contain a chord endpoint
of nullity at least \(r+1\).  No screened source states this precise capped
Lorentz barrier/recession reduction; the bounded projection-singular case
remains open.

A second primary-source screen on 2026-09-04 sharpened the provenance.
Ben-Tal--Nemirovski's
[*Lectures on Modern Convex Optimization*, Chapter 3](https://doi.org/10.1137/1.9780898718829.ch3)
and their
[*On Polyhedral Approximations of the Second-Order Cone*](https://doi.org/10.1287/moor.26.2.193.10561)
are antecedents for SOC modelling and the tower-of-variables idea.
Vielma--Ahmed--Nemhauser,
[*A Lifted Linear Programming Branch-and-Bound Algorithm for Mixed-Integer
Conic Quadratic Programs*](https://doi.org/10.1287/ijoc.1070.0256),
Section 3, explicitly recurse from a high-dimensional Lorentz cone through
paired norm variables and three-dimensional Lorentz factors.  Thus neither
norm trees nor small-cone decompositions are new.  Gouveia--Parrilo--Thomas
give the lift/slack-factorization and support-certificate framework, while
Fawzi's
[*On Representing the Positive Semidefinite Cone Using the Second-Order
Cone*](https://doi.org/10.1007/s10107-018-1233-0), Definition 2 and
Remark 2, defines ordinary SOC rank by the number of \(Q_3\) factors in a
global factorization and records the decomposition viewpoint.

That ordinary factor count is not the new minimax: a fixed lift can have
many factors while a seam support has only one nonzero Jordan-rank
certificate unit.  No screened source optimizes
\(\max_v\min_{Z\in\mathcal D(v)}\operatorname{rank}_J Z\), proves its
dimension-capped value, proves all-support uniqueness for the chain, or
identifies the strict one-unit smooth-versus-seam gap in exactly the
divisible cases.  The safe label is **candidate exact support-certificate
minimax synthesis; no direct statement located in a targeted
primary-source screen**, not a claim of priority for its classical
ingredients.

This remains a targeted negative screen, not a priority determination.

## 13. Seventh targeted screen: arbitrary affine PSD ball barrier cap

The companion
[arbitrary affine PSD ball cap note](2026-09-04-arbitrary-affine-psd-ball-barrier-cap.md)
asks whether every relative-Slater affine real-PSD lift of \(B_2^N\), with
block orders at most \(R\), makes the restricted standard product logdet
pay \(\lceil N/(R-1)\rceil\), apart from the direct \(B_2^2\) spin slice.
It proves the universal local bound
\(\lceil(N-1)/(R-1)\rceil\), hence the conjectured value in every
nondivisible case, and uses the convex-certificate-fiber theorem to close
the first divisible case \(N=R\geq3\).  A two-scale determinant lemma also
shows that a nonzero PSD recession direction contributes its rank in
addition to boundary nullity compressed to its orthogonal complement.
Thus every unbounded lift pays the missing unit; only bounded
projection-singular branching remains open when
\(N-1=q(R-1)\), \(q\geq2\).

The closest primary sources separate cleanly.  Gouveia--Parrilo--Thomas
give the lift/factorization and dual-certificate framework.
Fawzi--Parrilo's
[*Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite
Extension Complexity*](https://arxiv.org/abs/1311.2571) counts required
fixed-order factors for selected slack matrices.  Fawzi's
[*On Representing the Positive Semidefinite Cone Using the Second-Order
Cone*](https://doi.org/10.1007/s10107-018-1233-0) studies SOC
factorization rank and nonrepresentability, and Aubrun--La
Piana--Müller-Hermes,
[*Factorization through Lorentz cones*](https://arxiv.org/abs/2606.27825),
studies positive-map factorizations.  None of these sources studies the
least gradient parameter of a standard product logdet on an arbitrary
affine lift slice, or adds recession rank to compressed boundary nullity.
No primary source located in the targeted screen settles the remaining
bounded divisible case.  The conservative label is **candidate partial
cap theorem with a new recession reduction; full conjecture open**.

The independently hostile-audited
[Hermitian extension](2026-09-04-selection-free-hermitian-standard-barrier-cap.md)
uses the same local and recession mechanisms over
\(H_+^r(\mathbb F)\), \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\).
Writing \(a=\dim_{\mathbb R}\mathbb F\), the cross-Peirce channel has real
dimension \(a p_iq_i\), so an order cap \(R\) gives the selection-free
bound
\[
 \nu_{\rm std,slice}\geq
 \left\lceil {N-1\over a(R-1)}\right\rceil .
\]
It matches grouped Hermitian Schur blocks in every nondivisible case and
the direct rank-two spin cases.  The independently audited
[one-channel rigidity theorem](2026-09-04-selection-free-hermitian-one-channel-rigidity.md)
also closes every non-spin case \(N-1=a(R-1)\) at value two: a hypothetical
parameter-one lift makes the full normalized certificate fiber a continuous
rank-one singleton and embeds the support sphere into
\(\mathbb FP^{R-1}\), which is a sphere only for the rank-two projective
lines.  Compressing the original global pure-row certificate fibers makes
the result additive: for \(b\) non-spin critical source balls, one
simultaneous contact forces positive aggregate rank and every-fiber
nullity at least \(2b\), and separate grouped lifts attain the exact
standard-slice value \(2b\).  The two-scale Peirce--Schur determinant
formula adds recession rank to complementary-face nullity, so every
unbounded divisible lift pays the missing unit.  The screened PSD-rank,
extension-degree, projective-space, and symmetric-cone barrier sources do
not state this selection-free all-field standard-slice cap,
certificate-fiber rigidity, additive critical product law, or recession
reduction.  The conservative label remains **candidate partial all-field
cap theorem; only bounded projection-singular divisible saturation with
quotient at least two is open**.

The independently audited
[Hermitian exposed-rank theorem](2026-09-04-selection-free-hermitian-exposed-rank-frontier.md)
also makes the local lower bound exact as a different minimax:
\[
 \inf_{\mathcal L}\max_{v\in S^{N-1}}
 \min_{Y\in\mathcal D_{\mathcal L}(v)}
 \operatorname{rank}_{\mathbb F}Y
 =
 \left\lceil{N-1\over a(R-1)}\right\rceil .
\]
Its upper bound is a rotated Hermitian perspective whose blocks are
\(\left(\begin{smallmatrix}1-b&w^*\\w&zI\end{smallmatrix}\right)\);
explicit rank-one Gram certificates handle zero coordinate groups and
both poles.  The construction is a higher-order Hermitian analogue of a
classical rotated-SOC perspective, so the modelling primitive itself is
not claimed as new.  No screened source identifies this exact
max-support/min-certificate rank over arbitrary affine lifts, its
field-dependent capacity, or its additive shared-product existence lower.
Combined with the separately screened support-principal-minor theorem, it
gives a formulation-universal hard support with path-independent
\(\sqrt q\log(1/\epsilon)-O_{\mathcal L,X^c,S}(1)\) movement and the
corresponding bounded-Dikin-round lower bound.  Nesterov--Todd supplies the
generic chord-to-distance conversion; the new input is the
selection-free hard certificate rank.  This movement claim is not a
query lower bound, and its hard support, accuracy scale, reference
constant, and warm-start term are not uniform over formulations.  The
grouped Hermitian Schur lift, whose exact restricted parameter is
\(g\leq q+1\), supplies an all-support
\(O_\theta(\sqrt q\log(q/\epsilon))\) standard short-step upper.
Therefore, with the lift and start fixed before
\(\epsilon\downarrow0\), the infimum-over-lifts/supremum-over-supports
bounded-Dikin asymptotic coefficient has exact order
\(\Theta_\theta(\sqrt q)\), independently of \(R\).  This is a movement
minimax, not a query-complexity minimax.
The safe label is **candidate exact selection-free support-certificate
minimax synthesis; novelty of the formulation primitive not claimed**.

## 14. Eighth targeted screen: spectral-ball Hessian distance and centrality tax

Screen date: 2026-09-04. The companion
[spectral-ball path note](2026-09-04-spectral-ball-low-rank-objective-path.md)
studies the real Hessian metric of
\[
 \phi(X)=-\log\det(I-XX^*)
\]
on the real or complex operator-norm ball. Two claims need different
provenance labels: the exact center-to-point distance
\[
 d_\phi(0,X)=\left[\sum_i\rho(\sigma_i(X))^2\right]^{1/2},
 \qquad
 \rho'(u)={\sqrt{2(1+u^2)}\over1-u^2},                         \tag{L14.1}
\]
and the sharp-order \(\Theta(\sqrt{\log r})\) excess of a specially weighted
rank-\(r\) primal central path both over the distance to its own endpoint
and over the shortest distance to the same objective-accuracy sublevel.

### The bounded-symmetric-domain formulas use a different metric

The complex matrix ball is the classical type-I bounded symmetric domain,
so there are superficially very close singular-value distance formulas.
Falbel, Guilloux, and Will,
[*A Hilbert Metric for Bounded Symmetric
Domains*](https://doi.org/10.1515/advgeom-2025-0015)
([arXiv](https://arxiv.org/abs/2403.18634)), Proposition 4.6, obtain for
their generalized Hilbert metric
\[
 d_H(0,X)=\sum_i\log{1+\sigma_i(X)\over1-\sigma_i(X)}.
\]
Their Corollary 4.7 explicitly distinguishes this \(\ell_1\)-type Finsler
metric from the Bergman \(\ell_2\) and Caratheodory \(\ell_\infty\) metrics.
Lemmens and Walsh,
[*Caratheodory Distance-Preserving Maps Between Bounded Symmetric
Domains*](https://doi.org/10.1007/s00208-026-03408-6), recall in Section 9
the normalized Bergman formula
\[
 d_B(0,X)=\left[\sum_i\operatorname{artanh}^2\sigma_i(X)\right]^{1/2}.
\]
These are genuine classical exact radial formulas, but neither is (L14.1).

The distinction is not just a normalization. Although
\(-\log\det(I-XX^*)\) is a Kahler potential for the invariant complex
geometry, the IPM metric here is its **real Hessian**, rather than its mixed
\(\partial\bar\partial\) Hessian. Already on one complex disk, the real
Hessian has radial coefficient
\(2(1+u^2)/(1-u^2)^2\), giving the derivative in (S1), whereas the Bergman
radial coefficient is a constant multiple of \((1-u^2)^{-2}\), giving
\(\operatorname{artanh}u\). Thus a citation to bounded-symmetric-domain
Bergman geometry does not prove the local exact-distance theorem (L14.1).

### Classical ingredients of the real-Hessian proof

Nesterov and Todd,
[*On the Riemannian Geometry Defined by Self-Concordant Barriers and
Interior-Point Methods*](https://doi.org/10.1007/s102080010032), establish
the general Hessian-metric framework. Lemmas 4.1--4.2 give the Euclidean
\(\ell_2\) product rule for distances and geodesics. Section 6.2 computes
an exact coordinatewise distance on a cube, but for the different scalar
barrier \(-\log\cos u\), not for \(-\log(1-u^2)\) and not for a matrix ball.
Their Theorem 6.1 also gives the familiar affine-invariant distance for the
ambient positive-definite cone. This does not settle the present affine
slice. Indeed,
\[
 \phi(X)=-\log\det\begin{pmatrix}I&X\\X^*&I\end{pmatrix},
\]
but the ambient positive-definite geodesic generally leaves the fixed-
diagonal slice. Its center-to-endpoint length is
\(\big[\sum_i\log^2(1+\sigma_i)+\log^2(1-\sigma_i)\big]^{1/2}\),
which is not (L14.1); it is only an ambient lower bound for the intrinsic slice
distance.
Lee and Vempala,
[*Geodesic Walks in Polytopes*](https://doi.org/10.1137/17M1145999)
([arXiv](https://arxiv.org/abs/1606.04696)), Lemma 31, explicitly records
the general one-dimensional Hessian coordinate
\(u\mapsto\int_0^u\sqrt{\phi''(t)}\,dt\); it mentions the standard interval
log barrier \(-\log(1-u)-\log(1+u)\). This directly precedes the scalar
function \(\rho\), but not the global reduction from arbitrary matrix paths
to singular-value paths.

Papa Quiroz and Oliveira,
[*New Self-Concordant Barrier for the
Hypercube*](https://doi.org/10.1007/s10957-007-9220-2), Theorem 3.1,
also compute explicit coordinatewise geodesics and product distances on
\((0,1)^n\). Their barrier is
\[
 \sum_i(2x_i-1)\bigl(\log x_i-\log(1-x_i)\bigr),
\]
whose diagonal Hessian is
\(x_i^{-2}(1-x_i)^{-2}\). It is not the usual box log barrier, whose
scalar Hessian is \(x_i^{-2}+(1-x_i)^{-2}\), and its log-odds distance
therefore is not the \(\rho\) formula in the companion note. This source
does confirm that explicit flat product-box Hessian distances are
classical for suitable separable barriers.

The other decisive ingredient is also classical. Lewis and Sendov,
[*Twice Differentiable Spectral
Functions*](https://doi.org/10.1137/S089547980036838X), give the Hessian of
a twice differentiable real-symmetric spectral function, including the
divided-difference off-diagonal terms. Drusvyatskiy and Kempton,
[*Variational Analysis of Spectral Functions
Simplified*](https://arxiv.org/abs/1506.05170), give another derivation and
state the direct Hermitian and rectangular singular-value analogues.
Applied to the Hermitian dilation of \(X\), positivity of those terms
supplies the metric lower bound by the singular-value velocity used in the
companion proof. General orbit-space results such as
Alekseevsky, Kriegl, Losik, and Michor,
[*The Riemannian Geometry of Orbit Spaces: The Metric, Geodesics, and
Integrable Systems*](https://arxiv.org/abs/math/0102159), also explain why
singular-value sections are natural for isometric matrix actions. The
targeted screen did not locate an application of those results that states
(S1) for this real log-determinant Hessian metric.

The safe label for (L14.1) is therefore **candidate exact real-Hessian
spectral-ball specialization; classical scalar, product, spectral-Hessian,
and orbit-space ingredients, but no direct formula located**. It should
not be described as a new distance formula for the Bergman metric.

### Central-path length comparisons

Nesterov and Nemirovski,
[*Primal Central Paths and Riemannian Distances for Convex
Sets*](https://doi.org/10.1007/s10208-007-9019-4)
([author manuscript](https://www2.isye.gatech.edu/~nemirovs/FCM_Riem_2008.pdf)),
are the direct comparator. The article first circulated as CORE Discussion
Paper 2003/51, [*Central Path and Riemannian
Distances*](https://dial.uclouvain.be/pr/boreal/object/boreal%3A4930).
Their Theorem 4.1 proves for every
\(\nu\)-self-concordant barrier
\[
 L_{\rm CP}\le \log2+\nu^{1/4}
 \sqrt{d\,[d+\log12]},                                        \tag{L14.2}
\]
where \(d\) is the Hessian geodesic distance between the two central-path
endpoints; the constants improve when the initial Newton decrement is at
least \(1/2\). Their Theorem 5.3 gives the analogous mixed estimate with
distance \(d_{\rm sub}\) from the starting central point to the whole
objective sublevel:
\[
 L_{\rm CP}\le O(1)\nu^{1/4}
       \sqrt{d_{\rm sub}[d_{\rm sub}+\log\nu]}.
\]
The displayed theorem assumes that a radius-\(1/10\) Dikin ellipsoid at
the starting point misses the target sublevel; its footnote disposes of the
intersecting case by a constant-length bound. Thus it is the relevant
global comparison after splitting off that trivial near-target case.
Example 1.1 exhibits a much larger central-path/target-set gap for the
unbounded orthant. Example 5.1 does use the same product-box barrier
\(-\sum_i\log(1-x_i^2)\), but only to compare two generic complexity
bounds for minimizing the barrier; it does not compute a weighted linear-
objective central path or a sharp path/geodesic ratio.

Consequently, the companion bound
\[
 {L_{\rm CP}(0,\eta)\over d_\phi(0,X(\eta))}
 \le
 \left[\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2\right]^{1/2}
 =\Theta(\sqrt{\log r})                                       \tag{S3}
\]
is a structured strengthening of (L14.2): for this barrier and its ordered
singular-value central paths it replaces the generic \(r^{1/4}\) factor by
the sharp-order \(\sqrt{\log r}\) factor. The multiscale weights in the
companion note match (S3) in order. The finite-dimensional
\(\sqrt{\log r}\) norm comparison is closely related to classical Lorentz
sequence-space embeddings; the apparently unlocated part is its exact use
for these central-path velocities and the matching spectral-weight
construction.

The companion note now supplies that additional theorem. Let
\(L_{\rm opt}(\epsilon)\) be the exact Hessian distance from the center to
the objective-accuracy sublevel, and stop the central path at its first
\(\epsilon\)-accurate point. Its Lambert-\(W\) water-filling comparison
proves
\[
 L_{\rm CP}(\epsilon)
 \le c_\star\Gamma_r L_{\rm opt}(\epsilon)
 <{69\over50}\Gamma_r L_{\rm opt}(\epsilon),                   \tag{S4}
\]
where
\(c_\star=\max_{y>0}p^{-1}(yp'(y))/y\) is the exact scalar dilation for
the interval barrier.  A separate independently audited analytic
certificate proves \(c_\star<69/50=1.38\); numerical evaluation suggests
\(c_\star\approx1.37486420044\), without a uniqueness claim.  This
supersedes the earlier sufficient constant
\(\kappa_0=1.391010896\ldots\).
The multiscale instance with \(T=m\) proves the matching lower order, so
\[
 \sup_{w,\epsilon}{L_{\rm CP}(\epsilon)\over L_{\rm opt}(\epsilon)}
 =\Theta(\sqrt{\log r}).                                        \tag{S5}
\]
This is strictly stronger than the earlier one-sided separation from an
explicit accurate endpoint. It is still an arclength-versus-shortest-path
statement by itself. The companion note now also contains a separate,
audited discrete theorem. On its \(T=m\) instance, any sequence with
nondecreasing central labels, endpoints at geodesic distance at most a
fixed \(\delta\) from the labeled centers, and forward Dikin chords of
fixed radius \(R<1\), needs
\[
             \Omega_{R,\delta}(m\log m)
\]
rounds to reach the first accurate central label. The optimal unrestricted
noncentral Dikin sequence to the same accuracy has
\(\Theta_R(m\sqrt{\log m})\) chords. Hence this precise neighborhood model
has an \(\Omega_{R,\delta}(\sqrt{\log m})\) round overhead. It is not a
claim about every standard primal--dual neighborhood or about quantum
queries.

There is substantial prior art on neighborhood-based iteration lower
bounds, so the discrete theorem should not be presented as the first such
separation. Nesterov--Todd (2002), Definition 3.1 and Lemmas 3.2--3.4,
already relate bounded local-norm steps, ordered proximity samples along a
curve, Hessian distance, and curve length; their Theorem 3.1 derives
optimality when the followed curve is uniformly \(\tau\)-geodesic. It does
not give the spectral-ball threshold potential or compare a winding
central-neighborhood route with the optimal noncentral Dikin route.

Hildebrand,
[*Optimal Step Length for the Newton Method near the Minimum of a
Self-Concordant Function*](https://arxiv.org/abs/2003.08650), gives an
exact worst-case optimal-control analysis of one damped Newton step as a
function of the current Newton decrement, and Section 7 uses it to enlarge
a standard central-path neighborhood and improve constants in path
following. This is the closest screened source specifically about sharp
Newton-decrement neighborhood progress. It is an upper-performance theorem
for a corrector step over the whole class of self-concordant functions; it
does not prove a multiround lower bound, use the matrix-ball Hessian
distance, or compare central and noncentral bounded-Dikin routes.

Zong, Lee, and Yue,
[*Short-step Methods Are Not Strongly
Polynomial-Time*](https://doi.org/10.1007/s10107-023-02002-x), define a
short-step method by requiring its entire polygonal trajectory to remain in
the union of fixed-width Newton-residual \(\ell_2\) neighborhoods and prove
an exponential LP lower bound. Allamigeon, Benchimol, Gaubert, and Joswig,
[*Log-Barrier Interior Point Methods Are Not Strongly
Polynomial*](https://doi.org/10.1137/17M1142132), prove an exponential
segment lower bound for a primal--dual log-barrier wide neighborhood using
tropical central paths. Allamigeon, Gaubert, and Vandame,
[*No Self-Concordant Barrier Interior Point Method Is Strongly
Polynomial*](https://doi.org/10.1145/3519935.3519997), Theorems 17, 21,
and 25, extend the polygonal-trajectory lower-bound mechanism to
multiplicative neighborhoods for arbitrary self-concordant barriers on a
parametric LP family.

The closest modern organizing notion is the **straight-line complexity**
of Allamigeon, Dadush, Loho, Natura, and Vegh,
[*Interior Point Methods Are Not Worse than
Simplex*](https://doi.org/10.1137/23M1554588): the minimum number of
Euclidean line segments whose whole polygonal curve traverses a wide
coordinatewise/multiplicative neighborhood of an LP central path. The
spectral theorem differs in three material ways. Its neighborhood is a
fixed intrinsic Hessian-distance tube around explicitly labeled centers;
only the chord endpoints, not the entire chord, must lie in that tube; and
each chord instead has a fixed one-sided Dikin cap. It also computes the
sharp-order overhead relative to the optimal arbitrary Dikin sequence on
one explicit matrix-ball family, rather than tropical or combinatorial
segment complexity for LPs. No screened source states this combination.

Nesterov--Nemirovski's Theorem 5.3 remains the verified general comparator
for objective sublevels, but (S4)--(S5) sharpen its \(O(\nu^{1/4})\)
dependence to the exact order \(\Theta(\sqrt{\log r})\) for this structured
spectral-ball family.

Dedieu, Malajovich, and Shub,
[*On the Curvature of the Central Path of Linear Programming
Theory*](https://doi.org/10.1007/s10208-003-0116-8)
([arXiv](https://arxiv.org/abs/math/0312083)), and the later tropical
lower-bound literature study Euclidean total curvature or combinatorial
central-path complexity. Those notions do not equal Hessian arclength
divided by intrinsic endpoint distance and do not subsume (S3).

The conservative novelty label is **candidate sharp structured
centrality-tax theorem for both same endpoints and the same objective-
accuracy sublevel, together with a candidate new sharp bounded-Dikin
separation for its explicitly defined intrinsic central-neighborhood
model; exact within the spectral-ball support-objective family, but not a
generic IPM-neighborhood or QIPM runtime lower bound**. This is a targeted
primary-source screen, not an exhaustive priority determination.

## 15. Ninth targeted screen: sharp separable centrality tax

Screen date: 2026-09-04. The companion
[separable centrality-tax
note](2026-09-04-sharp-separable-centrality-tax.md) abstracts the matrix-
ball argument to a product of identical scalar barriers. In exact scalar
metric coordinates, its central path consists of translates of one velocity
profile. If that profile is nondecreasing, the note proves the sharp
same-endpoint factor
\[
 L_{\rm cen}\le\Gamma_r d_F,
 \qquad
 \Gamma_r^2=\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2
 ={1\over4}\log r+O(1).
\]
More strongly, the note proves that every fixed normalized scalar
one-self-concordant barrier has monotone metric velocity with the requisite
integrable tails, and hence has exact worst translated-profile supremum
\(\Gamma_r\). The standard interval barrier is one explicit realization. It
also constructs smooth bounded-interval self-concordant barriers with
nonmonotone velocity whose exact worst-case factor is instead \(\sqrt r\).
These statements and the trace-spectral extension have been independently
audited.

The dynamical ingredients have classical antecedents. Iusem, Svaiter, and
da Cruz,
[*Central Paths, Generalized Proximal Point Methods, and Cauchy
Trajectories in Riemannian
Manifolds*](https://doi.org/10.1137/S0363012995290744), identify central
paths with Cauchy trajectories for a class including linear programming in
the Hessian metric of an orthant barrier. Alvarez, Bolte, and Brahic,
[*Hessian Riemannian Gradient Flows in Convex
Programming*](https://doi.org/10.1137/S0363012902419977), develop the
general Legendre-coordinate Hessian-gradient-flow framework and give
several equivalent interpretations for linear objectives. These sources
precede the scalar metric-coordinate and translated-flow viewpoint; they do
not state a dimension-sharp central-arc/endpoint-distance constant.

Nesterov--Todd (2002) supply the exact product \(\ell_2\) distance rule. In
their Section 6.2 they also compute the hypercube geometry for the scalar
one-self-concordant barrier \(f(\tau)=-\log\cos\tau\):
\(\psi(\tau)=\log(\sec\tau+\tan\tau)\) gives a global Euclidean metric
coordinate. Its central profile is
\(h(t)=\operatorname{arsinh}(e^t)\), with monotone velocity tending from
zero to one, so it supplies another classical fixed barrier to which the
local sharp theorem applies. The paper does not compare the weighted primal
central arc to its same-endpoint chord or state \(\Gamma_r\).

Nesterov--Nemirovski (2008) supply the generic \(O(\nu^{1/4})\)
central-path comparison discussed above. Their Example 5.1 explicitly uses
the standard box barrier \(-\sum_i\log(1-x_i^2)\), but to instantiate their
general length analysis, not to derive the translated-profile extremum.
The prefix decomposition used to obtain \(\Gamma_r\) is recognizable as a
classical finite-dimensional Lorentz-sequence norm argument; see G. G.
Lorentz,
[*On the theory of spaces \(\Lambda\)*](https://doi.org/10.2140/pjm.1951.1.411)
(1951). Neither the rearrangement device nor its weighted \(\ell_2\)
comparison is by itself a novelty claim. A useful adjacent
comparison outside interior-point geometry is Gupta, Balakrishnan, and
Ramdas,
[*Path Length Bounds for Gradient Descent and
Flow*](https://www.jmlr.org/papers/v22/19-979.html), Theorems 10 and 18:
Euclidean gradient flow on quadratic objectives has sharp path-length
factor \(\Theta(\min\{\sqrt d,\sqrt{\log\kappa}\})\). Their construction
also activates separated coordinates at different scales. It uses a fixed
Euclidean metric, condition number, and distance to the minimizer, not a
self-concordant Hessian metric, translated central profiles, or the exact
\(\Gamma_r\) coefficient.

The targeted primary-source search did not locate the combined sharp
\(\Gamma_r\) theorem, the barrier-independent assertion that every fixed
normalized scalar one-self-concordant barrier has exact supremum
\(\Gamma_r\), the differential monotone-velocity test used to prove it, or
a smooth self-concordant barrier family attaining the contrasting
\(\sqrt r\) supremum. The safe label is **candidate sharp
separable-product centrality theorem and counterexample; built from
classical Hessian-flow, product-metric, box-geometry, and Lorentz-sequence
ingredients, with priority still requiring specialist review**.

The universal discrete extension (25a)--(25k) has closer lower-bound
antecedents. Zong--Lee--Yue,
[*Short-step Methods Are Not Strongly
Polynomial-Time*](https://arxiv.org/abs/2201.02768), prove
\(2^{r-3}\) iterations for every self-concordant barrier of scale-independent
parameter on an ill-conditioned Klee--Minty-type LP, when the entire polygonal
trajectory remains in an \(\ell_2\) Newton neighborhood. Allamigeon--Gaubert--
Vandame,
[*No Self-Concordant Barrier Interior Point Method Is Strongly
Polynomial*](https://arxiv.org/abs/2201.02186), obtain a related exponential
arbitrary-barrier lower bound from tropical central paths and multiplicative
neighborhoods. Earlier, Allamigeon--Benchimol--Gaubert--Joswig,
[*Long and Winding Central Paths*](https://arxiv.org/abs/1405.4161), proved
exponential total curvature for a log-barrier family. Hence the local result
must not be called the first barrier-universal central-neighborhood lower
bound.

Allamigeon--Dadush--Loho--Natura--Végh,
[*Interior Point Methods Are Not Worse than
Simplex*](https://arxiv.org/abs/2206.08810), define straight-line complexity
through polygonal traversal of a wide neighborhood and use it as a lower
bound for path-following iterations. The new separable theorem uses a
different contract: one fixed identical normalized scalar barrier on a
product of intervals, arbitrary nonmonotone labels, membership of the
iterates (not the whole polygonal interpolation) in a metric or
Newton-decrement tube, and a starting-point Dikin cap on every move. Its
unlocated feature is the matched relative law
\[
 N_{\rm central}=\Omega_{f,R,\delta}(r\log r),\qquad
 N_{\rm noncentral}=O_{f,R}(r\sqrt{\log r}),
\]
for actual endpoint accuracy and every fixed scalar normalized barrier. This
is a candidate sharp simple-product separation, but it is polynomial,
barrier-dependent in its hidden constants, potentially nonuniform in bit
description, and much narrower than the tropical impossibility results.

The independently audited [sparse box-LP
specialization](2026-09-04-sparse-box-lp-geodesic-centrality-tax.md) makes
the interval example a uniformly constructible rational LP with row
sparsity one, column sparsity two, and exact restricted standard-barrier
parameter \(r\).  At \(\log(1/\epsilon)=\Theta(r)\), analytic-center
initialization, actual \(\epsilon\)-accurate output, and any fixed metric or
Newton-decrement central tube force \(\Theta_R(r\log r)\) bounded chords;
the optimal unrestricted same-endpoint schedule uses
\(\Theta_R(r\sqrt{\log r})\).  No monotonicity or endpoint-label condition
is assumed.  The box barrier, dyadic LP encoding, phase-kickback state
preparation, and parity readout lower bound are individually standard.  The
conservative candidate contribution is their sharp discrete
centrality-versus-geodesic synthesis on one sparse LP, not a new barrier or
an unrestricted LP/QIPM runtime theorem.  For logarithmically homogeneous
cone barriers, Nesterov--Todd's 2002 theorem says that a feasible primal--
dual central-path segment is \(\sqrt2\)-geodesic: its length is at most
\(\sqrt2\) times its endpoint distance in the combined primal--dual product
metric.  The box-LP tax instead uses the restricted primal metric.  Its
lower bound applies to a full method only when primal feasibility and the
full neighborhood and step contracts project to the stated primal
contract; its primal noncentral shortcut supplies no dual-feasible
trajectory to the central dual endpoint.  Therefore the note does not
claim a primal--dual \(\sqrt{\log r}\) separation.  More decisively, between
any two finite primal--dual central endpoints, Nesterov--Todd's inequality
and the standard forward-Dikin chord comparisons make arclength-partitioned
central tracking constant-factor optimal among all combined-metric
bounded-chord paths, with a constant depending only on the chord radius.
Thus charging the full dual trajectory rules out any dimension-growing
centrality tax in this model; this obstruction is classical, not a new
theorem of the box-LP construction.

The independently audited
[dual-completion companion](2026-09-04-sparse-box-primal-dual-completion-tax.md)
quantifies what replaces that primal tax on the same sparse multiscale
instance.  In the standard orthant formulation, restricted-primal
unrestricted movement, restricted-primal central movement, and optimal
movement to any strictly feasible primal--dual gap certificate have the
three sharp orders
\[
 \Theta_R(r\sqrt{\log r}),\qquad
 \Theta_R(r\log r),\qquad
 \Theta_R(r^{3/2}).
\]
The last lower bound has a direct slack proof, not merely a same-central-
endpoint argument: gap at most \(2\epsilon_r\) forces all \(r\) relevant
dual slacks from at least \(1/\sqrt2\) down to at most \(\epsilon_r\), and
the dual orthant metric is Euclidean in logarithmic coordinates.  The exact
Nesterov--Todd constant-speed law supplies the matching central upper.
Nesterov--Nemirovski's primal comparison is the nearest geometric
antecedent found.  Gao--Liu--Ye--Udell,
[*When Does Primal Interior Point Method Beat Primal-dual in Linear
Optimization?*](https://arxiv.org/abs/2411.16015), is close in theme but
compares late-stage scaling stability, preconditioned normal-equation
arithmetic, and empirical runtime rather than Riemannian movement or this
dyadic box family.  No screened source stated the resulting
\(\Theta(\sqrt{r/\log r})\) gap-certification completion premium.  The safe
label is **candidate explicit sparse multiscale primal-versus-primal--dual
metric separation assembled from classical product geometry and the
candidate separable-box construction**.  It must not be advertised as the
first primal-versus-primal--dual IPM comparison or as a total-runtime
separation.

## 16. Tenth targeted screen: connected extremes and the additive factor gap

Screen date: 2026-09-04. The companion
[connected-extremes counterexample
note](2026-09-04-connected-extremes-additive-factor-gap-counterexample.md)
constructs, for every \(s,L\geq2\), the codimension-two slice
\[
 Z_{s,L}=\left\{z\in Q_{s+1}^L:\sum_i t_i=1,\ \sum_i x_i=0\right\}.
\]
It has dimension \(N=(s+1)L-2\), ambient factor dimension \(M=N+2\), a
path-connected extreme set, and every Lorentz factor is essential and
slack-visible. It also proves the exact intrinsic barrier value
\(\nu_{\rm opt}(Z_{s,L})=2L-1\) and, after setting \(s=d-1\), an exact
factor-count/total-dimension frontier against arbitrary dictionaries of
nonzero proper cones of dimension at most \(d\).

### Affine sections and extreme points

Two classical or now-explicit general results cover the abstract
extremality layer. Dubins,
[*On Extreme Points of Convex
Sets*](https://doi.org/10.1016/S0022-247X(62)80007-9), proves that every
extreme point of a codimension-\(m\) affine section of a linearly bounded,
linearly closed convex set is a convex combination of at most \(m+1\)
extreme points of the original set. Normalize \(Q_{s+1}^L\) by
\(\sum_i t_i=1\); the remaining balance equation is one hyperplane, so
Dubins already implies that an extreme point of \(Z_{s,L}\) is supported on
at most two normalized product-cone extreme rays. It does not identify the
one-block zero-cosine and two-block opposite-cosine cases, prove their
path-connected gluing, or show that codimension two is sharp for connected
extremes of a full-Slater product-cone slice.

Henrion, Kružík, and Weis,
[*Extreme Points and Faces in the Moment
Problem*](https://arxiv.org/abs/2606.21391), Theorem 2.6, give a general
smallest-face injectivity criterion for an affinely constrained convex set.
For a singleton affine fiber in finite dimensions, this specializes to
\[
 z\in\operatorname{ext}\{u\in K:Au=b\}
 \quad\Longleftrightarrow\quad
 \ker A\cap\operatorname{span}F_K(z)=\{0\},
\]
the principle used in the companion note. Pataki's
[*On the Rank of Extreme Matrices in Semidefinite Programs and the
Multiplicity of Optimal
Eigenvalues*](https://doi.org/10.1287/moor.23.2.339) is the familiar PSD
rank specialization. Thus neither the general kernel/minimal-face test nor
the PSD activation bound is novel. The product-Lorentz classification,
its topology, the all-factor visibility witnesses, and the exact
\(M=N+2\) realization are additional calculations not stated in these
sources.

### Lift and capped-dictionary comparators

Gouveia, Parrilo, and Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164), supply the proper
lift--slack-factorization equivalence used to pass from the explicit slice
to a factorization claim. Fawzi and Parrilo,
[*Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite Extension
Complexity*](https://arxiv.org/abs/1311.2571), prove exponential factor-count
lower bounds for products of fixed-order PSD cones, including the
second-order-cone case at PSD order two. Averkov,
[*Optimal Size of Linear Matrix Inequalities in Semidefinite Approaches to
Polynomial Optimization*](https://arxiv.org/abs/1806.08656), instead makes
the largest allowed PSD block order the invariant and allows any finite
number of blocks. Saunderson,
[*Limitations on the Expressive Power of Convex Cones without Long Chains
of Faces*](https://arxiv.org/abs/1902.06401), obstructs lifts through finite
products of cones with bounded face-chain length using neighborliness.

These sources establish the surrounding product-lift and fixed-block
complexity framework. The targeted search did not find their exact analogue
of the companion statement: for one explicit connected-extreme body and a
dictionary containing **all** nonzero proper cones of dimension at most
\(d\), simultaneously
\[
 L_{\min}=(N+2)/d,\qquad M_{\min}=N+2,
\]
with equality attained by \(Q_d^L\). In particular, the cited fixed-PSD and
face-chain results do not subsume the companion proof from ordinary slack
rank plus the equality-rigidity/connectivity obstruction. This distinction
should remain explicit because the latter argument depends on a separate
minimum-dimension rigidity theorem in the local workbench.

### Barrier optimum

Nesterov and Nemirovskii,
[*Interior-Point Polynomial Algorithms in Convex
Programming*](https://doi.org/10.1137/1.9781611970791), Proposition 2.3.6,
prove that a self-concordant barrier parameter is at least the number of
linearly independent facets meeting at a simple polytope vertex; in
particular an \(m\)-simplex needs parameter at least \(m\). Hildebrand,
[*A Lower Bound on the Optimal Self-Concordance Parameter of Convex
Cones*](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf),
develops projective cross-ratio lower bounds for logarithmically homogeneous
cone barriers and recovers the Nesterov--Nemirovskii polyhedral bound as a
special case.

Accordingly, the lower-bound theorem used in the companion note is
classical. What the targeted search did not locate is the exact synthesis
for \(Z_{s,L}\): a boundary-inheriting \((2L-1)\)-simplex section that applies
to every coupled barrier, together with the inverse-Hessian projection and
boundary-order argument showing that the restricted standard product
Lorentz barrier attains \(2L-1\). Nor did it locate the paired ambient
identity \(\nu_{\rm opt}(\widehat Z_{s,L})=2L\).

The companion note now also transfers this lower bound to every convex
affine lift of \(Z_{s,L}\) with bounded nonempty projection fibers.  The
mechanism is classical. Nesterov,
[*Parabolic Target Space and Primal--Dual Interior-Point
Methods*](https://doi.org/10.1016/j.dam.2007.05.002), Theorem 3, proves a
partial-minimization preservation result in a special product-variable
setting. Chares,
[*Cones and Interior-Point Algorithms for Structured Convex Optimization
Involving Powers and
Exponentials*](https://dial.uclouvain.be/pr/boreal/en/object/boreal%3A28538),
Assumption 4 and Theorem 5.2.1, treats an affine lifted set with
base-dependent equality right-hand side. He assumes the relevant interior
fibers are bounded, obtains a unique partial minimizer, and proves that
the marginal of a \(\nu\)-self-concordant barrier is a nondegenerate
\(\nu\)-self-concordant barrier on the projection.

Therefore the preservation of \(\nu\) under bounded-fiber marginalization
is not new. Combining it with the exact intrinsic value above immediately
gives
\[
    \nu_{\rm lift}\geq \nu_{\rm opt}(Z_{s,L})=2L-1.
\]
The targeted search did not locate this exact lower bound for all
bounded-fiber lifts of the \(Z_{s,L}\) family, or a general
extension-complexity theorem phrased as monotonicity of optimal barrier
parameter under bounded-fiber affine lifts. The safe label is **new
family-specific corollary of a known partial-minimization theorem**.
Unbounded fibers are outside Chares's hypothesis: even the redundant
product with \(\mathbb R_{++}\) makes the naive marginal of
\(F(z)-\log r\) equal to \(-\infty\), so the screened sources do not justify
dropping boundedness.

The companion note separately proves a lift-invariant result for
**polytopes**, where finiteness of the vertex set repairs this issue. For a
closed line-free lift \(D\) of a compact polytope, choose a functional
strictly positive on \(\operatorname{rec}D\setminus\{0\}\). Lifting every
vertex bounds the fiberwise minimum of that functional uniformly over the
polytope; one sufficiently high constant-level section is therefore
bounded, retains the whole projection, and meets the relative interior.
Affine restriction followed by Chares's theorem transfers the original
barrier parameter to the polytope. Consequently every self-concordant
barrier on every closed full-Slater conic lift of an \(n\)-polytope with a
simple vertex satisfies \(\nu\geq n\), regardless of original fiber
boundedness or barrier coupling.

The two endpoints are classical. Nesterov--Nemirovskii, Proposition 2.3.6,
is the simple-vertex lower bound. Lee--Yue,
[*Universal Barrier is
\(n\)-Self-Concordant*](https://arxiv.org/abs/1809.03011), Theorem 2 and
Remark 2, give the matching universal-barrier upper and explicitly recall
that lower bound. Polyhedral extension-complexity literature also commonly
defines an extension of a polytope to be a bounded polytope, while
Gouveia--Parrilo--Thomas supply bounded slack-factorization constructions.
Those conventions and constructions do not transport a specified coupled
barrier from a given unbounded conic lift.

No screened primary source stated the full lift-invariant corollary or its
recession-positive constant-level normalization for a given SCB. The safe
label is **candidate general lift-invariant corollary of known ingredients**,
not a new intrinsic lower bound or partial-minimization theorem. This
polytope result does not remove the bounded-fiber qualification for the
nonpolyhedral \(Z_{s,L}\) family.

The conservative label is **candidate explicit counterexample and sharp
synthesis**. Its general lift/factorization theorem, affine-slice
extremality criterion, support-at-most-two phenomenon, Pataki specialization,
and simplex barrier lower bound all have direct antecedents. The apparently
unlocated contribution is their exact combination in the \(Z_{s,L}\)
family: connected extreme topology at codimension two, all-factor
visibility with \(M=N+2\), the matching coupled-barrier value, and the exact
arbitrary-dictionary cap frontier. This was a targeted primary-source
screen, not an exhaustive novelty or priority determination.

## 17. Eleventh targeted screen: PSD/Hermitian balance slices

Screen date: 2026-09-04. This screen covers
[the identical-factor PSD/Hermitian construction](2026-09-04-psd-hermitian-cap-hard-connected-slices.md)
and [the heterogeneous Hermitian balance
construction](2026-09-04-hermitian-balance-slice-sharp-frontier.md).
Their proposed package consists of a full-Slater codimension-two slice of a
product of classical Hermitian cones, a path-connected extreme-point set,
the exact arbitrary-proper-cone cap frontier \(M_{\min}=N+2\) and
\(L_{\min}=L\) in the identical-factor case, and exact intrinsic barrier
parameter \(\sum_iR_i-1\) on the normalized slice.

### Extreme points and topology

The general affine-section mechanism has direct antecedents. Dubins,
[*On Extreme Points of Convex
Sets*](https://doi.org/10.1016/S0022-247X(62)80007-9), shows that an extreme
point of a codimension-\(m\) affine section of a linearly bounded, linearly
closed convex set is a convex combination of at most \(m+1\) extreme
points. Apply this after trace-normalizing the product cone: the remaining
balance constraint is one hyperplane, so the support-at-most-two conclusion
is already classical. Pataki,
[*On the Rank of Extreme Matrices in Semidefinite Programs and the
Multiplicity of Optimal
Eigenvalues*](https://doi.org/10.1287/moor.23.2.339), is the standard
real-PSD rank comparator. Henrion, Kružík, and Weis,
[*Extreme Points and Faces in the Moment
Problem*](https://arxiv.org/abs/2606.21391), Theorem 2.6, state the general
smallest-face injectivity criterion whose finite-dimensional singleton-fiber
specialization is the kernel/minimal-face test used in both notes.

Thus neither the abstract criterion nor support at most two is a novelty
claim. The targeted search did not locate the explicit balance family:
one- and two-block rank-one extreme points classified by the sign of an
off-diagonal Hermitian moment, followed by projective zero-level and
cross-factor deformations that make the full extreme set path connected.
Recent work such as Scheiderer's
[*Extreme Points of Gram Spectrahedra of Binary
Forms*](https://doi.org/10.1007/s00454-022-00385-w) and Vill's
[*Integrating Spectrahedra*](https://doi.org/10.1007/s00454-025-00719-4)
studies rank strata, faces, and extreme points of particular Gram
spectrahedra and their fiber bodies, but does not state this product-cone
codimension-two topology.

### Exact barrier parameter

The ambient values are completely classical. Güler and Tunçel,
[*Characterization of the Barrier Parameter of Homogeneous Convex
Cones*](https://uwaterloo.ca/combinatorics-and-optimization/sites/default/files/uploads/documents/corr95.pdf),
identify the optimal parameter of a homogeneous cone with its Siegel rank.
Cardoso and Vieira,
[*On the Optimal Parameter of a Self-Concordant Barrier over a Symmetric
Cone*](https://doi.org/10.1016/j.ejor.2004.11.027), identify the
Carathéodory number of a symmetric cone with its Euclidean-Jordan rank and
analyze the generalized log-determinant barrier. This includes real,
complex, and quaternionic Hermitian PSD cones. Gouveia, Ito, and Lourenço,
[*Minimal Hyperbolic Polynomials and Ranks of Homogeneous
Cones*](https://www.heldermann-verlag.de/jca/jca33-oa/jca2623-b.pdf),
Section 4.2, use the same rank optimum in a 2026 comparison between optimal
homogeneous-cone barriers and minimal hyperbolic barriers.

Nesterov--Nemirovskii's independent-halfspace and simplex lower bounds
(*Interior-Point Polynomial Algorithms in Convex Programming*, Section
2.3.4 and Proposition 2.3.6) cover the lower-bound theorem used on the
diagonal orthant/simplex sections. A modern thematic comparator is He,
Saunderson, and Fawzi,
[*Exploiting Structure in Quantum Relative Entropy
Programs*](https://arxiv.org/abs/2407.00241): they construct optimally
self-concordant structured Hermitian-matrix cones which remove redundant
log-determinant terms compared with a larger lifted formulation. Their
domains are quantum-relative-entropy epigraph cones, not affine product-PSD
balance slices.

The targeted screen did not find the exact statement
\[
 \nu_{\rm opt}(\widehat Z)=\sum_iR_i,\qquad
 \nu_{\rm opt}(Z)=\sum_iR_i-1,
\]
or the proof pairing a boundary-inheriting diagonal section with the
inverse-Hessian projection of product logdet. The safe novelty scope is the
**explicit exact slice calculation**, not the ambient symmetric-cone
parameter or the simplex lower bound.

Chares,
[*Cones and Interior-Point Algorithms for Structured Convex Optimization
Involving Powers and
Exponentials*](https://dial.uclouvain.be/pr/boreal/en/object/boreal%3A28538),
Assumption 4 and Theorem 5.2.1, proves that exact partial minimization of a
\(\nu\)-barrier over bounded interior fibers yields a \(\nu\)-barrier on the
projection. Consequently the lower bound \(\nu_{\rm lift}\geq\sum_iR_i-1\)
for bounded-fiber affine lifts is a **new family-specific corollary of a
known transfer theorem**, if the family result is new. No screened source
supports the same conclusion for arbitrary unbounded fibers.

### Capped product lifts

Gouveia, Parrilo, and Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164), provide the general
lift--slack-factorization correspondence. Fawzi and Parrilo,
[*Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite Extension
Complexity*](https://arxiv.org/abs/1311.2571), prove exponential
factor-count lower bounds for products of fixed-order PSD cones. Saunderson,
[*Limitations on the Expressive Power of Convex Cones without Long Chains
of Faces*](https://arxiv.org/abs/1902.06401), gives a broader obstruction for
products of cones with bounded face-chain length. Soh and Chandrasekaran,
[*Fitting Tractable Convex Sets to Support Function
Evaluations*](https://doi.org/10.1007/s00454-020-00258-0), Proposition 2.6,
prove that an order-\(q\) real PSD cone cannot be represented by a lift
through a product of smaller-order PSD cones. Gouveia--Ito--Lourenço's 2026
paper also studies clique-product descriptions of sparse PSD-completion
cones through minimal hyperbolic polynomials.

These are the closest product-PSD and sparse-PSD comparators found. They do
not optimize total **real** cone dimension and factor count over a
dictionary containing every nonzero proper cone of dimension at most \(d\),
and do not state the equality
\[
 M_{\min}=N+2=dL,\qquad L_{\min}=L
\]
for an explicit connected-extreme body. That exact frontier relies on the
separate minimum-dimension factorization-rigidity theorem in the local
workbench, in addition to the classical lift/factorization correspondence.

The conservative overall label is **candidate explicit sharp synthesis**:
the support/rank criterion, symmetric-cone barrier optimum, simplex lower
bound, bounded-fiber marginalization, and general lift machinery all have
primary antecedents. The unlocated part is their simultaneous sharp
realization by these codimension-two Hermitian balance slices. This was a
targeted primary-source screen through 2026, not an exhaustive novelty or
priority determination; the quaternionic and mixed-spin-factor extensions
especially require specialist review.

## 18. Twelfth targeted screen: two-Lorentz-factor compact ball rigidity

Screen date: 2026-09-04. The companion
[two-factor compact-rigidity
note](2026-09-04-two-lorentz-factor-compact-ball-barrier-rigidity.md)
proves that every bounded full-Slater affine slice of
\(Q_{a+2}\times Q_{b+2}\) projecting onto
\(B_2^{a+b+1}\) makes the restricted standard product Lorentz barrier pay
at least three; a two-level norm chain attains three. For \(a=b=c\), this
settles the factor-count-minimal quotient-two divisible case.

The matching construction has classical antecedents. Ben-Tal--Nemirovski,
[*Lectures on Modern Convex Optimization*, Chapter
3](https://doi.org/10.1137/1.9780898718829.ch3), develop SOC modelling and
recursive norm epigraphs. Vielma--Ahmed--Nemhauser,
[*A Lifted Linear Programming Branch-and-Bound Algorithm for Mixed-Integer
Conic Quadratic Programs*](https://doi.org/10.1287/ijoc.1070.0256),
Section 3, explicitly recurse through a tower of lower-dimensional Lorentz
constraints. The two-level norm chain is therefore not a novelty claim.

Gouveia--Parrilo--Thomas give the general lift/slack-factorization
correspondence. Fawzi's
[*On Representing the Positive Semidefinite Cone Using the Second-Order
Cone*](https://doi.org/10.1007/s10107-018-1233-0) develops SOC rank and
proves nonrepresentability of \(S_+^3\) by finite products of three-
dimensional SOCs. Saunderson's
[*Limitations on the Expressive Power of Convex Cones without Long Chains
of Faces*](https://arxiv.org/abs/1902.06401) gives face-chain and
neighborliness obstructions to product-cone lifts. Aubrun--La
Piana--Müller-Hermes,
[*Factorization through Lorentz
cones*](https://arxiv.org/abs/2606.27825), classify several pairs of cones
for which every positive map factors through a direct sum of Lorentz cones.
None of these screened sources classifies compact affine lifts of one ball
through exactly two prescribed Lorentz factors.

Güler--Tunçel and Cardoso--Vieira determine optimal barriers on homogeneous
and symmetric cones, so the ambient rank-four value for a product of two
Lorentz cones is classical. Their results do not determine the exact
parameter of the standard product barrier after affine restriction. The
targeted search also did not locate the particular topological lift
obstruction in the companion proof: the definite-sign hyperplane section
has extreme-ray space \(S^a\times S^b\), whereas proper projection and
one-dimensional fibers would force a continuous injection of
\(S^{a+b}\). Invariance of domain and product-sphere cohomology are standard
ingredients, but no screened cone-lift source used them to force a
rank-one-plus-vertex contact and hence determinant order three.

The safe label is **candidate exact two-factor compact-rigidity synthesis**,
not a general SOC-rank or extension-complexity theorem. It leaves open
lifts with extra Lorentz factors whose active labels can switch across
projection-singular seams. This was a targeted primary-source screen
through 2026, not an exhaustive novelty or priority determination.

## 19. Thirteenth targeted screen: selection-free Hermitian exposed rank

Screen date: 2026-09-04. The companion
[selection-free Hermitian exposed-rank
note](2026-09-04-selection-free-hermitian-exposed-rank-frontier.md) proves
the exact all-field capped-block minimax
\[
 \inf_{\mathcal L}\max_v\min_{Y\in\mathcal D_{\mathcal L}(v)}
       \sum_i\operatorname{rank}_{\mathbb F}Y_i
 =\left\lceil {s-1\over a(R-1)}\right\rceil,
 \qquad a=\dim_{\mathbb R}\mathbb F,
\]
and converts it into a hard-objective standard-logdet distance and
bounded-Dikin-movement lower bound.
It also proves the stronger generic statement: every fixed lift has the
same rank lower bound on a dense open semialgebraic, full-measure set of
supports, while the perspective construction has equality away from one
pole.  Thus the infimum over lifts of the essential infimum over supports
is the same ceiling.  Combining the lower bound with the grouped Schur
lift gives asymptotic bounded-Dikin minimax order
\(\Theta_\theta(\sqrt q)\), with the lift and start fixed before accuracy
tends to zero and without multiplying by a query cost.

Gouveia--Parrilo--Thomas,
[*Lifts of Convex Sets and Cone
Factorizations*](https://arxiv.org/abs/1111.3164), supply the general
lift--slack-factorization correspondence. Fawzi--Gouveia--Parrilo--
Robinson--Thomas,
[*Positive Semidefinite Rank*](https://arxiv.org/abs/1407.4095), study real
PSD factorization rank, and Gribling--de Laat--Laurent,
[*Lower Bounds on Matrix Factorization Ranks via Noncommutative Polynomial
Optimization*](https://doi.org/10.1007/s10208-018-09410-y), include complex
Hermitian factorization ranks. Dannemüller--Netzer,
[*Lifts of Operator Systems*](https://arxiv.org/abs/2508.15348), extend slack
factorizations to complex-Hermitian matrix levels and free spectrahedrops.
These works minimize global factorization or free-lift size; the screened
statements do not minimize rank over the full scalar certificate fiber at
every support and then take the worst support.

Fawzi--Parrilo's fixed-size PSD-rank lower bounds count real PSD blocks.
Averkov's
[*Optimal Size of Linear Matrix Inequalities in Semidefinite Approaches to
Polynomial Optimization*](https://arxiv.org/abs/1806.08656) optimizes the
largest real LMI order, Saunderson's face-chain method obstructs products
of weak cones, and Fawzi--Safey El Din's algebraic-boundary method
lower-bounds one PSD lift order. None of these resource measures records
the objective-wise certificate rank or the real cross-Peirce capacity
\(a p_iq_i\). The targeted search did not locate the exact
\(\lceil(s-1)/(a(R-1))\rceil\) formula, its mixed-dictionary version, or
its quaternionic extension. Schmieta--Alizadeh,
[*Associative and Jordan Algebras, and Polynomial Time Interior-Point
Algorithms for Symmetric
Cones*](https://doi.org/10.1287/moor.26.3.543.10582), do establish the
classical complex/quaternionic Hermitian Jordan-algebra and IPM machinery,
but not this affine-lift minimax. The rotated perspective attaining the upper
bound is likewise classical Schur-complement modelling.

Nesterov--Todd's barrier-metric work gives the bounded-Dikin
chord-to-distance conversion used by the corollary. Nesterov--Nemirovski's
target-set geometry and Permenter's geodesic IPM are the closest movement
comparators found, but they do not attach the coefficient to minimum
support-certificate rank. Quantum IPM papers by Kerenidis--Prakash and
Augustino--Nannicini--Terlaky--Zuluaga give algorithmic upper bounds, not
this formulation-universal hard-objective movement obstruction. The
result therefore remains explicitly restricted to the standard-logdet
metric or stated bounded-chord model; it is not an unrestricted quantum
query or runtime lower bound.

The conservative label is **candidate exact selection-free Hermitian
support-certificate frontier and movement synthesis**. It is not a claim
of a new general PSD-rank, extension-degree, or QIPM lower-bound theory.
This was a targeted primary-source screen through 2026, not an exhaustive
novelty determination; quaternionic specialist review is still needed.

The independently audited
[same-instance query/readout companion](2026-09-04-hermitian-exposed-rank-query-readout-boundary.md)
specializes the grouped Hermitian perspective lift to balanced hidden-sign
supports.  Its certificate and principal-minor calculations give rank
\(q\) and the exact uniform scale \(\Delta=1\) on every hidden instance.
Standard phase kickback prepares the normalized signed optimizer state with
one raw query.  For every fixed \(\epsilon<1/8\), a degree-\(T\)
Fourier-span/Holevo/rate-distortion argument gives a matching
\(\Theta_\epsilon(s-1)\) bounded-error quantum and randomized query cost for
a full classical feasible projected or explicit lifted
\(\epsilon\)-optimal solution.  At accuracy below
\(1/[8(s-1)]\), the simpler pointwise argument recovers every sign and
parity.  The scalar optimum is public.  Van Dam's oracle-interrogation work
is the classical source boundary for approximate bit recovery: its
fixed-distortion examples use linear-in-\((s-1)\) query counts with improved
quantum constants.  The linear lower bound here comes from the companion's
separate span/information argument.  This is a candidate exact synthesis of
standard ingredients with the new exposed-rank geometry; it is not a
priority claim for phase kickback, oracle interrogation, parity, or
Schur-complement modelling.

The companion also prevents a stronger uniform-oracle reading.  It proves
the quantifier gap
\[
 \inf_{\mathcal L}\sup_v r_{\mathcal L}(v)=q,
 \qquad
 \sup_v\inf_{\mathcal L}r_{\mathcal L}(v)=1:
\]
after a support-dependent projection rotation, any fixed objective becomes
the rank-one north pole.  For the balanced-sign family this rotation can be
applied coherently with one sign query, even though outputting its full
classical matrix requires all signs.  No screened source was found that
combines this exact rank/scale certificate, state-versus-full-output
hierarchy, and formulation quantifier obstruction.  The safe conclusion is
only that a formulation-independent raw-query lower bound cannot follow
from exposed rank without a charged compilation/access contract.  Movement
and readout costs are simultaneous and are not multiplied.

## 20. Fourteenth targeted screen: genuinely coupled symmetric box barrier

Screen date: 2026-09-04.  The companion
[coupled symmetric box
note](2026-09-04-genuinely-coupled-symmetric-box-barrier-tax.md) studies
\[
 F_r(x)=-\sum_i\log(1-x_i^2)-\log(r-\|x\|_2^2)
\]
on \((-1,1)^r\).  It has full signed-permutation symmetry, genuine Hessian
coupling, and exact parameter \(r+1\), yet separated positive objective
scales give central-arc/same-endpoint-distance ratio at least
\(\Gamma_{r-1}=\Theta(\sqrt{\log r})\).

Papa Quiroz--Oliveira,
[*New Self-Concordant Barrier for the
Hypercube*](https://doi.org/10.1007/s10957-007-9220-2), is the closest
explicit alternative cube-barrier source found.  Its \(3r/2\)-parameter
barrier is a coordinate sum with a diagonal Hessian; the paper computes
geodesics and develops path-following algorithms, but does not treat a
coupled barrier or the candidate \(\Gamma_{r-1}\) distortion.  Nesterov--
Todd's product-distance examples and Nesterov--Nemirovski's
\(O(\nu^{1/4})\) bounded-domain theorem are the direct classical metric
comparators.  The latter uses the standard separable box barrier in an
example, not the radial coupling above.

Deza--Nematollahi--Terlaky,
[*How Good Are Interior Point Methods?*](https://doi.org/10.1007/s10107-006-0044-x),
already show that redundant inequalities can change a cube central path
drastically: many asymmetric redundant linear constraints make a
Klee--Minty path visit neighborhoods of exponentially many vertices.  That
literature prevents any broad priority claim about redundancy-induced path
distortion.  Its construction does not use one symmetric nonlinear
redundant inequality, keep parameter \(r+1\), or prove a same-endpoint
Hessian-distance ratio for the resulting coupled metric.

Lee--Yue and Chewi prove the optimal dimension parameter for the universal
and entropic barriers.  Both canonical barriers specialize to separable
products on a box, so they do not answer the genuinely coupled question.
The targeted primary-source search did not locate the displayed radial
augmentation, its bounded-channel multiscale proof, or the exact
\(\Gamma_{r-1}\) conclusion.  The safe label is **candidate explicit
coupled-barrier counterexample**, not the first nonstandard cube barrier,
the first redundant-constraint path pathology, or an arbitrary-barrier
lower bound.  This was a targeted screen through 2026, not an exhaustive
novelty determination.

## 21. Fifteenth targeted screen: optimal-parameter dense coupled box barrier

Screen date: 2026-09-04.  The companion
[dense coupled box
note](2026-09-04-exact-optimal-dense-coupled-box-barrier-tax.md) adds the
rank-one quadratic \((8r)^{-1}({\bf1}^Tx)^2\) to the standard box barrier,
proves that the resulting dense-coupled barrier still has the exact optimal
parameter \(r\), and exhibits \(\Gamma_r=\Theta(\sqrt{\log r})\)
central-arc/same-endpoint-distance distortion.

Nesterov--Vial,
[*Augmented Self-Concordant Barriers and Nonlinear Optimization Problems
with Finite Complexity*](https://doi.org/10.1007/S10107-003-0392-8),
already develop arbitrary PSD quadratic augmentations of
self-concordant cone barriers.  On their unbounded conic domain the
augmentation is self-concordant but is not itself a barrier with uniformly
bounded Newton decrement.  Thus they establish the perturbation template,
but not the bounded-box exact-parameter statement.

Castro--Cuesta,
[*Quadratic Regularizations in an Interior-Point Method for Primal
Block-Angular Problems*](https://doi.org/10.1007/s10107-010-0341-2), are a
closer collision.  They add a diagonal PSD quadratic to the two-sided box
log barrier and prove that sufficiently small scalar coefficients preserve
parameter one per coordinate, hence the exact dimension parameter for the
product.  Their Operations Research Letters paper
[*Existence, Uniqueness, and Convergence of the Regularized Primal--Dual
Central Path*](https://doi.org/10.1016/j.orl.2010.07.010) studies the same
regularized path.  Accordingly, quadratic box regularization and exact
optimal-parameter preservation are prior art in the separable diagonal
case.  The papers optimize preconditioning and convergence, not Hessian
arc/geodesic distortion.

Papa Quiroz--Oliveira give another nonstandard separable cube barrier;
Nesterov--Todd and Nesterov--Nemirovski provide the metric framework and
generic path comparisons.  The targeted primary-source search did not find
a non-diagonal dense quadratic with an exact unchanged parameter proof, or
its combination with the sharp \(\Gamma_r\) multiscale distortion.  The
safe label is **candidate dense-coupled optimal-parameter specialization
and sharp centrality-tax synthesis**.  The conjunction is the unlocated
part; none of quadratic augmentation, exact parameter preservation in the
diagonal case, or generic central-path geometry is new.  This was a
targeted screen through 2026, not an exhaustive novelty determination.

The later [hyperoctahedrally coupled
family](2026-09-04-exact-optimal-hyperoctahedral-box-barrier-tax.md)
strengthens this example in two directions.  It uses
\[
 -\sum_i\log(1-x_i^2)-\lambda\log(c-\|x\|^2),
 \qquad \lambda\geq1,\quad c-r\geq4\lambda,
\]
so the barrier is invariant under every signed permutation, and it still
has exact parameter \(r\) and the full \(\Gamma_r\) tax.  Varying \(c\)
with \(\lambda\) also makes the generic sum certificate \(r+\lambda\)
overcount the exact parameter by an arbitrarily large additive amount.
The sources above cover quadratic augmentation, diagonal regularization,
alternative separable cube barriers, and generic metric geometry; the
completed targeted screen did not locate this larger-ball logarithmic
family, exact parameter preservation for it, or the combined symmetry and
tax statement.  The conservative label is **candidate explicit
optimal-parameter radial-family synthesis**, not a theorem about every
optimal or symmetric cube barrier.  The companion facet-regular theorem
extends the tax to \(U+G\) whenever the convex coupling has bounded first
two derivatives on a full signed facet collar; it leaves singular coupling
outside that regularity class open.

## 22. Sixteenth targeted screen: exact scalar centrality dilation

Screen date: 2026-09-04.  The companion
[scalar dilation note](2026-09-04-exact-scalar-centrality-dilation.md)
reduces the accuracy-sublevel/central-endpoint comparison for
\(b(x)=-\log(1-x^2)\) to the exact one-variable constant
\[
 {68743\over50000}<c_\star
 =\sup_{y>0}{p^{-1}(yp'(y))\over y}
 =1.37486420044\ldots<{69\over50},
\]
and proves the rational upper bound without using the displayed numerical
maximizer.

Nesterov--Nemirovski's 2008 Example 5.1 uses this same standard box
barrier and computes local quantities for a refined short-step complexity
comparison.  Their bounded-domain theorem gives the generic
\(O(\nu^{1/4})\) central-path/geodesic bound, not the coordinate dilation
optimization or the constant above.  Nesterov--Todd's 2002 hypercube
example gives exact product geodesics after a scalar metric transform, but
for the different barrier \(-\log\cos\tau\).  Papa Quiroz--Oliveira also
compute a diagonal cube-barrier geometry for a different scalar summand.

The targeted primary-source search did not find
\(\sup_y p^{-1}(yp'(y))/y\), its numerical value, or the KKT scale matching
that makes it a uniform central-endpoint dilation.  The safe label is
**candidate exact scalar constant refinement** within the local
spectral-interval theorem.  The elementary integral and one-dimensional
optimization are not claimed as a new general method, and the note does
not prove that \(c_\star\Gamma_r\) is the globally sharp multivariate
constant.  This was a targeted screen through 2026, not an exhaustive
novelty determination.

The [sharp separable
theorem](2026-09-04-sharp-separable-centrality-tax.md) also proves the
profile-uniform comparison
\[
 L_{\rm CP}(\epsilon)
 \leq C_{\rm sc}\Gamma_r L_{\rm opt}(\epsilon),
 \qquad C_{\rm sc}<2,\qquad
 C_{\rm sc}\approx1.831856423,
\]
for every fixed normalized scalar one-self-concordant barrier.  This
constant is exact for the relaxed differential-envelope problem using the
profile-independent safe scale \(\log2\); it is not proved globally sharp
over products of one fixed smooth scalar barrier.  The existing Riemannian
and box-barrier sources supply the differential ingredients and generic
comparisons but do not state this optimized envelope constant.  The
conservative label is **candidate universal separable comparison
refinement**, with the global fixed-barrier minimax explicitly open.

## 23. Seventeenth targeted screen: selection-free Lorentz barrier frontier

Screen date: 2026-09-04.  The companion
[selection-free Lorentz barrier
note](2026-09-04-selection-free-lorentz-standard-barrier-cap.md) proves the
universal lower value
\(q=\lceil(s-1)/(d-2)\rceil\), exactness off the divisible seam, and the
extra lower unit for every unbounded lift in the divisible regime through a
two-scale recession determinant lemma.  The later arbitrary-factor
wide-cap theorem closes every bounded divisible case with
\(d-2\geq q-1\), including all quotient-two cases.  Only the bounded
narrow-cap range \(d-2\leq q-2\) remains open.

Classical SOC modelling in Ben-Tal--Nemirovski supplies the recursive norm
upper constructions.  Cardoso--Vieira and Güler--Tunçel identify the
ambient symmetric-cone optimum with Jordan rank.  Gouveia--Parrilo--Thomas
give the lift/slack-factorization correspondence, while Gouveia--Robinson--
Thomas extend it to noncompact convex sets and recession-sensitive slack
operators.  Fawzi's SOC-rank work and Saunderson's face-chain obstructions
are the closest product-cone lift lower-bound comparators.  None of these
screened statements computes the standard product determinant's parameter
after arbitrary affine restriction to a ball.

The targeted primary-source search did not locate the exact off-divisible
formula, the generic all-certificate curvature proof, or the additive
two-scale bound \(\nu\ge r+z\) coupling a recession rank with a complementary
boundary nullity.  Nor did it locate the later factor-count-independent
wide-cap proof, which combines a universal source-face codimension budget,
singleton boundary fibers, active-label globalization, and the obstruction
to an injection \(S^{q(d-2)}\to(S^{d-2})^q\).  The safe label is
**candidate selection-free restricted-standard-barrier frontier in the
proved regimes**.  The ingredients are classical, the bounded narrow-cap
case remains unresolved, and the result is not an arbitrary-barrier or
unrestricted QIPM lower bound.  This was a targeted screen through 2026,
not an exhaustive novelty determination.

The [Hermitian wide-cap
companion](2026-09-04-arbitrary-factor-wide-cap-hermitian-barrier-rigidity.md)
gives the same exact \(q+1\) conclusion for arbitrary finite products of
real, complex, or quaternionic PSD cones of order at most \(R\), where
\(B=a(R-1)\), \(s-1=qB\), and \(B\geq q-1\).  Its endpoint is an impossible
homeomorphism from \(S^{qB}\) to
\((\mathbb F P^{R-1})^q\), detected by mod-two cohomology in degree
\(a\in\{1,2,4\}\).  The already-screened symmetric-cone classification,
slack-factorization, face-chain, and barrier-optimality sources provide the
ingredients, but no cited source states this affine-slice parameter theorem
or its factor-count-independent compact-fiber argument.  Priority therefore
remains provisional.  Together with the recession theorem, the only fixed-
type Hermitian divisible cases left open are bounded and satisfy
\(q\geq B+2\).

## 24. Eighteenth targeted screen: all-simple-EJA frontier and query boundary

Screen date: 2026-09-04.  The [all-simple-EJA exposed-rank
theorem](2026-09-04-selection-free-symmetric-cone-exposed-rank-frontier.md)
sets
\[
 B=\max_i a_i(r_i-1),\qquad q=\left\lceil{s-1\over B}\right\rceil,
\]
and proves that \(q\) is the exact selection-free minimum-certificate-rank
frontier over repeatable dictionaries of simple symmetric cones.  It also
proves the dense-open/full-measure strengthening, a Peirce-perspective upper
construction valid for the Albert cone, the
\(\Theta_\theta(\sqrt q)\) bounded-Dikin movement minimax, and exact
restricted standard-barrier value \(q\) off the divisible seam.

Faraut--Korányi supplies the EJA and Peirce calculus; Hauser--Güler supplies
the classification of self-scaled barriers; Cardoso--Vieira identifies
Jordan rank as the optimal ambient symmetric-cone parameter; and
Schmieta--Alizadeh and Permenter provide the nearest all-symmetric-cone IPM
framework.  Aubrun--La Piana--Müller-Hermes treat positive-map
factorization through Lorentz cones, including the Albert cone, but not
support-fiber rank or affine ball-lift minimax.  The targeted screen did not
locate the exact \(\lceil(s-1)/B\rceil\) formula, its essential-infimum
version, or the field-independent Peirce-perspective attainment.  The safe
label is **candidate exact all-EJA support-certificate and
restricted-standard-barrier synthesis**; the EJA ingredients and generic
Dikin-distance conversion are prior art.

The [same-instance query/readout
companion](2026-09-04-symmetric-cone-exposed-rank-query-readout-boundary.md)
combines, in the divisible case, exact certificate rank \(q\), exact support
scale \(\Delta=1\), one-query preparation of hidden-sign amplitude states
under a charged public-magnitude contract, and
\(\Theta_\epsilon(s-1)\) raw-query complexity for explicit classical
\(\epsilon\)-optimal output.  It also proves the formulation quantifier gap
\(\inf_{\mathcal L}\sup_v r_{\mathcal L}(v)=q\) versus
\(\sup_v\inf_{\mathcal L}r_{\mathcal L}(v)=1\).  No screened source states
this conjunction.  The movement and readout lower bounds are simultaneous
maximum-type obstructions, not a product and not an unrestricted QIPM
runtime lower bound.  This was a targeted screen through 2026, not an
exhaustive priority determination.
