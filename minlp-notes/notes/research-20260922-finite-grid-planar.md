# Finite-grid transfer for necessary support formulas

Date: 2026-09-22. Status: new proof, independently rederived by the
coordinator; an independent adversarial review found no mathematical gap in
the first-moment theorem or the conditional higher-moment extension. This
note transfers the
[continuous planar bound](research-20260922-higher-dimensional-smoothing.md)
to rational finite-grid noise. It bounds distinct necessary formulas, rather
than the number of connected regions. The argument also gives a simpler
finite-grid bound for the scalar dynamic program.

The transfer uses monotonicity in each penalty coordinate. No quantitative
quantifier elimination, algebraic discriminant estimate, or coefficient
separation bound is needed.

## 1. The elementary transfer theorem

Let `Z` be a nonempty subset of `{0,1}^m`, and let `q_z` be a real polynomial
on a nonempty open parameter domain `T subset R^d`. Quadratic degree and
parameter dimension two are not needed in this section. For a penalty vector
`eta`, put

```
F_z(t;eta)=q_z(t)+eta dot z.
```

Let `U(eta)` count supports that uniquely minimize the family at some point
of `T`. Let `K(eta)` count distinct polynomial formulas that equal the lower
envelope on a nonempty open subset of `T`, identifying globally identical
polynomials. Equivalently, `K` is the number of formulas necessary in the
lower-envelope representation after deleting duplicates and formulas that
only touch the envelope. A necessary formula can occur in several regions
and is counted once.

These formulas still represent the envelope everywhere on `T`: outside the
finite union of zero sets of distinct polynomial differences, its minimizing
formula is unique and belongs to this list. That complement is dense, and
continuity extends the equality to all parameter points.

Let `mu_i` and `nu_i` be probability laws on the real line, and suppose their
discrepancy on half-lines, including either endpoint convention, is at most
`Delta_i`:

```
|mu_i((-infinity,a))-nu_i((-infinity,a))| <= Delta_i,
|mu_i((-infinity,a])-nu_i((-infinity,a])| <= Delta_i.
```

Write `mu` and `nu` for their independent product laws. Suppose `B` bounds
the expected unique-support count under `mu` for every deterministic constant
shift of the original branches:

```
E_mu U_{q+c}(eta) <= B   for all c in R^Z.             (1)
```

**Theorem.** Under these assumptions,

```
E_nu K(eta) <= B + |Z| sum_i Delta_i.                 (2)
```

It is enough that (1) hold for the particular shifts `c_z=delta a_z`, for
a fixed family of distinct numbers `a_z` and every sufficiently small
positive `delta`.

### Unique activity is coordinatewise monotone

Fix a support `z`. Its activity event is

```
A_z = {eta: exists t in T, F_z(t;eta)<F_w(t;eta)
                            for every w!=z}.
```

This is a Borel event: continuity allows the witness `t` to be taken from a
fixed countable dense subset of `T`, so it is a countable union of open
sets in penalty space. Fix every coordinate except `eta_i`. If `z_i=0`,
increasing `eta_i` leaves all same-bit comparisons unchanged and improves
every opposite-bit comparison. The same witness remains valid. Thus the
section of `A_z` is an upward half-line, possibly empty or the whole line.
If `z_i=1`, the section is a downward half-line. Either endpoint convention
is allowed in this argument.

Replace the `m` marginal distributions one at a time. Conditional on the
other coordinates, the change in the probability of `A_z` is at most
`Delta_i` at replacement `i`. Independence permits integration against the
unchanged product law for the other coordinates. Telescoping and summing
over supports give

```
|E_nu U(eta)-E_mu U(eta)| <= |Z| sum_i Delta_i.        (3)
```

This step uses only continuous branches, not polynomials. It applies also
after adding any deterministic constants to them.

### Persistent identical formulas

