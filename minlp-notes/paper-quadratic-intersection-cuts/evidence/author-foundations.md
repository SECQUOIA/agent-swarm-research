# Foundations author report

Completed files:

- sections/02-corners.tex: general corner values and closure, attainment,
  cone containment, boundary examples, rank/inertia support reduction,
  algorithms, hardness, and the unrestricted first-round triangle example.
- sections/03-quadratic-geometry.tex: Lorentz classification and slicing,
  point-rule restrictions, determinant orbit and completion, orbit feasibility,
  tangent pencil, exact starting counterexamples, and maximal wedge.
- appendices/A-foundations.tex: full proofs and exact certificates, the second
  rational example, the constant-direction closure limit, and efficacy oracle.
- evidence/audit-foundations.md: 53-item claim inventory, corrections,
  replacement arguments, and exact-check record.

The required section labels are fd:section and fd:geometry-section.
All definitions use the shared constraint-space notation.

## Original-to-manuscript coverage

| Original statement | Final statement/proof | Disposition |
|---|---|---|
| §1 validity, cut LP value | fd:cut-value and preceding discussion | Includes zero-cost/infinite-step convention |
| Theorem 1(1)–(3) | fd:single-cut | Full direct proof; background attribution |
| Theorem 1(4), Fritz John remark | fd:attainment, fd:attainment-proof | Full noninjective-image proof and multiplier identity |
| Theorem 1(5) | fd:dominant | Direct separation proof |
| Proposition 2(a),(b) | fd:boundary-examples, fd:boundary-proof | Both examples, plus finite zero-cost variant |
| Lemma 3 | fd:rank-support | Exact convex-hull identity and optimization statements |
| Theorem 4 | fd:inertia | Full regular and abnormal proofs |
| Theorem 4 reverse-convex/bilinear/two-variable remarks | Paragraph after fd:inertia | Corrected complement hypothesis and min(k,rho) language |
| Theorem 5(1),(2) | fd:algorithms, fd:algorithm-proof | Decision, relative approximation, degeneracy-safe normal fan |
| Theorem 5(3) generic formula | fd:generic-kkt | Denominator, multiplier, and feasibility restrictions |
| Theorem 5(3) two-ray cases | fd:two-ray, fd:two-ray-proof | Positive-root, singular, and identity cases |
| Theorem 5(4) | fd:hardness, fd:hardness-proof | Rational decision and relative approximation hardness |
| Efficacy remark | fd:efficacy | Specified metric, separation oracle, bounded weak optimization |
| Proposition 6 | fd:fixed-rule, fd:fixed-rule-proof | Exact fixed-coordinate formulas and vanishing ratio |
| Remark 7 | fd:constant-family | Analytic pointed perturbation proves closure limit |
| Theorem 8(1)–(3) | fd:lorentz, fd:lorentz-proof | Elementary classification, orbit, slice, lineality proofs |
| Theorem 8 two-variable and SOCP consequences | Text after fd:lorentz | Supremum exactness; no universal attainment |
| §6.1 span, angle, chord | fd:point-rule, fd:point-rule-proof | Exact criterion; dimensions stated |
| §6.1 varying-apex gloss | fd:asymptotic-example | False gloss replaced by maximal quadrant exclusion |
| §6.1 numerical scans/enlargements | Computation/evidence author | No scans rerun; numerical status preserved |
| §7 nonlocal hull | fd:nonlocal-hull, fd:polytope-proof | Includes empty feasible set |
| Proposition 9 | fd:rank-one-example, fd:polytope-proof | All bases and second round accounted for |
| §8 rank-two classification | Bilinear subsection opening | Supremum qualification |
| Lemma 10(1)–(3) | fd:orbit, fd:orbit-proof | Group, orbit, freeness, positive contact branch |
| Lemma 10(4) | fd:completion, fd:completion-proof | Dual decomposition, finite lowering, exact exception |
| SCIP Case 4 identification | Text after fd:completion | Cited cap-support identification |
| Theorem 11(1),(2) | Text after fd:two-ray, fd:bilinear-attainment-proof | Two-ray complexity and independent-support attainment argument |
| Proposition 12 | fd:orbit-sdp | Exact target feasibility and strict-LMI normalization |
| Lemma 13 | fd:tangent-pencil, fd:pencil-proof | Sign/orientation corrected; ruling case included |
| Theorem 14(1)–(3) | fd:counterexample, fd:counterexample-proof | Polynomial identity, pencil witnesses, strict limit proof |
| Theorem 14(4) | Final paragraph of fd:counterexample-proof | Open-neighbourhood gap/attainment proved |
| Second rational instance | fd:second-example | Six-edge/facet certificate and strict A gap; B unasserted |
| Remark 15 wedge/ruling ties | fd:wedge, fd:wedge-proof | Full maximality and exact multi-contact exclusion |
| Proposition 16(1),(2) | fd:support-one, fd:support-one-proof | Polynomial identity and integer PD certificate |
| §8.6 random/adversarial values | Computation and depth authors | Corrected and qualified; no reruns |
| Literature Proposition A | fd:cone-attainment, fd:cone-proof | Direct dual-vertex domination, zero and infinite values |
| Bilinear cone-containment equivalence | Text following fd:det-model | Midpoint proof of conv(S)=R3 gives the exact full-cone equivalence |
| Printed/corrected KY corollary comparison | Prior-work discussion and audit item 52 | Draft comparison, no essential dependency |
| Literature Proposition B | fd:bcm | Rotation identity, lineality, opposite-side exclusion |

