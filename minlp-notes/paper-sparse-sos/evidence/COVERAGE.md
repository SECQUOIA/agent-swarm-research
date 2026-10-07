# Result-to-section coverage

Initial mapping by the main writer, 2026-10-05; updated after the final GPT
proof reviews, 2026-10-06 UTC. Every included result is now written and
reviewed. Paths of sources are relative to
`research-20260928/solver/`. Audits are under `evidence/AUDIT-*.md`.

| Result (public label) | Section / owner | Primary source | Audit evidence | Novelty stance | Status |
|---|---|---|---|---|---|
| Notation, cones, hierarchies, weak duality (`def:cones`, `def:sparse-hierarchy`, `lem:zero-decomposition`, `lem:weak-duality`) | 2 / main | all notes | AUDIT-KERNELS (standalone statements); reviews/setting-sol-r1.md | standard | reviewed |
| Private-degree-two hierarchy (`def:rec-model`, `def:rec-hierarchy`, `eq:rec-size`) | 2 / main | `partial-kernel-rounding.md` §1, `affine-recourse-kernel-upper.md` §2 | AUDIT-RECOURSE | hierarchy design follows partial lifting precedents | reviewed |
| Chebyshev moment bound (`lem:cheb-moment`), compactness and Slater (`lem:compact`, `lem:slater`) | 2 / main | `sparse-putinar-kernel.md` (26)–(27) | AUDIT-KERNELS "Moment positivity" | standard | reviewed |
| Interval positivity with degrees (`lem:interval-sos`) | 2 / main | cited | AUDIT-KERNELS ext. item 1 | classical (citation from Luna) | reviewed |
| Junction-tree gluing (`lem:gluing`) | 2 / main | `sparse-kernel-rounding.md` §4 | AUDIT-KERNELS | classical (Lasserre 2006; Vorob'ev) | reviewed |
| Jackson kernel (`lem:jackson`) | 3 / kernel | `sparse-kernel-rounding.md` §3 | AUDIT-KERNELS | classical | reviewed |
| Full-preordering rounding `O(r^-2)` (`thm:pre`) | 3 / kernel | `sparse-kernel-rounding.md` §2–5 | AUDIT-KERNELS | rate NOT new (Magron slides 2025/2026); proof/constants/rounding presented as self-contained | reviewed |
| Grid extraction (`cor:pre-grid`), real certificate (`cor:pre-certificate`) | 3 / kernel | same §6 | AUDIT-KERNELS | grid+DP established; comparison only | reviewed |
| SOS kernel interface (`lem:sos-kernel`) | 4 / kernel | `sparse-putinar-kernel.md` §3 | AUDIT-KERNELS | Gribling–de Klerk–Vera prior | reviewed |
| Ordinary-module exact consistency, `C_f O(log^3 r/r^2)`, no bag-count factor (`thm:mod`, `cor:mod-rate`, `cor:mod-certificate`) | 4 / kernel | `sparse-putinar-exact-consistency.md`, `signed-kernel-final-audit.md` | AUDIT-KERNELS | candidate contribution, priority qualified | reviewed |
| Approximate-consistency variant (optional remark) | 4 / kernel | `sparse-putinar-kernel.md` §4–5 | AUDIT-KERNELS "Gluing" | superseded by `thm:mod` | omitted; superseded by exact consistency |
| Moment matching = 2 x best approximation (`prop:moment-matching`) | 5 / kernel | `quadratic-sharpness.md` §1 | AUDIT-KERNELS | prior (Han–Jiao–Weissman) | reviewed |
| Fixed quadratic `Theta(r^-2)` preordering; `Omega(r^-2)` for ordinary module; dense order 2 exact (`thm:quad-sharp`) | 5 / kernel | `quadratic-sharpness.md` | AUDIT-KERNELS | candidate (quantitative); qualitative obstruction prior (Nie–Qu–Tang–Zhang Ex. 6.7) | reviewed |
| Exact orders one and two (`prop:exact-orders`) | 5 / kernel | `quadratic-exact-gap-frontier.md` | AUDIT-KERNELS (symbolic recheck) | modest benchmark | reviewed |
| Fixed private polytope `O(r^-2)` (`thm:fixed-recourse`) | 6 / recourse | `partial-kernel-rounding.md` §2 | recourse audit | combination; ingredients prior | reviewed |
| Private quadratic bounds needed (`prop:private-bounds-needed`), convexity needed (`prop:convexity-needed`) | 6 / recourse | `partial-kernel-rounding.md` §3 | recourse audit | supporting | reviewed |
| Affine recourse `O(1/r)` (`thm:affine-recourse`) | 6 / recourse | `affine-recourse-kernel-upper.md` | recourse audit | combination; Hoffman mean repair has precedent (Zhang–Zhong) | reviewed |
| `Theta(1/r)` example, both hierarchies separately (`thm:affine-sharp`) | 6 / recourse | `affine-recourse-rate-boundary.md`, `affine-recourse-upper-prior.md` | recourse audit | candidate quantitative boundary | reviewed |
| Dual statement for private-degree-two hierarchy (`prop:rec-dual`) | 6 / recourse | AUDIT-RECOURSE §7 | reviews/recourse-duality-sol-r1.md (accepted) | supporting | reviewed |
| Grid/QP baseline (`rem:grid-baseline`) | 6 / recourse | `partial-kernel-prior.md`, `affine-recourse-upper-prior.md` | — | comparison | reviewed |
| Regular multipliers `O(r^-2)` / `O(r^-(1+beta))` (`thm:reg-cheb`, `thm:reg-holder`, `lem:half-degree`) | 7 / recourse | `active-region-rates.md` | recourse audit | candidate; QP sensitivity prior | reviewed |
| Regular sharp example, strict convexity insufficient (`ex:reg-sharp`, `ex:strict-convex-insufficient`) | 7 / recourse | `active-region-rates.md` §4 | recourse audit | supporting | reviewed |
| Constraints with global error bound (`thm:constr-pre`, `thm:constr-mod`) | 8 / extensions | `general-constraints-kernel.md` | AUDIT-EXTENSIONS §1–3 | dense exponent prior (Tran–Toh; lift composition); log refinement and sparse consistency are the additions | reviewed |
| Exact-density domination variant of constrained ordinary theorem | 8 / extensions | AUDIT-EXTENSIONS §4 | reviews/developments-sol-r1.md (accepted) | optional | reviewed |
| Common Slater regime, global vs local geometry (`prop:convex-slater`, `ex:global-local`) | 8 / extensions | `general-constraints-kernel.md` §5, `general-constraints-prior.md` | AUDIT-EXTENSIONS | supporting | reviewed |
| Constrained moment/certificate supremum equality and strict-slack certificates (`prop:constr-dual`) | 8 / extensions | Developed during final review from the full box order unit and separator quotient | reviews/constrained-duality-gpt-r1.md | supporting; no priority claim | reviewed |
| Finite-state preordering (`thm:finite-state`) | 8 / extensions | `mixed-discrete-extension.md` | AUDIT-EXTENSIONS §5 | direct consequence | reviewed |
| Finite-state ordinary module (`thm:finite-state-mod`) | 8 / extensions | AUDIT-EXTENSIONS §6 | reviews/developments-sol-r1.md (accepted) | new development, priority qualified | reviewed |
| Rational certificates with slack (`thm:rational`), ordinary module (`cor:rational-mod`) | 9 / extensions | `rational-sparse-certificates.md` §1–6 | AUDIT-EXTENSIONS §7 | specialization of established methods; ordinary version already in source §6, not new | reviewed |
| Unified rational contract at both rates | 9 / extensions | AUDIT-EXTENSIONS §7.6 | audit final contract | supporting | reviewed |
| Higher-order exactness `rho_r = -2E_{2r}(h)` | 10 / main | `quadratic-exact-gap-frontier.md` §4 | AUDIT-KERNELS | conjecture only | reviewed |

## Historical drafting records

The following records describe earlier snapshots and dependencies, not
the final manuscript's status.

Introduction and discussion (`sections/01`, `10`) cite the public labels
above. They must be re-read after the technical sections settle, in
particular for: constants dependence of constrained ordinary bounds on the
number of bags; inclusion of `prop:rec-dual`, `thm:finite-state-mod`.

Main-writer sections drafted 2026-10-05: `sections/00-abstract.tex`,
`01-introduction.tex`, `02-setting.tex`, `10-discussion.tex`. Targeted check:
`latexmk -pdf -interaction=nonstopmode -outdir=/tmp/sparse-sos-build main.tex`
(run in `paper-sparse-sos`) exited 0 with no LaTeX errors; undefined
references are exactly the public labels owned by Sections 3–9, and all
citations are undefined because `literature.bib` does not exist yet.

Section 2 repairs after `reviews/setting-sol-r1.md`: R1 (rectangular vs
total-degree comparison restated, no inclusion), R2 (odd-degree interval
proof for all `deg p = 2j-1 <= 2k-1`, `k >= 0`, negative-degree SOS cones
`{0}`), R3 (option 2: `w >= 1`, `r >= 1` scoped to box parts; Section 8
states finite-state/empty-bag/order-zero conventions), R4 (nondegenerate
intervals), R5 (`N` includes 0); also nonempty feasible set wording for the
recourse model and "every sufficiently high order" for the unboundedness
example. Rebuild with the same `latexmk` command exited 0, no LaTeX errors.
Open: exact conic duality theorem locator in `bental2001-lectures-modern-convex`
(Luna).

## Final proof-review coverage

| Manuscript scope | Final GPT report | Outcome |
| --- | --- | --- |
| Sections 2–5 and front-matter interfaces | `reviews/final-kernels-gpt-r1.md` | Accepted; no unresolved mathematical defects. |
| Sections 6–7, private-degree-two interfaces, Appendix B | `reviews/final-recourse-gpt-r1.md` | Accepted; no unresolved mathematical defects. |
| Sections 8–9 and their interfaces | `reviews/final-extensions-gpt-r1.md` | Accepted after rational local-data premise was clarified. |
| Full-manuscript prose and claim correspondence | `reviews/final-editorial-gpt-r1.md`, `reviews/final-integration-gpt-r1.md` | All editorial findings repaired and verified; accepted for prose and final citation integration. |
| Constrained certificate closure and updated public claims | `reviews/constrained-duality-gpt-r1.md` | Accepted; exact strict-level membership at the proved rates, without boundary attainment. |

The earlier build records above describe historical draft checks. Final
bibliography integration, source checks, PDF build, and archive validation
are recorded separately in `VERIFICATION.md`. The optional approximate
consistency variant was omitted because the stronger exact-consistency
theorem is proved. The constrained exact-density domination refinement,
finite-state ordinary-module theorem, and recourse value/certificate
supremum equality are all integrated. The final constrained-duality
development also gives real certificates with arbitrary positive slack
at the same finite-order error budgets, without strict moment feasibility.
