# Separator moments in finite-horizon mixed-integer control

Date: 2026-09-22. Status: supporting research screen and proofs; a fresh
[independent review](review-20260922-moment-control.md) found no substantive gap.
The transport proof is a synthesis of standard ideas,
not a claim of a new approximation theorem. The fixed-data lower example below
is the most useful conclusion of this screen.

## Scope and principal conclusions

Matching finitely many state moments between exact local transition measures
admits feasible forward repair when actions are independent of the continuous
state and the state domain is invariant. Disaggregating the matching equations
by a finite automaton state preserves admissible mode words exactly. Incremental
stability controls repair cost, including when individual modes expand.

These statements concern **actual measures supported on exact local feasible
sets**. A truncated positive semidefinite moment matrix need not have such a
representing measure. This distinction prevents interpreting the theorem as a
finite-order SOS extraction result.

Even fixed two-stage data, one continuous state, two modes, affine reset
dynamics, and polynomial constraints have a degree-k separator gap exactly
`2 E_k(|x|)`, where `E_k` is best uniform polynomial approximation error on
`[-1,1]`. Hence the gap is Theta(1/k). Increasing smoothness of the input
polynomials or strengthening state contraction does not by itself improve
this worst-case rate. The value function can have a switching kink.

## A fixed-data sharp obstruction

Consider the following problem, whose data do not depend on k:

\[
 \min h-zx,\qquad
 x=u,\quad -1\le u\le1,\quad u\le h\le1,\quad -u\le h,
 \quad z\in\{-1,1\}.
 \tag{1}
\]

Every feasible point has `h-zx >= |u|-|u| = 0`, and equality is attainable.
Thus the true optimum is zero. Stage zero chooses the action `(u,h)` in the
fixed triangle `|u| <= h <= 1`, incurs cost h, and resets the state to u.
Stage one chooses z, incurs cost `-zx`, and resets the state to zero. Both
transition maps are 0-Lipschitz in their incoming state. The initial state is
fixed and irrelevant. Both action domains are state independent. All local
constraints are linear; the sole bilinear term is the binary-continuous cost.
This is also exactly reformulable as a small MILP.

Let R_k be the relaxation with an arbitrary probability measure on the first
stage feasible set and an arbitrary probability measure on `(x,z)` in
`[-1,1] x {-1,1}`, matching `u^j` and `x^j` for `j=0,...,k`. The local support
sets are exact. Optimizing conditional h and z gives

\[
 R_k=\inf_{\nu,\mu}\left\{
 \int |u|\,d\nu-\int |x|\,d\mu:
 \int t^j\,d\nu=\int t^j\,d\mu\quad(0\le j\le k)
 \right\}.
 \tag{2}
\]

**Proposition 1.** For every k >= 0,

\[
 R_k=-2E_k(|x|;[-1,1]). \tag{3}
\]

More generally, if X is compact, V is a finite-dimensional subspace of C(X)
containing constants, and f is continuous, then

\[
 \max_{\mu,\nu\in\mathcal P(X):\,\mu|_V=\nu|_V}
 \int f\,d(\mu-\nu)=2\inf_{v\in V}\|f-v\|_\infty.
 \tag{4}
\]

**Proof.** For the upper bound subtract v from f and bound the integrals
against two probability measures. Write E for the right-hand approximation
distance before multiplying by two. If E=0 the result follows. Otherwise
Hahn--Banach applied to the quotient by V gives a norm-one bounded linear
functional ell annihilating V and satisfying ell(f)=E. The Riesz representation
theorem gives a signed measure sigma with total variation one. Because
constants belong to V, sigma(X)=0, so its positive and negative parts each
have mass one half. Taking `mu=2 sigma_+` and `nu=2 sigma_-` proves equality.
The feasible set of measure pairs is weak-star compact, so the maximum is
attained. Equation (2) applies (4) with f=|x|. QED.

Bernstein's classical approximation theorem gives

