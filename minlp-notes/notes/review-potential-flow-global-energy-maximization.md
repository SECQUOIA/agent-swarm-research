# Independent review: maximum dissipation over a resistance polytope

Date: 2026-09-05. Reviewer: `benders_property`. Status: PASS, including the appended rational global-quality certificate.

Reviewed [the full candidate](potential-flow-global-energy-maximization.md), including its compactification, lower-dimensional parameter treatment, exact feasible-output argument, and final certificate. This review verifies the mathematics and bit-output guarantee; Fenchel duality, perspectives, second-order cones, and convex optimization remain classical ingredients requiring the separate source assessment.

## Physical duality and the factor of three

For positive fixed beta, the primitive energy is finite, differentiable, strictly convex, and coercive on the nonempty affine conservation space. Its unique minimizer has the physical edge laws as stationarity equations. The scalar conjugate of `beta*abs(x)^3/3` is exactly `(2/3)*abs(d)^(3/2)/sqrt(beta)`, including d=0. Equality-constrained Fenchel duality is valid because the primitive has full domain; normalizing one potential removes only its constant ambiguity and does not change the balanced-nomination objective.

At the physical state, `b^T*pi=sum beta*abs(x)^3`, so D=3V. The conjugate is the perspective of the convex function `(2/3)*abs(d)^(3/2)`, hence is jointly convex in (d,beta) for beta>0. Its negative plus the affine potential objective is concave. Maximization over beta and pi is therefore convex optimization, and exchanging these two maximizations introduces no minimax issue.

## Exact cone representation

With z,u,t nonnegative, `z^2<=t*u` and `u^2<=beta*z` imply `z^4<=beta*z*t^2`. If z>0, division gives `z^3<=beta*t^2`. Conversely, that inequality with z>0 forces t>0, and choosing `u=z^2/t` satisfies both constraints. When z=0, the second cone forces u=0 and permits every t>=0. Thus the zero case is exact, not a limiting argument.

Adding z>=d and z>=-d and minimizing the penalized t projects to the required conjugate epigraph. More directly, every feasible lift has `t>=sqrt(abs(d)^3/beta)`, and every point of that epigraph has a lift by choosing z=abs(d) and the preceding u. Both quadratic inequalities are convex rotated cones only with the stipulated nonnegative coordinates; those restrictions are present. No irrational coefficient is required in the rational product-form cone representation.

The physical witness `z=beta*abs(x)^2`, `u=beta*abs(x)`, `t=beta*abs(x)^3` satisfies both cone inequalities at equality, including at x=0. Its conic objective is exactly V, confirming all constants.

## Compactness and an explicit rational interior radius

Passivity gives the nomination flow bound B on every connected graph. A spanning-tree path from the reference vertex therefore bounds each physical potential by `m*beta_U*B^2`. The proposed bounds for z,u,t follow immediately. Enlarging these and the potential bounds as stated preserves a physical optimizing witness for every beta. Thus the compact conic problem has the same optimum as the unbounded-potential dual. Its closed bounded feasible set also proves attainment of the joint maximum.

At the displayed rational strict point, z=1, u=r and t=2/r give `t*u-z^2=1`. Since `r=min(1,beta_L)/2`, one has `beta_L-r^2>0`. All nonnegativity and absolute-drop inequalities are strict. Coordinate upper bounds enlarged by at least one preserve strictness. These magnitudes and slacks have polynomial rational bit length, even when beta_L is numerically very small.

For P, test each inequality by LP to identify rows tight everywhere. For every remaining row choose a rational point having positive slack and average all such witnesses. This gives a rational relative-interior point with positive slack in every nonuniversal row. Rational LP vertex bounds and the polynomial number of averaged points bound all encodings and the inverse of each nonzero slack by polynomial bit length. Universal rows determine the affine hull; rational Gaussian elimination gives its coordinate representation in polynomial time. A singleton P simply has no remaining resistance-coordinate variables.

An explicit radius can be obtained without a qualitative Slater assumption. In the reduced affine coordinates, write every remaining linear or quadratic constraint as p_j(y)>=0 and let y0 be the strict point. On the unit coordinate neighborhood of y0, bound the l1 norm of each polynomial gradient by a rational M_j>=1 using its coefficient absolute values and rational coordinate-magnitude bounds. Set

    rho=min(1, min_j p_j(y0)/(2*M_j)).

