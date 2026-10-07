# Independent quadratic mathematical review, frozen round 1

Reviewer: Sol. Date: 2026-10-06. This is a fresh proof review of the immutable
snapshot `evidence/snapshots/integrated-mathematical-draft-r1`, not an approval
of mutable author files or of the whole paper. The assigned scope is all of
Section 04 and Appendix B, their model/counting dependencies, and their rows
in the introduction's results table. I also checked the actual transferred
ambient-barrier proof and the narrow integer-lattice scope needed to assess
the table's separable rows.

## Verdict and remaining corrections

The assigned main theorem chains are mathematically sound in this snapshot,
subject to the stated exact-solver primitives and completion of the independent
source audit. I found no fatal or major mathematical defect. The earlier
major concerns have actual repairs in the frozen proofs, rather than only
responses in author reports. Two corrections remain:

1. **Moderate summary/parameter-scope correction:** the introduction's table
   calls a supplied factor's parameter its rank, although the aligned and
   native-integer bounds are proved in its number of supplied rows. This can
   change the noise law and the bound when rows are dependent. Use the number
   of supplied factor rows, with rank at most that number, in these rows.
2. **Minor omitted proof branch:** the sharp-fiber proof invokes the joint
   density of the sample minimum and maximum for a statement that also allows
   `n=1`. Add the direct one-dimensional calculation. The proposition itself
   is true.

After these corrections and the source audit, the assigned mathematics is
ready for the next integrated review. This verdict does not certify the
unassigned sparse, constraint, recourse, or general integer theorems, nor does
it certify novelty or bibliography identities. I did not infer correctness
from compilation, the author reports, or the original experiments.

## Frozen provenance and scope

The manifest capture is `2026-10-06T03:49:31.635993+00:00`; its status says
“Frozen complete mathematical revision; bibliography pending Luna final
audit.” All locators below refer to this snapshot. For compactness, `04:195`
means line 195 of `sections/04-quadratic.tex`, and `B:191` means line 191 of
`appendices/B-quadratic.tex`. The other prefixes are their numbered sections
or lettered appendices in the same snapshot.

I independently checked the manifest SHA-256 values and line counts for the
following ten assigned or dependency files. All matched. This was a targeted
ten-file check, not a claim that I checked every one of the twenty manifest
entries.

| File | Lines | SHA-256 |
|---|---:|---|
| `sections/01-introduction.tex` | 524 | `c3b27472e13d0c6a94d1cb6693d264d6ac0f6137c7e64d039bc613eb3d35ba56` |
| `sections/02-model.tex` | 559 | `0a9267cd7a893497d212e5ccb0fbb6433b6428c4784793dd9fc79ec4f4e38a63` |
| `sections/03-counting.tex` | 754 | `9818728f37864c878ab2e7d0bb1690bb79e8d53f3a338e2f316e31787692b049` |
| `sections/04-quadratic.tex` | 909 | `020d70a1f2d3380776aa908dc25a5d9351c126674c0571a74e73a7dab867edd5` |
| `appendices/A-finite-noise.tex` | 822 | `4ff3fe30e76466dcc744389e88deaa9759fc19a2709c1104cba89612379c39cd` |
| `appendices/B-quadratic.tex` | 888 | `c15f3a6f76d6a65ab4b6a4f2e861597d0b1c21f35baa41b1b4f670ad63308d31` |
| `appendices/G-boundaries.tex` | 481 | `163333352717c3b090f62924f8a8b90eea63cf7c4fc50bf1da0dafd4556f1553` |
| `sections/08-integer.tex` | 775 | `27809e4472aa7e53c36e8a211bf91d348f5e25c651d74f75936e9d5df7e3f573` |
| `appendices/F-integer.tex` | 1127 | `c561d9401b3cc15e9072ab7bffe843f6205a894886fba219a8ee02150a472ef0` |
| `sections/09-boundaries.tex` | 824 | `1acb7217806f6e53e27a653e9ca36df3adfa3d37cc25a428b45c4770cb8e7bf8` |

