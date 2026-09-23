# Stage 3c, round 1: independent reviewer 5

Verdict: no major mathematical issues found. Two minor statement-clarity
issues should be corrected. I reviewed the whole new Section 10, its source
notes, source-map dispositions and author audit. I did not edit the manuscript,
read other reviewers' reports, or delegate this review.

## Numbered findings

1. **Minor — make the blockwise sampling contract explicit in the cone
   corollary.** `sections/10-structured.tex:310–319` says, for `L_c` blocks,
   to supply `SQ(z)` or `SQ(alpha), SQ(z)`. The reduction actually uses a
   separate source-vector oracle and norm for every selected block. Ordinary
   SQ of a concatenated vector need not provide this: conditioning on a
   block with very small squared mass can be expensive. The one-block
   discussion at lines 218–219 refers to block norms, and the intended
   contract is clear from the proof, but the multi-block corollary should
   explicitly say **SQ access separately to each block vector, including
   each block norm**. This is particularly important in a paper whose other
   results distinguish free conditional block norms from aggregate iterate
   access. No theorem change is needed under the intended blockwise access.

2. **Minor — restate the local hypotheses of the full-output profile
   proposition.** `sections/10-structured.tex:424–450` starts a new structural
   comparison and asserts that `P_theta` is positive definite without
   expressly carrying forward full row rank of `A`. The preceding cone
   corollary imposes that condition, but its theorem-local hypothesis is not
   a clear global assumption for the new subsection. **Fix:** begin the
   profile construction with a full-row-rank `A=[A_1 ... A_L]` at interior
   Lorentz points and explicitly identify `H_j` as the Hessian of
   `-log(t_j^2-||z_j||^2)`. This also makes the same meaning of `H` explicit
   for the inverse identity at lines 203–210. Without full row rank, for
   example when `A=0`, the stated positive-definiteness assertion is false;
   with it, the proof is correct.

Major findings: none. No other minor mathematical findings.

## Technical verification

### Sparse base and sampled correction theorem

I checked the core identity without assuming that `L` is invertible or
positive. Writing `C=S^(1/2)V` gives an orthogonal row map and yields
`0 <= K <= I`, `||h|| <= sqrt(kappa)`, and
`J=I-L X^T C^T N^(-1) C X`. The latter gives the stated `1+ell/a` bound
even when the small system is nonsymmetric. The polynomial bounds, Gram and
right-hand-side bias bounds, entry-estimator second moments, and conversion
from entrywise error to matrix/vector error are consistent.

The small-system perturbation gives
`||zhat-z|| <= 2 U_* (nu + rho U_* sqrt(kappa))`. Propagating polynomial and
coefficient errors yields all three terms of the displayed vector error.
The supplied choices make each term at most `epsilon/(12 beta)`, while
`||N^(-1)b|| >= 1/beta` converts to the requested relative bound. The
separate Frobenius inverse guard does not reject a good setup and makes no
unsupported spectral-certification claim.

The rejection construction never normalizes a potentially tiny transformed
column. A rectangular raw trial has probability
`|(Tv)_i|^2/(W B_T^2 ||v||^2)`, including for singular `T`. The mixture and
second rejection cancel the component denominators and leave exactly
`|ytilde_i|^2/((r+1)Z)`. The `Z` upper bound and nonzero-output lower bound
give the stated acceptance floor. Capping independent identical trials
preserves the accepted conditional law and bounds runtime even on an
incorrect statistical setup. The good-event versus per-draw failure
distinction is explicit. The positive-form corollary correctly uses an
independent scalar estimator and a smaller vector tolerance.

### Cone reductions and scalar acquisition

The Lorentz inverse has the stated radial and tangential eigenvalues. Its
normalized rank-two coefficient has norm at most `chi_max-1`, and the two
orthogonal source directions fit the general theorem.

I independently checked the generalized-power Hessian by differentiating
`p`, the barrier, and its mixed derivatives. The chosen diagonal base and
two-dimensional correction agree. For every point in the clipping interval,
`ct <= 1/(2 lambda)` gives determinant at least one and trace at most
`4 lambda`. This controls both eigenvalues. The identity expressing `L(t)`
through the symmetric `Q(t)` establishes symmetry, the norm bound, and the
derivative formula `L'=L E11 L`; its Lipschitz constant is valid. The sampled
quantity is the expectation of `1/k_I` under squared-weight sampling, as
claimed. No exact norm for the contracted positive-coordinate direction is
silently granted.

In the cone corollary, the fixed estimated coefficient matrix causes a
whitened perturbation at most `v`. The Loewner and resolvent bounds propagate
this through the inverse, and the two setup failure budgets are sufficient.
The claimed polynomial parameter cost survives the tighter scalar tolerance.

