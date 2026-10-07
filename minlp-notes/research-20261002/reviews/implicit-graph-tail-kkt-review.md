# Independent audit of implicit-graph finite tails and KKT roots

Date: 2026-10-02. Status: completed-draft finite-tail and KKT interface
review passed; no substantive gap found.
This is a mathematical review, not an external literature or priority
assessment.

Scope: Sections 1, 5, and 6 of the completed
[implicit graph theorem](../new-direction/smoothed-implicit-graph-constraints.md).
Anchors `t` lie in a mixed product box. Each continuous dependent coordinate
`y_j` is the unique root of `q_j(t_{S_j},y_j)=0` in a rational interval
`V_j`; `q_j` depends on no other dependent coordinate. Certified global
brackets and `partial_{y_j}q_j>=alpha_j>0` hold on the full real anchor
hull times `V_j`. The objective and graph polynomials have fixed bounded
degree. Independent ambient linear noises perturb the retained anchors and
the dependent coordinates. This review does not establish the separate
approximate-DP or convex-evaluator implementation interfaces.

## 1. The graph assumptions are sufficient and substantive

Global brackets and strict monotonicity give exactly one `y_j` for every
anchor point, including throughout the continuous hull of integer anchor
domains. The implicit function theorem makes the selected graph smooth.
The local branch extends past an output-interval endpoint when needed;
on the anchor box it remains inside the interval by the global premises.

Consequently the output bounds are redundant restrictions on the graph.
They remain useful branch selectors but need not have their own KKT
multipliers in the reduced optimization problem. An output lying on
`partial V_j` does not obstruct two-sided variation of an interior free
anchor coordinate: that variation remains feasible by the global graph
premise. This would be false for an arbitrary extra bound cutting a graph.

The premises need valid supplied bounds or counted verifiable certificates.
Checking arbitrary multivariate polynomial inequalities is not a free
polynomial-time operation. Derivative estimates for the reduced objective
must concern the selected graph and be uniform over the bounded auxiliary
noise. An ambient diagonal-curvature bound alone is insufficient after
implicit substitution.

## 2. Positive reduced Hessian implies a nonsingular polynomial KKT root

Fix an integer anchor assignment and an original continuous anchor face.
Let `u` be its `k` free coordinates; all other anchors are fixed. Let there
be `m` dependent coordinates. Write the restricted objective as `f(u,y)`
and define

\[
 \mathcal L(u,y,\lambda)=f(u,y)+\lambda^Tq(u,y).
\]

The polynomial equations are

\[
              \mathcal L_u=0,\qquad\mathcal L_y=0,\qquad q=0.
 \tag{1}
\]

There are `k+2m` equations and unknowns. At a selected graph point,
`Q=q_y` is diagonal and invertible. The multipliers are uniquely determined
by `lambda=-Q^{-T}f_y`. Inserting them into the first equations gives
stationarity of the reduced objective `G(u)=f(u,psi(u))`.

Let

\[
 C=[q_u\ Q],\qquad Z=\begin{bmatrix}I\\-Q^{-1}q_u\end{bmatrix},
 \qquad H=\nabla^2_{(u,y)}\mathcal L.
\]

Implicit differentiation and stationarity give

\[
 CZ=0,\qquad Z^THZ=\nabla^2G(u),\qquad
 J_{\rm KKT}=\begin{bmatrix}H&C^T\\C&0\end{bmatrix}.
 \tag{2}
\]

If `J_KKT(v,mu)=0`, its constraint rows imply `v=Z a` for some `a`.
Multiplying the stationarity rows by `Z^T` gives
`nabla^2 G(u) a=0`. A positive definite reduced Hessian forces `a=0`,
hence `v=0`. Then `C^T mu=0`, and the invertible block `Q^T` forces
`mu=0`. Thus the full polynomial KKT Jacobian is nonsingular.

Block elimination also gives the exact identity

\[
 \det J_{\rm KKT}=(-1)^m\det(Q)^2\det(\nabla^2G(u)).
 \tag{3}
\]

