# Independent audit of finite and residual OBBT certificates

Date: 2026-10-05. Scope: October finite-witness certificates, cutoff reuse,
integer rounding, objective ceilings, the matrix residual theorem, and the
exact reference checker and closure driver. The audit is complete for these
inputs. The findings and complete proofs below are ready for the certificate
writer. The mathematical results are sound after correcting the upper-residual
warning and stating the lifted attainment premise explicitly.

## Findings available for revision

1. The current-round primal bounds, finite protected-box induction, pairwise
   cutoff-frontier construction, and matrix supersolution proof are sound
   under their stated hypotheses. The residual proof does **not** require
   `rho(M)<1` when a finite nonnegative supersolution is supplied.
2. The projected and lifted formulations need an explicit attainment
   distinction. Compactness of `K_U(B)` gives coordinate support attainment;
   it does not imply that the lifted objective infimum defining `phi_B(x)`
   is attained. Identify `K_U(B)` with the projection of the lifted cutoff
   set only when that extra premise holds. The reference McCormick family
   has compact lifted relaxations, so its implementation is unaffected.
3. The finite certificate is complete **for checking whether a specified
   compact candidate box is fixed**: `T_U(P)=P` if and only if at most `2n`
   feasible points attain its coordinate faces. This does not make the
   floating proposal routine a complete search for protected boxes.
4. `max_W v` is the exact cutoff threshold for retaining **every point** of
   a fixed pool `W`. It can be stronger than necessary for retaining face
   coverage. The exact cutoff threshold for some covering subpool is the
   maximum, over faces, of the minimum objective among that pool's points
   on the face. A separate full-face optimization gives the exact cutoff
   threshold for protecting the **same box** using any available witnesses.
   Neither threshold is a necessary condition for the existence of some
   different protected inner box.
5. **A mathematical correction is required in the upper-residual warning.**
   The archived claim that `e-dbar` is not a safe after-round bound when
   `dbar>=d` and `dbar+Me<=e` is false. Under precisely those premises, the
   exact tail after the first Jacobi round is at most `Me`, and
   `Me<=e-dbar`. This does not authorize subtracting a residual bound after
   a partial or inexact first update. The corrected theorem below separates
   these cases.

## 1. Projected order, lifted order, and attainment

Let `phi_B(x)=inf{v(z): z in R(B), projection_x z=x}`, with `+infinity`
for an empty fiber. Set `K_U(B)={x in B: phi_B(x)<=U}` and
`T_U(B)=hull K_U(B)`. The projected order assumption is

\[
 P\subseteq B\quad\Longrightarrow\quad
 \phi_B(x)\le\phi_P(x)\qquad(x\in P).
\]

This assumption suffices for all box-containment results expressed in terms
of `K_U` and `T_U`. It gives `K_U(P) subset K_U(B)` directly. It does not
assert that an individual lifted point feasible on `P` remains feasible on
`B`. To reuse exactly the same lifted points and affine objective values,
assume the stronger lifted order `R(P) subset R(B)` with the same variables
and objective. Lifted order implies projected order by taking infima over
nested fibers.

For the lifted cutoff set `R_U(B)={z in R(B): v(z)<=U}`, one always has
`projection_x R_U(B) subset K_U(B)`. The converse needs attainment whenever
`phi_B(x)<=U`. A sufficient assumption is that `R(B)` is nonempty compact
and the common objective is continuous. More locally, compactness and
nonemptiness of each relevant fiber suffice.

**Counterexample to inferring fiber attainment from compact projected
sublevels, even at an exact incumbent cutoff.** Take the original objective
`f(x)=x^2` on `B_0=[-1,1]`, with its exact optimum and incumbent cutoff
`U=f*=0`. For each subbox `B`, set

\[
 R(B)=\{(x,t,s):x\in B,\ t\ge0,\ s\ge0,\ ts\ge x^2\},
 \qquad v(x,t,s)=t.
\]

The set is closed and convex: its common cone constraint is equivalent to
`t+s >= sqrt((t-s)^2+4x^2)`, a norm cone inequality. The family is lifted
monotone, and the common original lift `(x,x^2,1)` is feasible with the
correct objective, so validity holds. Nevertheless `phi_B(x)=0` for every
`x`, since taking `s` arbitrarily large allows `t=x^2/s` to approach zero.
For `x!=0`, that infimum is not attained. Thus `K_0(B_0)=B_0` is compact,
while `projection_x R_0(B_0)={0}`. Compact projected sublevels alone do
not justify interpreting lifted cutoff support problems as the operator
`T_U`, even when the cutoff is justified by an exact original incumbent.

**Suggested foundations wording.** Assume the nonempty projected sublevel
sets used for coordinate supports are compact. When `phi_B` is defined as
a lifted objective infimum and coordinate OBBT is implemented by a lifted
cutoff set, also assume those fiber infima are attained at every relevant
projected sublevel point; compact lifted relaxation sets are sufficient.
The finite reference LP family satisfies this stronger premise.

## 2. Finite completeness for a fixed candidate box

**Proposition.** Let `P=[a,b]` be a nonempty box, and assume `K_U(P)` is
nonempty and compact. Then the following are equivalent:

