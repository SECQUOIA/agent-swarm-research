# Independent review of corners and quadratic orbits

Reviewer scope: `sections/02-corners.tex`,
`sections/03-quadratic-geometry.tex`, and `appendices/A-foundations.tex`.
All three actual TeX files have been read, including the final corrected
first pencil and completed second rational example. **Final verdict: pass.
No unresolved substantive mathematical issue remains in this scope.**

## Findings communicated to the author

1. **Minor, repaired.** `fd:inertia`, section 02 line 176 in the first
   draft: the indicator lacked its `\mathbf` command backslash. The current
   source has `\mathbf1`.
2. **Missing hypothesis, repaired.** `fd:algorithms`, section 02 lines
   215–220: explicitly require `q(\sbar)>0`, as the inertia reduction and
   positive-value approximation proof use a violated apex. The current
   theorem includes that hypothesis.
3. **Minor, repaired.** `fd:pencil`, section 03 line 209 in the
   first draft: `quad` lacked its command backslash. This needs `\quad`.
   The current source has the command.
4. **Local hypothesis clarification, repaired.** `fd:orbit-sdp`,
   section 03 lines 172–185: state positive costs explicitly, since the
   endpoint LMIs divide by every cost and section 02 initially permits
   nonnegative costs. Section 03 line 119 now states positive costs and
   a violated apex throughout its bilinear corner statements.
5. **Major exact-certificate transcription defect, repaired and
   independently rechecked.** `fd:counterexample-proof`, appendix A
   lines 720–724 in the first draft, printed
   `G(u)=[[12,36-u],[u,4+3u]]`. Its determinant is `48+u^2`, so the
   printed constant determinant and subsequent witnesses did not follow
   from that matrix. The actual final source in `fd:counterexample-proof` has the correct
   oriented pencil `G(u)=[[12,36],[-u,4-3u]]`. Independent exact arithmetic
   now confirms determinant 48 and all four scalar witness identities.
6. **Missing dimension hypothesis, repaired.** The final-added
   `fd:scip-cap`, appendix A lines 685–706 in the added draft, initially stated the spherical
   cap support formula without specifying its dimension. In dimension one,
   `gamma=0,y_last=1` has support `-1`, whereas the displayed boundary
   formula would give zero. The actual final source explicitly requires
   `beta\in\R^m,m\ge2`, which covers the bilinear application and makes
   the elementary proof valid.

Every repair above has been checked in the actual TeX. The author did not
leave a false theorem in place or depend on an unverified experiment to
repair it.

## Mathematical scope checked

- `fd:single-cut`: positive-cost compactness, strict positivity, finite
  feasibility versus an infinite supremum, fattening of compact objective
  simplexes, and maximal extensions. The theorem uses suprema correctly.
- `fd:cone-attainment`: the audit's fibre-dual construction gives a free
  neighbourhood dominating a prescribed valid nonnegative inequality.
  The final proof handles zero and infinite corner values separately.
  The additional full-cone cost image is closed and full dimensional;
  extending an interior radial segment proves its freeness and attainment.
- `fd:attainment`: the compact contact and mean-value proof works with a
  noninjective projected ray matrix. The ray-coordinate cost argument,
  rather than a supposed geometric far face of the projected simplex,
  establishes that a limiting convex-combination weight is zero.
- `fd:boundary-examples`: both zero-cost examples and the positive-cost
  nonattainment example have the stated values and mechanisms.
- `fd:dominant`: the closure is the closed upward dominant, not a claim
  about the full hull in an original polytope. Nonnegative separation
  normals can be perturbed positively while preserving strict separation.
- `fd:rank-support` and `fd:inertia`: fibre-polyhedron identity, independent
  supports, regular second-order conditions, and the abnormal symmetric
  negative-direction argument. The kernel saving uses
  `b\notin\operatorname{range}Q` precisely.
- `fd:algorithms`, `fd:two-ray`, and `fd:hardness`: rational input,
  positive costs, finite-value relative approximation, discriminant
  boundaries and stationary candidates, graph normalization, threshold
  encoding, and the adjacent clique-value approximation gap. The actual
  appendix supplies the algebraic bit-size bracket, perturbation fan,
  unbounded-polyhedron truncation counts, and degeneracy details.