The Euclidean ball of radius rho lies in every constraint by the mean-value bound. Every quantity is rational of polynomial bit length because the polynomials have degree at most two and the affine transformation has polynomial encoding. Universal affine equalities have already been removed. An outer radius follows from the coordinate boxes and a rational left inverse of the affine parameterization; alternatively choose its free coordinates among original beta coordinates. Gaussian-elimination bounds ensure polynomial encoding for this radius too. The complete reduced conic region is consequently a centered full-dimensional convex body with explicit rational data.

## Oracle theorem and rational scenario guarantee

I reopened [Dadush's primary thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf) and checked Theorem 2.5.9 together with the preceding computational conventions. The theorem returns a point in K, not merely near K, for a centered convex body with weak membership and a globally Lipschitz convex value oracle. Its complexity includes the encodings of the center and radii. The candidate supplies precisely these data. Exact rational membership by polynomial inequalities is a valid weak membership oracle. Negating the linear conic objective gives an everywhere Lipschitz convex function with an exact rational value oracle and an explicit rational norm bound.

The theorem therefore supplies a rational feasible reduced-coordinate point within epsilon/3 of the conic maximum. The rational affine map returns beta in the original P exactly. For any such feasible point, its objective J satisfies J<=V(beta) by weak duality and the conjugate epigraph inequalities. Hence

    D(beta)=3*V(beta)>=3*J>=max_P D-epsilon.

Its auxiliary potentials need not be physical for this conclusion. No physical-flow rounding, exact optimal rational profile, or exact scalar threshold decision is asserted. B=0 and edgeless cases are correctly separated. The distinction between mathematical dissipation and literal gas-system power is also correctly stated.

## Appended exact rational global certificate

For rational conserved y, the trial primitive energy bounds V(beta) above for every beta. With `w_e=abs(y_e)^3/3`, dual feasibility `lambda>=0` and `R^T*lambda=w` gives `beta^T*w<=c^T*lambda=U` throughout P. Thus U bounds the global maximum V, even though y need not be a physical state of any profile.

For a chosen admissible rational beta0, normalized rational pi and nonnegative rational t with `beta0_e*t_e^2>=abs((A^T*pi)_e)^3` give the exact dual lower bound L<=V(beta0). These two independent inequalities imply the displayed global suboptimality bound `max D-D(beta0)<=3*(U-L)`. All checks are rational and do not require the chosen profile's physical flow. The complete bounded polytope description ensures a feasible LP dual exists for any trial objective w if one chooses to compute it by LP.

In the triangle example, the flow (1/2,1/2,1/2) is conserved. Its w entries are 1/24, so the sum-beta constraint yields U=6/24=1/4. The proposed beta and pi give edge drops (3/8,3/8,3/4); the proposed t values sum to 3/4 and meet the conjugate bounds exactly. Therefore L=3/4-(2/3)*(3/4)=1/4. This certifies D=3/4 and a globally optimal original profile exactly.

No correction was required.

## Addendum: exact capacity filters on a cactus

The final composition corollary passes. The reviewed global-correlation arc theorem turns all specified rational cactus arc capacities into an exact rational parameter polytope P_cap. After checking nonemptiness, P_cap inherits boundedness and the same explicit positive resistance bounds from P. Its description has polynomial bit length. It may have a smaller affine dimension or be a singleton; the conic algorithm already recomputes the affine hull and relative interior for its supplied polytope, so these cases are covered.

Apply the conic formulation with P_cap as its parameter domain. Its auxiliary potentials and cone variables need not themselves represent the physical state, but every returned beta belongs to P_cap exactly. The scalar capacity characterization therefore guarantees that beta's unique physical flow satisfies all capacities exactly. The approximation affects only the energy objective. No capacity relaxation, margin, or rounded physical-flow certificate is required.

The general-graph theorem retains its unfiltered physical scope. The affine capacity description used by this corollary is the cactus-specific import; it is not silently assumed on other graphs. If the global-quality certificate is also used for the constrained optimum, its polytope rows can be those of P_cap. Its conserved trial flow need not itself satisfy capacities, since it still bounds the unconstrained primitive energy of every capacity-admissible profile from above.
