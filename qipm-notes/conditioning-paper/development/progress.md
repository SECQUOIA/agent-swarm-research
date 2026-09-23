# Development and review record

This file records the coordinating author's stage decisions. Review reports are
internal working records, not part of the journal manuscript.

## Process

Each authoring stage is completed by one subagent before five independent
reviewers examine it. The coordinating author assesses findings. A separate
agent fixes every accepted issue. Any accepted major issue triggers another
five-reviewer round; accepted minor issues are corrected before the next stage.
The full manuscript receives the same process after assembly.

## Stages

1. Repository inventory, scope and literature audit — complete after two
   five-reviewer rounds and all accepted corrections.
2. General geometric theory, equal-gap comparison and perturbation transfer —
   complete after five reviews and all accepted minor corrections.
3. Conditioning classifications, exact examples and LP endpoint limits —
   complete after five reviews and all accepted minor corrections.
4. Spectral consequences, right-hand sides, Krylov bounds and formulation scope —
   complete after five reviews and all accepted minor corrections.
5. Reproducible numerical evidence and complete submission-facing exposition —
   authoring in progress.
6. Whole-manuscript review, corrections, compilation and final verification.

## Stage 1

Author: `stage1_scope_author`. Reviewers: `reviewer1` through `reviewer5`.
The author produced the scope/literature audit, curated bibliography and
buildable scaffold. Initial build passed. No original manuscript files changed.

The scope includes relevant newer repository developments. It excludes full
cone-lift topology, central-path distance, and quantum oracle lower-bound
packages because they concern different quantities; the manuscript will explain
the relevant boundaries. The Xiong--Freund level-set/Hessian connection is a
substantive antecedent. The degenerate LP Hessian limit is attributed to
classical endpoint theory.

### First review assessment

All five reports are in `development/reviews/stage1-r1.md` through `stage1-r5.md`.
The coordinating author accepts every reported issue. Four reviewers found no
major issue. Reviewer 5 identified a major omission: Peña (2002) directly studies
central-path matrix conditioning and objective-value parameterization. It and
the connected Peña (2001) and Renegar (1996) sources require an explicit source
comparison before originality is settled. This is a major literature-audit
issue; it does not establish that the candidate theorem is already known.

Accepted minor fixes: state the common attained gap interval; distinguish the
fixed face tangent from the finite-gap weak eigenspace; cover gap-dependent
barrier families with uniformly bounded parameters; distinguish fixed coordinate
changes from gap-dependent preconditioning; require a complete numerical
reproduction manifest and compactness/relative-interior audit; correct the
oscillatory example's rescaled-Hessian notation; and add Nesterov--Todd's
Riemannian-geometry comparator. The distinct correction agent `stage1_fixer`
has corrected the scope and bibliography; see `stage1-corrections.md` for the
finding-to-change map and source-access record. The mandatory second round of
five reviews is now complete. Stage 2 has not started.

### Second review assessment

All five repeat reviews found no major issues. Reviewers 1, 2, 3 and 5 found
no remaining minor issue. Reviewer 4 requested one accepted minor addition:
screen the local Alizadeh--Haeberly--Overton SDP spectral-clustering source
referenced by Peña before assigning originality to the fractional example.
The correction agent is addressing that source comparison. No additional
five-reviewer round is required for this minor correction.

The coordinating author checked the completed source comparison and accepts it.
Stage 1 is complete. Stage 2 is assigned to `stage2_geometry_author` and covers
the general geometric theorem, its direct approximate-centrality extension,
same-gap Hessian comparison and radial-width bounds. Examples and solver
consequences remain for the later stages.

## Mathematical leads requiring independent verification

The coordinating author proposed the following developments during inventory.
They are not treated as established until authored and independently reviewed.

### Difference-body comparison