I read the original brief, independent-review brief, integration contract and
decisions, root's integration-to-final-math and scope reports, the prior Sol
reports named in the task, the editorial interim/disposition, the partial
Opus mathematical review, and the quadratic author responses. These establish
requirements and prior concerns. The mathematical conclusions below come
from the frozen statements and proofs.

## New findings requiring correction

### Q1. Supplied row count is not intrinsic factor rank

Severity: moderate in the summary; the cited main theorem statements are
correct.

At `01:133–134`, `tab:intro:results` says that `k` is “negative inertia,
factor rank, or core size.” At `01:159–164`, its separable rows describe a
“rank-k” concave term. In contrast, `thm:qp:aligned` at `04:615–626` permits
an arbitrary supplied factor with `k` rows. The aligned part of `thm:qp:sep`
inherits that contract. The native-integer `thm:int:lowrank` explicitly
permits zero and dependent factor rows (`08:652–717`). The proven bounds
and laws depend on the supplied row count.

For a concrete distinction, take one variable and

\[
 T=\begin{pmatrix}1\\1\end{pmatrix},\qquad
 \operatorname{rank}T=1,\qquad k=2.
\]

Under the stated aligned law the perturbed linear term is
`(xi_1+xi_2)x`, where the two `xi_i` are independent uniforms on the prescribed
finite grid. Removing one row and then applying a one-coordinate uniform law
changes this distribution. Replacing the two rows by a single rational row
also requires adjusting the concave coefficient or the represented square;
it does not justify substituting intrinsic rank into the existing count.
The theorem's product over two supplied coordinates is therefore not proved
with an exponent one for that original sampled objective.

Repair: in the table caption use “number of supplied factor rows” for these
regimes. In the affected structure cells say that the concave term is
represented by `k` supplied rows, or has rank at most `k` with the bound
parameter equal to the supplied row count. The intrinsic quadratic
normalization and the full-row-rank Gaussian regimes may still identify this
count with rank. No theorem proof needs to change. The warning at
`04:874–877` already makes the separable Gaussian limitation precise.

### Q2. Sharp-fiber proof omits n=1

Severity: minor proof-completeness correction; no false inequality.

`prop:qp:fiber-sharp` at `04:674–683` allows `n=m^2=1`. Its proof at
`B:768–770` uses the joint density

\[
 n(n-1)(B'-A')^{n-2}
\]

of the minimum and maximum of `n` independent uniform variables. This
density formula applies for `n>=2`; for `n=1`, the minimum and maximum coincide
and have a singular joint law. Substitution into that integral is invalid.

Repair: precede the density argument with the scalar branch. When `n=m=1`,
the residual is zero, `xi=gamma_1`, and its conditional support is
`[-sigma,sigma]`. Thus an interval centered at zero of length
`0<=ell<=2sigma` has probability

\[
 \frac{\ell}{2\sigma}
 =1-\left(1-\frac{\ell}{2\sigma}\right)^1,
 \qquad \operatorname{Var}\xi=\sigma^2/3.
\]

The remaining proof and disjoint-block product then apply. Restricting the
proposition to `m>=2` would also suffice but would unnecessarily narrow a
true statement.

## Correctness, rational factors, and exact termination

### Intrinsic normalization and supplied curvature

`lem:qp:normalize` (`04:101–115`, proof `B:11–89`) has a complete rational
construction. The lower nonzero spectral bound follows by clearing the
matrix denominators and bounding a nonzero characteristic coefficient.
Successive rational PSD tests find `nu<=beta<2nu` in polynomial work.
The exact range projector is rational. Rational Jacobi rotations and
dyadic approximation to their parameters reduce off-diagonal energy at a
geometric rate with polynomially many rotations and polynomial bit heights.
The specified tolerance is strong enough relative to the spectral lower
bound. The final range projection retains the PSD margin on the range and
annihilates the kernel exactly. It produces `alpha=2beta<4nu`, `k=n_-(A)`,
and the advertised `63/64` frame bound. The scalar matrix branch is present.

The supplied-factor interface is separate (`04:85–99`). Its rational
`alpha,T,c_fr` and certificates contribute to `I`; the frame constant is
not a hidden real input. The Gaussian supplied-factor bound depends on
these supplied quantities. Only intrinsic normalization changes the
curvature parameter to the negative spectral magnitude of the original
quadratic. The anisotropic separable theorem instead uses
`beta=alpha||T||^2`, the supplied concave curvature. The paper correctly
retains that distinction at `04:874–877` and in the Section 04 summary.