1. `T_U(P)=P`.
2. For every coordinate `i`, points in `K_U(P)` attain `x_i=a_i` and
   `x_i=b_i`.
3. There is a finite pool `W subset K_U(P)` with `hull W=P`, and a pool of
   at most `2n` points suffices.

**Proof.** If `T_U(P)=P`, the minimum and maximum of each continuous
coordinate function on compact `K_U(P)` are `a_i` and `b_i`, respectively.
Choose one minimizer and one maximizer per coordinate, omitting duplicates.
These at most `2n` points have hull `P`. Conversely, if such a pool exists,
`P=hull W subset hull K_U(P) subset P`; hence equality holds. Degenerate
coordinates cause no difficulty because the two faces coincide. No convexity
assumption is needed. QED.

Under lifted attainment, replace each chosen projected point by a feasible
lift in `R_U(P)`. The same statement then gives a finite lifted certificate.
Without compactness, equality of the closed hull and `P` need not give finite
face witnesses: `K=(0,1)` has closed coordinate hull `[0,1]` but no point on
either face.

**Rational completeness of the checker at a prescribed rational box.**
Suppose the lifted relaxation at `P`, its cutoff, and all endpoints of `P`
have rational linear data. If `P` is fixed, each face has a nonempty rational
polyhedron of feasible lifts, obtained by adding the face equality. Every
nonempty rational polyhedron has a rational point; in the bounded reference
family a rational vertex can be chosen. Selecting one rational feasible
point per face produces a certificate accepted by exact row and endpoint
checks. Therefore a prescribed rational fixed box admits a rational finite
certificate. This does not establish that every protected box has rational
endpoints, that an exact fixed point is reached in finitely many rounds, or
that the floating proposal/recovery routine will find that certificate.

## 3. Exact cutoff thresholds for a pool and for a prescribed box

Let `W` be a finite lifted pool feasible in `R(P)` and assume its original
coordinates have hull `P`. Let `q_j=v(z_j)` and let `F` range over the `2n`
coordinate faces, counting coincident faces harmlessly. Define

\[
 \tau_W(P)=\max_F\ \min_{j:\,x_j\in F}q_j.
\]

Each inner minimum is over a nonempty finite set because `W` covers every
face. All quantities are exact once the pool is fixed.

**Proposition.** The eligible subpool `W_U={z in W: v(z)<=U}` has coordinate
hull `P` if and only if `U>=tau_W(P)`. Thus `tau_W(P)` is the smallest cutoff
at which some subpool of `W` certifies the same box `P`.

**Proof.** The eligible subpool has hull `P` precisely when every face has
at least one eligible point. For a face `F`, this happens precisely when
`U` is at least the minimum objective of the pool's points on `F`. Requiring
this simultaneously for all faces is the displayed maximum. For sufficiency,
one may retain a least-objective pool point on each face, giving at most `2n`
points. QED.

By contrast, `U_W=max_{z in W}v(z)` is the smallest cutoff retaining all
points of the original pool. It is a safe reuse threshold, but it can be
larger than `tau_W(P)` because an expensive point may be redundant for face
coverage. For example, with `P=[0,1]^2`, objective `v(x)=x_1+x_2`, and
pool `W={(0,0),(1,0),(0,1),(1,1)}`, one has `U_W=2` and `tau_W(P)=1`.
The first three points alone cover all four faces at cutoff `1`.

Convex mixing does not lower `tau_W(P)` for protection of this same box.
If a convex combination of points in `P` attains a coordinate face, every
point with positive weight must attain that face. Its affine objective is
then at least the minimum pool objective on that face. Consequently

\[
 \hull\bigl(\conv(W)\cap\{v\le U\}\bigr)=P
 \quad\Longleftrightarrow\quad U\ge\tau_W(P).
\]

Pairwise mixtures can give useful witnesses on a **smaller candidate hull**
at tighter cutoffs; protection of that hull still requires rebuilding and
checking its rows. The equivalence above concerns the fixed hull `P` only.

There is also a full-relaxation version. Assume `R(P)` is compact and `v`
continuous. Set

\[
 \mu_F(P)=\min\{v(z):z\in R(P),\ x\in F\},\qquad
 \tau(P)=\max_F\mu_F(P),
\]

with `mu_F=+infinity` for an empty face fiber. Then

\[
 T_U(P)=P\quad\Longleftrightarrow\quad U\ge\tau(P),
\]

where the left side is understood through the lifted cutoff projection
under the attainment premise above. **Proof:** a face is attained under
the cutoff exactly when its compact face fiber has minimum objective at
most `U`; finite face completeness then supplies the equivalence. QED.

Computing all `mu_F` can require up to `2n` constrained objective LPs.
This result characterizes compatibility of a prescribed box and cutoff;
it does not provide an unconditional inexpensive screening method. A cutoff
below `tau(P)` proves this box is not fixed, but it does not rule out a
different protected box or establish worthwhile solver benefit.

## 4. Corrected matrix residual theorem, including an upper residual

The endpoint convention must be consistent: use `p=(-ell,u)` throughout
the paper. The older theory note uses `(u,-ell)`, which is only a permutation
but requires the same permutation of every matrix and vector.