The sharp containment constant has a short direct proof. Restrict F to a line
through x, normalize its second derivative at 0 to one, and choose direction
with phi'(0)>=0. Self-concordance gives phi''(t)>=(1+t)^-2, hence
phi'(t)>=t/(1+t). Semiboundedness to a feasible point at local distance R
gives phi'(t)(R-t)<=nu. If R>sqrt(nu), choose t=sqrt(nu), obtaining
R<=t+nu(1+t)/t=nu+2sqrt(nu). Otherwise the bound is immediate. This proof
can replace reliance on an unavailable sharp-constant source, while crediting
the standard theorem. Boundary points follow by limits.

For an exact center at gap g, let K_g=L(g)-L(g), and let E_F be its unit
tangent Dikin ellipsoid. Choosing the objective-decreasing sign in Dikin
containment gives E_F contained in K_g. Asymmetric containment gives K_g
contained in 2 C_F E_F. At an equal gap this should imply
H_G <= 4 C_G^2 H_F and H_F <= 4 C_F^2 H_G.

If P contains a relative Euclidean ball of radius r and has objective range
Delta, a homothetic copy about an optimum gives
2 r g/Delta times the unit ball contained in K_g. Consequently
lambda_max(H_F) <= (C_F Delta/(r g))^2. Together with the chord law this
would yield the same accuracy exponent for every fixed barrier, beyond the
canonical-barrier upper bound in the original paper.

### Approximate centrality

Dikin support gives ||c_V||_(H_center^-1) <= g_center. A point at local
distance t<1 therefore has gap within factors 1-t and 1+t of the center gap.
Convex dilation gives D(a g)<=a D(g) for a>=1. Combine this with Hessian
comparison to state geometry at the observed iterate gap.

A stronger direct route avoids the center-distance transfer entirely. Suppose
rho=||grad F(y)+c/mu||_(H_y^-1)<1. Along a unit-H_y direction to any point
of L(g(y)), the univariate restriction has phi'(0)>=-rho. Consequently
phi'(t)>=t/(1+t)-rho. Set u=(1-rho)t-rho>0; semiboundedness gives
R<=t+nu/phi'(t)=[u+rho+nu+nu/u]/(1-rho).
Choosing u=sqrt(nu) gives
C(nu,rho)=(nu+2sqrt(nu)+rho)/(1-rho).
If the line endpoint occurs before the chosen t, the same upper bound is
immediate. Thus L(g(y)) is contained in y+C(nu,rho)E_y, giving the same
difference-body and two-sided conditioning theorem at the observed gap for
every residual rho<1. This is a candidate direct approximate-containment
refinement requiring full proof review, including the relative-gradient norm.

### General barrier LP spectra and sharp alignment

An equal-gap Loewner comparison with the log barrier should give f bounded
eigenvalues and d-f eigenvalues of order g^-2, where f is optimal-face
dimension. A lower bound against the fixed normal-to-face projector then
gives an O(g) weak-projector angle and O(g) weak fraction of the exact Newton
right-hand side c_V. The log barrier's bounded off-diagonal perturbation
improves this to O(g^2).

A possible sharp O(g) example is P=[-1,1] x [0,1], objective y, and
F=4[-log(1-x^2)-log(y)-log(1-y)+epsilon x sin(log y)], epsilon=1/100.
Relative to the unperturbed Hessian H_0, the perturbation Hessian has norm
at most 3 epsilon, its third differential at most 7 epsilon ||h||_H0^3,
and gradient dual norm at most 2 epsilon. These estimates should certify
self-concordance after scaling by 4 and barrier parameter at most 20.
At y_k=exp(-2 pi k), the center has x=0 and the Hessian divided by 4 is
[[2,epsilon/y],[epsilon/y,y^-2+(1-y)^-2]]. The weak RHS component is
asymptotic to epsilon y. All constants and global domain properties need proof.

### Exact fractional SDP spectrum

For min X_22 subject to tr X=1 and X_33=X_12, symmetry makes the log-det
center X=[[a,b,0],[b,g,0],[0,0,b]]. Set
b=(-g+sqrt(3g-2g^2))/3, a=1-g-b, q=ag-b^2, and
mu=q/(1-b-2g). Then g~3mu/2, b~sqrt(mu/2), q~mu.

