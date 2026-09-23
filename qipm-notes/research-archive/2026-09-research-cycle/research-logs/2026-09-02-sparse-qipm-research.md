# Sparse QIPM research log

**Started:** 2026-09-02  
**Status:** superseded by the audited results in
`notes/research-archive/2026-09-research-cycle/supporting-results/sparse-qipm-structural-results.md`. The entries below preserve the initial search
path; they should not be read as final claims.

## Research standard

A result is promoted to a candidate contribution only if it has:

1. a precise input, access, output, and error model;
2. a complete proof or a reduction to explicitly cited theorems;
3. a matched structure-aware classical comparator;
4. an adversarial review for hidden normalization, conditioning, refresh, and readout
   costs; and
5. a targeted open-literature novelty search that finds no prior statement of the same
   result.

"Not found" is evidence of novelty, not proof of novelty.

## Initial evidence

The existing synthesis in `notes/background/literature-surveys/ipm-sparsity-quantum-advantage.md` rules out the
shortcut "sparse input implies cheap QIPM." The relevant sparse object is the Newton
operator, and its block-encoding normalization, condition number, changing diagonal
data, and output cost must all be charged. Two established results sharply constrain
the search:

- van Apeldoorn, Cornelissen, Gilyén, and Nannicini characterize pure-state
  tomography with state-preparation-unitary access. Dense \(\ell_2\) recovery costs
  \(\widetilde\Theta(N/\epsilon)\) unitary queries, but their Section 5.3 also gives
  support-sensitive tomography for sparse vectors. This suggests a possible positive
  result when *Newton directions*, not merely Newton matrices, are sparse or
  compressible.
- Apers and Gribling prove a sparse-row quantum lower bound for constant-precision LP
  solving and give an explicit-output QIPM for tall LPs. Their result already supplies
  an \(\Omega(N)\)-scale lower bound on square separable LP families, so an elementary
  output-size lower bound alone would not be new.

## Candidate A: support-adaptive hybrid QIPM

### Proposed statement (not yet verified)

Take a convergent inexact hybrid QIPM whose iteration theorem accepts an approximate
scaled Newton direction with \(\ell_2\) error at most \(\eta_t\). Suppose the normalized
scaled direction at iteration \(t\) is exactly \(k_t\)-sparse (or has a quantified
\(k_t\)-term tail), and a QLSA provides controlled preparation and inverse-preparation
access to that direction. Replacing dense tomography by sparse-vector tomography
should reduce direction recovery from
\(\widetilde O(N/\eta_t)\) to approximately
\(\widetilde O(k_t/\eta_t)\) QLSA state preparations in the exact-sparse case.

If the iterate and the diagonal Newton scaling are held in an updateable data
structure, applying the recovered sparse step changes only \(O(k_t)\) entries. The
per-iteration classical update and dynamic diagonal refresh can then be support-sized,
rather than dimension-sized. The intended total ledger is

\[
  \widetilde O\!\left(
    \sum_{t=1}^{T} {k_t\over\eta_t}
    Q_{\mathrm{state},t}
    + \sum_{t=1}^{T} k_t
    + C_{\mathrm{static}}
    + C_{\mathrm{final\ output}}
  \right),
\]

where \(Q_{\mathrm{state},t}\) must include effective block-encoding condition and
normalization. A full explicit final vector still costs \(\Omega(N)\) once.

### Proof obligations and risks

- Use the exact sparse-tomography theorem, including its threshold/tail promise,
  failure probability, gate cost, and phase convention; do not infer a \(k\)-bound
  from rank-based density-matrix tomography.
- Translate normalized-state error and norm recovery into the precise scaled Newton
  residual accepted by an inexact feasible IPM.
- Show positivity/neighborhood preservation after thresholding.
- Specify how sparse classical coordinate updates induce a valid changing block
  encoding without hiding an \(N\)-cost normalization or rebuild.
- Compare with a classical active-set, localized, or sparse-direct solver that receives
  the same support promise. Exact sparsity may make the quantum gain disappear.

## Candidate B: treewidth/full-output speedup ceiling

### Proposed statement (not yet verified)

For a family of Newton systems with a supplied width-\(\tau\) elimination ordering,
sparse direct solution takes \(O(N\tau^2)\) arithmetic operations and
\(O(N\tau)\) storage under the standard scalar-elimination model. Any algorithm that
must emit an unrestricted dense classical Newton direction takes \(\Omega(N)\) output
operations. Hence its speedup over this classical baseline is at most
\(O(\tau^2)\); for constant \(\tau\), there is no asymptotic speedup in \(N\).

This is a useful structural no-go boundary, but it is currently too close to a direct
combination of standard treewidth elimination and output-size facts to call a
publishable theorem. Novelty would require a stronger oracle lower bound, an LP
central-path construction, or a trajectory-level statement.

## Candidate C: a QIPM-specific tomography lower bound

Construct a sparse, uniformly well-conditioned LP Newton step whose normalized
direction ranges over a hard family of arbitrary pure states. Composing that
construction with the tight unitary-access tomography lower bound would prove that a
full-vector hybrid QIPM step needs
\(\widetilde\Omega(N/\xi)\) state-preparation calls even when Newton sparsity and
condition number are constant. The key unresolved issue is making the hard direction
arise at a legitimate central-neighborhood iterate without turning the theorem into a
statement only about an artificially supplied linear-system right-hand side.

## Early novelty check

Targeted searches on 2026-09-02 found extensive work on QIPM tomography overhead,
sparse-row LP query lower bounds, sparse QLSA lower bounds, and sparse-vector quantum
tomography. No source found in the initial pass states a support-adaptive inexact QIPM
with support-sized dynamic diagonal refresh, or a QIPM-specific tomography reduction
that remains hard for constant-sparse, constant-conditioned Newton systems. These are
the two claims to check most aggressively.

## Final audit outcome

The initial support-adaptive algorithm does **not** follow from sparse input or a sparse
optimum. The complementarity row forces linear pair support in a short step, and any
latent sparse representation with column locality \(g\) obeys \(gk=\Omega(n)\).
Sparse tomography remains only a conditional substitution and additionally needs norm
and real-sign recovery.

The strongest surviving new candidate is instead a lower-bound lifting theorem. A
balanced standard-form LP embeds any suitable sparse QLS instance in a strictly
feasible OSS short step with \(\sigma=1-\alpha/\sqrt n\). The OSS preserves condition
number and sparsity up to constants; the exact step reduces complementarity by
\(\sigma\), remains in the central neighborhood, and has constant probability on the
hard dual block. An independent algebra audit and direct numerical checks confirmed the
equations and probability bound.

Other surviving pieces are the fixed-pattern box LP with condition-one central systems,
the treewidth-two KKT precision restriction, and an exact-treewidth structural
corollary of the Apers--Gribling LP lower bound. Ratio-based outlier correction and
multiplicative lazy diagonal maintenance collided with classical prior art
(Baryamureeba; Bellavia et al.; Lee--Sidford), so the main note demotes that material to
a projective-variation refinement and makes no quantum runtime claim.
