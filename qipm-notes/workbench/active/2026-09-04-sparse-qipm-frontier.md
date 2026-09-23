# Sparse-QIPM frontier: 2026-09-04 completed cycle

Status: Research cycle closed
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: Preliminary  
Question: Which new theorem can materially sharpen the positive or negative
complexity frontier for sparse quantum interior-point methods?

## Status convention

This is the historical research ledger for the closed cycle. Claims are
labeled as follows.

- **Proved:** a complete argument has been written and independently audited.
- **Candidate theorem / synthesis:** a proof is present, but its audit or
  priority status is stated locally and should be checked before reuse.
- **Conditional:** the conclusion depends on an explicit unresolved assumption.
- **Conjecture / lead:** useful direction, not a result.
- **Refuted:** the proposed statement is false; the counterexample is retained to prevent reuse.

No claim in this file should be advertised as novel merely because it is absent
from the local repository. Apparent novelty requires a targeted open-literature
search, and priority cannot be guaranteed by such a search.

The final audited results, surviving caveats, and deliberately open problems
are indexed in the [research closure
summary](2026-09-04-research-closure-summary.md).

## Baseline inherited from the 2026-09-02 cycle

The paper and closure audit already contain strong results on:

1. central-path conditioning from sublevel geometry;
2. block log-det condensation and mass--conditioning--visibility laws;
3. sparse LP and SDP query-hardness families, including state-output bounds;
4. normalization, preconditioning, recovery, and iterate-interface tradeoffs;
5. exact-path lazy refresh, implicit dual coordinates, and block-angular border
   aggregation as conditional positive modules; and
6. several no-go frontiers for local-linear parity gadgets.

The present cycle must therefore avoid presenting any of those mechanisms as
new. The initial targets are the open problems listed in
`paper/sections/16-discussion.tex`, together with genuinely different
algorithmic and lower-bound directions.

## Historical starting tracks and future follow-ups

- exact normalization for shifted block encodings;
- a general-inner small-success composition theorem;
- intrinsically nonabelian word-query hardness and its SDP transfer;
- a bounded-scale, bounded-degree full-KKT amplifier or a sharper impossibility
  theorem;
- a low-parameter projected block-angular barrier;
- bounded-treewidth and separator-sensitive QIPM complexity;
- broad sparse-QIPM dequantization under matched access and output contracts;
- amortized path-following through correlated Newton systems.

## Results of this cycle

Audited and candidate results are now recorded separately:

- [General-inner small-success composition](2026-09-04-general-inner-small-success-composition.md)
  closes open problem A2, with a necessary subtractive baseline term.
- [Intrinsically nonabelian \(A_5\) holonomy hardness](2026-09-04-nonabelian-a5-holonomy.md)
  closes open problem A5 and transfers to a bounded-incidence, condition-one
  sparse SDP and its Newton-state output.
- [Lorentz-cone winner condensation](../parked/2026-09-04-lorentz-cone-condensation.md)
  was proved but parked after its \(D=3\) case was recognized as exactly the
  existing \(2\times2\) PSD condensation theorem; it remains a useful explicit
  SOCP corollary.
- [Exact normalized two-cluster shift](2026-09-04-exact-two-cluster-shift.md)
  gives a two-query QSVT construction and a contrasting interval-promise
  lower bound; it also identifies a needed correction to the paper.
- [Two-interval normalized-shift theorem](2026-09-04-two-cluster-interval-shift-upper.md)
  closes that interval-promise gap at relative error above an exact affine
  threshold, and proves a hierarchy of stronger fixed-QSVT obstructions below
  successive approximation thresholds.
- [Adaptive normalized-shift lower-bound hierarchy](2026-09-04-adaptive-normalized-shift-hierarchy.md)
  extends the obstruction beyond QSVT: vanishing relative error forces
  \(\Omega_\varepsilon(\delta^{-1+\varepsilon})\) queries for every
  \(\varepsilon>0\) in the reusable-unitary model.
- [Normalized-shift query staircase](2026-09-04-normalized-shift-staircase.md)
  gives the complete phase diagram, a closed Chebyshev formula and sharp
  asymptotic for every threshold, and an explicit polynomial separation
  between mixed-parity generalized QSP and every standard definite-parity
  QSVT sequence.
- [Joint gap--accuracy normalized-shift law](2026-09-04-joint-accuracy-normalized-shift.md)
  upgrades the fixed-accuracy hierarchy to growing accuracy.  Two independent
  finite-order proofs and a contractive integrated-sign construction give
  \(Q=\Theta_{\rho,\beta}(\delta^{-1}\log(1/K))\) whenever
  \(K\leq\delta^\beta\), with no upper restriction on \(\log(1/K)\).
  Equivalently, normalized complement conversion to error
  \(\epsilon\leq\delta^{1+\beta}\) costs
  \(\Theta_\beta(\delta^{-1}\log(1/\epsilon))\).  A separate
  [uniform pinned-gate construction](2026-09-04-joint-accuracy-pinned-gate.md)
  also gives the sharper sublinear exponent throughout
  \(\log(1/K)=o(\log(1/\delta))\).
- [Sparse LP Newton access separation](2026-09-04-sparse-lp-newton-access-separation.md)
  realizes the shift hierarchy on a genuine exact-central three-variable LP
  and proves a tight \(\kappa\)-versus-\(\sqrt\kappa\) normal-matrix/factor
  Newton-state separation.  At high accuracy its complement compiler has the
  sharper \(\Theta(\kappa\log(1/\epsilon))\)-versus-\(O(1)\)
  normal-matrix/factor gap, with the sparse-value bypass stated explicitly.
- [Quantum barrier compilation for a sparse tree SOCP](2026-09-04-quantum-barrier-compilation-socp.md)
  gives a query-optimal positive conic result with an exact barrier/path-length
  reduction and a matched explicit-loading closure.
- [Local full-KKT parity--mass obstruction](2026-09-04-local-full-kkt-parity-mass-obstruction.md)
  rules out the paper's remaining bounded-scale local amplifier target across
  arbitrary nonorthogonal mixed-mode constructions.
- [Sparse-Newton dequantization envelope](2026-09-04-sparse-newton-dequantization-envelope.md)
  gives a cone-agnostic exclusion criterion for dense-transcript hybrid QIPMs.
- [Bounded-treewidth full-output trajectory replacement](2026-09-04-bounded-treewidth-full-output-no-advantage.md)
  upgrades the one-system output ceiling to an adaptive IPM sequence theorem,
  adds a condition-one treewidth-zero oracle-interrogation lower bound for a
  classical Newton direction, and closes symbolic reuse, numerical stability,
  chordal-SDP, parallel-depth, and coherent-refresh assumptions.
- [Bounded-degree treewidth-one simplex search
  boundary](2026-09-04-simplex-search-central-path-treewidth-boundary.md)
  gives the complementary compressed-output obstruction.  A balanced
  summation-tree lift has \(O(N)\) coefficients in
  \(\{-1,0,1\}\), a public analytic center, and an actual augmented KKT graph
  that is a maximum-degree-three tree.  At the public path parameter
  \(\eta=N-2\), one literal bounded subtree-sum coordinate decides which
  public half contains a unique marked objective coefficient.  Its matched
  raw-input and canonical full-SQ query laws are exactly
  \(Q=\Theta(\sqrt N)\) and \(R=\Theta(N)\), including offline compilation
  of the exact current-iterate SQ interface.  Every exact Newton solve still
  costs \(O(N)\) arithmetic.  Since the displayed barrier has \(\nu=N\),
  this is also an unconditional total raw-query lower bound
  \(\Omega(\sqrt\nu)\) quantum and \(\Omega(\nu)\) randomized even when the
  tree decomposition and all exact solves of fully specified Newton systems
  are free.  It is not an iteration lower bound.  The reduced leaf Hessian has condition
  \(N-1\), and no common input-oblivious square invertible two-sided
  preconditioner can reduce the worst marked instance below \(N/2\); this
  follows because the pairwise generalized spectrum survives the relative
  product \(LG_kR(LG_jR)^{-1}\) by similarity.  The exact pair eigenvalue
  \(\tau_N=N-1-\Theta(1/N)\) is also the search-completeness threshold:
  constructing an effective classical adaptive two-sided preconditioner
  with target \(K<\tau_N\) costs
  \(\Theta(\sqrt N)\) quantum or \(\Theta(N)\) randomized queries.  One
  fixed output pair can serve at most one marked index, while finding that
  index supplies a succinct exact rank-one inverse.  The
  accuracy--conditioning extension is nearly minimax-sharp for every
  central readout offset \(\delta\): its common-preconditioning lower and
  identity upper differ by less than \(1/(N-1)\), with a closed-form exact
  pairwise generalized-eigenvalue threshold.  Constructing an adaptive
  preconditioner below that threshold is again search-complete.  For
  \(\delta=\Theta(1/N)\), the reduced Newton condition is constant while
  recovering the scalar to the required inverse-linear accuracy still costs
  \(\Theta(\sqrt N)\) quantum or \(\Theta(N)\) randomized queries.  Thus
  search hardness here need not be caused by poor reduced conditioning,
  although no finite-precision or end-to-end runtime separation follows.  The
  independently audited result refutes a dimension-independent classical
  query bound based only on treewidth and degree.  It is a compressed-task
  obstruction, not a constructed \(O(\sqrt N)\)-time QIPM, and makes no
  full-KKT condition-number claim.
- [Product-disk central-readout query
  hierarchy](2026-09-04-product-disk-central-readout-query-hierarchy.md)
  gives a sharper output-contract separation on the exact host domain
  \((B_2^2)^N\), represented by the analytically minimum product
  \(Q_3^N\).  At the fixed public multiplier \(\eta=2\), the reduced
  barrier Hessian has condition exactly \(\sqrt5\), its structural graph is
  a disjoint union of constant-size components, and the exact normalized
  central state is prepared by one canonical hidden-bit query.  Nevertheless
  the centered scalar
  \[
                  Nr(2)+\sum_i x_i=r(2)|b|
  \]
  has exact arbitrary-input query law
  \(Q=R=\Theta(N)=\Theta(\nu_{\rm red})\) at constant additive
  accuracy, by parity.  Under the zero-versus-one-mark promise it instead
  gives the sharp Grover separation
  \(Q=\Theta(\sqrt N)\), \(R=\Theta(N)\).  Any explicit feasible
  \(1/8\)-suboptimal solution recovers all hidden bits and hence also needs
  \(\Omega(N)\) quantum queries.  A sign-balanced public slice strengthens
  the scalar statement to the ordinary optimum value while keeping every
  raw objective-block norm, coordinate magnitude, sampling probability,
  and coordinate-column norm input-independent; its reduced Hessian has
  condition at most four along the entire path.  The bounds cover raw
  coefficient, constant-size block, ordinary vector-SQ, and the specified
  canonical coherent-SQ access.  They do not cover free norms of the
  equality-eliminated objective or hidden central iterate, either of which
  leaks the answer.  Nor does a constant local-neighborhood guarantee alone
  force the scalar accuracy: it needs \(O(N^{-1/2})\) local error.  Thus the
  theorem is a total formulation-query/readout boundary, not an iteration
  lower bound. Rescaling the sign-balanced sliced objective to public raw
  norm \(\Gamma\) gives the complete accuracy laws
  \[
   Q=\Theta(\min\{N,\Gamma\sqrt N/\epsilon\}),\qquad
   R=\Theta(\min\{N,\Gamma^2N/\epsilon^2\}).
  \]
  An equivalent encoding makes this sliced objective entirely public and
  puts each hidden sign in a disjoint two-sparse equality row with
  \(EE^T=2I\); the nullspace basis is one-query coherently accessible but
  not free classically.
  Hence quantum readout saturates at normalized error
  \(\epsilon/\Gamma=\Theta(N^{-1/2})\), versus
  \(\Theta(N^{-1})\) for the direct one-ball theorem below. At the same
  raw norm \(\Gamma=\sqrt N\) and fixed accuracy this is
  \(\Theta(N)\) versus \(\Theta(\sqrt N)\) quantum queries, while both
  randomized costs are \(\Theta(N)\). This compares different feasible
  geometries and is not a same-problem formulation separation.
  Packing the unsliced disks into one PSD factor of order \(N+2\) gives a
  separate same-instance synthesis: \(L=1\), exact
  \(\nu_{\rm slice}=N\), latent Newton treewidth one, the same one-query
  normalized projected central state and \(\Omega(N)\) scalar/full-output
  query bounds, and, for the fixed standard restricted log-determinant, the
  path-independent bounded-Dikin lower bound
  \[
    \Omega_{\rho,R,m}(\sqrt N\log(N/\epsilon))
  \]
  from the analytic center. The state claim is only for the projected disk
  variables, not the dense lifted Gram auxiliary. A stronger combined
  encoding adds the disjoint hidden sign rows inside that same packed PSD
  lift and makes the objective entirely public. At raw norm
  \(\Gamma=\sqrt N\) and fixed small accuracy it retains
  \(L=1\), \(\nu_{\rm slice}=N\), the latent forest,
  \(\Omega(\sqrt N\log N)\) bounded-Dikin rounds,
  \(Q=R=\Theta(N)\) scalar/projected-full-output queries, and \(O(1)\) normalized
  projected-state queries on one sparse-data formulation. The query and
  movement lower bounds are simultaneous and are not multiplied. The separately
  stated, independently audited
  [arbitrary-cap companion](2026-09-04-product-ball-central-state-readout-separation.md)
  extends the one-query-state versus Grover-readout hierarchy to
  \((B_2^s)^B\): with
  \(h=\lceil s/(d-2)\rceil\) below the direct-cone threshold, it uses the
  exact \(Bh\)-block analytic frontier, has latent treewidth one and a
  publicly rescaled reduced-Hessian condition at most \(27/2\), and has
  all-diagnostic query law \(\Theta(B\sqrt s)\) quantum versus
  \(\Theta(Bs)\) randomized.  It is retained as a cap-dependent companion,
  not a second headline, because its amplified diagnostic is subject to the
  same local-norm-output caveat.
- [One-cone SOCP exponential SQ separation](2026-09-04-exponential-sq-separation-one-cone-socp.md)
  transfers the Grønlund--Larsen hard sparse linear systems to an exact
  Lorentz-barrier Newton state, giving a matched-access
  \(\operatorname{polylog}N\) versus \(\Omega(N^{1-1/k})\) compressed-output
  separation.  A cyclic-clock refinement gives the parameterized lower
  exponent \(\exp(\Omega(K\log s\log(1/\epsilon)))\) on the same one-cone
  Newton/optimizer state, even when full SQ access to the sparse reduced
  Hessian and its Newton right-hand side is supplied directly.  For fixed
  \(k\), the block-Hadamard \(k\)-Forrelation version also retains
  \(\widetilde\Omega_k(N^{1-1/k})\) classical hardness while varying both
  conditioning and sparsity.
- [One-cone SOCP scalar-observable separation](2026-09-04-one-cone-socp-scalar-observable.md)
  adds a public sparse accumulator and upgrades the separation to the same
  classical decision-bit/scalar-coordinate output on both sides.
- [Parameterized one-cone scalar frontier](2026-09-04-parameterized-one-cone-scalar-frontier.md)
  combines the cyclic conditioning family with a public three-sparse
  accumulator.  A literal optimizer coordinate at additive accuracy
  \(\delta\) has classical SQ complexity
  \(\exp(\Omega(K\log s\log(1/\delta)))\), while the structured coherent
  instance needs only constant hidden quantum queries.  This removes the
  rare-event prefactor and vanishing-failure caveat of solution sampling and
  transfers from exactly feasible objective gap \(\Theta(\delta^2/K)\).
  Its fixed-\(k\) version simultaneously gives
  \(\widetilde\Omega_k(N^{1-1/k})\) ambient-dimension hardness. A public
  clock-only normalization of the objective tilt upgrades the same bound to
  ordinary optimal-value approximation at additive accuracy
  \(2^{-O(k)}\delta/\sqrt K\); an independently valid small-tilt argument
  gives the weaker fallback \(2^{-O(k)}\delta^2/K\). An exact
  binary norm-tree lift preserves that value separation using only
  three-dimensional Lorentz cones.  Balanced-tree symmetry also preserves
  the hard first Newton direction.  At the public analytic center, the
  tilted problem's squared Newton decrement is exactly a public multiple of
  the hard optimal value squared, so the lower bound survives even with
  direct full-SQ access to the sparse SPD Newton matrix and right-hand side.
  The same Hessian and normalized decrement arise at the public analytic
  center of the scalar-inequality LP \(-\mathbf1\leq Mx\leq\mathbf1\), so
  the diagnostic separation is already an LP path-following lower bound.
  For the unperturbed LP, the entire central path is
  \(x(\eta)=\rho(\eta)M^{-1}e\), so its normalized iterate and accumulated
  scalar remain hard beyond the first step. Strong convexity of the box
  barrier transfers this to an approximate centering-subproblem gap
  \(2^{-O(k)}\delta^2/K\).
  In the bounded-cone lift that multiple is \(1/[2(D-1)]\); the value and
  normalized-direction gaps are unchanged, while the decrement accuracy
  must retain this factor. The stronger one-cone squared-decrement scale is
  \(2^{-O(k)}\eta^2\delta/\sqrt K\).
- [Fixed-instance sparse-KKT temporal
  collapse](2026-09-04-fixed-instance-sparse-kkt-temporal-collapse.md)
  gives the complementary noncomposition theorem. For the one-Lorentz
  ellipsoid \(u=Mx\), every exact central predictor solves the literal
  \((s+2)\)-sparse augmented KKT system to the same normalized state
  \((e,M^{-1}e,0)/\sqrt{1+\|M^{-1}e\|^2}\), although reaching objective
  gap \(\epsilon\) from the analytic center needs
  \(\Omega_R(\log(1/\epsilon))\) bounded-Dikin moves. An elementary
  four-sparse signed-tree instance has \(\kappa=\Theta(L)\), needs
  \(\Theta(L)\) queries to prepare that state at any one checkpoint, and
  has a constant-width \(O(L)\)-time classical forward solve. The
  precision-sensitive Mori parity clock gives
  \(\Omega(\kappa\log(1/\delta))\) instead. In both cases, reading the
  hidden bits and solving once serves any number of checkpoints. Thus even
  literal repeated KKT hardness cannot be multiplied by movement without a
  joint final-output, online, oracle-revocation, or memory adversary. This
  is a raw-query obstruction; repeated state-preparation gates, dense
  writes, and arithmetic remain chargeable resources.
