# Independent review: generic kinetic-fold moment orders

Reviewed 2026-09-07 by `review_degenerate_mobility`, independently of the derivation in [generic-kinetic-folds.md](generic-kinetic-folds.md).

**Verdict:** the stated scalar order theorem passes under assumptions 1–3. The arbitrary-integrable-mobility lower bounds, the critical logarithm, and the graded upper bounds are consistent and admit the detailed estimates below. The subsequently added finite-bulk order corollary also passes under its stated fixed-domain, positive bulk-diffusivity, positive constant-affinity, and nonzero-mean-velocity assumptions. No mathematical flaw was found. This review does not establish novelty or sharp constants.

## Geometry and uniformity

The compactness assertions used in the proof follow from the assumptions, rather than requiring an extra bound on the number of roots.

At each simple zero, a sufficiently small product neighborhood has `|g_s|` bounded below, with fixed sign. For every parameter value it contains at most one spatial root. At each fold, a product neighborhood has `|g_ss|` bounded below, with fixed sign. Strict convexity or concavity implies at most two spatial roots there for every parameter value. A finite collection of these neighborhoods covers the compact zero set. Consequently the number of roots is uniformly finite. On the closed part of the zero set outside retained open fold neighborhoods, continuity gives a uniform positive lower bound on `|g_s|`.

Also, `c↦∫g(s,c)²ds` is continuous. It cannot vanish at any parameter: that would make the entire spatial profile zero and contradict the finite transverse-fold assumption. Its minimum on the compact parameter interval is therefore positive.

Near a fold, the nonzero derivative `g_c` allows the zero curve to be written `c=C(u)`, with

\[
C'(s_j)=0,\qquad C''(s_j)=-g_{ss}(s_j,c_j)/g_c(s_j,c_j)\ne0.
\]

Hence `|C'(u)|≍|u−s_j|`, and the two root positions at parameter distance `|c−c_j|≍r²` have distance and separation comparable to `r`. Their slopes satisfy `|g_s|≍r`. The local potential comparison `k_c(s)≍r²(s-u)²` holds on a fixed sufficiently small multiple of that root distance. All comparison constants can be chosen uniformly after shrinking finitely many fold neighborhoods.

The density assumptions imply parameter measure `p(C(u))|C'(u)|du≍r du` on a retained root-position shell. Upper bounds need only the density upper bound; lower bounds use its positive lower bound near one fold. No derivative condition on ordinary root motion is needed.

## Lower bounds for arbitrary nonnegative integrable mobility

For a moving root in a shell of length comparable to `r`, use a bump of width `ℓ` and let `m` be the mobility mass in a fixed spatial enlargement. The derivative energy is

\[
B(u)=\ell^{-2}\int D(s)|\psi'((s-u)/\ell)|^2ds.
\]

Tonelli's theorem applies since its integrand is nonnegative, and gives

\[
\int B(u)du\le C m/\ell.
\]

The reaction energy is at most `Cr²ℓ³`, while the squared source integral is `cℓ²`. The function `x↦(x+b)^{-q}` is convex for **every** `q>0`. Jensen's inequality can therefore be applied to the derivative energy even for `q<1`; it does not require convexity of `J↦J^q`.

Using the parameter weight comparable to `r`, the resulting lower bound is

\[
\mathbb E[J_c(D)^q;\text{retained shell}]
\ge c_qr^2\ell^{2q}
\left[\frac{m}{r\ell}+r^2\ell^3\right]^{-q}.
\]

Choose `ℓ=κ(m/r³)^{1/4}`. The condition `m≤c_*r⁷` ensures `ℓ≤c r`, so the bumps lie in the required neighborhood. Both denominator terms have comparable order, proving

\[
\mathbb E[J_c(D)^q;\text{retained shell}]
\ge c_qr^{2-5q/4}m^{-q/4}.
\tag{R1}
\]

Only local mass appears; concentration of `D` into arbitrarily narrow spikes does not evade the estimate. If `m=0`, derivative energy is zero on every retained bump and the quotient diverges as the width tends to zero. The response definition using smooth tests is sufficient throughout; a diffusion generator for an irregular competitor is unnecessary.

For `q<8/5`, retain one fixed small shell. Its mass is at most `M`, and eventually satisfies the small-mass condition, yielding `c_qM^{-q/4}`.

