# Second independent review: fractional-law additive optimization

Date: 2026-09-05. Reviewer: `benders_property`, independent of the author and first reviewer. Reviewed [the fractional-law investigation](potential-flow-fractional-additive-investigation.md), including its subsequently added Section 5, against the fixed-core theorem and the reviewed dense-degree polynomial-law extension.

**Verdict: pass for the fixed law `phi(x)=sign(x)|x|^(3/2)`.** The construction supports polynomial bit-time additive potential-difference and signed edge-flow optimization at fixed maximum biconnected-block cycle rank, with rational admissible near-optimal uncertain inputs. It does not imply exact threshold comparison. One initially implicit point, rational recovery for edge-flow objectives, was identified during this review and has been supplied explicitly in Section 5. No remaining substantive mathematical gap was found.

This is a proof and encoding audit. Positive fractional-power rational approximation is prior work, and this review makes no novelty claim for it or for the proposed combined network theorem.

## 1. Integral truncation, quadrature, and the endpoint zero

For `alpha=1/4`, the integral converges at both ends. At `t=0` its integrand and every quadrature term are exactly zero; the normalization therefore also preserves zero exactly. The substitution proof of `I(t)=t^alpha I(1)` is needed only for `t>0`, so no division by zero is hidden in extending the identity to the endpoint.

Uniformly for `0<=t<=1`, the lower tail is bounded by integrating `s^(alpha-1)`, giving `4*2^(-L/4)`. For the upper tail, `t/(t+s)<=1/s`, giving `(4/3)*2^(-3L/4)`. Both displayed bounds are correct, including as `t` approaches zero.

The complex disk centered at `3/2` of radius one lies in `Re(u)>=1/2`. The principal fractional power is analytic on a neighborhood of this disk. Also

```
|u^(-3/4)| <= 2^(3/4) < 2,
|t/(t+2^k u)| <= 1.
```

The second bound follows from the positive real part of the denominator and remains true for all `t>=0`. Cauchy's coefficient bound on that disk gives Taylor remainder at most `4*2^(k/4)*2^(-2n)` on `[1,2]`. Polynomial exactness through degree `2n-1`, positive weights, and weights summing to one bound the quadrature error by twice this remainder. Summing the `2L` panels yields a bound no larger than the stated `16L*2^(L-2n)`. There is no nearby moving pole as `t` tends to zero.

For example, `L=4p+O(1)` with a sufficiently large constant and `2n>=L+p+log_2 L+O(1)` makes the total error at most `2^(-p)`. Hence `O(p^2)` terms suffice. The constants are conservative but valid.

## 2. Rational coefficient construction and normalization

Gauss-Legendre nodes are isolated real roots of a rational polynomial of degree `n`, whose coefficient bits are polynomial in `n`. Its positive weight formula and the fixed fractional powers used in each panel coefficient are algebraic computations of polynomial degree and height. Each coefficient can therefore be enclosed and rounded individually in polynomial bit time. No common algebraic field containing every unrounded panel coefficient is required. The construction stores only rational approximations of them.

