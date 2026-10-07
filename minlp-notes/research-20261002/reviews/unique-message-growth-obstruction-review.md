# Independent review of the unique-optimum scalar-message obstruction

Date: 2026-10-02. Reviewed the unit-box revision of
[the construction](../new-direction/unique-message-growth-obstruction.md),
including its expanding-box companion. This is a mathematical review, not
an external literature audit or a claim of originality.

The claims are sound as written. No mathematical correction is required.
The result is a lower bound for complete interval-quadratic message
representations, not optimization hardness or a lower bound for selective
certificates.

## Construction, uniqueness, and graph

The unit-box objective is

```
F(s,z)=4^m s_m^2+sum_(t=1)^m [2^t(s_t-s_(t-1))-z_t]^2
       +(1/8)sum_(t=1)^m z_t(1-z_t),
s_0=0,       s,z in [0,1]^m.
```

Every summand is nonnegative. Zero residuals imply
`s_t=sum_(j<=t)2^(-j)z_j`. With nonnegative controls, a zero terminal
state forces every control and state to vanish. Thus the origin is the
unique global optimizer. Each recurrence factor has the claimed bag
`{s_(t-1),s_t,z_t}`; adjacent bags intersect in a single state and satisfy
the running-intersection condition. For `m>=2`, every later recurrence
square gives a triangle with three nonzero cross coefficients, none of
which cancels with another factor. The interaction treewidth is exactly
two. There are `O(m)` nonzero coefficients with at most `O(m)` bits each,
so the input length is `O(m^2)`.

## Point growth survives the state scaling

Set `S_t=2^t s_t`. The residual becomes
`r_t=S_t-2S_(t-1)-z_t`. Since all `S,z` are nonnegative,

```
S_(t-1) <= (S_t+|r_t|)/2,
z_t <= S_t+|r_t|.
```

Backward iteration gives the displayed geometric convolution. Its
terminal coefficient vector has squared norm at most `4/3`, and its
strictly backward convolution operator has norm at most one. Hence

```
||S||^2 <= (8/3)S_m^2+2||r||^2,
||z||^2 <= 2||S||^2+2||r||^2,
||S||^2+||z||^2 <= 8(S_m^2+||r||^2).
```

The endpoint penalties are nonnegative, and `||s||<=||S||`, so
`F(s,z)>=(||s||^2+||z||^2)/8`. No upper bound on `S` was used. In
particular, the unit-box formulation's transformed domains
`[0,2^t]` need not equal the companion's `[0,2^t-1]`: both are covered
by the proof. This addresses the potentially delicate change of domain
when scaling the original construction.

## Curvature and negative inertia

The full Hessian is a sum of positive semidefinite square Hessians minus
`(1/4)D_z`. Consequently its smallest eigenvalue is at least `-1/4`,
independently of the large state coefficients. The argument is in the
actual unit-box coordinates; it does not assume that spectral curvature
is invariant under diagonal scaling. Together with `g=1/8`, it gives
`nu_actual/g<=2`.

Direct coefficient expansion gives state diagonals `10*4^t` for
`t<m`, terminal diagonal `4^(m+1)`, and control diagonals `7/4`. The
largest diagonal is indeed `4^(m+1)`, including `m=1`.

The simultaneous equations `r=0,s_m=0` impose one independent linear
condition `sum_t 2^(-t)z_t=0` on the controls; the states are then uniquely
determined. This subspace has dimension `m-1`. A nonzero vector in it
has nonzero control component and Hessian value `-||z||^2/4<0`.
The negative inertia is therefore at least `m-1`. These ambient
directions need not lie in the feasible tangent cone at the origin, so
there is no conflict with the point-growth bound on the box.

For the expanding-box companion, `||[I-2J,-I]||^2<=10` proves the stated
Hessian bounds `-I/4<=H_G<=22I`. Its diagonal and encoding bounds are
also correct. It has the same growth proof and unique optimum.

## Message representation lower bound

For every terminal value `v in [0,1]`, the conditional box is nonempty
and compact, so its minimum is attained. Removing the constant terminal
cost on that slice gives

```
W(v)=M(v)-4^m v^2
    =min_(s_m=v) [sum_t r_t^2+(1/8)sum_t z_t(1-z_t)].
```

It is nonnegative. Attainment ensures that `W(v)=0` holds if and only
if every residual is zero and every control is binary. Each binary
control sequence gives feasible intermediate states and a distinct value
`sum_t 2^(-t)z_t`. Thus its zero set is exactly
`{j/2^m:0<=j<2^m}`. The endpoint `v=1` is not in this set and has strictly
positive `W`; the larger full terminal domain introduces no extra zero.

Subtracting the same terminal quadratic from every piece preserves the
number and intervals of a finite quadratic-piece representation. Each
nonzero polynomial of degree at most two has at most two roots. An
identically zero polynomial cannot represent `W` on a nondegenerate
interval, since its zeros are isolated. A singleton piece covers at most
one zero. Therefore a covering representation needs at least
`2^(m-1)` pieces.

For a finite lower envelope of interval-restricted quadratic pieces, a
piece active at a zero must itself vanish there. Every piece is at least
the envelope on its validity interval. Hence an identically zero piece
on a nondegenerate interval would force `W=0` on that interval, again
impossible. The same root count applies. This argument concerns pieces
with interval validity domains; it does not rule out representations
that encode exponentially many separated validity points implicitly.
It also does not rule out representations retaining latent variables.

The companion has the corresponding integer zero set and the same
count. Since the explicit family has input length `O(m^2)`, exponential
piece count in `m` is superpolynomial in its encoding length.

## Targeted verification and limits

Targeted reads used `cat` on the source note and `head -35` to check
that its unit-box revision had landed. One independent inline command
ran as `python3 - <<'PY'`, using `fractions.Fraction`,
`itertools.product`, and `Random(26100227)`; the script was not saved.
It exited successfully with:

```
PASS: 900 unit-box growth checks, 1022 binary terminal witnesses,
36 negative directions
```

For each `m=1,...,9`, it sampled 100 unit-box points with coordinates
in `{0,1/32,...,1}` and checked both the growth inequality in `S,z`
and its transfer to `s,z`, along with equality of the scaled residual
formulas. It checked every binary control sequence for these lengths,
verified all intermediate state bounds and residual equations, and
compared the resulting terminal set with the complete dyadic set.
Finally, adjacent control pairs `(1,-2)` generated 36 explicit
residual-null, terminal-zero directions with negative quadratic value.

These independent checks support the formulas; the algebra proves the
claims for arbitrary length. No full Bellman message was constructed,
and no solver-performance claim was tested. No external literature
search, project-wide verification, or CI inspection was performed.
