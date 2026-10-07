# Stage 3a, round 1: independent review 3

## Verdict

No major issues found. The coherent block-access statement and the optimization realizations are supported by the proofs under their stated output and oracle contracts. Three minor precision/wording fixes are needed. I read both new sections and the Section 3 accuracy extension, and did not read other review reports or modify manuscript files.

## Findings

1. **Minor mathematical precision: a constant accuracy calibration costs O(K) clock layers, not O(1).** In `sections/07-scalar-realizations.tex:449-451`, the claimed exact lower-bound parameter is `ell = log(sqrt(K)/varepsilon)/(3 alpha_K) + O(1)`. The proof instead substitutes `delta = Theta(varepsilon/sqrt(K))`, because the source reduction needs a sufficiently small absolute accuracy constant. Taking logarithms of a Theta relation adds an O(1) *inside* the numerator, which becomes O(1/alpha_K)=O(K) layers. It cannot be called bounded rounding uniformly in K. The leading Theta exponent and the theorem's scientific conclusion remain valid. **Repair:** write `ell = [log(sqrt(K)/varepsilon)+O(1)]/(3 alpha_K)+O(1)`, or choose and display a sufficiently small fixed calibration constant c and write `ell = log(c sqrt(K)/varepsilon)/(3 alpha_K)+O(1)`. Keep the original exact delta-parameterized length elsewhere. Do not absorb the calibration into an O(1) layer count.

2. **Minor parameter clarification: retain the central-path radius in the box-centering gap.** At `sections/07-scalar-realizations.tex:410-412`, the scalar signal is `rho(eta) h Phi`, whereas the perturbation estimate is `sqrt(K tau)`. Consequently a uniformly sufficient centering gap is `tau <= c rho(eta)^2 (beta-alpha)^2 delta^2/K`. The current text drops rho while saying “any fixed public eta>0.” This is correct only if its hidden constant c may depend on that fixed eta; it is false for a universal c as eta tends to zero. **Repair:** include the rho(eta)^2 factor, or explicitly use a fixed constant eta bounded away from zero, or write `c_eta` and state that the constant depends on eta. Including rho is the clearest exact statement.

3. **Minor ambiguity in the literal coordinate construction.** At `sections/07-scalar-realizations.tex:423-424`, “Multiplying the coefficients of [the accumulator] by R” could mean multiplying each entire equality by R, which leaves the output coordinate unchanged. The intended operation scales only the readout coefficients multiplying x. **Repair:** say “Replace a by tilde a=Ra in the accumulator equalities and use w as the objective.” Then the asserted one-sparse unit objective follows literally.

## Focused LP and norm-tree checks

- The affine-slice constraint forces `x=t M^{-1}e`, and maximization over `[-1,1]` yields `OPT=Rh|Phi|`. Both the unaugmented objective tilde a and the one-coordinate augmented objective have norm one under the intended accumulator replacement.
- `A_eq A_eq^T=MM^T+ee^T` gives the upper singular-value bound. The multiplicity at least two of the minimum eigenspace leaves a vector orthogonal to e with eigenvalue K^{-2}; consequently the minimum singular value is exactly K^{-1}, and `K <= kappa_2(A_eq) <= sqrt(2) K` follows. No condition claim is improperly transferred to the augmented KKT system.
- Full SQ access to the added equality column and the objective remains public. The one exceptional row norm is explicit and contains no hidden amplitude. Sampling the inverse solution is not granted in the upper-bound input contract.
- The Section 3 inverse-overlap extension to `epsilon<=R_e/2` is valid: `eta=epsilon/(4R_e)<=1/8`, the statistical sample bound stays at least a positive constant, and all polynomial and variance arguments remain valid. Applying it with the exact public R gives the upper exponent in the affine theorem. With the calibration correction in finding 1, the lower exponent matches at the stated level.
- The interval barrier has parameter one; its displayed derivative and self-concordance calculations check out. The squared affine decrement is `eta^2 OPT^2/2` in the intrinsic t-coordinate. The text correctly warns that supplying the projected scalar right-hand side would supply the hard quantity itself.
- For the box barrier, Hessian `>=2I` in u-coordinates gives objective-subproblem gap `>=||u-rho e||^2`. Its pullback and accumulator error bounds are correct. Parameter N is correct for the paired interval barrier, and the box optimal value is not equated with the ball/SOCP value.
- The binary norm tree has exactly the ball as feasible projection. The depth-symmetric gaps are `2^d/(D-1)`, giving the displayed center; stationary derivatives in the identified internal variables vanish and strict convexity gives uniqueness. At zero leaves the mixed u/t Hessian block vanishes. The bottom squared radius is `1/(D-1)`, so the leaf Hessian coefficient is indeed `c_D=2(D-1)`.
- The norm-tree Newton direction and normalized-tilt decrement both follow from that coefficient. The public tree-variable block and scaled clock block admit the claimed SQ simulation. The text correctly retains the dimension-dependent decrement scaling and product-barrier parameter, and does not assert a small condition number for the full lifted Hessian.