### Square completion and each attaining witness

`lem:qp:aux` (`04:130–173`, proof `B:93–118`) uses the exact identity

\[
 W_\zeta(a)=\min_{x\in X}\left[
 F(x)+\zeta^{\mathsf T}x+\frac\alpha2\|a-Tx\|^2\right].
\]

Every attaining witness supplies a globally valid quadratic upper model
touching the auxiliary function at that query. If its gradient is
`g=alpha(a-Tx)+xi`, minimizing that particular upper model gives

\[
 \|g\|^2\le 2\alpha\,[V(a)-V^*].
\]

The inequality therefore holds for every returned exact witness, including
ties and nonunique inner minimizers. It requires neither differentiability
of the auxiliary value nor a kernel inclusion. The bound is global in
auxiliary space; the bounded search box is used to locate an optimizer, not
to constrain this upper-model descent. This resolves the earlier kernel
concern without adding a regularity hypothesis.

### Face enumeration and rational output

`lem:qp:face` (`04:327–348`, `B:120–149`) gives an all-draw exact fallback.
Choose a minimizing point whose containing face has least dimension. The
tangent Hessian must be positive definite: a zero tangent curvature gives
a constant feasible line after first-order stationarity, and that line
reaches a smaller face. An independent constraint basis then gives a
nonsingular rational KKT system. Enumerating faces and feasible candidates,
and taking the least value, is exact. The argument also covers lower
dimensional polytopes. For a fixed integer label the same argument applies
to the continuous slice; bounded integer labels have polynomial bit length.

Convex mixed solves are followed by continuous-slice polishing. Therefore
the returned rational coordinates and values have polynomial height
independent of the magnitude of the solver's parameter factor `f(n_z)`.
The exact convex QP/MIQP primitives remain external dependencies, discussed
below. The paper does not infer a small complete search trace merely from
small output height (`04:499–507`).

### Growth-conditioned search, including the mixed extension

The actual proof of `thm:qp:conditioned` at `B:191–260` retains the full PSD
inner model when a factor coordinate has singleton range. It removes such
coordinates only from the mesh, then embeds every query with the omitted
coordinates fixed. This avoids deleting a convexifying square.

The denominator bounds for `f*` and, under uniqueness, `Tx*` are computable
before the search and have polynomial bit length. The value reconstruction
occurs only when the certified interval is shorter than the separation of
two bounded-denominator rationals. The optimizer reconstruction is guarded
by that value reconstruction (`B:211–221`). Any accepted witness is feasible
and has the already certified value `f*`. Premature guesses cannot produce
a wrong output.

The growth transfer is

\[
 W_0(a)-f^*\ge g_W\|a-Tx^*\|^2,
 \qquad g_W=\frac{\alpha g}{2g+\alpha},
 \qquad \alpha/g_W<2+4\nu/g.
\]

The retained corner lies in the stated ball; bounding grid points in its
enclosing box proves the actual
`4^k(2 sqrt(k kappa)+2)^k` processed-cell count. This supports the stated
`c_k`, which may depend on `k`. It would not on its own support replacing
`c_k` by an absolute constant to the power `k`; the frozen theorem does not
make that stronger claim. For `k<=2`, the constants are absolute and the
count is genuinely `O(Z^(k/2))`, with a fixed logarithmic power. No additional
power of `Z` is hidden by the cell count.

At the sufficiently accurate reconstructed point `Tx*`, square completion
forces every exact recourse witness to attain original value `f*`. The
level bound follows from polynomial denominator height and
`O(log(1+kappa))` precision, with polynomial query bit lengths.

`cor:qp:conditioned-mixed` (`04:228–237`, `B:262–280`) has an actual proof.
LP ranges over the relaxation enclose `TX`; exact mixed recourse and
continuous-slice polishing replace the continuous oracle. The growth
transfer never used convexity of `X`. Fixed integer labels and their
smallest continuous faces give the same polynomial denominator bounds.
The only extra work factor is `f(n_z)`, with absolute polynomial exponents.
This is a deterministic growth-conditioned extension; it is not an aligned
mixed smoothing theorem.

