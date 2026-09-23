# Source and novelty audit: local Hessian rank for smooth graph precision

Date: 2026-09-05. Independent source audit for the candidate in
`results/smooth-map-local-rank-integer-complexity.md`, developed by
`binary_formulation_review`. Mathematical reviewers are auditing the
complete argument separately.

## Assessment

The required oscillatory-integral estimate is an established theorem
with exactly the needed hypotheses. An original, directly applicable
statement was located: Hörmander (1973), Theorem 1.1, printed page 2.
Wolff's editor-hosted notes independently confirm the same statement and
its localization argument.

No prior use was found that combines a noncommutative-rank matrix
blow-up of pointwise Hessians with the midpoint defect of a smooth map
to prove its minimum mixed-integer convex graph-approximation dimension.
The proposed connection therefore remains a credible novelty candidate,
conditional on the separate mathematical reviews. The harmonic-analysis
estimate, matrix blow-up characterization, and integer-parity mechanism
must all remain attributed as known results.

The main candidate statement is a local lower bound: noncommutative
Hessian rank `r` at an interior point forces at least
`(r/2)log2(1/epsilon)-O(1)` integer coordinates in every convex lift.
Full rank at one point, combined with a standard smooth grid upper
bound, gives the sharp leading coefficient `n/2`. In rank-deficient
cases this does not claim a matching global upper bound from the
pointwise rank alone.

## Exact original theorem

Lars Hörmander, *Oscillatory integrals and multipliers on FL^p*,
Arkiv för Matematik **11** (1973), 1–11, Theorem 1.1, printed page 2,
[institutional archive of the original article](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7179-11512_2006_Article_BF02388505.pdf).
DOI: 10.1007/BF02388505. The archive metadata sometimes displays 1972,
which is the receipt year; the established citation is 1973.

In current notation, let `a in C_c^infinity(R^(2N))`, let the phase
`phi in C^infinity(R^(2N))` be real-valued, and define

```
T_lambda u(x) = integral exp(i lambda phi(x,y)) a(x,y) u(y) dy.
```

If `det(phi_xy) != 0` throughout `supp(a)`, then, for `lambda>=1`,

```
||T_lambda u||_(p') <= C lambda^(-N/p') ||u||_p,
1<=p<=2, 1/p+1/p'=1.
```

Set `p=2` to obtain the desired `C lambda^(-N/2)` operator norm.
The proof localizes the support, estimates the kernel of `T* T` by
integration by parts, and applies the Schur bound. No sign-definiteness
condition on the mixed Hessian is imposed.

The full original text was readable through the web tool. Direct
download and screenshot attempts returned HTTP 500 during this audit;
this access limitation does not affect the separately downloaded
Wolff verification below.

## Independently accessible verification

