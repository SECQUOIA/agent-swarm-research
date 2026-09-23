# Independent audit: commuting quadratic covariance reduction

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed note: `notes/commuting-quadratic-covariance-reduction.md`.

**Verdict: PASS.** The diagonal-optimizer reduction, correlated-budget
extension, scalar allocation program, and single-Hessian formula are
correct. No substantive correction is needed. This audit does not
establish novelty or an exact rational simultaneous-diagonalization
algorithm.

Real symmetric pairwise commuting Hessians have a common orthonormal
eigenbasis. In that basis, every coordinate sign flip `S` commutes
with every Hessian. Orthogonal congruence `P -> SPS` preserves the
cap, determinant, and energies. For correlated budgets, it preserves
each cross-trace as well and therefore preserves the full budget.

The geometric-mean step has the claimed fixed symmetry. If
`M=P#Q`, then `M P^(-1) M=Q`; inverting and rearranging gives
`M Q^(-1) M=P`, proving symmetry by uniqueness of the positive
definite solution. The same defining equation proves orthogonal
congruence invariance. Consequently, for `Q=SPS`,

```
S(P#(SPS))S=(SPS)#P=P#(SPS).
```

The midpoint is therefore fixed by the selected sign flip. If a previous
commuting sign flip already fixes both arguments, it fixes their
geometric mean by the same congruence identity. Thus sequential
symmetrization preserves every previously imposed symmetry.

The twice-reviewed geodesic feasibility argument applies to this midpoint:
the cap remains valid and every energy is no larger than the average
of its equal endpoint values. Its determinant equals the geometric mean
of their determinants, hence is unchanged. Starting from a positive
definite determinant maximizer and applying all coordinate flips therefore
produces a diagonal maximizer. Commuting with every coordinate flip forces
each off-diagonal entry to vanish. No arithmetic averaging or Euclidean
convexity of indefinite quadratic energies is being assumed.

For a correlated positive semidefinite budget `W`, factor it
conceptually as a Gram matrix. Its energy is a sum of ordinary energies
for linear combinations of the Hessians. Those combinations retain the
same commuting symmetries and their energies are geodesically convex.
Thus the same midpoint argument applies to correlated budgets.

For diagonal covariance entries `p_i>0`, the ordinary energy is
`sum_i h_ji^2 p_i^2`. Setting `t_i=p_i^2` gives exactly the stated
linear inequalities, and `sum_i log t_i=2 log det P`. For a correlated
budget the coefficient is `h_:i^T W h_:i>=0`, as claimed. Maximizing
this strictly concave objective on its convex feasible domain is an
ordinary convex optimization problem in the standard concave-maximization
convention. The note correctly restricts its rational-data simplification
to a rational common diagonalization already being supplied.

For one Hessian, if the full vector `t=1` fits the budget, it maximizes
every increasing logarithmic summand. Otherwise the function
`s -> sum_i min(a_i,s)` increases continuously and strictly from zero
to `sum_i a_i` as `s` runs from zero to `max_i a_i`. This proves
existence and uniqueness of the stated positive threshold.

The proposed coordinate values use the full budget. For multiplier
`mu=1/s`, the maximization stationarity condition is

```
1/t_i - mu a_i - nu_i=0.
```

An unsaturated coordinate has `a_i>s`, `t_i=s/a_i`, and
`nu_i=0`. A saturated coordinate has `t_i=1` and
`nu_i=1-a_i/s>=0`; the same formula gives `nu_i=1` when
`a_i=0`. Complementarity holds, including ties `a_i=s`.
Concavity then certifies global optimality. All-zero Hessians are
already handled by the full-budget case.

Sorting the coefficients identifies the linear segment containing
`s`, on which its defining equation is linear. For `H=I` and unit
tolerance it gives `t_i=1/n` and `p_i=1/sqrt(n)`, agreeing with
the independently audited dimension-gap example.

