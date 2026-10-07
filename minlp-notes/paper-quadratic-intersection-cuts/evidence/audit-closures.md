# Closure audit

The fixed-corner closure results survive. The final statements require a
nonempty cut family with nonnegative coefficient vectors, positive objective
weights for the single-cut characterizations, and finite positive corner
value for the tight-cut theorem. The archived finite certificates establish
strict closure loss for A, B, BP and the uncompleted point-rule family P at
the tangent-edge corner, and strict improvement without exactness for A at
the support-one corner.

This audit read the final orbit-closure note, both reviews and their relevant
proof/checker records, the stopped-job closeout, the starting sfree results,
and the October program closeout. It inspected certificate logic and saved
data. It did not rerun an experiment, verifier, numerical optimizer, replay,
scan, or project-wide check, and did not inspect CI. Exact symbolic and
rational arithmetic was used for the narrowly identified proof calculations
below. The stopped ancillary searches remain stopped.

## Original-claim inventory

| Original location | Disposition and corrected scope | Final location |
| --- | --- | --- |
| Setting; closure equals D iff all positive-cost values agree | Retain. Closed convex upward sets are separated by a nonnegative normal; perturbing it by a small positive all-ones vector preserves strict separation. | Main §5, `cl:factors` |
| Lemma 1(a), blocking description | Retain for nonempty V⊂Rⁿ₊, ω≥0, z>0. | `cl:blocking`, full proof |
| Lemma 1(b), one-cut description | Retain for ω>0; do not extend this characterization to zero coordinates using undefined 0·∞ products. | `cl:blocking` |
| Lemma 1(c), convex coefficient up-set criterion | Retain for equality in every positive direction. | `cl:blocking` |
| Theorem 2, tight limit cuts | Retain; expand the vanishing-weight argument and state nonnegative V explicitly. Zero-limit slots may diverge; drop their nonnegative contributions. The surviving weights still sum to one. Tightness then reduces N+1 slots to N. | `cl:tight` |
| Proposition 3, smooth-face rigidity | Retain with C¹ regularity near the corner, ω>0, zK∈(0,∞), selected minimizing λ*, and ∇Jg≠0. Add complete convex domination characterization on unused coordinates, requiring at most |Jᶜ|+1 tight limit vectors. | `cl:smooth` |
| Corollary 4, ≤1 unused ray | Retain. This is exactness equivalence, not equality of two suboptimal values. | `cl:one-unused` |
| Bilinear support-two specialization | Retain for three projected rays spanning R³. Give a direct regularity proof from the indefinite quadratic on the tangent plane. The general inertia theorem guarantees a sparse minimizer; its statement alone does not justify replacing “there is a minimizer” by “all minimizers.” | Main after `cl:one-unused` |
| Proposition 5, z1≥zcl/N | Retain with ω>0 and finite positive zcl. Expand the supporting-face and limiting argument. The abstract coefficient family {e₁,…,eN} attains N. | `cl:gain` |
| A/B/P/BP definitions and inclusion diagram | Retain. BP means all transformed point-rule completions, not signed permutations. B permits vertex interior in its completion even if the original orbit set does not contain the vertex in its interior. | `cl:bilinear`, `cl:point-parameters` |
| Lemma 6, kept inequalities/interior/recession | Retain; direct necessary kept inequalities suffice for every closure certificate. Interior criterion is also established in the foundations. | `cl:certificate-tools`, `fd:orbit` |
| Lemma 7, B parameter half-space | Retain; include the rank-two affine-image plane argument and interior-of-convex-sum step. | `cl:halfspace` |
| Lemma 8, kept-boundary BP vector | Retain; include general 2×2 matrix identities, not just instance checks. | `cl:kept-boundary` |
| Theorem 9, four explicit closure points | Retain every point, family and exact sum. The tighter files have suffix thm14t; base thm14 files hold the earlier weaker points. | `cl:counterexample`, `cl:finite-certificates` |
| Theorem 9, decimal lower brackets | Retain rounded-down .97538 and rational 2539/10000. .97539 is only an approximation. | `cl:counterexample` |
| Certificate-free closure obstruction | Retain. It uses strict supremum loss zB<1, not merely failure to attain one. | Main proof of `cl:counterexample`; `fd:counterexample` |
| Starting larger A tangent-edge example | Retain A closure loss using support-two rigidity. B closure loss at that example remains numerical. | Main after `cl:counterexample`; foundations |
| Proposition 10, support-one improvement | Retain .9838≤zA≤.9839<.9953611≤zcl,A≤.999<1. Reduce the lower proof to three saved rational cuts and an explicit rational dual. Upper point remains an exact finite SDP cover. | `cl:support-one`, `cl:support-one-certificate` |
| Proposition 10, B extension | Retain only zcl,B≥zcl,A and numerical estimates near .9953622. The B upper certificate is incomplete; no exact B nonexactness at this particular corner is claimed. | Main after `cl:support-one`; appendix limits |
| Theorem 11(a), BP infinite fixed-corner factor | Retain the exact universal a₁≥7/2, closure point, rational feasible-set lower bound, and positive-cost limit. Add an exact parameter showing attainment of inf a₁; source had only numerical attainment. | `cl:unbounded`, `cl:bp-factor` |
| Theorem 11(b), A four-ray factor | Retain integer dual certificate and all ε>0 upper bounds. Correct auxiliary lower depth estimate to 0<ε≤√2; the unqualified source display is false for sufficiently large ε. | `cl:unbounded`, `cl:wcorner-proof` |
| Theorem 11(c), BP sharp four-ray constant | Retain exact constant, equality class, closure-point characterization and untransformed point-rule cut. Replace five-case proof with exact involution exchanging rays, removing the delicate final admissibility case. | `cl:wcorner-proof` |
| Theorem 11(d), B exact four-ray closure | Retain explicit S-free completion and cut (0,0,0,1/2). | `cl:unbounded`, `cl:wcorner-proof` |
| Lemma 12, recession explanation | Retain as explanatory proof: an orbit set cannot have the two specified positive recession directions simultaneously. It explains a structural difference but is not itself a quantitative closure certificate. | `cl:wcorner-proof` |
| Proposition 13, every ray hits S | Retain finite factor bound for every chosen member C. All-ray finite hits are required; do not weaken to an arbitrary subset. | `cl:finite-factor` |
| Corollary 14, no uniform factor A/B | Retain the proved qualitative limit and fixed-vertex scaling; separately state the computer-assisted 411√ε/z₀ rate for 0<ε<1. | `cl:no-uniform` |
| BP “uniform factor unresolved” task shorthand | Exclude as false: BP⊂B transfers the zero uniform guarantee, and BP already has an infinite factor at one fixed corner. Genuine BP open issues concern coefficient convexity/observed agreement, not existence of a uniform positive closure ratio. | `cl:no-uniform`, appendix limits |
| §6.2, local A/B factor | Retain exact lower factor >1.1166. A finite numerical scan near 1.128 does not establish local finiteness. Add exact six-edge proof for zK>649/2500. | `cl:local-factor`, main final factor paragraph |
| §6.3, ABP comparison | Retain as a comparison with different hypotheses and conclusions; do not transfer ABP’s theorem directly or assert publication novelty from failed searches. Root’s sole librarian verified bibliography/source interpretation. | End of main §5, ABP2018 |
| §7, eleven-instance closure survey | Preserve all rows and numerical status. Single B values are heuristic lower estimates. Finite-cut closure LP values are lower estimates; incomplete pricing does not certify an upper estimate. 17 of 18 point-rule comparisons agree numerically. | `cl:numerical-records` |
| §8, six rebasing trajectories | Preserve all six, with five reaching the bound. These are numerical trajectories, not a convergence theorem. | `cl:numerical-records` |
| §9, finite box and SDP lemmas | Retain complete affine/PSD proofs, free-coordinate rule, distinct-ray rule, sign/length checks and coverage arguments. | `cl:box-certificate`, `cl:sdp-certificate`, `cl:finite-certificates` |
| §§10–12, failed searches, review history and process logs | Preserve provenance in this audit/evidence; omit agent and process-stage narrative from the manuscript. Searches do not establish novelty. | Evidence companion and verification record |
| §§13–14, remaining limitations and open questions | Retain mathematical questions and incomplete B support-one status. The W BP target is now proved analytically; the stopped search is not evidence for it. | End of `cl:numerical-records` |
| Unrestricted fixed-corner and polyhedron rank-one closures | Retain distinction. All S-free sets at one corner give D; the original-basis closure of a polyhedron need not give its nonlinear hull. | `cl:unrestricted`, `fd:dominant`, `fd:rank-one-example` |

