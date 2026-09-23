# Root development candidates for stage 3

These are working arguments, not accepted manuscript theorems. The stage author
must verify them and five independent reviewers must examine the final text.

## Unit conductance, bipartite graphs, and prescribed fixed girth

In the base RPF construction g belongs to {1,2}. For fixed positive integer L,
replace each g=1 edge by a path of 4L edges of unit conductance and each g=2
edge by a path of 2L edges of unit conductance. Assign new internal vertices
zero power injection and voltage bounds [1/2,4]. Positivity forces zero current
divergence at such vertices and therefore linear voltage interpolation along
each path. Effective conductance is g/(4L). Divide every old injection bound
by 4L. Old voltage coordinates and bounds are unchanged.

Both directions appear exact and rationally bijective. New voltages are convex
combinations of old endpoint voltages and satisfy their bounds. Old degrees do
not increase; internal degrees are two. All replacement paths have even length,
so the graph is bipartite (all old vertices can have the same color). Every new
cycle has at least 2L times as many edges as its old cycle; the base construction
is simple. For every fixed requested girth, choose a fixed sufficiently large L.
The data alphabet remains fixed for each fixed L and graph growth is linear.
Do not claim one universal finite alphabet for variable L, preservation of
planarity, or hardness on trees/bounded treewidth from this argument.

## New primary-source lead: planarity may be obtainable

Root downloaded the open publisher version of Dobbins, Kleist, Miltzow,
Rzazewski (2023), Completeness for the Complexity Class forall-exists-R and
Area-Universality, DOI 10.1007/s00454-022-00381-0, to
build/source-cache/dobbins-area.pdf with extracted text alongside. Exact
source: printed p.163, Theorem 2.1 and Figure 3; the PDF has a repository
cover sheet, so verify PDF indices before screenshots. Retrieval URL:
https://dspace.library.uu.nl/bitstream/handle/1874/430446/s00454-022-00381-0.pdf?isAllowed=y&sequence=1

The source PLANAR-ETR-INV is promised either unsatisfiable over R or to have
a solution in [1/2,4]. This is NOT an ordinary unbounded feasibility theorem
that may be indiscriminately restricted afterward. Use its precise source
promise or explicitly reproduce its planarization of bounded ETR-INV.

Its crossover is X+Y=Z, X+Y'=Z, X'+Y=Z, forcing X'=X, Y'=Y,
Z=X+Y. X,Y,X',Y' retain the original [1/2,2] values and Z is in [1,4].
Copy wires carrying original values through crossings; local Z edges do not
need further crossing. For feasible-set universality, preserve the original
variable [1/2,2] bounds (otherwise widening to [1/2,4] can add extraneous
solutions). Only the designated root bus need impose that tighter interval;
other value copies can use [1/2,4]. The crossover introduces uniquely
determined auxiliary variables and preserves rational equivalence.

Generalize the electrical complement to C=9/2 on [1/2,4]. Pinned copy
injection becomes 2-C=-5/2; addition injection 3-C=-3/2; inversion D
injection 5-3C=-17/2. I still has injection -1 and voltage [1/2,4], and W
has [1,4]. Exact inversion forces xy=1; since x,y>=1/2, actually x,y<=2,
so the old W range remains valid. All voltages still belong to [1/2,4],
so the same free injection bound85 is valid. Constants x=1 may be imposed
by fixing that root voltage, or normalized as previously with distinct copies.

Embedding candidate: replace each variable vertex by a disk carrying its
alternating copy path, ordered around the disk boundary according to incident
constraint occurrences. Multiple strands for a repeated incidence are adjacent
within its original corridor. Each addition gadget is a three-leaf star.
Each inversion gadget is a tree with three boundary leaves: two x-bar copies
and one y-bar copy; duplicate the x incidence into two parallel corridor
strands. A three-leaf tree admits any cyclic leaf order after reflection.
Variable copy paths can have a break between boundary ports so they do not
form a closed cycle that traps other edges. Prove this topologically, including
repeated names and embedding-order allocation; numerical planarity alone is
not a proof. The ordinary append-only variable allocation must be reordered
to match embedding ports, though the same <=2 extensions/request bound holds.

