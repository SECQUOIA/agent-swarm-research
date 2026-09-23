# Stage 1, round 1: independent review 4

Verdict: no major findings; two minor findings. The stated fixed-relative-accuracy staircase and the concrete parity separation are supported by the proofs as written, subject to the local wording repairs below.

I read all of `sections/02-model.tex`, `sections/03-exact.tex`, and `sections/04-fixed-accuracy.tex`, together with the abstract and bibliography. I also checked the source staircase and definite-parity notes and the cited primary implementation/lower-bound results. I did not inspect other reviews or edit the manuscript. Joint accuracy limits, LP consequences, and a full introduction/literature treatment were outside this stage's scope.

## Findings

### R4.1 — Minor: distinguish parity lower-bound cutoffs from a proved optimal staircase

Location: `sections/04-fixed-accuracy.tex:227`, opening sentence of the definite-parity subsection; relevant results at lines 241–294.

The sentence introducing `E_r` calls them “the thresholds for an even polynomial.” The results establish a lower-bound implication below each `E_r`, and an upper construction strictly above `E_1`. They do not characterize optimal even-polynomial complexity in every tier or at equality `K=E_1`. This distinction matters immediately after a complete all-circuit staircase with proved equality cases: the parallel terminology can imply a second complete staircase that has not been proved.

The definition of `E_r` is an unconstrained approximation problem. Turning it into an optimal bounded-polynomial construction would require further argument; the lower-bound proof alone does not do that. The source definite-parity note explicitly describes the general hierarchy as a lower-bound observation with matching constructions below the affine threshold unproved.

Repair: replace the introductory sentence with, for example, “Even polynomials satisfy additional lower bounds governed by the following approximation errors.” Describe `E_1` as the affine cutoff where needed, and optionally say that no complete even-parity staircase or equality result is asserted. The displayed separation table is already careful to use lower bounds for its last two rows and needs no change.

### R4.2 — Minor: give the correct domains of two local sign assertions

Location: `sections/04-fixed-accuracy.tex:161` and `:169`, proof of the upper bound at every positive threshold.

At line 161, “the nonnegative polynomial `G_r-e(y)`” is nonnegative on `[1,rho]`, rather than on the real line. In fact `e(y)=G_r T_{2r}((y-m_rho)/h_rho)`, so `G_r-e(y)` becomes negative outside that interval. The proof uses only interval nonnegativity and is valid, but the paper otherwise makes global nonnegativity a central and carefully distinguished condition.

At line 169, the assertion `d(x)=1-x-S_N(x^2) in [0,1]` is stated “for `x>=0`.” The established bounds for `S_N` justify this for `0<=x<=1`, which includes every point used in the proof. They do not justify the unbounded half-line; for instance with `N=1`, `S_1(u)=u(1-u)/2` and `d(2)=5`.

Repair: write “the polynomial `G_r-e(y)`, nonnegative on `[1,rho]`,” and replace “for `x>=0`” with “for `0<=x<=1`.” No construction or estimate changes.

## Checks supporting the verdict

- The two-query polynomial has the claimed exact residual and global range. The sufficient condition `b>=1/2` is correct. The statement does not claim two-query optimality.
- The pairwise constants follow from the complementary output norms and the canonical oracle derivative. The normalization-slack derivative is correct, and the following paragraph appropriately explains why it is not an attainable exact tradeoff below normalization two.
- The general-parity implementation handles arbitrary oracle completions through explicit hermitianization and qubitization. The centered Laurent polynomial has degree at most `2d`, and multiplication by the inverse walk power preserves normalization. [Motlagh–Wiebe, Corollary 5](https://arxiv.org/pdf/2308.01501) supports the bounded unit-circle polynomial implementation.
- [Gilyén et al., Corollary 18 and Theorem 73](https://arxiv.org/pdf/1806.01838) support the definite-parity real-polynomial implementation and the attributed pairwise lower-bound method, respectively. The manuscript does not present either method as new.
- The explicit affine minimax error, second-Markov constant, odd-parity derivative bound, and Fejér-kernel upper construction are consistent. At `rho=2`, the strict inequalities `G_1<1/32<E_1=1/24` yield the displayed polynomial separation. Restriction to one definite-parity transform is clearly stated; arbitrary compositions are not excluded from the unrestricted model.
- The Taylor-limit lower bound, pinned equality construction, high-band tail exponents, and the separate `c=1` coarse tier are internally consistent. In particular, the pinned error estimate has sufficient vanishing order at positive contacts to achieve the exact threshold error rather than merely an asymptotic overshoot.

Counts: **0 major, 2 minor**.