The standard positive-rule facts can also be checked in [NIST DLMF §3.5(v)](https://dlmf.nist.gov/3.5#v). The author's added Johansson–Mezzarobba reference supplies a direct constructive node/weight algorithm; the argument here also follows from ordinary rational-polynomial root isolation and the algebraic weight formula.

For each rounded term, the displayed derivative bounds are valid. Along a rounding segment with `s>=2^(-L-1)` and `a<=2^(L+3)`, a safe node sensitivity bound is `2^(2L+4)`. With `N=2Ln` terms, per-coefficient absolute error at most `2^(-p)/(N*(1+2^(2L+4)))` gives total error at most `2^(-p)`. Thus the required bit precision is `O(p+L+log N)`, as claimed. Positive rational rounding is possible even for a small weight: one may use a positive endpoint of its certified enclosure, or a positive rational of the allowed absolute tolerance. Nodes can be rounded with the stated positive lower bound.

Exact rational addition in `Q_R(1)` has polynomial bit cost: the bit length of a common denominator is at most the sum of the term-denominator bit lengths. It need not be numerically small. The lower bound `I(1)>=1/6` is valid by integration over `[1,2]`. If the unnormalized uniform error is `zeta<=1/12`, then `Q_R(1)>=1/12` and

```
|Q_R(t)-t^alpha Q_R(1)| <= 2 zeta.
```

Dividing proves the stated `24 zeta` normalization error. This step avoids a transcendental normalization constant without sacrificing exact positivity.

## 3. Scaled rational law and dense encoding

Choosing a power of four `T>=max(1,B)` gives rational `S=sqrt(T)` of polynomial bit length. The scaling identity is exact:

```
S*x*(x^2/T^2)^(1/4) = sign(x)|x|^(3/2).
```

It proves the uniform constitutive-error bound on `[-B,B]`. Every resulting rational term is a positive multiple of `x^3/(x^2+c)` with `c>0`. Its derivative is nonnegative, and positive away from zero. Thus their sum is smooth and strictly increasing, has the sign of `x`, and is unbounded in both directions. Its asymptotically positive linear growth makes its energy primitive coercive. Unique physical flow, acyclic sign orientation, and the uniform nomination-based flow bound therefore hold for the surrogate as well as the original law.

If the rational sum has `N` terms with polynomial coefficient bit lengths, multiplying its positive quadratic denominators produces degree `2N`; adding its numerators produces comparable degree. Expanded coefficient bits grow polynomially, since multiplication adds bit lengths and combinatorial coefficient growth contributes only polynomially many further bits. Evaluation at rational arguments to any specified polynomial precision likewise has polynomial cost. Large denominator values or small positive denominators do not create exponential encoding length.

## 4. Fixed-dimensional network optimization

The smooth surrogate has nonnegative derivative; adding `rho*x` makes the electrical derivative resistance positive. The reviewed adjoint face proof and its compact limiting argument therefore apply. They use monotonicity and positive electrical resistances, not fractional algebraicity. The surrogate's globally positive denominators introduce no additional flow-sign cells.

After selecting a face, all edge flows are affine in a fixed-dimensional core. Substitution into the rational law preserves polynomial dense size. Multiplying a cycle equation by all relevant denominators is exact because their product is strictly positive everywhere, and it remains linear in resistance leaves. The product's degree and coefficient bits are polynomial in graph size and approximant size. In a fixed number of core variables its monomial count is polynomial as well.

The additional objective-value core coordinate and denominator-cleared path-value equation increase the core and aggregate dimensions by one. A simple rational objective bound is `m*beta_U*(B*max(1,B)+delta)`, since `|psi|<=|phi|+delta`; expanded polynomial interval bounds also work. The core is compact.

The growing-degree version of the fixed-core construction is valid here. Fixed-size minors, support signs, and products all retain polynomial dense size. Fixed-dimensional sign determination, quantifier elimination, and algebraic sampling have polynomial dependence on degree and coefficient bits; see [Basu's survey, Theorems 2.18 and 3.6](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf). Scalar resistance boxes make the support representation particularly direct. The required fixed dimension concerns variables, not polynomial degree.

Exact local samples and their resistance leaves lie in one polynomial-degree local algebraic extension. Independent blocks need not be merged into a common field: approximate their values separately and add rational intervals. A target edge uses only its own block. These distinctions avoid the sum-of-independent-algebraic-values representation obstruction.

## 5. Transfer from law error to physical error

The difference of the two physical flows is a circulation. Its scalar product with either potential gradient vanishes, proving the displayed energy identity with the correct sign. For the original signed power,

```
|phi(a)-phi(b)| >= (1/2)|a-b|^(3/2).
```

For equal signs, the constant one suffices by convexity of the positive power. For opposite signs, convexity gives the stronger constant `2^(-1/2)`. Multiplication by `|a-b|` establishes the draft's uniform monotonicity inequality, including zero.

With `D=||x-y||_infinity`, one edge supplies the lower bound `(beta_L/2)D^(5/2)`. The error term is at most `beta_U*delta*||x-y||_1<=m*beta_U*delta*D`. Dividing when `D>0` proves the exponent `2/3` in (C). The rational sufficient choice proportional to `eta^2` is valid because `eta^(4/3)<=eta` for `0<eta<=1`.

On `[-B,B]`, `|phi'|=(3/2)sqrt(|x|)<=2max(1,B)`. Every edge-drop difference is therefore at most `beta_U*(2max(1,B)*eta+delta)`. Summing along a simple terminal path proves (D). These bounds are uniform across the full independent resistance and balanced nomination boxes.

If the uniform original/surrogate objective discrepancy is at most `a`, their optimal values differ by at most `a`; an exact surrogate optimizer loses at most `2a` in the original objective. Add the surrogate optimization and rational-rounding budgets. Choosing each below a fixed fraction of the requested tolerance gives the claimed certified interval and witness. All required law and coordinate tolerances have polynomial bit length. Trivial zero-flow or edgeless cases should be processed before formulas divide by `m` or a positive error budget.

## 6. Rational recovery of edge-flow witnesses

Section 5 now closes the originally implicit edge-flow recovery step. Start from a surrogate **edge-flow** optimizer. The original law's electrical adjoint gives polynomial-bit rational pressure Lipschitz constants using `M=2max(1,B)` and `N=Bmax(1,B)`. For the objective edge, the one-edge path yields the sharper nomination coefficient `beta_upper_e*M` used in the draft.

The endpoint equations and scalar monotonicity imply

```
|x-y|^(3/2) <= (2/beta_lower_e)
                 (|D-D'|+N|beta_e-gamma_e|).
```

Thus sufficiently fine rational rounding of nominations and resistances controls the original edge flow directly. Recovering nominations inside rational isolating boxes intersected with balance is a rational LP; the original algebraic nomination proves this intersection nonempty. Resistances can be rounded independently within their intervals. This requires neither evaluation of an exact original physical state nor a positive inverse-derivative bound for the surrogate at zero.

Combining two uniform original/surrogate edge errors with this rounding bound gives rational near-extremal inputs. A pressure optimizer cannot replace the surrogate edge optimizer when target-edge resistance varies, and the revised draft states that restriction correctly.

No exact pressure or edge threshold guarantee follows from these additive estimates. This remains compatible with the separately reviewed exact fractional-power arithmetic barrier.

## 7. Subsequent fixed-exponent and heterogeneous-family extension

The author's final additional section was also independently checked. **It passes for any fixed rational exponent `1<q<3`, and for edge laws chosen from a fixed finite family of such exponents.** This strengthens the initial verdict's scope under exactly that fixed-family qualification.

For `alpha=(q-1)/2`, the two stated tails are correct. The same complex-disk bound applies because `|u^(alpha-1)|<=2^(1-alpha)<2`. The constants in the required panel count may depend on the fixed exponent. Normalization still works with `I_alpha(1)>=1/6`, uniformly for `0<alpha<1`. Algebraic computation of the coefficient powers has bounded rational-exponent degree for a fixed family.

Choosing the binary exponent of `T` divisible by the denominator of `q-1` makes the prefactor `T^(q-1)` rational, with polynomial bit length. The exact scaling identity gives `x|x|^(q-1)`. The rational surrogate terms retain the same positive `x^3/(x^2+c)` form; approximation accuracy, dense degree, and coefficient bits remain polynomial.

The signed-power increment constant is at least `2^(1-q)>1/4`, so the proposed uniform constant `1/4` is safe. The rational bounds `M=3max(1,B)^2` and `N=Bmax(1,B)^2` bound every derivative and law in the fixed family. In the heterogeneous energy identity, selecting an edge attaining the maximum flow difference gives exactly `D^(q_e)<=4m beta_U delta/beta_L`. The choice proportional to `eta^3` implies `D<=eta` for `0<eta<=1`, since every `q_e<3`. No common exponent in the energy sum is required.

For rational input recovery on a target edge, the inverse estimate has power `q_e` and coefficient `4/beta_lower_e`. Choosing its pressure/resistance error budget proportional to the cube of the desired flow error is again sufficient. This supplies a uniform fixed-power precision rule across the family, without evaluating an irrational exponent during rational recovery.

The exclusion of arbitrary binary-encoded exponent input is necessary for this proof: `alpha` or `1-alpha` can then be exponentially small, making the chosen dyadic truncation length exponential. The reviewed statement does not claim that stronger algorithm.