The X_13,X_23 Hessian block, in the Frobenius metric, is A^-1/b for
A=[[a,b],[b,g]], giving eigenvalues asymptotic to sqrt(2)mu^-1/2 and
sqrt(2)mu^-3/2. In b,g coordinates the tangent Gram matrix is
[[4,1],[1,2]], while the Hessian entries are
H_bb=b^-2+q_b^2/q^2+2/q,
H_bg=q_b q_g/q^2+1/q,
H_gg=q_g^2/q^2+2/q,
with q_b=-g-2b and q_g=1-b-2g.
The generalized eigenvalues should be asymptotic to mu^-1 and
(4/7)mu^-2. Thus the condition constant should be 2sqrt(2)/7 in the
mu^-3/2 law. This must be checked analytically rather than inferred from data.

An independent standard-library Decimal check at 70 digits gives the scaled
ordered eigenvalues at g=1e-12 as approximately
(1.41421539949, 1.00000101037, 1.41421458300, 0.571428901344), with
kappa*mu^(3/2)=0.404060726215. This supports the proposed constants but
is not their proof. The qipm environment has numpy/scipy/matplotlib; it does
not have mpmath or sympy. Use Decimal and analytic formulas for high precision
rather than adding dependencies.

### Singularity degree does not determine the exponent

A concrete candidate counterexample sharpens the facial-reduction boundary.
Add X_13=X_23=0 to the fractional 3-by-3 SDP above. The feasible matrices
become [[a,b,0],[b,g,0],[0,0,b]], a+b+g=1. Their sublevel diameter is
Theta(sqrt(g)): b<=sqrt(g) gives the upper bound and a positive-definite
choice b~sqrt(g) attains it. The optimality system still appears to have
singularity degree two. Any one-step PSD exposing combination with zero
11 entry must have zero first row, forcing the coefficient of X_33-X_12
and of X_13 to vanish; the remaining zero 33 entry then forces the X_23
coefficient to vanish. Only a multiple of E_22 remains, so two steps are
needed. If verified, the paired examples prove that singularity degree two
permits at least two conditioning exponents (1 and 3/2) and that degree alone
cannot supply the exact sublevel-diameter law. This is a concrete resolution
of the sufficiency question, without claiming a general facial classification.

### Solver and reproduction safeguards

The original clustered-CG proof bounds relative energy-norm error in exact
arithmetic, not the recursively updated Euclidean residual used by old scripts.
Its original 40-variable experiment reports an eight-step recursive residual
below 1e-8 while the true residual is about 1e-4 at the deepest float64 point.
Any retained computation must recompute the true residual and keep the
precision limitation visible. Do not copy the unbundled 80-bit experiment.

For the oscillatory barrier, at the proposed subsequence, H^-1 c has a weak
component of order g and a strong component of order g^2. Thus discarding weak
modes can give relative residual O(g) while losing asymptotically all Euclidean
solution mass. This may provide a useful explicit contract counterexample in
the same construction; verify before use. Use 'relative component norm' for
projector norm ratios and distinguish squared probability mass.

Do not turn a generic quantum QLS condition lower bound into a fixed-instance
accuracy lower bound: the cited two-point worst-case construction has a
dimension requirement that need not hold on a fixed-dimensional central tail.
The geometry paper should keep oracle normalization, supplied projector/RHS,
output and actual Newton RHS qualifications visible, and avoid claiming an
end-to-end runtime separation.

## Stage 2 review assessment

The author completed the three mathematical sections and a clean 10-page build.
All five independent reviews found no major issue. The coordinating author
accepts three minor corrections: distinct symbols for the gap and barrier
parameterizations (reviewer 3); standalone wording for the directed-exit
construction (reviewer 2); and sharper minimax width bounds (reviewer 5).
The last improvement follows by applying the lower Rayleigh bound in the
minimum-over-dimension formula and the upper bound in the maximum-over-codimension
formula. Root checked both directions independently. The distinct correction
agent is implementing all three; no repeat review is required for minor-only
findings.

