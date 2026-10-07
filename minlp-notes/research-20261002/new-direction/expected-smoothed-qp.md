# Expected exact work for perturbed QPs with at most two negative directions

Date: 2026-10-02. Status: complete proof with a
[fresh independent review](../reviews/expected-smoothed-qp-review.md).
The finite-grid growth tail is an input from the separately reviewed
[proximal-tail note](proximal-growth-tail.md). No novelty claim.

The growth-conditioned negative-inertia algorithm can be combined with
an exact fallback to obtain an expected-work theorem. The same sampled
objective is used throughout. The algorithm never resamples or conditions
the perturbation distribution on successful optimization.

## 1. Result

Let

\[
 F_\xi(x)=\tfrac12x^TAx+(b+\xi)^Tx+c,
 \qquad X=\{x:Cx\le d\},
\]

where the base data are rational, `A` is symmetric, and `X` is a
nonempty bounded rational polytope in `R^n`, described by `m`
inequalities. Lower-dimensional polytopes and redundant inequalities
are allowed. Let

\[
 k=n_-(A)\le2,\qquad
 \nu=\max\{0,-\lambda_{\min}(A)\},\qquad
 S=\sum_{i=1}^n\left(\max_{x\in X}x_i-\min_{x\in X}x_i\right).
\]

Fix a positive rational noise half-width `sigma`. Put

\[
 F_{\rm face}=2^m,\qquad B=\max\{2,2^m\},\qquad
 D=8(F_{\rm face}+1)^2.
\]

Choose the least power of two `M` satisfying

\[
 M\ge 2nDB,
\tag{1}
\]

and sample every `xi_i` independently and uniformly from

\[
 \left\{-\sigma+\frac{2\sigma j}{M-1}:j=0,\ldots,M-1\right\}.
\tag{2}
\]

The zero-variable case is trivial and is handled before this sampling
rule. Each index uses exactly `log_2 M=O(m+log(n+1))` unbiased random
bits. The perturbed rational input length is polynomial in the base
input length, including the binary description of `sigma`.

**Theorem.** There is an always-correct algorithm that returns an exact
rational optimizer and exact optimum value for every draw (2), including
draws with multiple optimizers. If `I` is the base input length including
`sigma`, then for an absolute constant `K` its expected bit work is at
most

\[
 (I+1)^K\left(1+\frac{\nu S}{\sigma}\right).
\tag{3}
\]

The constant and exponent are uniform for `k<=2`. A numerical bound on
`nu S/sigma`, rather than merely its binary encoding length, therefore
gives expected polynomial time. The algorithm does not need the growth
modulus, `nu`, or `S` as supplied inputs. For `k=0`, a single exact convex
QP solve already gives a deterministic polynomial-time algorithm.

The output solves the perturbed objective. No conclusion about the exact
optimizer of the base objective is asserted. The finite-grid law (2),
whose precision is part of the theorem, is not an arbitrary coarser
discrete approximation to continuous noise.

## 2. The growth tail on this fixed grid

For every draw, let `g_*(xi)` be the largest global quadratic-growth
modulus of `F_xi` on `X`, with `g_*=0` when there are distinct
optimizers and `g_*=infinity` when `X` is a singleton. The
[finite-grid theorem](proximal-growth-tail.md) supplies, for every
`epsilon>0`, on the same grid (2),

\[
 \Pr\{g_*<\varepsilon\}
 \le a\varepsilon+\beta,\qquad
 a=S/\sigma,\qquad \beta=2nD/M.
\tag{4}
\]

The component bound `D=8(F_face+1)^2` is independent of `epsilon`, of
the grid precision, and of the numerical coefficient values. This
uniformity is needed when integrating the tail below. The sampling rule
(1) guarantees

\[
 \beta B\le1.
\tag{5}
\]

In particular, possible atoms at ties are included in the residual term
`beta`. The argument does not assume that every rational perturbation
has positive growth.

## 3. An exact fallback with no growth assumption

There is a deterministic exact algorithm using at most

\[
 B P(L)
\tag{6}
\]

bit operations, where `L` is the perturbed input length and `P` is a
fixed polynomial. Its exponential factor `B` depends only on the number
of base inequalities; sampling precision affects the polynomial factor.

