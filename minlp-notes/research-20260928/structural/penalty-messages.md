# Exact separator penalties and bounded Lipschitz messages

Date: 2026-09-28. Status: supporting consequences of the
[repair theorem](repair-probe.md), using classical transport duality and
tree dynamic programming. Novelty is unestablished. These statements concern exact local
probability measures and global local-set oracles, not a finite solver.

Use the compact spaces, separator maps, tree, product domain `K`,
nonempty feasible set `F`, and residuals `r` and `R` from the repair
note. Let `c_v:K_v -> R` be continuous local costs. Put

\[
 c(z)=\sum_v c_v(z_v),\qquad p^*=\min_{z\in F}c(z).
\]

**Proposition 1.** For every finite `lambda >= 0`,

\[
 \min_{\mu_v\in\mathcal P(K_v)}
 \left\{\sum_v\int c_v\,d\mu_v+\lambda R(\mu)\right\}
 =\min_{z\in K}\{c(z)+\lambda r(z)\}.
 \tag{1}
\]

**Proof.** Every tuple gives a family of Dirac laws, proving the
left side is no greater. Conversely, jointly realize all optimal edge
couplings of a family of bag laws, as in equation (5) of the repair note.
The left objective is the expectation of `c(Z)+lambda r(Z)` under this
joint law and is therefore at least its minimum over `K`. Compactness
gives attainment on both sides. ∎

This is an infinite-dimensional convex formulation of the ordinary
deterministic penalty problem. Its convexity does not remove the cost
of representing probability measures or solving the local subproblems.

**Proposition 2.** Let

\[
 C_*:=\sup_{z\in K:r(z)>0}\frac{\operatorname{dist}_D(z,F)}{r(z)},
 \tag{2}
\]

with value zero when the indexed set is empty. A finite `lambda >= 0`
makes (1) equal to `p*` for **every** family of local 1-Lipschitz costs
if and only if `lambda >= C*`. The convention is that no finite value
satisfies this condition if `C*` is infinite.

**Proof.** If `lambda >= C*`, nearest feasible repair gives

\[
 p^*\le c(z)+\operatorname{dist}_D(z,F)
       \le c(z)+\lambda r(z).
\]

Taking the minimum and using a feasible optimizer gives equality.
If `lambda < C*`, choose `a in K` with
`dist_D(a,F)>lambda r(a)` and define `c_v(x)=d_v(a_v,x)`.
These costs are 1-Lipschitz, the true minimum is `dist_D(a,F)`, and
the penalized value at `a` is `lambda r(a)`, strictly smaller. ∎

At the threshold, infeasible minimizers may tie feasible minimizers.
If `C*` is finite and `lambda > C*`, every deterministic minimizer
of the penalty is feasible. Indeed, for every infeasible `z`, its
nearest feasible repair has strictly smaller penalized objective.

## Exact dual messages

Choose an orientation of each edge `e=vw`, with `v` its tail and `w`
its head. Replace `S_e` by the compact union of the two separator-map
images and choose an anchor `s_e^0` in that union. Let

\[
 \Phi_e^\lambda=
 \{\phi\in C(S_e):\operatorname{Lip}(\phi)\le\lambda,
                         \ \phi(s_e^0)=0\}.
\]

For a collection of such potentials, define

\[
 q_v^\phi(x)=c_v(x)
 +\sum_{e:\,v\text{ tail}}\phi_e(p_{ve}x)
 -\sum_{e:\,v\text{ head}}\phi_e(p_{ve}x).
\]

**Proposition 3.** The value in (1) equals the attained maximum

\[
 \max_{\phi_e\in\Phi_e^\lambda}
       \sum_v\min_{x\in K_v}q_v^\phi(x).
 \tag{3}
\]

**Proof.** Every allowed potential satisfies
`phi_e(s)-phi_e(t) <= lambda d_e(s,t)`. Summing over a tuple
shows that (3) never exceeds the deterministic penalized value.

