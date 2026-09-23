# Stage 2, round 2 — independent review 08

**Verdict: PASS.** I found no major or minor defect in the assigned frozen Stage 2. The corrected finite two-level results, parameter quantifiers, and asymptotic claims are supported by the proofs as written.

## Coverage

I read the following frozen files in `process/snapshots/stage02-round02/` in full:

- `sections/02-universal-positive.tex`;
- `sections/03-cubic-equal-means.tex`;
- `sections/appendix-positive-couplings.tex`;
- `sections/appendix-cubic-certificates.tex`;
- `sections/01-foundations.tex`, `main.tex`, `macros.tex`, and `references.bib`.

I read the round assignment and review protocol, both Stage 2 author records, every Stage 2 row of `process/scope-proposal.md`, the prior-round adjudication, and the separate correction record. I read all ten canonical Stage 2 result files identified by the assignment. I also inspected the original analytic-family and two-level audit corrections, the second-order audit, and the coefficient-removal audit. I did not read another current-round report. The accepted Stage 1 signing appendix was not re-enumerated: Stage 2 introduces no new dependency on its computation. I read the full foundations file, independently checked its positive-polynomial lemmas used here, and treated the unrelated accepted signed-bilinear external inputs as background.

After reading `literature/AGENTS.md`, I directly checked these primary-source passages:

- Luedtke–Namazifar–Linderoth, local original author PDF, pp. 8–9 and 22: vertex representation, common upper-envelope statements, nonnegative-box expansion, and Conjecture 1. I visually checked the conjecture in the original PDF. Its positive-coefficient/nonnegative-box scope matches the stated counterexample. The manuscript accurately identifies its author-version numbering.
- Sherali, local original PDF, pp. 252–256: equation (13), Theorem 3, and its proof. I visually checked equation (13). Its coefficients and index limits agree with `eq:sherali-symmetric`, after renaming the degree from Sherali's `m` to `d`.
- Hoeffding, the openly accessible original [PDF](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf), printed p. 16: visually checked Theorem 2 and equation (2.6). Its independence and bounded-range assumptions yield the manuscript's two-tail sum bound after rescaling the sample mean. An ephemeral original and rendered source pages were kept under `/tmp`, not copied into the manuscript directory.

No required Stage 2 source was inaccessible. These are direct checks of relevant source passages; they are not claims to have re-audited every result in those articles. I also visually inspected frozen PDF pages 31–32 and checked the complete two-block printed program against the supplied executable.

## Findings

None. In particular, the three smaller two-level witnesses and the within-family if-and-only-if threshold are now present and proved. The arbitrary-partition integral says “at most,” the positive logarithm is defined, and the printed checker is complete in two explicitly ordered blocks.

## Independent verification

The reproducible checker is `verification/reviewer08/stage02-round02/check.py`; its output is `results.json` in the same directory. It reads the frozen appendix for the printed program. I used `/home/sgusev/miniconda3/envs/minlp-notes/bin/python` to run it successfully. The following proof checks were performed independently of earlier audit verdicts.

### Probability laws and dyadic exactness

The shared vertex-law lemma establishes equality of the full graph hull and the vertex graph hull by independent conditional rounding. Common-threshold rounding attains all positive monomial upper envelopes simultaneously. The resulting deficiency is nonnegative for every feasible law, including at zero term gaps. This permits mixtures and omission of unneeded components without an adverse contribution.

For the dyadic example, each level contributes one to both the termwise gap and common upper value. The failure-count relaxation has the correct inequality direction. Selecting every anchor from the upper tail of the same failure count is feasible simultaneously. The affine cap has equality at the two claimed resource-profile endpoints. Mixing profiles using `B_s` and `B_{s+1}` imposes expected failure count one. A uniform XOR shift preserves prefix-hit counts and makes the conditional failure probability of each leaf exactly `R/2^L`; thus the surrogate optimum is attained for nested partitions. This step is not asserted for arbitrary partitions.