- `fd:generic-kkt` and `fd:efficacy`: the generic multiplier formula
  explicitly excludes singular and zero-denominator cases. The specified
  Euclidean metric, nonnegative-cost support identity, violated-point weak
  separation, positive feasible ball, and bounded weak optimization region
  address the limitations of the original efficacy remark.
  The last paragraph correctly proves equality with the efficacy supremum
  of genuine intersection cuts, while distinguishing attainment.
- `fd:nonlocal-hull` and `fd:rank-one-example`: separation of the compact
  feasible hull proves the nonlocal operation. The disk is the unique
  maximal full-dimensional free set; both original lower bases, exact
  exits, cut intersection, strict hull gap, and second-round chord check.
- `fd:lorentz` and `fd:point-rule`: the complete signatures, the two null
  halfspace orientations, Lorentz-basis construction, radical-coordinate
  products before slicing, positive apex coefficients, and the distinction
  between a set-generation exclusion and a strict corner-value gap.
- `fd:fixed-rule`: the two ray exits, exact corner minimum, and limiting
  ratio. The pointed constant-family extension in the audit has the stated
  boost and coefficient-sum formula. The actual appendix proves the limit
  analytically on pointed corners.
- `fd:orbit`: determinant automorphisms, the three-parameter orbit, the
  rank-one contact test, and the positive branch of the increasing Möbius
  graph. The complete rational graph would be an incorrect contact domain;
  the draft correctly requires `F_{12}x+F_{22}>0`.
- `fd:completion`: retained normals, balanced two-term PSD decomposition,
  bounded lowering parameters, exceptional empty class
  `F_{12}=0,F_{11}<0`, and maximality of every other completion. A delegated
  independent check also derived the explicit nonexceptional completion
  formulas and confirmed the normal-cone proof in the author's audit.
- `fd:scip-cap`: both support branches, the active endpoint versus the
  unconstrained sphere optimum, zero vectors, endpoint caps, and the
  corrected dimension hypothesis.
- `fd:orbit-sdp`: strict apex membership, positive determinant, equivalent
  scaling to an identity lower bound, and nested feasible target values.
- `fd:tangent-pencil`: two-sided tangency, vanishing lowerings and mixed
  null entries, constant determinant, ruling exclusion, and the required
  `d_x>0` orientation. Without that orientation the correct condition is
  `\theta d_x>0`.
- `fd:counterexample`: the all-face nonnegative polynomial certificate,
  oriented pencil, scalar witnesses excluding every real parameter for
  both families, bounded normalized limits, and the rank-one plane
  obstruction. The completed neighbourhood proof uses value continuity
  and compactness, avoiding an unproved persistence of a tangent edge.
- `fd:second-example`: exact edge table, negative Hessian determinants on
  triangular faces, affine independence, correctly oriented pencil and
  exact disjoint PSD intervals, and normalized rank-one exclusion. The
  statement correctly avoids inferring a certified completion gap.
- `fd:support-one`: all-face nonnegative certificate, derivative values,
  strict inactive multipliers, integer positive-definite dual certificate,
  and normalized strict-gap argument. The statement correctly claims the
  strict one-cut gap for family A only.
- `fd:wedge`: all possible outside-point cases can be excluded by explicit
  interior mixtures. Two feasible contacts on one ruling exclude both A
  and B, since a feasible boundary contact cannot be lowered.

## Source corrections verified

The final main statements correctly repair these substantive source issues:

- Convexity of the closure of the complement alone does not imply freeness.
  The draft instead requires the open complement itself to be convex.
- The low-dimensional orbit theorem gives exact suprema, and does not imply
  universal attainment.
- A positive tangent-pencil scale requires an orientation.
- The exceptional bilinear completion is a class with an empty affine
  slice, not an unexplained isolated parameter.
- Varying an affine point-rule apex still misses a maximal quadrant with
  only asymptotic contacts.
- Numerical infeasibility and old local completion searches are not used
  as exact proofs of the main-section gaps.

## Targeted verification record

Only read-only source inspection and custom exact SymPy arithmetic have
been used. No solver, experiment replay, web/literature search, project-wide
verification, or CI inspection was performed.

The custom arithmetic checked:

1. The residuals of the proposed `64Q` support-two and `512Q` support-one
   identities are exactly zero.