## Critical pieces, labels, and closure

### All real parameters and degenerate active sets

`lem:qp:pieces` (`04:362–395`, `B:318–376`) proves coverage for every real
auxiliary parameter, not only rational query points. For each feasible
integer label, the compact set of convex continuous minimizers has a
vertex. Its tangent Hessian is positive definite by the same least-face
argument; independent active constraints give a nonsingular KKT basis.
Nonnegative optimal multipliers can be represented by independent active
normals. Thus the listed affine response regions cover every parameter,
including boundary points, redundant constraints, singular Hessians in
the original variables, and continua of optimal points. A zero-dimensional
continuous block is covered as well.

For each active basis, the affine response satisfies
`D_{c,S} X_i=0` identically in the parameter. Multiplying its KKT identity by
`X_i^T` cancels the multiplier derivative term algebraically. This proves
the boundary derivative identity without differentiating the optimal-value
envelope or assuming strict complementarity (`B:362–368`). The coefficient
height bound depends on fixed input coefficients; the value of a query only
enters through its explicitly charged rational height.

### Best competing label, finite sections, and feasibility

`lem:qp:gap` (`04:423–440`, `B:378–405`) compares the winning label with the
best different feasible label. The `2n_z` restrictions really cover every
different integer label: at its first differing coordinate it is either
at most `z_i-1` or at least `z_i+1`. Equality at the certification threshold
is allowed. The width bound uses a single common feasible interval, so
there is no missing factor two. The witness-gradient inequality transfers
auxiliary suboptimality to primal suboptimality with the explicit
`h<=1` cutoff used in the mixed gap test.

`lem:qp:isolation` (`04:446–456`, `B:407–428`) groups integer labels by the
chosen coordinate. Slopes are distinct integers, and the lower envelope
has at most the coordinate width in switches. Arbitrary costs and the
remaining original coefficients are held fixed. Consequently the small-gap
axis sections are uniformly bounded independent of those values. The
probability estimate does not assume independent projected factor noise
and residual noise.

The definition requires nonempty mixed `X`, or a prior feasibility branch,
not merely a nonempty relaxation (`04:41–43`). The main closure algorithm
performs mixed feasibility before constructing nonempty-set ranges or
thresholds (`B:644–647`). Empty label slices are omitted. Thus the earlier
mixed feasibility defect is resolved.

### Cell certification and fallback on the same objective

`lem:qp:closure` (`04:480–497`) tests a response region at every cell vertex,
not just at the currently winning corner. Since the region is polyhedral,
this certifies the entire cell. The mixed test additionally certifies the
best competing-label margin over the cell. The displayed corner-only
counterexample at `04:467–478` correctly explains why that extra test is
needed. A certified quadratic is minimized exactly by enumerating its at
most `3^k` faces. Failure to close by the base-chosen cutoff invokes the
finite exact fallback on the same sampled objective; it does not resample.

`lem:qp:tubes` (`04:513–525`, `B:430–468`) uses the attaining witness's
gradient inequality. A violated region boundary pulls back to a hyperplane
with a normalized normal. A singular value quadratic confines gradients
to a proper affine plane. Zero rows do not create a false violated-boundary
case. For ambient noise the identity `TL=u` gives the requisite lower
bound on the pulled-back normal norm. The resulting fixed finite family
of tubes suffices for all queried cells; the failure proof does not take a
union over an uncontrolled adaptive search tree.

The atom example (`04:536–548`) is valid: an actual finite-law coefficient
can produce a flat auxiliary interval, and a nondyadic transition prevents
its crossing cell from satisfying the piece tests at every depth. The
theorems need their finite-law atom budget and exact fallback. Almost-sure
genericity under a continuous proxy cannot replace those mechanisms.

## Noise, expected counts, and precision selection

### Shared finite-law interfaces

The model explicitly defines rational finite uniforms and the particular
finite Gaussian-like law (`02:85–144`). Projected aligned noise has a
different coordinate system and is not independent noise in the original
variables (`02:118–127`). The accuracy or grid resolution is chosen from
base data before sampling; the sampler draws once, and its own bit work
is charged.