### Additional literature check for Stage 3

The fractional SDP's optimality constraints are the n=3 case of Sturm (2000),
Example 2, printed p.1244, with a trace normalization. Root checked the original
PDF equation, not only OCR. Drusvyatskiy--Wolkowicz (2017), Theorem 4.5.1 and
Example 4.5.2, printed pp.116--117, reproduce the error bound and construction;
Section 4.7 attributes both to Sturm. The preprint example numbering differs
(Example 4.5.1). The manuscript must explicitly credit this geometry and not
present its fractional contact exponent as a new SDP construction. The new
work to assess is the exact reduced log-Hessian spectrum, transfer to all
barriers, and the paired equal-singularity-degree conditioning comparison.

The Stage 2 correction agent completed all accepted minor fixes. Root checked
the hatted gap-path definitions and reciprocal minimax proof. Stage 2 is
complete; Stage 3 can now begin.

### Numerical instance screening (root, preparation only)

Using the existing standard-form cache and SciPy/HiGHS, afiro is 9-by-18,
sc50b is 15-by-29, and adlittle is 55-by-136, all full row rank and with
positive Phase-I margins (1, 1, and about 0.187, respectively). Tests of
nonnegative recession rays find afiro/sc50b bounded; adlittle is unbounded
but has no nonzero recession ray of nonpositive objective. Thus adlittle
should use compact-sublevel localization, not the global compact theorem.
These are numerical screening results, not exact certificates.

A portable certificate strategy for Stage 5: find y and eta>=0 such that
A^T y+eta c is componentwise strictly positive. This proves boundedness
of every fixed upper objective sublevel from the linear identity; eta=0
certifies the entire feasible set. Generate with linear programming with
margin >=1, then verify the stored certificate against the exact decimal
input using standard-library Decimal/Fraction arithmetic. A strict point
can similarly be reconstructed with rational Gaussian elimination after
fixing the Phase-I free coordinates to rational values, and checked exactly.
Bundle small derived arrays and certificates with source hashes/provenance;
avoid dependence on parent-repository imports in final reproduction scripts.

### Current-literature scope screen

Root inspected Monteiro--da Silva (2026), arXiv:2606.04348v1, primary HTML
https://arxiv.org/html/2606.04348v1, especially Definition 4.1 and Remark 11.1.
The authors explicitly distinguish differential self-concordance from a finite
global barrier-gradient parameter for inverse-power perturbations. This work
therefore does not contradict or subsume the present fixed-parameter theorem.
No result of that preprint is needed for our proofs. A simple independently
verifiable rectangle example may clarify the boundary: add eta/y to its
logarithmic barrier. Differential self-concordance persists, but the gradient
ratio diverges as eta/(2y) and conditioning grows as eta*g^-3. The Stage 3
author has been asked to consider this concise illustration, with neutral
attribution and no claim about the preprint's other results.

For the oscillatory Stage 4 barrier, the first centrality equation is
2x/(1-x^2)+epsilon*sin(log y)=0. It has a unique solution in (-1,1),
which oscillates between distinct values as y tends to zero; F_y remains
negative for all sufficiently small y. Thus the same fully verified example
also shows that a general finite-parameter barrier path need not have a single
endpoint on a positive-dimensional optimal face. This is an optional short
observation, not needed for the all-barrier theorem (which never assumes such
endpoint convergence). Keep it only if it helps clarify why classical log-path
endpoint convergence cannot silently be generalized to all barriers.

### Elementary projector proof for Stage 4

