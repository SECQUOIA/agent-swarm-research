# Measured coverage of the native-model cuts

These counts describe the seed-0 full runs. They do not identify the causal effect of native relaxations, reformulation or a different activation policy.

| Suite | Mode | Callback runs | Callback calls | Discovery runs | Supported blocks | Auto-eligible blocks | Unsupported sides | Callback seconds |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| holdout | all | 8/8 | 18 | 8 | 52 | 42 | 130 | 1.912 |
| holdout | auto | 8/8 | 20 | 8 | 52 | 42 | 130 | 1.739 |
| diagnostic | all | 7/7 | 12 | 5 | 52 | 22 | 179 | 4.080 |
| diagnostic | auto | 7/7 | 15 | 5 | 52 | 22 | 179 | 3.273 |
| synthetic | all | 0/0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| synthetic | auto | 0/0 | 0 | 0 | 0 | 0 | 0 | 0.000 |

| Suite | Mode | Mutually exclusive outcome classifications |
|---|---|---|
| holdout | all | added_cuts: 4; discovery_without_supported_blocks: 4 |
| holdout | auto | added_cuts: 2; discovery_without_supported_blocks: 4; supported_blocks_but_none_auto_eligible: 2 |
| diagnostic | all | added_cuts: 2; discovery_stopped_at_budget: 2; discovery_without_supported_blocks: 2; eligible_blocks_without_added_cut: 1 |
| diagnostic | auto | discovery_stopped_at_budget: 2; discovery_without_supported_blocks: 2; eligible_blocks_without_added_cut: 1; supported_blocks_but_none_auto_eligible: 2 |
| synthetic | all |  |
| synthetic | auto |  |

`coverage.json` records instance-level classifications, source-side refusals, support failures, actual-row binding and rounding rejections, selection skips, budget exhaustion, callback/discovery/certification time, and zero-node solves. A model solved without invoking this separator did not need these cuts on that run; it does not show that the cuts can never help. A supported block without an added cut can reflect the bounded direction search, insufficient violation, certification or binding rejection, or the work budget. The recorded counters do not isolate the causal contribution of these mechanisms.

No callback is not itself proof of a presolve solve; zero nodes is reported separately. No cut within the bounded search is not hull membership or proof that native cuts dominate. Block counts overlap and are not unique source-variable counts.
