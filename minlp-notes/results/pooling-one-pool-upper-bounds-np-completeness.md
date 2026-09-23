# One-pool pooling is NP-complete with only upper bounds and sparse bypasses

Date: 2026-09-05. Status: combined proof independently reviewed; precise
literature priority remains qualified.

A later reviewed [constant-data construction](pooling-constant-data-two-feed-np-completeness.md)
strengthens the hardness to strong NP-completeness and restricts the pool
to two feeds. The explicit error-bound and penalty proof below remains
a separate useful result.

**Theorem.** The rational threshold decision problem for standard pooling
is NP-complete under all of the following restrictions:

- There is exactly one pool and one scalar quality coordinate.
- Every output quality specification is an upper bound; no lower quality
  bounds are needed. All input qualities and output bounds lie in `[0,1]`.
- Every flow lower bound is zero. All input, output, pool and arc upper
  capacities are at most four.
- Every input has total out-degree at most two, every output has total
  in-degree at most three, and the pool has out-degree two. Its in-degree
  is unrestricted. Direct input-output arcs are allowed.
- The objective can use nonnegative input production costs and nonnegative
  output unit revenues.

This is ordinary binary-encoded NP-completeness. Quality, objective and
threshold coefficients can have large numerical magnitudes, so the proof
does not give strong hardness or an approximation barrier. The construction
uses no pool-to-pool arcs. Bypass maximum degree two remains outside this
argument.

The theorem combines a positive-product hardness reduction, copy gadgets,
closed cycles that force upper quality bounds to equality, and an explicit
linear penalty that removes fixed flow contracts. The large penalty is
computed from the full final copy network; it is not assumed to exist
without an encoding bound.

## 0. The contracted hard family with one upper quality

