# Second review: allocation benchmark degree gap

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed note: `notes/positive-polynomial-allocation-degree-gap.md`.
Verdict: **PASS** for the benchmark obstruction and its matching order.

This review checks the finite mathematical example and its scope. It does
not establish publication priority or a lower bound on algorithmic overhead
relative to the optimal integer count.

## Benchmark and pairwise separation

The polynomial's coefficient sum is one, its maximum degree is `D=2^M`,
and `epsilon=1/(512M)<1`. Consequently its one-coordinate capped
allocation optimum is exactly `epsilon`, and
`Phi=(1/2)log2 M+9/2`.

For `j<ell`, the chosen points satisfy

```
x_ell-x_j=2^(-j)-2^(-ell)>=2^(-j-1)=1/(2k),
k=2^j>=2.
```

The monomial `x^k` is one of the polynomial's terms. Its second derivative
on the interval is bounded below by its value at `x_j=1-1/k`. The estimate
`k(k-1)>=k^2/2` is valid. Also
`(1-1/k)^(k-2)>1/4`: the exponent `k-1` gives an even smaller quantity,
whose reciprocal is `(1+1/(k-1))^(k-1)<=e<4`.
This includes `k=2`. Thus the stated lower curvature `k^2/8` is safe.

Subtracting the quadratic with that constant curvature gives midpoint gap
at least curvature times interval length squared divided by eight. In
this case the bound is

```
(k^2/8)*(1/(2k))^2/8=1/256.
```

All other monomial Jensen gaps are nonnegative, so the complete polynomial
gap is at least `1/(256M)=2epsilon>epsilon`. Hence any two of these
`M` exact graph points require distinct parity classes in an arbitrary
convex mixed-integer lift. Selecting one exact lift for each point and
applying the pigeonhole principle proves `2^p>=M`, independently of
integer ranges, closure, or continuous lift dimension. The case `M=1`
has no pair to check and gives the valid lower bound zero.

## Finite upper count

The polynomial is continuous and strictly increasing from zero to one.
Thus all `N=512M` equal-height interval knots exist uniquely. On each
cell, both the function and its chord lie between the endpoint heights,
which differ by `epsilon`; convexity places the chord above the function.
Its error is therefore in `[0,epsilon]` throughout the cell.

The band between chord minus `epsilon` and chord contains the exact graph
and admits only absolute errors at most `epsilon`. Include the cell's
input interval constraints in its complete polytope. The finite Hamming
encoding uses `ceil(log2 N)` bits with no extra integers. Assign cells
codes `0,...,N-1`; a single linear inequality on the binary code value
can exclude unused strings. Alternatively, individually excluding them
also gives a finite formulation. Global input and output bounds make
all deactivation constants finite. There is no need for rational knots
or a polynomial coefficient-length bound in this finite statement.

This proves the stated upper count. Since
`ceil(log2(512M))=ceil(log2 M)+9`, both integer minima lie in an interval
of width nine around their common leading term `log2 M`.

## Exact order and interpretation

The inequalities prove the two separate statements

```
p_conv=log2 M+O(1),
p_bin=log2 M+O(1).
```

They do not prove exact equality of the two minima. I requested that the
candidate's chained asymptotic notation be written separately to avoid
suggesting such an equality; the author applied this clarification.
Subtracting the exact benchmark gives

```
p_conv-Phi=(1/2)log2 M+O(1)
          =(1/2)log2 log2 D+O(1).
```

The upper and lower constants are uniform in `M`, so this establishes
the matching order of the benchmark gap, not merely an unbounded
subsequence or a one-sided estimate. It rules out a uniform additive
`O(r)` upper comparison with this coefficient-sum benchmark when degrees
vary, already for `r=1`.

The conclusion does not constrain the excess count of every algorithm
above `p_conv`; a richer benchmark or a construction within constant
additive error of the true optimum is not excluded. The finite upper
proof also makes no rational compactness claim. The exponential relation
between degree and `M` is consistent with a dense polynomial family and
is not used as a polynomial-time hardness reduction. The coexistence of
many powers in one coordinate distinguishes this example from the
pure-power subclass. No unresolved mathematical defect was found.
