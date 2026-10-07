# Whole-paper integration review, round 2

Reviewed on 2026-10-05. This is the final bounded Sol integration round after
the completed Appendix L, final framing, numerical repairs, and reader
corrections. It supplements integration-r1.md; it does not replace the
independent chapter proof reviews or the separate fresh Opus review.

**Pass for the mathematical and exposition interfaces in the recorded body
snapshot.** The pending Appendix L follow-up from round 1 is complete. One
new overview scope contradiction was found, repaired by root, and reread in
the actual source. No unresolved mathematical, complexity, representation,
or statement-to-proof interface finding remains in this review's scope.
All 97 original inventory entries remain in scope. This is internal review,
not external peer review, an independent priority audit, or a guarantee of
journal acceptance.

## Scope and evidence

I reread the complete integration-r1 report, the framing and numerical
repair records, numerical-r2, nonconvex-r1, cones-r1 and cones-r2,
authoring/further-arithmetic, and readability-r1. I read the current BRIEF,
author conventions and decisions, integration records, and final coverage
audit. The coverage audit's statement and proof inventory is separate from
this correctness review; I did not repeat its locator checker.

I read all 1,167 lines of actual Appendix L and reconstructed its proof
chain. I checked the final abstract, 00/01/11 interfaces, actual inclusion
in main.tex, the reused J ordered-elimination and common-field recovery
contracts, and the local statement changes in 02 and 05–10/D/G/J. The
round-one A–K integration conclusions remain applicable to their unchanged
proofs. The numerical changed-scope review records that B and F stayed
unchanged; their current hashes agree. J's new multihomogeneous Bézout
locator changes attribution, not its mathematical interface.

Two fresh delegated read-only checks separately examined L's output-model
interfaces and its field/elimination/certificate interfaces. Both read
the actual completed appendix and its full proof-review/response records,
including cones-r2. They found no further concrete issue. Their conclusions
are incorporated below. Literature contracts were supplied through the
designated literature lane; no reviewer in this integration round searched
for or retrieved external sources.

## New finding and actual repair

**Medium exposition severity; resolved.** The previous introduction said
that limits applied to all results and that the hardness results were
relative to PosSLP or Square Root Sum, neither NP-hardness nor unconditional
lower bounds. That blanket sentence contradicted the new nonconvex results
at L:611–628. On [L:611](/workspace/minlp-notes/paper-exact-arithmetic/appendices/L-further-arithmetic.tex:611),
the concave row sum_i x_i(1-x_i) <= 0 on [0,1]^n forces Boolean
coordinates; the affine clause rows then reduce 3-SAT to feasibility with
one constraint-Hessian direction. At [L:617](/workspace/minlp-notes/paper-exact-arithmetic/appendices/L-further-arithmetic.tex:617),
the row sum_i x_i(1-x_i)-ty <= 0 and objective t give a supplied zero
infimum, attained exactly for a satisfiable formula. These actual reductions
are valid and use bounded coefficients. The contradiction was in the
overview, not in their proofs.

Root's actual repair at [00:918](/workspace/minlp-notes/paper-exact-arithmetic/sections/00-introduction.tex:918)
now scopes the PosSLP/Square Root Sum sentence to continuous convex
polynomial families and explicitly identifies Appendix L's strong
NP-hardness of nonconvex feasibility and attainment at a supplied zero
infimum with one constraint-Hessian direction. I reread and accept that
text; the output-model helper independently confirmed closure. The accepted
00 hash is 697822ed8c772532c85172845cce06742c6a07dd18591d393f8fa55a0506c96b.

The four round-one contract repairs remain present and accepted:

- [02:734](/workspace/minlp-notes/paper-exact-arithmetic/sections/02-points.tex:734)
  charges L,D,q in the global-convex column and L,q in fixed-degree columns.
- [09:193](/workspace/minlp-notes/paper-exact-arithmetic/sections/09-certificates.tex:193)
  transfers the prime family's monomial count and mathematical parts
  (b)–(d), charges the arbitrary integer scale's binary length, and gives
  coefficient/Gram-entry bits O(log ell+log c).
- [G:254](/workspace/minlp-notes/paper-exact-arithmetic/appendices/G-fields.tex:254)
  distinguishes rational from integer scales and charges the supplied scale
  instead of inheriting an uncharged constructor or integrality claim.
- [02:495](/workspace/minlp-notes/paper-exact-arithmetic/sections/02-points.tex:495)
  names the hard minimum-norm selector at accuracy 1/4; the easy fixed
  selector already furnished by the proposition remains available.