Connectedness candidate: each variable chain's initial value bus has degree
at most2 and a redundant free injection bound. In each component choose such
a bus; attach a new voltage1 bus with free injection85 and unit conductance.
Connect the new buses in a path. Their connecting lines have zero voltage
drop and their degree is at most3. Every altered old injection was free and
still bounded by84 for all allowed voltages; every new injection is also
redundant. Thus the solution-set correspondence is unchanged. For planarity,
choose an accessible root and exterior face and arrange components along the
connector path; justify access via the variable-disk embedding. Handle the
empty graph separately. Apply even subdivisions afterward for unit conductance,
bipartiteness, and fixed girth. This needs independent verification.

## Feasible-set universality

The own reduction has an explicit rational bijection with coordinate-projection
inverse. Combine it with Abrahamsen--Miltzow, Dynamic Toolbox for ETRINV,
Theorem 1 and Definition 5 (primary local fulltext pages 3--4). This appears
to realize every compact semialgebraic set defined over Q as a rationally
equivalent RPF voltage set. State the inherited source theorem exactly; do not
invent polynomial bit bounds for the affine recovery coefficients. This yields
the algebraic-degree result and arbitrary compact topology as consequences.
An isolated real algebraic alpha has a rational polynomial and rational
isolating interval. The source linear projection yields a designated variable
of the same algebraic degree when alpha is irrational, not just field generation.

## Approximation promise and exact rational witnesses

For bounded positive rational voltage box with global upper bound U, let
D=max_i sum_j g_ij and P_i(V)=V_i sum_j g_ij(V_i-V_j). The infinity-norm
Lipschitz constant 4UD follows from the row sums of absolute gradients on the
box. Define rho(V)=max_i dist(P_i(V),[P_i^L,P_i^U]) with voltage bounds exact.
Rounding inside the voltage box (preserving singleton bounds) gives rational
epsilon-feasible witnesses of bit length polynomial in input size and
log(1/epsilon), whenever an exactly feasible solution exists. This is a
certificate existence theorem, not an algorithm finding the witness.

The promise problem min rho=0 versus min rho>epsilon has an NP verifier using
a rational box point and violation at most epsilon/2 (round fine enough).
State explicitly that answers in the promise gap are unconstrained and this
does not put exact RPF in NP. Neither fixed finite data nor continuity provides
an inverse-polynomial lower bound for rho on all infeasible instances.
Investigate a quantitative residual transfer for the actual inversion/copy
gadgets; do not infer a gap-preserving reduction from a generic exact ETR
reduction. A strong robust NP-hardness theorem may require genuinely different
Boolean gadgets and should not be assumed.

### Concrete candidate residual transfer for the ordinary reduction

Let gamma_Phi be the minimum over the exact source box [1/2,2]^n of the
maximum absolute addition/inversion equation residual, and gamma_G the minimum
injection interval violation over the exact constructed voltage box (pinned
voltages remain exact). There are at most6m value-to-value copy transitions.
If a voltage vector has injection residual epsilon, every requested value copy
differs from its root value or complement by at most delta=6m epsilon.
An addition source residual is at most epsilon+3delta. In inversion CI gives
|I-x|<=epsilon+delta. I's residual gives |W-h(I)|<=2epsilon, where
h(t)=2t-1+1/t has |h'|<=2 on[1/2,2]. D gives
|y-(W-2x+1)|<=epsilon+3delta. Hence
|xy-1|<=2(epsilon+3delta)+2(2epsilon+2(epsilon+delta))
=10epsilon+10delta. Thus gamma_Phi<=10(6m+1)gamma_G.

Conversely for any source-box assignment (not necessarily feasible), take all
copies exact, I=x and W=h(x). Every voltage bound holds; all copy/CI/I residuals
vanish, an addition residual is its source residual, and D residual is
|y-1/x|<=2|xy-1|. Free injection intervals never bind. Therefore
gamma_G<=2gamma_Phi. This would give an explicit polynomial-loss transfer of
residual minima. State exact voltage-box convention, constant normalization,
m=0 case, and do not infer an inverse-polynomial gap for arbitrary NO inputs.

