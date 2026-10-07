# Points and constraints changed-scope review, round 2

The revised points and constraints proofs pass this round. All round-one findings and the three small precision findings identified during this round are resolved in the final inspected files. P1–P10, C1–C8, and M1–M5 retain their scope and proof chains. I found no new mathematical blocker or unresolved proof correction in this scope.

This internal review is dated 2026-10-05. Its primary files are `sections/02-points.tex`, `appendices/C-points.tex`, `sections/05-constraints.tex`, and `appendices/D-constraints.tex`. I read both round-one reports and the actual revised files, using `evidence/authoring/repair-points-constraints-algebraic-r1.md` to locate changes rather than treating that response as verification. I checked the relevant model, introduction, abstract, root-gate definition, selector proof, and supplied Luna literature report. A delegated independent review rechecked the changed constraint steps and refreshed those files. No manuscript file was edited; only this report was written. No literature research, experiment, mathematical script, historical checker, compilation, project-wide check, or CI inspection was run. Q13/Q14 are outside this round's scope.

## Resolved points findings

| Change | Actual location | Verification |
| --- | --- | --- |
| Fixed-degree input accounting | `02-points.tex:582–587`, `:635–636` | Both examples have Θ(n) nonzero monomials with full exponent vectors of Θ(n) entries and constant-size coefficients. Their explicit box data do not raise the order beyond Θ(n²). Thus `L=Θ(n²)` is correct. The P8 bounds become `2^{Ω(√L)}` and are correctly described as superpolynomial in L, exponential in n. The dense and sparse P9 output bounds remain valid. |
| Output-size qualification | `02-points.tex:604–610`, `:674–676` | The text now identifies dimension-exponential output sizes and distinguishes paths from the multiplier rectangle's treewidth-two graph. No exponential-in-L claim is introduced. |
| Certificate reference | `02-points.tex:28–34` | Exact representations point to the model definition; enclosing boxes point to the actual rectangle proposition. |
| Interaction graph and bags | `02-points.tex:453–456`; `C-points.tex:1050–1057` | The graph is defined before its first use in Section 2. A term's variables contain every edge of its expanded monomials, and connected occurrences in the displayed bag trees give a tree decomposition. Bags of at most three vertices prove treewidth at most two. The paragraph explicitly applies only where a treewidth bound is claimed; it does not impose that bound on the unrestricted PosSLP gate construction. |
| Square Root Sum attribution | `02-points.tex:448–451` | The imported result is correctly stated as polynomial-time computation with a PosSLP oracle. The manuscript's own deterministic closure theorem supplies the many-one consequence. The two ingredients are attributed separately. |
| Root-gate output | `02-points.tex:632–633`; relevant definition `06-algebraic.tex:118–123` | The positive recurrence uses n−1 additions and n−1 square-root gates. All radicands are positive, so it fits the stated root-gate contract. It is no longer described as an ordinary rational circuit computing irrational coordinates. |
| Selector dependence on R | `02-points.tex:50–52`, `:198–208`; `C-points.tex:458–506` | The added `log R` term is necessary and agrees with the actual parameter. The unbounded-optimal-set proof still bounds the projection error by `2R`, retains the factor 4, and uses the original minimum-norm selector. The exact formula is `log₂(1/τ)=(2d−2)q+O(d)+d log₂R+d log₂Γ`. The final summary also includes the additive 1 needed at zero precision. |

The actual abstract now charges numerical degree, and the introduction states regularization approximation at accuracy 1/2 and distinguishes the path enclosure from the treewidth-two multiplier enclosure. These repairs resolve the corresponding round-one scope and output-contract discrepancies. Bibliography integration remains a separate task for the root; an unintegrated vetted record is not an analytic proof defect.

## Resolved constraints findings