- [One-barrier boxed parity
  chain](2026-09-04-boxed-parity-chain-readout-separation.md) gives an even
  smaller state/readout obstruction with public objective and hidden
  two-sparse equalities.  Only the first chain coordinate is boxed.  After
  equality elimination the objective coefficient is
  \(1+2\prod_m\sigma_m\), so the optimum is exactly \(3\) or \(1\): every
  multiplicative estimate with relative error \(\gamma<1/2\) needs
  \(\Theta(N)\) quantum and randomized raw, sparse, or charged full-SQ
  queries.  The fixed public center \(\eta=1\) has the constant-separated
  values \(\sqrt{10}-1\) and \(\sqrt2-1\).  In contrast, the restricted
  barrier \(-\log(1-\alpha^2)\) has exact parameter one because
  \(\sup(\phi')^2/\phi''=1\), the reduced Hessian has condition one, and
  every normalized reduced optimizer, center, or predictor is the same
  one-dimensional state up to global phase.  This does not make equality
  elimination free: the hidden nullspace basis is the prefix-parity state.
  The literal equality-embedded KKT graph is a path of treewidth one and,
  at a fixed center, has condition \(\Theta(N)\), while a classical forward
  solve costs \(O(N)\).  Boxing every chain coordinate would instead give
  parameter \(N+1\) and KKT condition \(\Theta(N^2)\).  Query, movement,
  and solve costs are simultaneous max-type bounds, never a product.
- [Multiplexed sparse-LP central-path direct sum](2026-09-04-multiplexed-lp-central-path-direct-sum.md)
  upgrades the one-checkpoint box-LP statement to one trajectory carrying
  \(B\) independent hard instances. Geometrically separated objective scales
  make consecutive shared-accumulator increments an almost diagonal
  convolution with constant total cross-talk. Returning the \(B\) selected
  increments to additive \(O(\delta)\) therefore costs
  \(\Omega(Bq^{\ell/2}/(r\ell))\) classical full-SQ queries, while the
  structured source realization uses \(O(B)\) quantum queries. The lower
  bound survives exact-feasible approximate centering gaps
  \(\Theta(\delta^2/(BK))\). This is explicitly a checkpoint-increment trace
  contract, not a lower bound for algorithms returning only a final optimum.
- [Multiplexed SOCP Newton-decrement direct sum](2026-09-04-multiplexed-socp-decrement-direct-sum.md)
  removes the custom increment observable: the ordinary squared predictor
  decrement at each of \(B\) selected central points reveals a different
  independent Forrelation instance after subtracting a public baseline.
  Radial Lorentz geometry gives an exact band-pass sensitivity kernel and
  hence the classical lower bound
  \(\Omega(Bq^{\ell/2}/(r\ell))\), versus \(O(B)\) structured quantum
  queries. With the natural relative update \(\sigma=\Theta(B^{-1/2})\),
  every total decrement is \(O(1)\), its required squared accuracy is
  \(\Theta(\delta/(B\sqrt K))\), and the product barrier parameter is only
  \(2B\). The same direct sum lower-bounds building a checkpoint-iterate SQ
  interface that reports active cone-block norms to
  \(O(\delta/\sqrt K)\): those norms themselves reveal the independent
  amplitudes. The theorem concerns a prescribed diagnostic/access trace, not
  a final-optimum-only algorithm.
- [Thresholded Forrelation XOR in one optimizer coordinate](2026-09-04-forrelation-thresholded-single-optimizer-coordinate.md)
  removes both the checkpoint-output and mean-estimation loopholes. A
  constant-size LP threshold gadget converts each promised sparse inverse
  observable \(z\Phi_j\) into an exact unique optimizer bit
  \(t_j^*=g(\Phi_j)\); a public XOR-polytope chain then gives one bounded
  coordinate \(P^*=\bigoplus_{j=1}^Tg(\Phi_j)\). The full LP has a unique
  optimizer, dimension \(\Theta(TN_0)\), sparsity \(s+O(1)\), and a scalar
  product barrier with certified parameter \(\nu_{\log}=12T-4\).
  Perfect adversary composition and the strong randomized XOR lemma give the
  matched same-instance laws
  \[
    Q(P^*)=\Theta(T),\qquad
    R(P^*)=\Omega\!\left(T\frac{q^{\ell/2}}{r\ell}\right),
  \]
  for constant additive accuracy on this one bit. The access augmentation
  and public finite-bit threshold/readout ledger have been independently
  audited. Geometric objective weights place the base count formulation on
  separated path scales, but the XOR barrier couples those blocks; moreover
  the weighted version transfers to an objective-gap solution contract only
  at gap \(O(\Gamma^{-T})\). Taking equal weights restores a constant-gap
  transfer but removes the separated scales. In either form this is static
  endpoint hardness, not a proof that each IPM iteration must pay separately,
  and it is not a normalized-state amplitude lower bound.
- [One-Lorentz constant-barrier value
  lower bound](2026-09-04-one-lorentz-constant-barrier-value-lower.md)
  removes both the growing-product-barrier and hard-nullspace explanations
  from the scalar-readout separation.  One cone \(Q_{2N+1}\) and the public
  orthonormal two-sparse slice \(y_i=x_i\) reduce exactly to a unit ball
  with standard restricted parameter one.  At the public multiplier
  \(\eta_0=1/C\), where the public raw objective norm is \(C\), the reduced
  Hessian is diagonal plus rank one, has
  condition at most \(3/\sqrt5\), latent treewidth one, and an \(O(N)\)
  classical solve. Nevertheless a sign-balanced raw objective makes both
  the ordinary optimum value and its ordinary value at that exact central
  point obey the sharp accuracy-parametric laws
  \[
   Q=\Theta(\min\{N,C/\epsilon\}),\qquad
   R=\Theta(\min\{N,(C/\epsilon)^2\})
  \]
  for \(\epsilon/C\) below a small constant. Taking \(C=N\) recovers
  \(Q=R=\Theta(N)\) at fixed additive accuracy. Any explicit feasible
  solution of gap below \(C/(8\sqrt5N)\) is also quantum-query
  linear, while the normalized optimizer and central states have
  constant-query preparations (heralded exact with constant expected cost,
  or bounded-query constant error).  All raw norms, magnitudes, and
  squared-sampling laws are public. An equivalent and more sparse-data-facing
  encoding makes the objective entirely public and moves every hidden sign
  into a disjoint two-sparse equality row. Its hidden slice matrix satisfies
  \(E_bE_b^T=2I\), so all row norms, singular values, column degrees, and SQ
  sampling laws are public; only queried signs vary. The nullspace basis is
  then hidden but coherently accessible with one query, and granting its
  classical description would reveal the input. The unique-mark promise
  at a sufficiently small constant times \(C/N\) recovers the
  sharp \(Q=\Theta(\sqrt N)\), \(R=\Theta(N)\) separation.  This proves
  that barrier parameter, selected Hessian condition, sparse equality
  elimination, latent treewidth, and easy state output still do not control
  scalar or explicit readout cost.  The access simulation, scaling
  constants, all-regime approximate-counting reduction, path calculation,
  and output reductions were independently hostile-audited. On the same
  reduced-ball instances, the fixed barrier also gives an independently
  audited \(\Omega_{\rho,R,m}(\log(C/\epsilon))\) path-length lower bound
  for feasible trajectories made from a bounded number of bounded-Dikin
  chords per round. This movement bound and the query laws are simultaneous,
  not multiplicative, and do not cover arbitrary long-step QIPMs.
- [Constant-barrier affine-slice LP value lower bound](2026-09-04-affine-slice-lp-value-lower.md)
  gives a more direct, but deliberately qualified, optimization-output
  wrapper: \(Mx=te\), \(|t|\leq1\), with the unit objective \((Ra)^Tx\).
  Its exact optimum is \(R\sqrt p\,|\Phi|=\Theta(\sqrt K\,\delta)|\Phi|\),
  so the same exponential or fixed-\(k\) near-linear classical SQ lower
  bound applies to ordinary LP optimal-value approximation. The equality
  operator has sparsity \(\Theta(q)\) and condition \(\Theta(K)\), while the
  interval barrier has parameter one. Setting \(\delta=\Theta(K^{-1/2})\)
  gives a constant value gap and classical lower bound
  \(\exp(\Omega(K\log s\log K))\); the initial squared Newton decrement is
  exactly \(\eta^2\operatorname{OPT}^2/2\) and has the same constant-error
  lower bound. The feasible affine slice is only
  one-dimensional: the result isolates equality/nullspace preprocessing
  hardness and collapses if a nullspace basis is supplied, so it is not a
  barrier-iteration lower bound.
- [Affine-slice LP value SQ upper bound](2026-09-04-sparse-sq-affine-lp-value-upper.md)
  gives the matching classical scalar side.  A normal-equation Chebyshev
  inverse and one-coordinate overlap estimator approximate
  \(|a^*M^{-1}e|\) in dimension-independent time
  \(\operatorname{poly}(K/\epsilon)
  (d+1)^{O(K\log(K/\epsilon))}\).  If a public bound
  \(R_e\geq\|M^{-1}e\|/\|e\|\) is available, \(K\) inside the logarithm and
  variance ledger improves to \(R_e\).  The clock family has the exact public
  value \(R_e=\Theta(\sqrt K)\), yielding the matching exponent
  \(\Theta(K\log s\log(\sqrt K/\epsilon))\), including constant value
  accuracy.  The upper returns only the scalar, so it does not erase the
  nullspace/explicit-optimizer boundary.
- [Universal cone curvature capacity](2026-09-04-universal-cone-curvature-capacity.md)
  shows that the coarsest curvature budget does not require symmetry,
  homogeneity, or self-duality.  For any exact lift of a positively curved
  \(N\)-body by a product of proper cone factors definable in one o-minimal
  structure,
  \[
    N-1\leq\sum_i c_i\leq\sum_i(m_i-2),
  \]
  where \(c_i\) is the rank of the pairing between the primal and dual
  lineality tangent spaces at a generic complementary contact.  Under a
  factor-dimension cap \(d\), Lorentz norm trees are simultaneously optimal
  for the Euclidean ball even against products of arbitrary such cones:
  \(k_{\min}=\lceil(N-1)/(d-2)\rceil\),
  \(M_{\min}=N-1+2k_{\min}\), and the minimum logarithmically homogeneous
  self-concordant barrier parameter on the ambient product is
  \(\nu_{\min}=2k_{\min}\).  The barrier lower holds even for a coupled,
  nonseparable barrier, by restriction to an orthant section.  The theorem
  covers semialgebraic, exponential, and fixed-power cone products and has
  passed two hostile audits and a targeted literature screen.
- [Exact tame-cone granularity of \(\ell_p\) balls](2026-09-04-lp-ball-exact-cone-granularity.md)
  shows that the simultaneous factor and coordinate optimum is not a
  Euclidean accident. For every fixed \(1<p<\infty\), the known
  \(p\)-order-cone tree is optimal against every definable proper-cone
  dictionary with factor dimension at most \(d\):
  \[
    k_{\min}=\left\lceil\frac{N-1}{d-2}\right\rceil,
    \qquad M_{\min}=N-1+2k_{\min}.
  \]
  The lower bound uses one all-nonzero strictly curved boundary patch; the
  matching tree uses \(K_{p,m}=\{(t,u):t\geq\|u\|_p\}\) blocks and fixes the
  root scalar affinely. Rational \(p\) is semialgebraic and arbitrary fixed
  real \(p\) is \(\mathbb R_{\exp}\)-definable. The ambient LHSC barrier
  lower \(\nu\geq2k_{\min}\) holds, but equality is claimed only for
  \(p=2\). The exact lower/optimality statement has been independently
  audited and literature-screened; the tree upper itself is prior work.
- [Strict barrier premium for products of non-Lorentz \(p\)-cones](2026-09-04-pcone-product-barrier-premium.md)
  strengthens the ambient barrier part under the natural \(p\)-order-block
  dictionary. If every block has dimension at least three, every possibly
  coupled barrier on \(\prod_{i=1}^kK_{p,m_i}\) satisfies
  \[
    \nu\geq k h(p)>2k\qquad(p\ne2),
  \]
  where \(h(p)\in(2,3)\) is Hildebrand's explicit three-dimensional
  cross-ratio bound. A positive-branch product lemma amplifies the local
  witnesses without assuming barrier separability. Consequently the exact
  \(p\)-order tree has \(\nu\geq h(p)\lceil(N-1)/(d-2)\rceil\), and every
  arbitrary minimum-space lift has \(\nu\geq h(p)\) by lift rigidity.
  Rational \(p\)-balls also have finite pure-SOC lifts, proving that this
  premium cannot be transferred per realized factor to arbitrary
  dictionaries; a stronger target-level bound outside minimum space remains
  open. The theorem, formula, product construction, and SOC boundary have
  passed three independent audits and a targeted literature screen.
- [Exact coupled barrier parameter for exponential and one-sided perspective products](2026-09-04-exponential-product-exact-barrier-parameter.md)
  proves that
  \(\nu_{\mathrm{opt}}(K_{\exp}^{R})=3R\) even among arbitrary coupled
  standard self-concordant barriers; the standard separable barrier is
  therefore exactly optimal.  The same holds for dual exponential cones and
  mixed primal/dual products, since the dual is linearly isomorphic to the
  primal cone.  More generally, a product of one-sided
  homogeneous-concave hypograph cones has lower bound
  \(\sum_j(n_j+1)\), and the same certificate gives exact product bounds
  for scalar and matrix relative-entropy perspectives whenever the matching
  barrier is known.  Projection can genuinely reduce the parameter: the
  aggregate \(d\)-coordinate relative-entropy cone has exact parameter
  \(2d+1\), compared with \(3d\) for its coordinatewise exponential-cone
  product lift; \(B\) aggregate blocks with \(N\) total coordinates have
  exact parameter \(2N+B\).  More generally, for every nonnegative
  \(B\times N\) aggregation matrix \(A\), the cone
  \(z-A(D(x_i\|y_i))_i\in\mathbb R_+^B\) has exact optimal parameter
  \(2N+B\).  Its displayed coordinatewise exponential-cone-plus-slack lift
  has exact parameter \(3N+B\), so aggregation that retains all inputs can
  improve the parameter-driven short-step factor by less than
  \(\sqrt{3/2}\), never asymptotically.  The intrinsic optimal barrier has
  an exact block-diagonal triangular Hessian factorization requiring only
  \(O(N+B+\operatorname{nnz}A)\) unit-cost work per cone-Hessian solve.
  The exponential-product theorem passed two hostile audits, and the
  positive-output extension passed a separate hostile audit.  The main
  \(3R\) statement is a short latent
  corollary of Fawzi--Saunderson's general theorem, so its mathematical
  novelty is low; the exact coupled-barrier and aggregation accounting is
  nevertheless useful for sparse-QIPM formulation comparisons.
- [Three-dimensional \(p\)-cone optimal-barrier frontier](2026-09-04-three-dimensional-pcone-optimal-barrier-frontier.md)
  proves that Chares's scaled characteristic-function proposal cannot attain
  Hildebrand's lower bound. For \(p>2\), boundary regular variation forces
  every self-concordant \(\kappa\log\zeta_p\) to satisfy
  \[
     \nu=3\kappa\geq\frac{3p}{p+1}>h(p).
  \]
  This establishes the necessity half, but not the conjectured sufficiency,
  of Chares's numerically proposed scale. Natural defining-function,
  bounded-correction, and nested Lorentz-fiber ansatzes are also ruled out.
  The exact intrinsic optimum remains \(h(p)\leq\nu_{\rm opt}(p)\leq3\).
  Exact asymptotics show a cusp
  \(h(p)=2+W(e^{-1})|p-2|+O((p-2)^2)\) and logarithmic approach to three at
  \(p\to1,\infty\). The obstruction, asymptotics, lift-marginal boundary,
  and literature distinctions have passed independent audits.
- [Rigidity at minimum cone dimension](2026-09-04-minimal-cone-lift-rigidity.md)
  identifies the equality case behind these dimension bounds. Every exact
  proper-cone lift of a full-dimensional compact \(N\)-body needs at least
  \(N+1\) reduced cone coordinates; if equality holds, the cone is linearly
  isomorphic to the homogenization cone of the body and the reduced slice
  projects affinely bijectively. Thus every minimum-space lift of an
  \(\ell_p\) ball uses a cone linearly isomorphic to its \(p\)-order cone:
  no different cone of the same dimension can hide a better barrier. This
  elementary structural lemma has been independently audited; it is useful
  support for the granularity theorem rather than a headline novelty claim.
- [Curvature-saturation nonrigidity](2026-09-04-curvature-saturation-nonrigidity.md)
  identifies the exact local equality case without overextending it.  If
  \(\sum_i(m_i-2)_+=N-1\), every block saturates its tangent-pairing rank;
  after whitening the mixed curvature \(H\), the matrices
  \(H^{-1/2}M_iH^{-1/2}\) are mutually orthogonal projections.  This local
  Parseval decomposition does not classify the global factors.  For every
  \(1<p<\infty\), \(B_p^3\) has a saturated minimum two-block lift using
  \(K_{p,3}\) and \(K_{p,3}\cap\{t\geq0\}\), where the added halfspace is
  redundant in the lift.  The second cone has a two-dimensional exposed
  face and is not isomorphic to the strictly convex \(p\)-order cone.  The
  audited example rules out cone/tree classification or a barrier premium
  derived from local rank saturation alone; it does not rule out a premium
  proved from additional global hypotheses. The audited companion
  [count-saturation arithmetic](2026-09-04-lp-count-saturation-equality.md)
  gives the complete excess interval: for
  \(k_*=\lceil(N-1)/(d-2)\rceil\) and
  \(\sigma=k_*(d-2)-(N-1)\), every count-optimal lift has
  \(0\leq\Delta\leq\sigma\) and reduced dimension
  \(M=N-1+2k_*+\Delta\), and every integer \(\Delta\) in that interval is
  attained by a full-face padded \(p\)-tree.
- [Universal bi-\(C^1\) saturation rigidity and the exact capped
  frontier](2026-09-04-sphere-submersion-curvature-gap.md) is the canonical
  global-integrability result.  If a compact \(N\)-body and its polar have
  \(C^1\), strictly convex boundaries and their full slack has globally
  labelled \(C^1\) factors over arbitrary proper cones, saturation
  \(\sum_i(\dim K_i-2)_+=N-1\) forces exactly one positive-capacity block,
  of dimension \(N+1\).  The normalized maps of all saturated blocks
  assemble into a same-dimensional local diffeomorphism from the contact
  sphere to a product of spheres.  Covering-space theory and cohomology
  rule out every nontrivial saturated partition, with no exceptional Hopf
  dimensions and no classification of individual sphere submersions.
  Hence a cap \(3\leq d<N+1\) forces
  \[
   \sum_i(\dim K_i-2)_+\geq N,\qquad
   k\geq\left\lceil\frac{N}{d-2}\right\rceil,\qquad
   M\geq N+2\left\lceil\frac{N}{d-2}\right\rceil.
  \]
  For \(B_2^N\), grouped Lorentz blocks attain these bounds and the matching
  full-product barrier value \(2\lceil N/(d-2)\rceil\); at
  \(d\geq N+1\), one \(Q_{N+1}\) block gives \((k,M,\nu)=(1,N+1,2)\).
  Grouped perspective cones give the same exact \((S,k,M)\) phase
  transition for every \(B_p^N\), \(1<p<\infty\); the nonsymmetric barrier
  optimum remains open for \(p\ne2\).  This is a global-factor theorem, not
  an unrestricted lift lower bound.
- [Sphere submersions onto balanced real Grassmannians](2026-09-04-sphere-submersions-balanced-real-grassmannians.md)
  classifies the projector-orbit analogue without assuming a spherical
  fiber.  Browder's arbitrary-fiber theorem and the mod-two Gysin sequence,
  followed by the oriented-Grassmannian Euler formula and the exceptional
  quadric calculation, rule out every proper \(C^1\) submersion
  \(S^n\to\operatorname{Gr}_{\lfloor r/2\rfloor}(\mathbb R^r)\) for
  \(r\geq4\), for all \(n\) and for all connected finite covers.  The only
  nondegenerate exception is \(r=3\): the sphere cover in dimension two and
  the complex Hopf map in dimension three.  The theorem and all small-r
  cases have passed an independent hostile audit.
- [Global smooth saturation has a topological obstruction](2026-09-04-global-smooth-saturation-topology.md)
  shows that the local Parseval equality becomes globally restrictive when
  one assumes fixed, globally \(C^2\) primal and dual factor selections on
  the full contact boundary of a strictly positively curved \(N\)-body.
  Saturation splits its tangent bundle into curvature subbundles.  If \(q\)
  factors are three-dimensional, Adams's vector-field theorem forces
  \(q\leq\rho(N)-1\).  In particular, an all-three-dimensional saturated
  factorization would parallelize \(S^{N-1}\), so for \(N\geq2\) it can be
  globally smooth only when \(N\in\{2,4,8\}\).  In every other dimension,
  minimum representations over arbitrary three-dimensional cones must have
  factor-selection
  singularities or chart changes.  A stronger Euler-class corollary applies
  whenever the ambient dimension \(N\geq3\) is odd: saturation permits only
  one positive-curvature summand, necessarily from a block of dimension
  \(N+1\).  Thus any cap \(d<N+1\) rules out a saturated globally smooth
  factorization in those dimensions, regardless of the individual positive
  block ranks.  The independently audited theorem
  applies to global factor selections, not lift existence; norm trees exist
  in all dimensions and evade it through nonsmooth partial norms.
- [Contact-regular lifts incur a strict topological granularity
  penalty](2026-09-04-contact-regular-lift-topology.md) upgrades the preceding
  selection theorem to a checkable lift-level condition.  It suffices that
  the primal and normalized-dual contact incidences contain proper
  nonsingular \(C^2\) sheets: simple connectivity turns those sheets into
  global factor selections.  The canonical sphere-submersion theorem then
  applies in every dimension: saturation forces one positive block of
  dimension \(N+1\).  Thus any cap \(3\leq d<N+1\) gives
  \[
    \sum_i(m_i-2)_+\geq N,
  \]
  and hence
  \[
    k_+\geq\left\lceil\frac{N}{d-2}\right\rceil,\qquad
    M_+\geq N+2\left\lceil\frac{N}{d-2}\right\rceil,\qquad
    \nu\geq2\left\lceil\frac{N}{d-2}\right\rceil .
  \]
  Grouped Lorentz lifts attain all three bounds, including a smaller final
  block.  The earlier Adams--Steenrod estimate
  \(m_*\geq N+2-\rho(N)\) remains an independently audited consequence of
  the weaker tangent-splitting data, but is superseded when the summands
  integrate to the global factors supplied by the contact sheets.  This is
  still a regular-lift result: the standard
  Lorentz norm tree evades it because its unique-boundary-fiber map has the
  nonsmooth local graph \(t=\sqrt{x_1^2+x_2^2}\) at a pole, despite strict
  cone factors, semialgebraicity, and singleton-fiber analytic centering.
- [The exact globally smooth Lorentz-block frontier for the Euclidean
  ball](2026-09-04-smooth-q3n-ball-factorization.md) is now sharp in every
  dimension and under every block-dimension cap. For \(N\geq3\), any exact
  \(Q_3^k\) ball-slack factorization
  with globally labelled \(C^1\) primal and dual contact selections obeys
  \[
                              k\geq N.
  \]
  The curvature bound gives \(k\geq N-1\). At equality, every
  three-dimensional contact pair normalizes to a rank-one \(C^1\) map into
  the boundary of a compact planar cone base.  That boundary is a
  topological circle even when it has corners.  The constant-rank theorem
  and one-dimensional invariance of domain make the normalized map locally
  open; lifting its circle-valued topological phase to the real line then
  contradicts compactness.  This integrability obstruction closes the
  \(N=4,8\) exceptions left by parallelizability and applies to arbitrary
  three-dimensional proper cones without boundary regularity. The bound is
  attained by the
  coordinatewise identity
  \[
   \left\langle
    \left({1+x_i^2\over2},{1-x_i^2\over2},x_i\right),
    \left({1+y_i^2\over2},-{1-y_i^2\over2},-y_i\right)
   \right\rangle={1\over2}(x_i-y_i)^2.
  \]
  Summation gives \(1-x^Ty\). The corresponding \(Q_3^N\) affine lift is
  strictly feasible, has full minimal face, unique polynomial boundary
  fibers, and compact embedded smooth primal and normalized-dual contact
  sheets. Its ambient dimension is \(3N\), and even a coupled ambient
  product barrier has optimal parameter \(2N\). The lift construction is
  the standard coordinatewise rotated-SOC square model; the new part is
  the independently audited sharp bi-contact-regular count.
  More generally, under \(3\leq d<N+1\), grouped coordinate blocks attain
  the simultaneous optima
  \[
   k_{\min}=\left\lceil\frac{N}{d-2}\right\rceil,\qquad
   M_{\min}=N+2k_{\min},\qquad \nu_{\min}=2k_{\min}.
  \]
  At \(d\geq N+1\), the direct Lorentz lift gives
  \((k_{\min},M_{\min},\nu_{\min})=(1,N+1,2)\). The parameter is for the
  full ambient Lorentz product, including arbitrary coupled barriers.
- [Joint smooth \(Q_3\) contact factorizations for products of
  balls](2026-09-04-joint-product-ball-q3-contact-factorizations.md) give a
  sharp new product-stratum law.  For
  \(C=(B_2^s)^k\), \(s\geq3\), and any fixed positive weight vector
  \(\lambda\), the regular contact manifold is
  \((S^{s-1})^k\), not the nonsmooth full boundary of \(C\).  Every globally
  labelled \(C^1\) factorization over arbitrary proper cones that attains
  the minimum total capacity \(k(s-1)\) has exactly \(k\) positive blocks,
  each of capacity \(s-1\) and cone dimension \(s+1\).  This fixes the
  capacity multiset, though the induced block maps may still mix ball
  coordinates.  Separate \(Q_{s+1}\) factors attain the profile.  For the
  finer all-small-cone question, every globally labelled bi-\(C^1\)
  \(Q_3^L\) factorization of the weighted slack obeys
  \[
                         L\geq k(s-1)+1.
  \]
  At curvature saturation the complementary circle phases lift to real
  functions whose joint map would immerse this compact
  \(k(s-1)\)-manifold in equal-dimensional Euclidean space, a contradiction.
  A new paired stereographic construction gives the globally smooth,
  nowhere-zero upper bound
  \[
                         L\leq ks-\lfloor k/2\rfloor.
  \]
  It is exact for two balls: \(L=2s-1\).  One global common-scale chordal
  construction provably needs \(ks-1\) channels by functional rank, so any
  further saving for \(k\geq3\) must share genuinely different radial
  scales.  The phase/topology obstruction itself cannot improve the lower
  bound because every product of spheres embeds in codimension one.  The
  triple-audited
  [near-saturation boundary note](2026-09-04-product-q3-near-saturation-boundaries.md)
  proves the paired count exact for positive block-group chordal
  decompositions even with overlapping groups and split weights, and proves
  \(L\geq n+m\) for partition-separated channels.  It also shows that every
  finite sampled submatrix and every local product chart already factors
  with \(n=k(s-1)\) channels, while a generic single channel can depend on
  all \(k\) blocks.  Thus any unrestricted improvement must use a genuinely
  global invariant of asymmetric amplitudes, not finite jets or assumed
  pair-locality.  The
  lower bound transfers to every full lift with such global contact
  selections and implies ambient \(\nu\geq2[k(s-1)+1]\); the smaller
  stereographic construction is currently only a fixed-contact
  factorization, not a claimed affine lift of the whole product body.  All
  identities, counts, and this scope distinction were independently
  audited.
- [The \(C^1\) top-class no-sharing
  theorem](2026-09-04-c1-euler-no-sharing-product-balls.md)
  resolves the corresponding full extreme-slack problem without analytic,
  support-density, or nonvanishing assumptions.  Contact positivity makes
  every Lorentz channel a PSD low-rank form, and a channel cannot be active
  for two source rows at the same point.  If too few channels are used, the
  compact exact-activity strata project into proper phase regions of each
  sphere, killing its ordinary top class on an open cover; their relative
  cup product contradicts the fundamental class of the sphere product.
  Consequently a globally labelled bi-\(C^1\) selected factorization of
  \(C=(B_2^s)^k\), \(s\geq3\), by \(Q_3\) factors needs exactly
  \(L=ks\).  More generally, if every Lorentz factor has dimension at most
  \(d<s+1\), the exact simultaneous optima, with
  \(h=\lceil s/(d-2)\rceil\), are

  \[
       (L,D_{\rm amb},\nu_{\rm ambient})
       =(kh,\ k(s+2h),\ 2kh),
  \]

  while \(d\geq s+1\) gives \((k,k(s+1),2k)\).  Grouped coordinate
  Lorentz lifts attain every bound.  The theorem also gives the exact
  heterogeneous product frontier by summing the per-ball count and
  capacity formulas.  Its lower-bound half extends to products of smooth
  strictly convex bodies with \(C^1\) polar contact diffeomorphisms and
  nondegenerate mixed contact forms; only the ball construction is claimed
  to attain those structural lower bounds.  The independently audited
  [exact regularity-premium theorem](2026-09-04-exact-product-ball-contact-regularity-premium.md)
  compares this frontier with arbitrary finite-dimensional exact affine
  Lorentz-product lifts; neither semialgebraicity nor Slater is an extra
  hypothesis.  If
  \(p=s-1\), \(c=d-2<p\), and
  \(\delta=\mathbf1_{\{c\mid p\}}\), arbitrary-arity norm trees attain
  \((T,L,D_{\rm amb},\nu_F)=(kp,k\lceil p/c\rceil,
  k[p+2\lceil p/c\rceil],2k\lceil p/c\rceil)\), while global
  \(C^1\) contact selections impose the exact premium
  \((\Delta T,\Delta L,\Delta D_{\rm amb},\Delta\nu_F)
  =(k,k\delta,k(1+2\delta),2k\delta)\).  The earlier
  [analytic continuation theorem](2026-09-04-analytic-no-sharing-full-product-balls.md)
  remains useful because it proves the stronger channelwise disjointness
  statement, while an explicit flat smooth switch shows that channelwise
  disjointness itself fails in the unrestricted \(C^1\) class.  The total
  count survives that switching.  In fact the unrestricted optima are
  attained with globally labelled Lipschitz primal and dual contact maps;
  their subtree-norm singularities are exactly what prevents global
  \(C^1\) regularity.  Here \(\nu_F=2L_{\rm full}+L_{\rm ray}\) is the
  operational barrier parameter after minimal-face reduction, not the
  ambient-cone value \(2L\) of an unreduced product whose slice may miss
  its interior.  The top-class proof, cap arithmetic, constructions, and
  minimal-face barrier scope were independently hostile-audited.
- [The everywhere-differentiable contact-gap
  theorem](2026-09-04-everywhere-differentiable-lorentz-contact-gap.md)
  locates a sharper regularity threshold.  Let \(p=s-1\ge2\),
  \(c=d-2<p\), and \(h_0=\lceil p/c\rceil\).  If all globally labelled
  primal and dual full-slack factors are everywhere Fréchet
  differentiable—their derivatives need not be continuous—then

  \[
   T_{\rm full}\ge kp+1,\qquad
   L_{\rm full}\ge kh_0+\mathbf1_{\{c\mid p\}},
  \]

  and consequently
  \(D_{\rm amb}\ge kp+1+2(kh_0+\mathbf1_{\{c\mid p\}})\) and
  \(\nu_F\ge2(kh_0+\mathbf1_{\{c\mid p\}})\).  Equality
  \(T_{\rm full}=kp\) would make the aggregate Lorentz phase map
  \((S^p)^k\to\prod_iS^{r_i}\) everywhere differentiable with invertible
  derivative.  Saint Raymond's nonsmooth inverse theorem makes it a
  finite covering; fundamental group and cohomology then force exactly
  \(k\) target factors of dimension \(p\), contradicting \(c<p\).
  For one ball these bounds are exact and coincide with the global
  \(C^1\) frontier:

  \[
   (T,L,D,\nu_F)=
   \left(p+1,\left\lceil\frac{p+1}{c}\right\rceil,
   p+1+2\left\lceil\frac{p+1}{c}\right\rceil,
   2\left\lceil\frac{p+1}{c}\right\rceil\right).
  \]

  Thus globally Lipschitz norm-tree selections attain the smaller
  unrestricted values, whereas everywhere differentiability already
  costs one capacity unit.  For \(k>1\), the theorem proves only the
  strict global \(+1\) gap; whether everywhere differentiability forces
  the full additive \(+k\) \(C^1\) gap remains open.  The theorem and its
  resource/minimal-face scope were independently hostile-audited.
- [The ray-exposed cone-dictionary product-ball
  theorem](2026-09-04-ray-exposed-cone-dictionary-product-balls.md)
  shows that this exact full-slack frontier is cone-independent: it holds
  for arbitrary proper blocks whose common-primal nonzero exposed
  complementary faces are rays.  Neither self-duality, smooth cone
  boundaries, nor positive-semidefinite individual mixed channels are
  needed.  Quotient rank and topological dual-phase spheres give the same
  count, dimension, and coupled ambient-barrier bounds, with Lorentz blocks
  needed only for attainment.  A single bundled product cone is a sharp
  counterexample without the ray-face condition.  The heterogeneous and cap
  boundary cases were independently hostile-audited.
- [Bounded complementary-face
  interpolation](2026-09-04-bounded-face-sharing-product-ball-factors.md)
  quantifies what replaces no-sharing for arbitrary cones.  If one block is
  active on several source rows with mixed ranks \(t_a\), then
  \(\sum_at_a\leq m-1\), while every active contact face contains the
  contact ray plus all rank-detecting directions for the other rows.  Thus
  an exposed face of dimension at most \(f\) lets one block serve at most
  \(f\) rows.  Combining this local packing law with the relative top-class
  argument gives global weighted face budgets \(F\geq kh(c)\),
  \(G\geq k\tau(c)\), and the independent rank ledger
  \(R+L\geq k(s-1)\).  The \(f=1\) case recovers the exact ray-exposed
  theorem; PSD faces become explicit nullspace-support packing inequalities.
  The result was independently hostile-audited.
- [Universal whole-row contact-codimension
  frontier](2026-09-04-universal-whole-row-contact-codimension.md)
  removes the ball and regularity assumptions.  For arbitrary
  full-dimensional convex bodies \(C_a\subset\mathbb R^{n_a}\), let
  \(\lambda_a\) be the codimension of their largest exposed contact face
  whose normal is an extreme polar point.  Any proper cone carrying a
  whole row group \(G\) has dimension at least \(1+\sum_Gn_a\) and a
  proper exposed face of dimension at least
  \(1+\sum_Gn_a-\min_G\lambda_a\), with no continuity assumption; the
  shared homogenization cone attains both.  This gives an exact two-cap
  partition law across arbitrary whole-row cones.  Strictly convex bodies
  have \(\lambda_a=n_a\), polytopes have \(\lambda_a=1\), and spectral
  balls have \(\lambda_a=r_a+c_a-1\).  Equality in the dimension bound is
  rigid: every minimum-dimensional cone and its factorization are linearly
  isomorphic to the shared homogenization.  Therefore the exact Euclidean
  and spectral ambient barrier ledgers extend to every
  minimum-dimensional whole-row formulation, not only the displayed
  cones.  At the absolute dimension minimum this rigidity also permits
  arbitrarily split rows: connected source extreme manifolds force one
  nonzero cone factor.  Under a strict factor-dimension cap
  \(d<1+\sum_an_a\), this gives the unconditional gap
  \(M\geq2+\sum_an_a\), without smooth selections.  The theorem was
  independently hostile-audited.
- [The connected-extremes additive-gap
  counterexample](2026-09-04-connected-extremes-additive-factor-gap-counterexample.md)
  proves that the preceding \(N+2\) gap is sharp for arbitrarily many
  factors. For every \(s,L\geq2\), the compact full-Slater codimension-two
  slice \(\sum_it_i=1,\ \sum_ix_i=0\) of \(Q_{s+1}^L\) has
  \(N=(s+1)L-2\), \(M=(s+1)L=N+2\), and a path-connected extreme set; every
  Lorentz factor is indecomposable, essential, and slack-visible.
  Therefore the deficit \((N+L)-M=L-2\) is unbounded. A complementary
  \(Q_N\times\mathbb R_+^2\) family has extreme set \(S^{N-2}\) in every
  \(N\geq3\). Thus connected extreme points do not imply the tempting
  additive law \(M\geq N+L\). That law does hold for the narrower class
  of linear images of one normalized product-cone base. Equivalently,
  among injective compact full-Slater slices with at least two factors,
  connected extremes force slice codimension at least two, and the
  \(Q_{s+1}^L\) family is sharp. More generally, at an extreme point of
  any rank-\(q\) affine product-cone slice, the sum of the active
  minimal-face span dimensions is at most \(q\); this recovers the
  real/complex product-PSD Pataki rank ledgers and limits the pointwise
  number of active factors to \(q\). Its restricted standard product-SOC
  barrier has exact parameter \(2L-1\): normalization removes one radial
  unit, but the additional equality that connects the extreme set removes
  no further unit. Even an arbitrary coupled barrier has parameter at least
  \(2L-1\), because the section \(x_i=0,\ y_i=u_ie\) is a
  \((2L-1)\)-simplex whose boundary lies in the body's boundary. Thus the
  standard product barrier is intrinsically optimal on the slice. The
  homogenizing balance cone has exact arbitrary coupled parameter \(2L\),
  certified by the corresponding \(\mathbb R_+^{2L}\) section. Exact
  partial minimization transfers the \(2L-1\) lower bound to every
  bounded-fiber affine lift, with arbitrary auxiliary cones and barrier
  coupling. More generally, an unbounded closed lift admits a
  barrier-preserving bounded normalization exactly when a
  recession-positive linear functional has uniformly bounded fiber
  minima. Finite vertex lifts verify this automatically for every compact
  polytope. Consequently every SCB on every closed full-Slater conic lift
  of an \(n\)-polytope with a simple vertex has \(\nu\geq n\), even with
  unbounded fibers and arbitrary coupling. This does not currently extend
  to every nonsimple polytope: the classical local lower bound requires
  exact facet incidence, and selecting \(n\) normals from a nonsimple
  vertex does not remove the other locally blocking facets. For curved
  bodies the
  unbounded-fiber extension remains open, and cannot be
  obtained by an automatic affine normalization: an audited semialgebraic
  epigraph lift over the same compact body has only one pointed recession
  ray, yet every affine restriction that preserves the whole projection
  retains that ray. Even the trivial product lift makes the barrier
  infimum along a fiber ray equal to \(-\infty\). For
  \(N=dL-2\), the same \(Q_d^L\) body is an exact arbitrary-dictionary
  hard instance under factor-dimension cap \(d\):
  \(L_{\min}=L\) and \(M_{\min}=N+2=dL\), even with split rows and
  discontinuous factor maps. All claims were independently hostile-audited.
- [Sharp bounded-face sharing
  models](2026-09-04-bounded-face-sharing-sharp-models.md) show both an
  integrability gap and genuine linear-in-face sharing.  A block carrying
  \(q\) whole ball rows must have dimension at least \(qs+1\) and a
  complementary face of dimension at least \(1+(q-1)s\); the homogenization
  cone \(\mathcal H_{q,s}\) attains both.  The shared-perspective cone
  \(\mathcal P_q\) has dimension \(2q+1\), maximum complementary-face
  dimension \(2q-1\), and carries \(q\) scalar square channels, proving
  that inverse-linear face sharing is possible for split rows.  Both cones
  have exact intrinsic LHSCB parameter \(q+1\), with explicit corrected
  determinant barriers.  For heterogeneous row dimensions
  \(s_1,\ldots,s_q\), the same \(\mathcal H\)-block has dimension
  \(1+\sum_as_a\), exact maximum complementary-face dimension
  \(1+\sum_as_a-\min_as_a\), and the same optimal parameter \(q+1\).
  The exact heterogeneous row-indivisible grouping problem is a two-cap
  bin-packing problem and is strongly NP-hard by 3-PARTITION; within the
  dimension-sharp \(\mathcal H\)-family, the same grouping simultaneously
  minimizes factor count, ambient dimension, and exact coupled ambient
  barrier parameter.
  Most sharply, one \(\mathcal H_{k,s}\) block
  collapses \(k\) cone factors to one, but its fixed-scale restriction is
  exactly the ordinary product-ball barrier: parameter \(k\), central
  path, Hessian, Dikin geometry, and reduced Newton oracles are all
  grouping-independent, and the audited bounded-move lower bound remains
  \(\Omega(\sqrt{k}\log(k/\epsilon))\).  For a product of \(g\)
  \(\mathcal H\)-blocks with group sizes summing to \(k\), an explicit
  parameter-sharp recession certificate and its direct-sum tensorization
  now prove the exact coupled ambient value \(\nu_{\rm opt}=k+g\).
  The structural and barrier arguments were independently hostile-audited.
- [Chordal PSD-completion ball
  packing](2026-09-04-chordal-completion-ball-packing.md) gives a sparse
  matrix analogue with an exact all-barrier law.  Every \(n\)-vertex
  PSD-completion cone has optimal barrier parameter \(n\), and products are
  exactly additive even against coupled barriers, by a conjugate sparse
  log-determinant upper bound and a diagonal-orthant lower section.  A
  chordal star with an \(s\)-clique hub and \(q\) leaves carries all \(q\)
  product-ball slack rows in one cone, removes \(q(q-1)/2\) variables
  relative to a dense order-\((s+q)\) PSD factor, and has exact ambient
  parameter \(s+q\).  Its clique--separator barrier gives the exact overlap
  credit \(q(s+1)-(q-1)s=q+s\), rather than charging the repeated hub once
  per clique.  For \(g\) groups the exact ledgers are
  \(D=k(s+1)+g s(s+1)/2\) and \(\nu=k+gs\), while fixing the hubs and leaf
  diagonals gives exactly the ordinary parameter-\(k\) product-ball
  barrier and grouping-independent reduced Newton geometry.  The
  max-determinant barrier is classical; the full-slack/resource synthesis
  is the screened candidate contribution.  The result was independently
  hostile-audited.
- [Shared-scale spectral-norm product
  packing](2026-09-04-spectral-norm-product-sharing.md) extends the same
  phenomenon from vector balls to rectangular spectral-norm balls.  If
  \(\rho_a=\min\{r_a,c_a\}\), grouping the blocks into \(g\) shared-scale
  spectral cones has exact ambient parameter
  \(g+\sum_a\rho_a\), even for an arbitrary coupled barrier, while fixing
  the scales gives exact slice parameter \(\sum_a\rho_a\).  The displayed
  determinant barrier has squared local gradient norm
  \(\sum_i2\sigma_i^2/(1+\sigma_i^2)<\rho_a\), and diagonal cube and
  recession certificates make both values sharp.  Rank-one nuclear-polar
  rows give exact full-slack factors.  The independently audited
  [face-capped whole-row theorem](2026-09-04-spectral-norm-face-capped-grouping-frontier.md)
  is cone-independent: any proper cone carrying a row group \(G\) has
  dimension at least \(1+\sum_G r_ac_a\) and a proper exposed face of
  dimension at least
  \(1+\sum_G r_ac_a-\min_G(r_a+c_a-1)\); the shared spectral cone attains
  both.  This gives the exact two-cap grouping law and makes heterogeneous
  optimal grouping strongly NP-hard.  The complementary independently
  audited [split-row contact-curvature
  theorem](2026-09-04-spectral-ball-contact-curvature-packing.md) removes
  row indivisibility under globally \(C^1\) factors: an
  \(r\times c\) spectral-ball contact has exact mixed rank \(c-1\) over
  \(\mathbb R\), \(2c-1\) over \(\mathbb C\), and \(4c-1\) over
  \(\mathbb H\).  Tangent-ray quotients and unrelated-row cylinders turn
  these ranks into dimension-, face-, and incidence-weighted lower
  ledgers for arbitrary proper cone blocks; no exact attainment or
  barrier lower bound is inferred from this local theorem.
  A block-star PSD-completion
  alternative has exact ambient parameter \(s+\sum_ap_a\), the same exact
  slice parameter \(\sum_a\min\{s,p_a\}\), and sparse clique-tree
  structure.  After fixing scales and identity blocks, the two barriers,
  central paths, reduced KKT matrices, condition numbers, normalized Newton
  states, and exact classical/coherent derivative oracles coincide up to a
  public permutation; this equivalence excludes the different ambient KKT
  systems and their compilation costs.  The primitive barriers are
  classical; the independently hostile-audited candidate contribution is
  the exact shared-product synthesis and resource comparison.  For a
  rank-saturating objective with \(R=\sum_a\rho_a\), every
  bounded-Dikin-move method from the analytic center needs
  \(\Omega(\sqrt R\log(R/\epsilon))\) moves on all these fixed slices,
  matching the standard short-step dependence; this is not an unrestricted
  query or runtime lower bound.  The independently audited
  [singular-weight spectral-ball Dikin
  theorem](2026-09-04-spectral-ball-dikin-iteration-lower-bound.md)
  handles arbitrary full-row-rank objective blocks \(C_a\).  If
  \(w_{a,i}>0\) are all their singular values, it gives
  \[
    d_F(0,X)\geq\sqrt R
      \left[\log{\Delta_{\rm spec}\over2\epsilon}\right]_+,\qquad
    \Delta_{\rm spec}=R\left(\prod_{a,i}w_{a,i}\right)^{1/R}.
  \]
  This holds for arbitrary nonaligned endpoints over both
  \(\mathbb R\) and \(\mathbb C\); block weights recover the previous
  \(\Delta_{\rm eff}\) as a specialization.
  Its explicit normalized central path matches
  \(\Theta_\delta(\sqrt R\log(1/\epsilon))\) bounded chords.
  The complementary audited
  [objective-rank-adaptive spectral path
  theorem](2026-09-04-spectral-ball-low-rank-objective-path.md) closes the
  opposite regime. For a support matrix \(C\), the exact center is the
  singular-value transform
  \[
    X(\eta)=\eta(I+\sqrt{I+\eta^2CC^*})^{-1}C,
  \]
  and its squared primal speed is
  \(\operatorname{tr}[I-(I+\eta^2CC^*)^{-1/2}]\). Thus a rank-\(r\)
  objective reaches primal error \(\epsilon\) in
  \(O_R(\sqrt r[1+\log(r/\epsilon)])\) Dikin chords, with matching order
  for a rank-\(r\) partial isometry, even when \(r\ll\rho\).
  This match is path-independent: convexity of the negative log determinant
  of the complementary LMI Schur complement proves that the active
  rank-\(r\) minor has Hessian dominated by the full matrix-ball barrier,
  giving
  \[
    d_F(0,X)\geq\sqrt r
      \left[\log{r(\prod_iw_i)^{1/r}\over2\epsilon}\right]_+.
  \]
  Compressing to every top-\(m\) singular subspace strengthens this to the
  maximum of the same expression over \(m\), with the geometric mean of
  the top \(m\) weights.  Together with the exact speed law, this proves
  tight arbitrary-path distribution laws: geometric decay
  \(w_i=e^{-a(i-1)}\) costs
  \(\Theta_a(\log^{3/2}(1/\epsilon))\), while polynomial decay
  \(w_i=i^{-\beta}\), \(\beta>1\), costs the genuinely log-free
  \(\Theta_\beta(\epsilon^{-1/[2(\beta-1)]})\), assuming the finite
  truncation contains the active indices.  These profile lower bounds and
  decay comparisons were independently hostile-audited.  Nuclear-tail
  and Frobenius-tail versions replace exact rank by an accuracy-dependent
  numerical rank; pooling singular values gives the product-block theorem.
  On the conic homogenization the dual squared speed is exactly
  \(\rho+1-r_{\rm eff}(\eta)\), so full product-metric movement remains.
  A stronger, separately audited conclusion identifies the exact global
  center-to-point distance.  With
  \[
   \varrho(x)=\int_0^x{\sqrt{2(1+t^2)}\over1-t^2}\,dt,
  \]
  one has
  \[
    d_\phi(0,X)^2=\sum_i\varrho(\sigma_i(X))^2
  \]
  over both \(\mathbb R\) and \(\mathbb C\), including repeated and zero
  singular values.  Therefore the shortest distance to objective error
  \(\epsilon\) is exactly the strictly convex water-filling problem
  \[
   L_{\rm opt}(\epsilon)=
   \min\left\{\left(\sum_i\varrho(x_i)^2\right)^{1/2}:
        \sum_iw_i(1-x_i)\leq\epsilon,\ 0\leq x_i<1\right\},
  \]
  whose unique endpoint satisfies
  \(2\varrho(x_i)\varrho'(x_i)=\lambda w_i\).
  For feasible forward-Dikin radius \(R<1\), the optimal number of
  arbitrary noncentral chords is consequently sandwiched between
  \(L_{\rm opt}/[-\log(1-R)]\) and
  \(\lceil L_{\rm opt}/\log(1+R)\rceil\).
  The audited [constructive shortcut
  note](2026-09-04-spectral-rho-geodesic-shortcut-algorithm.md) implements
  this endpoint and path by one scalar multiplier search under explicitly
  charged compact-SVD access; it does not make singular frames, amplitude
  tables, readout, or generic affine constraints free.
  Centrality itself has an exact worst-case distortion scale:
  \[
   L_{\rm CP}(0,\eta_f)\leq\Gamma_r d_\phi(0,X(\eta_f)),\qquad
   \Gamma_r^2=\sum_{i=1}^r(\sqrt i-\sqrt{i-1})^2
             ={1\over4}\log r+O(1),
  \]
  and an explicit singular-weight family attains
  \(\Theta(\sqrt{\log r})\).  A complementary water-filled family has
  \(L_{\rm opt}=\Theta(\sqrt{\log r})\) while every determinant
  rank-profile positive part vanishes, so the profile is a certificate,
  not a constant-factor characterization.  The Hermitian-dilation
  spectral Hessian formula is classical.  The standalone
  [sharp subgeodesicity note](2026-09-04-spectral-ball-sharp-subgeodesicity.md)
  proves the stronger same-accuracy statement: if \(\eta_\epsilon\) is
  the first accurate central parameter, then
  \[
   L_{\rm CP}(\epsilon)\leq c_\star\Gamma_rL_{\rm opt}(\epsilon)
      <{69\over50}\Gamma_rL_{\rm opt}(\epsilon),
   \qquad
   \sup_{w,\epsilon}{L_{\rm CP}(\epsilon)\over L_{\rm opt}(\epsilon)}
      =\Theta(\sqrt{\log r}).
  \]
  Here
  \(c_\star=\max_{y>0}p^{-1}(yp'(y))/y\) is the exact scalar dilation for
  \(p(y)=b'(\rho^{-1}(y))\).  The independently audited
  [scalar-dilation theorem](2026-09-04-exact-scalar-centrality-dilation.md)
  proves that the maximum is attained and \(c_\star<69/50=1.38\) by an
  analytic certificate.  Numerics suggest
  \(c_\star\approx1.37486420044\), but uniqueness of the observed
  stationary point is not claimed.  The earlier one-regime argument gives
  the weaker certified value \(\kappa_0=1.391010896\ldots\).
  On the sharp multiscale family, any sequence starting at the analytic
  center, remaining within fixed geodesic
  radius \(\delta\) of arbitrarily labeled exact centers and using forward
  \(R\)-Dikin chords needs \(\Omega_{R,\delta}(r\log r)\) rounds before
  returning an actually \(\epsilon\)-accurate iterate; no endpoint-label
  or monotonicity assumption is needed.  Optimal unrestricted movement to
  the accuracy set needs only \(\Theta_R(r\sqrt{\log r})\), proving a sharp discrete
  \(\Theta_R(\sqrt{\log r})\) centrality tax.
  The lower family uses a diagonal objective with only \(r\) nonzeros and
  one conic-slice equality, so the tax is not caused by dense input data;
  this does not make spectral-cone oracle access free.  Standard self-concordance
  turns the conventional fixed Newton-decrement condition
  \(\lambda_\eta(Z)\leq\beta<1/2\) into the same tube with
  \(\delta=\log((1-\beta)/(1-2\beta))\), so the discrete separation is
  directly a bounded-move short-step neighborhood theorem.  The same
  proof quantifies growing tubes: with
  \(C_r=2\delta_r-\log(1-R)\) and \(\delta_r=o(r^{2/3})\), it gives
  \(N=\Omega_R(r\log r/[C_r\sqrt{1+C_r}])\); the overhead over optimal
  movement still diverges for \(\delta_r=o((\log r)^{1/3})\).  The
  same lower count applies to full feasible primal--dual product-Dikin
  chords on the conic homogenization with \(t=1\) and final duality gap
  \(\epsilon\).  The conventional scaled centrality residual
  \(\|q+\mu\nabla F(z)\|_{z,*}\le\beta\mu\) contracts on the \(t=1\)
  slice to the required primal decrement
  \(\lambda_{1/\mu}(X)\le\beta\).  It does not cover infeasible-start methods.
  The
  candidate new result is this exact distance, water-filling, optimal-move,
  and sharp continuous/discrete centrality synthesis.
  The independently audited
  [sharp separable centrality theorem](2026-09-04-sharp-separable-centrality-tax.md)
  isolates the scalar mechanism.  For every fixed one-dimensional
  self-concordant barrier with normalized gradient parameter at most one,
  the metric central velocity \(v=f'/\sqrt{f''}\) satisfies
  \(v'\geq v(1-v)\), rises from zero to one, and differs integrably from a
  translated unit step.  Consequently the exact worst translated-product
  same-endpoint constant is \(\Gamma_r\) for **every** such scalar barrier,
  not only for \(-\log(1-x^2)\).  A new same-accuracy theorem also controls
  the distance to the entire objective sublevel: if \(L_{\rm opt}(\epsilon)\)
  is the closest accurate Hessian-metric endpoint, the first-accurate central
  arc satisfies the audited sharper bound
  \[
    L_{\rm CP}(\epsilon)
       \le C_{\rm sc}\Gamma_rL_{\rm opt}(\epsilon),
       \qquad C_{\rm sc}<2.
  \]
  Here \(C_{\rm sc}\approx1.831856423\) is the attained maximum of the
  explicit two-branch scalar envelope in the companion note.  The proof
  starts from the universal scalar sandwich
  \(p(y)/(yp'(y))\le1/\log2\) and
  \(p(2y)\ge yp'(y)/\log2\), then uses
  \(1-\upsilon\le\upsilon'\le1+\upsilon\) for
  \(\upsilon=p/p'\).  This constant is exact for that relaxed
  differential-envelope proof with the profile-independent safe scale
  \(\log2\); it is not claimed to be the globally sharp fixed-barrier
  minimax constant.  The same universal profile yields a
  sparse-box discrete theorem: for every fixed normalized scalar barrier,
  actual endpoint accuracy and an arbitrary-label fixed central
  neighborhood require \(\Omega_f(r\log r)\) forward bounded-Dikin rounds,
  while an explicit noncentral geodesic schedule uses
  \(O_f(r\sqrt{\log r})\).  Together these prove the exact worst-case order
  \(\Theta(\sqrt{\log r})\) for every fixed barrier in the normalized scalar
  class.  This is geometric and makes no finite-bit or
  quantum-query claim.  A stretched-threshold rounding makes every
  objective weight and the target tolerance dyadic with \(O(r)\) bits
  while preserving both orders, but does not make an arbitrary fixed
  barrier oracle efficiently evaluable.  The independently audited
  [canonical-box-barrier calculation](2026-09-04-canonical-box-barriers-do-not-remove-centrality-tax.md)
  shows that neither standard optimal universal construction escapes:
  the cube's universal polar-volume barrier is exactly
  \(\mathrm{const}-\sum_i\log(1-x_i^2)\), while its entropic barrier
  tensorizes because the uniform log-partition function does.  Both have
  exact parameter \(r\) and inherit the sharp \(\Gamma_r\) and discrete
  taxes.  Genuine coupling, full symmetry, and even the exact optimal
  parameter are not sufficient either.  The independently audited
  [exact-optimal hyperoctahedral example](2026-09-04-exact-optimal-hyperoctahedral-box-barrier-tax.md)
  adds the larger-ball term \(-\log(r+4-\|x\|^2)\).  Its Hessian is
  genuinely dense, it is invariant under every signed permutation, its
  exact parameter remains \(r\), and its worst positive-objective
  same-endpoint tax is still at least the full \(\Gamma_r\).  The whole
  family
  \[
       U(x)-\lambda\log(c-\|x\|^2),
       \qquad \lambda\geq1,\quad c-r\geq4\lambda,
  \]
  has the same exact parameter and tax.  Thus the generic sum-rule
  certificate \(r+\lambda\) can overcount the actual parameter by an
  arbitrarily large additive amount.  More
  generally, the independently audited
  [facet-regular stability theorem](2026-09-04-facet-regular-coupling-box-centrality-tax.md)
  proves the same lower bound for every decomposition \(F=U+G\) with
  convex coupling whose gradient and Hessian stay bounded on one full
  signed facet collar.  Thus any escape within this class must have
  singular coupling on every such collar.  This does not settle every
  custom optimal barrier; regularity only near a final almost-vertex face
  misses the earlier flag stages which create the logarithmic tax.
  The closure-audited
  [dyadic discrete companion](2026-09-04-exact-optimal-hyperoctahedral-box-discrete-tax.md)
  strengthens the explicit \(c=r+4\) barrier to an actual-accuracy
  neighborhood theorem.  For fixed forward Dikin radius and fixed metric
  tube—or fixed Newton decrement below \(1/2\)—analytic-center start,
  arbitrary and possibly backward central labels, and a dyadic
  \(\epsilon\)-accurate finish require
  \(\Omega(r\log r)\) coupled-metric chords.  A direct
  product-\(\rho\) comparison path, with the added radial metric integrated
  explicitly, uses \(O_{R,\Delta}(r\sqrt{\log r})\) coupled-metric chords.  Every
  listed weight and tolerance has \(O(r)\) bits.  The proof passed a
  complete closure check and a subsequent independent hostile audit; this
  is still a fixed-barrier bounded-primal-movement theorem, not a runtime
  or query lower bound.
  Without the unit gradient normalization,
  smooth scalar self-concordant barriers can have nonmonotone velocity and
  attain the larger worst order \(\Theta(\sqrt r)\); their growing barrier
  parameter is essential.
  This suggests singular-activity-adaptive checkpoints, but generic affine
  constraints destroy the SVD reduction, and singular-space access,
  conditioning, success amplitude, and output costs prevent an automatic
  QIPM runtime claim.  Under coherent indexed access to
  \(w_i\le w_{\max}\), testing the exact water-filling residual reduces to
  relative mean estimation: the capped query upper bounds are
  \(O(\min\{r,\sqrt{rw_{\max}/\epsilon}\})\) quantumly and
  \(O(\min\{r,rw_{\max}/\epsilon\})\) by randomized sampling, before
  root-conditioning and arithmetic factors.  These are ordinary
  approximate-counting laws for an artificial closest-endpoint contract,
  not a new QIPM separation.  A custom coherent \(\ell_1\)-sampler exposes
  the nuclear norm and hence the unconstrained optimum; ordinary SQ access
  instead supplies the Frobenius norm.  Full checkpoint output still costs
  \(\Omega(r)\).
  There is nevertheless an exact same-instance raw-oracle conjunction.
  Put independent hidden signs on the public multiscale diagonal weights.
  Every normalized exact-central or radial-geodesic checkpoint state is
  prepared from its public amplitude table by one sign-oracle query, while
  a constant-coordinate-accuracy classical terminal matrix reveals all
  signs and costs \(\Theta(r)\) quantum or randomized queries.  The signs
  leave the \(\Theta_R(r\log r)\) central and
  \(\Theta_R(r\sqrt{\log r})\) unrestricted movement counts unchanged.
  The optimum value is public, amplitude-table construction is charged,
  and these query/readout/movement conclusions are simultaneous, not
  multiplied.
  Restricting the same diagonal construction gives the standalone
  [one-sparse box-LP theorem](2026-09-04-sparse-box-lp-geodesic-centrality-tax.md).
  It has only the \(2r\) one-sparse inequalities \(-1\le x_i\le1\), while
  the restricted standard barrier \(-\sum_i\log(1-x_i^2)\) has exact
  parameter \(r\), not the nominal slack count \(2r\).  Cumulatively rounded
  dyadic weights preserve the same
  \(\Theta_R(r\log r)\) exact/near-central and
  \(\Theta_R(r\sqrt{\log r})\) unrestricted same-endpoint chord counts at
  \(\log(1/\epsilon)=\Theta(r)\).  Conventional rational input length is
  \(L=\Theta(r^2)\), so these become
  \(\Theta_R(\sqrt L\log L)\) and
  \(\Theta_R(\sqrt{L\log L})\).  Its Newton matrices are diagonal and the
  noncentral path is a direct separable solve, so this is a centrality-cost
  counterexample, not an unrestricted LP/QIPM runtime lower bound.  The
  near-central lower needs no assumed label progress: analytic-center start,
  actual \(\epsilon\)-accurate output, and a fixed metric or
  Newton-decrement tube force the labels across the hard clipped range.
  This growing tax is intrinsically primal.  Between finite feasible
  primal--dual central endpoints for an LH cone barrier, Nesterov--Todd's
  classical \(\sqrt2\)-geodesicity theorem and chord comparison make
  arclength-partitioned central tracking constant-factor optimal in the
  combined metric.  Thus the primal radial shortcut cannot yield a
  dimension-growing primal--dual separation when the full dual trajectory
  is charged.
  The independently audited
  [sparse dual-completion theorem](2026-09-04-sparse-box-primal-dual-completion-tax.md)
  makes the missing cost exact on the same dyadic instance.  In the
  standard orthant formulation \(u_i=1+x_i,v_i=1-x_i\), every equality row
  has two nonzeros, every slack column has one, and the ambient barrier has
  \(\nu=2r\).  Starting at the finite center \(\eta=1\), the optimal
  forward-\(R\)-Dikin movement to **any** strictly feasible primal--dual
  output of gap at most \(2\epsilon_r\) is
  \(\Theta_R(r^{3/2})\), while the restricted-primal central and
  unrestricted counts are respectively
  \(\Theta_R(r\log r)\) and
  \(\Theta_R(r\sqrt{\log r})\).  The lower bound to the whole gap set has
  an elementary dual-slack proof: initial slacks
  \(\alpha_i^0\ge1/\sqrt2\), terminal gap forces
  \(\alpha_i\le\epsilon_r\), and dual orthant log coordinates give distance
  \(\Omega(\sqrt r\log(1/\epsilon_r))\).  Exact primal--dual central speed
  \(\sqrt{2r}\) supplies the matching upper.  Thus gap certification creates
  a \(\Theta(\sqrt{r/\log r})\) completion premium over the primal
  geodesic.  At ordinary input length \(L=\Theta(r^2)\), the three scales
  are \(\Theta(L^{3/4})\),
  \(\Theta(\sqrt L\log L)\), and
  \(\Theta(\sqrt{L\log L})\).  This is a metric/output-contract separation,
  not a claim that primal IPMs have lower total runtime, and it is not
  multiplied by the simultaneous sign-query/readout facts.
  The independently hostile-audited [Jordan spectral-interval
  theorem](2026-09-04-jordan-spectral-interval-distance-centrality-tax.md)
  shows that none of this exact metric geometry is special to rectangular
  matrix balls.  For every Euclidean Jordan algebra, including Lorentz,
  real/complex/quaternionic PSD, and Albert factors, the barrier
  \(\Phi_\alpha(x)=-\alpha\log\det(e-x^2)\) on
  \(-e\prec x\prec e\) satisfies
  \[
   d_{\Phi_\alpha}(0,x)^2
      =\alpha\sum_i\varrho(|\lambda_i(x)|)^2.
  \]
  Consequently the exact \(\epsilon\)-sublevel distance is the same
  scalar water-filling problem over the active Jordan eigenvalues, the
  optimal bounded-Dikin chord count has the same logarithmic sandwich,
  and a common-scale product has sharp same-accuracy centrality tax
  \(\Theta(\Gamma_r)=\Theta(\sqrt{\log r})\), where \(r\) is pooled
  active spectral rank rather than cone dimension.  The same multiscale
  eigenvalue family gives the discrete separation
  \(\Omega_{R,\delta}(r\log r)\) versus
  \(\Theta_R(r\sqrt{\log r})\) for fixed-radius
  central-neighborhood following from the analytic center to an actually
  accurate output, even when the labeled central parameters may move
  backward.  Fixed Newton decrement \(\beta<1/2\) implies such a geodesic
  tube, so this is a standard-barrier short-step iteration lower bound,
  though not a query or runtime lower bound.
  Exact distance and water filling also extend to unequal classified
  self-scaled weights.  Ordering channels by activation threshold and
  writing \(S_i=\sum_{k\leq i}\alpha_k\) gives the explicit sharp-order
  interpolation
  \[
   L_{\rm cent}\leq\Gamma_{\boldsymbol\alpha,a}d_\Phi,\qquad
   \Gamma_{\boldsymbol\alpha,a}^2
    =\sum_i{\alpha_i\over(\sqrt{S_i}+\sqrt{S_{i-1}})^2}
    \leq1+{1\over4}\log{S_r\over\alpha_{\min}}.
  \]
  This coefficient is the exact supremum for every fixed ordered scale
  profile; for a fixed multiset of scales, increasing activation order is
  worst and decreasing order is best.  It recovers \(\Gamma_r\) for equal
  scales.  The worst order
  \(\Theta(\sqrt r)\) is attainable, including for the same-accuracy
  ratio and fixed-radius central-neighborhood rounds even with label
  backtracking, but requires exponential scale dynamic range; for polynomial
  active weight-rank mass the tax remains logarithmic.  A targeted
  literature screen found the invariant cone geometry and EJA spectral
  calculus as classical antecedents, but not this bounded-interval exact
  distance/water-filling/centrality synthesis; priority is not claimed.
  The independently audited
  [principal-minor contraction
  theorem](2026-09-04-spectrahedral-principal-minor-dikin-contraction.md)
  abstracts the path-independent step: for every real symmetric or complex
  Hermitian affine pencil \(L(x)\succ0\), the Hessian of
  \(-\log\det(Q^*LQ)\) is dominated by that of \(-\log\det L\).  If a
  rank-\(r\) exposed PSD slack \(W=QDQ^*\) satisfies
  \(\operatorname{tr}(WL(x))\leq\epsilon\), this gives
  \[
   d_F(x_0,x)\geq\sqrt r
    \left[\log{r\{\det D\det(Q^*L(x_0)Q)\}^{1/r}\over\epsilon}\right]_+.
  \]
  More strongly, letting \(\lambda_i\) be the decreasing eigenvalues of
  \(D^{1/2}Q^*L(x_0)QD^{1/2}\), one may maximize
  \(\sqrt m[\log(m(\prod_{i\leq m}\lambda_i)^{1/m}/\epsilon)]_+\)
  over \(m\leq r\).  This basis-free exposed-rank profile survives all
  inactive affine and completion coordinates; it is a standard-logdet
  bounded-move theorem, not an arbitrary-barrier or query lower bound.
  For normalized start \(L(x_0)=I\), optimizing this envelope gives the
  exact leading lower asymptotics
  \[
   \left\{{2\over3}\sqrt{2\over3a}+o_a(1)\right\}
     \log^{3/2}(1/\epsilon)
  \]
  for \(d_i=e^{-a(i-1)}\), once \(r\) contains the scale
  \(2\log(1/\epsilon)/(3a)+O_a(\log\log(1/\epsilon))\), and
  \[
   \left\{2(\beta-1)e^{(2-\beta)/(2(\beta-1))}+o_\beta(1)\right\}
   \epsilon^{-1/[2(\beta-1)]}
  \]
  for \(d_i=i^{-\beta}\), once
  \(r\) contains the scale
  \(e^{(2-\beta)/(\beta-1)}\epsilon^{-1/(\beta-1)}\).
  A diagonal paired-slack box spectrahedron has explicit feasible
  noncentral paths matching both orders.  This proves attainability by
  examples, not a universal or central-path upper bound.
  A new [low-rank matrix-ball readout
  construction](2026-09-04-spectral-ball-low-rank-readout-separation.md)
  supplies the missing exact oracle example.  One column-sparse rank-\(r\)
  objective with equal, disjoint row norms has a central point, predictor,
  and optimizer all proportional to the objective, so their normalized
  Frobenius states have expected \(O(1)\) raw coefficient-query
  preparation.  Nevertheless, additive \(\epsilon\) estimation of the
  optimum or a fixed finite central objective costs
  \(\Theta(\min\{N,Ar/\epsilon\})\) quantum queries and
  \(\Theta(\min\{N,(Ar/\epsilon)^2\})\) randomized queries.  On a
  balanced-row promise, a sufficiently accurate explicit classical
  optimizer recovers all \(rN\) hidden bits and costs \(\Theta(rN)\)
  queries, even though all scalar singular data are then public.  The same
  instance has exact central movement
  \(\Theta(\sqrt r[1+\log(Ar/\epsilon)])\), independent of the ambient
  parameter \(P\gg r\); the active-principal-minor theorem makes this a
  matching lower bound for every path made of bounded moves in the fixed
  standard primal barrier metric.  Exact norm or normalized-SQ metadata invalidates
  the scalar lower bound; classical rejection sampling is also constant
  query; and the state, scalar/full readout, and movement bounds are
  simultaneous max-type statements, never a product.  A diagonal
  one-sparse companion of rank \(R=2k+1\) makes both Frobenius and
  operator norms public while retaining constant-expected-query central,
  predictor, and optimizer states, sharp \(k\)-bit scalar/full-output
  laws, and matching \(\Theta(\sqrt R\log(AR/\epsilon))\) standard-metric
  movement; its price is that rank now grows with the hidden information.
- [The standard-slice product-ball barrier
  theorem](2026-09-04-product-ball-standard-slice-barrier-frontier.md)
  turns the same top-class obstruction into a barrier result that is
  insensitive to redundant extra factors.  For a heterogeneous product
  \(\prod_aB_2^{s_a}\) and Lorentz capacity cap \(c=d-2\), define
  \(h_a=1\) when \(c\geq s_a-1\), and
  \(h_a=\lceil s_a/c\rceil\) otherwise.  Every globally \(C^1\) selected
  lift has a common all-active boundary fiber with at least
  \(\sum_ah_a\) primal determinant zeros.  Hence its standard product
  log-determinant, after restriction to the affine slice, has exact minimum
  parameter
  \[
                          \nu_{\rm std,slice}=\sum_ah_a.
  \]
  Separate direct/grouped Lorentz lifts attain it.  This is stronger than
  an ambient factor-count ledger: using more factors cannot lower the
  restricted standard parameter.  It remains a theorem about the standard
  barrier, not arbitrary custom barriers on competing lifted domains.
  The nullity charge, heterogeneous deficit cover, and upper construction
  were independently hostile-audited.
- [Coupling cannot lower the barrier parameter of the grouped ball
  slice](2026-09-04-coupled-barrier-grouped-ball-slice.md) closes the
  custom-barrier loophole for the frontier-attaining grouped formulation.
  If \(L\) is the total number of nonempty coordinate groups, fixing every
  positive allocation variable and one coordinate direction per group cuts
  out an affine \(L\)-cube.  The cube lower bound therefore applies to
  every possibly coupled, non-logarithmically-homogeneous
  self-concordant barrier on the reduced affine slice:
  \[
                         \vartheta_{\rm opt}=L.
  \]
  The separable paraboloid barrier attains the bound and retains the forest
  Newton graph.  Thus the capped product-ball construction has intrinsic
  reduced parameter \(kh\), whereas the projected product body itself has
  parameter \(k\): granularity creates an exact \(k(h-1)\) slice-barrier
  tax that coupling cannot remove on this formulation.  A diagonal-block
  duplication example gives the sharp scope boundary: productive
  boundary-ray count alone does not lower-bound arbitrary slice barriers,
  because repeated factor conormals can coincide.  The result therefore
  does not yet prove \(kh\) for every non-grouped small-cap lift.
- [Exact contact-smooth granularity of \(\ell_p\) balls](2026-09-04-smooth-lp-perspective-cone-optimality.md)
  extends the same phase transition to every \(1<p<\infty\).  Separate
  \(C^1\) primal and polar boundary charts retain a nondegenerate mixed
  slack pairing even where Gauss-map curvature degenerates.  Thus, among
  product-cone lifts with globally labelled \(C^1\) primal and normalized
  dual contact selections, for \(3\leq d<N+1\),
  \[
   S_{\min}=N,\qquad
   k_{\min}=\left\lceil\frac{N}{d-2}\right\rceil,\qquad
   M_{\min}=N+2k_{\min}.
  \]
  A matching lift partitions the coordinates into groups \(G\) and uses
  the proper perspective cone
  \(u v^{p-1}\geq\|w_G\|_p^p\).  Its primal boundary fiber is uniquely
  \(u_G=\|x_G\|_p^p,v_G=1\); the dual Young factor
  \((1/p,\|y_G\|_q^q/q,-y_G)\) gives a global \(C^1\) normalized dual
  sheet.  At \(d\geq N+1\), the direct \(p\)-order cone attains
  \((S,k,M)=(N-1,1,N+1)\).  For \(p=2\), the grouped cones are Lorentz and
  \(\nu_{\min}=2k_{\min}\); for \(p\ne2\), the exact nonsymmetric barrier
  optimum remains open.  On every grouped reduced slice, however, the
  embedded-cube argument gives the arbitrary-coupled lower bound
  \(\vartheta_{\rm slice}\geq k_{\min}\); it is exact at \(p=2\).
  The cone, duality, regularity, and lower-bound
  arguments have been independently audited.
- [Robust \(Q_3\) phase integrability](2026-09-04-robust-q3-phase-integrability.md)
  gives a quantitative approximate analogue of the preceding exact
  submersion obstruction.  For any nonzero globally \(C^1\) Lorentz
  boundary factor on \(S^{N-1}\), \(N\geq3\), with contact defect
  \(0\leq\sigma\leq\epsilon\), derivative \(\|d\sigma\|\leq\eta\), and
  radial log-scale bound \(K\), its mixed channel satisfies
  \(\|{-dA^*dB}\|\leq K\eta+K^2\epsilon\) at some phase-critical point.
  Hence uniform \(\delta\)-closeness to rank-one positive forms with mass
  at least \(\mu\) forces
  \[
                    \delta+K\eta+K^2\epsilon\geq\mu.
  \]
  More strongly, for exactly \(n=N-1\) near-rank-one channels whose sum is
  \(\xi\)-close to the sphere metric, the spectral floor is automatic and
  common bounds obey
  \[
                    \xi+(n+1)\delta+K\eta+K^2\epsilon\geq1.
  \]
  A modulus-of-continuity interpolation gives
  \(\eta=\inf_r[\epsilon/r+\bar\omega(r)]\), and the \(C^{1,1}\) case gives
  \(\eta\leq\sqrt{2H\epsilon}\).  The independently audited inequality
  holds in every \(N\geq3\), including the parallelizable exceptions
  \(N=4,8\).  It is restricted to globally labelled, quantitatively
  nonzero \(Q_3\) boundary selections with controlled radial gauge and
  individual \(C^1\) modulus; it is not a no-go theorem for arbitrary
  approximate lifts.
- [Robust rank-\(r\) submersion obstruction](2026-09-04-robust-saturated-block-submersion.md)
  extends the phase theorem to a locally saturated block of dimension
  \(r+2\).  Outside the only proper sphere-submersion pairs
  \((n,r)=(3,2),(7,4),(15,8)\), every normalized ray map
  \(S^n\to S^r\) has a critical point.  There the mixed channel splits as
  \[
       -dA^*dB=-a\,dp^*dB-d\log(a)\otimes(A^*dB),
  \]
  with the first term of rank at most \(r-1\).  Thus uniform
  \(\delta\)-closeness to rank-\(r\) forms with \(r\)-th singular value at
  least \(\mu\) forces the audited threshold
  \[
                         \delta+K_A\eta_B\geq\mu,
        \qquad \eta_B=\sup\|A^*dB\|.
  \]
  If both normalized primal and dual base boundaries are \(C^1\), the
  sharper right side is
  \(\delta+\min\{K_A\eta_B,K_B\eta_A\}\geq\mu\).  Cone
  nonnegativity and a one-sided \(C^1\) modulus derive
  \(\eta_B\leq\inf_s[\epsilon/s+\bar\omega_B(s)]\), or
  \(\sqrt{2H_B\epsilon}\) in the Lipschitz-derivative case.  A total
  diagonal derivative alone is insufficient for \(r>1\); an explicit
  normal-misalignment term is necessary.  In every nontrivial saturated
  product profile, the Hopf-rank arithmetic guarantees at least one
  forbidden block.  This remains a theorem for global nonzero \(C^1\)
  boundary selections with controlled one-sided contact regularity, not
  for arbitrary approximate lifts.
- [Contact regularity versus IPM conditioning](2026-09-04-contact-regularity-vs-ipm-conditioning.md)
  identifies the exact algorithmic boundary of that robust theorem.  In the
  \(C^{1,1}\) regime it gives the intrinsic cross-contact blowup
  \[
       H_B\geq { (\mu-\delta)^2\over 2K_A^2\epsilon},
  \]
  but two explicit, independently audited Lorentz families prove that
  neither \(K_A\) nor the one-sided contact derivative is bounded by a
  standard central-neighborhood radius, primal/dual barrier-Hessian
  conditioning, NT scaling conditioning, or even a pointwise artificial
  KKT condition number.  One family is exactly central with bounded scales
  while \(K_A\to\infty\); the other stays in any fixed central neighborhood
  while contact error vanishes and one-sided sensitivity diverges.  Hence a
  genuine QIPM condition-number or bit-precision lower bound requires a
  normalized cross-instance data-path/sensitivity contract.  If such a
  contract gives \(K_A\leq c_K\chi^a\) and
  \(H_B\leq c_H\chi^b\), the rigorous conditional consequence is
  \(
    \chi\geq[(\mu-\delta)/(c_K\sqrt{2c_H\epsilon})]^{1/(a+b/2)}
  \).
- [Exact ball formulation barrier--regularity--treewidth
  tradeoff](2026-09-04-ball-formulation-latent-treewidth-tradeoff.md)
  turns the curvature, topology, and latent-Hessian results into a sharp
  formulation theorem.  For \(N\geq3\), the direct \(Q_{N+1}\) slice is
  bi-contact-regular with \(\nu_{\rm amb}=2\) and a one-hub Newton graph
  that is a tree of size \(N+3\).  A minimum pure-\(Q_3\) norm tree has
  \(N-1\) blocks, \(\nu_{\rm amb}=2N-2\), and a one-hub graph that is again
  a tree, now of size \(5(N-1)\), but every count-optimal lift has a global
  primal or dual contact defect.  Requiring bi-contact regularity costs
  exactly one further block and two barrier units; the smooth coordinate
  \(Q_3^N\) lift attains them with an exact width-two graph of size \(5N+1\).
  Thus small-cone compilation buys no asymptotic Newton sparsity after rank
  expansion, but forces a linear ambient-barrier penalty; removing contact
  singularities under the dimension-three cap has an additional exact
  one-block penalty.  All three exact systems solve in \(O(N)\) arithmetic,
  so the corresponding generic well-initialized short-step envelopes are
  \(O(N\log(1/\epsilon))\) direct versus
  \(O(N^{3/2}\log(1/\epsilon))\) for both granular formulations.  The
  theorem and graph counts passed hostile audit.  The new path-independent
  reduced-barrier corollary makes the iteration separation genuine in the
  bounded-feasible-Dikin-step model: under cap \(d\), both count-minimal
  norm trees and smooth grouped lifts require
  \(\Omega(\sqrt{N/(d-2)}\log(1/\epsilon))\) rounds from their analytic
  centers, while the direct ball needs only
  \(\Theta(\log(1/\epsilon))\).  All three per-round latent solves remain
  \(O(N)\).  Under mandatory \(\Theta(N)\)-coordinate materialization at
  every round, this gives a tight
  \(\Theta(N\sqrt{\lceil N/(d-2)\rceil}\log(1/\epsilon))\)
  full-output work frontier for the granular formulations versus
  \(\Theta(N\log(1/\epsilon))\) direct, with a matching classical
  implementation and hence no polynomial quantum advantage under the same
  contract.  The square-root compilation tax is not an unconditional
  finite-precision, long-step, custom-barrier, or output-only lower bound.
- [Exact reduced norm-tree barrier
  parameter](2026-09-04-norm-tree-reduced-barrier-parameter.md)
  adds the formulation-sensitive slice ledger omitted by the ambient
  comparison.  For a norm tree of arbitrary node arities and \(L\) Lorentz
  factors, fixing its root gives exact parameter \(2L-2\) iff every root
  slot is an internal-child axis, and \(2L-1\) iff a root slot is a free
  leaf.  Under a cone-dimension cap \(d\), put
  \(L_0=\lceil(N-1)/(d-2)\rceil\).  The exact optimum over all capped norm
  trees is \(2L_0-1-\chi_{N,d}\), where \(\chi_{N,d}=1\) exactly when
  \(L_0\geq3\) and
  \[
    N-1\leq(L_0-1)(d-2)+\min(d-1,L_0-1)-1.
  \]
  The proof converts logarithmic homogeneity into an exact root-leverage
  formula, bounds an arbitrary-arity diagonal-plus-rank-one Schur complement
  sharply by superadditivity, and solves the root-incidence feasibility
  problem exactly.  The smooth grouped lift uses only
  \(h=\lceil N/(d-2)\rceil\in\{L_0,L_0+1\}\) factors and has exact reduced
  parameter \(h\).  It therefore weakly dominates the count-minimal norm
  tree in the displayed reduced parameter and, except for two explicit
  small equality families, strictly improves it; asymptotically the gap is
  a factor of two.  The independently audited result is not an optimum over
  arbitrary coupled slice barriers and not an iteration lower bound.
  Nevertheless, an explicit \(L\)-dimensional polytope affine section of
  every \(L\)-block norm-tree slice proves the formulation-intrinsic lower
  bound \(\nu\geq L\) for **every** self-concordant barrier on that extended
  domain.  Before root fixing, the corresponding complementary-ray cone
  section and Hildebrand's conic active-facet theorem give
  \(\nu_{\rm LH}\geq L+1\) for every logarithmically homogeneous barrier on
  the full linked cone.  Hence the smooth grouped barrier lies within one unit of the
  lower bound forced by any count-minimal norm-tree formulation and matches
  it numerically whenever \(h=L_0\).  This arbitrary-barrier statement also
  passed independent hostile audit; attainability of the norm-tree floor
  \(L\) remains open.
- [Path-independent norm-tree small-step lower
  bound](2026-09-04-norm-tree-short-step-iteration-lower-bound.md)
  upgrades that parameter ledger to an actual iteration obstruction for
  the fixed standard restricted barrier.  For \(k\) copies of any rooted
  norm tree with \(b\) internal blocks, \(L=kb\), an explicit analytic
  center has every determinant equal to \(1/b\).  The tree determinants
  telescope exactly to \(1-\|w_a\|^2\), so an all-positive objective gap
  at most \(\epsilon\) forces their full product below
  \((2\epsilon/L)^L\).  If \(\nu_T\) is the exact restricted parameter of
  one tree and \(\nu=k\nu_T\), the global gradient inequality makes the
  distance from that center to the entire accurate set at least

  \[
    \left[{L\over\sqrt\nu}
      \log\!\left({k\over2\epsilon}\right)\right]_+.
  \]
  Consequently every path assembled from at most \(m\) feasible
  \(R\)-Dikin chords per round, starting \(\rho\)-close to the center,
  requires the explicit lower bound

  \[
    {\left[(L/\sqrt\nu)\log(k/(2\epsilon))
       -\log(1/(1-\rho))\right]_+
     \over m\log(1/(1-R))}.
  \]
  This holds for every tree shape and arity and uses no central-path
  condition after initialization.  It is an independently hostile-audited
  geometric lower bound for a fixed lift, barrier, and bounded-feasible-
  chord model, not for long-step, infeasible, output-only, or unrestricted
  quantum algorithms.  General Riemannian-distance lower bounds for
  short-step methods are prior art; the new candidate contribution is the
  explicit norm-tree distance-to-accurate-set certificate.  The audited
  heterogeneous refinement assigns tree \(a\) a block share
  \(p_a=b_a/L\) and objective weight \(\lambda_a\), and replaces the raw
  source count by the exact effective scale

  \[
    \Delta_{\rm eff}=\prod_a(\lambda_a/p_a)^{p_a}.
  \]
  For equal weights this is \(\exp(H(p))\), so the obstruction records the
  entropy of a nonuniform sparse compilation; it equals the full objective
  range exactly when weights are proportional to block counts.
  The exact central path also collapses to a tree-shape-independent scalar
  profile: every determinant equals
  \(2/(\sqrt{b^2+\tau^2}+b)\), and its squared logarithmic speed is
  \(L(1-b/\sqrt{b^2+\tau^2})\).  Its closed-form arc length can be
  partitioned into \(O(\sqrt L\log(k/\epsilon))\) feasible bounded-Dikin
  chords.  Thus the path-independent lower is matching-order, not merely a
  one-sided obstruction, for this fixed barrier model.  Quantitatively, the
  central-path arc is asymptotically within
  \(\sqrt{\nu/L}<\sqrt2\) of the distance lower bound before the
  radius-dependent chord discretization, a dimension-independent
  specialization of the general Riemannian sub-geodesic theory.
- [Exact ball-cap latent-treewidth
  Pareto frontier](2026-09-04-ball-cap-latent-treewidth-pareto.md)
  extends the preceding three-point comparison to every block cap
  \(3\leq d<N+1\) under global bi-\(C^1\) primal and polar factors.  The
  simultaneous optima are
  \[
    k_{\min}=\left\lceil{N\over d-2}\right\rceil,\qquad
    M_{\min}=N+2k_{\min},\qquad
    \nu_{\rm amb,min}=2k_{\min}.
  \]
  A grouped Lorentz lift attains them.  Its explicitly reduced separable
  paraboloid barrier has exact parameter \(k_{\min}\), including after the
  final sum equality; a direct third-derivative and local-dual-norm
  calculation separates this from the exact ambient logarithmically
  homogeneous value \(2k_{\min}\).  The embedded-cube theorem now proves
  that \(k_{\min}\) is optimal over arbitrary coupled slice barriers on this
  fixed grouped formulation.  After eliminating block-local affine
  equalities, its exact one-hub structural graph is a tree with
  \(N+2k_{\min}+1\) vertices; its positive-diagonal signed two-hub
  quasidefinite graph has exact width two.  The raw conic graphs have exact
  widths two and three, the latter certified by a \(K_4\) subdivision.  Thus
  every cap admits \(O(N)\) exact Newton work, while the standard
  ambient-product short-step envelope varies sharply as
  \(O(N\sqrt{\lceil N/(d-2)\rceil}\log(\Delta/\epsilon))\).
  The independent hostile audit checked the reduced Hessian, Jacobian
  congruence, raw and reduced graph counts, and the distinction between the
  exact ambient and displayed reduced parameters.  This is not an
  iteration lower bound or an all-lifts intrinsic optimum,
  and the quasidefinite numerical branch retains explicit regularization and
  refinement hypotheses.
- [Rank-two curvature summands spend two vector fields](2026-09-04-rank-two-curvature-summand-topology.md)
  strengthens the Adams obstruction from three-dimensional factors to
  mixtures of three- and four-dimensional factors.  If their respective
  counts are \(a,b\) and \(N\geq4\), then
  \[
                    a+2b\leq\rho(N)-1.
  \]
  The reason is that every oriented two-plane bundle on \(S^{N-1}\) is
  trivial when \(N-1\geq3\).  Hence a globally \(C^2\) saturated
  factorization with all blocks of dimension at most four is possible only
  if \(N\in\{2,3,4,8\}\).  More generally, blocks of dimension at least five
  must carry at least \(N-\rho(N)\) curvature ranks, so under cap \(d\) there
  are at least
  \(\left\lceil\frac{N-\rho(N)}{d-2}\right\rceil\) such blocks.  Under cap five the
  congruence \(N\equiv6\pmod {12}\) is impossible.  The note also records
  the exact unstable clutching-class test for arbitrary prescribed ranks
  and explains why stable \(KO\)-theory alone is mostly silent.  The results
  have passed an independent hostile audit and retain the same
  global-selection—not lift-nonexistence—scope.
- [Steenrod effective curvature capacity](2026-09-04-steenrod-effective-curvature-capacity.md)
  gives the much stronger arbitrary-rank obstruction.  For
  \(n=N-1\), \(s=\rho(N)-1\), and curvature ranks
  \(r_i=m_i-2\), every subset satisfies
  \[
       0<\sum_{i\in I}r_i\leq n/2
       \quad\Longrightarrow\quad
       \sum_{i\in I}r_i\leq s.
  \]
  This follows by applying the classical Steenrod plane-field theorem to
  the direct sum of those curvature subbundles.  If \(s<n/3\), there is
  consequently a unique dominant block with
  \(r_*\geq n-s\), hence
  \[
                         m_*\geq N+2-\rho(N).
  \]
  The condition holds for every \(N\geq3\) except \(N\in\{4,8,16\}\), and
  \(m_*\geq N-2\log_2N\).  Thus no bounded, polylogarithmic, or \(o(N)\)
  block cap can admit a globally \(C^2\) saturated factorization in all
  large dimensions.  If the cap is below \(N+2-\rho(N)\), integrality
  strengthens the curvature budget to \(\sum_i(m_i-2)_+\geq N\), with the
  corresponding one-unit factor, ambient-dimension, and barrier penalty.
  The dominant rank is sharp at the pure tangent-bundle level, since a
  maximal Adams frame and its orthogonal complement have ranks
  \(\rho(N)-1\) and \(N-\rho(N)\).
  Under a cap \(c=d-2\leq n/2\), each block also has
  effective curvature capacity at most \(\min\{c,s\}\), yielding the
  audited factor, ambient-dimension, and coupled-barrier lower bounds in the
  note.  The exact source statement, subset argument, dominant-block
  arithmetic, and scope have passed hostile audit.  This remains a global
  factor-selection theorem; the robust and contact-regular versions inherit
  it only when their hypotheses produce the same continuous splitting.
- [Robust global saturation topology](2026-09-04-robust-global-saturation-topology.md)
  makes that obstruction quantitative for approximate balls.  For
  \(B_2^N\subset C_\epsilon\subset(1+\epsilon)B_2^N\), globally \(C^2\)
  factor maps through \(k\) blocks of dimensions \(m_i\), and the saturated
  rank budget \(\sum_i(m_i-2)=N-1\), base-norm lower bound \(\mu\),
  first-derivative bound \(L\), and contracted second-derivative bound \(H\)
  produce a continuous direct-sum decomposition of \(T^*S^{N-1}\) whenever
  \[
  \mathfrak E_k(\epsilon)=\frac{2L\sqrt{2Hk\epsilon}}{\mu}
  +\frac{L^2\epsilon}{\mu^2}
  +\frac{2H\epsilon^2}{\mu^4}<1
  \]
  (with the stated chart-radius and \(\epsilon<\mu^2\) conditions).  Hence
  the number \(q\) of three-dimensional blocks obeys Adams's bound
  \(q\leq\rho(N)-1\).  If every block is three-dimensional this recovers
  \(N\in\{2,4,8\}\); more strongly, for odd \(N\geq3\), the Euler class
  forces a single positive-capacity block of dimension \(N+1\), so no cap
  \(d<N+1\) is possible.  The note also removes the fixed-coordinate
  loophole: using the exact \(\psi_{r_0}\) errors, it defines the
  blockwise-\(GL\)-invariant index
  \(\mathcal D=\inf_S\max\{\Gamma(S),E(S)\}\) and proves
  \(\mathcal D\geq1\) for every topologically obstructed saturated rank
  profile.  This independently audited robust counterpart to the preceding
  exact [global topology theorem](2026-09-04-global-smooth-saturation-topology.md)
  is still a global-selection obstruction, not an unrestricted
  approximate-lift or QIPM condition-number lower bound: \(\mathcal D\)
  depends on the chosen factor selections and sphere parameterization.
- [Conditioned stability for approximate balls](2026-09-04-approximate-ball-curvature-stability.md)
  extends the curvature budget to outer approximations
  \(B_2^N\subset C\subset(1+\epsilon)B_2^N\).  The mixed slack derivative
  remains exactly \(I_{N-1}\); only complementarity is perturbed.  An
  explicit near-complementarity estimate gives errors \(e_i\) such that
  \(\sum_i e_i<1\) forces
  \(N-1\leq\sum_i\max\{m_i-2,0\}\).  Uniform nonzero base-factor norms,
  bounded first and second derivatives, a fixed chart radius, and a bounded
  block count give \(\sum_i e_i=O(\sqrt\epsilon)\). Metric accuracy alone
  cannot force the weighted/non-ray conclusion at *any* positive error:
  arbitrarily accurate circumscribed polytopes have ray-only orthant lifts.
  This does not rule out a lower bound on the total number of rays, which
  grows with accuracy. Separately,
  \(B_2^{d-1}\times B_2^{d-1}\) uses two \(d\)-dimensional Lorentz blocks
  and is a \(\sqrt2\)-approximation where the exact ball needs three blocks,
  so even an all-block theorem needs a small-error threshold. The conditioned
  theorem and both obstructions have passed an independent audit. In the
  prior Ben-Tal--Nemirovski lifted-polyhedral model, the sharp
  \(\Theta(N\log(1/\epsilon))\) inequality count is also the optimal
  ambient-orthant LHSC parameter, versus parameter two for the exact Lorentz
  cone. This comparison is dictionary-specific, not an intrinsic iteration
  lower bound.
- [Derivative-free finite-stencil stability](2026-09-04-conditioned-approximate-curvature-capacity.md)
  gives a complementary, fully discrete criterion.  On \(N\) tangent-stencil
  points, each approximate block mixed-difference matrix is within an
  explicit conditioning error \(\mathcal E_i\) of rank
  \((m_i-2)_+\).  If \(4(N-1)\epsilon+\sum_i\mathcal E_i<h^2\), the exact
  curvature-capacity and block-count lower bounds follow by Eckart--Young.
  A two-point \(\mathbb R_+^2\) construction shows that slack accuracy plus
  absolute boundedness of factors cannot replace the relative conditioning:
  its error tends to zero while its mixed difference equals the full ball
  signal.  This disproves only an unconditioned finite-stencil inference, not
  a global approximate-lift theorem.  The criterion, constants, and
  obstruction have been independently audited and literature-screened.
- [Factor conditioning versus QIPM invariance](2026-09-04-curvature-conditioning-kkt-invariance-obstruction.md)
  shows why the approximate theorem's Euclidean conditioning blowup is not
  yet a Newton-cost lower bound.  A sparse two-coordinate Lorentz boost can
  shrink both members of a complementary primal/dual boundary pair by an
  arbitrary factor while preserving every slack pairing.  Under the same
  cone-coordinate change, the standard-barrier Schur complement
  \(A\nabla^2F(z)^{-1}A^T\) is exactly invariant, although the raw Hessian
  condition number can change by \(\lambda^{-4}\).  The audited obstruction
  rules out inferring an intrinsic barrier-scaled QIPM condition number from
  the current \(\mu,L,H\) bounds alone; representation-specific KKT,
  normalization, and oracle costs may still change and require a separately
  fixed access model.
- [Symmetric-cone curvature capacity](2026-09-04-symmetric-cone-curvature-capacity.md)
  unifies and strengthens the Lorentz and PSD results through Euclidean
  Jordan algebra. A simple factor of rank \(r\), Peirce constant \(a\), and
  complementary contact ranks \(p,q\) has exactly \(apq\) mixed-curvature
  channels, without strict complementarity. Hence every symmetric-cone lift
  of a positively curved \(N\)-body obeys
  \[
  N-1\leq\sum_i a_ip_iq_i
  \leq\sum_i a_i\lfloor r_i^2/4\rfloor
  \leq M-\nu,
  \]
  where \(M\) is total cone dimension and \(\nu\) is total Jordan rank, or
  equivalently the optimal ambient normal-barrier parameter. Under
  irreducible block dimension cap \(d\), Lorentz norm trees are simultaneously
  optimal for the ball among *all* symmetric-cone products:
  \(k_{\min}=\lceil(N-1)/(d-2)\rceil\),
  \(\nu_{\min}=2k_{\min}\), and \(M_{\min}=N-1+2k_{\min}\).
  The theorem includes real, complex, quaternionic, Lorentz, and exceptional
  blocks and has been independently audited and literature-screened.
- [Symmetric-cone support-orbit rigidity](2026-09-04-symmetric-cone-support-orbit-rigidity.md)
  upgrades the local Jordan capacity law under globally labelled bi-\(C^1\)
  primal/polar factors.  Saturation makes each support-idempotent map a
  submersion onto its balanced idempotent orbit, and makes the joint map
  from \(S^{N-1}\) a same-dimensional finite covering.  The complete
  simple-EJA classification then forces exactly one positive factor:
  \(Q_{N+1}\) in every contact dimension except two, where
  \(\mathbb S_+^3\) is the only additional topological possibility.  That
  exception needs at least three active rays by the Schwarz genus of
  \(S^2\to\mathbb {RP}^2\), so it is strictly dominated by \(Q_4\); for
  the round three-ball a separately audited finite-affine-selection and
  determinant argument excludes it entirely, even with finitely many
  \(C^1\) ray factors.
  Consequently every cap \(3\leq d<N+1\) forces the strict integer budget
  \(\sum_i a_i\lfloor r_i^2/4\rfloor\geq N\), and grouped Lorentz factors
  attain the exact simultaneous ball frontier
  \[
    k_{\min}=\left\lceil{N\over d-2}\right\rceil,\qquad
    M_{\min}=N+2k_{\min},\qquad \nu_{\min}=2k_{\min}.
  \]
  Independently of a cap, it also gives the sharp defect dichotomy:
  \(M-\nu=N-1\) only for one positive \(Q_{N+1}\) block, up to ray
  factors; every other globally regular symmetric-cone factorization has
  \(M-\nu\geq N\).
  For \(d\geq N+1\), one \(Q_{N+1}\) gives \((1,N+1,2)\).  Two independent
  audits checked the Peirce support differential, covering proof, orbit
  classification, ray-genus refinement, and construction.  The result is a
  global-factor regularity theorem, not an unrestricted lift lower bound.
- [Exact standard-slice barrier frontier for capped symmetric-cone
  balls](2026-09-04-symmetric-cone-standard-slice-barrier-frontier.md)
  converts Peirce curvature into a direct restricted-barrier lower bound.
  Along a segment from a selected boundary fiber to Slater, the standard
  Jordan log-determinant has logarithmic order equal to the fiber's total
  primal Jordan nullity \(Z\), so
  \(\nu_{\rm std,slice}\geq Z\).  The curvature chain gives
  \(N-1\leq(d-2)Z\); in the only divisible equality case, every active
  block would be a fixed saturated \(Q_d\) block and their joint phase map
  would give an impossible sphere-to-product covering.  Therefore the exact
  Euclidean-ball optimum is
  \[
   \nu_{\rm std,slice}^{\min}=
   \begin{cases}
    \lceil N/(d-2)\rceil,&3\leq d<N+1,\\
    1,&d\geq N+1.
   \end{cases}
  \]
  Grouped Lorentz and direct Lorentz lifts attain the two regimes.  The
  theorem is independently hostile-audited and concerns the standard
  product barrier after restriction, not arbitrary custom barriers or an
  iteration lower bound.
- [Exact Lorentz curvature budget](2026-09-04-exact-lorentz-curvature-budget.md)
  sharpens the earlier
  [SOC-granularity note](2026-09-04-soc-granularity-barrier-tradeoff.md).
  Every exact lift of the \(N\)-ball by Lorentz blocks, even with arbitrary
  affine slices, projections, and free variables, obeys
  \[
  \sum_i(m_i-2)\geq N-1.
  \]
  Hence the exact minimum number of blocks of dimension at most \(d\) is
  \(\lceil(N-1)/(d-2)\rceil\), matching the norm tree, and the exact minimum
  ambient normal-barrier parameter is twice this number. More generally,
  the same weighted lower bound holds for every SOC-lifted compact body
  having one relatively-open \(C^2\) boundary point of strict positive
  curvature. The proof factors the boundary slack and decomposes its mixed
  curvature into rank-\(\leq m_i-2\) Lorentz terms. This is a
  representation-dependent QIPM granularity law, not a universal iteration
  lower bound.
- [PSD-block curvature capacity](2026-09-04-psd-block-curvature-capacity.md)
  extends the differential slack method beyond SOCP. At a smooth
  primal/polar contact, a complementary \(S_+^r\) factor pair of ranks
  \(p,q\) contributes mixed-curvature rank at most \(pq\), without assuming
  strict complementarity. Consequently every product-PSD lift of an
  \(N\)-dimensional body having one relatively-open \(C^2\), strictly
  positively curved boundary point obeys
  \[
  \sum_i\left\lfloor r_i^2/4\right\rfloor\geq N-1.
  \]
  Blocks of size at most \(d\) therefore number at least
  \(\lceil(N-1)/\lfloor d^2/4\rfloor\rceil\), and their ambient normal
  barrier is \(\Omega(N/d)\). For \(d=2\), this recovers the exact
  \(N-1\)-block Lorentz theorem. The result is independently audited and
  literature-screened.
- [Hermitian PSD support maps force a strict all-order smooth
  gap](2026-09-04-psd-support-grassmannian-submersion.md) upgrades that local
  bound under global bi-\(C^1\) primal/polar factor selections.  Equality in
  \(\sum_i\lfloor r_i^2/4\rfloor\geq N-1\) makes every factor strictly
  complementary with balanced ranks and turns its range map into a
  submersion onto
  \(\operatorname{Gr}_{\lfloor r_i/2\rfloor}(\mathbb R^{r_i})\).  The
  combined range map is a same-dimensional covering from \(S^{N-1}\) onto
  the product of these Grassmannians.  Passing to oriented covers, product
  cohomology forces one factor, while \(\pi_2\) excludes every balanced
  order \(r\geq4\); orders two and three handle the remaining cases.
  Therefore, for every \(N\geq4\) and arbitrary PSD matrix orders,
  \[
               \sum_i\left\lfloor{r_i^2\over4}\right\rfloor\geq N.
  \]
  Under an order cap \(R\), this gives
  \(k_+\geq\lceil N/\lfloor R^2/4\rfloor\rceil\),
  \(M\geq(2+1/\lfloor R/2\rfloor)N\), and
  \(\nu_{\rm normal}\geq RN/\lfloor R^2/4\rfloor\).
  For \(R=3\), grouped Schur-complement lifts attain the simultaneous
  Euclidean-ball optima
  \[
       k_{\min}=\lceil N/2\rceil,\qquad M_{\min}=3N,\qquad
       \nu_{\min}^{\rm normal}=\lceil3N/2\rceil.
  \]
  The same covering proof over mixed real, complex, and quaternionic
  Hermitian blocks shows that saturation is possible only for contact-sphere
  dimension \(1,2,\) or \(4\), realized by the rank-two division-algebra
  cones \(Q_3,Q_4,Q_6\).  Hence outside ball dimensions
  \(N\in\{2,3,5\}\),
  \[
    \sum_i a_i\left\lfloor{r_i^2\over4}\right\rfloor\geq N .
  \]
  It also gives matching fixed-order-two complex and quaternionic
  ball frontiers in their stated nonexceptional dimensions.
  The support-map theorem, topology, construction, and resource optima have
  been independently audited.  The result remains conditional on global
  factor regularity and is not an unrestricted SDP-lift or iteration lower
  bound.
- [Exact Hermitian-PSD standard-slice barrier
  frontier](2026-09-04-hermitian-psd-standard-slice-barrier-frontier.md)
  combines determinant nullity with the projective support-cover
  obstruction.  For a fixed field
  \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\), order cap \(R\),
  \(a=\dim_{\mathbb R}\mathbb F\), and \(b=a(R-1)\), the exact globally
  bi-\(C^1\) ball frontier is
  \[
   \nu_{\rm std,slice}^{\min}=
   \begin{cases}
    1,&N\leq b,\\
    1,&R=2,\ N=a+1,\\
    \lceil N/b\rceil,&\text{otherwise}.
   \end{cases}
  \]
  The exceptional second line is precisely the direct division-algebra
  spin cones \(Q_3,Q_4,Q_6\).  The real order-\(R\geq3\) divisible case,
  which topology alone does not exclude, is ruled out by a new affine PSD
  pencil argument: the projective kernel cover would invert an even
  quadratic map on a sphere.  Grouped Hermitian Schur blocks attain every
  value.  The theorem is independently audited and concerns the standard
  restricted log-determinant, not custom barriers or an iteration lower
  bound.
- [Dense-open contact regularity does not imply the global capacity
  gap](2026-09-04-generic-contact-regularity-obstruction.md) shows that this
  qualification is essential.  A binary norm-tree lift represents
  (B_2^N) with exactly (N-1) copies of (Q_3), saturating the local
  budget.  Its primal boundary fiber is unique, and explicit primal and dual
  factors are continuous semialgebraic and real analytic away from a
  codimension-at-least-two set.  The generic joint support map is a local
  diffeomorphism but is not proper: when a subtree vanishes, one Lorentz
  factor hits the cone vertex and its support circle has direction-dependent
  limits.  Thus generic smoothness, definable choice, stratification, and
  graph normalization alone cannot upgrade the conditional (+1) gap to an
  unconditional affine-lift theorem.
- [Projective rank-one contact kernels force Euclidean
  embeddings](2026-09-04-projective-contact-q3-embedding-bound.md) gives a
  distinct conditional small-cone obstruction on the pure-state stratum.
  For the strict-diagonal kernel
  \(1-\operatorname{tr}(xx^Tyy^T)=1-(x^Ty)^2\) on
  \(\mathbb{RP}^{r-1}\), globally labelled nowhere-zero \(C^1\)
  \(Q_3^L\) factors lift to real phases whose joint map embeds
  \(\mathbb{RP}^{r-1}\) in \(\mathbb R^L\).  Stiefel--Whitney classes and
  Lucas parity give
  \[
  L\geq
  \begin{cases}
  r,&r\text{ a power of two},\\
  2^{\lceil\log_2r\rceil}-1,&\text{otherwise}.
  \end{cases}
  \]
  In particular, \(r=2^t+1\) forces \(L\geq2r-3\).  At \(r=3\), the
  nonembedding of \(\mathbb{RP}^2\) in \(\mathbb R^3\) and an explicit
  Veronese--stereographic construction give the exact nowhere-zero
  fixed-contact count \(L=4\).  This is not a full PSD-cone SOC-lift claim;
  Fawzi's nonrepresentability theorem has a different, stronger scope.
  The obstruction tensorizes: on \((\mathbb{RP}^{r-1})^k\), the analogous
  weighted strict-diagonal kernel forces
  \(L\geq\max\{k(r-1)+1,\,k(2^{\lceil\log_2r\rceil}-1)\}\), and hence
  \(L\geq k(2r-3)\) for \(r=2^t+1\).  This additive sparse-product effect
  follows from the external product of the inverse normal classes and was
  independently audited.
- [Exact PSD order-cap resource and QIPM
  ledger](2026-09-04-psd-order-cap-qipm-ledger.md) extracts the strongest
  integer consequences of the all-order theorem.  With
  \(c_r=\lfloor r^2/4\rfloor\), factor count, cone-coordinate dimension, and
  exact ambient normal-barrier parameter are the three covering minima
  \[
    \min_{\sum c_ra_r\geq N}
      \left(\sum a_r,\ \sum {r(r+1)\over2}a_r,\ \sum ra_r\right).
  \]
  The factor minimum is \(\lceil N/c_R\rceil\); the dimension minimum has an
  exact \(O(NR)\) knapsack recurrence; and, writing
  \(N=qc_R+t\), the normal-parameter minimum has the closed form
  \(qR+\mathbf1_{t>0}\lceil2\sqrt t\rceil\).  In particular,
  \(\nu_{\rm normal}\geq\lceil2\sqrt N\rceil\) and
  \(M\geq2N+\lceil\sqrt N\rceil\) without a cap.  These are capacity-only
  minima, not asserted attainable lift optima for \(R\geq4\).
  Grouped Schur-complement ball lifts have an exact count--dimension--barrier
  Pareto curve: at \(k\) balanced groups, their ambient parameter is \(N+k\)
  and their minimum dimension is explicit.  Eliminating public identity
  blocks collapses the same log determinant to an exact
  \(\nu_{\rm slice}=k\) paraboloid barrier whose one-hub Newton graph is a
  tree and solves in \(O(N)\) exact arithmetic per round.  Its embedded
  \(k\)-cube proves that this reduced value is optimal among arbitrary
  coupled barriers on the grouped Schur slice.  Hence, under
  matched access and mandatory \(N+k\)-coordinate materialization, every
  QIPM Newton round has a linear classical replacement and no polynomial
  full-output advantage.  This is not a condition-number, finite-precision,
  compressed-output, or iteration lower bound.
- [PSD nullity gives an exact restricted log-det
  frontier](2026-09-04-psd-nullity-restricted-barrier.md) closes the slice
  optimality gap left by the capacity ledger.  At a selected boundary tuple,
  the restricted standard log-determinant has vanishing order equal to total
  primal nullity, so its self-concordant parameter is at least that nullity.
  A PSD block of order at most \(R\) carries at most \(R-1\)
  mixed-curvature dimensions per nullity unit.  The apparent
  \(N-1\) divisibility equality would make the contact sphere finitely cover
  a product of projective spaces; covering topology, plus cross-contact
  slack injectivity in the one-factor case, excludes it.  Therefore, among
  strictly feasible globally \(C^1\) full-contact selected PSD-product
  lifts of \(B_2^N\),
  \[
        \nu_{\rm std,slice}^{\min}
          =\left\lceil{N\over R-1}\right\rceil .
  \]
  Grouped Schur lifts attain equality for every cap, while retaining an
  \(O(N)\) exact tree solve.  This yields the sharp standard-barrier
  short-step certificate
  \(O(\sqrt{\lceil N/(R-1)\rceil}\log(\Delta/\epsilon))\);
  it is not an arbitrary coupled-barrier or actual iteration lower bound.
  The nullity, equality-topology, construction, and QIPM scope all passed an
  independent hostile audit.
- [PSD column packing shares full product-ball slack
  rows](2026-09-04-psd-column-packing-product-balls.md) gives the sharp
  boundary between Lorentz no-sharing and higher-rank PSD sharing for
  \(C=(B_2^s)^b\).  Combining all polar extreme rows through one common
  support differential, then using full-slack injectivity to exclude
  equality, gives
  \[
       \sum_i\left\lfloor r_i^2/4\right\rfloor
          \geq b(s-1)+1.
  \]
  A finer cylindrical-zero argument shows that every source row needs a
  private primal-kernel direction, so
  \(\sum_i\operatorname{nullity}X_i(x)\geq b\) at every simultaneous
  extreme.  Hence, under order cap \(R\),
  \[
    \nu_{\rm std,slice}\geq
    \max\!\left\{b,
       \left\lceil{b(s-1)+1\over R-1}\right\rceil\right\}.
  \]
  PSD factorwise no-sharing is nevertheless false.  A shared-principal-block
  Schur lift of order \(p+c\) packs \(c\) coordinate groups, even from
  different balls, into one factor with \(pc\) curvature channels and exact
  restricted parameter \(c\).  Packing all rows gives a one-factor
  polynomial lift of order
  \(\min_p[p+b\lceil s/p\rceil]\); the transparent order-\((s+b)\)
  specialization has exact restricted parameter \(b\).  Balanced packing
  matches the factor-count, ambient-parameter, and cone-dimension lower
  scales in the stated ceiling-free regime.  The exact standard-slice
  optimum is \(b\) for \(R\geq s+1\); a small-cap integer gap remains.
  For the transparent one-factor order-\((s+b)\) slice, a
  [bounded-fiber projection theorem](2026-09-04-one-block-psd-packing-coupled-barrier.md)
  strengthens this further: its intrinsic parameter is exactly \(b\) among
  all nondegenerate self-concordant barriers, even fully coupled and
  non-logarithmically homogeneous.  Exact partial minimization sends any
  hypothetical smaller lift barrier to the product of balls, where a
  \(b\)-cube gives the sharp lower bound.  This also handles \(b>s\), without
  requiring \(b\) orthogonal column directions in \(\mathbb R^s\).
  Bare embedding topology cannot close the remaining small-cap capacity
  gap: an explicit codimension-one
  embedding \(S^p\times S^p\hookrightarrow\mathbb {RP}^{2p+1}\) defeats
  generic characteristic-class arguments, so any \(bs\) strengthening must
  use the row-specific cylindrical subspaces.  The lower bounds,
  construction, barrier calculation, ceiling ledger, and codimension
  boundary were independently hostile-audited.  These are formulation
  certificates, not iteration lower bounds.
- [One PSD factor still forces square-root-many bounded
  steps](2026-09-04-one-factor-psd-packing-short-step-lower-bound.md)
  turns the transparent packing construction into an actual,
  path-independent iteration obstruction.  At its analytic center the
  Schur complement is (D=I_h).  Objective error at most \(\epsilon\)
  makes every diagonal residual collectively small; Hermitian Hadamard
  (including the quaternionic Moore determinant) and AM--GM imply

  \[
       \det D\leq(2\epsilon/h)^h,
       \qquad F=-\log\det D\geq h\log(h/(2\epsilon)).
  \]
  Since the restricted barrier has exact gradient parameter \(h\), its
  value changes at speed at most \(\sqrt h\) in its Hessian metric.
  Therefore any method using at most \(m\) feasible \(R\)-Dikin substeps
  per round needs at least

  \[
       {\sqrt h\log(h/(2\epsilon))
        \over m\log(1/(1-R))}
  \]
  rounds from the center, regardless of directions or intermediate
  centrality.  This proves that collapsing \(h\) product-ball rows into
  one real, complex, or quaternionic PSD factor does not collapse the
  standard-barrier short-step count.  The independently audited theorem is
  fixed-lift, fixed-barrier, exact-real, and bounded-feasible-step; it is
  not an unrestricted IPM or QIPM lower bound.
- [Exposed Jordan rank forces bounded-Dikin iterations on arbitrary
  symmetric-cone lifts](2026-09-04-symmetric-cone-exposed-rank-dikin-lower-bound.md)
  subsumes the determinant-distance mechanism in a coordinate-free form.
  If an optimal dual exposing slack has total Jordan rank \(Q\), its
  support-principal-minor potential has exact local dual norm \(\sqrt Q\)
  in the standard log-determinant metric.  Objective error \(\epsilon\)
  forces that potential to increase by
  \(Q\log(\Delta/\epsilon)\), so every path to the accurate set has
  distance at least \(\sqrt Q\log(\Delta/\epsilon)\).  The proof uses
  \(P(c)P(x)P(c)=P(P(c)x)\), works for Lorentz, real/complex/quaternionic
  PSD, and exceptional \(H_+^3(\mathbb O)\) factors, and needs neither
  strict complementarity nor bounded inactive fibers.  For globally
  labelled \(C^1\) lifts of \(\prod_a B_2^{s_a}\), the summed support
  objective and Peirce curvature give
  \[
       \sum_a(s_a-1)\leq\sum_i a_ip_iq_i
          \leq\kappa Q,
       \qquad \kappa=\max_i a_i(r_i-1),
  \]
  and hence \(Q\geq\lceil\sum_a(s_a-1)/\kappa\rceil\).  This proves
  directly that factor sharing cannot shorten the square-root metric scale
  unless it genuinely lowers exposed Jordan rank by spending greater
  Peirce capacity.  For \(L\) factors from one Peirce-\(a\), order-at-most-
  \(R\) family, the sharper exact integer rank-budget envelope balances the
  dual ranks and has continuous relaxation
  \[
       n\leq a(RQ-Q^2/L),\qquad
       Q\geq {L\over2}\left(R-\sqrt{R^2-{4n\over aL}}\right).
  \]
  Near maximum curvature load this forces \(Q=\Theta(LR)\), so the metric
  coefficient is \(\Theta(\sqrt{LR})\), not merely \(\sqrt L\).  The
  Hauser--Güler classification extends the distance theorem from the
  standard barrier to every self-scaled barrier
  \(-\sum_i\alpha_i\log\det_i\), \(\alpha_i\geq1\), with weighted exposed
  rank \(Q_\alpha=\sum_i\alpha_iq_i\); rescaling cannot reduce the
  asymptotic coefficient.  For a single \(B_2^N\) under dimension cap
  \(d<N+1\), a global support-cover argument adds the missing divisible
  unit: some support objective always has
  \[
                  Q\geq\left\lceil{N\over d-2}\right\rceil.
  \]
  Equality at every contact would force a nonexistent finite cover
  \(S^{L(d-2)}\to(S^{d-2})^L\).  This existential hard-objective premium
  is independently audited; it is not claimed for every prescribed
  objective.  It is strictly stronger than the local sourcewise ceiling
  exactly when \(d-2\mid N-1\), including the saturated Lorentz case.
  For heterogeneous products lifted through order-at-most-
  \(R\) Hermitian PSD cones over \(\mathbb F\), the cylindrical row zeros
  give a stronger sourcewise theorem at every simultaneous contact:
  \[
      Q\geq\sum_a\left\lceil
        {s_a-1\over(\dim_{\mathbb R}\mathbb F)(R-1)}
      \right\rceil.
  \]
  Private dual-support quotients add inside the summed slack's range.  Mixed
  real, complex, and quaternionic orders obey the same formula with
  denominator \(\kappa_{\mathrm H}=\max_i\beta_i(r_i-1)\); arbitrary Lorentz
  blocks can also be mixed in because each productive complementary-ray
  rank unit is private to one source.  The independently audited
  [exceptional Albert incidence
  lemma](2026-09-04-exceptional-albert-sourcewise-exposed-rank.md) closes the
  last nonclassical case: an Albert block with aggregate exposed rank \(q\)
  serves at most \(q\) productive source rows, each through at most 16 real
  tangent channels.  Thus every product of simple symmetric cones satisfies
  \[
      Q\geq\sum_a\left\lceil{s_a-1\over\kappa}\right\rceil,
      \qquad \kappa=\max_i a_i(r_i-1),
  \]
  and, under dimension cap \(d\), every product of finite-dimensional
  symmetric cones satisfies
  \(Q\geq\sum_a\lceil(s_a-1)/(d-2)\rceil\).  This is exact against grouped
  Hermitian constructions for every nondivisible source.  The independently
  audited [sequential Peirce-compression
  theorem](2026-09-04-sequential-peirce-compression-additive-exposed-rank.md)
  is stronger for a selected hard objective.  With
  \[
   h_d(s)=\begin{cases}1,&d\geq s+1,\\
          \lceil s/(d-2)\rceil,&d<s+1,
          \end{cases}
  \]
  it proves \(Q\geq\sum_a h_d(s_a)\).  Compression into the face orthogonal
  to earlier row supports preserves the next exact one-ball factorization,
  while
  \(\operatorname{rank}P(e-c)y=\operatorname{rank}(c\vee\operatorname{supp}y)
  -\operatorname{rank}c\) makes all selected hard ranks telescope.  Thus the
  topological premium adds separately for every strict-cap divisible source.
  The branch \(d\geq s+1\) is necessary: a direct \(Q_{s+1}\) lift has rank
  one.  The bound is the exact minimax hard exposed rank over admissible
  globally labelled certificate sheets: separate grouped Lorentz lifts
  attain \(Q=\sum_a h_d(s_a)\) at every contact.  Combining the induction
  with the balanced finite-factor envelope
  strengthens this further to
  \(Q\geq\sum_a\max\{h_d(s_a),Q_{\min}(s_a-1)\}\) for at most \(L\)
  order-at-most-\(R\), Peirce-\(a\) factors.  This can be strictly stronger
  than applying the capacity envelope once to the total tangent dimension.
  The sheet hypothesis cannot be deleted.  The independently audited
  [selection-free Lorentz
  frontier](2026-09-04-selection-free-exposed-rank-premium-counterexample.md)
  proves the exact one-ball affine-lift minimax
  \[
    \inf_{\mathcal L}\max_{v\in S^{s-1}}
       \min_{Z\in\mathcal D_{\mathcal L}(v)}
          \sum_i\operatorname{rank}_JZ_i
       =\left\lceil{s-1\over d-2}\right\rceil .
  \]
  A grouped norm chain through dimension-at-most-\(d\) Lorentz cones has
  a unique certificate at every support and attains the right side.  It
  differs from \(h_d(s)\) by one exactly for strict-cap divisible sources.
  The same chain's restricted standard log-determinant has exact parameter
  \(2\lceil(s-1)/(d-2)\rceil-1\), because the missing dual rank reappears
  as primal nullity at a nonsmooth seam.  This separates exposed rank,
  smooth contact topology, and restricted-barrier complexity.  For
  arbitrary shared-factor product lifts, sequential compression gives the
  exact favorable-certificate product minimax
  \[
   \inf_{\mathcal L}
    \sup_{\substack{u\in\prod_aS^{s_a-1}\\Y^a\in\mathcal D_a(u_a)}}
     \sum_i\operatorname{rank}_J\!\left(\sum_a\lambda_aY_i^a\right)
       =\sum_a\left\lceil{s_a-1\over d-2}\right\rceil
       \qquad(\lambda_a>0).
  \]
  It also forces that much nullity in every primal fiber at the selected
  simultaneous contact.  Minimum rank over the full certificate fiber of
  the aggregate objective remains open because a certificate of a sum
  need not split positively into certificates of its rows.
  A further independently audited
  [rotated-Lorentz fiber
  counterexample](2026-09-04-rotated-lorentz-fiberwise-nullity-counterexample.md)
  rules out adding one unit with an “every primal completion” quantifier.
  With \(q=\lceil(s-1)/(d-2)\rceil\), every boundary fiber contains a
  completion of nullity exactly \(q\), and every support-certificate fiber
  has maximum rank exactly \(q\).  Nevertheless the restricted standard
  barrier parameter is \(2q-1\), witnessed by auxiliary-simplex vertices;
  the north-objective central path sees only the smaller \(\sqrt q\)
  logarithmic coefficient.  This separates fiberwise minimum nullity,
  favorable exposed rank, global barrier parameter, and objective-specific
  movement.
  The core result, exceptional incidence lemma, sequential theorem, and
  discrete envelope are independently
  audited and path independent, but the theorem is restricted
  to standard or self-scaled Jordan barriers and feasible iterates with
  bounded intrinsic displacement per counted round.  Its explicit Dikin
  specialization assumes local norm below one and a bounded number of
  chords per round; it is not a lower bound for arbitrary barriers or
  non-iterate quantum procedures.
- [Barrier-independent primal--dual bounded-Dikin
  theorem](2026-09-04-barrier-independent-primal-dual-dikin-lower-bound.md)
  supplies the precise all-barrier boundary missing from the preceding
  primal results. For any \(\nu\)-logarithmically homogeneous
  self-concordant barrier \(F\), Nesterov--Todd geometry makes the central
  point of gap \(\epsilon\) the analytic center of the entire feasible
  \(\epsilon\)-gap set. The product-barrier value on the central path is
  exactly \(\nu\log t-\nu\), while its gradient has product dual norm
  \(\sqrt{2\nu}\). Hence the distance from a central point of gap
  \(\Delta_0\) to **every** feasible \(\epsilon\)-gap output is at least
  \(\sqrt{\nu/2}\log(\Delta_0/\epsilon)\), and a trajectory of at most
  \(m\) product-cone \(\rho\)-Dikin chords per round needs
  \[
    T\geq{\sqrt{\nu/2}\log(\Delta_0/\epsilon)
            \over m\log(1/(1-\rho))}.
  \]
  This now has a universal bounded-dimension transfer. If a compact
  \(N\)-body has a positively curved \(C^2\) boundary point and an exact
  lift over proper cone factors of dimension at most \(d\geq3\), all
  definable in one o-minimal structure, minimal-face reduction and the
  universal curvature theorem force
  \(q\geq\lceil(N-1)/(d-2)\rceil\) operational non-ray factors. Taking a
  two-dimensional interior section of each such factor, while retaining
  all operational ray factors, gives an orthant section and forces every
  possibly coupled ambient LHSC barrier to satisfy
  \[
    \nu\geq2q+r\geq2\left\lceil{N-1\over d-2}\right\rceil,
    \qquad
    T\geq{\sqrt{\lceil(N-1)/(d-2)\rceil}
                 \log(\Delta_0/\epsilon)
            \over m\log(1/(1-\rho))}.
  \]
  This arbitrary-cone result needs only the single generic contact supplied
  by definable stratification, not globally smooth factor sheets; it still
  assumes reduced strict feasibility and the primal--dual product metric.
  Restriction of the canonical homogenized \(k\)-ball product to one
  diameter per factor is the \((k+1)\)-dimensional \(\ell_\infty\) cone;
  Hildebrand's sharp theorem forces \(\nu\geq k+1\) for every such
  barrier. This proves the desired
  \(\Omega(\sqrt{k}\log(\Delta_0/\epsilon))\) law independently of the
  barrier in the **primal--dual product metric**, even if intermediate
  iterates violate the affine equations. Combining the same theorem with
  this ledger's exact formulation parameters gives two further
  barrier-independent transfers. For a globally primal-and-dual \(C^1\)
  capped Lorentz lift of \((B_2^s)^k\), put
  \[
   h_d=\begin{cases}
    \lceil s/(d-2)\rceil,&3\leq d<s+1,\\
    1,&d\geq s+1.
   \end{cases}
  \]
  Its facially reduced operational product has intrinsic ambient
  LHSC parameter at least \(2kh_d\), so the coefficient becomes
  \(\sqrt{kh_d}\). For a globally primal-and-dual \(C^1\) real-PSD lift
  of \(B_2^N\), \(N\geq3\), with operational orders at most
  \(R_{\rm cap}\), the
  strict curvature theorem and the product-cone rank identity give
  \(\nu\geq V_{R_{\rm cap}}(N)\), hence coefficient
  \(\sqrt{V_{R_{\rm cap}}(N)/2}\); here
  \(V_{R_{\rm cap}}\) is the exact integer rank-budget envelope in the
  [PSD ledger](2026-09-04-psd-order-cap-qipm-ledger.md). The \(N=3\)
  statement uses the separate \(\mathbb S_+^3\)-saturation exclusion.
  For \(N=2\), the strict extra unit is false and the valid value is
  \(V_{R_{\rm cap}}(1)=2\). These are ambient primal--dual results and do not turn
  the much smaller parameters of fixed-scale restricted barriers into
  ambient lower bounds. They require strict feasibility after facial
  reduction. The theorem does not project to a parameter-only primal
  statement. A hostile-audited pointwise Hessian
  countermodel shows that active-facet Dikin containment, determinant
  growth, and the gradient-parameter inequality alone lose the
  \(\sqrt{k}\) factor. The new [exact primal--dual speed-splitting
  theorem](2026-09-04-primal-dual-speed-splitting-product-ball-counterexample.md)
  gives the global obstruction: along every LHSCB central path the primal
  and dual squared speeds are orthogonal projection energies summing to
  \(\nu\). For the optimal barrier on \(\mathcal H_{k,s}\), a weighted
  support objective has primal energy
  \(\sum_a[1-(1+(\eta w_a)^2)^{-1/2}]\). One visible factor gives only
  \(O(\log(1/\epsilon))\) primal length while the dual component carries
  \(\Theta(\sqrt{k}\log(1/\epsilon))\); making every other weight positive
  but below the target scale preserves the separation with a unique
  product-vertex optimizer. Thus a refined all-barrier primal theorem would
  need quantitative objective nondegeneracy, such as a precision-dependent
  exposed-factor count or support scale; that version remains open. For the
  explicit optimal \(\mathcal H_{k,s}\) barrier, the same audited note gives
  the matching positive ledger
  \[
    L_{\rm P}\asymp
    \int\sqrt{\sum_a\min\{(\eta w_a)^2,1\}}\,d\log\eta.
  \]
  If the weights after the largest \(m\) have total mass at most
  \(\epsilon/2\), an \(\epsilon\)-objective-accurate center is reachable by
  \(O_R(\sqrt m[1+\log(m/\epsilon)])\) feasible primal \(R\)-Dikin chords,
  independent of \(k\). If instead their \(\ell_2\) norm is at most
  \(\epsilon\sqrt m/(k+1)\), the same primal movement scale, with
  \(\log((k+1)/\epsilon)\), reaches a central point of full ambient gap
  \(\epsilon\); the dual projection carries the complementary energy.
  Geometric weights \(w_a=2^{-(a-1)}\) give the tight explicit path length
  \(\Theta(\log^{3/2}(1/\epsilon))\) once
  \(k\gtrsim\log(1/\epsilon)\). These are movement results for a closed-form
  support-objective family, not general runtime or query bounds.
  This is not an oracle-query bound and requires a feasible primal--dual
  output; primal-only, state, SQ, and scalar-output contracts remain
  outside its scope.
- The independently audited [dimension-only arbitrary-cone
  theorem](2026-09-04-dimension-only-arbitrary-cone-primal-dual-movement.md)
  removes even the curvature and definability hypotheses. For any
  full-dimensional compact \(C\subset\mathbb R^D\) with an exact lift over
  arbitrary proper operational cone factors of dimension at most
  \(d\geq2\), ordinary slack rank gives \(D+1\leq r+dq\), while an interior
  orthant section forces every possibly coupled LHSC barrier to satisfy
  \[
   \nu\geq r+2q\geq
   \Psi_d(D+1),\qquad
   \Psi_d(h)=2\lfloor h/d\rfloor+\min\{h\bmod d,2\}.
  \]
  The residual-sensitive formula is exact for this dimension ledger,
  including \(d=2\). Therefore every primal--dual trajectory in the
  preceding bounded-Dikin model obeys
  \[
   T\geq{\sqrt{\Psi_d(D+1)/2}\log(\Delta_0/\epsilon)
           \over m\log(1/(1-R))}.
  \]
  In particular, for \(\prod_a B_2^{s_a}\) this is
  \(\Omega_{R,m}(\sqrt{(1+\sum_a s_a)/d}\log(\Delta_0/\epsilon))\)
  against every bounded-\(d\) proper-cone dictionary. The theorem needs
  reduced strict feasibility and a certified primal--dual endpoint; it is
  not a query, long-step, primal-only, state-output, or scalar-output lower
  bound.
- The independently audited [one sharing-cone disk
  synthesis](2026-09-04-one-sharing-cone-disk-qipm-separation.md) places
  the sparse query hierarchy and the arbitrary-barrier movement theorem
  on one nonsymmetric factor
  \[
   \mathcal H_{N,2}
    =\{(\tau,z_1,\ldots,z_N):\|z_i\|_2\leq\tau\}.
  \]
  The objective is public and every hidden bit lies in one disjoint
  two-sparse equality \(y_i=(-1)^{b_i}x_i\); all row norms, singular
  values, column degrees, and SQ sampling probabilities are public. The
  explicit optimal ambient barrier has \(\nu=N+1\), while fixing
  \(\tau=1\) gives exactly the standard product-disk barrier of parameter
  \(N\). For this explicit barrier, the equality-eliminated central Newton
  system is diagonal with condition at most four, and normalized projected
  optimizer, checkpoint-central, and predictor-Newton states need \(O(1)\)
  canonical equality-sign queries. Nevertheless a constant-accuracy
  optimum value, finite-checkpoint scalar, or sufficiently accurate
  explicit projected output needs \(\Theta(N)\) quantum and randomized
  queries. Independently, **every** ambient LHSC barrier on the same cone
  forces
  \[
   T\geq{\sqrt{(N+1)/2}\log(\Delta_0/\epsilon)
        \over m\log(1/(1-R))}
  \]
  bounded product-Dikin rounds from an exact central point of gap
  \(\Delta_0\) to a strictly feasible primal--dual \(\epsilon\)-gap
  output. At the public multiplier \(2\sqrt5\), this is
  \(\Omega_{R,m}(\sqrt N\log(N/\epsilon))\). The easy-state claim is only
  for the explicit barrier and projected variables; it is not asserted
  for arbitrary barriers or a full primal--dual state. Query and movement
  costs are simultaneous maximum-type obstructions and are never
  multiplied.
- [Private curvature closes every nondivisible PSD product-ball
  cap](2026-09-04-psd-product-ball-private-curvature-frontier.md)
  strengthens the preceding standard-slice lower bound source by source.
  If \(d_{ia}\) is the private kernel dimension assigned by PSD block \(i\)
  to source ball \(a\), then the full rank of that source's contact metric
  gives
  \[
      s-1\leq\sum_i p_i d_{ia}
          \leq(R-1)\sum_i d_{ia}.
  \]
  The private subspaces are jointly independent inside each primal kernel,
  so their dimensions add into total boundary nullity.  Divisibility
  equality is excluded by the injective projective support-map argument.
  Consequently
  \[
    \nu_{\rm std,slice}\geq
      b\left\lceil{s-1\over R-1}\right\rceil+
      {\bf1}_{(R-1)\mid(s-1)}.
  \]
  This exactly matches the grouped Schur upper bound
  \(b\lceil s/(R-1)\rceil\) whenever
  \((R-1)\nmid(s-1)\).  The twice-audited companion
  [divisible-cap top-class
  theorem](2026-09-04-psd-product-ball-divisible-topclass.md) closes the
  divisible case \(s-1=q(R-1)\) as well whenever \(q\geq2\), without a
  constant-rank assumption:
  \[
       \nu_{\rm std,slice}^{\min}=b(q+1).
  \]
  Its key device takes closures of the possibly nonclosed saturated-label
  loci; continuous full-rank/zero curvature limits make distinct label
  closures disjoint, and top-eigenline spectral projectors then support
  the relative top-class contradiction.  The all-field sequential theorem
  below now supersedes these staged closures: it also closes the last real
  one-channel switching case \(s=R\geq3\) at the exact value \(2b\), without
  a persistent matching or canonical positive split.  All barrier claims
  retain the globally bi-\(C^1\), restricted-standard-logdet scope.
- [The Hermitian private-nullity
  law](2026-09-04-hermitian-product-ball-private-nullity.md) isolates and
  extends the pointwise part of PSD column packing.  For labelled
  differentiable full-slack factors over any fixed
  \(H_+(\mathbb R),H_+(\mathbb C)\), or \(H_+(\mathbb H)\) product, every
  simultaneous extreme of \(h\) source balls satisfies
  \[
                       \sum_i\operatorname{nullity}_{\mathbb F}X_i\geq h.
  \]
  Under a uniform order cap \(R\), with
  \(a=\dim_{\mathbb R}\mathbb F\), the independently audited sourcewise
  refinement is
  \[
    \nu_{\rm std,slice}\geq
      \sum_a\left\lceil{s_a-1\over a(R-1)}\right\rceil,
  \]
  and the same sourcewise ceiling sum lower-bounds the rank of every
  positive weighted simultaneous-contact dual exposing slack.  For genuine
  affine-slice certificates, the exposed-rank Dikin theorem therefore gives
  the square root of this sum as a path-independent
  \(\log(1/\epsilon)\) distance coefficient.  Grouped Hermitian Schur
  blocks give
  \(\sum_a\lceil s_a/[a(R-1)]\rceil\).  The two ledgers differ only at
  divisible sources; a simultaneous additive closure of those gaps is not
  claimed.
  Cylindrical complementarity makes each row's mixed curvature use a
  private quotient of the primal kernel, and those private subspaces are
  jointly independent.  One order-\((p+h)\) Hermitian Schur block, with
  \(p=\max_a\lceil s_a/\dim_{\mathbb R}\mathbb F\rceil\), serves every
  row and attains both total nullity and exact restricted standard-barrier
  parameter \(h\).  Bounded-fiber partial minimization strengthens this:
  the same value \(h\) is optimal over every nondegenerate coupled
  self-concordant barrier on the fixed one-block slice, uniformly over all
  three fields.  The theorem and construction are independently
  hostile-audited.  They permit factor sharing but prove that neither
  productive nullity nor the intrinsic barrier parameter can fall below the
  number of source rows.
- The independently audited [Hermitian sequential contact-range
  frontier](2026-09-04-hermitian-sequential-contact-range-frontier.md)
  closes the additive theorem over all three fields, including every real
  switching residue. Fix \(\mathbb F\in\{\mathbb R,\mathbb C,\mathbb H\}\),
  let \(\delta=\dim_{\mathbb R}\mathbb F\), impose order cap \(R\), and put
  \(B=\delta(R-1)\). Define
  \[
   \kappa_{\mathbb F,R}(s)=
   \begin{cases}
    1,&R=2,\ s=\delta+1,\\
    \lceil s/B\rceil,&\text{otherwise}.
   \end{cases}
  \]
  For every finite globally bi-\(C^1\) full row factorization of
  \(\prod_aB_2^{s_a}\), a sequential quotient-compression argument selects
  one simultaneous contact at which, for every positive row weighting,
  the aggregate dual rank and primal nullity are at least
  \(\sum_a\kappa_{\mathbb F,R}(s_a)\). This bare factorization theorem
  permits arbitrary label and rank switching. With genuine affine-slice
  dual certificates it gives a path-independent exposed-rank distance
  coefficient \(\sqrt{\sum_a\kappa_{\mathbb F,R}(s_a)}\); with common
  relative-Slater boundary closure it gives the exact restricted standard
  barrier frontier
  \[
        \nu_{\rm std,slice}^{\min}
        =\sum_a\kappa_{\mathbb F,R}(s_a).
  \]
  Grouped Hermitian Schur blocks and the exceptional direct trace-one
  \(H_+^2(\mathbb F)\cong Q_{\delta+2}\) slices attain it. The companion
  [projective/top-class proof](2026-09-04-hermitian-product-ball-standard-additive-frontier.md)
  records the earlier complex/quaternionic argument, while the sequential
  theorem is now canonical.
- The independently audited [intrinsic affine-PSD sequential
  theorem](2026-09-04-affine-psd-sequential-compression-without-selections.md)
  removes the smooth-selection hypothesis completely in the last critical
  real case.  Every finite affine real-PSD lift of \((B_2^s)^b\),
  \(s\geq3\), with block orders at most \(s\), has a simultaneous contact
  and genuine pure-row dual certificates whose every positive weighted sum
  has rank at least \(2b\); at that contact **every** lift fiber has total
  nullity at least \(2b\).  Hence the exposed-rank theorem gives a
  selection-free path-independent standard-logdet metric coefficient
  \(\sqrt{2b}\), and
  the unrestricted affine-lift standard-slice frontier is exactly
  \(\nu_{\rm std,slice}=2b\).  The one-ball engine uses the entire compact
  convex dual-certificate fiber: unless it already contains a total-rank-two
  certificate, convexity and Slater normalization make it a unique continuous
  rank-one branch, whose range would embed
  \(S^{s-1}\) in \(\mathbb {RP}^{r-1}\), \(r\leq s\), contradicting
  dimension theory and invariance of domain.  Sequential compression of
  the **global** certificate fibers preserves the pure-row identity on the
  whole future cylinder, and compressed rank is exactly the new range
  dimension.  Higher-rank certificate fibers obey an intrinsic span bound,
  but the span correspondence need not yet be continuous or injective.
  Norm trees test the seam sharply.  A binary \(\mathbb S_+^2\) chain for
  \(B_2^s\) has a **unique** support certificate of rank at most \(s-1\)
  everywhere, disproving a blanket selection-free promotion of the smooth
  exposed-rank value \(s\).  Complex/quaternionic two-block trees for
  \(B_2^5\) and \(B_2^9\) gain primal vertex nullity at their nonsmooth
  seams, but the rotated-perspective construction below shows that this is
  not a universal every-fiber phenomenon.  The full compact certificate
  incidence projects properly onto the support sphere with convex fibers;
  Vietoris--Begle therefore preserves the sphere's Čech cohomology without
  any selector.  Classifying this incidence under higher-rank saturation is
  the current route to a Hermitian extension.
- The independently audited [exact selection-free PSD2 exposed-rank
  theorem](2026-09-04-selection-free-psd2-product-ball-exposed-rank.md)
  determines the obstruction left by those seams.  For arbitrary finite
  affine lifts of \(\prod_dB_2^{s_d}\) over real \(2\times2\) PSD blocks and rays,
  the exact minimax rank of a positive aggregate of genuine row-support
  certificates is
  \[
                         \sum_d(s_d-1).
  \]
  A semialgebraic minimum-rank selection on one generic contact stratum
  gives each one-ball lower bound \(s_d-1\); compression of the original global
  certificate fibers makes these ranks add across source rows.  Separate
  binary norm chains attain the bound and have unique support certificates.
  This is exactly one rank unit per source below the globally bi-\(C^1\)
  value \(\sum_ds_d\), proving that unique continuous semialgebraic fibers and
  generic analyticity do not recover the smooth theorem.  At the selected
  simultaneous contact every primal fiber nevertheless has nullity at least
  \(\sum_d(s_d-1)\).  The rotated-perspective counterexample below shows
  that no additional nullity unit can be forced in every completion; the
  exact unrestricted standard-barrier parameter remains a different open
  question.
- The independently audited [selection-free arbitrary-cap Lorentz
  theorem](2026-09-04-selection-free-exposed-rank-premium-counterexample.md)
  gives the exact one-ball law behind this phenomenon.  If every Lorentz
  factor has dimension at most \(d\), then over all finite affine lifts of
  \(B_2^s\)
  \[
    \inf_{\mathcal L}\max_{v\in S^{s-1}}
       \min_{Z\in\mathcal D_{\mathcal L}(v)}\operatorname{rank}_J Z
       =\left\lceil {s-1\over d-2}\right\rceil.
  \]
  The lower bound is the generic semialgebraic mixed-curvature rank; a
  grouped nested Lorentz chain has a unique certificate at every support
  and attains it.  Both its unique primal boundary fiber and unique dual
  certificate are globally Lipschitz and semialgebraic, so even
  bi-Lipschitz selections and almost-everywhere \(C^1\) regularity do not
  recover the smooth premium.  Its restricted standard product barrier has exact
  parameter \(2\lceil(s-1)/(d-2)\rceil-1\), exposing a genuine separation
  between pointwise dual rank and seam-sensitive barrier complexity.  The
  selection-free exposed-rank value is one below the globally bi-\(C^1\)
  value exactly when \(d<s+1\) and \(d-2\mid s-1\).  For shared-factor
  heterogeneous products, sequential compression and independent chains
  give the exact favorable-aggregate minimax
  \(\sum_a\lceil(s_a-1)/(d-2)\rceil\).  This does not assert additivity of
  the minimum rank in the aggregate certificate fiber.  At the hard
  one-ball support every exposing slack has rank at least the displayed
  ceiling, so the exposed-rank theorem gives the path-independent standard-
  logdet metric lower
  \(\sqrt{\lceil(s-1)/(d-2)\rceil}\log(1/\epsilon)-O(1)\), with its
  formulation-dependent reference constant.  This is a movement theorem,
  not an unrestricted QIPM iteration lower bound.
- The independently audited [exact selection-free Hermitian exposed-rank
  theorem](2026-09-04-selection-free-hermitian-exposed-rank-frontier.md)
  extends that minimax law to every real, complex, and quaternionic order
  cap.  With \(a=\dim_{\mathbb R}\mathbb F\) and \(R\geq2\),
  \[
   \inf_{\mathcal L}\max_{v\in S^{s-1}}
    \min_{Y\in\mathcal D_{\mathcal L}(v)}
       \operatorname{rank}_{\mathbb F}Y
    =\left\lceil{s-1\over a(R-1)}\right\rceil .
  \]
  More strongly, every fixed lift obeys this rank lower bound on a dense
  open semialgebraic, full-measure set of supports, and the rotated
  perspective attains equality away from one pole.  Hence the
  infimum-over-lifts essential infimum over supports is also exactly
  \(q=\lceil(s-1)/[a(R-1)]\rceil\), not merely a worst-support value.
  A rotated Hermitian perspective
  \(X_G=\left(\begin{smallmatrix}1-b&w_G^*\\
  w_G&z_GI\end{smallmatrix}\right)\), \(\sum_Gz_G=1+b\),
  attains the upper bound with explicit rank-one Gram certificates in
  every group, including zero-coordinate and pole cases.  The formula
  extends to a repeatable mixed Hermitian dictionary by replacing the
  denominator with its largest block capacity.  Sequential compression
  of the original pure-row certificate fibers gives the additive
  shared-product **existence** and every-final-fiber nullity lower
  \(\sum_d\lceil(s_d-1)/[a(R-1)]\rceil\).  It does not assert a
  minimum-rank theorem for the full aggregate-objective certificate
  fiber.  For every formulation, some support objective therefore forces
  the path-independent restricted-standard-logdet distance
  \[
      d_F\geq
      \bigl[\sqrt q\log(1/\epsilon)-C_{\mathcal L,X^c,S}\bigr]_+,
  \]
  where the finite constant depends on the fixed formulation, interior
  reference, and chosen support certificate; the hard support, accuracy
  scale, and warm-start distance are not uniform over lifts.  If a counted round contains
  at most \(m\) forward Dikin chords of radius \(\theta<1\), and the start
  lies within reference radius \(\rho<1\), the exact lower denominator is
  \(m\log(1/(1-\theta))\), with the additive start penalty
  \(\log(1/(1-\rho))\).  Thus fixed-model bounded-Dikin methods need
  \(\Omega(\sqrt q\log(1/\epsilon))\) outer rounds on a
  formulation-dependent hard support, asymptotically below its fixed
  accuracy scale.  The perspective construction matches the \(\sqrt q\)
  coefficient only for one objective-specific intrinsic distance, not as
  a central-path algorithm.  For the actual minimax upper, the grouped
  Hermitian Schur lift has exact parameter
  \(g=\kappa_{\mathbb F,R}(s)\leq q+1\leq2q\), so a standard short-step
  schedule handles every support in
  \(O_\theta(\sqrt q\log(q/\epsilon))\) rounds.  Thus, with the lift and
  start fixed before \(\epsilon\downarrow0\), the infimum-over-lifts,
  supremum-over-supports asymptotic bounded-Dikin coefficient is
  \(\Theta_\theta(\sqrt q)\), with constants independent of \(R\) when
  the problem parameters and lift are fixed before accuracy tends to zero.
  This movement lower bound is not a query lower bound and is not
  multiplied by an independent query obstruction.
- The independently audited [same-instance Hermitian exposed-rank
  query/readout boundary](2026-09-04-hermitian-exposed-rank-query-readout-boundary.md)
  makes the access distinction exact on the grouped perspective lift.  In
  the divisible case \(s-1=q\,a(R-1)\), balanced hidden-sign support
  objectives force certificate rank \(q\) and have the uniform
  exposed-minor scale \(\Delta=1\).  From the displayed public Slater point,
  every forward \(\theta\)-Dikin sequence in the restricted standard-logdet
  metric therefore uses at least
  \(\sqrt q\log(1/\epsilon)/[-\log(1-\theta)]\) chords.  Nevertheless, one
  clean phase query prepares the normalized projected optimizer state, and
  the symmetry-reduced lifted optimizer and standard-barrier central states
  have the same one-query sign pattern when preparation of their public
  magnitude states is charged separately.  The scalar optimum is public,
  whereas, for every fixed \(\epsilon<1/8\), a full classical feasible
  \(\epsilon\)-optimal projected solution, or an explicit lifted solution,
  with success at least \(2/3\) costs \(\Theta_\epsilon(s-1)\) quantum or
  randomized raw sign queries.
  The lower bound uses the degree-\(T\) Fourier-span dimension
  \(\sum_{j\leq T}\binom{s-1}{j}\), Holevo information, and binary
  rate distortion; at \(\epsilon<1/[8(s-1)]\), the stronger pointwise
  statement recovers every sign and parity.  These are simultaneous,
  maximum-type obstructions, never a product.

  The same note also identifies the sharp formulation boundary:
  \[
    \inf_{\mathcal L}\sup_v r_{\mathcal L}(v)=q,
    \qquad
    \sup_v\inf_{\mathcal L}r_{\mathcal L}(v)=1.
  \]
  A formulation fixed before seeing the objective has a hard balanced-sign
  family.  If an objective-dependent projection is allowed, a rotation
  sends any chosen support to the rank-one north pole.  On this family the
  rotation itself has an implicit coherent implementation using one sign
  query per application, but an explicit classical matrix description
  costs \(\Theta(s-1)\) queries.  Thus exposed-rank geometry alone cannot
  yield a formulation-independent raw-query lower bound for state or scalar
  output; compilation and output access must be charged explicitly.  The
  movement claim remains a fixed restricted-standard-barrier theorem, not
  an unrestricted or arbitrary-barrier QIPM lower bound.
- The closure-checked
  [all-symmetric-cone query/readout
  companion](2026-09-04-symmetric-cone-exposed-rank-query-readout-boundary.md)
  extends this same-instance boundary to every simple EJA dictionary,
  including spin and Albert factors.  In the divisible case
  \(s-1=qB\), \(q\ge2\), balanced signs in \(q\) full half-Peirce groups
  give exact certificate rank \(q\) and exact exposed-minor scale
  \(\Delta=1\).  The movement lower is therefore
  \(\sqrt q\log(1/\epsilon)/[-\log(1-\theta)]\).  One clean sign query
  prepares the normalized projected optimizer and the hidden-sign part of
  structured lifted/central real-coordinate states once their public
  magnitudes are charged, whereas every explicit classical feasible
  \(\epsilon\)-optimal vector costs
  \(\Theta_\epsilon(s-1)\) raw queries for fixed
  \(0<\epsilon<1/8\).  The Albert statement encodes its 27 real EJA
  coordinates in ordinary complex amplitudes; it assumes neither
  octonionic amplitudes nor free Jordan arithmetic.  The same quantifier
  obstruction persists: an objective-dependent projection rotation sends
  a fixed support to a rank-one pole.  This theorem passed both a complete
  closure check and an independent hostile audit, including the Albert
  normalization, state contract, and Fourier--Holevo--rate-distortion
  proof.  Its novelty label remains conservative.  Movement and readout
  are MAX-type statements.
- The new [all-symmetric-cone exposed-rank
  theorem](2026-09-04-selection-free-symmetric-cone-exposed-rank-frontier.md)
  subsumes the Lorentz and Hermitian minimax laws and closes the exceptional
  case.  For a repeatable dictionary of simple symmetric cones, let
  \(B=\max_i a_i(r_i-1)\).  Then
  \[
   \inf_{\mathcal L}\max_{v\in S^{s-1}}
    \min_{Y\in\mathcal D_{\mathcal L}(v)}
       \sum_i\operatorname{rank}_JY_i
      =\left\lceil{s-1\over B}\right\rceil .
  \]
  The lower bound is the generic selection-free mixed-Peirce rank inequality.
  The upper bound uses a universal Peirce perspective
  \(X=(1-b)c+\sqrt2w+z(e-c)\), whose determinant is
  \(z^{r-2}((1-b)z-\|w\|^2)\), together with an explicit rank-one completion
  \(AP(c-g/(\sqrt2A))c\).  These identities use only rank-two Peirce calculus
  and therefore include \(H_+^3(\mathbb O)\), where \(B=16\).  Sequential
  support compression yields the additive favorable-certificate law
  \(\sum_a\lceil(s_a-1)/B\rceil\) for heterogeneous products.  Every fixed
  formulation has a hard support with standard-Jordan metric movement
  coefficient at least
  \(\sqrt{\lceil(s-1)/B\rceil}\); the reference-minor scale remains
  formulation dependent.  The same lower coefficient holds for every
  classified self-scaled product barrier, since its block weights satisfy
  \(\alpha_i\geq1\); arbitrary coupled/custom barriers remain outside the
  theorem.  This is an exposed-rank and bounded-movement result, not a
  standard-barrier-parameter, query, or runtime lower bound.
  A second, fixed-tail Peirce lift groups all \(s\) coordinates into
  \(g=\lceil s/B\rceil\) blocks and has restricted standard barrier
  \(-\sum_G\log(t_G-\|w_G\|^2)\) of parameter at most \(g\).  Since
  \(q=\lceil(s-1)/B\rceil\leq g\leq q+1\leq2q\), this matches the hard
  lower asymptotically: over fixed lifts and starts, the minimax number of
  forward \(\theta\)-Dikin chords per \(\log(1/\epsilon)\) is
  \(\Theta_\theta(\sqrt q)\), uniformly in the symmetric-cone rank and
  type.  The dictionary and ball dimension are fixed before
  \(\epsilon\downarrow0\).  The same two bounds determine the exact
  optimal restricted standard-barrier parameter off the divisible seam:
  every lift has \(\nu_{\rm std,slice}\geq q\), the fixed-tail lift has
  parameter at most \(g\), and therefore
  \(\inf_{\mathcal L}\nu_{\rm std,slice}=q\) whenever
  \(B\nmid(s-1)\).  Nondivisible heterogeneous products add exactly;
  remaining divisible cases with \(q\geq2\) lie in the one-unit interval
  \([q,q+1]\).  At \(q=1\), the separate one-channel rigidity theorem gives
  exact value one for a matching spin factor and two otherwise, additively
  across critical sources.
- The audited [selection-free PSD2 nullity-seam
  reduction](2026-09-04-selection-free-psd2-nullity-seam-obstruction.md)
  explains why the proposed every-fiber \(+1\) fails.  The span of
  the full dual certificate fiber lies in the kernel of **every** primal
  lift, and its dimension is generically \(s-1\).  But saturation gives only
  a semialgebraic phase incidence, not an unbranched cover: algebraic
  branched maps \(T^2\to S^2\) show that phase topology alone cannot close
  the gap.  The later construction realizes the required fiber-valued seam.
- The independently audited [rotated-Lorentz perspective
  counterexample](2026-09-04-rotated-lorentz-fiberwise-nullity-counterexample.md)
  makes the separation exact for every ball dimension and Lorentz cap.
  With \(q=\lceil(s-1)/(d-2)\rceil\), it is a compact full-Slater affine
  lift in which every boundary fiber contains a tuple of nullity exactly
  \(q\), and every support-certificate fiber has maximum rank exactly
  \(q\).  At one pole the primal fiber is a simplex: its all-positive point
  has nullity \(q\), while its vertices have nullity \(2q-1\).  Consequently
  the restricted standard product barrier has exact parameter \(2q-1\),
  although the pole-objective central path has leading metric coefficient
  only \(\sqrt q\).  This simultaneously refutes the every-fiber premium
  and shows why global barrier parameter, objective-specific exposed rank,
  and central-path movement cannot be substituted for one another.
  Independent copies give the exact heterogeneous product values
  \(\sum_aq_a\), \(\sum_aq_a\), and \(\sum_a(2q_a-1)\) for minimum
  simultaneous fiber nullity, maximum positive-aggregate certificate rank,
  and restricted standard parameter, while the simultaneous pole central
  coefficient is \(\sqrt{\sum_aq_a}\).
- The independently audited [selection-free Lorentz standard-barrier cap
  theorem](2026-09-04-selection-free-lorentz-standard-barrier-cap.md)
  proves the exact unrestricted affine-lift value
  \(\lceil s/(d-2)\rceil\) in every nondivisible cap case.  The generic
  curvature bound gives \(\nu_{\rm std,slice}\geq
  \lceil(s-1)/(d-2)\rceil\); these ceilings agree unless
  \(d-2\mid s-1\).  In the divisible case, a two-scale determinant lemma
  shows that any nonzero recession direction contributes its Jordan rank
  in addition to compressed boundary nullity, so every unbounded lift pays
  the missing unit.  At that stage only bounded projection-singular
  branching remained open; the wide-cap theorem below now closes part of
  it.  Moreover, any non-singleton compact fiber of minimum nullity
  \(r\) contains an endpoint of nullity at least \(r+1\); hence a
  hypothetical low-parameter bounded escape must first drop its seam
  minimum below the generic value before gluing the branches.  For a
  factor-count-minimal divisible lift through exactly \(q\) copies of
  \(Q_d\), a saturated tuple with \(z\) zero blocks must obey
  \(z(d-2)\leq q-1\), and the full-dual-rank-drop set has codimension at
  least \(d-2\).  Its homogenized projection kernel must have dimension
  \(1\leq k\leq q-1\).  At \(k=q-1\) and \(d-2\geq q-1\), one block must
  see a genuinely multidimensional normal space; otherwise the cone is a
  common-height product of balls and the forbidden product-sphere
  injection returns.  These audited span and stratum bounds sharply
  confine the possible label-switching set.  The later wide-cap theorem
  below eliminates it whenever \(d-2\ge q-1\); only the narrow-cap range
  \(d-2\le q-2\) remains open.
- The independently audited
  [arbitrary-factor wide-cap Lorentz rigidity
  theorem](2026-09-04-arbitrary-factor-q2-lorentz-barrier-rigidity.md)
  closes the bounded divisible seam whenever
  \[
       s-1=q(d-2),\qquad d-2\ge q-1,\qquad q\ge2,
  \]
  even with arbitrarily many extra Lorentz blocks of dimension at most
  \(d\) and arbitrary ray factors.  Every such bounded full-Slater affine
  lift has
  \[
                    \nu_{\rm std,slice}\ge q+1,
  \]
  and the grouped norm-chain construction attains equality.  The proof is
  factor-count independent: universal face codimension and the hypothetical
  determinant order \(q\) force every boundary tuple to have nullity exactly
  \(q\); compact fibers are therefore continuous singletons; finitely many
  generic active-label closures cannot switch; and a fixed active tuple
  would give an impossible injection
  \(S^{q(d-2)}\to(S^{d-2})^q\).  In particular, it closes every
  quotient-two case with arbitrary extra factors.  Combined with the
  recession theorem, this settles all affine lifts in the wide-cap range.
  The remaining bounded divisible Lorentz regime is precisely
  \(d-2\le q-2\), where lower-nullity positive-dimensional singular fibers
  are not excluded.  This is a restricted standard-product-barrier
  theorem, not an arbitrary-barrier or query lower bound.
- The independently audited [two-factor compact rigidity
  theorem](2026-09-04-two-lorentz-factor-compact-ball-barrier-rigidity.md)
  closes the bounded quotient-two seam for factor-count-minimal lifts in
  every cap.  If \(s-1=2(d-2)\), every bounded full-Slater exact lift of
  \(B_2^s\) through exactly \(Q_d\times Q_d\) has
  \(\nu_{\rm std,slice}\geq3\), and the two-level norm chain attains three.
  Homogenization leaves only one possible span dimension; its definite
  hyperplane case would inject \(S^{2(d-2)}\) into
  \(S^{d-2}\times S^{d-2}\), while every other case forces a boundary
  tuple of determinant order three.  A separate compact affine seam of
  exact parameter two shows that local compact-fiber geometry alone is
  insufficient.  The later arbitrary-factor theorem above rules out those
  extra-factor/global-switching escapes as well, so this two-factor result
  is now a sharper structural precursor rather than the final
  quotient-two frontier.
- The independently audited [selection-free Hermitian standard-barrier cap
  theorem](2026-09-04-selection-free-hermitian-standard-barrier-cap.md)
  extends that reduction to real, complex, and quaternionic Hermitian PSD
  products.  With \(a=\dim_{\mathbb R}\mathbb F\), order cap \(R\geq2\),
  \(B=a(R-1)\), and \(q=\lceil(s-1)/B\rceil\), every finite affine lift of
  \(B_2^s\) satisfies

  \[
                \nu_{\rm std,slice}\geq q.
  \]

  This exactly matches the grouped Hermitian Schur construction whenever
  \(B\nmid s-1\), as well as the direct rank-two spin cases.  The audited
  [one-channel theorem](2026-09-04-selection-free-hermitian-one-channel-rigidity.md)
  now closes every non-spin \(q=1\) divisible case at two.  If a
  parameter-one lift existed, every boundary certificate fiber would be a
  singleton rank-one ray, producing an embedding
  \(S^{a(R-1)}\hookrightarrow\mathbb FP^{R-1}\); invariance of domain and
  projective-space cohomology leave exactly the direct \(R=2\) spin
  spheres.  Compression of the original pure-row certificate fibers makes
  this additive: for \((B_2^s)^b\) in any non-spin one-channel regime,
  one simultaneous contact has every positive aggregate certificate rank
  and every primal-fiber nullity at least \(2b\), so the exact unrestricted
  standard-slice value is \(2b\).  The same statement holds for repeatable
  mixed Hermitian dictionaries without a matching direct spin face.  In
  every other divisible case, the Peirce--Schur two-scale
  recession formula proves the grouped \(q+1\) value for every unbounded
  lift.  The wide-cap theorem below also closes the bounded branch whenever
  \(B\geq q-1\).  Thus the only unresolved fixed-type Hermitian
  standard-barrier branch is bounded, projection-singular, divisible, and
  has \(q\geq B+2\).
  This is a restricted standard-logdet result, not a lower bound for
  arbitrary barriers or unrestricted QIPM iterations.
- The independently audited
  [arbitrary-factor wide-cap Hermitian rigidity
  theorem](2026-09-04-arbitrary-factor-wide-cap-hermitian-barrier-rigidity.md)
  closes every bounded divisible case
  \[
     s-1=qB,\qquad B=a(R-1)\geq q-1,\qquad q\geq2
  \]
  over real, complex, or quaternionic PSD factors of arbitrary finite
  count and orders at most \(R\), together with arbitrary ray factors.
  Every such lift has
  \(\nu_{\rm std,slice}\geq q+1\), and the grouped Hermitian Schur lift
  attains equality.  The factor-count-independent face-codimension budget
  forces constant nullity and singleton boundary fibers under a
  hypothetical smaller parameter.  Active null-line labels then
  globalize, yielding an impossible homeomorphism
  \[
       S^{qB}\cong(\mathbb F P^{R-1})^q,
  \]
  contradicted by mod-two cohomology in degree
  \(a\in\{1,2,4\}\).  Together with the recession theorem, only the
  bounded narrow-cap cases \(q\geq B+2\) remain open.  This concerns the
  restricted standard product log-determinant, not arbitrary barriers or
  quantum query complexity.
- The independently audited [all-symmetric-cone one-channel
  theorem](2026-09-04-selection-free-symmetric-cone-one-channel-rigidity.md)
  classifies the same selection-free equality case for an arbitrary
  repeatable dictionary of simple symmetric cones.  Put
  \(B=\max_i a_i(r_i-1)\) and \(s-1=B\).  The exact restricted standard
  value is one if and only if the dictionary contains the matching spin
  factor \(Q_{B+2}\); otherwise it is two.  Under a hypothetical
  parameter-one lift, every normalized certificate fiber is forced by
  convexity to be a continuous singleton ray.  Its range embeds \(S^B\)
  into the primitive-ray manifold of one factor.  The simple-EJA
  classification gives \(\mathbb RP^{r-1}\), \(\mathbb CP^{r-1}\),
  \(\mathbb HP^{r-1}\), a sphere for spin factors, and
  \(\mathbb OP^2\) for the Albert algebra; only the spin cases are
  spheres.  In particular the Albert critical ball \(B_2^{17}\) needs
  parameter at least two because \(H^8(\mathbb OP^2)\ne0\).
  Sequential Peirce support compression makes the non-spin result
  additive over \(b\) source balls: one simultaneous contact has positive
  aggregate rank and every-final-fiber nullity at least \(2b\), and the
  exact standard value is \(2b\).  This is again an existence theorem for
  selected pure-row certificates, not a minimum-rank claim for the whole
  aggregate fiber. For the corresponding selected aggregate objective,
  the exposed-rank theorem gives the path-independent metric lower bound
  \[
       d_F\geq\sqrt{2b}\log(\Delta_c/\epsilon),
  \]
  and therefore the matching \(\sqrt{2b}\log(1/\epsilon)\) round scale in
  any model with uniformly bounded standard-Dikin movement per round. A
  matching-spin dictionary has the separate direct construction with
  parameter and generic aggregate rank \(b\), hence scale \(\sqrt b\).
  This comparison is barrier-geometric, not an unconditional quantum
  query or runtime lower bound.
- [Hermitian product-ball saturation
  rigidity](2026-09-04-hermitian-product-ball-capacity-rigidity.md) gives
  the exact equality classification for the full row slack, assuming no
  active scalar-ray terms.  If \(n=\sum_a(s_a-1)\), then
  \[
        n\leq\sum_i a_i\left\lfloor r_i^2/4\right\rfloor,
  \]
  and equality makes the joint support map a diffeomorphism from the
  product of source spheres to a product of balanced Hermitian
  Grassmannians.  Fundamental groups and mod-two Schubert squares force
  every block to have order two and the source sphere dimensions to match
  the field dimensions \(1,2,4\) as a multiset.  Outside precisely those
  direct \(Q_3,Q_4,Q_6\) product profiles, integrality strengthens the
  bound to \(n+1\).  The result is independently hostile-audited and
  remains conditional on global \(C^1\) factors and the stated ray scope.
- [Active rays do not enlarge the Hermitian saturation
  profiles](2026-09-04-hermitian-product-ball-active-ray-covering.md).
  For globally labelled \(C^1\) full extreme-row factors, every scalar ray
  has zero mixed-curvature channel at contact.  Capacity equality therefore
  still makes the joint positive-block support map a finite covering.  This
  forces every complex or quaternionic block to have order two and every
  real block to have order at most four.  The complete necessary source
  multiset is obtained from
  \(\mathbb R2\mapsto\{1\}\),
  \(\mathbb R3,\mathbb C2\mapsto\{2\}\),
  \(\mathbb R4\mapsto\{2,2\}\), and
  \(\mathbb H2\mapsto\{4\}\).  The real order-three and order-four
  Grassmannian covers are the only possibilities left by topology alone.
  The independently audited
  [cylinder-integrability theorem](2026-09-04-real-low-order-cylinder-exclusion-product-balls.md)
  excludes both for the full product-ball slack, even with finitely many
  active rays: a fixed-kernel cylinder conflicts with the two rulings of
  \(\operatorname {Gr}_2^+(\mathbb R^4)\), while an order-three block
  reduces to the audited impossible single-\(B_2^3\) factorization.  Thus
  actual saturation forces only order-two \(Q_3,Q_4,Q_6\) profiles.  Any
  forbidden block or failure of this multiset profile
  gives the integer capacity gap
  \(\sum_i a_i\lfloor r_i^2/4\rfloor\geq n+1\).
  The theorem is independently hostile-audited and retains its global
  labelled-selection scope.
- [All-symmetric-cone active-ray
  saturation](2026-09-04-symmetric-cone-product-ball-active-ray-saturation.md)
  extends the preceding classification to arbitrary irreducible symmetric
  cones, including every Lorentz dimension and \(H_3(\mathbb O)_+\).
  Under the same global \(C^1\) full-row hypothesis,
  \[
       \sum_i a_i\lfloor r_i^2/4\rfloor
          =\sum_a(s_a-1)
  \]
  forces exactly one spin factor \(Q_{s_a+1}\) per source ball.  Every
  nonassigned dual row factor of that block vanishes, so positive blocks
  cannot share rows at minimum capacity; finite active rays remain allowed
  but curvature-flat.  The exceptional orbit \(\mathbb OP^2\) is excluded
  by its nonzero mod-two square, and a degreewise determinant matching
  handles odd-sphere mixing without assuming that the support covering
  splits.  Any other profile has the integer one-unit capacity gap.  The
  theorem is independently hostile-audited; a targeted screen found no
  prior statement of this equality/no-sharing result.
- [One-factor PSD packing still forces square-root-many short-step
  rounds](2026-09-04-one-factor-psd-packing-short-step-lower-bound.md)
  turns the packed barrier certificate into an actual algorithmic lower
  bound for a precise path-following class.  For the one-block
  \(H_+^{p+h}(\mathbb F)\) lift of \(h\) balls, the standard restricted
  barrier has exact central-path speed
  \[
                  \beta(\tau)^2
                    =h\left(1-{1\over\sqrt{1+\tau^2}}\right).
  \]
  Any fixed-radius central-tube sequence whose outer round contains at most
  a fixed number of substeps of local norm below one therefore needs
  \(\Omega(\sqrt h\log(\Delta/\epsilon))\) outer rounds.  The proof is
  field-uniform over \(\mathbb R,\mathbb C,\mathbb H\) and independently
  hostile-audited.  It allows arbitrary predictor/corrector directions but
  does not cover long steps, an unbounded number of substeps, other
  barriers, or general QIPMs.
- [Exact Pareto ledger for PSD column
  packing](2026-09-04-psd-column-packing-pareto.md) optimizes the preceding
  construction rather than selecting the heuristic balanced point.  For
  padded row width \(p\), \(H_p=b\lceil s/p\rceil\) columns, and \(\ell\)
  PSD factors, balancing the factor column counts gives the exact tuple
  \[
   \left(L,G,r_{\max},\nu_{\mathrm{slice}},\nu_{\mathrm{ambient}},M\right)
   =\left(\ell,H_p,p+\lceil H_p/\ell\rceil,H_p,
      p\ell+H_p,(\ell-t)d_{p+q}+td_{p+q+1}\right),
  \]
  where \(H_p=q\ell+t\).  Enumerating
  \(\ell\geq\lceil H_p/(R-p)\rceil\) and dominance-pruning is the exact
  finite Pareto frontier of this fixed-width family. The exact number of
  genuinely free affine coordinates is
  \[
        V(p,\ell)=bs+(\ell-t)d_q+td_{q+1}.
  \]
  Unlike the full cone-coordinate ledger \(M\), for every
  \(\theta\geq0\) the proxy \(V\nu^\theta\) is minimized by single-column
  blocks and a largest feasible row width, i.e. the canonical grouped
  Schur point. Under the same raw order cap this PSD Schur point also
  weakly beats grouped Lorentz in \(V\) and restricted parameter because
  it carries \(R-1\), rather than \(R-2\), source coordinates per group;
  Lorentz still wins in full ambient cone dimension. The identity
  \(d_{p+c}=(2p+1)c+(p-c)(p-c+1)/2\) shows that static cone dimension
  favors \(c=p\) or \(p+1\).  There is also a universal joint lower
  envelope: if \(z=\lfloor\nu_{\rm std,slice}\rfloor\), then
  \[
    z\geq b\left\lceil{s\over R-1}\right\rceil,
    \qquad b(s-1)\leq{\cal C}_R(L,z)
      :=\max_{\substack{0\leq c_i\leq R\\\sum c_i\leq z}}
             \sum_i c_i(R-c_i).
  \]
  Discrete concavity evaluates \({\cal C}_R\) exactly by balancing the
  \(c_i\)'s, and its continuous efficient frontier is
  \(b(s-1)\leq Rz-z^2/L\).  In the ceiling-free, cap-active regime,
  \(p=c=R/2\) minimizes factor count, ambient parameter, or cone dimension
  separately.  Multiplying any of them by
  \(\nu_{\mathrm{slice}}^{\theta}\), however, moves the unique optimum to
  \[
             p:c=(1+\theta):1;\qquad
             p:c=3:2\quad\text{for }\theta=1/2.
  \]
  provided the sharp sourcewise constraint on \(z\) is slack; otherwise
  the universal relaxation is source-width limited. More strongly, put
  \(J_\omega=\sum_i r_i^\omega\). Every eligible order-\(R\) PSD lift
  satisfies the formulation-independent family
  \[
   J_\omega\nu^\theta\geq
   {(2+\theta)^{2+\theta}\over(1+\theta)^{1+\theta}}
   {\{b(s-1)\}^{1+\theta}\over R^{2+\theta-\omega}},
   \qquad0\leq\omega\leq2+\theta.
  \]
  Its equality shape is \(p:c=(1+\theta):1\). Divisible packings attain
  the same bound with \(bs\) in place of \(b(s-1)\), so they are
  asymptotically globally optimal for factor-count and ambient-rank
  proxies. The cap inequality
  \(M\geq(1+1/R)J_2/2\) matches the packing's triangular-coordinate
  factor exactly, so the same conclusion holds for cone-coordinate work,
  even at fixed \(R\). The short-step specialization is \(\theta=1/2\),
  hence \(3:2\).
  An exact divisible example shows the \(3:2\) point loses every static
  ledger but wins all three short-step-weighted proxies.  Uncapped direct
  Lorentz lifting still strictly beats every PSD packing in both total
  cone coordinates and restricted parameter; PSD sharing buys factor
  count and, exactly when \(b>s\), can also lower ambient normal parameter.
  Within blockwise Schur lifts, the scalar-coordinate proxy
  \(M\sqrt\nu\) instead has exact optimal group width four (when
  available); packed PSD beats that PSD-only benchmark asymptotically,
  while grouped Lorentz retains the smaller leading constant.
  The theorem and comparison passed a hostile audit.  The weighted
  quantities are formulation proxies, not runtimes: packed Newton
  treewidth, conditioning, access, and output costs remain separate.
- [Aggregate contact rank composes curvature with bounded-Dikin
  movement](2026-09-04-psd-packing-work-iteration-composition.md) gives
  the exact condition under which the preceding proxy becomes total work.
  At one simultaneous contact, the same exposing ranks \(q_i\) obey
  \[
                   b(s-1)\leq\sum_i p_iq_i
  \]
  and force path distance
  \(\sqrt{\sum_iq_i}\log(\Delta/\epsilon)\). Thus a model that explicitly
  charges \(J_\omega=\sum_i r_i^\omega\) fresh work in every bounded-Dikin
  round has the genuine lower frontier
  \[
   {\cal W}_\omega=\Omega\!\left(
      { \{b(s-1)\}^{3/2}\over R^{(5-2\omega)/2}}
      \log{\Delta\over\epsilon}\right),
  \]
  with the sharp constant and \(3:2\) equality shape in the note.
  Divisible packed paths match the resource powers asymptotically. The
  fresh-work premise cannot be dropped in a general QIPM oracle model:
  fixed factor data and KKT rays can be prepared once and reused, so
  one-shot query lower bounds do not tensor over IPM rounds. In fact,
  dense sign objectives make every normalized packed center and predictor
  the same uniform phase state at all path parameters, preparable with one
  phase query per checkpoint independently of \(L\).
- [PSD column packing has an exact Newton forest after auxiliary
  centering](2026-09-04-psd-column-packing-newton-forest.md) resolves that
  Newton-structure question for the explicit packing family.  Hadamard
  equality and AM--GM give the exact packing-independent marginal barrier
  \[
      \bar F(x)=-h\sum_{a=1}^b\log(1-\|x_a\|^2)+bh\log h,
      \qquad h=\lceil s/p\rceil,\qquad \nu(\bar F)=bh.
  \]
  The materialized projected Hessian is generically a disjoint union of
  \(s\)-cliques, but an exact congruence and auxiliary Schur elimination
  produce \(b\) stars plus isolated residual modes, hence rank-expanded
  treewidth one and \(O(bs)\) projected solve work.  This is independent of
  cross-source packing: even the one-\(\mathbb S_+^{s+b}\)-factor lift has
  no cross-ball edge after reduction.  More generally, sparse affine
  constraints add only their incidence hubs, so the exact latent width is
  the augmented constraint-incidence width, not the PSD packing layout.
  Balanced blocks can therefore attain the \(bs/R^2\) factor,
  \(bs\) cone-dimension, and \(bs/R\) barrier scales in the ceiling-free
  regime while keeping linear projected solves.  Conversely, the
  barrier-minimal choice \(p=\min\{s,R-1\},c=1\) minimizes the standard
  short-step reduced-work certificate; factor sharing optimizes a different
  resource.  The conditional quantum state-solve ledger explicitly charges
  conditioning and access, while full lifted direction/iterate
  reconstruction still requires Gram products.  This audited result is not
  a finite-precision theorem, an iteration lower bound, or an end-to-end
  quantum speedup.
- [Packed PSD and grouped Lorentz lifts have identical reduced Newton
  oracles](2026-09-04-psd-lorentz-reduced-oracle-equivalence.md) upgrades
  the forest calculation to an exact end-to-end state-generation
  impossibility theorem under a precise matched interface.  At exact fiber
  centers, the two standard barriers have the same marginal function and
  the same projected KKT matrix and right-hand side.  More strongly, in
  residual coordinates the complete packed PSD system is the grouped
  Lorentz system direct-summed with positive diagonal, zero-right-hand-side
  off-diagonal modes.  Consequently two zero-query-overhead simulations
  give equal quantum and classical query complexity for normalized
  projected Newton states, preserving dimension, block-encoding
  normalization, spectrum, condition number, precision, success amplitude,
  and adaptive transcripts.  A common rank-one projector compiler gives
  the explicit unconstrained state-solve ledger
  \(\widetilde O(\kappa_H\log(1/\epsilon_{\rm lin}))\), independent of
  packing arity or cone-factor count per encoding call.  For fixed group
  width \(p\), arbitrary cross-source packing, unshared PSD Schur blocks,
  and grouped Lorentz blocks are therefore oracle-equivalent throughout a
  fiber-oblivious run.  The theorem requires identical complete oracle
  unitaries (not merely equal advertised blocks), and excludes ambient
  lifted states, off-center lifted iterates, uncharged factor-bundled
  access, and Gram reconstruction.
- [Off-center PSD packing has an exact quotient Hessian and a sharp
  obstruction](2026-09-04-off-center-psd-packing-schur-obstruction.md)
  closes the main scope gap in the centered oracle theorem.  For arbitrary
  positive-definite packed residuals \(D_\ell\), eliminating all auxiliary
  matrix directions gives
  \[
    Q_D(U)=2\sum_\ell\operatorname{tr}(D_\ell^{-1}U_\ell^TU_\ell)
      +4z(U)^TM(D)^{-1}z(U),
    \quad
    M_{ab}=\sum_\ell\operatorname{tr}(E_a^\ell D_\ell E_b^\ell D_\ell).
  \]
  Thus off-diagonal residual covariance couples both packed columns and
  source allocation rows.  If the residual is relatively centered,
  \(\mu D_\ell^0\preceq D_\ell\preceq L D_\ell^0\), the centered
  Lorentz Hessian is a primal-nullspace and dual-normal preconditioner with
  condition at most \((L/\mu)^2\); a fiber Dikin radius \(\delta<1\)
  gives \(((1+\delta)/(1-\delta))^2\).  This dependence cannot be removed:
  at the same projected analytic center, the feasible two-source residual
  \(D=\left(\begin{smallmatrix}1&\rho\\\rho&1\end{smallmatrix}\right)\)
  has projected condition
  \((1+|\rho|)/(1-|\rho|)\to\infty\), while the centered Lorentz condition
  is one, and the corresponding normalized Newton states remain a constant
  trace distance apart.  Hence projected centrality alone gives no
  off-center oracle transfer; auxiliary fiber eccentricity is necessary.
  The quantum comparison remains conditional on charged block encodings,
  inverse residual access, and preconditioner application.  The theorem
  does not address arbitrary PSD lifts or full ambient IPM convergence.
- [Implicit PSD fiber recentering is linear with norms and Grover-hard
  without them](2026-09-04-implicit-psd-fiber-recentering-access.md)
  gives the positive algorithmic completion of that obstruction. At any
  explicit projected iterate, the exact unique fiber center is stored as
  \(S_\ell=W_\ell^TW_\ell+\operatorname{Diag}(d)\),
  \(d_\gamma=(1-\|x_a\|^2)/h\), without materializing a Gram matrix. It
  costs \(O(bs)\) arithmetic and storage independently of packing; a
  common-denominator \(B\)-bit implementation is backward exact in
  \(\widetilde O(bs\,\mathsf M(B+\log(bs)))\) bit operations. A certified
  relative fiber error \(\delta<1\) preserves the centered preconditioner
  within \(((1+\delta)/(1-\delta))^2\). With a maintained radial-scale
  oracle, each centered diagonal query costs one scale query and the
  reduced PSD--Lorentz compiler remains packing independent. This metadata
  is essential: normalized-state access cannot determine the radius, while
  raw coordinate access needs \(\Omega(\sqrt s)\) quantum or \(\Omega(s)\)
  randomized queries even for one source. Materializing all \(b\)
  independent scales costs \(\Omega(b\sqrt s)\) quantum or \(\Omega(bs)\)
  randomized queries, but one online coherent superposed scale evaluation
  can use source-controlled Grover search in \(O(\sqrt s)\); its raw queries
  must be charged on every use. A replicated-block strengthening makes the
  missing-metadata cost margin-sensitive and tight:
  \(\Theta(\rho^{-1/2})\) quantum versus \(\Theta(\rho^{-1})\) randomized
  queries for centered slack \(\rho=k/s\). Explicit dense PSD output
  separately costs \(\Omega(\sum_\ell c_\ell^2)\) writes. Thus the theorem yields a robust
  reduced-QIPM equivalence under scale-aware access, not a generic ambient
  primal--dual SDP implementation or an unqualified end-to-end speedup.
- [Dynamic PSD fiber-scale maintenance has an exact query
  tradeoff](2026-09-04-dynamic-psd-fiber-scale-maintenance-lower-bound.md)
  composes the scale obstruction across genuinely fresh sparse update
  batches under a precise access contract. For \(T\) epochs, \(b\) sources,
  and a universal service supporting \(r_t\) arbitrary scale-oracle uses at
  epoch \(t\), its independently audited raw-query law on zero-or-one-mark
  hidden-support updates is
  \[
    Q=\Theta\!\left(\sqrt s\sum_t\min\{r_t,b\}\right),
    \qquad
    R=\Theta\!\left(s\sum_t\min\{r_t,b\}\right).
  \]
  A reusable compile-and-commit oracle has \(r_t\geq b\) and therefore
  costs \(\Theta(Tb\sqrt s)\) quantum or \(\Theta(Tbs)\) randomized
  queries; a single raw-backed coherent evaluation costs only
  \(\Theta(\sqrt s)\), independent of \(b\). A replicated \(k\)-coordinate
  promise replaces the factors by
  \(\rho^{-1/2}=\sqrt{s/k}\) and \(\rho^{-1}=s/k\). The lower bound is a
  Kronecker-sum adversary direct sum and remains valid with persistent
  quantum workspace and all epoch oracles revealed in advance. Explicit
  sparse-list updates evade it and admit support-linear scale maintenance.
  A static input also defeats naive roundwise multiplication by caching:
  the hard theorem needs fresh independent batches. On the exact uncoupled
  linear product-ball central path this escape is constructive:
  \(\rho_a(\eta)=2/(1+\sqrt{1+(\eta\|c_a\|/h)^2})\), so objective-block
  norms are compiled once and reused for every path parameter. Thus this is an exact
  dynamic access/service boundary, not a Newton trajectory or end-to-end
  iteration lower bound for one fixed conic program.
- [The exact standard-slice frontier for product-ball Lorentz
  lifts](2026-09-04-product-ball-standard-slice-barrier-frontier.md) turns the
  \(C^1\) top-class theorem into an exact standard-barrier
  result.  Along an affine segment to a selected boundary lift, every
  nonzero Lorentz ray contributes one copy of \(-\log t\), while a cone
  vertex contributes two.  The self-concordant gradient inequality therefore
  forces \(\nu_{\rm slice}\geq J_1+2J_0\).  The top-class cover produces
  one contact where every source simultaneously has its required active
  rays, despite smooth vertex-mediated switching.  Hence, for
  \((B_2^s)^k\) and a Lorentz cap \(d<s+1\), the minimum parameter of the
  restricted standard product barrier is exactly
  \[
    \nu_{\rm std,slice}^{\min}
      =k\left\lceil{s\over d-2}\right\rceil,
  \]
  attained by the grouped lift; it is exactly \(k\) above the direct-block
  threshold.  The heterogeneous value is exactly \(\sum_a h_a\), with the
  same per-source cap transition as in the factor-count theorem.  This is an
  audited barrier certificate within the compatible globally \(C^1\)
  selected-lift class, not an arbitrary-barrier result for every lift or an
  iteration lower bound.  The embedded-cube theorem
  separately makes the same value optimal over arbitrary coupled barriers
  on the fixed grouped lift.
- [Sparse-SQ conditioning frontier](2026-09-04-sparse-sq-conditioning-frontier.md)
  gives a dimension-independent classical solution sampler and proves that
  polynomial sampling separations require \(\kappa=\Omega(\log N)\), or
  \(\Omega(\log^2N)\) for SPD systems; a squared hard family attains the SPD
  threshold.  A cyclic Forrelation clock now gives matching
  \(\exp(\Omega(\kappa\log s\log(1/\epsilon)))\) general and
  \(\exp(\Omega(\sqrt\kappa\log s\log(1/\epsilon)))\) SPD lower exponents.
- [Sparse-SQ Newton-decrement estimator](2026-09-04-sparse-sq-newton-decrement-upper.md)
  supplies the matching classical scalar half: for a \(d\)-sparse SPD
  Hessian, \(SQ(b)\) suffices to estimate \(b^*H^{-1}b\) relatively in
  dimension-independent time
  \(\exp(O(\sqrt\kappa\log(d+1)\log(1/\epsilon)))\), up to polynomial
  factors.  A positive quadratic-form/Kantorovich argument reduces the
  sampling variance factor from the naive \(\kappa^2\) to \(O(\kappa)\).
  A separate [two-sparse sign-block lower bound](2026-09-04-inverse-quadratic-polyfactor-lower.md)
  proves that its \(O(\kappa\epsilon^{-2})\) statistical factor is
  algorithmically sharp:
  \[
    \Omega\!\left(\min\{N,\kappa/\epsilon^2\}\right).
  \]
  The construction survives full matrix SQ because every norm and
  squared-magnitude distribution is public.  Its two-sparse square root
  realizes the same quantity as an exact small Newton decrement at the
  public analytic center of a sparse box LP.  On the same commuting family,
  coherent queries have the tight high-dimensional law
  \(\Theta(\sqrt\kappa/\epsilon)\).  The companion
  [coherent inverse-quadratic frontier](2026-09-04-coherent-inverse-quadratic-frontier.md)
  specializes variable-time negative-power estimation to \(H^{-1/2}\) and
  improves the generic upper to
  \(\widetilde O(\alpha\kappa/\epsilon)\), hence
  \(\widetilde O(d\kappa/\epsilon)\) for the standard sparse block encoding.
  A three-dimensional hybrid proves the matching
  \(\Omega(\alpha\kappa/\epsilon)\) lower for plain black-box block access.
  That lower does not transfer to an exact sparse-value oracle, where one
  query exposes its varying diagonal entry; closing the sparse-access gap
  from \(\sqrt\kappa\) to \(d\kappa\) remains open.
  A matching [full-SQ inverse-quadratic lower bound](2026-09-04-sparse-sq-inverse-quadratic-lower.md)
  follows by affine-shifting the Montanaro--Shao matrix-function clock to an
  SPD matrix, applying the exact approximate degree of the normalized
  reciprocal, and polarizing one hard inverse entry into two positive
  relative quadratic forms.  The weighted clock has public row/column norms
  and constant-query SQ simulation.  Its formerly ideal-real public weights
  now have a robust finite-bit strengthening: downward dyadic rounding at
  \(O(\log(\kappa/\epsilon))\) bits preserves the hard signal, and an exact
  rational block-\(LDL^T\)/four-square Gram factor realizes the SPD matrix as
  the analytic-center Hessian of a sparse box LP.  The public table is
  nonuniform; a terminating generator exists, but polynomial-time stable
  generation is open.  The scalar LP Newton-decrement frontier is therefore
  tight over the full accuracy range.  The structured coherent clock obeys
  the exact reduction \(q_\pm=D\pm C\Phi\), but without a proved
  noncancellation ratio this gives only \(O(\kappa)\) on the lower-bound
  scaling \(\tau=\Theta(\epsilon)\).  It is \(O(1/\epsilon)\) when
  \(\kappa\epsilon=O(1)\), but no such claim is made uniformly or for generic
  inputs.  This box lift has
  ambient barrier parameter \(\Theta(N)\).  The one-cone SOCP theorem supplies a different conic
  realization whose exponent is closed for fixed conditioning and when
  \(\log(1/\delta)=\Omega(\log\kappa)\).
  The [product-composition audit](2026-09-04-inverse-quadratic-product-composition-obstruction.md)
  proves a genuine single-form product by distributional block averaging:
  for fixed clock contrast it gives
  \(\epsilon^{-2}s^{\Omega(\sqrt\kappa)}\) on one full-SQ sparse SPD/box-LP
  family, and more generally a continuous contrast--accuracy tradeoff.
  An independently audited constant-weight path makes another point on this
  tradeoff explicit: for \(\kappa\geq128\) and
  \(\epsilon\lesssim\kappa^{-3/2}\), one instance requires
  \[
    \Omega\!\left(
      \frac{\kappa^2q^{\ell/2}}{r\ell}
    \right),\qquad
    \ell=\Theta\!\left(
      \sqrt\kappa\left[1+\log\frac1{\kappa^{3/2}\epsilon}\right]
    \right),\qquad q=2^r,
  \]
  at matrix sparsity at most \(2q+1\).
  This does not improve the optimized lower envelope beyond the maximum of
  the two endpoint bounds.  Multiplying the full
  \(\kappa\epsilon^{-2}\) factor by the full-accuracy clock exponent would
  require narrow \(\Theta(\kappa)\)-contrast levels.  Two-cluster
  polarization, scalar Schur resonance, and the standard cyclic resolvent
  each have a proved condition/clock-budget obstruction to doing so.
- [Lorentz Newton SQ dequantization](2026-09-04-lorentz-newton-sq-dequantization.md)
  proves a dimension-independent one-step sampler for a few arbitrarily large
  SOCP blocks under bounded eccentricity, sparse-base conditioning, and
  iterate-SQ access; it is explicitly conditional rather than an end-to-end
  classical IPM.
- [Eccentricity-profile SOCP preconditioning](2026-09-04-eccentricity-profile-socp-preconditioner.md)
  removes dependence on the worst Lorentz block for explicit Newton solves.
  Treating exactly the \(b_\theta\) blocks with eccentricity above \(\theta\)
  gives a signed rank-\(2b_\theta\) correction and the sharp comparison
  \(\theta^{-1}P_\theta\preceq N\preceq\theta P_\theta\), hence
  \(O(\theta\log(1/\eta))\) PCG iterations.  With a width-\(\tau\) sparse
  base normal graph, the exact-arithmetic work is near-linear when
  \(\tau,\theta,b_\theta\) are subpolynomial, even if the assembled normal
  matrix is dense and arbitrarily ill-conditioned.  A genuine \(Q_3\)-block
  witness proves that rank \(2b\) is worst-case necessary to guarantee
  condition at most \(\theta^2\); the PCG energy error is exactly the induced
  primal barrier-metric error.  The matched-access full-output QIPM exclusion,
  order-statistic Pareto envelope, and rank lower bound are independently
  audited and literature-screened.  An audited quasidefinite alternative
  factors an expanded width-\(\tau+2b_\theta\) system and avoids an explicit
  signed Woodbury-core inverse.  Finite precision still requires a stable
  product-form update or explicit growth and refinement bounds, and the
  eccentricity/base graph remain representation-dependent.
- [Latent treewidth of Lorentz Newton systems](2026-09-04-latent-treewidth-lorentz-newton-systems.md)
  shows that a dense high-dimensional Lorentz Hessian has a one-hub exact
  expansion and a two-hub quasidefinite expansion.  If the resulting
  rank-expanded incidence graph has width \(\tau_{\rm L}\), its Newton system
  is solvable in \(O((M+p+k)(\tau_{\rm L}+1)^2)\) field operations by the
  sharp low-treewidth elimination theorem, independently of the largest cone
  dimension and without regularization.  Controlled dual regularization
  additionally yields a reusable quasidefinite \(LDL^T\) factor.  If the
  coarse cone--row graph has width \(w\) and every
  scalar column is used once, then
  \(\tau_{\rm L}\leq\max\{2w+1,3\}\): forest-coupled many-cone families have
  linear structured solves even while their materialized Hessians contain
  arbitrarily large cliques.  A new additive curvature argument shows that
  every joint exact lift of \(Q_{s+1}^k\) by
  \(\prod_jQ_{m_j}\) satisfies
  \(\sum_j(m_j-2)\geq k(s-1)\).  Hence even a coupled pure-\(Q_3\) lift needs
  exactly \(k(s-1)\) factors, and every coupled ambient product-cone barrier
  has \(\nu\geq2k(s-1)\).  Splitting into norm trees therefore gives no
  per-step asymptotic gain and worsens the generic ambient-barrier
  short-step factor by \(\Theta(\sqrt s)\), holding logarithmic
  initialization terms fixed.  The exact-arithmetic, graph, additive-factor,
  and ambient-barrier claims are independently audited; the QIPM consequence
  is scoped to matched access and full iterate materialization and is not an
  intrinsic barrier or iteration lower bound for the projected slice.
- [Generalized-power Newton SQ dequantization](2026-09-04-generalized-power-newton-sq-dequantization.md)
  extends the diagonal-plus-low-rank mechanism to high-dimensional
  generalized-power cones with arbitrary positive power weights.  A
  dimension-free Hessian comparison yields a
  rank-two correction per block and a conditional one-step SQ sampler; the
  note also proves that maintaining the geometric-mean barrier scalar is a
  necessary access assumption.  The algebra and reduced-column access
  argument have been independently audited.
- [Checkpoint-span recycling](2026-09-04-checkpoint-span-recycling.md)
  replaces path-variation control by exact or numerical solution-ray rank, but
  remains a conditional module shared with classical recycling methods.
- [Projected block-angular barriers](2026-09-04-projected-block-angular-barriers.md)
  gives two exact low-parameter compilers and a factorized-Cramér normalization
  obstruction.
- [Pareto-active SOC compilation](2026-09-04-pareto-soc-barrier-compiler.md)
  gives a tight \(\Theta(\sqrt{Nk})\) exact compiler for a coupled,
  irredundant two-dimensional cone intersection, with constant-treewidth
  lift and an explicit product-barrier/path-length separation.
- [Cone-meet compilers](2026-09-04-cone-meet-compilers.md)
  characterize exact one-translate compilation by simpliciality, give a
  rank-sensitive quantum compiler, and prove that \(N\) fixed-rank Lorentz
  translates can all remain indispensable despite treewidth one.
- [\(k\)-block Pareto-SOC compiler](2026-09-04-kblock-pareto-soc-compiler.md)
  gives a rational bounded-incidence family with tight
  \(\Theta(\sqrt{Nk})\) versus \(\Theta(N)\) full-solution query bounds and
  matching \(\Theta(N)\)-to-\(\Theta(k)\) barrier/path compression.
- [Exact zero-query state-conversion radius](2026-09-04-zero-query-state-conversion-radius.md)
  resolves much of the \(p-\epsilon=o(k/G)\) sliver and proves that no
  winner-mass-only boundary is possible.
- [Dilation-rank perspective compilers](2026-09-04-dilation-rank-perspective-compilers.md)
  characterize the exact continuous summary width of common-ray perspective
  families and give a two-moment noncommutative Umegaki source compiler,
  carefully separating source-evaluation complexity from the already-known
  small QRE barrier parameter.
- [Blockwise relative-entropy source compiler](2026-09-04-blockwise-relative-entropy-source-compiler.md)
  gives tight \(\Theta(\sqrt{NB})\) quantum versus \(\Theta(N)\) randomized
  explicit-compilation/full-coordinate bounds and an exact matched-gap
  \(\sqrt N\)-versus-\(\sqrt B\) fixed-slice metric comparison.
- [Positive-slope exponential moment compiler](2026-09-04-positive-slope-exponential-moment-compiler.md)
  gives a certified sector-wise approximation of \(N\) exponential-recourse
  factors by \(O(\Lambda L+\log(1/\epsilon))\) power cones using cached slope
  moments, with explicit inner/outer epigraphs, barrier and source-query
  accounting.  Optimized moment tolerances give
  \(\widetilde O(\min\{N,e^K\sqrt K/\delta\})\) source queries and matching
  \(\Omega(\min\{N,1/\delta\})\) quantum dependence for fixed nonzero
  sector width \(K\), up to confidence logarithms.  Its proof and access
  qualifications have been independently audited.
- [Gaussian-quadrature exponential-cone compiler](2026-09-04-gaussian-quadrature-exponential-cone-compiler.md)
  handles signed slopes and signed ratios by replacing the source slope
  distribution with an at-most-\(m\)-node positive Gaussian quadrature rule.
  Moment exactness gives a uniform relative error
  \(4^{1-m}e^{2K}K^{2m}/(2m)!\); Gaussian error positivity makes the
  unscaled rule a certified outer model.  The inner model and barrier
  compression from \(3N\) to at most \(3m+O(1)\) are explicit.  The note
  also gives a robust confidence-box/Hausdorff-moment variant: for fixed
  \(K\), it uses \(\widetilde O(\min\{N,1/\delta\})\) quantum source queries
  and at most \(m\) output cones for signed slopes, matching an
  \(\Omega(\min\{N,1/\delta\})\) lower bound up to confidence logarithms.
  Both variants have been independently audited; finite-bit atom extraction
  for the robust variant is retained as an explicit caveat.
- [Sharp exponential-mixture support lower bound](2026-09-04-exponential-mixture-support-lower-bound.md)
  proves that the Gaussian compiler's fixed-sector support order is minimax
  optimal against all positive atomic slope mixtures, not only Gaussian or
  moment-matching rules.  For every fixed \(K>0\), in-range competitors
  satisfy
  \(-\log\mathcal E_m(K)=2m\log m+O_K(m)\), hence the exact leading support
  complexity is
  \((1/2+o(1))\log(1/\epsilon)/\log\log(1/\epsilon)\).  Even allowing arbitrary
  real competitor nodes leaves that leading constant unchanged:
  \(-\log\mathcal E_m^{\mathbb R}(K)
  =2m\log m+O_K(m\log\log m)\).
  A single fixed uniform
  slope distribution is hard, and an \(m+1\)-scenario Gauss--Legendre source
  gives the same finite-instance lower bound.  The theorem has been
  independently audited.  For in-range nodes, the joint growing-sector law
  is also sharp:
  if \(m/K\to\infty\), then
  \(-\log\mathcal E_m(K)=2m\log(m/K)+O(m+K)\); equivalently, for
  \(L_\epsilon=\log(1/\epsilon)\) with \(L_\epsilon/K\to\infty\) and
  \(L_\epsilon/W(L_\epsilon/(2K))\to\infty\),
  \(m_*=(1+o(1))L_\epsilon/[2W(L_\epsilon/(2K))]\).
- [Robust signed exponential moment-grid compiler](2026-09-04-robust-signed-exponential-moment-grid-compiler.md)
  repairs that extraction issue at the formulation level by rounding slopes
  to a public rational grid, solving a rational moment-box LP, and applying
  Caratheodory compression.  It returns at most \(d+1\) grid atoms and exact
  inner/outer exponential-cone models without Hankel root recovery.  The
  error ledger also rules out a tempting estimate for this proof method:
  independent rectangular moment boxes cost
  \(\widetilde O(\min\{N,e^{2K}\sqrt K/\epsilon\})\), not
  \(\widetilde O(e^K\sqrt K/\epsilon)\), for uniform relative error on a
  signed sector.  A new tilted-local-jet confidence LP instead achieves
  \(\widetilde O(\min\{N,e^K/\epsilon\})\) queries.  Post hoc exact ordinary-
  moment compression keeps the delivered formulation at
  \(O(K+\log(1/\epsilon))\) positive atoms/cones.  This matches the
  \(\Omega(e^K/\epsilon)\) lower bound in the large-\(N\) growing sector,
  up to confidence logarithms.  The theorem has been independently audited;
  the corresponding classical sampling-only law is
  \(\widetilde\Theta(e^{2K}/\epsilon^2)\), giving the full quadratic
  source-query separation while both algorithms deliver classical positive
  atoms.  With indexed weight-and-value access the audited worst-case law is
  instead
  \(\widetilde\Theta(\min\{N,e^{2K}/\epsilon^2\})\); the full quadratic
  relation therefore requires \(N=\Omega(e^{2K}/\epsilon^2)\), while the
  intermediate finite-population regime saturates classically at \(N\).
  The classical corollary has been independently audited.
  The simpler value-grid certificate remains as an independently checkable
  but dominated construction.
- [Certified one-factor entropic-risk ECP compression](2026-09-04-tilted-jet-entropic-risk-ecp.md)
  transfers the tilted-jet theorem to an end-to-end scenario optimization
  result.  On \(0\leq V\leq V_{\max}\), \(|U|\leq LV\), it gives explicit
  inner/outer sparse exponential-cone programs whose optimal-value and
  feasible-solution gap is at most
  \((\gamma V_{\max}/\beta)\log(U_*/L_*)\).  At additive target \(\tau\),
  the compiler uses
  \(\widetilde O(\min\{N,e^K\max\{1,\gamma V_{\max}/(\beta\tau)\}\})\)
  source queries and
  \(O(1+K+\log_+(\gamma V_{\max}/(\beta\tau)))\) exponential cones, versus
  \(N\) cones in the original scenario lift.  Balanced copy and aggregation
  trees preserve constant incidence outside the sparse base links.  In the
  hidden weighted-sampling model, optimal-value estimation has matched
  quantum and classical source laws
  \(\widetilde\Theta(e^K\gamma V_{\max}/(\beta\tau))\) and
  \(\widetilde\Theta(e^{2K}\gamma^2V_{\max}^2/(\beta^2\tau^2))\).
  For indexed uniform scenarios, the quantum unsaturated hard pair requires
  \(N=\Omega(e^{2K}\gamma V_{\max}/(\beta\tau))\), while the full
  unsaturated classical quadratic law requires
  \(N=\Omega(e^{2K}\gamma^2V_{\max}^2/(\beta^2\tau^2))\); below the latter
  threshold the classical law saturates at \(N\).  The application theorem,
  including its value and returned-feasible-solution certificates, has been
  independently audited.  A Fenchel-biconjugacy reduction also makes the
  fixed-\(K\) cone count sharp within reusable positive-atom scenario
  models: if one compressed model must approximate the optimal value after
  every linear objective tilt in the bounded natural slope range
  \(|a|\leq\gamma V_0\Lambda\), then it needs
  \[
   \left(\frac12+o(1)\right)
   {\log(\gamma V_0/(\beta\tau))\over
    \log\log(\gamma V_0/(\beta\tau))}
  \]
  atoms/cones in the worst case, matching the fixed-sector upper bound.
  The exact leading upper is existential through Gaussian quadrature, not a
  leading-constant guarantee for the robust tilted-jet recovery algorithm.
  This lower bound is for reusable positive-mixture lifts, not arbitrary
  exponential-cone extended formulations or summaries tailored to one
  objective tilt.
- [Fixed-factor multivariate tilted-jet compression](2026-09-04-fixed-factor-multivariate-tilted-jet-compiler.md)
  extends the signed compiler to \(z\in[-K,K]^r\), with the norm convention
  \(B=rK\) explicit.  For fixed factor rank \(r\), it gives uniform relative
  error with \(\widetilde O_r(e^{rK}/\epsilon)\) quantum source queries and
  at most \(\binom{r+d}{r}\) positive atoms/cones, where
  \(d=O(rK+\log(1/\epsilon))\).  The honest nonconstant-\(r\) ledger is
  \(\widetilde O(A_r(Cr)^re^{rK}/\epsilon)\), a public grid of size
  \(O((1+rK/\epsilon)^r)\), and a temporary tilted LP with
  \(O((1+rK)^r\binom{r+m}{r})\) rows.  Opposite cube corners force the
  lower bounds \(\Omega(e^{rK}/\epsilon)\) quantum and
  \(\Omega(e^{2rK}/\epsilon^2)\) classical, so the exponent \(rK\) is not a
  one-coordinate embedding artifact.  The theorem has been independently
  audited.
- [Growing-factor tilted-jet refinement](2026-09-04-growing-factor-tilted-jet-refinement.md)
  shows that the preceding \((Cr)^r\) query prefactor is an artifact of
  forcing constant \(\ell_1\)-radius charts.  Constant coordinate-radius
  charts and local degree \(O(r+\log(1/\epsilon))\) improve the large-box
  source cost to
  \(\widetilde O(C_0^r e^{rK}/\epsilon)\), without changing the final
  \(\binom{r+d}{r}\) support or barrier parameter.  Two measured-source
  fallbacks give, with \(B=rK\), the additional sample bounds
  \[
   O\!\left({e^{2B}\over\epsilon^2}
   [r\log(1+rK/\epsilon)+\log(1/\alpha)]\right)
   \quad\hbox{and}\quad
   O\!\left({e^{4B}B^2\over\epsilon^2}
   [1+\log(1/\alpha)]\right).
  \]
  The second has no covering-number or dimension factor.  Thus for
  \(K=\Theta(1/r)\) and fixed \(\epsilon,\alpha\), the source-query count is
  \(O(1)\), and direct delivery of the empirical measure uses only \(O(1)\)
  positive atoms/scenario cones, improving the single-chart
  \(\widetilde O(e^{O(\sqrt r)}/\epsilon)\) bound.  Exact post hoc moment
  compression remains optional when its moment count is smaller.  This statement
  assumes one full-vector-value query per measured source index; a
  coordinate-value oracle adds a factor \(r\), and reading and writing the
  atoms costs \(\Omega(r)\), so the runtime and output length are not
  dimension-free.  A separate sharp cube-section argument shows that, for
  integer \(r\geq B\), every signed exponential sum with arbitrary real
  coefficients and nodes that uniformly approximates the Rademacher MGF
  has exponent-span dimension
  \[
   d\geq r-{\log((1+\epsilon)/(1-\epsilon))
                   \over\log\cosh(B/r)}.
  \]
  Optimizing \(r\) at fixed \(B\) gives
  \(R\geq d\geq(1-o(1))B^2/(16\epsilon)\).  Thus this is a signed-rank
  obstruction, not merely a positive support bound or a restriction to
  nodes in the source cube.  For the reusable direct positive-mixture
  ECP this forces \(\Omega(B^2/\epsilon)\) exponential-cone factors.  The
  exact optimal parameter of the full ambient product is \(3R\), even for
  arbitrary coupled standard self-concordant barriers, and therefore has
  asymptotic lower \((3-o(1))B^2/(16\epsilon)\); the standard separable
  product barrier attains it.  Negative-weight sums do not themselves define these convex
  lifts; the conic consequence uses the positive subclass.  This is not an
  arbitrary-lift or IPM-iteration lower bound.
  Separately, the empirical \(1/\epsilon^2\) law is sharp for every
  measure-first compiler: a two-corner Bernoulli reduction gives
  \(\Omega(\epsilon^{-2}\log(1/\alpha))\) preparations even with arbitrary
  later reweighting.  On the same family, coherent amplitude estimation
  uses \(O(\epsilon^{-1}\log(1/\alpha))\) queries and emits a classical
  positive two-atom measure.  Thus positivity and classical output do not
  themselves cause the quadratic accuracy law.
  Hence a still-open coherent
  \(\widetilde O(e^B\operatorname{poly}(B)/\epsilon)\) compiler would be
  optimal in accuracy and avoid any extra factor-rank cost; at bounded
  \(B\) this is \(\widetilde O_B(1/\epsilon)\).  The remaining
  large-box gap is between \(e^{rK}/\epsilon\) and
  \(C_0^re^{rK}/\epsilon\); no lower bound forcing \(C_0^r\) was found.
  All arms, lower bounds, and access-model qualifications have been
  independently audited.
- [Arbitrary exponential-cone lifts versus exponential
  rank](2026-09-04-arbitrary-exponential-cone-lifts-vs-exponential-rank.md)
  identifies the precise limit of the preceding support theorem.  A
  bounded-slope binomial MGF can have exact signed exponential rank \(m+1\)
  while its epigraph has a fixed lift using three exponential cones and one
  linear inequality.  The product-cosh hard source itself has exact signed
  rank \(2^r\) but an exact \(2r+1\)-exponential-cone lift.  Thus auxiliary
  log-sum-exp/exponential composition prevents any syntactic transfer from
  signed rank to arbitrary ECP factor count.  A separate exact theorem does
  survive: slicing at a strictly interior level and applying curvature
  capacity gives \(R\geq r-1\) for every exact
  \(K_{\exp}^R\times\mathbb R_+^P\) lift, and the full ambient product has
  exact barrier parameter
  \(3R+P\geq3(r-1)+P\).  This exact \(\Theta(r)\) factor law is matched
  within a constant by the explicit lift.  It does not extend from uniform
  relative approximation alone: finite tangent envelopes give certified
  multiplicative brackets using no exponential cones when polyhedral
  inequalities are uncharged.  The theorem and obstruction have been
  independently audited.

## Strongest current publication candidates

The eight result groups with the clearest present combination of novelty,
completeness, and impact are:

1. the universal dimension-minus-two curvature theorem for arbitrary
   definable proper-cone products, with simultaneous exact ball optima in
   block count, total cone dimension, and ambient product-barrier parameter;
   the audited \(\ell_p\)-ball corollary shows that the factor/dimension
   optimum holds throughout \(1<p<\infty\), not only in Euclidean geometry;
   the new coupled-product cross-ratio theorem further gives the strict
   \(p\)-dependent barrier premium
   \(\nu\geq h(p)\lceil(N-1)/(d-2)\rceil\) for \(p\)-order-block lifts when
   \(p\ne2\), plus a dictionary-independent strict bound at minimum total
   cone dimension;
   the audited one-cone follow-up proves a sharp necessary boundary scale
   for the characteristic-barrier ansatz and rules out three natural
   matching constructions while leaving the exact optimum open;
   the independently audited Euclidean-Jordan theorem supplies the sharper
   contact law \(apq\) and \(N-1\leq M-\nu\) for symmetric cones;
   the new independently audited PSD support-Grassmannian theorem makes the
   local maximum-capacity equality globally impossible for every
   \(N\geq4\), sharpening
   \(\sum_i\lfloor r_i^2/4\rfloor\geq N-1\) to \(N\) for arbitrary PSD
   orders under bi-\(C^1\) selections, and gives the exact order-three
   smooth-ball frontier
   \((k,M,\nu_{\rm normal})=(\lceil N/2\rceil,3N,
   \lceil3N/2\rceil)\); its mixed real/complex/quaternionic extension
   classifies the only sharp division-algebra cases \(N=2,3,5\);
   the new twice-audited Euclidean-Jordan support-orbit theorem gives the
   sharp structural classification behind these cases: global saturation
   forces one spin/Lorentz factor of dimension \(N+1\), except for a
   topological \(\mathbb S_+^3\) possibility at \(N=3\) that necessarily
   uses at least three additional ray factors and is resource-dominated by
   \(Q_4\); a separately audited round-ball argument excludes that
   possibility entirely for \(B_2^3\), even with finite \(C^1\) ray
   factors.  It also classifies the ambient defect:
   \(M-\nu=N-1\) only for one positive \(Q_{N+1}\) block, while every
   genuinely different globally regular factorization has \(M-\nu\geq N\).
   Thus every cap \(d<N+1\) raises the integer curvature budget
   from \(N-1\) to \(N\).  Grouped Lorentz lifts attain the resulting
   simultaneous Euclidean-ball optima
   \[
     k=\left\lceil\frac{N}{d-2}\right\rceil,\qquad
     M=N+2k,\qquad \nu=2k
   \]
   for \(3\leq d<N+1\), while one direct block gives
   \((k,M,\nu)=(1,N+1,2)\) for \(d\geq N+1\).  Grouped perspective cones
   give the same exact all-cap \((S,k,M)\) frontier for every
   \(B_p^N\), \(1<p<\infty\); determining the non-Euclidean ambient barrier
   optimum remains open.  A new audited nullity theorem further identifies
   the exact parameter of the **standard product Jordan barrier after
   affine restriction**: it is \(\lceil N/(d-2)\rceil\) in the capped
   regime and one in the direct regime, with grouped Lorentz attaining it.
   Its Hermitian-PSD refinement is field- and order-sensitive: with
   \(a=\dim_{\mathbb R}\mathbb F\) and order cap \(R\), the exact value is
   \(\lceil N/[a(R-1)]\rceil\), apart from the one-block range
   \(N\leq a(R-1)\) and the direct rank-two spin exceptions
   \(N=2,3,5\).  A projective-cover plus even-quadratic affine-pencil
   obstruction closes the otherwise surviving real divisible case.
   The independently audited Hermitian sequential contact-range theorem
   upgrades this to an exact additive product law over all three fields:
   for heterogeneous source dimensions \(s_a\), both the aggregate exposed
   dual rank at one simultaneous contact and the restricted standard-
   barrier optimum equal the sum of the sharp one-ball quantities
   \(\kappa_{\mathbb F,R}(s_a)\).  This permits arbitrary source/label and
   rank switching, closes every real one-channel residue, and supplies the
   path-independent exposed-rank distance coefficient given by the square
   root of that sum.  In the critical real regime \(s=R\geq3\), the new
   intrinsic certificate-fiber theorem goes further: for arbitrary finite
   affine lifts, with no selected sheets at all, genuine global certificates
   have every positive aggregate rank at least \(2b\), every final fiber at
   their simultaneous contact has nullity at least \(2b\), and the
   path-independent standard-logdet metric coefficient is \(\sqrt{2b}\).
   Thus the exact restricted-standard-barrier value \(2b\) is unconditional
   within the affine PSD dictionary.  The independently audited
   certificate-fiber/projective argument now extends this exact
   one-channel product law to complex and quaternionic Hermitian lifts:
   every non-spin critical \(b\)-source lift has exact value \(2b\).
   A blanket selection-free promotion to the larger globally smooth
   exposed-rank value is nevertheless false.  For arbitrary affine real PSD2 lifts the
   exact selection-free minimax aggregate exposed rank is \(b(s-1)\), attained
   by independent binary norm chains, rather than the globally smooth value
   \(bs\).  More generally, under Lorentz dimension cap \(d\), the exact
   one-ball selection-free value is \(\lceil(s-1)/(d-2)\rceil\), and a
   unique-certificate grouped norm chain attains it; the chain's restricted
   standard barrier has parameter one less than twice that rank.  A compact
   rotated-perspective lift goes further: every boundary fiber has a
   completion of exactly that nullity and every dual fiber has maximum rank
   exactly that value, while simplex vertices still make its restricted
   barrier parameter twice the value minus one.  Thus an every-fiber
   nullity premium is false; the exact unrestricted standard-barrier
   frontier remains open only through the bounded divisible branch case.
   The new selection-free barrier theorem already proves the grouped value
   in every nondivisible cap case and for every unbounded divisible lift;
   its recession-rank-plus-compressed-nullity lemma rules out escape to
   infinity as a counterexample mechanism.  The independently audited
   exact Hermitian exposed-rank theorem proves, over
   \(\mathbb F=\mathbb R,\mathbb C,\mathbb H\), the all-order
   selection-free one-ball minimax
   \[
       \left\lceil{N-1\over
       (\dim_{\mathbb R}\mathbb F)(R-1)}\right\rceil,
   \]
   attained by a rotated Hermitian perspective, and gives the corresponding
   additive shared-product existence/nullity lower by global-certificate
   compression.  Hence every formulation has a support objective whose
   restricted-standard-logdet distance from any fixed interior reference
   is
   \(\sqrt q\log(1/\epsilon)-O_{\mathcal L,X^c,S}(1)\); bounded-metric
   outer rounds inherit the same asymptotic
   \(\Omega(\sqrt q\log(1/\epsilon))\) dependence below a
   formulation-dependent scale.  The grouped Schur lift supplies the
   all-support \(O_\theta(\sqrt q\log(q/\epsilon))\) upper, so the
   infimum-over-lifts/supremum-over-supports asymptotic bounded-Dikin
   coefficient is \(\Theta_\theta(\sqrt q)\), with lift and start fixed
   before accuracy tends to zero.  This is a path-independent movement
   result with nonuniform hard support, additive constant, and warm-start
   term, not a query lower bound.  Separately, the Hermitian standard-barrier extension
   proves the same barrier trichotomy over
   \(\mathbb F=\mathbb R,\mathbb C,\mathbb H\): with
   \(B=(\dim_{\mathbb R}\mathbb F)(R-1)\), the universal selection-free
   lower bound is \(\lceil(N-1)/B\rceil\), it is exact in every
   nondivisible or direct-spin case, while convex certificate-fiber
   projective rigidity closes every non-spin one-channel case at two and,
   by global-certificate compression, closes its \(b\)-source product at
   the exact additive value \(2b\).
   Every unbounded divisible lift pays the grouped extra unit.  The
   arbitrary-factor wide-cap rigidity theorems now close bounded lifts as
   well whenever the block capacity is at least \(q-1\).  For Lorentz
   factors, the exact grouped value \(q+1\) holds when
   \(N-1=q(d-2)\) and \(d-2\geq q-1\); only the bounded narrow-cap cases
   \(d-2\leq q-2\) remain.  For real, complex, or quaternionic Hermitian
   factors of order at most \(R\), the exact grouped value holds when
   \(N-1=qB\) and \(B\geq q-1\); only bounded cases \(q\geq B+2\)
   remain.
   Both wide-cap proofs are factor-count independent: face codimension
   forces singleton boundary fibers and globally fixed active labels.
   The older factor-count-minimal seam-incidence reduction shows how
   singular a remaining narrow-cap escape must be: a hypothetical
   low-parameter lift needs a nonempty semialgebraic seam on which the span
   of the **entire** normalized certificate fiber loses rank.  The
   wide-cap theorems show that no such seam can survive their codimension
   budget; they do not eliminate it in the narrow-cap range.
   This is distinct from the ambient normal parameter and from arbitrary
   custom slice barriers.  Proper nonsingular primal and dual contact sheets
   turn this into a checkable lift-level theorem.  The universal
   arbitrary-proper-cone covering theorem remains the cone-independent
   version, while the Jordan theorem identifies the unique sharp symmetric
   factor.  The earlier
   Adams--Steenrod \(N-O(\log N)\) dominant-block result remains supporting
   history under the weaker information of a tangent-bundle splitting, but
   is superseded whenever the summands integrate to global cone-factor maps.
   The audited joint-product extension adds a distinct sharp case: on the
   fixed weighted contact stratum of \((B_2^s)^2\), the minimum globally
   smooth \(Q_3\) factor count is exactly \(2s-1\), attained by a shared
   stereographic construction.  For \(k\) balls it gives
   \(k(s-1)+1\leq L\leq ks-\lfloor k/2\rfloor\).  On the full extreme-slack
   operator, the \(C^1\) top-class no-sharing theorem restores the exact
   separate-factor count \(L=ks\).  Under a Lorentz dimension cap \(d\), it
   also gives the exact simultaneous bi-\(C^1\) frontiers
   \((L,D_{\rm amb},\nu_{\rm ambient})=(kh,k(s+2h),2kh)\),
   \(h=\lceil s/(d-2)\rceil\), for \(d<s+1\), and
   \((k,k(s+1),2k)\) for \(d\geq s+1\).  Flat vertex-mediated switching
   defeats channelwise unique continuation but not this total-count theorem.
   The independently audited ray-exposed dictionary theorem is the
   cone-independent structural generalization: the identical full-slack
   frontier holds for every proper cone family whose common-primal exposed
   complementary faces are rays, without self-duality or smooth cone
   boundaries; Lorentz geometry is needed only for attainment.  Bundling
   the separate Lorentz factors into one cone shows that the face condition
   is essential.
   The audited bounded-face interpolation theorem quantifies the transition
   away from rays: contact-face dimension bounds simultaneous row sharing,
   and yields weighted global face-incidence, curvature-capacity, and
   ambient-rank ledgers, with PSD sharing interpreted as support-nullspace
   packing.  The audited universal whole-row contact-codimension theorem
   gives the exact cone-independent endpoint: for arbitrary convex bodies,
   one group costs its full coordinate dimension plus one, and its largest
   required cone face is determined exactly by the smallest source contact
   codimension.  The shared homogenization cone attains both, with no
   smoothness or factor regularity; strictly convex bodies, polytopes, and
   spectral balls respectively give contact losses \(n_a\), \(1\), and
   \(r_a+c_a-1\).  Equality in ambient dimension is rigid up to a linear
   cone isomorphism, so the exact Euclidean and spectral product-barrier
   laws hold for every minimum-dimensional whole-row formulation.
   At the absolute dimension minimum the same rigidity covers arbitrary
   row splitting: connected extreme manifolds force a single cone factor,
   yielding an unconditional one-dimension storage gap under any strict
   factor cap.  This is the strongest possible universal additive gap:
   the audited codimension-two slices of \(Q_{s+1}^L\) have path-connected
   extreme sets and \(L\) essential, slack-visible indecomposable factors
   but \(M=N+2\), so the deficit from \(N+L\) is the unbounded quantity
   \(L-2\). The stronger \(N+L\) law does survive for the useful
   restricted model obtained by projecting a single normalized base of a
   product cone. On the sharp all-Lorentz slices, the standard product-SOC
   barrier still has exact parameter \(2L-1\), so the topology-changing
   equality yields no additional standard-barrier saving. A
   \((2L-1)\)-simplex section proves that arbitrary coupled barriers cannot
   improve it either: \(\nu_{\rm opt}=2L-1\); before normalization, the
   balance cone has exact arbitrary coupled parameter \(2L\). The
   \(2L-1\) lower bound also holds for every bounded-fiber affine lift by
   exact partial minimization. An exact recession-positive fiber-minimum
   criterion extends this transfer through every unbounded closed lift of
   a compact polytope; in particular, a simple vertex forces
   \(\nu_{\rm lift}\geq n\) for every lift of an \(n\)-polytope. The same
   exact lower for polytopes with no simple vertex remains open under the
   screened results; independent active-normal rank alone is insufficient.
   Arbitrary unbounded fibers over curved bodies are the sharply
   isolated remaining scope: a semialgebraic one-recession-ray epigraph
   lift proves that compact projection and conic Slater regularity do not
   automatically permit a projection-preserving bounded-fiber affine
   normalization. For
   \(N=dL-2\), these are
   also exact arbitrary-cone cap-hard instances:
   \(L_{\min}=L,\ M_{\min}=N+2=dL\) under block dimension cap \(d\), with
   no row-integrity or regularity assumption.
   The independently audited
   [Hermitian balance-slice extension](2026-09-04-hermitian-balance-slice-sharp-frontier.md)
   gives the same phenomenon for heterogeneous products of real, complex,
   and quaternionic PSD cones and Lorentz spin factors. If \(\rho\) is
   the sum of their symmetric-cone ranks, its balance cone and normalized
   body have exact arbitrary-coupled barrier parameters \(\rho\) and
   \(\rho-1\), respectively, while the body has connected extreme points
   and ambient dimension deficit two. For \(L\) repetitions of one factor
   of dimension \(d\), the fully split, discontinuous,
   arbitrary-proper-cone cap frontier is again
   \(L_{\min}=L\) and \(M_{\min}=N+2=dL\).
   At matched real factor dimension \(d=d_{\mathbb F}(R)\), this Hermitian
   family and the Lorentz family built from \(Q_d^L\) therefore have the
   same \(N=dL-2\), exact factor count, and exact total cone dimension, but
   their optimal direct-slice barrier parameters are \(RL-1\) and
   \(2L-1\).  Thus their \(\sqrt{\nu}\) coefficients differ by
   \(\Theta_{\mathbb F}(d^{1/4})\).  This is a separation between two
   cap-hard bodies, not a claim that either is a lift of the other; it shows
   that factor count and total cone dimension do not determine the optimal
   barrier scale.
   The same theorem now covers every simple Euclidean Jordan cone,
   including the exceptional Albert cone. An off-diagonal Peirce balance
   leaves a boundary-inheriting frame orthant and simplex, proving the
   exact coupled parameters \(\rho\) and \(\rho-1\). In the Albert
   primitive-ray manifold, the reduced-coordinate height
   \((1-\|x\|^2)/(1+\|x\|^2+\|y\|^2)\) has connected positive, negative,
   and zero strata (the latter is \(S^7\times\mathbb R^8\) compactified by
   one point), so the connected-extreme cap proof also applies. For
   \(L\) identical Albert factors this gives the exact frontier
   \(N=27L-2,\ L_{\min}=L,\ M_{\min}=N+2=27L\).
   The family also has an explicit objective whose exposing Jordan slack
   has rank exactly \(\rho-1=\nu_{\rm opt}(Z)\). Its standard-barrier
   central path stays in the frame-diagonal simplex, and every feasible
   lifted path from the analytic center to gap \(\epsilon\) has length at
   least
   \(\sqrt{\rho-1}\log(((\rho-1)/\rho)/\epsilon)\).
   Thus the exact barrier parameter and the bounded-intrinsic-movement
   iteration coefficient align on these mixed symmetric-cone and Albert
   cap-hard instances. This is a standard-barrier geometric obstruction,
   not a quantum-query or runtime lower bound.
   Its audited sharp-model companion separates whole-row
   integrability from split-channel sharing: \(\mathcal H_{q,s}\) exactly
   minimizes dimension and face size for \(q\) whole rows, whereas
   \(\mathcal P_q\) realizes linear-in-face sharing for scalar channels.
   Heterogeneous dimensions \(s_a\) obey the exact \(\mathcal H\)-counts
   \(1+\sum_as_a\) in ambient dimension and
   \(1+\sum_as_a-\min_as_a\) in maximum complementary-face dimension; the
   resulting exact two-cap grouping problem is strongly NP-hard by
   3-PARTITION.
   Both have exact intrinsic barrier parameter \(q+1\).  Consequently the
   extreme one-cone model \(\mathcal H_{k,s}\) collapses factor count but,
   on its fixed-scale slice, leaves the exact parameter \(k\), central
   path, Dikin metric, reduced Newton oracle, and
   \(\Omega(\sqrt{k}\log(k/\epsilon))\) bounded-move lower bound unchanged.
   For several \(\mathcal H\)-blocks, explicit parameter-sharp recession
   certificates tensorize to prove the exact coupled ambient value
   \(\nu_{\rm opt}=k+g\), matching the sum barrier without assuming
   additivity from factorwise optimality alone.
   A complementary chordal-PSD construction shares an \(s\)-vertex Gram
   hub across each row group.  Its completion cone deletes all leaf--leaf
   PSD coordinates and has exact coupled ledgers
   \(D=k(s+1)+g s(s+1)/2\), \(\nu=k+gs\), while the fixed formulation slice
   again has the ordinary parameter-\(k\) product-ball barrier.  This is
   less barrier-efficient than \(\mathcal H\), but it exposes a
   clique-tree-sparse route compatible with classical PSD-completion
   machinery.
   The same sharing law extends to rectangular spectral-norm balls: with
   \(\rho_a=\min\{r_a,c_a\}\), \(g\) shared-scale groups have exact coupled
   ambient parameter \(g+\sum_a\rho_a\) and exact fixed-scale parameter
   \(\sum_a\rho_a\), with explicit nuclear-polar slack factors.  Block-star
   PSD completion gives the supporting sparse alternative
   \(gs+\sum_ap_a\), isolating matrix-rank cost from grouping cost.  On the
   fixed slice the two reduced barriers and every Newton/derivative oracle
   are exactly the same up to a public coordinate permutation, and the
   audited bounded-move lower remains
   \(\Omega(\sqrt{\sum_a\rho_a}\log(\sum_a\rho_a/\epsilon))\).
   The independently audited
   [spectral face-capped grouping
   theorem](2026-09-04-spectral-norm-face-capped-grouping-frontier.md)
   gives the exact whole-row two-cap law
   \[
      \sum_{a\in G}r_ac_a\leq D-1,\qquad
      \sum_{a\in G}r_ac_a-\min_{a\in G}(r_a+c_a-1)\leq F-1.
   \]
   It is necessary for any proper cone carrying the group through one
   full-slack block, without smoothness assumptions, and shared spectral
   cones attain it.  For equal \(r\times c\) rows the exact capacity is
   \[
     \min\!\left\{\left\lfloor{D-1\over rc}\right\rfloor,
       \left\lfloor{F+r+c-2\over rc}\right\rfloor\right\};
   \]
   heterogeneous optimal whole-row grouping is strongly NP-hard by
   3-PARTITION.  Complex matrix and face dimensions double, while barrier
   ranks do not.  Without row indivisibility, the audited split-row
   contact theorem still gives exact per-row mixed budgets
   \(\delta_ac_a-1\) for
   \(\mathbb F_a\in\{\mathbb R,\mathbb C,\mathbb H\}\),
   \(\delta_a=\dim_{\mathbb R}\mathbb F_a\).  Its direct-sum cylinder
   argument yields cone-dimension and complementary-face incidence
   lower bounds for arbitrary globally \(C^1\) proper-cone
   factorizations, while deliberately making no attainment or barrier
   claim.
   Boundary-ray multiplicity further makes the
   minimum restricted standard-product barrier parameter exactly \(kh\) in
   the small-cap regime and \(k\) above threshold, rather than merely giving
   the ambient values \(2kh\) and \(2k\).  On the frontier-attaining grouped
   slice, an embedded \(kh\)-cube upgrades this to the exact intrinsic
   optimum over every coupled self-concordant barrier and proves a
   \(k(h-1)\) granularity tax relative to the projected product body.  The
   diagonal-duplication counterexample shows why this arbitrary-barrier
   conclusion does not follow from factor count alone for a general lift.
   On the grouped slice, the exact central path for an all-groups objective
   has squared local speed
   \(kh(1-h/\sqrt{h^2+\tau^2})\).  More strongly, every path to the
   \(\epsilon\)-accurate set has barrier-metric distance at least
   \(\sqrt{kh}\log(r_0\Delta/\epsilon)\): the Hessian dominates the
   Euclidean metric of all log slacks, and two AM--GM steps force their
   product below \((2\epsilon/(kh))^{kh}\).  This yields a genuine,
   independently audited
   \(\Omega(\sqrt{kh}\log(\Delta/\epsilon))\) lower bound for any method
   assembled from uniformly bounded Dikin chords on this fixed lift and
   barrier, even if all iterates after initialization leave the central
   tube.  From the analytic center it specializes cleanly to
   \(\Omega(\sqrt{kh}\log(k/\epsilon))\).
   The [cross-packed PSD extension](2026-09-04-psd-packing-geodesic-iteration-lower-bound.md)
   survives arbitrary off-diagonal completion paths: for \(H=kh\) packed
   group columns, the log-determinant metric, Hadamard's inequality, and
   weighted Cauchy--Schwarz give the same
   \(\Omega(\sqrt H\log(k/\epsilon))\) bounded-move law, independently of
   the packing pattern.  In particular, the one-block order-\((s+k)\) PSD
   lift needs \(\Omega(\sqrt k\log(k/\epsilon))\) such moves despite its
   fully shared auxiliary matrix.  Unlike the barrier ledger, these are
   actual iteration lower bounds, but they do not cover long steps, other
   barriers or lifts, or algorithms not represented by feasible primal
   Dikin moves.  The independently audited
   [exposed-rank symmetric-cone theorem](2026-09-04-symmetric-cone-exposed-rank-dikin-lower-bound.md)
   now gives the coordinate-free explanation and a broader result.  For
   any product of symmetric cones, including the exceptional factor, a
   dual optimal slack of Jordan rank \(Q\) forces
   \(\sqrt Q\log(\Delta/\epsilon)\) distance in the standard Jordan metric,
   even through unbounded inactive fibers.  On a globally \(C^1\)
   product-ball lift, summed-slack Peirce curvature forces
   \(Q\geq\lceil\sum_a(s_a-1)/\kappa\rceil\), where
   \(\kappa=\max_i a_i(r_i-1)\).  Thus reducing factor count alone cannot
   reduce the actual bounded-Dikin movement scale; only increased
   cross-Peirce capacity per exposed rank unit can do so.  With \(L\)
   uniform order-\(R\), Peirce-\(a\) factors, discrete concavity gives an
   exact balanced rank-budget envelope and the continuous consequence
   \(n\leq a(RQ-Q^2/L)\); at capacity saturation the distance coefficient
   grows as \(\sqrt{LR}\).  Classification extends the theorem to every
   self-scaled barrier, replacing \(Q\) by
   \(Q_\alpha=\sum_i\alpha_iq_i\) for \(\alpha_i\geq1\), so the standard
   barrier minimizes the asymptotic coefficient within that class.  This
   also turns the all-cap single-ball frontier into an actual hard-objective
   movement theorem: some support direction has
   \(Q\geq\lceil N/(d-2)\rceil\), including the globally forced extra unit
   in the divisible case.  For heterogeneous product-ball lifts through
   arbitrary simple symmetric cones, private exposed-support quotients,
   complementary-ray tokens, and an Albert rank-two-face incidence lemma
   further give at every simultaneous contact
   \[
      Q\geq\sum_a\left\lceil{s_a-1\over\kappa}\right\rceil,
      \qquad \kappa=\max_i a_i(r_i-1).
   \]
   Under factor-dimension cap \(d\), this becomes
   \(Q\geq\sum_a\lceil(s_a-1)/(d-2)\rceil\).  Sequential Peirce-face
   compression strengthens this for a selected hard objective to
   \(Q\geq\sum_a h_d(s_a)\), where \(h_d(s)=1\) when \(d\geq s+1\) and
   \(h_d(s)=\lceil s/(d-2)\rceil\) otherwise.  Hence every strict-cap
   divisibility premium adds even across shared Hermitian, Lorentz, and
   Albert factors.  The branch at \(d=s+1\) is sharp by the direct Lorentz
   lift, and grouped Lorentz factors attain the full sum, making it an exact
   minimax exposed-rank frontier in the selected-sheet model.  A factor-aware
   refinement also adds the exact balanced rank budget
   row by row, giving
   \(Q\geq\sum_a\max\{h_d(s_a),Q_{\min}(s_a-1)\}\) in a uniform finite
   Peirce family.  The Albert lemma, universal token ledger, and sequential
   theorem were independently hostile-audited.  This
   remains a standard-or-self-scaled-barrier, feasible-bounded-metric-move theorem
   and does not cover arbitrary coupled barriers or non-iterate quantum
   algorithms.  A separate
   [barrier-independent primal--dual
   theorem](2026-09-04-barrier-independent-primal-dual-dikin-lower-bound.md)
   closes the arbitrary-barrier gap only in the canonical homogenized
   product and its primal--dual product metric: every logarithmically
   homogeneous barrier there has \(\nu\geq k+1\), and the distance from a
   central point of gap \(\Delta_0\) to the entire feasible
   \(\epsilon\)-gap set is at least
   \(\sqrt{\nu/2}\log(\Delta_0/\epsilon)\). Thus the
   \(\Omega(\sqrt{k}\log(\Delta_0/\epsilon))\) bounded-move law is
   barrier-independent in that model. The exact globally \(C^1\) capped
   Lorentz frontier similarly has arbitrary-LH coefficient
   \(\sqrt{kh_d}\), because its facially reduced ambient rank is at least
   \(2kh_d\). The real-PSD order-\(R\) frontier has coefficient
   \(\sqrt{V_R(N)/2}\) for a globally \(C^1\) full-slack lift of
   \(B_2^N\), \(N\geq3\); \(N=3\) uses the special
   \(\mathbb S_+^3\) exclusion, while the direct \(N=2\) spin case has
   only \(V_R(1)=2\). All require strict primal--dual feasibility in the
   operational cone after facial reduction. They neither project to a primal
   distance theorem, cover non-LH barriers, nor lower-bound oracle
   queries or primal-only/state/SQ/scalar outputs. The audited
   pointwise countermodel explains why active-face, determinant, and
   parameter inequalities alone cannot supply the missing primal theorem;
2. the scalar sparse-Newton frontier: a dimension-independent classical
   sparse-SQ estimator, matching separate exponential local-walk and statistical
   lower bounds, a finite-bit rational box-LP realization, and the separate
   exact \(\widetilde\Theta(\alpha\kappa/\epsilon)\) frontier for plain
   block-encoding access;
3. the independently audited thresholded-Forrelation XOR theorem: a
   constant-size linear threshold compiler turns each interval-promised
   inverse observable into an exact optimizer bit, and a public XOR-polytope
   chain compresses \(T\) such bits into one bounded coordinate of the unique
   optimizer.  The sparse LP has certified scalar-log barrier parameter
   \(12T-4\) and matched same-instance complexity
   \[
      Q=\Theta(T),\qquad
      R=\Omega\!\left(Tq^{\ell/2}/(r\ell)\right).
   \]
   This is the first result in the ledger to retain the full \(T\) factor for
   constant-accuracy output of one bounded scalar, rather than a checkpoint
   trace or a normalized mean.  The scale-weighted version remains an
   endpoint theorem with an exponentially fine objective-gap transfer;
   equal weights give a constant-gap transfer but no separated chronology.
   Neither version lower-bounds a normalized solution-state amplitude or
   proves an unavoidable charge at every IPM iteration;
4. the independently audited one-Lorentz readout hierarchy: already on one
   growing Lorentz cone with a public orthonormal two-sparse slice, the
   standard restricted barrier has constant parameter one, and at one
   public central multiplier the reduced Hessian has condition at most
   \(3/\sqrt5\), latent treewidth one, and a linear classical solve. For
   public raw objective norm \(C\), the ordinary optimum value and its
   ordinary value at the exact central point have the matched arbitrary-input
   accuracy laws
   \[
    Q=\Theta(\min\{N,C/\epsilon\}),\qquad
    R=\Theta(\min\{N,(C/\epsilon)^2\}).
   \]
   Thus \(C=N\) gives \(Q=R=\Theta(N)\) at constant additive accuracy,
   while \(C=1\) gives the normalized inverse-accuracy frontier. Explicit
   output of gap \(O(C/N)\) is query-linear. In contrast, normalized
   optimizer and central states are constant-query easy, and the unique-mark
   promise at accuracy \(O(C/N)\) gives the sharp
   \(\Theta(\sqrt N)\)-versus-\(\Theta(N)\) Grover separation. An equivalent
   encoding makes the objective completely public and moves every hidden
   bit into a disjoint two-sparse equality row; its hidden slice has
   condition one and entirely public row norms, singular values, column
   degrees, and SQ sampling law. Its nullspace basis is hidden but
   one-query coherently accessible. This
   supersedes any suggestion that the readout law is driven by a growing
   product barrier. On the same direct-ball instances, the fixed barrier
   additionally forces
   \(\Omega_{\rho,R,m}(\log(C/\epsilon))\) feasible bounded-Dikin rounds
   from the analytic center. The product-disk theorem remains the
   bounded-\(Q_3\), analytically minimal \(Q_3\)-full-slack companion; its one-factor
   PSD packing gives a distinct same-instance synthesis with
   \(L=1\), \(\nu_{\rm slice}=N\), latent projected Newton treewidth one,
   a one-query normalized projected center, \(\Omega(N)\) scalar/full-output
   queries, and
   \(\Omega_{\rho,R,m}(\sqrt N\log(N/\epsilon))\) bounded-Dikin rounds
   for the fixed restricted log-determinant. Adding the disjoint hidden
   sign slice inside this packed lift makes the objective public and retains
   the same fixed-accuracy joint ledger. The cleaner
   [one-sharing-cone synthesis](2026-09-04-one-sharing-cone-disk-qipm-separation.md)
   realizes the public-objective hidden-equality family directly on the
   single nonsymmetric cone \(\mathcal H_{N,2}\), of dimension \(2N+1\).
   Its explicit optimal barrier has ambient parameter \(N+1\) and restricts
   exactly to the standard product-disk barrier of parameter \(N\).
   For that barrier, the projected central and predictor-Newton states are
   \(O(1)\)-query preparable and the diagonal projected Newton condition is
   at most four, while constant-accuracy scalar/full classical readout is
   \(\Theta(N)\). In addition, every ambient LHSC barrier on the same cone
   forces
   \(\Omega_{R,m}(\sqrt N\log(N/\epsilon))\) primal--dual bounded-Dikin
   rounds from its exact central point at the public multiplier
   \(2\sqrt5\) to a strictly feasible \(\epsilon\)-gap output. The
   easy-state claim is not made for those arbitrary barriers.
   These query and movement costs
   are simultaneous, never multiplicative. The independently audited
   [fixed-instance sparse-KKT temporal-collapse
   theorem](2026-09-04-fixed-instance-sparse-kkt-temporal-collapse.md)
   shows that this is a real obstruction, not merely caution: on a
   one-Lorentz ellipsoid, a literal constant-width augmented KKT state can
   be \(\Theta(L)\)-query hard at every checkpoint while remaining exactly
   the same normalized state throughout an
   \(\Omega(\log(1/\epsilon))\)-move path. A single \(O(L)\) signed-tree
   solve serves every checkpoint. Thus even repeated one-shot KKT hardness
   does not compose with movement absent a joint adversary and an output,
   online, revocation, or memory contract.
   Essential scope remains:
   the cone dimension grows; arbitrary unitary completions and free
   hidden-dependent projected norms or a free classical hidden nullspace
   basis are excluded; a constant
   local-neighborhood guarantee alone does not imply the scalar accuracy;
   the primal movement theorems cover fixed restricted barriers, while the
   arbitrary-barrier extension requires an ambient LHSC primal--dual
   product metric, an exact central start, a strictly feasible gap-certified
   output, and bounded chords; and no oracle-query lower bound is inferred
   from \(\nu\);
5. the SOCP eccentricity-profile and latent-treewidth theorems: exact
   treatment of only the \(b\) eccentric Lorentz blocks gives a
   rank-\(2b\) preconditioner, condition at most \(\theta^2\), and a
   treewidth-parametric near-linear classical solve; a matching genuine-cone
   witness proves rank \(2b\) is worst-case necessary for this condition
   target.  Independently, two hub variables per Lorentz block expose a
   fixed rank-expanded graph whose width, rather than the arbitrarily large
   clique in the materialized Hessian, controls exact elimination.  Together
   these results give complementary matched-access full-output QIPM exclusion
   criteria, an order-statistic complexity envelope, and a concrete warning
   that three-dimensional norm-tree splitting can worsen the barrier count
   without improving structured Newton work.  The warning is now
   formulation-independent within ambient Lorentz-product barriers:
   \(\sum_j(m_j-2)\geq k(s-1)\) for every joint exact Lorentz lift of
   \(Q_{s+1}^k\), so pure-\(Q_3\) formulations cannot share factors to beat
   the norm-tree count.  For one \(N\)-ball this becomes an exact
   no-free-lunch theorem: direct \(Q_{N+1}\), the minimum \(Q_3^{N-1}\)
   norm tree, and the minimum smooth \(Q_3^N\) coordinate lift all have
   linear exact Newton solves (latent widths one, one, and two), while their
   optimal ambient barrier parameters are respectively \(2\), \(2N-2\),
   and \(2N\).  The independently audited PSD packing theorem shows the
   same phenomenon survives maximal higher-rank sharing: balanced
   column-packed blocks attain the curvature-capacity resource scales, but
   exact auxiliary elimination turns their central Newton system into a
   packing-independent forest with linear projected solve work.  Even a
   single PSD factor shared by every product-ball row creates no cross-ball
   reduced edge.  The audited matched-oracle follow-up proves the stronger
   quantum statement: after exact fiber centering, packed PSD and grouped
   Lorentz formulations have identical complete reduced Newton oracles and
   projected solution states, so their state-generation query complexities
   are equal in both directions; factor count cannot create a speedup
   without changing the access or output contract.  Its audited off-center
   completion identifies the exact missing parameter: relative auxiliary
   fiber eccentricity gives a squared preconditioning transfer, whereas a
   two-source correlation family makes the packed projected condition
   diverge and its Newton state stay constantly separated while the
   projected point and centered Lorentz condition remain fixed.  Thus
   projected centrality alone is insufficient.  Its audited implicit
   recentering companion gives the matching positive result: the exact
   center has an \(O(bs)\), packing-independent factorized compiler, and a
   fiber residual \(\delta\) gives condition overhead
   \(((1+\delta)/(1-\delta))^2\).  Quantum compilation needs radial-scale
   metadata: it is impossible from a normalized projected state alone and
   Grover-hard from raw coordinates, while a maintained scale oracle makes
   each centered diagonal query constant-cost. The dynamic access companion
   makes the maintenance charge exact for fresh hidden-support batches: a
   universal service with \(r_t\) uses at epoch \(t\) costs
   \(\Theta(\sqrt s\sum_t\min\{r_t,b\})\) quantum queries, interpolating
   between raw-backed evaluation and full scale compilation. Explicit
   sparse-list updates instead admit support-linear maintenance, and a
   fixed QIPM trajectory does not inherit the fresh-batch direct sum. The finite-precision claim
   remains conditional on stable product-form updates or certified
   regularization and refinement;
6. the tilted-jet exponential-cone compiler and its certified entropic-risk
   application, including matched \(e^K/\epsilon\) quantum versus
   \(e^{2K}/\epsilon^2\) classical source laws, a sharp reusable positive-
   atom support minimax theorem, and the audited fixed-factor multivariate
   extension with the genuine \(e^{rK}\) exponent; the growing-factor
   refinement removes the former \(r^r\) query overhead, while its audited
   Rademacher fallback is dimension-free in both source queries and
   scenario-induced cone count at bounded dual width \(B=rK\), subject to
   full-vector access and dimension-linear atom representation; an audited
   \(\Omega(B^2/\epsilon)\) signed exponential-rank lower bound makes the
   open bounded-width coherent
   \(\widetilde O_B(1/\epsilon)\) target output-optimal in accuracy; and
7. the sharp all-coherent normalized-shift staircase and joint gap--accuracy
   law, including exact thresholds, the arbitrary-completion converter lower
   bound, and the generalized-QSP versus QSVT polynomial separation; and
8. the independently audited
   [sharp spectral-ball subgeodesicity theorem](2026-09-04-spectral-ball-sharp-subgeodesicity.md):
   exact standard-barrier distance in transformed singular coordinates,
   exact objective-sublevel water filling, a matched characterization of
   optimal arbitrary bounded-Dikin moves, and a sharp
   \(\Theta(\sqrt{\log r})\) central-path arclength tax.  Its multiscale
   family also gives a genuine round separation: fixed-radius
   central-neighborhood sequences started at the analytic center—including
   those satisfying a fixed
   Newton decrement \(\lambda\leq\beta<1/2\)—require
   \(\Omega_{R,\beta}(r\log r)\) rounds before actual
   \(\epsilon\)-accuracy, versus
   \(\Theta_R(r\sqrt{\log r})\) optimal noncentral moves.  The result is
   unchanged if the reference central parameters move backward, and it
   assumes no terminal-label progress.  It is
   exact for the explicit unconstrained standard-barrier family and pooled
   products; it is not a generic affine-constrained IPM or QIPM runtime
   claim.

The trajectory direct sums, sparse-LP access separation, one-cone SOCP
transfers, and Lorentz one-step dequantization are strong supporting
theorems.  The affine-slice \(\nu=1\) LP lower is deliberately scoped as
nullspace-preprocessing hardness, and the SOCP trajectory lower distinguishes
formulation/dynamic-access costs from a local diagnostic with a freely given
iterate SQ interface.  Older dilation-rank/QRE barrier components are prior
art and should not be used as headline novelty.
The exact exponential-product and positive-output relative-entropy theorem
is likewise a supporting formulation result, not a strongest publication
candidate: its exact constants and \(\sqrt{3/2}\) aggregation ceiling are
useful for sparse-QIPM accounting, but the proofs are short specializations
of Fawzi--Saunderson's published compatibility and recession-certificate
machinery.

### Audited supporting corollary: spectrum at a degenerate LP vertex

**Status:** Proved and independently audited; a decisive classical antecedent
was found. The complete audit, a nonuniformity example, and primary-source
screen are in
[the standalone note](2026-09-04-degenerate-lp-reduced-hessian-limit.md).
The result resolves the mathematical part of open problem G1 in
`paper/sections/16-discussion.tex` and corrects Section 4's restriction to
nondegenerate unique optima, but it is not standalone novelty. Adler and
Monteiro's 1991 Theorems 3.3 and 5.1 already give the dual analytic-center
limit and \(x_N(\mu)/\mu\to(s_N^a)^{-1}\), from which the compression formula
below follows immediately.

Consider the primal--dual pair

\[
 \min\{c^Tx:Ax=b,\ x\geq0\},\qquad
 A^Ty+s=c,\ s\geq0,
\]

where \(A\in\mathbb R^{m\times n}\) has full row rank and the primal and dual
are strictly feasible. Suppose the primal optimum \(x^*\) is a unique vertex;
it need not be nondegenerate. Let

\[
 B=\{i:x_i^*>0\},\qquad N=[n]\setminus B.
\]

Let \((x(\mu),y(\mu),s(\mu))\) be the canonical logarithmic central path,
so \(x_i(\mu)s_i(\mu)=\mu\). Let \(s^a\) be its dual limit. Equivalently,
\(s^a\) is the relative analytic-center slack of the dual optimal face. In
particular,

\[
 s_B^a=0,\qquad s_N^a>0.
\]

If \(W\) has orthonormal columns spanning \(\ker A\), then the equality-reduced
primal log-barrier Hessian

\[
 H_{\rm red}(\mu)=W^T\operatorname{Diag}(x(\mu)^{-2})W
\]

obeys the operator-norm limit

\[
 \boxed{\quad
 \mu^2H_{\rm red}(\mu)\longrightarrow
 L:=W^T\operatorname{Diag}((s^a)^2)W\succ0.
 \quad}
\]

Consequently, for every ordered eigenvalue,

\[
 \mu^2\lambda_j(H_{\rm red}(\mu))\to\lambda_j(L),
 \qquad
 \kappa(H_{\rm red}(\mu))\to\kappa(L)<\infty.
\]

Thus degeneracy of a unique vertex does not merely preserve bounded reduced
conditioning: its complete limiting spectrum is the compression to the
tangent space of the squared relative-analytic-center reduced-cost vector.

#### Proof

Complementarity gives the exact identity

\[
 \mu^2H_{\rm red}(\mu)
 =W^T\operatorname{Diag}(s(\mu)^2)W.
\]

The standard central-path convergence theorem gives \(s(\mu)\to s^a\), hence
the asserted operator-norm limit. It remains only to show that \(L\) is
positive definite, which is the point at which uniqueness replaces
nondegeneracy.

Take \(z\in\ker A\) with
\(z^T\operatorname{Diag}((s^a)^2)z=0\). Because \(s_N^a>0\), this forces
\(z_N=0\). Therefore \(A_Bz_B=0\). But \(A_B\) has full column rank: if
\(A_Bv=0\) for a nonzero \(v\), then, since \(x_B^*>0\), both
\(x_B^*+tv\) and \(x_B^*-tv\) are positive for sufficiently small \(t>0\);
with the zero coordinates fixed on \(N\), these are two distinct feasible
points. Moreover every feasible point supported on \(B\) has the same
objective value, because dual optimality gives

\[
 c_B^Tv=(A_B^Ty^*)^Tv=(y^*)^TA_Bv=0.
\]

This would contradict uniqueness of \(x^*\). Hence \(z=0\). Applying this to
\(z=Wu\) proves \(L\succ0\). Continuity of ordered eigenvalues and of the
condition number on the positive-definite cone proves the remaining claims.

#### Direct active-set formula for the dual limit

The vector \(s^a\) is determined without following the central path. It is the
unique slack vector associated with the solution of

\[
 \max_y\ \sum_{i\in N}\log(c_i-a_i^Ty)
 \quad\text{subject to}\quad
 A_B^Ty=c_B,\quad c_N-A_N^Ty>0,
\]

with \(s_N^a=c_N-A_N^Ty^a\). Under the stated full-row-rank assumption,
\(A^T\) is injective, so \(y^a\) is unique as well. If redundant equality
rows are retained instead, only the resulting slack vector is intrinsic and
unique. This gives a finite-dimensional active-set/reduced-cost
characterization of every limiting eigenvalue.

Let \(R_N\) restrict a vector to the zero coordinates and put

\[
 \sigma_N=\sigma_{\min}(R_NW)>0,\qquad
 \rho_N=\|R_NW\|_2\leq1.
\]

Positivity of \(\sigma_N\) is equivalent to the uniqueness argument in the
proof. If
\(s_{\min}=\min_{i\in N}s_i^a\) and
\(s_{\max}=\max_{i\in N}s_i^a\), then

\[
 s_{\min}^2\sigma_N^2\leq\lambda_{\min}(L)
 \leq s_{\max}^2\sigma_N^2,
\]

\[
 s_{\min}^2\rho_N^2\leq\lambda_{\max}(L)
 \leq s_{\max}^2\rho_N^2.
\]

Therefore

\[
 \left(\frac{s_{\min}}{s_{\max}}\right)^2
 \left(\frac{\rho_N}{\sigma_N}\right)^2
 \leq\kappa(L)\leq
 \left(\frac{s_{\max}}{s_{\min}}\right)^2
 \left(\frac{\rho_N}{\sigma_N}\right)^2.
\]

This separates the limiting condition number into a reduced-cost spread and
the angle between the tangent space and the coordinate subspace supported on
\(B\). It extends the usual \(A_B^{-1}A_N\) estimate to rectangular
full-column-rank \(A_B\), which is precisely the degenerate-vertex case.

#### Scope and prior-art boundary

The limit concerns the orthonormal-tangent reduced primal Hessian, not the
normal equations or the full primal--dual KKT matrix. The argument uses the
canonical log barrier and exact centrality. The limit is an immediate matrix
corollary of [Adler--Monteiro
1991](https://doi.org/10.1007/BF01594923), pp. 40 and 44--45, and should not
be advertised as novel. The exact orthonormal compression and the two-sided
condition-number bounds remain useful packaging. Moreover, the limiting
constant is not uniform: the standalone note gives a four-variable sparse
degenerate LP with \(\mu^2H_{\rm red}=\operatorname{Diag}(1,M^2)\) exactly.
Thus the result removes accuracy-driven condition growth for each fixed
instance but gives no dimension-, bit-length-, or data-independent QIPM
complexity bound.

#### Degenerate numerical witness

Take

\[
 A=\begin{bmatrix}1&1&1&1\\0&1&3/2&3\end{bmatrix},\quad
 b=\binom1{3/2},\quad c=(1,1,0,1)^T.
\]

The unique optimum is \(x^*=e_3\), so \(|B|=1<m=2\): the optimal vertex is
degenerate, while positive feasible points exist. Writing the dual analytic
center as \(y=(-3t/2,t)\), its nonzero slacks are

\[
 (s_1^a,s_2^a,s_4^a)=(1+3t/2,1+t/2,1-3t/2),\qquad
 t=\frac{-6+4\sqrt3}{9}.
\]

An SVD-generated orthonormal basis of \(\ker A\) gives
\(\operatorname{spec}(L)\approx(0.24888160,1.14289062)\), hence the predicted
limit \(\kappa(H_{\rm red}(\mu))\to4.59210571\). This is only a numerical
check of the displayed closed-form theorem, not part of its proof.