## Quantitative equal-angle stability (possible stage 2/3 strengthening)

For a connected purely resistive graph, positive magnitudes v_i>=ell>0,
and real edge angle differences within[-pi/2,pi/2], put a_ij=g_ij v_i v_j
and let q be the actual reactive injection vector. Center theta to mean zero.
The identity -theta^T q=sum_edges a_ij delta_ij sin(delta_ij), together with
t sin t>=(2/pi)t^2, gives
||theta||_2 <= pi ||q||_2/(2 ell^2 lambda_2(L_g)).
This is a classical strong-monotonicity/Poincare estimate; application and
explicit residual consequences, not its general mechanism, may be useful.
For magnitudes<=U, the active injection discrepancy from equal angles satisfies
0<=P_i(v,theta)-P_i(v,0)<= (U^2/2) sum_edges g delta^2
<= pi^2 U^2 ||q||_2^2/(8 ell^4 lambda_2(L_g)).
Check all constants, sign conventions and one-vertex/disconnected cases.
An elementary rational lower bound lambda_2(L_g)>=2g_min/(n-1)^2 follows from
||theta||^2=(1/n)sum_{i<j}(theta_i-theta_j)^2 and paths of length<=n-1.
Can use that to give explicit rational polynomial bounds instead of claiming
exact spectral computation. A coarser rational inequality sin t>=t/2 on
[0,pi/2] avoids pi in certificate bounds. Tiny reactive tolerances then control
active-law error quadratically, but do not repair arbitrary principal-angle
winding or make a positive-tolerance exact-feasibility reduction automatic.

## Stage 2 caution supplied by stage 1 author

Review C's optional angle extension uses a unit-circle identity. The raw test
e_i+e_j>0 cannot simply be retained for arcs longer than pi/2 with unequal
magnitudes. Normalization by auxiliary positive magnitude variables is a
possible sound route; the author must verify all endpoints and encodings.

Root found a simpler all-short-arcs candidate avoiding normalization in the
crossing test: for arc from v_j to v_i with principal difference in(-pi,pi),
put d=e_j f_i-f_j e_i. The crossing count is +1 iff f_j<0<=f_i and d>0,
and -1 iff f_i<0<=f_j and d<0; otherwise0. The sign of d is the orientation
of the short arc, and the half-plane change distinguishes the positive ray
from the negative ray. Root exact check passes all504 pairs of eight rational
directions (excluding antipodal pairs) with three independent positive scales.
This permits c=cos(gamma) in(-1,1] via auxiliary positive magnitudes r_i and
the unsquared polynomial inequality e_i e_j+f_i f_j>=c r_i r_j. Keep r_i^2
=e_i^2+f_i^2 and voltage bounds. Excludes antipodal arcs and thus gamma=pi.
Stage2 author must prove, test cycles, and explain endpoints independently.

### Positive principal-angle bounds can also give a sound hardness transfer

For n>=2 choose c_n=1-1/n^2, a rational with O(log n) bits, and impose the
principal cosine limit cos(delta)>=c_n on every line. The short principal
differences have |delta|<=gamma_n=acos(c_n). On [0,pi], the elementary bound
1-cos(t)>=2t^2/pi^2 gives gamma_n<=pi/(sqrt(2)n). Every simple cycle has
length<=n, hence its principal sum has absolute value<2pi. It is a multiple
of2pi, so it is zero. All principal angles therefore admit a real lift and
zero reactive injection forces equal angles. This gives principal-only AC
hardness with strictly positive angular windows and polynomial-bit rational
cosines. It does NOT establish the same transfer for one fixed positive
window on arbitrary-size graphs, nor make the cosines a fixed finite alphabet.
Cases n=0,1 can be handled separately or a harmless isolated bus added for
hardness. The cubic graph bounds and all other fixed-data restrictions remain.
An n-independent zero-width window would be a trivial principal hardness
transfer, but does not address the positive-window issue. Evaluate whether
the positive-window corollary merits inclusion; if so verify the encoding,
cycle-sum bound and its precise distinction from the documented counterexample.

