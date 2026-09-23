# Continuing frontier: sparse quantum interior-point methods

Date: 2026-09-02

This is the live ledger for the research cycle requested after the coupling,
effective-dimension, and stable-active-subspace results.  Those earlier results,
and every other theorem already in `notes/`, are treated as prior work rather
than candidates for rediscovery.

The final disposition of every live direction, including prior-art collisions,
dead ends, conditional modules, and genuinely open programs, is recorded in
`2026-09-02-research-closure-and-open-frontier.md`.

## Cycle verdict

The first pass promoted two results to dedicated notes:

1. `2026-09-02-newton-state-output-interface-lower-bounds.md`: a worst-case
   tight normalization--query product lower bound for converting a Newton state
   into a reusable diagonal block encoding, plus an
   \(\Omega(\sqrt n/\mu)\) centrality-test lower bound on feasible triples of a
   fixed one-sparse strictly complementary LP.
2. `2026-09-02-sdp-newton-rank-progress-barrier.md`: a coordinate-invariant
   Schatten rank--progress theorem for NT-scaled SDP directions, with a
   treewidth-one path-Laplacian witness having a rank-one optimum but
   \(\Omega(n)\) NT approximate direction rank.

The positive projective lazy-refresh theorem is in
`2026-09-02-projective-lazy-quantum-newton-refresh.md`.  The exact tall-LP
crossover was proved but downgraded after a stronger exact Clarkson/oracle
literature collision; it remains a supporting QIPM module rather than a main
complexity result.

## Later-cycle results

The continuing search produced the audited results and limitations catalogued
below.

1. `2026-09-02-parity-amplified-primal-state-lower-bound.md` began the
   representation-independent lower-bound line in this cycle.  A
   fixed-support LP family with row and column sparsity at most four has a
   unique nondegenerate strictly complementary optimum and a condition-one
   reduced primal-barrier Hessian along its entire central path.  Nevertheless,
   preparing a constant-trace-error amplitude encoding of **any exactly
   feasible primal point** needs \(\Omega(N)\) standard coefficient queries.
   This includes every relative objective-gap promise and every fixed-parameter
   central point.  A bounded-degree copy tree and local upper-bound slacks make
   one fixed measurement recover parity, so this is neither an output-length
   nor a tomography lower bound.  The original equality-normal representation
   is not uniformly conditioned, and exact feasibility is essential; the
   theorem isolates hard feasible-state construction despite trivial reduced
   Newton geometry.
   A robust parallel-path extension removes exact feasibility at a quadratic
   size cost.  For \(P=33N^2-1\) nodes (and \(4P\) nonnegative variables), it
   retains fixed support, row/column degree at most four, full row rank, a
   unique nondegenerate strictly complementary optimum, and a scalar-identity
   reduced Hessian.  Yet producing a constant-trace-error state of **any**
   nonnegative vector with relative equality residual at most \(1/200\)
   needs \(\Omega(N)=\Omega(\sqrt P)\) coefficient queries, even without an
   objective-gap promise.  The \(N\) parallel length-\(N\) paths give constant
   effective conductance; a stability lemma forces a constant fraction of the
   endpoint mass to retain parity.  A matching drift example proves why the
   original one-path copy amplifier cannot tolerate constant \(\ell_2\)
   residual.  An effective-resistance converse shows that the quadratic size
   is optimal for bounded-degree signed-edge propagation: if each edge
   coefficient depends on at most \(k\) input signs and each output carries
   their full parity, constant residual soundness requires
   \(\Omega(N^2/k^2)\) vertices.  Thus constant-\(k\) expanderization cannot
   produce a near-linear robust gadget in this model.
   The stronger 2026-09-02-linear-size-robust-gain-parity-lp.md leaves the
   unit-modulus class through a short gain-two prefix and a height
   \(H=\Theta(\sqrt N)\) plateau.  It has only \(P=17N+1\) nodes,
   coefficients at most two, row/column degree at most four, and polynomial
   solution range.  Producing a trace-\(1/100\) state of **any** nonnegative
   vector with relative residual at most \(1/100\) requires the optimal
   \(\Omega(N)=\Omega(P)\) coefficient queries.  Its public reduced
   primal-barrier Hessian has condition below \(7/6\) throughout
   \(0<\mu\le1/16\), so every exact central state on that whole late tail is
   also linearly hard.  A sharp path-bundle frontier
   \(PH^2=\Omega(N^2)\) explains the trade: bounded height needs quadratic
   volume, whereas linear volume needs \(H=\Omega(\sqrt N)\), which the new
   family attains.
   The later `2026-09-02-prefix-rigidified-condition-one-newton-hardness.md`
   is now the strongest theorem in this line.  Adding only
   \(T=O(\log N)\) public three-sparse rows removes the small-height prefix
   null modes.  The augmented LP remains linear-size, bounded-coefficient,
   and row/column-four-sparse, but its **complete reduced primal barrier
   Hessian is a scalar identity along the entire central path**.  Its reduced
   Newton matrix at a public complementarity-centered infeasible start is
   also scalar.  All Newton right-hand sides are public, one standard
   \(\sigma=1/2\) correction lands at a genuine common-\(\mu=1/16\) central
   point, and the fraction-to-boundary test permits the full step.
   Nevertheless, preparing the normalized original-primal direction—or any
   nonnegative original-primal state with relative residual at most
   \(1/100\)—requires \(\Omega(P)\) raw coefficient queries.  Independent
   algebraic, numerical, hostile-referee, and primary-literature audits found
   no exact collision.  This is an affine-loading/recovery separation, not a
   condition-one QLS lower bound and not a new sparse-LP lower-bound exponent.
   The general-graph converse in
   `2026-09-02-cut-resistance-frontier-signed-parity-lps.md` extends the
   path-bundle calculation: for every cycle-consistent local signed-equality
   gadget, constant amplified-output residual soundness requires
   \(MB^2H^2=\Omega(N^2)\).  Thus the gain--plateau height is optimal
   throughout that graph class.  The theorem does not cover arbitrary
   multi-variable sparse constraints or assert that the entire adversarial
   approximate state is parity-free.
2. `2026-09-02-newton-state-output-interface-lower-bounds.md` was strengthened
   in three ways.  Its equal-norm one-sparse LP pair now gives an end-to-end
   scalar-value lower bound \(\Omega(\sqrt n/\mu)\) for a normalized-objective-
   state input interface at the natural \(n\mu\) duality-gap scale.  A separate
   compiler-free theorem shows that turning a near-uniform iterate state into
   the solution state of the next one-sparse, condition-below-two diagonal
   system costs \(\Omega(\sqrt n)\).  These costs add over an explicitly online
   fresh-oracle stream, but the note proves why this does not yet imply a
   \(T\sqrt n\) lower bound for one fixed LP.
3. `2026-09-02-projective-lazy-quantum-newton-refresh.md` proves that the
   normalized exact-centering solution ray of every fixed strictly feasible LP
   has finite projective variation on the strict-complementarity tail.  A new
   one-sided cross-gain bound remains uniform in the direction in which an IPM
   approaches the optimum even though \(\kappa(H_\mu)=\Theta(\mu^{-2})\).
   Hence the number of expensive QLSA/tomography refreshes can be independent
   of final precision under a fixed residual contract.  This is an exact
   central-trajectory theorem.  The later sparse cycling witness shows that a
   standard feasible \(N_2(\theta)\) neighborhood does not imply the needed
   finite-refresh property; a realized-trajectory speedup requires the
   face-leakage or normalized-forcing controls stated later in this ledger.
4. `2026-09-02-implicit-dual-coordinate-oracle-qipm.md` gives a concrete escape
   from the state-to-diagonal obstruction.  Store the explicit \(m\)-dimensional
   dual iterate and compute every slack \(s_i=c_i-a_i^Ty\) coherently from a
   static sparse-column oracle.  This composes exactly across iterations and
   removes an \(n\)-coordinate changing-diagonal refresh, while retaining all
   block-encoding normalization, RHS cancellation, tomography, and coherent-
   memory costs in the ledger.
