# Recognizing a globally affine optimal response by linear programming

Date: 2026-10-02. Status: complete constructive argument with an
[independent review](../reviews/affine-selector-recognition-review.md)
finding no substantive gap; targeted checks are recorded below.
No publication-priority claim is made.

The [affine convex-recourse reduction](../affine-convex-recourse.md) need
not rely on a guessed active face or a supplied affine certificate. For
a convex quadratic over a fixed box, existence of a globally affine
optimal response on a parameter box can be decided and a response
constructed in polynomial rational bit time. The Hessian may be singular,
and the conditional optimizer may be nonunique.

The algorithm solves one convex QP and one LP for the affine map.
It does not enumerate active sets or
critical regions. It recognizes one affine selection on the entire box;
it does not construct a general piecewise-affine solution map.

## 1. Model and theorem

Let `Y=[l,u]` be a rational product box in `R^r`, and let `Z` be a rational
product box in `R^k`. Substitute fixed coordinates first. Thus remaining
private and parameter intervals have positive width. All data are rational,
`C` is symmetric positive semidefinite, and

\[
 \phi_z(y)=\tfrac12 y^TCy+(Dz+c)^Ty,\qquad y\in Y.       \tag{1}
\]

A globally affine optimal response is a real affine map `a+B(z-z0)`
belonging to `argmin_Y phi_z` for every `z in Z`. Uniqueness is not
required. Terms depending on `z` alone do not affect this definition.

**Theorem.** Existence of such a response is decidable in polynomial time
in the rational input encoding length. If a real affine response exists,
the algorithm returns a rational one of polynomial encoding length,
together with affine bound multipliers satisfying the global certificate
in the parent note.

The theorem uses standard polynomial-time exact rational convex-QP and LP
algorithms. The finite diagnostic described below is not an implementation
of those general-purpose polynomial-time algorithms.

## 2. The central gradient determines a sufficient fixed pattern

Let `z0` be the midpoint of `Z`, which is strictly interior, and put
`h0=Dz0+c`. Solve the convex QP at `z0` to obtain one rational optimizer
`yhat`. Its entire optimizer set is

\[
 P_0=\{y\in Y:Cy=Cyhat,\quad h_0^Ty=h_0^Tyhat\}.       \tag{2}
\]

Indeed, for `d=y-yhat`, quadratic expansion gives

\[
 \phi_{z_0}(y)-\phi_{z_0}(yhat)
     =(Cyhat+h_0)^Td+\tfrac12d^TCd.                   \tag{3}
\]

The first term is nonnegative for every feasible `y` by convex first-order
optimality; the second is nonnegative by `C>=0`. Equality forces both to
vanish. For a PSD matrix, `d^TCd=0` implies `Cd=0`, after which the first
term reduces to `h0'd`. This proves (2) in both directions. In particular,
all points in `P0` have the same gradient `Cyhat+h0`.

Put `g0=Cyhat+h0`. All central optimizers have this same gradient.
Partition the coordinates by its exact signs:

\[
\begin{split}
 K_l&=\{i:(g_0)_i>0\},\\
 K_u&=\{i:(g_0)_i<0\},\qquad
 J=[r]\setminus(K_l\cup K_u).                         \tag{4}
\end{split}
\]

By box KKT conditions, a positive gradient fixes the coordinate to its
lower bound, and a negative gradient fixes it to its upper bound.
Thus the coordinates in `K_l,K_u` have these fixed values throughout
`P0`. Every remaining central gradient coordinate is zero:

\[
                 (Cyhat+h_0)_j=0\quad(j\in J).        \tag{5}
\]

The algorithm does not need to compute coordinate ranges or a relative
interior point of `P0`. A coordinate fixed to a bound throughout `P0`
may nevertheless lie in `J` if its multiplier is zero. This causes no
problem: the zero-gradient identity below and global primal feasibility
already impose everything needed on that coordinate.

## 3. Every affine selector obeys one fixed KKT pattern

Suppose `ybar(z)` is a globally affine optimal response. For `i in K_l`,
its central coordinate is `l_i`. An affine function that is everywhere
at least `l_i` on a full-dimensional box and attains `l_i` at an interior
point is constant. Thus `ybar_i(z)=l_i` throughout `Z`. The upper-bound
case is identical. These fixed coordinates require the corresponding
gradient sign on the whole parameter box.

Now fix `j in J` and define its affine gradient

\[
        G_j(z)=(C\bar y(z)+Dz+c)_j.                  \tag{6}
\]

At the center this is zero by (5), since `ybar(z0)` belongs to `P0` and
all its optimizers have the same gradient. There are two possibilities.

* If `ybar_j` is identically one of its bounds, then KKT gives a fixed
  sign for the affine function `G_j` on `Z`. Its zero at the interior
  point `z0` forces `G_j` to vanish identically.
* Otherwise `ybar_j` is strictly between its bounds at every interior
  parameter point. Any interior attainment of a bound would force an
  affine bounded function to be constant at that bound. KKT therefore
  gives `G_j=0` on the parameter interior, and the affine identity holds
  everywhere.

Consequently every globally affine optimal response satisfies

\[
\begin{array}{ll}
 \bar y_i=l_i,\quad (C\bar y+Dz+c)_i\geq0,&i\in K_l,\\
 \bar y_i=u_i,\quad (C\bar y+Dz+c)_i\leq0,&i\in K_u,\\
 (C\bar y+Dz+c)_j=0,&j\in J,\\
 \bar y\in Y,&z\in Z.                                \tag{7}
\end{array}
\]

