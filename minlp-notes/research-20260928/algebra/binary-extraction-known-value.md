# Exact binary extraction can retain PosSLP hardness at a known rational optimum

Date: 2026-09-28. This is a short consequence of the repository's reviewed
[rational-optimizer coordinate theorem](../../research-20260927/rational-optimizer-posslp-coordinate-comparison.md),
not a proposed main contribution. A fresh adversarial review is recorded
in [the companion review](binary-extraction-review.md).

Knowing the exact optimum value does not in general remove the arithmetic
difficulty of identifying an optimal integer decision. The following
reduction makes that distinction precise with one binary variable.

## Statement and proof

Given an integer straight-line program with output V, the coordinate
theorem constructs in polynomial time an explicit rational quartic F in
N real variables, a coordinate j, rational quadratic square factors,
and a full positive definite rational Hessian Gram Q such that

\[
 F\geq0,\quad F^{-1}(0)=\{p\},\quad
 p\in\mathbb Q^N\cap[-1,1]^N,\quad
 \nabla^2F\succeq\tfrac32 I,\quad
 p_j\ne0,\quad (p_j>0\iff V>0).
\]

Consider the mixed-integer problem

\[
 \begin{aligned}
 \min_{x\in\mathbb R^N,\ z\in\mathbb Z}\quad &
 H(x,z)=F(x)+(z-\tfrac12)^2,\\
 \text{subject to}\quad &0\leq z\leq1,\\
 &z-1\leq x_j\leq z.
 \end{aligned}                                                    \tag{1}
\]

**Proposition.** The input in (1) has polynomial bit length and a
supplied rational certificate of global strong SOS-convexity. Its exact
optimum is the known rational number 1/4. It has the unique optimizer

\[
             (x_*,z_*)=(p,\mathbf1[p_j>0]),                       \tag{2}
\]

which is rational and belongs to [-1,1]^N times {0,1}. The continuous
constraint matrix has rank one. Therefore returning the optimal binary
decision for this promised class is PosSLP-hard under polynomial-time
many-one reduction to the decision predicate z_*=1.

Indeed z is either zero or one, so every feasible objective value is
at least 1/4. If p_j>0, then (p,1) is feasible, since 0<p_j<=1;
(p,0) is infeasible. If p_j<0 the roles reverse. Equality in the
objective lower bound forces F(x)=0, hence x=p. This proves the
optimum and uniqueness claims without any lower bound on |p_j|.

The objective Hessian is block diagonal with blocks Hessian(F) and
2, so its global curvature is at least 3/2. The supplied SOS expression
for F gains one square. Its short rational strong-convexity certificate
can be obtained directly from Q: if d is the dimension of Q, set

\[
 \eta=\min\{1,\det(Q)/(2\operatorname{tr}(Q)^{d-1})\}>0.
\]

The standard determinant-over-trace eigenvalue bound gives Q>=2 eta I.
Subtracting eta times the identity restricted to the constant-direction
part of the Hessian basis leaves a rational positive semidefinite Gram.
Together with the scalar 2-eta, this certifies that
H-(eta/2)||(x,z)||^2 is SOS-convex. The certificate size is polynomial.
The specific global lower bound 3/2 comes from the imported construction;
the certificate calculation by itself supplies eta.

Only the last two constraints in (1) involve x. Their continuous normals
are e_j and -e_j, so their rank is exactly one. There are no box
constraints on the other continuous variables: the optimizer is bounded,
while the feasible domain need not be bounded.

The resulting objective does **not** have a positive definite Gram on
the full joint Hessian basis. Its quartic leading form is independent
of z, which prevents that strict Gram property. Global strong convexity
and the rational strong SOS-convexity certificate above are the promises
being asserted.

## A variant preserving a full positive definite Hessian Gram

The full-Gram restriction can also be retained. This refinement was
proposed by the independent reviewer and then independently rederived by
the author, including its full Hessian identity and Schur-complement
bound. Put

\[
 \rho=\det(Q)/\operatorname{tr}(Q)^{d-1},\qquad
 0<\epsilon\leq\min\{\rho/4,1/(100N)\},
\]

with a rational epsilon of polynomial bit length, and replace H by

\[
 \widehat H(x,z)=F(x)+(z-\tfrac12)^2
   +\epsilon z(z-1)\|x\|^2+\tfrac14 z^2(z-1)^2.                \tag{3}
\]

Both added terms vanish at z=0 and z=1. Therefore every feasible
objective value in (1), its unique optimizer, its known optimum 1/4,
and the rank-one continuous constraint matrix remain exactly the same.

