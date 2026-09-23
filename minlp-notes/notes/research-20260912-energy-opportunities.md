# Storage convexification: prior-art elimination and a retained nonlinear gap

Date: 2026-09-12. Status: closed exploratory mathematics with an exact arithmetic
check and [accepted independent review](research-20260912-storage-independent-review.md).
The scan below records its historical proposals and source-reading state.
No storage solver or performance study was implemented, and no
publication-level novelty is claimed.

The strongest direction found in this bounded energy/process scan is
**convexification of storage degradation costs across time**. It has a clear
MINLP connection: mutually exclusive charge/discharge decisions, nonlinear
operating costs, and storage state equations occur inside energy-system design
and dispatch models. However, this scan does not establish that the direction
is more promising than the other active research lanes. Existing storage and
warehouse research already covers much of the attractive linear theory.

The concrete retained finding is a three-period example in which even the
exact hull of all linear storage trajectories, together with exact
single-period quadratic-cost hulls, underestimates the convexified degradation
cost by a factor of `9/8`. A simple valid conic inequality closes this example.
The inequality is elementary; its novelty and computational value remain
unestablished. It is useful as a regression instance for stronger temporal
relaxations and as a precise explanation of the remaining nonlinear issue.

The initial idea was a polynomial full-horizon hull when the allowed charge
and discharge endpoints lie in a fixed rational alphabet, including
time-varying state bounds. After normalizing a leaky recursion
`e_t = rho_t e_(t-1) + x_t` by `R_t = product_(i<=t) rho_i`, this condition
becomes a fixed alphabet for `x_t/R_t`. In a fixed-mode difference-constraint
polytope, every connected component of active difference edges at a vertex
must contain an active state bound. Hence every vertex state equals a state
bound plus a signed sum of allowed endpoints. A fixed alphabet gives
polynomially many candidate states and a layered network hull.

This is **not retained as a novelty candidate**. Bansal and Günlük explicitly
provide polynomial algorithms and extended network formulations for
fixed-dimensional lattice-structured time-varying warehouse bounds. Their
work covers the core counting argument and its storage interpretation. The
leakage change of variables alone does not rescue novelty. The broader
warehouse literature must be checked before reusing this argument in any
paper.

The following primary sources establish the main boundaries. The cited works
were sent to the single reusable literature agent; this note does not edit the
knowledge base or assign its reading statuses.

