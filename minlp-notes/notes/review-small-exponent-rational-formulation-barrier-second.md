# Second independent review: small-exponent rational formulation size

Date: 2026-09-05. Reviewer: `potential_flow_review`.

**Verdict: PASS.** I reviewed [the rational formulation barrier](small-exponent-rational-formulation-barrier.md), including the strengthened rowwise determinant bound, and root's matching sixteen-piece construction. The conclusion is a tight `Theta(D)` total rational encoding bound at error `1/16`, despite an upper construction using only four binaries. No novelty clearance is supplied for the classical rational-LP argument or its particular consequence.

The encoding model must be the ordinary explicit rational MILP model: rational linear rows, finite lists of continuous and integer variables, and the bit lengths of coefficients and structural data counted in the formulation size. The proof allows arbitrarily many unrestricted integer coordinates and places no bound on an integer witness's magnitude. It does not concern nonlinear mixed-integer convex constraints or unit-cost arbitrary real coefficients.

## 1. Freezing a witness gives the required positive LP value

Whole-graph containment supplies a feasible lift of `(2^(-D),1/2)`. Fix its entire integer vector. The remaining feasible set is a rational polyhedron, regardless of whether the chosen continuous witness is rational. Adding `y>=1/4` preserves feasibility. Every feasible point of this fixed-integer slice is still an integer-feasible point of the original formulation, so its projection satisfies the graph-tube inclusion.

The objective `x` is bounded below by zero. A nonempty polyhedron with a finite LP optimum attains that optimum. The optimum cannot be zero: a minimizer with `x=0,y>=1/4` would violate the permitted error `1/16`, since the target value at zero is zero. Thus

```
0<v<=2^(-D).
```

There is no appeal to closedness of an infinite union of integer slices. Only one fixed slice is used, and it is polyhedral. In fact its tube condition already implies `x>=(3/16)^D` after imposing `y>=1/4`; this is consistent with, but not needed for, the denominator argument.

## 2. Freezing integers changes only the right-hand side

Clear denominators separately in each original row, including denominators of the integer-column coefficients and right-hand side. If `ell_i` is that row's total coefficient bit length, each cleared continuous coefficient has magnitude at most `2^(ell_i)` up to an immaterial universal encoding convention. This follows by bounding its numerator times the product of all other denominators by the total row bit budget.

After substituting integer values, the right-hand side is integral. Its magnitude may depend arbitrarily on the chosen witness, but the continuous coefficient matrix remains the same cleared integer matrix. This distinction is the central point: no integer-continuous product is present in a MILP, so witness substitution cannot change these continuous coefficients.

The added inequality has constant coefficient size. Under an explicit encoding, its row and variable-reference overhead contributes only `O(s+1)`, which is absorbed in the final universal constant. The total row coefficient budget and total number of nonzero entries are `O(s)`.

## 3. Standard form and basic solutions do not require an original vertex

Split every free continuous variable into its positive and negative parts and add nonnegative slack variables. The resulting feasible set has equality constraints and nonnegative variables. It contains no line, and a finite optimum has an optimal basic feasible solution.

For rank reduction, select a maximal linearly independent **subset of the cleared rows**. This avoids introducing coefficients through row combinations. Feasibility guarantees that discarded dependent rows have consistent right-hand sides, so this subset defines the same equality system. The original polyhedron need not itself have a vertex; the standard-form representation supplies the relevant basic solution.

Splitting doubles a row's continuous nonzero count at most, and its slack adds at most one. Therefore its Euclidean coefficient norm is bounded by

```
sqrt(2*t_i+1)*2^(ell_i).
```

For any basis, removing columns only decreases these row-norm bounds. Hadamard gives

```
log_2 |det B|
 <=sum_i ell_i+(1/2)sum_i log_2(2*t_i+1)
 <=C*s.
```

The second sum is linear in the total nonzero count, for example by `log_2(2t+1)<=2t` for positive integer `t`. This is the reason the result improves on a coarser dimension-times-maximum-height estimate. No factor `s` multiplies the total coefficient budget a second time.

## 4. Numerator cancellation does not defeat the bound

At the chosen basic solution, all basic coordinates have denominators dividing the same nonzero integer determinant. Nonbasic coordinates are zero. The original objective variable `x` is either one coordinate or the difference of its two split coordinates, so it has this same common denominator bound; subtracting them does not multiply denominators.

Its numerator may involve huge fixed integers and may undergo cancellation. Nevertheless, when the resulting objective value is positive, that numerator is a positive integer and is at least one. Hence

```
v>=1/|det B|>=2^(-Cs).
```

Combining with `v<=2^(-D)` proves `s>=D/C`. This reasoning is independent of the number, bounds, signs, or magnitude of the integer coordinates. Rationality and linearity are essential.

If a formulation describes its output through an explicitly encoded rational affine map rather than literal coordinate projection, appending output-defining rows brings it into this setting with encoding overhead proportional to that map's explicit encoding. An uncounted external projection would be a different model and is not covered.

## 5. The matching four-binary upper construction

For `j=0,...,16`, define

```
x_j=(j/16)^D,
t_j=j/16.
```

On piece `j=0,...,15`, let

```
x=(1-theta)*x_j+theta*x_(j+1),
t=(j+theta)/16,
0<=theta<=1.
```

Concavity of `f_D` places its graph above this chord, so `t<=f_D(x)`. Monotonicity gives `f_D(x)<=t_(j+1)<=t+1/16`. Consequently the band

```
t<=y<=t+1/16
```

contains every exact graph value on the piece and admits no point farther than `1/16` from it. The pieces cover `[0,1]` because their exact rational input knots increase from zero to one. Values of `y` slightly above one at the final endpoint are permitted by the stated tube and cause no issue.

An explicit encoding confirms that only four binaries are needed. For each four-bit word `j`, introduce a continuous selector `s_j>=0`, impose `sum_j s_j=1`, and impose `s_j>=1-H_j(b)`, where `H_j` is the Hamming distance of the input bits from word `j`. Integral input bits force the matching selector to one and every other selector to zero. Introduce `0<=lambda_j<=s_j` and define

```
x=sum_j [x_j*s_j+(x_(j+1)-x_j)*lambda_j],
t=sum_j [(j/16)*s_j+lambda_j/16].
```

Together with the band, these are linear equations and inequalities. The selected `lambda_j` acts as its piece's interpolation coordinate. There are no products between variables and no other integer declarations.

There are only sixteen pieces. Each input knot has numerator and denominator lengths `O(D)`, because `j<=16` and the common denominator is `16^D`. Knot differences have the same encoding order. Thus the total rational formulation encoding is `O(D)` with a constant number of rows and variables. Exact integer powering can construct these coefficients in time polynomial in their output length.

This matches the lower bound. Therefore total encoding is `Theta(D)` while four binaries suffice uniformly in `D`. With `D=2^B`, the total bit complexity is exponential in the exponent's binary input length, even though integer dimension stays bounded.

## Scope and conclusion

The result does not contradict compact graph approximations for powers greater than one. Swapping axes of such an approximation changes vertical error into horizontal error; near zero the inverse power can amplify it substantially. The present whole-graph tube requires vertical error bounded in the small-exponent output.

All substantive steps pass: LP attainment, standard-form conversion, an independent original-row subset, shared-denominator accounting, unbounded integer witnesses, and the matching upper construction. The proof establishes the rational encoding barrier under the precise whole-graph inclusion model; the source comparison remains separate.