## Mathematical repairs

1. “The closure of the complement is convex” does not ensure freeness.
   The manuscript assumes the complement itself is convex.
2. The pencil multiplier is positive after orienting d_x>0; generally
   its sign condition is theta*d_x>0.
3. Orbit completeness implies exact supremum, not universal attainment.
4. Varying the affine apex does not generate maximal sets with only
   asymptotic contacts under the point rule. The exact quadrant example
   asserts set exclusion, without claiming a point-rule bound gap.
5. Completion maximality treats the exact empty class F12=0,F11<0.
   All other positive-determinant completions are proved maximal.
   Closure/lowering on the positive slice is proved explicitly.
6. Both original simplex-minimum assertions use nonnegative polynomial
   identities covering every face. The second rational example has six
   exact edge polynomials and indefinite-Hessian checks for every face.
7. Strictness and the neighbourhood theorem use compactness and continuity,
   without an unsupported limit-set freeness statement or KKT sketch.
8. Wedge maximality uses explicit interior mixtures and ruling contacts.
9. Relative approximation includes finite-positive and bit-size conditions;
   the fixed parameter is sharpened to min(rank P,rho), and the normal-fan
   perturbation preserves unperturbed costs.
10. Efficacy has a specified norm, separating witnesses, and a bounded
    epigraph with explicit inner/outer balls for weak linear optimization.
    The verified GLS monograph Corollary 4.2.7 supplies that equivalence.

## Exact verification

Targeted symbolic scripts expanded both homogeneous positivity identities
(zero residuals), all edge polynomials and projected facet determinants for
the three starting tetrahedra, the first corrected oriented pencil and its
scalar witnesses, and the second pencil's endpoint discriminants. The second
example has
K_A(v3)=[-1/14-3*sqrt(14)/7,-1/14+3*sqrt(14)/7] and ray determinant
-6083/8. These are proof arithmetic, not experiment reruns.
An own-file static check also passed: theorem/proof environments balance,
foundation labels are unique, and no bare command typos or stale active
proof placeholders remain.

The lead ran the integrated manuscript build. This author did not run
project-wide verification or inspect CI. Independent review inspected the
actual TeX and corrections were incorporated.

The algebraic-decision/QE citation is the inspected Part III of Renegar
(1992), Theorem 1.1, PDF pages 1–2, under the distinct bibliography key
Renegar1992PartIII. The metadata-only Part I citation was removed.
The efficacy argument cites the inspected GLS monograph Corollary 4.2.7.
The Case 4 formula citations use the inspected November 2020 ZIB report
under ChmielaMunozSerrano2020ZIB, rather than the uninspected journal text.
Final review also covers the explicit bounded epigraph, rational
inner/outer-ball encoding, bilinear midpoint cone equivalence, and
rank-based algorithm parameter.
The final independent review passes, and its recorded SHA-256 hashes match
all three current foundation TeX files after the citation-only substitutions.

Other authors may reference fd:single-cut, fd:attainment, fd:dominant,
fd:cone-attainment, fd:rank-support, fd:inertia, fd:algorithms, fd:two-ray,
fd:hardness, fd:lorentz, fd:point-rule, fd:orbit, fd:completion,
fd:orbit-sdp, fd:tangent-pencil, fd:counterexample, fd:support-one,
and fd:wedge. General sharp contact/depth criteria remain with the depth
author, restricted closures with the closure author, and later minor and
reoptimization results with their authors. No proof depends on an internal
research note.