**Theorem.** Let `F` be the exact Jacobi endpoint map at a fixed cutoff.
Let `D` be an `F`-invariant set of finite valid endpoint vectors, and assume
`F(p)<=p` for every `p in D`. Suppose a fixed nonnegative matrix `M` satisfies

\[
 |F(p)-F(q)|\le M|p-q|\qquad(p,q\in D).
\]

Choose `p_0 in D`, define `p_{k+1}=F(p_k)`, and let
`d=p_0-p_1>=0`. Let `dbar>=d` be a certified nonnegative upper bound.
If a finite vector `e>=0` satisfies

\[
 \bar d+Me\le e,
\]

then the endpoint sequence converges to a finite vector `p_infinity`, and
for every integer `m>=0`,

\[
 0\le p_m-p_\infty\le M^m e.
\]

In particular,

\[
 0\le p_0-p_\infty\le e,\qquad
 0\le p_1-p_\infty\le Me\le e-\bar d\le e-d.
\]

No spectral-radius condition is required. If `rho(M)<1`, the choice
`e=(I-M)^{-1} dbar` is admissible, with equality in the supersolution
inequality. With the exact residual, set `dbar=d`.

**Proof.** Put `Delta_k=p_k-p_{k+1}>=0`. Invariance allows the uniform
estimate to be applied at consecutive iterates. Therefore
`Delta_{k+1}<=M Delta_k`, and induction gives
`Delta_k<=M^k d<=M^k dbar`. From `dbar<=e-Me`, multiplication by each
nonnegative power of `M` and summation yield, for every `N>=1`,

\[
 \sum_{k=0}^{N-1}M^k\bar d\le e-M^Ne\le e.
\]

Hence `0<=p_0-p_N<=e`: the decreasing endpoint sequence is bounded below
componentwise by `p_0-e` and has a finite coordinatewise limit. For every
`N>m`,

\[
 0\le p_m-p_N
 =\sum_{k=m}^{N-1}\Delta_k
 \le M^m\sum_{j=0}^{N-m-1}M^j\bar d
 \le M^m e.
\]

Take `N` to infinity. At `m=1`, the supersolution gives the stated
`Me<=e-dbar<=e-d` chain. If `rho(M)<1`, the nonnegative Neumann series
converges and supplies the displayed inverse formula. QED.

This proves more than simply subtracting the exact first displacement
from a total bound. The extra estimate uses the recurrence on **all later
increments**. Therefore the sentence in `document/certificates.tex` and
`theory/remaining-benefit.md` saying the bound is “not `e-dbar`” should be
replaced. The corresponding assessment in `reviews/theory-review.md`
repeats the same erroneous restriction; its conclusion should not be copied.

**Correct scope warning.** The after-round bound concerns the exact
`p_1=F(p_0)`. An observed movement during a selective, interrupted, or
inexact pass need not be an upper bound on `d`. Even with a separately
valid bound `dbar`, an arbitrary partially updated current state need not
equal `p_1`, so its remaining motion is not automatically bounded by
`e-dbar`. For example, with `F(s)=s/2`, `p_0=1`, `dbar=d=1/2`, and `e=1`,
the exact after-round motion is `1/2`. If no update has been applied, the
current state is still `1` and its remaining motion is `1`, exceeding
`e-dbar=1/2`.

The theorem does not require convexity of `D`; the proof only uses
invariance and the uniform matrix comparison. Convexity is useful when
establishing that comparison by integration of derivative bounds. Nor
does it require order preservation of `F` beyond the separately assumed
deflation `F(p)<=p`. Keep order preservation in the OBBT foundations,
where it is needed for protected-box induction.

**Constructing an upper residual from current primal witnesses.** A
nonempty pool `W subset K_U(B_0)` gives, in the shared order
`p=(-ell,u)`, the vector

\[
 \bar d=\left(\left(\min_{x\in W}x_i-\ell_i\right)_{i=1}^n,
              \left(u_i-\max_{x\in W}x_i\right)_{i=1}^n\right).
\]

The current-round ceiling proposition proves `d<=dbar`, even without
solving the exact directional LPs. Consequently, a separately established
invariant region and uniform matrix bound allow `dbar+Me<=e` to certify
total future exact Jacobi motion **before** computing the first exact
round. The available pool does not establish those additional hypotheses;
their construction can itself be expensive. The bound `Me` still concerns
the state after the exact first round, not the unchanged current box.

**Invariant region from a protected box.** If `P subset B_0` is protected
and `p_P=(-a,b)`, the order interval `D=[p_P,p_0]` consists of valid boxes
containing `P`. Projected order makes `F` order preserving and protection
gives `F(p_P)=p_P`. Thus, for every `p in D`,

\[
 p_P=F(p_P)\le F(p)\le p\le p_0.
\]

This proves `F(D) subset D`. This particular region is compact and convex;
the remaining task is to establish a uniform matrix on the **entire**
interval, not merely at the current LP basis or along sampled iterates.

The limit is a fixed point if it belongs to `D`, because the uniform
matrix estimate makes `F` continuous there. Closedness of `D` is one
sufficient condition. Without that extra premise, the theorem certifies
the limit and its motion without asserting `F(p_infinity)=p_infinity`.

