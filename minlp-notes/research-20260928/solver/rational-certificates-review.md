# Independent review of rational sparse box certificates

Date: 2026-09-28. Reviewed
[rational-sparse-certificates.md](rational-sparse-certificates.md), including
the revised denominator bound, the explicit free-coordinate feasibility
reduction, and the revised literature discussion. This review did not edit
the source note. A further independent subagent audited the feasibility
reduction and its bit-complexity assumptions.

**Verdict:** the stated certificate existence, encoding-length, and
polynomial-time construction results are supported by the arguments, under
the stated quantitative slack promise and with the full local preordering
bases. One minor denominator claim in the initial version was false. It
has been corrected and independently rechecked; the theorem and asymptotic
bound are unchanged. No remaining substantive gap or counterexample was
found. This is evidence from adversarial review, not formal verification.

## 1. Scope and significance

The central sufficient hypothesis is that `p-tau` already has a real PSD
Gram certificate in the chosen finite cone. The tree, running intersection,
and kernel error estimate supply that hypothesis. They are not needed for
the subsequent rationalization. The theorem consequently makes no hidden
claim that pointwise positivity of `p` at an arbitrary order implies
strict Gram feasibility at that order.

The useful consequence is exact, independently checkable rational lower
bound certificates at the order supplied by the sparse kernel theorem.
The analysis discharges the finite cone's interior and boundedness
requirements with explicit box formulas. This can support certified
optimization, but it is not a standalone new general rational SOS method,
an efficient practical SDP implementation, or a polynomial-time result in
the original polynomial input size. In particular, the `2^w` generator
products and order-dependent monomial bases are included in the expanded
dimensions. The note states these limitations appropriately.

## 2. Algebra and transfer of objective slack

For each allowed diagonal position, the first sum in equation (4)
telescopes to `1-x^(2alpha)`: its `i`th group is

\[
 \left(\prod_{j<i}x_j^{2\alpha_j}\right)
 (1-x_i^{2\alpha_i}).
\]

The second sum telescopes to `x^(2alpha)(1-g_I)`. Its `q`th square has
monomial degree `|alpha|+1` and generator set of cardinality `q-1`, so
the sum of these degrees is `|alpha|+q<=|alpha|+|I|<=r`. The first sum's
terms also meet the permitted degree bound. In particular, every term is
in an existing block, including when `alpha=0`, when `I` is empty, and
when a source term is at maximum allowed degree.

Summing `D` source identities gives one baseline unit in each local
diagonal position. After division by `D`, every block is at least
`I/D`. A source identity has exactly `1+|alpha|+|I|` displayed square
terms, counted with multiplicity; hence the aggregate trace is at most
`r+1`. Coincident terms only add their nonnegative diagonal weights and
cannot invalidate this bound. Thus equation (5) is correct.

For the slack transfer, write a real certificate for `f-rho_r` as `G`.
The stated promise gives

\[
 \rho_r-\gamma-\tau
 \ge f^*-E_r-\gamma-\tau\ge0.
\]

Adding this nonnegative constant gives a PSD certificate for `p-tau`.
Adding `tau H` then gives a feasible tuple with every block at least
`eta I`, where `eta=tau/D`. This uses the finite SDP dual attainment
established in the underlying note; it does not infer rationality of
`rho_r`, `f*`, or `G`.

## 3. The rational outer bound

Each moment matrix `W` is positive definite because its monomial vector
is linearly independent and its nonnegative weight is strictly positive
on the open box. The product-uniform moment factors in equation (8) are
correct. Their denominators divide `((2r+3)!)^(2w)` because there are at
most `w` factors, each with at most two denominator factors bounded by
`2r+3`.

If a block has size `s`, the integer matrix `q0 W` has a positive integer
determinant. Thus `det(W)>=q0^(-s)`. Since every diagonal entry is at
most one, `trace(W)<=s`, and every eigenvalue is at most `s`. Dividing
the determinant lower bound by `s^(s-1)` gives the claimed minimum
eigenvalue bound. Replacing `s` with `S` weakens it in the correct
direction. The special case `s=1` is consistent with the convention in
the note.

For PSD `Q`, `trace(WQ)>=lambda0 trace(Q)`. The global polynomial
identity and the single global product measure give

\[
 \lambda_0\sum_{b,I}\operatorname{tr}Q_{b,I}
 \le \ell(p)\le\|p\|_1.
\]

Overlap of bags does not change this identity. The aggregate Frobenius
norm is at most the sum of the PSD blocks' traces, so the resulting
outer bound applies to every feasible PSD tuple, including the unknown
strictly feasible one. No computed feasible point is needed to obtain it.

The apparently large factorial is compatible with the stated complexity:
`r+1<=S`, because at least one nonempty bag has an empty-generator block;
also `w<=r`. Consequently the encoding length of `lambda0` is polynomial
in the expanded dimensions. The construction does not assert favorable
numerical conditioning.

## 4. Global coefficient correction and the repaired denominator claim

