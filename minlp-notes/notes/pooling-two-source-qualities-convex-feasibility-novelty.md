# Two source-quality vectors: focused source comparison

Date: 2026-09-05. This is a bounded primary-source comparison of the
complete derivation in
[the two-quality investigation](pooling-two-source-qualities-convex-feasibility.md),
including its Section 6 source-supply-interval extension. Mathematical
audits are separate.

No matching theorem was located in the primary pooling sources checked.
The plausible contribution is an exact convex reformulation of a
restricted physical feasibility problem. It is not a new convex-QP
algorithm, a general pooling convex hull, or an economic optimization
theorem. Search absence does not establish exhaustive priority.

## Exact scope being compared

The class has one pool, at most two distinct rational source-quality
vectors, and unrestricted numbers of sources, products, conserved
attributes, and bypass arcs. Sources may have distinct finite supply
intervals and different feed and bypass bounds. Products have exact
demand and quality contracts. Every pool-outlet lower bound and the
common pool lower bound is zero; individual outlet upper bounds and an
arbitrary restrictive common pool upper bound remain. There are no
additional economic requirements. The output is an exact feasibility
decision and a polynomial-size rational physical witness.

Two distinct source vectors do not mean two physical sources. Combining
sources by their common quality can destroy their separate supply and
arc restrictions. The proposed method retains those rows explicitly.
Likewise, two distinct vectors is substantially stronger than affine
quality rank one: rank one can permit arbitrarily many different values.

The candidate's decisive identity, after normalizing the two values to
zero and one, is

```
W_0j = q b_j(B_j-1) + q(1-q) v_j.
```

The bounds `0 <= v_j <= U_j` therefore give an affine lower bound and a
concave quadratic upper bound on `W_0j`. The same identity summed over
products handles common pool capacity. A shared variable `r >= q^2`
makes every other row linear. Exact product contracts also fix consumed
totals of the two source classes, allowing individual source supplies
to vary without introducing another nonlinear balance. The resulting
test minimizes `q^2-r` over a rational polytope. Original fixed-quality
LPs handle singular endpoints; the strict interior branch has a separate
exact rational recovery argument.

## Earlier polynomial pooling subclasses

Boland, Kalinowski, and Rigterink, *A polynomially solvable case of the
pooling problem* (2015 preprint; published 2017), prove polynomial
solvability for one pool and a fixed number of inputs. Their model
explicitly excludes direct input-to-output arcs on PDF page 2. Replacing
each bypass by an auxiliary pool preserves a model but increases the
number of pools. Thus their theorem does not directly apply to this
arbitrary bypass class, even if sources could otherwise be aggregated.
The model definition and the main reduction on PDF pages 5–7 were read.
[Primary manuscript](https://optimization-online.org/wp-content/uploads/2015/08/5059.pdf).

Baltean-Lugojan and Misener, *Piecewise parametric structure in the
pooling problem: from sparse strongly-polynomial solutions to
NP-hardness* (2017/2018), is the closest checked tractability comparison
with bypasses and fixed product demands. Assumption 2.2, PDF page 5,
drops feed availability and pool capacity, restricts to one conserved
quality, and fixes demands. Its Section 4 solves the corresponding
one-pool, multiple-output economic problem. These passages and Remark
4.6 on PDF page 24 were reread. The present feasibility class retains
availability and restrictive pool capacity, but requires exact product
qualities and only two distinct source values. The classes therefore
trade restrictions; this is not a blanket improvement of their economic
algorithm. Their discussion of hardness when assumptions are relaxed
does not establish hardness of every further restricted subclass.
[Primary manuscript](https://optimization-online.org/wp-content/uploads/2016/05/5457.pdf).

## Established convexification ingredients

Luedtke, D'Ambrosio, Linderoth, and Schweiger, *Strong Convex Nonlinear
Relaxations of the Pooling Problem* (2018 preprint; published 2020),
already use excess-quality contributions, quality-times-flow variables,
and aggregated pool/bypass flows. Section 3, PDF pages 4–5, explicitly
relaxes to one attribute, one product, and one selected pool before
studying its five-variable set. Its convex hull inequalities strengthen
the full pooling relaxation. Those passages do not give the present
exact full-model feasibility equivalence. Signed quality mass is an
established modeling idea; the candidate's specific common-pool scaling
and simultaneous exactness under all retained capacity rows are the
points requiring credit and review.
[Primary manuscript](https://arxiv.org/pdf/1803.02955).

Dey, Kocuk, and Santana, *A study of rank-one sets with linear side
constraints and application to the pooling problem* (2019), give exact
polyhedral or second-order-cone convex hull descriptions for selected
rank-one sets. Theorem 2 handles two arbitrary linear side constraints;
later results handle specified row/column structures. Section 3.3 applies
these results to obtain pooling relaxations. The theorem statement and
pooling application on PDF pages 5 and 11–13 were read. Two source
quality classes are not two linear side constraints. Moreover, replacing
a rank-one substructure by its convex hull and then intersecting with
all remaining physical rows need not preserve feasibility. This paper
therefore provides important convexification precedent, but its checked
results do not directly supply the proposed full-model equivalence.
[Primary manuscript](https://www2.isye.gatech.edu/~sdey30/RankonePool.pdf).

The polynomial algorithm for rational convex quadratic programming is
classical: Kozlov, Tarasov, and Khachiyan, *The polynomial solvability of
convex quadratic programming*, 1980, with a 1979 announcement. The primary
bibliographic record was checked. The candidate invokes this established
primitive; this source comparison does not independently reprove its
bit-complexity theorem. The rank-one objective also avoids relying on a
general assertion about exact rational SOCP feasibility.
[Primary record](https://www.mathnet.ru/eng/zvmmf5189).

## Search boundary and recommended positioning

Fresh searches combined pooling, two distinct qualities or concentrations,
two inputs, exact or fixed demands, convex quadratic feasibility, and
rank-one convexification. Results about statistical, economic signaling,
and neural-network pooling were excluded. The additional
Haugland–Hendrix polynomial-algorithm paper was located bibliographically,
but a primary full text was not obtained in this bounded review, so no
independent detailed model comparison with it is claimed here.

Recommended statement: “For one-pool instances with two distinct source
quality vectors and exact product contracts, a signed flow transformation
reduces feasibility to rational convex quadratic programming, despite
unrestricted bypass topology and retained supply and capacity bounds.
No equivalent theorem was found in the primary sources checked.”

The restriction to zero pool and outlet lower bounds is material: positive
lower bounds give the opposite quadratic curvature. The two-quality
restriction is also material to this derivation. Feasibility and rational
witness recovery do not imply polynomial economic optimization when
individual source use varies. These boundaries should remain in any
abstract or comparison table, alongside the completed independent proof
audits.
