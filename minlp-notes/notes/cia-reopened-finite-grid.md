# Exact one-switch minimax on arbitrary finite grids

Developed 2026-09-07. **Status: both the LP theorem and its explicit-formula refinement passed independent mathematical and implementation review.** See [the mathematical review](review-cia-reopened-finite-grid.md) and [the implementation review](review-cia-reopened-finite-grid-code.md). The [primary-source audit](cia-reopened-literature.md) found no matching theorem in its bounded search; this does not establish exhaustive priority.

The finite-grid question left open in [the earlier investigation](cia-investigation.md) now has an **explicit exact formula on every nonuniform grid**, evaluated with O(N²) rational arithmetic operations. It also constructs a worst relaxed control with only two component types and at most three time phases. The final formula and proof are in equations (2)–(7) below. The ten-variable LP characterization developed first is retained as an independently verified derivation and computational check.

## Statement

[Lean topic 17](../formal/topics/17-grid-switching/COVERAGE.md) verifies the
LP characterization, explicit formula, compressed maximizers, and exact
examples below. The linked verification record documents the completed
proof checks; it does not certify the Python implementations or novelty.

Fix n≥3 and a strictly increasing grid

\[
0=t_0<t_1<\cdots<t_N=T.
\]

Relaxed and integer controls are constant on its intervals. Write F_n(t) for the largest optimal CIA cumulative discrepancy over relaxed controls, when the integer control may switch at most once at a grid endpoint. Constant integer controls are allowed and initial activation is free.

**Theorem.** F_n(t) is the maximum of the optimal values of the two linear programs below, for 1≤a≤b≤N. Thus it is computable by N(N+1) linear programs, each with ten variables and a constant number of constraints. For rational grid endpoints this is an exact polynomial-time algorithm in the grid input length and log n. Some maximizing relaxed control has components 3,…,n identical and is constant on each of [0,t_a], [t_a,t_b], [t_b,T], ignoring empty segments.

The theorem concerns the *full worst case over all input controls*, not merely solving the rounding problem for a given input. Its dimension is independent of both n and N. The log n complexity returns a compressed witness; expanding n component rows takes at least linear time in n.

## Linear programs

Use variables u_j,v_j,m_j, j=1,2,3, and E. Index 3 represents each of n−2 identical modes, not their sum. Let w=(1,1,n−2). Both programs have the common constraints

\[
\begin{aligned}
&0\le u_j\le v_j\le m_j &&(j=1,2,3),\\
&\sum_jw_ju_j=t_a,\qquad \sum_jw_jv_j=t_b,
\qquad\sum_jw_jm_j=T,\\
&m_1\ge m_2\ge m_3,\qquad E\ge T/3,\\
&T-t_a\le E+m_1\le T-t_{a-1},\\
&T-t_b\le E+m_2\le T-t_{b-1},\\
&u_2+E\le t_a,\qquad v_1+E\le t_b.
\end{aligned}
\tag{LP}
\]

The **all-initial-modes program** adds u_3+E≤t_a. The **two-large-modes program** instead adds m_2≥E. In both cases maximize E. Empty feasible sets are ignored.

There are no strict constraints and no auxiliary discrete variables. In particular, the all-initial-modes program does *not* impose m_2≤E: that restriction is useful when proving coverage, but unnecessary for sufficiency.

## Proof

### Schedule identity and dominance

Let A_i(t) be the cumulative relaxed allocation and m_i=A_i(T). The exact error for distinct modes p,q and a switch at τ is

\[
D(p,q,\tau)=\max\{\max_{i\notin\{p,q\}}m_i,
\ \tau-A_p(\tau),\ T-m_q-\tau\}.
\tag{1}
\]

This includes constant controls through τ=0,T; it follows from monotonicity on the two activation pieces, as proved in the existing [continuous one-switch theorem](../results/cia-uniform-switching-obstruction.md).

Order totals m_1≥m_2≥…≥m_n. For fixed p and τ, a largest-total mode other than p is an optimal final mode: replacing a smaller final total decreases the last expression in (1), leaves the initial deficit fixed, and cannot increase the omitted maximum. Consequently it suffices to consider p→1 for p≠1 and 1→2.

### Every feasible LP point is an adversarial control

From any LP point, give modes 1 and 2 cumulative allocations (u_j,v_j,m_j) at (t_a,t_b,T), and give every remaining mode the values for j=3. Interpolate each cumulative function linearly between consecutive distinct times in {0,t_a,t_b,T}. Nonnegative increments and the weighted sum equalities make its derivatives nonnegative and sum to one. This is a valid relaxed control on the original grid. If a=b or b=N, the corresponding equal endpoint states follow from monotonicity and equal sums, so zero-length segments present no problem.

