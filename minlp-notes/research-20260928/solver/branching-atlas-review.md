# Independent review of the curvature atlas theorem

Date: 2026-09-28. Reviewed: [branching-curvature-atlas.md](branching-curvature-atlas.md).

The finite-cover upper bound, matching negative-slice lower bound, and
rotating example are correct under the stated assumptions. I found no
counterexample to these claims. The proof establishes an approximation
exponent for a fixed function and compact domain. It does not establish a
uniform algorithmic complexity bound or practical solver improvement.
The missing companion degeneracy note was not available when this review
began, so its announced conclusion is outside this review.

## Independent reconstruction of the upper bound

Order the eigenvalues increasingly. The assumption is
`lambda_(k+1)(H(x)) > 0` on `D`. Eigenvalue continuity and compactness
give a uniform positive lower bound `mu_*`; boundedness of `H` gives a
uniform `M >= 0` such that `H(x) >= -M I`. At a center `a`, let `P_a`
project onto any orthonormal collection of eigenvectors for the first
`k` eigenvalues and put `tau=M+mu_*`. Then

```
H(a)+tau P_a >= mu_* I.
```

Uniform continuity of `H` supplies a positive neighborhood radius on
which the same fixed `P_a` gives lower bound `mu_* I/2`. Thus the local
construction requires neither continuous eigenvector selection nor an
eigenvalue gap between the kth and (k+1)st eigenvalues. Repeated
eigenvalues do not invalidate the argument. A finite collection of such
neighborhoods covers `D`.

For a projected coordinate interval `[l_i,u_i]`, the correction
`(tau/2)(y_i-l_i)(y_i-u_i)` has Hessian `tau v_i v_i^T`, is nonpositive
on the interval, and has absolute value at most `tau(u_i-l_i)^2/8`.
Summation proves both convexity and the claimed uniform error. The
number of coordinate boxes is bounded by

```
product_i (1 + W_i sqrt(tau k/(8 epsilon))),
```

up to an immaterial endpoint convention, where `W_i` is the chart's
projected width. This proves the exponent after summing over finitely
many charts. Each epigraph lies inside the allowed lower epigraph,
and the union contains the entire original epigraph, including its
unbounded vertical rays.

For `k=n`, choose `tau>0` explicitly. The manuscript currently permits
`tau=0`, which makes its subsequent formula for `h_j` undefined; choosing
a larger positive value resolves this harmless edge case without
changing the proof. Alternatively, a zero regularizer means the
corresponding function is already convex. For `k=0`, convexity gives
one piece directly.

The strict positive-complement assumption is substantive. It says that
the total number of nonpositive eigenvalues is at most `k`, not merely
that the number of negative eigenvalues is at most `k`. It is sufficient,
not necessary: degenerate convex functions also have one-piece covers.

## Literal branching and boundary cells

The proposed finite preliminary axis-aligned partition is valid. Here
is a precise argument that avoids assumptions about cells touching only
the boundary of `D`.

Take the finite open curvature neighborhoods `U_j`. Choose finitely many
balls `B(a_i,r_i)` covering `D` such that every `B(a_i,2r_i)` lies in
one `U_j`. Set `delta=min_i r_i>0`. Partition an enclosing box for `D`
into closed grid boxes of diameter less than `delta`. If a grid box `B`
meets `D`, select `z` in that intersection and an index `i` with
`z in B(a_i,r_i)`. Every point of `B` then belongs to `B(a_i,2r_i)`, so
the entire box lies in the corresponding curvature neighborhood.
Assign that chart to `D intersect B`.

This argument also covers boxes whose intersection with `D` has empty
interior. The preliminary grid has a fixed finite number of boxes,
independent of `epsilon`. Successive affine splits can implement the
subsequent projected-coordinate subdivisions. Closed children may
overlap on a splitting hyperplane; this preserves coverage, validity,
and the leaf count. A finite binary realization has order the number
of leaves, though its preprocessing cost and numerical representation
are not bounded by the theorem.

## Independent lower-bound check

On a small interior negative slice, let
`g(s)=f(x_0+Ts)` with `H_g <= -m I`. Concavity of
`g(s)+(m/2)||s||^2` gives

```
g((s+t)/2) - (g(s)+g(t))/2 >= m||s-t||^2/8.
```

If two graph points belong to the same convex piece, the midpoint
also belongs to that piece and its height must be at least
`g((s+t)/2)-epsilon`. Hence their parameter distance is at most
`sqrt(8 epsilon/m)`. For each piece, take the closure in the parameter
cube of its graph-point parameter set. This is compact, has the same
diameter bound, and is contained in a coordinate box with each side no
larger than that diameter. These finitely many boxes cover the cube.
Ordinary finite subadditivity of volume proves exactly the displayed
lower-bound constant. No measurability or closedness of the original
pieces is needed. Allowing continuous convex lifts cannot evade this
argument, because each projected piece is still convex.

