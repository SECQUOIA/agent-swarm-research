# Root integration review: remaining scope and calibration statements

These findings refer to the completed first front/shared-tool drafts. The
four Opus round-2 authors are incorporating them. This report is outside
the submission sources and makes no final readiness claim. No literature
search, experiment, or project-wide check was performed.

1. **Quadratic output needs a domain qualification.** The introduction's
   universal rational-output sentence is false for implicit graph domains.
   On `0 <= x <= 1`, `y^2=2`, `1 <= y <= 2`, the quadratic objective `x^2`
   has optimizer `(0,sqrt(2))`. Rational quadratic outputs in this paper
   concern rational boxes and polyhedral domains. A graph lift can remain
   algebraic.
2. **The common search premise needs its proved replacements.** The
   introduction says all three routes use outside feasibility independent
   of searched coordinates. Direct conditional minimization uses that
   premise; graph charts and order transport replace its literal box form
   with their own curvature and noise-comparison arguments. The common
   mechanism should state the invariant, then distinguish these premises.
3. **Finite support follows from bounded random bits.** A Turing machine
   can sample a countably supported rational law: flip a fair coin until
   its first success and output the number of flips. Our chosen sampler
   has a worst-case bound on random bits, hence finitely many possible
   outputs. Section 3 must use this precise motivation.
4. **Independence belongs to each noise model.** Aligned noise has
   `gamma=T^T xi`; the original coefficients can be dependent even when
   the supplied factor coefficients are independent. Discussion must not
   describe every theorem as independent original-coefficient noise.
5. **Strong noise does not support arbitrary small-noise calibration.**
   The original-objective width bound applies, but the strong-field
   expectation theorem has a lower noise-scale requirement. The prescribed
   small-epsilon consequence is therefore scoped to routes valid at
   arbitrary positive scales.
6. **Projected widths must enter the calibration itself.** Define
   `W_noise` as the sum of widths in the chosen perturbation coordinates,
   including supplied rows of `T` for aligned noise. The correct projected
   width in an earlier proposition does not repair a later recipe that
   still divides epsilon by original-coordinate widths. For the normalized
   Hadamard factor `T=H_16/4`, original widths `(1,delta,...,delta)` give
   projected total width `4(1+15 delta)`. The allowed aligned endpoint draw
   `xi_i=sigma` gives `gamma_1=4 sigma` and all other coefficients zero.
7. **Gaussian calibration needs positive logarithms and zero-width cases.**
   Treat `W_noise=0` separately. Put `R=max{1,W_noise/epsilon}` and choose
   a nonnegative integer `t` with noise scale `2^-t`. If the effective
   accuracy envelope is `b(t)<=P(I0+t)` for a fixed nondecreasing
   polynomial, the condition
   `2(W_noise/epsilon)(b(t)+20)<=2^t` has a solution
   `t=O(I0+log R+1)` after enlarging a fixed constant. Exponential growth
   dominates the fixed polynomial; all constants are effective. For the
   least adequate `t>=1`, failure at `t-1` gives
   `2^t < 4 R(P(I0+t)+20)`. For `t=0`, `2^t=1<=R`.
   Thus `1/sigma <= R poly(I0+log R+1)` with polynomial sampling bits.
   This preserves the exact Gaussian-like support `(b+20)sigma` and the
   numerical factors in the work bounds.

The complete boundary Sol review separately identified: positive modulus
in the amplifier lemma; logarithmic native-label format counts; distinct
structural scope of Square Root Sum and PosSLP reductions; binary penalties
in the Del Pia--Khajavirad construction; and the narrow scope of retention
barriers. Those findings are recorded in the live integration contract and
will have their own full reviewer report.

All items above have been sent to their owning Opus revision authors.
The final integrated review must verify the actual revised sentences and
formulas; an author report alone is insufficient.