**Why `rho(M)<1` is not necessary for this tail.** On `[0,1]^2`, let
`F(s,t)=(s,t/2)` and use the valid, deliberately loose comparison matrix
`M=diag(2,1/2)`. Starting at `(1,1)` gives `d=(0,1/2)` and the supersolution
`e=(0,1)`, even though `rho(M)=2`. The exact limit is `(1,0)` and total
movement equals `e`. The unstable comparison direction has no initial
or propagated residual in this example. The archived example with
`diag(1,1/2)` is also valid.

For a given nonnegative residual `r`, a finite nonnegative supersolution
`r+Me<=e` exists exactly when the nonnegative series
`sum_{k>=0} M^k r` is componentwise finite. Indeed, a supersolution bounds
every partial sum by the telescoping inequality; conversely, the finite
series sum `s` satisfies `s=r+Ms` by finite-dimensional continuity. This
sum is the least supersolution, since every supersolution bounds its
partial sums. This observation is a precise explanation of the weaker
premise; no new algorithm for constructing the uniform matrix is implied.

For the cutoff perturbation result, retain its stronger condition
`rho(M)<1` (or another premise forcing `M^k |p_U-p_V|` to vanish). A
supersolution for the cutoff perturbation vector alone does not remove
differences between inactive fixed-point coordinates. For instance,
`F_U(s,t)=(s,t/2)` has many fixed points differing in `s`, with zero
cutoff dependence. A residual certificate for one trajectory and a
cross-cutoff comparison of arbitrary fixed points have different premises.

For completeness, the full fixed-point comparison proof is short. Suppose
the common region and cutoff interval satisfy

\[
 |F_U(p)-F_V(q)|\le M|p-q|+h|U-V|,
 \qquad h\ge0,\ M\ge0,\ \rho(M)<1.
\]

For fixed points `p_U,p_V` in the region, set `r=|p_U-p_V|` and
`b=h|U-V|`. Substitution gives `r<=Mr+b`; iteration gives
`r<=M^N r+sum_{k=0}^{N-1} M^k b`. Taking `N` to infinity yields
`r<=(I-M)^{-1}h|U-V|`. This proves a comparison of existing fixed points;
invariance of an arbitrary nonclosed region alone does not establish their
existence. A rational positive vector `v` and rational `q<1` satisfying
`Mv<=qv` give a sufficient exact check of `rho(M)<1`, because the weighted
maximum norm `max_i |z_i|/v_i` has matrix norm at most `q`. Such a check
establishes contraction of the supplied matrix, not its missing uniform
relationship to `F_U`.

## 5. Full protection proof, sequential updates, and objective ceilings

**Theorem.** Assume projected order for the whole relaxation construction.
Let `P=[a,b] subset B_0=[ell^0,u^0]` and let a finite pool
`W subset K_U(P)` have coordinate hull `P`. Starting at `B_0`, consider
any sequence of exact Jacobi rounds or selected directional coordinate
updates, each using this relaxation construction and a cutoff `U_k>=U`.
The relaxation may be rebuilt between individual updates. Every retained
box `B_k=[ell^k,u^k]` contains `P`, and

\[
 0\le \ell_i^k-\ell_i^0\le a_i-\ell_i^0,\qquad
 0\le u_i^0-u_i^k\le u_i^0-b_i.
\]

The same conclusion holds for conservative coordinate updates whose lower
bound never exceeds the exact coordinate minimum and whose upper bound
never lies below the exact coordinate maximum, with updates restricted to
shrinking the current box.

**Proof.** The pool's hull gives
`P=hull W subset T_U(P) subset P`, hence `T_U(P)=P`. Suppose inductively
that the current box `C` contains `P`. Projected order and cutoff order
give `K_U(P) subset K_{U_k}(C)`. Each coordinate face of `P` has a pool
point in this latter set. Therefore its coordinate minimum is at most
`a_i`, and its maximum is at least `b_i`. Updating a selected lower bound
to that minimum cannot pass `a_i`; updating a selected upper bound to
that maximum cannot pass `b_i`. Rebuilding before the next coordinate
does not affect the induction because the current box still contains `P`.
For a frozen Jacobi round, all coordinate extrema obey those inequalities
simultaneously. A conservative update moves no farther inward than the
exact update, and therefore also retains `P`. Each operation shrinks its
input box, so `P subset B_k subset B_0`; reading its endpoints proves the
displayed ceilings. QED.

This proof does not require continuity, convergence to a fixed point,
fairness of the selected directions, or nonlinear feasibility of the pool.
It proves nonemptiness of the relevant relaxation sublevel sets because
the pool remains available in projection. It does **not** prove that the
original sublevel set is nonempty. In the old theory note, replace “even
none if the cutoff is infeasible” by “even none if the original sublevel
set at that cutoff is empty”; a protected certificate itself rules out
emptiness of the relevant relaxation sublevel sets.

For a lifted proof that literally retains the same `z` witnesses, use
`R(P) subset R(C)` and a common objective. Projected order alone guarantees
the existence of suitable projected feasible points, not persistence of
the supplied auxiliary coordinates. This is a distinction in the contract,
not a defect of the projected theorem.

**Example separating projected and lifted order while preserving original
validity.** For a one-dimensional box `B`, let `r=w(B)` and define

