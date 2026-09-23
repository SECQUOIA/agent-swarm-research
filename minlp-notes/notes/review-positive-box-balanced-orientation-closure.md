# Balanced orientations: finite-dimensional bound and closing audit

Date: 2026-09-04. Reviewer: `review_fbbt`. The proposed closure of the last
section of [the coefficient proof note](positive-box-rho-plus-two-proof.md)
is correct. This note completes that bounded verification; it does not start
further extensions or assert independent novelty.

## Proposition

Fix an ambient number of coordinates `N>=2` and `rho>1`. Define

\[
p_N=\frac{2\lfloor N/2\rfloor\lceil N/2\rceil}{N(N-1)},
\qquad \beta_N=\frac1{p_N}
=\begin{cases}
2-2/N,&N\text{ even},\\
2-2/(N+1),&N\text{ odd}.
\end{cases}
\]

Every positive multilinear polynomial on an `N`-dimensional strictly positive
box with coordinate aspect ratios at most `rho` satisfies

\[
\operatorname{tbtgap} f\le(\rho+\beta_N)\operatorname{chgap} f.
\]

Fixed coordinates may first be removed; the cases of zero or one remaining
coordinate have zero gaps. The upper bound uses one global distribution, so it
applies simultaneously to every monomial support.

## The fixed ambient distribution

Choose a uniform subset `H` of `[N]` with size `floor(N/2)`, independently of
one uniform variable `U` on `[0,1]`. Coordinate `i` succeeds on `[0,u_i]` if
`i` belongs to `H`, and on `[1-u_i,1]` otherwise. Call this law `O`.
Both possible intervals have length `u_i`, so every marginal is correct.
For odd `N`, the individual orientation choices are not fair; fairness is
unnecessary for this assertion or the proof below.

Every distinct pair has opposite orientations with probability `p_N`. This
probability is unchanged when the law is restricted to any set of coordinates.
Throughout the proof, restrictions retain this same ambient law. They are
**not** replaced by balanced laws sampled anew in the smaller dimension.

## Coefficient induction for restrictions

For any support `S` of size `n<=N`, define `C_j,P_j,V_j` as in the reviewed
coefficient theorem and let `O_j` be the orientation moment under the
restriction of the ambient law to `S`. Set

\[
F_{S,j}=\beta_N C_j+V_j-P_j-\beta_N O_j+C_{j-1}-P_{j-1}.
\]

Use degree-zero moments equal to one and negative or above-dimension moments
equal to zero. Then `F_{S,0}=F_{S,1}=0`, `F_{S,n+1}=C_n-P_n>=0`, and higher
orders vanish.

For a pair, equal orientations give its upper Fréchet intersection probability
and opposite orientations give its lower one. With `L_2` denoting the sum of
pairwise lower bounds,

\[
O_2=(1-p_N)C_2+p_N L_2.
\]

Since `beta_N p_N=1`, this gives
`F_{S,2}=(C_2-P_2)+(V_2-L_2)>=0`, exactly as in the original base case.

Deleting a coordinate whose mean is zero restricts the same law further.
A coordinate whose mean is one is deterministic in the rounded vector, so
Pascal's identity gives

\[
F_{S,j}(u,0)=F_{S\setminus\{i\},j}(u),\qquad
F_{S,j}(u,1)=F_{S\setminus\{i\},j}(u)
 +F_{S\setminus\{i\},j-1}(u).
\]

In particular, deleting a deterministic coordinate does not condition on its
orientation coin. Correlations among the remaining coins therefore cause no
change to these identities. The adjacent-cardinality moments `V_j` obey the
same Pascal relation.

For an interior vector and `3<=j<=n`, spread distinct global minimum and
maximum coordinates from `x,y` to `x-h,y+h`, taking
`0<h<=min(x,1-y)`. Put
`B=binom(n-1,j-1)` and `D=binom(n-1,j-2)`. The finite comparisons from the
reviewed proof give

\[
\Delta C_j=-Bh,\quad \Delta C_{j-1}=-Dh,\quad
\Delta V_j=0,\quad
\Delta(-P_j-P_{j-1})\le Dh.
\]

The orientation comparison also survives the dependence of the coins.
Couple using the same `H,U`: increasing a single mean is monotone, changes
that coordinate with probability exactly its increment, and changes
`binom(K,j)` by at most `B` on that event. Decreasing the minimum and then
increasing the maximum therefore gives `Delta O_j>=-Bh`. Consequently

\[
\Delta F_{S,j}\le-\beta_N Bh-Dh+Dh+\beta_N Bh=0.
\]

Take `h=min(x,1-y)` and use boundary induction. Dimension one and all moment
orders outside `3<=j<=n` were already covered. Thus every `F_{S,j}` is
nonnegative, with the same constant `beta_N` on every support and restriction.

## Products, sums, and positive boxes

For `t=rho-1`, the coefficient of `t^j` in

\[
(\beta_N+t)C+V-(1+t)P-\beta_N O
\]

is `F_{S,j}`. Since `t>0`, coefficient nonnegativity makes this expression
nonnegative, which rearranges to the local inequality

\[
T=C-V\le\rho(C-P)+\beta_N(C-O).
\]

Choose independent rounding with probability `rho/(rho+beta_N)` and the
fixed ambient orientation law with probability `beta_N/(rho+beta_N)`.
This same mixture captures at least `T/(rho+beta_N)` for every physical
monomial. Summing with positive coefficients and using the simultaneous
common-threshold concave maximizer proves the common-aspect result.

For unequal positive boxes, apply the same positive affine substitution as
in the canonical theorem. Every original monomial expands into nonnegative
physical monomials on the same `N` coordinates. The original termwise gap
is at most the expanded termwise gap, and the full hull gap is invariant.
The expanded supports use restrictions of the same ambient orientation law,
so the constant remains `rho+beta_N`. This proves the stated transfer.

The restriction issue identified in the exploratory note is therefore
resolved. No independence assumption about orientation coins is needed in
the pair base case, the finite-step Lipschitz comparison, or the boundary
identities. The result improves the finite-dimensional upper bound only;
it does not determine the exact worst-case ratio.

## Formal verification follow-up

The [topic-18 Lean package](../formal/topics/18-positive-box/README.md)
formalizes this refinement in `BalancedOrientation`, `BalancedMoments` and
`BalancedRefinement`. The [coverage map, PB27–PB31](../formal/topics/18-positive-box/COVERAGE.md)
identifies the declarations, and the
[independent review](../formal/topics/18-positive-box/REVIEW.md) records the
separate review of those obligations. The
[verification record](../formal/topics/18-positive-box/VERIFICATION.md)
reports the checks and their scope. The formal statements retain one ambient
law and `beta_N` as supports shrink; they establish the bound without claiming
that `beta_N` is minimal.
