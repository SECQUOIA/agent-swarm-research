# Independent mathematical review: exact rational realization

Reviewed `sections/arithmetic.tex` against the stable model and regridding sections and the assigned arithmetic brief. The mathematical assertions were independently checked, including the degree-zero and degree-one cases, zero smoothness, repeated/contained bags, empty separators, positive-dimensional boxes after fixed-coordinate elimination, arbitrary tree structure, and retained incumbents from earlier stages of a fixed-grading run.

No literature discovery, knowledge-base operation, computational experiment, project-wide check, or CI inspection was performed.

## Verdict

The realization is mathematically sound. It supplies a genuine exact implementation for explicit sparse rational polynomials of fixed total degree, with no general convex-optimization oracle. The affine model error, deterministic endpoint minimization, stage coordinate denominator invariant, common cost denominator, message magnitude and scalar-bit bounds, explicit polynomial-term costs, and compact proof representation are correct. The unknown-growth search is valid when its budget includes all elementary computation and final output work.

Two small operational clarifications would remove avoidable ambiguity from verification and output accounting. Neither affects the analytic theorem or the displayed asymptotic bounds.

## Concrete clarifications

1. **Verifier center membership.** In the compact-certificate verification proof, explicitly check that the stored center belongs to $X$, that the stage index is nonnegative and the grading exponent is a positive integer, and regenerate the canonical shell partitions using those values. The shell coverage theorem requires a center in the domain. The current phrase “checks the generated partitions” can reasonably include these checks, but an independent verifier should not silently trust a certificate field needed for coverage.

2. **Charge final output before accepting a trial.** In the elementary-bit budget search, explicitly include certificate serialization and output writing among the charged trial operations, and accept a candidate only when its gap test and output serialization both complete within its budget. If a budget expires after a valid test but before output completion, discard that trial and continue. The sufficiently graded run's bound already covers $O(pNm^p(J+1)b_J)$ output work, so the same $O(T_*\log T_*)$ search bound holds. This makes the last paragraph's output-size assertion operationally precise.

An optional computational-model clarification is to state that bit work uses a bit-cost random-access model. Alternatively, balanced dictionaries keyed by the bounded-length identifiers realize table lookup in $O(\mathfrak b_J^2)$ bit work per access. The present identifier allowance in $\mathfrak b_J$ is sufficient either way; no asymptotic change is required. A pure tape-machine claim without a lookup implementation would need additional explanation.

## Independently verified mathematics

### Computable curvature and the affine Taylor model

For one monomial of degree $d$, summing the absolute second derivatives over ordered coordinate pairs gives the coefficient $d(d-1)$. Since $R\ge1$ bounds every original coordinate magnitude, the termwise Hessian entry sum is at most $|c|d(d-1)R^{d-2}$. The operator norm is bounded by this entry sum, so $M_0$ is sound. Terms of degree zero or one contribute zero. With fixed $D$, the common coefficient denominator and a fixed power of the rational denominator of $R$ give $O_D(L)$ bits for the entire bound and polynomial-time exact construction.

At the leaf midpoint, $\|v-m_B\|^2\le p\operatorname{width}(B)^2/4$. The Taylor remainder lies between $\pm Mp\operatorname{width}(B)^2/8$. Subtracting precisely that quantity yields a lower model with error between zero and $Mp\operatorname{width}(B)^2/4$, hence the bag contract with $A=Mp$. This remains valid for affine or constant data and $M=0$. A supplied $M\ge M_0$ is exactly checkable; a smaller bound properly needs a separate sound certificate.

Every local objective is an affine bag model plus affine child bounds minus an incoming affine slope, on a rational coordinate-box intersection. Sign-based endpoint selection exactly minimizes it, including zero coefficients and fixed face coordinates. The selected endpoint rule, rather than mere rationality of an arbitrary minimizer, is what prevents denominator growth.

### Coordinate and cost denominators

Every shell endpoint at stage $j$ has form $c_i+s_0t2^{-(j+\mu)}$ with integer $t$. This holds for the central grid as well as every positive shell level. Clipping, projection, intersection, and endpoint selection only choose existing endpoints. Starting from denominators dividing $Q$ therefore gives the invariant $Q2^{j+\mu}$ and the midpoint invariant $W_j=Q2^{j+\mu+1}$. Endpoint magnitude is bounded by $R$ after clipping; temporary unclipped endpoints have at most a constant multiple of that magnitude and the same bit-order bound. Reconstruction selects an endpoint and closes the induction. Midpoints are never used as future centers.

For $D\ge1$, polynomial values have denominator dividing $C_{\mathrm{coef}}W_j^D$, derivatives divide $C_{\mathrm{coef}}W_j^{D-1}$, and multiplying a derivative by an endpoint or midpoint restores exponent at most $D$. The affine correction divides $8q_M(Q2^{j+\mu})^2$. Thus all mathematical cost entries divide $Z_j=8q_MC_{\mathrm{coef}}W_j^{\max(D,2)}$. For $D=0$ derivatives vanish; for $D=1$ the exponent-two denominator still covers any supplied positive smoothness correction.

No multiplication of inherited message intercepts occurs: they are added, subtracted, or selected by minima. The subtree induction therefore preserves one common denominator instead of multiplying child denominators. A retained incumbent chosen at an earlier stage of the same fixed-grading run also has a coordinate denominator dividing the current coordinate denominator, so its objective fits the same $Z_j$. Separate search candidates restart from the original center, as stated; the invariant should not be applied blindly to an arbitrary center transferred between grading candidates.

