# Convex polynomial performance in continuous cactus design

Date: 2026-09-05. Status: verified by two independent full mathematical audits. The supporting arithmetic and convex-optimization mechanisms are credited; this verification does not establish publication priority.

## Extension theorem

In the [reviewed exact-capacity cactus design theorem](../results/potential-flow-cactus-capacitated-convex-design.md) and its [correlated cycle-polytope extension](../results/potential-flow-cycle-polytope-resistance-design.md), replace the rational positive-semidefinite quadratic objective by any rational densely encoded polynomial f of the flow vector that is promised convex on the expanded box |x_e|<=B+1, where B=sum_v |b_v|.

The same conclusion holds: for every rational epsilon>0, one can find in polynomial time in input length and requested accuracy bits a rational resistance scenario satisfying all specified capacities exactly and attaining f within epsilon of its constrained minimum. The polynomial degree may grow with its dense input encoding. Sparse binary-exponent encoding and validation of the convexity promise are not included.

The proof below only supplies the convex-optimization oracle needed by the previously reviewed surrogate/recovery arguments. It does not change physical feasibility, capacity clipping, or resistance recovery.

## 1. Explicit gradient bounds and surrogate error

For f(x)=sum_alpha c_alpha x^alpha and S=B+1>=1, compute rational bounds

    V_f=sum_alpha |c_alpha| S^|alpha|,
    G_f=1+max_i sum_alpha |c_alpha| alpha_i S^(|alpha|-1),

with zero derivative terms omitted. Then |f|<=V_f and every partial derivative has magnitude at most G_f on the expanded flow box. These bounds have polynomial bit length under dense encoding. All previous objective perturbation estimates hold with G_f in place of the quadratic gradient bound.

Use eta<=min(1/2,epsilon/(16mG_f)). The correlated-polytope proof has projection error at most 3m eta and final recovery error at most m eta. Optimizing the rational surrogate objective within epsilon/2 therefore gives total loss at most

    4mG_f eta+epsilon/2<=3epsilon/4<epsilon.

The interval-only proof has the smaller earlier projection constant and remains valid as well. Handle m=0 or B=0 directly as before.

## 2. A rational globally Lipschitz convex extension from a cube

Remove every fixed coordinate from the rational surrogate box, including frozen coordinates and retained rational singleton intervals, and transform each remaining positive-width rational interval affinely to [-1,1]. Write the resulting objective as h(z)=f(Tz+a) on [-1,1]^k. This polynomial is convex on that cube, and it has an exact rational value and gradient oracle in polynomial bit time by composition; expanding its coefficients is unnecessary.

The affine image of the cube lies in the expanded flow box. Thus a rational bound V>=|h| is V_f, and a rational bound G>=max_j |partial_j h| is obtained from G_f times the largest column l1 norm of T, increased to at least one. Both bounds have polynomial bit length. The dimension-zero case is evaluated directly.

Set

    M=1+V+kG,
    t(z)=max(1,||z||_infinity),
    H(z)=t(z) h(z/t(z))+M(t(z)-1).

This agrees with h throughout the cube. It is globally convex. To see this, restrict h to the cube, assigning value +infinity outside it. Its perspective t h(z/t) is convex on t>0 and z/t in the cube. Add the affine term M(t-1), and impose t>=1. For fixed z and feasible t>=max(1,||z||_infinity), differentiation gives

    d/dt [t h(z/t)+M(t-1)]
      =h(w)-grad h(w)^T w+M>=1,
    w=z/t in [-1,1]^k.

The minimum over feasible t is therefore attained at t=t(z). Partial minimization of this convex function over the convex feasible set proves convexity of H.

Moreover H is globally Lipschitz. At every z choose tau in the subdifferential of t(z), so every coordinate of tau has magnitude at most one. Put w=z/t(z) and

    K(w)=h(w)-grad h(w)^T w+M,
    0<=K(w)<=1+2(V+kG).

The supporting inequality for the joint perspective at (z,t(z)) gives, for every z',

    H(z')>=H(z)+grad h(w)^T(z'-z)+K(w)(t(z')-t(z)).

Since t(z')-t(z)>=tau^T(z'-z) and K(w)>=0, the vector

    s(z)=grad h(w)+K(w)tau

is a subgradient of H at z. Its infinity norm is bounded by

    C=G+1+2(V+kG).

Applying this support inequality at both points proves |H(z)-H(z')|<=C||z-z'||_1. Equivalently kC is a rational Euclidean Lipschitz upper bound. This argument includes every tie among maximizing coordinates and every boundary point of the cube.

At rational z, t(z), z/t(z), H(z), and this subgradient can be computed using rational arithmetic in polynomial time. For tau choose a signed maximizing coordinate when ||z||_infinity>1, zero when ||z||_infinity<1, and any valid choice from their convex hull at equality. Only the exact value oracle and explicit Lipschitz bound are needed for the cited optimization theorem.

## 3. Apply established bounded convex optimization

The rational cube contains a Euclidean unit ball and lies within radius k of the origin. The extension H is globally convex and globally Lipschitz with an exact rational polynomial-time oracle. [Dadush's thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf), Theorem 2.5.9 and its input-length convention, therefore yield a rational point in the cube within epsilon/2 of its minimum in polynomial bit time. Since H=h there, this is exactly the surrogate optimizer needed in Section 1.

Convexity of the perspective and preservation of convexity under partial minimization are standard; see [Boyd and Vandenberghe, Convex Optimization](https://www.seas.ucla.edu/~vandenbe/cvxbook/bv_cvxbook.pdf), Sections 3.2.5–3.2.6, especially printed page 89. The primary indexed passages were read. The extension only makes the global-Lipschitz oracle condition explicit for this application.

## Verification and source scope

Both [the first full audit](../notes/review-potential-flow-convex-polynomial-design.md) and [the second full audit](../notes/review-potential-flow-convex-polynomial-design-second.md) passed. They checked cube-only convexity, all boundary and tie cases in the supporting inequality, rational oracle complexity at growing dense degree, the cited bounded convex-optimization theorem, and exact physical capacity recovery. Review clarified that every zero-width surrogate interval must be removed before rescaling.

The perspective transform, partial minimization, and convex polynomial optimization are established. This result records the explicit oracle implementation needed by the flow-design proof and extends its objective scope. The same proof composes with the [correlated polynomial-law cycle theorem](potential-flow-correlated-polynomial-cycle-design.md): the physical recovery is unchanged, and only the objective gradient bound and surrogate optimizer are replaced.

The independent [subgradient checker](../code/potential_flow_mpd/convex_polynomial_extension_subgradient_review.py) passed 5,580 exact supporting-hyperplane inequalities, including cube boundaries and tied maximizing coordinates.

## Exact diagnostics

[`convex_polynomial_extension_checks.py`](../code/potential_flow_mpd/convex_polynomial_extension_checks.py) passed 1,600 exact rational Jensen, global-Lipschitz, and cube-agreement checks over 20 polynomials in one to four variables. Degrees ranged up to eight, constants and linear terms could be negative, and cases included `sum_i (6z_i^2-z_i^4)`, which is convex on the cube but not globally. These checks exercise the extension's boundary and oracle formulas; the universal convexity and bit bounds follow from the proof.