## Corrected theorem content and dependencies

Let V be a nonempty subset of the nonnegative cut-coefficient orthant.
The closure coefficient up-set is cl(conv V+Rⁿ₊), while the single-cut
coefficient up-set is cl(V+Rⁿ₊). Positive-cost equality of their radial
bounds is equivalent to convexity of the latter. The tight-cut theorem
requires zK∈(0,∞) and positive weights. Its conclusion is domination by
a finite convex combination, not equality of a barycenter. This distinction
is what makes the vanishing-weight/unbounded-vector limit sound.

For a smooth regular minimizing support J, every tight valid coefficient
vector has aJ=ωJ/zK. Exact closure is equivalent to finite convex domination
of ωJᶜ/zK by unused coordinates of these tight limit cuts. No additional
closure of this final convex hull is needed: the nonnegative limiting
argument already supplies actual vectors in cl V. When |Jᶜ|≤1, one of these
vectors dominates alone and the single-cut supremum is exact. This does
not require attainment by a member of the original family.

S-freeness has an elementary certificate. If sym(FᵀM(s))≽0 and detF>0,
then det(FᵀM(s))=det(sym(FᵀM(s)))+k²≥0, so q(s)≥0. The upward completion
also lies in {q≥0}, because q(c+tew)=q(c)+t. Every q=0 point has points
of q<0 arbitrarily near it, since ∂q/∂w=1; hence its interior cannot
meet S. The maximality exceptional class is addressed by the foundation
audit: if F=[[a,b],[c,d]], b=0 and a<0, the completion slice is empty.
Every B set admissible at the current vertex is therefore nonexceptional.
The closure arguments require only S-freeness, not blanket maximality.

