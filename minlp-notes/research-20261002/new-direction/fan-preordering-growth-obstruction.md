# A width-two quadratic-growth obstruction to exact box preorderings

Date: 2026-10-02. Status: elementary rational construction, targeted
exact checks, and a [fresh independent review](../reviews/fan-preordering-growth-obstruction-review.md)
finding no substantive gap. The non-SPN fan phenomenon
is classical. Comparison of the displayed matrix with the primary source's
particular matrix is pending; no novelty claim is made.

## Result and scope

There is a rational quadratic on `[0,1]^5` with a unique optimum, exact
coordinate-curvature/growth ratio `202`, and interaction treewidth two,
whose optimum has no finite-degree identity in the full polynomial
preordering of the box slacks. Connected chains of copies retain width two,
growth `1/100`, and curvature/growth ratio at most `206`.

This sharpens the width of the existing
[Horn-based box-preordering obstruction](box-preordering-growth-obstruction.md).
It does not establish optimization hardness or rule out other certificate
families. In particular, it concerns exact unmultiplied identities, not
strictly approximate bounds or certificates using a vanishing multiplier.

The [SPN graph audit](../prior-art/spn-graph-prior.md) attributes the
non-SPN five-vertex fan to Shaked-Monderer's 2016 Lemma 7.1. The proof below
is self-contained from the displayed rational matrices and the existing
Horn calculation. It does not rely on retrieving that lemma's exact matrix.

## A rational copositive fan matrix

Let `H=J-2 Adj(C5)` be the Horn matrix. For nonnegative `u`,

    u' H u=(sum_i u_i)^2-4 sum_i u_i u_(i+1) >= 0.

The elementary proof in the existing obstruction maximizes the cycle edge
sum at fixed coordinate sum, merges nonadjacent support, and reduces to an
edge, whose product is at most one quarter of the squared sum.

Take the nonnegative rational matrix with columns

    V=[e1, e2, e3, (e2+e4)/2, (e3+e5)/2].

Then `C=V' H V` is copositive, and direct multiplication gives

    C = [ 1  -1   1    0     0  ]
        [-1   1  -1    1     0  ]
        [ 1  -1   1   -1     1  ]
        [ 0   1  -1    1    -1/2]
        [ 0   0   1   -1/2   1  ].

Its exact nonzero off-diagonal graph is the fan with hub `3` and outer
path `1-2-4-5`. The bags

    {1,2,3},       {2,3,4},       {3,4,5}

form a path decomposition of width two. Since the graph contains a
triangle, its treewidth is exactly two. This uses every nonzero matrix
entry, not just the negative entries.

Set

    Q=C+I/100,       F(x)=x' Q x,       x in [0,1]^5.

Copositivity gives `F(x)>=||x||^2/100`, so the unique optimum is zero.
The vector `e1+e2` satisfies `V(e1+e2)=e1+e2` and has zero Horn energy.
It is feasible and attains equality in that growth bound. Therefore

    g=1/100,       L=2 max_i Q_ii=101/50,       L/g=202.

All data are fixed rationals. The maximum absolute row sum of `C` is five,
so the full Hessian norm is at most `501/50`; full-curvature conditioning
is bounded as well.

## An exact rational separating witness

Use the symmetric integer matrix

    W = [1773  1803     0     0  336]
        [1803  3544  1803     0    0]
        [   0  1803  4020  2286    0]
        [   0     0  2286  2476  392]
        [ 336     0     0   392  200].

It is entrywise nonnegative. Its leading principal determinants are

    1773,
    3032703,
    6427781703,
    66900290040,
    378879939072.

All are positive, so Sylvester's criterion makes `W` positive definite.
Thus it is a rational doubly nonnegative separating witness. Exact trace
products give

    <C,W>=-163,       trace(W)=12013,
    <Q,W>=-163+12013/100=-4287/100<0.

If `Q=P+N` with `P` positive semidefinite and `N` entrywise nonnegative,
both `<P,W>` and `<N,W>` would be nonnegative. The displayed negative trace
therefore proves that `Q` is not SPN. It also proves that `Q` is not PSD,
so the objective is nonconvex.

## Consequence for full box-preordering identities

For clarity, the certificate family consists of identities

    F=sum_(A,B) sigma_(A,B)(x) product_(i in A) x_i
                                  product_(j in B)(1-x_j),

where every `sigma_(A,B)` is a polynomial sum of squares, `A,B` are
subsets of the coordinate set and may overlap, and there is no degree
bound. Coefficients may be arbitrary real numbers.