5. `2026-09-02-projective-lazy-quantum-newton-refresh.md` now also identifies
   the exact boundary of its positive theorem.  On the exact strictly
   complementary central path, the OSS solution ray has finite tail variation
   and bounded ordered cross-gain.  But a row-three-sparse LP admits feasible
   short-step iterates in the standard \(N_2(\theta)\) neighborhood whose OSS
   residuals are only \(O(\mu/\sqrt n)\) and whose direction rays cycle by
   \(\Omega(1/\sqrt n)\) per iteration.  Over
   \(T=\Theta(\sqrt n\log(1/\epsilon))\) iterations this gives
   \(\Omega(\log(1/\epsilon))\) projective variation.  Thus ordinary published
   inexact-feasible residual conditions do not imply precision-independent
   refresh; a face-tangent accuracy or coherent direction-selection condition
   is genuinely necessary.  A later proximal audit proves that ordinary
   Tikhonov or ray locking does not supply that condition: on a weak face mode
   of singular value \(\Theta(\mu)\), movement toward the exact direction and
   the unresolved OSS residual have the complementary filters
   \(\sigma^2/(\sigma^2+\lambda)\) and
   \(\lambda\sigma/(\sigma^2+\lambda)\).  The same sparse three-phase family
   forces either non-summable ray motion or violation of the accepted OSS
   residual.  Proximal selection is positive only after a checkpoint ray is
   already inside the current residual tube, where direct certified reuse
   needs no proximal solve.  The same note now gives the sharp replacement:
   two explicit projected residual moments \(g_p,g_d\) are amplified by exactly
   \(1/\mu\) along the primal and dual optimal faces.  The summability ledger
   \(\sum_t(\|g_p(r_t)\|+\|g_d(r_t)\|)/\mu_t<\infty\) is worst-case sharp;
   \(O(\mu^2)\) projected error is sufficient but not necessary.  An exact
   feasibility-preserving correction removes both modes and makes the
   restricted OSS inverse uniformly bounded, at the cost of knowing the
   optimal partition and solving in the two face subspaces.
   The follow-up 2026-09-02-partition-free-spectral-face-repair.md removes that
   supplied partition assumption on a strict-complementarity tail.  The
   coherent comparison \(E_{ii}=\mathbf1\{x_i\ge s_i\}\) identifies the optimal
   partition with constant absolute margin, and QSVT constructs the active
   range and both basis-free repair projectors with no polynomial
   \(1/\mu\) factor.  It also makes stable active-range equilibration fully
   constructible from current \(A,X,S\).  A row-two-sparse witness proves that
   unfiltered or Tikhonov global repair restores respectively
   \(\Theta(1/\mu)\) or \(\Omega(1/(\delta\mu^2))\) conditioning.  The remaining
   end-to-end obstruction is output: generic classical correction tomography
   at the summable leakage scale costs
   \(\widetilde\Theta(d/(\tau\mu))\).
6. `2026-09-02-congruence-condition-recovery-frontier.md` extends the earlier
   power-scaling example to every scalar block SPD congruence
   \(T_\mu=t_UQ+t_KR\).  With \(r=t_U/t_K\), the square-root condition cost is
   \(\Theta(\max\{r/\mu,\mu/r\})\), while inverse-amplitude recovery and local
   normalized-state sensitivity are both
   \(\Theta(\max\{r,r^{-1}\})\).  Their product is always
   \(\Omega(1/\mu)\), and a fixed two-sparse LP matches every regime.
7. `2026-09-02-projective-implicit-oracle-combination.md` combines projective
   checkpoints with implicit dual-coordinate access.  Storing
   \(y_t=y_0+\sum_{r\le R}\theta_{r,t}\widehat z_r\) reduces trajectory writes
   to \(\widetilde O(RmB+TB)\), with coherent slack queries costing
   \(O(d_cR)\).  A tall-expander candidate does not yield an end-to-end quantum
   advantage: bounded normalization also lets a classical randomized sketch
   approximate the inactive Hessian in \(\widetilde O(m)\) work, while rare
   influential columns either make the quantum normalization linear in the
   tallness or leave only a one-time Grover preprocessing gain.
8. `2026-09-02-parity-preconditioner-dichotomy.md` separates construction,
   conditioning, and application.  Every input-independent SPD preconditioner
   has worst-case condition number \(\Omega(N^2)\) on two signed-path inputs.
   A data-dependent signed-incidence factor is locally constructible and makes
   the normal matrix exactly identity (and the block-preconditioned KKT matrix
   condition \(\varphi^2\)), but preparing its transformed Newton RHS needs
   \(\Omega(N)\) coefficient queries.  The hard vector is the actual
   infeasible-start correction RHS at \(x=s=\mathbf1,y=0,\mu=1\).  Hence the
   family proves a condition--application/loading dichotomy, not a false
   preconditioner-construction lower bound.  The full Newton step lands exactly
   on the hard feasible central state at \(\mu=3/4\).  Consequently every
   possibly data-dependent factor obeys the invariant end-to-end accounting
   bound
   \(Q_{\rm set}+Q_{\rm rhs}+Q_{\rm solve}+Q_{\rm rec}=\Omega(N)\).
   For a block-encoded solve with condition \(K\), per-call raw cost
   \(q_{\rm on}\), and polylogarithmic factor \(L\), either a noniterative phase
   costs \(\Omega(N)\) or \(Kq_{\rm on}=\Omega(N/L)\).  A stronger
   condition-only or transformed-RHS-only claim is false because an
   input-dependent orthogonal factor can move parity among RHS preparation and
   recovery.
9. `2026-09-02-linear-plateau-full-kkt-lower-bound.md` upgrades the output
   contract from a primal block to a full primal--dual Newton direction.  At
   the public all-ones complementarity-centered start, the entire untransformed
   KKT right-hand side is sign-independent.  A fixed multiplier-block
   interference observable and the polynomial method give the exact lower
   bound \(Q\ge N/2=\Omega(P)\) for one constant-error full-direction state.
   Exact Schur preconditioning transforms the two-block KKT matrix to absolute
   condition \(\varphi^2\).  Even a state of any \(10^{-3}\)-relative-residual
   transformed solution, with trace error \(1/200\), still needs \(N/2\) total
   raw queries when preconditioner construction, transformed-RHS preparation,
   block encoding, and recovery are all charged.  This constant-conditioned
   result also transfers to the prefix-rigidified family.  The φ² spectrum
   and Schur preconditioning are classical; the apparently new part is the
   public-RHS LP Newton instantiation and end-to-end residual-robust query
   theorem.
