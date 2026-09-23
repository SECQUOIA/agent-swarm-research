# Lead-agent checks to resolve in later author stages

These are investigation notes, not manuscript theorems or certification.

## Stage 3b

The multiplexed notes' random-target direct-sum argument leaves average
success 7/12 after truncation under a hard distribution. Repetition does
not automatically amplify a distributional average advantage. Select the
hard distribution at a fixed error just below 5/12 from the outset;
constant-error randomized complexities are comparable, so this proves the
claimed lower bound directly. Do not copy the unsupported amplification
sentence.

If retaining robust checkpoint rank, explicitly normalize approximate stored
rays. The QR-volume bound depends on a bound for every column norm. The
method also charges residual certification rather than assuming it free.

If retaining the sharper R<=r approximate-checkpoint result, its stable
representation hypothesis must apply to the exact versions of the previously
selected checkpoint rays whenever a new ray is dependent. Stability in one
unspecified final basis alone does not certify the adaptive algorithm.
The exact scalar centrality dilation is a separate path-geometry result,
not a theorem about querying inverse forms; do not import its constants just
because its title says scalar. Route neighboring parity/search comparisons
according to their mathematical role and existing manuscript overlap.

Primary references checked by the lead agent for this stage:
Brody--Kim--Lerdputtipongporn--Srinivasulu, Theory of Computing 19(11),
1--14 (2023), DOI 10.4086/toc.2023.v019a011, Theorem 1.1 applies to
expected randomized complexity of partial Boolean functions. A worst-case
query lower follows since it dominates expected complexity; constant-error
expected and worst-case complexities agree up to constants by truncation
and bounded-error amplification. Buhrman--Newman--Roehrig--de Wolf,
Theory of Computing Systems 40(4),379--395(2007),
DOI 10.1007/s00224-006-1313-z, Corollary 3 gives joint Boolean recovery
of n instances at O(nT) coherent subroutine calls. It is not a joint
real-valued estimation theorem.

## Stage 3c

Investigate avoiding the low-visibility-column truncation in the power-cone
notes entirely. For S=CC^T and correction G=CED with public small D and
SQ source columns E, estimate G^T P G through E^T C^T P C E and G^T P b
through E^T C^T P b. These are sparse-polynomial local evaluations with
bounded operator norms; they do not require SQ access to Ce_j or its norm.
Likewise use raw proposals for P b and P C e_j in the final mixture.
The denominators depend on known transform bounds and source norms, and
the total acceptance probability depends on the norm of the whole output.
This should remove division by a small individual column norm.

For generalized-power cones, A_alpha=sum alpha_i^2/k_i is generally not
exactly computable under the stated SQ interface. Estimation must produce a
fixed, accurately approximated low-rank correction. One route is to keep
unnormalized positive-coordinate directions alpha_i/sqrt(k_i)/||alpha||,
whose norm is between 1/sqrt(2 Lambda) and 1; raw proposals can start at
alpha/||alpha||, retaining the diagonal 1/sqrt(k_i) inside the transform.
Do not silently grant exact norms or exact eigenvectors derived from an
estimated A_alpha. Work out explicit polynomial stability bounds.

An alternative that also avoids eigenvalue-sign continuity: write the
normalized inverse correction as X L X^T, with X columns obtained by
known norm-bounded sparse diagonal maps from supplied unit SQ vectors.
For power cones, use x-direction alpha/(||alpha|| sqrt(k)) and radial
z/||z||. Their Gram matrix is diag(t,1), where
t=E_(alpha^2/||alpha||^2)[1/k] lies in [1/(2 Lambda),1]. The normalized
Hessian has the form I+X B X^T, with explicit two-by-two B, and its inverse
correction coefficient is L=-(I+B X^T X)^(-1)B. Only t requires estimation.
Check symmetry, positivity preservation and polynomial sensitivity directly.

