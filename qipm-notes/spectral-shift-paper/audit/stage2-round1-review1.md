# Stage 2, round 1: independent review 1

**Findings: 0 major issues; 0 minor issues.** I found no mathematical repair
required in the reviewed Stage 2 material.

I read `sections/05-joint-accuracy.tex` in full, the new developments beginning
with the nonnegative even thresholds in `sections/04-fixed-accuracy.tex`,
`scripts/joint_accuracy_diagnostics.py`, `audit/stage2-author.md`, and
`audit/root-parity-development.md`. I did not read other reviewers' reports
and did not edit the manuscript. The assessment below concerns the stated
query model and exact oracle-independent gate synthesis, not gate-synthesis
or classical preprocessing cost.

## Uniform lower bounds

### Exact sine coordinate: verified

In `05-joint-accuracy.tex`, Theorem `thm:joint-exterior`, the affine angle
coordinate maps the fixed comparison interval exactly to the promised angle
interval. Convexity gives `b_delta > arcsin(delta)` and hence the required
negative extrapolation point. The inequality

    a_delta - b_delta*a_n <= -arcsin(delta*a_n)

is valid for `0 < a_n <= 1`; its use requires no restriction on how rapidly
the selected index grows. All relevant angles remain on the principal branch
for one sufficiently small `delta_0` depending only on `rho`.

Keeping the Taylor polynomial of the sine target is essential, and the proof
does keep it. The factorial remainder bounds use trigonometric derivatives,
so there are no uncontrolled growing-order derivatives of `arcsin`. The
comparison `u_s/K` follows from maximality of the chosen odd index and is
uniform in that index. The numerical constants in
`H_n <= K + 2*u_T + 2*u_s` imply `u_T >= 5*K/2` as stated.

The argument only assumes a bounded trigonometric circuit entry for every
real angle. It does not replace that entry by an algebraic polynomial in the
encoded scalar or assume that oracle completions with the same scalar have
identical outputs. Thus the all-circuit scope is preserved.

### Fejer–Riesz factor and both radius branches: verified

In Lemma `lem:FR-remainder`, the nonnegative trigonometric defect has an
analytic polynomial factor of degree at most `T`. Its circle norm bound and
the maximum-principle growth estimate give the displayed Cauchy remainder
for `A(exp(i*arcsin(x)))`. Squaring the complex Taylor polynomial, with
conjugation on coefficients, genuinely gives a real polynomial nonnegative
on the whole real line. The resulting error obstruction has the correct
cross term and square term.

In Theorem `thm:FR-margin`, endpoint magnitudes provide a positive uniform
square-root separation because `K < G_1 < (rho-1)/2`. The apparently missing
`+1` in choosing `s=r+1 <= T` is harmless: `r>=1` implies `r+1<=2r`, and
decreasing the fixed constant in `r <= c_rho*delta^(-1/2)` suffices. The
large-`T*delta` branch directly implies the claimed bound. In the other
branch, `R=s/(4T)` satisfies both radius conditions and gives exactly the
factor `4*sqrt(e)` inside the growing power. Taking the root of the required
error preserves a constant independent of `r`.

In Theorem `thm:FR-all`, direct evaluation of the threshold formula gives
the explicit lower estimate with its stated factor `1/(2*e*r)`. The
half-threshold assumption therefore supplies the requisite positive margin.
If `T<r+1`, the fixed-radius remainder divided by the required error is at
most a fixed constant times

    r * delta^(r+1/2) * (4*rho*sqrt(e)*R0^2)^r.

One small `delta_0` makes this less than one for every `r>=1`, using a
geometric bound on `r*2^(-r)`. This closes the branch that would otherwise
leave an artificial upper restriction on the index. The adaptive-radius
argument then applies for all remaining indices. In particular, the
ultra-high-accuracy assertion and the `K=0` consequence are justified.

### Matching high-accuracy consequences: verified

The integrated-sign polynomial is globally in `[0,1]`; oddness makes its
total integral exactly one. Its error identity has the correct sign and
gives the stated absolute error on the full positive interval. For
`L>=beta*D`, the exterior lower bound and, independently, the Fejer–Riesz
bound match its `delta^(-1)*L` order uniformly, including `L/D` tending to
infinity. The conversion to absolute complement accuracy uses
`L=log(1/eta)-D` correctly. No constant depending on the high-band endpoint
is needed for these particular matched bounds.

## Growing pinned upper bound and intermediate regime

