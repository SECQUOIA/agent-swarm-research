# Independent review: small-exponent rational formulation barrier

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed candidate: `notes/small-exponent-rational-formulation-barrier.md`.
Verdict: **PASS for the final tight `Theta(D)` encoding theorem, including
the upper bound with four binary variables**.

The first audit strengthened the original `s=Omega(sqrt(D))` conclusion.
Counting the total explicit coefficient encoding, rather than multiplying
a global coefficient bound by the basis dimension, gives

```
s=Omega(D).
```

The candidate now incorporates this stronger proof and a matching upper
bound. Both are independently checked below. The lower bound tolerates
arbitrarily large integer witnesses. This review makes no priority claim
for the classical rational LP determinant argument or this application.

## Freezing an integer witness is legitimate

Exact graph containment supplies a lift of `(2^(-D),1/2)`. Fix its finite
integer vector `z*`; no bound on its magnitude is needed. The remaining
system in continuous variables is a rational polyhedron. Adding `y>=1/4`
keeps that graph point feasible.

Its minimum input coordinate is finite because all projected inputs are
nonnegative. A finite optimum of a linear function over a nonempty
polyhedron is attained. This can also be seen by projecting that
polyhedron onto the objective coordinate: a linear projection of a
polyhedron is a polyhedron, so a finite endpoint of its range is included.

The attained value cannot be zero, because at `x=0` the graph-tube
condition forces `|y|<=1/16`, contradicting the added lower bound on
`y`. Therefore

```
0<v<=2^(-D).
```

Neither the selected graph coordinate nor the integer witness is inserted
as a coefficient into the original formulation. Only the constant-size
inequality on `y` is added. If a formulation's domain restrictions were
implicit only on the unit box, adding `0<=x<=1` would also cost constant
encoding and would make the same argument applicable.

## Optimal basic solutions exist after standard-form conversion

Split unrestricted continuous variables into differences of nonnegative
variables and add slack variables for inequalities. Remove dependent
equations when needed. The resulting nonnegative standard-form polyhedron
is pointed, so its nonempty optimum face has a basic feasible solution.
The existence of a vertex in the original lifted polyhedron is not needed.

For a direct argument, choose an optimal standard-form point whose positive
support has minimum cardinality. If its corresponding matrix columns were
dependent, a nonzero null direction supported there would allow small
feasible steps of both signs. Optimality forces zero objective derivative
along that direction. Moving until one positive coordinate vanishes then
preserves the optimum and reduces its support, a contradiction. Thus the
positive columns are independent, and extending them to a full row-rank
basis gives an optimal basic feasible solution.

After rational denominators are cleared, the frozen right-hand side is
integral. Cramer's rule gives every basic coordinate a denominator dividing
the nonzero integral basis determinant. The objective coordinate `x`, even
if represented as the difference of two standard-form coordinates, has the
same denominator bound. Cancellation or an enormous integer right-hand
side can alter the numerator, but cannot increase this denominator.

These observations justify the candidate's coarse `2^{O(s^2)}` determinant
estimate and its original conclusion already. The following accounting
improves the estimate.

## Rowwise clearing gives a determinant bound exponential in total size

Consider the original rational rows together with the constant-size added
inequality. For row `i`, let `ell_i` bound the sum of the binary lengths
of all its rational numerators and positive denominators. Include its
integer-variable coefficients and original right-hand-side constant in
this budget. Under the ordinary explicit encoding,

```
sum_i ell_i=O(s+1).
```

Clear denominators **separately in each row**, using their product `Q_i`.
Every resulting matrix entry in a continuous-variable column has absolute
value at most `2^{O(ell_i)}`. For example, an entry with numerator `p`
and denominator `q` becomes `p Q_i/q`; its logarithmic magnitude is
bounded by that numerator length plus the sum of the row's denominator
lengths. The original integer columns are also integral after this
clearing, so fixing `z*` gives an integral right-hand side without changing
these continuous-variable coefficients.

Let `t_i` be the number of original nonzero continuous coefficients in
row `i`. Splitting free variables at most doubles that number, and adding
a slack contributes at most one unit entry. Therefore the standard-form
row norm is at most

