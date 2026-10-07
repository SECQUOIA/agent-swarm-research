# Campaign 4, Part S: the star oracle at scale

Protocol: `../campaign-v4-protocol.md`, Part S. Script: `star_bench.py`.
Record: `star-bench.json` (all values exact, as strings); run output:
`star-bench.log`. Run on 2026-10-03, 12:31:36 to 12:34:10 EDT, one
single-threaded process, Python 3.13.11, load average 2.2 at start (shared
host). No solver is involved.

## What was run

- **Instances.** Random constrained quadratic stars with k in {10, 100,
  1000, 10000} leaves and 5 instances per k (seed string
  `campaign-v4-star:<k>:<index>`, index 0-4). Each star has a center box,
  leaf boxes, one to three center-only rows and exactly two center-leaf rows
  per leaf (2k in total), each row involving the center and one leaf with
  nonzero coefficients. All coefficients are small rationals of either sign;
  leaf curvature d_i can be positive, negative or zero. Each leaf's rows hold
  on an anchor segment that spans the center box, so every instance is
  feasible and the center interval does not shrink as k grows. The
  `star_bench.py` docstring gives the exact distributions.
- **Oracles.** `sweep_star` from `../../verification/M3_star_sweep.py` (the
  O((m+k) log(m+k)) reference sweep) and the inherited `support_star` from
  `research-20261002-convexification/theory/quadratic_star.py`, imported
  read-only with `sys.dont_write_bytecode`. Times are CPU seconds
  (`time.process_time`); wall time is in the record and is within 0.2% of
  CPU time in every run. The inherited time excludes building its dense input.
- **Checks.** Exact equality of the two minimum values (Fractions). For
  every run, including k = 10000, an exact check that the sweep's minimizer
  satisfies every bound and row and attains the reported value.
- **Pieces.** The number of center intervals each oracle evaluates. The
  sweep merges coinciding breakpoints and changes rules only where some leaf
  minimizer changes. The inherited partition also cuts at every pairwise
  crossing of a leaf's bound lines inside the center interval, so it is finer.
- **Bit length** of the minimum: bit lengths of its numerator (absolute
  value) and denominator in lowest terms.

## Inherited oracle skipped at k = 10000

The script skips the inherited oracle at a given k when its time,
extrapolated quadratically in k from the slowest run at the previous k,
exceeds 600 s. At k = 10000 the estimate is 34.9 s x 100 = 3495 s per
instance, so the oracle was not run on the five k = 10000 instances. A
second estimate gives the same verdict. At k = 1000 the inherited oracle costs
32-38 us per (piece x leaf), and its partition has 1.9-2.5 times as many
pieces as the sweep's. Applied to the k = 10000 sweep piece counts, these
rates give 1000-2800 s per instance. That estimate leaves out the oracle's
O(k^2) input handling: its dense rows hold 2.0e8 coefficients at k = 10000,
which it converts to new Fractions and then to strings in its certificate.

## Results

Summary (medians over the 5 instances of each k):

| k | median pieces sweep | median pieces inherited | median sweep CPU s | median inherited CPU s | values equal |
|---:|---:|---:|---:|---:|---:|
| 10 | 7 | 12 | 0.00128 | 0.00599 | 5/5 |
| 100 | 62 | 144 | 0.0118 | 0.427 | 5/5 |
| 1000 | 416 | 900 | 0.165 | 29 | 5/5 |
| 10000 | 2347 | - | 2.07 | skipped | not run |

Per instance:

| k | inst. | rows (center-leaf + center) | pieces sweep | pieces inherited | sweep CPU s | inherited CPU s | equal | min bits (num/den) | sweep point attains |
|---:|---:|---:|---:|---:|---:|---:|:---:|---:|:---:|
| 10 | 0 | 20 + 2 | 2 | 7 | 0.000948 | 0.00482 | yes | 27/21 | yes |
| 10 | 1 | 20 + 1 | 5 | 12 | 0.00128 | 0.00599 | yes | 27/22 | yes |
| 10 | 2 | 20 + 2 | 9 | 17 | 0.00145 | 0.00787 | yes | 29/22 | yes |
| 10 | 3 | 20 + 2 | 7 | 9 | 0.00112 | 0.00584 | yes | 20/16 | yes |
| 10 | 4 | 20 + 2 | 7 | 15 | 0.00205 | 0.0113 | yes | 27/18 | yes |
| 100 | 0 | 200 + 1 | 62 | 157 | 0.0136 | 0.633 | yes | 51/41 | yes |
| 100 | 1 | 200 + 1 | 71 | 164 | 0.0157 | 0.448 | yes | 44/33 | yes |
| 100 | 2 | 200 + 2 | 72 | 136 | 0.0118 | 0.403 | yes | 41/31 | yes |
| 100 | 3 | 200 + 1 | 55 | 106 | 0.0113 | 0.313 | yes | 52/42 | yes |
| 100 | 4 | 200 + 1 | 54 | 144 | 0.0114 | 0.427 | yes | 49/38 | yes |
| 1000 | 0 | 2000 + 2 | 416 | 900 | 0.152 | 29 | yes | 90/76 | yes |
| 1000 | 1 | 2000 + 3 | 312 | 728 | 0.165 | 25.8 | yes | 58/44 | yes |
| 1000 | 2 | 2000 + 2 | 454 | 1059 | 0.189 | 34.9 | yes | 58/43 | yes |
| 1000 | 3 | 2000 + 1 | 478 | 912 | 0.194 | 31.2 | yes | 53/40 | yes |
| 1000 | 4 | 2000 + 3 | 163 | 402 | 0.131 | 15.3 | yes | 54/40 | yes |
| 10000 | 0 | 20000 + 1 | 2347 | - | 2.07 | skipped | - | 61/44 | yes |
| 10000 | 1 | 20000 + 3 | 1384 | - | 2.16 | skipped | - | 59/42 | yes |
| 10000 | 2 | 20000 + 3 | 1399 | - | 1.99 | skipped | - | 53/37 | yes |
| 10000 | 3 | 20000 + 3 | 3559 | - | 3.84 | skipped | - | 56/40 | yes |
| 10000 | 4 | 20000 + 1 | 2561 | - | 1.95 | skipped | - | 94/78 | yes |

## Observations

- Where both oracles ran (15 instances, k <= 1000), the minimum values are
  exactly equal. Every sweep minimizer (20 of 20) is feasible and attains the
  reported value exactly.
- The sweep's median CPU time per leaf is 0.13, 0.12, 0.17 and 0.21 ms for
  k = 10, 100, 1000 and 10000. Its time is close to linear in k over three
  orders of magnitude: 2-4 s at k = 10000 with 20000 center-leaf rows.
- The inherited oracle's time grows by a factor of about 70 per tenfold
  increase in k (median 0.006 s, 0.43 s, 29 s). This is consistent with a
  cost proportional to (number of pieces) x k, since every piece re-evaluates
  every leaf rule: about 30 us per (piece x leaf) at k = 100 and 32-38 us at
  k = 1000.
- Piece counts grow less than linearly in k (median sweep pieces 7, 62, 416,
  2347), for two reasons, both measured by recomputing the sweep on the same
  instances. First, many leaves keep one minimizer rule on the whole center
  interval: 30-90% of leaves at k = 10, 44-54% at k = 100, 49-79% at
  k = 1000 and 36-67% at k = 10000. Second, the coefficients come from a
  finite grid of small rationals, so rule changes of different leaves often
  fall at the same center value. At k = 10000 the leaves have 3610-8943 rule
  changes in total, but only 1383-3558 distinct breakpoints.
- The minimum's bit length (numerator/denominator) is 20-29/16-22 at
  k = 10, 41-52/31-42 at k = 100, 53-90/40-76 at k = 1000 and 53-94/37-78
  at k = 10000. It does not grow steadily with k. The upper end of the range
  at k = 1000 and k = 10000 comes from one instance each (90/76 and 94/78);
  the other instances have at most 58/44 and 61/44.
- Timings are descriptive (shared host, one run per instance).
