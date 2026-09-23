# Stage 6 correction assignment

Use this assignment only after the coordinator confirms all fifteen reports have been read and adjudicated. Act as the separate correction agent. Do not edit snapshots, original literature, accepted core mathematics, other paper directories or reviewer reports.

Accepted local corrections:

1. R09-1: In `sections/appendix-scaling.tex`, make the rectangularity proposition explicitly assume a finite nonnegative catalogue with `{0,s,M}` contained in it and `0<s<M=max Lambda`. The intended three-member assumption is clear from the proof and endpoint-only exception, but current chain wording is ambiguous. Make the corresponding membership explicit in the coverage ledger's supporting and bounded-development rows. Do not change the proof or broaden its scope.
2. R09-2: In `process/claim-coverage.md`, change incoming **low** coordinates to incoming **high** coordinates for incidence ownership. The manuscript proof at `sections/04-incidence-interiority.tex:36` already has the correct high-coordinate partition.
3. R11-1: Qualify the opening LP comparison in `sections/appendix-fbbt.tex` by nonemptiness of the limiting box and cite Belotti et al. Theorem4.1. Root independently read original PDF13–15 and visually inspected14: that theorem and its following infeasibility discussion require the qualification. Own constructed systems remain feasible and no core theorem depends on this contextual result.

Read the complete reports09 and11 and the coordinator adjudication before editing. Preserve all other content. Write a correction log describing exact edits and source verification. Compile with `verification/build_and_check.py`, inspect changed pages and resolve warnings. Do not rerun unrelated unchanged mathematical tests or change historical validation hashes to make them appear current. Record current build/PDF hashes in a new correction-validation artifact. The coordinator will verify the changes, accept Stage6 if no issue remains, and then run the separate fifteen-reviewer whole-paper loop.