```
sqrt(2t_i+1) 2^{O(ell_i)}.
```

Rows that are removed need not be included in the bound. Restricting the
remaining rows to any basis columns can only decrease their Euclidean
norms. Hadamard's inequality consequently yields

```
log2 |det basis|
 <=O(sum_i ell_i)+(1/2)sum_i log2(2t_i+1)
 =O(s+1).
```

For the final equality, the number of explicitly stored nonzero entries
is `O(s)`, and `log2(2t+1)<=2t` for integral `t>=1` (with zero contribution
at `t=0`). This works for both ordinary dense and ordinary sparse rational
matrix encodings. Index and dimension fields only add to the input length.

Hence every such basis determinant is at most `2^{C(s+1)}` for a universal
constant depending only on the fixed encoding convention. The optimum is
a positive integer numerator divided by such a determinant, and therefore

```
v>=2^(-C(s+1)).
```

Combining this with `v<=2^(-D)` gives `D<=C(s+1)`, or `s=Omega(D)`.
For `D=2^B`, the formulation length is consequently `Omega(2^B)`.
No restriction on the number, signs, or magnitudes of its integer variables
was used beyond their finiteness in an explicit formulation.

## Matching rational upper bound and the four declared binaries

The final candidate adds 17 rational knots `a_j=(j/16)^D`, for
`j=0,...,16`. They are strictly increasing from zero to one. On segment
`j`, the equations

```
x=(1-theta)a_j+theta a_(j+1),
t=(j+theta)/16,       0<=theta<=1
```

trace the chord of the concave function `x^(1/D)`. Concavity gives
`t<=f_D(x)`, and monotonicity gives
`f_D(x)<=(j+1)/16<=t+1/16`. Thus both the true value and every permitted
value in `t<=y<=t+1/16` belong to an interval of length exactly the
allowed error. This proves exact graph containment and the two-sided
error restriction, including the first segment touching zero. The input
segments cover all of `[0,1]`.

Assign the 16 segments all distinct four-bit strings. The continuous
selectors, their sum-one equation, and upper bounds by the corresponding
bit literals force exactly one selector to equal one when the four bits
are integral. All others equal zero. Consequently `0<=v_j<=lambda_j`
sets every inactive segment variable to zero and leaves precisely the
selected segment parameter in `[0,1]`. The candidate's two aggregate
equations then reproduce that segment's `x` and `t` exactly. There are
no further integer variables or nonlinear products.

The number of rows and variables is constant. Each knot and difference
has numerator and denominator of `O(D)` bits: before reduction they use
`j^D/16^D` or `((j+1)^D-j^D)/16^D` with fixed `j<=16`. Reducing the
fractions cannot increase these lengths. Therefore the total ordinary
rational encoding is `O(D)`. Exact coefficient construction may take
time polynomial in `D`; no polynomial-time construction in `log D`
is implied or required.

The lower and upper bounds together prove optimal total rational encoding
`Theta(D)` at error `1/16`, while four binary variables suffice. The
statement does not claim that four is the minimum binary count.

## Encoding and scope boundaries

The projection is the ordinary coordinate projection onto `(x,y)`. A
rational affine projection can be handled by adding its defining output
equations, provided its coefficients are included in the formulation
encoding; this changes total size only by a constant factor. Arbitrary
unencoded projection maps are outside the assertion.

The size convention must count rational coefficients explicitly by their
integer numerators and denominators. A coefficient presented by a compressed
expression such as `2^(-D)` with only `log D` symbols would use a different
encoding and is not covered. Real coefficients treated as unit-cost entries
are also outside the bound. Unrestricted integer witnesses are covered:
their values are not added to the size budget, and the denominator proof
does not require doing so.

The fixed-integer-slice argument needs ordinary non-strict linear
constraints, as in a rational MILP. It does not apply to nonlinear convex
constraints or to a different approximation requirement that allows the
origin at heights above the separating threshold. The obstruction is to
short rational whole-graph formulations; it is not an integer-count lower
bound by itself. No unresolved mathematical defect was found.
