# Targeted source contracts to verify

These requests supplement the Luna lead's original brief. They do not
authorize a second concurrent `$lit` session.

1. Exact convex MIQP oracle: confirm the strongest applicable Del Pia
   theorem returns an attained exact optimizer and value over the bounded
   rational mixed polytope, with fixed-parameter dependence on integer
   dimension and an absolute input-size exponent. Distinguish feasibility,
   approximate objective, and exact output.
2. Rational Gaussian-like smoothed laws: search for comparable finite-bit
   noise formulations, and qualify claims that depend on base-selected
   discretization. The manuscript does not cover arbitrary coarse Gaussian
   approximations.
3. Polynomial-time exact separable convex integer flow/TU algorithms:
   verify their dependence on binary capacities, explicit polynomial degree,
   restricted intervals, and supplied cost-oracle contracts. Our uses preserve
   a fixed feasible set; core-dependent feasibility is a different problem.
4. Strong-noise coordinate persistence and random-component/percolation
   optimization: inspect nearest precedents, including spin systems,
   smoothed graphical optimization, and persistency. Distinguish a novel
   composition and bit/output analysis from classical monotonicity and
   connected-set counting.
5. Effective real-algebraic bounds needed for finite rational noise and
   constant-base component solvers: quantify the number of quantifier blocks,
   free variables, coefficient-bit dependence, and common-root output.
# Constant-base box solver: narrow novelty only

The joint critical-limit construction uses pure-power deformation, multiplication
matrices, a moment-curve list of separating forms, and derivatives of a
characteristic polynomial to recover a tuple from one root. Check the nearest
primary rational-univariate-representation and critical-point/deformation
algorithms (including Rouillier and Basu--Pollack--Roy). Do not infer originality
merely from an explicit c_d^k polynomial-input bound: classical Macaulay or
multiplication-matrix methods may already give such a bound for fixed degree
and box domains. The manuscript can use this as a self-contained constructive
interface without claiming a new general algebraic complexity result.
