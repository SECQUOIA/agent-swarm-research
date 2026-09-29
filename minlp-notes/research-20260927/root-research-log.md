# Research log: September 27 continuation

## Scope and initial assessment

The user authorized new research without a preferred direction and asked for
continued work beyond publishable milestones. The initial working tree was
clean. Read the root instructions and targeted summaries of the September 25
batch, sparse indicator manuscript, exact penalty manuscript, and literature
challenge map. No previous manuscript was changed.

Parallel scouts examined sparse indicator quadratics, new structural
algorithms, penalties, cube quadratics, and singular-equality certification.
Each lane was asked for explicit claims, adversarial checks, and comparisons
with primary sources. Generic finite-moment separator approximation was
rejected as a main direction after finding the repository's prior-art audit;
it is already established approximation and optimal-transport theory.

## Initial candidates and assessment

1. **Quadratic path moment-order separation.** A Chebyshev-doubling circuit
   gives an exact threshold, with actual local probability measures below
   it. The root independently checked the Fourier-moment witness, the
   degree accounting for equality propagation, and a degree-four repair
   using four-variable paired bags. An independent reviewer improved the
   repair to three-variable bags of width two. The formulation must include
   quadratic box localizers and full truncated equality-ideal constraints.
   The threshold is exponential in chain length; ordinary bit input includes
   variable indices and has size `O(m log(m+1))`. This gives a superpolynomial
   input-size obstruction, without a claim of intrinsic optimization hardness.
   Detailed source comparison remains open.
2. **Native nonlinear dimension and penalties.** The common kernel of the
   native PSD Hessians can be eliminated with Farkas certificates. The
   resulting exponentially many projected rows retain small coefficient
   encoding, so effective real-algebraic radius bounds apply in the remaining
   dimension. The draft refines existing encoding bounds. The author is
   replacing a convex-objective multiplier argument by a metric error bound
   to cover nonconvex Lipschitz objectives as well.
3. **Few repulsive interactions.** A candidate approximation scheme replaces
   positive quadratic interactions by diagonal arithmetic-geometric-mean
   majorants and solves established submodular indicator subproblems. The
   proposed running time depends on the number and normalized strength of
   those interactions. Proof and prior-art review are pending.
4. **Budgeted low-rank selection.** Existing repository Loewner approximation
   sets may imply a scale-independent approximation scheme with exact binary
   budget feasibility. The general matrix-cover machinery is already local
   prior work; the specific optimization consequence requires comparison.
5. **Succinct fractional penalties.** Qualitative exactness for compact
   semialgebraic sets is classical. Effective Łojasiewicz bounds may give a
   useful encoding consequence: shrink the exponent to absorb an enormous
   coefficient. A polynomial-bit objective-range bound is essential; sparse
   binary-encoded degrees otherwise give an immediate counterexample. This
   lane is a supporting consequence unless a stronger contribution emerges.

## Targeted validation so far

The root has performed source and proof inspections, not a project-wide test
run. Initial commands were `pwd`, `git status --short`, scoped `rg` searches,
and selected `cat`/`sed` reads. Primary web sources inspected include
Han--Jiao--Weissman on moment matching, Wang--Pang's quadratic error-bound
abstract, Basu--Mohammad-Nezhad's effective Łojasiewicz theorem, and
Jiao--Pham--Tuyen's semialgebraic exact-penalty comparison. Source versions
and precise claims will be recorded in the corresponding result notes.

No Lean verification has been run in this continuation. The individual notes
record their exact arithmetic checks and independent reviews separately from
the root's checks.

## Reassessment after independent reviews

The shared-Hessian line became the leading positive direction. Its parameter
is the dimension of the linear span of the native Hessian **matrices**,
distinct from the dimension of their joint **ranges** in the initial rank
bound. The root independently read the complete active-set reduction,
affine restriction, sparse KKT argument, determinant reconstruction, and
two-block singleton elimination. No gap was found. The reviewer who proposed
the simpler KKT argument is explicitly credited as a contributor to that
proof; the root's separate reread supplies another check. A fresh reviewer
also audited the finite-bit ellipsoid bridge and primary GLS theorem.

The resulting exact-feasibility theorem needs no Slater condition. It concerns
decision, not a promise of a rational feasible point. The independently checked
three-quadratic singleton at `(cuberoot(2),cuberoot(4))` makes this distinction
concrete. The source audit compares generic algebraic degree, fixed-count
quadratics, one-row mixed-integer convex quadratic optimization, and the
Square-Root Sum barrier for unrestricted Hessian span.

A consequential follow-up is now proved and independently reviewed: compact
rational polyhedral approximations of convex quadratic rows, taken below the
uniform slice gap, give a MILP with the same integer variables and exactly the
same feasible integer assignments. Joint convexity is required for this route,
unlike the slice-convex NP consequence. The root separately read the full
formulation, discounted-tent LP proof, and algebraic-value resultant argument.
For fixed integer dimension and continuous Hessian span this gives exact
feasibility and an optimal integer assignment, though the formulation alone
does not recover an exact continuous solution. Its zero-integer-variable
special case gives a rational LP proof of exact continuous decision; the
ellipsoid proof remains an independent alternative.

A fresh package audit found a material precedent omitted from the initial
comparison. Kocuk (2021), Proposition 7, already preserves integer points of
intersections of integral balls through compact rational outer approximations.
The root independently inspected the open primary PDF, pp. 20--21, and added
the comparison to the reduction note. The candidate advance is the uniform
gap for existential continuous fibers, rather than the general idea of
integer-preserving approximation. The same audit replaced the diagonal
moment-curve motivation by a span-three PSD family needing arbitrarily many
common PSD generators, even outside its matrix span. The root independently
checked the range-intersection proof before updating the main value note.

The star lane produced an exact SDP projection for a continuous center and
arbitrarily many binary leaves. The root independently read both clipping
corrections, the complement transformation, the final affine-square identity,
and compact support-function separation. Forest gluing and the stronger
upper-RLT theorem for stable positive diagonal vertices have now passed fresh
reviews. The root separately read the greedy modular-minorant bridge and
common-uniform rounding proof. This strengthens the relaxation conclusion,
but does not supply a new tractability classification: Tardella's earlier
algorithm covers the latter objective class. The fixed-mean identity projects
out continuous means and must not be described as their complete moment hull.

The Chebyshev candidate survived proof review, including a distinct-chain
perturbation and uniform local regularity. Its novelty assessment narrowed:
Nie--Qu--Tang--Zhang already show a qualitative path-versus-dense separation,
the witness is classical Gauss/Lobatto quadrature, and a 2026 paper develops
composition-chain hierarchies. The retained additional claim is its exact
threshold and constant gap through exponentially many orders with fixed
quadratic coefficients. It is a possible focused limitation result rather
than a general solver advance.

The low-rank selection and few-positive-interaction schemes were documented
with independent reviews but downgraded relative to the main goal. Existing
repository matrix-cover theory and ordinary coordinate gridding respectively
provide strong methodological antecedents. The cube classification is proved
only under its stated strict assumptions; complete hull description remains
open. The singular-equality examples also remain supporting boundary results.

## Root-penalty completion and targeted document check

The root-authored succinct-root-penalty theorem received a fresh independent
review. The root separately inspected the primary source's Theorem 4.1, which
explicitly supplies the needed coefficient-bit bound. The weak-inequality and
compact-native-domain clarifications were incorporated, and the root rechecked
the review's small-exponent necessity, coefficient tradeoff, and numerical
tolerance examples. This is a supporting encoding corollary, not a new
qualitative exact-penalty theorem or an asserted speedup.

The command `git diff --check -- README.md` passed. A targeted inline Python
scan of the batch README, this log, `succinct-root-penalties.md`, and
`holder-penalty-prior.md` passed for four files and eighteen local links,
checking missing targets, raw control characters, trailing whitespace, and
final newlines. This was a document check of those files only. The root did
not rerun unchanged mathematical scripts already checked by their authors
and independent reviewers. No project-wide suite or CI inspection was run.

## Next implications under investigation

The root proposed removing continuous input bounds by applying the active
affine reduction to the minimum squared norm. Its restricted objective is
already positive definite, so the unknown norm of any existing feasible
point supplies convergence compactness without entering the algebraic
formula. A coefficient-height bound then gives a computable radius. Separate
authors and reviewers are developing and challenging this extension.

Two further tasks have been delegated: whether a low-complexity description
of the continuous projection combined with Khachiyan--Porkolab's small
integer-point theorem removes integer bounds as well; and whether coordinate
height bounds plus certified approximation recover exact algebraic continuous
witnesses. These are ongoing research questions at this point in the log.
The root inspected the local primary Khachiyan--Porkolab PDF using a targeted
`pdftotext -layout` conversion and read Basu's coefficient-sensitive block
elimination theorem directly. A separate terminology audit is checking
quadratic maps, few quadratic forms, and older algebraic optimization results.

The continuous-radius and canonical algebraic-witness extensions subsequently
passed independent review. The root read their full proofs, including the
coordinate singleton formulas, norm-sublevel localization, and conjugate
isolation. The witness procedure supplies coordinate minimal polynomials and
isolating intervals for one common minimum-norm point. It does not rely on
the existence of a rational feasible point. The common-field degree argument
also uses uniform degree bounds for every rational linear combination.

The unbounded integer-witness extension also passed review. The root read
the parameter-dependent affine charts, all-ranks consistency guards, sparse
stationarity parameterization, and bounded-approximation formula. Applying
Khachiyan--Porkolab directly to a common three-block formula avoids building
the potentially large chart disjunction. Its small-witness conclusion is
independent of predicate count; the existing bounded algorithm then decides
feasibility. A generic-background sentence about nonclosed projections was
corrected: affine images of finite convex-quadratic systems are closed.
The proof's bounded-limit argument does not need that additional theorem.

The root additionally read the complete unbounded finite-value proof through
its singleton elimination, and directly inspected Luo--Zhang's primary
closedness theorem. General convex-objective attainment is classical; its
use here removes the artificial ball from the span-dependent value bound.
Full optimizer recovery and mixed-integer objective extensions are now being
audited separately. These later developments require their own final scope
and source checks before replacing the earlier limitations throughout the
package.

A targeted inline Python check passed for the batch README, this log, the
main span theorem, its exact-feasibility note, and the mixed-integer reduction:
five documents and 37 local links, with whitespace, control-character, and
final-newline checks. This check preceded the latest log update and the
correction to the original prior-audit example. Mathematical checks run by
other agents remain recorded in their result and review files.

## Full optimization and sharper precision

The full unbounded mixed-integer optimization theorem subsequently passed
independent review. For fixed integer dimension and fixed continuous
Hessian span, it classifies feasibility and unboundedness and returns an
exact algebraic optimum and optimizer in the finite case. The root read
the complete proof, including the distinction between continuous recession
eliminations, which only delete coefficients, and integer eliminations,
which can change them. Bounding an optimal assignment in the original
coordinates is essential: lifting a small terminal assignment through a
sequence of quadratic eliminations can produce unnecessarily large values.
The corrected final optimization step either boxes each threshold problem
after adding the threshold or uses a uniform optimizer radius. A box that
only preserves feasibility would be insufficient.

Finite mixed-integer attainment is not a new contribution: the independent
source audit located Bank--Mandel's broader 1987 result. The candidate
advance remains the span-dependent precision and exact algorithm. The root
read the audit and reviewed proof but did not independently inspect the
entire original Bank--Mandel chapter.

