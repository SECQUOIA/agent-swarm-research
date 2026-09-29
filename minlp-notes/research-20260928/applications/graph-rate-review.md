# Independent review of graph-constrained prefix discrepancy

Date: 2026-09-28. Reviewer: independent `graph_rate_review` agent.

The proposed trichotomy is correct under its stated grid and graph assumptions,
with one minor exception: the one-mode complete graph has zero discrepancy,
not a positive constant order. For every fixed graph with at least two modes,
the three orders are constant, square root, and linear. The non-strongly-connected
lower bound can be strengthened to a dimension-independent bound.

This is a proof audit and a narrow literature comparison. It does not establish
publication-level novelty.

## Precisely reviewed statement

Let `G` be a fixed directed graph on `m` modes, containing every self-loop. A
word `w_1,...,w_N` must follow its arcs; the first mode is free. For simplex
vectors `alpha^t`, define

\[
 e_i(k)=\sum_{t=1}^k(\alpha_i^t-1_{w_t=i}),\qquad
 D(\alpha,w)=\max_{i,0\le k\le N}|e_i(k)|,
\]

and `D_G(N)=sup_alpha min_w D(alpha,w)`. For fixed `G` and `m>=2`,

\[
 D_G(N)=
 \begin{cases}
 \Theta(1),&G\text{ contains every ordered arc};\\
 \Theta(\sqrt N),&G\text{ is strongly connected but incomplete};\\
 \Theta(N),&G\text{ is not strongly connected}.
 \end{cases}
\]

All asymptotic constants may depend on the fixed graph. With cell duration
`h=T/N` and fixed physical horizon `T`, the corresponding primitive-error
orders are `h`, `sqrt(h)`, and `1`.

## Complete graph

The upper bound has a short direct proof. Start with `e(0)=0`. At step `t`,
select a coordinate maximizing `x_i=e_i(t-1)+alpha_i^t`, then subtract one
from that coordinate. Because `sum_i x_i=1`, the selected coordinate after
subtraction exceeds `-1`. Unselected coordinates remain greater than `-1`
by induction. Since the new errors sum to zero, every error is less than
`m-1`. Thus `D<=m-1` for `m>=2`.

The first cell with target `(1/2,1/2,0,...)` gives `D>=1/2` for every word.
These bounds suffice for the constant order; neither is claimed optimal.
For `m=1`, the unique word equals the unique target and `D_G(N)=0`.

## Missing-arc lower bound

Take a missing ordered arc `u->v` and the constant target with masses `1/2`
on `u,v`. Let `D` be the discrepancy of an arbitrary allowed word, and let
`R` be its total number of other-mode cells. Every other coordinate has
target zero, so its final count is at most `D`. Therefore

\[
 R\le(m-2)D.
\]

Delete other-mode symbols and consider the remaining binary word. Every
consecutive projected change `u->v` requires at least one deleted symbol
between its two endpoints in the original word. These intervals are
disjoint, so there are at most `R` such changes. The number of `v->u`
changes differs from the number of `u->v` changes by at most one.
Consequently the number of nonempty projected runs is at most `2R+2`.

For any projected run of `u`, its original span contains no `v`. Over that
span the `v` discrepancy increases by one half per cell. The difference of
two prefix errors is at most `2D`, so the span, and hence the projected
run length, is at most `4D`. The same argument applies to a `v` run. If
the projected word is empty, the following bound still holds trivially:

\[
 N-R\le4D(2R+2),\qquad
 N\le8(m-2)D^2+(m+6)D.
\]

This proof correctly allows arbitrarily many relay cells inside a projected
run. It does not assume projected runs are contiguous original intervals.
In the strongly connected incomplete case, `m>=3`, so the inequality gives
the required square-root lower bound. The target is constant in time; temporal
roughness of the target is not responsible for the obstruction.

## Strong-connectivity upper bound

There is a closed walk visiting every mode with edge length
`L<=m(m-1)`: order all vertices and concatenate shortest paths between
successive vertices, including the return to the first. Write its cyclic
vertex word using `L` symbols, omitting the duplicated final endpoint. Let
`c_i` be the number of mandatory occurrences of mode `i`, so `sum_i c_i=L`.
The cyclic convention matters: the last symbol has an arc to the first,
which makes consecutive blocks compatible.

For a full block of integer length `B>=L`, let `A_i` be its target masses.
Choose nonnegative integers `d_i` summing to `B-L` and satisfying

\[
 \left|d_i-\frac{B-L}{B}A_i\right|<1.
\]

Flooring and allocating the remaining units to fractional coordinates gives
such integers. Follow the closed-walk word and insert `d_i` self-loop cells
at an occurrence of each mode. The total mode count is `c_i+d_i`, and

\[
 |c_i+d_i-A_i|<L+1.
\]