The Thm14 corner value and uniqueness can be proved without enumeration.
For barycentric coordinates (α,β,γ,δ) of (sbar,v₁,v₂,v₃), let
Q=w(α+β+γ+δ)−xy. Then

```
64 Q = 3[16(β−γ)−5α+2δ]^2
       +21α²+148δ²+1036αδ+192αγ+1280βδ.
```

At the Prop16 corner the analogous identity is

```
512 Q = (64α−79γ−32δ)^2+31γ²+512δ²
        +1280αδ+4032γδ+128β(8α+γ+2δ).
```

Both are exact polynomial identities and all displayed products are
nonnegative on the simplex. Their unique zeros establish the corresponding
unique corner minimizers. The foundation author independently expanded
both identities and incorporated them in the manuscript.

At the four-ray corner, the sharp BP proof is fully analytic. The exact
involution T(x,y,w)=(-y,-x,w) fixes the vertex, exchanges rays 1 and 2,
and maps the BP parameter Σ to Σ′=HΣ⁻¹H, H=[[1,1],[1,-1]]. The identity
AΣ(Ts)=(ΣH/2) AΣ′(s) (ΣH/2)ᵀ gives the needed interchange of kept and
unrestricted maximizing directions. It reduces the source’s five cases
to: an abnormal parameter with one coefficient at least 1/2; both
unrestricted maxima kept, where AM–GM gives the sharp constant; or one
maximum unkept, where two boundary vectors give a sum >3/4. Equality occurs
only at Σ proportional to I. This proof needs only necessary kept
inequalities and containment C⊂B, so it does not depend on sufficiency of
the kept-halfspace description.

## Exact data for standalone appendices

All compact data are printed in `appendices/C-closures.tex`:

- All four Thm14 closure points, family assignments, sums and brackets.
- BP lower-bracket Σ=[[1,-392/621],[-392/621,47753/99290]],
  μ=2539/10000 and lowering parameters (0,0,227/64).
- BP attainment Σ=[[1,-7/12],[-7/12,7/18]], detΣ=7/144 and zero endpoint
  sym(Σ(I+(2/7)N₁))=0.
- Recession witness Ξ=[[a,b+k],[b-k,c]] with
  (a,b,c,k)=(658069/904895,-83794/200103,246826/904895,-385931/893930),
  proving λ₂+λ₃≥367/759 on X.
- Four-ray integer matrices Y₁,Y₂,Y₃,Y₄=0 and R; positive-definiteness
  principal-minor values at every coefficient-simplex vertex.
- The three Prop16 rational parameter matrices, all nine rational steps,
  exact endpoint principal-minor lower margins, rational dual y, all three
  dual slacks, and y-sum 24884029/25000000.
- Exact six-edge q minima for the local factor bound and all four
  triangular projection determinants. These replace reliance on the
  original face-enumeration script.