The section-transfer lemma (`03:293–310`, `A:140–165`) works for all fixed
values of the other coordinates and includes isolated points. Telescoping
one coordinate at a time gives the asserted CDF-error or atom contribution.
The bounded Gaussian sampler proof (`A:167–226`) has an actual support
bound, bounded rejection attempts, exact dyadic output, and polynomial
bit work. Its approximated Gaussian weights and rounding errors give the
claimed CDF discrepancy; the zero-output rejection-failure mass is included.
No enumeration of its exponentially fine grid is required.

The general growth-tail proof needed here (`03:358–373`, `A:238–325`)
uses compactness and lower semicontinuity, conjugate/proximal monotonicity,
the differentiability and area-formula argument, and coordinate integration.
It does not assume the original objective is convex. The quadratic axis
sections in `lem:qp:growth-sections` (`B:151–187`) are finite for all real
fixed coefficients: enumerate label/face candidates for both the original
and growth-shifted quadratic, and bound the roots of their quadratic
comparisons. Hence the finite-law growth residual is independent of the
chosen growth threshold.

### Uniform ambient law

`lem:qp:volume` (`04:660–670`, `B:539–554`) is a volume estimate for intervals
whose positions depend on the residual. Complementary minors and the
projection-zonotope volume give the sum of absolute `t`-minors, with the
Jacobian factor handled by the frame and `||T||<=1`. Cauchy–Binet bounds
that sum by `n^(t/2)`. Discarding interval constraints with factors larger
than one gives the capped tensor bound. This does not assert independence
or a uniform conditional density on projected fibers.

The fiber sharpness proposition is true, subject to Q2's scalar proof
branch. The actual ambient-barrier proof is present in `G:1–175`, not an
outline. Its rational quadratic construction, negative eigenvalue bound,
small derivative event, and retained/local node lower counts check out.
The finite uniform order-statistic estimate uses `M>=32` and retains enough
endpoint mass for the constant-probability event. Disjoint blocks yield
the stated product probability. The main box contains the exhibited
dyadic cells. This is a limitation of the counting surrogate; the text
does not turn it into an algorithmic lower bound or hide that ambient
diameter grows in the example.

### Gaussian proxy and finite transfer

For the real Gaussian proxy, factor coefficients and residual are
independent, with factor covariance bounded by the frame constant
(`B:576–610`). Each local event also has a witness-location interval.
Conditioning on the residual, then applying the Gaussian density majorant
to the subset of factors whose probability bound is below one, yields the
product of the capped interval-density bounds. This is compatible with
correlation among factor coordinates; it does not assume their independence.

The weighted lattice sum at `B:615–626` controls the two tails separately
and includes the unrefined endpoints. Its bound is uniform in the mesh
box's position and size. This is why Gaussian counts avoid the uniform
law's dimension power. The subsequent finite-law transfer uses uniformly
bounded axis sections, not Gaussian proxy independence for the actual
finite law. The text explicitly excludes that incorrect shortcut at
`04:738–743`.

The all-real fixed-label coverage proved earlier is used in the mixed
local-event section count (`B:497–537`). Continuous/separable response
intervals, mixed pair comparisons, and the `2k+1` query family are all
charged. Since the section bound is uniform in fixed original coefficients,
it remains valid when conditioning on continuous original-coordinate
perturbations for the label-gap estimate.

### Support/precision loop and all-draw work

The main algorithm proof (`B:639–756`) constructs fallback budgets, section
counts, tube counts, polynomial denominator heights, and their thresholds
from the base instance. Uniform/aligned resolution budgets charge both
atoms and local counts. Gaussian support grows with `b`, so the proof uses
a base-only trial support index rather than treating it as fixed.

At trial index `t`, the search-depth bound satisfies `J(t)<=J_0+t`, because
the relevant constants and the `h<=1` cutoff are support independent.
The required precision has a polynomial base term plus linear/logarithmic
dependence on `t`. Choosing a trial with `2^t>=b(t)+20` therefore halts in
polynomially many bits; the selected support contains the support of the
actual chosen finite Gaussian law. Sampling happens only after this loop.
There is no circular post-sample precision choice.