The explicit value refinement now proves degree at most
`(2n+1)^min(h,n)` and coefficient bits `N^O(h+1)`. Its proof selects
independent active KKT gradients, then uses a finite multiplication
determinant and successive lowest-coefficient extractions. This tolerates
unrelated positive-dimensional complex components and unbounded
multipliers. The root independently reread the full proof and its exact
specialization arguments. Fixing an attained optimal integer assignment
also proves that the optimal value's degree has this bound independently
of integer dimension. The height does not: a pure integer repeated-squaring
chain has a rational optimum with exponentially many bits.

## Sharp error bounds and continued research

The qualitative Hölder bound and its quantitative refinement have passed
separate adversarial reviews. On a bounded region, distance to a nonempty
convex quadratic feasible set is at most `C V^(2^-h)`. The exponent is
sharp. With a rational input box, `log C <= N^O((h+1)^2)`. The root
independently read both complete proofs and the terminal-margin audit.
The quantitative argument fixes one canonical feasible point and keeps
every exposing multiplier and affine face in its common number field.
Absolute heights control determinants, Hoffman constants, and conversion
to one primitive element; compressed elimination then bounds the terminal
strict-feasibility margin.

One review found a necessary correction: exposing multipliers must be
restricted to native rows active at the fixed point, as well as active
polyhedral normals. Stationarity and normalization alone can choose a
combination with negative value and discard feasible points. The corrected
linear system explicitly enforces both activity conditions. The author,
independent reviewer, and root separately rechecked this correction.

Classical work already supplies quadratic Hölder bounds, repeated
square-root facial reduction, and coefficient-sensitive Łojasiewicz
constants. The proposed addition is the Hessian-span dependence while
retaining the sharp exponent. An additional source search is pursuing
unavailable original Wang--Pang and Luo--Sturm texts. Search failure does
not establish priority.

The next investigations sharpen optimizer coordinates using ordered
objective regularization and row relaxation, and test a multihomogeneous
Bézout improvement to the explicit degree. Separate authors and fresh
adversaries are checking these arguments. Two further lanes examine
transparent algebraic primal/dual certificates and succinct feasible
curves certifying unboundedness. These remain investigations at this log
entry, not established consequences.

The ordered optimizer refinement and sharp degree theorem subsequently
passed independent reviews. The root read their full proofs. The exact
worst-case degree for the canonical optimizer field and optimal value is
`max_{s<=min(h,n)} 2^s binom(n,s)`; coordinate coefficient bits are
`N^O(h+1)`. The upper bound applies classical multihomogeneous Bézout to
regular selected KKT roots, with a single parameter identity that survives
exceptional specializations and ordered limits. The matching rational
strictly convex examples use the classical generic QCQP degree, an
irreducible universal KKT incidence, and Hilbert specialization inside a
real open set. Differentiating the critical value with respect to objective
linear coefficients proves that the generic value generates the optimizer
field. The root independently checked these arguments and directly inspected
the isolated-root Bézout theorem and the Hilbert irreducibility corollary
in the cited primary papers. These classical ingredients are explicitly
credited; sharpness does not establish priority of the structural theorem.

The further Hölder source audit obtained the complete Luo--Sturm quadratic
systems chapter and found a short alternative derivation through the full
Shor lift and established partial-polyhedral conic error bounds. The root
read and checked the compressed exposing-matrix argument and its slack-sign
conditions. The qualitative exponent is now positioned as a modest
structural corollary. The arithmetic constant and its dependence on the
matrix span remain separate results. A discrepancy between later accounts
of Wang--Pang's singularity count remains unresolved without the original
proof; no identification of those counts is used here.

The root ran a targeted inline Python check of the batch README and this
log: two documents and 33 relative links passed whitespace, control-character,
and final-newline checks. This check preceded the present sharp-degree and
source-audit additions. Other targeted symbolic checks are recorded in the
new result and review files; no project-wide verification or CI inspection
was performed.

## Common-field output, rational certificates, and a broader frontier

The common-field recovery procedure has completed independent review. The
root read its full proof: recognize a primitive linear combination, recover
the norm polynomials of its sums with each coordinate by interpolation, and
differentiate to recover coordinate expressions in the primitive element.
Raising each sampled minimal polynomial to the correct field multiplicity
handles nonprimitive samples. The procedure uses classical recognition and
rational univariate representation methods; its role is to complete the
exact output and verification contract.

Continuous optimality certificates now use that one field, at most `h`
curved exposing sections, and a final KKT identity. The root checked the
full certificate proof. All native tangents are valid global relaxations,
so the certificate does not need to verify an affine-hull calculation or
a constraint qualification. A separate reviewed refinement makes convex
infeasibility certificates entirely rational. Rounding their positive
aggregate weights must preserve exact kernel equations; otherwise a nearby
quadratic can become unbounded below. The root independently checked this
kernel-preserving rounding argument and its inverse-perturbation bound.
Nested-square examples show that the rational aggregate weights themselves
can require exponentially many bits in `h`. This is a limitation of that
certificate format, not of every proof system.

The error-bound constant also improved to `log C <= N^O(h+1)`.
Direct elimination over the common number field avoids the larger exponent
from encoding a primitive element before quantifier elimination. The root
read the complete local-norm and product-formula proof, including the
selected-embedding reciprocal Cauchy bound. A fresh independent reviewer
checked the arithmetic and the terminal-margin application. The earlier
quantifier-elimination proof remains a valid conservative alternative.

The escape construction now produces integer-coefficient polynomial
increments for every feasible anchor in a supplied box. Its circuit has
polynomial size even when its expanded degree is exponential. The root
independently read the complete strengthened proof and checked the
denominator clearing and uniform anchor bounds. With the common-field
anchor, the complete unboundedness certificate is polynomially checkable
for fixed integer dimension and continuous Hessian span. The literature
audit located the exact older conditional boundedness classification and
continuous/integer equivalence in Obuchowska (2008). Those conclusions are
credited as prior work. The circuit is retained as a supporting constructive
result, with priority unresolved.

A fresh package reassessment found no direct subsumption of the principal
fixed-span exact optimization class in the examined sources. It separately
reconstructed the optimal integer-witness and ordered-degree proof chains.
The next investigations now address two stronger questions: algebraic
feasible-point certificates without convexity, and polynomial-input-size
families forcing degree `n^Omega(h)` in explicit exact output. They have
promising arguments but are not recorded here as established results.

The latest targeted inline Python check passed for the updated batch README
and this log: two documents and 43 local links, with final-newline,
trailing-whitespace, and control-character checks. It did not rerun unrelated
mathematical scripts or inspect CI.

## Nonconvex certificates and general second-order cones

The nonconvex witness theorem has now passed both written proof reviews.
The second reviewer had not participated in its development. The root read
the entire proof and the revised genericity argument: cumulative degree
must include components of lower dimension, and both the multiplier
Hessian and bordered KKT matrix must be nonsingular. The latter condition
cannot be replaced by gradient independence for indefinite Hessians.
The final proof includes both safeguards.

The theorem gives a common algebraic feasible-point representation of size
`N^O(h+1)` for arbitrary rational weak quadratic inequalities of Hessian
span `h`, with arbitrarily many affine rows and no bounds. Thus exact
feasibility lies in NP for fixed `h`. The usual Boolean encoding makes it
NP-hard already at span one. Boxed arbitrary quadratic optimization has a
small exact optimum and optimizer encoding, but this does not certify
global optimality or give a polynomial-time discovery algorithm. The root
independently reconstructed the perturbation, finite-limit and common-field
arguments. Exact sample calculations were run by the reviewer and are
reported there; the root did not rerun unchanged scripts.

The result may support a broader convex algorithmic class. A general
second-order cone inequality becomes one possibly indefinite quadratic
inequality and a sign condition. The nonconvex precision theorem could
therefore supply the gap needed by a rational polyhedral outer
approximation. Separate agents are testing exact continuous feasibility,
preservation of bounded integer assignments, and removal of integer bounds
through a compressed continuous-fiber formula. These remain pending proof
and literature review. In particular, finite values need not be attained
for general second-order cone programs; the earlier convex-polynomial
attainment theorem cannot be transferred to this setting.

A separate investigation is extending the nonconvex value bound to finite
infima on unbounded domains by treating an expanding box radius as an
algebraic parameter. The explicit input-size lower-bound construction is
also still under review. Neither pending result is used as an established
claim in the main synthesis.

The fresh nonconvex literature auditor then found a simpler route to the
feasible-point and radius conclusions. In the lifted set `P` intersected
with `h` quadrics, choose a face of `P` of minimum dimension that meets the
quadrics. No point of that variety lies on the face's relative boundary.
Every connected component of the variety on its affine hull that meets the
face therefore lies entirely in the face: its intersection with the face
is both closed and open in the component. Applying Grigoriev--Pasechnik's
established component-sampling theorem on this rational affine space gives
the required short common algebraic point. The root independently checked
the argument, and another reviewer checked the face and source details.
The certificate and radius bounds should consequently be positioned as a
short structural corollary, not a principal original contribution. The
value bounds and parameterized projection descriptions require separate
arguments; this simplification does not by itself subsume them.

The exact SOCP feasibility and unbounded mixed-integer extension have since
passed their written independent reviews. The root read the entire rational
folding construction, uniform fiber gap proof, compressed projection formula,
and the integer-witness application. The formula includes a finite grid of
small integer perturbations: a successful choice may depend on the real
integer-coordinate parameter, while the grid and its coefficient bounds do
not. All affine ranks are covered. A radius quantified before the residual
tolerance forces an actual feasible fiber instead of a point in a projection
closure. The large Boolean formula is used only for the established
Khachiyan--Porkolab witness bound; the algorithm never constructs it.
No gap was found in this independent reconstruction.

The cone source audit found an elementary projective reduction proving
one-cone exact feasibility from classical convex quadratic programming.
The one-cone bounded-integer projection also follows from older rational
QP witnesses and rational cone approximations. Those cases are not treated
as main novelty claims. Further audits are testing whether the whole
span-one subclass has a similarly short prior-based proof.

The small-input degree lower bounds are also complete. The root read both
the effective Hilbert construction and the direct Eisenstein construction,
including the latter's local splitting, compositum degree, value valuation,
constructive primitive weighting, and positive definite Hessian refinement.
The root directly checked the Hilbert-index definition and specialization
estimate in Dèbes--Walkowiak's primary paper. The results force degree
`n^Omega(h)` with polynomial input length. They obstruct writing a dense
minimal polynomial in FPT time, not feasibility decisions or succinct exact
answers. The arithmetic construction is a direct refinement of the
existence theorem, not a stronger degree lower bound. Existing exact
computational checks and their limits remain recorded in the source notes;
the root did not rerun them.

The finite-infimum extension has completed a fresh proof review and a
separate audit of its elimination lemma. The root read the complete proof:
affine charts depend affinely on the box radius with fixed denominators;
generic perturbations work outside finitely many exceptional radii;
the lowest perturbation coefficient is extracted before the highest radius
coefficient. This order is essential. The resulting nonconvex finite-value
degree and height bounds give exact classification and value recovery in
`FP^NP` for fixed Hessian span, including unattained infima. The refined
coefficient accounting is linear in the input coefficient bit bound,
times a structural factor with exponent `O(h+1)`.

The reviewed SOCP recovery procedure now completes exact feasible-point
output. The root independently checked minimum-norm uniqueness, rational
norm-cone thresholds, coordinate-box bisection, and the use of a fixed
canonical point for algebraic recognition. An enlarged witness box contains
the global minimum-norm point; a box containing merely some feasible point
would not justify that claim. The original conservative complexity bounds
suffice for polynomial time at fixed span; sharper coefficient-sensitive
runtime accounting is receiving its own recheck.