The equal-norm pair construction indeed makes the geometric mean an injective
function of Hamming weight while all original SQ calls cost at most one
source query. In the growing logarithmic-range example, consecutive geometric
means have ratio greater than three, so every relative error strictly below
one half still determines the weight. The ideal-real-arithmetic and range
limitations are stated. The aggregated logarithm-cone rank-three identity
also checks; the text correctly declines to infer a uniform sampling result
from that identity alone.

### Profile and latent-width comparisons

With the full-row-rank hypothesis, summing block comparisons proves the
profile Loewner bounds and positive definiteness. The PCG condition is at
most `theta^2`; inverse Loewner comparison gives the exact residual energy
certificate, and elimination gives the claimed equality of primal barrier
energy and multiplier normal energy.

I checked assembly, factorization, update-core, application and matrix-product
costs, including the dense `m b_theta` correction storage. The indefinite
Woodbury core is nonsingular by the determinant identity. The alternative
augmentation is quasidefinite because the complete negative rank correction
leaves a positive definite base. The text separates this exact factorability
from finite-precision stability. Sorting and ties in the order-statistic
choice do not invalidate the bound.

The rank lower bound's inertia argument is valid for its stated `A=I`
witness: rank below `2b` leaves the required nullspace intersections and at
least one uncorrected high or low generalized Rayleigh quotient. The stronger
Loewner rank statement is likewise valid on that witness family; it should
continue to be read within that family, not as an assertion for arbitrary
compressive equality maps.

The one-hub Hessian identity, equality-KKT Schur complement, and nonsingularity
argument are correct. Doubling each scalar graph bag into row and column
copies produces the advertised bipartite width and preserves connectedness.
The supplied compact-decomposition assumption matches the cited elimination
result. For the two-hub version, the negative downdate is strictly smaller
than the positive diagonal base, and dual regularization gives the claimed
quasidefinite partition. The regularization bias is the ordinary Neumann
bound on the original KKT system. The three-index proof of the positive
diagonal one-hub obstruction is valid under its nonzero-coordinate and
dimension assumptions. The coarse-incidence bag construction gives
`max{2w+1,3}` as written.

Finally, the consistent full-column-rank CGLS residual estimate follows from
CG on the normal equations, and the arithmetic count includes vector work
through `M+D_K`. The output lower bound and trajectory replacement discussion
are properly limited to materialized directions, matched access, exact
arithmetic and a robust outer algorithm whose assumptions hold uniformly
over permitted iterates.

## Source coverage and attribution

The five main notes listed for this stage are represented at the appropriate
level: Lorentz and generalized-power conditional SQ algorithms; the profile
preconditioner and its limitations; latent width and regularized alternatives;
and the sparse full-output comparison. The source-map explicitly excludes
the separate joint-lift curvature/barrier-geometry program rather than
silently presenting its omission as coverage. The old transformed-column
visibility sketch is replaced by a complete raw-proposal construction, and
the author audit records that correction.

The section credits existing cone algebra, low-rank factorization, SQ matrix
arithmetic and sparse elimination. It does not make an unsupported first-ever
claim for these ingredients. Its specific contribution positioning is
reserved for the later synthesis stage, which should preserve these
boundaries.

Primary literature checked:

- [Roy–Xiao, author manuscript](https://www.microsoft.com/en-us/research/wp-content/uploads/2018/01/powercones-5a71024933c4b.pdf):
  the generalized-power barrier and parameter match the quoted result.
- [Chen–Goulart, publisher full text](https://link.springer.com/article/10.1007/s10957-024-02573-5):
  prior sparse-plus-low-rank cone Hessians and quasidefinite augmentation
  support the attribution. Their generalized-power presentation has three
  signed columns within the same small correction subspace, so the paper
  correctly avoids claiming the underlying low-rank structure as new.
- [Fürer–Hoppen–Trevisan, ESA 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2025.116):
  the supplied bipartite decomposition, arbitrary-field and consistent-system
  width-squared theorem matches the latent-width invocation.

The direct DOI pages for Goldfarb–Scheinberg and Vanderbei were inaccessible
through the browsing tool in this review. Their stated uses are consistent
with the primary Chen–Goulart treatment and the explicit algebra checked
above; this review does not treat a failed page fetch as independent metadata
verification.

## Diagnostics

Ran with the required environment:

`/home/sgusev/miniconda3/envs/qipm/bin/python notes/scalar-newton-paper/checks/check_structured_identities.py`

All 152 numerical identities and comparison checks passed. The conclusions
above rest on the derivations, with these diagnostics as supplementary checks.
