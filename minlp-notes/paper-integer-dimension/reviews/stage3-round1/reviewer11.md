# Reviewer 11 — stage3-round1

Primary lens: Stieltjes approximation, rational coefficient conditioning, and the signed P/Q endpoint gadget.

Major findings: 0

Minor findings: 0

I found no concrete defect requiring correction after reading the complete stage and reconstructing its main proof chain. The Stieltjes construction has uniform control at zero and as the exponent decreases; the endpoint gadgets preserve exact graph containment without adding integer variables. The draft distinguishes dense numerical-degree complexity from binary-exponent complexity and count bounds from encoding bounds. This is a bounded review, not a guarantee of correctness or external priority.

## Snapshot and coverage

All seven SHA-256 values matched `reviews/stage3-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `19ccd1e2bea4439da83da8959d8d1bb59d172efa6e4160b40d80722def385ec5` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `e662d0747e850fe23c3625c0cd6e9fe39d1bc370223f2f8c4b2659095cbea599` |
| `references.bib` | `d1c9428ba522987e3709b9d902163ae99ee940d8ec6fb781bf04255f3d23aa80` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `dbd488d7fa1d3e377f57bea9f48f8391e5b153b827e4d4caf62e9aa0c3bc66be` |

I read the task, lens list, process/protocol, complete 1,564-line stage-3 section, coverage inventory and relevant bibliography. All eleven canonical stage-3 results and thirteen explicit supporting developments have identifiable statements or proof passages in this draft. Stage-4 vector developments remain explicitly pending; I did not treat those as omissions.

I had reviewed the complete preceding stages in their original rounds. For this round I rechecked the accepted dependencies used here: parity contacts, finite disjunction, exact bounded binary products, covariance-volume estimates, unconditional domination, and the scalar specialization of the accepted rational log-determinant allocation oracle, including its exact central-ball repair.

Original-source comparison was deepest for `results/positive-pure-power-linear-dimension-precision.md`, `notes/positive-rational-stieltjes-power-approximation.md`, and `notes/shared-prefix-rational-interpolation-gadget.md`. I also compared the scalar two-bit and relative-error supporting notes and inspected the second compact-power audit after reconstructing the argument. The audit's verdict was not used as proof.

I inspected the cached primary passages in Bonito–Pasciak, Section 3.3, equation (37), Lemma 3.4; and Sagraloff–Mehlhorn, Theorem 36 and its square-free setting. The first gives positive resolvent approximations under the stated substitution, and the second supplies the requisite polynomial root-isolation/refinement bound after rational denominator clearing and square-free preprocessing. I did not audit every bibliographic datum, repeat an external novelty search, implement certified root isolation, implement the full curvature compiler, compile LaTeX, or inspect the PDF.

## Findings

No numbered major, minor, or question finding is submitted. The following verification records the main obligations I checked and why they are satisfied.

## Primary-lens reconstruction

**Stieltjes integral and tails, lines 1058–1088.** For `gamma=2/D`, `D>=3`, both tails of the defining integral converge. Substitution at positive `t` gives `I_gamma(t)=t^gamma I_gamma(1)`, with the value at zero handled directly. Splitting at one gives the lower bound `1/(2gamma)+1/(2(1-gamma))>=2` and upper bound `1/gamma+1/(1-gamma)<=D/2+3`. The separate `D=2` case is necessary and is correctly excluded from this integral proof.

With the displayed truncation indices, the low tail is at most `e/512` and the high tail at most `3e/256`; their sum is `7e/512<e/64`. The low cutoff grows proportionally to numerical `D`, which is included in the complexity statement. These estimates are uniform for every `t` in the closed unit interval; they do not implicitly discard an input neighborhood near zero.

**Complex panels and positive quadrature, lines 1090–1109.** The radius-one disk centered at `3/2` lies in the open right half-plane. Its power branch is holomorphic, and the possible resolvent pole is outside the disk. For nonpositive panel index, the scale/resolvent factors have product modulus at most one; for nonnegative index their product is at most two. Together with the power-factor bound this gives the uniform modulus four, independent of the panel index and input. Cauchy's estimate gives the stated Taylor remainder, and Gaussian positivity and exactness bound both quadrature and integral remainders. The chosen order gives summed error at most `e/16`.

The unnormalized approximation is a positive sum, so it is increasing and bounded by its value at one. Its value, rather than the potentially much larger sum of numerator coefficients, is correctly used in rationalization.

**Rationalization and normalization, lines 1111–1149.** Perturbing both positive coefficients of one resolvent term by relative error at most `tau` bounds its value ratio by `(1-tau)/(1+tau)` and its reciprocal. Consequently the perturbation is at most `4tau` times the original term, including a direct zero-value argument at `t=0`. Summing positive terms gives error at most `e/32`.

The length-one Gaussian weight formula has the correct factor. Its lower bound from the Legendre coefficient estimate, and its upper bound from positivity and weight sum, give polynomial logarithmic magnitude bounds for every coefficient. The denominator in the weight formula is at least one at the exact node. Polynomial derivative bounds therefore permit polynomial-depth interval refinement. For the additional power expression, its positive argument stays between explicit bounds with polynomial bit lengths. Rational test powering and positive-root bisection have polynomial cost in numerical `D` and the precision parameters. No common number field for all quadrature nodes is required.

The exact rational normalizer is at least `2-E>0`. The normalized error is at most `2E/(2-E)`, hence at most the requested tolerance; both endpoint identities hold exactly. Rational denominator products add bit lengths over polynomially many terms. The stated term count and dense-degree encoding bound follow.

The primary Bonito–Pasciak formula, after `lambda=1/t`, indeed becomes a positive sum of `t/(t+b)`. The draft credits that approximation mechanism and separately proves rational coefficient conditioning and endpoint normalization; it does not claim the integral or positive resolvent principle as new.

**Signed P/Q endpoints, lines 1152–1184.** At a fixed integral prefix, each recurrence forces `v_k=t^k v_0`. The denominator equation is then `Q(t)v_0=theta`. The supplied positive denominator bound gives a unique solution `v_0=theta/Q(t)` and bounds every `v_k` by `1/q_min`. The numerator is decoded by a signed linear combination, so signs of coefficients create no extra integrality requirement. This includes constant polynomials, zero numerator, zero bits, and zero weight. The stated `(d+1)(L+1)` size convention covers these degeneracies.

Exact endpoint normalization makes the piecewise-linear path join zero to one. Its image covers the unit interval even with reversed segments or excursions; intersecting with the original input bounds preserves that coverage. Endpoint approximation errors interpolate with the same absolute bound. The lemma explicitly assumes the denominator certificate rather than claiming to find one or to approximate an arbitrary inverse function.

**Dense reciprocal formulation, lines 1186–1227.** The reciprocal equations have unique nonnegative solutions bounded by `1/b_k`. Expanding the prefix makes each apparent product a sum of existing-bit products. The identity for `x` is correct term by term, and the expression for `y` is the chord of the squared power coordinate, including the term `h^2 theta`. It is not the square of the interpolated power coordinate.

The uniform inverse approximation gives `abs(x-x_0)<=delta`. Combining the power-coordinate chord error with the `D`-Lipschitz bound gives the asymmetric error interval used by the output band. Every original input has a segment representation; its exact power lies in the band. The total admitted error is at most `4h^2+2D delta<=3p/8`. Positive output coefficients and unconditional domination transfer this to the entire output vector. Summing depths and adding the allocation loss gives the claimed `13r/2+1` comparison. Reciprocals of small rational denominator parameters have polynomial encoding length.

## Checks across the rest of the stage

The scalar chord proof correctly trims a finite cover and uses compact extrema of parity contacts. The three-piece refinement works even when the gap has a plateau. Uniform continuity bounds incompatible packing cardinality; interval monotonicity of the convex midpoint gap justifies the maximal-packing cover.

For truncated curvature mass, I checked the split at `(b-t)A(t)=1`, the bound `z-1/2` from the remaining interval, the local remainder constant, and the telescoping potential estimate at `b=1`. The raw-curvature and degree-allocation examples use different stated tolerances and do not confuse their conclusions.

For certified integration, the positive-coefficient sectors and the signed Taylor-certificate panels are distinct valid arguments. Failure near a complex root bounds the number of failed panels at each depth. The square-free discriminant bound supplies a polynomial depth bound even when roots approach the real interval; the root at zero is separated by the cutoff. Subinterval disks remain inside certified disks. The inverse-quantile mass modulus uses a positive rational value at `delta/4`, whose encoding remains polynomial even with cancellation.

The compiled mass knots have sufficient error slack for reversed or equal consecutive knots. Forced endpoints ensure coverage, and the one-sided endpoint rounding matches the asymmetric final band. The hybrid's unfinished `9D`-cell branch proves `N_eta>D`, which absorbs the cost of curvature splitting. It uses one global index rather than adding independent local index counts. Fixed common denominators and implied Boolean wire values meet the indexed compiler's hypotheses.

The separable lower packing uses Jensen superadditivity and a lattice-ball deletion count at most `6^r`. Combining this with the actual local cell counts gives the stated finite and compiled constants. Positive-allocation proofs take covariance after the coordinate homeomorphism and do not assume volume preservation. Supporting scalarization handles zero rows and capped coordinates; the multipliers need not be computed by the construction. Dyadic layer curvature bounds and rounded sparse powering provide the stated shared output bands with polynomial dependence on binary exponent lengths.

The scaled Jensen and chord inequalities handle `1<alpha<2`, including the first cell at zero. The rational inverse routine has polynomial precision even as `alpha` approaches one or becomes large. Its uncertainty stopping rule follows from the lower derivative bound on the intervening power values. Rational log/exp evaluation uses only polynomial numerical work in the index length, not numerical exponent magnitude. Reversed or duplicate inverse knots retain graph coverage.

Finally, the relative-error obstruction uses residues modulo an arbitrary chosen integer and finite convex combinations, requiring neither bounded witnesses nor closed lifts. The concave-power threshold differs from the convex-power assertion and is stated correctly. The truncated-domain construction supplies the claimed order, without claiming a sharp leading constant. For root encoding, freezing a possibly huge integer witness changes right-hand sides but not the continuous basis denominator bound. The row-wise encoding accounting gives the linear `Omega(D)` lower bound. In the conic-value gadget the zero-weight proof rules out a spurious recession value. The squaring-chain dual pairings telescope to the correct objective gap; their potentially long values are witnesses rather than encoded coefficients.

## Executed checks and limits

I wrote and ran `verification/reviewer11-stage3-endpoints.py`. It passed 504 exact rational signed P/Q endpoint cases and 93 exact normalized reciprocal/chord cases. The cases include mixed-sign numerator and denominator coefficients, a certified denominator minimum `1/2`, zero-bit prefixes, both cell endpoints, and interpolation weights zero and one. These checks verify the recurrence bounds, binary-product inequalities, denominator equation, signed numerator decoding, endpoint normalization, and reciprocal interpolation identities.

I also inspected and reran `code/quadratic_rank/check_positive_rational_stieltjes.py`. It passed 5,776 positive rational terms and 62 sampled values for degrees 3, 8, and 32, including endpoints and inputs below the truncation scale. Exact rational endpoint checks passed. The largest sampled error/tolerance ratio was `0.0004390012`.

The Stieltjes checker uses high-precision numerical Gaussian nodes rather than certified root isolation. Its samples are supporting evidence; the uniform approximation and bit-complexity conclusions rely on the analytical proof and the checked root-refinement import. No manuscript, original research file, bibliography, literature, or other review was edited.