Further boundary checks have proved useful. Three rational native PSD
quadratics can meet at the sole point `(cubert(2), cubert(4))`; a positive
algebraic aggregate proves uniqueness, while no nonzero rational positive
aggregate exposes it. The root directly checked this identity and the
positive definite ellipsoid variant. A separate standard Boolean encoding
and Valiant--Vazirani argument shows why a convexity promise on an arbitrary
quadratic description is insufficient for the cone algorithm. Rational
SOC examples also show that the earlier integer-polynomial escape and
continuous/integer boundedness equivalence cannot be transferred to
general cones; direct earlier conic examples are credited.

The next main proof task is an encoding bound for attained nonconvex
optimizers without an input box. The proposed argument uses ordered limits
for a generic perturbation, norm regularization, and the growing box. If
successful, it should give an attainment decision and optimizer recovery,
and enable full exact continuous SOCP optimization. These extensions are
pending and are not used in the completed theorem statements.

The root's latest targeted inline Python check passed for the batch README
and this log: two documents, 56 local links, final newlines, trailing
whitespace, and control characters. No project-wide verification or CI
inspection was performed. This entry records that check after the text
and link changes above.

### September 28: attained optimizers, rationality, and common range

The nonconvex attained-optimizer extension is complete and independently
reviewed. The root read the full replacement proof and its algorithmic
consequences. If a global optimizer exists, minimizing the objective plus
epsilon times squared norm bounds every regularized minimizer by the norm
of a minimum-norm optimizer. An unknown box contains all their quadratic
lifts strictly. For each fixed epsilon, every limit of the generic band
perturbations is an exact regularized optimizer, so all box rows eventually
become inactive. The selected KKT charts contain only original affine rows;
the unknown radius never enters their coefficients. Ordered extraction
first in the band parameter and then in epsilon bounds the common field
and representation of a global minimum-norm optimizer. This simplifies
the original three-limit proposal without exchanging limits.

The root separately checked the attainment algorithms. A computable box
contains some optimizer if one exists, so equality between its compact
minimum and the original exact infimum decides attainment. With a general
NP oracle, an algebraic-point certificate can instead be tested against
the already recovered value using its minimal polynomial and isolator.
Prefix search recovers a point; norm-threshold queries recover the least
optimal norm first if desired. The one-quadratic SAT construction has
known infimum zero and attains it exactly for satisfiable instances. These
arguments establish fixed-span FP^NP classification and recovery; they do
not supply short certificates of global optimality or remove the NP oracle.

The continuous SOCP affine-optimization reduction is also complete. The
root read its entire proof after the optimizer dependency cleared review.
Value bounds and rational thresholds handle finite nonattainment. Compact
restricted minima equal to the recovered optimum simulate optimal-face
feasibility without giving algebraic coefficients to the conic oracle.
Norm and coordinate bisection approximate the same canonical optimizer;
joint-field recognition then returns it exactly. Keeping structural size
separate from coefficient bits preserves N^O(h+1) through the nested
queries. The integer-only objective corollary was separately read: a
denominator-scaled objective has integer values, its convex epigraph has
a small optimal integer assignment by Khachiyan--Porkolab, and rational
quadratic thresholds add no continuous Hessian direction. Neither result
establishes general optimization with unbounded integer variables and a
continuous objective.

The root read the quantitative completion of the two-span PSD rationality
theorem. Its tangency argument counts roots of the reduced rational
Schur-complement numerator, not the raw determinant. In the strict case,
one added quadratic inequality s*y >= 1 converts a classical fixed-map
sampling radius into a lower bound on common slack. Dyadic rounding then
gives a polynomial-size rational feasible point. The non-strict cases
require one rational affine restriction and then LP or the classical
one-quadratic witness theorem. Span three is therefore the sharp native
PSD threshold for possible irrational-only feasibility. The older boundary
note now links to this resolution. Efficient rational output and stronger
prior-art comparison are being investigated separately.

The common-range feasibility theorem has completed a fresh proof review.
The root read the proof and source audit, then directly checked the saved
primary Basu--Roy Theorems 3--4 and Del Pia Proposition 4. Farkas projection
leaves only r nonlinear coordinates and exponentially many quadratic rows,
each with polynomial coefficient bits. The meeting-radius theorem bounds
some feasible point. Applied to the compact reciprocal residual epigraph,
the containing-radius theorem instead bounds the reciprocal of the least
positive violation. Their logarithmic dependence on row count permits
implicit use of the projected rows. Rational outer lifts then have size
2^O(r) times a fixed polynomial in input length. The mixed-integer theorem
uses an explicitly FPT MILP algorithm, rather than inferring a uniform
exponent from a fixed-dimension polynomial-time statement. For unbounded
SOC integer variables, the eliminated continuous directions must avoid
integer-continuous cross terms too. The proof does not assert the stronger
continuous-block parameter alone in that case.

The sparse-output refinement was also read in full: an integer objective
translation can make every minimal-polynomial coefficient nonzero, and
a rational unimodular coordinate change can put a primitive optimizer
element in one coordinate. These extend the dense-output lower bound to
ordinary sparse minimal-polynomial lists and coordinate minimal polynomials.
They do not exclude circuits, towers, or shifted bases.

Active higher-potential tasks now include exact unbounded MISOCP optimization
with one integer variable, possible extensions to more integer variables,
and FPT optimization and algebraic recovery under the common-range
parameter. These are not yet used as established results. A simplification
of the already proved finite-infimum theorem is receiving fresh review.

The root's targeted inline Python check passed for four changed documents
(the repository README, batch README, rationality boundary note, and this
log), covering 305 local links, final newlines, trailing whitespace, and
control characters. Subagent work was then interrupted by a usage limit.
The user's renewed continuation instruction resumed research from the saved
files; incomplete extensions retained their pending labels.

Fresh reviewers have now completed the interrupted finite-infimum addendum
and bounded-integer SOCP checks. The root read both full proofs. For a
finite unattained infimum, an epsilon-dependent unknown box contains all
norm-regularized minimizers. Its boundary becomes inactive before the
algebraic step, and only the scalar value needs a finite outer limit. The
original independently reviewed symbolic-radius proof is retained as an
alternate. The bounded-integer theorem uses a compact continuous box both
to decide attainment and to choose an attained optimal integer fiber;
comparison with an unboxed fiber infimum would be invalid. Neither review
required a mathematical correction. Their targeted checks and exact
examples are recorded in the separate review files.

The root subsequently read the common-range witness proof in full. Its
canonical nonlinear projection has a joint algebraic degree bounded solely
by the nonlinear dimension. The proof keeps the exponentially many Farkas
rows implicit: the generic perturbation coefficient bits depend on their
logarithmic count. The full KKT system has at most twice the nonlinear
dimension, so no large affine block enters its degree. In the remaining
linear fiber, an active Gram-matrix formula keeps all coordinates in that
same field. Outward rational right-side approximations, exact rational
minimum-norm QPs, and a uniform rational-matrix Hoffman bound approximate
one fixed point for recognition. A fresh adversary, separate from the
reviewer who suggested a simplification, checked the full proof and found
no substantive gap. This completes FPT exact feasible output under the
common-range parameter.

The common-field conic feasibility extension is complete and reviewed.
The root read the whole manuscript and review, including the local-height
extension for indefinite squared cone rows, the extra field-generator
quantifier, and every outward-rounding inequality. Its exact gap belongs
to the original field-valued system; the rationally rounded Hessians need
not preserve its span. The final rational MILP preserves feasible integer
fibers inside the proved boxes. One encoded algebraic objective threshold
is an important special case. This supplies an attainment oracle after a
finite value has been encoded, but does not itself bound that value.

The one-integer value theorem has also passed independent review. The root
read the full argument and directly inspected the coefficient-size clause
of Basu's survey Theorem 2.27 in the saved primary text. After eliminating
only the compressed few-variable formula, all finite changes of planar
epigraph branches occur below a uniform root bound. Far-tail branches are
constant or strictly monotone, including their endpoint-membership status.
A finite integer infimum is consequently a bounded fiber value or a finite
algebraic limit at infinity. An attained optimum can be moved to a bounded
integer assignment if necessary. This proves fixed-span FP^NP full
optimization for one-integer nonconvex quadratics, and polynomial-time full
affine MISOCP optimization. The conic attainment algorithm can use the
already reviewed bounded-integer theorem and does not need the separate
common-field extension. The stronger nonconvex conclusion remains limited
to one integer variable.

The rational-output algorithm at native PSD span two is now complete and
reviewed. The root read the full proof. It determines the minimal relevant
affine face by exact affine optimization. A positive common margin permits
coordinate bisection and rational rounding inside that face. A zero margin
instead gives a rational gradient restriction, or a computable rational
tangency multiplier from the reduced Schur-complement numerator. The
remaining problem is an LP or one classical rational convex QP. This
constructive result supersedes the earlier statement that rational output
was only possible in principle. General rational-point algorithms with
ambient-dimension dependence are explicitly credited.

The main ongoing extension now uses bounded rational linear forms to treat
several unbounded integer variables. The root reconstructed the complete
geometric induction and read its draft, including the coefficient-sensitive
general convex-semialgebraic epigraph theorem. A sublevel's bounded-form
space is independent of its level above the continuous infimum. If its
rational part vanishes in full dimension, maximal lattice-free containment
forces equality of integer and continuous infima. Otherwise a bounded
integer form can be fixed along a near-optimal subsequence. Proper affine
hulls are handled first by rationalizing a sampled algebraic equation.
The root directly checked Lovasz's cylinder theorem and maximal-containment
corollary in Basu--Conforti--Cornuejols--Zambelli, as well as the relevant
Khachiyan--Porkolab size statements. A further fresh adversarial review
and a dedicated prior audit are checking the completed manuscript. No
unqualified novelty assertion is being made.

The several-integer theorem has now passed its fresh full review and a
separate coefficient-height audit. The root read those arguments and the
completed primary-source comparison. Expanding sampled affine equations
in one number field, then taking rational minors, keeps bit growth linear
in the current coefficient height. Integral lattice substitutions have
the same property, and the proof carries the original atoms through the
dimension reductions. The qualitative rational-slice consequence already
gives algebraicity and a degree bound. The additional quantitative work
controls height and optimal integer assignments; those are the points
requiring further publication-level novelty assessment.

The objective-excluded common-range optimization theorem is also complete.
The root read the full constant-matrix QP chart argument, its low-dimensional
value and witness bounds, and the unbounded-integer composition. A basis
of every active normal, including zero-multiplier rows, identifies the
minimum-norm fiber optimizer through a rational Moore--Penrose solution.
Quartic charts give exact arithmetic bounds without being enumerated.
The continuous recovery proof uses the common objective gradient and
rational-normal equations to recover a point over the recognized field.
The general mixed-integer value bound then removes integer input bounds
with an absolute polynomial exponent. Conditional optimal-assignment
bounds and the reviewed boxed algorithm decide attainment. At zero full
continuous common range, rational polynomial chart values lie in a fixed
rational grid, so every finite mixed-integer minimum is attained.

The root has also read the proposed convex-polynomial feasibility theorem
and its full implicit-oracle audit. A certified residual gap permits a
strict relaxation and a grid only in the nonlinear continuous coordinates.
Normalized Farkas multipliers give an LP oracle returning one violated
convex polynomial. Rational LDL test points provide shallow cuts, and
controlled lattice maps preserve linear coefficient-bit growth through
the fixed-dimensional recursion. A fresh full review remains pending;
the theorem is not yet promoted in the main index. Full polynomial
optimization and exact witness recovery are being investigated separately.

