# Independent review of rational affine-flow certificates

Date: 2026-09-12. Reviewer: a fresh agent assigned only this component.
Status: accepted within the stated assumptions. No correctness defect was
identified, and no implementation changes were requested.

Reviewed implementation:
[`rational_affine_flow.py`](../code/research_20260912/rational_affine_flow.py).
Its SHA-256 at review was
`2f00b3df92496d7a8a633f378ec7e0e96d2ea1741cf0b4dd07ba43a021a880a5`.
The mathematical description in
[`research-20260912-rational-flow.md`](research-20260912-rational-flow.md)
agrees with the code. This review makes no originality claim for matrix
exponential enclosures or comparison for cooperative linear systems.

The component rigorously certifies the final affine comparison solution for
exact rational inputs. Its role is conditional: the caller must establish the
initial lower bound and the differential inequalities that connect that
comparison solution to an original ODE. The review does not audit
`extended_rpd.py`, any support-generation procedure, or any original state tube.

## Proof audit

All matrices and scalar error bounds on the certificate path are computed
with `Fraction`. The documented admissible scalar inputs are Python `int`,
`str`, and `Fraction`. Floats and Boolean values are rejected. Decimal strings
specify exact decimal rationals; they do not certify the validity of a
previously rounded support.

On one slab let `X=hM`, where

\[
M=\begin{bmatrix}B&A&d\\0&0&0\end{bmatrix},
\qquad Z=\begin{bmatrix}C\\I\end{bmatrix}.
\]

The top rows of `exp(X) Z` give exactly the affine coefficients after the
slab: the lower augmented coordinates are the fixed parameters and the
constant one. The bottom identity block has size `p+1`, including when there
are no parameters. Its norm is one.

The Taylor-tail proof is valid. Put `q=||X||_inf`, let `K` be the Taylor
order, and let `N=X^(K+1)/(K+1)!`. For every integer `j >= 0`,

\[
\left\|\frac{X^{K+1+j}}{(K+1+j)!}\right\|_\infty
\le \|N\|_\infty
       \left(\frac{q}{K+2}\right)^j.
\]

This follows by repeated submultiplicativity; the actual successive
factorial denominators are at least `K+2`. Thus, when `q < K+2`, the
implemented bound

\[
\tau=\frac{\|N\|_\infty}{1-q/(K+2)}
\]

bounds the entire exponential remainder. Using the norm of the first omitted
matrix term is sound even when its entries have cancellations. A zero term
implies that every later power also vanishes, so the exact zero tail for a
nilpotent matrix is justified. The strict norm/order guard is checked before
division. Order zero is covered by this proof.

Let `Chat` be the current approximate coefficient matrix and suppose
`||C-Chat||_inf <= epsilon`. Let `T` be the Taylor matrix and `U` its top-left
state block. Before rounding, the next approximation is the top rows of
`T [Chat;I]`. Adding and subtracting the top rows of `T [C;I]` gives the bound

\[
\epsilon_{\rm next}^{\rm unrounded}
\le \|U\|_\infty\epsilon
   +\tau\bigl(\max\{\|\widehat C\|_\infty,1\}+\epsilon\bigr).
\]

The implemented recurrence has exactly these terms. In particular:

- Existing coefficient error is propagated only through `U`, since the
  bottom identity rows have no error.
- The remainder acts on the whole augmented matrix, so the identity norm
  must remain in the second term even if the current coefficients vanish.
- The exact row-sum norm of coefficient rounding is added. Rounding ties
  toward positive infinity causes no issue because the error is measured
  after rounding, including for negative values.
- Rounding the resulting nonnegative error upward to the chosen rational
  grid preserves the inequality. Induction starts from the exact supplied
  initial coefficient matrix and zero error.

The conversion from a coefficient error to an affine lower bound is also
correct. For every `p` in the box,

\[
\|[p;1]\|_\infty
\le P:=\max\{1,\max_j|p_j^{\rm lower}|,
                   \max_j|p_j^{\rm upper}|\}.
\]

Therefore every row evaluation differs by at most `epsilon P`. Subtracting
this common quantity from the constant column gives a lower affine
function everywhere in the box. No extra factor equal to the number of
parameters is needed: the induced infinity matrix norm already bounds the
sum of coefficient errors in each row.