For p→1, a switch τ<t_a is at most t_{a−1}, and hence

\[
T-m_1-\tau\ge T-m_1-t_{a-1}\ge E.
\]

A switch τ≥t_a has initial negative discrepancy at least t_a−u_p, since τ−A_p(τ) is nondecreasing. The same reasoning for 1→2 uses t_b and v_1.

In the all-initial-modes program, t_a−u_p≥E for every p≠1, while t_b−v_1≥E. Dominance therefore proves every schedule has error at least E.

In the two-large-modes program, every schedule omitting mode 1 or 2 has error at least m_2≥E. The only remaining two-mode possibilities are 2→1 and 1→2, and the common constraints prove their error at least E by the preceding argument. Constant schedules also omit at least one of these two modes. Thus every feasible LP point yields a control with optimal error at least E in both programs.

### Every worst case is covered

The relaxed control polytope is compact, and its optimal error is the minimum of finitely many continuous functions (1). A maximizer α therefore exists. Write its error F. Always F≥T/3: assign three modes total T/3 each and all other modes zero. Every one-switch schedule omits at least one of those three modes.

Suppose first F>T/3 and choose T/3<E<F. Sort the totals. There are at most two totals strictly exceeding E. For j=1,2, let k_j be the first grid index for which

\[
t_{k_j}\ge T-E-m_j.
\]

Then k_1≤k_2. Both are positive. Indeed, k_1=0 implies T−m_1≤E, and the constant schedule selecting mode 1 has error max(T−m_1,max_{i≠1}m_i)=T−m_1≤E, a contradiction. Thus 1≤a=k_1≤b=k_2≤N, and the two cutoff inequalities in (LP) hold, with strict upper inequalities before taking a limit.

If m_2≤E, every schedule p→1 and 1→2 omits only totals at most E. At its earliest eligible time its final deficit is at most E. Since its error is strictly above E, (1) forces

\[
A_p(t_a)<t_a-E\ (p\ne1),\qquad A_1(t_b)<t_b-E.
\]

If m_2>E, the third-largest total is at most E because 3E>T. Apply the same argument only to 2→1 and 1→2; their omitted totals are at most E. This gives the common initial-deficit inequalities and m_2>E.

Average the cumulative functions of modes 3,…,n. This preserves the total sum, nonnegative increments, total ordering relative to m_2, and the inequalities just obtained. The resulting endpoint data are feasible for the corresponding closed LP at objective E.

Let E tend up to F. There are finitely many choices (a,b,program); choose a fixed one along a subsequence. Its endpoint data are bounded, and their limit is an LP point with objective F. This proves coverage when F>T/3.

If F=T/3, at least one LP still attains F. Set E=T/3, m_1=m_2=E, m_3=E/(n−2). Choose a=b as the first grid endpoint at least E and set

\[
u_1=v_1=u_2=v_2=(t_a-E)/2,\qquad
u_3=v_3=E/(n-2).
\]

These values satisfy the two-large-modes LP: 0≤t_a−E≤2E and t_{a−1}≤E≤t_a verify the nontrivial constraints. This covers the boundary case. Together with sufficiency it proves the theorem, including the three-phase, three-component-type extremizer. ∎

## Exact computation and the open nine-interval case

[The exploratory LP implementation](../code/cia_reopened/finite_grid_research.py) uses SciPy/HiGHS only to discover solutions. It reconstructs primal and dual vectors as rational numbers and checks all primal inequalities, dual signs, stationarity, and equality of primal and dual objective values using `Fraction` arithmetic. It additionally constructs a rational upper-bound certificate for **every** region, including regions the numerical solver declared infeasible. No numerical infeasibility classification is trusted for the final universal bound. Bounded-denominator recovery can fail on valid inputs; this optional audit is a certificate finder, not a complete exact solver. The separate [formula implementation](../code/cia_reopened/minimax.py) has no such limitation and uses only the Python standard library. Every expanded extremizer reported by the research CLI is checked by rational enumeration of all ordered mode pairs and grid switch times.

The previously unresolved full value for n=5,N=9 is now **F_5(9)=17/5**. The certificate establishes the formerly missing universal upper bound. One maximizing relaxed control uses these constant vectors:

| Time segment | Mode 1 | Each of modes 2,3,4,5 |
|---|---:|---:|
| [0,4] | 2/5 | 3/20 |
| [4,5] | 0 | 1/4 |
| [5,9] | 1/4 | 3/16 |

Its totals are (13/5,8/5,8/5,8/5,8/5), and its cumulative vector at time 4 is (8/5,3/5,3/5,3/5,3/5). This supplies a simpler representative of the already known exact lower-bound example. It still disproves the tempting extension “maximum of uniform-input error and the three-mode worst-case error,” whose value would be only 16/5.