The 17 reader repairs also preserve their actual proof contracts. In
particular the chart vector is bar c while c_0 remains the separation
constant, degree summaries have the correct dimension ranges, the
interior-Gram Rayleigh quotient uses m_k=min h_k, and the tower's negative
square coefficient is explicitly a signed decomposition. Recourse now
states which coordinates remain provisionally free after certified
endpoints are substituted, defines its core approximation and positive
regularization parameter, and separates internal face/margin certificates
from the point/value output. None of these changes drops a result or
supplies an unproved extension.

## Appendix L and the existing manuscript

The nonconvex parameter counts constraint-Hessian directions and excludes
the arbitrary objective Hessian. The graph lift keeps every affine row.
The minimal-face argument samples a whole connected component contained in
a selected face; a zero-dimensional chart is handled directly. Therefore
the feasibility consequence does not import GP's announced optimization
Theorem 1.5 or delete inactive inequalities from a global problem.

The indefinite KKT reduction requires both M and the bordered KKT matrix
to be nonsingular. Its Jacobian is -det(M)^2 G M^{-1} G^T, so the
bordered determinant supplies the regular multiplier roots needed by
J's elimination lemma. No native PSD-QCQP theorem, positive-definite
Lagrangian Hessian, or bounded-multiplier premise is transferred to squared
cone rows. Formal parameters and local coefficient norms give the stated
height bounds before any expanded monomial or numerical precision charge.

For a finite nonconvex infimum, f+epsilon||x||^2 is coercive on the closed
feasible set. Each fixed-epsilon auxiliary box encloses all exact
regularized minimizers; compactness and comparison force every sufficiently
small inner perturbation minimizer into its interior. Its rows disappear
before the chart/KKT coefficients are formed. The inner perturbation limit
is taken before the outer regularization limit. A finite scalar outer limit
is enough when primal points escape, so there is no hidden log R_epsilon
term and no unattained-infimum-to-feasible-point inference.

When attainment holds, least norm bounds the selected regularized points.
All coordinates and all fixed linear forms use one nested limiting tuple.
The primitive-element argument bounds its joint field, rather than
multiplying coordinate degrees. Nonconvex least-norm optimizers may be
nonunique. The NP-oracle status/value/attainment/output argument keeps that
distinction, handles an infimum equal to a negative-query midpoint and norm
zero, and verifies separately recognized values in a candidate's own
field. Its mixed-integer extension has explicit finite integer bounds;
neither it nor the framing asserts unrestricted unbounded-integer NP
membership or ordinary polynomial nonconvex optimization.

Cone input charges a dense defining polynomial, its selected isolator,
power-basis coefficient lists, and the varying field degree D. The span is
over that field of the continuous Hessians of the squared cone residuals.
Every cone sign remains in the exact system. The formula includes all
active affine subsets, rank charts and zero-dimensional cases, and a finite
perturbation grid whose selected member may depend on the free z. A common
finite radius stays outside the universal small-parameter quantifier.
These details prove exact projection even if the convex projection is
nonclosed.

## Corrected cone radius composition

The source grouping problem reported in cones-r1 is resolved by the actual
QE-first proof at [L:791](/workspace/minlp-notes/paper-exact-arithmetic/appendices/L-further-arithmetic.tex:791).
I independently checked its composition from the supplied precise source
contracts, rather than accepting the earlier favorable source relay.

The fixed-zero objective coordinate is adjoined before QE. Thus the same
convex set {0} x Y has t+1 free variables and quantified block dimensions
(2,1,h+1), including one generator variable selecting the input embedding.
Basu 2014, Theorem 2.27 gives individual output degrees
d_*^{O(n_omega)...O(n_1)} and coefficient bits
b_* d_*^{O(n_omega)...O(n_1)O(t+1)}. With the actual polynomial input
bounds and d_* >= 2, these become d'=L^{O(h+1)} and
b'=L^{O((h+1)(t+1))}. These are per-polynomial bounds independent of atom
count; the text makes no such claim about the number of output polynomials
or the cost of constructing them.

Only the quantifier-free case of Khachiyan–Porkolab Theorem 1.1 is then
used. Its coordinate-bit bound b'(d')^{O((t+1)^4)} gives
L^{C(h+1)(t+1)^4} after enlarging an absolute constant. Minimizing the
coordinate fixed to zero makes every feasible integer point an optimizer,
so an integer optimum exists exactly when Y has an integer point,
including for nonclosed Y. Neither huge formula nor its QE computation is
constructed by the algorithm. The repeated-d-th-power counterexample to
the old transcription no longer contradicts this derivation: the eliminated
degree charges its quantified dimension before the witness bound is applied.