Enumerate all subsets `J` of the input rows of `C`. Skip any subset whose
rows are linearly dependent. For an independent subset, write
`E=C_J`, `e=d_J`, and form the rational KKT matrix

\[
 K_J=\begin{pmatrix}A&E^T\\E&0\end{pmatrix}.
\]

Skip singular matrices. Otherwise solve exactly

\[
 K_J\binom{x}{\lambda}=\binom{-(b+\xi)}{e}.
\tag{7}
\]

Keep every resulting `x` satisfying all inequalities `Cx<=d`, and
return one having the least perturbed objective value `F_xi(x)`. A positive
semidefiniteness test or a sign restriction on these multipliers is
unnecessary: every retained point is genuinely feasible, and the list
contains a global optimizer.

To see the latter claim, choose a global optimizer lying in a face of
smallest possible dimension. It lies in the relative interior of that
face. Its restricted gradient vanishes and the Hessian on the tangent
space is positive semidefinite. If that Hessian had a null direction,
the quadratic would remain constant along that direction until reaching
a lower-dimensional face, contradicting minimality. The tangent Hessian
is therefore positive definite, or the face is a vertex. An independent
basis of its active input rows defines its affine hull. For that subset
`J`, the matrix in (7) is nonsingular and its solution is the chosen
optimizer.

This argument also covers a singular ambient Hessian, lower-dimensional
`X`, and a continuum of optimal points. Equal candidate values are
handled by a deterministic tie rule. Rational linear algebra, feasibility
tests, and comparisons take polynomial bit work per subset. Determinant
bounds give polynomial-length coordinates and objective values. Thus
the fallback always terminates and proves (6).

## 4. The explicit conditioning exponent of the fast algorithm

Use the algorithm from [the negative-inertia note](negative-inertia-qp.md)
as the second computation. When `g_*>0` and `k` is either one or two,
unpacking its proof gives constants `d>=0` and a polynomial `P`,
independent of `k<=2`, such that its exact running time is at most

\[
 P(L) Z^{k/2}(1+\log Z)^d,
 \qquad Z=\max\{1,\nu/g_*\}.
\tag{8}
\]

Enlarge the common polynomial `P` so that it also bounds the fallback
in (6). There is no extra power of `nu/g_*` hidden in (8):

- Rational spectral normalization gives an auxiliary dimension at most
  `k` and auxiliary conditioning `kappa<2+4nu/g_*`.
- The number of retained cells per level, including child generation
  and corner queries at fixed `k<=2`, is
  `O((1+sqrt(kappa))^k)`.
- Exact optimum-value isolation and auxiliary-coordinate recovery need
  `poly(L)+O(log kappa)` levels.
- At level `j`, corner coordinates, convex-QP inputs and rational
  witnesses have bit length polynomial in `L+j`. Exact convex QP,
  rational reconstruction, and the other work have fixed polynomial
  exponents. Consequently depth and arithmetic introduce only a fixed
  power of `1+log Z` in addition to `P(L)`.

These statements use the polynomial-time convex-QP algorithm specified
in the negative-inertia note. Treating a numerical solver call as an
unverified unit-cost oracle would not establish (8).

The fast computation's certificates and exact acceptance tests remain
sound when `g_*=0`; only its termination guarantee can fail. The fallback
handles those draws. If all auxiliary coordinate ranges are constant,
the fast computation terminates with its one-solve branch, which also
obeys the bound after enlarging `P`.

## 5. Interleave the computations on one draw

After sampling once, run the fallback and the fast exact algorithm on
the same perturbed input. Interleave their elementary bit operations
and stop when either returns its exact answer. This can be implemented
with interruptible rational and convex-QP algorithms; it is not an
instruction to wait for an uninterruptible oracle call before allowing
the other computation to proceed.

Up to fixed simulation overhead, the total work is at most

\[
 2P(L)\min\{B,Z^p(1+\log Z)^d\},\qquad p=k/2,
\tag{9}
\]

where `Z=infinity` is allowed on `g_*=0`, so the minimum equals `B`.
The polynomial costs of sampling and preprocessing can be added to this
bound. The algorithm need not know `P`, `g_*`, or the time of either
computation to interleave them.

