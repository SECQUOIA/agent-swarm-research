# Review of the full-separation feasibility transfer

Date: 2026-09-22. Independent adversarial review of
[the oracle investigation](research-20260922-oracle-conjectures.md).

**Assessment.** The candidate proposition is correct under its stated
resisting-adversary assumption and its stated quantifiers. Its geometric
mechanism has a direct published antecedent. It should remain a supporting
lemma, described as an explicit generalization of that mechanism, rather than
an original main contribution. Two qualifications deserve greater prominence:
the distinction between two chart models, and the strong overlap with Basu's
existing mixed-integer feasibility construction.

## Independent reconstruction

Write a query as $q=(x,y)$, with $x\in[0,1]^n$ and
$y\in[-R,R]^d$. For a cube vertex $v$, put

\[
d_v(x)=\sum_i[v_i(1-x_i)+(1-v_i)x_i],\qquad
s_v=(1-2v_i)_i.
\]

The identity $d_v(x)=s_v\cdot(x-v)$ fixes the signs of the proposed
separator. Given a source unit normal $a$ at $y$, the lifted normal

\[
g=(-Hs_v,a)
\]

satisfies

\[
g\cdot((x',y')-(v,y))<0
\quad\Longleftrightarrow\quad
a\cdot(y'-y)<H d_v(x').
\]

At the queried vertex this is exactly the source inequality. At a different
vertex its right side is at least $H$, whereas its left side is at most
$2R\sqrt d$. At any previously accepted fractional point $p$, its right
side is $H d_v(p_x)>0$. There are finitely many such points. Thus one finite
$H$ can preserve all of them, regardless of how close their integer
coordinates are to $v$. The proposed strict bound on $H$ suffices. No
uniform source separation margin is needed.

One potentially confusing step is reusing an earlier normal at a new
fractional query. Let the earlier query be $q_0$, its normal be $g_0$, and
suppose the new query $q$ violates the earlier strict inequality. Then

\[
g_0\cdot(q-q_0)\ge0.
\]

Every point $z$ that satisfied that earlier cut obeys

\[
g_0\cdot(z-q)
=g_0\cdot(z-q_0)-g_0\cdot(q-q_0)<0.
\]

Consequently the old normal remains a strict separator when the hyperplane
is translated to pass through the new query. Equality in the violation test
causes no problem. Caching the response at each full query point handles
repetitions, including queries made before a fiber was retired.

Retiring $v$ uses the normal $(-s_v,0)$, which gives the strict
inequality $d_v(x)>0$. It excludes the entire fiber at $v$ and preserves
all other vertex fibers and all fractional YES points. Prior source
constraints become vacuous on the retired fiber.

For any finite transcript, choose one surviving source set in each active
fiber and take the convex hull of those fibers and all retained YES points.
This is the convex hull of finitely many compact sets in finite-dimensional
space, so it is compact. Each recorded strict inequality holds on every
constituent and hence on every point of the convex hull. Later YES points
were explicitly tested against all previous cuts; earlier YES points were
protected by the choice of tilt. These are both necessary parts of the
consistency argument.

A convex combination of points in the cube can have first coordinate equal
to a vertex $v$ only if every positively weighted point has first coordinate
$v$. Therefore fractional YES points cannot enlarge any integer fiber. The
final fiber at $v$ is exactly its selected source set if active, and empty
if retired.

Fewer than $2^n(L+1)$ queries cannot retire every vertex. At least one
rho-fat fiber survives. If the output lies in an active fiber, the empty
intersection of its surviving source family permits choosing that fiber's
set to exclude the output. This final selection does not invalidate the
other cuts or the fractional YES responses. An output outside the product
box, in a retired fiber, or asserting infeasibility already fails.

Finally, extend the finite cached responses to a total chart. At unqueried
points in the final set use YES; at exterior points use a normalized strict
separator, which exists for every nonempty compact convex set. Thus the
transcript is realized by one set and one chart fixed for the completed run.
The construction does not merely use an inconsistent sequence of locally
valid cuts.

The same reasoning covers $L=0$, boundary points of the known product box,
and an algorithm stopping before its query budget is exhausted. Queries
outside the product box can be answered by fixed strict box separators.

## Source lower bound and quantifiers

The decision-tree argument deriving the source assumption is valid for the
stated unrestricted deterministic model. A residual family with a common
feasible point is solvable with zero further queries. If a residual family
cannot be solved with $k>0$ further queries, every proposed next query has
some response whose residual family cannot be solved with $k-1$ further
queries. Otherwise residual successful strategies could be selected for
each response and combined into a successful strategy. The lower-bound
assumption supplies the initial unsolvable family. A YES response cannot
maintain the invariant because its query point solves every survivor.

This argument uses unrestricted selections, as the note says. It is not a
polynomial-time reduction. It also depends on the source class containing
only nonempty sets. For a class containing empty instances, uncertainty
between an empty set and a nonempty set can prevent termination without
producing an empty intersection among the nonempty survivors.

There are two different chart quantifier orders:

\[
\forall A\ \exists(C,g)\quad A\text{ fails on the charted instance }(C,g),
\tag{A}
\]

and

\[
\exists G\ \forall A\ \exists C\quad
A\text{ fails on }C\text{ under the class-wide chart }G.
\tag{B}
\]