2. The support-one integer matrices have determinants
   `(263,791,224,64)` and their four `M(v)Y_v` products sum exactly to zero.
   The zero-LMI coefficient system has rank four.
3. The six second-instance edge polynomials have minima
   `(71/288,5/4,5/4,0,3/2,21/4)`. All four triangular-face Hessian
   determinants are negative.
4. The ray matrices have determinants `249` and `67/2` in the support-two
   and support-one instances, respectively.
5. The first contact's projected point has the strictly positive vertex
   representation `(184,463,433,72)/1152`. The manuscript's alternative
   `(184,287,257,72)/800` was also checked exactly. Both confirm
   interiority of the projection.
6. For the repaired first pencil, the determinant and all four witness
   identity residuals are zero. The kept-normal endpoint values are
   `-8/3+4sqrt(2)` and `1/5+13sqrt(30)/300`, both positive.
7. For the second pencil, the determinant is `147/2`, the two diagonal
   and determinant tests give exactly the printed PSD interval endpoints,
   and the ray determinant is `-6083/8`.
8. A targeted static Python check of the three owned TeX files found no
   duplicate foundations labels, no undefined local `fd:` references, and
   no unexpected control characters.

One first inline arithmetic command had a syntax error before execution;
the corrected command completed with the exact results above. The executed
verification commands were targeted `rg`, `nl -ba`, `sed`, and `cat`
reads; `python3 - <<'PY'` custom SymPy expansions, matrix products,
determinants, and root calculations; and one `python3 - <<'PY'` static
label/control-character check. These are symbolic proof and document
checks, not reruns of retained experiments. PDF compilation and global
reference integration belong to the lead's verification record.

## Final local additions and reviewed source hashes

The lead requested another review of the final local additions after the
initial closeout. They are sound, and the pass verdict remains unchanged.

- `fd:algorithms` now uses the stronger parameter
  `r=min(rank P,rho(q))`. The independent-support and inertia bounds give
  exactly this parameter; the fixed-variable decision argument is unchanged.
  The two-ray discriminant was consistently renamed `Delta`.
- Section 03 now proves `conv(S)=R^3` by expressing each `(x,y,w)` as the
  midpoint of `(x+a,y+a,w)` and `(x-a,y-a,w)`, both feasible for large `a`.
  The products grow as `a^2±a(x+y)+xy`. Thus cone containment is equivalent
  to the projected ray cone being all of `R^3`. The stated opposite-side
  symmetry preserves the conclusion.
- `fd:efficacy` now explicitly minimizes the linear coordinate `t` over
  the bounded epigraph `E={(a,t):a in V, ||a||<=t<=2R}`. With
  `a0=(2/z1)1` and `R=4sqrt(N)/z1`, the claimed center, inner radius
  `1/(2z1)`, norm slack, upper slack, and outer radius `2sqrt(2)R` are
  valid. The rational version `b<=z1<=2b` is also valid: the stronger
  estimate `a0^T lambda-1>=||lambda||/b` gives a feasible coefficient ball
  of radius `1/b`, so the stated joint radius `1/(2b)` fits. The outer
  radius `3R` exceeds `2sqrt(2)R`. These bounds justify the bounded-body
  weak linear optimization formulation and do not assert exact attainment
  of the intersection-cut efficacy supremum.

The literature agent owns verification of the precise Renegar Part III,
GLS, and inspected ZIB-report references; this reviewer did not undertake
literature research. A final citation-only substitution identifies the
inspected 2020 ZIB report in both Case 4 passages; mathematical text is
unchanged, and the hashes below include that substitution.
The final local label/control-character check was repeated after these
edits and passed. SHA-256 hashes of the actual reviewed TeX files are:

| File | SHA-256 |
| --- | --- |
| `sections/02-corners.tex` | `eefc219d2533eff355d98b4424e3a5668a3f8c4cff23d1a03158edfc77010dd3` |
| `sections/03-quadratic-geometry.tex` | `44f92e2971692e6d967e3cd809033170eb7ca376daa1673ef95d824189a5d32e` |
| `appendices/A-foundations.tex` | `c59d673ab59dc6f9155317d13450dcc46178f4cff9de658378a1c2830d500116` |
