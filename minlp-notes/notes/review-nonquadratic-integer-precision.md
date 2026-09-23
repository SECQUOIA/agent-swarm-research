# Independent audit: smooth-map integer precision

Date: 2026-09-05.
Reviewer: independent agent `graph_precision_second_review`.
Sources: `results/smooth-map-local-rank-integer-complexity.md` and
`notes/nonquadratic-integer-precision-investigation.md`.

## Verdict

The local noncommutative-rank lower bound, global Hessian-span upper
bound, equality when the ranks coincide, and fixed-degree polynomial
compact upper construction pass independent mathematical review.
No substantive gap was found. The phase normalization, fixed cutoff,
Cartesian-power exponent, original-domain Taylor centers, and polynomial
prefix encoding are all consistent in the completed draft.

This review does not establish novelty or publication priority. It
covers the stated `C^infinity` assumption. It does not silently weaken
that assumption to `C^2` for the oscillatory estimate. The smooth upper
controls binary count but can have polynomially many rows in `1/epsilon`;
only the fixed-degree polynomial theorem claims polynomial size in the
precision depth.

## Analytic source and localization

I read Hörmander's original 1973 Theorem 1.1 in the linked open paper.
It assumes a real smooth phase, compactly supported smooth amplitude,
and nonzero mixed-Hessian determinant on the amplitude support. At
`p=2`, its estimate is the required `lambda^(-N/2)` operator norm.
The proof uses integration by parts and a Schur estimate. The draft's
localization satisfies these assumptions. [Primary source](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7179-11512_2006_Article_BF02388505.pdf).

I independently checked the local proof mechanism. Restrict to a convex
product neighborhood where the mixed Hessian stays sufficiently close
to its invertible value at the base point. For
`psi(Y)=Phi(X,Y)-Phi(Z,Y)`, integrating the mixed derivative along the
`X-Z` segment gives `|grad_Y psi|>=c|X-Z|`; its higher `Y` derivatives
are bounded by constants times `|X-Z|`. Repeated integration by parts
in the `TT*` kernel gives
`|K_lambda(X,Z)|<=C_M(1+lambda|X-Z|)^(-M)`. With `M>N`, both Schur
integrals are `O(lambda^(-N))`. Taking the square root proves the
operator estimate used here. A small fixed neighborhood makes all
constants independent of the later contact set and epsilon.

The amplitude can equal one on the full compact product of the smaller
box while remaining supported inside a slightly larger nondegenerate
neighborhood. All midpoint evaluations remain in the smooth domain.
If desired, a smooth extension outside that neighborhood allows a
globally written integral; only the compact amplitude support matters.
No derivatives of the contact-set indicator are needed because the
operator estimate extends from smooth functions to `L^2`.

## Real matrix evaluation and exact phase factors

Full noncommutative rank of the pointwise real symmetric Hessian tuple
supplies an invertible finite matrix evaluation over the complex
numbers. For that fixed matrix size, its determinant is a polynomial
with real coefficients in the evaluating matrix entries. A nonzero real
polynomial cannot vanish at every real tuple, so a real witness exists.
It is fixed throughout the approximation argument. Its matrices need
not be symmetric: the analytic mixed Hessian is not required to be a
symmetric matrix.

The completed draft consistently uses the *full* midpoint difference

```
D_j(x,y)=f_j(x)+f_j(y)-2f_j((x+y)/2).
```

Its mixed derivative is `-(1/2) Hess f_j((x+y)/2)`. At an admitted
midpoint of two exact graph points, the graph error is `D_j/2`, so
`|D_j|<=2 epsilon`. Both factors are correct.

For the phase on Cartesian powers, the `(a,b)` block of the mixed
Hessian is
`-(1/2) sum_j (B_j)_ab Hess f_j((x_a+y_b)/2)`. At the repeated base
point it is exactly the stated invertible matrix evaluation times
`-1/2`. Continuity gives a single small input box whose entire
Cartesian product remains in the nondegenerate region. The block order
matches the Kronecker product convention in the draft.

## Contact-volume inequality