## Explicit doubly small NO-instance residuals (new root candidate)

This may resolve the numerical-gap question much more concretely. Introduce
t,h,x_0,...,x_k,a_0,...,a_{k-1},b_0,...,b_{k-1},c_0,...,c_{k-1}, all in
[1/2,2]. Impose t*t=1, h+h=t, t+h=x_0. At every step impose

  a_j+h=x_j, x_j*b_j=1, a_j+b_j=c_j, x_{j+1}+h=c_j.

Finally impose x_k*t=1. Exact equations force t=1, h=1/2, x_0=3/2 and
x_{j+1}=x_j+1/x_j-1. If x_j=1+delta_j, then
delta_{j+1}=delta_j^2/(1+delta_j)>0. Thus the final equation is impossible.

Nevertheless take the exact recurrence values and leave only the last equation
unsatisfied. x_j is in(1,3/2], a_j=x_j-1/2 in(1/2,1], b_j=1/x_j in[2/3,1),
c_j=x_j+1/x_j-1/2 in(3/2,5/3]. Every box bound holds. With delta_0=1/2,
delta_k<=2^(-2^k). More explicitly delta_k=1/d_k with d_0=2 and
d_{j+1}=d_j(d_j+1); exact rational finite checks are easy for moderate k.
There are4k+3 variables and4k+4 equations.

Apply the ordinary RPF extension to these nonsolutions. All original bus
injection constraints except final inversion D hold exactly. At that D the
absolute residual is |1-1/x_k|=1/(d_k+1)<2^(-2^k). All voltage bounds,
including pinned voltages, hold exactly. The RPF network is infeasible by
the main equivalence but admits that tiny residual. Its size is at most
68k+67 buses and72k+72 lines; all numerical data are from the fixed alphabet.
It is connected because the source incidence graph is connected and every
gadget and variable path is connected. Subdivision preserves the phenomenon
with a fixed scaling if desired, but do not invent a simultaneous planar
linear-size claim without an embedding proof.

Consequences to state carefully: no inverse-polynomial or singly-exponential
universal lower bound on positive minimum injection violation follows even for
the fixed-data degree-three class. Exponentially many tolerance bits can be
needed to rule out such infeasible instances by a residual threshold. This is
not a lower bound on all exact decision algorithms; the displayed family itself
has a simple algebraic infeasibility proof. The minimum violation is positive
by compactness and continuity, but the exhibited point is only an upper bound
on that positive minimum, not an exact minimum calculation.

LMI representability in prior DC feasibility work does not alone establish
polynomial exact Turing decidability. Keep exact feasibility, approximate
feasibility, strict feasibility, and promise problems distinct.

## Additional root audit before stage 3

For planar connectedness, an arbitrary chosen spare-degree root is incident to
some face; choose that face as the exterior face of its connected component
before arranging the components. This avoids assuming a previously fixed
outer-face incidence. The new fixed-voltage/free-injection connectors have
unique voltage1, so do not add solution-set dimensions. Handle the zero-bus
source (the single point of R^0) explicitly if stating universal connectedness.

For planarization, distinguish occurrences from incidence edges. An equation
with repeated names can use adjacent parallel strands in its original
corridor and all requests still receive distinct electrical bus identities.
All newly introduced crossing wire values stay in the original [1/2,2]
range; only local sum Z may reach4. After substitution use root intervals
[1/2,2] for original and wire variables, [1,4] for sums, and copy intervals
[1/2,4]. State original bounds explicitly in the projected solution set.

The explicit small-residual family has graph-encoding length O(k log k)
with a standard adjacency-list encoding, so its doubly exponential residual
refutes every universal lower bound 2^{-poly(input length)}, not merely
2^{-C times number of buses}. No exact algorithm lower bound follows.
