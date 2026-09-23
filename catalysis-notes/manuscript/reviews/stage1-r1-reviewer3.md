# Stage 1, round 1 — reviewer 3

Verdict: **approve with minor clarifications; no major issues found.**

Independent review of `manuscript/sections/01-water.tex`, the stage 1 evidence note, source-series JSON, output-check script, bibliography, and main document. Emphasis: equations, balances, uncertainty, useful-output accounting, and the validity of the proposed decisions. Read `literature/AGENTS.md` before consulting the library; made no library changes and did not consult other review reports.

## Minor issues

1. **Define the reference concentration for the two-pool excess.** `manuscript/sections/01-water.tex:40` gives the producing pool's “steady excess” as `q_T/(lambda B_1)` without explicitly saying that this is relative to `c_g`, not the inlet. From the displayed balances, `c_g,ss = c_in + q_T/F`, so `c_1,ss - c_in = q_T/F + q_T/(lambda B_1)`. The pool-to-gas excess changes threefold in the example; the total pool-to-inlet excess generally does not. The nonidentifiability demonstration remains correct. Fix: write `c_1,ss - c_g,ss = q_T/(lambda B_1)` and identify that quantity as the threefold-changing excess.

2. **Specify both absolute rates in each experimental condition.** `manuscript/sections/01-water.tex:85` requests “the four absolute rates,” although line 79 defines two rates, pre-challenge and post-recovery, for each of the four conditions. Four post-recovery rates alone do not expose formulation differences hidden in the retention denominators. Fix: request the pre-challenge and post-recovery absolute rates for all four conditions, alongside the retention interaction and cumulative output.

## Checks supporting the verdict

- Running `python manuscript/evidence/check_water_output.py` reproduces reference **116.0352 h**, promoted **219.8266 h**, ratio **1.89448**, and additive-mass ratio **1.80427**. All four retained arrays match the original XLSX through the existing source loader; the recorded SHA-256 matches the workbook. The common interval is 25–585 h. Simpson integration is exact for the product of the two linear interpolants on each combined interval.
- Checked the consequential Fang platform quantities against its original HTML: catalyst/additive masses, granule size, feed basis, carbon-based selectivity, and approximately 80/175 s responses. The manuscript appropriately calls the calculation a proxy, excludes unobserved startup, avoids statistical precision and lifetime extrapolation, and distinguishes catalyst-plus-additive mass from complete-bed accounting.
- The single-pool balance, differential-storage units, steady excess, and source-feedback relaxation expression are consistent. Summing the two pool balances yields the displayed aggregate system; redistributing capacity at fixed total capacity and common relaxation constant preserves outlet identifiability limits as claimed.
- The external-water ratios, gas demand, and supplied-water estimate are arithmetically consistent. The chapter correctly limits them to planning estimates and does not equate low whole-bed conversion with negligible intragranular gradients.
- The randomized four-condition design, matched handling, absolute-rate endpoints, predefined complete output horizon, independent repetitions, balance uncertainty, and withheld functional prediction address the principal causal and practical ambiguities. The proposal does not need positive experimental data to be complete; its unresolved qualification and measurement dependencies are explicitly identified.
- Prior work is credited without claiming novelty for physical mixing, water cofeeding, or history effects. The original question is appropriately narrower: late addition after common conditioning and a prospective functional prediction. Failure to identify local water transport is not misrepresented as failure of every useful formulation result.
