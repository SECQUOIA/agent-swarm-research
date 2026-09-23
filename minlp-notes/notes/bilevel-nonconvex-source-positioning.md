# Source positioning for the nonconvex scalar implementation

Date: 2026-09-07. This bounded audit concerns the
[scalar implementation](bilevel-nonconvex-scalar-algorithm.md), not the
full fixed-aggregate theorem. It records an established computational
antecedent and a useful implementation pitfall. Neither is claimed as a
new discovery in convex analysis.

## The scalar value function is a classical conjugate

After the strictly convex resource-allocation fiber has been minimized,
write its piecewise quadratic value as `C(w)` and set
`psi(w)=C(w)-h*w^2/2`, extended by `+infinity` outside its aggregate interval.
The tariff-dependent global follower value is

```
v(x) = min_w [psi(w)+gamma*x*w] = -psi*(-gamma*x),
psi*(p) = sup_w [p*w-psi(w)].
```

Thus the global scalar comparison step is an instance of computing the
Legendre–Fenchel conjugate of a nonconvex univariate piecewise quadratic
function. This identity follows directly from the definition, and rules
out treating the scalar envelope operation itself as novel.

Gardiner and Lucet, *Convex Hull Algorithms for Piecewise Linear-Quadratic
Functions in Computational Convex Analysis*, Set-Valued and Variational
Analysis 18 (2010), 467–482, give quadratic-time and linear-time algorithms
for the univariate piecewise quadratic convex envelope. The former is
described as easier to implement. This audit verified the publisher's public
abstract and the author bibliography; it did not retrieve the full original and does
not import its detailed algorithm or a bit-complexity theorem.
[Author publication list](https://cmps-people.ok.ubc.ca/ylucet/research.php),
[publisher abstract](https://link.springer.com/article/10.1007/s11228-010-0157-5).

An openly accessible constructive account is Moehle, Gindi, Boyd, and
Kochenderfer, *Portfolio Construction as Linearly Constrained Separable
Optimization*, arXiv:2103.05455v2, Section 6.3 and Appendix B, printed
pp.13–14 and 21–24. It constructs a piecewise quadratic convex envelope
incrementally using common supporting lines; its tangent cases reduce
to quadratic equations. This is a direct computational antecedent, although
the paper's portfolio solver is a heuristic with bounds, not an exact
bilevel algorithm. The relevant full text was inspected. Its final
publication is Optimization and Engineering 24 (2023), 1667–1687.
[Open primary manuscript](https://arxiv.org/pdf/2103.05455v2),
[author publication page](https://stanford.edu/~boyd/papers/portf_constr_lcso.html).

The local fiber formulas also have the already recorded
[resource-allocation antecedents](bilevel-fixed-aggregate-response-novelty.md).
The implementation's defensible role is a reproducible exact specialization
of the repository's broader theorem, including reconstruction of all actual
global responses and upper-level feasibility and attainment decisions.
No claim of the first algorithm for diagonal-minus-rank-one box QP, or for
univariate nonconvex conjugation, is made.

## Correct values do not guarantee correct follower choices

Let `psi**` be the closed convex envelope. Replacing `psi` by `psi**`
preserves the minimum under every linear tariff, but can add minimizers.
The actual response set is

```
argmin_w [psi(w)+gamma*x*w]
  = {w in argmin_w [psi**(w)+gamma*x*w] : psi(w)=psi**(w)}.
```

To verify this, let `m` be the original minimum. The affine function
`m-gamma*x*w` lies below `psi`, hence below its convex envelope. The relaxed
minimum is therefore at least `m`, and the opposite inequality follows
from `psi**<=psi`. Equality at an original minimizer forces contact;
a relaxed minimizer at contact has original value `m`. This proves the
display without assumptions about uniqueness.

A one-coordinate example makes the consequence explicit. Set `d=1`,
`c=-1`, `u=1`, `h=3`, `gamma=1`, `z in [0,1]`, and `x in [1,3]`.
The follower minimizes

```
-z^2+(x-1)*z.
```

Its actual responses are `{1}` for `x<2`, `{0,1}` for `x=2`, and `{0}`
for `x>2`. The untariffed convex envelope is `-2*z`. At `x=2` its
relaxed response set is the whole interval `[0,1]`. The upper equality
`z=1/2`, expressed by two affine inequalities, is infeasible for every
true response at every tariff. The convexified reaction model declares
it feasible at `x=2`, with apparent revenue `1`.

This is why the implementation keeps original minimizing branches and
original flat intervals. A future faster convex-envelope implementation
must preserve the contact test; using the relaxed argmin graph directly
can give false optimistic feasibility even when every follower value is
correct. The example is a regression case, not a priority claim.

The [reproducible figure](../code/bilevel_nonconvex/figures/convex_envelope_false_choices.pdf)
shows the cost and the resulting false response choices. Its
[plot script](../code/bilevel_nonconvex/plot_contact_example.py) also exports
SVG and PNG versions.

## What the experiment can establish

The implemented leader enters only through the aligned linear tariff
`gamma*x*(u^T*z)`, and the aggregate nonconvexity is quadratic. It supplies
computational evidence for this specialization. It does not implement
two leader variables, general polynomial aggregate costs, moving normals,
or shared follower resource constraints from the full theorem. Exact
arithmetic runtimes must also be reported separately from floating-point
heuristic runtimes and from fixed-price follower queries.