At a block boundary errors accumulate by at most `L+1` per block. Inside
a block, any coordinate error can change by at most `B`. A remaining
partial block can hold the last mode using its self-loop. If there is no
full block, start at any mode and hold it. Thus

\[
 D\le\lfloor N/B\rfloor(L+1)+B.
\]

For `N>=L`, taking `B=ceil(sqrt((L+1)N))` gives
`D<=2sqrt((L+1)N)+1`; the finitely many smaller horizons satisfy the
same asymptotic conclusion by `D<=N`. All scheduling details needed for
the upper bound are accounted for.

## Non-strong-connectivity lower bound: stronger correction

Choose a nonempty proper forward-closed vertex set `A`, a mode `u` in it,
and a mode `v` outside it. Such a set exists, for example as a sink strongly
connected component. Use the same half-half constant target on `u,v`.

Let `s` be the number of cells preceding the first entry into `A`, with
`s=N` if entry never occurs. Then `u` has not been used by prefix `s`, so
`D>=s/2`. After entry, `v` cannot be used. Its entire count is at most `s`,
so `D>=N/2-s`. Combining the two inequalities gives

\[
 D\ge N/6.
\]

No aggregation factor `|A|` is necessary. Since doubled errors are integers
for this target, the discrete statement is

\[
 D\ge\tfrac12\lceil N/3\rceil.
\]

The bound is sharp over the class of non-strongly-connected graphs: on the
two-mode graph with both loops and only the arc `v->u`, an appropriately
chosen word `v^s u^(N-s)` attains `ceil(N/3)/2`. The upper bound `D<=N`
requires only an arbitrary constant-mode word.

## Positive-support refinement

The proposed refinement is also correct. Assume `alpha_i^t>=eta>0` for
all cells and modes. Keep a closed tour with mandatory counts `c_i`.
Choose an integer block length `B` with

\[
 B\eta\ge\max_i c_i+2.
\]

At each full block boundary `bB`, round the cumulative target vector to
an integer vector `C(b)` with sum `bB` and coordinate error strictly below
one; set `C(0)=0`. These roundings need not be coordinated between blocks.
Their increments `n_i(b)=C_i(b)-C_i(b-1)` sum to `B` and satisfy

\[
 n_i(b)>B\eta-2\ge c_i.
\]

They can therefore be realized by the tour and extra self-loops. Every
boundary error is below one, and the within-block or final-tail error is
at most `B` more. Thus `D<=B+1`, uniformly in `N`.

There is no missing condition `B>=L`: the simplex condition gives
`eta<=1/m`, and the displayed threshold implies `B>=m max_i c_i>=L`.
The refinement is uniform for fixed positive `eta`, but its bound degrades
as `eta` approaches zero. It does not contradict the missing-arc example,
whose relay target masses are zero.

### Sharp dependence on the positive floor

The strengthened claim subsequently supplied by the author is correct:
for a fixed strongly connected incomplete graph and `0<=eta<=1/m`,

\[
 \sup_{\alpha_i^t\ge\eta}\min_wD(\alpha,w)
 =\Theta_G\bigl(\min\{\sqrt N,1/\eta\}\bigr),
\]

where `1/0=infinity`. Constants can be chosen independent of both `N`
and `eta`; in particular, `eta` may depend on `N`.

Here is an independent reconstruction of the lower bound. Write `a=m-2`.
For a missing arc `u->v`, give each relay target mass `eta` and each active
mode target mass `p=(1-a eta)/2`. Then `p>=1/m` and every target mass is
at most `1/2`, so every first mode gives `D>=1/2`. The total relay count
satisfies `R<=a eta N+aD`. A projected active run has length at most
`2D/p<=2mD`, so

\[
 N-R\le4mD(R+1).
\]

Substituting the relay-count bound and rearranging yields

\[
 (1-a\eta)N
 \le4ma\eta ND+4maD^2+(a+4m)D.
\]

Use `1-a eta>=2/m` and `D<=2D^2` to get

\[
 (2/m)N\le4ma\eta ND+C_mD^2,
 \qquad C_m=4ma+2a+8m.
\]

At least one of the two right-hand terms is at least `N/m`, proving

\[
 D\ge\min\left\{\frac1{4m^2a\eta},
                  \sqrt{\frac{N}{mC_m}}\right\}.
\]

The previously verified general upper bound and the positive-floor upper
bound give the matching order. This is a stronger contribution than the
fixed-interior corollary because it identifies the scale
`eta` comparable to `N^(-1/2)` at which the two rates meet.

## Contracting state dynamics

For the explicitly stated diagonal system

\[
 \dot x_i=-\lambda x_i+w_i,\qquad\lambda\ge0,
\]

