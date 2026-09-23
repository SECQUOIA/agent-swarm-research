# Independent audit: positive-polynomial allocation degree gap

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS.** Reviewed [the supporting negative result](positive-polynomial-allocation-degree-gap.md). The example proves a limitation of the coefficient-sum allocation benchmark. It does not prove a lower bound on an algorithm's excess integer count over the true optimum.

For the scalar error interval `[-epsilon,epsilon]`, coefficient sum one gives allocation optimum `epsilon`, since `epsilon=1/(512M)<1`. Thus `Phi=(1/2)log2 M+9/2` is correct.

For each pair `j<ell`, the chosen exponent `k=2^j` is present in the polynomial. The separation of the two rational points is at least `1/(2k)`. The monomial's second derivative is nondecreasing on the interval, including the constant-curvature case `k=2`. At its left endpoint it is at least `k^2/8`: `k(k-1)>=k^2/2` and the remaining power is at least `1/4`. The displayed elementary estimate using `e<4` justifies the latter constant.

Subtracting `(m/2)x^2` from a function with second derivative at least `m` gives a convex function, hence midpoint gap at least `m(b-a)^2/8`. With the stated curvature and separation, the selected monomial gap is at least `1/256`. Multiplying by its coefficient `1/M` and retaining the nonnegative gaps of all other monomials gives a total gap at least `1/(256M)=2epsilon`. Therefore the midpoint of two selected exact graph points violates the permitted error strictly.

Each exact graph point has at least one lift. Choosing one lift for every selected point and applying the midpoint argument shows that their integer vectors occupy distinct parity classes. This proves `p>=ceil(log2 M)` for arbitrary convex mixed-integer lifts, including unbounded integer variables and unrestricted continuous dimension. For `M=1`, the packing consists of one point and gives the valid trivial bound zero.

The upper construction is also valid. Strict increase and continuity provide unique inverse-height knots with image increments exactly `epsilon`. On each interval the convex function and its chord remain between those endpoint heights, and the chord is above the function. Consequently `0<=chord-f<=epsilon`. The band `[chord-epsilon,chord]` contains the exact graph and permits only absolute error at most `epsilon`, not twice `epsilon`.

There are `512M` bounded cell bands. Assigning distinct binary words and excluding unused words gives a finite union formulation with `ceil(log2(512M))=9+ceil(log2 M)` binary variables. Finite Hamming-distance big-M constants exist on global bounded coordinate and output ranges. The knots can be irrational, which the finite real-coefficient statement explicitly allows.

The two integer minima therefore each lie between `ceil(log2 M)` and `9+ceil(log2 M)`. In particular, the benchmark gap satisfies the explicit bounds

```
(1/2)log2 M - 9/2
 <= p_conv-Phi
 <= (1/2)log2 M + 11/2,
```

with the same bounds for `p_bin-Phi`. Since `log2 D=M`, the asserted leading gap `(1/2)log2 log2 D+O(1)` follows. The notation giving both minima as `log2 M+O(1)` is an asymptotic statement, not an assertion that they coincide exactly at every `M`.

An independent Python `Fraction` check verified **66** exact pairwise midpoint inequalities for indices up to twelve, with the selected-power curvature checks through exponent 2048. Every case passed. The complete symbolic argument covers all `M`.

No mathematical correction is needed. The example requires multiple powers on the same coordinate and is consistent with the stronger pure-power theorem. Its degree is exponential in the number of nonzero terms; the note correctly uses it as a finite mathematical obstruction and does not infer a sparse-input complexity reduction or a rational compact upper formulation.