\[
 \lim_{k\to\infty}kE_k(|x|)=\beta>0,
 \qquad -kR_k\longrightarrow2\beta.
 \tag{5}
\]

Lubinsky's [primary research paper on Bernstein constants](https://lubinsky.math.gatech.edu/Research%20papers/BrnstnDec05CA.pdf),
Introduction, reviews this limit and the numerical value near 0.280169499.
The present note invokes that classical theorem; it does not reprove its
asymptotic analysis or certify the displayed numerical constant.

Exact small-degree witnesses are useful checks. For k=1, take `nu=delta_0`
and `mu=(delta_-1+delta_1)/2`, obtaining gap one; the constant approximant
1/2 gives the matching upper bound. For k=2 and k=3, take

\[
 \nu=\tfrac18\delta_{-1}+\tfrac34\delta_0+\tfrac18\delta_1,
 \qquad \mu=\tfrac12\delta_{-1/2}+\tfrac12\delta_{1/2}.
\]

Their first three moments agree, whereas their absolute-value expectations
are 1/4 and 1/2. The approximant `p(x)=x^2+1/8` has error at most 1/8:
on `s=|x| in [0,1]`, `p(x)-|x|=(s-1/2)^2-1/8`. Hence the gap is exactly 1/4.

**Limitations.** This is an obstruction to the specified separator feature
architecture, not to all relaxations or all solvers. Matching the extra
feature |x| makes this example exact immediately. Branching at x=0 also
removes the difficulty. A global formulation easily recognizes the valid
inequality `h-zx >= 0`. No complexity lower bound for solving (1) is claimed.
The significance is that the obstruction needs neither k-dependent data,
many modes, a growing horizon, nor expansive dynamics.

## Feasible repair with exact finite-state logic

Let X be a compact subset of Euclidean space. At t=0,...,T-1, a finite
automaton occupies state q_t, an action a_t chooses a legal edge to q_{t+1},
and the continuous state obeys

\[
 x_{t+1}=F_t(x_t,a_t),\qquad c_t=c_t(x_t,a_t).
\]

Allowed actions can depend on t and q_t, including the selected edge, but
not on x_t. Assume these domains are compact metric spaces, F_t and c_t are continuous
on each edge, `F_t(X,a) subset X`, and c_t is L_t-Lipschitz in x uniformly
over actions. The initial `(q_0,x_0)` is fixed and the final automaton state
must be accepting. A terminal cost can be included as a final action-free
stage. There are no additional state-dependent constraints beyond X.

For each t, let lambda_t be an actual probability measure on feasible local
records `(q,x,a,q',y)` with `y=F_t(x,a)`. Its initial marginal is fixed when
t=0 and its final q marginal is accepting when t=T-1. At every separator
t=1,...,T-1, write alpha_t for the preceding output marginal `(q,y)` and
beta_t for the next input marginal `(q,x)`. Assume their q masses agree.
Let

