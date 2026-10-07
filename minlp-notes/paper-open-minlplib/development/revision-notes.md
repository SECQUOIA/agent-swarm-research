# Revision notes (items to apply in the first revision round)

## From the independent eg audit review (development/reviews/sol-eg-audit.md, verdict: verified)
Apply to Appendix F (sections/F-eg-rounding.tex), Appendix B.7 and Section 5 eg text:
1. Power-auditor proof: restrict the floating comparison to arguments whose tolerance product CP*z is normal, or state it only for the eg arguments (all nonzero CP*z on the eg power paths are normal: p >= 2.03e-33 etc.); zero is checked exactly.
2. Natural-enclosure table: elo/ehi are approximations whose errors are covered by the chained term padding, not directed exp endpoints. Thresholds 1.9548e-14 and 1.0778e-14 must be labelled approximate or rounded down (1.9547e-14, 1.0777e-14). The el deficit uses the 3u allowance.
3. Historical bit identity holds for eg_disc2_s only (all 38 chunks byte-identical). For eg_int_s and eg_disc_s: a complete audited certificate was obtained and the historical logs reproduce apart from timings.
4. State Lemma A1's domain restriction: boxes contained in the outward-enlarged roots of these instances (including recursively split pieces) with the stated assertions satisfied. Remove "full run has not been launched yet".
Use the review's trust-base wording (section "Trust-base statement for the paper").