At atomic penalty vectors, several supports can represent the same active
polynomial. Therefore `U` may be zero even when `K` is positive; (3) cannot
be applied directly to `K`.

Choose distinct deterministic numbers `a_z`, for example

```
a_z=sum_(i=1)^m 2^(-i) z_i.
```

Let `U_delta` be the unique-support count for branches `q_z+delta a_z`.
For every fixed `eta`,

```
K(eta) <= liminf_(delta down to 0) U_delta(eta).       (4)
```

To prove this, choose an open activity set for each necessary original
polynomial. A nonzero polynomial cannot vanish on a nonempty open set.
Consequently one can choose a point in that activity set outside the zero
sets of the differences from every distinct original polynomial. At this
point the selected formula is strictly below every different formula.
Within its class of identical formulas, choose the support with smallest
`a_z`. That support becomes the unique winner at the selected point after
every sufficiently small positive `delta` shift. There are finitely many
necessary original formulas, and their chosen supports are distinct. This
proves (4).

Fatou's lemma, (3) for the shifted branches, and (1) now give

```
E_nu K <= liminf_(k to infinity) E_nu U_(1/k)
         <= B+|Z| sum_i Delta_i.
```

The infinitesimal shifts are a proof device. The sampled instance remains
exactly the original finite-grid instance. No additional infinitesimals
must be represented or compared by an implementation.

For general continuous branches, (4) still applies if `K` is defined using
strict witnesses against every distinct global function. To infer that
these functions give a complete lower-envelope representation, an extra
condition is needed: for example, every difference is either globally
constant or has no constant value on a nonempty open subset. Polynomial
families satisfy this condition. Arbitrary continuous families can have
local coincidence sets with interior, so the polynomial interpretation
must not be transferred to them without qualification.

## 2. Uniform rational grid and the planar theorem

Let `mu_i` be uniform on `[-sigma,sigma]`, where `sigma>0`, and let `nu_i`
be uniform on the `N>=2` equally spaced points

```
-sigma + 2sigma k/(N-1),    k=0,...,N-1.
```

Then `Delta_i<=1/N`. After rescaling to `[0,1]`, a grid distribution function
is constant between adjacent values `k/(N-1)`. Its maximum discrepancy from
the identity occurs at an endpoint of one of these intervals and is at
most `1/N`. This also checks the open-half-line convention at atoms. Thus

```
E_grid K <= B + m |Z|/N <= B+m 2^m/N.                (5)
```

Now suppose the quadratic family satisfies the assumptions of the
[planar theorem](research-20260922-higher-dimensional-smoothing.md): after
subtracting one common quadratic, every branch is concave and has gradient
norm at most `L` on `[-M,M]^2`. Write `P=8M`, `A=4M^2`, and
`phi=1/(2sigma)`. Constant branch shifts preserve all these assumptions.
The continuous theorem bounds unique activity by connected region count,
so (1) holds with

```
B = 1+(1+1/pi)m phi L P
      +96 binom(m,2) phi^2 L^2 A.
```

We obtain the explicit finite-grid result

```
E_grid K <= 1+(1+1/pi)m phi L P
              +96 binom(m,2) phi^2 L^2 A
              +m 2^m/N.                             (6)
```

For any tolerance `tau>0`, choose the smallest power of two
`N>=max(2,m 2^m/tau)`.
Then the additive transfer error is at most `tau`, and exact uniform
sampling uses

```
log_2 N = O(m+log(m+1)+log_+(1/tau))
```

random bits per penalty coordinate. For rational `sigma`, a sampled penalty
has bit length polynomial in the bit length of `sigma` and `log N`.
For `m=0`, the single support is handled directly without random bits.

This proves polynomial expected exact representation size using
polynomial-bit rational perturbations. It does not construct the necessary
formulas in polynomial expected time, and it does not give an expected
region bound for the grid model. Multiple disconnected regions of one
formula are deliberately identified.

## 3. Consequence for scalar messages