## Optimization and mixed-integer consequences

For nonempty cells, let `x_c` minimize the continuous convex objective
`f_c` and set `L=min_c f_c(x_c)`, `U=min_c f(x_c)`. Compactness ensures
existence. Every candidate is feasible, and coverage implies
`L <= f_* <= U`. Choosing a cell attaining `L` gives

```
U <= f(x_c) <= f_c(x_c)+epsilon = L+epsilon.
```

Thus the optimization corollary is valid. The same reasoning holds
after imposing integrality on selected coordinates, discarding cells
with no mixed-integer feasible point. The correct feasible set is
`D intersect (Z^p x R^(n-p))`; `D` itself remains the convex continuous
domain. This wording issue was reported to the author and corrected
during review. The subproblems retain their separate combinatorial cost.
Numerical versions need certified lower bounds and feasible points
with a specified subproblem gap; for a uniform certified gap `eta`,
the same reasoning yields `U-L <= epsilon+eta`.

The warning about nonconvex constraints is warranted even when each
row has a strict positive complement. For example, the matrices
`A=diag(-1,1)` and `-A` each have one negative and one positive
eigenvalue, but no rank-one positive semidefinite matrix `P` can make
both `A+tau_1 P` and `-A+tau_2 P` positive semidefinite. For a nonzero
`w in ker(P)`, their quadratic forms force `w^T A w=0`. A positive
semidefinite matrix with zero quadratic form on `w` must annihilate
`w`, which would force `Aw=0`, contradicting invertibility. Individual
inertia bounds therefore do not establish a common branching space.

## Rotating example and significance

Symbolic differentiation independently confirmed the stated Hessian
of `exp(x)cos(y)`, its characteristic polynomial
`lambda^2-exp(2x)`, and the identity
`w^T H w=exp(x)cos(y+2 theta)`. For every kernel direction `w`, the
last expression is negative at some interior point of the box. A
fixed rank-one positive semidefinite regularizer cannot remove that
negative curvature. The example therefore separates the local atlas
construction from a single global rank-one quadratic regularizer.
Its heading should be read in this restricted sense: the calculation
does not prove that every possible optimization or branching method
must change directions. The example is explicitly easy to optimize.

The theorem gives a useful structural extension of fixed-direction
quadratic subdivision to smooth functions. Its elementary proof and
uncontrolled chart count limit the significance claim presently
supported. In particular, the finite chart count may depend badly on
the positive spectral gap and Hessian variation. The theorem does not
bound certified construction cost, expression size, convex-oracle
cost, or uniform complexity as the function or dimension varies.

## Additional literature terminology

The hypothesis has established terminology. Thomas Patrick
Pawlaschyk's 2015 dissertation,
[*On some classes of q-plurisubharmonic functions and q-pseudoconcave sets*](https://d-nb.info/1081429941/34),
Theorem 2.4.3, characterizes smooth real `q`-convexity by at most `q`
negative Hessian eigenvalues and strict real `q`-convexity by at most
`q` nonpositive eigenvalues. Thus the atlas assumption is strict real
`k`-convexity on a neighborhood of `D`, after shrinking that neighborhood.

The same source's Definition 2.6.5 and Theorem 2.6.7 concern
approximation from above by real `q`-convex functions with corners,
defined locally as finite maxima of smooth real `q`-convex functions.
Those examined statements neither give convex epigraph covers nor
an `epsilon^(-k/2)` piece count. This is a relevant terminology and
prior-work lead, not a priority determination. Earlier sources cited
there were not independently checked in this review.

The search queries were `"Hessian" "negative eigenvalues" "convex"
"approximation" global optimization smooth functions`, `"convex
epigraph" "cover" "Hessian"`, and `"low dimensional nonconvexity"
Hessian optimization`. Only the cited primary source was examined
in enough detail to support a literature comparison. The manuscript's
qualified novelty language remains appropriate.

## Verification scope and record

The mathematical arguments above were checked independently by hand.
The targeted command below was run successfully from the repository
root; its two residual outputs were zero and the zero matrix:

```bash
python - <<'PY'
import sympy as s
x,y,theta=s.symbols('x y theta',real=True)
f=s.exp(x)*s.cos(y)
H=s.hessian(f,(x,y))
w=s.Matrix([s.cos(theta),s.sin(theta)])
print('Hessian:',H)
print('characteristic polynomial:',s.factor(H.charpoly().as_expr()))
print('directional expression difference:',s.trigsimp((w.T*H*w)[0]-s.exp(x)*s.cos(y+2*theta)))
print('H squared difference:',s.simplify(H*H-s.exp(2*x)*s.eye(2)))
PY
```

This symbolic check verifies the example's identities, not the general
covering theorem, the companion barrier, or novelty. No Lean check,
project-wide verification, or CI inspection was performed. No major
proof repair was required; the positive-`tau` edge case and presentation
qualifications above remain the requested small clarifications.