\[
 \delta_t=\min_{\pi:\,\pi_1=\alpha_t,\,\pi_2=\beta_t,
                              \,q=q'\ \pi\text{-a.s.}}
                   \int\|y-x\|\,d\pi.
 \tag{6}
\]

Thus delta_t is the sum, over q, of q's mass times the Wasserstein distance
of the conditional continuous-state marginals. Zero-mass q states contribute
zero. Compactness ensures the minimum exists.

**Proposition 2.** Suppose every F_t is rho-Lipschitz in its incoming
continuous state, with 0 <= rho < 1. There is a probability law on exactly
feasible full trajectories preserving the joint action/automaton word of a
gluing of the local records and satisfying

\[
 \mathbb E J\le C_{\rm loc}+
 \sum_{s=1}^{T-1}\delta_s
                  \sum_{t=s}^{T-1}L_t\rho^{t-s},
 \qquad C_{\rm loc}=\sum_t\int c_t\,d\lambda_t.
 \tag{7}
\]

In particular, at least one feasible deterministic trajectory has objective
at most the right side. If `L_t <= L`, the additive bound is
`L sum_s delta_s/(1-rho)`.

**Proof.** Choose optimal separator couplings in (6). Disintegrate each
local measure and each coupling on their shared marginals. Successively
sample the resulting kernels along the chain. This standard gluing
construction retains every local lambda_t and every chosen coupling.
It also joins q states exactly, hence produces an admissible automaton word
from the prescribed initial state to an accepting final state.

Use uppercase X_t,Y_{t+1},A_t for the local record variables. Start the
repaired trajectory at x_0 and define
`Xhat_{t+1}=F_t(Xhat_t,A_t)`. Its actions remain legal because their domains
are independent of the continuous state, and invariance keeps every repaired
state in X. Define `e_t=||Xhat_t-X_t||` and
`Delta_t=||Y_t-X_t||` for separators. Then e_0=0 and

\[
 e_{t+1}\le\rho e_t+\Delta_{t+1},\qquad
 e_t\le\sum_{s=1}^t\rho^{t-s}\Delta_s.
\]

The first recurrence is used only up to separator T-1. Lipschitz continuity
of the costs, `E Delta_s=delta_s`, and interchanging finite sums give (7).
The repaired trajectory is feasible almost surely. A random variable cannot
be strictly larger than its expectation everywhere up to null sets, proving
the deterministic existence assertion. QED.

The local actions remain jointly distributed as in the chosen gluing; there
is no assertion that an arbitrary preselected global action law is preserved.

## Finite features, moment degree, and a posteriori rounding

Suppose at each q the separator marginals match all functions in a finite
space V containing constants. Define

\[
 A(V,X)=\sup_{\operatorname{Lip}(f)\le1}
                         \inf_{v\in V}\|f-v\|_\infty.
\]

Kantorovich--Rubinstein duality and subtraction of v show
`delta_t <= 2 A(V,X)`. Importantly, disaggregation by q introduces no factor
equal to the number of automaton states: the conditional bounds are weighted
by masses summing to one. The number of matching equations does grow with
the number of q states.

For a fixed-dimensional box and all polynomials of total degree at most
`k>=1`, Jackson approximation gives `A(V,X) <= C_X/k`. If `p*` is the
true total-cost optimum and `r_k` the infimum over these exact local measures,
the normalized gap, meaning total cost divided by the horizon `T`, satisfies
`(p*-r_k)/T <= 2 L C_X/((1-rho)k)`. The constant depends on dimension,
the domain scale, and the chosen norm. It is not a dimension-free assertion.
The basic rate is also accessible from Lipschitz Bellman functions and the
classical approximate linear programming argument; it should not be
marketed as novel by itself.

With explicit finitely supported local measures, (6) is a finite transport
LP and the gluing consists of finite probability kernels. Each sample can
be repaired by forward simulation. If B is the transport bound in (7) and
ell is a certified lower bound on the original optimum, then

\[
 J-\ell\ge0,\qquad \mathbb E(J-\ell)\le C_{\rm loc}-\ell+B=:D.
\]

For D>0, Markov's inequality gives a sample of cost at most `ell+2D` with
probability at least one half. The best of N independent repaired samples
has this guarantee with probability at least `1-2^{-N}`. If D=0, optimality
holds almost surely. This is a feasible rounding guarantee once actual local
measures and a lower bound are available; computing those inputs efficiently
is a separate requirement. It is invalid to treat C_loc itself as a global
lower bound merely because the supplied local measures are feasible.

## Beyond one-step contraction

Suppose each selected edge/action has a Lipschitz factor lambda_t(a_t), and
every admissible complete action word satisfies, uniformly over all its
subwords,

\[
 \prod_{j=s}^{t-1}\lambda_j(a_j)\le C\rho^{t-s},
 \qquad 0\le s\le t\le T,\quad C\ge1,\quad 0\le\rho<1.
 \tag{8}
\]

The same proof replaces `rho^(t-s)` in the pointwise error recurrence by
the product of factors, then uses (8). The bound becomes
`C L sum_s delta_s/(1-rho)`. This allows expanding individual modes when
the accepted words force enough subsequent contraction. One cannot replace
(8) by an unqualified average contraction statement about one-stage marginals:
the factors and separator errors are correlated under the gluing.

Automaton-dependent norms can certify analogous one-step bounds. This is
standard constrained-switching stability structure; see Philippe, Essick,
Dullerud, and Jungers, [Stability of discrete-time switching systems with
constrained switching sequences](https://arxiv.org/abs/1503.06984).
Their multinorm/CJSR theory treats linear switched dynamics. Applying an
available incremental stability certificate to separator repair is the
limited synthesis claimed here; no new stability criterion is established.

## Literature screen and novelty assessment

- de Farias and Van Roy, [The Linear Programming Approach to Approximate
  Dynamic Programming](https://www.mit.edu/~pucci/discountedLP.pdf), 2003:
  basis-function value approximations and approximation-error bounds.
  The control-value upper estimate here is closely related; the different
  object is an explicit repair of supplied primal local measures.
- Savorgnan, Lasserre, and Diehl, *Discrete-Time Stochastic Optimal Control
  via Occupation Measures and Moment Relaxations*, CDC 2009,
  [DOI](https://doi.org/10.1109/CDC.2009.5399899): polynomial control, moment
  relaxations, and Bellman-dual control recovery. Bibliographic abstract was
  inspected; a full theorem comparison remains necessary.
- Han, Jiao, and Weissman, [Local moment matching](https://proceedings.mlr.press/v75/han18b.html),
  COLT 2018: moment matching, polynomial approximation, and Wasserstein
  distribution estimation. The general approximation/moment duality in (4)
  is already given with its exact factor two in Lemma 25, including a
  translated absolute-value application. It is not a new duality theorem.
- Lubinsky's paper cited above: supplies the classical Bernstein asymptotic
  used in the fixed-data example. That rate is an imported theorem.
- Soheili, Nadarajah, and Yang, [Weakly Time-Coupled Approximation of Markov
  Decision Processes](https://arxiv.org/html/2603.12636v1), March 2026:
  continuous exogenous stochastic states, finite deterministic endogenous
  states, and a basis architecture between ALP and pathwise optimization.
  Sections 1--2 were examined. Its method and computation claims are distinct
  from deterministic state repair, but it reinforces the need not to claim
  that weak time coupling or basis approximation is itself new.
- Barz and Glanzer's [ALP encyclopedia chapter](https://doi.org/10.1007/978-3-030-54621-2_818-1)
  was located as broader background; only metadata/reference information was
  inspected, so no theorem-level exclusion is based on it.

The screen supports preserving the fixed-data obstruction and the explicit
rounding theorem as useful ingredients. It does not establish priority or a
standalone publishable contribution. A stronger target is a sharp feature
budget law for arbitrary interfaces, together with an application-specific
choice of features that avoids the generic dimensional barrier. That
direction requires its own literature comparison and adversarial review.

## Verification record and open concerns

The proof of (4) is functional analytic, not computational. The asymptotic
lower rate rests on the cited Bernstein theorem. The accompanying exact
rational check verifies only the k=1,2,3 witnesses and their moment identities;
it does not verify asymptotics, measure gluing, or independent novelty.

Targeted command: `python code/research_20260922/check_moment_control.py`.
The independent reviewer ran this command successfully and reconstructed
both propositions and the incremental-stability extension. No project-wide
verification or CI inspection was performed for this note.

Remaining concerns are state-dependent action feasibility, extraction of
actual measures from truncated SDP data, dimension dependence of useful
feature spaces, and prior explicit primal repair results. These limitations
must accompany any stronger practical or novelty claim.