The proposition proves (A). Its final chart may depend on the algorithm and
the transcript. This is the appropriate lower-bound statement when an
algorithm must work for every valid separation chart, or when charted sets
are the instances. It does **not** by itself prove (B). Extending one finite
transcript to a chart does not make the charts constructed against different
algorithms mutually compatible on a common geometric set.

The distinction is consequential when comparing sources. Theorem 7 and
Conjecture 2 of Basu–Jiang–Kerger–Molinaro use a class-wide chart fixed before
the query strategy; their constrained transfer question is Conjecture 1.
Their oracle and information-complexity definitions are in Sections 1 and
1.1. The present argument should not be described as establishing their
fixed-chart transfer theorem even in the feasibility special case without
an additional uniformization argument.
[Primary paper](https://optimization-online.org/wp-content/uploads/2023/08/information_complexity_of_convex_mixed_integer_opti.pdf).

## Direct prior mechanism and significance

The closest source is more specific than the general bounds cited in the
draft. Basu's *Complexity of optimizing over the integers*, Section 4.1,
proof of Theorem 4.2 for $n,d\ge1$, already uses the following construction:
independent cube-vertex fiber boxes, rotated cuts that leave other fibers
intact, retirement after sufficiently many fiber queries, fractional YES
answers, and a final convex hull containing those YES points. It obtains
the familiar $2^n d\log(R/\rho)$ feasibility lower bound. The displayed
proof does not explicitly impose preservation of earlier fractional YES
points when choosing the rotations. The draft's finite-$H$ estimate makes
that condition explicit and establishes it. Replacing coordinate-box
adversaries by an arbitrary source resisting adversary is also an extension.
The underlying geometric method is already present, however.
[Primary source, arXiv:2110.06172v6, Section 4.1](https://arxiv.org/html/2110.06172v6).

There is also a simple ceiling on the asymptotic significance of a transfer
restricted to full separation. For a nonempty continuous set containing an
infinity-norm ball of radius rho in a known box, exact centroid cuts find a
feasible point in $O(1+d\log(R/\rho))$ oracle calls: every NO response
removes a constant fraction of the localization volume, while the surviving
set always contains volume $(2\rho)^d$. Thus arbitrary full-separation
source hardness in this class cannot exceed the scale that the classical
mixed-integer lower bound already multiplies by $2^n$, in its nondegenerate
parameter regime. The lemma packages a direct construction and preserves
the chosen source fiber family, but establishes no new general asymptotic
rate. It preserves neither a useful algebraic description nor a bound on
input bits or separation conditioning.

I recommend replacing the draft's phrase “original lemma” by “an explicit
arbitrary-source version of the classical fiber construction.” An exact
equivalent statement may occur elsewhere; this review does not establish
novelty of the generalization.

## Current literature status

The July 2026 exact-value result is real and the draft describes its scope
correctly. Kerger's Theorem 4 gives deterministic complexity
$\Omega(d^2/\log(d+1))$ at one universal constant times $d^{-1/2}$
accuracy. Corollary 2 supplies the $2^n$ mixed-integer factor. Smaller
accuracies inherit the same lower bound by monotonicity, but no additional
multiplicative accuracy logarithm follows. The theorem permits exact real
values and unrestricted deterministic query maps. It gives no subgradient
information, so it cannot directly establish a lower bound against general
binary first-order queries.
[Kerger, arXiv:2607.13335v1, Theorem 4 and Corollary 2](https://arxiv.org/html/2607.13335v1).

The bit-oracle paper has a later version than the title used in the draft:
arXiv:2511.02082v2, dated 14 July 2026, is titled *Tight Lower Bounds for
Binary First-Order Oracles for Convex Optimization*. Despite the broader
title, Theorems 3 and 4 still concern coordinate and inner-product access,
respectively. They do not settle the arbitrary-binary-query conjecture.
Definition 2 explicitly requires a single algorithm to succeed for every
valid first-order map. Therefore (A), unlike (B), matches this version's
feasibility model. The changed model definition should be acknowledged in
a careful comparison.
[Basu–Kerger–Molinaro, arXiv:2511.02082v2](https://arxiv.org/html/2511.02082v2).

These comparisons concern theorem statements and models. This review did
not independently verify the long proof of Kerger's near-quadratic theorem
or its reported Lean development. The precise current status of the broad
conjectures remains qualified by the scope of the source search.

## Partial-information limitation

The draft is right not to claim a partial-information transfer. More
precisely, an adversary is allowed to perform free internal computation;
the obstruction is not that it must pay to inspect its own known vectors.
The obstruction is that a lower-bound adversary for a partial-information
source may not have fixed a complete normal consistent with all future
responses. Deciding whether to accept a fractional point using a chosen
completion can constrain that hidden normal and destroy the source
hardness invariant. A valid reduction needs a consistent completion or a
query simulation preserving the relevant permissible-query model. The
present proof supplies neither.

## Verification record

I reconstructed the signs, reused-normal step, finite tilt bound,
retirement, compact final-set consistency, exact integer fibers, final
output exclusion, repeated queries, and the chart extension independently.
I checked the primary sources linked above, including the current v2
bit-oracle paper and the direct older fiber construction. No mathematical
counterexample to the proposition as stated was found. The main correction
is to its provenance and model comparison, not its proof.

No numerical calculation or Lean check would materially resolve the chart
quantifier or novelty questions here, and none was run. No project-wide
verification or CI inspection was performed.
