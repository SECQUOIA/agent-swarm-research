# Exponential scalar messages with a unique, well-conditioned optimum

Date: 2026-10-02. Status: the unit-box result and its companion passed a
[fresh independent review](../reviews/unique-message-growth-obstruction-review.md)
and targeted exact checks. No external literature search or originality claim
is made.

## What this rules out

The [earlier scalar-message example](scalar-message-growth-obstruction.md)
has exponentially many optima. The following family has a unique optimum,
bag size three, global growth constant `g=1/8`, and negative curvature at
most `1/4`, on a unit box. Nevertheless, its full terminal Bellman message
needs exponentially many quadratic pieces.

Thus uniqueness does not repair full-message enumeration as a route to the
[negative-curvature sparse target](negative-curvature-sparse.md). Negative
inertia grows with the family, so this is not a fixed-negative-inertia case.
Positive curvature grows exponentially, with polynomial binary encoding
length, as the target permits. A companion formulation has bounded full
curvature and expanding boxes. The conversion scales only the state
variables; its preservation of negative-curvature conditioning is proved
below rather than assumed for arbitrary coordinate changes.

This is a representation obstruction, not optimization hardness. The family
has an immediate exact global certificate. It does not rule out the desired
fixed-parameter algorithm, selective messages, or factorized certificates.

## Construction

For `t=1,...,m`, use continuous variables

    z_t in [0,1],       s_t in [0,1],       s_0=0,

and define

    r_t=2^t(s_t-s_(t-1))-z_t,
    F(s,z)=4^m s_m^2+sum_t r_t^2+(1/8)sum_t z_t(1-z_t).

Every term is nonnegative on the box. If `F=0`, the terminal state is zero,
every residual is zero, and the recurrence with nonnegative controls gives
`s=z=0`. Conversely, zero is feasible and has value zero. It is the unique
global optimum.

The bags `{s_(t-1),s_t,z_t}`, omitting fixed `s_0`, form a path
decomposition with bag size at most three. For `m>=2` there is a triangle,
so the treewidth is exactly two. Objective coefficients have `O(m)` bits
each, giving total input encoding length `O(m^2)`. All variable intervals
are `[0,1]`.

## Uniform global growth

Set `S_t=2^t s_t`, so that `S_0=0`,

    r_t=S_t-2S_(t-1)-z_t,
    4^m s_m^2=S_m^2.

The states `S_t` and controls are nonnegative. Nonnegativity of the controls
gives

    S_(t-1)=(S_t-z_t-r_t)/2 <= (S_t+|r_t|)/2.

Iterating backward from the terminal state yields

    S_t <= 2^(-(m-t))S_m
           +sum_(j=t+1)^m 2^(-(j-t))|r_j|.

The vector of terminal coefficients has squared norm at most `4/3`.
The strictly backward convolution has Euclidean operator norm at most
`sum_(j>=1)2^-j=1`, by the triangle inequality for shift operators.
Therefore

    ||S|| <= (2/sqrt(3))S_m+||r||,
    ||S||^2 <= (8/3)S_m^2+2||r||^2.

Also `z_t=S_t-2S_(t-1)-r_t<=S_t+|r_t|`, so

    ||z||^2 <= 2||S||^2+2||r||^2.

Combining the two estimates gives

    ||S||^2+||z||^2
      <= 3||S||^2+2||r||^2
      <= 8S_m^2+8||r||^2
      <= 8F(s,z).

Since `||s||<=||S||`, this proves

    F(s,z)>=(||s||^2+||z||^2)/8.

Thus `g=1/8` is valid independently of `m`. The proof used no upper bound on
the nonnegative states `S`. Consequently the larger transformed intervals
`S_t in [0,2^t]` cause no problem. This is a feasible-domain growth bound,
not a global positive-definiteness claim about the Hessian.

## Curvature and growing negative inertia

Let `R(s,z)=r`, and let `D_z` be the diagonal projector onto the controls.
The Hessian is

    H=2R'R+2*4^m e_(s_m)e_(s_m)'-(1/4)D_z.

Its negative-curvature magnitude is therefore at most `nu=1/4`. Hence
the actual ratio `nu_actual/g` is at most two. Scaling states does not change
the concave control term, while every scaled residual remains a square.
This directly proves the negative-curvature bound in the unit-box
coordinates. No spectral bound is transferred by an unjustified invariance
under rescaling.

A nonterminal state has diagonal curvature `10*4^t`, the terminal state has
diagonal curvature `4^(m+1)`, and each control has diagonal curvature `7/4`.
The exact maximum diagonal is therefore `L=4^(m+1)`. Large positive curvature
is essential to this unit-box construction and has polynomial bit length.

There is an `(m-1)`-dimensional subspace defined by

    r=0,       s_m=0.