The unclosed-cell event is covered by one fixed tube family, or by the
mixed competing-label event. Each total failure probability is budgeted
against the corresponding fallback cost. The local-count transfer error
is summed over the full deterministic level grids before invoking adaptive
domination, and has total budget at most a constant. Corner, child, and
face enumeration costs are charged. Exact fallback guarantees termination
on every actual draw, including atoms, ties, continua, and nongeneric
active sets. The main Gaussian, uniform, and aligned theorem bounds follow
with absolute bit-polynomial exponents; Gaussian and aligned numerical
parameters give the claimed FPT statements, while the ambient uniform
bound is correctly described as polynomial only for fixed `k` and controlled
numerical scales.

## The two-negative-direction theorem and its distinct bound

`thm:qp:two` at `04:261–282`, with `B:282–314`, now specifies the least
adequate power-of-two grid and least positive Gaussian accuracy. Thus
`log M` and `b` are `O(r+log(n+1))`. If a larger accuracy is used, its bit
length is explicitly charged and required to be polynomial in `I`.
The earlier arbitrary-accuracy defect is resolved.

Bit-by-bit interleaving with the exact face fallback bounds work by the
minimum of the conditioned work and `B poly(L_in)` on the same objective.
The residual growth probability is at most `1/B`, so all atoms and
zero-growth draws contribute only the bounded fallback residual. For
`p=k/2` the capped tail integration gives a constant integral for `k=1`
and `log B` for `k=2`. Together with the repaired deterministic
`Z^(k/2)` cost, this proves an absolute bit polynomial times
`1+nu S/sigma` for both specified finite laws. The zero-width and `k=0`
branches are present in the proof.

`rem:qp:moments` now starts its lower integral at
`t_0=max(1,a_0^(k/2))` and asserts it only for `B>t_0` (`04:303–311`).
That is the correct cutoff after passing from `Z` to `Z^(k/2)`; the old
impossible lower bound larger than the cap is gone. Its claim concerns
failure of inverse-growth moment integration, not a lower bound on the
algorithm. The example also distinguishes the real continuous proxy used
for this limitation from the actual finite-law theorem.

The old expected result is therefore not fully superseded. For `k<=2`
it gives linear numerical dependence on `nu S/sigma`; the closure theorems
give a degree-`k` product in their factor-range ratios. Neither is uniformly
stronger. The common-law qualification at `04:319–322` is correct: increase
the Gaussian accuracy budget before drawing so it satisfies both theorem
requirements, and charge that polynomial accuracy. No exact real-Gaussian
Turing-input claim is made.

## Separable and integer scope, anisotropy, and output

`def:qp:separable` and the scalar-oracle lemma (`04:752–794`, `B:782–800`)
use globally convex continuous rational piecewise-quadratic unaries with
rational knots. Integer scalar optimization uses exact forward-difference
binary search. Continuous scalar responses are affine on curved pieces
or constant at a knot; a flat piece is covered by endpoint responses.
This is enough for affine recourse pieces and rational exact output. It
does not establish the same finite affine-piece machinery for arbitrary
continuous higher-degree polynomial unaries.

`lem:qp:sep-pieces` (`04:796–813`, `B:802–836`) certifies the full global
separable recourse at every cell vertex. Its regions include the integer
forward-difference optimality inequalities, so no competing-label gap is
needed. This justifies aligned noise even with many integer variables.
Scalar binary search costs depend on integer label ranges only through
their bit lengths. The piece/fallback count includes all polynomially
encoded scalar pieces and labels as appropriate. Thus the theorem has no
`f(n_z)` factor, but it does not omit the input encoding of those variables.

`lem:qp:aniso` (`04:836–846`, `B:838–854`) rotates and rescales only the
supplied factor rows by exactly orthogonal rational `Q` and positive dyadic
scales. It preserves
`U^T Lambda U=alpha T^T T` exactly. The rational Jacobi accuracy and dyadic
enclosures yield the `1/16` frame and `max lambda_i<8 beta`; small singular
values increase bit lengths only polynomially. Approximation error is not
discarded or transferred into the convex unaries.

