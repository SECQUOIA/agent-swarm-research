# Links between univariate terms that share a variable

Code and raw results for [results/shared-variable-term-links.md](../../results/shared-variable-term-links.md).

- `scan.py`, `scan.jsonl`, `scan_candidates.txt` — MINLPLib scan for variables with several distinct
  univariate subexpressions; candidate list used by the SCIP pilot.
- `link_detect.py` — the two detection rules (sine/cosine pair, powers of a nonnegative variable).
- `link_pilot.py`, `run_links.sh`, `results_links.jsonl` — SCIP 10, native against linked, 60 s.
- `gurobi_link.py`, `run_gurobi_links.sh`, `link_instances.txt`, `results_gurobi_60.jsonl`,
  `results_gurobi_1800.jsonl` — Gurobi 13, native against linked.
- `results_lnts_1800.jsonl`, `trig_pilot.py`, `lnts_soc.py` — particle-steering family.
- `run_linked2.sh`, `compare_rules.py`, `results_gurobi_60_linked2.jsonl` — alternative reference-exponent rule.
- `baron_link.py`, `run_baron_links.sh`, `results_baron_1800.jsonl` — BARON through GAMS, native against linked.
- `polish_point.py`, `point_waterno2_18.json`, `exact_check_point.py` — improved primal point for
  `waterno2_18` and its exact rational residual check of the parsed
  floating-point model. The saved point meets the stated feasibility
  tolerance but has a positive residual, so exact feasibility is not certified.
- `check_scip_waterno2.py` — shows that SCIP 10 accepts a point better than its reported optimum.
- `moment_pilot.py` — exact moment-curve hull of `(x, x^2, x^3)` as cone constraints in SCIP (small gains).
- `run_moment.sh`, `moment_instances.txt`, `results_gurobi_60_moment.jsonl`, `compare_moment.py` — the same
  hull in Gurobi 13, 60 s, modes `moment` and `linkmoment` of `gurobi_link.py`.
- `run_moment_1800.sh`, `results_gurobi_1800_moment.jsonl` — Gurobi 13, 1800 s, exact hull on six instances.
- `review/` — scripts and outputs of the independent review.

Environment: `uv run --project ../minlp_solver_lab python <script>`; MINLPLib OSiL files in
`~/.cache/minlplib/minlplib/osil/`.