The starting point is the reviewed
[one-pool copy reduction](pooling-one-pool-bypass-np-completeness.md).
Its source is Matsui's positive-product construction,
[METR95-13](https://www.keisu.t.u-tokyo.ac.jp/data/1995/METR95-13.pdf),
Sections 2–3, Theorem 3.1. A polynomial-size homogeneous cone `Cx<=0`
encodes the source polytope after `z=x/sum(x)` at positive throughput.
The source's bounded integer cone coefficients permit polynomially many
port occurrences even though its quality and reward coefficients are
large. Every original intake has quality `a_i>1` and reward `b_i>0`.
For the source polytope `P`, its exact contracted optimum is

```
OPT_contract = max( {0} union
    { b(z)(1+1/a(z)) : z in P } ).
```

The threshold is the source's positive `K_source`; crossing it is
NP-hard. Zero intake is feasible even when `P` is empty. The full source
construction, coefficient bounds and threshold equivalence are in the
linked result.

The [degree-three averaging construction](../notes/pooling-bypass-degree-three-hardness.md)
implements each cone row using full and half signal ports and a balanced
averaging tree. A full gadget has endpoint qualities `0,beta`, middle
quality `beta/2`, two outputs of exact demand four, and middle input exact
supply four. A half gadget has endpoint qualities `0,3`, middle quality
one, two outputs of exact demand three, and middle supply three. Keep
only their upper quality bounds. At each output, endpoint flows `alpha,b`
then satisfy `b<=alpha` in a full gadget and `2b<=alpha` in a half gadget.

For each signal, place its full gadgets and intake-conversion gadget in
one closed zero-port cycle: each link is a quality-zero input of exact
supply two joining one gadget's second zero port to the next gadget's
first zero port. For `r` gadgets, summed zero-endpoint flow is `2r` and
summed endpoint flow is `4r`. Consequently summed other-endpoint flow is
`2r`; every inequality `b<=alpha` is tight. This argument permits distinct
positive `beta` values, so ordinary and conversion gadgets coexist.
All gadgets now have full port values `x,2-x`, and each cycle link forces
the same `x` in successive gadgets.

Keep half gadgets in a separate closed cycle for the same signal.
Their summed zero-endpoint flow is `2r` and summed endpoint flow is `3r`.
Thus the inequalities `2b<=alpha` are all tight, giving half-port values
`x/2,1-x/2`. To identify full and half signals, use a quality-three exact
supply-two input on one full positive port and two distinct complementary
half ports:

```
x_full + (1-x_half/2) + (1-x_half/2) = 2.
```

This enforces equal signals with degree three. Separate gadgets supply
every port occurrence, so repeated terms introduce no parallel arcs.
All original averaging equations and cone-row bounds are recovered.
The [complete cyclic proof](../notes/pooling-single-upper-quality-cycles.md)
records both projection directions, signal ranges, padding and size.

Finally reduce input out-degree from three to two. Every degree-three
source just described has exact supply two and port capacities `(2,1,1)`.
Replace it by three same-quality sources with exact supplies `c_h`, each
feeding its original port `f_h` and a new common collector. The collector
has exact demand `sum(c_h)-2=2` and a redundant upper quality bound equal
to the sources' quality. Its incoming flows are `c_h-f_h`, so its demand
is equivalent to the original source equation `sum(f_h)=2`. New sources
have degree two and the collector degree three. All other input degrees
were already at most two. This substitution preserves original intakes,
rewards, the cone projection, and the zero-intake feasible assignment.

The resulting contracted family has one upper-bound quality, input
out-degree two, output in-degree three, and upper flow capacities at most
four. All auxiliary data have polynomial encoding length. The following
penalty removes its remaining positive lower flow bounds. Define its
matrices and constants *after* the cycle and source-splitting changes.

## 1. Linear copy subsystem and contract deficits

Use the Matsui-specific hard family in the
[copy reduction](pooling-one-pool-bypass-np-completeness.md),
so each actual pool input has distinguished quality `a_i>1` and intake
reward `b_i>0`. Write `a_max=max_i a_i`, `b_max=max_i b_i`.
All these rational numbers have polynomial binary encoding length.

Let `w` consist of all direct flows in the copy network and all actual
pool intakes `x_i`. Exclude the anchor and the two primary output flows;
they do not participate in the copy constraints. Include the linear
constraint `T=sum_i x_i<=2`. The original exact-contract copy subsystem is
a nonempty bounded rational polytope

```
Q = { w : A w<=d, E w=e }.
```

The matrix `E` records the required exact source supplies and exact gadget
output demands. Its coefficients are zero or one, and its right-hand
entries are the original zero-, one-, two-, three-, or four-unit contracts. The rows
`Ew<=e` are among the upper-bound constraints `Aw<=d`.
All other rows in `A` are arc/source/output upper bounds, nonnegativity,
the copy outputs' linear quality constraints, and `T<=2`. They contain no
pool-quality variables or primary nonlinear outlet constraints.

Nonemptiness does not require a nonempty source product polytope. The
assignment with every original intake signal zero satisfies all
homogeneous source-cone rows; complementary ports and any averaging
signals are filled at their corresponding values. This satisfies every
exact copy contract. Boundedness follows from finite arc bounds.

Delete all positive lower flow bounds in the physical instance, retaining
their upper bounds. Any feasible solution then supplies a vector `w`
satisfying `Aw<=d`, with nonnegative contract deficits

```
Delta=e-Ew>=0,       delta=sum_j Delta_j.
```

The primary pool still blends its actual intakes and obeys its upper
capacity and the two primary output specifications.

## 2. Explicit rational error bound for restoring contracts

The following elementary bound is a quantitative form of the standard polyhedral
error bound used here. The classical source is [Hoffman (1952)](https://nvlpubs.nist.gov/nistpubs/jres/049/4/V49.N04.A05.pdf),
Section 2; the explicit coarse bound below is proved directly. Its explicit coefficient dependence ensures the
penalty has polynomial encoding length.

**Lemma.** Let `Q={v:R v<=s}` be a nonempty rational polyhedron in
`R^N`. Clear each row's denominators by a positive factor so that all
row coefficients are integers, with absolute values at most an integer
`K>=1`. Then for any `w`,

```
dist_1(w,Q) <= H * max_j (R_j w-s_j)_+,
H=N (N K)^(N-1),                                           (H)
```

where the residuals are measured in this integer row representation.
The case `N=0` is trivial and can be omitted.

**Proof.** Let `v` be the Euclidean projection of `w` onto `Q`, and put
`h=w-v`. If `h=0`, there is nothing to prove. The normal cone of a
polyhedron at `v` is the cone generated by its active row normals.
Removing linear dependencies from a conic representation gives

```
h=B^T lambda,       lambda>=0,
```

where the `r<=N` rows of `B` are linearly independent active integer row
normals. Since each selected inequality is tight at `v`,

```
||h||_2^2 = lambda^T B h
          <= ||lambda||_1 * eta,
eta=max_j (R_j w-s_j)_+.
```

Also `||lambda||_1<=sqrt(N)||h||_2/sigma_min(B)`. The positive integer
`det(B B^T)` is at least one, while every singular value of `B` is at
most its Frobenius norm, at most `NK`. Hence

```
sigma_min(B) >= (NK)^(-(r-1)) >= (NK)^(-(N-1)).
```

Cancel `||h||_2>0`, and use `||h||_1<=sqrt(N)||h||_2` to obtain (H). □

Apply this lemma to `Q` using rows of `A`, `E`, and `-E`. Only rows of
`A` with nonintegral coefficients require denominator clearing; they are
already satisfied by `w`, so their positive residuals are zero at any
scale. The contract rows `E,-E` have integral coefficients and integral
right-hand sides and are left unscaled. The largest positive residual is
therefore at most `delta`. Consequently there exists `w' in Q` with

```
||w'-w||_1 <= H delta.                                    (2)
```

Let `x'` be its actual intake vector. In particular
`||x'-x||_1<=H delta`. The integer bound `K` is computable by clearing
the explicitly given rational row denominators; the resulting bit length
is polynomial in the original matrix encoding. Thus `H` also has
polynomial bit length. No projection or optimal Hoffman constant needs
to be computed to construct the reduction.

## 3. Restoring primary outlet feasibility by radial scaling

For a nonnegative intake vector `x`, put

```
T=sum_i x_i,       S=sum_i a_i x_i,
F(x)=S(T-1)-T.
```

Because `a_i>1`, `S>=T`. The primary two-output subsystem can accommodate
exactly those intakes with `T<=2` and `F(x)<=0`: for `T>0` its pool
quality is `S/T`, and its maximum possible throughput is
`1+T/S`. This follows from the two unit output capacities and the
distinguished bound with the zero-quality anchor. Conversely assign
as much as possible, up to one, to output 2, and send the remainder to
output 1 with enough anchor. In particular the maximal radial throughput
is attainable. The zero-intake case is feasible separately.

The original upper-only solution has `F(x)<=0`. The restored copy vector
`x'` obeys `x'>=0`, `sum x'<=2`, and all homogeneous source-cone rows,
but may violate `F(x')<=0`. On the convex domain
`x>=0, sum x<=2`,

```
dF/dx_i = a_i(T-1)+S-1,
|dF/dx_i| <= 3 a_max+1 = L.
```

Therefore `F(x')_+<=L ||x'-x||_1`. If `F(x')>0`, then `T'>1` and
`S'>1`. Scale `x'` by

```
theta=(1+T'/S')/T' < 1,
x''=theta x'.
```

Its new throughput is exactly the feasible radial cap and `F(x'')=0`.
The mass removed is

```
||x'-x''||_1 = T'-1-T'/S' = F(x')/S'
             <= L ||x'-x||_1 <= L H delta.                 (3)
```

If `F(x')<=0`, set `x''=x'`, so the same bound holds. Homogeneity
preserves every source-cone row when scaling, and all original signals
remain in `[0,2]`. Rebuild the entire exact copy network from `x''`,
including all complementary and averaging signals. This gives a feasible
original-contract pooling solution with intakes `x''`.

The difference in intake profit satisfies

```
b^T x <= b^T x'' + C delta,
C=b_max (1+L) H.                                         (4)
```

This is a uniform bound over every feasible solution of the upper-only
instance. No division by a possibly vanishing throughput is used in the
error estimate; scaling is needed only when `T'>1,S'>1`.

## 4. A polynomially encoded exact linear penalty

Choose rational `M=C+1` and reward every originally contracted source
and gadget output by an additional `M` per unit of its throughput.
The new objective, in maximum-profit convention, is

```
P_new = b^T x + M sum_j (E_j w).
```

This is an ordinary linear arc objective: each term in `E_j w` is an
ordinary arc flow incident to that contracted source or output. Each
coefficient can be formed explicitly in polynomial time. Put
`B0=M sum_j e_j`; then

```
P_new-B0 = b^T x-M delta
         <= b^T x''-(M-C)delta
         <= OPT_contract.
```

Every original-contract solution is feasible in the new instance and
has `delta=0`, so equality of optimal values holds:

```
OPT_new = B0 + OPT_contract.                             (5)
```

In fact a positive deficit is strictly suboptimal compared with the
constructed exact-contract repair. All objective and threshold
coefficients have polynomial encoding length: `N`, the cleared-row
coefficient bound `K`, `a_max`, `b_max`, `H`, `C`, `M`, and `B0` are
explicit and have polynomial bit bounds. Their numerical magnitudes
can be large, so no strong-hardness conclusion follows.

Use decision threshold `B0+K_source`, where `K_source` is the positive
product threshold of the reviewed reduction. Equation (5) proves
NP-hardness with all lower flow bounds zero. The topology and every upper
flow or quality bound are unchanged. Fixed-pool/fixed-quality NP
membership gives ordinary NP-completeness. It applies with one pool-quality
parameter, using the [reviewed NP lemma](fixed-parameter-linear-fibers-np-membership.md).

## 5. Optional input-cost and output-revenue version

For the standard production-cost version, reward the private input
feeding each conversion gadget's `A-beta` port by `b_i` per unit, instead
of the actual pool intake arc. Before repair these two flows need not
coincide, so that identity must not be used on the upper-only instance.

Write this objective as `c^T w`, with `||c||_infinity<=b_max`. Projection
to `w'` changes it by at most `b_max H delta`. At the exact point `w'`,
it equals `b^T x'`. Radial rebuilding changes it by at most
`b_max L H delta`. Thus the identical constant `C` in (4) proves the
same exact-penalty result. Both the base rewards and source-throughput
penalties are input production costs; contracted gadget outputs receive
the indicated revenues. Adding a common charge `D>=M+b_max` to every
input unit cost and common revenue `D` to every output unit revenue
cancels by total mass conservation, and makes all input costs and output
revenues nonnegative.

## 6. Normalization, checks and literature status

All unscaled input qualities and output upper bounds are nonnegative.
Divide them by their positive global maximum to put them in `[0,1]`.
This preserves every quality inequality, flow, objective and degree; the
proof can compute its penalty in the original coordinate scale before
this final equivalent normalization. Rational arithmetic retains polynomial
encoding length.

The complete proof received two independent audits of the
[penalty](../notes/review-pooling-upper-flow-only-penalty.md) and its
[second review](../notes/review-pooling-upper-flow-only-penalty-second.md),
and two of the [cyclic construction](../notes/review-pooling-single-upper-quality-cycles.md)
and its [second review](../notes/review-pooling-single-upper-quality-cycles-second.md).
The cycles reviews include the degree-two input substitution. Earlier
source-copy and averaging audits remain linked from the component notes.

The independent cycle constructor checked 100 original-network projection
LPs and 94 fixed-composition pooling LPs, including 46 excluded
compositions. It also checked eight penalized LPs with both reward
realizations and a control that fails when cyclic upper capacities are
relaxed. A separate exact rational checker passed 500 radial-repair
estimates, with 183 nontrivial repairs. After the degree-two source
substitution, a further 24 independent checks covered projection and
penalized objectives, shifted qualities and both reward conventions.
The first reviewer additionally ran 18 global solves and 12 penalized
solves on the split-input construction, with both negative controls.
The author ran 26 original-network global solves and 12 penalized solves
on the final degree-two-input construction; logs are
[here](../code/pooling_bypass_copy/upper_quality_split_inputs_output.txt)
and [here](../code/pooling_bypass_copy/upper_quality_split_inputs_penalty_output.txt).
The numerical penalty experiments use a moderate `M=100`; they validate
examples of the mechanism, not the huge theoretical constant. Its
correctness and polynomial encoding are established by the proof and
independent audits.

Baltean-Lugojan and Misener already assert a broader one-pool capacity
hardness boundary in Remark 4.6 of their
[open full text](https://d-nb.info/1149002905/34). The repository's
[source audit](../notes/pooling-single-quality-bypass-novelty.md) records
that this assertion does not give a checked explicit reduction with the
restrictions above. This result supplies such a reduction and its NP upper
bound. Priority for the precise combination of restrictions remains
unestablished; it is not presented as the first general one-pool capacity
hardness claim. The exact-penalty and closed-cycle component proofs are
preserved separately for reuse and further checking.
