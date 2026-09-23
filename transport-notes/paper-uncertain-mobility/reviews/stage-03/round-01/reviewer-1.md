# Independent review: Stage 03, round 01, reviewer 1

Reviewer: `/root/paper_reviewer_1`. Date: 2026-09-07.

Snapshot: `13abd3fbd62d1a6faf46617e4f678ed14ac22bacb42b8ff161f0ee27d67f0b00`. All twelve manifest hashes matched. I read the complete new section, the accepted form/transfer and localization prerequisites, handoff, relevant notation and claims, and the new reference. I did not consult another reviewer, another reviewer report, or coordinator-checks; I did not delegate or edit manuscript sources.

## Verdict

**Accept Stage 03. No major or minor issue identified.** In particular, I find the new sharp supercritical argument complete for the stated smooth-test scalar convention: singular measure mass is ineffective, the relaxed local infimum is attained by a unit-mass density, arbitrary designs satisfy the claimed liminf, and the graded recovery construction gives the matching integrated moment with its exact budget and coefficient. This is stronger than a dimensional-scaling argument.

The lack of an explicit or unique local minimizing profile is an explicitly stated limitation, not a gap in this value theorem. No conclusion about a measure-valued diffusion process is needed or claimed.

## Checks of the new measure and compactness arguments

### Singular mass is ineffective under this scalar convention

I checked the derivative-flattening construction independently, including its compact-support constraint. Given a fixed compact smooth test v, choose one compact interval containing both its support and the support of the correction bump. A finite singular measure on that interval can be approximated in mass by compact null sets. Open neighborhoods of those sets can have both vanishing Lebesgue measure and vanishing integral of d. The cutoffs rho can be chosen between zero and one, equal to zero near the compact sets and one outside those neighborhoods.

Since `int v'=0`, the correction coefficient `a_n=int rho_n v'` is O of the neighborhood's Lebesgue measure. The modified derivative has integral zero and common compact support, so its primitive is itself a compact smooth test. Its primitive differs uniformly from v by at most the L1 norm of the derivative modification. On the absolutely continuous part, the difference of derivative energies tends to zero because `int_U d -> 0` and the correction coefficient tends to zero. On the singular part, the uncorrected derivative vanishes on the compact set carrying almost all relevant mass; the remaining derivative is uniformly bounded, and the correction costs at most `a_n^2 int zeta^2 d nu_s`. Both vanish. Source and reaction terms then converge by uniform convergence on the common compact support.

Thus each density-only trial can be approximated without singular derivative cost. This proves the difficult direction of `J_mu(nu)=J_mu(d dx)`; the reverse inequality is monotonicity. The argument depends on the one-dimensional derivative/primitive construction and on the prescribed smooth-test definition. It is not presented as a universal fact about reinforcement in arbitrary dimensions or alternative interface realizations.

### Semicontinuity, positivity, finite value, and attainment

For a fixed compact test, `int |v'|^2 d nu` is continuous under vague convergence. Its source-minus-energy expression is therefore continuous; the supremum is lower semicontinuous. The dependence on mu is also a supremum of continuous functions, hence Borel. Fatou consequently gives integrated lower semicontinuity without requiring a jointly selected maximizing test.

A fixed bump, optimized in amplitude, gives a common positive lower response on a bounded mu interval for every measure of mass at most one. This establishes a strictly positive local value. For finiteness, the interval `1<alpha<min(2,6-8/q)` is nonempty exactly throughout the stated supercritical range. Near roots at `sqrt(mu)`, the derivative coefficient is comparable to `mu^(-alpha/2)` and the quadratic rate coefficient to mu. The local response therefore has power `mu^(-(6-alpha)/8)`. This power has integrable qth power by the upper restriction on alpha. The complementary/rootless reciprocal potential is of order `|mu|^(-3/2)` and is also integrable to power q here.

The mass dilation `d_m(x)=m^(6/7)d(x/m^(1/7))` has mass m and transforms the response by `m^(-3/7)` with parameter `mu/m^(2/7)`. Integration gives `m^(-(3q-2)/7)` in both directions. Zero density has infinite response at every positive mu by local reaction-only root tests, so its integrated value is infinite.

These facts justify the attainment paragraph. From a unit-mass minimizing sequence, vague compactness gives a measure with mass at most one. If its absolutely continuous mass were m<1, singular-mass ineffectiveness and exact scaling would force its cost to be at least `m^(-beta_q) S_q > S_q`, contradicting lower semicontinuity and the minimizing sequence. This simultaneously rules out lost mass and singular mass, rather than assuming either away. The limiting density has mass one and reaches the infimum. No compact-domain theorem is being used as an unproved substitute for this argument on the line.

