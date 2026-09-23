# Stage 2 author report

Author: `paper_stage2_author`. Date: 2026-09-07. Status: five independent reviews and accepted minor corrections are complete; coordinator verification is complete and stage 2 is accepted. See `stage2-revision.md`. No reviewer was spawned by the author, and no later stage was started.

## Files and foundation

Added `sections/auxiliary-process.tex` and `sections/log-limits.tex`, included them in `main.tex`, and added five bibliography entries. Updated the claim-level coverage map, workflow status, and README. The accepted `sections/model.tex`, `sections/fractional-moments.tex`, and `appendices/wellposedness.tex` are unchanged; their hashes were checked against `stage1-accepted-snapshot.json`. Existing bibliography entries are unchanged.

Read the four assigned source developments and six designated proof/literature reviews, and checked their claims against the accepted assumptions. The controlled research note’s outdated limitation on parent-dependent existence was not copied. The new estimates require only a specified solution in `def:solution`, while the accepted existence theorem supplies one under finite initial second moment.

## Proof decisions and covered claims

1. **Number process and identification.** The normalized bounded-test equation has daughter rate `2σ` and coagulation rate `λNx`. Measurable quantile maps and independent Poisson drivers give a minimal construction. First-moment localization includes size overshoots and locally integrable, potentially unbounded controls. Uniform stopped count estimates prove nonexplosion. Marginal identification uses the accepted weak loss formula with weight one, retains the full incoming gain on restricted output sets, and dominates the positive finite-jump expansion. Nonexplosion makes that expansion a probability law. No unproved forward-equation uniqueness or Bochner derivative is used.
2. **Interpretation.** The inverse-size Doob relation is an algebraic generator identity, with the established mass representation attributed to Deaconu–Fournier–Tanré. It does not claim a path-space change-of-measure theorem under first moments. Physical mass tags and lineages are explicitly distinguished from this auxiliary number process.
3. **Finite correction.** Nonnegative compensation gives the exact double integral `a(t)`. The inequality `log(1+r)≤√r` and accepted half-affinity estimate make its full-time integral finite. Monotone convergence gives almost-sure and L1 convergence. For finite total activity the integral tail vanishes even though the last exponential upper bound need not.
4. **Finite total coagulations.** The product `exp(F) ∏Θ` has zero conditional drift even with adaptive daughter marks. Finite-horizon boundedness gives a mean-one martingale; Doob’s inequality gives an almost-sure finite global supremum. The coagulation compensator is pathwise finite. A compensator-level stopping argument proves finite event count without assuming integrability of `exp(A∞)`. Expected count remains `Bc(t)` and can diverge.
5. **Controlled path consequences.** Infinite fragmentation activity gives `X_t→0` almost surely. Finite fragmentation activity gives an eventually constant positive finite path. The weak number-law limits follow by bounded convergence, without log moments or parent independence. These are direct consequences requested by the coordinator.
6. **Exact transport.** Parent-independent, possibly time-dependent fractions give an independent marked Poisson reference. The single path coupling is ordered. Increasing clipped identity tests prove optimality without subtracting infinite marginal means. The bounded-test remainder is also given, without unsupported separate log moments for its two components. Adaptive parent-dependent marks are explicitly excluded from the independent-reference assertion.
7. **All constant rates.** Cost and remaining-correction estimates use rate `κ(b+σ)` and constant `λH0²/[κ(b+σ)N0]`. Criticality reduces this to `H0²/(2κmN0)`. The increasing one-time cost and decreasing residual are kept distinct.
8. **Limit theory.** The path LLN assumes the first daughter log moment. The functional CLT assumes the second, specifies Skorokhod J1 on compact time intervals, and reduces the reference to iid centered unit-block increments. A finite-second-moment tail estimate controls the largest within-block fluctuation. The Gaussian variance parameter uses the raw second jump moment times `2σ`. Initial logs need only be finite almost surely for weak/path limits. Bounded truncations also prove the moment-free upper speed and speed minus infinity when the daughter log mean is minus infinity.
9. **Ordinary Wasserstein limits.** An initial first absolute log moment is explicit. The path decomposition propagates first moments. Uniform integrability from the centered reference’s bounded second moments gives its ordinary W1 CLT; the finite paired correction transfers it. The square-root speed estimate and an ordinary W1 LLN with only first moments are both proved, the latter by jump truncation.
10. **General diverging scales.** Every weak reference limit on a diverging log scale transfers, as do path limits when the reference converges in J1. No stable domain-of-attraction statement is claimed without the corresponding reference hypothesis. No density, raw-size-moment, or actual-variance convergence is asserted.
11. **Logarithmic identities.** First log integrability is proved before taking expectations. Geometric means have a finite positive prefactor. The general constant-rate entropy identity includes the count term `b−σ`; criticality reduces to the expected expression. The zero-fragmentation case needs no unused daughter log moment. No mass-weighted log moment or extra entropy-production claim is added.
12. **Pure coagulation.** The monotone finite-cost limit uses the same path and clips. The Borel formula is classical and attributed. The proper critical Borel limit and its infinite arithmetic mean explain the limits of log transport.

The updated `COVERAGE.md` maps every stage 2 item to the relevant theorem, proposition, corollary, or remark.

## Primary sources checked

Read `literature/AGENTS.md` before literature use. No literature package was ingested or altered.

- [Deaconu–Fournier–Tanré (2002), author PDF](https://www-sop.inria.fr/members/Etienne.Tanre/publication/AOP104.pdf): equations (2.3) and (2.6) identify the mass law and generator. Existing metadata retained.
- [Bertoin (2003), publisher PDF](https://ems.press/content/serial-article-files/31511?nt=1): title-page metadata and Theorem 1 checked; the Gaussian limit uses mass weighting. DOI `10.1007/s10097-003-0055-3`.
- [Doumic–Escobedo (2016), publisher record](https://www.aimsciences.org/article/doi/10.3934/krm.2016.9.251) and [open manuscript](https://arxiv.org/pdf/1510.03588): journal metadata, constant-rate scope, and mass-weighted Corollary 1 checked.
- [Bertoin (2009), primary PDF](https://www.numdam.org/article/AIHPC_2009__26_6_2073_0.pdf): equation (3), page 2074, gives the Borel solution and credits Golovin. The paper’s limited-aggregation models are not conflated with the present model. DOI `10.1016/j.anihpc.2008.10.007`.
- [Deaconu–Tanré (2000), Numdam record and article](https://www.numdam.org/item/ASNSP_2000_4_29_3_549_0/): author, journal, series, volume, issue, and pages verified; branching interpretation of additive coagulation cited as established context.
- [Billingsley (1999), Wiley record](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316962) and [Chapter 2 record](https://onlinelibrary.wiley.com/doi/10.1002/9780470316962.ch2): second-edition metadata and Donsker chapter checked. The theorem invoked is the standard iid finite-variance invariance principle; all hypotheses and the compound-Poisson reduction are established explicitly in the manuscript.

## Build and open issues

Built with `make`: PDFLaTeX, BibTeX, and two further PDFLaTeX passes. The final PDF has 19 pages. Final `main.log` and `main.blg` have no warnings, undefined references/citations, or overfull/underfull boxes. Build transcript: `/tmp/ramki-stage2-build.log`.

No unresolved mathematical issue was identified by the author. This does not replace the required five independent reviews. Quantitative last-event tails, daughter extrema, exact critical products, finite-population results, and later applications remain outside this stage.