10. `2026-09-02-prefix-rigidified-access-normalized-separation.md` pinpoints
    the hard stage in a canonical gauge.  In the Moore--Penrose decomposition
    \(\Delta x=p_\sigma+Wz\), the reduced equation is a public scalar identity:
    its condition, inverse-state factor, two-inverse filter factor, RHS state,
    solution state, and orthogonal recovery all cost zero or constant raw
    queries.  In contrast, preparing
    \(p_\sigma=(A'_\sigma)^\dagger(b'-A'_\sigma x^0)\) has tight
    \(\Theta(P)\) coefficient-query complexity.  Thus affine feasibility
    correction, rather than the reduced inverse, carries the whole exponent.
11. `2026-09-02-convex-mixture-local-input-obstruction.md` gives a
    graph-independent optimality frontier.  Averaging exact witnesses from the
    \(N\) single-bit-flipped neighboring instances preserves nonnegativity,
    a common objective value, and any mixture-stable wrong-parity output, while
    producing residual at most
    \(2BH\sqrt{sM_{\rm dep}}/N\).  Hence constant robust soundness forces
    \(M_{\rm dep}B^2H^2=\Omega(N^2)\) at constant row sparsity and RHS norm.
    This rules out linear-size bounded-range LDPC/expander repairs throughout
    the one-bit-local sparse linear model, not merely signed graphs.  The
    amplitude-state corollary requires a pair-margin or common padded-output
    condition; no claim is made for arbitrary quadratic decoders.
12. The companion 2026-09-02-single-flip-mixture-frontier-sparse-lps.md is the
    multi-bit and primal--dual supplement. Its stationarity-preserving
    central-mixture theorem gives simultaneous \(O(N^{-1/2})\) primal and
    dual residuals, exact algebraic gap \(n\mu\), and complementarity defect
    \[
      \frac{\bar x_j\bar s_j}{\mu}-1
      =\frac1{2N^2}\sum_{i,k}
       \frac{(x_j^{(i)}-x_j^{(k)})^2}{x_j^{(i)}x_j^{(k)}}.
    \]
    A neighbor coordinate ratio at most \(R\) gives central-neighborhood width
    \((R-1)^2/(4R)\). Weighted mixtures give a sharp incidence-energy versus
    multiplicative-variance tradeoff, and a unit-bounded diagonal witness
    proves that some neighbor-stability hypothesis is necessary.
13. `2026-09-02-bounded-range-exact-only-condition-one-hardness.md` realizes
    the sharp bounded-range escape from the mixture obstruction.  It has
    linear size, coefficient magnitude at most two, bounded feasible primal
    range, public data, and an exactly scalar reduced Hessian on the whole
    central path.  Exact central and public-start Newton-direction states need
    \(\Omega(P)\) raw queries.  More strongly, every nonnegative point with
    \(\|Ax-b\|_2\le1/(100\sqrt N)\) has constant correct-parity amplitude
    bias, so preparing a state of *any* vector in this residual tube is still
    \(\Omega(P)\)-hard.  A wrong-output neighbor mixture at residual
    \(2/\sqrt N\), and a zero-signal drift at \(1/\sqrt N\), make the
    absolute and relative \(N^{-1/2}\) exponent sharp for this family.
    Homogeneous prefix rigidification preserves \(\|b\|_2=\sqrt2\) and makes
    the wrong-output mixture exactly dual feasible and exactly complementary.
    Tuning the hidden length gives the accuracy curves
    \(Q_{\rm abs}(P,\epsilon)=
      \Omega(\min\{P,\epsilon^{-2}\})\) and
    \(Q_{\rm rel}(P,\eta)=
      \Omega(\min\{P,\eta^{-2}\})\).  This is a family reparameterization,
    not a progressive lower bound for one fixed LP.
14. `2026-09-02-schur-factor-access-normalization-frontier.md` proves the
    sharp plateau-factor curve
    \(\alpha_P\sqrt K=\Omega(N)\), matched by spectral clipping, and the
    preprocessing-aware reusable-inverse bound
    \(Ns+q\alpha=\Omega(N^2)\).  The general separate-factor warning is prior
    work; the apparently new content is the explicit tight plateau
    interpolation and raw-input setup/per-call product.  No analogous bound is
    possible for a freely supplied already-preconditioned product, since its
    input-dependent gauge may have been compiled into the oracle.
15. `2026-09-02-dual-homogeneity-bounded-full-kkt-lower-bound.md` proves a
    general homogeneity transfer lemma: scaling
    \((c,y^0,s^0,\widehat\mu)\) by \(\lambda\) leaves \(\Delta x\) unchanged
    and scales \((\Delta y,\Delta s)\) by \(\lambda\).  At \(\lambda=1/P\),
    the unit-height parity LP has a complete \(11P\)-coordinate Newton target
    with every coordinate \(O(1)\), norm \(\Theta(\sqrt P)\), public RHS, and
    canonical block-encoding normalization five, yet its state needs
    \(\Omega(P)\) raw or canonical block-encoding queries.  The exact
    representation-dependent law
    \(\alpha_j=(32/9)\mu\tau_j(P-j)\) shows why bounded multipliers force
    \(\mu=O(1/P)\) on this scaling ray.  Both raw full KKT matrices have
    \(\kappa_2=\Theta(P)\), so the theorem is not condition independent: it
    trades dual accumulation for inverse complementarity scale and
    \(O(1/P)\) numerical accuracy.
16. The note `2026-09-02-sdp-central-mixture-kantorovich.md` proves the
    noncommutative SDP extension. For neighboring exact SDP centers
    \(S_i=\mu X_i^{-1}\) with \(mI\preceq X_i\preceq MI\), their averages obey
    \[
      I\preceq
      \bar X^{1/2}(\bar S/\mu)\bar X^{1/2}
      \preceq\frac{(R+1)^2}{4R}I,\qquad R=M/m.
    \]
    An exact PSD matrix-variance identity quantifies the Jensen gap without
    assuming commutativity. It also gives the instance-specific alternatives
    \(\|Z-I\|_F\le m^{-2}N^{-1}\sum_i\|X_i-\bar X\|_F^2\) and its
    operator-norm analogue. These can avoid the generic \(\sqrt r\) loss:
    using only the global ratio, a fixed-width Frobenius neighborhood forces
    \(\log R=O(r^{-1/4})\), whereas small actual Frobenius variance suffices
    without that explicit dimensional tightening. After fixed
    Frobenius-isometric svec, sparse
    single-flip locality gives simultaneous primal and dual-stationarity
    residual \(O(N^{-1/2})\), while the algebraic gap remains exactly
    \(r\mu\). A fixed density-matrix observable supplies an SDP-native
    mixture-stable wrong-output condition. The operator Kantorovich inequality
    is classical; the sparse neighboring-instance phase boundary is the
    apparent new conjunction.
17. `2026-09-02-signed-copy-cut-multiplier-conservation.md` identifies the
    structural price of keeping the *complete* primal--dual direction bounded
    in parity-copy gadgets.  At a central point, signed incidence rows switch
    to an ordinary flow with positive vertex demand
    \(2\mu|d_v|/(q_v^2-d_v^2)\); at a pair-symmetric Newton start, the demand is
    \((s_v^0/(2x_v^0))|\Delta d_v|\).  Every output cut must carry the sum of
    these demands.  After diagonal row scaling, the conserved quantity is the
    physical force \(r_e y_e\), yielding the one-bit-local frontiers

    \[
      M_{\rm dep}B_{\rm row}\|y\|_\infty
      \ge \frac{2\mu a}{Q^2-a^2}KN,
      \qquad
      M_{\rm dep}B_{\rm row}\|\Delta y\|_\infty
      \ge \rho aKN.
    \]

    Hence a linear-incidence, linear-output, bounded-coefficient copy
    amplifier with constant local scales necessarily has an
    \(\Omega(P)\) multiplier; the dual-homogeneity construction escapes exactly
    by taking \(\rho=\Theta(1/P)\).  More generally, arbitrary
    pair-antisymmetric constraint blocks satisfy the graph-free work identities

    \[
      b_a^Ty=\sum_v\frac{2\mu d_v^2}{q_v^2-d_v^2},
      \qquad
      r_a^T\Delta y=\Delta d^T
      \operatorname{Diag}\!\left(\frac{s_v^0}{2x_v^0}\right)\Delta d.
    \]

    These bilinear quantities survive arbitrary invertible row mixing, and
    their dual norm products remain at least the invariant work.  This does
    not preclude both norms shrinking from poorly aligned values in an
    original basis.  Signed-graph switching and flow conservation are
    classical; the central/Newton source formulas and their sparse
    input-incidence conjunction are the apparent new gadget-design frontier,
    subject to the dedicated literature audit.
18. `2026-09-02-involution-central-work-identity.md` lifts the paired-LP work
    identity to every differentiable convex barrier invariant under an
    orthogonal involution, and then to finite or compact orthogonal symmetry
    groups through the Reynolds projector.  For a symmetric cost, every exact central KKT
    point satisfies

    \[
      y^TAx_-
      =\frac{\mu}{4}\langle x-Rx,
        \nabla F(x)-\nabla F(Rx)\rangle
      =\frac\mu2D_F(Rx,x)\ge0.
    \]

    For a \(C^2\) barrier this is exactly the Hessian energy integrated along
    the involution chord.  The note proves quantitative eigenvalue and local
    self-concordant bounds, recovers the paired-log-barrier formula with the
    exact factor, and gives the noncommutative log-det SDP identity

    \[
      b_-^Ty_-=\frac\mu2
      [\operatorname{tr}(QXQX^{-1})-r]
    \]

    in a pure parity row split.  The robust antisymmetric work vector is
    \(Ax_-\), so the general identity survives arbitrary mixed rows and
    invertible row-basis changes.  No multiplier uniqueness or row
    independence is required.  Strict
    positivity does require strict convexity along the orbit; asymmetric
    objectives or untracked antisymmetric rows add work terms and can cancel
    the barrier energy.  Gradient monotonicity, Bregman divergence, and KKT
    virtual work, symmetry reduction, and Reynolds averaging are classical;
    the useful synthesis is the coordinate-free barrier-geometric obstruction
    template and its exact LP/SDP/QIPM-gadget specializations, not a new
    convex-analysis identity.
19. `2026-09-02-beyond-pair-full-kkt-obstruction.md` extends the multiplier
    obstruction from scalar signed copies to public flat
    constant-dimensional orthogonal block copies.  If two inputs have one
    transported codeword separation of norm at least \(2a\) throughout an
    output region \(S\), share a local metric \(D_v\succeq\rho I\) and a
    numerical source, and boundary row scales have norm at most \(B\), then

    \[
      \max_{p\in\{+,-\}}
      \|\Delta y^p_{\partial S}\|_{2,\infty}
      \ge \frac{\rho a|S|}{B|\partial S|}.
    \]

    Thus swaps, constant-size simplex/permutation codes, public rotations,
    path-consistent fanout, and flat circulations retain the small-interface
    dual-accumulation price.  A concrete quarter-turn cycle is an especially
    useful failed construction: every bounded two-dimensional block encodes
    parity, yet its closure multiplier is exactly \((N+1)/2\), its copy
    operator has
    \(\sigma_{\min}=2\sin(\pi/[4(N+1)])\), and its eliminated saddle system
    has a \(\Theta(N^{-2})\) small eigenvalue.  Connection-Laplacian transport
    and vector-flow energy are established; the apparently new content is the
    QIPM two-input/public-source-cancellation synthesis.  General orthogonal
    label incidence is not proved, and nonflat holonomy, differing metrics,
    or mixed-mode nonlinear encodings remain outside the theorem.
20. `2026-09-02-nonsoc-schur-block-sdp-parity.md` gives a linear-size
    higher-rank product-SDP parity family.  Its \((k+1)\times(k+1)\) blocks
    have a free \(\mathbb S_+^k\) Schur complement, and the full reduced
    log-det Hessian is exactly
    \((\mu_0^2/\mu)I\) on every point of the central path.  The two local
    sign blocks do not commute.  With \(k=3\), the \(4\times4\) block slice
    is affinely isomorphic to \(\mathbb S_+^3\), so Fawzi's theorem rules out
    every finite SOCP lift; this is the first member that escapes the SOCP
    caveat of the \(3\times3\) construction.  Isometric-svec rooted chains
    give scalar row and column sparsity two, \(\|b\|_2=\sqrt3\), bounded
    centers and multipliers on the full tail \(0<\mu\le\mu_0=1/P\), and
    \(\Omega(P)\) raw-query lower bounds for both constant-trace-distance
    density-state preparation and full central-triple amplitude-state
    preparation.  For \(k=3\), the density decoder remains hard for every
    PSD primal block vector with objective at most the \(t=1\) center value
    and equality residual at most \(1/(4\sqrt P)\); a single-flip mixture
    shows that the \(\Theta(P^{-1/2})\) residual scale is asymptotically
    sharp for this construction.
    The Schur coordinates make the free optimization public and
    input-independent, so the result is honestly an output-interface lower
    bound, not hardness of abstract SDP optimization.
21. `2026-09-02-free-s3-parity-central-hessian.md` moves the obstruction into
    the free problem in a fixed public root coordinate, using a maximum-degree-
    two congruence chain and two public anisotropic cost regions.  After exact
    elimination, that coordinate gives a problem over \(\mathbb S_+^3\) with
    parity-dependent, noncommuting
    cost
    \[
       \bar C_p=I+\frac8{33}H_{12}
                   +p\frac8{33}H_{13}.
    \]
    Its normalized qutrit central state and physical product-cone density
    state require \(\Omega(P)\) raw coefficient queries, although the
    reduced central Hessian has condition number below five.  A separate
    short-step scaling uses public anisotropy
    \(\delta_P=1/(16\sqrt P)\).  At the public feasible start
    \(X_i=I,\mu=1\), the full reduced Newton Hessian is exactly identity,
    the complete unreduced KKT right-hand side is public, and the Newton
    decrement is \(2/33\).  The free-root direction is
    \(-\frac1{33\sqrt P}(H_{12}+pH_{13})\); a fixed swap of the \(12\) and \(13\)
    svec coordinates reads parity exactly from either its normalized
    constant-dimensional state or the global primal-direction state.  Thus
    both require \(\Omega(P)\) raw queries despite condition one, scalar
    row/column incidence two, bounded public data, and a genuinely non-SOCP
    feasible cone.  The complete primal-plus-equality-multiplier KKT state is
    also linearly hard: an original-row same-edge observable retains magnitude
    above \(6/7\), despite multiplier domination.  The equality-elimination
    isometry is input-dependent and the full saddle KKT matrix has condition
    \(\Theta(P^2)\).  Indeed, a parity-dependent orthogonal gauge canonicalizes
    the whole instance, so the theorem lower-bounds discovering/applying that
    gauge in the fixed original coordinates; it is not an intrinsic
    inequivalence under arbitrary supplied coordinate changes.
22. `2026-09-02-intrinsic-spectrum-trace-normalized-s3-parity.md` closes the
    remaining gauge and output-only loopholes with a signed anisotropy
    triangle.  A degree-two path reduces to the full density spectrahedron
    \(\{Z\succeq0:\operatorname{tr}Z=1\}\), with
    \[
      \bar C_h=3I+\tfrac1{10}(H_{12}+H_{23}+hH_{13}).
    \]
    Its spectra are \(\{16/5,29/10,29/10\}\) and
    \(\{31/10,31/10,14/5\}\), so the optimal values differ by exactly
    \(1/10\).  Consequently additive-\(1/25\) or relative-\(1/100\)
    optimal-value estimation requires \(\Omega(P)\) raw queries and is not a
    chosen-output-coordinate theorem.  At the public start \(X_i=I/3\),
    \(\mu=1/P\), the reduced primal barrier Hessian is a scalar identity,
    the complete KKT right-hand side is public, the symmetric scalar KKT
    graph has treewidth one, and the undamped step has minimum eigenvalue
    \(14/45\).  Fixed observables decode both the primal state and the
    complete primal-plus-multiplier state; the latter retains bias above
    \(7/10\).  The same linear lower bound holds for a canonical
    normalization-three KKT block encoding and for synthesizing the
    normalization-one tangent projector, whose public-gradient signal is
    exactly \(24/41\).  Reduced-residual and \(P^{-1/2}\)-feasibility-robust
    variants, matching linear upper bounds, scalar row sparsity three,
    column sparsity two, and the trace-one non-SOC proof are all explicit.
23. `2026-09-02-batched-holonomy-objective-accuracy-frontier.md` takes
    \(G\) disjoint intrinsic triangle gadgets with \(N\) bits each.  Returning
    all \(G\) component optima to additive \(1/25\) costs
    \(\Theta(GN)=\Theta(L)\) raw queries for total sparse size \(L=33GN\),
    and the Lee--Roland strong direct-product theorem gives exponentially
    small all-correct probability below a constant fraction of that work.
    For the single averaged scalar objective, a parity-block conditional
    symmetrization lemma and the Nayak--Wu counting bound give the tight phase
    law
    \[
      Q_\varepsilon
      =\Theta\!\left(N\min\{G,1/\varepsilon\}\right)
      =\Theta\!\left(\min\{L,N/\varepsilon\}\right).
    \]
    An exact adaptive simulation shows that a classical decision tree learns
    no conditioned block-parity information until it completes all \(N\)
    signs in that block.  This gives the matching classical law
    \[
      R_\varepsilon
      =\Theta\!\left(N\min\{G,1/\varepsilon^2\}\right),
    \]
    including the quantum--classical phase separation between the classical
    saturation scale \(G^{-1/2}\) and quantum saturation scale \(G^{-1}\).
    Hence linear total-size hardness holds exactly at accuracy
    \(\varepsilon=O(1/G)\); constant-accuracy scalar output admits coherent
    sampling across the batch.  The corresponding simultaneous Newton
    preprocessing task retains a scalar reduced Hessian, public right-hand
    sides, full steps, and the same direct-product obstruction.
24. `2026-09-02-group-holonomy-trace-one-sdp.md` replaces the signed scalar
    transport by a fixed orthogonal representation \(U:G\to O(d)\).  Exact
    elimination gives the trace-one \(\mathbb S_+^{3d}\) problem with
    connection-triangle
    cost
    \[
      \bar C_W=3dI+\tfrac1{10}
      \begin{pmatrix}0&I&W^T\\ I&0&I\\ W&I&0\end{pmatrix},
      \qquad W=U_{g_N}\cdots U_{g_1},
    \]
    and its spectrum is the union of
    \(2\cos((\theta+2\pi\ell)/3)\) over the eigenphases \(e^{i\theta}\) of
    \(W\).  In the natural three-dimensional representation of \(S_3\), the
    scalar optimum separates all three conjugacy classes, including the
    identity from three-cycles even though they have the same abelianization.
    The local SDP has \(9\times9\) blocks, public \(\pm1\) coefficient values,
    bounded row and column incidence, a non-SOCP density-spectrahedron feasible
    set, and a forest scalar primal-barrier KKT graph.  At the public start
    \(X_i=I/9,\mu=1/P\), the original KKT right-hand side is public, the reduced
    Hessian is exactly scalar, the decrement is \(\sqrt2/30\), and a full step
    stays uniformly interior.  Restriction to one fixed transposition subgroup
    yields \(\Omega(P)\) raw-query lower bounds for the scalar value, root and
    global primal Newton states, complete primal-plus-multiplier state, a
    canonical constant-normalization KKT block encoding, and approximate
    tangent-projector synthesis.  The unrestricted objective is genuinely
    nonabelian, but the proved query exponent uses ordinary \(\mathbb Z_2\)
    parity; the novelty claim is only the optimization-native conjunction, not
    a new holonomy spectral formula or an intrinsically nonabelian word-query
    lower bound.
25. `2026-09-02-winner-take-all-global-trace-holonomy-sdp.md` couples \(G\)
    intrinsic triangle gadgets through one global trace budget, implemented
    by a public free-scalar accumulator chain with row sparsity five and
    column sparsity two.  Exact elimination gives
    \[
      \min\left\{\sum_g\langle\bar C_{h_g},Z_g\rangle:
      Z_g\succeq0,\ \sum_g\operatorname{tr}Z_g=1\right\}
      =\min_g\lambda_{\min}(\bar C_{h_g}).
    \]
    The optimum is \(29/10\) if all path parities are even and \(14/5\) if
    any is odd.  Additive-\(1/25\) value estimation therefore has tight
    quantum query complexity \(\Theta(N\sqrt G)\) by
    \(\mathrm{OR}_G\circ\mathrm{PARITY}_N\), versus randomized classical
    \(\Theta(NG)\).  At public \(X=I/(3G),t_g=g/G,\mu=1/(GP)\), the
    \((6G-1)\)-dimensional PSD-root Hessian after public elimination is
    \(9G I\), the Newton decrement is \(1/\sqrt{150}\), all unreduced
    right-hand sides are public, and the undamped step has minimum block
    eigenvalue \(14/(45G)\).  The unbarriered free accumulators keep incidence
    bounded, but no condition-one claim is made for their ambient singular
    Hessian or the full saddle KKT matrix.
26. `2026-09-02-winner-central-path-condensation.md` solves the same family's
    root log-det central path.  With one odd component, barrier coefficient
    \(\tau\), and \(\alpha=\tau G\), its winner trace mass has the sharp
    threshold \(\alpha_*=2/45\): it tends to
    \(1-(45/2)\alpha\) below threshold, is \(\Theta(G^{-1/2})\) at threshold,
    and is \(\Theta(G^{-1})\) above threshold.  The Frobenius reduced Hessian
    simultaneously changes from condition \(\Theta(G)\) to \(\Theta(1)\).
    More generally, constant winner mass forces \(\Omega(G)\) conditioning,
    including for approximate centers with a constant local-barrier residual.
    In the condensed tail, two group-register samples distinguish the
    all-even and unique-odd central states without parity verification, giving
    an \(\Omega(N\sqrt G)\) raw-query lower bound for constant-trace-error
    central-state preparation.  The note also gives exact state-distance and
    coherent-preparation frontiers, and separates QIPM continuation from the
    matching search-then-crossover algorithm.
27. `2026-09-02-general-block-logdet-condensation.md` abstracts the
    preceding phenomenon to one winning \(d\times d\) cost block and
    \(G-1\) identical losing blocks.  If the loser gaps above the winning
    value are \(\delta_j>0\), the exact matrix-Burg center has
    reciprocal-gap capacity \(B_0=\sum_j\delta_j^{-1}\), critical scale
    \(\tau G=B_0^{-1}\), and critical winner mass
    \(B_0^{-1}\sqrt{m(\sum_j\delta_j^{-2})/G}\), where \(m\) is the
    winning ground multiplicity.  The equality-reduced Frobenius Hessian has
    the phase law
    \[
      \kappa_{\rm red}=
      \begin{cases}
      \Theta(G),\Theta(G),\Theta(1),&m=1,\\
      \Theta(G^2),\Theta(G),\Theta(1),&m\ge2,
      \end{cases}
    \]
    in the subcritical, critical, and supercritical regimes.  More sharply,
    for every exact finite center with winner mass \(p\) and \(G\ge3\),
    \[
      \kappa_{\rm red}\ge
      \left(\frac{(G-1)p}{1-p}\right)^2\quad(m\ge2),
    \]
    while a simple non-scalar ground state gives the corresponding linear
    inequality and scalar blocks admit an exact formula.  Combining this with
    the central-density trace-distance bound yields a quantitative
    conditioning--visibility dichotomy: constant output visibility forces
    \(\Omega(G^2)\) conditioning for a degenerate winning ground space and
    \(\Omega(G)\) for a simple one.  A noncommutative relative-residual
    theorem preserves these exponents for approximate centers.  The note also
    proves an explicit \(\operatorname{Adv}^{\pm}(f)\sqrt G\) raw-query
    transfer for unique-winner state outputs, a \(k=o(G)\) multiwinner
    critical law, and matching exactly-\(k\) coherent-preparation bounds.
    The reciprocal-gap condensation mechanism itself is classical
    Rayleigh--Jeans/matrix-Burg physics; the candidate novelty is the
    growing-block SDP constants, multiplicity exponents, finite
    mass--conditioning law, and their QIPM output/query conjunction.

Useful supporting results are in
`2026-09-02-congruence-condition-recovery-frontier.md`,
`2026-09-02-geometric-locality-qipm.md`, and
`2026-09-02-block-angular-qipm-frontier.md`.  The first proves a sharp
conditioning--recovery frontier for active/inactive power congruences; the
second separates condition-one reduced Newton geometry from bounded-range
hardware depth; the third gives an optimal \(\widetilde O(\sqrt N)\) per-step
quantum border-aggregation module for block-angular systems, but not yet an
end-to-end iteration advantage.

## Excluded local results

- structural, output-size, and query lower bounds already in the repository;
- QCPM corrections, OSS/QLS liftings, treewidth results, and RHS-loading bounds;
- the active/inactive DLS coupling theorem and its four/eight-power phase law;
- stable active-subspace equilibration when the active projector is supplied.

## Candidate A: factorized filtered Newton solve

Let

\[
 D=(XS^{-1})^{1/2},\qquad B=AD,\qquad H=BB^\top.
\]

For a feasible Newton step define the scaled variables

\[
 u=D^{-1}\Delta x,\qquad v=D\Delta s,
 \qquad h=(XS)^{-1/2}r_c.
\]

Primal and dual feasibility imply

\[
 Bu=0,\qquad v\in\operatorname{range}(B^\top),\qquad u+v=h.
\]

Consequently the physical step is the orthogonal decomposition

\[
 u=\Pi_{\ker B}h,
 \qquad
 v=\Pi_{\operatorname{range}(B^\top)}h,
\]

up to the sign convention used for the centering residual.  Equivalently, if
\(f=Bh\), then

\[
 v=B^+(Bh)=B^\top (BB^\top)^{-1}f.
\]

This suggests solving the consistent rectangular system directly instead of
solving the squared normal system for the multiplier and then multiplying by
\(B^\top\).

For full-row-rank \(B\), the natural pseudoinverse analogue of the filtered
linear-system parameter is

\[
 \rho_B(f)=
 \alpha_B
 \frac{\|(BB^\top)^{-1}f\|_2}
 {\sqrt{f^\top(BB^\top)^{-1}f}},
\]

where \(\alpha_B\geq\|B\|\) is the block-encoding normalization.  Indeed,
\(B^+f=B^\top H^{-1}f\), its squared norm is \(f^\top H^{-1}f\), and applying
the adjoint pseudoinverse once more gives \(H^{-1}f\).

### Central-path asymptotic

In the mixed strictly-complementary regime

\[
 H_\mu=\mu^{-1}C+\mu D+o(\mu),
 \qquad U=\operatorname{range}C,
 \qquad 1\leq\dim U<m,
\]

take the exact-centering right-hand side \(f=b\in U\).  Under the generic
active/inactive coupling used in the earlier local theorem,

\[
 H_\mu^{-1}b=\mu(p,-g)+o(\mu),
 \qquad
 b^\top H_\mu^{-1}b=\Theta(\mu).
\]

Since \(\alpha_{B_\mu}=\Theta(\mu^{-1/2})\),

\[
 \boxed{\rho_{B_\mu}(b)=\Theta(1).}
\]

By contrast, the normal-equation filtered parameter can be
\(\Theta(\mu^{-2})\), because applying \(H_\mu^{-1}\) a second time amplifies
the \(K\)-component of \(H_\mu^{-1}b\).  The rectangular formulation therefore
appears to remove the second-inverse obstruction without requiring the active
projector used by stable active-subspace equilibration.

### Novelty boundary and unresolved obligations

Direct minimum-norm solution of a rectangular system is not new.  In
particular, Li (2025), arXiv:2510.05588, studies instance-dependent preparation
of \(A^+b\) for rectangular \(A\).  The apparently new part is the IPM
specialization, the constant central-path asymptotic above, and potentially a
full physical-Newton-step theorem.  Before promotion, all of the following must
be proved or audited:

1. a rectangular, rank-deficient version of the filtered QLS theorem with the
   exact normalization and error dependence claimed here;
2. preparation of \(f=Bh\) without a hidden \(\mu\)-dependent postselection
   cost;
3. coherent construction of both \(u\) and \(v\), including norm estimation and
   cancellation error;
4. propagation of state error through an inexact-IPM neighborhood;
5. a changing-iterate oracle/update implementation that does not reintroduce
   tomography or dense work;
6. a primary-literature audit of rectangular/augmented/orthogonal-subspace
   QIPMs.

Final disposition: **proved parameter observation, but open as a QLS/QIPM
algorithm**.  Li's rectangular minimum-norm solver (arXiv:2510.05588) already
covers closely related pseudoinverse geometry and can give bounded
\(\mu\)-dependence under additional sparse-access hypotheses.  What remains
unproved here is a rank-deficient rectangular extension with the sharper DLS
error law, together with \(f=Bh\) loading, cancellation-safe recovery of
\(u,v\), neighborhood propagation, changing-iterate access, and an
end-to-end classical comparison.  The displayed \(\rho_B=\Theta(1)\)
asymptotic must not be cited as an implemented speedup.

## Candidate B: certified quantum optimal-basis crossover

Consider a standard-form LP with a unique, nondegenerate, strictly
complementary optimum.  Let \(B=\operatorname{supp}(x^*)\), \(|B|=m\), and
write \(N=[n]\setminus B\).  Define

\[
 \alpha=\min_{j\in N}s_j^*>0,\qquad
 \beta=\min_{i\in B}x_i^*>0,\qquad
 \Theta=\|A_B^{-1}A_N\|_{1\to\infty},\quad
 M=\max(1,\Theta).
\]

For any primal-dual feasible interior point with gap \(G\), optimality and
feasibility give

\[
 \alpha\|x_N\|_1\leq G,
 \qquad
 x_B-x_B^*=-A_B^{-1}A_Nx_N.
\]

Thus, whenever

\[
 G\leq G_0:=\frac{\alpha\beta}{4M},
\]

every basic coordinate is at least \(3\beta/4\), while every nonbasic
coordinate is at most \(\beta/4\).  A coherent coordinate oracle accurate to
less than \(\beta/8\) therefore supplies an exact membership predicate for the
unknown basis.  Quantum enumeration finds all \(m\) marked coordinates in
\(\widetilde O(\sqrt{nm})\) predicate queries.  After retrieving the \(d\)-sparse
columns of \(A_B\), solve the \(m\)-dimensional basis systems and use quantum
minimum search over inactive reduced costs to produce an exact candidate with
bounded-error KKT verification.  A deterministic explicit certificate requires
reading or materializing the inactive slacks, or otherwise paying for exact
verification.

This crosses over at a structural tolerance \(G_0\), independent of the final
requested accuracy.  It can therefore remove every late high-precision IPM
iteration and dense tomography, returning the explicit sparse primal optimum,
the dual basis solution, and an implicit slack oracle.

Important caveat: this is an end-to-end speedup only when coherent coordinate
threshold access is already available.  A hybrid QIPM that materializes all
\(n\) coordinates has already paid the classical scan cost.  Classical basis
identification/crossover is established prior art; the candidate novelty is the
Grover enumeration/certification module and its precise crossover theorem.

Final disposition: **sound conditional separation lemma and supporting
module, not a headline complexity result**.  It assumes certified structural
margins and a coherent absolute-accuracy coordinate oracle; a normalized
iterate state does not provide that oracle for free.  The dedicated note
2026-09-02-exact-quantum-crossover-tall-lp.md supplies the precise tall-row
query model and proof, and records stronger exact-LP collisions
(Objois--Vladu and Dadush--Végh--Zambelli).  Classical crossover and Grover
enumeration/pricing are prior art.

## Candidate C: state-to-diagonal lifting

If \(U_v|0\rangle=|v\rangle=\sum_i(v_i/\nu)|i\rangle\), define

\[
 G_0|i\rangle=|v\rangle|i\rangle,
 \qquad
 G_1|i\rangle=|i\rangle|i\rangle.
\]

Then

\[
 G_1^\dagger G_0=\operatorname{Diag}(v)/\nu.
\]

Hence a phase-aligned coherent preparation unitary, together with controlled
and adjoint access and the norm \(\nu\), can be lifted exactly to a projected
block encoding of its diagonal update.  An ordinary density-state output is
insufficient: its arbitrary global phase becomes physical when the diagonal
update is added coherently to another operator.  LCU with a block encoding of
\(X=\operatorname{Diag}(x)\) yields
\(X+\alpha\operatorname{Diag}(v)\), and the absolute operator errors add.
If \(|\alpha v_i|\leq\rho x_i\), then
\(|\alpha|\|v\|_2\leq\rho\|x\|_2\) and
\(\|x+\alpha v\|_2\geq(1-\rho)\|x\|_2\), so the LCU normalization overhead
relative to the new Frobenius/Euclidean norm is at most
\((1+\rho)/(1-\rho)\) when the encoding of \(X\) is normalized by
\(\|x\|_2\).  With an arbitrary normalization \(\alpha_X\), the honest
ratio is
\((\alpha_X+|\alpha|\nu)/\|x+\alpha v\|_2\).

Final disposition: **exact known primitive, recorded in IPM notation**.
Rattew--Rebentrost (arXiv:2309.09839, Theorem 2) already give the same
state-amplitude-to-diagonal block encoding.  It does not by itself give
persistent coordinate access or show how errors accumulate over the full
central path.  The repository's output-interface lower bound explains the
normalization/query obstruction, while the implicit-dual-coordinate note gives
the positive persistent-access alternative.

## Candidate D: condition--recovery frontier

Ideal congruence scaling can trade Newton-system condition number for recovery
precision without removing the total obstruction.  In the mixed regime above,
let

\[
 T_{\mu,\beta}=\mu^{\beta/2}\Pi_U+
 \mu^{-\beta/2}\Pi_{U^\perp},\qquad 0\leq\beta\leq1,
\]

and \(G_{\mu,\beta}=T_{\mu,\beta}H_\mu T_{\mu,\beta}\).  Under generic nonzero
coupling,

\[
 \kappa(G_{\mu,\beta})=\Theta(\mu^{-2(1-\beta)}).
\]

The transformed solution suppresses the physically important inactive
component by \(\mu^\beta\).  Applying the normalized recovery map has success
probability \(\Theta(\mu^{2\beta})\), and the normalized recovered state has
sensitivity \(\Theta(\mu^{-\beta})\).  Consequently

\[
 \boxed{
 \sqrt{\kappa(G_{\mu,\beta})}\,
 \operatorname{cond}(\text{state recovery})
 =\Theta(\mu^{-1})
 =\Theta(\sqrt{\kappa(H_\mu)}).
 }
\]

This is witnessed by the two-sparse LP

\[
 \min x_2+x_3,
 \quad x_1+x_2=1,
 \quad x_2-x_3=0,
 \quad x\geq0.
\]

The dedicated note
2026-09-02-congruence-condition-recovery-frontier.md now extends this result
to every scalar block-diagonal SPD congruence
\(T_\mu=t_U(\mu)\Pi_U+t_K(\mu)\Pi_{U^\perp}\).  With
\(r_\mu=t_U/t_K\), it proves

\[
 \sqrt{\kappa(T_\mu H_\mu T_\mu)}
 =\Theta\!\left(\max\{r_\mu/\mu,\mu/r_\mu\}\right),
 \qquad
 \operatorname{cond}(\text{state recovery})
 =\Theta\!\left(\max\{r_\mu,r_\mu^{-1}\}\right).
\]

Their product is always \(\Omega(\mu^{-1})\), and it is
\(\Theta(\mu^{-1})\) exactly for the maximal class
\(r_\mu=\Omega(\mu)\) and \(r_\mu=O(1)\).  The same fixed two-sparse LP
matches all regimes.

Status: **proved and independently checked structural obstruction**.  It
applies to the whole scalar block-diagonal congruence class, but remains
neither a universal preconditioning lower bound nor a generic QLS runtime
lower bound.

## Undeveloped lower-bound fallback

A degree-two cycle-connectivity promise can be reduced to a row-sparsity-five,
column-sparsity-two feasible LP whose optimum has a constant gap between one
cycle and two cycles.  The reduction is robust to an \(\ell_2\) primal residual
that is a fixed fraction of \(\|b\|_2\), and hence yields an
\(\Omega(n)\)-query lower bound invariant under row/column scaling and arbitrary
preconditioning.  The LP wrapper and residual statement may be new, but the
underlying quantum connectivity lower bound is published and parity-derived.

Final disposition: **do not cite as a repository result**.  No dedicated proof
of the LP wrapper, residual constants, displayed sparsities, or claimed
preconditioning invariance was completed in this cycle.  The later
parity/holonomy constructions are both stronger and fully documented, so this
idea is retained only as an undeveloped lead.

## Post-closure cycle (same date, after the closure audit)

Two new referee-audited theorem packages were added after
2026-09-02-research-closure-and-open-frontier.md was written. They are
authoritative over any conflicting status language above.

28. `2026-09-02-barrier-independent-conditioning-dichotomy.md` (title now:
    barrier-independent central-path conditioning — the sublevel chord
    law). For every compact convex feasible region, every objective, and
    **every** \(\nu\)-self-concordant barrier, the reduced central-path
    Hessian satisfies the chord-law floor
    \(\kappa_{\rm red}\ge(D(g)\|\Pi_Vc\|/(2(\nu+2\sqrt\nu)g))^2\), where
    \(D(g)\) is the diameter of the gap-\(g\) sublevel set; the canonical
    log/log-det barrier achieves \((SnD(g)/g)^2\), so barrier redesign can
    never improve central-path conditioning by more than a
    \(\mu\)-independent instance factor. Consequences: complete LP
    dichotomy (bounded conditioning iff unique optimum, degenerate
    vertices included; \(\Theta(1/\mu^2)\) for every barrier iff the
    optimal face has positive dimension); a corrected SDP folklore point
    (unique nondegenerate SDP optimum gives \(\Theta(1/\mu)\), not
    \(\Theta(1/\mu^2)\), in the reduced primal log-det geometry); and the
    barrier-choice escape route for QLSA-based QIPMs is closed
    (scoped against the condition-free Apers--Gribling line). Novelty
    audit: no published all-barriers conditioning lower bound found;
    differentiate from Allamigeon--Gaubert--Vandame (iterations, not
    conditioning).
29. `2026-09-02-zero-versus-k-verified-sample-state-conversion.md`
    resolves closure Direction III.M in the constant-visibility regime:
    verified-sample decoder (one-sided, collision-free), \(k\)-copy
    embedding into Theorem P, and a detuned fixed-point rejection
    preparation give \(Q_\varepsilon=\Theta(N\sqrt{G/k})\) for
    \(p=\Theta(1)\), \(k=O(G/\log^2G)\), \(\varepsilon\le(1-c)p\), with
    classical law \(\Theta(N\delta G/k)\). Open residue: the
    \(\sqrt\delta\)-vs-\(\delta\) factor in the transition window,
    equivalent to a composed small-success search theorem
    \(Q_\delta(\mathrm{SEARCH}_{G,k}\circ f)
    \overset{?}{=}\Omega(\sqrt\delta\,A\sqrt{G/k})\).
30. `2026-09-02-composed-small-success-search-polynomial.md` closes the
    \(\sqrt\delta\)-vs-\(\delta\) residue of item 29 for the parity inner
    function: a polynomial-method theorem (parity collapse to block
    variables, symmetrization, Coppersmith--Rivlin boundedness, Markov
    derivative bound) shows one-sided bias \(\delta\) between zero and
    \(k\) parity-marked blocks forces
    \(T=\Omega(\sqrt\delta\,N\sqrt{G/k})-O(N)\). Consequences: the
    composed small-success search theorem
    \(Q_\delta(\mathrm{SEARCH}_{G,k}\circ\mathrm{PARITY}_N)
    =\Theta(\sqrt\delta N\sqrt{G/k}+N)\), and the complete
    zero-versus-\(k\) state-conversion accuracy curve
    \(Q_\varepsilon=\widetilde\Theta(N(1+\sqrt{(p-\varepsilon)G/k}))\).
    The \(N=1\) case is Zalka/KŠdW; general inner predicates remain at
    linear-in-\(\delta\) strength via the adversary route. Verification
    of the Coppersmith--Rivlin constant and the novelty sweep pending.
31. Corollary D added to the chord-law note (item 28): singularity-degree
    conditioning hierarchy. Attained Hölder error-bound exponent
    \(\theta\) forces \(\kappa_{\rm red}=\Omega(g^{2\theta-2})\) for
    every barrier; explicit singularity-degree-2 SDP witness with
    \(D(g)=\Theta(g^{1/4})\) shows the fractional law
    \(\kappa=\Theta(\mu^{-3/2})\), confirmed numerically
    (\(\kappa\mu^{3/2}\to0.40\)). Facial-reduction complexity is thereby
    a barrier-independent QIPM conditioning obstruction.
32. `2026-09-02-two-cluster-central-hessian-benign-kappa.md` calibrates
    the chord law: log-barrier central Hessians of degenerate LPs have
    two-interval spectra with \(\mu\)-free intra-cluster ratios (proved
    via Weyl splitting plus the chord converse), so CG/QSVT residual
    polynomials of degree \(O_\rho(\log(\Lambda/\varepsilon)
    \log(1/\varepsilon))\) solve them despite
    \(\kappa=\Theta(1/\mu^2)\) — verified with CG converging in 3--8
    iterations while \(\kappa\) spans \(10^1\)--\(10^{13}\).
    Consequences: conditioning is not the QIPM bottleneck (normalization,
    RHS structure, and I/O are — consistent with the repository's
    lower-bound program), and \(\kappa\)-based QIPM resource estimates
    are pessimistic on clustered instances. Open: a sparse family with
    genuinely spread central-Hessian spectra.
    Addendum to item 30: Corollary S3 of the same note upgrades the
    exactly-\(k\) AP6 preparation lower bounds of
    2026-09-02-general-block-logdet-condensation.md from operator-level
    unitary access to mere trace-close mixed-state outputs (the caveat
    explicitly recorded there), and proves the critical-regime
    \(\Theta(N(G/k)^{1/4})\) line tight for relative-error contracts
    \(\varepsilon\le p/2\), via the one-sided verified-sample decoder run
    outside the promise.
33. Post-audit strengthenings of item 28 (all in the chord-law note):
    (i) Theorem B′ — universal \(\lambda_{\min}\) rigidity: the chord
    converse \(\lambda_{\min}\ge1/\ell(x)^2\) holds for every barrier at
    every interior point via Dikin containment alone, so the flat
    spectral edge is geometry, not design; (ii) Corollary E —
    near-degeneracy plateau: a \(\theta\)-nearly-optimal face freezes
    \(\kappa\) at \(\Theta(1/\theta^2)\) below gap \(\theta\) (verified:
    plateau exactly \((4/3)\theta^{-2}\)); (iii) real-instance
    validation on Netlib afiro: \(\kappa g^2\) constant over four
    decades (positive-dimensional optimal face), \(\lambda_{\min}\ell^2
    \in[3.6,6.6]\subset[1,701]\), CG in 11--39 iterations at
    \(\kappa=8\times10^{13}\) (notes/scripts/afiro_chord_check.py). Item 30's
    note also received its referee audit: Theorem S verified in full;
    S2/S3 domain repairs applied (exact verification, \(\delta\ge Ck/G\)
    hypothesis, supercritical phase marked vacuous); citations corrected
    to Dohotaru--Høyer and Carolan--Poremba for k-marked small-success
    search; CR92 constants confirmed unspecified (existence suffices).
34. `2026-09-02-netlib-conditioning-survey.md`: empirical companion —
    chord-law conditioning exponents measured on 14 small Netlib
    instances. The two dominant classes are exactly the predicted
    endpoints (\(\alpha\approx2\): afiro, adlittle;
    \(\alpha\approx0\): sc family, seba, scorpion), with crossover
    slopes on kb2/scagr7 and two float64 failures at
    \(\kappa\gtrsim10^{15}\). Two-cluster CG benignity confirmed on
    afiro/seba/sc50a but obstructed by large intra-cluster instance
    constants and roundoff on adlittle/scagr7 — an honest limit of the
    benign-kappa message in the wild.
    Addendum to item 34: direct sublevel-diameter measurement
    (notes/scripts/netlib_sublevel_exponent.py) cross-validates the chord law on
    real data by a second computation path: afiro theta->0 predicts
    alpha=2.000 (measured 2.00), sc50b theta->1 predicts alpha=0
    (kappa frozen at 582), kb2 is a real-world Corollary E crossover
    (theta climbs 0.08->0.99), and adlittle at practical depths has a
    single 9-decade spread spectrum answering the two-cluster note's
    open item (notes/scripts/adlittle_spectrum_probe.py).
35. AUDIT CORRECTION to item 32, replacing its quantum claim, plus two
    new theorems. (a) The two-cluster note's original QSVT corollary was
    refuted by its referee audit and replaced by **Theorem Q
    (gap-boundedness obstruction)**: QSVT-implementable polynomials must
    be bounded on the whole interval including the spectral gap; a
    Markov-brothers argument (audit) shows any residual-style polynomial
    bounded by \(M\) there has degree \(\Omega(\sqrt{\kappa/M})\), and a
    Bernstein branch argument (added, self-checked) shows even
    cluster-filtered inversion pays degree×subnormalization
    \(\Omega(\sqrt\kappa/\rho_1)\) at intra-cluster relative accuracy.
    So clustered central-path ill-conditioning is benign for classical
    CG but **provably not** for single-polynomial QSVT — a structural
    classical-quantum separation and a fourth quantum-only cost
    interface (off-spectrum boundedness) beyond loading/recovery/output.
    Item 32's resource-estimation advice is reversed for QSVT-based
    solvers. (b) **Theorem W (width-spectrum rigidity)** added to the
    chord-law note: every eigenvalue of every barrier's reduced central
    Hessian is sandwiched between reciprocal squared Gelfand- and
    Bernstein-type chord widths of the sublevel body
    (\(1/(w_j^-)^2\le\lambda_j\le(\nu+2\sqrt\nu)^2/(w_j^+)^2\)) — the
    whole spectral profile is geometry, not barrier design; edge cases
    reproduce Theorems A/B′. (c) The singularity-degree-2 SDP witness
    spectrum was measured by the audit: four windows with exponents
    \(\mu^{-1/2},\mu^{-1},\mu^{-3/2},\mu^{-2}\) and \(\mu\)-free
    prefactors.
    Addendum to item 35: the Theorem Q tradeoff is numerically tight —
    a Remez-style LP (notes/scripts/qsvt_cluster_tradeoff_lp.py) shows the
    minimal off-spectrum bound collapses to O(1) exactly at degree
    \(\approx0.5\sqrt\Lambda\) for \(\Lambda=10^4,10^6\). Filtered-QSVT
    on two-cluster spectra therefore costs
    \(\widetilde\Theta(\sqrt\kappa)\): a quantified three-way separation
    CG polylog < QSVT-clustered \(\sqrt\kappa\) < QSVT-generic
    \(\kappa\). The analytic \(O(\sqrt\kappa)\)-degree construction is also in the
    note (truncated Laplace \((1-e^{-yT})/y\) plus Sachdeva--Vishnoi
    exponential approximation), so Theorem Q is tight both ways; open
    only: adaptive quantum schemes below \(\sqrt\kappa\).
36. Final audit of the cycle: Theorems W and Q both externally
    referee-audited and found sound (W: all steps and edge cases
    verified, numerical sandwich exact at the A(a) floor; Q: Markov and
    truncated-Laplace items verified in full, Bernstein item repaired at
    the constant/wording level with an explicit relative-accuracy
    hypothesis, LP collapse points independently reproduced, and the
    branch no-go noted to cover all fixed admissible polynomials). All
    six external audits of this cycle are now complete and every repair
    is applied in the notes.
37. SECOND CORRECTION AND FINAL FORM of Theorem Q (supersedes the
    sqrt-kappa tightness language in items 35's addendum). An in-house
    implementability audit found that the truncated-Laplace polynomial
    and the one-sided tradeoff LP are bounded on \([0,\Lambda]\) but not
    on \([-\Lambda,\Lambda]\), hence not QET-implementable with a plain
    block-encoding; a symmetric-constraint LP
    (notes/scripts/qet_implementability_lp.py) shows the implementable minimal
    separating degree is \(\approx1.0\Lambda\) (vs \(1.7\sqrt\Lambda\)
    relaxed). A literature sweep then grounded the final picture:
    Orsucci--Dunjko (arXiv:2101.11868) already prove an all-algorithms
    \(\Omega(\min(\kappa,N))\) QLS bound on a two-point-cluster
    block-encoded instance; Somma--de Wolf (arXiv:2608.24493) prove the
    \(1/\delta\)-vs-\(1/\sqrt\delta\) split between plain and
    factor (\(H=G^\dagger G\)) access; and the one-sided polynomial
    class is exactly the factor-access class (\(p(\lambda)\) bounded on
    \([0,1]\) = even \(p(\sigma^2)\) on \([-1,1]\)). Final solve-cost
    table for two-cluster Newton systems: classical CG polylog;
    factor-access QSVT \(\widetilde\Theta(\sqrt\kappa)\) (the natural
    model for IPM normal equations — never square the condition
    number); plain block-encoding \(\widetilde\Theta(\kappa)\).
    Clustering helps no quantum access model beyond what the model
    already gives, while collapsing classical cost — a separation not
    previously written down (the quantum ingredients are
    Orsucci--Dunjko's; the classical-side observation that CG solves
    their hard instance in O(1) iterations appears new). All downstream
    references in the chord-law note, the Netlib survey, and the paper
    skeleton have been updated to this final form.
38. `2026-09-02-newton-rhs-spectral-alignment.md` completes the
    two-cluster story on the positive side: at exact central points the
    reduced Newton RHS of both centering and affine-scaling steps is one
    universal vector \(Z^\top X^{-1}\mathbf1\) whose weak-face
    (bottom-cluster) fraction is \(O(\mu^2)\) — the log-barrier path's
    analytic-center limit annihilates the leading weak-mode pairing —
    so a \(\kappa\)-free top-window solve meets any constant
    inexact-Newton contract (verified: dropped-mode residual
    \(6.7\times10^{-6}\to6.7\times10^{-14}\) as \(\mu^2\) on afiro).
    Theorem Q's \(\kappa\)-obstruction therefore binds worst-case RHS
    and weak-mode output contracts, not on-path solves; off-path
    accumulation is governed by the repository's existing face-leakage
    summability conditions. Not yet externally audited.
    Addendum to item 38: the RHS-alignment note is now referee-audited
    (verdict: sound with one repair — the O(mu^2) eigenspace-rotation
    bookkeeping needed and received the Davis--Kahan patch, gap
    \(\Theta(1/\mu^2)\) vs perturbation \(O(1)\); all algebra and
    numbers independently reproduced; the general-barrier parenthetical
    downgraded to a conjecture). Seven external audits in this session;
    all findings repaired.
    Second addendum to item 38: end-to-end validation — a full
    path-following run with adaptive window-only solves (drop bottom
    cluster only when a >2-decade spectral gap exists) converges
    identically to exact solves on both the toy family and afiro
    (rel gap 7.4e-10, same 393 corrections;
    notes/scripts/window_solve_ipm_run.py). A naive gap-free window rule stalls
    on afiro — the early-path continuum must be solved fully — which is
    the correct algorithmic reading of Proposition R.