The canonical O(g^2) weak-subspace angle can be shown directly without a
resolvent calculation. Write H_log=H_N+H_B, with ker(H_N)=T, its restriction
to T-perp bounded below by a*g^-2, and ||H_B||=O(1). If Q spans the weak
eigenspace and H_log Q=Q Lambda, then H_N Q=Q Lambda-H_B Q has bounded
operator norm. Applying the inverse of H_N on T-perp yields
||P_(T-perp) Q||=O(g^2). For a general barrier, the equal-gap lower
quadratic-form bound H_F>=a*g^-2 P_(T-perp), together with bounded weak
eigenvalues, instead yields O(g). Equal subspace dimensions convert this
sine-angle bound to the difference of orthogonal projectors. Since c_V is
orthogonal to T, it immediately controls the weak component of the exact
Newton RHS. This is a lead for the author to verify, not a substitute for
independent review.

## Stage 3 authoring and review

The author completed classifications, LP endpoint constants, and paired SDP
examples with exact spectral asymptotics. Root read all three sections and
checked the principal calculations. The author corrected two TeX typos and
two wording points before completion. The five independent reviewers have
now been dispatched. The optional inverse-power example was not added in
this stage; it may fit the later scope discussion if retained.

Root additionally screened the Wei--Wolkowicz local original PDF with rendered
pages/OCR (pages 1, 2, 7, 8, 9 and 18), overcoming its font-encoding problem.
Section 3 studies spectral diagnostics of complementarity gaps using the
primal/dual eigenvalues and their ratios; the conclusion compares those
measures, Renegar conditioning and iteration counts empirically. This is
relevant established context, but the inspected portions do not state an
exact reduced-Hessian four-eigenvalue calculation for our trace-normalized
example. The manuscript's existing broad citation is supported, and the
narrow qualified priority statement remains subject to the independent
review. Temporary rendered/OCR files are outside the deliverable folder.

### Stage 3 review assessment

All five reviewers found no major issue. Root accepts their common minor
terminology correction: μ is the central-path parameter, while ν is the
barrier parameter. Root also accepts reviewer 3's minor literature addition:
Sremac--Woerdeman--Wolkowicz, Error Bounds and Singularity Degree in
Semidefinite Programming, studies spectra of primal/dual iterates on external
paths. The correction must distinguish those paths and matrices accurately
from the reduced Hessian here. This is a missing comparator, not evidence
that the explicit spectral constants or paired-diameter result is false or
already stated. The distinct fixer is addressing both accepted findings;
minor-only findings do not require a repeat review round.

The distinct fixer completed both accepted Stage 3 corrections, verified the
published 2021 Sremac--Woerdeman--Wolkowicz source, and recorded version-specific
locators. Root checked the new comparison and terminology. Stage 3 is complete.
Stage 4 now begins: LP spectra across barriers, Newton RHS alignment and its
sharpness, clustered solves, and precise formulation/access boundaries.

### Original CG toy has additional symmetry

Root read scripts/two_cluster_cg_check.py. Its 40-variable simplex uses only
two positive objective coordinates and 38 zero coordinates. On the exact
log path the 38 inactive coordinates coincide, so the 37-dimensional face
tangent is an exactly repeated eigenvalue; only two other eigenvalues remain.
Consequently exact-arithmetic CG terminates in at most three iterations.
The reported 3--8 float64 counts principally illustrate numerical loss, not
a demanding test of the general two-interval polynomial estimate. If this
toy is retained in Stage 5, explain that symmetry. A second deterministic
rotated spectrum with many distinct values inside each fixed-ratio cluster
would test the interval statement more informatively, with energy error and
recomputed true residual both reported. Do not present the synthetic matrix
as a Newton Hessian without an explicit realization.

### Benchmark transformation provenance

Root reproduced each cached .std array exactly, without writing to the cache,
by reading its MPS with HiGHS 1.15.1, calling presolve with default options,
and applying the repository's standard_form._lp_to_standard_form conversion.
The equality/bound conversion is in parent standard_form.py; the original
pipeline is parent transform.py. Dimensions (MPS rows, columns) -> presolved
rows, columns -> standard-form rows, columns:

- afiro: (27,32) -> (7,10) -> (9,18).
- sc50b: (50,48) -> (15,15) -> (15,29).
- adlittle: (56,97) -> (53,95) -> (55,136).

All c,b,A,objective-offset arrays match their cached .std values exactly.
The .std files are NPZ archives, not text. Stage 5 must describe these as
presolved standard-form representations and specify that the fixed metric
is Euclidean in those coordinates. Do not equate their Hessian conditioning
with the original unreduced MPS representation. A frozen data bundle can
serve as the exact definition of the tested instances, with original MPS and
cached-array hashes in the manifest; optional data preparation should not
require the parent repository for ordinary reproduction.

### Stable numerical quantities for Stage 5

For an LP log Hessian, the factor B=Diag(1/x)W is available explicitly.
Its singular values squared give the Hessian eigenvalues without forming
B^T B, reducing loss of the small spectral edge. A QR or SVD factorization
also provides a more reliable Newton solve/decrement than a raw normal
matrix at the deepest float64 points. Record the actual unscaled decrement
||W^T(-1/x+c/mu)||_(H^-1), not the decrement of mu*F+c, whose extra
sqrt(mu) factor can produce false centering acceptance. Use positivity,
scaled equality residuals, and an objective-gap accuracy cutoff. Retain
failed or uncertified tail points in the machine-readable results.
Frozen floating-point data can be interpreted as exact binary rationals
for simple strict-point and compactness-certificate checks via Fraction;
publication plots still represent finite-precision numerical paths.

## Stage 4 author completion and additional source screening

The author completed all three sections and independent numerical formula
checks. Root read the sections and requested clarification of the optimal-face
tangent proof, Newton forcing notation, ambient versus reduced Hessians, and
objective sensitivity. The author resolved these before declaring completion.
Five independent reviewers were dispatched after completion.

Root's further primary-source search found Bolte--Pauwels, *Curiosities and
counterexamples in smooth convex optimization*, Mathematical Programming 195,
553--603 (2022), DOI 10.1007/s10107-021-01707-1. The publisher metadata and the
author/institution manuscript were read:
https://www.tse-fr.eu/sites/default/files/TSE/documents/doc/wp/2020/wp_tse_1080.pdf
Section 5.8, Corollary 11, printed p.43, gives a nonconvergent central path
for a Legendre function continuous on a closed square. That is a direct
antecedent to the qualitative nonconvergence observation. Its stated function
is finite on the boundary and is not a diverging finite-parameter barrier of
the class defined here. Add a precise short comparison beside our observation;
do not claim the first nonconvergent central path. Our global finite-parameter
certification and sharp eigenspace/solution-error calculation are the specific
additional facts established in the present example. This is an accepted root
minor citation addition, to be handled by the distinct Stage 4 fixer alongside
the reviewers' accepted findings.

An additional search found Vladu, *Interior Point Methods with a Gradient
Oracle*, arXiv:2304.04550, STOC 2023. The primary abstract concerns maintaining
a Hessian preconditioner using first-order information. It does not establish
the equal-gap cross-barrier theorem or invalidate the manuscript's coordinate
scope. No detailed theorem is cited on the strength of its abstract.

### Stage 4 review assessment

All five reviewers found no major issue. Root accepts the shared R1/R3/R5
clarification that the off-path extension states the eigenvalue scales and
general O(g) projector rate explicitly. Root also accepts R5's request to
write the restricted approximate solution's range condition and full residual
assumption explicitly. Both remove ambiguity from already valid arguments.
Together with the root's Bolte--Pauwels comparator above, these are the three
distinct accepted minor corrections. The distinct agent `stage1_fixer` is
addressing all of them. A repeat five-reviewer round is not required because
there was no accepted major issue. Stage 5 starts only after these corrections
are complete and checked.

