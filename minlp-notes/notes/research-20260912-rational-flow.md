# Exact rational integration of held affine ODE supports

Date: 2026-09-12. Status: implementation and author checks complete; fresh
[independent review](research-20260912-rational-flow-independent-review.md)
accepted the implementation without a remaining defect. This is a certification component using standard matrix
exponential bounds and comparison, with no originality claim for either fact.

The implementation is
[`rational_affine_flow.py`](../code/research_20260912/rational_affine_flow.py).
It returns a rational affine lower bound at the final time of a sequence of
slabs, provided the supplied affine fields are valid lower supports on those
slabs. It does not use, validate, or assume an accurately integrated reference
trajectory. Establishing the support inequalities remains the caller's task.

## Interface and assumptions

```python
from fractions import Fraction
from rational_affine_flow import Slab, certify_affine_flow

certificate = certify_affine_flow(
    [Slab(Fraction(1, 10), B=[[-1]], A=[[2]], d=[3])],
    initial=[[1, 0]],
    parameter_box=[[-2, 3]],
    order=18,
    grid_denominator=10**12,
)
lower_coefficients = certificate.lower
lower_value_at_zero = certificate.evaluate([0])
```

For an `n`-dimensional state and `p` parameters, `initial` and the returned
coefficient matrices have shape `n` by `p+1`. Parameter coefficients precede
the constant column. Each slab has rational duration `h >= 0`, `B` of shape
`n` by `n`, `A` of shape `n` by `p`, and `d` of length `n`. Every off-diagonal
entry of `B` must be nonnegative. Parameter boxes are closed, bounded rational
intervals; fixed parameters and zero parameter dimensions are allowed.

The numerical core uses only the Python standard library. Inputs must be
`int`, `Fraction`, or rational strings; floats and Boolean values are rejected.
A string such as `"0.1"` means exactly `1/10`. Rationalizing approximate support
coefficients does not itself preserve their support property. The caller must
establish a correction for coefficient conversion if it starts with floating
point supports.

The mathematical assumption connecting the certificate to an original ODE
is as follows. For each fixed parameter in the supplied box, an absolutely
continuous state `v(t,p)` exists over the whole horizon, its initial value
dominates the supplied affine initial function, and almost everywhere on each
slab it satisfies

\[
\dot v(t,p)\;\ge\;Bv(t,p)+Ap+d
\]

componentwise. This inequality may follow from an affine support valid on an
established state domain containing the whole true trajectory. A support
valid only at the reference point is insufficient. Coefficients are held
constant within a slab; varying coefficients require more slabs or a separate
enclosure argument.

Let the exact affine comparison solution satisfy
`ell' = B ell + A p + d` with the supplied affine initial value. The difference
`w = v-ell` satisfies `w' >= B w`. Since `B` is Metzler, its exponential is
entrywise nonnegative: choose a scalar `a` with `B+aI >= 0` and expand
`exp(Bt)=exp(-at) exp((B+aI)t)`. Variation of constants then gives `w >= 0`.
Apply this argument sequentially across the slabs. The returned function is
below this exact comparison solution, hence also below `v`.

## Rational coefficient enclosure

Write `ell(p)=C [p;1]`, with an exact, possibly irrational coefficient matrix
`C`. On a slab define

\[
M=\begin{bmatrix} B&A&d\\0&0&0\end{bmatrix},\qquad
Z=\begin{bmatrix} C\\I_{p+1}\end{bmatrix}.
\]

Then the exact next coefficient matrix is the top `n` rows of
`exp(hM) Z`. All norms below are induced infinity norms, namely the largest
absolute row sum. The finite Taylor polynomial

\[
T_K=\sum_{j=0}^K\frac{(hM)^j}{j!}
\]

is computed with exact fractions. Put `q=||hM||_inf`. The interface requires
`K+2 > q`; otherwise it raises an error explaining that the caller can raise
the order or subdivide the slab. The exponential remainder satisfies

\[
\|\exp(hM)-T_K\|_\infty
\le \tau :=
\frac{\|(hM)^{K+1}/(K+1)!\|_\infty}{1-q/(K+2)}.
\]

Indeed, after the first omitted term each successive term has norm at most
`q/(K+2)` times its predecessor's bound. Summing the resulting geometric
series proves the formula. Computing the norm of the first omitted matrix
term is at least as strong as replacing it with `q^(K+1)/(K+1)!`. In
particular it detects a zero tail when the matrix is nilpotent of sufficiently
small index.