Reproduce with:

```bash
python code/cia_reopened/finite_grid_research.py --modes 5 --intervals 9
```

Add `--audit-lp` to compare the formula with the independently rational-certified LP formulation. The standalone library entry point `minimax(n, grid)` in `code/cia_reopened/minimax.py` returns the exact value and a constant-size compressed worst-case control.

**Short analytic upper bound, found independently by the reviewer.** Sort m_1≥…≥m_5. If m_1≥13/5, use mode 2 until time 3 and mode 1 afterward. Its initial deficit is at most 3, its omitted maximum is at most m_3≤3, and its final deficit is 6−m_1≤17/5. If m_1<13/5, then m_2≥(9−m_1)/4>8/5. At time 4 choose an initial mode p with A_p(4)≥4/5, and as final mode a largest-total mode q≠p. The initial deficit is at most 16/5, the final deficit is 5−m_q<17/5, and every omitted total is below 13/5. Both cases give an error at most 17/5. Together with the displayed lower witness, this proves F_5(9)=17/5 without any optimization software.

## Scope and retained investigative lessons

The LP theorem solves the exact finite-grid minimax computationally for every n≥3 and every rational grid. The subsequent formula below removes linear programming entirely. A shorter expression specialized to unit grids could still clarify the arithmetic pattern, but is not needed for a complete exact answer on any given grid.

The initial derivation introduced a positive slack variable to encode failure at a threshold and tried to exclude degenerate closed regions. That complication is unnecessary: weak inequalities already prove error at least E directly. Closed LPs give valid lower-bound witnesses, including their boundary points. This observation removes numerical strict-feasibility decisions entirely.

The result concerns one allowed switch. Arbitrary switch budgets and more operational restrictions remain separate questions. The exact instance solver in the parallel investigation is substantially cheaper than these adversarial LPs and should be used when only rounding one given relaxed input is required.

## Stronger result: explicit rational formula without linear programming

The LP characterization above can be simplified further. This section supersedes the ten-variable LPs as an algorithm while retaining them as an independent certificate formulation. **This extension has passed independent mathematical review**, including every elimination inequality and boundary case.

Let c be the first index with t_c≥T/3 and define

\[
H=\min\{(T+t_c)/4,\ (T-t_{c-1})/2\}.
\tag{2}
\]

For each 1≤a≤b≤N abbreviate A=t_a, B=t_b, P=t_{a−1}, Q=t_{b−1}. Retain the pair only if

\[
(n-2)(T-A)\le(n-1)B.
\tag{3}
\]

Set

\[
\begin{aligned}
L_{ab}&=\max\left\{\frac T3,\frac{(n-1)T}{n}-B,
\frac{(n-1)T-A-(n-1)B}{n}\right\},\\
U_{ab}&=\min\left\{A,\frac{(n-2)A+B}{n},
\frac{(n-1)T}{n}-P,
\frac{(n-1)T-P-(n-1)Q}{n},
\frac{T-P+(n-2)A}{n}\right\}.
\end{aligned}
\tag{4}
\]

Also require U_ab≥L_ab. An empty maximum below is ignored.

**Explicit minimax theorem.**

\[
\boxed{F_n(t)=\max\{H,\ \max_{(a,b)\text{ retained}}U_{ab}\}.}
\tag{5}
\]

Thus O(N²) arithmetic operations suffice. For rational inputs this is a direct exact algorithm using rational arithmetic, with polynomial bit complexity. It returns a compressed worst-case control in polynomial time in the grid encoding length and log n; expanding n individual components necessarily takes at least linear time in n.

Every extremizer supplied by the formula has just **two types of component**: either one distinguished mode and n−1 identical modes, with at most three time phases; or two identical distinguished modes and n−2 identical modes, with at most two time phases.

### Proof: the two-large-modes contribution

In a feasible two-large-modes LP, the initial negative discrepancy of mode 2 is at least E at t_a and therefore also at t_b. At t_b both selected modes consequently have cumulative allocations at most t_b−E. All other modes have total sum at most T−2E. Hence

\[
t_b\le2(t_b-E)+T-2E,\qquad
E\le(T+t_b)/4.
\]

The cutoff for mode 2 and m_2≥E give E≤(T−t_{b−1})/2. If t_b<T/3, the first bound is below T/3; if t_{b−1}>T/3, the second is below T/3. The only index yielding a value above T/3 is c. At a boundary equality other indices can give only T/3≤H. Therefore every two-large-modes LP has value at most H.

For attainment set E=H and let the two distinguished modes have total E each. Give every other mode total (T−2E)/(n−2). At C=t_c, give each distinguished mode cumulative allocation