Thomas Wolff, *Lectures in Harmonic Analysis*, notes revised March 2002,
Section 9A, Theorem A, printed pages 50–51,
[editor-hosted PDF](https://personal.math.ubc.ca/~ilaba/wolff/notes_march2002.pdf).
The PDF was downloaded and its relevant pages read locally.

Wolff states the smooth real phase, compact smooth amplitude, and
nonvanishing mixed-Hessian determinant hypotheses explicitly. His
normalization is `exp(-pi i lambda phi)`, which only changes constants.
He proves the estimate for small support using nonstationary phase in
`T T*`, then removes the support-size restriction with a partition of
unity. He also notes the version with mixed-Hessian rank at least `k`
and exponent `k/2`.

The text explains why applying scalar stationary phase directly is
insufficient: the input function need not be smooth. The operator norm
is the appropriate tool for characteristic functions of contact sets.
Its bounded extension to `L2` follows from density. These statements
justify using an arbitrary compact measurable contact set without
regularity of its boundary.

## Applicability to the candidate phase

This section records the source-to-model calculation, not a claim that
the oscillatory theorem is new. Write

```
D_j(x,y)=f_j(x)+f_j(y)-2 f_j((x+y)/2).
```

For smooth `f_j`,

```
partial_x partial_y D_j(x,y) = -(1/2) Hess f_j((x+y)/2).
```

For real `d by d` matrices `B_j`, use the scalar phase on two copies
of `R^(nd)`

```
Phi(X,Y)=sum_(a,b,j) (B_j)_(a,b) D_j(x_a,y_b).
```

At the diagonal point with every input equal to `x0`, its mixed Hessian
is `-(1/2) sum_j B_j tensor Hess f_j(x0)`. An invertible matrix blow-up
therefore supplies exactly the nondegeneracy required by Hörmander.
Continuity gives a fixed open product neighborhood on which the
determinant remains nonzero. A smaller closed input box permits a
smooth compact cutoff equal to one on the relevant product box. One
can extend the phase smoothly outside this neighborhood without
altering it near the cutoff support.

The cutoff and neighborhood must be fixed independently of epsilon.
Otherwise the operator-norm constant could conceal unwanted powers of
epsilon. The author proposes `C^infinity` on an open neighborhood of the
original box, which safely meets the checked theorem. A theorem for
merely `C2` functions requires a separate argument and is not justified
by this citation alone.

If a contact set `S` obeys `|D_j(x,y)|<=2epsilon` for every pair and
output, then `|Phi|<=2epsilon sum_(a,b,j)|(B_j)_(a,b)|` on
`S^d times S^d`. Choose `lambda` as a sufficiently small fixed multiple
of `1/epsilon`. The real part of the oscillatory integrand is bounded
below by a positive constant on this product. Pairing the operator
with the characteristic function of `S^d` gives

```
c |S|^(2d) <= |<1_(S^d), T_lambda 1_(S^d)>|
            <= C lambda^(-nd/2) |S|^d.
```

Thus `|S|<=C' epsilon^(n/2)`. The dimension introduced by the matrix
blow-up cancels when taking the `d`th root. This is the useful proposed
connection to graph-contact volume. It does not require `S` to be
convex, which matters for integer parity classes. Closures in the
compact box make those classes measurable and preserve the pairwise
defect inequality by continuity.

## Attribution and overlap

The matrix blow-up certificate for full noncommutative rank is existing
algebra; see Garg, Gurvits, Oliveira, and Wigderson,
*Operator Scaling: Theory and Applications*, Theorem 1.4(3),
[published PDF](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf).
For real Hessians an invertible complex witness implies a real witness,
because the corresponding nonzero determinant polynomial has real
coefficients. The quadratic audit
`notes/quadratic-noncommutative-rank-novelty.md` records the broader
rank, capacity, and shrunk-subspace attribution.

The parity step comes from Lubin, Vielma, and Zadik,
*Mixed-integer convex representability*, Lemma 4.1,
[open manuscript](https://arxiv.org/abs/1706.05135).
Its exact-representability obstruction already permits unrestricted
integer ranges. The proposed new conclusion is the quantitative smooth
graph precision bound obtained after the contact-volume estimate.

Classical scalar quadratic and smooth piecewise affine approximation
already relates curvature to mesh size. Pottmann and collaborators,
*On Piecewise Linear Approximation of Quadratic Functions*,
[publisher PDF](https://www.heldermann-verlag.de/jgg/jgg01_05/jgg0403.pdf),
and the anisotropic mesh references in the earlier novelty note are
relevant background. They should not be described as if curvature-based
approximation first appears here. Their inspected statements do not
give the noncommutative-rank lower bound for arbitrary convex lifts of
the full graph.

The generic `n/2` smooth grid upper bound is an established Taylor-error
and disjunction argument. It may require a number of inequalities
polynomial in `1/epsilon`, even though the number of selector binaries
is logarithmic. Keep that distinction explicit. The author's stronger
compact construction for fixed-degree polynomials is a separate claim
requiring its own proof and formulation-literature comparison.

## Search limits

Targeted searches combined oscillatory integral, Hörmander, mixed
Hessian, noncommutative rank, matrix blow-up, shrunk subspace, midpoint,
convex cover, smooth graph, piecewise affine approximation, and
mixed-integer convex. No direct prior instance of the combined argument
was found. Many apparent hits concern unrelated meanings of convex
covering or noncommutative harmonic analysis.

The exact harmonic-analysis source is secure. The novelty assessment is
limited negative evidence, especially regarding older approximation
geometry and unpublished arguments. No claim of publication priority
is made. Scratch source files are under `/tmp/minlp-smooth-novelty/`.