Suppose the current rational approximation is `Chat`, with a certified error
`||C-Chat||_inf <= epsilon`. Let `U` denote the upper-left `n` by `n` block of
`T_K` and let `D` be the top rows of `T_K [Chat;I]`. Before grid rounding,

\[
\|C_{\rm next}-D\|_\infty
\le \|U\|_\infty\epsilon
  +\tau\bigl(\max\{\|\widehat C\|_\infty,1\}+\epsilon\bigr).
\]

To see this, add and subtract `T_K [C;I]`. Its coefficient error is
`U(C-Chat)`. The remaining error is the top rows of
`(exp(hM)-T_K)[C;I]`, whose norm is bounded by
`tau max(||C||_inf,1)`. The stated expression follows from the triangle
inequality. The identity in the augmented rows is essential; omitting its
norm can produce an invalid bound when all current coefficients are small.

Every entry of `D` is rounded to the nearest multiple of `1/grid_denominator`.
The implementation calculates the exact row-sum norm of this rounding error
and adds it to the right side. It then rounds the scalar error bound upward
to the same grid. Both operations preserve validity and keep denominators
controlled between slabs. The initial matrix is exact and starts with zero
error; an empty slab sequence therefore returns it unchanged.

At the final time, let

\[
P=\max\{1,\max_j|p_j^{\rm lower}|,\max_j|p_j^{\rm upper}|\}.
\]

For every parameter in the box, each row evaluation error is at most
`epsilon P`. Subtracting this quantity from every constant coefficient of
`Chat` gives the returned rational lower affine functions. There is no
additional parameter-count factor because `epsilon` already bounds the
row-sum coefficient norm.

`FlowCertificate.approximate` stores `Chat`; `coefficient_error` stores
`epsilon`; `evaluation_error` stores `epsilon P`; `lower` stores the shifted
coefficients. Each `SlabRecord` records its duration, `q`, Taylor tail,
coefficient rounding norm, and final error bound. `evaluate` returns exact
fractions and rejects parameters outside the stated box.

## Checks and reproduction

Run the self-contained diagnostics in the existing isolated environment:

```bash
uv run --project code/research_20260912 python code/research_20260912/rational_affine_flow.py
```

The exact scalar test uses
`ell' = ell + 2p + 3`, `ell(0)=p+1`, and unit time. Its final coefficients
are `(3e-2, 4e-3)`. An independently computed rational enclosure of `e`, using
the scalar series through degree 60 and a geometric tail, verifies the
entire row coefficient error bound and lower evaluations at three parameter
values. With order 35 and denominator `10^12`, the certified coefficient
error is exactly `1/10^12`.

Additional exact checks cover a nilpotent forcing flow, an empty horizon,
and coefficient rounding at zero elapsed time. Six malformed-input checks
cover floating inputs, reversed boxes, negative durations, a non-Metzler
matrix, an insufficient Taylor order, and evaluation outside the box.

Sixty deterministic floating point diagnostics compare with SciPy `expm` for
one to four states, zero to two parameters, and one to five noncommuting
slabs. They passed; the largest observed coefficient error divided by its
certified bound was approximately `0.991584`. These comparisons are
diagnostics, not the mathematical certificate. A run took approximately
0.65 seconds on the current computer. The certificate path itself performs
no floating point arithmetic and does not call SciPy.

The code reuses the existing project environment and adds no dependencies.
The environment currently records Python 3.13.11, NumPy 2.5.3 and SciPy
1.18.1; NumPy and SciPy are used only in these optional diagnostics.

The independent reviewer additionally verified 100 randomized and nine
explicit cases using a different exact rational exponential enclosure,
244 parameter-box corner combinations, 25 malformed inputs, and 24 mpmath
comparisons at 120 decimal digits. The independent report preserves its
verifier and machine-readable results.

## Limits

- This certifies integration of the supplied affine fields. It cannot repair
  invalid support inequalities, an invalid initial bound, or a state tube
  that does not contain the original trajectory.
- The output certifies the final time. To obtain a certificate at a slab
  endpoint, propagate the corresponding prefix; no assertion is made about
  a polynomial interpolation within the slabs.
- A large norm of the augmented forcing block can make the norm tail loose
  or require a higher order even when the exact dynamics are benign.
  Slab subdivision is a valid remedy. Adaptive subdivision and sharper
  blockwise exponential bounds are not implemented.
- The scalar error is shared across rows and can be conservative. The
  default fixed grid introduces a controllable error floor. The result is
  exact arithmetic certification, not a claim that the resulting relaxation
  is tight or computationally superior to established validated integrators.
