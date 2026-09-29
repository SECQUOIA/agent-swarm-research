# Independent adversarial review of sparse kernel rounding

Date: 2026-09-28. Reviewer: `smoothing_proof_review`.

Reviewed draft: [sparse-kernel-rounding.md](sparse-kernel-rounding.md),
Theorem 1 and equations (1)–(21), in the version using the rational
squared-Fejér kernel and `m=floor(r/w)+1`. Section 6 was reviewed after
the initial core audit.

## Assessment

I found no invalid inference in the stated box theorem. I reconstructed the
degree bounds, the kernel normalization and damping estimate, local density
positivity, separator consistency, the gluing argument, and the objective
error independently. The theorem gives the asserted `O(r^-2)` error for the
specified full local preordering moment relaxation. This assessment is
evidence from a proof audit, not a machine-checked proof or a final novelty
determination.

The claim is substantially narrower than a general sparse MINLP convergence
result. Extra constraints and integrality are not preserved by this
smoothing. The draft states these limitations correctly. The main remaining
publication risks are overlooked equivalent prior work and overstating the
meaning of coefficient-dependent constants or of a numerical SDP solution.

## Independent proof audit

### 1. The positive kernel and its coefficients

The triangular sequence `b_j=(m-|j|)_+` is the Fourier coefficient sequence
of `|D_m|^2`. Consequently its autocorrelation `a_k` is the Fourier
coefficient sequence of `|D_m|^4`; symmetry of `b` makes the convolution and
autocorrelation expressions coincide. Normalization by `a_0` gives constant
Fourier coefficient one. The stated formula

\[
a_0=m^2+2\sum_{j=1}^{m-1}j^2=(2m^3+m)/3
\]

is correct. There are exactly `2m` unit increments or decrements in the
sequence extended by zero, so `a_0-a_1=m` is correct. Nonnegativity of `g_k`
uses the nonnegative triangular sequence; it does not follow merely from
nonnegativity of the trigonometric density. The draft uses the correct
argument. Cauchy–Schwarz gives `g_k<=1`.

For all integer `k`, the pointwise inequality

\[
1-\cos(kt)=2\sin^2(kt/2)\le k^2(1-\cos t)
\]

proves the damping estimate after integration. This remains true beyond
the Fourier support, where `g_k=0`. Thus the draft does not require the
objective coordinate degrees to lie below `2m-2`. That detail is essential
when `w` is large relative to the total objective degree.

The substitution `x=cos(theta), y=cos(phi)` establishes positivity at all
box points, including endpoints. The normalized arcsine reference measure
is essential for the Chebyshev orthogonality and normalization in (9).
Lebesgue probability measure cannot be substituted without changing the
kernel. Every kernel coefficient is rational by the finite integer-sum
definition; the trigonometric proof does not introduce irrational
coefficients into the polynomial kernel.

### 2. Source positivity and exact truncation

The kernel has source degree at most `2(m-1)`. The interval positivity
theorem with an even degree bound gives

\[
K_m(x,y)=\sigma_0(x)+(1-x^2)\sigma_1(x)
\]

with squared-polynomial degrees at most `m-1` and `m-2`, respectively.
This applies even when special values of `y` reduce the actual degree.
It suffices to choose a representation separately for each fixed real `y`;
there is no unproved need for SOS factors depending polynomially or
continuously on `y`.

Products of SOS polynomials are SOS. On expanding the tensor product, a
term indexed by `I` has a square factor of degree at most
`|B|(m-1)-|I|`, followed by `|I|` box generators. Its total degree is
therefore at most `2|B|(m-1)<=2r`. Every use of source positivity is inside
the stated truncation. An ordinary quadratic module would not supply these
products automatically.

The even degree choice removes the common parity error in this argument.
For an arbitrary degree-`s` nonnegative interval polynomial, the safe
degree cap in the `1-x^2` representation is `2 ceil(s/2)`, not always `s`.
For example, `1+x` cannot have a degree-one representation of that form.

### 3. Actual measures and exact separator marginals

The expression `h_b(y)=L_b(K_{m,b}(.,y))` is a polynomial, so it is
measurable. Pointwise source positivity gives `h_b>=0`; integrating the
finite polynomial expression gives mass one. No representing measure for
the original truncated functional is assumed.

Integrating out a nonseparator coordinate removes its kernel factor
exactly. The remaining source polynomial has degree
`2|S|(m-1)<=2r`, so the stipulated shared moments determine the entire
separator density. The same kernel in all bags is indispensable here.
Matching only low-degree separator moments unrelated to this bound would
not suffice.