For `S` of volume `v`, the indicator of `S^d` has squared `L^2` norm
`v^d`; the product `S^d times S^d` has measure `v^(2d)`. With
`K=sum_(a,b,j)|(B_j)_ab|>0`, the contact inequalities give
`|Phi|<=2K epsilon` on this product. Choosing
`lambda=1/(4K epsilon)` ensures `|lambda Phi|<=1/2`, so its exponential
has real part greater than `1/2`. Restricting to sufficiently small
epsilon also ensures `lambda>=1`, as the analytic theorem requires.

The cutoff is exactly one throughout this product. Thus the real-part
lower bound and the `L^2` upper bound give

```
(1/2) v^(2d) <= C(4K epsilon)^(nd/2) v^d.
```

For positive volume, division by `v^d` and the `d`th root produce
`v<=C' epsilon^(n/2)`. The matrix-evaluation size disappears from the
exponent, although it remains in the fixed constants and differentiability
requirements of the invoked analytic estimate. Zero volume needs no
division. Compact contact sets can be disconnected, highly anisotropic,
or have irregular boundary; the indicator argument covers them all.

This step does not replace the original nonlinear function by a
quadratic approximation. That distinction avoids an uncontrolled
Hessian-remainder error on elongated contact sets.

## Arbitrary integer lifts and partial rank

Within the fixed small box, graph inputs admitting integer lifts of a
specified parity form at most `2^p` covering sets. Any two such lifted
points have an integer midpoint in the original convex lifting set.
Their visible midpoint lies in the input box. This proves the contact
inequalities without bounded integer ranges, projection closedness, or
any regularity of the support sets.

Taking closures within the compact small box preserves every midpoint
inequality by continuity. The compact closures still cover it and are
measurable. The contact-volume lemma therefore gives the stated binary/
integer dimension lower bound by volume subadditivity.

At a point of rank `r`, the previously reviewed Hermitian principal
compression lemma selects `r` original coordinate indices with a
full-rank compressed pencil. Fixing the other coordinates at the
interior base point gives an actual `r`-dimensional input box and smooth
restricted functions. The preceding proof applies in that dimension.
The maximum defining `r_loc` is attained in the stated sense: the
nonempty set of actually occurring ranks is a subset of the finite set
`{0,...,n}`, so its largest element occurs at an interior point. No
compactness claim about the open interior is needed for that observation.

## Global Hessian structure and Taylor cells

The span of all Hessians is finite-dimensional even though it is
indexed by continuously many points. Choose a finite real basis and
apply the reviewed real shrinking and symmetric zero-block lemmas to
that matrix space. Its one fixed orthogonal coordinate decomposition
therefore works at every input in the original box. The resulting
precision exponents sum to `r_all/2`, and every possibly nonzero Hessian
entry has endpoint exponent sum at least one.

After the coordinate change, the original domain is a compact convex
parallelepiped. Intersecting the enclosing-box grid with that domain is
necessary: the smooth Hessian zero pattern has only been proved on the
original domain. Each nonempty intersection is a compact convex
polytope, and choosing its Taylor center inside it keeps every remainder
segment inside the domain. The draft explicitly does this, so it does
not use derivative bounds or zero blocks at unauthorized outside points.

For displacement `Delta` inside a cell,
`|Delta_i Delta_k|<=b_i b_k 2^(-T)` at every potentially nonzero entry.
The integral Taylor remainder is bounded by one constant times
`2^(-T)`, uniformly over cells and outputs. Entries that vanish
identically on the original domain contribute nothing even if a
corresponding coordinate cell has full fixed width.

With remainder at most `epsilon/2`, the affine band of radius
`epsilon/2` contains the exact graph and stays within epsilon of it.
The output bands and compact cells are bounded polyhedra. Their number
is at most the product of all coordinate grid counts. The stated
binary-code convex-hull disjunction is exact at integral codes:
a convex combination of zero-one codes can equal a zero-one vector
only if every code with positive weight equals that vector. Distinct
member codes therefore isolate a single member polyhedron. Boundedness
avoids any extraneous recession contribution from inactive members.

This proves the upper coefficient without any hidden compact-size
claim for arbitrary smooth maps. Vanishing Hessians make the functions
affine on the connected convex box, so the zero-rank case is exact.

## Fixed-degree polynomial compactness

For polynomial outputs, each forbidden Hessian entry is a polynomial
that vanishes on the full-dimensional interior of the original domain.
It consequently vanishes identically. This legitimizes Taylor estimates
on the larger normalized box, including at binary-prefix points that
may be outside the transformed original domain.