The root's targeted inline `python -` check passed for the repository
README, continuation README, and this log: three changed documents and
316 local links, plus final newlines, whitespace, and control characters.
No unchanged mathematical script, project-wide check, or CI inspection
was run for these index and research-record updates.

### September 28: an explicit quartic obstruction and broader exact models

The three-ellipsoid construction led to a stronger concrete result. The
integer quartic

\[
 F=A^2+10000[(x^2-y)^2+(y^2-2x)^2],
\quad
 A=12599x^2-10000xy+7937y^2-15874x-12599y+20000
\]

has Hessian at least \(4124I\) everywhere and unique zero
\((\sqrt[3]{2},\sqrt[3]{4})\). The root independently derived the
translated quadratic, cubic, and quartic Hessian bounds and checked their
exact constants with rational arithmetic and symbolic reduction. An
initial checker used a strict comparison at an equal rational interval
endpoint; changing it to a weak comparison corrected the check, with no
change to the proof. The complete root reconstruction is in
[the additional audit](convex-quartic-root-audit.md), alongside a fresh
review by an investigator who did not develop the example.

The root directly read Table 1 and Appendix C of Slot--Steurer--Wiedmer's
November 2025 manuscript. It leaves rational compact witnesses for exact
convex quartic programming unknown, gives an irrational-zero sextic, and
proves a univariate quartic rationality statement. The example answers
the stated general rational-witness possibility negatively in two
variables. It does not establish decision hardness or preclude algebraic
certificates. Degree four and dimension two are the first possible pair
for this obstruction. A separate rational SOS certificate for the Hessian
and targeted Lean coverage are being investigated; neither is yet part
of the verification claim.

The root also read the full three-ellipsoid construction, its short
binomial coefficients, independent field blocks, and primitive-coordinate
argument. The rational companion pencil converts positivity on the
nonreal-root subspace into a positive semidefinite matrix of corank one.
A rational triangle around that member gives three positive-definite
quadratic inequalities isolating the algebraic power-basis point.
Independent blocks yield a feasible-coordinate minimal polynomial of
degree \(d^k\); a small translation makes every coefficient nonzero.
This excludes both dense and ordinary sparse FPT output in that format.
It does not exclude compact extension towers or FPT decision.

The convex-polynomial feasibility theorem has now passed its full review,
including the corrected short lattice-map proof. The root additionally
rechecked Toledo's primary Theorem 4.4 and Section 5. Its parallel explicit-row
application has a dimension-dependent power of logarithms, which is
compatible with FPT arithmetic complexity. Earlier blanket descriptions
as XP have been corrected in the two affected prior comparisons.
Controlled Turing precision and the implicit LP evaluator remain separate
issues. Full polynomial optimization and its exact output are in final
review, with classical finite attainment expressly credited.

The quasiconvex semialgebraic value theorem and affine-fractional MISOCP
completion have passed fresh reviews. The root read the entire proof:
nested bounded-form spaces and affine hulls have finitely many controlled
transition levels; a small cap inside the interval containing the unknown
infimum permits dimension reduction. Strict sublevel convexity suffices
for value bounds, while optimal integer witnesses require convexity of
the weak optimal slice. A Pell construction shows this distinction is
necessary. For positive affine denominators, a rational auxiliary value
variable adds only one continuous Hessian direction after fixing the
integer assignment. The nonconvex minimum-norm theorem then supplies the
uniform conditional optimizer box used in compact attainment queries.

The full convex-polynomial optimization theorem has now completed its
fresh review. The root read the assembled proof, including the uniform
canonical-point bound for every optimal integer assignment in the search
box, the inclusion of the value in the output field, and rational QP
recovery of the remaining linear coordinates. Classical attainment lets
one fix an optimal integer fiber to bound the value and output field
degree solely by nonlinear continuous dimension and polynomial degree.
Time and height retain their dependence on integer dimension. The
repeated-squaring example independently shows that exponential degree
growth in nonlinear continuous dimension is unavoidable.

The root's targeted inline Python check passed for four changed files:
the two README files, this log, and the quartic root audit. It checked
329 local links, math delimiters, final newlines, trailing whitespace,
and control characters. No unchanged theorem script or project-wide
verification was rerun for these documentation changes.

### September 28: universal quartic realization and completed formal checks

The root has read the complete effective arbitrary-algebraic singleton
construction, the universal strongly convex quartic construction, and
its rational SOS-convex strengthening. Each has a fresh independent
review. The construction realizes every real algebraic number with
exactly one real conjugate as a coordinate of a unique rational quartic
zero, with polynomial-time construction and polynomial coefficient length
in the dense minimal-polynomial input. Rational squares certify
nonnegativity, and a positive definite rational Hessian Gram matrix
certifies convexity. The converse is the real-embedding obstruction.
The root independently checked the translated homogeneous Hessian bounds,
the Gram block and Schur-complement estimates, and the coefficient
projection that preserves its positive margin.

The explicit two-variable example now also has completed targeted Lean
coverage. Its actual second directional derivative is at least
\(4096\) times the squared direction norm; affine-line convexity then
proves the functional ConvexOn statement on the plane. Existence and
uniqueness of the irrational zero and absence of rational feasible
points are formalized. A separate reviewer matched the final frozen
source to the intended formulas. The root read the derivative chain,
SOS identity, and final convexity bridge. The stronger analytic bound
\(4124I\) is not formalized. The exact targeted command and source hash
are in the verification record; the root did not duplicate that build.

The publication audit identified important close prior results. The
Bienstock--Del Pia--Hildebrand cubic already has the same irrational zero
and is strongly convex on its stated rectangle. Global convexity is the
essential distinction. Rational Gram rounding, interpolation modulo an
ideal, and SOS-convex regularization are established techniques. The
explicit example answers the rational-point-witness entry in the
inspected November 2025 arXiv version of Hesse's Redemption. A STOC
2026 version exists, but its full text remains uninspected. The root's
additional web searches for the title, proceedings identifier, and
quartic irrational zeros found no verified replacement source resolving
that access gap. These searches do not establish priority. The full
assessment records sources and separates the structural theorem from
decision-hardness and performance claims.

The root also read the full globally quasiconvex polynomial extension
and its main review. The zero-row Farkas vertex classification preserves
quasiconvexity, while rational line samples avoid the invalid stationary
gradient shortcut. The continuous affine-direction lemma justifies
computing the nonlinear core from continuous Hessian blocks. The
result retains full exact FPT optimization and a common output-field
degree independent of integer dimension, with classical attainment
and quasiconvex integer machinery credited.

The root read the completed common-range affine-fractional main and
witness proofs. Retaining denominator directions gives rational
coefficients in the remaining linear fiber. Uniform canonical-point
boxes and compact value comparisons decide attainment and recover the
optimizer; minimum-norm cuts use only retained coordinates. The shared
reciprocal cone lift preserves the intended positive-denominator domain
and adds only its stated number of nonlinear directions. A wording
error about representing affine inequalities by both signs was flagged;
the working version correctly says equalities. No mathematical change
to the proof was needed.

New work remains active. A separately drafted construction aims to
halve the power-basis embedding dimension and prove its optimality for
that particular embedding. Independent tasks study arithmetic degree
versus arbitrary embedding dimension and the degree cost of univariate
convex realization. These candidates are not promoted as verified results.

The root's latest targeted inline Python document check passed for the
two README files, this log, and the quartic root audit: four documents
and 341 local links, plus math delimiters, final newlines, whitespace,
and control characters. No project-wide verification or CI inspection
was performed.

The root subsequently completed the full read of the quadratic-over-affine
value and canonical-output proofs. The numerator Hessian may have
arbitrary rank and stays outside the native common-range parameter.
The same constant-matrix QP charts prove that the projected optimal set
is closed. On an optimal fiber, the numerator's raw gradient is constant,
allowing rational-normal equations for the remaining algebraic fiber.
The proof correctly restricts its common-field chart assertion to actual
optimal levels; the minimum-norm point of an arbitrary quadratic
sublevel can require a larger field. The complete FPT theorem is now
indexed with its classical continuous polyhedral predecessor.

### September 28: degree, dimension, and certificate boundaries

The smaller universal quartic realization has passed a fresh review.
The root read its full proof and independently checked root-pair Gram
products, exact congruence projection, normalized residual Jacobians,
precision bounds, and the lower bound from restricting to the moment
curve. It uses \((d+1)/2\) variables, optimally for consecutive-power
coordinates. No unrestricted minimum-dimension claim follows.

The cyclic construction has also passed a fresh full review and a
separate quantitative audit. The root independently reconstructed its
exponent relations, grounded energy, Jacobian bound, and short rational
coefficient construction in
[an additional audit](cyclic-quartic-exponential-degree-root-audit.md).
The zero has degree \((2^{n+1}-(-1)^{n+1})/3\), although the
integer coefficients have only logarithmically many bits in \(n\).
The root's exact inline fraction and symbolic checks passed the
specified 78 exponent/parameter cases and ten determinant/energy cases.
These check identities, not universal convexity by sampling.
The fresh reviewer additionally built and verified a rational Hessian
Gram in two variables. The original binomial root description is
succinct; the root's one-coordinate translation supplies the separate
ordinary sparse minimal-polynomial obstruction.

The root developed a rational rank-one square-root adjustment reducing
this family to \(n+1\) integer quadratic squares. Two other investigators
independently checked the matrix identity and precision range. The
full independent review and exact checker are linked from
[the supplement](cyclic-quartic-square-compression.md).
One sentence initially assigned an interval margin to the bisection
midpoint instead of the exact target root. The root rechecked and fixed
it: the target-root margin is \(4\Delta\), and the midpoint margin
is at least \(7\Delta/2\). The algorithm and its conclusion did not
change. No minimum-number-of-squares claim is imported before its
separate topological proof has been fully checked.

The root read the expanded arithmetic-degree upper proof. Weighted
projective degrees control positive-dimensional intersections, and
complex conjugation excludes a sole line without real points. The
length-three residual argument explicitly handles nonreduced schemes.
The root opened the primary Eisenbud--Green--Harris PDF and inspected
printed pages 195--197 as images. Its modern Cayley--Bacharach formula
has the required degree \(n-3\), and its stronger conditional theorem
indeed covers ambient dimension at most six. The new bounds used here
give exact maxima three, five, and eleven in dimensions two, three,
and four for the stated rational SOS class. These are applications
and refinements of classical intersection tools, not new versions
of Cayley--Bacharach. The scope excludes arbitrary convex quartics.

The univariate degree lower bound and compressed multiplier construction
now have fresh assembled-proof reviews. The former forces exponential
expanded degree for short cubic inputs; the latter retains a short
arithmetic circuit. The root independently checked the Markov mechanism,
the finite-inequality extension, and the convex-objective derivative
argument. The compressed construction's full quantitative proof retains
its own reviewers' verification; the root has not yet reread that proof
in full. A restricted monotone cube-root circuit extension has also
completed fresh review. Its explicit \(k\ge1\) correction is necessary:
the previous zero-gate wording would make its constants undefined and
could not produce a quartic in zero variables.

The root supplied a fresh full review of the shared-curvature fractional
maximum theorem. All normalized numerators must have the same strictly
positive curvature multiple. A common lifted QP gives the value bound,
and the active-midpoint argument gives a constant raw gradient on each
continuous optimal set. The reviewed algorithm recovers the canonical
point through compact value comparisons and rational-normal fibers.
No additional symbolic test duplicated the author's checks.

