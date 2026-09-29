# Lean verification of the ternary quartic's zero and curvature

Date: 2026-09-28. Status: targeted Lean checking passed, including
directional stationarity. The
[independent correspondence review](ternary-rational-sos-convex-lean-review.md)
also passed, including a separate targeted Lean rerun.
The standalone proof is
[TernarySOSDescent.lean](../formal/TernarySOSDescent.lean), using the
repository's pinned Lean 4.33.1 and Mathlib dependencies. No dependency,
project configuration, or existing formal proof file was changed.

## Exact statements checked

The definitions `r0` through `r4`, `exposing`, and `quartic` reproduce
the polynomial in
[the construction note](ternary-rational-sos-convex-counterexample.md):

\[
\begin{aligned}
r_0&=2-2xy,&r_1&=2x^2-2yz,&r_2&=2y^2-4z,\\
r_3&=2z^2-x,&r_4&=2xz-y,&&\\
A&=4r_0+5r_1+3r_2+9r_3,&
F&=A^2+r_0^2+r_1^2+r_2^2+r_3^2-r_4^2.
\end{aligned}
\]

All these functions have real arguments and exact integer coefficients.

| Lean theorem | Verified statement |
| --- | --- |
| `residuals_at_fifth_root` | If $a\in\mathbb R$ satisfies $a^5=2$, all five residuals vanish at $p=(a^4/2,a,a^2/2)$. |
| `quartic_zero_at_fifth_root` | Under the same hypothesis, $F(p)=0$. |
| `quartic_stationary_at_fifth_root` | Under the same hypothesis, the actual derivative of $t\mapsto F(p+tv)$ at zero is zero for every real direction $v$. |
| `quartic_line_second_deriv` | For every real base point and direction, the actual second derivative along that affine line at zero equals the defined `hessianForm`. |
| `hessian_sos_identity` | The difference between `hessianForm` and the squared direction norm equals the explicit rational weighted-square certificate. |
| `hessianGapSOS_nonneg` | That certificate is nonnegative for all real inputs. |
| `quartic_second_deriv_lower_bound` | For every $X,v\in\mathbb R^3$, $\left.\frac{d^2}{dt^2}F(X+tv)\right|_{t=0}\geq\|v\|^2$. |

The last theorem is unconditional: it assumes no zero, positivity of
coordinates, bounded region, or normalized direction. It formalizes
the actual directional curvature corresponding mathematically to
$\nabla^2F(X)\succeq I$ everywhere.

## Derivatives and the rational certificate

For a scalar quadratic along a line, the file defines

\[
S(q,d,e,t)=(q+td+t^2e)^2.
\]

Lean proves its first derivative at every $t$ and the derivative of that
first-derivative formula at zero, namely $2d^2+4qe$.
The six quadratics $A,r_0,\ldots,r_4$ have their exact affine-line
expansions checked by polynomial normalization. Sum and difference
rules then prove the two derivatives of $F$ itself. Thus the argument
does not merely name a polynomial `hessianForm` and assume that it is
a Hessian. The required differentiability is established explicitly.

The certificate uses

\[
u=(x-3/4,y-1,z-1/2),\qquad
Z=(v,u\otimes v).
\]

The [generator](generate_ternary_lean_certificate.py) obtains the
existing exact factorization $M-I=LDL^{\mathsf T}$ from the
[targeted checker](check_ternary_rational_sos_convex_counterexample.py).
Clearing denominators separately in each component of $L^{\mathsf T}Z$
gives twelve integer linear forms $W_i(Z)$ and positive rational
weights $c_i$. The literal expression embedded in Lean is

\[
\operatorname{hessianForm}(X,v)-\|v\|^2
 =\sum_{i=0}^{11}c_iW_i(Z)^2+\sum_{i=3}^{11}Z_i^2.
\]

The nine extra squares account for the difference
$\|Z\|^2-\|v\|^2$. Lean's `ring` tactic proves the complete identity
after substitution into the original coordinates. Its `positivity`
tactic checks nonnegativity of the displayed rational weighted squares.
No numerical eigenvalue, approximate root, assumed matrix positivity,
external solver, or Python result is admitted as a proof premise.
Python generates a candidate expression; Lean checks it independently.

## Commands, results, and fingerprint

The final command, run from `formal/`, was

```sh
lake env lean TernarySOSDescent.lean
```

It exited with code zero and no warnings. The file prints transitive
axiom reports for six headline declarations: the zero, stationarity,
actual second derivative, certificate identity, certificate
nonnegativity, and actual curvature lower bound. Every report lists only

```text
[propext, Classical.choice, Quot.sound]
```

These match the repository's permitted foundations. The reports contain
neither `sorryAx` nor custom axioms. A scoped source search found no
`sorry`, `admit`, `axiom` declaration, or `native_decide`.

The checked Lean source SHA-256 is

```text
d290557f8c15084e53e51a883f3a23c4bb18975239a7523442e35cd8aec14e5e
```

Additional targeted commands actually run from the repository root were

```sh
python research-20260927/generate_ternary_lean_certificate.py > /tmp/ternary-lean-certificate.txt
sha256sum formal/TernarySOSDescent.lean research-20260927/generate_ternary_lean_certificate.py
```

An inline Python check reran the generator and compared its complete
output to the certificate definition in the Lean source; it matched
exactly. The existing exact checker also passed when invoked to obtain
its factorization. Its checks are additional finite arithmetic evidence,
not part of Lean's trusted basis. Scoped whitespace and local Markdown
link checks passed. No project-wide build, CI inspection, or separate
kernel replay was run. This standalone file is not imported into the
canonical aggregate.

The scoped whitespace command also passed:

```sh
git diff --check -- formal/TernarySOSDescent.lean research-20260927/generate_ternary_lean_certificate.py research-20260927/ternary-sos-descent-lean-verification.md
```

## What remains outside the formalization

The root equation $a^5=2$ is an explicit hypothesis for the zero and
stationarity results. This file does not prove existence, uniqueness,
or irrationality of that root. It does not formalize the number-field
argument excluding rational SOS, the minimum SOS coefficient-field
degree five, minimal dimension, or the positive-constant perturbation.
Those conclusions retain their separate mathematical proofs and reviews.

The file also does not state a `ConvexOn` or `StrongConvexOn` predicate,
the global lower bound $F(X)\geq\|X-p\|^2/2$, uniqueness of the zero,
or global nonnegativity as separate Lean theorems. Mathematically these
follow from the verified zero, stationarity, and curvature bound, but
that analytic implication is not packaged here. Nor does the file
declare a multivariate polynomial over $\mathbb Z$, verify its degree
or coefficient count, or formally assert positivity of the particular
$12\times12$ matrix. Its certified scalar identity suffices for the
directional curvature statement. Novelty and publication priority are
outside proof-assistant verification.
