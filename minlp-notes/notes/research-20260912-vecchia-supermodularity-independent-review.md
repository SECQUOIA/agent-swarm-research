# Independent review of the Vecchia pivot supermodularity counterexample

Date: 2026-09-12. This is a bounded review of the counterexample proposed in
[the localized-factor priority audit](research-20260912-noisy-markov-fsai-priority-audit.md).
It does not assess the rest of the source or establish priority for the
counterexample. No author was contacted, and no production solver or
literature knowledge-base file was changed.

The counterexample is correct. It contradicts the supermodularity inequality
used in the source proof, under both the displayed fixed-order formulation
and the intended pivot-first column-Nyström-plus-diagonal formulation. The
failure is independent of the source's positive objective scaling.

## Source scope and convention

I inspected the primary PDF of Eagan Kaminetz's
[*Everything is Vecchia: Unifying Column Nyström and Sparse Vecchia Approximations*](https://math.ucsd.edu/sites/math.ucsd.edu/files/Eagan%20Kaminetz%20Thesis%20Final.pdf),
§4.1.3, printed pages 12–13, accessed 2026-09-12. Theorem 4.3 expressly allows
an arbitrary positive-definite matrix. Its displayed sparsity pattern retains
the pivot indices preceding each variable in the ordering. Its objective is
one half of the Gaussian KL divergence, and equation (4.10) asserts
supermodularity. The proof uses the marginal identity (4.9). No Matérn,
Markov, or additional conditional-independence assumption appears in that
theorem.

The sections preceding the theorem discuss a permutation that moves pivots
to one end of the factorization order. Both conventions are checked below.
The narrower conclusion that is insensitive to this convention is the failure
of equation (4.10).

## Exact independent construction

Set

```text
R = [[1,   0,   3/5],
     [0,   1,   3/5],
     [3/5, 3/5, 1  ]].
```

The leading principal minors are `1,1,7/25`, so `R` is strictly positive
definite. Use fixed order `1<2<3` and the displayed conditioning sets
`H_j={i in I:i<j}`. Write `Q_I` for the corresponding working precision,
and use the ordinary KL convention

```text
g(I)=KL[N(0,R) || N(0,Q_I^(-1))].
```

Independent direct construction gives

```text
Q_empty = I,

Q_{1} = [[25/16,   0, -15/16],
         [    0,   1,      0],
         [-15/16,  0,  25/16]],

Q_{2} = [[1,      0,      0],
         [0,  25/16, -15/16],
         [0, -15/16,  25/16]],

Q_{1,2} = [[ 16/7,   9/7, -15/7],
           [  9/7,  16/7, -15/7],
           [-15/7, -15/7,  25/7]] = R^(-1).
```

These follow by regressing the third variable on its retained pivots and
forming `Q=A^T D^(-1)A`. In particular, the two one-pivot regressions have
coefficient `3/5` and residual variance `16/25`; the two-pivot regression has
coefficient vector `[3/5,3/5]` and residual variance `7/25`.

Exact rational arithmetic independently verified `tr(Q_I R)=3` for all four
matrices. The Gaussian KL formula therefore reduces to

```text
exp(2g(I))=1/[det(Q_I) det(R)].
```

The values are

| Pivot set `I` | `exp(2g(I))` |
| --- | ---: |
| empty | `25/7` |
| `{1}` | `16/7` |
| `{2}` | `16/7` |
| `{1,2}` | `1` |

Supermodularity requires the following slack to be nonnegative:

```text
g(empty)+g({1,2})-g({1})-g({2})
  = (1/2) log(175/256) < 0.
```

Its sign is exact because `175<256`; it does not depend on numerical
logarithms. The source's objective `f=g/2` has slack
`(1/4)log(175/256)`, with the same strict violation.

For pivot-first CNV, jointly retain the selected pivot block and approximate
the unselected variables as conditionally independent given the pivots.
For the four sets above, the same matrices result. Specifically, variables
one and two are uncorrelated, so moving the single pivot two before variable
one changes no nonzero regression. Thus the counterexample also applies to
that interpretation of the pivot-set objective.

## The marginal identity does not describe this objective

For the pivot-first CNV model, an independent determinant calculation gives
the exact objective

```text
2g(I)=logdet(R_II)
       +sum_(j notin I) log Var(Y_j|Y_I)-logdet(R).
```

Adding a pivot `ell` cancels its own conditional-variance term against the
pivot-block determinant change, leaving

```text
2[g(I union {ell})-g(I)]
  =sum_(j notin I union {ell})
     log[Var(Y_j|Y_I,Y_ell)/Var(Y_j|Y_I)].
```

This sum of logarithms of individual conditional variances is generally
different from the logarithm of a joint residual determinant.

For example, adding pivot one to the empty set gives an actual unscaled
marginal `2[g({1})-g(empty)]=log(16/25)`. The conditional-variance expression
in (4.9) instead gives `log(7/16)`, because
`Var(Y_1|Y_2,Y_3)=7/16` and `Var(Y_1)=1`. Moreover, that expression gives
the same result after conditioning on pivot two, since `Var(Y_1|Y_2)=1`.
The true two marginals differ. Thus changing a global KL normalization cannot
repair the identity.

This locates the issue in the displayed conversion from sums of conditional
diagonal logarithms to a joint log determinant. The Schur-complement
conditioning monotonicity used after that conversion is itself valid.

## Separate consequence under the literal fixed-order interpretation

The four-set table alone already disproves the supermodularity step. A
stronger consequence is available if the theorem is read with one fixed
ordering `1<2<3` for every candidate set. In that formulation, pivot three
changes no conditioning set, so `g({3})=g(empty)`. The greedy first pivot is
therefore one or two. With target cardinality `m=2`, the optimum is zero at
`{1,2}`. At `t=1`, the displayed exponential convergence inequality would
require

```text
g({1}) <= exp(-1/2) g(empty).
```

It fails: the two sides are approximately `0.4133393` and `0.3860464`.
An exact sign argument avoids relying on these approximations:

```text
16^8 = 4,294,967,296 > 3,349,609,375 = 25^5 7^3,
```

so `log(16/7)/log(25/7)>5/8`. Also
`exp(1/2)>1+1/2+1/8=13/8>8/5`, giving `exp(-1/2)<5/8`.
The extra positive scaling of `f` again cancels.

This additional convergence-bound contradiction must remain explicitly tied
to fixed order. With pivot-first CNV, pivot three instead has
`exp(2g({3}))=256/175`, so greedy chooses it and this particular
convergence-bound contradiction disappears. The supermodularity
counterexample still holds. A failure of the proof alone should not be
reported as disproving every possible convention's final greedy guarantee.

## Review outcome

The robust finding is an exact counterexample to the general supermodularity
claim and the marginal identity supporting it. The stronger fixed-order
convergence counterexample is separately qualified above. This review does
not affect the established Vecchia regression formula, the other results in
the thesis, or the independently proved noisy Markov memory bound.
