# Independent review of the rational circle minimizer construction

Date: 2026-09-28. Verdict: the stated construction passes this review.
Publication priority remains unestablished.

The reviewer did not develop the construction. I first reconstructed its
circle identity and denominator argument from the proposed outline, then
read the complete [construction](rational-convex-quartic-minimizer-height.md).
The frozen manuscript reviewed had SHA-256
`8179afc45f30d7f7c8d4dc57394ed7ad89b39b422c2e2fc900a20a6bf96cff0b`.
I also read the quantitative proofs in the
[strongly convex quartic construction](general-strongly-convex-quartic-singleton.md)
and the [rational Hessian certificate](sos-convex-quartic-realization.md).
Their abstract estimates apply here; the univariate hypotheses of their
original theorem statements are not being imported without proof.

## Denominators and the exact exposing identity

Write the true predecessor as \((a,b)\), with \(a^2+b^2=1\),
and let its successor be \((A,B)=(a^2-b^2,2ab)\).
With centered predecessor and successor displacements \(u\) and \(w\),
the local quadratic in the manuscript has the exact form

\[
 E_j(p+(u,w))=\|w\|^2-4(-b u_1+a u_2)^2.
 \tag{1}
\]

In particular, both its value and its full gradient vanish. Its
predecessor quadratic block is \(-4tt^{\mathsf T}\), where
\(t=(-b,a)\) has norm one. This checks the sign and the factor four,
including radial and tangential directions. There are no cross blocks.
Consequently the weights \(8^{-j}\) yield predecessor block lower
bounds \(8^{-j}/2\) and the last block \(8^{-k}I\). Thus the
claimed uniform bound \(H_*\succeq8^{-k}I\) holds, including
\(k=0\).

Cancellation in the final fractions cannot occur. In
\(\mathbb Z[\mathrm i]/5\mathbb Z[\mathrm i]\),
\((3+4\mathrm i)^2=3+4\mathrm i\). Every positive power therefore
has its real and imaginary numerators congruent to 3 and 4 modulo five.
Both fractions with denominator \(5^{2^j}\) are already reduced.
This proves a lower bound on ordinary binary output length even though
every coordinate has magnitude at most one.

## Approximation and the hypotheses of the quartic construction

Replacing \(a_j,b_j\) only as coefficients of \(r_j,s_j\) keeps
the quadratic's value at the exact point equal to zero. Approximating
the coefficients of a centered squared-distance polynomial directly
would not have this property; the displayed residual representation
does have it.

For coordinate errors bounded by \(\eta\), the error in one
predecessor block is

\[
 2\begin{pmatrix}\Delta a&\Delta b\\
             \Delta b&-\Delta a\end{pmatrix},
\]

whose norm is \(2\sqrt{\Delta a^2+\Delta b^2}\leq4\eta\).
Each block receives only one such error. This justifies the global
bound \(4\eta\), with no omitted sum over gates. The gradient
error is at most \(4kV\eta\) by the triangle inequality. The
chosen tolerance therefore gives \(H\succeq mI\),
\(\|H\|\leq L\), and \(\|\ell\|\leq\varepsilon\).

The dyadic iteration is also valid for negative coordinates. Rounding
each coordinate to a grid with error at most \(h\) contributes at
most \(2h\) in Euclidean norm. The recurrence
\(e_j\leq3e_{j-1}+2h\) gives
\(e_j\leq h(3^j-1)\). The prescribed mesh keeps this below one at
every stage, so the Lipschitz estimate is not used outside its domain.
The initial rational point can be represented exactly; subsequent
points are rounded before their denominators grow.

The residual Jacobian has identity diagonal blocks and determinant
one. More precisely, its squared Frobenius norm is \(2+10k\),
which is bounded by \(V^2=(4N)^2\). The determinant and norm bound
give \(\sigma_{\min}(J)\geq V^{-(N-1)}\). Each residual's
quadratic-part matrix has norm at most one, including the imaginary
residual's two off-diagonal entries equal to minus one. The two initial
linear residuals are allowed, with quadratic part zero.

These facts verify every abstract hypothesis used in the two imported
calculations: a rational vanishing quadratic with positive definite
leading part and small gradient, exactly \(N\) rational vanishing
residuals with a controlled invertible Jacobian, and controlled
quadratic parts. Their Hessian estimate gives \(\nabla^2F\succeq
(3/2)I\), and their block Gram estimate gives a strictly positive
definite full Hessian Gram. Nonnegativity and the residual equations
give the asserted unique rational zero. No root-isolation or
irreducibility assumption is needed at this stage.

## A rational Gram can be produced without the large fractions

The polynomial-time certificate claim is substantive: expanding the
exact rational center would be too expensive. The proposed approximation
and exact projection avoid that step.

