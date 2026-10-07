# Opus editorial review, round 1: preserved interim findings

The reviewer sent these findings before its task ended with a Claude API
rate limit. A complete final report was not produced. This file preserves
the substantive findings, rather than treating the failed task as a
completed review. Locators refer to `complete-editorial-draft-r1`.

**P1, major.** Exact-arithmetic `sections/10-recourse.tex`,
`rem:recourse-quartic`, already contains this manuscript's noisy-core
quartic consequence, `thm:lim:posslp(c)`. Remove the implied novelty in
`09:758–762` and `G:179–182`. The companion also contains a positive
full-selected-optimizer theorem for residual-convex cubics,
`thm:recourse-cubic`, with core-only noise and no residual modulus or
convexifier, and `thm:recourse-convexified` with a supplied convexifier.
The unqualified residual-point statements in `01:104–111,336–341`,
`09:614–635`, `07:665–669`, and `10:130–136` must account for the cubic
case and scope the obstruction to quartics. List the positive companion
results in the overlap comparison. The recourse opening `07:3–7` also
nearly repeats the companion's opening and should be rewritten.

**P2, major.** The decomposition-aware companion describes a deterministic
growth-conditioned graded-grid algorithm with
`f(p,kappa)(I+q+1)^5` work and exact `f1(p,kappa) I^{O(1)}` output. It
compares graded `sqrt(kappa) log(n+2)` coordinate counts to uniform-grid
`sqrt(n kappa)` counts (`growth-sharp.tex`, `prop:sharp`) and gives an
rETH lower bound on the exponent of kappa (`limits.tex`,
`prop:lbproduct`). The manuscript's companion paragraph and sparse scope
understate this comparison. Explain why the linear small-growth tail alone
does not control high inverse-growth moments, rather than claiming that
every width-FPT algorithm must use certified conditional values.

**P3, moderate.** The sparse-indicator companion perturbs only the binary
indicator penalties by an independent uniform grid draw. It gives exact
answers on every draw for fixed treewidth and a numerical-dependence
complexity obstruction. Describe this precise relationship instead of
calling its perturbation model merely different.

**P4, major.** FPT claims must include the numerical ratio in the parameter.
If `L/sigma` grows polynomially with input length, the displayed
`(1+L/sigma)^{O(k)} poly(I)` bound is polynomial for fixed k, not FPT in k
alone. Fix abstract `00:9–11,16–18`, results table `01:148`, and all
summaries consistently with the already precise model definition.

**P5, major scope correction.** Algorithm-constructed finite laws do not
automatically cover exogenous uncertain cost distributions. Two-stage
analogies permit first-stage variables only in second-stage costs; general
second-stage feasibility coupling is excluded. The conservative
nonquadratic strong-field sufficient scale contains the astronomical
solver base `c_d`; disclose this severe numerical condition and distinguish
the smaller quadratic weight `a_i=3`. The reviewer's suggested practical
verdict was not accepted without performance evidence; see the root
disposition record.

The root decisions and required responses are in
`review-disposition-editorial-r1.md`. Luna owns verification of exact
companion theorem scopes and citation identities. No external literature
search was performed by this reviewer.