The gluing proof is valid for finite bags of compact intervals. Under the
running-intersection property, a child bag intersects all previously
attached variables only in its parent separator. Regular conditional laws
exist because the spaces are standard Borel. The draft correctly permits
arbitrary values of these laws on separator-null events. It does not
assume strictly positive separator densities or divide by zero densities.
The resulting global density need not be a polynomial; the theorem does
not require one.

### 4. Pseudo-moment bounds and objective error

The telescoping identity (15) is exact when zero-index summands are
interpreted as zero. Every weighted square has degree at most
`2|alpha|`. For `|alpha|<=r`, it proves
`L(T_alpha^2)<=1`. Positivity on ordinary squares implies
`L(T_alpha)^2<=L(T_alpha^2)`, using `L(1)=1`. This is a valid truncated
Cauchy–Schwarz argument: both polynomials have degree at most `r`.

Thus `r>=d` is a sufficient hypothesis. It is stronger than simply having
the objective in the domain of `L`, which would only require `d<=2r`.
Dropping the present hypothesis without a replacement proof would leave
a real gap. A possible sharper proof is recorded below, but is not needed
for Theorem 1.

The tensor damping identity remains valid when some objective frequency
is outside the kernel support: that frequency integrates to zero on the
left and has zero multiplier on the right. The inequality
`1-product(g_i)<=sum(1-g_i)` uses only `g_i` in `[0,1]`.
The weighted coefficient budget then gives precisely (3).

Finally, every feasible local objective value `v` obeys `f*<=v+E`,
where `E=3A/(2m^2+1)`. Taking its infimum yields
`rho_r>=f*-E`, even without attainment. Together with point-evaluation
feasibility this proves (4). Since `m>r/w`, the advertised simpler bound
also follows. A minimizing point of the continuous objective on the compact
box has value no greater than the rounded law's expectation.

## Concrete failure modes outside the stated assumptions

For the draft's `m=2` kernel,

\[
K_2(x,y)=1+\frac43xy+\frac13T_2(x)T_2(y).
\]

The following are exact examples, not floating-point observations.

1. **Endpoint positivity is not strict.**
   `K_2(x,1)=2(x+1)^2/3`, so `K_2(-1,1)=0`. A formula dividing by a
   separator density requires an almost-everywhere interpretation.

2. **The wrong reference measure changes the mass.**
   Integration against `dy/2` gives `1-T_2(x)/9`, not one.

3. **Too few shared moments fail.** The source laws `delta_0` and
   `(delta_-1+delta_1)/2` both have first moment zero. Their smoothed
   densities differ by `2T_2(y)/3`. They do not have a common second
   source moment. A separator requirement limited to first moments would
   fail even for genuine local measures.

4. **Different bandwidths fail.** Applying `K_2` and `K_3` to the same
   source law `delta_1` gives different densities. One cannot pick a
   separate bandwidth for each bag without coordinating shared variables.

5. **A hard equality is destroyed.** Smoothing `delta_0` gives density
   `1-T_2(y)/3`, positive throughout the interval. It is not supported on
   the feasible set `y=0`. Prescribed binary support is likewise not
   retained by this continuous kernel.

6. **The tree assumption is substantive.** On three binary coordinates,
   the three pair laws requiring the two coordinates to differ are
   individually realizable and have the same uniform singleton marginals.
   No common joint law exists, because three pairwise inequalities cannot
   all hold. This example shows why local consistency by itself is not a
   gluing theorem for a cyclic bag hypergraph. It does not contradict the
   draft's junction-tree hypothesis.

## Scope of a certificate and numerical use

Theorem 1 is a statement about the infimum of the moment relaxation and
about rounding every feasible moment point. An arbitrary feasible moment
objective is not itself a certified lower bound on `f*`: it can exceed the
true optimum. A numerical solver needs a verified dual lower bound or a
separate rigorous enclosure of the relaxation optimum.

The subsequently added Section 6 correctly supplies finite-dimensional
conic duality. Product arcsine moments are strictly feasible: integrating
a nonzero square times any box-generator product is strictly positive.
These moments obey every overlap equality. The objective is bounded by the
proved moment bounds. Primal Slater feasibility and finite optimal value
therefore give dual attainment and no gap. Summing the local dual
identities cancels the separator multipliers, yielding the claimed sparse
SOS certificate. Adding the stated nonnegative constant proves (21)'s
consequence.

Rational kernel coefficients do not alone imply rational rounded sample
points, rational moment optimizers, or a bit-complexity bound. Section 6
separately constructs a finite extraction method on algebraic nodes.
The draft properly distinguishes these facts. Likewise, the coefficient budget is additive in the supplied bag
decomposition and may grow with the number of terms or variables. The
bound is not uniform in dimension under arbitrary objective normalization.

### Added finite quadrature and dynamic programming consequence