compare with the relaxed system driven by `alpha`, with the same initial
state. Let `z=x^w-x^alpha` and `q(t)=int_0^t(w-alpha)`. Integration by parts
and integration of the differential equation give

\[
 z_i(t)=q_i(t)-\lambda\int_0^t e^{-\lambda(t-s)}q_i(s)\,ds,
 \qquad q_i(t)=z_i(t)+\lambda\int_0^t z_i(s)\,ds.
\]

Hence

\[
 \frac{\|q\|_\infty}{1+\lambda T}
 \le\|z\|_\infty\le2\|q\|_\infty.
\]

For slotwise constant controls on equal cells, the primitive is affine
inside every cell, so `||q||_infty=hD` exactly. Both upper and lower
discrepancy orders therefore transfer to state sup-norm error when
`lambda,T` are fixed independently of `N`. This is a valid application
to a contracting system. It does not establish lower bounds for arbitrary
nonlinear systems, terminal-only objectives, or an incomplete observation
of the state vector.

The additional horizon-independent upper bound is also correct for
`lambda>0`. For the full-block construction, put `b=Bh`, `a=(L+1)h`,
and `r=exp(-lambda b)`. On each completed block the local primitive is
bounded by `b`, and its terminal value is bounded by `a`. Integration by
parts bounds that block's forcing contribution by `a+b(1-r)`. The endpoint
recurrence therefore has magnitude at most `a/(1-r)+b`, since initial
state error is zero. On a current partial block, the forcing magnitude
is at most its duration, hence at most `b`. Consequently

\[
 E\le2Bh+\frac{(L+1)h}{1-e^{-\lambda Bh}}
 \le2Bh+(L+1)h+\frac{L+1}{\lambda B}.
\]

The last step uses `1/(1-exp(-x))<=1+1/x` for `x>0`. Selecting `B` of
order `sqrt((L+1)/(lambda h))`, subject to `B>=L`, gives a bound of order
`sqrt(h/lambda)+h`, with no dependence on `T`. The requirement
`lambda>0` is essential to this form; the finite-horizon bound above also
allows `lambda=0`.

## Literature comparison and significance limits

