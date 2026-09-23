# Independent second review of the strict PDLC four-bound transfer

Date: 2026-09-22.

Reviewed draft: [candidate theorem](research-20260922-pdlc-frontier.md).
This review independently reconstructed the mathematical argument rather
than relying on the author's conclusions or another review.

**Conclusion:** I found no mathematical gap in Lemmas A–E or their
composition. Subject to the cited four-bound theorem, the argument proves
the stated result for three linearly independent homogenized quadratics in
dimension `n >= 3`, with a nonempty strict feasible set and a proper ordinary
convex hull. The proof includes the singular cases that could otherwise
invalidate the limit argument. This is a mathematical review, not a
confirmation of novelty or of all versions of the literature inputs.

## Literature input checked independently

I inspected [Blekherman–Dunbar, arXiv v1, Theorem
1.4](https://arxiv.org/html/2405.18282v1). Its stated assumptions are PDLC,
`C = cl(int C)`, nonempty interior, and no nonzero feasible homogenized
point at infinity. It gives at most four good aggregations for the closed
convex hull. The surrounding definitions require permissible aggregates
to have at most one negative eigenvalue. The theorem does **not** state a
smoothness assumption on the spectral curve. Such assumptions occur in
other theorems in that paper and must not be imported into this one.

The linked published full-text endpoint was inaccessible during this
review. Thus my independent source check supports an invocation of the
identified preprint theorem. It does not independently certify that every
word of the published theorem is identical. I also checked Corollary 2.6
and Theorem 2.8 in the repository's Blekherman–Dey–Sun full text; together
they provide the initial strict-good aggregate under the stated dimension,
PDLC, nonemptiness, and proper-hull assumptions.

## Reconstruction of the proof

### 1. Generic inward levels work simultaneously at every point

Let `L` be the set of local minimizers of the continuous semialgebraic
function `h` on its semialgebraic domain. Its definition uses only
first-order quantifiers over the reals, so both `L` and `h(L)` are
semialgebraic. If `h(L)` contained an interval, semialgebraic selection
would provide a section `c -> z(c)` with `h(z(c)) = c`; on a smaller open
interval this section is continuous. Fixing any interior level `c0`, the
points `z(c)` with `c < c0` approach `z(c0)` and have smaller function
value. This contradicts local minimality at `z(c0)`. Consequently `h(L)`
is finite.

If a point of `{h <= c}` is not in `cl{h < c}`, it has value exactly `c`
and has a neighborhood with `h >= c`. Hence `c` belongs to that finite
set. The conclusion therefore concerns every point of each retained
level, not just almost every point or a point-dependent sequence of
levels. This resolves the relevant quantifier issue in Lemma A.

For `h(z) = max_i z^T Q_i z` on the unit sphere, the perturbed system is
the level `h <= -epsilon`. Homogeneous rescaling then gives regularity
away from zero. At zero, scaling a single nonzero strictly feasible point
to zero gives the required closure inclusion. Such a point exists for
all sufficiently small positive epsilon by the fixed original feasible
point. Thus one may choose a single decreasing sequence of admissible
epsilon values tending to zero.

### 2. Singular initial cones cause no ambiguity

A symmetric matrix with exactly one negative eigenvalue has an orthogonal
coordinate representation

```
q(s,y,w) = -a s^2 + sum_i b_i y_i^2,
a > 0, b_i > 0,
```

where `w` comprises any null directions. Its negative set has precisely
the two convex components

```
s > sqrt(sum_i b_i y_i^2 / a),
s < -sqrt(sum_i b_i y_i^2 / a).
```

The same description includes the rank-one negative semidefinite case:
the two components are then the open halfspaces `s > 0` and `s < 0`.
They are always distinguished by the sign of the scalar product with a
negative eigenvector.

For an original strict-good aggregate, the connected lift of `conv(S)`
lies in its negative set. Therefore all lifted feasible points occupy one
of these components. After adding `epsilon I`, all zero eigenvalues
become positive and the unique negative eigenvalue stays negative for
small epsilon. The new negative set lies in the old negative set. Each
new component lies in a single old component, and antipodality assigns
them to opposite old components. Since `S_epsilon` is contained in `S`,
its lifts all occupy the same new component. This proves strict goodness
for the inward system, without requiring the old aggregate to be
nonsingular.

PDLC persists because a fixed signed positive definite combination
changes by a scalar multiple of `epsilon I`; sufficiently small changes
preserve positive definiteness. Linear independence is also an open
condition on a finite list of matrices.

### 3. The new affine chart has exactly the intended strict component

Choose the negative eigenvector of the perturbed good aggregate as the
new chart functional `l`, with the feasible sign positive. A vector
strictly satisfying every perturbed original inequality also satisfies
the perturbed aggregate. Thus `l > 0` puts it in the designated negative
component.

If such a vector had original homogenizing coordinate `t < 0`, its
antipode could be divided by its positive `t` coordinate to give an
original-chart feasible lift. That lift would be in the designated
component, while the antipode is in the opposite component. A strict
feasible vector with `t = 0` is also impossible: openness allows a nearby
strict feasible vector with `l > 0` and `t < 0`. Hence every strict point
in the new chart has `t > 0`. The reverse chart map is therefore defined
on the whole strict feasible set, not just a selected subset.

The aggregate is positive definite on `ker(l)`. Its nonpositive section
at `l = 1` is a bounded ellipsoid, so the new nonstrict feasible set is
bounded and has no points at infinity. For a generic epsilon, sphere
approximants to any nonstrict point have positive `l` eventually;
normalizing them to `l = 1` gives strict chart approximants. This proves
`C_epsilon = cl(T_epsilon)`, not merely homogeneous regularity in an
unrelated chart. Since `T_epsilon` is nonempty and open, it also proves
the regularity and interior assumptions of the four-bound input.

### 4. Strictification and the original chart are both justified

After applying the four-bound theorem, remove aggregate polynomials that
are globally nonpositive on the new affine chart. For any other quadratic
`p`, a zero in the interior of `{p <= 0}` would be a local maximum of
value zero. The Hessian would be negative semidefinite and the gradient
zero. The quadratic Taylor formula would then imply `p <= 0` globally,
a contradiction. Thus the interior of its nonpositive sublevel is exactly
its negative sublevel.

The interior of a finite intersection equals the intersection of the
interiors. Also, a nonempty open convex set is the interior of its
closure. These facts give the asserted strict description of
`conv(T_epsilon)`. Some inequality remains because this hull is bounded
and the ambient chart has positive dimension.

Let `G` be the common strict homogeneous sublevel of the remaining
aggregates. A nonzero point of `G` in `ker(l)` would, by openness, admit
nearby points with arbitrarily small positive `l`. Dividing by `l` would
produce unbounded points in the bounded section `conv(T_epsilon)`.
Therefore `G` has no nonzero point with `l = 0`. Homogeneity and
antipodality now identify all of `G` with the positive cone over that
section and its negative. There is no third component hidden outside the
chosen projective chart.

Every point in `conv(T_epsilon)` has `t > 0`, because every point in
`T_epsilon` does and convex combinations are finite. Thus the negative
cone has `t < 0` and contributes no point to the original section `t = 1`.
Finally, taking finite positive conical combinations of the feasible lifts
and then intersecting with either positive affine section commutes with
taking the corresponding ordinary convex hull. This proves the global
original-coordinate equality in Lemma D, including points initially
outside the domain of a projective formula.

### 5. The strict limit retains both validity and exactness

Pad to four aggregates by duplication and normalize their multipliers
in the nonnegative simplex. A simultaneous subsequence converges. Every
limit multiplier is nonzero, and its quadratic value is strictly negative
at **every** original feasible point, because each original constraint is
strict there. Matrix convergence gives at most one negative eigenvalue;
negativity at a fixed feasible lift gives at least one.

To check component orientation, take normalized negative eigenvectors of
the approximating matrices, with positive scalar product at a fixed
feasible lift. Their negative eigenvalues remain bounded away from zero:
the quadratic value at that fixed vector converges to a negative number,
which bounds the smallest eigenvalue above by a negative constant. A
convergent subsequence of eigenvectors is therefore a negative
eigenvector of the limit matrix, rather than a vector in its nullspace.

Every other fixed feasible point belongs to all sufficiently small inward
systems. Its scalar product with the oriented eigenvector is positive at
those stages and nonnegative in the limit. It cannot be zero in the
limit, because the limit quadratic is strictly negative there, while the
quadratic is nonnegative on the orthogonal complement of the unique
negative eigenvector. All feasible lifts consequently belong to one
convex negative component of each limit aggregate. Finite convex
combinations remain in that open component. This establishes strict
validity on the ordinary convex hull even for a rank-one negative
semidefinite limit.

Conversely, a point strictly satisfying all four limiting inequalities
satisfies every approximating inequality for all sufficiently large
indices, since there are only four of them. It therefore belongs to an
inward hull, which is contained in the original hull. This proves
exactness. No closure of the original convex hull and no interchange of
an infinite intersection with a limit is needed.

## Adversarial checks and limitations

The deletion step in Lemma D is essential. For example, the closed
interval `[-1,1]` is the common nonpositive sublevel of `x^2 - 1` and
`-x^2`. Replacing both inequalities by strict inequalities removes zero
and gives a disconnected set. Deleting the globally nonpositive second
polynomial first gives the correct interior. The draft handles this
failure explicitly.

Rank-one negative semidefinite limits were a second candidate failure.
Their strict sublevels exclude an entire hyperplane even though their
nonstrict sublevels are the whole space. The oriented-component argument
above excludes that hyperplane from the original hull and therefore
addresses this failure; ordinary nonstrict validity alone would not.

The dependent-triple reduction and dimensions below three remain outside
the proved statement in the draft. This review does not silently add
them. It also does not establish that the proof or its conclusion is
absent from the dissertation or later sources. Those comparisons remain
necessary before an originality claim.

No numerical experiment or Lean proof was used. The review checks the
general mathematical argument directly, including singular matrices and
the relevant universal quantifiers. Only the identified local source
passages and primary web source were inspected; no project-wide checks
or CI checks were run.

## Addendum: independent recheck of the shorter proof

The author subsequently proposed a substantial simplification. I checked
it separately. **The simplification is correct**, and it removes the
initial good-aggregation theorem and the projective-chart argument from
the proof of the main result.

First, let `h` be a continuous real-valued function on a space `M` with a
countable base. If

```
{h <= c} != cl_M {h < c},
```

continuity implies that there is a point `x` in the left side but not the
right side. It has `h(x) = c`. Choose an open neighborhood of `x` that
avoids `{h < c}`, and then a member `B` of the countable base containing
`x` and contained in that neighborhood. On `B`, `h >= c`, with equality
at `x`, so `c = inf_B h`. Thus every exceptional level belongs to the
countable collection of those infima that are real numbers. No
semialgebraic selection, differentiability, compactness, or uniform
neighborhood radius is required. A decreasing positive sequence
`epsilon_k -> 0` avoiding the exceptional negative levels can be selected
recursively in nonempty intervals, since an interval cannot be exhausted
by a countable set.

Second, write the original quadratics as

```
f_i(x) = x^T A_i x + 2 b_i^T x + c_i.
```

If a nonzero direction `d` satisfied `d^T A_i d < 0` for every `i`, then
for any fixed `x` both `x + t d` and `x - t d` would satisfy all original
strict inequalities for sufficiently large positive `t`. The negative
quadratic term dominates both linear terms. Their midpoint is `x`, so
the ordinary convex hull would be all of `R^n`. Properness of the hull
therefore rules out every such direction, in every positive dimension.

Consequently, for every `epsilon > 0`, a nonzero direction satisfying

```
d^T (A_i + epsilon I) d <= 0 for all i
```

would imply the forbidden strict inequalities for the original leading
forms. The perturbed system has no nonzero nonstrict point at infinity
in the original chart. It is also bounded: an unbounded feasible sequence
`x_j`, divided by `||x_j||`, has a subsequence tending to a unit direction;
dividing all feasible inequalities by `||x_j||^2` would give precisely
such a point at infinity.

Now apply the countable-base lemma directly on `R^n` to

```
h(x) = max_i f_i(x) / (1 + ||x||^2).
```

Its strict and nonstrict sublevels at `-epsilon` are exactly the strict
and nonstrict systems for `Q_i + epsilon I`. At each retained level the
nonstrict feasible set is the closure of the strict feasible set. The
latter is nonempty and open for sufficiently small epsilon. All
hypotheses of the four-bound theorem therefore hold in the original
chart. Strictification after deleting globally nonpositive quadratics
and the previously reviewed multiplier-limit argument complete the
proof without any projective map.

Finally, the dimension restriction can be removed for linearly independent
triples. The inspected BD preprint's Theorem 1.4 has no dimension
exclusion. Its Section 8 explicitly handles `n = 1` and `n = 2` in
Proposition 8.7, and then treats `n >= 3` separately. The shorter transfer
requires no initial BDS theorem and every remaining step holds for
`n >= 1`. Thus, relative to the stated BD theorem, the corrected scope is
**all positive dimensions for linearly independent triples**. The earlier
paragraph excluding low dimensions describes the superseded longer
proof; it is not a limitation of this shorter argument.

This addendum leaves the prior caveats about publication-version checking,
dependent triples, and novelty in place. It uses mathematical reasoning
and the identified theorem statements, not computational verification.
