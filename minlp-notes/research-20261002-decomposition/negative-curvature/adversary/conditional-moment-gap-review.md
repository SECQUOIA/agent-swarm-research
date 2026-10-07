# Independent review of the conditional moment gap

Date: 2026-10-02. Verdict: the stated counterexample and its limited
consequence are correct. No substantive mathematical revision is required.

Reviewed [conditional-moment-gap.md](../convex-energy/conditional-moment-gap.md)
and its [exact checker](../convex-energy/check_conditional_moment_gap.py).
This review concerns their mathematical argument, implementation, and scope;
it is not a publication-priority or literature audit.

## Algebra and conditioning

Writing `a=(u_1+u_2)/2` and `b=1/4+v/2` gives

\[
8(t-a)^2+8(t-b)^2
=16\left(t-\frac{a+b}{2}\right)^2+4(a-b)^2.
\]

Adding the three concave unary terms to the last square gives exactly

\[
\frac14+2(u_1u_2+v-u_1v-u_2v).
\]

The latter parenthesis equals
`(1-v)u_1u_2+v(1-u_1)(1-u_2)` and is nonnegative throughout the
unit box. With the strictly positive linear control penalty, equality in
the objective lower bound forces all controls to zero and then `s=h/8`.
Consequently the optimum is uniquely `1/4`.

For `S=u_1+u_2+v` and `delta=t-1/8-S/4`, Cauchy--Schwarz and
`h<=1` give

\[
\|x-x^*\|^2
\le 2\delta^2+\frac{11}{8}\|w\|^2,
\qquad
F_h-f^*\ge16\delta^2+\frac1{16}\|w\|^2.
\]

Since `(11/8)/22=1/16`, the asserted global growth bound `g=1/22`
follows for the entire box, including the portion where `s/h>1`.
This argument holds uniformly over the whole stated range of `h`;
the finite checker fixtures are supplementary.

Let `r_1=(1/h,-1/2,-1/2,0)` and
`r_2=(1/h,0,0,-1/2)`. The Hessian satisfies

\[
H_h+2I=16r_1r_1^T+16r_2r_2^T+2e_se_s^T\succeq0.
\]

The vector `(0,1,-1,0)` is an eigenvector with eigenvalue `-2`.
Thus the least eigenvalue is exactly `-2`, while `H_{ss}=32/h^2`.
The example indeed fixes `n=4`, largest bag size `p=3`, and a valid
ratio `nu/g=44`, while allowing arbitrarily large positive curvature.

## Relaxation witness

Both displayed bag distributions have mass one. Their normalized
separator moments are `1/2`, `5/16`, and `7/32` through degree three.
Their fourth moments differ by `3/256`. Multiplying degree `j` by
`h^j` transfers these statements from `t` to `s`.

All separator atoms lie strictly below `2h`, so disaggregation by the
stated partition preserves moment agreement separately for each
separator-cell label. The control atoms at zero and one can be assigned
to their respective endpoint cells under a consistent boundary convention.
No unsupported assumption about a common control-cell label is needed:
the stated sparse interface sums these labels out before comparing
separator moments.

Every local square and binary concave penalty vanishes. Each control
mean is `1/2`, giving objective `3/32`. Hence the relaxation gap is
at least `5/32`; the argument does not assert that this witness is a
relaxation optimizer.

The proposed covariance is an explicit sum of two positive semidefinite
rank-one matrices. Its restrictions agree with the two bag moment
matrices. In particular its nonedge moments are
`E[u_1v]=E[u_2v]=3/8`, and its trace is `3/4+h^2/16`.
The McCormick assertions are consistent with both the unit control
bounds and the tighter separator interval `[0,2h]`.

There can be no representing joint measure: binary control second
moments would force binary controls almost surely, while the two zero
square expectations would force `u_1+u_2-v=1/2`. The stated violated
global inequality has pseudoexpectation `-1/8`, independently confirming
the failure of joint realizability.

## Error bound and scope

The PSD covariance inequality and the sufficient globally conditioned
mixture interface are valid. PSD covariance alone need not represent a
measure, and the argument correctly does not require one for that
sufficient interface.

For the counterexample, `nu sum_i w_i^2=32h^2`. Therefore

\[
\frac{f^*-L_{\rm witness}}{\nu\sum_iw_i^2}
=\frac{5}{1024h^2}\longrightarrow\infty.
\]

This disproves a finite coefficient depending only on `p` and `nu/g`
in the stated local-width bound for the stated relaxation. It also
disproves that bound after adding matching separator moments through
degree three and an unconditional PSD completion. A weaker relaxation
inherits the obstruction because it admits the same witness.

It does not establish a complexity lower bound for adaptive algorithms,
rule out stronger global constraints, or obstruct every fixed moment
order. Equality of the fourth separator moment already rejects this
particular witness. The author's explicit scope clarification is
appropriate. Likewise, the exponentially many cells in the uniform
partition are used only to refute the error estimate; no runtime lower
bound follows from counting those cells.

## Targeted verification

Executed from the repository root:

```text
python research-20261002-decomposition/negative-curvature/convex-energy/check_conditional_moment_gap.py
```

Result: exit status zero, `status: passed`; 11 dyadic family parameters,
11 exact polynomial identities, 2,673 rational growth fixtures, and 704
global McCormick inequality checks. The checker also verifies the
Hessian representation, exact negative eigenvector, bag restrictions,
moments through degree four, PSD-completion formula, objective gap, and
violated global inequality. Inspection found no floating-point step in
these arithmetic checks.

No project-wide checks or CI inspection were performed.