- Bestehorn, Hansknecht, Kirches, and Manns, [*Mixed-integer optimal control
  problems with switching costs: a shortest path approach*](https://link.springer.com/article/10.1007/s10107-020-01581-3),
  Mathematical Programming 188 (2021), 621–652. Definition 2 uses the same
  primitive discrepancy after multiplication by cell width. Their DAG
  method optimizes switching costs under a prescribed discrepancy tolerance;
  Remark 15 explains added combinatorial restrictions, and the preceding
  discussion recognizes that these can make a chosen tolerance infeasible.
  Those algorithmic statements are not the fixed-transition-graph rate
  classification proved above. The comparison examined the article's
  formulation, consistency definition, and combinatorial-extension discussion.

- Bestehorn and Kirches, [*Matching Algorithms and Complexity Results for
  Constrained Mixed-Integer Optimal Control with Switching Costs*](https://optimization-online.org/wp-content/uploads/2020/10/8059.pdf),
  open preprint (2020). Theorem 4.4 establishes a matching construction
  with primitive error at most the mesh width under its vanishing-constraint
  assumptions. Pointwise mode eligibility differs from a restriction on
  successive mode pairs. That theorem cannot supply the missing-arc upper
  bound without checking and changing its assumptions. The matching and
  feasibility results and uses of the word “transition” were examined.

- Robuschi, Zeile, Sager, and Braghin, [*Multiphase Mixed-Integer Nonlinear
  Optimal Control of Hybrid Electric Vehicles*](https://optimization-online.org/wp-content/uploads/2019/05/7223.pdf),
  open 2020 manuscript, published in Automatica 123 (2021), 109325.
  Section 3.4 imposes mode-transition rules. Assumption 5 requires the CIA
  approximation error to be bounded by a constant times mesh width;
  Remark 6 explicitly identifies this assumption as critical with transition
  and dwell restrictions. The classification supplies a fixed-graph setting
  where such a uniform linear-mesh bound fails, while weaker square-root
  convergence still holds. Their physical dwell times, phase logic, and
  additional constraints exceed the present model, so the theorem is not
  a general convergence replacement for that application. Sections 3.4 and
  4, especially Assumption 5, Remark 6, and Theorem 7, were examined.

- Holroyd and Propp, [*Rotor Walks and Markov Chains*](https://arxiv.org/pdf/0904.4507),
  Theorem 4, proves bounded occupation-count discrepancy from a stationary
  distribution of a fixed finite irreducible Markov chain. This is important
  adjacent prior art for positive-support or stationary targets. It does not
  directly settle uniform approximation of arbitrary time-varying simplex
  targets, including targets on boundary faces with zero relay mass.
  The theorem and its occupation-frequency assumptions were examined.

The strongest present contribution appears to be the exact worst-target
rate classification, together with a concrete reason that a missing mode
transition can invalidate linear-mesh rounding assumptions. The filtered
state example shows that the obstruction persists in a simple stable
dynamic model; it is not merely an artifact of a discrepancy objective.
These are useful theoretical consequences. No computational solver speedup,
industrial improvement, or publication-level originality follows from
the proof audit. Wider searches under graph walks, constrained discrepancy,
deterministic sampling, and switching approximation remain necessary.

The principal modeling limits are essential: all modes have self-loops;
relay cells consume one full grid cell; the graph is fixed as the grid is
refined; the horizon is fixed when translating rates to physical time;
and the target is allowed to use boundary faces of the simplex. Positive
physical transition times, fixed dwell times, time-dependent graphs,
prescribed terminal modes, and state constraints need separate analysis.

## Verification record

The reviewer independently reconstructed every proof above and obtained
the improved non-strong-connectivity constant before receiving the separate
computational review. A separate checker independently obtained that same
correction. No Lean proof or project-wide checks were run. Exact finite
computations are supplemental evidence and cannot establish the asymptotic
claims or novelty.

The separate checker ran the following targeted command successfully:

```
python /tmp/minlp_graph_discrepancy_finite_20260928.py
```

That temporary script remains outside the repository. Its exact integer
dynamic program keeps the active-mode counts and last mode, retaining the
smallest historical discrepancy for each state. It checked all five looped,
strongly connected three-mode graphs missing a specified arc, for
`N=1,...,100`: 500 checks of the missing-arc inequality, with minimum slack
`7/2`. It also enumerated the nondecreasing binary occupancy optimum through
`N=10000`, confirming `ceil(N/3)/2`, and checked 66 exact maximum-horizon
instances for complete-minus-one-arc graphs. A fresh independent reviewer
checked 45 additional maximum-horizon instances. These finite checks
supplement the symbolic proofs rather than substituting for them.

## Supplemental exact half-target capacity

The finite checker derived a sharper result, which this reviewer then
checked algebraically and which a fresh adversarial reviewer also checked.
It is not necessary for the rate classification, but gives exact benchmark
instances and a lower-bound constant independent of the number of modes.

Take the complete looped digraph missing only `u->v`, and the constant
half-half target on those modes. For a prescribed half-integer discrepancy
bound `D`, set `K=2D` and

\[
 q_* = \min\{(m-2)\lfloor K/2\rfloor,K\}.
\]

The largest feasible horizon is exactly

\[
 N_{\max}=3K+4Kq_*-2q_*(q_*+1).
\]

To prove the upper bound, let `c` be the relay count and let
`S=count(u)-count(v)`. The two active-coordinate bounds are equivalent to
`|S|+c<=K`. Each individual relay count is at most `floor(K/2)`, so the
total relay count `q` is at most `q_*`. Between two successive relay cells,
the active word has form `v^a u^b`, because `u->v` is missing. In the segment
with relay count `c`, put `B_c=K-c`; let `s_c,t_c` be its initial and final
values of `S`. Its lowest value is at least `-B_c`, so its length is at most
`s_c+t_c+2B_c`. Empty segments satisfy this inequality too.

The first initial value is zero; a relay leaves `S` unchanged, so
`s_{c+1}=t_c`; and feasibility after that relay requires
`t_c<=K-c-1` for `c<q`. The final value satisfies `t_q<=K-q`. Summing
the segment bounds and adding the `q` relay cells gives

\[
 N\le 3K+4Kq-2q(q+1).
\]

The right side is nondecreasing for integer `0<=q<=K`, since the increment
from `q` to `q+1` is `4(K-q-1)`. Thus `q=q_*` gives the upper bound.

For equality, in each active segment first descend in `S` to `-B_c` by
using `v`, then ascend by using `u`, ending at `B_{c+1}` if a relay follows
and at `B_q` in the final segment. Insert one relay cell between segments,
distributing the total relay uses across the `m-2` relay modes with at most
`floor(K/2)` uses of any one. This is possible by the definition of `q_*`.
Every segment and every relay respects all coordinate bounds, and all arcs
used are present. A prefix supplies every shorter horizon.

For `m>=4`, `q_*>=K-1`, and the two final possible values give

\[
 N_{\max}=2K^2+K=8D^2+2D,
 \qquad
 D_N=\frac12\left\lceil\frac{\sqrt{1+8N}-1}{4}\right\rceil.
\]

The formula concerns the optimum separately at each horizon. It does not
construct a single infinite word simultaneously attaining all horizon
optima. For any graph missing `u->v`, deleting further arcs can only
increase discrepancy; moreover the capacity expression for fewer relay
modes is no larger. Therefore the dimension-independent bound
`N<=8D^2+2D` holds for the half-target witness on every such graph.