At an optimizer with anchor point growth `g>0`, two-sided Taylor expansion
along the free original face gives `nabla^2G>=2g I`. Therefore

\[
 |\det J_{\rm KKT}|
       \ge\left(\prod_j\alpha_j^2\right)(2g)^k>0.
\]

The empty reduced Hessian when `k=0` has determinant one, so the argument
also covers a face with no free anchors. Positive definiteness is a
stopping-analysis consequence of growth, not an unverified certificate
premise on arbitrary draws.

## 3. Isolated roots and the active-anchor strip bound

If the objective has degree at most `d_F` and graph equations degree at
most `d_q`, the equations in (1) have degree at most
`D=max{1,d_F-1,d_q}`. Multiplication of a graph derivative by a multiplier
raises its degree by one, giving degree at most `d_q`. A coarser `2d`
bound when all original degrees are at most `d>=1` is valid.

A nonsingular real root is also an isolated nonsingular complex root.
The isolated-root Bezout bound gives at most `D^(k+2m)` such roots.
Other roots or positive-dimensional singular components do not invalidate
this bound. Counting every stationary point as isolated would be unjustified;
the reduced-Hessian argument supplies precisely the needed restriction.

Now fix an active continuous anchor coordinate `i`, its original face,
and all noises except its own anchor coefficient `gamma_i`. On this face
`t_i` is fixed, so `gamma_i t_i` is constant. It disappears from every
equation in (1), including the equations determining the multipliers.
Thus the finite set of relevant nonsingular roots is independent of
`gamma_i`. At each such root the reduced active derivative is

\[
                            \gamma_i+\beta
\]

for a fixed real number `beta`. Its absolute value is at most `tau` only
on an interval of length `2tau`. Under the endpoint-inclusive `M`-point
uniform law on `[-sigma,sigma]`, its probability is at most
`tau/sigma+1/M`.

Union over active anchor coordinates, original anchor faces, native integer
assignments, and the isolated roots. With `n_c` continuous anchors and
`R_Z` integer assignments, the safe factor

\[
 K=\max\{1,n_c3^{n_c}R_Z D^{n_c+2m}\}
 \tag{4}
\]

is singly exponential in base format. The bounded event is the intersection
of positive growth and a small active derivative. One does not condition
the noise law on positive growth. Rather, every draw in that intersection
must hit one of the fixed root intervals just counted.

## 4. Growth and canonical output use exactly two quantified blocks

Let `A(t,y)` be the quantifier-free mixed anchor-domain formula together
with the output interval bounds and all graph equations. For a fixed
auxiliary-noise vector, retain one anchor-noise coefficient as a free scalar
`v` and fix the others. The good-growth condition is exactly