## Other correctness checks

- Verified the cyclic gauge, even-clock condition number, finite inverse series, exact public R, plateau mass and Hessian row-norm metadata.
- Verified the literal accumulator chain and the distinction between an accurate optimizer coordinate, the coordinate of a genuinely feasible approximately optimal point, and a full feasible vector. The quantum upper bound only claims the numerical scalar output.
- Checked the exactly public inverse-transpose norm G and its lower bound from the homogeneous recurrence on the pre-plateau interval. The plateau-only optimality statement is correctly restricted to that readout family.
- Checked the normalized tilt, objective value, direct Newton decrement and SQ mixture for its right-hand side; the two vector components have disjoint clock support. The fallback tilt is weaker but valid.
- Checked the projected approximate-vector inequalities used for sampling. The source reduction costs O(1/p) draws and therefore preserves the p factor in the lower bound. The text distinguishes per-call contamination from a reusable good-sampler setup and charges setup separately.
- Checked the generic feasible-sample upper: `||MPe-e||<=xi` follows directly from the singular-value residual; normalizing MPe gives a unit-ball point of objective gap O(xi^2), while preserving the x-block sample law. It does not yield a free norm or free coordinate oracle for the normalized feasible point, and the text explicitly says so.
- Checked the exact three-dimensional block-encoding lower family, the disjoint relative intervals and the unitary-completion distance. Exact sparse-value access bypasses that family, so the distinction in lower-bound models is necessary and correctly stated.
- Checked the fixed-transform probability error budget and the bounded polynomial/Laurent derivative obstruction. Neither is improperly presented as a general lower bound against variable-time or rational methods.

## Primary-source checks

Read the relevant primary local text and used `conda run -n qipm --live-stream pdftotext` to check formulas omitted by extraction.

- `[[shantanav2019-power-block-encoded-matrix-powers]] p.38`: Theorem 33 includes a **norm** estimate as well as state preparation. With c=1/2 and q=max(1,c)=1 it gives exactly the displayed alpha*kappa matrix cost, sqrt(kappa) preparation cost, epsilon^{-1} factor and logarithms. The input-encoding error specialization also agrees. Squaring the norm estimate only changes constants.
- `[[bansal2021-k-forrelation-optimally-separates-quantum]] p.2-4`: the positive high promise and thresholds are correct. Theorem 1.3/Corollary 1.4 give `(N/log(kN))^{1-1/k}` for fixed k, consistent with the manuscript's substitution N_work=q^ell and its polylogarithmic conversion to total dimension. The k+1 Hadamard transforms and O(k) sign queries implement the amplitude; exact numerical estimation to the fixed-k gap uses 2^{O(k)} queries.
- `[[apers2026-quantum-speedups-linear-programming-interior]] p.34-35`: Lemma 8.5 is indeed a constant-additive-error LP value lower bound with SQ(A), SQ(A^T), SQ(b), and SQ(c). The manuscript acknowledges this prior scalar optimization lower bound and confines its novelty statement to the stated parameter/interface combination.
- `[[alase2022-tight-bound-estimating-expectation-values-system]] p.1-2`: its oracle lower bound concerns the encoded observable. The manuscript's distinction between that observable-access bound and querying the inverse matrix itself is supported by the source.

## Diagnostic

`/workspace/local-home/miniconda3/envs/qipm/bin/python notes/scalar-newton-paper/scripts/verify_cyclic.py` passes the cyclic-history, public metadata, tilt, decrement, tree and completion checks. The proof review above does not rely solely on these finite numerical examples.