Further work remains active on noncirculant degree constructions,
minimum SOS length, restricted algebraic circuits, and rational SOS
descent. The last question has produced a concrete candidate: a rational
strongly SOS-convex quartic with rational minimum zero but no rational
SOS representation. Its coefficient-level certificate and fresh
review are still being documented, so it is not yet indexed as a result.

The root's targeted inline Python document check passed for seven
changed root-authored or index files and 356 local links, including
math delimiters, final newlines, whitespace, and control characters.
The scoped git diff --check on those paths also passed; untracked
files are covered by the Python check rather than that Git command.
No project-wide check or CI inspection was performed.

### September 28: exact SOS coefficient fields

The rational SOS descent candidate is now a verified milestone.
The four-variable example passed two independent proof reviews and
exact rational Hessian checks. The root then read its main proof,
algebraic construction, and prior comparison in full. Its degree-nine
zero forces six rational quadratic relations; a mixed coefficient
lies outside their product span. This establishes failure of rational
SOS even with a strict rational Hessian Gram.

A stronger three-variable example was subsequently found:
\(F=A^2+r_0^2+r_1^2+r_2^2+r_3^2-r_4^2\), with the small integer
quadratics specified in
[the final main note](ternary-rational-sos-convex-counterexample.md).
It has 31 terms, coefficient magnitudes at most 448, and
\(\nabla^2F\succeq I\). Its zero is
\((a^{-1},a,a^{-3})\), \(a^5=2\). Two fresh reviewers checked the
explicit certificate, one by reconstructing its matrix and verifying
leading principal minors independently of the retained checker.

The root independently checked the two-coefficient SOS obstruction,
then supplied the prime-degree field restriction and a rational
three-square Taylor integral. The author strengthened the restriction
to every real subfield: a proper factor of \(T^5-2\) would already
put its real root in that field. The root rechecked this argument and
the separate PSD Gram necessity. The final result is an exact field
classification, not just a divisibility bound: SOS and PSD Gram
certificates exist over a real field precisely when it contains
\(\mathbb Q(2^{1/5})\). Fresh reviewers verified the strengthened
statement and the dimension-minimality deduction from Scheiderer's
classification. The root's role and nonduplicated verification are
recorded in [its audit](rational-sos-convex-descent-root-audit.md).

Every positive rational constant perturbation admits rational SOS.
The proof uses the strict centered polynomial Gram and rational
density in its full affine Gram space. It makes no certificate-size
claim near the optimum. General arithmetic SDP nonattainment,
odd-degree descent counterexamples, and the point-ideal perturbation
method have strong predecessors; the literature notes compare those
hypotheses explicitly. Priority remains unestablished.

The root also developed
[moment and Gram field consequences](strict-hessian-moment-arithmetic.md),
with additional field and facial-reduction observations supplied by
the range investigator. A fresh noncontributor reviewed the integrated
proof. Full positive definiteness of the Hessian Gram forces a unique
rank-one moment optimum. The optimizer field is exactly the least
field for maximal-rank optimal Grams and exposing matrices. When the
optimizer is irrational, a rational exposing step preserving all real
optimal Grams is impossible, although real singularity degree is one.
The primary comparisons credit Lasserre's exactness theorem and
Laplagne's conjugate-kernel restrictions. One wording correction
replaced “rational basis” with “basis over Q”; basis elements need
not themselves be rational. The root checked that correction.

The minimum SOS-length theorem now has a fresh full review. The root
read the flat-direction reduction and proper quadratic homotopy in
full and found no gap. The cyclic \(n+1\)-square representation is
therefore minimal even over real coefficients. The fresh review also
found a simple sextic counterexample to extending the conclusion
unchanged; it is preserved in the main note.

The root read the complete binomial-network degree bound. The gcd of
all rooted cofactors, rather than one grounded determinant, gives the
arithmetic index. Primitive stationary weights bound the non-Eulerian
case; classical interlace evaluations bound the odd Eulerian case.
The normal-form argument covers the minimum-size binomial exposing
strategy at an all-nonzero point. This closes that approach to
improving the cyclic degree without asserting a bound for all quartics.
The independent source audit checks the exact graph conventions.

The root has now also read the full compressed univariate construction
and its qualitative multiplier dependency, including all root
separation, inner-region, tail, and bit bounds. The previous record
that this read was pending is superseded. The monotone cube-root
construction received the same complete root read, including its
corrected precision accounting. A broader signed odd-root theorem
has a fresh review; its full root read is still pending.

Research continues on three consequential questions. One seeks
unbounded least coefficient fields for SOS certificates with short
rational convexity certificates. Another tests whether rational
denominators repair the explicit obstruction with small degree; a
quadratic radial multiplier candidate is under exact independent
review. A third revisits the zero-curvature limitation in the
shared-curvature fractional algorithm, using a different fiber
selection rather than assuming the old canonical witness survives.
These are active investigations, not conclusions imported into the
existing theorems.

### September 28: denominators and the zero-weight extension

The denominator investigation is now a verified milestone. An exact
positive definite rational Gram certifies
\((1+x^2+y^2+z^2)F\) for the ternary counterexample. Multiplying
once more gives rational-function squares with that common quadratic
denominator and no real poles. Degree two is minimal: an affine
common denominator would divide every numerator on its real
hyperplane and cancel, contradicting the polynomial SOS obstruction.
The author checked rational LDL factors; a fresh reviewer independently
reconstructed the polynomial identity and checked integer principal
minors using Bareiss elimination. The root read both proofs, without
duplicating those computations.

The reviewed [radial scaling theorem](rational-radial-exponent-obstruction.md)
uses \(f_t(X)=t^{-2}F(tX)\). For every fixed \(N\), all sufficiently
large integer \(t\) make \((1+\|X\|^2)^Nf_t\) fail rational SOS.
The root independently reconstructed the closed-cone argument and
read the complete assembled theorem and fresh review, including its
finite-menu extension. Closedness is proved by an integral coercivity
bound on Gram matrices; it is not inferred from a general PSD image.
The separate rational sphere corollary supplies existence of a finite
radial order for each instance. Thus the least order tends to infinity.
An adaptive quadratic denominator still has certificate length
\(O(\log t)\), and the Hessian at the minimizer is exactly constant.
No rate for radial order versus input height is proved. Reznick's
scaling-and-closedness method and earlier work on rational denominators
are explicitly credited.

The [nonnegative shared-curvature extension](nonnegative-shared-curvature-fractional.md)
now includes zero scenario weights in the full exact FPT algorithm.
A fixed negative-ray test separates two fiber selections. In its
absence, minimize the lifted residual and choose its least-norm
minimizer. In its presence, select a polyhedral minimum-norm point
and shift it along the fixed ray until the residual is nonpositive.
The latter case does not imply an unbounded original objective.
Both selections have closed polynomial charts and stay in the one
field of the retained optimizer and value.

The root read the full integrated proof and the new supporting
number-field QP algorithm. It independently checked the chart
identity, the two Hoffman bounds, the norm-regularization estimates,
the rational precision choices, and feasibility and boundedness
classification. The algorithm uses rational matrices and affine
data in one explicitly supplied dense real field; it does not cover
arbitrary separately encoded algebraic data with an uncontrolled
compositum. A fresh noncontributor reviewed this algorithm and its
primary exact rational-QP source. Existential active-set charts are
used for bounds, never enumerated as the algorithm. The root corrected
the supporting note's stale opening status after that review finished.

The signed odd-root circuit theorem has now received the full root
read, including its exposing identity, diagonal weights, approximation
precision, and strict Hessian Gram construction. The earlier pending
read record is superseded. Its compact convex-optimizer baseline is
a separate prior comparison and does not by itself yield the quartic
singleton or its strict certificate.

The root also read all of
[the ternary Lean source](../formal/TernarySOSDescent.lean).
The actual second derivative is identified with the certified
polynomial biform; a literal rational weighted-square identity gives
the global lower bound. The zero and stationarity theorems assume
\(a^5=2\). Field necessity, irrationality, dimension minimality,
and the global convexity predicate are not formalized in this file.
Two independent targeted compilations passed as recorded in its
verification note; the root did not run a redundant third compilation.

The next main candidate uses iterated quintic roots to force an
exponentially large least coefficient field for every SOS and PSD
Gram certificate while preserving polynomial-size input and a short
rational Hessian certificate. Its slice, field, and size arguments
are under fresh adversarial review. This is stronger than requiring
a large field only for maximal-rank Grams; it is not yet indexed as
a completed theorem.

### September 28: exponential certificate fields verified

The [quintic-tower theorem](exponential-least-sos-field.md) has now
passed a fresh complete review and a full root read. This supersedes
the pending status immediately above. In \(3k\) variables it gives
a rational quartic with Hessian at least \(I\), a polynomial-size
rational positive definite Hessian Gram, and minimum zero, for which
SOS and PSD polynomial Grams over a real field \(E\) exist exactly
when \(2^{1/5^k}\in E\).

The author used the reviewed signed odd-root construction to obtain
one exposing square and three residual squares per gate. A negative
square at the final gate is incompatible with the unique Gram on its
five-dimensional quadratic vanishing space, after specializing earlier
gates over \(E(2^{1/5^{k-1}})\). The root and fresh reviewer separately
checked why the last extension still has degree five whenever \(E\)
misses the final root. A determinant lower bound makes a sufficiently
large rational baseline scaling explicit, with polynomial coefficient
bit length. The PSD Gram obstruction is proved without assuming a
factorization over its coefficient field.

The root contributed a stronger coefficient-output consequence:
any finite algebraic list generating a field containing \(2^{1/5^k}\)
must include one element of degree at least \(5^k\). The splitting
field has an automorphism of order \(5^k\), whereas a compositum of
normal closures of fields of smaller individual degree cannot have
such an element in its Galois group. The fresh reviewer independently
reconstructed the proof and then checked the root's elementary
totally-real cyclotomic argument for the required automorphism.
The author also rechecked it. This rules out short separate dense
minimal-polynomial output, not sparse polynomials or succinct towers.
The [root audit](exponential-least-sos-field-root-audit.md) records
contributions and verification scope.

The [new prior comparison](exponential-sos-field-prior.md) identifies
Scheiderer's stronger predecessor excluding any one prescribed real
number field at fixed form degree. The root independently read that
primary construction and checked a useful distinction: its fixed
quartic norm examples already admit an SOS field of degree at most
24. Exclusion of a chosen field therefore does not establish
unbounded least coefficient-field degree. High-degree SDP optima
and joint spectrahedra encoding primal-dual optimality are also
explicitly credited. The root contributed that general-SDP caution.
The comparison does not establish priority, and its specific SPECTRA
examples were inspected by its author rather than reread by the root.

Research continues beyond this milestone. The main certificate
question is whether adapted rational denominators can stay small for
the exponential-field family. In parallel, a conditional degree-21
bound in five variables has a fully checked finite-scheme proof;
removing its proper-complete-intersection assumption requires a new
complex-base argument and is under fresh review. The effective radial
separator now also has a rational recursive construction, with its
asymptotic coefficient-height growth still being assessed.

Targeted root verification after integration: an inline
\(\texttt{python3 -}\) check passed the two indexes, this log, the
new tower root audit, and the QP supporting note: 379 local file
links, paired math delimiters, final newlines, trailing whitespace,
and control characters. The command
\(\texttt{git diff --check --}\) with those same five paths returned
no diagnostics. The Python check covers new files that Git does not
yet track. No project-wide verification or CI inspection was run.