On an interval of length `T`, the reviewed scalar continuous theorem gives

```
E U <= 1+2m phi L T
```

for `L`-Lipschitz branches with independent bounded-density coordinate
penalties. Deterministic constant shifts preserve the bound. For polynomial
branches, (5) therefore gives

```
E_grid K <= 1+2m phi L T+m 2^m/N.                    (7)
```

This improves the atomic correction `4m 2^m/N` in the existing
[scalar finite-grid argument](research-20260922-finite-grid-smoothing.md)
when the quantity needed is distinct retained formulas. It does not assert
the same improvement for the number of intervals in a piecewise
representation. A lower envelope of `K` full univariate quadratics has at
most `2K-1` intervals after adjacent identical formulas are merged. Thus
the distinct-formula bound is sufficient for algorithms that store one
copy of each full quadratic and use its envelope intervals separately.

The transfer theorem is independent of parameter dimension and polynomial
degree. Any future continuous-noise bound for distinct active polynomial
formulas that is uniform under constant branch shifts will automatically
have a finite-grid counterpart of the form (5).

## 4. Conditional transfer of higher moments

There is a useful extension if a continuous-noise higher-moment bound later
becomes available. For a fixed positive integer `p`, assume

```
E_mu U_(q+c)^p <= B_p
```

uniformly under the required constant shifts. Then

```
E_nu K^p <= B_p+2 |Z|^p sum_i Delta_i.               (8)
```

Indeed expand `U^p` as a sum over ordered `p`-tuples of supports, allowing
repetitions. Each summand is the indicator of their simultaneous activity.
On a coordinate line this is an intersection of upward and downward
half-lines, hence an interval with arbitrary endpoint conventions,
possibly empty or unbounded. Interval discrepancy is at most `2Delta_i`.
The same product replacement argument proves the comparison for `U^p`.
Apply the deterministic tie-breaking limit and Fatou to obtain (8).

For the uniform grid, its additive error is at most `2m 2^(mp)/N`, so fixed
moments need `O(pm+log(m+1))` random bits per coordinate for constant error.
The sharper first-moment estimate (5) uses one-sided sections. This argument
does not establish a continuous higher-moment bound; in particular, it
does not turn the planar first-moment result into such a bound.

## 5. Sources, verification, and limits

The half-line discrepancy argument is the elementary one-dimensional
bounded-variation quadrature estimate, followed by product replacement.
The proof is included, so no quantitative geometric integration theorem
is assumed. Monotonicity of a fixed support's optimality under a favorable
change in its own bit penalty is also elementary.

Finite-precision perturbation and rounding arguments are established in
smoothed analysis. In particular, the existing
[priority audit](review-20260922-smoothed-dp-priority.md) records the
finite-precision treatment in Roeglin and Teng's 2009 paper, Section 6.2.
This note does not claim to introduce finite-precision smoothed analysis.
The candidate contribution is the direct transfer of an entire parametric
activity-count bound through binary-coordinate monotonicity, including
persistent duplicate formulas.

Additional searches on 2026-09-22 examined finite-precision isolation,
discrete perturbations, and monotone quadrature terminology. The primary
[Beier and Voecking paper](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/BeierV.pdf)
is an antecedent for coordinate conditioning in smoothed binary
optimization. These searches have not established priority for the exact
activity-count transfer statement. Novelty remains provisional.

The coordinator independently rederived the monotone-section argument and
the deterministic tie-breaking passage. A fresh
[independent review](review-20260922-monotone-grid-transfer.md) found no
mathematical gap in either transfer theorem and reported 65,790 exact grid
distribution-function endpoint comparisons. These calculations check the
one-dimensional discrepancy constant, not the activity or limiting proof.
No Lean proof was attempted. The deduction depends on the continuous planar
theorem and does not independently verify that theorem's geometric proof.
A targeted Python check of this note's local Markdown links and trailing
whitespace passed. No project-wide checks were run.