\[
 R(B)=\{(x,t,s):x\in B,\ 0\le t\le1,\ s=r(1-t)\},\qquad v=t.
\]

Each lifted set is compact and convex, and `phi_B(x)=0` identically, so
projected order holds. For the original problem `f(x)=1`, the common exact
lift `(x,1,0)` is feasible for every box, so the construction is valid.
However, the minimum-objective lift `(x,0,w(P))` on a strict smaller-width
box `P` is not feasible on `B`; lifted order fails. Projected OBBT and
objective-value bounds remain valid, while reusing that precise lifted
point as a primal LP witness on `B` is unjustified.

### Integer rounding

Coordinate rounding has a simple sufficient extension. Suppose every
integer-coordinate face `a_i,b_i` of the protected box is integral.
Immediately before rounding, the updated endpoints satisfy
`ell_i<=a_i` and `u_i>=b_i`. Then

\[
 \lceil\ell_i\rceil\le a_i,\qquad \lfloor u_i\rfloor\ge b_i,
\]

because `a_i,b_i` are integers. Thus rounding these endpoints retains `P`.
The pool's other integer-coordinate components need not be integral for
this proof: the operation being justified is only coordinate rounding of
continuous-relaxation supports. This condition does not justify an integer
support solve or arbitrary native integer propagation that excludes pool
points for other reasons.

Fractional faces can be removed by correct rounding. For example, with one
integer variable, the continuous relaxation `R(P)=P=[0,1/2]` and constant
objective has fixed box `P`, covered by the witnesses `0` and `1/2`.
Rounding the upper endpoint gives `0`, retaining the original integer point
but removing the fractional protected face.

### Objective ceiling

Define the projected relaxation value

\[
 L(C)=\inf_{x\in C}\phi_C(x).
\]

In the compact lifted reference family this equals the attained minimum
of its common affine objective over `R(C)`. If `x_0 in P` and a known finite
number `v_0` satisfies `phi_P(x_0)<=v_0`, every retained box satisfies

\[
 L(B_k)\le\phi_{B_k}(x_0)\le\phi_P(x_0)\le v_0.
\]

Projected order alone proves this value inequality. A feasible lifted
point `z_0 in R(P)` gives such an upper value `v_0=v(z_0)`; the point does
not have to be an original feasible point. Under lifted order, the simpler
proof retains `z_0` itself in every `R(B_k)` and applies primal weak duality.
Thus lifted order is sufficient for the literal point-retention argument,
not logically necessary for an objective **value** ceiling formulated in
terms of `phi_B`.

Projected order and box shrinking also give `L(B_k)>=L(B_0)`. If a finite
certified current lower bound obeys `L_cert<=L(B_0)`, then

\[
 0\le L(B_k)-L(B_0)\le v_0-L(B_0)\le v_0-L_{\rm cert}.
\]

The premise on `L_cert` concerns this particular relaxation value. A valid
lower bound for the original optimum, or for a stronger native relaxation,
need not lie below `L(B_0)` and cannot be substituted automatically. For
the nonnegative-square three-variable example, `L(B_0)=-3` while the exact
original optimum is `0`; using the original lower bound `0` in place of
`L_cert` would produce the impossible negative ceiling `-3`.

Taking `v_0=min_{z in W}v(z)` already gives a ceiling from the face pool.
An additional primal feasible point on `P` can lower it. Proving the point
objective-optimal is unnecessary. Cut changes, other domain reductions,
or a different relaxation are outside this conclusion unless their own
validity contract preserves the needed projected value or lifted point.

### Original feasible pools

Let `S` be a nonempty finite set of exact original feasible points with
`f(x)<=U`, and let `P=hull S`. Validity gives `S subset K_U(P)`, so `P` is
protected. More strongly, any later box operation obtained from a valid
relaxation at a cutoff at least `max_{x in S} f(x)` must retain all points
of `S`, and therefore must retain their coordinate hull. This argument
continues to apply when new valid cuts change the relaxation, without
requiring persistence of relaxation-only witnesses. In a lifted checker,
one must supply exact original lifts and verify all the rows; floating
incumbent feasibility alone is insufficient. If `S` respects original
integrality, its integer-coordinate hull endpoints are automatically
integral.

## 6. Cutoff mixing, pool frontier, and reuse events

The affine mixing formula is correct under one fixed convex lifted
relaxation. If `v(a)<=U<v(z)`, then

\[
 \theta=\frac{U-v(a)}{v(z)-v(a)}\in[0,1),\qquad
 z_U=(1-\theta)a+\theta z
\]

is feasible by convexity and has objective exactly `U` by affinity. If
`v(z)<=U`, retain `z`. An anchor with `v(a)=U` gives `theta=0`, a valid
degenerate case. An anchor above the cutoff does not suffice. Convexity
and a common affine objective must be stated; the formula is not justified
for arbitrary nonlinear relaxed objectives or unrelated lifted models.

The rebuilding counterexample is correct. On `[-1,1]`, square graph points
`(x,w)=(+1,1),(-1,1)` mixed with `(0,0)` to cutoff `1/4` give
`(+1/4,1/4),(-1/4,1/4)`. Both pass the old endpoint tangents and secant.
On their new original-coordinate hull `[-1/4,1/4]`, the new square secant
is `w<=1/16`; both points fail it. Therefore current convex feasibility
does not prove a protected hull.