The choice `N=m+floor(d_infty/2)` satisfies
`2N-1>=2(m-1)+d_infty`, for both parities of `d_infty`. Hence product
Gauss–Chebyshev quadrature integrates `h_b` and `f_b h_b` exactly. The
same coordinate grids are used throughout, and summing a bag probability
table onto a separator gives `N^(-|S|)` times the shared separator density.
Thus the finite marginal consistency and grid-minimum conclusion (20)
are correct. Zero-probability separator entries cause no difficulty for
finite gluing.

One minor correction was requested: table storage is
`O(sum_b N^|B_b|)`, but an arithmetic count of the same order needs an
aggregation argument or a bounded-degree bag tree. Direct message
aggregation has the safe bound
`O(sum_b (1+deg_T(b))*N^|B_b|)`, hence `O(t N^w)` for `t` bags.
For varying bag sizes and unrestricted tree degrees, the sharper sum
bound should not be asserted without justification. The author applied the
`O(t N^w)` arithmetic correction; that formulation passes this check.
This issue does not affect the theorem, finite rounding, or certificate
corollary.

## Prior results inspected

- Laurent and Slot, [*An effective version of Schmüdgen's
  Positivstellensatz for the hypercube*](https://arxiv.org/html/2109.09528),
  especially Sections 2.3 and 3: the positive tensor Chebyshev kernel,
  source preordering argument, and dense quadratic convergence rate are
  established ingredients. The new contribution cannot be the kernel
  or the dense rate. Their argument does not, by itself, state the draft's
  consistency-preserving sparse primal rounding theorem.
- Korda, Magron, and Ríos-Zertuche, [*Convergence rates for sums-of-squares
  hierarchies with correlative sparsity*](https://link.springer.com/article/10.1007/s10107-024-02071-6),
  published online in 2024, in the 2025 journal volume: Theorem 2(i)
  summarizes the sparse box result of Theorem 6 under running intersection,
  with exponent `2/(w+3)`. The draft's exponent two is a real improvement
  over that inspected result for fixed data, if its hierarchy conventions
  are compared correctly. Different constants and total versus coordinate
  degree conventions must still be acknowledged. This comparison does not
  establish priority against all subsequent or differently formulated work.
  A later [source audit](sparse-putinar-prior.md) located July 2025 and
  February 2026 author slides that already assert the inverse-square
  sparse preordering rate. Thus the comparison with the published theorem
  remains valid, but novelty of the rate itself is not asserted. This
  correction changes the significance assessment, not the proof audit.
- Blekherman, Parrilo, and Thomas, [*Semidefinite Optimization and Convex
  Algebraic Geometry*](https://sites.math.washington.edu/~thomas/frg/frgbook/SIAMBookFinalvNov12-2012.pdf),
  Theorem 3.72: the even-degree interval representation used in the source
  positivity step has the required exact degree bound.

Searches included `Jackson kernel polynomial optimization hypercube
Schmudgen O 1 r2 Laurent Slot 2022`, `sparse Schmudgen hierarchy convergence
Jackson kernel running intersection`, and interval-positivity degree
queries. This was a proof-focused search, not an exhaustive priority audit.

## Targeted computation and its limits

Command actually run:

```sh
python research-20260928/solver/proof-review-checks.py
```

Result: PASS. The script uses exact SymPy arithmetic. It verifies finite
Fourier identities for `m=2,...,7`, the normalization and coefficient bounds
for `m=2,...,12` across and beyond their support, and the explicit endpoint,
reference-measure, and marginal-consistency examples above. It also checks
the optional sign-product identity below for widths one through six.

These checks catch transcription errors in concrete cases. They do not
prove the infinite family of kernel inequalities, the interval positivity
theorem, the measure-theoretic gluing theorem, or novelty. No project-wide
verification or CI inspection was performed. Lean was not used; the main
remaining imported steps are classical analysis rather than a short
algebraic identity whose formalization would independently audit the entire
argument.

## Optional degree refinement, not required by the draft

For scalars `a_1,...,a_s`,

\[
1+\epsilon\prod_{i=1}^s a_i
=2^{1-s}\sum_{\substack{\eta\in\{-1,1\}^s\\
                         \prod_i\eta_i=\epsilon}}
                \prod_{i=1}^s(1+\eta_i a_i),\qquad \epsilon\in\{-1,1\}.
\]

Taking `a_i=T_{alpha_i}(x_i)` and using univariate interval positivity
puts `1+/-T_alpha` into the box preordering with term degree at most
`2 sum_i ceil(alpha_i/2)`. Thus `|L(T_alpha)|<=1` can hold at a lower
order than the draft's sufficient condition `|alpha|<=r`. This would
permit a refined theorem based on the actual objective frequencies.
The current simple assumption is sound and should not be complicated
unless such a refinement has a concrete use.
