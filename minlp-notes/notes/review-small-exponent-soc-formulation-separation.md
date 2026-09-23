# Independent review: conic versus rational MILP small-exponent encoding

Date: 2026-09-05. Verdict: **PASS** for
[the candidate proof](small-exponent-soc-formulation-separation.md).
No mathematical correction is required. This review verifies the construction
and its dependence on the separately stated rational MILP lower bound; it
does not establish literature priority.

## Fixed optimal values multiplied by nonnegative variables

For positive `theta`, division of both the primal and dual witnesses by
`theta` gives feasible points of the original programs. Their objective
values sandwich the common optimum. The equality of the two unscaled
objective values therefore forces each to equal `theta*v`. Conversely,
scaling an attained optimal pair supplies a witness. This uses only products
of a variable with fixed input coefficients; the cone constraints are
homogeneous and introduce no hidden variable products.

At `theta=0`, an original feasible dual gives
`c^Tz=(A^Tu0+s0)^Tz=s0^Tz>=0`. An original feasible primal gives
`b^Tu=z0^TA^Tu=-z0^Ts<=0`. Equality forces zero. The zero witness is feasible.
Thus the potentially unbounded homogeneous fibers at zero do not introduce
extra projected values. No compactness of the primal or dual feasible sets
is required.

## Repeated squaring: an explicit standard form and dual certificate

The repeated-squaring optimum is attained at `z_i=a^(2^i)`. Nonnegativity
of successive coordinates makes induction through the square inequalities
valid. A convenient strict feasible point is

```
z_i=a+i(1-a)/(B+1),   i=0,...,B.
```

All coordinates belong to `(0,1)` and increase strictly, so every cone
inequality is strict. This point has polynomial bit length. The usual
Slater argument therefore applies, but an explicit optimal dual also makes
the claimed dual attainment independently checkable.

Use one rotated cone variable `q_i=(r_i,h_i,w_i)` per square, with
`2r_i h_i>=w_i^2`, `r_i,h_i>=0`. Impose

```
h_i=1/2;   w_1=a;   w_i-r_(i-1)=0 for i>=2,
```

and minimize `r_B`. This is precisely conic standard form, with `3B`
cone coordinates and `2B` equations. Its nonzero matrix coefficients are
`+/-1`; its right-hand side uses only `1/2` and `a`. Rotated cones are
self-dual in these coordinates.

At the optimal primal point `q_i=(z_i,1/2,z_(i-1))`, define positive numbers

```
lambda_B=1,
lambda_i=2 z_i lambda_(i+1) for i<B.
```

Give the equation `h_i=1/2` multiplier
`alpha_i=-2z_i lambda_i`, and the equation containing `w_i` multiplier
`beta_i=2z_(i-1)lambda_i`. The conic dual slack is then

```
s_i=(lambda_i, 2z_i lambda_i, -2z_(i-1)lambda_i).
```

The first-coordinate stationarity equation is `lambda_i=beta_(i+1)`
for `i<B`, and `lambda_B=1` at the last coordinate. The other two
stationarity equations hold by their definitions. Every slack belongs
to the rotated cone because `z_i=z_(i-1)^2`, and `q_i^Ts_i=0`.
The feasible primal and dual thus have equal objective values. This proves
both dual attainment and zero gap directly, without importing a general
strong-duality theorem for this particular program. These witness values
can have large explicit encodings; they are variables, not formulation
coefficients, so this does not affect the formulation-size bound.

## Selection, graph coverage, and encoding

Four integral bits specify one of the sixteen codes. Every selector with
a different code is bounded by a false literal and must vanish; the sum
constraint makes the matching selector one. The bounded interpolation
variables vanish on every inactive segment. Their associated conic-value
weights are nonnegative, so the exact projection lemma applies even to
zero inactive weights.

The selected segment has input endpoints `(j/16)^D` and `((j+1)/16)^D`.
Its chord height lies below the concave root function. Monotonicity places
the function below `(j+1)/16`, which is at most one sixteenth above the
chord height. Hence the allowed output interval contains the exact graph
and has width one sixteenth, proving both inclusions in the required tube.
The endpoint constants zero and one are handled directly. No long rational
knot coefficient appears in the actual conic constraints.

There are a constant number of conic-value gadgets. Their dual standard
forms add only a constant factor to row and variable counts. The structured
cone list uses `O(B)` constant-size coefficients; an ordinary sparse
encoding additionally records indices of `O(log(B+2))` bits. The resulting
size is `O(B log(B+2))` bits, which is polynomial in the binary length of
`D=2^B`. The rational MILP lower bound applies to this same tube definition
and allows arbitrarily many integer variables, so the advertised encoding
separation follows. It is not an assertion that exact conic optimization
has polynomial-size rational output or polynomial running time.

## Independent exact checks

[The independent checker](../code/small_exponent_soc/check_first_review.py)
passed 105 exact rational primal/dual/Slater certificate cases, covering
`B=1,...,7` and all interior knots `a=j/16`. It checks every cone membership,
stationarity equation, complementarity equality, common value, and selected
homogeneous scaling, including zero. It also checks all sixteen binary
selector codes. The calculations use exact fractions and no numerical
optimization solver. They support, but do not replace, the general proof.
