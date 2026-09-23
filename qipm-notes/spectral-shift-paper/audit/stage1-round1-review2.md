# Stage 1, round 1: independent review 2

Reviewed `sections/02-model.tex`, `sections/03-exact.tex`, and
`sections/04-fixed-accuracy.tex`, with `audit/source-map.md` for scope. I did
not read another review or edit the manuscript. This review does not treat
the intentionally absent introduction, joint-accuracy results, or LP
application as omissions.

**Finding count: 0 major, 1 minor.** The principal fixed-accuracy theorem
appears correct, including exact threshold equality and the separate
coarse tier at `c = 1`.

## Minor finding: state the domains of two positivity assertions

**Location:** `sections/04-fixed-accuracy.tex:161` and `:169`, in the proof
of Proposition `threshold-upper`.

The phrase “the nonnegative polynomial `G_r-e(y)`” needs the qualification
“on `[1,rho]`.” Global nonnegativity is a central and explicitly distinct
condition in this paper, and this polynomial is not globally nonnegative:
by the displayed extremizer,

\[
G_r-e(y)=G_r\left[1-T_{2r}((y-m_\rho)/h_\rho)\right],
\]

which is negative for every `y > rho`. The factorization argument only
needs nonnegativity on the approximation interval and remains valid.

Similarly, the assertion `d(x)=1-x-S_N(x^2) in [0,1] for x >= 0` should say
`0 <= x <= 1`. As written it is false outside the contraction domain. For
example, `N=1` gives `S_1(u)=u(1-u)/2`, and therefore `d(2)=5`. Every use
of this assertion in the proof is within `[0,1]`.

**Repair:** Add the two domain qualifications. Neither correction changes
the construction, estimates, or theorem statements.

## Mathematical checks supporting the assessment

- **Exact constrained optimum.** Applying exterior Chebyshev extremality
  to the rescaled error gives the stated necessary bound at every
  negative `y`. The proposed extremizer satisfies it on that half-line.
  On the remaining exterior regions its two terms are nonnegative. On
  a negative Chebyshev lobe inside `[-1,1]`, the proof correctly uses
  `x+z_0 > 1/n^2 > G_r/h_rho`. In particular, the global nonnegativity
  proof does not assume that small error on `[1,rho]` implies global
  feasibility. Strict convexity yields uniqueness of the exterior
  maximizer. The displayed formula for `G_1` and its squared-affine
  minimizer agree algebraically with the general formula.

- **Threshold asymptotics.** In the hyperbolic coordinate, the stationary
  point is `t=a+1/n+O_rho(n^-2)`, for `n=2r`. Consequently
  `h_rho(cosh(t)-cosh(a))/cosh(nt)` has leading term
  `2 sqrt(rho) exp(-na)/(e n)`, giving precisely the stated prefactor,
  exponential rate, and logarithmic correction on inversion. Integer
  rounding is properly retained as a bounded uncertainty. Numerical
  checks with the `qipm` interpreter for `rho=1.01,2,10,100` and
  `r=1,2,4,8` were consistent with the formula and its asymptotic ratio;
  these checks supplemented the calculation and did not replace it.

- **All-circuit hierarchy.** The scalar entry remains a bounded
  trigonometric polynomial for all real oracle parameters, independently
  of the correctness promise. After rescaling, the Taylor remainder
  vanishes if the proposed lower-bound scale fails. Values at fixed
  interpolation nodes bound the coefficients; coefficient convergence
  then provides a polynomial nonnegative at every fixed real argument.
  Its odd leading degree must vanish. This proves the claimed hierarchy
  without imposing polynomial or parity structure on the converter.

- **Exact equality in the upper construction.** The paired shifted
  kernels produce an even algebraic polynomial, not merely a
  trigonometric function of `arcsin(x)`. The complementary product is
  pinned to sufficiently high order at every positive error contact.
  Its leakage is `O(delta^(1+1/r) dist(y,A)^(2r+2))`, which is absorbed
  uniformly by `delta [G_r-e(y)]`. The negative error inequality uses
  the correct sign of the upper-band approximant. The three-region
  estimate makes the global loss at most one after selecting the fixed
  constant `M`, and the high-band loss is `O(delta^(4-2/r))=o(delta)`.
  Thus no unstated positive error slack is needed at `K=G_r`.

- **Coarse tier and parity.** The coarse gates are pinned at the sole
  positive contact `y=1`. The degree-four gate when `c=1` is contractive
  for sufficiently small `delta` and vanishes at the high point. The
  interpolation lower bound correctly requires a high interval of
  positive length. The even-parity Markov constant, affine threshold
  `E_1`, Fejer-kernel expansion, and odd-parity Bernstein bound check
  out. The comparison table is appropriately restricted to one
  definite-parity transform.

- **Implementation and exact supports.** The Hermitian dilation and
  walk give the displayed invariant-plane matrix for arbitrary oracle
  completions. Multiplying the GQSP block for `R(V)` by `V^-d` yields
  the desired compression without normalization loss. The cited
  real-polynomial QSVT result allows the two-query even construction.
  The two-point factorization, pairwise constants, differentiated
  complement-norm bound, and interval impossibility argument are
  consistent.

For the implementation check, I verified the relevant statements in
[Gilyen et al., Corollary 18](https://arxiv.org/pdf/1806.01838) and
[Motlagh–Wiebe, Corollary 5](https://arxiv.org/pdf/2308.01501). The former
allows definite-parity real polynomials bounded by one, and the latter
allows ordinary polynomials bounded by one on the unit circle, as needed
by the manuscript.