### September 28: the five-variable maximum is twenty-one

The combined degree argument is now verified. A globally convex
rational sum of quadratic squares in five variables, with unique
zero \(p\) and positive definite Hessian there, has
\([\mathbb Q(p):\mathbb Q]\le21\). The cyclic family attains this
bound. Rational SOS remains an explicit hypothesis.

The first proof handles a proper complete intersection of five
quadrics. Its top-degree Frobenius pairing gives a quotient with a
totally isotropic linear subspace. Bézout in that subspace's span
forces every nonzero quotient of length at most nine to have length
eight. Real local factors preserve the odd residual parity, giving
a contradiction even for nonreduced schemes.

The second proof removes the proper-intersection limitation.
Twenty-three simple isolated points leave weighted degree at most
nine for a positive-dimensional complex base. The possible supports
are a short list of curves and surfaces. Each contains a reduced
local complete intersection with quadratically generated ideal sheaf.
Its generic residual has at most twenty-two points, and simple
isolated points of the original equations persist under perturbation.
The rational flat-direction reduction handles a real zero of the
leading quartic.

Two fresh reviewers separately checked global generation and the
blowup argument. The root independently read both full proofs,
reconstructed the case list and seven numerical contributions, and
directly checked Eklund–Jost–Peterson's residual theorem and the
classical minimal-degree classification. The
[root review](five-variable-degree-root-review.md) records the
details and limits. The root did not duplicate the retained
arithmetic checker runs. The canonical degree note and continuation
index now supersede the previous unresolved five-variable status.
The exact upper bound's publication priority remains unestablished.

### September 28: short certificates and quantitative radial obstruction

The tower's rational-denominator question is resolved for a refined
scaling of the same construction. The
[quadratic-denominator theorem](rational-tower-quadratic-denominator.md)
produces a polynomial-size rational-function SOS with common
denominator \(1+\|X\|^2\), of minimum degree two, and numerator
degree at most four. Its exponential least polynomial-SOS field and
individual-coefficient degree obstruction survive the rescaling.
The earlier prescribed scale is not claimed to suffice. This
supersedes the open-size statement in the preceding milestone.

The key identity adds the factors \(X_jR\) to the positive Gram
space of \((1+\|X\|^2)F_0\). A positive quadratic relation
\(G\) and the identity \(R=xr_2-yr_1\) give an exact zero
Gram with a positive definite new diagonal block. A rational Schur
bound and determinant bound then allow subtraction of
\((1+\|X\|^2)R^2\) after increasing the scale. The general
multiplier lemma does not require convexity. Its application to the
tower retains the original rational Hessian-Gram threshold.

The root contributed the use of a redundant full factor list and the
binary conversion of rational weights into actual rational squares.
The root independently reconstructed the full proof and quantitative
constants. A fresh reviewer separately checked them and ran an exact
stress example with a negative constant and nonzero linear term in
\(G\). The requested distinction between strong convexity and the
Hessian-Gram hypothesis has been corrected and rechecked. The root
read that final review and the correction without duplicating the
checker's execution.

The [auxiliary-certificate note](tower-rational-auxiliary-certificate.md)
and [shared-root encoding note](tower-sos-coefficient-encoding.md)
have also passed fresh review and a full root read. The root checked
the Taylor integration coefficients, the two affine ideal identities,
the solvability of the auxiliary equations, all degree bounds, and the
polynomial-size rational LDL and binary-square construction. The
Hessian Gram is explicitly the Gram of the final signed quartic.
These give matching polynomial-size shared root descriptions for
the otherwise large dense algebraic SOS output, and fixed-degree
rational certificates when root variables are retained. The underlying
Taylor SOS theorem is credited to Ahmadi and Parrilo. The independent
reviewer's distinct exact Hessian example produced 91 rational Taylor
squares; the root did not rerun it.

The separate scaled ternary family now has an effective
[rational separating-functional recursion](rational-radial-quantitative-separation.md)
and a reviewed [coefficient-height estimate](rational-radial-height-lower-bound.md).
They prove that its prescribed radial order grows at least as
\(\Omega(\log L/\log\log L)\), although its adapted quadratic
certificate has size \(O(L)\). Here \(L=\Theta(\log t)\)
is the binary input length for positive integer scale \(t\).
The root independently read both full proofs and checked the common
denominator, determinant estimates, recurrence
\(b_d\le64d^3b_{d-1}\), and inversion of the resulting double
exponential threshold. This is a hierarchy-order lower bound, not a
runtime lower bound or an obstruction to all exact certificates.

Publication priority remains qualified. Research continues on broader
multiplier mechanisms and on whether exact comparison of bounded
odd-root circuits can transfer arithmetic decision hardness to this
strictly convex quartic class. That decision reduction remains
provisional and is not part of the verified claims above.

Targeted root document verification after this integration passed:
an inline \(\texttt{python3 -}\) checked seven topic documents
(the two indexes, this log, the tower and five-variable root reviews,
the canonical degree note, and the QP supporting review), including
407 local file links, paired math delimiters, final newlines, trailing
whitespace, and control characters. The command
\(\texttt{git diff --check --}\) on those same seven paths produced
no diagnostics. No project-wide verification or CI inspection was run.

### September 28: exact unconstrained quartic decision encodes PosSLP

The provisional arithmetic direction above has produced a stronger
reviewed result. The
[unconstrained reduction](unconstrained-quartic-posslp-reduction.md)
maps an integer circuit to a rational quartic \(G\) with a supplied
full rational Hessian Gram at least the identity. Its unique global
minimum is negative exactly when the circuit output is positive, and
is strictly positive otherwise. There are no domain constraints and
no zero-optimum instances in the reduction.

The first component, developed by the span agent, simulates integer
arithmetic through analytic cubic-root macros near one. A product
macro vanishes identically on both axes, permitting relative error
bounds even for signals with different orders or cancelled leading
terms. Shared numerator and denominator signals prevent exponential
circuit duplication. A short squaring-root chain creates the required
tiny parameter, while polynomial-bit interval boxes validate the
signed-root theorem's actual input promises.

The root independently reconstructed this full argument and then
developed the stronger unconstrained extension. Append another tiny
signal \(u\), let \(v\) encode the comparison, and perturb the
zero quartic by \(-u^2v\). An explicit cubic Hessian Gram has
norm below eight; a polynomial-bit rational scaling preserves a full
Gram at least the identity. At the old zero \(p\),
\(G(p)=-u(p)^2v(p)\) and
\(\|\nabla G(p)\|^2=4u(p)^2v(p)^2+u(p)^4\).
The support bound
\(\min G\ge G(p)-\|\nabla G(p)\|^2/2\)
then proves the strictly positive branch. A fresh noncontributing
reviewer independently checked the circuit proof and the complete
new perturbation. The span author separately checked the extension.

The root also supplied the rational SOS consequence. In the positive
branch choose a rational Taylor center sufficiently close to the new
minimizer. Completing its linear Taylor part gives a rational SOS
with a positive definite polynomial Gram. This is an existence
argument, with no certificate-size bound. The fresh reviewer
independently reconstructed the full-factor span proof. Replacing
the original integer output \(V\) by \(1-V\) reverses the
answer and gives PosSLP-hardness of SOS or nonnegativity membership
within the supplied strict Hessian class. This polarity step is
explicit in both the theorem and prior comparison.

The [restricted root-circuit upper bound](posslp-certified-cubic-root-upper.md)
has meanwhile passed a separate fresh review and a full root read.
One common denominator makes every gate output integral; conjugate
growth and the field norm give a double exponential separation bound.
Polynomially many Newton operations reach that precision in a shared
rational arithmetic circuit. A shifted final comparison handles
equality, and denominator-positive pair arithmetic removes divisions.
Thus that particular certified cubic-root language is PosSLP-complete.
The separation and Newton method is explicitly credited to prior
work, including Allender and coauthors. This upper bound is not yet
a theorem for general convex quartics.

The root read the [primary comparison](posslp-convex-quartic-prior.md),
directly checked Tarasov--Vyalyi's reduction, and independently
verified the stated SOCP deduction by ordinary Slater duality.
General exact conic hardness is therefore established prior, not the
new claim. The root also read the dated *Hesse's Redemption* exact
decision discussion and its explicit bit-model approximation
Corollary 1.2. The restricted quartic construction gives a PosSLP
lower bound; it does not settle whether the general exact convex
quartic problem is in P, NP, or coNP. Publication priority remains
unestablished.

The fresh perturbation reviewer ran
\(\texttt{python3 research-20260927/check_posslp_unconstrained_tilt_review.py}\),
which passed exact Hessian, gradient, scalar-margin, and Taylor
identities. The separate root-circuit upper reviewer ran
\(\texttt{python research-20260927/check_posslp_upper_independent_review.py}\),
which passed exact recurrence and fraction identities and finite
constant checks. The root read both reviews without rerunning these
calculations. No finite checker substitutes for the universal
construction or asymptotic bit proof.

Two follow-ups are active: a matching upper bound for unconstrained
strongly convex quartics with an encoded curvature bound, and a
strictly feasible compact quartic body where every rational witness
has exponentially many denominator bits. Neither pending claim is
included in this milestone.

### September 28: strictly feasible quartics with long rational witnesses

The second pending claim above has passed its fresh independent review.
The [rational-witness construction](strict-convex-quartic-rational-witness-lower-bound.md)
uses \(k\) cubic roots to create a positive quantity at most
\(M^{-2^k}\), where \(M=1000^{k+3}\). The supplied boxes still
have only polynomial bit length. Its signed-root realization has
\(2k\) coordinates and a rational Hessian Gram; scaling and subtracting
the square of the tiny signal preserve a full Gram at least the identity.

The negative value at the old zero proves strict feasibility. Strong
convexity confines the entire zero sublevel set to a ball of radius
less than \(5\kappa M^{-2^k}\). The first center coordinate has a
cubic equation with \(O(k)\)-bit integers. A nonzero integer numerator
then forces every rational feasible first coordinate to have
\(\Omega(k2^k)\) denominator bits. All coordinates stay in
\((-1,5)\), and the sublevel set is compact and has nonempty interior.

The root read the complete final proof and independent review, and
reconstructed the interval bounds, fixed normalization, rank-one
Hessian perturbation, localization, and denominator inequality.
No correction was needed. The author's targeted command
\(\texttt{python research-20260927/check_strict_quartic_witness_lower_bound.py}\)
passed finite interval, scalar, and Gram checks; the root did not rerun it.
The universal claim rests on the proof and its reviewed realization
dependency, not those finite examples.

The root also read the [primary comparison](strict-convex-quartic-witness-prior.md).
Large rational witnesses for strictly feasible convex quadratic systems
are old; the new construction adds one globally strongly SOS-convex
quartic, bounded coordinates, compactness, and a supplied strict Hessian
certificate. General open semialgebraic sets already have exponential
rational-sampling bounds, consistent with this lower bound. Priority
for these restrictions is unestablished. The result bounds expanded
rational output and neither excludes succinct certificates nor proves
nonmembership in NP.

Research is continuing on the general exact-comparison upper bound and
its consequences for a fixed number of integer variables. Separate
investigations concern constrained continuous optimization and rational
Gram-certificate size; no conclusion from these investigations is
asserted in this entry.

### September 28: matching PosSLP upper bound and complete classification

