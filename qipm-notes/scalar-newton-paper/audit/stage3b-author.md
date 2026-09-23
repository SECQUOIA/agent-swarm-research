# Stage 3b author report

Scope: scalar trajectory composition, one-coordinate endpoint composition,
and the limitations and opportunities for reuse. The author stage adds
`sections/08-temporal.tex`, `sections/09-reuse.tex`, their `main.tex` inputs,
six bibliography entries, and `checks/check_temporal_identities.py`.
Earlier reviewed section files were not changed.

## Developed results

- Classical random-target direct sum with an explicit minimax distribution
  chosen at success 9/16. Truncation leaves 7/12, giving a contradiction
  directly. The source's proposed amplification of distributional average
  success is not used.
- Sparse box LP increments: exact central path, telescoping nonnegative
  kernel, uniform leakage bound, approximate-centering transfer, fixed-k
  extension, and two distinct joint-success quantum outputs. Boolean
  recovery gives O(B) at error 0.21h; actual numerical estimation gives
  O(B log B) at error h/100. Absolute checkpoint values remain a stronger
  sum-estimation task. The paired interval barrier gives parameter BN0;
  counting every scalar logarithm would give a valid but weaker 2BN0.
- SOCP ordinary predictor squared decrements: exact radial inverse-Hessian
  identity, scale sensitivity, summed off-diagonal tails, classical direct
  sum, short-step scale, and fixed-k extension. The O(B) Boolean midpoint
  point is proved with analytic derivative bounds rather than trusted
  floating-point constants. The dynamic active-block norm interface lower
  charges setup plus all B answers, jointly correct with probability 2/3.
- LP threshold compiler: full uniqueness and objective-gap proofs, sparse
  equality encoding of activation times an implicit overlap, XOR facets,
  one bounded optimizer coordinate, full-SQ simulation, classical strong
  XOR and coherent Boolean-recovery/parity bounds. Positive-high fixed-k
  promises are consistent with the reviewed preceding section. Equal and
  geometric objective weights have different approximate-optimizer gaps;
  XOR facets couple the central path. Public readout rounding uses a
  narrower effective promise gap and explicitly handles values slightly
  outside [-1,1].
- Signed parity endpoint: literal bounded carrier, exact central path,
  localized transitions, Theta(BL) single-scalar complexity, objective-gap
  dependence, and the different accuracy needed for a normalized sum.
- Fixed sparse KKT ray: exact block equations and common state, one-shot
  transfer, bounded-Dikin movement proof, self-contained four-sparse
  signed-tree witness with condition Theta(L), and width-three KKT bags.
  Read-once reuse, the coefficient-word query cap, and the direct scalar
  identity c^T x(eta)=rho(eta)c^T M^-1 e make the noncomposition scope
  explicit. Mori's precision-sensitive state lower is attributed only as
  a comparator; it is unnecessary for the counterexample.
- Residual-certified recycling: exact rank bound, robust 2r-1 refresh bound
  with normalized approximate columns and complete QR-volume argument,
  stable ell1 refinement tied to previously selected exact rays, explicit
  testing costs, holomorphic Chebyshev-width proof, and a strictly
  complementary QP counterexample. The normalized two-coordinate QP ray
  has a singularity approaching the parameter interval, so the failure of
  a uniform ellipse is demonstrated for normalized rays as well.
- Certification and dense output: unique search under coordinate access
  (free exact RHS norm would reveal its answer), and an approximate dense
  sign-vector lower under a canonical bit/value oracle. The latter uses
  the multilinear-state dimension bound and Hamming-ball counting.

## Source routing

`audit/source-map.md` records the six main notes as incorporated, and the
nearby parity/state note as a concise comparator. The exact scalar
centrality-dilation problem is separate path geometry. The one-Lorentz
counting and simplex/search constructions are excluded as independent
scalar counting/search programs; their relevant access and output lessons
are explicitly captured here without importing their separate cone/path
geometry as new inverse-form results. The full source Mori precision-clock
matching cache calculation is not reasserted; the elementary witness proves
the required noncomposition result without that external construction.

The corrected parity-chain comparator states the strict two-sided relative
value threshold below 1/2 and notes that its terminal optimizer coordinate
is one in both parity cases. It therefore does not accidentally use that
constant coordinate as the hard readout.

## Literature verification

Consulted local records for Brody et al., Buhrman et al., Beals et al.,
Mori et al., Parks et al. Primary online verification used:

- Brody et al., Theory of Computing 19(11), 1–14 (2023), Theorem 1.1:
  <https://theoryofcomputing.org/articles/v019a011/>.
  The complexity in that theorem is worst-input expected randomized cost.
- Buhrman et al., Theory of Computing Systems 40(4), 379–395 (2007),
  Corollary 3 and the coherent subroutine model:
  <https://homepages.cwi.nl/~rdewolf/publ/qc/robust_journal.pdf>.
  This is joint Boolean recovery, not joint real-valued estimation.
- Beals et al., Journal of the ACM 48(4), 778–797 (2001):
  <https://arxiv.org/abs/quant-ph/9802049>.
- Mori et al., Quantum Science and Technology 11, 035063 (2026), current
  arXiv version 2 revised 24 August 2026:
  <https://arxiv.org/abs/2601.16697>. The first author's name is Hitomi.
- Parks et al., SIAM Journal on Scientific Computing 28(5), 1651–1674
  (2006), DOI 10.1137/040607277:
  <https://vtechworks.lib.vt.edu/items/590c07fe-a0c8-49b2-9494-be5061f5fbf7>.
- Binev et al., SIAM Journal on Mathematical Analysis 43(3), 1457–1472
  (2011), DOI 10.1137/100795772:
  <https://www.mimuw.edu.pl/~wojtaszczyk/Publikacje/BCDDPW_10.pdf>.

The manuscript credits direct sums, quantum Boolean recovery, XOR
composition, polynomial-method parity lower bounds, and classical
recycling/reduced-basis methods. Its qualified contribution language
concerns the explicit sparse wrappers, quantitative kernels, and precise
output/access/reuse contracts. It does not claim the classical recycling
idea or Boolean composition theory as original.

## Validation

Run with the qipm environment:

```
/home/sgusev/miniconda3/envs/qipm/bin/python checks/check_temporal_identities.py
conda run -n qipm --live-stream make
```

The deterministic diagnostic covers increment leakage, SOCP sensitivity and
midpoint constants, LP threshold optimization and objective gaps, fractional
XOR stability, signed-tree matrix structure and exact KKT solutions, and
rank/QR-volume calculations. These finite checks supplement the proofs;
they are not numerical evidence substituted for proof.

The integrated staged PDF builds to 44 pages. The final LaTeX and BibTeX
logs contain no warnings, unresolved references or citations, or overfull
or underfull boxes. The author stage is ready for the required five
independent reviews; it is not yet marked reviewed or complete.