\[
x=\max\{0,(C-T+2E)/2\},
\]

and each other mode allocation min(C,T−2E)/(n−2). Interpolate linearly on [0,C] and [C,T]. We have E≥T/3, E≤C, 4E≤T+C, and T−C≤2E≤T−t_{c−1}. These verify the two-large-modes LP with a=b=c. The construction is valid also when C=T, where the last segment is empty. It attains error at least H, so H is the exact contribution of that LP family.

### Proof: one distinguished mode suffices in the other family

Use the coverage proof at a strict level T/3<E<F in its case m_2≤E. Average **all** modes other than the largest-total mode 1, not merely modes 3,…,n. The initial negative discrepancy at t_a remains above E for every averaged mode, because it is their average. Their new common total m is no larger than the old second-largest total m_2. The first eligible final-mode time for 1→an averaged mode therefore moves weakly later. Mode 1's initial negative discrepancy is nondecreasing in time, so it remains above E there. Thus this averaging preserves the obstruction, with some new b≥a.

Consequently the coverage argument needs only a largest-total mode of total M and n−1 identical modes of total (T−M)/(n−1). Taking limits as before handles all boundary cases. Conversely, such a symmetrized control is a special case of the already proved sufficient all-initial-modes LP.

### Proof: eliminate cumulative states and the largest total

Write x=A_1(A), y=A_1(B). Once M,x,y are specified, the bulk cumulative values are (A−x)/(n−1), (B−y)/(n−1), and (T−M)/(n−1). The two failure inequalities are

\[
x\ge(n-1)E-(n-2)A,\qquad y\le B-E.
\]

Monotonicity of both cumulative types is equivalent to

\[
0\le x\le y\le M,\qquad
0\le A-x\le B-y\le T-M.
\]

In conjunction with the cutoff constraints, these cumulative states exist exactly when

\[
E\le A,\qquad nE\le(n-2)A+B,
\]

and the interval for M is nonempty:

\[
\begin{aligned}
\max\{&T/n,\ T-A-E,\ (n-1)(E+Q)-(n-2)T,\
 &(n-1)E-(n-2)A\}\\
&\le M\le
\min\{T-P-E,\ (n-1)(E+B)-(n-2)T\}.
\end{aligned}
\tag{6}
\]

For sufficiency, choose any M in (6), then set

\[
x=\max\{0,(n-1)E-(n-2)A,A-T+M\},\qquad
y=\max\{x,B-T+M\}.
\tag{7}
\]

The displayed inequalities imply x≤min(A,M,B−E). They also give y≤min(M,B−E), y−x≤B−A, and B−y≤T−M, proving feasibility. Necessity follows immediately from the cumulative bounds and cutoff constraints.

Finally compare each of the four lower endpoints in (6) with each of its two upper endpoints. Two comparisons hold automatically because P≤A and Q≤B. One is exactly (3). The remaining five comparisons, together with E≥T/3, E≤A, and nE≤(n−2)A+B, give precisely L_ab≤E≤U_ab in (4). Maximizing E yields (5). Equations (6)–(7) construct its corresponding extremizer. ∎

### Verification and a failed simpler formula

Before deriving (5), a tempting candidate for the all-initial-modes contribution retained only the first-sum bound ((n−2)A+B)/n and the total-sum bound ((n−1)T−P−(n−1)Q)/n. It matched all tested unit grids but failed on the nonuniform grid

\[
n=9,\quad (t_0,\ldots,t_5)=(0,19/2,61/6,265/24,481/24,2669/120).
\]

The incomplete formula predicts 2077/216; the exact all-initial-family maximum is only 2593/270. Thus the remaining admissibility and upper bounds in (3)–(4) must not be omitted on arbitrary grids.

The complete formula matched the independently rational-certified LP answer on 100 random rational nonuniform grids (seed 27, mode counts 3,…,9, one through seven intervals). The earlier LP formulation additionally reproduced all known three-mode unit-grid results through N=12 and certified a 72-case table with n=3,…,8 and N=1,…,12, plus eight nonuniform cases. These are computational checks, supplemental to the proof above.

The independent mathematical reviewer completed 33 comparisons among the exact formula, the original rational-certified compressed LPs, and separately assembled LPs retaining all modes and all interval rates; every extracted witness also passed exact enumeration of the original cumulative discrepancy. The independent code reviewer added 99 formula-versus-certified-LP comparisons and 24 extreme-arithmetic cases, including n=10^100+7, denominators above 10^30, and grid endpoints within 10^−40 of T/3. All passed. Import and evaluation under `python -S` confirmed that the standalone formula implementation requires no installed third-party packages.