For a general reduced system N=S+C X L X^T C^T with CC^T=S and ||X||<=1,
avoid L^{-1}: use the small core I+L K, K=X^T C^T S^{-1} C X. If
N>=a S, then
(I+L K)^(-1)=I-L X^T C^T N^{-1} C X
has norm at most 1+||L||/a. This is a direct stable formula even when L is
singular or indefinite. Approximate K with X^T C^T P C X and h with
X^T C^T P b. Local SQ estimators can start at the original supplied source
vectors and include their diagonal maps inside the sparse local evaluation.
No norm of an individual C X column is needed. The final raw mixture uses
P b and P C X_j directly, with known operator-norm proposal bounds.
The author must supply the full error/rejection analysis before claiming
the resulting theorem; this outline is not that proof.

Additional lead-agent calculations to verify in the author stage:

- Write kappa for the condition of S, L0>=||L|| and D=1+L0/a.
  With ||b||=1, K<=I, ||h||<=sqrt(kappa), and z=(I+LK)^(-1)Lh,
  one has ||z||<=D L0 sqrt(kappa). If ||Khat-K||<=rho,
  ||hhat-h||<=nu and D L0 rho<=1/2, then
  ||zhat-z||<=2D L0(nu+rho D L0 sqrt(kappa)).
  For a residual-eta polynomial, the vector P b-P C X zhat differs
  from N^(-1)b by at most
  eta kappa(1+D L0)+4D L0 sqrt(kappa) nu+
  4D^2 L0^2 kappa rho (eta<=1).
  Since ||N^(-1)b||>=1/b_upper, all required tolerances are polynomial.
- P has norm <=2 kappa and P C has norm <=2 sqrt(kappa).
  Raw proposal denominators can therefore use these public bounds and
  a common sparse-walk count W. A coefficient-weighted mixture has
  denominator Z<=4 W kappa^2(1+16 D^2 L0^2); an additional (r+1)
  Cauchy--Schwarz rejection gives the exact distribution of the fixed
  approximate output, without component norms.
- IMPORTANT power-cone clipping detail: t must not merely be clipped to
  [1/(2 Lambda),1]. For public lambda and c=||alpha||^2, clip to
  [1/(2 lambda), min(1,1/(2 lambda c))]. The actual t lies here.
  This retains c t<=1/(2 lambda), which gives determinant>=1 for
  the two-dimensional normalized Hessian for every clipped estimate.
  The Gram matrix is diag(t,1). On this whole interval, its similarity
  transform has eigenvalues in [1/(4 lambda),4 lambda], so the small
  inverse norm is <=4 lambda sqrt(2 lambda), and the coefficient
  L(t)=-(I+B diag(t,1))^(-1)B is polynomially Lipschitz (a coarse
  O(Lambda^7) derivative bound suffices). Its norm is <=10 Lambda^2
  by conjugating Q^(-1)-I with Gram^(-1/2).

- Runtime/failure detail for the randomized low-rank setup: a bad estimate
  could create a singular small core or an approximate output of zero norm.
  Guard the small inverse and coefficient norms, and cap rejection trials
  using the public acceptance lower bound valid on the good-setup event.
  Return an explicit failure flag if the cap is reached. On a good setup,
  truncation does not change the conditional accepted sample law; its
  failure can be made as small as desired. State setup failure separately
  from per-draw flagged failure, and do not assert unconditional expected
  runtime for an unbounded rejection loop on a potentially bad setup.
- If the structured theorem is stated for relative solution-vector error,
  add a scalar corollary useful to this paper. With N<=b_upper I and
  N>=a S>=a/kappa I, q=b^T N^{-1}b>=||b||^2/b_upper and
  ||N^{-1}b||<=kappa||b||/a. Requesting vector error of order
  epsilon*a/(b_upper*kappa) controls the scalar bias. An independent
  SQ(b) inner-product estimate then gives a relative q estimate with a
  polynomial sample cost (a coarse variance bound suffices). This does
  not require claiming an optimal prefactor or an SPD approximate map.
