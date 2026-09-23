# Closure audit for the sparse-QIPM research cycle

Date: 2026-09-02

## Purpose and verdict

This note closes the current research cycle at the user's request. It does
not assert that every imaginable sparse-QIPM question is solved. It records
the disposition of every live direction in the current frontier: proved,
conditional, collided with prior art, refuted in the proposed form,
undeveloped, or genuinely open. Historical draft logs remain in notes/, but
this note and 2026-09-02-continuing-sparse-qipm-frontier.md are the
authoritative status ledgers.

The strongest candidate surviving this audit is the globally trace-coupled
block-SDP central-path theorem in
2026-09-02-general-block-logdet-condensation.md, together with its concrete
sparse holonomy realization. Its candidate paper-scale core is not the classical
matrix-Burg/Rayleigh--Jeans condensation mechanism. The candidate new
contribution is the explicit growing-\(G\) optimization law, the
ground-multiplicity-dependent Hessian exponents, the exact finite
mass--conditioning--visibility inequalities, their noncommutative approximate
version, and the sparse raw-query output consequence.

No remaining bounded lemma or calculation was identified that would turn the
open positive-algorithm sketches into a rigorous end-to-end QIPM advantage.
Those directions are classified below rather than silently left as candidates.

## I. Main result package

### 1. General block log-det condensation

For one winning \(d\times d\) cost block with ground multiplicity \(m\) and
\(G-1\) identical losing blocks with gaps \(\delta_j>0\), put
\[
 B_0=\sum_j\delta_j^{-1},\qquad
 \beta=\sum_j\delta_j^{-2},\qquad
 \alpha=\tau G.
\]
The exact trace-one matrix-Burg center undergoes a capacity transition at
\(\alpha_*=B_0^{-1}\). Its winner mass is constant below the transition,
\(\Theta(G^{-1/2})\) at the transition, and \(\Theta(G^{-1})\) above it.
The equality-reduced Frobenius Hessian obeys
\[
 \begin{array}{c|ccc}
 &\alpha<\alpha_*&\alpha=\alpha_*&\alpha>\alpha_*\\ \hline
 m=1&\Theta(G)&\Theta(G)&\Theta(1)\\
 m\ge2&\Theta(G^2)&\Theta(G)&\Theta(1).
 \end{array}
\]

The sharper finite theorem uses only the winner mass \(p\). For \(G\ge3\),
\[
 \kappa_{\rm red}\ge
 \left({(G-1)p\over1-p}\right)^2\quad(m\ge2),
\]
and
\[
 \kappa_{\rm red}\ge
 \min\{1,\delta_{\max}/\gamma_{\min}\}
 {(G-1)p\over1-p}\quad(m=1<d).
\]
Scalar blocks have an exact closed formula. Combining these inequalities
with the trace-distance visibility theorem shows
\[
 D_{\rm tr}(\rho_{\mathrm{no\ winner}},\rho_{\mathrm{winner}})\ge\nu>0
 \Longrightarrow
 \begin{cases}
 \kappa_{\rm red}=\Omega(G^2),&m\ge2,\\
 \kappa_{\rm red}=\Omega(G),&m=1.
 \end{cases}
\]
The conclusion survives a blockwise relative stationarity error and trace
residual without assuming that the approximate blocks commute with their
costs. The scalar robust case is also recorded.

The same note proves:

- exact two-copy collision visibility and its mixed-output error transfer;
- an explicit
  \(\operatorname{Adv}^{\pm}(f)\sqrt G\) unique-winner composition witness;
- a \(k=o(G)\) multiwinner transition with critical mass
  \(B_0^{-1}\sqrt{m\beta k/G}\);
- an empirical-resolvent extension to nonidentical losing blocks;
- controlled-purification preparation upper bounds under a clean,
  query-optimal winner marker and public local resolvents;
- the zero-query coarse-error boundary and the unresolved
  intermediate-error zero-versus-\(k\) regime.

