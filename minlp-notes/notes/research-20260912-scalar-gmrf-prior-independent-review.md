# Independent review of the scalar GMRF prior reduction

Date: 2026-09-12. Reviewed
[the proposed reduction](research-20260912-scalar-gmrf-prior-reduction.md)
against Mahalanabis and Štefankovič's primary paper, §3.2/Theorem 43, and the
corresponding thesis treatment. This is a prior-method implication, not a
claim of a new algorithm or a completed implementation of the prior code.

The normalization, perturbation, constant-width Gaussian construction,
condition-number bound, and accuracy conversion are sound. The focused
target and restricted-candidate adaptations also work, with the singleton
target root described below. A printed local-cost formula in the source needs
care: it is inconsistent with the source's error-function definition in
general, but the focused construction can avoid using it at any nonzero
cost where that inconsistency matters.

The source's spectral-rounding numerical model remains a separate
implementation/bit-complexity qualification. It does not support claiming
that the specialized finite-history method is the first FPTAS.

## Algebraic reduction

The powers-of-two normalization is valid. From
`s^2<=rmin<4s^2` and `d_t^2<=r_t<4d_t^2`, one obtains
`s/d_t<2`, normalized noise in `[1,4)`, and normalized latent variance at
most `4B0`. The maximum normalized absolute sensitivity `h` is positive
after removing the trivial zero-sensitivity case. Dividing by `h` gives
`|g_t|<=1`, with equality somewhere. These operations are rational and have
polynomial-size encodings. The parameter rescaling multiplies every
schedule's information by the same positive factor.

For the normalized chain, the strict subdiagonal transition matrix has
operator norm at most `rho0`. Thus `T=(I-A)^(-1)` has largest singular value
at most `1/(1-rho0)` and smallest singular value at least `1/(1+rho0)`.
Adding independent variance `zeta` to the initial innovation and every
process innovation adds precisely `zeta T T^T` to the latent covariance.
The two spectral bounds in the reduction follow, including when the
original latent covariance is singular.

The normalized observation-error covariance satisfies `R>=I`. Since
`||diag(c_t)||<=2`, the perturbation adds at most
`4zeta/(1-rho0)^2 I`. With the proposed `zeta`, this is at most `tau I<=tau R`.
Principal submatrices preserve the bounds, and inversion gives

```text
I(S)/(1+tau) <= I_plus(S) <= I(S)
```

for every selected subset. No minimum process variance or finite-history
approximation is used in this part of the reduction.

Adding the independent unit-variance scalar target gives posterior variance
`1/(1+I_plus(S))`. The precision factors involve only a latent-chain edge or
the triangle `{vartheta,U_t,Z_t}`. The displayed bags cover every such edge
and satisfy running intersection, proving treewidth at most three.

For the covariance conditioning argument, the shear's off-diagonal block is
`[g,C]`, whose norm is at most `sqrt(n+4)`. Both the shear and its inverse
have norm at most `1+sqrt(n+4)`. Congruence therefore multiplies the block
diagonal covariance condition bound by at most
`(1+sqrt(n+4))^4`. This establishes the claimed
`O_(rho0,B0)(n^2/epsilon)` bound for covariance and precision alike. It also
explains why arbitrary original noise and sensitivity scales do not reappear
as exponentially large condition numbers.

The lower bound on the optimal information is correct. `D0` bounds the
**observation-error** variance `R_plus,tt`, excluding the artificial target's
own contribution to the unconditional variance of `Z_t`. At a candidate
with `|g_t|=1`, singleton information is at least `1/D0`. Cardinality `k>=1`
and monotonicity permit including that candidate in a size-`k` schedule.

If the prior algorithm achieves posterior variance at most `1+gamma` times
optimum, direct inversion gives

```text
I_plus(S_hat) >= [I_plus(S_star)-gamma]/(1+gamma).
```

Using `I_plus(S_star)>=1/D0` and the stated `gamma` proves the requested
relative information factor. Padding a smaller candidate set can only
increase both true and regularized Gaussian mean information. Combining
the regularization factor and adding any nonnegative original scalar prior
preserves the final approximation guarantee. The zero-sensitivity and zero-
cardinality cases should continue to be returned directly.

## Source recurrence audit and the focused specialization