For every `Z>=1` and `B>=2`,

\[
 \min\{B,Z^p(1+\log Z)^d\}
 \le (1+p^{-1}\log B)^d\min\{B,Z^p\}.
\tag{10}
\]

If `Z^p<=B`, the logarithmic factor has the displayed upper bound. If
`Z^p>B`, the left side is at most `B` and the right side is at least
`B`. This simple cap removes the need to prove a separate universal
rational lower bound on positive growth. Even extremely small growth
cannot force unbounded precision before the fallback ends.

## 6. The capped inverse-growth moment

Let `r=a nu=nu S/sigma`. By (4), for `t>=1`,

\[
 \Pr\{Z>t\}\le r/t+\beta.
\tag{11}
\]

Using the tail integral of the bounded random variable
`min(B,Z^p)` gives

\[
 \begin{aligned}
 \mathbb E\min\{B,Z^p\}
 &=1+\int_1^B\Pr\{Z^p>t\}\,dt\\
 &\le1+r\int_1^B t^{-1/p}\,dt+\beta(B-1).
 \end{aligned}
\tag{12}
\]

For one negative direction, `p=1/2`, so

\[
 \mathbb E\min\{B,Z^{1/2}\}\le1+r+\beta B\le2+r.
\tag{13}
\]

For two negative directions, `p=1`, so

\[
 \mathbb E\min\{B,Z\}\le1+r\log B+\beta B
 \le2+r\log B.
\tag{14}
\]

The cap is decisive in (14): integrating `1/t` without it does not
bound expected work. Both inequalities include all bad draws and ties.
Combining (9)--(14), `log B=O(m+1)`, and the polynomial bound on `L`
proves (3).

The atom correction creates no sampling-size circularity. The grid is
chosen against the combinatorial count `B`, not against a bit-work bound
containing its own sampling precision. After (5), the atom contribution
is at most the same external polynomial `P(L)` and the capped logarithmic
factor as all other terms. As `log M=O(m+log(n+1))`, both remain
polynomial in the base input length.

For `k>2`, the same calculation has `p>1` and gives a term of order
`r B^(1-1/p)`. That is generally exponential. The proof therefore does
not establish the stated expected polynomial bound for three or more
negative directions.

## 7. Scope and verification

The theorem strengthens a high-probability conditioning statement to an
expected exact-work statement by combining a sharp inverse-growth
exponent with a deterministic fallback. It does not claim expected
polynomial time for the uncapped conditioned algorithm. Its guarantee
applies to a single draw from the explicit fine rational grid, including
every realization where the fast algorithm has poor conditioning.

The magnitude `nu S/sigma` is material. Very narrow noise, large negative
curvature, or large feasible coordinate ranges can make (3) large even
when their encodings are short. Positive curvature enters the ordinary
rational input length and convex arithmetic; it is not an additional
numerical multiplier in (3).

The proof uses the existing exact convex-QP theorem, the separately
reviewed spectral normalization and conditioned solver, and the new
finite-grid tail. It makes no claim of publication priority or competitive
practical running time.

A delegated agent independently checked the exact fallback, the absence
of sampling-size circularity, the capped logarithmic factor, and the
inverse-growth integral before this draft was written. Its
[completed-text review](../reviews/expected-smoothed-qp-review.md) found
no mathematical or bit-complexity blocker. The parent researcher also
independently read the full proof and checked the fallback, conditioning
exponent, capped logarithms, uniform grid tail, and expectation integral;
that was an analytic check, not executable validation.

The targeted command actually run was

```text
python research-20261002/new-direction/check_expected_smoothed_qp.py
```

It passed five exact-rational active-subset fallback fixtures, covering
a zero objective, a singular ambient Hessian with an optimal edge, a
lower-dimensional segment, a concave endpoint tie, and redundant
equalities. The [checker](check_expected_smoothed_qp.py) reuses the
existing diagnostic face enumerator. It does not implement the
perturbation tail, production convex-QP algorithm, interleaving, or an
expected-runtime benchmark. No project-wide checks, CI inspection, or
literature search were performed in this workstream.
