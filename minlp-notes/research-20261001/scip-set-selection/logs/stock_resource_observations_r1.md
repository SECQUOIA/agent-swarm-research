# Resource observations during the stock rerun

Observed near 2026-10-04 02:49 UTC (2026-10-03 22:49 local):

- `free -h`: 47 GiB physical memory, 42 GiB used, 3.6 GiB free,
  4.6 GiB available; 16 GiB swap, 9.9 GiB used.
- `ps -C scip-stock -o pid,etime,time,stat,pcpu,rss`: six stock solvers
  near 11.5–12 minutes wall time had consumed about 5.7–6.2 minutes of
  process CPU. One was in state D. SCIP had not reached its CPU-clock
  limit or printed final statistics before the wall guard expired.
- Load samples in `full_stock/driver.jsonl` reached 125.853 before
  declining. The driver retained the eight-worker limit.
- `stock_load_processes_r1.txt` records concurrent Python processes
  owned by other work as well as this rerun's solvers. No other work's
  process was stopped or changed.

These observations document load and memory pressure. They do not isolate
which external process caused the slowdown or quantify a pure capture cost.
