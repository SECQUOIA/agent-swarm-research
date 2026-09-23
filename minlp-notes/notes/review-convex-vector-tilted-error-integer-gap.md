# Independent audit: convex vector graphs with tilted error bodies

Date: 2026-09-05. Reviewer: potential_flow_review. Verdict: PASS.

I independently checked the complete construction in
[the candidate](convex-vector-tilted-error-integer-gap.md), including its
[scalar polynomial antecedent](nonconvex-polynomial-binary-integer-gap.md).
This is a mathematical audit, not an independent literature-priority claim.

The Bernstein polynomial has degree at most `N=1024M^2`, rational data,
range `[0,1]`, and uniform triangle-wave error at most `1/32`: the wave is
`2M`-Lipschitz and the binomial standard deviation divided by `N` is at
most `1/(2sqrt(N))`. Its dense coefficient encoding has polynomial length
in `N` and `log M`.

For `C=1+sum k(k-1)|c_k|`, the bound `|q''|<=C-1` holds on `[0,1]`.
Consequently `(q+Cx^2)''>=C+1>0`, while `(Cx^2)''=2C>0`.
Computing this rational `C` and the vector and error-body coefficients
preserves polynomial encoding length in the dense input.

The scalar two-integer formulation covers the entire exact graph and has
error at most `1/16`. Appending `0<=w_2<=C` and `w_1=s+w_2` covers every
exact vector graph point, and every feasible projected point satisfies
`|e_1-e_2|<=1/16` and `|e_2|<=C`. The upper bound therefore controls the
whole projection, not just selected witnesses.

Conversely, the linear projection `s=w_1-w_2` of any binary convex lift
covers the exact scalar graph and has scalar error at most `1/4`. Two
distinct exact peak points cannot share a binary assignment: their convex
segment reaches an intervening trough with output at least `31/32`, where
the true polynomial is at most `1/32`. Thus all `M` peaks need distinct
binary strings, giving `p_bin>=ceil(log2 M)`. Encoding the explicit period
index in binary gives the stated upper bound `ceil(log2 M)+1`.

The conditioning calculation is also valid. The point `(C,C)` gives
circumradius at least `sqrt(2)C`, and the narrow strip gives inradius at
most `1/(4sqrt(2))`. At a peak with adjacent trough spacing `h=1/(2M)`,
the centered second difference is at most `-15/8`. Its integral expression
against the nonnegative triangular kernel of total mass `h^2` yields
`max|q''|>=15M^2/2`. Hence `C>=1+15M^2/2` and the radius ratio grows at
least as `8+60M^2`.

The varying and increasingly ill-conditioned error body is essential to
the stated construction. A separate follow-up proves finite upper bounds
for fixed conditioning and for all unconditional bodies in this same
one-input setting; see
[the finite comparison candidate](componentwise-convex-fixed-condition-integer-gap.md).
That follow-up does not alter the tilted-body counterexample.
