# Width-two hardness and the linear-noise scale

Date: 2026-10-02. Scope: compatibility check for the
[expected sparse solver](sparse-bag-cell-smoothed-qp.md), not a
general assertion that smoothed hardness is impossible.

Del Pia and Khajavirad prove strong NP-hardness for continuous box QP
at treewidth two, with bounded integral coefficients. The original
[paper](../../literature/papers/pia2026-treewidth-and-the-complexity-of/original.pdf),
Theorem 3 and its proof on printed pp. 21--24, was read directly for
this check. Its decision question is exact equality to a threshold;
bounded coefficients do not provide an inverse-polynomial gap to that
threshold.

The earlier [growth sanity check](../reviews/pruned-grid-hardness-sanity.md)
studied a unique-optimum YES family. For the smoothed theorem, the
more relevant family is a NO instance with an exponentially small
positive objective value.

## An explicit small-gap NO family

Take the SUBSET SUM items and target

```
A=2^r,       a_1=A,       a_2=A+2,       T=A+1,       r>=1.
```

The possible subset sums are `0,A,A+2,2A+2`, so this is a NO
instance. In the paper's notation,

```
U=2A+2,       ell=ceil(log_2(U+1))=r+2,
D=2^ell=4A,   N_var=2*2*ell+2+ell=5r+12.
```

The nonnegative objective `Psi` is the sum of binary penalties,
bit-copy squares, bit-serial recurrence squares, partial-sum squares,
target-recurrence squares, and the final square `(s_2-w_ell)^2`.
Choose the binary subset `(1,0)` and follow every recurrence exactly.
All variables remain in the unit box. Every term except the final
square is zero, while

```
s_2=A/D,       w_ell=(A+1)/D,
Psi(y)=delta=D^(-2)=2^(-2r-4).                                  (1)
```

The reduction proves that a zero of `Psi` exists exactly for a YES
instance. Compactness therefore gives

```
0 < min Psi <= delta.                                           (2)
```

The positive decision gap can consequently be exponentially small in
the number of constructed variables despite bounded coefficients and
unit boxes. Removing the constant `C` in the paper merely changes
the decision threshold from zero to `-C`; it does not change this gap.

## Inverse-polynomial noise does not preserve that threshold

The feasible trajectory `y` from (1) has at least one coordinate equal
to one: all copies of the first selected binary item have that value.
For independent symmetric uniform noise on `[-sigma,sigma]`, put
`Z=gamma'y`. The distribution of `Z` is symmetric. Conditioning on
every coefficient except one whose multiplier is one shows that its
density is bounded by `1/(2sigma)`. Hence

```
Pr{Z < -delta} >= 1/2-delta/(2sigma).                            (3)
```

On this event the perturbed objective at `y` is negative, so the
perturbed optimum crosses the original NO threshold:

```
Pr{min_x[Psi(x)+gamma'x] < 0}
 >= 1/2-delta/(2sigma).                                         (4)
```

For the symmetric `N_noise`-point rational noise grid, the same
conditioning gives
`Pr{|Z|<=delta}<=delta/sigma+1/N_noise`. Symmetry gives the exact
identity

```
Pr{Z < -delta} = [1-Pr{|Z|<=delta}]/2,
```

including any atoms at zero or at the interval endpoints. It follows that

```
Pr{min_x[Psi(x)+gamma'x] < 0}
 >= 1/2-delta/(2sigma)-1/(2N_noise).                             (5)
```

Thus inverse-polynomial noise has a substantial chance of changing the
original threshold answer on this NO family. Solving the sampled
objective exactly does not by itself decide the original equality
question. This directly explains why the bounded-coefficient width-two
hardness theorem is compatible with the new expected bound.

This check does not rule out a different robust reduction, or a method
that uses perturbed outputs in a more elaborate way. It establishes
only that this known reduction has no uniform inverse-polynomial value
gap and that its stated threshold is not preserved by the perturbation
scale used in a polynomial smoothed bound.

## Verification

The primary PDF was read with
`pdftotext -f 21 -l 24 -layout literature/papers/pia2026-treewidth-and-the-complexity-of/original.pdf -`.
An inline exact-fraction check constructed the NO trajectories for
`r=1,...,12`, verified all variables lie in the unit box, checked every
individual residual, and obtained precisely `D^(-2)` in all 12 cases.
The probability calculation is analytic; no sampling estimate is used.
Two independent checks confirmed the trajectory family and the
finite-law symmetry argument, including its treatment of atoms.
No project-wide verification or CI inspection was performed.