The distinct fixer completed all three corrections and checked the primary
Bolte--Pauwels source and journal metadata. Root checked the changed text and
clean build log. Stage 4 is complete. Stage 5 is assigned to
`stage5_numerics_author`, covering the portable reproduction package and the
complete submission-facing introduction, abstract, numerical evidence,
discussion and assembly. The numerical and source-provenance obligations
above were included explicitly in the assignment.

### Root checks during Stage 5 authoring

Root reread the setup, direct containment proofs, gap parameterization,
difference-body and diameter bounds, both minimax width proofs, classifications,
LP limit and the SDP geometry/facial-reduction calculation. No new substantive
issue was found. A minor explanatory bridge was sent to the author: the
rectangle's standard-form slack embedding (1+x,1-x,y,1-y) multiplies its
tangent metric by two and hence preserves the sharp eigenspace-angle example.

After the numerical author generated frozen benchmark data, root independently
parsed their binary-rational interpretation and checked the strict-point and
near-optimal primal equalities, coordinate positivity, dual feasibility,
positive compactness vectors, and objective brackets with standard-library
Fraction arithmetic. All certificates pass without tolerance. The exact
objective-bracket widths are approximately 8.1597e-12 (afiro), 9.3974e-12
(sc50b), and 4.4338e-7 (adlittle). The first two compactness certificates have
eta=0; the third has eta=1 and certifies objective-sublevel boundedness.
These checks are independent of the author's forthcoming verifier. Plotted
floating-point central points still require their own residual and gap checks.

Root also revisited the primary publisher abstracts and accessible author
pages for Renegar (1996) and Peña (2001). Full texts were not obtained in this
additional search; the established source-access limits remain unchanged.
The current Xiong--Freund arXiv record still lists the inspected July 15, 2024
v3 as latest, with no journal reference on that record. No new priority claim
is inferred from these checks.

### Two further primary geometric comparators

Root's targeted search of Hilbert-metric and symmetric-chord comparisons led
back to Nesterov--Nemirovskii (1994), Proposition 2.3.2(iii), equation (2.3.9),
printed p.35. Root inspected the original local PDF page visually. The
symmetric chord radius at a given point is between the reciprocal Hessian
norm and (1+3nu) times that value. Thus comparison of different barriers at
the same point is already a classical consequence. The author was asked to
distinguish it explicitly from the equal-gap comparison at different centers.
Narayanan--Rakhlin (NIPS 2010), Theorem 10, was the search lead, but the original
book is the direct source; no new sampling claim is imported.

Root also read Duistermaat, *On the boundary behaviour of the Riemannian
structure of a self-concordant barrier function*, Asymptotic Analysis 27(1),
9--46 (2001), DOI 10.3233/ASY-2001-448. The primary Utrecht manuscript is at
https://dspace.library.uu.nl/bitstream/handle/1874/2052/1113.pdf?isAllowed=y&sequence=1
and journal metadata was verified at the publisher. Its introduction and
Assumption 2.1 concern smooth strongly convex boundary and additional
boundary-regularity assumptions. Remark 2.3 (printed p.4, visually checked)
uses f+A sin(f) to produce oscillating rescaled derivatives within the
self-concordant class. This is a direct antecedent to oscillatory barrier
perturbations. The author was asked to cite it concisely and reserve the
specific claim here for the mixed rectangle perturbation, globally certified
parameter, nonconvergent center, and sharp projector/solution-error calculation.
Neither the first oscillatory barrier nor the first pointwise norm comparison
is claimed. These additions will be included in the Stage 5 five-reviewer audit.

### Stage 5 review assessment

The complete 36-page draft and portable reproduction package received five
independent reviews, recorded in reviews/stage5-r1.md through stage5-r5.md.
Root read every report. All five found no major issue. Root accepts every
reported minor: (1) the abstract must say at most two LP spectral scales;
(2) numerical SDP formulas describe an exact central point, not the single
analytic center; (3) the simplex perturbation remains vartheta in prose and
figure labels; and (4) introductory uniformity requires residuals uniformly
bounded away from one. Root adds one minor precision clarification: synthetic
CG interval ratios two and three are prescribed before floating-point matrix
construction, not exact spectral equalities for the rounded matrix.

