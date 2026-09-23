# Stage 2 independent review 3

Scope: `sections/02-locality.tex`, `appendices/locality-scope.tex`, accepted foundations, macros, and the relevant coverage entries. Primary focus was the intrinsic partial-observation theorem, its singular-covariance proof, and the shared residual-to-precision argument. I did not read other reviewer reports or change manuscript files.

## Verdict and classified findings

**No MAJOR issues identified. No actionable MINOR issues identified.** Stage 2 is acceptable from this review's mathematical and stated-scope perspective. Numerical tests below support the independently reconstructed argument; they are not substitutes for its proof and do not establish literature priority.

## Independent proof reconstruction

1. **Shared precision transfer (lines 118–140).** The matrices `BB^T` and `B^TB` are square, invertible and have the same eigenvalues. The claimed factors `1-delta` and `1+delta`, rather than their reciprocals, therefore do follow for `R^(1/2) Q R^(1/2)`. Addition of a positive-semidefinite prior is valid even when the prior or sensitivities are singular. The prior-aware upper bound uses only `delta<1`.

2. **Transport for singular latent covariances (lines 595–625).** The process promise gives `A Pi_previous^+ A^T <= gamma^2 Pi_current^-` because `Pi_current^- <= P_current`. Joseph's posterior identity gives `E Pi^- E^T <= Pi^+`. Their alternating congruences give the stated transport inequality without an inverse of `Pi`. The process promise is stronger than mere positive process noise but is explicitly imposed; the theorem does not treat this assumption as automatic filter stability.

3. **Endpoint and gain estimates (lines 627–649).** For possibly singular `Pi`, the representation through `Pi^(1/2)` and `M=Pi^(1/2) H^T V^(-1) H Pi^(1/2)` is valid. The measurement promise bounds all eigenvalues of `M` by the signal constant. Both displayed identities are obtained from a Woodbury identity that only inverts `I+M` and `V`, so they do not implicitly assume a latent inverse. The eigenvalue inequalities `u/(1+u)<=kappa` and `u/(1+u)^2<=kappa/(1+u)` prove the two estimates. The range factorization at lines 643–647 correctly sets the nullspace rows to zero and thus handles moving or unequal latent supports.

4. **Different fresh histories (lines 651–673).** For a far residual pair, the earlier residual uses its own history, giving `Cov(X_s,Z_s)=Pi_s^{-,s} H_s^T`. The later filter can be initialized at time `s` with unconditional `P_s`: its actual selected history begins strictly after `s`, so unconditional propagation to that history gives exactly the same later gains and target innovation covariance. Future process and observation noises have zero cross covariance with `Z_s`. Consequently transport of the earlier cross covariance really uses the later filter's matrices, not those from the earlier history. Bounding `U D_s^(-1) U^T` by `kappa P_s` before transport and applying the target endpoint estimate gives `kappa gamma^(t-s)`. The old-observation argument similarly gives `sqrt(kappa signal) gamma^(t-j)` with normalization by `V_j`, as claimed.

5. **Regression coefficient and overlap (lines 674–689).** A particular raw observation coefficient is its own Kalman gain followed by later update and transition matrices. It is not an innovation coefficient with a mismatched history. The gain covariance bound starts this transport from the posterior covariance and the target endpoint supplies the second square-root factor, giving `kappa gamma^(s-j)`. Inserting the observation-noise square roots in the residual-pair identity has the correct order. Multiplication of the old-covariance and coefficient bounds produces exactly the stated `kappa sqrt(kappa signal)` near coefficient. The double geometric sum and symmetric block row estimate contain no hidden packet-dimension factor.

6. **Exact boundaries and Euclidean corollary (lines 690–729).** Zero observed signal and zero process contraction eliminate cross-time observation covariance even if latent covariances are singular. Positive observation noise still makes the full observation covariance positive definite, consistent with the foundations. `q I >= (q/Pbar) P_t` proves the Euclidean reduction. The older unnormalized constants follow from the weaker gain covariance estimate and the same transport. Their comparison with the intrinsic bound uses nonnegative scalar inequalities and is correct.

7. **Broader checks.** I reconstructed the common overlapping-history row calculation, the exact complete-observation Markov path factorization and forward/reverse telescoping, the spacing-floor monotonicity argument, the weighted-conjugation decay estimate, and the supplied block-metric equivalence. I found no mismatch with the partial-observation theorem. The appendix correctly limits the covariance-parameter extension to exact Markov information, and does not infer covariance-parameter Fisher control from mean-information precision bounds. Its KL-to-relative-spectral implication and repeated-pair separation are consistent; the supermodularity example is attributed specifically to the thesis and distinguishes ordering conventions.

## Independent validation

Created only reviewer-owned `verification/stage02-review3/check_partial.py` and its `results.json`. The script constructs observation covariances directly from six time-varying state models with:

- Seven candidate packets, four-dimensional latent states and two-dimensional partial observations.
- Rotating latent supports of ranks one, two and three; every latent covariance is singular.
- Noncommuting transitions, varying correlated observation-noise matrices, three contraction rates and three signal-to-noise bounds.
- Every nonempty schedule and every calendar window from zero through complete history.

The verification uses direct dense Schur regression, rather than the manuscript's Kalman implementation or the repository's existing result producers. All **5,334 schedule/window cases**, **10,752 far-pair bounds**, **21,504 old-observation bounds**, and **17,472 coefficient bounds** passed. The largest ratios of observed norm to theoretical bound were approximately 0.989865, 0.989842 and 0.957088 for the three endpoint-based estimates, and 0.530224 for the global bound. Direct eigenvalue checks also confirmed that the normalized-residual error and the relative-precision error coincide to floating-point tolerance. These near-unit endpoint ratios are useful stress checks rather than merely very loose random examples.

Command: `code/research_20260912/.venv/bin/python paper-correlated-measurements/verification/stage02-review3/check_partial.py`.

## Primary-source and scope check

Read `literature/AGENTS.md` before source inspection. Checked the local original PDF for Kozdoba et al., *On-Line Learning of Linear Dynamical Systems: Exponential Forgetting in Kalman Filters*, PDF pages 6–8, especially Theorems 1 and 2 and equations (18), (24), (30)–(34). These support the manuscript's description of covariance-norm process-noise dissipation, observable time-invariant systems, and approximation after burn-in. The manuscript appropriately states its finite-horizon and every-fresh-history specialization without calling covariance contraction or finite-memory filtering new. I did not attempt an exhaustive independent priority search for all other locality references, and no finding here certifies absence of earlier equivalent results.