My exact rational checker independently evaluated both resource profiles for every `L=2,...,200`, checking their mixing weights, all anchor means, expected failures, pointwise equality on every supported state, and the stated objective. It also checked both choices at all ties in that range: `L=4,9,18,35,68,133`. These finite checks supplement the general prefix and affine-cap arguments.

The separate arbitrary-partition proof uses a valid Jensen measure `r(t)dt/M_0`, with the zero-density and `M_0=0` cases treated correctly. The dense predecessor has its own count LP: projecting any law gives a feasible LP point, and conditional uniform failed subsets with conditionally sampled anchors realize every LP point. The dyadic tail-integral lemma and discrete scale mixture remain complete distinct arguments.

### Harmonic parameters and asymptotic quantifiers

For every finite real `M >= d-1 >= 1`, the harmonic normalizer satisfies `1 <= A_p <= Lambda`, and direct integration gives marginal failure exactly `p`. The `p=0` rule covers boundary coordinates. On the hard-term integration interval all positive failure marginals are at most the integration variable. Inactive mass is bounded by `(d-1)t/M=eta t`. This bound is independent of ambient dimension, supports, coefficient sizes, and the number of terms. It therefore supports the global, objective-independent coupling claim.

The curve is decreasing, its integral is strictly convex, and `J(z)-z` crosses zero exactly once. The tangent mixture establishes the uniform scalar guarantee, while evaluation at the crossing proves only the stated scalar-mixture optimality. The final inverse-guarantee mixture has positive normalized weights and handles every nonlinear term class.

I re-derived the two elementary integrals used in the Lambert estimate. With `A=w-1/(2w)` and `w>=1`, one has `A>=1/2`, a positive denominator, and

`A + log A + 1/(2A) - w - log w = log(1-1/(2w^2)) + 1/(4Aw^2) <= 0`.

Thus the fixed-point comparison applies under precisely the advertised finite restriction. The theorem does not require that restriction for the integral bound itself, including the endpoint `d=2, M=1`.

The tuned choice fixes `M` as a function of degree before taking the limit: `Lambda=N+log N`, `eta=1/N`. Consequently `w=log N-log log N+o(1)`, and multiplying the denominator by `N/Lambda` changes it by `O((log N)^2/N)=o(1)`. This does not interchange a parameter optimization with an unproved uniform expansion. The reciprocal appendix instead fixes `eta=1`; its integrated cubic remainder is at most `1/(12 alpha^2)`, and its discarded endpoint terms are smaller order. The resulting `-1` and reciprocal corrections are explicitly scalar-certificate statements.

The original explicit finite and leading-constant mixtures also have valid intervals and normalizations. The largest admissible dyadic example differs from any large integer degree or dimension allowance by a bounded multiplicative factor. Padding by unused coordinates therefore extends the lower asymptotics to all integers. The simultaneous Fréchet fraction has the same sharp leading constant by summing it over that lower family.

As supplementary numerical evidence, I checked 20 integral roots and applicable Lambert bounds over degrees `2,3,16,1000,1000000` and several real cutoffs, including `M=d-1`. All passed. These checks are numerical and do not establish the universal theorem or any additional uniform asymptotic claim.

### Coefficient removal and finite interior witnesses

Both directions of the cloning construction preserve the entire feasible expectation interval. Conditional independent rounding of clone averages preserves every original multilinear monomial; identifying all clones of a group embeds every original binary law. Distinct source supports remain distinct after homogenization and cloning.

The concentration union bound covers every clone vertex plus the separate termwise-gap event. Independence is required across retention indicators, not across these events. With the original `f,n,s,d` fixed, `K^2>sn log(2)/2` makes the failure exponent strictly negative, while `t/m^d -> 0` because `d>=2`. Positive limiting hull gap then justifies ratio convergence. This proves equality of suprema with unrestricted dimension; it supplies no fixed-dimensional preservation or uniform sample size over all original instances. The manuscript states those distinctions.