Independent isolated reruns reproduced all 23 manifest hashes. Reviewers
independently verified exact rational certificates, cache provenance, and
source comparisons. Reviewer 4 additionally used a separate 110-digit
Cholesky solve to confirm all final CG residual and energy errors. Root
inspected the title and numerical PDF pages and found the presentation legible.
The distinct fixer is assigned all accepted minor corrections, regeneration
of the changed figure/manifest, and a clean build. No Stage 5 major-issue
repeat is required; the separate whole-manuscript five-reviewer cycle follows
only after these corrections are complete.

Stage 5 corrections are complete. Root checked the five edits and the distinct
fixer's validation record. The regenerated numerical rows and tables are
unchanged; only the intended script and simplex legend figure changed hashes.
All 23 hashes verify and the 36-page PDF builds without warnings. Stage 5
is complete. The separate final whole-manuscript review is now assigned to
five independent reviewers, with mathematical correctness, claim support,
completeness, consistency and readability all in scope for every reviewer.

### Full-manuscript review, round 1: root assessment

All five fresh full-manuscript reports are complete in
reviews/full-r1-round1.md through full-r5-round1.md. Root read every report
in full. All five identify no major issue. Reviewers 1–4 request no remaining
minor corrections. Root accepts both minor integration findings from reviewer 5:

1. Section 10 must explicitly distinguish the ordinary Euclidean spectrum of
   the congruent coordinate matrix from the generalized spectrum with the
   transported original metric. The latter uses Gram matrix R^T R and is
   exactly invariant. The displayed congruence inequality is correct; the
   added explanation prevents interpreting preconditioning as mere renaming.
2. Replace the otherwise undefined contact-representation terminology with
   a plain statement about auxiliary representations and their data maps.
   This retains the relevant sensitivity boundary without importing an
   unexplained object from a separate repository topic.

No other actionable finding was identified by root. The integrated reviews
rechecked the complete proof chain, precise prior-work comparisons, scope
inventory, numerical interpretations, and standalone build. Several fresh
isolated numerical runs reproduce all recorded artifacts, and clean builds
produce 36 pages without final warnings. The distinct fixer is assigned both
minor edits. Because no accepted major issue was found, the user's process
does not require another five-reviewer cycle; root will verify both corrections
and the final standalone submission bundle before completing the task.

### Completion

Root verified both full-review corrections in the final Section 10 and the
fixer's clean-build record. All accepted findings from every stage and the
separate whole-manuscript review are addressed. No accepted major issue or
remaining valid minor issue is open. The scientific manuscript is complete;
author names, affiliations and journal-specific administrative metadata remain
for the submitting authors, as stated in the README.

The final reading PDF has 36 pages. Root created submission-source.zip with
43 portable manuscript/reproduction files, excluding internal development
records and build/bytecode caches. Root extracted that exact archive into a
fresh temporary directory, checked every file against the source and all
23 numerical manifest hashes, and built the extracted manuscript successfully
without final LaTeX warnings. The extracted PDF's complete text is identical
to the delivered reading PDF. The numerical programs had already passed
multiple independent standalone reproductions; the final edits changed no
numerical input, program, table or figure. Exact archive/PDF checksums and
validation details are in final-validation.json.

The final deliverables are main.pdf, main.tex with its supporting source tree,
submission-source.zip, and the bundled reproduction package. Original paper
and literature sources are unchanged. The staged process included two
five-reviewer rounds for Stage 1, one five-reviewer round for each of Stages
2–5, and a separate five-reviewer whole-manuscript round: 35 independent
review reports, with distinct-agent corrections after all accepted findings.
This records the completed checks and their limits; it makes no guarantee of
journal acceptance or of exhaustive priority beyond the reviewed evidence.