**Proposition (full frontier statement).** Let the finite nonempty pool
`W={z_1,...,z_k}` lie in one fixed convex lifted relaxation, with affine
objective values `q_j=v(z_j)`. Let `C_U=conv(W) intersect {v<=U}`. If
`C_U` is nonempty, every minimum and maximum of an original or lifted
coordinate on `C_U` is attained among:

- originals `z_j` with `q_j<=U`;
- pair mixtures with `q_j<U<q_l`, taken at objective exactly `U`.

There are at most `k` original candidates and `k(k-1)/2` possible pair
candidates. In particular, at most `O(k^2)` mixtures suffice without a new
LP; this is a count of candidates, not an assertion that row checking,
rational arithmetic, or data transfer has negligible cost.

**Proof.** Consider the compact coefficient polytope

\[
 \Lambda_U=\{\lambda\ge0:\boldsymbol1^T\lambda=1,
                            q^T\lambda\le U\}.
\]

Its image under `lambda -> sum_j lambda_j z_j` is exactly `C_U`, because
the objective is affine. At an extreme coefficient vector, let `s` be the
number of positive coefficients. If the cutoff is inactive and `s>=2`,
there is a nonzero perturbation supported on those coefficients that
preserves their sum. A sufficiently small perturbation of either sign
preserves nonnegativity and the strict cutoff, contradicting extremality.
If the cutoff is active and `s>=3`, the two homogeneous equations
`1^T h=0` and `q^T h=0` have a nonzero solution on the positive support;
the same two-sided perturbation again contradicts extremality. If `s=2`
and both objective values equal `U`, the cutoff equation is redundant
there and the sum-preserving perturbation still exists. Consequently an
extreme vector has one positive coefficient, giving an eligible original,
or two positive coefficients at distinct objective values. In the latter
case their strictly positive convex weights have average `U`, so the
values strictly straddle `U` and give the stated pair mixture. Each linear
coordinate objective on the compact coefficient polytope attains an
optimum at an extreme vector. Its image is a listed point. QED.

The coefficient proof handles repeated points, equal objective values,
cutoff equality, degenerate coordinate hulls, and affinely dependent
pool points. It does not require the image of each coefficient vertex to
be a vertex of `conv(W)`.

`C_U` is nonempty exactly when some original pool point has `q_j<=U`,
since an affine objective cannot decrease below the least pool value
under convex mixing. An empty frontier proves nothing about feasibility
of the full relaxation.

For a changed box, all pool points used in the theorem must be feasible
in the current rebuilt relaxation. Filtering out failed points yields an
eligible smaller pool, and the theorem remains exact for that smaller
pool. It is not generally exact for the old convex hull intersected with
all new domain rows: mixtures of individually excluded old points can
be feasible, and adding many inequalities to the coefficient polytope
can create vertices requiring more than two positive coefficients. The
implementation's requirement that every supplied point pass current
rows is therefore essential to its stated full-frontier contract.

**Reuse contract.** For a checked protected pool on `P`, a future box
must contain `P`; its cutoff must retain enough points for face coverage;
and the relevant relaxation and row-validity scope must remain compatible.
With the implementation's whole-pool contract the exact arithmetic cutoff
event is `U'<max_W v`; with a reselected covering pool it is
`U'<tau_W(P)`. Crossing either threshold loses that specified certificate,
and does not establish profitability of OBBT. A new node excluding part
of `P` does not automatically preserve `P intersect B'`; that candidate
requires rebuilding and another face check. New valid cuts can remove
relaxation-only witnesses. Equal row arrays alone do not establish
node-local row provenance or authorize moving local cuts between nodes.

## 7. Exact reference checker and closure-driver audit

The code's mathematical contracts agree with the corrected theory:

- `current_round_ceilings` validates every lifted coordinate and current
  row plus cutoff, then returns possible frozen-round improvements. Its
  output consists of upper bounds on benefit, not valid new variable bounds.
- `ProtectedBox.__post_init__` validates feasibility on its own rebuilt
  box and verifies all coordinate extrema. The invariant also holds for
  direct construction, without relying on the factory. Its `required_cutoff`
  is the exact whole-pool threshold, and `objective_ceiling` is the least
  pool objective.
- `verify_protected_box` separately checks containment in the declared
  outer box and satisfaction of the requested cutoff. Its certificate
  does not need optimality of any witness.
- `ProtectedBox.reusable` checks equality of the declared rational model,
  containment of `P`, and cutoff compatibility. As documented, caller
  obligations still include original validity and node-local row scope.
- `mix_for_cutoff` and `cutoff_frontier` perform exact row checks with a
  common affine objective. Above-cutoff old points are checked against
  relaxation rows without the new cutoff, as required for mixing.
- `check_tail_majorant` verifies nonnegative rational dimensions and
  `r+Me<=e`. It correctly leaves uniform sensitivity and exact residual
  provenance as external hypotheses. No code change is needed for the
  corrected upper-residual theorem: supplying `r=dbar` already checks its
  required inequality.

### Discovery is incomplete even with exact endpoint-optimal proposals