\[
 \exists(t,y)\ \forall(t',y'):\quad
 A(t,y)\ \wedge
 \left[\neg A(t',y')\ \vee
 \{F_v(t',y')-F_v(t,y)\ge\varepsilon\|t'-t\|^2\}\right].
 \tag{5}
\]

Both blocks have size `n+m`. No stationarity variables or nested root
quantifiers are needed. Graph uniqueness makes positive anchor growth
equivalent to growth at a unique ambient optimizer. The norm is the anchor
norm, not a silently substituted ambient norm.

The degrees are bounded by the original polynomial degrees and two.
Native integer domains add conceptual finite disjunctions, whose number
of atoms can be exponential but whose logarithm is polynomial in the base
encoding. The graph contributes only polynomially many extra atoms. The
two-block scalar-section bound from the
[finite-tail theorem](../new-direction/polynomial-finite-noise-tails.md)
therefore remains singly exponential in base format. It is uniform in all
fixed coefficients, auxiliary noise values, and thresholds. The real-valued
coefficient version covers the hybrid continuous/discrete comparison.

For canonical exact output, compare feasible pairs using the order

\[
 F(t,y)<F(t',y')\quad\text{or}\quad
 [F(t,y)=F(t',y')\ \wedge\ t\le_{\rm lex}t'].
 \tag{6}
\]

Requiring (6) against every feasible competitor selects the lexicographically
least anchor among all global optimizers. Compactness supplies that anchor,
and graph uniqueness supplies one associated output vector. Append an
equality setting the free scalar to the desired anchor coordinate, output
coordinate, or objective value. The resulting singleton formula still has
only the existential candidate block and universal competitor block.
Lexicographic comparison has polynomial formula size. Keeping the graph
equations avoids expanding implicit algebraic branches or their degrees.

This fallback formula works on tied or degenerate samples as well. It does
not rely on the KKT nonsingularity used solely for the active-gradient tail.

## 5. Uniform constants and verification scope

Condition first on all auxiliary output noises. Independent retained anchor
noises remain on their original product finite law. Section-count constants
and (4) depend on degree and format, not those fixed coefficient values or
heights. Positive certified `alpha_j`, bounded rational chart boxes, and
fixed-degree monomial bounds provide uniform derivative bounds with
polynomial encoding lengths. Reduced curvature and higher derivative
constants must be selected over the entire permitted auxiliary-noise box.

The graph-assisted fallback formulas have base-fixed degree, atom counts,
and quantifier dimensions. Sampled coefficients enter through polynomial
coefficient height, as in the
[constructive fallback proof](../new-direction/polynomial-exact-fallback-construction.md).
Thus choosing a common base exponential budget before sampling, followed
by cutoff and finite-grid precision, is consistent with these interfaces.
This reasoning does not authorize an unverified general positivity test
for a proposed graph or curvature bound.

The independent diagnostic command actually run was

```text
python research-20261002/reviews/check_implicit_graph_tail_kkt_review.py
```

The [checker](check_implicit_graph_tail_kkt_review.py) passed 36 exact
KKT determinant identities with indefinite ambient Hessians allowed,
including zero free dimension. A nonlinear graph fixture checks the
multiplier equations, determinant `-7`, reduced Hessian `7/4`, and 16 finite
active-gradient strip bounds. A degenerate reduced-Hessian fixture gives
a singular KKT system. These are finite algebraic diagnostics, not an
implementation of quantifier elimination or the full optimizer. No
project-wide verification, CI inspection, or external search was performed.

## 6. Comparison with the completed draft

The actual saved theorem matches the interfaces proved above. In particular:

- Its growth modulus and active derivatives are in retained coordinates.
  It does not reuse ambient derivatives after substitution.
- Its dependent bounds are global branch selectors and redundant feasible
  restrictions, as required when their multipliers are omitted.
- Its KKT count uses `k+2m` unknowns and the safe uniform exponent
  `n_c+2m`; it counts nonsingular roots even if other components have
  positive dimension.
- Its conditional growth discrepancy is `2n C_tail/M`, because only the
  `n` retained noise coordinates undergo the continuous-to-finite hybrid
  argument. The auxiliary noises are fixed during that argument; the
  larger `n+m` dimension enters the quantifier-elimination format instead.
- Its common thresholds and grid precision precede every noise draw. The
  two bad events each cost at most `rho`, and their sum `1/(2B)` pays for
  the same-draw fallback.
- Its fallback operates on the original polynomial graph domain, not on
  a nonexistent explicit polynomial representation of the reduced
  algebraic objective. The two-block construction above justifies this.

I requested minor explicitness improvements: give a concrete safe KKT
degree such as `max{2,d_F,max_j deg(q_j)}`; state that the derivative floor
in the graph premise holds for all `y in V_j` as well as all real anchor
points; and count provided proof lengths and their polynomial verification
for the independently checkable-certificate variant. The stated theorem
already treats the bounds as valid input premises and explicitly rejects
a free general polynomial-positivity oracle. These requests do not change
the mathematical argument.

This review approves the finite-tail, isolated-root, and canonical fallback
format interfaces. Separate reviews are responsible for the approximate
grid DP and the detailed weak-separation/convex-evaluation implementation.