I read the [primary paper](https://arxiv.org/pdf/1209.5991), Definition 18 and
equations (37)–(48), Observation 33, Lemmas 35 and 41–42, and Theorem 43.
I also checked the corresponding thesis equation (2.59) and the explicit
nonnegative weights in its earlier tree treatment. The displayed theorem
optimizes total conditional variance; the focused-target version is an
adaptation of its argument, not its literal wording.

There is a genuine inverse/submatrix-order issue in the printed local cost.
Equation (39), visually checked on PDF page 17, uses the inverse of the
precision principal submatrix on the charged private coordinates. The
definition of conditional error instead requires the corresponding
coordinates of the inverse of the full unobserved bag precision.

An exact local witness makes the distinction clear. Let the bag be
`{x,z}`, with private coordinate `x`, separator `z`, no observations, local
precision factor

```text
Lambda_bag = [[2,1],[1,2]],
```

and incoming separator precision `Q_zz=1`. The full bag precision is
`[[2,1],[1,3]]`. Its variance of `x` is `3/5`, whereas the printed private-
precision inverse gives `1/2`. Varying incoming `Q_zz` changes the actual
variance and leaves the printed value fixed. Both the paper and thesis
display this order of operations.

The natural general correction is simple. If `V` is the unobserved bag and
`U` the charged private coordinates, the weighted local cost is

```text
sum_(u in U) w_u [H^(-1)]_uu,
H = Lambda'_bag[V,V].
```

The source's relative Loewner approximation immediately bounds this cost:
invert on `V`, select the relevant coordinates, then apply a nonnegative
diagonal trace functional. Zero weights cause no problem when the scalar
inequalities are written without division. This correction retains the same
fixed-width arithmetic cost and relative-error induction.

For the present **single target** reduction, the author's subsequent root
construction avoids needing that general correction:

1. Attach a singleton `{vartheta}` bag between the chain decomposition and
   an empty root. Keep `vartheta` in every other nonempty bag.
2. Use only messages oriented toward that root. Binaryization may add
   singleton `{vartheta}` leaves or copies, retaining width at most three.
3. Give only `vartheta` nonzero weight. At every earlier message, the target
   is in the separator, so every charged private coordinate has weight zero.
4. At the final singleton target bag, the separator is empty. Its nonzero
   cost is the inverse of a scalar precision, so the printed and intended
   inverse/submatrix orders coincide.

Thus every local cost used by this focused computation is correct even
with the printed local formula. The Schur-complement precision-message
transformations still transmit the information required at the target.
The source's final normalization of total error by the number of nodes is
a schedule-independent factor and cancels in a multiplicative guarantee.

To restrict observations, require each separator observation set to lie in
the designated candidate set and each local observation subset to lie in
its intersection with the private coordinates. This removes choices but
does not change the precision transformations. The comparison proofs keep
the chosen observation subsets fixed when constructing their rounded
witnesses, so an allowed optimum retains an allowed witness. Zero-weight
latent and target nodes must remain forbidden observations; zero cost alone
would not prevent the algorithm from observing them.

## Complexity qualification and priority outcome

The augmented model has `2n+1` Gaussian coordinates and fixed treewidth.
Its rational encoding size is polynomial in original input size and
accuracy encoding. Both the condition number and `1/gamma` are polynomial
in `n,1/epsilon` for fixed `rho0,B0`. Substitution into the source's
displayed bounded-width running time therefore gives a polynomial
arithmetic-operation bound.

The primary rounding construction uses spectral decompositions and
exponential grids. A fully explicit Turing-model implementation needs
controlled finite-precision versions of those operations or an equivalent
rational net. This review does not supply that additional implementation
proof. Polynomial conditioning and constant separator dimension remove the
obvious numerical-size obstruction, but this observation is not a substitute
for specifying a rounding routine and its error allowance.

With that numerical-model qualification, the reduction provides a sound
known-method explanation for the scalar approximation-scheme existence
claim. The printed local-cost inconsistency is explicitly isolated, and the
focused root construction bypasses it. A first-FPTAS novelty claim is
therefore unsafe. The specialized finite-history method can still be
evaluated for its explicit dependence on accuracy, simpler implementation,
and computational performance. None of those advantages has been established
by this prior-reduction review.