The printed integer box has polynomial-bit endpoints at fixed t,h.
Substitution and the nonconvex field-radius lemma give a uniform continuous
box meeting every nonempty exact fiber, without enumerating assignments.
The epigraph of the original maximum residual adds no Hessian direction and
supplies the uniform exact gap. Rational outward rounding preserves all
original feasible points and bounds every original residual strictly below
that gap; the cone bound remains 66 Delta/256 < Delta/2, including when
the original right side is negative or zero. Rational cone lifting leaves
only the original integer variables. Rounded squared-Hessian span is not
used. The MILP returns an assignment with an original exact nonempty fiber,
not an asserted exact original continuous point from the rounded lift.

## Exact recovery and framing

For continuous cone input, the original closed convex set has one
minimum-norm point. Auxiliary-box inactivity gives one selected tuple and
relative joint degree Lambda. The absolute field degree charges D Lambda.
The norm-slice approximation uses the Lorentz identity without leaving the
input field, adds at most one Hessian direction, and restarts the original
box for every accuracy request. Its rational midpoint is an internal
coordinate approximation; it is not asserted to be a feasible rational
fixed-selector output under Section 01's convention.

J's recovery theorem receives the fixed tuple (alpha,x*) and constructs the
absolute field containing the input generator. The final verification
checks its generator equation, selected isolator, original affine rows,
squared residuals, and cone signs. The continuous degree and total length
are L^{O(h+1)}, while conservative runtime is L^{C_h}. Mixed recovery
substitutes the returned polynomial-length integer assignment and charges
the input length of that original exact fiber. It supplies that fiber's
minimum-norm continuous point, not a global minimum-norm integer assignment
or the sharp continuous exponent in the original mixed input.

Actual 00:405–419 and 00:729–735, 01:578–585, and 11:144–155 preserve
these scopes. Known algebraic thresholds augment the exact system before
its boxes and gap are derived. Attainment uses a supplied true finite
infimum. The fractional corollary requires rational original data, a
supplied attained value, and the reciprocal cone enforcing d,s>0; it adds
at most one continuous Hessian direction. No unknown mixed-integer value
algorithm or absolute-exponent FPT bound is asserted.

The earlier global distinctions also remain intact: equality has the
PosSLP upper bound only, arbitrary-polyhedron deterministic one-instance
comparison stays open, the adaptive compiler returns one Boolean instance
without determinizing Las Vegas work, and the certified cyclic input
charges its dense Hessian Gram. General real-field PSD Grams are not
identified with SOS over that field. The abstract descent criterion does
not acquire an all-dimension cyclic stationary-space premise. The full
V1–V5/RQ1–RQ4 recourse contracts, minimum rational-SOS-failure dimension,
sharp five-variable degree 21 and qualitative finite radial order are
retained with their actual proof locations.

## Source and submission limits

This review accepts the supplied established theorem contracts and checks
their actual use. It does not independently certify external metadata,
priority, or the entire primary-source inventory. The repaired radius uses
exactly Basu 2014, Theorem 2.27 and the quantifier-free case of
Khachiyan–Porkolab Theorem 1.1. It does not need either earlier incorrect
direct quantified bound. GP Theorem 1.2 is credited for sampling;
cumulative affine degree/projected hypersurface bounds and KLL recognition
remain separately identified imports. The framing identifies the additional
limit, field, sign, rounding and output guarantees rather than presenting
all sampling or integer algorithms as original.

The six bibliography records absent at the original body snapshot are now
integrated: KrickPardoSombra2001, Heintz1983, KhachiyanPorkolab2000,
Kocuk2021, BenTalNemirovski2001 and Lenstra1983. A targeted read of the
current bibliography confirms all six keys; GrigorievPasechnik2005,
Basu2014 and BombieriGubler2006 were already present. Lenstra's name uses
the corrected BibTeX syntax for H. W. Lenstra Jr.; its identity is unchanged.
This closes the six-entry bibliography integration item. Root reports its
scoped source diagnostic passes with 27 sources, 658 labels, 1,766
references, 120 cited works and zero errors. I did not run that diagnostic.
The broader literature record remains owned by Luna. The root's review,
document build and package inspection remain separate evidence, not checks
run by this integration reviewer.

After the mathematical review, J's two elementary height identities were
placed on separate gathered rows at J:187–193. I reread those rows; the
product inequality and product-formula identity are unchanged. The
layout-only J hash is now
5d01e18401f2fde9d3c2e62d0dde59784101b923ed84980b972266b15e01b3d9.
The original J body-review hash remains in the historical snapshot below.
The current main file also starts the bibliography on a new page and adds
References to the contents. These navigation changes add no mathematical
claim. Later manuscript scope/source changes are reviewed separately; this
update does not silently refresh the earlier body verdict to a new snapshot.

## Reviewed SHA-256 snapshot

The body snapshot was refreshed after the concrete 00 scope repair. The
whole L and J hashes match cones-r2. The 02 hash includes both of its
round-one repairs; the 09 hash includes its later reader corrections as
well as the accepted integer-scale repair.