Conversely, (7) is sufficient for global conditional optimality, by the
convex box-QP KKT conditions. Thus the fixed pattern obtained from the
common central gradient loses no affine response, even if a particular
central optimizer has extra active bounds.

## 4. The remaining search is a polynomial-size LP

Write `Z={z0+w: |w_j|<=rho_j}`, where every `rho_j>0` is rational,
and search for `ybar=a+Bw`. The gradient coefficients are

\[
                 \gamma=Ca+h_0,\qquad T=CB+D.        \tag{8}
\]

The bound-fixed coordinates impose linear equations
`a_i=l_i` or `u_i` and `B_i*=0`. Zero-gradient coordinates impose
`gamma_j=0,T_j*=0` for `j in J`.

For primal bounds, introduce `v_ij>=B_ij` and `v_ij>=-B_ij`, and impose

\[
 l_i\leq a_i-\sum_j\rho_jv_{ij},\qquad
 a_i+\sum_j\rho_jv_{ij}\leq u_i.                     \tag{9}
\]

Existence of these auxiliaries is equivalent to feasibility of the affine
coordinate on all of `Z`: its exact range is
`[a_i-sum rho_j |B_ij|,a_i+sum rho_j |B_ij|]`.

For bound-gradient signs, introduce `s_ij>=T_ij` and `s_ij>=-T_ij`.
For `i in K_l` impose `gamma_i-sum rho_j s_ij>=0`; for `i in K_u`
impose `-gamma_i-sum rho_j s_ij>=0`. These are again equivalent to
the required sign on the entire box. All coefficients in (8) are linear
in the unknown `a,B`, so the complete system is an LP feasibility problem
with a polynomial number of variables and constraints.

If it is feasible, define affine lower multipliers by the gradient on
`K_l` and zero elsewhere; define upper multipliers by minus the gradient
on `K_u` and zero elsewhere. Equations (7) prove stationarity,
nonnegativity, and complementarity. If the LP is infeasible, necessity
of (7) proves that no real affine optimal response exists.

All intermediate data have polynomial encoding length. Exact rational
convex QP gives `yhat` of polynomial length; the central gradient has
polynomial length, and so does a feasible point of the final rational LP.
A rational affine selector therefore exists whenever a real
one does. When `k=0`, solve the single private QP and return a constant
response. Empty private blocks require no work.

## 5. Why one arbitrary central active face is insufficient

For a positive definite `C`, the central optimizer is unique. With a
singular `C`, the active bounds of an arbitrary central optimizer can be
misleading. The common-gradient partition avoids that problem directly.

Consider

\[
  \phi_z(y)=(y_1+y_2-z)^2,\qquad
  Y=[0,1]^2,\quad Z=[0,2].                           \tag{10}
\]

The parameter-only term `z^2` may be dropped to obtain (1). At `z0=1`,
the optimizer set is the segment `y1+y2=1`. A solver may return `(0,1)`;
fixing both of those bounds would give a constant response that is wrong
at other parameters. But the common central gradient is zero, so
`K_l=K_u=empty`, and
the final LP returns an affine response, for example `(z/2,z/2)`.
Its multipliers are zero, and its conditional value is exactly zero
for the full squared expression in (10).

The theorem recognizes the affine-selector class, not every convex
recourse map. For example, minimizing `(y-z)^2` over `y in [0,1]` for
`z in [-1,2]` gives the unique clipped response. No affine selector exists,
and the recognition LP is infeasible.

## 6. Positioning and verification

Affine optimizers on critical regions are classical in multiparametric
quadratic programming; see [Bemporad, Morari, Dua, and Pistikopoulos
(2002)](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf).
The present argument records an exact whole-box recognition procedure,
including a singular private Hessian, for the certificate used by this
continuation. Its ingredients are convex-QP optimal-face identities,
affine range tests, and linear programming. No originality claim is made.

The scoped diagnostic command is

```sh
python3 -B research-20261002-decomposition/negative-curvature/adversary/check_affine_selector_recognition.py
```

The checker uses supplied exact central optimizers and verifies their
KKT conditions, then checks the gradient partition and recognition LP on
small examples. Its final run passed 15 fixtures: 11 affine selections
were accepted and four nonaffine responses rejected. An independent
enumeration of 32 possible global active patterns agreed, and 205 exact
pointwise KKT checks passed. It also rejected one incorrect central
optimizer and reproduced the false negative from fixing the arbitrary
central vertex in (10).

The diagnostic uses exact SymPy linear algebra and a small rational
Fourier–Motzkin feasibility routine, with every returned point checked
against its original constraints. The first attempted diagnostic backend,
SymPy 1.14.0 `lpmin`, returned an infeasible candidate on the singular
example; the independent constraint check caught it, and that backend
was replaced before the successful final run. This was a diagnostic
implementation issue, not a failed mathematical claim.

Neither the finite elimination routine nor active-pattern enumeration is
claimed to have polynomial runtime. The theorem's polynomial bit bound
uses standard exact convex-QP and LP algorithms. This diagnostic does not
benchmark a general exact QP solver or the full sparse global algorithm.
Both the checker author and the coordinating reviewer ran the displayed
command successfully. The linked independent mathematical review approved
the final central-gradient formulation. No project-wide checks or CI
inspection were run.