The [general upper bound](strong-convex-quartic-posslp-upper.md)
has passed fresh independent review. The root read the full frozen
proof and review and independently checked its constants. The input
supplies a global rational curvature lower bound; an explicit positive
definite rational Hessian Gram is a polynomially verifiable sufficient
format. A polynomial-bit weak approximation enters a known Newton
neighborhood. Exact Newton steps stored in a shared arithmetic circuit
then reach doubly exponential precision after polynomially many steps.

One-block real quantifier elimination bounds a nonzero observable's
distance from zero. The proof uses uniqueness of the real critical
point and does not assume a finite complex critical locus. It never
executes the elimination. Shifted rational circuits handle strict and
weak inequalities and equality, and positive-denominator arithmetic
turns each comparison into one PosSLP instance. The construction of
that instance uses no PosSLP queries.

Together with the lower constructions, this proves PosSLP-completeness
of minimum and minimizer-coordinate order comparisons for the supplied
strict Hessian class. Equality has the upper bound only. The root's
[synthesis](exact-convex-quartic-complexity.md) distinguishes real SOS,
nonnegativity, positive definite rational polynomial Grams, and rational
SOS at a zero minimum. Real SOS and nonnegativity are complete; positive
definite rational Gram existence is complete; unrestricted rational
SOS membership currently has only the lower bound. Earlier rational
descent counterexamples prevent conflating those last two questions.

The root directly read Slot--Steurer--Wiedmer's Corollary 1.2 and
Basu's one-block quantifier-elimination theorem, used for the initial
point and algebraic gap. The root also directly read
Etessami--Stewart--Yannakakis, Appendix C, Corollary C.8 and its proof:
the same Newton/separation/circuit architecture, including a many-one
PosSLP reduction, is established prior for probabilistic polynomial
systems. The [focused prior audit](strong-convex-quartic-posslp-upper-prior.md)
has its own source review. The new restricted quartic lower bound is
the more substantial construction; the upper adapts established tools.
Publication priority for the combined classification remains unestablished.

The fresh upper reviewer ran
\(\texttt{python research-20260927/check_strong_convex_quartic_upper_review.py}\).
Exact Newton, rational elimination, final sign cases, and finite
constant margins passed. The root read the checker scope and review
without duplicating that run. The all-input theorem depends on the
universal proof and its cited quantitative theorems.

The upper construction also supplies a polynomial-size rational
arithmetic-circuit feasible point whenever the zero sublevel has
nonempty interior. The reviewed witness family above requires
superpolynomial expanded rational output for every such point.
These are compatible representation bounds, not an NP-membership
or NP-nonmembership result.

Separately, the root read both complete proofs and fresh reviews of
the [tower quadratic space](tower-quadratic-vanishing-space.md) and
[stationary quartic space](tower-quartic-stationary-space.md).
Base-five normal forms give \(\dim I_2=5k\); last-gate degree
separates all relation products. A twenty-dimensional first-derivative
interpolation map then proves \(J_3=0\) and
\(J_4=\operatorname{Sym}^2 I_2\) by induction. The root rechecked
the coefficient and gradient steps, including the polynomial identity
\(c_{y^2}+c_{xz}=0\). Exact local-block and finite-rank checks
were run by authors and reviewers, not rerun by the root. The resulting
rational SOS recognition algorithm is special to the supplied tower
zero and is documented as a structural companion, not a general solver
advance.

The complexity synthesis subsequently passed its separate composition
and scope review. The reviewer checked all four order polarities,
the equality-only upper bound, the rational-versus-real SOS boundary,
and the witness representations. One wording correction makes the
positive-Gram argument rescale the polynomial and its Hessian Gram
together. The root applied and independently rechecked that correction.
The general upper's polynomial-observable extension and its joint
comparison of two minima also passed fresh review; their proof uses
the supplied curvature bound, without assuming a full joint Hessian
Gram for a separable sum.

Targeted root document verification after this integration passed.
An inline \(\texttt{python3 -}\) checked the two indexes, this log,
the new complexity synthesis, and the root's unconstrained reduction:
434 local links, paired math delimiters, final newlines, trailing
whitespace, and control characters. The command
\(\texttt{git diff --check --}\) on those five paths produced no
diagnostics. No project-wide verification or CI inspection was run.

### September 28: quantitative size of interior polynomial Grams

The [interior-Gram lower bound](interior-gram-bit-lower-bound.md)
and [singly exponential upper bound](interior-gram-single-exponential-upper.md)
have passed separate fresh proof reviews. The root read the complete
proofs and reviews and reconstructed their matrix and encoding arguments.
For strictly positive quartics with a supplied full positive definite
rational Hessian Gram, an interior rational polynomial Gram of total
size \(\operatorname{poly}(L)2^{O(n)}\) always exists. Some
polynomial-size inputs need \(\Omega(n2^{n/2})\) denominator
bits in every such Gram. This matches exponential dependence on
dimension qualitatively, not its constants or polynomial factors.

For the lower bound, adding the square of the tiny root-chain signal
to the baseline zero quartic gives a positive minimum and a short
singular rational SOS Gram. Every positive definite Gram has a doubly
small Rayleigh quotient at the old zero. A cube-moment bound controls
the norms of all Grams, while a positive rational determinant cannot
be too small without large denominators. The root independently
checked the centered cube weights and the determinant-denominator
product. Compactness of ordinary Gram spectrahedra is established
prior, not the new claim. The fresh reviewer's command
\(\texttt{python research-20260927/check_interior_gram_bit_lower_bound_review.py}\)
passed exact moment and rational LDL checks in dimensions one through
four; the root did not rerun them.

For the upper bound, the nonempty strict set
\(f(q)-\|\nabla f(q)\|^2/(2\mu)>0\) has degree at most six.
Basu--Pollack--Roy's rational sampling theorem supplies a center of
singly exponential coordinate size. Taylor integration and completion
of the square give an explicit positive definite rational Gram with
the same form of total size bound. The author and fresh reviewer read
the primary sampling theorem; the root checked its application and
the displayed Gram formula. Rational LDL and binary splitting of
positive rational weights give an unweighted SOS of singly exponential
size as well. This is a certificate-size theorem, without a new
polynomial-time construction claim in the original input length.

The root read the [primary comparison](gram-bit-size-prior.md),
including corrected versions of general SOS bounds and recent exact
algorithms requiring a supplied ordinary Gram margin. A small strict
Hessian certificate supplies no such ordinary Gram margin. The lower
family nevertheless has a short singular SOS certificate, so no
all-PSD or general SOS-size lower bound follows. The
[remaining frontier](all-psd-gram-size-frontier.md) preserves failed
penalty-transfer arguments and the unresolved stronger question.
Priority for the restricted interior bounds remains unestablished.

### September 28: bounded rational optimizers and exact certificate height

The [circle construction](rational-convex-quartic-minimizer-height.md)
and its [Gram consequence](rational-circle-optimal-gram-height.md)
passed fresh independent reviews. The root read both complete proofs,
the reviews, and the primary-source comparison. The rational point
obtained by repeatedly squaring \((3+4i)/5\) has terminal coordinate
denominators exactly \(5^{2^k}\). The numerator congruences modulo
five prevent cancellation. A weighted quadratic exposer, rounded at
ordinary polynomial precision, realizes the point as the unique zero
of a short strongly SOS-convex quartic. The root rechecked the exposer
Hessian blocks, triangular Jacobian bound, rounding accuracy, and the
interface to the reviewed realization theorem.

The optimizer is rational and bounded; its expanded coordinates are
nevertheless long. Short rational square factors remain explicitly
available. For a maximal-rank optimal Gram, deleting its constant
row and column leaves a positive definite block. The kernel equation
then recovers all optimizer monomials by rational linear algebra.
Cramer's rule forces exponentially long entries in that Gram. The
rank-one optimal moment matrix and every nonzero PSD matrix exposing
the optimal Gram face also recover the long coordinate directly.
The root independently checked both denominator estimates, including
arbitrary positive scaling of the exposing matrix.

The [prior audit](rational-minimizer-height-prior.md) records Jiang's
explicit rational-height parameter, established convex witness bounds,
and earlier nonconvex rational optimizer examples. Homogenizing
Khachiyan's matrices already separates short feasible PSD points from
long full-rank points. The note therefore does not claim that generic
SDP distinction as new. Its additional restrictions are a bounded
rational unique optimizer and the associated certificates of one
strongly SOS-convex quartic. Publication priority is unestablished.

The author and fresh reviewer ran the expanded exact checker
\(\texttt{python research-20260927/check_rational_circle_minimizer_review.py}\).
It passed finite denominator and exposer checks and a complete
small-dimensional Hessian and optimal Gram calculation. The root read
the check scope and did not duplicate those runs. The universal claims
depend on the proofs, not these finite computations.

### September 28: nonpotential maps and unique active-set certificates

The [strongly monotone cubic theorem](strong-monotone-cubic-posslp-upper.md)
has passed its complete fresh review and final reconciliation. The root
read the full proof and review. Rational central ellipsoid cuts give a
polynomial-precision warm start; exact shared Newton circuits then use
normal equations for a nonsymmetric Jacobian. The symmetric Jacobian
lower bound controls inverse norms. A singleton real-projection gap
reduces exact degree-four observable comparisons, including zero, to
one PosSLP instance. The root rechecked the retained-ball constants and
the explicit positive definite Gram for a map with variable skew part.
The ellipsoid, algebraic-gap, and Newton tools are established prior.
Order predicates are complete through the gradient subclass; equality
has only the upper bound established here.

The [polyhedral unambiguous theorem](polyhedral-strong-quartic-unambiguous-upper.md)
also passed a full fresh review and two narrower reviews. The root
read the full proof and consolidated review. Guessing the full active
set gives a unique certificate. Its verifier reconstructs a strongly
convex affine restriction and checks all slacks exactly. A uniform
algebraic gap over the vertices of a rational tangent polytope reduces
the remaining first-order test to rational LP with a shared-circuit
objective. The GLS arithmetic-operation bound and a separate rational
vertex recovery avoid expanding long circuit values. The root
reconstructed the sign-transfer, recovery, and uniqueness arguments;
the primary GLS operation model was inspected by the fresh reviewers.
The consequence is \(\mathrm{UP}^{\mathrm{PosSLP}}\cap
\mathrm{coUP}^{\mathrm{PosSLP}}\), not a deterministic
polynomial algorithm for finding the active set. Finite exact checks
were run by the authors and reviewers, not rerun by the root.

### September 28: closing the fixed-integer search theorem

The [FPT candidate-list theorem](fixed-integer-strong-quartic-fpt.md)
passed a fresh proof review and a separate source review. The root
read the full proof, final all-optima amendment, and consolidated review.
A rational gradient error of at most \(\mu/4\) gives a strict
cut retaining every other no-worse integer point. Running the existing
integer-query feasibility algorithm with these always-rejecting cuts
is a valid empty-set oracle execution, so its FPT bound proves
termination. If any optimizer were absent from the recorded queries,
the identical execution would be valid for a hardcoded singleton
containing that optimizer and would wrongly report emptiness. This
also proves retention of all tied optimizers. A parity argument bounds
their number by \(2^k\).

The root independently reconstructed this singleton argument and the
radius and precision bounds. It read the primary Ari--Hildebrand
integer-query interface and the source audit of the underlying
Basu and Hildebrand--Goess results. The stronger all-optima statement
was proposed by the fresh reviewer and separately rechecked by the
author and root. The oracle-free candidate list has time and total
size \(2^{O(k\log(k+1))}L^C\), with absolute \(C\).
All pairwise fiber comparisons can then be prepared nonadaptively
using the reviewed continuous observable theorem. This is an FPT
algorithm relative to PosSLP for exact selection, not an ordinary
exact FPT algorithm. Del Pia's stronger-domain quadratic theorem is
credited and not subsumed.