For `thm:qp:sep-gauss` (`04:853–869`, `B:856–888`), the balanced dyadic mesh
has `1<=lambda_i rho_i^2<4`. Hence its local-count constant is `1+8k`,
without a numerical largest/smallest curvature ratio. The anisotropic
witness gradient and diameter bounds supply the stated tube constant.
The base-only support/accuracy loop is repeated with the weighted range
sum, and the finite-law transfer remains valid. The full-row-rank promise
after preprocessing is explicit; no minimum-rank representation is
claimed. Its rational outputs and parameter
`beta diam(X)/sigma` are the actual supplied-factor contract.

The different pure native-integer theorem in `08:652–775` does cover
fixed-degree expanded rational convex polynomial unaries, including an
explicit finite list of rational polynomial pieces with rational knots.
I checked only the low-rank lattice dependency, `F:1018–1127`, for this
review. Clearing coefficient, factor, curvature, and noise-scale
denominators gives `D_0=2Q^3`; every original objective at an integer label
lies on `1/[D_0(M-1)]`. The terminal primal gap is at most
`1/(8D_0 M)`, strictly below that spacing. The auxiliary objective can have
a larger denominator; the proof correctly uses the original objective's
lattice instead. Exact integer witnesses, forward-difference search,
the mesh/resolution budget, and all query/evaluation bit heights are
polynomial in the stated fixed-degree input. No fallback is needed.
This does not extend the continuous piecewise-quadratic theorem. The
introduction distinguishes those scopes, apart from Q1's rank wording.

## Model calibration and final summary interfaces

`02:385–406` defines numerical parameters as part of an FPT tuple. The
Gaussian quadratic FPT bound uses intrinsic normalization; supplied-factor
regimes retain supplied curvature and range ratios. A short binary encoding
of a large numerical ratio is not called a small parameter. The ambient
uniform regime is not advertised as FPT in `k` alone.

The original-objective guarantee is the deterministic support regret
bound (`02:420–475`, `04:634–643`). For the actual Gaussian-like law its
support radius is `(b+20)sigma`, not the proxy standard deviation. Aligned
regret uses factor-coordinate widths. The calibration proof at
`02:477–516` chooses precision and scale jointly before sampling, finds a
least sufficient dyadic scale with polynomial bit length, and keeps the
resulting numerical runtime factors. It makes no claim to return the
unperturbed exact optimizer or to improve worst-case approximation theory.

The assigned rows of `tab:intro:results` (`01:150–165`) and
`tab:qp:regimes` (`04:888–900`) otherwise agree with their actual theorem
contracts: finite Gaussian-like law, exact rational values and minimizers,
mixed-solver factor only in general mixed quadratic recourse, no such
factor in separable recourse, linear two-direction numerical bound, and
the uniform dimension power. Q1 should be corrected before the table is
called a precise summary.

## Remaining dependencies and work performed

The internal mathematical proofs reviewed here do not leave an unproved
Gaussian count, a missing mixed conditioned proof, or an unresolved
all-draw termination mechanism. The external exact-solver prerequisites
at `04:60–76` still require the requested Luna source audit: the cited
exact rational convex QP result must cover singular and lower-dimensional
instances; the convex MIQP result must supply `f(n_z)L^c` with an absolute
exponent and the exact output contract actually used; and LP feasibility,
vertices, and denominator bounds must have the stated rational bit model.
The standard KKT, parametric-region, convex-analysis, measure, and
continued-fraction sources also need their final identities and precise
scope checked. I did not perform literature work or certify a novelty
claim. The discussion at `04:407–417` appropriately separates classical
parametric machinery from this manuscript's closure/counting argument,
but literature priority remains with that independent audit.

Work performed: targeted `sed`, `nl`, and `rg` source reads; an exact
Python SHA-256/line-count comparison for the ten listed files; independent
algebraic reconstruction of the inequalities and finite probability
budgets; and a targeted format check of this report. No computational
experiments, solver benchmarks, project-wide tests, builds, CI inspection,
delegation, bibliography search, or author-source edits were performed.
This report is the only file written for this review round.