| Source | What it rules out or provides |
| --- | --- |
| [Wolsey and Yaman, *Convex hull results for the warehouse problem* (2018), DOI 10.1016/j.disopt.2018.06.002](https://www.sciencedirect.com/science/article/pii/S1572528617301482) | Earlier fixed-cost warehouse hulls, unit-flow formulations, and projected flow-cover inequalities. Only the publisher abstract was inspected in this lane; the complete theorem comparison is pending retrieval. |
| [Bakhshi and Ostrowski, *A Polynomial Algorithm for the Lossless Battery Charging Problem* (2023)](https://optimization-online.org/wp-content/uploads/2023/07/A_Polynomial_Algorithm_for_the_Lossless_Battery_Charging_Problem-2.pdf) | A full-horizon shortest-path/hull algorithm for storage without standing losses, permitting distinct buy/sell prices. The authors explicitly leave nonunit standing efficiency unresolved and report that polynomial size does not ensure useful runtime. The PDF was inspected. |
| [Bansal and Günlük, *Warehouse Problem with Time-varying Bounds, Fixed Costs and Complementary Constraints*, DOI 10.2139/ssrn.7371800](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7371800) | Direct prior art against the proposed alphabet theorem: time-varying bounds, complementarity, exact network formulations, and fixed-dimensional lattice cases. An earlier version has the title *Warehouse Problem with Bounds, Fixed Costs and Complementarity Constraints*. The full version history and exact theorem correspondence require KB reading. |
| [Bansal, Cornell dissertation, institutional PDF](https://ecommons.cornell.edu/server/api/core/bitstreams/138c4e73-c30c-4010-84bc-52e1a633347c/content) | The warehouse chapter contains extreme-point, network-hull, lattice-bound, approximation, and hardness sections. Exact bibliographic identification was delegated to the literature agent. This lane inspected the table of contents and search-exposed source passages, not the complete thesis. |
| [Elgersma et al., *Tight MIP Formulations for Optimal Operation and Investment of Storage Including Reserves* (2024)](https://arxiv.org/html/2411.17484v1) | Exact one-period storage, investment, and reserve hulls. Their paper distinguishes these from a full multi-period hull, and identifies limitations in some reserve models. This is a necessary formulation baseline. The primary HTML was inspected. |
| [Qu et al., *Convex Hull Model for a Single-Unit Commitment Problem with Pumped Hydro Storage Unit* (2023)](https://ira.lib.polyu.edu.hk/bitstream/10397/99201/1/Qu_Convex_Hull_Model.pdf) | Polynomial dynamic programming and a hull formulation for a pumped-storage unit model. Temporal-mode logic alone is not an adequate novelty distinction. The institutional abstract was inspected; detailed model comparison is pending. |
| [*Determining cost-efficient controls of electrical energy storages using dynamic programming* (2024), DOI 10.1186/s13362-024-00140-1](https://link.springer.com/article/10.1186/s13362-024-00140-1) | Nonlinear storage-control models and rounding-based dynamic programming provide an approximation baseline. Full assumptions and guarantees must be read before proposing an approximation theorem. |
| [Morales, *Linear and Second-order-cone Valid Inequalities for Problems with Storage* (2025)](https://arxiv.org/abs/2506.21470) | Multi-period linear cuts and quadratic-objective SOC cuts already exist. Any nonlinear storage contribution must compare with these, not just a naive continuous relaxation. The author-uploaded preprint passages were inspected. |

The Morales [author benchmark repository](https://github.com/groupoasys/storage_valid_inequalities)
contains arbitrage and set-point-tracking implementations and data. It is a
concrete open benchmark starting point, with GPLv3 code. Its advertised suite
and numerical claims were not independently reproduced in this lane.

For the retained example, let internal charging and discharging amounts be
`c_t,d_t >= 0`, with a binary charge indicator `delta_t`. Set

\[
\begin{aligned}
&e_t=e_{t-1}+c_t-d_t,\
&0\le e_t\le 1,\
&0\le c_t\le (2/5)\delta_t,\
&0\le d_t\le (2/5)(1-\delta_t),\
&e_0=e_3=1/2,\
&Q\ge\sum_{t=1}^3(c_t^2+d_t^2).
\end{aligned}
\]

Here `x_t=c_t-d_t` is the change in stored energy. Constant physical charging
and discharging efficiencies can be absorbed into the internal quantities;
the displayed cost specifically assumes equal quadratic coefficients in these
internal quantities. It is an illustrative convex degradation cost, not a
validated electrochemical degradation model. Standing losses are absent.

Let `H` be the convex hull of the feasible `(e,c,d,delta)` trajectories before
the cost epigraph is added. Consider the six trajectories formed by the three
distinct permutations of

\[
(x_1,x_2,x_3)=(2/5,-1/5,-1/5)
\]

and their negatives. Each obeys all bounds and the terminal equality. Give
them equal weight. Their mean has

\[
\bar e_1=\bar e_2=1/2,\qquad
\bar c_t=\bar d_t=2/15,\qquad
\bar\delta_t=1/2.
\]

Thus this point belongs to `H` by an explicit decomposition; no approximation
to the linear trajectory hull is used. The sum of the local perspective
epigraph bounds is

\[
\sum_{t=1}^3\left(
\frac{\bar c_t^2}{\bar\delta_t}
+\frac{\bar d_t^2}{1-\bar\delta_t}
\right)=\frac{16}{75}.
\]

The same value is feasible in the exact single-period state-and-cost hulls.
For periods one and two, independently mix increments `+4/15` and `-4/15`
with equal probability and start state `1/2`; their mean end state is `1/2`.
For period three, choose start states `1/2 - 4/15` and `1/2 + 4/15` and the
corresponding increments that end at `1/2`. These mixtures satisfy every
one-period bound and have the required means and per-period cost `16/225`.
The distributions of the shared state need not agree between these local
mixtures. That lack of distributional consistency is the source of the gap.

The exact convexified cost at these full-trajectory moments is instead

\[
Q_{\mathrm{hull}}=\frac6{25}
=\frac98\left(\frac{16}{75}\right).
\]

The following elementary inequality gives a proof and a valid strengthening.
For every integer `n>=2` and real vector `x` with `sum_t x_t=0`,

\[
\sum_{t=1}^n x_t^2\ \ge\
\kappa_n\left(\sum_{t=1}^n|x_t|\right)^2,
\qquad
\kappa_n=\frac{n}{4\lfloor n^2/4\rfloor}.
\tag{1}
\]

The coefficient is sharp. To prove it, write the total positive and negative
mass as `W/2`, where `W=sum |x_t|`. If there are `p` positive and `q` negative
entries, Cauchy--Schwarz separately on each sign gives

\[
\sum x_t^2\ge\frac{W^2}{4}\left(\frac1p+\frac1q\right).
\]

Over positive integers `p,q` with `p+q<=n`, this coefficient is minimized by
`p=floor(n/2)`, `q=ceil(n/2)`. Equal positive magnitudes and equal negative
magnitudes attain the bound. The zero vector is immediate.

For a cyclic storage trajectory, complementarity gives
`|x_t|=c_t+d_t`. Consequently

\[
Q\ge\kappa_n\left(\sum_t(c_t+d_t)\right)^2
\tag{2}
\]

is a convex valid inequality and therefore holds on the complete epigraph
hull. It is representable with a rotated second-order cone. For the displayed
three-period mean, total throughput is `4/5`; (2) yields `Q>=6/25`.
Every one of the six original trajectories has cost `6/25`, so their mixture
attains the bound. This proves the exact envelope value claimed above.

This also identifies several practical limits. For even `n`, (1) has the same
coefficient `1/n` as ordinary Cauchy--Schwarz; for odd `n` the coefficient
improvement is only `n^2/(n^2-1)`. Large uniform horizons therefore give little
additional strength from this single aggregate cut. A subwindow requires an
actual cyclic balance over that window; equality of mean endpoints in a
relaxation is insufficient. Arbitrary initial/final energy differences or
standing losses do not satisfy the displayed zero-sum hypothesis. The result
does not establish a convex hull formulation for general nonlinear storage.

A weighted version clarifies both generalization and computational limits.
For positive weights `a_t`, let `A=sum_t 1/a_t`. The largest universal
coefficient in

\[
\sum_t a_t x_t^2\ge\kappa(a)\left(\sum_t|x_t|\right)^2,
\qquad \sum_t x_t=0,
\]

is

\[
\kappa(a)=\frac{A}{4\max_{\varnothing\ne P\subsetneq[n]}
A_P(A-A_P)},\qquad A_P=\sum_{t\in P}\frac1{a_t}.
\tag{3}
\]

Indeed, separate weighted Cauchy--Schwarz gives the lower bound for each sign
partition. Zero entries can be assigned to either side when minimizing the
bound. For a maximizing partition, choose positive and negative magnitudes
proportional to `1/a_t` within their respective sign groups; this attains (3).
Determining whether `kappa(a)=1/A` is precisely equal-sum partition of the
reciprocal weights. Thus computing the sharp coefficient for arbitrary
rational weights is NP-hard, by taking `a_t=1/b_t` for an integer PARTITION
instance `b`. With a fixed number of distinct weights, enumerating the number
of entries of each weight in `P` gives a polynomial algorithm. These are
elementary observations about the sharp scalar cut, not claims about the
complexity of the full storage problem or new general partition theory.

The exact arithmetic check is

```bash
python code/research_20260912/storage_balance_perspective_gap.py
```

It uses only the Python standard library and was run with Python 3.13.11. It
checks all six schedules, their states, their exact means and costs, the
`9/8` ratio, and all sign-count coefficients for `2<=n<=19`. It passed. The
general proof above is necessary; the finite checks do not prove the theorem.
The file does not test (3); that claim currently rests on the proof above and
needs independent review if retained for use elsewhere.

The most useful next experiment, if this lane is reopened, is a small
three- to nine-period cyclic battery set-point or industrial-load-following
problem with an explicit quadratic degradation term. Compare the original
MIQP, the strongest available linear temporal relaxation, exact local
quadratic hulls, and short-window disjunctive conic relaxations. Add (2) only
for windows whose cyclic balance is part of the model. Measure lower-bound
improvement, optimality gap, branch-and-bound time, and added formulation
size. Start from the Morales data and code after reading its complete SOC
construction; local perspective cuts alone are not an adequate prior-art
baseline. Large-horizon value and realistic degradation modeling remain open
questions. No solver speedup has been measured in this lane.

The recommendation is to retain the exact counterexample and the rejected
alphabet idea in the research record, obtain a fresh review of the mathematics,
and give the current higher-potential research lanes priority. This bounded
scan did not find a sufficiently strong reason to promote storage as the main
project direction.