All conditioning statements refer to the equality-eliminated root Hessian in
Frobenius coordinates. They are not lower bounds for every input-dependent
preconditioner or for the unreduced saddle KKT matrix. The query statement is
for trace-normalized primal-density output with a public component decoder.

### 2. Concrete sparse realization

2026-09-02-winner-take-all-global-trace-holonomy-sdp.md realizes the theorem
with \(G\) qutrit holonomy gadgets of \(N\) private signs each and one global
trace budget implemented by a free-scalar accumulator chain. Scalar row
sparsity is at most five, column sparsity at most two, and the feasible set
has a face isomorphic to the qutrit density spectrahedron, whose conic hull
has no finite SOC lift (Fawzi, arXiv:1610.04901). The optimum distinguishes all-even
from any-odd with a constant gap. Its tight query complexities are
\[
 Q=\Theta(N\sqrt G),\qquad R=\Theta(NG).
\]
At a public start the reduced root Hessian is scalar, the right-hand side is
public, the Newton decrement is \(1/\sqrt{150}\), and the full step stays
strictly feasible. In the condensed central-path tail, preparation of a
sufficiently small constant-trace-error primal density also costs
\(\Omega(N\sqrt G)\).

2026-09-02-winner-take-all-global-trace-search.md supplies the matching
search-then-solve algorithm for compact winner/root output. It is a quantum
search/crossover module, not a new quantum search primitive and not by itself
a path-following QIPM.

### 3. Novelty calibration

The following components are prior art and are excluded from the novelty
claim:

- affine-resolvent density operators from matrix Burg entropy
  (Ishihara, arXiv:1904.03363);
- reciprocal-gap Rayleigh--Jeans condensation and excited-mode capacity
  (Baudin et al., arXiv:2007.11950);
- inverse-gap critical density, inverse-square fluctuation scale, and
  multi-state condensation in spherical models
  (Lukkarinen, arXiv:1806.01806);
