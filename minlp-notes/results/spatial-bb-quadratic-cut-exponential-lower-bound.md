# Spatial lower bounds with every quadratic box cut

Date: 2026-09-05. Status: independently verified by two reviewers. Novelty
remains provisional after the targeted literature search below. The SOS
construction is classical; the proposed contribution is the spatial cover
transfer with exact node quadratic moment information.

Reviews: [first audit](../notes/review-spatial-bb-beyond-clique.md) and
[second audit](../notes/review-spatial-bb-beyond-clique-second.md).
[Investigation record](../notes/spatial-bb-beyond-clique-investigation.md).
The [monomial-lifting extension](spatial-bb-monomial-lift-exponential-lower-bound.md)
covers branching on bounded-degree product auxiliaries.

## Main result

There are constants `c>0` and `n0` such that for every sufficiently large
`n`, a multilinear cubic polynomial `F_n:[-1,1]^n -> [0,1]` has all the
following properties:

- `min F_n >= 1/8`.
- Every variable occurs in at most 64 of its three-variable terms.
- For any integer `2<=r<=c n`, a spatial branch-and-bound certificate of
  absolute gap `1/16` requires at least `2^(7n/1024)` leaves, even when each
  node receives the full degree-`2r` box preordering relaxation **and the
  exact degree-two moment hull of its node box**.
- The same bound holds for certifying relative gap `1/2`.

The degree-two hull condition means that the first and second moments must
be representable by an actual probability distribution on the entire node
box. Equivalently, the node oracle receives every quadratic polynomial
inequality valid on that box. This includes all valid continuous versions
of Boolean-quadric clique inequalities, not merely a selected standard cut
family. The objective has degree three, so its unknown optimum is not itself
a quadratic cut.

The oracle adds these quadratic cuts as linear inequalities on degree-two
moments. It does **not** automatically include every product or SOS localizer
of every such global quadratic inequality. That stronger closure remains
outside the current proof. Ordinary full preordering products of the
coordinate-bound generators are included through degree `2r`.

A spatial certificate here is a finite cover of the original cube by
regions, each certified to meet the requested objective lower bound by its
stated node oracle. In a complete variable-split tree without additional
domain deletion these regions are its leaves. If objective-based propagation
discards feasible points, separately certified discarded regions must also
be included in the cover and in the region count. The theorem does not
justify counting only the final leaves after uncharged propagation.

## A general transfer theorem

Let a signed 3-uniform constraint multihypergraph have `n` variables, `m`
clauses, maximum variable occurrence `Delta`, and signs `b_e in {-1,1}`.
Consider

```
F(x)=(1/m) sum_e (1-b_e prod_{i in e}x_i)/2,  x in [-1,1]^n.
```

Each clause uses three distinct variables; repeated clauses are permitted.
Because `F` is multiaffine, its minimum on the cube equals its minimum on
Boolean vertices. Every term lies in `[0,1]` throughout the continuous cube.

Assume a Boolean pseudoexpectation `E` is available through degree `4r`,
where `r>=2`, such that:

1. `E[1]=1`, `E[p^2]>=0` whenever `deg(p)<=2r`, and Boolean reductions
   `x_i^2=1` are respected through degree `4r`.
2. `E[prod_{i in e}x_i]=b_e` for every clause; hence `E[F]=0`.
3. Its degree-two moment vector is realized by an actual probability
   distribution on `{-1,1}^n`.

For a box `B=prod_i[a_i,b_i] subset [-1,1]^n`, define `LB_r(B)` by minimizing
`L[F]` over normalized functionals through degree `2r` satisfying:

- `L[g p^2]>=0` for every product `g` of the node-bound slacks `x_i-a_i` and
  `b_i-x_i`, including repetitions and the empty product, whenever
  `deg(g)+2deg(p)<=2r`;
- the degree-two moment vector of `L` belongs to
  `conv{(x,xx^T):x in B}`.

This is a valid relaxation of continuous minimization on `B`. The second
condition need not be computationally tractable; granting it makes the
lower bound stronger.

