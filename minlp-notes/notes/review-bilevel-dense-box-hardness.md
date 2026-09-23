# Independent audit: one leader and a dense strictly convex box follower

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS after the joint-convexity clarification.** I independently reviewed
[the dense-box hardness construction](bilevel-dense-box-hardness-investigation.md).
The reduction proves the stated NP-completeness and gap of zero versus at
least two. It uses one continuous leader, a rational constant
positive-definite follower Hessian, a pure follower box, and affine upper
data. The proof does not infer hardness merely from an exponential path.

The author corrected an important representation distinction during this
review: the original sum-of-squares lower objective is jointly convex,
including its leader-only quadratic term. Deleting that term preserves
all follower responses but generally destroys joint convexity of the
normalized expression. Both versions support the same reduction, with
joint convexity claimed only for the former.

## Boolean response certificates

The residual matrix `L` is triangular with unit diagonal, so the base
Hessian `L^T diag(w_i)L` is positive definite. The leader value

```
x_b=sum_i 2b_i/3^i+1/(2*3^n)
```

lies strictly between zero and one for every Boolean vector. Substitution
into the residuals gives the stated remaining ternary quantity. If the
current bit is zero, its residual is at least
`1/(2*3^(n-i))` and at most one. If the bit is one, the residual lies
between minus one and the negative of that positive lower bound. These
inequalities include the final bit, whose residual magnitude is one half.

The contribution of all later residuals to coordinate `i`'s derivative,
after division by `w_i`, is bounded by

```
2 sum_(ell>=1)(3rho)^ell=6rho/(1-3rho)<1/(10*3^n).
```

The current residual magnitude is at least `3/(2*3^n)`, using `i>=1`.
Thus its sign survives with the claimed strict margin greater than
`w_i/3^n`. The signs are correct for box minimization: a positive gradient
at a zero coordinate and a negative gradient at a one coordinate are
sufficient KKT conditions. Strict convexity makes these certificates
identify unique responses, rather than merely stationary points.

## Auxiliary coordinates and feedback

Conditional minimization of each added scalar square on `[0,1]` gives
`p_i=max(0,2y_i-1)` and `q_i=max(0,1-2y_i)` because `y_i` is itself in
the unit interval. Consequently `p_i+q_i=|2y_i-1|` at every complete
follower optimum, independently of the effect these added terms have on
the optimal `y`.

The full residual matrix has diagonal blocks `L,I,I` and is square and
invertible. Its positive weighted Gram matrix is therefore positive
definite. At the proposed Boolean response `(b,b,1-b)`, the auxiliary
gradient in a base coordinate is `-2eta` for bit zero and `+2eta` for bit
one. These oppose the base signs but are strictly smaller in magnitude
than the existing margin:

```
2eta=2rho*w_n<w_n/3^n<=w_i/3^n.
```

The auxiliary coordinates themselves satisfy the required box signs,
including their zero-gradient endpoint cases. Therefore the complete
unique response remains exactly `(b,b,1-b)` at every encoded leader.

At `x=1/2`, all base coordinates equal to one half make every base
residual zero. Setting `p=q=0` also makes the auxiliary residuals zero.
Positive definiteness gives the claimed unique midpoint response.

## Always-feasible gap reduction

The exact-three-distinct-variable clause restriction is legitimate. For
completeness, repeated literals can first be removed and tautologies
discarded. Two-literal clauses can be padded by a fresh variable with
both signs in two clauses; unit clauses can be padded by two fresh
variables with all four sign pairs. An empty clause is an immediately
unsatisfiable instance. Thus the restriction preserves NP-hardness without
depending on multiplicities in the rounding argument.

Every clause has value `3/2` at the midpoint response, making the
constructed bilevel problem feasible regardless of satisfiability. The
unique follower response is continuous in the scalar leader: compactness
gives convergent subsequences, and passing the follower optimality
inequalities to their limits identifies every limit with the unique
limiting optimizer. The feasible leader-response graph is closed in a
compact box. Hence the affine upper minimum exists.

At every response the upper objective satisfies

```
F=n-sum_i(p_i+q_i)=2 sum_i min(y_i,1-y_i)>=0.
```

A satisfying assignment is reached by its encoded leader and gives zero
objective. Conversely, round each `y_i` upward at a tie. If the Boolean
formula is unsatisfiable, some clause is false under this rounded vector.
For every literal in this false clause its continuous value is exactly
`min(y_i,1-y_i)`, including ties. The upper clause inequality forces their
sum to be at least one. Since the three variables are distinct, these
three terms form a subset of the total nonnegative sum in `F/2`.
Therefore every feasible response has `F>=2`.

The gap is thus exact, and an objective approximation with absolute error
strictly less than one separates its two cases at the threshold one.
The distinction between strict error below one and error at most one is
appropriate. The result concerns exact follower responses; the proof
does not furnish a uniform tolerance for approximate follower solutions.

## Rational encoding and joint convexity

The numbers `3^i` have linear bit length and `rho^i` have quadratic bit
length in `n`. Expanding the weighted squares produces only polynomially
many quadratic coefficients, each of polynomial rational encoding length.
The full Hessian is constant in the leader. Clause coefficients are in
`{-1,0,1}`, their right-hand sides in `{-1,0,1,2}`, and the objective
constant is `n`, as the revised statement specifies. No large numerical
data are hidden in the upper model.

Each weighted square is convex in the leader and all followers together.
However, after dropping the leader-only term, the joint quadratic
Hessian of the normalized model is `[0,d^T;d,Q]`, which cannot be positive
semidefinite when `d` is nonzero. The clarified statement correctly keeps
joint convexity with the sum-of-squares representation and treats
normalization as response equivalence only.