Every global output monomial has a containing bag and degree at most
`2r`. Its exponent can be split into two nonnegative exponents of
degree at most `r`. In the empty-generator block this gives a column
with one nonzero coefficient: one for a diagonal entry or two for an
off-diagonal coordinate. Distinct output exponents require distinct
matrix positions, since a fixed position has only one exponent sum.
Thus the proposed pivot columns exist simultaneously even when bags
overlap, and `mathcal A Z=id` holds on the whole stated output space.

The aggregate Frobenius norm of each `Z_beta` is either one or
`1/sqrt(2)`. Their supports are disjoint. In particular, the stated
inequality `||Z(c)||_F<=||c||_1` is valid, though conservative.

Each upper-triangular coordinate appears once on a diagonal or twice
off the diagonal, and each generator product expands into at most
`2^w` distinct monomials. These facts justify both rounding-error
estimates. Their sum is bounded by `2^(w+2)Vh`; equation (13) makes this
at most `eta/2`. The spectral norm of each block perturbation is bounded
by its Frobenius norm, which is bounded by the aggregate Frobenius norm.
The positive definite margin in equation (3) therefore follows.

The initial version claimed that all corrected denominators divide
`lcm(2^(B+1), input denominators)`. This can fail when an off-diagonal
pivot halves an input coefficient whose denominator has more factors of
two than the rounding grid. For example, with `B=8`, correcting a linear
coefficient `2^(-100)` at an off-diagonal pivot can produce `2^(-101)`.
The old common multiple has only `2^100` as its two-power component.
This situation is compatible with the theorem's assumptions: for one
variable, `r=1`, `tau=1`, `f=2^(-100)x`, and `gamma=-2`, the slack
promise and the specified choice `B=8` both hold.

The revised bound is correct. If
`L=lcm(2^B, input coefficient denominators)`, both `Q0` and the coefficient
residual have denominators dividing `L`. Applying `Z` introduces at
most one additional factor of two, so `2L` clears every corrected
entry. Its encoding length is at most a constant plus `B` and the sum
of the input denominator lengths. This correction does not alter the
polynomial bound.

## 5. Exact feasibility construction

The `M` pivot columns establish full row rank of the coefficient map.
After the remaining `k=V-M` coordinates are assigned, the pivot
coordinates are uniquely determined. Equation (14) is therefore a
bijective affine parameterization of the coefficient-equality space,
not merely a sufficient family of feasible identities.

A free-coordinate insertion has Frobenius norm at most two. Its
coefficient correction has norm at most `2^(w+1)`. Summing columns and
using `||z||_1<=sqrt(k)||z||_2<=V||z||_2` establishes the deliberately
loose Lipschitz constant `beta=2^(w+2)V`.

For `||z||_2<=a`, the matrix perturbation from `Q(y*)` has block
spectral norm at most `eta/2`. Also `a<=1` and every coordinate of
`y*` has magnitude less than `R`. Thus the stated full-dimensional
ball is inside both the PSD restrictions and the box. The outer
Euclidean radius `k(R+1)` is valid for `k>=1`. The zero-dimensional
case is separately handled. The revised one-dimensional case correctly
uses rational interval bisection.

Exact rational PSD separation is also valid. A negative diagonal is
already a negative quadratic witness. A positive diagonal permits a
Schur-complement reduction. If no positive or negative diagonal remains,
a nonzero off-diagonal entry admits one of `e_i+e_j` and `e_i-e_j` as
a negative witness. Back substitution gives a witness for the original
matrix. The rational entries involved can be expressed through minors
and linear systems, giving polynomial bit length when rational
arithmetic is reduced in the standard way.

Every such quadratic witness defines an affine cut valid for the whole
feasible body and strictly violated by the query. Under the promise
that the body is nonempty, this cut cannot have zero free-coordinate
normal. If it did, its constant negative value would contradict the
promised feasible point. An implementation outside the promise can
terminate immediately when that situation occurs.

The unknown location of the inner ball is not a circular initialization
assumption. Its positive volume suffices: a sequence of valid separating
cuts and enclosing ellipsoids cannot continue until the ellipsoid volume
is smaller than that ball's volume. Standard rounded rational ellipsoid
updates provide polynomial-size queries. The source note now states
this arithmetic requirement explicitly and supplies inner and outer
radii of polynomial encoding length. It invokes an established
algorithm rather than implementing or reproving its rounding analysis.

The use of de Klerk--Vallentin's theorem was checked separately. Its
Theorem 1.1 explicitly supplies a known rational feasible point as part
of its assumptions, so it cannot by itself construct the first point
here. The note correctly avoids that circular application.

The optional conversion of rational weighted squares to unweighted
rational squares is correct. For a positive weight `a/b`, express the
integer `ab` in binary. An even power of two is one integer square;
an odd power is two equal integer squares. Division by `b^2` then gives
at most twice the bit length of `ab` rational squares. No integer
factorization algorithm or four-square algorithm is required.

## 6. Conditional extension to the ordinary box module

The source author proposed restricting the construction to empty and
singleton generator sets. This extension was independently checked after
the main review. It is correct under the sufficient hypothesis that
`p-tau` already has a real certificate in the restricted ordinary sparse
module.