For `y=A+rho`, the polynomial expression

```
f_j(A)+sum_i partial_i f_j(A) rho_i
```

is exactly the first-order Taylor polynomial at the prefix point `A`.
The segment to `y` lies in the normalized box. The same weighted
remainder bound makes its error at most `epsilon/2`, and an output band
of that radius gives the desired graph relaxation.

Expansion in input bits gives products of at most `D` bits, or at most
`D-1` bits multiplied by a single residual. Repeated bits can be deleted
because the existing bits are integral. The displayed AND inequalities
force the continuous variable for a nonempty bit subset to its exact
zero-one product. Consequently a subsequent bounded-product four-row
formulation is exact at integral input bits even though this AND
variable is not itself declared integer. Empty subsets give a constant
or a residual directly. No new binary coordinate is needed.

There are polynomially many such terms in total input depth, with
exponent at most the fixed degree `D`; each needs only a bounded number
of constraints for fixed `D`. The coefficient-weighted sums can have
arbitrary signs because they are exact expressions. Accuracy is lost
only in the rigorously bounded Taylor remainder, not in these prefix
products. This verifies the stated polynomial-in-depth formulation size
and the unchanged `r_all/2` binary coefficient.

## Independent quartic check and the cone limitation

I checked a concrete anisotropic nonquadratic example symbolically:

```
f(z_1,z_2,w,r)=z_1 w^3+z_2(w+w^2)+w r^2+r^4.
```

With `Z=(z_1,z_2)`, `W=w`, and `R=r`, its `ZZ` and `ZR` Hessian blocks
vanish. Its generic scalar Hessian rank is three, while the common
zero-block structure bounds the global noncommutative rank by three;
hence both ranks are three on a box containing a generic point.
For exponents `(0,0,1,1/2)`, exact expansion of the first-order Taylor
remainder gives 12 residual monomials, each with total precision
exponent at least one. All symbolic checks passed. This illustrates
coefficient `3/2` in four input dimensions and the compact quartic upper
construction; it is not needed to prove the general theorem.

The investigation note's cone example is also correct. On `[1,2]^2`,
`sqrt(x^2+y^2)` has pointwise Hessian rank one, while three distinct
coordinate ratios give three independent symmetric Hessians. Angular
sectors have polyhedral intersections with this box and supporting
linear forms with uniform error quadratic in angular width. Thus the
actual coefficient is one half, as established by a scalar curved
slice below and the sector cover above. This refutes interpreting the
global-span rank as an exact invariant for every smooth map. The draft
correctly retains only a sandwich when its two ranks differ.

## Subsequent audit: arithmetic-circuit identity-testing reduction

The later representation-dependent reduction in the investigation note
also passes independent review. For a circuit polynomial `g(z)`, the
system `(xyg(z),z_1^2,...,z_d^2)` has coefficient `d/2` if `g` vanishes
identically, by the quadratic result applied to the `d` active square
coordinates. If `g` does not vanish identically, it is nonzero at some
point in the interior of `[-1,1]^d`: otherwise polynomial uniqueness
on an open set would force it to vanish everywhere.

At `(x,y,z)=(0,0,z_0)`, all mixed derivatives between `z` and either
`x,y` in the first output vanish, as do its `zz` derivatives. The
stated scalar sum of outputs therefore has precisely the displayed
block-diagonal Hessian, with invertible two-by-two block of determinant
`-g(z_0)^2` and invertible square-coordinate block. The smooth theorem
gives the other exact coefficient `(d+2)/2`.

The coefficient gap is exactly one. An additive approximation with
error strictly smaller than one half distinguishes the cases by the
threshold `(d+1)/2`. The added circuit size is polynomial in the original
circuit and the explicitly listed variables. The reduction already
holds with rational circuit constants, the usual finite-encoding
setting; allowing real constants requires specifying their computation
model before interpreting a running-time statement. No bound on the
expanded degree or coefficient-list length is assumed, and the
fixed-degree compact formulation theorem does not imply a uniform
polynomial-time algorithm on these succinct circuit inputs. The note
correctly states a reduction rather than an unconditional complexity
lower bound, and correctly separates explicit coefficient-list input.