The verifier is complete for a supplied valid finite certificate, but the
proposal routine is incomplete for finding one. Failure can arise from
unfortunate auxiliary coordinates even if all proposed coordinate values
are exact optima and their hull really is fixed.

For example, take one square product, outer box `[-1,1]`, fixed rows `x=0`,
and constant objective with cutoff `0`. Every directional coordinate
optimum has `x=0`. The old point `(x,w)=(0,-1)` is feasible and coordinate
optimal. If both endpoint proposals use that point, their hull is `{0}`,
but after rebuilding the square relaxation on `{0}` the auxiliary value
must be `w=0`, so the proposed points fail. The box `{0}` is nevertheless
fixed and has the valid witness `(0,0)`. An exact callback returning
`(0,-1)` makes `discover_protected_box` return `None`. Thus incompleteness
is not solely a floating-point rational-reconstruction issue.

An accepted discovery result supplies a protected **inner** box; it does
not prove that this box equals the exact first Jacobi image of the outer
box. The discovery routine deliberately does not verify endpoint
optimality. The ceilings remain valid because they rely on protection,
not on that equality. Only when the protected box equals the current box
do its zero ceilings establish no further coordinate movement there.

### Exact weak-duality proof for committing a round

For the minimization LP `min c^T z` subject to `Az<=b`, all variable bounds
being explicit rows, let a proposed primal `z*` satisfy `Az*<=b`. Let
`lambda<=0`, `A^T lambda=c`, and `c^T z*=lambda^T b` hold exactly. Every
feasible `z` satisfies

\[
 c^Tz=\lambda^TAz\ge\lambda^Tb=c^Tz^*,
\]

where the inequality follows by multiplying each primal inequality by a
nonpositive multiplier. Thus `z*` is optimal. No constraint qualification,
strong-duality invocation, tolerance, or solver status is needed once
these finite identities have been checked.

The driver uses this proof for all `2n` endpoints on one frozen row array.
For lower directions its objective is `+x_i`; for upper directions it is
`-x_i`, and it records the primal coordinate itself as the upper endpoint.
The resulting candidate is exactly the Jacobi hull. It commits only after
all endpoint proofs pass. If any proposal or exact replay fails before
then, no part of that round is committed; previous certified rounds and
all proposal-call costs remain recorded. This rollback is correct.

After a complete round, the old primal endpoint points are checked on the
new hull. If those checks pass, the finite certificate proves the new
box fixed. If they fail, the committed Jacobi reduction remains correct;
only that particular stopping proof is absent. Continuing on the new
box is appropriate. On the degenerate example above, one further round
forces `w=0` and can supply the missing finite stopping proof.

A round limit properly returns `unfinished`; failed reconstruction
properly returns `inconclusive`. Neither is a proof that a fixed box does
not exist. An optional objective proposal needs only exact primal
feasibility and can improve the ceiling without invalidating an already
checked face certificate if it fails. The reference workflow does not
independently certify native SCIP rows or a nonlinear incumbent.

## 8. McCormick inclusion and constructive examples

For distinct product indices, the four McCormick rows describe the convex
hull of the bilinear graph on the rectangle. The graph on a smaller
rectangle is a subset of the graph on a larger one, so its convex hull
is also a subset. Every selected product lift obeys this inclusion.
Intersecting these sets with the same fixed linear rows and the smaller
original box preserves lifted order of the complete family.

For a repeated square index, one can also view the construction as the
bilinear rectangle hull intersected with the diagonal. Its relaxation
is the two endpoint tangents and the secant, **not** the exact convex
square epigraph. A direct proof of its nesting avoids that confusion.
For `[a,b] subset [ell,u]`, put `t_c(x)=2cx-c^2` and
`s_cd(x)=(c+d)x-cd`. On `[a,b]`,

\[
 t_a(x)-t_\ell(x)=(a-\ell)(2x-a-\ell)\ge(a-\ell)^2\ge0,
\]

\[
 t_b(x)-t_u(x)=(u-b)(u+b-2x)\ge(u-b)^2\ge0.
\]

The affine difference `s_{ell,u}-s_{a,b}` is nonnegative at both endpoints:
its values are `(a-ell)(u-a)` at `a` and `(b-ell)(u-b)` at `b`. It is
therefore nonnegative throughout the interval. The new lower tangents
dominate the respective old tangents, and the new upper secant lies below
the old one. Every new square-feasible lift is old-square-feasible. The
argument includes signed bounds and degenerate intervals.

### Positive-cutoff square residual example

On `[0,u]`, `u>=r>0`, the square rows are
`w>=0`, `w>=2ux-u^2`, and `w<=ux`. With cutoff `w<=r^2`, the upper tangent
gives `x<=(u^2+r^2)/(2u)=F(u)`. The point `(F(u),r^2)` is feasible:
`r<=F(u)<=u`, `w>=0`, the upper tangent holds at equality, and
`r^2<=uF(u)` is equivalent to `r^2<=u^2`. The lower point `(0,0)` remains
feasible. Hence this is the exact endpoint map, not merely an estimate.