### Natural endpoints for an arbitrary integrable background profile

The local lower bound on d gives H1 control on each fixed interval, even when d is unbounded above. Potential anchoring controls the local constant mode, and the quartic potential outside a fixed core controls the source tails by `L^(-3/2)` times the energy norm. This yields uniformly bounded maximizing energies on growing intervals.

The weighted derivative density argument is valid on a finite interval: smooth functions are dense in L2 of the finite measure `d dx`; the positive lower bound converts derivative convergence into ordinary L2 and hence L1 convergence. A fixed smooth integral correction restores endpoint constraints, and integration with an anchor gives uniform convergence of the functions. That suffices for convergence of reaction and source terms. It does not presume smooth density in an arbitrary degenerate weighted space without a floor.

For the limiting whole-line function, I checked the displayed Sobolev estimate. On a unit interval near large x, the potential bounds the squared L2 norm by `C |x|^(-4) E`, while the lower bound on d bounds the squared derivative norm by `C |x|^alpha E`. The one-dimensional estimate `|v(x)|^2 <= C(||v||_2^2+||v||_2 ||v'||_2)` gives the second power `|x|^(alpha/2-2)` exactly. With the chosen alpha<2, this gives boundedness. A spatial cutoff therefore adds at most `C R^(-2)||v||_infinity^2 int_annulus d` to the derivative energy; this vanishes since d is integrable. Existing energy tails vanish separately. Compact derivative approximation then places the limit in the actual whole-line smooth-test completion. This closes the possible free-endpoint/escaping-source gap.

### Unrestricted supercritical liminf and constants

For the common scale `ell=(M/b_0^2)^(1/7)` and test amplitude `b_0^(-2) ell^(-4)`, the source, mobility, and potential terms all acquire common factor `b_0^(-2) ell^(-3)`. The derivative contribution uses the pushed-forward measure divided by M, as required by `M=b_0^2 ell^7`. Thus compact-test vague convergence proves the pointwise lower bound even for concentrated or oscillatory competitors.

The parameter differential is `dc=b_0 ell^2 dmu`. After multiplying by `M^beta_q`, one fold contributes coefficient `b_0^((3-8q)/7)/4`. The two bounded parameter windows are disjoint for small M; Fatou on each, followed by window expansion, gives the sum of local integrated responses. If the two limiting masses are theta_0 and theta_1, they sum to at most one, and local scaling gives lower cost `S_q(theta_0^(-beta_q)+theta_1^(-beta_q))`. Strict decrease uses all available mass, and strict convexity splits it equally. For b_0=1/2, the factor is

`(1/4) 2^((8q-3)/7) 2^(1+(3q-2)/7) = 2^((11q-12)/7)`.

This calculation also verifies the final statement about mass allocation for sequences reaching the sharp equivalent. Singular or escaped mass would make the local lower inequality strict. Merely reaching the order does not have that implication, and the supplied half-uniform counterexample correctly distinguishes the two conclusions.

### Exact-budget recovery and integrated convergence

Adding a small integrable graded profile cannot increase the local scalar cost. Dilation back from mass `1+varepsilon` to mass one raises it by at most `(1+varepsilon)^beta_q`. A reflection average preserves its background and mass and decreases the moment by the already valid convexity argument.

The exact sine coordinate on each half-cell has metric between one and sqrt(2). With mobility `b_0^2 ell^6 w_ell d_tilde`, the two metric factors in the squared derivative and the factors from mobility and measure cancel, leaving the canonical derivative integral. Source and reaction receive exactly one `w_ell`. The preliminary cell mass is `m int w_ell^2 d_tilde`, which tends to m by dominated convergence despite the expanding interval. Scalar normalization by a factor tending to one preserves the leading response by two-sided comparison of the complete quadratic energies.

The preceding free-endpoint lemma therefore applies to the recovery profile even if it is unbounded or otherwise nonsmooth. The other half-cell has a rate bounded away from zero at any fixed scaled parameter near one fold, so its unscaled O(1) response vanishes after multiplication by `ell^3`.

Finally, the positive graded lower bound survives transplantation over the entire circle. The resulting root-side scaled envelope has power `(1+mu)^(-(6-alpha)/8)` and the rootless side has power `(1+|mu|)^(-3/2)`. For ordinary roots at offsets a fixed distance from the fold, `mu` is of order `ell^(-2)`, and both the regular-root bound and that envelope have scale `ell^((6-alpha)/4)`. Thus the envelope covers the full parameter half, not just compact mu ranges. Its qth power is integrable. Dominated convergence completes the whole-moment recovery and supplies the same coefficient as the unrestricted liminf.