The exponentially separated rational weights do not justify strong
NP-hardness, a polynomial condition-number guarantee, or robustness to
fixed lower-objective perturbations. The stated boundaries retain these
distinctions.

## NP certificate

For an arbitrary rational instance in the displayed class, guess a lower,
free, or upper status for each follower coordinate. The principal matrix
`Q_FF` is positive definite and invertible. Setting upper coordinates to
one and lower coordinates to zero, the free coordinates are

```
z_F(x)=-Q_FF^(-1)(c_F+x d_F+Q_FU*1).
```

Exact rational linear algebra gives these affine functions with polynomial
bit length. Free-coordinate bounds, endpoint gradient signs, upper
constraints, and the objective threshold all reduce to finitely many
closed rational affine inequalities in `x`. Their feasible set inside
`[0,1]` is a closed interval, possibly a point. If nonempty it contains a
rational endpoint of polynomial bit length. Empty free sets and
free-coordinate values at bounds are covered by the same weak tests.

A certificate may supply the status and this rational leader. The verifier
reconstructs the follower and checks all box KKT and upper conditions with
exact rational arithmetic in polynomial time. Positive definiteness makes
the verified point the unique follower optimum. Thus the zero-threshold
decision problem belongs to NP, completing NP-completeness on the
constructed always-feasible subclass.

## Independent exact checks

[The reviewer checker](../code/bilevel_dense_box/second_review_checks.py)
uses Python rational arithmetic only. It passed:

- 510 complete Boolean response certificates for every assignment with
  `1<=n<=8`, differentiating the residual squares and checking all base
  and auxiliary KKT signs exactly;
- eight midpoint residual identities;
- 1,000 literal and readout checks on a rational grid, including 25
  feasible false-clause cases that verify the two-unit objective gap.

Run `python code/bilevel_dense_box/second_review_checks.py`. These checks
supplement the symbolic proof; no full bilevel solver or empirical novelty
claim is involved. Literature priority and antecedent path constructions
remain the subject of the separate source audit.

## Strengthening: no upper constraints and a smaller follower

I also independently checked
[the clause-shortfall extension](bilevel-dense-box-no-upper-constraints-extension.md)
and the author's final simplification that removes `q`. Both pass.

For each clause add a boxed follower `v_a` with quadratic residual
`v_a-1+ell_a(y)` and weight `xi=eta/(m+1)`. Because continuous literal
sums are nonnegative, its exact conditional optimum is
`v_a=max(0,1-ell_a(y))` in `[0,1]`. At a Boolean vector the residual is
zero, zero, one, or two according as the number of true clause literals
is zero, one, two, or three. Every coordinate derivative of a clause sum
has magnitude at most one. Thus the total clause feedback on any base
coordinate has magnitude at most `2m xi<2eta`.

The symmetric construction's auxiliary feedback was at most `2eta`.
Consequently total feedback is less than `4eta`, which is smaller than
the previously proved base margin. Every Boolean response therefore
survives the clause additions, whether or not the assignment satisfies
the formula. The residual map remains square with invertible diagonal
blocks `L,I,I,I`, and the follower Hessian stays positive definite.

To simplify further, remove every `q_i` and its quadratic square. Keep
only `p_i=clip(2y_i-1)`. Then

```
y_i-p_i=min(y_i,1-y_i),
F=2 sum_i y_i-2 sum_i p_i+2 sum_a v_a.
```

The remaining Boolean auxiliary feedback is `-2eta` at a zero bit and
zero at a one bit, so the same less-than-`4eta` estimate applies. The
residual map on `(y,p,v)` now has diagonal blocks `L,I,I`, again
invertible. The final follower has `2n+m` coordinates, all boxed in
`[0,1]`. The upper objective has coefficients only `+2` and `-2` and
zero constant term; there are no upper constraints beyond `x in [0,1]`.

For any follower response put `D=sum_i min(y_i,1-y_i)`. Its upper value is

```
F=2D+2 sum_a max(0,1-ell_a(y)).
```

A satisfying Boolean response gives zero. For an unsatisfiable formula,
round the base vector as before and choose a clause false under the
rounded assignment. Its literal sum is at most `D`, using distinctness
of its variables. Therefore

```
F>=2D+2 max(0,1-D)>=2.
```

This argument requires no clause feasibility constraints. Every leader
is now automatically feasible because the follower box is nonempty and
compact. The unique response is continuous, so the upper minimum is
attained. The original midpoint zero-residual assertion must not be
applied after adding clause squares; it is unnecessary for this final
construction. The active-status NP certificate and all rational encoding
bounds remain unchanged, including the joint-convexity distinction.

The exact checker was extended to 1,008 clause-feedback certificates,
testing both the symmetric predecessor and the final version without
`q`, across satisfying and unsatisfiable clause families. It also checked
the unconstrained upper gap on all 125 points of a rational three-variable
grid for the unsatisfiable family containing all eight clauses. Every
check passed. The stronger construction can replace the upper-constrained
presentation in the final result.

## Final integrated result

I reread
[the final scalar-leader SPD-box theorem](../results/bilevel-scalar-leader-spd-box-np-completeness.md)
after integration. It consistently uses only `(y,p,v)`, a follower
dimension of `2n+m`, no upper constraints, and the linear objective with
coefficients in `{-2,0,2}`. The strict margins, feedback estimate,
unconstrained objective gap, encoding bounds, and active-status NP
certificate match the reviewed construction. The final theorem passes.
I requested one prose-only adjustment: call the gradient signs at the
Boolean point box optimality signs, since the vector lying in the outward
normal cone is the negative gradient. No displayed equation changes.