Here is a short full positive definite rational Hessian Gram for (3).
Write t=z-1/2, let v be the direction in x and s the direction in z,
and use the full Hessian basis in the order

\[
                  (v,\ x\otimes v,\ s,\ tv,\ xs,\ ts).
\]

Let E project onto the first, constant-direction v block of Q, and let
d_0 be the vector supported on x tensor v with
d_0^T(x tensor v)=x^Tv. Set A=Q-(epsilon/2)E and b=4 epsilon d_0.
The proposed Gram has diagonal blocks

\[
                   A,\quad 7/4,\quad2\epsilon I_N,
                   \quad2\epsilon I_N,\quad3,
\]

and its only new off-diagonal block is b between the A block and the
final ts entry. Direct differentiation gives

\[
 \begin{aligned}
 D^2\widehat H[(v,s),(v,s)]
  ={}&v^T\nabla^2F(x)v-\tfrac\epsilon2\|v\|^2
      +\tfrac74s^2+2\epsilon t^2\|v\|^2\\
    &+2\epsilon\|x\|^2s^2+8\epsilon t(x^Tv)s+3t^2s^2,
 \end{aligned}
\]

which is exactly the displayed Gram identity. The determinant-over-trace
bound gives A>=rho I/2. Since ||d_0||^2=N,

\[
 b^TA^{-1}b\leq32\epsilon^2N/\rho
               \leq8\epsilon N\leq2/25<3.
\]

The Schur complement and all other diagonal blocks are strictly positive.
Translating t back to z is an invertible rational basis transformation,
so the full Gram remains rational and positive definite in the original
coordinates. All matrices and constants have polynomial bit length.
It supplies a positive rational global strong-convexity modulus by the
same determinant-over-trace bound. This refinement does not preserve the
particular modulus 3/2 or the base construction's supplied objective
square factors; neither promise is needed for its extraction hardness.

The objective is also globally strictly positive. Indeed,
F(x)>=3||x-p||^2/4 and ||p||^2<=N give

\[
 F(x)-\epsilon\|x\|^2/4\geq-\epsilon N/2.
\]

For u=t^2>=0, u+(u-1/4)^2/4 is increasing and has minimum 1/64.
Dropping the nonnegative epsilon t^2||x||^2 therefore gives

\[
                 \widehat H\geq1/64-\epsilon N/2
                              \geq17/1600>0.
\]

No additional short objective SOS certificate is asserted for this
variant. Its short full Hessian certificate is explicit above.

## What this adds and what it does not

Earlier padding reductions preserved exact objective-value hardness
after adding an irrelevant integer variable. In (1), the integer decision
itself contains the arithmetic answer, even though the optimum value is
given in advance. This provides a direct lower-bound counterpart to the
[constraint-rank algorithm](../../research-20260927/mixed-quartic-integer-constraint-rank-oracle.md):
already k=1 and continuous constraint rank r=1 can retain the PosSLP
oracle in exact integer extraction. An ordinary polynomial-time exact
extraction algorithm on this class would imply PosSLP in P.

This is a restricted reduction, not an unconditional lower bound against
polynomial-time optimization, an NP-hardness claim, or a demonstrated
solver speedup. It does not require that the continuous minimizer in the
losing branch be rational. Approximate objective optimization may return
the wrong binary decision when its tolerance exceeds the branch gap.
No quantitative lower or upper branch-gap family is established here.

The main arithmetic construction and its novelty qualifications are
in the imported coordinate theorem and its
[primary-source audit](../../research-20260927/quaternion-circuit-posslp-prior.md).
This elementary binary bridge does not warrant an independent priority
claim. The classical arithmetic context is Allender, Buergisser,
Kjeldgaard-Pedersen, and Miltersen,
[*On the Complexity of Numerical Analysis*](https://eccc.weizmann.ac.il/report/2005/037/).
Their PosSLP framework does not itself supply the restricted convex
quartic and rational-optimizer realization used here.

## Verification scope

The proof is the equality case of a nonnegative objective plus two
linear inequalities; a numerical experiment would add little confidence.
The [base review](binary-extraction-review.md) checked the reduction,
uniqueness, rank count, certificate distinction, and retained promises.
A separate [fresh full-Gram review](binary-joint-gram-fresh-review.md)
independently reconstructed the refinement and checked its Hessian,
positive definiteness, bit bounds, and unchanged integer fibers. Its exact
symbolic tests passed. No project-wide checks,
CI inspection, or Lean formalization were performed for this corollary.