**Transfer theorem.** Every cover of `[-1,1]^n` by boxes with
`LB_r(B)>=T>0` has at least `2^(m T/Delta)` members. In particular, an
absolute-gap certificate uses `T=OPT-epsilon`, while a relative-gap
certificate uses `T=(1-theta)OPT`, whenever the target is positive.

*Proof.* Choose witnesses uniformly from all `2^n` Boolean vertices. For a
box containing witness `w`, let `R` be the coordinates whose interval
excludes at least one endpoint of `[-1,1]`, and put `U=[n] minus R`.
Every `U` interval is `[-1,1]`. Define `L` by fixing `x_R=w_R` and applying
the marginal of the original pseudoexpectation to the remaining variables:

```
L[p(x)] = E[p(w_R,x_U)].
```

This is substitution followed by marginalization, **not conditioning** on
an event under `E`. It is defined through degree `2r` and normalized.

For preordering positivity, the restricted-coordinate slack factors become
nonnegative constants. Each remaining bound slack is `1+x_i` or `1-x_i`.
Modulo `x_i^2=1`, their product is either zero or a nonnegative scalar times
a Boolean assignment indicator `I`. If `v` distinct coordinates occur in
that indicator, then `v<=deg(g)`. Boolean idempotence gives
`I p(w_R,x_U)^2=(I p(w_R,x_U))^2`. The squared polynomial has degree at most
`2[v+deg(p)]<=4r`. Positivity of `E` therefore proves every required node
preordering inequality. Repetitions and conflicting factors cause no issue.

Let `mu` be an actual Boolean distribution realizing `E` through degree
two. Take its marginal on `U` and set `x_R=w_R` deterministically. This is
an actual distribution supported in `B` and its first two moments agree
with `L`. Thus `L` satisfies the exact quadratic moment hull requirement.

Clauses supported wholly in `U` retain pseudo-cost zero. At most
`Delta|R|` clauses touch `R`. After substitution, each such clause has form
`(1-sigma x_S)/2` with `|S|<=3`. Its pseudoexpectation is in `[0,1]`:
Boolean positivity gives `|E[x_S]|<=1`, for example by applying positivity
to `(1+x_S)^2` and `(1-x_S)^2`, of degree at most six. Consequently,

```
LB_r(B) <= L[F] <= Delta |R|/m.
```

If the box is pruned at target `T`, it must have `|R|>=mT/Delta`. A box
containing any Boolean witness contains at most `2^(n-|R|)` Boolean
vertices, since every restricted coordinate permits at most one Boolean
value. Therefore every pruned box contains at most a `2^(-mT/Delta)`
fraction of all witnesses. A cover must have at least `2^(mT/Delta)` boxes.
QED.

The proof uses only the final cover and allows arbitrary real split points,
variable choices, and node orders. It does not use integer branching.

## Exact quadratic realization from signed character moments

**Lemma.** Let `E` be any Boolean pseudoexpectation through degree two with
all first and second moments in `{0,-1,1}`. Then its degree-two moment vector
is realized by an actual Boolean probability distribution.

*Proof.* Its augmented moment matrix, indexed by `1,x_1,...,x_n`, is PSD,
has diagonal entries one, and all entries in `{0,-1,1}`. Represent it as a
Gram matrix of unit vectors. Inner product `+1` or `-1` means two vectors
are equal or opposite. Partition the vectors into these signed equivalence
classes. Vectors from different classes are orthogonal, because their inner
product cannot have absolute value one and can therefore only be zero.
Associate an independent unbiased Rademacher variable with each class except
the class containing the constant vector; fix that class variable to one.
Give each coordinate its corresponding class variable times the sign of its
Gram vector. This actual Boolean distribution has exactly the prescribed
first and second moments. QED.

Thus pairwise independence is a sufficient but unnecessary hypothesis.
Schoenebeck's XOR construction uses signed equivalence-class basis vectors,
so its character moments are zero or signs and this lemma applies directly.

## Existence from a classical random-3XOR construction