I checked all growing powers in Theorem `thm:joint-pinned`. The contact
spacing and the Dirichlet-kernel estimate yield the displayed
leakage-to-slack ratio, including the factor `r^(-r)`. Endpoint contacts
cause no loss: the slack bound in terms of distance in `y` is weaker there
and remains valid. The signed-error blend therefore reaches exactly the
threshold error.

The explicit tail factor `2^(n+4)` is retained in the global estimates.
The three global regions give, respectively, `o(1)`, an exponentially
decreasing term after choosing one fixed large `A`, and the stated
`C*r^2*2^n/k` plus polynomial tail term. Both high-band exponents,
`n+2-4/n` and `3-4/n`, are correct. The assumption `r=o(D)` absorbs the
remaining fixed bases raised to `n`. The high-band estimate includes the
standalone gate leakage, not merely its product with the threshold
polynomial. The degree is `O(r^3*k+N)` and the positive-series length is
`O_c(D)` under the theorem's assumptions.

The near-match corollary correctly applies the finite-margin lower bound at
index `r-1`. Away from the upper boundary, the root of the margin is bounded
below uniformly. Since `G_r/G_(r-1)` tends to `R0^(-2)<1`, the same comparison
does cover exact lower thresholds. The text accurately retains the margin
near the upper boundary and does not claim a uniform multiplicative optimum
there.

## New parity results

The even cone is closed under coefficientwise limits. The compactness
argument, positivity of each threshold, and approximation argument giving
convergence to zero are sound. Retaining evenness in the Taylor limit gives
the stronger even lower hierarchy. An attained minimizer has a nonempty
finite positive-error contact set, and the existing fixed-order pinned
construction preserves parity; it therefore proves equality cases as well.
Plateaus are correctly handled by choosing the first admissible index.

For `F_2=F_1`, writing the even quartic as a quadratic in `y^2` gives a
nonnegative leading coefficient and hence convexity on the positive axis.
The chord comparison yields the claimed minimax lower bound. The displayed
cubic for `rho=2` has a strictly positive derivative on `z>=-1`, a positive
value at `-1`, and the stated uniform binomial-tail bound. It proves
`F_3(2)<1/32`, so the matched even exponent is indeed `5/6`.

The odd lower proof supplies the logarithm without an additional assumption
on the degree: Taylor's remainder estimate applies at every order to the
trigonometric polynomial. Choosing the exterior comparison order
proportional to `D` gives the claimed `D/delta` lower bound. The odd upper
construction is contractive both inside and outside its transition interval;
it does not assume an unstated sign condition inside that interval. The final
three-way comparison is properly limited to the specified converter classes.

## References and diagnostics

I directly checked [Gilyén et al., Lemma 25 and Theorem
30](https://arxiv.org/pdf/1806.01838). They supply the bounded odd sign
approximant and the cited alternative uniform-amplification upper order.
The Fejer–Riesz attribution is consistent with the root-factorization proof
in [Motlagh–Wiebe, Theorem
4](https://doi.org/10.1103/PRXQuantum.5.020368), previously checked in the
Stage 1 review. The exterior inequality is stated in [Bos–Ma'u–Waldron,
Proposition 2.1](https://www.math.auckland.ac.nz/~waldron/Preprints/Extremal-growth/BosMauWaldron1.pdf).
The manuscript also proves that inequality directly. I found no unsupported
priority claim in the reviewed material; this is not a comprehensive
literature-priority determination.

I ran the diagnostic script using the required qipm interpreter, with output
directed to `/tmp/spectral-review1-stage2`. Its three gate examples reproduce
the author audit: sampled normalized absolute errors are `1.0`, pin leakages
are zero at working precision, and the leakage/slack ratios are approximately
`6.85449e-25`, `1.93773e-46`, and `3.33209e-74`. The positive-series coefficient
recurrence and its polynomial evaluation match the mathematical definition.
The script avoids the principal cancellation in subtracting two values near
one and accurately labels its output as diagnostics rather than certificates.

Additional independent numerical checks found a maximum sampled cubic error
of `0.01430056` on `[1,2]`, below its analytic tail bound `0.02001129` and
`1/32`. The computed first threshold differs from its closed formula by
`4.51e-17`. The explicit all-index threshold lower estimate held in all 128
checks for `rho` in `{1.1,2,10,100}` and `r=1,...,32`. These checks support,
but do not replace, the analytic arguments above.
