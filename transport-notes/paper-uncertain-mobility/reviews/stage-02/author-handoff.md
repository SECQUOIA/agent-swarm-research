# Stage 02 author handoff

Status: author complete and ready for the coordinator's frozen-snapshot five-reviewer round. This is not stage acceptance. The author has stopped editing manuscript files. No later-stage result was developed.

## Files and coverage

- `sections/02-local-baseline.tex`: new complete section, approximately eight pages in the combined 16-page draft.
- `main.tex`: includes the new section after the accepted model section.
- `notation.md`: adds the whole-line and finite-interval response notation.
- `references.bib`: adds Azaïs–Wschebor and Grisvard references.
- `reviews/stage-02/author-sanity-checks.json`: reproducible algebra and coefficient sanity output, not an independent review.

The section covers claims L1–L4, including the stronger uniform-trial bulk result requested by the coordinator:

1. An energy-dual whole-line constant source, uniform anchored coercivity, source-tail bounds, expanding Dirichlet and Neumann intervals, and stability under uniformly comparable locally convergent weights. The Neumann upper limit explicitly uses source-tail control and lower semicontinuity.
2. The harmonic heat-kernel integral, exact gamma coefficient, and compact-circle localization at any finite nonempty set of quadratic zeros. The zero-free alternative is separate.
3. The quartic pair response, continuity, exact fold scaling, both exact whole-line parameter tails, and the precise integrability threshold. Artificial rootless interval endpoints are explicitly excluded from an unjustified joint tail equivalent.
4. Uniform cosine response and spectral-gap envelopes. The compact-fold limit and separated-root matching are separately stated and proved. Moving neighborhoods have radius ratio eta=(epsilon/t^3)^(1/8); their complementary reciprocal-rate contribution has relative order at most (epsilon/t^3)^(1/8).
5. All three uniform-design positive-moment equivalents, with density 1/4, two-fold, Jacobian, and critical logarithm factors tracked. Mean and variance, budget conversion epsilon=M/(2pi), and the exact limiting scalar random-variable law are included.
6. The special exchange-flux identity and uniform O(epsilon^(1/12)) L2 convergence of kh to one. This gives an offset-independent regular bulk remainder and its rate through the accepted Schur identity and an explicit Neumann bulk problem. Its H2 step uses the accepted C2 domain and L2 flow hypotheses.
7. Gaussian amplitude collapse, including the lower bound for adaptive mobility; marked-zero moment context with explicit Gaussian path/noncriticality conditions; and failure of replacing the realized rate by its ensemble mean. No stable-law or general Gaussian averaging result is asserted.

## Author verification and proof boundaries

- Read the relevant source notes and accepted Stage 01 text. Reworked the localization and moment arguments in the manuscript; no proof invokes a repository note.
- Rechecked the heat-kernel double integral and the dual-source cutoff justification.
- Checked the critical logarithm using a retained interval epsilon^b <= t <= t0, first epsilon to zero and then b up to 1/3. The omitted normalized contribution is bounded by C(1/3-b), so the coefficient is determined without extending compact-fold convergence into the tails.
- Checked the direct k'' identity symbolically: the residual is exactly zero. The uniform flux bound uses both independently derived spectral gaps and response envelopes; it is not inferred from the response alone.
- Evaluated the harmonic gamma and heat-integral formulas with 50-digit mpmath. Their difference is approximately 2.53e-27 (a numerical integration check, not an error certificate). Checked the beta mean against C0^2/sqrt(pi), and the rootless reaction integral against pi/2. Output records the critical coefficient 1.628601974379... .
- The pair second-moment coefficient remains an exact convergent integral here. No unverified numerical digits are presented as a certified constant; its numerical evaluation belongs to Stage 07.
- No theorem known to the author has an unresolved gap, but the required independent five-reviewer audit has not yet occurred. This handoff does not assert correctness by author self-assessment alone.
- No stronger scalar additive remainder, joint rootless finite-interval tail, non-Gaussian particle law, or new oscillator/Kac–Rice identity is claimed.

## Primary-source and standard-theorem checks

Read the author-hosted Azaïs–Wschebor draft at <https://www.math.univ-toulouse.fr/~azais/styles/other/student/level.pdf>, Theorems 6.2 and 6.4 (draft printed pages 121–122). The hypotheses are Gaussianity, almost-sure C1 paths, a nondegenerate point law, and almost-sure absence of critical zeros. The weighted formula permits a continuous jointly Gaussian auxiliary field; take the derivative at the root and a singleton auxiliary parameter set. Bounded continuous truncations and monotone convergence handle the singular negative-power marks. The manuscript cites the published 2009 book by theorem number and identifies the linked file as an author draft.

For the standard H2 Neumann regularity used in the stronger bulk limit, checked Guermond's author-hosted chapter <https://people.tamu.edu/~guermond/M661_FALL_2017/chap27.pdf>, Theorem 27.23(ii) and Remark 27.24. They give W2,p regularity for a C1,1 boundary, Lp source, and W^(1-1/p),p Neumann datum, and explain the compatible zero-reaction case. Their referenced primary theorem is Grisvard, Section 2.4 (Theorems 2.4.2.5–2.4.2.7). The manuscript cites that standard book section; the SIAM 2011 reprint metadata and DOI were checked on the publisher page <https://epubs.siam.org/doi/book/10.1137/1.9781611972030>. The full Grisvard chapter was not newly obtained in this stage. No added regularity beyond the accepted C2 domain is needed.

No literature package was created or changed.

## Build and checks

Command, run from `paper-uncertain-mobility/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

The final build succeeds, generating a 16-page PDF. The final `main.log` has no warnings, undefined references, overfull boxes, or underfull boxes. `git diff --check` succeeds. A transient BibTeX warning while replacing the preliminary Assaf citation disappeared after latexmk's normal reruns; the final bibliography contains only the intended references. A transient wrong-relative-path command failed before changing any file and was rerun from the repository root.

The coordinator may now record the pre-review manifest and dispatch all five independent reviewers on this unchanged source snapshot.
