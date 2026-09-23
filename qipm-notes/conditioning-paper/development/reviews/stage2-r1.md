# Stage 2 independent review — reviewer 1

Reviewed `macros.tex`, `sections/02-setup.tex`, `sections/03-geometry.tex`, `sections/04-widths.tex`, `main.tex`, and the author notes. I independently checked the displayed derivations and their assumptions rather than relying on the author report. The introduction, abstract, examples, and later algorithmic sections are outside this review's scope.

**No major or minor issues identified.** The authored stage is mathematically coherent and can proceed to the next stage.

## Mathematical audit

- **Standard facts and gap parameterization.** The one-dimensional reciprocal-Hessian estimate correctly yields Dikin containment by contradiction with boundary divergence. The positive-gradient differential inequality correctly proves semiboundedness, including boundary endpoints. The objective-support inequality follows from minimizing the objective over the closed Dikin ellipsoid. Compactness, an affine lower support of the barrier, and boundary divergence justify existence of the analytic center and all penalized minimizers. Differentiation gives the positive gap derivative with the correct power of `mu`. The integration inequality for `1/g` has the correct direction and gives the stated lower gap bound. The attained interval and its endpoints are properly stated. The classical Peña attribution matches the primary manuscript inspected in the preceding review.

- **Approximate containment.** For a normalized local direction, the lower curvature integral gives `phi'(t) >= t/(1+t)-rho`. The choice `t0=(sqrt(nu)+rho)/(1-rho)` makes this derivative positive and gives exactly the displayed constant after semiboundedness. The case in which the endpoint precedes `t0` is included. The sublevel application uses a positive objective weight and the relative dual norm correctly. All derivative evaluations occur at interior points; the proof does not silently evaluate the barrier at a boundary point.

- **Difference body and matrix order.** The sign choice puts one of `x+h` and `x-h` in the observed-gap sublevel for every closed Dikin displacement. Symmetry then gives the complete inner inclusion. The outer inclusion follows by subtracting two vectors with local norm at most `C`. The Loewner directions are correct: normalizing in the first Hessian norm gives the upper bound involving the second barrier's constant. The condition-number comparison correctly carries the product factor `16 C_F^2 C_G^2`.

- **Spectral edges and diameter law.** The circumradius of the difference body is the diameter of the sublevel. Its inradius is the minimum support value, hence the minimum full width of the sublevel. The aspect-ratio inequalities have the correct factors. The smallest-eigenvalue lower bound follows at every interior point from the objective-decreasing Dikin radius; the upper bound follows from an attained longest chord and containment. The largest-eigenvalue lower bound follows from objective support with the correct inverse-Hessian inequality. Homothety of a fixed relative ball gives the stated upper bound, including the factor two that cancels against outer difference-body containment. All ratio manipulations are valid.

- **Uniformity.** Applying asymmetric containment at the analytic center bounds the objective range above that center by `C_nu a_F`, giving the claimed common interval for uniformly bounded barrier parameters. The stated uniform constants also require a residual bound below one and fixed instance geometry, as the text expressly records. The conversion of a power law in gap to one in `mu` follows from the proved two-sided gap comparison.

- **Canonical constants.** Tangent centrality supplies an equality multiplier because the annihilator of the equality kernel is the adjoint range. Positive primal coordinates or positive-definite blocks give the canonical positive dual slack. Complementarity then bounds its pairing with a fixed strict primal point. Dividing by that point's smallest positive coordinate/eigenvalue provides the claimed uniform tail bound; no unnecessary endpoint nondegeneracy or strict-complementarity hypothesis is used.

- **Localization.** A compact positive sublevel contains a relative ball by interpolation from an optimum toward a relative interior point. All pointwise proof steps survive replacing the full compact set by that sublevel in the homothety argument. The proposition appropriately avoids importing analytic-center or global-path conclusions for an unbounded feasible set.

- **Full spectrum.** The radial function is distinguished from the support function. Its positivity and compactness properties justify the reciprocal minimax manipulations. Both Courant–Fischer formulas use increasing eigenvalue order correctly. The subspace intersection proves the profile ordering; the endpoint identities with diameter and centered inradius are correct. The directed-exit construction handles objective-orthogonal directions, boundedness, and possible discontinuity, and gives the stronger constant and the first-profile equality with the longest chord.

## Exposition and build

The relative tangent metric, unscaled Hessian, primal gap, residual norm, and common attained gap interval are clear and used consistently. The account of prior work appropriately credits classical containment, gap parameterization, and general conditioning upper bounds, while identifying the further statements actually proved here. I found no unsupported priority claim in these sections.

`make -C conditioning-paper` succeeds, with the PDF up to date. No manuscript edits were made in this review.