At `q=8/5`, choose geometric shells with a sufficiently large fixed scale ratio so that both their spatial enlargements and parameter images are disjoint. Restrict to `r_n≥C M^{1/7}`, choosing `C` large enough that every mass `m_n≤M` meets the bump condition. There are `N≍log(1/M)` shells. Equation (R1) and the shared budget yield

\[
\mathbb E J_c(D)^{8/5}\ge c\sum_{n=1}^N m_n^{-2/5}
\ge cN^{7/5}M^{-2/5}.
\tag{R2}
\]

If any retained mass is zero, the inequality holds with an infinite left side. The exponent `7/5` is the sum of the number-of-shells exponent and the convex budget-sharing exponent; disjointness avoids double counting either budget or probability.

For `q>8/5`, take a bump of width `R=M^{1/7}` centered at one fold. Taylor expansion gives `k_c≤CR⁴` on its support whenever `|c−c_j|≤cR²`. Its derivative energy is at most `CM/R²`, reaction energy at most `CR⁵`, and source integral comparable to `R`. Thus `J_c≥cR^{-3}` throughout a parameter window of probability at least `cR²`, giving the lower order `M^{(2−3q)/7}`. Extra roots elsewhere cannot invalidate any of these lower tests.

## Uniform upper bounds for the graded designs

For the proposed nonnegative exponent

\[
\alpha=\max\{0,(6q-4)/(q+4)\},
\qquad D_M=A(\rho+R)^{-\alpha},
\]

integration near each of finitely many distinct sites gives exactly the three normalization orders in the derivation. With its choices of `R`, these imply `A≍R^{α+6}`. Since distance to the site set is bounded above and `α≥0`, the global minimum mobility is comparable to `A`. Thus an ordinary root cannot be harmed by sitting at a different fold's spatial site.

Neumann bracketing is in the correct direction: allowing independent functions on a finite partition enlarges the variational supremum, so the full response is bounded above by the sum of interval responses. Potential-only estimates may then be used on intervals free of roots.

### Ordinary-root interval estimate

On an interval centered at a root, suppose `D≥d`, `k≥a x²`, and the interval half-width is at least a fixed positive multiple of the oscillator length `ℓ=(d/a)^{1/4}`. Rescaling by `ℓ` bounds the interval response by

\[
C d^{-1/4}a^{-3/4}.
\tag{R3}
\]

The needed constant is uniform even when the rescaled interval grows without bound. To see this, bracket a fixed central interval, whose Neumann energy is coercive, and estimate its two exterior pieces by `∫x^{-2}dx`. Bounded rescaled interval lengths bounded away from zero are handled by compactness. This fills in the uniform interval harmonic-oscillator estimate used in the main proof.

For a fold-side root with `r≥CR`, take `d≍Ar^{-α}` and `a≍r²`. Its oscillator length divided by `r` is comparable to

\[
(A/r^{\alpha+6})^{1/4}\asymp(R/r)^{(\alpha+6)/4}.
\]

Thus (R3) applies and gives `CA^{-1/4}r^{-3/2+α/4}`. The remaining local fold region has reciprocal-potential integral at most `Cr^{-3}`: scaling its spatial coordinate by `r` leaves an integrable reciprocal of `(x²−1)²` after fixed neighborhoods of the two roots are removed. The ratio of this remainder to (R3) is at most `C(R/r)^{(α+6)/4}`, so it is absorbed.

### Central fold window and rootless side

For `|c−c_j|≤CR²`, use an interval of radius `KR`, with `K` fixed large enough to contain any nearby roots. On it `D_M≍R⁶`. After setting `s−s_j=Ry`, the derivative and potential parts of the operator both have scale `R⁴`. The rescaled potential converges uniformly to `(a_j y²+b_jτ)²`, where `|τ|≤C`, `a_j≠0`, and `b_j≠0`.

The rescaled Neumann forms have a uniform positive coercivity constant. Otherwise a sequence of unit-`L²` fields with energy tending to zero would converge to a nonzero constant, while the limiting quadratic-square potential would force that constant to vanish. No member of this compact potential family is identically zero. Consequently the integrated inverse is at most `CR^{-3}`. Outside the central interval, the local reciprocal-potential integral has that same bound.