For attainment, root the tree and orient every edge from parent to
child. Define the following functions from leaves toward the root:

\[
 A_v(x)=c_v(x)+\sum_{w:\,w\text{ child of }v}
                    M_w(p_{v,vw}x),
\]
\[
 M_v(s)=\min_{x\in K_v}
       \{A_v(x)+\lambda d_{pv}(p_{v,pv}x,s)\}
       \quad(v\ne\text{root},\ p=\text{parent of }v).
\]

These are continuous functions, and each `M_v` is `lambda`-Lipschitz
by the triangle inequality. Ordinary tree elimination gives the
penalized minimum as `min A_root`. Use `phi_pv=M_v` before anchoring.
For a nonroot vertex, its dual local expression is
`A_v(x)-M_v(p_v,pv x)`. Its minimum is zero: the expression is
nonnegative by using `x` as a candidate in the definition of `M_v`;
at a minimizer `x*` of `A_v`, the nonnegative metric term gives
`M_v(p_v,pv x*) >= min A_v`, so equality holds. The root contributes
`min A_root`. Subtracting each potential's value at its anchor changes
the two incident bag minima by opposite constants and leaves their
sum unchanged. Thus the constructed anchored potentials attain (3). ∎

For completeness, the dual identity between local laws and potentials
also holds on graphs with cycles: apply Kantorovich--Rubinstein duality
to each edge and compact minimax to the bag laws and anchored
Lipschitz balls. The latter are compact in uniform norm by
Arzelà--Ascoli. The tree is required for equality with the
deterministic penalty in (1). On a consistent feasible tuple the
potential terms cancel, so every choice of potentials supplies a
valid lower bound for `p*`.

Together, Propositions 2 and 3 characterize the smallest common
Lipschitz bound that suffices to certify the optimum for every
1-Lipschitz local objective. It is exactly the deterministic repair
constant. This is a statement about the existence of dual certificates,
not a method for computing the constant or those certificates.
Ordinary conditional feasible value functions may be discontinuous;
the functions in (3) are dual separator potentials for the penalized
problem and should not be identified with those conditional values.

For example, let a root bag contain `t in [0,1]`, and let its child
contain `(s,y)` with `y in {0,1}` and `0 <= s <= y`. Require `t=s`.
Use the metrics `|Delta t|` and `|Delta s|+|Delta y|`, and the costs
`-t` and `y`. Here `h(t,s,y)=r(t,s,y)=|t-s|`: changing only the root
to `s` proves the upper bound, and the triangle inequality proves
the reverse bound. Thus `C*=1`.

The child's hard conditional message is zero at `s=0` and one at
every `s>0`, so it is discontinuous. Its penalized message is
`M_lambda(t)=min(lambda t,1)`. At the sharp threshold `lambda=1`,
the potential `M(t)=t` certifies the true optimum zero through the
two local inequalities `-t+t=0` and `y-s>=0`. This small MILP is an
illustration of the distinction, not a separate novelty claim.

## Prior theory and practical limits

Equation (1) uses classical tree marginal gluing. Equation (3) is
a tree dynamic-programming construction with a metric infimal
convolution; it also follows from transport duality and minimax. The link from
metric error bounds to exact penalties is classical. The focused
formulation here is their joint interpretation for hard-support bag
models, with a sharp universal threshold and an explicit distinction
between dual potentials and feasible value functions. The
[source audit](source-audit.md) records the closest inspected transport
and error-bound results. It does not establish external novelty of
these consequences.

For a solver, a usable finite `C*` would permit bounded-slope
separator approximations and exact penalty certificates while keeping
hard local integer/nonlinear constraints inside each bag oracle.
Efficiently computing a useful constant, approximating the potentials,
and certifying the local minima remain necessary. The strongly
contractive terminal example in the repair note has infinite `C*`,
so no finite universal Lipschitz message bound follows there.