The compact three-cut argument proves the claimed .9953611 lower endpoint.
The archived sixty-cut LP optimum
396503562307491652037015395705021177207626376155404352 /
398351441316353660966368086274075897893464946699521021
is retained as a finite-relaxation value. It is not asserted equal to the
infinite closure value.

Large universal-membership proofs require their finite rational partitions.
The submission evidence companion must include the following originals,
not references to repository notes. Paths below are relative to
`research-20261001/orbit-closure/` for packaging only.

| Original artifact | SHA-256 |
| --- | --- |
| logs/boxcert_thm14_B.json | fbce9b68b73e1e05e027a0ac1463b21da36c0ccd81c96875c156437c81871d05 |
| logs/boxcert_thm14t_B.json | 311ff0e8f17ceecf83293bb5593766736844e6a27786c63465d09d8ef138992a |
| logs/boxcert_thm14_BP.json | f939ef023ad123d295ba4e838a5a9c0575021bc8fd50834c6d94707f5f18a976 |
| logs/boxcert_thm14t_BP.json | bf8aa0ca390cda9e53d87823d47ea4b1cf2b6179e28d5ed0dcdde717c1615e37 |
| logs/boxcert_thm14w_B.json | 04b780137a4737ccda774a97081422a8f8bafcc853c5ea13d8c103457d102369 |
| logs/closure_cert_thm14_A.json | 49814426de83592107ba0e4165093a3133ecdd577f55d0a775eff7aa6ec9b025 |
| logs/closure_cert_prop16_A.json | 3ca0a339919d5f54ca69c344ecb79497dda6dcbf312d9b0545c6e9fa1ac3f8bb |
| logs/closure_cert_wcorner_A_A.json | 79412c723b855e3c4ce5b99bd4d0ee4eeee51e1aa54a7ac33a9b3e34862e5d0b |
| logs/revision-r1/closure_lower_prop16_cuts.json | 6687df3e44b4909efe79ec526db0d7a4074de6b80b0724baf96b6a5d944daf90 |

The separate source checkers are `code/verify_box_cert.py` and
`code/verify_closure_cert.py`. They reconstruct all required algebra from
the complete instance data; neither imports repository modules, notes,
literature files or a knowledge base. Box verification uses the Python
standard library and SymPy only for deriving the BP linear forms; those
forms are also displayed explicitly in the appendix. SDP verification uses
the Python standard library. Their packaging documentation must name these
dependencies and exact invocation arguments. The large JSONs contain every
terminal box/simplex coordinate and rational witness needed for coverage and
inequality checks. Today's hashes identify source bytes; they do not replace
verification of the finite records.

For numerical-record reproducibility, also preserve the closure survey
JSONL files, factor-scan/edge JSONL files, both positive-near-edge closure
JSON records, and six `loop_rank2_single_*.jsonl` files. Their rows carry
instance coordinates and provenance for the survey/trajectory labels. The
manuscript calls those results numerical throughout.

The paper uses data-record labels R1–R8 for the otherwise undefined survey
corners. Old identifiers remain only in this companion mapping. Matrices
below are row-major, with projected rays as columns; decimal entries are
the recorded floating inputs, not newly asserted exact rational instances.

| Paper label | Original data identifier |
| --- | --- |
| R1 | adv8_1 |
| R2 | adv8_4 |
| R3 | prop16_v2_1 |
| R4 | prop16_v8 |
| R5 | supp1_1074 |
| R6 | supp1_3437 |
| R7 | supp1_4580 |
| R8 | supp1_5512 |

```json
[
 {"record":"R1", "sbar":[0.1868874448153055,-1.2291780321978756,-0.135790100177966],
  "P":[[0.10752380469324785,-1.5317820655583327,0.19843966849177308],[-2.59977541016562,-2.522829840368569,-4.903591167511008],[-0.9388796809510396,5.197664354901601,2.0311135439309567]]},
 {"record":"R2", "sbar":[-4.160080992943655,-0.4344985844618101,3.132393758828675],
  "P":[[7.803594044886229,2.541987939771521,9.14255170855347],[-0.6014164833885192,15.483782519564958,-5.156366510880319],[-5.825984036837008,39.10316270908147,1.8311340133806526]]},
 {"record":"R3", "sbar":[-2,3,2],
  "P":[[2,8,3],[-3,-5,-5.5],[-2,-1,-1.5]]},
 {"record":"R4", "sbar":[-2,3,2],
  "P":[[2,10,3],[-3,-6,-5.5],[-2,-1.75,-1.5]]},
 {"record":"R5", "sbar":[0,-4.5,3],
  "P":[[-1,2.05,-1],[2.5,1.52,5.5],[-1,-5.98,1]]},
 {"record":"R6", "sbar":[-3.5,1.5,4],
  "P":[[1.5,3.55,4.5],[-2.5,-8.4,-3],[-2,8.05,-3.5]]},
 {"record":"R7", "sbar":[0.5,0.5,0.5],
  "P":[[-1.5,1.5,-4.5],[-0.5,-9.41,2],[-0.5,8.59,0]]},
 {"record":"R8", "sbar":[-1.5,0.5,0.5],
  "P":[[1.5,2.5,3.5],[-0.5,-2.5,-0.5],[-0.5,-0.48,0.5]]}
]
```

