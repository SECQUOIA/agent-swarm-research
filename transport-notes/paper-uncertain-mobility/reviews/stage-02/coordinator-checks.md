# Coordinator's independent Stage 02 checks

Date: 2026-09-07. Current-stage supporting checks, before the author's handoff. They do not replace the five independent reviews of the completed section.

## Localization and source limits

For the harmonic oscillator, the heat equation with initial value one has solution `(cosh(2t))^(-1/2) exp[-x^2 tanh(2t)/2]`. Its spatial integral is `sqrt(2pi/sinh(2t))`. Integrating in t and substituting `z=exp(-4t)` gives `C0=(sqrt(pi)/2) B(1/4,1/2)=pi Gamma(1/4)/(2 Gamma(3/4))`. Independent SciPy quadrature of the heat integral gives 4.647476009400743, versus 4.647476009400967 from the gamma quotient (absolute difference 2.25e-13). This arithmetic check does not substitute for the whole-line source-space proof.

For bounded quartic unfolding parameter, anchored Poincare controls a fixed core and the quartic potential controls the tails. Weighted Cauchy–Schwarz gives an absolute source tail of order `L^(-3/2)` times the energy norm. A bounded sequence of Neumann maximizers therefore has locally weakly convergent subsequences with convergent total source integrals; energy lower semicontinuity gives the upper limit. Dirichlet inclusion supplies the lower limit. Parameter equicontinuity needs control of the perturbation `(delta mu)(1+x^2)` by the energy, not merely pointwise potential convergence.

For positive mu, neighborhoods of relative radius eta around the two roots fit uniformly in `[-R,R]` when `mu<=theta^2 R^2`, theta<1, and eta is sufficiently small. Their oscillator-scaled radii grow as `eta mu^(3/4)`. The complementary reciprocal-potential integral is `O_eta(mu^(-3/2))`, smaller than the paired harmonic response of order `mu^(-3/4)`. Quadratic curvature comparison gives the exact coefficient `C0/sqrt(2)` after eta tends to zero.

For negative mu, the whole-line reciprocal-potential test gives leading response `(pi/2)|mu|^(-3/2)` with derivative-energy error `O(|mu|^(-9/2))`. This equivalent is **not** uniform on truncated intervals under only `|mu|<=theta^2 R^2`: `R/sqrt(|mu|)` may remain finite and a fixed fraction of the reciprocal-potential integral can be missing. The required uniform envelope is valid; an exact joint negative-tail equivalent needs `R/sqrt(|mu|)` to diverge. This distinction was sent to the author before drafting.

The exact cosine-fold coordinate `z=2sin(x/2)` gives source weight w, derivative weight 1/w, and reaction weight w. For nonnegative tests with `1<=w<=w_*`, the physical response lies between `w_*^(-1)` times the canonical Dirichlet value and `w_*^3` times the canonical Neumann value. Positivity permits restricting to those tests. Sending the fixed physical neighborhood to zero makes these metric factors tend to one.

## Factors and probabilistic limits

Each cosine fold contributes `2 epsilon^(-1/2) Cpair(mu)` with `dt=(epsilon/2)^(1/3) dmu`. Two folds and density 1/4 give total coefficient `2^(q-4/3)` for high uniform-design moments. At q=4/3 the positive tail is marginal: `(C0/sqrt(2))^(4/3) log(mu_max)` with `log(mu_max)~log(1/epsilon)/3`. Thus the critical coefficient is `2^(1/3) C0^(4/3)/6`, numerically 1.6286019743790596.

For q=1 the beta coefficient `.5 C0 B(.5,.25)` equals `C0^2/sqrt(pi)`, numerically 12.18594957884120. The second-moment exponent -2/3 is more singular than the squared-mean exponent -1/2, so the second-moment coefficient is also the leading variance coefficient. These are moments among sampled wall patterns.

The limiting cosine variable has an atom 1/2 at zero. Its positive tail for `w>=2C0` is `.5[1-sqrt(1-(2C0/w)^(4/3))]`, obtained directly from the uniform parameter law. Its large-w coefficient is `2^(-2/3) C0^(4/3)`.

For sinusoidal Gaussian amplitudes, `integral g^2=pi R^2` for **any** subsequently chosen mobility. The constant source trial therefore yields `J>=2P/R^2`, even under exact observation. Rayleigh amplitude density makes its mean infinite, while the limiting zero sum `2R^(-3/2)` has finite mean and infinite second moment. The counterexample is caused by failure of uniform rate anchoring; it does not contradict the compact cosine theorem.

## Uniform bulk correction

Multiplying `-epsilon h''+kh=1` by kh gives exactly

`||kh-1||_2^2+epsilon integral k(h')^2=(epsilon/2) integral k''h^2`.

For g=c+cos(s), direct differentiation gives `k''=2(1-c^2)+6cg-4g^2`. The positive part of the constant term is only of order t=1-|c| on the zero-containing side. Together with the independently justified gap and response envelopes, the squared flux error is O(epsilon^(1/6)) uniformly in c, hence its L2 norm is O(epsilon^(1/12)). A bound on k'' alone would lose this smallness at the fold.

The limiting bulk problem has `-Db Delta b0=u-V` and `Db partial_n b0=-KV`; compatibility follows from `integral(u-V)=KPV`. The remainder is `R0=(Db/Z) integral|grad b0|^2`. C2 boundary and L2 forcing give the H2 regularity needed for a square-integrable boundary derivative. Inserting b0 bounds its surface residual by `epsilon integral|b0_trace'|^2`. The upper bound follows by dropping the nonnegative residual and using the energy-dual load norm. These yield the uniform O(epsilon^(1/12)) remainder convergence if the stated regularity theorem is invoked accurately.

## Primary weighted-Rice source inspected

The author-hosted draft of Azaïs and Wschebor, *Level Sets and Extrema of Random Processes and Fields*, is openly available at https://www.math.univ-toulouse.fr/~azais/styles/other/student/level.pdf . Theorem 6.2 (printed p.121 in this draft) gives the ordinary Gaussian Rice expectation under C1 paths, nondegenerate point law, and absence of critical zeros. Theorem 6.4 (printed p.122) gives bounded continuous weighted-root expectations using an auxiliary jointly Gaussian field. Taking the derivative as auxiliary field and then monotone limits of truncated marks supports the negative-power slope calculations. The published Wiley book is dated 2009, DOI 10.1002/9780470434642; its pagination differs. The manuscript should cite the theorem rather than conflate draft and published page numbers. These are established tools, not new results of the manuscript.

## Read-through of the completed Round 01 section

Read the complete section before and at freeze. The proofs above are present, with separate compact-fold convergence and moving-window separated-root matching. The isolated-zero theorem now explicitly requires at least one zero before stating its equivalent. The H2 Neumann step cites Grisvard Section 2.4, with the author's primary-source verification recorded in the handoff. Inspected rendered PDF page 13: formulas, margins, and page flow are readable.

One potential minor clarification for adjudication: the first display in the critical-moment proof replaces `1-c^2=t(2-t)` by `2t` and appends `[1+o(1)]` before specifying a joint t-to-zero limit. The subsequent integral argument correctly accounts for `(2-t)^(-1)` and has the right coefficient, so this is not a substantive asymptotic gap. Using the exact `t(2-t)` factor in that display would avoid suggesting that the replacement has uniformly vanishing relative error on a fixed interval ending at t0. The five independent reviewers have not been prompted with this observation.