| Finding or interface | Actual location | Verification |
| --- | --- | --- |
| R1: fixed-arc KKT exception | `D-constraints.tex:837–840`, `:859–861` | Only arcs with positive capacity impose reduced-cost sign conditions. A fixed arc has no residual arc, and its difference term is zero in the convexity comparison. The round-one opposite-fixed-arcs counterexample no longer applies. The potential bound and strict artificial-arc exclusion remain valid. |
| R2: operation count and isolated nodes | `D-constraints.tex:801–813`, `:876–877` | The source contract is restricted to a nonempty arc set with no isolated nodes, and `log(m'+2)` handles a one-arc graph. Isolated demands are checked in `O(|V|)` comparisons. Deleting isolated nodes after fixed-arc substitution is valid because feasibility has already been established. The circuit solver's count is polynomial in the original graph encoding. |
| Finite lower-bound shift | `D-constraints.tex:884–887` | For `s=y−ℓ`, demands become `b−A_Gℓ`, capacities become `[0,u−ℓ]`, and `a y²+c y` has linear coefficient `c+2aℓ`. The discarded term is constant. The printed capacity and demand transformations are computed once; Taylor coefficients use a constant number of new circuit gates per arc. This supplies the exact interface needed by the artificial-cost lemma. |
| R3: multiplier statement | `D-constraints.tex:1342–1345` | The text now says that the proof uses no bound on the multiplier norm. This is accurate and preserves the complementary-slackness identity used to bound the residual objective. |
| R4: coordinate margin | `05-constraints.tex:1003–1006` | The text distinguishes the absent inverse-polynomial input promise from the available doubly exponential separation bound. It does not assert that the designated output coordinate is tiny and now states only the absence of a uniform polynomial-precision guarantee. |
| R5: all-fixed box | `D-constraints.tex:759–763` | The sole feasible point is evaluated rationally and every original bound is active. The proof avoids an empty-index maximum or zero-variable Newton call. |
| R5: no remaining arc | `D-constraints.tex:873–876` | Feasibility is checked first. The original fixed arc values supply the unique flow, both bounds are reported active, and the observable is evaluated directly. The arc-free source contract is never invoked. |
| Known zero optimum | `05-constraints.tex:992–994` | Subtracting 1/4 preserves every minimizer and all Hessian identities and Hessian Grams. It gives known optimal value zero for both the base binary objective and its full joint Gram correction. No assertion about objective SOS factors is added. |
| Nonlinear-dimension accuracy wording | `05-constraints.tex:410–413` | The printed precision bound is now described as exponential in n in the unrestricted nonlinear-dimension case. The ordinary FPT theorem and its absolute input-length exponent are unchanged. |

The revised flow and box branches still preserve the exact observable and active-bound outputs. No arithmetic operation now depends on expanded circuit lengths. The primal–dual cut, complete candidate-list, rank sampling, and full joint binary Gram proofs were not weakened by the local changes. The ordinary list still contains every optimal integer block, exact selection still handles equality through the appropriate product-fiber observable, and the deterministic one-sign compiler still does not absorb Las Vegas or nondeterministic computations.

## Additional round-two findings, now resolved

1. **Low: selector cost at zero precision — resolved.** At `02-points.tex:52`, the final text gives `O(d(1+q+log Γ+log R))`. The allowed case `q=0`, `Γ=R=1` no longer makes the displayed bound zero. This agrees with the Θ(d) denominator-bit contribution from the actual τ and its exact formula at line 208.

2. **Low: uniform approximation guarantee — resolved.** At `05-constraints.tex:1005–1006`, the final text says: “That separation bound gives no guarantee that fiber values approximated to polynomially many bits certify the bit.” This correctly states the insufficiency of the general separation bound as a uniform polynomial-precision guarantee, without asserting failure on every individual instance. The PosSLP-hardness theorem is unaffected.

3. **Low: LP terminology after source clearance — resolved.** At `05-constraints.tex:54–55`, `:280–281`, and `D-constraints.tex:31–32`, `:192–193`, the final text describes an arithmetic count independent of objective and right-hand-side lengths or dependent only on the encoded constraint matrix. This matches the vetted Luna report at `evidence/literature-review.md:72`. The actual E3a numeric contract at D:198–204 still correctly charges `bits(D_0)`, which is all the normal-cone proof needs. No stronger LP claim is used.

The root's GLS and Végh clearances and the inspected vetted report supply the required weak-optimization, retained-ball ellipsoid, fixed-matrix LP, and exact quadratic-flow interfaces. The current proofs retain their own exact feasibility repair, rational circuit simulation, and graph preprocessing. Missing bibliography keys are not counted as unresolved proof findings in this round.

## Refreshed versions and targeted checks

The final inspected SHA-256 values are:

```text
sections/02-points.tex
09ece21b7bee335f18dcff4cd166b460bf4a434a36d6fdd9b07576c5d0d88442

appendices/C-points.tex
0469412f5fc0bb8a9122329e673a30690a2c6ddf9eb577f3844e7b39f04bde90

sections/05-constraints.tex
78e9d62b533d19edabf1b4c144ccf8f75b2e1153b95c37e37c227edccff8572e

appendices/D-constraints.tex
412eed3537513220a6b9249d0b693ede06de4657dee4c88f15ede03d00e06607
```

Actual targeted work used `sed`, `nl`, and `rg` for source and response inspection and `sha256sum` on these four files. The final repeated hashes matched the values above. `git diff --no-index --check /dev/null paper-exact-arithmetic/evidence/reviews/points-constraints-r2.md` produced no whitespace diagnostics; status 1 records that this new file differs from the empty file. No check performed here duplicates CI, and no executable mathematical diagnostic supports the verdict.