For fixed rational output quadratics, their quadratic-part matrices
are independent of the center. Their gradients are affine functions
of it. In the centered block Gram, \(C\) is quadratic in the center,
\(D\) is affine, and \(Q\) is constant. Translating the Gram back
to the original variables still gives entries of degree at most two:
the upper-left block is \(C-DP-P^{\mathsf T}D^{\mathsf T}
+P^{\mathsf T}QP\), with \(P=p\otimes I\).

Here is an explicit precision bound if desired. Let
\(d=N+N^2\), and let \(B\geq1\) bound the coefficient absolute
sum of each of these entry polynomials. It can be computed using
polynomially many rational operations, and has polynomial bit length.
On \([-2,2]^N\), each partial derivative is at most \(4B\).
If all center coordinates are approximated within \(\delta\leq1\),
the Frobenius error is at most \(4dNB\delta\). Thus
\(\delta<\mu/(16dNB)\) suffices for error less than \(\mu/4\),
where \(\mu\) is the explicit positive rational spectral margin
from the certificate proof. The circle iteration supplies this precision
in polynomial bit time.

Projection onto the exact Hessian coefficient equations fixes the true
Gram and is nonexpansive in the Frobenius norm. It therefore preserves
positive definiteness and returns an exact rational identity. The
spectral margin, coefficient bound, and required precision all have
polynomial bit length. This argument needs no expansion of a minimal
polynomial, exact rational optimizer, or number field.

The optional integer-square scaling of the final polynomial preserves
the rational square factors. The determinant-over-trace eigenvalue
bound has polynomial bit length for this polynomial-size rational
matrix. Choosing an integer square above its reciprocal is effective
with the same bit bound.

## Significance and primary-source scope

The result rules out a polynomial bound on expanded rational optimizer
length under a rationality promise, even with bounded coordinates,
global strong convexity, and supplied rational certificates. It does
not imply hardness of deciding the minimum value, NP nonmembership,
or large SOS certificate size. In fact this family explicitly has
small rational SOS factors and a short exact arithmetic circuit for
its optimizer. The distinction between output representations is
essential.

I directly examined the following primary sources:

- Slot, Steurer, and Wiedmer, [*Hesse's Redemption*, v1,
  §1.2 and §1.3](https://arxiv.org/html/2511.03440v1).
  Theorem 1.1 bounds minimizer norm, and Corollary 1.2 gives rational
  additive approximations in polynomial time. These statements do not
  bound denominators of exact rational minimizers. Table 1 labels
  compact exact witnesses for convex quartics unknown in that version.
  The circle family is compatible with their approximation theorem.
- Jiang, [*Minimizing Convex Functions with Rational Minimizers*,
  Theorem 1.6 and Definition 2.6](https://arxiv.org/pdf/2007.01445).
  The exact rational-minimizer result assumes a bound on LCM vertex
  complexity, which measures the common denominator separately from
  coordinate magnitude. For the singleton here that parameter is
  \(\lceil2^k\log_2 5\rceil\), although the coordinate bound is
  one. The theorem therefore does not give a polynomial-time expanded
  output algorithm in the construction's input size.
- Zhang, [*Complexity Aspects of Fundamental Questions in Polynomial
  Optimization*, Example 2.5.3, printed pp. 49--50](https://optimization-online.org/wp-content/uploads/2020/08/7992.pdf).
  This gives rational local minimizers of cubic polynomials with
  exponential bit length through Khachiyan-type successive lower
  bounds on their coordinate magnitudes. The cubic is nonconvex and
  has unbounded local-minimizer sets. It does not establish the bounded,
  unique, globally strongly convex quartic construction here.

The searches used the phrases `convex quartic polynomial rational
minimizer exponential bit length` and `strongly convex polynomial
rational minimizer bit size repeated squaring`. These are scoped
comparisons, not a proof of novelty. I did not inspect every subsequent
paper citing these sources.

## Exact checks and their limits

I wrote and ran an independent
[exact checker](check_rational_circle_minimizer_review.py):

```text
python research-20260927/check_rational_circle_minimizer_review.py
```

It passed the symbolic local identity modulo \(a^2+b^2-1\), the
modular numerator identity, and exact fraction checks for
\(k=0,\ldots,8\). Those instances check reduced denominators,
dyadic approximation errors, exact vanishing after rounding, the
gradient bound, positive quadratic margins, and determinant-one
Jacobians. At \(k=1\), exact rational LDL verifies the full centered
Gram is positive definite. Symbolic expansion verifies its Hessian
identity and affine translation. A separate rounding and coefficient
projection check preserves the exact identity and the proved distance
to that Gram.

These computations support the identities and implementation of one
certificate. The uniform inequalities and polynomial bit bounds are
established by the arguments above, not by finite tests. No Lean proof,
project-wide verification, or CI inspection was performed.
