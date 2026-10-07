# Stage 4, round 1: independent reviewer 5

**Verdict: PASS. No required major or minor findings.**

I verified all 22 frozen manifest hashes and read the stage-4 author scope report, integrated abstract/introduction/conclusion, bibliography, verification appendix, README, coverage map, and packaging rules. I did not read other stage-4 reviews. This report concerns integration; it does not substitute for the subsequent full-manuscript review.

## Claims and scope

The abstract now states the rational ground field explicitly. Its simultaneous graph restrictions, fixed numerical data, topology versus rational-equivalence distinction, algebraic-degree conclusion, and residual separation scale match the proved statements. The introduction explains why fixed girth does not imply a tree theorem and distinguishes fixed-data resistive inputs from size-dependent principal-angle cosines.

Real bus angles, principal line angles, and reference-fixed angle boxes remain distinct throughout. Zero reactive injection and common-sign positive-width reactive intervals are presented with the resistive-line restriction. Neither the introduction nor conclusion imports an unrestricted phase-alignment result on a meshed phasor network. Exact feasibility, numerical residual evidence, and the explicit gap-promise certificate result are also separated correctly. The conclusion makes no new mathematical claim requiring an additional proof.

The basic-closed restriction and self-contained arithmetic repair remain intact. The new literature narrative does not revive the defective general Boolean rational-equivalence assertion. It also avoids converting an LMI alternative, a numerical solver bound, or a polynomial-size approximation into an exact Turing algorithm.

## Independent primary-source checks

- **Gan–Low:** I retrieved the primary Caltech PDF and checked the physical DC model and the two scoped SOCP exactness regimes. The introduction accurately distinguishes physical DC from a linear AC approximation and attributes sufficient conditions involving voltage upper bounds and injection lower bounds; it does not claim unconditional exactness.
- **Jeeninga–De Persis–van der Schaft:** The archived Part I text, Theorems 3.18 and 3.22, supports convexity of the demand-feasibility set and both exact and interior feasibility alternatives. The fixed-source constant-power-demand model is distinct from the present arbitrary bus-interval input, as stated.
- **Lehmann–Grastien–Van Hentenryck:** The primary model fixes voltage magnitudes to one and includes active/reactive demands; its reduction uses a star. The introduction's tree/star comparison is accurate.
- **Bienstock–Verma and Bienstock–Munoz:** The former lossless fixed-magnitude scope and the version-specific Section 1.3 approximation question agree with the original arXiv v2 text checked during the earlier review. The archived latter source explicitly states scaled feasibility/optimality tolerance in Theorem 7 and an approximation scheme in Corollary 8. The introduction preserves these limitations.
- **Lavaei–Low:** I independently retrieved its primary Caltech PDF and read Appendix B, Case 2. It discusses resistive admittance and zero reactive bounds, supporting the historical connection credited here. The manuscript does not adopt its unrestricted discrete-phase conclusion. The Dörfler sine-coupling citation remains background only, as checked previously.

The other arithmetic, triangulation, polynomial-minimum, and complexity references retain their already verified roles. The separate journal/preprint entries make the Bienstock–Verma locator unambiguous. All 15 bibliography entries resolve in the final PDF. Initial browser fetches of the two Caltech PDFs timed out; direct retrieval succeeded and the source copies/extractions are retained in my verification directory.

## Verification appendix and reproducibility

I matched all eight table rows to the original source script and independently checked their algebra. The two contradictions follow from `z=1` with `x+y>=2`, and from `x=1/4` outside the source interval. The other six have exactly the listed unique positive source solutions. In particular, the underdetermined-looking sixth row is forced to its boundary by `z=4*x<=2` and `x>=1/2`. Both irrational solutions lie inside the source interval. The unique network-extension conclusion therefore follows from the accepted reduction.

I reran all four frozen exact suites. Their counts agree with Appendix B and the README. I also reran the legacy winding checker: 360 scaled pairs, 4,136 cycles, and 256 nonzero windings. The four historical AC instance sizes and the objective `sum_i f_i^2` match the repository verification record. The text clearly states that these solver runs were not repeated and are not exact proof certificates.

The README supplies the correct entry point, build command, four checker commands, and process/log locations. The coverage map assigns every listed source a destination or explicit disposition. Its preservation of failed historical claims through corrected mathematics is appropriate; a paper need not reproduce the authoring chronology. The ignore rules exclude generated builds and diagnostic images while retaining the source, exact checkers, reports, manifests, and text evidence.

## Build and layout

An independent build from the frozen sources completed successfully with 28 pages and no final warnings, undefined references/citations, or overfull/underfull diagnostics. I inspected the extracted integrated text and rendered final bibliography page. The references fit legibly on one page; the new section and appendix references resolve correctly.

Artifacts are under `/workspace/minlp-notes/paper-power-flow/verification/reviewer5/stage04-round01/`: all five checker logs, the independent build, extracted layout, rendered reference page, and primary-source PDFs/text used above. No manuscript file was edited.

There are no optional changes I consider necessary before advancing to the distinct full-manuscript review.
