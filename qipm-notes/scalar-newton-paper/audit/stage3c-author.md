# Stage 3c author report

Authored `sections/10-structured.tex`, integrated it into `main.tex`, added seven
primary bibliography entries, and added `checks/check_structured_identities.py`.
Earlier sections were not modified.

## Results developed and checked

- General sparse-base plus low-rank theorem with singular/indefinite coefficient
  matrix, source-vector SQ access, explicit entry-estimation tolerances and
  vector perturbation constants. The proof controls the small inverse without
  assuming that transformed correction columns have visible norm.
- Raw rectangular/singular rejection proposals and a coefficient-weighted
  mixture yield the exact squared-coordinate distribution of a fixed
  approximate vector on the good setup event. Setup failure and per-draw
  flagged failure are separate. The inverse Frobenius guard and finite trial
  cap bound runtime even on failed statistical setups. No exact output norm
  is promised.
- Relative positive inverse-form corollary with independently sampled scalar
  readout and an explicit polynomial second-moment bound.
- Lorentz inverse and eccentricity reduction with the supplied radial-vector
  SQ contract; generalized-power Hessian, dimension-free comparison and
  nonsymmetric coefficient reduction without diagonalizing an estimated core.
- Power-core scalar `t` is sampled from the original weight vector. Its
  physically valid clipping interval preserves the two-dimensional determinant
  bound. The derivative identity `L'=L E11 L` supplies the explicit
  `100 Lambda^4` Lipschitz constant; coefficient perturbation is propagated
  all the way to the final vector and scalar output.
- Exact and constant-relative geometric-mean acquisition lower bounds, with
  equal norm pairs and charged original SQ access. The bounded logarithmic
  range escape requires alpha-weight sampling, which is not supplied by
  ordinary squared-weight SQ access. Retained the logarithm-cone diagonal
  plus rank-three observation with a positive invertible diagonal base; no
  uniform sampling theorem is inferred.
- Eccentricity threshold, preconditioned residual certificate, primal energy
  identity, supplied-width setup/apply costs, sorting cost for threshold
  selection, and sharp rank-two charge within the specified preconditioner
  class. Quasidefinite augmentation is separated from numerical stability.
- One-hub exact Lorentz KKT expansion, explicit reduction to the published
  row-column bipartite treewidth theorem, two-hub regularized reusable factor,
  regularization perturbation bound, generic positive-diagonal hub minimum,
  and the coarse-incidence forest example. Joint Lorentz lift curvature is
  excluded as the existing source ledger requires.
- Full-output sparse CGLS and factorization comparisons, with total dimension
  included in the CGLS arithmetic bound. Replacement along a trajectory
  requires hypotheses uniformly over legal iterates and the actual robust
  outer residual contract; it does not assume different directions generate
  the same path.

## Source gaps corrected or replaced

The notes' low-visibility column-discarding discussion does not specify a
sufficient statistical classification and fixed-output perturbation protocol.
It is replaced entirely by raw proposals from the original vectors, so no
visibility test is needed. Estimating the generalized-power direction norm
and then speaking of exact normalized eigenvectors/SQ access would also need
extra error accounting. The new representation retains the diagonal map
inside every local evaluation and never grants that exact norm.

The source expected rejection cost did not explicitly bound runtime on bad
setup outcomes; a zero approximate output could otherwise make the loop
infinite. The theorem now caps every loop and states the conditional law and
failure events precisely. Power coefficient estimates are clipped to the
physical interval, rather than merely to a broad norm interval. All these
changes strengthen the rigor of the conditional one-solve result; they do
not invalidate the cone algebra or justify an end-to-end IPM claim.

## Literature checks

Consulted the local literature topics `sparse-qipm-structural-boundaries.md`
and `classical-baselines-benchmarking.md`, including their cautions on fill,
ordering, repeated factorization, and finite precision. Primary online checks:

- Roy--Xiao, *On self-concordant barriers for generalized power cones*,
  Optimization Letters 16(2),681--694 (2022), DOI
  10.1007/s11590-021-01748-7. Author PDF Theorem 1 is precisely the barrier
  and parameter used: https://www.microsoft.com/en-us/research/wp-content/uploads/2018/01/powercones-5a71024933c4b.pdf
- Goldfarb--Scheinberg, Mathematical Programming103(1),153--179 (2005),
  DOI10.1007/s10107-004-0556-1. Publisher explicitly compares product-form
  Cholesky with Woodbury numerical stability; no new low-rank identity claim.
- Chen--Goulart, JOTA204,Article33 (2025),
  DOI10.1007/s10957-024-02573-5. Publisher full text establishes the earlier
  sparse-plus-low-rank and regularized quasidefinite cone approach.
- Chia--Gilyén--Li--Lin--Tang--Wang, JACM69(5),Article33,72pp (2022),
  DOI10.1145/3549524; primary arXiv1910.06151v4. General SQ low-rank matrix
  arithmetic and sampling are attributed; the present theorem instead has
  a full-rank sparse base and explicit indefinite-correction access.
- Kapelevich--Andersen--Vielma, JOTA202,271--295 (2024),
  DOI10.1007/s10957-022-02076-1, arXiv2201.04121. Publisher distinguishes
  online publication in2022 from issue publication in2024. Inverse-Hessian
  operators precede this manuscript.
- Vanderbei, SIAM J. Optimization5(1),100--113 (1995),
  DOI10.1137/0805005. Strong factorability is cited only as an exact
  arithmetic property, not a floating-point stability theorem.
- Fürer--Hoppen--Trevisan, ESA2025,LIPIcs351,116:1--15,
  DOI10.4230/LIPIcs.ESA.2025.116. Primary Dagstuhl statement explicitly
  permits arbitrary fields and consistent-system solution in width-squared
  arithmetic with a supplied compact row-column bipartite decomposition.

No first-ever sampling, cone algebra, Woodbury, Krylov, or low-treewidth
elimination claim is made. Specific original contribution positioning is
left to the manuscript synthesis stage, using these explicit comparators.

## Verification

`/workspace/local-home/miniconda3/envs/qipm/bin/python checks/check_structured_identities.py`
passes 152 numerical identities, including indefinite and singular cores,
near-null transformed columns, raw rectangular trial probabilities,
independently finite-differenced power Hessians, clipping endpoints and
coefficient derivatives, Lorentz inverse identities, and KKT Schur solves.
These diagnostics supplement the analytic proofs and are not proof certificates.

The qipm build produces a 53-page staged manuscript. Final log inspection is
recorded by the lead agent. No unresolved mathematical claim is knowingly
left in this stage; the five independent reviews remain required.
