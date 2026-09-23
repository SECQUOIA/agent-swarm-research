# Independent audit: correlated quadratic output error budgets

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed [the ellipsoidal output precision extension](quadratic-ellipsoidal-output-precision.md). The finite constants and polynomial rational construction carry over to finitely many positive semidefinite output budgets. The required shared residual matrix, covariance inequality, gradient formula, and finite-bit conditioning all check.

For a conceptual factorization `W=C^T C`, put `G_a=sum_j C_aj H_j`. The budget energy equals `sum_a tr(G_a P G_a P)`. This proves nonnegativity, positive semidefinite order monotonicity, and the same geodesic log-convexity as the previously reviewed sums of Hessian energies. The factorization is only a proof device.

The same-parity midpoint error is `q(x-y)/4`, so its squared budget norm bounds `q(x-y)^T W q(x-y)` by `16 epsilon^2`. Apply the scalar fourth-moment identity to each `G_a` and sum: all other terms are nonnegative, and the covariance terms sum to the stated budget energy. The same covariance cap, scaling constant, volume bound, and parity cover therefore give the original dimension-only lower constant. Singular budgets do not cause a problem; they measure seminorms and the transformed argument remains valid.

The upper bound depends on using the same approximate residual monomial for every output. Under that construction, one symmetric error matrix `Z` represents all output errors simultaneously, with `||Z||_F<=1/4`. The identity `e_j=.5 tr(M_j Z)` is correct, including diagonal and off-diagonal quadratic terms. Frobenius Cauchy--Schwarz applied after the conceptual factorization gives

```
e^T W e <= .25 ||Z||_F^2 sum_a ||sum_j C_aj M_j||_F^2
        <= E(P)/64.
```

Thus there is no factor depending on the number of outputs or budgets in the error or binary-count constants. The formulation size and running time still depend polynomially on the complete input size. Independent residual copies for different outputs would not justify this particular shared-matrix argument; the construction explicitly shares them.

The half-log-energy gradient in isometric tangent coordinates is `N/E`, where `N=sum_jk W_jk M_j M_k`. Symmetry of `W` makes this symmetric, and the factorization gives `N=sum_a (sum_j C_aj M_j)^2`, which is positive semidefinite. Its trace is exactly `E`, so its Frobenius norm after normalization is at most one. The global Lipschitz bound and exact repair penalty therefore carry over unchanged.

For positive definite `P`, a budget energy vanishes exactly when every transformed Hessian vanishes, which is equivalent to `E(I)=0`. That test is independent of `P` and uses exact rational arithmetic. A zero energy need not mean that the corresponding output combination itself is zero: it can be affine. The formulation represents affine terms exactly, so omitting the zero energy from the covariance penalty is still correct.

For every remaining budget, `E(P)>=lambda_min(P)^2 E(I)`. The rational number `E(I)` has polynomial encoding length even when its double-sum expression has cancellations, so positivity gives the required inverse-exponential-polynomial lower bound. Rational evaluation of the sums, gradients, dyadic feasibility scale, and final upper repair factor therefore fits the already reviewed bit-complexity proof. No rational factorization of `W` is required. As in that proof, all affine as well as quadratic map coefficients must be rational for the produced formulation to have rational coefficients.

I also ran 16 exact rational checks, covering dimensions and output counts from one through four, signed off-diagonal budget entries, and singular budget matrices. Each checked the transformed-energy identity, the gradient numerator's square-sum identity and symmetry, and the shared-error inequality `e^T W e<=E(I)/64`. All passed. These checks support the algebra; the proof above covers arbitrary input dimensions and all positive semidefinite budgets.
