# Measured coverage of the native-model cuts

These counts describe the seed-0 full runs. They do not identify the causal effect of native relaxations, reformulation or a different activation policy.

| Suite | Mode | Callback runs | Callback calls | Discovery runs | Supported blocks | Auto-eligible blocks | Unsupported sides | Callback seconds |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| holdout | all | 28/30 | 60 | 28 | 156 | 63 | 186 | 27.633 |
| holdout | auto | 28/30 | 61 | 28 | 156 | 63 | 186 | 27.000 |
| diagnostic | all | 8/10 | 11 | 8 | 136 | 37 | 188 | 29.677 |
| diagnostic | auto | 8/10 | 13 | 8 | 136 | 37 | 188 | 28.681 |
| synthetic | all | 6/13 | 16 | 6 | 5 | 1 | 1 | 0.331 |
| synthetic | auto | 6/13 | 16 | 6 | 5 | 1 | 1 | 0.078 |

| Suite | Mode | Mutually exclusive outcome classifications |
|---|---|---|
| holdout | all | added_cuts: 7; discovery_without_supported_blocks: 12; eligible_blocks_without_added_cut: 9; solved_without_callback: 2 |
| holdout | auto | added_cuts: 3; discovery_without_supported_blocks: 12; eligible_blocks_without_added_cut: 3; solved_without_callback: 2; supported_blocks_but_none_auto_eligible: 10 |
| diagnostic | all | added_cuts: 2; discovery_without_supported_blocks: 2; eligible_blocks_without_added_cut: 4; model_not_admitted_or_worker_failed: 2 |
| diagnostic | auto | added_cuts: 1; discovery_without_supported_blocks: 2; eligible_blocks_without_added_cut: 1; model_not_admitted_or_worker_failed: 2; supported_blocks_but_none_auto_eligible: 4 |
| synthetic | all | added_cuts: 4; discovery_without_supported_blocks: 1; eligible_blocks_without_added_cut: 1; solved_without_callback: 7 |
| synthetic | auto | added_cuts: 1; discovery_without_supported_blocks: 1; solved_without_callback: 7; supported_blocks_but_none_auto_eligible: 4 |

`coverage.json` records instance-level classifications, source-side refusals, support failures, actual-row binding and rounding rejections, selection skips, budget exhaustion, callback/discovery/certification time, and zero-node solves. A model solved without invoking this separator did not need these cuts on that run; it does not show that the cuts can never help. A supported block without an added cut can reflect the bounded direction search, insufficient violation, certification or binding rejection, or the work budget. The recorded counters do not isolate the causal contribution of these mechanisms.

No callback is not itself proof of a presolve solve; zero nodes is reported separately. No cut within the bounded search is not hull membership or proof that native cuts dominate. Block counts overlap and are not unique source-variable counts.
