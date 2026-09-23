# Proposed residual-covariance refinements

Date: 12 September 2026. Status: both refinements passed
[fresh proof review](research-20260912-pair-refinements-independent-review.md).
An optional spacing-certificate integration passed
[separate review](research-20260912-refined-spacing-integration-review.md);
the earlier certificates retain their original pair bound.
The parent researcher independently obtained the same far-pair identity and
supplied the stationary near-pair gain refinement below. No publication
priority claim is made for these Kalman covariance identities.

## Exact far-pair covariance identity

Use the scalar model and genuine local conditionals of the
[base theorem](research-20260912-noisy-markov-memory.md). At selected time `s`,
write

```text
e_s = X_s-E[X_s | Y_j, j in H_s],
Z_s = e_s+v_s,
p_s^- = Var(e_s) = d_s-r_s.
```

All quantities concern centered errors with covariance parameters fixed.
Orthogonality of linear regression gives `Cov(X_s,Z_s)=p_s^-`.

Let `s<t` and `t-s>L`. Every observation in `H_t` then occurs strictly after
`s`. In the fresh filter using `H_t`, propagate covariance of the state
prediction error with `Z_s`. Each transition multiplies it by its scalar
transition coefficient. Each observation update multiplies it by `1-K_j^(t)`:
the new observation noise is independent of `Z_s`. New process innovations
are also independent of `Z_s`. Thus

```text
Cov(Z_t,Z_s) = Phi_(t,s) p_s^- alpha_t,
alpha_t = product_(j in H_t) (1-K_j^(t)).
```

The empty product is one. The gains belong to the fresh local filter for
`H_t`; they are not full-history gains whose coefficients have been
truncated. Since `0<=p_s^-<=Var(X_s)<=Pbar` and `0<=alpha_t<=1`, this yields

```text
abs(Cov(Z_t,Z_s)) <= Pbar*rho^(t-s),     t-s>L.
```

Signed transitions, nonstationary latent variances, unequal observation-noise
variances, and zero process-noise variances do not affect this argument.
The previous far-pair triangle bound included an additional positive
regression-history term. That term is unnecessary here because regression
at time `s` reduces `Cov(X_s,Z_s)` to the local prediction variance.

The check script
[verify_noisy_markov_far_pair.py](../code/research_20260912/verify_noisy_markov_far_pair.py)
compares this identity with dense exact rational residual covariance in
nonstationary scalar models. Its separate result is
[noisy-markov-far-pair-verification.json](../code/research_20260912/results/noisy-markov-far-pair-verification.json).
These are author checks; the linked independent review supplies separate
exact checks and the scope counterexamples.

All 12,805 exact far-pair identities passed across 8,785 subset/window
models from 35 nonstationary covariance models. The suite also checked
`Cov(X_s,Z_s)=p_s^-` in 28,150 cases. For the 96-candidate spacing probe,
changing only the far-pair majorant reduces delta from approximately
`0.003795597732542757` to `0.0035242102623550668`, a 7.15% reduction.
That calculation retains the old near-pair majorant; the next proposal
could provide an additional improvement.

## Additional stationary near-pair factor

For an excluded old selected observation `j<t-L`, the same propagation gives

```text
Cov(Z_t,Y_j) = Phi_(t,j) Var(X_j) alpha_t.
```

Now specialize to stationary scalar latent variance `P` and constant
observation-noise variance `r`. When `H_t` is nonempty, its first local
prediction variance is exactly `P`, so the first gain is
`kappa=P/(P+r)`. Consequently `alpha_t<=1-kappa`.

For a near residual pair, `1<=t-s<=L` implies `s in H_t`, so this product
bound always applies. In the original near-pair expansion, every surviving
old-observation covariance can therefore receive the additional factor
`1-kappa`. This multiplies the entire previous near-pair majorant by
`1-kappa`. It does not replace kappa in the regression coefficient bound.

For the spacing theorem, the resulting proposed pair bounds are

```text
phi_new(h) = P*b^h,                                  h>L,

phi_new(h) = P*kappa*(1-kappa)*b^h
             * sum_(d=ell,ell+g,...<=L) b^(2d),       g<=h<=L,
ell = max(g,L+1-h).
```

The previously reviewed innovation floor and row-pricing recurrence can be
retained. Only the pair majorant changes. The `1-kappa` improvement is stated
here for constant `P` and `r`; it must not be silently transferred to the
general nonstationary model using only its existing upper and lower bounds.

For reference, summing unrestricted near distances gives

```text
sum_(h=1)^L sum_(d=L+1-h)^L b^(h+2d)
 = b^(L+2)(1-b^L)(1-b^(L+1))/[(1-b)(1-b^2)].
```

Thus the far identity alone replaces the unrestricted two-sided row bound by
twice `Pbar/d_*` times the geometric far tail plus kappa times this near sum.
In the stationary setting, the near coefficient becomes
`kappa*(1-kappa)`. The `b=0` case is exact independence and is handled
separately. The [certificate note](research-20260912-spacing-certificates.md)
records the optional integration and its separate review status.