`F'(u)=(1-r^2/u^2)/2` is between `0` and
`q=(1-r^2/u_0^2)/2<1/2` on the invariant interval `[r,u_0]`. The mean-value
theorem gives the needed uniform scalar Lipschitz bound there. The limit
is `r`: decreasing iterates stay above `r`, and continuity gives the
positive fixed-point equation `u=(u^2+r^2)/(2u)`, hence `u=r`.
For `r=1,u_0=2`, `d=3/4`, `q=3/8`, and `e=d/(1-q)=6/5`. The exact total
motion is `1`, so the bound is valid and deliberately not exact. Its
after-first-round bound is `qe=9/20`, while actual remaining motion is
`F(2)-1=1/4`.

### Sharpness of the protected coordinate and objective ceilings

Consider the square objective `f(x)=x^2`, finite endpoint-tangent/secant
relaxation on `B_0=[-r_0,r_0]`, and cutoff `0`, where `r_0>0`. On
`[-r,r]`, the lower rows are `w>=2r|x|-r^2`; with the cutoff they give
`|x|<=r/2`. The lift `w=0` is feasible at every point of that smaller
interval, so exact Jacobi rounds give

\[
 B_k=[-2^{-k}r_0,2^{-k}r_0],\qquad
 L(B_k)=-4^{-k}r_0^2.
\]

The lower value is attained at `(x,w)=(0,-r^2)` without the cutoff,
because all tangent lower bounds are at least `-r^2` and the secant allows
that point. The degenerate box `P={0}` is protected by the exact lift
`(0,0)` when rebuilt on `P`, so the coordinate ceilings are `r_0` in
each direction and the objective ceiling is `0`. In the limit, both
coordinate ceilings and the remaining objective-improvement ceiling
`0-L(B_0)=r_0^2` are attained. A finite certificate can therefore bound
motion sharply without requiring finite termination of the actual
iteration. Discovering this particular inner point still requires
appropriate information; the example is not a general cheap procedure.

### Three-variable nonnegative-square stall

The archived stronger stall example is correct. For

\[
 f(x)=\sum_i x_i^2+\sum_{i<j}x_ix_j
     =\frac{\|x\|_2^2+(x_1+x_2+x_3)^2}{2},
\]

the unique original minimizer is `0`, with value `0`. On `[-1,1]^3`,
use square lifts constrained nonnegative and bilinear McCormick lifts,
with their sum as affine objective and cutoff `0`. At a face `x=+e_i`
or `-e_i`, set its square to `1`, all other squares and incident products
to `0`, and the product of the other two coordinates to `-1`. Every
McCormick row holds, and the objective is `0`; hence all six faces are
protected. At `x=0`, all squares may be `0` and all three cross products
may be `-1`, with objective `-3`.

Each cross product is at least `-1`: its two lower McCormick rows on this
box give `w_ij>=max(x_i+x_j-1,-x_i-x_j-1)>=-1`. With nonnegative squares,
the objective is at least `-3`, so the witness gives the exact relaxed
value. The face and objective points also satisfy the exact convex square
epigraphs. Thus the persistent gap is not caused by negative square lifts.
All later rounds of this family leave the full box fixed, while the
relaxation objective stays `-3` below the known original optimum.

The observed-ratio example is also correct: its two slopes are `1/4`
and `3/4`, and starting at `1` gives `1/2,3/8`. The first observed ratio
is `1/4`, but all subsequent iterates below `1/2` follow the slower slope
`3/4` and tend to zero. The quoted fitted tail `1/6` underestimates actual
remaining movement `1/2`; the correct uniform Lipschitz bound is `3/4`.

## 9. Verification actually performed

I read `AGENTS.md`, the manuscript brief, `theory/remaining-benefit.md`,
`document/certificates.tex`, `document/foundations.tex`,
`theory/certificates.py`, `theory/certified_driver.py`, and the October
`reviews/theory-review.md`. I also read the two focused certificate check
scripts and the relevant exact-workflow implementation description to
compare the claimed contracts with code. I did not run their archived LP
fixtures or numerical experiments. No project-wide check, CI inspection,
or literature search was run. No new source is needed for the proposed
proof corrections; existing attribution to primal feasibility filtering,
order arguments, weak duality, and matrix contraction theory should remain.

One targeted exact-arithmetic command was actually run from the repository
root: `python3 -B -`, with an in-memory heredoc script. The `-B` option
prevented Python cache writes. The script imported only the existing
certificate module, used exact rational callbacks, and performed no LP
solve. It checked the following distinct new cases:

- the square pool with a redundant objective-`2` corner retains full face
  coverage at cutoff `1`, and its cutoff-`1/2` frontier yields a different
  protected smaller box;
- exact endpoint-optimal auxiliary proposals `(0,-1)` miss the genuinely
  fixed box `{0}`, while the witness `(0,0)` certifies it;
- `diag(2,1/2)` accepts the stated finite supersolution despite global
  spectral radius `2`;
- a strict residual upper bound with `dbar+Me=e` gives the safe
  `Me=e-dbar` bound after the exact first round, while that number does
  not bound the remaining movement if the first update has been skipped.

Output:

```text
PASS: pool face threshold and smaller-hull reuse; exact-proposal incompleteness; noncontracting majorant; corrected upper-residual scope
```

These are targeted rational contract checks supporting the proof audit,
not empirical performance evidence or CI results. No file other than this
audit was intentionally written.
