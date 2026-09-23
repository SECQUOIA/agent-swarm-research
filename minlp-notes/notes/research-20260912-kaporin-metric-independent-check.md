# Independent check of a horizon-scaling metric example

Date: 2026-09-12. This verifies the proposed paired-chain illustration.
It distinguishes two error measures; it is not a counterexample to the 2026
paper or a claim of a new approximation result.

Fix `0<rho<1` and `n=2m`. Let the scalar latent variance and independent
measurement-noise variance both equal one. Set

```text
a_t=rho when t is even,
a_t=0 when t is odd and t>=3,
q_t=1-a_t^2,
Var(X_1)=1.
```

The variance recurrence preserves `Var(X_t)=1`. Each zero transition
separates consecutive pairs, so the observation-error covariance is

```text
R=diag(B,...,B),       B=[[2,rho],[rho,2]],
```

with `m` blocks. The zero-history working covariance is `Rhat=2I`, and its
precision is `Qhat=(1/2)I`.

The relative precision matrix is
`R^(1/2) Qhat R^(1/2)=R/2`. Each pair contributes eigenvalues
`1-rho/2` and `1+rho/2`, giving exactly

```text
||R^(1/2) Qhat R^(1/2)-I||_2 = rho/2.
```

For any selected subset, complete retained pairs contribute the same two
eigenvalues and isolated retained coordinates contribute one. Thus the
maximum relative precision error over every subset also remains `rho/2`,
independently of `m`.

I checked the normalization against Definition 1 of the primary
[*Everything is Vecchia: Unifying low-rank and sparse inverse Cholesky approximations*](https://arxiv.org/html/2603.05709v1#S1.SS1),
arXiv:2603.05709v1. In the full-rank case, that definition raises the mean
eigenvalue to the full dimension before dividing by the determinant.
Here `tr(R Qhat)=2m`, so that mean equals one and

```text
kappa_Kap = 1/det(R Qhat)
          = (1-rho^2/4)^(-m),
log(kappa_Kap) = -m log(1-rho^2/4).
```

Consequently the logarithmic Kaporin quantity grows linearly with the
number of pairs, while the maximum relative spectral error remains fixed.
The ordinary spectral condition number of `R Qhat` is also fixed at
`(1+rho/2)/(1-rho/2)`. If one instead uses a dimension-normalized Kaporin
root, its value here is the constant `(1-rho^2/4)^(-1/2)`; that is a
different normalization from the cited definition.

For completeness, the Gaussian divergence in this example satisfies

```text
KL[N(0,R) || N(0,Rhat)] = (1/2)log(kappa_Kap).
```

The example therefore also separates a subset-uniform relative precision
bound from a horizon-uniform total KL bound. No claim about the 2026 paper's
supermodularity or pivot-optimization guarantees is needed for this
calculation. The separate thesis counterexample must retain its own source
and version scope.
