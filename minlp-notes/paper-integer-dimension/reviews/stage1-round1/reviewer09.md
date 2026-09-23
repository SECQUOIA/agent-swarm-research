# Reviewer 09 — stage1-round1

Primary lens: one-sided inertia, epigraph row complexity, and positive perspectives.

Major findings: 0

Minor findings: 2

## Snapshot and coverage

I read all 1,206 lines of `sections/01-foundations.tex`, the process and review protocol, the coverage inventory, the bibliography, macros, and main file. The following SHA-256 hashes were recomputed and match `reviews/stage1-round1/snapshot.json`:

| File | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |

I checked the full proof chain: parity closure, disjunctions, scalar/product constants, graph allocation, scalar determinant bound, one-sided inertia, principal compression, symmetric shrinking, covariance/capacity and Hall bounds, quadratic upper encoding, smooth oscillatory lower bound, smooth and polynomial upper constructions, constant-rank tubes, and perspective transfer. I compared the corresponding original one-sided, perspective, scalar-rank, constant-rank, covariance, and smooth-map proofs, with particular attention to `results/quadratic-inertia-one-sided-integer-complexity.md`, `results/perspective-integer-precision.md`, and `notes/mip-binary-lower-bound-extensions.md`. I consulted the two specialist original audits only after reconstructing their arguments independently.

For primary-source checks I read the local extracted texts of GGOW Theorems 1.4, 1.17 and 2.18 and relevant Section 2 material; Wolff Theorem A on printed pp. 50–51; Nicola Definition 1.1 and its following paragraph; and the locally retrieved Lubin midpoint lemma and Beach interpolation/epigraph statements. I read `literature/AGENTS.md` first. The official Boyd PDF fetch timed out, so I do not certify its precise section locators. I did not comprehensively verify every bibliography entry, IQS's polynomial-bit algorithm, or Volčič's source statement. The rational algorithm is explicitly previewed for the next stage and is not treated as a missing stage-1 proof. No compilation or visual PDF inspection was performed. These limits do not constitute findings against the mathematics.

## Assessment

I found no major mathematical defect in this stage. The specialist results have the correct orientation of one-sided errors, preserve full unbounded epigraphs/hypographs, and avoid imposing bounds on homogenized continuous auxiliaries. The row-count argument is valid even with equality constraints and lineality. The positive-scale transfer preserves binary count by an exact correspondence at every fixed positive scale, and its lower transfer applies separately to arbitrary convex integer lifts. The qualifications about finite-LP attainment and the cone apex are appropriate.

The other proofs also survived my checks. In particular, the smooth lower bound uses a sufficiently small support for the mixed-Hessian estimate; the tube upper bound controls every point in each polytope, rather than only points assigned to that chart; and the quadratic upper construction retains the original transformed domain. This is a bounded independent audit, not a claim of formal verification or publication priority.

## Findings

1. **MINOR — malformed multiplication in the smooth upper proof.** Location: `sections/01-foundations.tex`, lines 974, 977 and 992, in the proof of `thm:smooth-ranks`. The expressions are written as `C_0,2^{-T}` and `2C_0,2^{-T}`. The literal comma renders as punctuation rather than multiplication and makes the displayed error bound and depth condition malformed. The surrounding proof, and the original smooth-map result, clearly require the products `C_0\,2^{-T}` and `2C_0\,2^{-T}`. Replace the commas with multiplication spacing. This is a notation defect, not a false estimate.

2. **MINOR — the capacity equivalence needs its own source locator.** Location: lines 529–541, especially the blanket citation to GGOW “Theorems 1.4 and 1.17” preceding `eq:capacity`. The checked primary text of Theorem 1.4 states the free-field, matrix-evaluation, shrinking and rank-decreasing equivalences; Theorem 1.17 gives the rank/decomposability characterization. Neither displayed theorem states the positive-capacity equivalence. GGOW develops capacity separately in Section 2 and attributes its framework to Gurvits. The original repository proof included “and Section 2” and explicitly credited Gurvits; that qualification was lost here. Add a separate accurate capacity citation/locator and attribution, or restore the Section 2 qualification with an appropriate source for the arbitrary complex-coefficient equivalence. Do not substitute Theorem 2.18 alone: it is explicitly for integral Kraus operators, whereas `eq:capacity` is used for arbitrary fixed real Hessians. The mathematical equivalence is established; this finding concerns precise attribution and verification of the imported hypotheses.

## Executed independent check

I ran an independently written inline Python/SciPy `linprog` check of exactly the continuous LP displayed at lines 423–425, retaining only its single final shifted lower band. This differs from checking a stronger sawtooth LP with additional tangent cuts. It solved 518 LPs across depths zero through seven, at all dyadic knots and interval midpoints at the tested depth. For each solve it compared the projected lower boundary with the independently computed chord interpolant minus `4^{-L}/4`; it checked graph containment, the one-sided error bound, and attainment of the claimed maximum error. All checks passed (absolute numerical tolerance `2e-8`). The depth-zero error was `1/4`, and the depth-seven error was `1/65536`, as stated. This supports the construction and its indexing; the general proof is still needed and was independently checked above.

No manuscript, bibliography, or original research files were edited.