For an empty generator set, the complement identity uses only singleton
generator terms. For `I={i}`, its second sum is the single square
`(x^alpha x_i)^2` in the empty-generator block, while its first sum again
uses singleton blocks. The restricted collection is therefore closed
under every term used to construct `H`. Averaging only the restricted
source positions gives `H>=I/D` and the same trace bound, with `D`
recomputed for those positions. The moment argument, empty-generator
right inverse, rational correction, and affine feasibility reduction all
remain valid, with the restricted dimensions.

The written corollary permits `r>=1` without `r>=w`, which is valid.
The algebra and separation arguments never require `w<=r`. The moment
encoding bound is still polynomial because `r+1<=S` for a nonempty bag
and `w` is bounded by the bag-list input length (and by the restricted
expanded dimensions). Even retaining the conservative factor `2^w` in
the Lipschitz bound contributes only `O(w)` to its encoding length and
to the logarithmic ellipsoid bound; in this restricted module each
coefficient column actually has at most two nonzero entries.

This conditional rationalization extension supplies no quantitative
ordinary-module convergence rate. In particular, the full-preordering
kernel theorem cannot simply be substituted for its stronger restricted
certificate hypothesis. The scope must remain explicit.

## 7. Prior results examined

The review examined these primary sources and distinguished their
assumptions from the note's particular box estimates:

- [Peyrl--Parrilo (2008)](https://www.mit.edu/~parrilo/pubs/files/PeyrlParrilo-ComputingSumOfSquaresDecompositionsWithRationalCoefficients.pdf),
  especially the strict-feasibility rounding and projection result
  identified as Proposition 8. This already provides the broad
  approximate-Gram-to-exact-rational-Gram strategy.
- [Davis--Papp (2024)](https://arxiv.org/abs/2305.19039), with the local
  [full text](../../literature/papers/davis2024-rational-dual-certificates-for-weighted/fulltext.md):
  Proposition 1.1 describes the coefficient-map framework, Theorem 2.9
  bounds integer dual-certificate size using cone and interior-distance
  parameters, and Section 4 supplies rational certificate algorithms
  with an initialization procedure. Section 5 explicitly discusses
  correlative and term sparsity. Sparse structure alone is therefore
  not a new rational-certification claim.
- [de Klerk--Vallentin (2016)](https://arxiv.org/pdf/1507.03549),
  Theorem 1.1 and the rational linear-algebra discussion. Its supplied
  feasible-point assumption differs from the feasibility problem solved
  in Section 5 of the note.
- [Grötschel--Lovász--Schrijver, *Geometric Methods in Combinatorial
  Optimization*](https://ir.cwi.nl/pub/10155/10155D.pdf), Section 1:
  the convex-body framework uses a known enclosing radius and a known
  radius of an inscribed ball; knowing the ball's center is a separate
  assumption needed for some reductions. This supports the distinction
  used by the note. The full rounded-ellipsoid machinery remains a
  cited standard result, not a newly established component here.
- The [revised Magron--Safey El Din report](https://arxiv.org/abs/1811.10062)
  was located. Davis--Papp's introduction expressly records corrections
  to earlier general complexity claims. This review did not reverify
  that report's complexity proof, and does not rely on it for the theorem.

The revised literature paragraph is appropriately conservative. Its
specific addition is the explicit route from this sparse kernel error
bound to rational Gram certificates, including a constant interior
certificate, rational moment bounds, and a global coefficient right
inverse. The review establishes no independent priority claim for any
of those ingredients or their combination.

## 8. Targeted exact checks and their limits

The independently written checker is
[check_rational_certificates_review.py](check_rational_certificates_review.py).
The command actually run was:

```text
python research-20260928/solver/check_rational_certificates_review.py
```

It returned:

```text
PASS: 295 diagonal identities; 14 exact moment bounds; 2 overlapping-bag round/correct certificates; denominator regression; 238 ordinary-module identities.
```

The checks use exact rational arithmetic. They enumerate all source
diagonal identities for widths one through three and orders from the
width through four, including term admissibility, the baseline diagonal
contribution, and the aggregate trace bound. They check denominator
clearing and positive definiteness of `W-lambda0 I` for fourteen local
moment blocks. For overlapping bags `{0,1}` and `{1,2}` at orders two
and three, they build the global coefficient columns and pivot map,
round explicit strict Gram certificates, repair every global coefficient,
and verify the claimed remaining matrix margin by exact positive LDL
pivots. They also reproduce the initial denominator failure and confirm
the corrected common multiple.

After the conditional ordinary-module extension was proposed, the same
targeted command was rerun with an added restricted-block check. It
verifies 238 further diagonal identities, closure within the empty and
singleton blocks, baseline positivity of every restricted diagonal, and
the restricted aggregate trace bound. The displayed output is from that
second run.

These finite checks can reveal indexing, overlap, parity, coefficient,
or denominator mistakes. They do not prove the identities for arbitrary
orders, verify general polynomial bit growth, implement the ellipsoid
algorithm, or assess practical numerical performance. No Lean
formalization, project-wide verification, or CI inspection was used.