The external input is Schoenebeck's random-CSP theorem and explicit signed
character construction: [Linear Level Lasserre Lower Bounds for Certain
k-CSPs, full version](https://schoeneb.people.si.umich.edu/papers/LasserreNew.pdf),
Theorem 12 and Lemma 13. Take `delta=1/4`, `gamma=1/4`, and `epsilon=0`
in the source: density 8 exceeds `1+8 log(2)`. Choosing `gamma=1/4` avoids
the zero denominator in the displayed bound at the boundary `gamma=1/2`
for `k=3`. For sufficiently large fixed clause density, random
3XOR has a constant unsatisfied fraction but admits linear-degree Boolean
pseudoexpectations satisfying every clause. In the proof of Lemma 13,
characters are mapped to signed coordinate vectors for equivalence classes;
hence each character expectation is in `{0,-1,1}`. This is a classical
construction, not a new SOS lower bound. The degree convention here is explicit: the source's width-`w` signed
character construction supplies moments through degree `w` and positivity
for squares of polynomials of degree at most `floor(w/2)`. Equivalently,
Lasserre level `ell` supplies degree-`2ell` moments. We require `4r<=w`;
the lifted extension requires `4rD<=w`.

For explicit elementary occurrence control, sample `m0=8n` random 3XOR
clauses, each on three distinct uniformly selected variables with an
independent uniform sign. With probability tending to one:

- every assignment violates at least `m0/4=2n` clauses;
- the Schoenebeck pseudoexpectation has degree at least `a n` for some
  constant `a>0`, and satisfies every clause.

The first assertion also follows directly from Hoeffding and a union bound:
for a fixed assignment, violations are `Binomial(8n,1/2)`, and the probability
of at most `2n` violations is at most `exp(-n)`. Multiplication by `2^n`
still tends to zero.

Delete every clause incident to a variable whose original degree is greater
than 64. If `D_i` is the original occurrence count, then
`D_i~Binomial(8n,3/n)`. The number of deleted clauses is at most
`sum_i D_i 1_(D_i>64)`. Using `1_(D_i>64)<=2^(D_i-64)`,

```
E[D_i 1_(D_i>64)] <= 2^(-64) E[D_i 2^D_i]
= 2^(-64) 48 (1+3/n)^(8n-1)
<= 48 exp(24)/2^64 < 1/8.
```

Markov's inequality therefore gives probability less than `1/8` that more
than `n` clauses are deleted. For sufficiently large `n`, this event's
complement intersects the two preceding high-probability events. Fix an
instance in their intersection.

The resulting formula has `7n<=m<=8n` clauses, maximum occurrence at most
64, and every assignment still violates at least `n` clauses. The same
pseudoexpectation satisfies all retained clauses; deleting constraints does
not change its positivity or its signed character moments. Thus normalized
`OPT>=n/m>=1/8`, while `E[F]=0`. Choose `r<=a n/4` with `r>=2`.
The transfer bound at `T=1/16` gives

```
number of leaves >= 2^(m/(16*64)) >= 2^(7n/1024).
```

For absolute tolerance `1/16`, actual pruning requires at least
`OPT-1/16>=1/16`. For relative tolerance `1/2`, it requires at least
`OPT/2>=1/16`. This proves the existence claim. Both independent reviews checked the
source construction and its translation to the stated pseudoexpectation
conventions.

## What improves, what remains limited

The old fractional-cardinality quadratic family is closed by a known clique
cut. Here the entire quadratic moment hull is granted at every node and the
lower bound survives. The mechanism is inconsistent three-variable parity
information whose first two moments are completely realizable.

No claim is made that arbitrary valid cubic inequalities, arbitrary lifted
reformulations, or all SOS localizers of all global quadratic cuts are
covered. Nor is this a new hardness result for Max-3XOR or a new SOS gap.
The potential contribution is the transfer to arbitrary continuous spatial
boxes and a leaf-cover obstruction despite complete quadratic information.
The continuous objective is a bounded sparse cubic interaction model; its
PSE relevance is broad polynomial nonlinear optimization, rather than a
specific process unit model.

## Novelty scope

The earlier literature note covers Jarre's binary SDP lower bound and
Coniglio's midpoint spatial lower bound. The new transfer should be compared
with branch-and-bound/SOS proof-complexity results for random CSPs and with
known reductions from polynomial optimization to CSPs before any priority
claim. Even if the transfer is already known, the exact-quadratic-hull
formulation and explicit obstacle to clique-cut strengthening are useful
research records.


## Targeted literature comparison, 2026-09-05

Ahmadi, Dash, Hua, and Stellato,
[Disjunctive Sum of Squares](https://arxiv.org/html/2605.28674v1)
(May 2026), prove that subdivision can keep the SOS degree fixed while
improving polynomial nonnegativity certificates. Their Section 6 develops
spatial branch-and-bound on simplicial regions and proves termination for
positive tolerance. The abstract, main contribution statements, definitions,
Section 6, and concluding questions were inspected. They do not state the
present exponential box-cover obstruction in those sections. Their results
are complementary: convergence does not bound the number of regions by a
polynomial. Our theorem does not cover arbitrary simplicial or algebraic
disjunctions, so it is not a lower bound on their specific algorithms.

Targeted searches combining spatial branch-and-bound, pseudoexpectation,
3XOR, Schoenebeck, and Lasserre did not find a direct match for the present
transfer with an exact quadratic moment hull. This is limited search
evidence, not proof of priority. Classical SOS gaps and branch-and-bound
lower bounds must remain prominent antecedents; see the
[shared novelty note](../notes/spatial-bb-strengthening-novelty.md).

## Extension: exact coordinate domains

The same transfer works for products `B=prod_i S_i`, where each nonempty
`S_i subset [-1,1]` may be disconnected. Replace the node box preordering by
all products of univariate polynomials nonnegative on their corresponding
coordinate domains, multiplied by squares, through total degree `2r`.
Keep the exact degree-two moment hull of `B`. For a witness in `B`, restrict
every coordinate whose set excludes an endpoint and keep the others.
Each unrestricted univariate generator, reduced modulo `x_i^2=1`, is a
nonnegative linear combination of `(1+x_i)/2` and `(1-x_i)/2`, because both
endpoints belong to its domain. Expand products of these combinations.
Every summand is a nonnegative scalar times an indicator times a square,
and the same degree-`4r` argument proves positivity. The actual quadratic
realization is still supported in `B`, and the witness count is unchanged.

This extension covers coordinate exclusions obtained by arbitrary
univariate transformations. It does not cover domains coupling coordinates,
branching on clause products, or localizers of arbitrary coupled quadratic
cuts. Both independent audits also checked this extension.


## Simple conditioning bounds for the objective

The objective does not require large polynomial coefficients or growing
coordinate curvature. For every point of the cube,

```
|partial_i F(x)| <= Delta/(2m),
sum_{j != i} |partial_i partial_j F(x)| <= Delta/m,
||Hessian F(x)||_2 <= Delta/m.
```

The second inequality counts two mixed derivatives per clause incident to
`i`; the diagonal Hessian entries vanish. The spectral bound follows from
symmetry and the maximum absolute row sum. In the selected family this is
at most `64/(7n)`. These bounds describe the scaling of this example; they
do not assert a general relation between curvature and certificate size.

## Finite certificates at fixed order

For completeness, fixed order `r=2` admits certificates with exponentially
many boxes. Given `epsilon>0`, divide each coordinate into
`M=ceil(3/epsilon)` equal intervals. Each resulting box has width at most
`2epsilon/3`. Fix a corner `a` of a box. A single clause term has derivative
magnitude at most `1/2` in each of its three coordinates, so its minimum on
the box is at least its value at `a` minus `epsilon`. Averaging clause minima
therefore gives a lower bound of at least `F(a)-epsilon>=OPT-epsilon`.

Each clause term is multiaffine on its three variables. Its value minus its
minimum on their box has a Bernstein representation whose coefficients are
nonnegative corner-value differences and whose basis terms are products of
three normalized coordinate-bound slacks. This is a degree-three box
preordering certificate. Thus the order-two node oracle proves the stated
bound on every box. The certificate uses `M^n` regions. In particular,
absolute gap `1/16`, and hence relative gap `1/2` for this family, has a
certificate with at most `48^n` regions. This establishes exponential upper
and lower region counts at fixed tolerance, up to their constants in the
exponent.