When evaluating affine objectives, an implementation should retain the derivative/endpoint denominator structure before scaling to $Z_j$, or use exact scaling of the reduced product. Storing every scalar over $Z_j$ and then naively treating its product with a coordinate as an unrestricted rational product would introduce an unnecessary denominator $Z_jW_j$. The manuscript's prescribed polynomial-numerator and exact-scaling method avoids that problem and realizes the claimed invariant.

### Magnitude and scalar lengths

The total absolute bag midpoint values are at most $SHR^D\le\mathcal H$. Gradient--displacement contributions total at most $D\mathcal H$, because each midpoint displacement is at most $R$ and the total gradient one-norm is at most $DSHR^{D-1}$. Corrections total at most $NMpR^2/2$.

A common separator slope component is at most $kD\mathcal H/R$. Each separator-copy difference is at most $2R$, and there are no more than $Np$ separator coordinates across all edges. Hence the configuration slope terms are at most $2NpkD\mathcal H$. A message-intercept expansion has one additional incoming unpaired term, at most $pkD\mathcal H$. Since $2N+1\le3N$ for $N\ge1$, the displayed $V$ bounds all such objective and intercept values. Subtree expansion, rather than iterating a loose message bound, is the right argument.

All magnitudes have logarithm $O_D(L)$, because $N,p,k,S$ are bounded by the explicit input size and the numerical input magnitudes have $O_D(L)$ bits. Together with $\log Z_j=O_D(L+j+\mu)$ this proves the scalar-bit bound. An input coordinate itself need not be bounded by the cost magnitude $V$ in a degree-zero instance, but it already has the separate $O(L+j+\mu)$ coordinate-bit bound; the conclusion is unaffected.

### Polynomial terms and bit work

Fixed total degree gives at most $D$ variable factors per monomial counted with multiplicity. Sparse derivative evaluations can be formed without dividing by a coordinate, so zero coordinate values cause no exception. Initializing dense bag gradient/model coefficient vectors costs $O(p)$ per bag leaf, which is included separately. If an input uses dense exponent tuples, scanning them is also covered by the coarser factor $p(N+S)$.

The stage operation count conservatively covers midpoint polynomial/gradient evaluation, center gradients and subtree sums, parent-leaf/child-intercept aggregation, all touching incidences, affine coefficient assembly and corner evaluation, comparisons, and exact incumbent evaluation. This verifies the explicit factor $S$ and the absence of an uncharged value/gradient oracle. Summing stage counts gives the cubic stage factor.

Schoolbook multiplication and exact integer division on $O(\mathfrak b_J)$-bit integers cost $O(\mathfrak b_J^2)$. Fixed-degree exponentiation only needs a fixed number of such operations. Common scaled-integer representations reduce additions and comparisons to integer operations. List identifiers and counters are covered by $p\log(m+1)+\log(J+2)$, while coordinatewise work is already paid by the outer factor $p$. The resulting bound is a conditional bit realization with numerical $m^p$ explicitly retained, not polynomial time in $L$ for arbitrary conditioning or variable bag dimension.

### Compact serialization and verification

There are $O(Nm^p(J+1))$ leaves and cells, with at most $p$ endpoint coordinates each. The number of parent-leaf/child intercept entries is at most $(N-1)m^p(J+1)$ because child degrees sum to $N-1$. Storing shared slopes once avoids per-incidence repetitions. The affine models and deterministic corner witnesses can be recomputed, so there is no need to serialize one separate local optimization proof for each own-cell incidence.

The certificate bound's use of $b_J$, rather than $\mathfrak b_J$, is valid: list identifiers can be coordinate-index tuples with one $O(\mu+\log(J+2)+L)$-bit entry per coordinate, and the outer factor $p$ pays those tuples. Stage and bag identifiers also fit the stated overall bound. Canonical list order can remove many explicit references altogether.

Recomputing all nonempty affine local minima exactly verifies the inequalities. Checking every touching child cell verifies each minorant. The original objective evaluated at the interval-feasible incumbent and the root bound verify the final gap. Model soundness is ensured by $M\ge M_0$, and validity needs no certificate of global quadratic growth. The explicit center-membership check suggested above completes the regeneration/coverage logic.

### Unknown growth and the countdown

For a sufficient $\mu_*$ and comparison work $T_*\ge\max\{2,2^{\mu_*}\}$, round $R_*=\lceil\log_2T_*\rceil$ includes the candidate and allows its full run. The total trial budgets satisfy $\sum_{r=1}^{R_*}r2^r\le4T_*\lceil\log_2T_*\rceil$. Every trial uses valid models; the exact gap test remains sound for insufficient grading. No numerical estimate of $g$ enters the algorithm.

The binary countdown can be implemented with its head at the low-order digit between decrements. Its borrow-chain traversals and digit changes sum geometrically over a full countdown, hence cost $O(2^r)$ rather than $O(r2^r)$. An end marker or equivalent highest-active-digit marker allows exhaustion detection within that amortized bound. Initial counter setup and round enumeration are lower-order costs covered by the trial-budget sum. This establishes only a constant scheduling overhead in addition to the displayed logarithmic search overhead.

The final output must be charged as suggested above; the fixed-sufficient-run work bound has enough slack to include serialization and does not change. Unknown curvature needed for lower-model soundness is correctly excluded from the grading search.

## Checks performed

Targeted reading only: `sed` and `rg` on the arithmetic manuscript and the existing audit. All constants and divisibility assertions were checked by independent algebraic reasoning. No executable numerical checker, computational experiment, TeX build, project-wide test, or CI check was run in this review.