Indeed, the controls can be chosen freely subject to the one independent
equation `sum_t 2^-t z_t=0`, and the recurrence then determines the states.
On every nonzero vector in this subspace,

    (s,z)'H(s,z)=-(1/4)||z||^2<0.

Thus the negative inertia is at least `m-1`. These are ambient directions;
they need not be feasible displacements from the boundary optimum zero.

## The full terminal message has exponentially many pieces

Define, on the entire terminal interval,

    M(v)=min{F(s,z): s_m=v, all other variables in their boxes},
    W(v)=M(v)-4^m v^2,       v in [0,1].

Every conditional domain is nonempty and compact. The function `W` is
nonnegative. It is zero precisely when all residuals vanish and every
control is binary. The recurrence then gives

    v=sum_(t=1)^m 2^-t z_t.

Every binary control sequence produces feasible intermediate states and a
distinct terminal dyadic value. Consequently the zero set of `W` is exactly

    {j/2^m : j=0,1,...,2^m-1}.

Compactness ensures that `W` is strictly positive elsewhere. In particular,
it vanishes on no nontrivial interval.

Suppose `M` is represented by `K` interval-restricted quadratic pieces
covering its domain. Subtracting `4^m v^2` gives such a representation of `W`.
Each nondegenerate piece uses a nonzero quadratic, because an identically
zero polynomial would produce a zero interval. It can therefore contain at
most two of the isolated zeros. A singleton piece covers at most one.
Hence

    K >= 2^(m-1).

The same counting applies to a lower envelope of interval-restricted
quadratic pieces: any piece attaining the envelope at a zero must itself
vanish there, and an identically zero piece cannot be valid on a nontrivial
interval. A different allocation of the terminal unary quadratic does not
avoid the obstruction, since it can be subtracted before counting zeros.

## Companion with bounded full curvature and expanding boxes

The same residuals give the alternative formulation

    G(S,z)=S_m^2+sum_t(S_t-2S_(t-1)-z_t)^2
                 +(1/8)sum_t z_t(1-z_t),
    S_t in [0,2^t-1],       z_t in [0,1],       S_0=0.

The preceding growth proof gives `g=1/8` in these coordinates too. The
negative-curvature bound remains `1/4`. Its upper coordinate curvature is
at most `10`: nonterminal states have diagonal `10`, the terminal state
has diagonal `4`, and controls have diagonal `7/4`. If
`R_0=[I-2J,-I]` is the residual matrix with one-step shift `J`, then
`||R_0||^2<=10`; hence its Hessian satisfies

    -I/4 <= H_G <= 22I,       ||H_G||<=22.

All objective coefficients are constants, while the box endpoints have
total encoding length `O(m^2)`. Its terminal message minus `v^2` has the
`2^m` integer zeros `0,...,2^m-1`, giving the same piece-count bound.
This version trades exponentially large positive curvature for exponentially
large state intervals. The unit-box result above is not merely a bijective
rescaling of these particular intervals: it allows the slightly larger
intervals `S_t in [0,2^t]`, which the growth and zero-set proofs also cover.

## Meaning for the open algorithmic target

This example satisfies the unique-optimum premise of the sparse
negative-curvature target, at fixed bag size and fixed negative-curvature
ratio, on a unit box, with growing negative inertia. Its positive curvature
can be exponentially large, precisely as the target permits. The companion
version instead has bounded full curvature and growing boxes. Exponential
message size is in the number of stages, and is superpolynomial in the
`O(m^2)` encoded input size in either formulation.

The lower bound `F>=0` is already visible term by term, and zero attains it.
The complete terminal message contains much more information than needed
to certify this optimum. The target algorithm may exploit that distinction;
this note provides no lower bound for selective representations or exact
convex-part certificates.

## Targeted verification

An inline `python3 - <<'PY' ... PY` calculation using `fractions.Fraction`
passed 800 feasible-point checks of the growth inequality for the expanding-
box companion, with 100 rational points for each `m=1,...,8`. It also
checked all 510 binary message-zero witnesses for these lengths, and 28
explicit negative directions obtained from adjacent control entries `1,-2`,
with the corresponding recurrence states.

A second inline calculation passed 800 exact unit-box growth and scaling
checks, all 510 dyadic zero witnesses through `m=8`, and the eight displayed
maximum diagonal-curvature values. Its negative-direction portion was then
repeated with explicit `Fraction` type assertions, passing all 28 directions.
The repetition removed implicit floating-point division in that portion of
the second harness; the growth, scaling, and zero-witness checks used exact
fractions throughout.

The independent reviewer checked the full proof and ran a separate exact
`Fraction` harness through `m=9`. It passed 900 unit-box growth checks,
1,022 binary terminal witnesses, and 36 negative directions. The linked
review records its command, data, and representation limits; no mathematical
correction was required.

The proof above supplies the general growth, inertia, and message-size
claims. The finite checks do not compute full Bellman messages or measure
solver performance. No project-wide verification, CI inspection, or external
literature search was run.