The [quadratic jet lemma](box-preordering-growth-obstruction.md) states
that a homogeneous quadratic `x'Qx` has such an identity if and only if
`Q` is SPN. Its necessity is local at the origin: nonnegative constant
terms must vanish, then nonnegative linear terms must vanish, leaving a
PSD quadratic jet plus nonnegative cross-products from pairs of lower
slacks. No higher-degree terms can change that jet.

The witness above therefore excludes every finite-degree identity of this
kind for `F`, including dense identities. Sparse versions are subclasses.
The same local argument also excludes finite exact rectangular covers with
one such certificate per cell, as detailed in the existing obstruction.

## Why width two is the minimum for this obstruction

The classical fact that every copositive forest matrix is SPN has a short
direct leaf proof. Let `i` be a leaf with neighbor `j`; isolated vertices
have only a nonnegative diagonal. If `A_ij>=0`, remove the nonnegative
leaf diagonal and cross term, and recurse on the copositive principal
matrix. If `A_ij<0`, copositivity forces `a=A_ii>0`: otherwise
`a t^2+2A_ij t+A_jj` becomes negative for large nonnegative `t`.

In the latter case, extract the rank-one PSD form

    (1/a)(a x_i+A_ij x_j)^2.

Its matrix is rational when `A` is rational. The remainder has a zero
row and column at `i` and changes only the diagonal at `j` by
`-A_ij^2/a`. For every nonnegative remaining vector, the value of that
remainder is the original quadratic at the feasible minimizing leaf
coordinate `x_i=-A_ij x_j/a`. Hence it is copositive. Induction proves
the SPN decomposition.

Graphs of treewidth at most one are forests. Together with the jet lemma,
this proves that width two is minimal for a homogeneous copositive
quadratic lacking the specified unmultiplied box-preordering identity.
This leaf argument is an elementary proof of the classical forest-SPN
property, not a new cone-classification theorem.

## Connected chains at the same width and bounded conditioning

For `m` disjoint five-variable blocks, connect coordinate `1` of successive
blocks and define

    F_m(x)=sum_(b=1)^m (x^(b))' Q x^(b)
             +(1/100)sum_(b=1)^(m-1)(x_1^(b)-x_1^(b+1))^2.

The graph is a chain of fans joined by bridges. Joining their displayed
decompositions with two-variable bridge bags proves width at most two;
triangles give equality. Its input length is `O(m)` up to index encoding,
and all numerical coefficients are fixed rationals.

Termwise growth proves `F_m>=||x||^2/100`. Taking every block equal to
`e1+e2` makes every bridge term zero and attains this ratio. Thus the exact
growth constant remains `g=1/100`, and zero is the unique minimizer.
Each coordinate meets at most two bridges. Hence

    L<=2(101/100+2/100)=103/50,       L/g<=206.

Suppose a full box-preordering identity for `F_m` existed. Restrict it to
one block, setting all other variables to zero. SOS multipliers remain
SOS, and box slacks become original slacks, zero, or one. The resulting
quadratic matrix is

    Q+(d/100)e1 e1',       d in {0,1,2},

where `d` is the block's bridge degree. Its trace product with `W` is at
most

    -4287/100+(2/100)*1773=-741/100<0.

Thus even the restricted matrix is not SPN, contradicting the jet lemma.
Every chain lacks a finite-degree exact unmultiplied box-preordering
certificate. The same negative trace also shows that the chains remain
nonconvex.

## Provenance and verification

The general failure of SPN membership on a five-vertex fan is established
prior work, as recorded in the linked source audit. The explicit congruence
and rational witness here make the growth and chain calculations directly
checkable. They should not be described as discovery of the non-SPN fan.
Comparison with the original displayed matrix and final source-version
checks remain with the literature reader.

A numerical SDP was used only to obtain a candidate separating witness.
Rounding and subsequent exact rational arithmetic supplied the displayed
witness; the proof uses its integer entries and positive determinants, not
floating-point feasibility.

Targeted inline Python calculations checked the Horn congruence, all five
leading principal determinants, the trace identities, and the curvature
row bound exactly. A further `python3 - <<'PY' ... PY` calculation using
`fractions.Fraction` and exact determinants passed 512 single-block growth
samples, 256 connected-chain growth samples, all 36 block restrictions for
chains of lengths one through eight, and eight exact growth equalities.
These finite checks support the formulas; the copositivity and local-jet
proofs establish the continuous-domain and arbitrary-degree claims.

The independent reviewer read the full construction and ran a separate
[exact checker](../reviews/check_fan_preordering_review.py), as recorded
in the linked review. Those reviewer checks are distinct from the author
checks above.

No full preordering was enumerated, and no solver-performance claim was
tested. No external search, project-wide verification, or CI inspection was
performed for this construction.
