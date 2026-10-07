# Second mathematical review of the local-rate development

Status: passed for the assigned local theory. The released author revision
and the root's final precision edits resolve every required finding in
`review-local-r1.md`. No remaining proof gap or missing hypothesis was found
in the local contraction, exact quadratic rates, composite expansion, or
boundary development. This verdict concerns those results, not the whole
manuscript or its bibliography.

The review read the complete revised `sections/local-rates.tex` and
`appendices/local-proofs.tex`, the analytic sequential example in
`sections/foundations.tex`, and `evidence/author-lead.md`. The September
theory, proofs, rate audit, brief, and integration notes were studied in the
first round. Final source snapshots have 1,232, 406, and 386 lines,
respectively.

| Result or scope | Second-round conclusion |
| --- | --- |
| `lem:tangent-properties`, `lem:cw`, `thm:tangent-contraction` | Compact support sets, convergence as the tangent cutoff decreases, comparison-box premises, and the robust factor are justified. The zero-gauge singleton is handled before division by its scale. General spectral equality is not asserted. |
| `prop:tangent-eigenrate`, `cor:tangent-rate` | Positive comparison shapes yield the two-sided geometric bound and the kth-root rate. Successive-ratio convergence is claimed only where proved. The zero-eigenvalue case collapses after one round. Generic positive-cutoff floors are upper bounds; a matching lower bound requires the stated feasible neighborhood and positive quadratic upper constant. |
| `prop:quadratic-rows` | The zero-diagonal formula has no division by zero. Fixed coordinates are removed for the contraction test. A zero Hessian gives the identity tangent map and stalling, rather than a spurious contraction. The indefinite-curvature discussion now requires restrictions on feasible directions. |
| `prop:rectangle-map`, `prop:asymmetric-eigenboxes` | The support minimizations are correct. The asymmetric necessity proof uses the unique zero of the single-plane minimum and strict positivity elsewhere; it no longer asserts a false strict inequality between the two relaxations. The exact eigenbox interval and its approximate decimals agree. |
| `prop:two-variable-cutoff-floor`, `ex:many-term` | The positive-cutoff cube map, its exact floor, the containing-start-box extension, and the error ratio are proved. Convex symmetrization gives the complete-graph support minimum and exact stall threshold for every stated dimension. |
| `thm:composite-expansion` and its full appendix proof | The interval, relaxation, and interval-dominance properties are proved together and uniformly on compact shape sets. The proof covers zero factor values, zero-width intervals and boxes, zero first derivatives, inflections, and coefficient sign changes. Both product rules are explicit. The unconditional sign-selection bound now includes opposite signs. Clipping preserves the quadratic coefficient; locally Lipschitz scalar second derivatives justify the cubic remainder. |
| Scalar-factor assumptions | Natural argument intervals must lie in the scalar domains, and the monotonicity claim states the Lipschitz premises. The nonsmooth discussion separates a nonzero absolute-value argument, a kink with an exact direct relaxation, and a smooth final objective whose nonsmooth factorization creates a first-order gap. Objective-only lifted auxiliaries yield the stated quadratic model only with the specified square rules. |
| `thm:boundary`, `lem:boundary-step` and their appendix proofs | The start shape is admissible. The first round uses the coarse constant; refinement starts only when `N>=2`, applies also at the terminal index `k=N`, and converges as the enclosing scale tends to zero. The negative lower-witness numerator is handled before choosing a nonnegative witness. Both positive-cutoff limit cases have the claimed constants. The theorem bounds enclosing free scales, not an actual gauge recurrence. The one-sided zero-gradient extension retains its contraction premise. |
| `thm:local-stall`, `ex:critical-scalar`, stopping discussion | The sufficient contraction and stall tests are not presented as a dichotomy. Strict tangent margins are required when a remainder is present. The critical example has `r*=1`, radii asymptotic to `2/k`, and an `epsilon^(1/3)` floor. Incumbent improvement can tighten outside protected fixed boxes. A unique minimizer alone supplies no contraction hypothesis. |

The sequential comparison is now analytic and uses the defined signed
directional updates. For `r=b/a`, its ratio map is
`(1+5r)/(4(1+r))`, which maps `[1/2,1]` into `[7/12,3/4]`; hence the
untruncated formulas remain valid from a symmetric start. The positive
matrix has dominant eigenvalue `(9+sqrt(17))/32<1/2`, establishing the
claimed strict improvement over Jacobi. The archived `0.705` attribution is
absent from the local theorem text.

Two additional precision issues found on this pass were corrected and
re-read: the strict scalar condition now shares a numerical threshold with
the cited non-strict conditions rather than being equated with them, and
the round-count paragraph assigns zero rounds before using a logarithm
when the initial gauge is already at or below the cutoff floor. The
`tau=0` convention also remains explicit in the sharp-growth gap result.

Final SHA-256 snapshots:

| File | SHA-256 |
| --- | --- |
| `sections/local-rates.tex` | `30a09df4b845062634b5b60584d4127be40add01c3ed5c32dfc9eb8f1c97ff4c` |
| `appendices/local-proofs.tex` | `5d764d0cb323afba53ef96b079424a3525c55b72bef871f1d114d840cf43294c` |
| `sections/foundations.tex` | `825ccbd5c15a5ef19cc06eb27a9d25112e446f57d32273a3d4f35ae51418d58b` |

Verification was analytic and read-only. Targeted commands actually used
were numbered `sed -n` source reads, `tail -n`, `rg --files`, `rg -n`,
`wc -l`, and `sha256sum` on the identified sources and evidence. This
reviewer ran no numerical experiment, solver loop, manuscript build,
project-wide verification, CI inspection, or literature search. Only this
second-round evidence file was written during the recheck. The author
report separately lists numerical development checks; those descriptions
were reported to the root and are not checks performed by this reviewer.