The finite 25,000-variable specialization has the correct exponent `m^3/23200`, and the strict ratio margin allows the full `5t` error. The 25-variable padding loss is `1840/1000`; the explicit 52-variable loss is `120(20/1000)=12/5`. Neither estimate assumes independence between padding variables and original coordinates. The claimed upper and lower termwise values remain unchanged at the stated padding means. Positive hull gaps follow from independent versus common-threshold rounding at the interior means.

### Cubic certificates, bounds, and limits

Concatenating both frozen verbatim blocks reproduces the frozen executable byte for byte. Running that extracted code passed every three-group integer inequality (`343+729+274625` states), all exact primal probabilities and count means, the three primal–dual equalities and ratios, and all two-group inequalities (`25+81+169+289` states). Conditional uniform subsets convert the count certificates into full singleton-marginal laws, so count enumeration covers every relevant binary vertex. The exact smaller ratios are `27/16,21/11,99/50`; the `m=16` ratio is `135/67`. The monotone lower bound at and above `m=20` completes the claimed threshold among positive multiples of four.

I independently solved the scalar stationary equations, re-derived both eliminated quartics, and exactly expanded all five Bernstein rows. Their minimum coefficient is `901/120000`, giving the reduced lower endpoint `1610000/743033`. The constrained first-order argument on `c<=3/10` has the correct outward derivative sign; unrestricted elimination on the remaining range gives a valid lower bound regardless of where its optimizer lies. The analytic-family count correction is uniformly at most `72/m`. Its certified ratios prove a supremum lower bound; the text correctly avoids claiming convergence of actual ratios to that endpoint.

Both two-level square identities were checked symbolically. Their equality atoms give all required means, and conditional independent sampling supplies the reverse finite bound. Thus these families do have proved convergence of their actual ratios, unlike the analytic three-group family. The older rational variant, finite `m=50` bound, analytic `m=36` specialization, and explicit homogeneous unit witness remain covered.

For the cubic upper bound I checked the complete case partition, including all four one-low cases, the all-high independent estimate, and separate quadratic cases. The orientation proof uses nested exclusion intervals and decreasing geometric weights correctly. I independently integrated the actual orientation and bounded-failure laws using rational intervals on 1,122 sorted quadratic/cubic tuples with coordinates in `{0,1/16,...,1}`. Every tuple satisfied the `12/31` guarantee, including classification boundaries. This exact finite check supplements the continuous case proof. The three limiting test configurations and cancelling weights establish only fixed-mixture termwise optimality, as stated.

### Equal means

The adjacent-count distribution preserves every singleton mean and works simultaneously for every degree. Discrete convexity of `binom(K,d)` proves attainment by each elementary symmetric polynomial. The independent comparison gives `q_{n,d}<=u^d<u`, so every denominator in the finite optimization is positive. Fixing `u` first makes the dimension-free optimizing degree one of two finite integers; taking that fixed degree as dimension grows justifies the claimed limit without interchanging an unbounded degree maximum and a limit.

The monotonicity on each side of `u/(1-u)` and Bernoulli's inequality establish the optimizer and factor two. I additionally checked 38,688 rational `(n,u,d)` cases for `2<=n<=32` and marginal denominators through 13, including the candidate optimizer comparisons and finite denominator inequalities. The unit-cube scope is stated explicitly and is not replaced by an unsupported exact positive-box formula.

## Remaining limits

This review does not determine the exact value of `R_3`, establish a matching second-order lower bound, certify novelty absence, or turn any finite test grid into a universal proof. I did not generate a 25,000-variable sample, solve all large finite-family envelopes, re-run the unrelated accepted Stage 1 signing computation, or perform the later whole-paper integration review. None is required for the Stage 2 statements as currently scoped. No manuscript files were edited.