The defined analytic examples keep semantic cross-references in the paper:
the tangent-edge theorem, the larger orbit example, and the support-one
proposition. The omitted near-boundary record is old identifier adv8_3.

## Corrections beyond those already applied in October

1. The four-ray auxiliary A lower bound must state 0<ε≤√2. Its unrestricted
   display is false for large ε; the infinite-factor result is unchanged.
2. BP a₁ infimum attainment at the three-ray corner now has an exact
   rational witness, rather than numerical evidence only.
3. The full smooth-face characterization is explicit on unused coordinates.
   The limiting representation does not assume bounded coefficient vectors.
4. In the old five-case W proof, the assertion t* >0 when b+c≥0 is false
   in general; e.g. a=1,b=2,c=5 gives t*=(-5+√10)/15<0. The new involution
   proof avoids this assertion entirely. The old derivative display had
   already been corrected by r2; neither display is needed by the new proof.
5. The generic box lemma states μj>0 explicitly. The saved verifier already
   checks this condition. The producer’s old chart docstring describes
   obsolete symmetric/skew charts; final data, code and checker use raw-entry
   facets as stated in the manuscript.

Previously fixed issues remain fixed: each ray contributes at most once;
canonical ray keys and duplicate JSON keys are checked by the box verifier;
both verifiers check point sign and dimension; free-coordinate pruning
requires zero coordinates in the feasible pruning point; rounded lower
endpoints are .97538 and .9953611. Historical review logs document independent
acceptance of the saved originals. Today's audit does not relabel that
historical work as a fresh replay.

## Remaining extensions and recommended disposition

Keep the following open: exact restricted closure with support one but
strict single-cut supremum loss; local finiteness of A/B factors at Thm14;
the observed P/BP single/closure agreement; finite convergence of rebasing;
and certified B nonexactness at the particular Prop16 corner. Every main
theorem is independent of these extensions.

Do not restart, repackage as success, or depend on the incomplete B Prop16
checkpoint or the stopped W BP run. The W BP claim is now proved
analytically and the historical log lacks rational witnesses. Do not treat
solver propagation of the W corner as evidence for a useful solver policy.
Do not use finite scans to assert exact closure values or finite worst-case
factors.

## Targeted verification performed for this audit

Source investigation used scoped `rg --files`, `rg -n`, `cat`, `sed`, and
`nl -ba` reads. Read-only inline `python3` scripts using Fraction and SymPy
checked the selected three-set support-one principal minors and dual slacks,
the BP attainment endpoint, the rational recession witness, the BP lower
bracket, the two simplex polynomial identities, the exact W symmetry and
its involution, the rational-max derivative and AM–GM identities, and file
SHA-256/metadata. One initial metadata script stopped on a box-schema type
assumption; the corrected schema read succeeded. An exploratory symbolic
check initially confused the exact inverse-defined symmetry with its
unscaled representative; the corrected exact involution has residual zero.

The lead closure author independently evaluated the six rational edge
quadratics and four facet projection determinants in an inline Fraction
script. All six minima are positive and match the local-factor appendix.
No optimizer or stored experiment script ran.

A targeted LaTeX harness loaded only `macros.tex`, `sections/05-closures.tex`
and `appendices/C-closures.tex` and ran
`pdflatex -interaction=nonstopmode -halt-on-error`. It produced a 12-page
fragment PDF with no LaTeX error or overfull box. Cross-section references
and bibliography resolution are integration work, not established by this
fragment check. A scoped `git diff --check` on the two authored TeX files
passed. These are local targeted checks, not CI checks.
