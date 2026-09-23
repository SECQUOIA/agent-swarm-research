# Stage 3, round 1 — corrections

Both accepted minor issues have been corrected in `sections/shared-baths.tex`. The current `stage-3-author.md` record has matching wording. No theorem or hypothesis was changed, and no alternative auxiliary construction or new topic was added.

## 1. Auxiliary law under temperature balancing

The balancing subsection now explicitly defines the auxiliary joint law as the new canonical spin law at `beta_N` times the **old** conditional Edwards–Sokal bond kernel at `beta_c`.

Its Radon–Nikodym derivative relative to the old joint law is exactly the new-to-old spin likelihood. Bounded energy per particle and a temperature shift of order `1/N` bound this likelihood above and below by fixed positive constants. This preserves the original positive contour decomposition as a decomposition of the new physical spin marginal. For any phase event, the ratio of its new conditional likelihood to the old one is bounded by the ratio of those constants; the conditional exponential moment remains bounded. The probability of the exceptional event grows by at most the upper likelihood bound. The old joint phase probabilities also remain bounded below.

The manuscript expressly identifies the retained kernel as auxiliary and does not claim that it is the natural Edwards–Sokal kernel at `beta_N`. The spin marginal is exactly the required canonical law, which is all the positive-decomposition theorem requires. The necessity argument continues to use the actual spin phase events and the already proved temperature-shift lemma.

## 2. Positive-variance hypothesis

The final paragraph now calls the linear-capacity statements **positive-variance**, replacing “density-based.” The same correction was made in the current author record. The stated exclusion of the pure-spin mean-field model comes from its zero disordered-phase limiting variance. It does not suggest that continuous microscopic energy densities are required.

## Validation

Checked the auxiliary Radon–Nikodym calculation and the conditional moment/probability inequalities directly against the positive-decomposition requirements. Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in the paper directory. Compilation succeeds; the final `main.log` has no warnings or overfull/underfull box diagnostics. The correction introduces no additional scientific issue requiring a new review round.