```text
ca55daf4ee1dc0cb4636255c3b488cf8ecd5d3d4a276d4df2f71fb2b6eebfaa8  main.tex
1eb51a834c6285ec54212db5dffc0e85c7d0c59a131df32cd7741cc2a273ebf8  macros.tex
697822ed8c772532c85172845cce06742c6a07dd18591d393f8fa55a0506c96b  sections/00-introduction.tex
f1883295ee64b7b75e17d2c86d26202169f852741934095a4efcff718d900fb0  sections/01-models.tex
9255c3b578fbef9981d96873db3effe3a0f65345fcab796bbed3e16d1f88e010  sections/02-points.tex
0db409d6a3b1e406e5e882d51311fb2df15ec345b23bea4667d61eaf7f6c2ee5  sections/03-upper.tex
0673ebfc72cfd606b7ce7d3f35d6e027520fa59188f4540b5c657f69b7ebd50e  sections/04-reductions.tex
0216cf2456eb982b40ea206dcb9f0fe4739eefd9b7b029d7b786b38a9599dc9e  sections/05-constraints.tex
b77ad09a3ad16a891f33eade8dc34cd3417a64cd3a88b8f565a1d5ee139469bb  sections/06-algebraic.tex
2cfaf3f0c8a4e6c144f3fb8b241bcdcba7a3683167c55adac4ea641a8090bbe1  sections/07-heights.tex
b05a1d5d0323344ce05eb679f4ac8651dca7cdea96360f5bdb549aeb46e4324e  sections/08-fields.tex
200313954066e5071cf3a25ec9d0f5c7a28e252b375297f2b9ec5a0515165c98  sections/09-certificates.tex
e38150a05d990980800c9e29724c6dcbe011932167b8331ff7ad88fffbe6b6b1  sections/10-recourse.tex
63252f4d6614dca06df90fa9476a6408ed6f8fb43eaeae9000ec77d0fec97440  sections/11-discussion.tex
d4a8f2ff59b5037342a6acf11cc6faf80ee475c81bac1da4a0a80ae212a64859  sections/abstract.tex
e0a65e32b8d02c2b30d29882c71c37d8f781388a73aa53bbc13dba9fbad5269d  appendices/A-upper.tex
1c78b5cd28b75854390eac3d8f48ffa6c623ecb7061f3bc4142375d70a692b94  appendices/B-reductions.tex
0469412f5fc0bb8a9122329e673a30690a2c6ddf9eb577f3844e7b39f04bde90  appendices/C-points.tex
3e7a43c5d884a915d99d0e9f46026d0d77ef1403ec04ab0157c4da03b194130e  appendices/D-constraints.tex
a55ecca962308f61f3bf882af9fde23ab8f736a830ac83f0290052a2644d1f43  appendices/E-algebraic.tex
523e1364bd3cc09c05d4f79d889826a1d4b010ead6276e8c1e71629b85d021d3  appendices/F-heights.tex
0c4ddf55ba158ccd8c3857002eaea8805d15373d183f46b785777d50117cfeb1  appendices/G-fields.tex
37ca5a03d9cbb382b9ffe327ab6894e3b43664f9a2c9e405527a37fa47f1a7c5  appendices/H-certificates.tex
f4c21d1ad36fac74449315f3b4a20c4c1652e41e50797e657796c8b0e526d155  appendices/I-recourse.tex
96a543bc359cd7fd25670752d80e35decec486d7865b6d5390eb58f82d15759f  appendices/J-quadratic-contrast.tex
ed88ea5a7c14d38370861141adb3a613a41f7e2cfd4fef42ef663af098568b82  appendices/K-boundaries.tex
eb1b9e925d0299e07f6eed8e742a1e0522789164522bb267b719b2d72a292a74  appendices/L-further-arithmetic.tex
20dbe6573a5b4be6749c6c188a6adbfe3a123e21d7599d14a07ca1fd67e3f7a5  references.bib (bibliography integration refresh)
```

## Targeted checks actually run

Read-only commands were scoped rg/rg --files, cat, nl -ba with sed reads,
and sha256sum on the named manuscript/evidence files. A sed display of
the coverage report removed link destinations only to make all 97 rows
readable; it changed no file. All actual proof reconstruction was analytic.
Only this assigned evidence file was written.

The direct whitespace check was git diff --no-index --check /dev/null
paper-exact-arithmetic/evidence/reviews/integration-r2.md. It printed no
whitespace diagnostics; exit 1 records that the new report differs from
an empty file. No manuscript edit, literature research, experiment,
mathematical script, CAS, historical diagnostic rerun, build, test,
project-wide verification, or CI inspection was performed. These document
and version checks are local review evidence, not CI results.