On the rootless side with `|c−c_j|≥CR²`, the local normal form gives the bound `C|c−c_j|^{-3/2}`. Other ordinary roots must still be included and together contribute `CA^{-1/4}` by the global positive mobility lower bound and uniformly nonzero slopes. The main note includes this necessary term. Fixed positive-potential pieces contribute a uniform constant.

### Integrating the bounds

There are uniformly finitely many interval contributions, so `(Σa_i)^q≤C_qΣa_i^q` applies for all fixed positive `q`, including `q<1`. The root-side moment integral is

\[
CA^{-q/4}\int_R^{r_*}r^{e-1}dr,
\qquad e=2-3q/2+\alpha q/4.
\]

When `q>2/3`, `e=(8−5q)/(q+4)`; for `q≤2/3`, `α=0` and `e>0`. This gives respectively the finite-upper-end integral, the critical logarithm, and the lower-end integral at `q<8/5`, `q=8/5`, and `q>8/5`.

The central parameter window contributes `CR^{2−3q}`. The rootless integral is bounded, logarithmic, or of this same order according as `q<2/3`, `q=2/3`, or `q>2/3`. When `e>0`,

\[
\frac{R^{2-3q}}{A^{-q/4}}\asymp R^e\to0.
\]

Thus neither changes the low-order bound. At criticality, `A≍M/log(1/M)` and the root integral is

\[
A^{-2/5}\log(1/R)\asymp
M^{-2/5}[\log(1/M)]^{7/5}.
\]

The central and rootless orders then contain one fewer logarithmic factor. For `e<0`, `A^{-q/4}R^e=R^{2−3q}=M^{(2−3q)/7}`, while the ordinary-root contribution `A^{-q/4}` is smaller. Every matching upper order in the theorem follows.

## Added finite-bulk corollary

I checked both the application and the general positive-background estimate in [review-risk-sensitive-finite-bulk.md](review-risk-sensitive-finite-bulk.md).

The generic family has uniform bounds `0≤k_c≤K_0` and `∫k_c≥κ>0`. For a mobility lower bound `D≥m>0`, anchored Poincaré gives `Q[f]≥cm||f||₂²`. The resolvent `h=H^{-1}1` consequently satisfies `J≤C/m`, `||h′||₂≤C/m`, and `||h||∞≤C/m`. Positivity and testing against 1 give `w=kh≥0` and `∫w=P`.

With normalized Fourier coefficients, `|ŵ_n|≤1` and `Σ|ŵ_n|²≤||w||∞`. Splitting the zero-mean `H^{-1/2}` norm at `N≍2+||w||∞` gives

\[
\|w-1\|_{H^{-1/2}}^2\le C[1+\log(2+\|w\|_\infty)]
\le C[1+\log(1/m)]
\]

in fixed units. The finite-bulk load annihilates constants, so the trace and bulk Poincaré estimates bound its dual norm by this expression. Dropping the nonnegative Schur boundary penalty yields the claimed logarithmic bound on the bulk remainder. No derivative of the graded mobility enters this estimate.

Here `m_M≍A`, and all three normalizations give `log(1/m_M)=O_q(log(1/M))`. Thus the explicit trials have a remainder at most `C_q[1+log(1/M)]`, uniformly in the parameter. For arbitrary competitors, setting the bulk test function to zero in the full variational formula gives `D_flow≥(KV²/Z)J`; the inverse Schur identity is unnecessary for this lower bound. It remains valid for extended responses.

The moment inequality for every `q>0` and the fact that each scalar scale diverges as a negative power of `M` show that the logarithmic bulk term is lower order. The generic scalar moment orders therefore transfer to finite bulk under the stated assumptions. This does not establish an `O(1)` remainder, a remainder limit, a result at `V=0`, or uniformity as bulk diffusivity tends to zero.

## Review limits

This is a proof audit of an order theorem. The estimates do not establish sharp coefficients or convergence of optimizing designs. Distinct fold sites and parameters, a bounded density positive on both sides near a fold, known fold locations, and the absence of a mobility cap or resolution constraint remain part of the statement. No numerical experiment is needed to distinguish the proof's exponents once the matching analytical bounds are established; none is claimed here. Literature novelty remains a separate task.
