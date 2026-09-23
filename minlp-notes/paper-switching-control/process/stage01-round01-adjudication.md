# Stage 1, round 1 adjudication

All five independent reviewers completed review of the same frozen eight-page draft. The primary agent read the reports in full and independently read the manuscript and central source passage. No reviewer or primary reading found a major mathematical issue.

## Valid findings and required corrections

1. **Integer domains (minor; R02-01 and reviewer 05).** Accept. Explicitly declare nonnegative integer switch budgets, positive integer activation-block counts, and positive integer grid sizes. This removes an avoidable ambiguity in the compactness proposition.
2. **Overview mode scope (minor; R02-02 and R04-01).** Accept. The abstract and opening overview must say that the full continuous one-switch minimax formula applies for at least three modes. The theorem itself is correctly scoped.
3. **Construction normalization (minor; R04-02 and reviewer 05).** Accept. Restore arbitrary-horizon definitions in the implementation-oriented paragraph, or explicitly maintain normalization. Prefer giving `E=H_n(T)` and `t_i=T-m_i-E`, so the construction can be used directly.
4. **Frozen verification dependencies (minor; R03-01).** Accept. The stage checker currently resolves its repository dependency incorrectly inside a snapshot, and the external checker sources are not frozen. Bundle the exact required existing scripts under the paper, adapt the checker and README to paper-relative paths, record origin hashes, and ensure the snapshot contains everything those commands use. Do not alter the original round01 snapshot; create an accepted-stage snapshot after corrections. This concerns reproducibility, not the analytic theorem.

Reviewer 01 reported no findings. Duplicated findings above are consolidated, not counted as additional independent defects. No criticism was rejected. No theorem or proof needs substantive mathematical revision.

## Decision

Assign all corrections to an agent other than the author. Check every change and execute the corrected frozen verification/build. Since no major issue was found, the user process does not require another five-reviewer round before acceptance. Stage 2 may begin only after all four corrections are verified.
