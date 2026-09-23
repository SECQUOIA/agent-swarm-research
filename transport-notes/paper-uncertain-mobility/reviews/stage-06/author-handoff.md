# Stage06 author handoff

Author: `paper_stage6_author`. Prepared 7 September 2026. **Author work complete; ready for the coordinator to freeze a snapshot and dispatch five independent reviewers. This is not an acceptance decision.**

## Changed files

- `sections/06-finite-precision.tex`: complete finite-precision stage, including the previously open interior crossover.
- `main.tex`: includes Section06 after the accepted exact-observation section.
- `notation.md`: adds the local response, global crossover function, conditional value and scales, and the locally scoped fold-neighborhood notation.
- `claims-map.md`: marks P1–P3 and X2 as authored and pending review; records the developed X2 proof rather than the old conjectural status.
- This handoff and `author-sanity-checks.json`, `author-build-checks.json` record author checks.

No accepted section, bibliography entry, research note, or literature package was changed. No later-stage work was begun. I did not delegate authorship or proofs.

## Results and proof structure

1. The equal-bin optimum has a separate exact budget for every bin. Finitely many conditional choices justify its decomposition into conditional infima and yield a measurable policy without any selection theorem.
2. The whole-line quadratic uncertain-center value `Fctr(eta)` is finite, continuous on `[0,infinity)`, and attained by an L1 density of mass one. An even minimizer may be chosen. Its lower bound is `max(Cpl,C0 eta^(1/4))`, its upper bound is `C(1+eta^(1/4))`, and its large-width equivalent is `C0 eta^(1/4)`.
3. The quadratic analogue of Stage03's expanding-interval lemma is proved with the actual slower source tail `L^(-1/2)`. The graded floor has exponent strictly between 1 and 2. The pointwise energy bound makes the limiting function bounded, allowing cutoff and weighted-derivative approximation even for unbounded integrable mobility.
4. Local-value existence and lower continuity use vague compactness, compact-test lower semicontinuity, removal of singular mass by the already proved one-dimensional derivative-flattening argument, and addition of density to complete missing mass. Tightness of the original sequence and strict mass scaling are not assumed. Upper continuity uses fixed positive-tail regularizations and anchored comparison of shifted quadratic forms.
5. On every fixed regular offset set, the normalized conditional optimum converges uniformly to `Fctr(eta_I)` for bounded `Delta/M^(1/5)`. Exact reflection in arclength preserves every rate in a bin, so symmetric competitors have half the budget on each half-circle. The arbitrary-competitor lower bound pushes those half-circle masses to rescaled measures and applies the compact-test liminf before averaging.
6. The recovery uses the exact coordinate `x=(-cos(s)-c_I)/(sqrt(a_I) ell_I)`. Its metric is bounded on a fixed regular-root neighborhood and tends locally to one. The coefficient `a_I ell_I^4 w_I d` gives the exact canonical derivative energy; source and reaction carry `w_I`. Its mass tends to the intended half budget, and one normalization restores the exact budget. The natural-endpoint lemma controls the response; the gapped exterior contributes only a bounded term. A finite collection of regularized profiles gives uniform bin policies.
7. Padded constant patches give the regular-bin envelope `C[M^(-1/5)t^(-4/5)+M^(-1/4)Delta^(1/4)t^(-7/8)]`. Shared fold-group patches give integrated cost `C M^(-1/4)(Delta+M^(2/7))^(3/8)`, including bins crossing either fold and the remaining rootless contribution. These bounds prove the unrestricted joint order law at every relative rate.
8. Riemann sums on regular offsets, the uniform conditional limit, and the integrable fold envelope give the exact finite-ratio crossover stated in the task, including ratio zero. The factor is `2^(6/5)/4` and the local argument is `2^(1/5) tau (1-c^2)^(-3/10)`. No unproved endpoint-to-interior inference is used.
9. The simultaneous coarse limit is proved independently through paired translated harmonic tests and padded root-arc recovery. Its coefficient is `2^(-3/4) C0 B(1/2,1/8)`. The large-tau asymptote of the new crossover integral is an additional consistency consequence, not a substitute for the simultaneous proof.
10. A fixed nonzero bin width retains exponent `-1/4`, without claiming its coefficient is the small-width limit. The bulk comparison, dimension conversion, binary-digit threshold, and nested-versus-nonnested distinction are stated within their actual assumptions.

## Author checks

The complete source builds to 45 pages. The final LaTeX log has no undefined references, multiply defined labels, warnings, or overfull/underfull boxes. The changed source files pass an explicit whitespace/control-character scan; this scan does not rely on `git diff --check` for untracked files. PDF pages 37 and 40 were inspected, and the long local-scale display was reflowed afterward.

The symbolic checks verify the exact-coordinate source, derivative and reaction factors; the paired half-budget normalization; the uncertainty argument; the coarse curvature exponent `-7/8`; the coefficient power `2^(-3/4)`; the fold exponents `2/35` and `1/40`; and all three powers in the unrestricted large-width test. High-precision evaluations recover `Cpl=6.2228237360198886`, `Kobs=22.4046282307491383`, and `Kcoarse=25.7238273887632910`. These checks substantiate normalization only and do not replace independent mathematical review.

## Boundaries and review priorities

There is no unresolved mathematical claim left intentionally conjectural in Stage06. The local minimizing profile and crossover value need not have an elementary formula; no uniqueness or monotonicity in uncertain-center width is asserted. No numerical approximation to the new continuum crossover is claimed here. Stage07 retains numerical reproduction and whole-paper literature/synthesis work.

Reviewers should independently scrutinize the quadratic weighted-form completion, the singular-removal and mass-completion existence argument, the arbitrary-design conditional liminf, exact reflection and budget factors, uniform recovery, and all fold/parameter-limit exchanges. The framework of decisions under partial information and quantized policies is established; Stage06 makes no claim to have invented that general framework. The coordinator has independently inspected relevant primary observation-channel literature for the final synthesis.