The comparison argument requires only the state block `B` to be Metzler.
The forcing columns `A` and `d` may have either sign, and the code correctly
does not require the augmented matrix to be Metzler. If an absolutely
continuous original state satisfies `v' >= Bv+Ap+d` almost everywhere on the
slab and dominates the initial affine function, its difference from the
exact affine comparison solution satisfies `w' >= Bw`. Nonnegativity of
`exp(Bt)` for `t >= 0` and variation of constants imply `w >= 0`.
Sequential application proves the same statement over all supplied slabs.

## Independent exact checks

The independent verifier is
[`review_rational_affine_flow.py`](../code/research_20260912/review_rational_affine_flow.py).
The saved outcome is
[`rational-flow-independent-review.json`](../code/research_20260912/results/rational-flow-independent-review.json).

The reference exponential enclosure uses a different remainder bound from
the implementation. It computes a degree-70 Taylor polynomial in exact
rational arithmetic and uses

\[
\|e^X-T_{70}(X)\|_\infty
\le e^q\frac{q^{71}}{71!},
\qquad
 e^q\le(1-q/m)^{-m}
\quad\text{for an integer }m>q.
\]

The first inequality follows from the integral Taylor remainder, or from
its scalar series majorant. The second follows from
`-log(1-u) >= u` for `0 <= u < 1`. The verifier chooses `m=floor(q)+2`.
Both bounds are rational. Exact nilpotence is detected separately and gives
an exact matrix exponential. Entrywise rational intervals are propagated
through all slabs using interval multiplication. This produces independently
justified enclosures of the final coefficients without calling the
implementation's norm, multiplication, Taylor, rounding, or error routines.

For every test, the upper bound on the actual row-sum error obtained from
these reference intervals is at most the reported `coefficient_error`.
Every tested lower affine value is also below the lower end of the exact
reference evaluation interval.

The checks comprise:

- 100 deterministic randomized instances, with one to three states, zero to
  two parameters, and one to four slabs. State matrices include positive
  and negative diagonals and nonnegative off-diagonal entries; different
  slabs generally do not commute. Initial and forcing coefficients have
  both signs.
- Taylor orders `0, 1, 2, 6, 18` and rounding denominators
  `1, 7, 10^8, 10^20`. The norm/order condition is enforced for every
  generated instance.
- Nine explicit cases covering an empty horizon, zero elapsed time,
  negative rounding ties, order-zero positive and negative forcing,
  exact nilpotent chains, a fixed parameter interval, and two noncommuting
  triangular state matrices.
- 244 parameter-box endpoint combinations, including zero parameter
  dimensions and boxes with large positive or negative endpoints.
- 25 malformed inputs rejected, covering empty state dimensions,
  nonintegral or negative orders, invalid grid denominators, Boolean and
  floating inputs, incompatible matrix shapes, malformed or reversed
  boxes, negative durations, a non-Metzler state matrix, equality at the
  forbidden Taylor-norm threshold, and invalid evaluations.

The largest ratio of the independently enclosed row-sum coefficient error
to the reported bound was approximately `0.9547531363`.

A separate diagnostic compares 24 further instances with `mpmath.expm` at
120 decimal digits, using one to three states, zero or one parameter, one
to four slabs, Taylor order 30, and denominator `10^40`. All comparisons
passed; the largest observed error/bound ratio was approximately
`0.8974001787`. These external numerical comparisons are diagnostics, not
the exact certificate or its proof. The environment already includes
`mpmath 1.3.0` as a SymPy dependency; no package was added.

Reproduce the independent checks with:

```bash
uv run --project code/research_20260912 python code/research_20260912/review_rational_affine_flow.py
```

The implementation author's diagnostics were also run and passed. They
provide additional exact scalar checks and 60 SciPy comparisons, but the
independent test counts above do not include them.

## Scope and practical limits

The API and note accurately disclose the material limits. In particular,
the norm test uses the complete augmented matrix. Large forcing coefficients
can force subdivision or a higher Taylor order even when the state dynamics
are benign. The shared row error and its propagation can be conservative,
and rational numerator/denominator sizes during Taylor evaluation are not
uniformly bounded by the coefficient grid. These affect cost and bound
quality, not certificate validity.

The returned bound applies at the final endpoint of the supplied slabs.
A slab prefix gives its endpoint bound; no continuous-time interpolation
certificate is returned. Zero-duration slabs can still change the rational
approximation through rounding, with that change included in the error.
Empty slab sequences return the exact initial coefficients. Fixed boxes and
no-parameter systems are supported.

No exact arithmetic guarantee here validates a floating point source
support, an unproved state tube, or the original ODE model. Subject to those
caller obligations, the reviewed implementation gives a valid rational
lower affine certificate.