The fresh reviewer ran
\(\texttt{python research-20260927/check_fixed_quartic_fpt_transcript_review.py}\),
passing 1,296 affine-line cases, tied optima, zero-gradient stops,
and a box of radius \(2^{100}\). The author separately strengthened
its checker to test retention of every optimizer. The root did not
repeat these finite runs; it checked their scope and the proof.

The root also read the full
[circle conditioning refinement](rational-circle-minimizer-local-conditioning.md)
and its fresh review. Shrinking radii make the residual derivative
blocks orthogonal, and linear weights give a fixed quadratic exposing
margin. The Hessian at the rational minimizer lies between \(2I\)
and \([8(k+1)^2+1]I\), although a terminal denominator is still
divisible by \(5^{2^k}\). The root rechecked the scaled residual
Jacobian and the Hessian formula. The claim is local, and does not
bound all condition measures or nearby higher derivatives.

The user then narrowed the work to finishing the current ideas and
directions, without opening new ones. The remaining work is review,
correction, and integration of the already started mixed-linear
extension, constraint-rank composition, sparse rational certificates,
quadratic graph extension, and rational quaternion sign reduction.
Further research directions are outside this closing scope.

### September 28: mixed linear constraints and rational-coordinate hardness

The [mixed-linear candidate theorem](mixed-linear-strong-quartic-candidate-list.md)
passed its fresh full proof review and an independent source check.
The root read the complete proof and review. At a feasible integer
query, a rational feasible primal approximation and a nonnegative
rational multiplier give a strong-convexity lower cut. The multiplier
is found by an ordinary convex quadratic residual minimization. The
root contributed and separately rechecked the identity bounding its
optimal error by the primal gradient times the primal displacement;
no multiplier norm is needed. A Farkas cut handles an empty fiber.
These are uniform polynomial-cost answers for the existing integer-query
framework, so its all-optima list remains ordinary FPT in the number
of integer variables, with arbitrary continuous dimension.

Fresh review requested explicit dispatch when \(k=0\); the author
added it, and the root checked that the only feasible integer block
is then the empty vector. The review also supplied a direct attainment
argument for the residual QP using its closed polyhedral image cone.
The root rechecked the compact objective sublevel in the image and
the existence of a nonnegative preimage. The independent checker
\(\texttt{python research-20260927/check_mixed_linear_candidate_review.py}\)
passed 4,240 residual certificates, 26,480 primal-dual inequalities,
22,240 integer cuts, 1,360 Farkas cuts, and candidate transcripts with
ties and large multipliers. The root did not duplicate these runs.
The result does not silently replace constrained exact selection by
the unconstrained PosSLP theorem.

The [quaternion compiler](quaternion-circuit-posslp-reduction.md)
has passed two fresh independent proof reviews. The root read its
complete proof and both review conclusions and reconstructed the
leading-term estimates, cancellation handling, scalar positivity,
and homogeneous numerator/denominator scaling. A polynomial number
of compact rational group operations generates a tiny positive signal
and encodes the sign of a nonzero integer arithmetic output. Exact
checks include signals with zero leading coefficient and nonzero
residual error; the proof does not assume exact cancellation at those
intermediate gates.

The root authored the separate
[unit-quaternion quartic realization](unit-quaternion-circuit-quartic-realization.md).
Its exposing identity is a positive current-gate square minus a
parent square; geometric weights dominate all negative parent terms,
including repeated parents and arbitrary reuse. Rounding only residual
coefficients preserves the exact zero. Quantitative residual and
Jacobian bounds then invoke the already reviewed full-Hessian realization
theorem. A fresh reviewer reconstructed the entire proof, ran
\(\texttt{python research-20260927/check_quaternion_realization_independent.py}\),
and reconciled the final status edits. The compiler author separately
read the realization. No substantive correction was required.

The [coordinate-comparison composition](rational-optimizer-posslp-coordinate-comparison.md)
now proves PosSLP-completeness even with a bounded rational unique
optimizer, known minimum zero, short rational square factors, and
a short strict Hessian certificate. The root independently checked
the composition but contributed to a dependency, so that check is
not described as a fresh review. The separate minimum-value tilt
does not preserve the rational-optimizer promise by any argument here.

The [fresh prior audit](quaternion-circuit-posslp-prior-review.md)
corrected one scope claim: Dawson--Nielsen already uses pointer sharing
in Solovay--Kitaev computation. The root read the correction and its
primary-source location and removed shared representation as an alleged
novel distinction. Compact rational coordinate sign, compressed identity,
and quantum tensor thresholds have different predicates and input
models. No inspected equivalent establishes the full claimed restricted
theorem, but priority remains unestablished. Full Ben-Or--Cleve proof
access was unavailable and is explicitly recorded.

### September 28: final constraint-rank composition

The [constraint-rank algorithm](constraint-rank-strong-monotone-oracle.md)
and its [mixed-integer composition](mixed-quartic-integer-constraint-rank-oracle.md)
passed fresh proof reviews, source checks, and final reconciliation.
The root read both complete proofs and consolidated reviews. It
reconstructed the violator-space locality argument, the bound on every
minimal basis, and the exact small-subproblem primitive. The rank counts
all constraint normals. It is not a bound on just the support eventually
selected at the solution. The primary Clarkson-type algorithm, including
the bit cost of sampling with weights, is credited explicitly.

For two continuous fibers, a product problem has the summed strongly
convex objective and constraint rank twice that of the original continuous
constraint matrix. The difference of the two objectives is an admissible
observable. This permits exact comparisons of the ordinary FPT candidate
list. A lexicographic tournament gives the smallest optimal integer block;
one final fiber solve returns an exact implicit continuous optimizer.
Conditional expected-time bounds compose to
\(F(k,\operatorname{rank}B)L^C\), with absolute \(C\).
No full positive definite joint Hessian Gram is needed for the separable
product objective. The proof does not claim deterministic computation,
removal of the PosSLP oracle, or short expanded algebraic output.

The author and fresh reviewer ran
`python research-20260927/check_constraint_rank_violator.py`, checking
128 exact affine VI instances, 702 locality cases, and all minimal bases
in 11 examples. These finite checks do not implement the randomized
sampling algorithm. The final composition required a proof and edge-case
audit, not another run of the same checkers; the root did not rerun them.

### September 28: closing sparse certificates and the quadratic graph

The [rational block lift](rational-block-sos-splitting-obstruction.md)
and [strong-convexity supplement](strongly-sos-convex-block-splitting-obstruction.md)
passed fresh reviews. The root read the proofs, reviews, and primary
comparison. It rechecked the exact joint SOS identity, the zero-shift
field obstruction, and the positive-family denominator bound. The
fixed strong-convexity padding lemma now explicitly counts a supplied
baseline rational SOS certificate in its input length. The concrete
application already supplies that certificate; the root independently
checked the correction. The separated-Gram lower bound concerns two
specified local Grams, not every unrestricted Gram. Existing sparse
real SOS and rational descent results are distinguished in the audit.

The already proposed [quadratic-graph realization](quadratic-graph-quartic-realization.md)
is also complete. The root contributed a quantitative construction
outline and then reconstructed the full proof, so a fresh review was
required and obtained. A separate reviewer checked the approximation
source and exact rational recovery. The lift keeps its exact zero at
the unknown optimizer's quadratic graph even when its coefficients use
an approximate optimizer. Uniform residual, Jacobian, and exposing
quadratic bounds yield a strict full Hessian Gram. Approximating that
Gram and projecting onto its exact coefficient equations supplies a
short rational certificate. The two precision choices are acyclic.

The graph reviewer ran
`python research-20260927/check_quadratic_graph_quartic_realization_review.py`.
Exact one- and two-variable examples passed the Taylor graph identity,
zero-gradient identity, and residual determinant identity. A one-variable
case also passed the formal-center degree, Hessian identity, coefficient
projection, and Frobenius contraction checks. The root read the checker
scope and full review rather than duplicating the run. The final capped
approximation tolerance and corrected approximation-point notation were
checked by the reviewer and root. They do not alter the theorem.

Applying the graph lift to the existing tower completes the polynomial-size
strongly SOS-convex growing-field block construction. The least separated
field is \(\mathbb Q(2^{1/5^k})\), while the unrestricted rational
SOS stays short. With \(\Theta(k^2)\) total variables, the individual
degree lower bound is exponential in the square root of that count.
Every positive semidefinite joint full Hessian Gram must be singular
because the blocks are additively separated; global strong convexity and a short rational
Hessian SOS certificate still hold.

The [closing record](closing-research-results.md) and both entry indices
now state the user's finish-only scope. All mathematical lanes in that
scope are closed; open questions and qualified priority assessments are
preserved without opening further directions. Fresh reviews are agent
reviews, not journal peer review. No practical speedup or publication
readiness is inferred from them.

A fresh closing-summary audit caught two missing qualifiers: rational
matrix output in the circle height consequence, and positive
semidefiniteness in the separated Hessian-Gram singularity statement.
The root corrected the summary and both block-construction notes.
The detailed mathematical reviews already used the PSD qualification.
The root independently rechecked why it is necessary: for
\(x^4+x^2+y^4+y^2\), in the basis
\((a,b,xa,xb,ya,yb)\), the diagonal entries
\((2,2,12,0,0,12)\) give its Hessian biform. Adding symmetric
entries \(Q_{xa,yb}=1\) and \(Q_{xb,ya}=-1\) changes no
polynomial coefficient but gives determinant \(-572\), so an
indefinite Gram can be nonsingular. A PSD Gram cannot use such a
coupling when the corresponding diagonal is zero. Thus the correction
preserves the intended SOS theorem and excludes a false reading about
arbitrary symmetric Grams.

The root also ran an inline `python3 - <<'PY'` SymPy calculation for
this correction. It verified the exact Hessian polynomial identity
and determinant \(-572\). This checks the displayed counterexample,
not a new general theorem. No previously passed algorithm checker was
rerun, and no project-wide verification or CI inspection was performed.

### Final targeted documentation verification

The fresh closing scope audit passed after rereading both qualifier
corrections and recording the final hashes of the closing record and
the two amended construction notes. The root read that review in full.

The root ran an inline `python3 - <<'PY'` check on ten explicit files:
the root README, the continuation README, this log, the exact-quartic
synthesis, the quaternion prior and realization, the closing record,
the quadratic-graph realization, the strongly SOS-convex block note,
and the closing scope review. It passed 529 local link checks, paired
inline and display math delimiters, final newlines, trailing whitespace,
control characters, and two known stray-patch-character patterns.
This includes the new untracked Markdown files.

The root also ran the following targeted command, which passed without
output. It checks tracked differences; the inline check above separately
covers untracked files.

```text
git diff --check -- README.md research-20260927/README.md research-20260927/root-research-log.md research-20260927/exact-convex-quartic-complexity.md research-20260927/quaternion-circuit-posslp-prior.md research-20260927/unit-quaternion-circuit-quartic-realization.md research-20260927/closing-research-results.md research-20260927/quadratic-graph-quartic-realization.md research-20260927/strongly-sos-convex-block-splitting-obstruction.md research-20260927/closing-research-scope-review.md
```

The same targeted document checks were repeated after adding this
verification record. These checks establish document consistency,
not mathematical correctness. Proof and source reviews and the distinct
exact computations are recorded above. Work stops at the user's current
scope; no additional direction has been opened.