- square-root central-path asymptotics in degenerate SDP classes
  (da Cruz Neto--Ferreira--Monteiro,
  https://optimization-online.org/2003/07/682/);
- generic low-rank SDP Schur/Hessian ill-conditioning
  (Alizadeh--Haeberly--Overton, DOI 10.1137/S1052623496304700;
  Zhang--Lavaei, arXiv:1703.10973);
- Grover search, amplitude amplification, collision testing, and general
  adversary composition (Høyer--Lee--Špalek, quant-ph/0509067).

A targeted search found no open source giving the exact finite
mass--conditioning laws above, the \(G\) versus \(G^2\) multiplicity split,
or their conjunction with trace-distance visibility and the bounded-incidence
sparse holonomy oracle. This is evidence of apparent novelty, not proof of
priority.

## II. Other theorem packages that survived

| Package | Final status | Canonical note |
|---|---|---|
| Intrinsic spectral qutrit parity SDP | Proved and repeatedly audited; scalar value, Newton state, full KKT state, projector, and robust-output lower bounds | 2026-09-02-intrinsic-spectrum-trace-normalized-s3-parity.md |
| Nonabelian group-holonomy SDP | Proved construction; unrestricted objective distinguishes \(S_3\) conjugacy classes, but the query exponent uses a \(\mathbb Z_2\) restriction | 2026-09-02-group-holonomy-trace-one-sdp.md |
| Prefix-rigidified condition-one Newton hardness | Proved; strongest among the repository's audited affine-loading constructions, not a condition-one QLS lower bound | 2026-09-02-prefix-rigidified-condition-one-newton-hardness.md |
| Full primal--dual KKT output lower bound | Proved with public raw RHS and end-to-end accounting after exact Schur transformation | 2026-09-02-linear-plateau-full-kkt-lower-bound.md |
| Schur normalization--conditioning frontier | Proved tight factor tradeoff and setup/per-call law; no claim for a freely supplied preconditioned product | 2026-09-02-schur-factor-access-normalization-frontier.md |
| Scalar congruence condition--recovery frontier | Proved and apparently uncollided in its restricted class; not a universal preconditioning lower bound | 2026-09-02-congruence-condition-recovery-frontier.md |
| Convex-mixture and cut/resistance frontiers | Proved no-go theorems for the specified bounded-degree local-linear and single-flip gadget classes | 2026-09-02-convex-mixture-local-input-obstruction.md; 2026-09-02-cut-resistance-frontier-signed-parity-lps.md |
| Symmetry/work and multiplier conservation | Proved structural identities; classical convex-analysis/flow ingredients are credited | 2026-09-02-involution-central-work-identity.md; 2026-09-02-signed-copy-cut-multiplier-conservation.md |
| SDP central-mixture Kantorovich theorem | Proved noncommutative mixture bounds and sparse neighboring-instance consequence; operator inequality itself is classical | 2026-09-02-sdp-central-mixture-kantorovich.md |
| Rank--progress barrier for SDP Newton directions | Proved structural theorem with sparse witness | 2026-09-02-sdp-newton-rank-progress-barrier.md |
| Projective exact-central refresh | Proved finite tail variation on the exact path; unconditional inexact-trajectory extension is refuted | 2026-09-02-projective-lazy-quantum-newton-refresh.md |
| Partition-free spectral face repair | Operator-level construction proved; generic classical full-output speedup remains blocked by tomography | 2026-09-02-partition-free-spectral-face-repair.md |
| Implicit dual-coordinate oracle | Proved composable representation primitive; end-to-end speedup remains conditional | 2026-09-02-implicit-dual-coordinate-oracle-qipm.md |
| Block-angular border aggregation | Proved optimal per-step border-output theorem; not an end-to-end QIPM | 2026-09-02-block-angular-qipm-frontier.md |

## III. Final disposition of every live algorithmic direction

### A. Factorized rectangular Newton solve

Disposition: **algebraic parameter observation proved; end-to-end algorithm
open and substantially collided**.

The orthogonal decomposition
\[
 u=\Pi_{\ker B}h,\qquad v=B^+(Bh)
\]
is correct, and the normalized rectangular parameter is \(O(1)\) on the
specified exact-centering asymptotic. Li (arXiv:2510.05588) already treats
instance-dependent rectangular minimum-norm state preparation with closely
related second-inverse geometry. A DLS-quality rank-deficient rectangular
filter theorem is not established. Also unresolved are \(Bh\) preparation,
cutoff/error dependence, norm and cancellation control for \(u,v\), recovery
of the physical step, inexact-neighborhood propagation, changing diagonal
oracles, output, and a strong classical comparison. Therefore
\(\rho_B=\Theta(1)\) is not a QIPM speedup theorem.

### B. Certified quantum basis crossover

Disposition: **separation lemma proved; conditional supporting module,
superseded as an overall exact-LP result**.

The gap threshold correctly separates basic and nonbasic coordinates under
unique nondegeneracy and strict complementarity. Grover enumeration is sound
if a coherent absolute-accuracy coordinate predicate and certified margins
are supplied. Quantum minimum search gives bounded-error verification of an
exact candidate; deterministic materialized KKT certification costs an
inactive scan unless another exact oracle is supplied. Objois--Vladu give a
stronger exact quantum Clarkson LP algorithm. Dadush--Végh--Zambelli give a
classical exact polyhedral-separation-oracle framework; obtaining a quantum
row-query corollary requires separately implementing its oracle. The precise
tall-row version is retained only as a supporting QIPM crossover lemma in
2026-09-02-exact-quantum-crossover-tall-lp.md.

### C. State-to-diagonal lifting

Disposition: **exact known primitive, not a new result**.

The isometry identity \(G_1^\dagger G_0=\operatorname{Diag}(v)/\|v\|\) is
correct with a phase-aligned coherent unitary, controlled/adjoint access, and
known norm. A density-state contract is insufficient because global phase
becomes physical under coherent LCU. Rattew--Rebentrost
(arXiv:2309.09839, Theorem 2) already give this amplitude-to-diagonal block
encoding. Persistent trajectory access remains subject to the repository's
normalization/query lower bound; implicit dual coordinates are the positive
alternative.

### D. Scalar congruence preconditioning

Disposition: **proved structural obstruction**.

For every scalar active/inactive SPD congruence, the product of the square
root of the transformed condition number and normalized recovery sensitivity is
\(\Omega(\mu^{-1})\), with a maximal equality class and a fixed two-sparse LP
witness. It does not cover arbitrary left preconditioners, variable-time
algorithms, direct physical-state solvers, or all input-dependent coordinate
changes.

### E. Projective lazy refresh

Disposition: **exact-path positive theorem proved; standard inexact extension
refuted**.

The exact strictly complementary central ray has finite projective tail
variation. A sparse cycling witness shows that standard
\(N_2(\theta)\)-neighborhood and OSS residual bounds do not imply
precision-independent refresh. Under only the standard \(N_2(\theta)\) and
fixed-relative OSS contracts, Tikhonov/ray locking is not guaranteed to repair
the weak face mode. Positive reuse requires the explicit face-leakage or
normalized-forcing summability conditions already in the note.

### F. Partition-free compressed dual method

Disposition: **operator modules proved; end-to-end theorem conditional**.

The spectral comparison, active-range construction, and face repair are
proved. A complete complexity theorem still needs a family with controlled
geometry parameters, finite-precision convergence, residual/event detection,
and an output contract that avoids
\(\widetilde\Theta(d/(\tau\mu))\)-scale generic correction tomography.

### G. Block-angular QIPM

Disposition: **per-step result proved; end-to-end speedup open**.

Coherent border aggregation has optimal \(\widetilde O(\sqrt N)\) query
scaling for its output contract. What is missing is an \(N\)-independent
barrier parameter together with locally evaluable derivatives, a persistent
iterate representation, error propagation, and a comparison with classical
decomposition/Krylov methods.

### H. Augmented spectral Newton sketch

Disposition: **least-squares embedding lemma useful; QIPM open**.

Sampling the augmented matrix \([D^{1/2}A^T,v]\) avoids separately sketching a
Hessian and RHS. The displayed regression error bound is valid. No complete
infeasible-step analysis, implicit update mechanism, or end-to-end quantum
advantage was proved. This overlaps the unresolved rectangular direction.

### I. Static trajectory direct sums

Disposition: **online/fresh-stream lower bound proved; fixed-LP multiplication
open and cannot be inferred**.

One-step costs add for causally fresh independent oracle streams or explicit
classical transcripts. A fixed sparse LP can be read and cached, and
controlled block access can prepare time-labelled states in superposition.
No \(T\)-times-one-step lower bound for one static LP is claimed.

### J. Projective plus implicit expander family

Disposition: **the proposed family is a dead end for quantum advantage**.

When normalization is bounded, a classical randomized sketch approximates the
inactive Hessian in comparable work. Rare influential columns either make
quantum normalization large or leave only a one-time Grover preprocessing
gain. A different structured family is a genuinely new problem, not an
unfinished proof of the current candidate.

### K. Robust bounded-scale parity gadgets

Disposition: **frontier characterized; stronger simultaneous regime open**.

Linear size and constant residual robustness are achieved by the gain plateau
using height \(\Theta(\sqrt N)\). Cut/resistance and convex-mixture theorems
show why constant-height, bounded-local-dependence variants need quadratic
volume. The old phrase “linear-size real-linear gadget remains open” is to be
read as the stricter bounded-height/unit-scale regime. A simultaneous bounded
primal, slack, reduced-cost, multiplier, and full-KKT construction is not
known.

### L. Nonabelian word hardness

Disposition: **optimization construction proved; intrinsically nonabelian
query exponent open**.

The \(S_3\) holonomy objective genuinely distinguishes conjugacy classes, but
the proved lower bound restricts inputs to a transposition subgroup and hence
uses ordinary parity. No claim of a new nonabelian word-query lower bound is
made.

### M. Intermediate-error zero-versus-\(k\) state conversion

Disposition: **resolved in the constant-visibility regime after this
closure** (post-closure update): see
2026-09-02-zero-versus-k-verified-sample-state-conversion.md. A
verified-sample decoder (measure the label, verify the sampled block with
\(O(Q(f))\) fresh queries; one-sided on the no-winner branch) bypasses the
\(1/k\) collision loss entirely and, with a \(k\)-copy embedding into
Theorem P and a detuned fixed-point rejection preparation, gives
\(Q_\varepsilon=\Theta(N\sqrt{G/k})\) for
\(p=\Theta(1)\), \(k=O(G/\log^2 G)\), \(\varepsilon\le(1-c)p\), plus a
tight classical law \(\Theta(N\delta G/k)\). Referee-audited. What remains
open is only the \(\sqrt{\delta}\)-vs-\(\delta\) factor in the transition
window \(\varepsilon\to p\) (a composed small-success search theorem).
The original disposition below is retained for the record.

Original disposition: **open, with both endpoints closed**.

Exact search followed by conditional preparation costs
\(O(q_f\sqrt{G/k})\). Returning the public all-loser state costs zero queries
once the allowed error exceeds the target distance upper bound. Between these
endpoints, pairwise trace distance does not give a common measurement for the
hidden winner set, while the collision statistic loses a factor \(1/k\). A
tight result requires a state-conversion adversary or extra public
observables.

### N. Connectivity fallback

Disposition: **undeveloped; do not cite**.

The ledger's degree-two connectivity-to-LP idea never received a dedicated
proof of its residual constants, sparsities, or arbitrary-preconditioning
claim. It is weaker than the completed parity/holonomy families and remains
only a discarded lead.

## IV. Dead ends and false shortcuts retained as useful information

- A small first-inverse norm does not imply a fast DLS filtering solve; the
  second inverse can restore the full condition-number exponent.
- Sparse Hessian or KKT support does not imply a sparse inverse, cheap block
  encoding after elimination, or low circuit depth.
- Condition-one reduced Newton geometry does not make the affine feasible
  offset, coordinate gauge, transformed RHS, recovery map, or output state
  free.
- Exact Schur preconditioning can make an abstract product constant
  conditioned while moving the relevant input hardness into construction, RHS loading,
  or recovery. A freely supplied product oracle is a stronger model.
- A state output is not a reusable coordinate oracle. Global phase, norm,
  controlled/adjoint access, and block-encoding normalization matter.
- Reapplying a one-step lower bound over a fixed trajectory is invalid without
  freshness, memory, adaptivity, or explicit-output restrictions.
- Ordinary feasible short-step residual bounds do not imply finite projective
  variation. Under those contracts alone, proximal or ray-locked selection is
  not guaranteed to suppress the weak face mode while retaining the required
  residual.
- Expanderization cannot evade the convex-mixture/cut-resistance frontier
  inside the bounded-degree local-linear gadget class.
- A scalar objective gap can coexist with a central density that is
  \(O(1/G)\)-close to a public state; output accuracy must be stated.
- Pairwise distinguishability of unknown-set states does not supply a common
  public decoder.

## V. Verification record

The final closure used independent audits of:

1. the central-path asymptotics and all critical constants;
2. the equality-restricted Hessian spectrum, including \(m=d=1\);
3. the finite mass--conditioning inequalities and their visibility inversion;
4. the noncommutative approximate-centrality Loewner and curvature bounds;
5. trace-distance, collision, purification, and fresh-copy contracts;
6. the explicit unique-OR adversary and raw/coefficient query simulation;
7. multiwinner, dense-winner, nonidentical-bath limits, and edge cases;
8. exact-one/exactly-\(k\) preparation and marker-complexity scopes;
9. the concrete sparse holonomy reduction, public start, step, and
   accumulator caveats;
10. Candidates A--D and every remaining ledger direction against primary
    literature.

The audit corrected duplicated drafts, a false \(O(1)\) Rayleigh shortcut
when \(\tau\ll1/G\), marker-cost overclaims, the general multiwinner
preparation bound, missing environment copying, purification contracts, stale
crossover/lazy-refresh statuses, the state-to-diagonal novelty claim, an
undocumented connectivity fallback, and minor LaTeX/cross-reference defects.

## VI. Canonical reading order

For a paper-scale development, read:

1. 2026-09-02-general-block-logdet-condensation.md;
2. 2026-09-02-winner-take-all-global-trace-holonomy-sdp.md;
3. 2026-09-02-winner-central-path-condensation.md;
4. 2026-09-02-winner-take-all-global-trace-search.md;
5. 2026-09-02-group-holonomy-trace-one-sdp.md;
6. 2026-09-02-intrinsic-spectrum-trace-normalized-s3-parity.md;
7. 2026-09-02-continuing-sparse-qipm-frontier.md.

The files 2026-09-02-sparse-qipm-research.md,
2026-09-02-beyond-kappa-qipm-research.md, and
2026-09-02-hamiltonian-qipm-research.md are historical exploration logs.
Their surviving claims are superseded by the canonical theorem notes named
inside them; their abandoned candidates should not be treated as current
results.

## VII. Supporting, companion, and superseded filename map

The following substantive files are not separate headline directions. This
map prevents their local status language from being mistaken for a live,
unaudited candidate.

Supporting theorem or negative-result files:

- 2026-09-02-block-treewidth-output-matching.md: tight original-coordinate
  loading bound for the non-SOCP tree family. A targeted search found no exact
  collision with its condition-one bounded-treewidth solve versus
  \(\Theta(P)\) recovery/loading conjunction; parity, tree propagation, and
  state-conversion ingredients remain prior art.
- 2026-09-02-lazy-central-oracle-tradeoff.md: reusable preprocessing versus
  lazy endpoint access; supports the no-generic-per-iteration conclusion.
- 2026-09-02-free-s3-condition-one-newton-parity.md: condition-one free-qutrit
  precursor, superseded as a headline by the intrinsic-spectrum theorem.
- 2026-09-02-nullspace-affine-offset-oracle-separation.md: robust affine-offset
  corollary; the prefix-rigidified theorem is stronger.
- 2026-09-02-partition-free-compressed-dual-qipm.md: canonical conditional
  positive theorem underlying Direction F.
- 2026-09-02-prefix-hardness-vs-compressed-dual-qipm.md: compatibility audit
  between the compressed-dual theorem and prefix hardness.
- 2026-09-02-proximal-residual-certified-oss-reuse.md: Tikhonov/proximal
  no-go and certified-reuse companion to projective refresh.
- 2026-09-02-relative-value-and-parity-amplification-barriers.md: historical
  relative-value result and bounded-height amplification obstruction.
- 2026-09-02-robust-parallel-newton-initialization.md: exact quadratic-size
  robust one-step wrapper, later dominated in size by gain/prefix families.
- 2026-09-02-walsh-row-resistance-frontier.md: bounded-arity
  character-linear supplement to the cut/resistance no-go frontier.

Historical or superseded construction files:

- 2026-09-02-sparse-block-sdp-parity-state-lower-bound.md is superseded by
  the non-SOCP and intrinsic-qutrit families.
- 2026-09-02-noncommuting-three-by-three-block-sdp-parity.md is a precursor
  to the non-SOCP Schur-block and intrinsic constructions.
- 2026-09-02-two-anchor-free-root-sdp-parity.md is a precursor to the
  intrinsic trace-normalized holonomy triangle.
- 2026-09-02-winner-take-all-global-trace-sdp.md is the structural draft
  superseded by the sparse-accumulator holonomy theorem.
- 2026-09-02-beyond-kappa-results.md is a historical summary routing to
  beyond-kappa-coupling-qipm.md, effective-spectral-dimension-qipm.md, and
  stable-active-subspace-qipm.md.

The remaining audit, redirect, and accuracy-frontier files identify their
parent theorem inside the file itself. A filename-level audit of all 72 notes
found no other orphaned live direction.
