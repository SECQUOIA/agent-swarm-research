# Stage 2 independent review — reviewer 5

Reviewed `sections/02-setup.tex`, `03-geometry.tex`, `04-widths.tex`, `macros.tex`, and the author notes. I checked the proofs and inequality directions independently, including the unbounded-set localization. Later exposition, examples, and solver sections are outside this stage.

## Decision

No major issue identified. One minor mathematical improvement should be made before closing the stage: the same minimax proof gives strictly stronger spectral bounds than those stated. The present bounds are valid, so this is not a false-theorem finding.

## MINOR 1 — use the stronger available minimax bounds

In `04-widths.tex`, Theorem `thm:radial-spectrum` and Corollary `cor:exit-spectrum` choose the weaker of the two Courant–Fischer formulas for each side. Since the text proves `w_j^+ <= w_j^-`, the existing displayed interval is wider than necessary.

The already-proved pointwise estimate is

`q_g(h)^(-2) <= R(h) <= 4 C^2 q_g(h)^(-2)`.

Apply the **lower** estimate in

`lambda_j = inf_{dim S=j} sup_{h in S, ||h||=1} R(h)`.

Taking reciprocal extrema gives

`lambda_j >= 1 / (sup_{dim S=j} inf_{h in S, ||h||=1} q_g(h))^2 = 1/(w_j^+)^2`.

Apply the **upper** estimate in

`lambda_j = sup_{codim U=j-1} inf_{h in U, ||h||=1} R(h)`

to obtain

`lambda_j <= 4 C^2 / (inf_{codim U=j-1} sup_{h in U, ||h||=1} q_g(h))^2 = 4 C^2/(w_j^-)^2`.

Thus replace the displayed radial theorem by

`1/(w_j^+)^2 <= lambda_j <= 4 C^2/(w_j^-)^2`.

Exactly the same argument yields the sharper directed-exit statement

`1/(v_j^+)^2 <= lambda_j <= C^2/(v_j^-)^2`.

**Required correction:** swap the profile superscripts in both displayed bounds and swap which Courant–Fischer formula receives the lower/upper pointwise estimate in the proof. Preserve the existing definitions, ordering, endpoint identities, and explanation of reciprocal extrema. This strengthens a main result at no cost in hypotheses or proof complexity. No new numerical test or prior-art claim is needed.

## Mathematical checks supporting the remaining material

- The one-dimensional Dikin argument uses an upper second-derivative bound only before the proposed exit, where it is valid; double integration rules out boundary divergence. The closed ellipsoid inclusion follows by closure.
- Semiboundedness follows from the positive-derivative differential inequality and handles boundary endpoints without differentiating there. Dikin objective support is valid even away from centrality.
- Compact barrier sublevels establish existence; positive tangent Hessians give uniqueness. The centrality derivative and integration of `(1/g)'` give the stated gap–mu inequalities with the correct signs. The attained interval and analytic-center endpoint are correctly specified.
- The residual containment constant follows by substituting the displayed `t_0` into semiboundedness. The pointwise residual controls the needed one-sided gradient for every point in the observed sublevel.
- The difference-body sandwich uses only the decreasing-objective half of the Dikin ellipsoid for the inner inclusion. Both Loewner directions and the condition-number comparison factor are correct.
- The homothetic interior-ball argument supplies the upper spectral edge for every barrier. The lower edges, chord constants, aspect-ratio bounds, minimum-width identity, and barrier-family quantifiers are consistent.
- The uniform exact-gap interval follows by applying asymmetric containment at the analytic center, where the gradient vanishes, and bounding the objective support with the Dikin ellipsoid.
- The canonical slack constant follows from a fixed strictly feasible primal point and complementarity. It does not secretly require a unique dual multiplier or strict complementarity.
- Localization needs only compactness of one positive sublevel, an attained optimum, and a relative interior point. The contracting-ball construction and bounded decreasing rays therefore remain available. It appropriately avoids claiming a global analytic center for the unbounded set.
- The radial profiles are well defined as reciprocal norm gauges; the equatorial sign convention in the directed profiles correctly handles discontinuities and yields the longest-chord endpoint identity.

## Attribution and writing

The stage now credits Peña for objective-gap parameterization and explicitly avoids novelty claims for inverse-square upper bounds. Its Xiong–Freund comparison identifies the primal–dual versus tangent-primal setting and the specific further statements. It does not assert unsupported exclusive priority. The Nesterov sharp-constant locator is transparently secondary to Xiong–Freund, while the manuscript supplies its own proof.

The notation and prose are sufficient for an optimization audience. The intentionally deferred abstract, introduction, examples, and complete prior-work synthesis are not defects of this authoring stage. No additional corrections are requested.