## Checks of the remaining stage results

1. **Convexity:** The quotient formula expresses `J^q` as a supremum of nonnegative constants times negative powers of affine energies. Those powers are convex for every positive q. Zero numerator/denominator conventions are inherited from the accepted scalar definition. Reflection and pi-translation generate the four transformations used for the symmetry average.
2. **Shell lower bounds:** Fubini gives average mobility cost `C m/(r ell)` while reaction cost is `C r^2 ell^3`. Their balance is `ell^4` proportional to `m/r^3`, so the mean response has order `m^(-1/4)r^(-5/4)`. Multiplying its qth power by parameter probability of order r squared yields exactly `r^(2-5q/4)m^(-q/4)`. Geometrically disjoint shells give the critical logarithm, and the single fold bump gives the supercritical lower power. Zero shell mass correctly gives infinite averaged cost by shrinking widths.
3. **Graded upper orders:** The ratio of the complementary reciprocal response to the root response is bounded by a constant times `(R/r)^((6+alpha)/4)`. Core scaling gives response `R^(-3)` and parameter width `R^2`. Exact normalization produces the three prescribed cutoff regimes. The endpoint exponent simplifies to `(8-5q)/(q+4)`, producing the threshold and logarithm in the stated ranges.
4. **Sharp supporting certificate:** The paired test has source `2Iz`, reaction `2Uz[1+o(1)]`, and reference energy `2(T+U)z`. The tangent to the negative qth power produces exactly the stated positive `qT/Q` term and negative derivative penalty. This algebra does not require the reference energy to come from a global admissible design. In the sliding kernel, squared amplitude, derivative factor, and root-coordinate Jacobian give `M^(-5/4)d^(-5/4)a^(-3/4)` before multiplication by `z^(q-1)`. The root density `|sin r|/4` and the chosen d cancel the spatial dependence. Counting paired roots introduces the factor `2^(q-3)` printed in K. At endpoints the nonnegative truncated kernel cannot exceed the full local kernel, so arbitrary mobility concentration is covered.
5. **Subcritical sharp upper bound:** The graded profile's normalized moment is dominated by `|t|^(-gamma_q)` with `gamma_q=q(6-alpha_q)/8=7q/[2(q+4)]<1`. The same envelope follows in the inner and rootless regimes, not only at separated roots. Thus dominated convergence remains justified above the uncontrolled threshold 4/3 and below 8/5.
6. **Critical sharp bounds:** Moving retained arcs have maximal oscillator-width/root-distance ratio bounded by `[M/(Z_E M^(7b))]^(1/4)`, which tends to zero for b<1/7. Logarithmic derivative and Jacobian errors are controlled by that same ratio, so the lower certificate remains uniform as the arcs approach the folds. For the upper bound, four one-sided fold approaches give `Z_R~4 log(1/R)~(4/7)log(1/M)`. The retained cutoff `r_0=R log(1/M)` and relative neighborhood size `log(1/M)^(-1/2)` produce the claimed diverging harmonic intervals and vanishing relative complementary error. Omitted annuli cost only a log-log factor, and core/rootless pieces have no leading logarithm. The resulting coefficient is `(2C0)^(8/5)(4/7)^(7/5)/8`.
7. **Physical transfer:** Every displayed optimum grows faster than powers of the logarithm, so the accepted same-budget transfer applies. The scalar/physical class distinction is retained, and positive-background recovery or the mixture construction supplies actual admissible physical competitors. No uniform vanishing-bulk-diffusivity claim is made.

## Citation and verification checks

I inspected [Buttazzo–Oudet–Velichkov, Proposition 4.1](https://arxiv.org/pdf/1506.00141). It does use measure relaxation with weak-star compactness and semicontinuity of compact-test variational values. The manuscript credits those methods without importing that bounded-domain proposition as proof of its own noncompact theorem. A full novelty comparison remains a later-stage task.

Independent symbolic simplification confirmed the graded endpoint exponent, the subcritical envelope exponent, the folded curvature power, and the final power of two. All residuals were zero. These symbolic checks supplement the derivations above; they do not verify the variational argument by themselves.

A fresh build was run only in the temporary output directory `/tmp/transport-review1-stage03.dpNUJ9`, using:

```sh
latexmk -pdf -outdir=/tmp/transport-review1-stage03.dpNUJ9 -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

It succeeded and produced a 25-page PDF. No manuscript source or frozen build artifact was changed by this review.

**Findings requiring correction: none. No major issue found.**
