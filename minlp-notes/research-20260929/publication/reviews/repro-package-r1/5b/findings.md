# 5b: COPS displays in open-instances-summary.md

Written by the main reviewer from the delegated agent's returned result (the
agent could not write this file). Evidence: `cops_summary_check.py` and
`cops_summary_check.log` in this directory, which the reviewer spot-checked.
Command: `OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 300 python3 cops_summary_check.py > cops_summary_check.log 2>&1`
(exit 0, about 1 s; it reads only saved files).

All eight OSIL models minimize. The summary's COPS numbers are on lines 33–34.

| line | display | exact value | verdict |
|---|---|---|---|
| 33 | `5.06862` (low end) | chain400 L = 5.068621694604009242… | safe |
| 33 | `5.07226` (high end) | chain50 L = 5.072261493982862745… | safe |
| 33 | `same to 1e-14`, `≤ 1.0e-14` | gaps against the double points: 9.6328e-15, 9.9046e-15, 9.3375e-15, 9.8054e-15 | valid |
| 34 | `−0.04806944` | catmix100 author −0.0480694320388827…, reviewer −0.0480694320311445… | safe |
| 34 | `−0.04805591` | catmix800 author −0.0480559018410768…, recheck −0.0480559014796756… | safe |
| 34 | `1.65e-13 (100)` | at most 1.649687e-13 | valid |
| 34 | `1.5e-10 (800, verifier)` | 1.48445e-10 (DP-policy point); 1.48828e-10 (snap point) | valid |

**No COPS number in the summary has to change under its current wording.**
None of the five unsafe strings appears in the summary.

Conditional correction: the integration notes ask to remove the line 43–46
statement that no exactly feasible chain point exists. If line 33's gaps are
then measured against the exact points (or the 60-digit KKT value), chain100's
gap becomes 1.00276e-14. The displays would then need to change:
- `same to 1e-14` → `within 1.1e-14`;
- `≤ 1.0e-14` → `≤ 1.1e-14`.

Optional: the listed-dual endpoint `0.0826` (listed 0.08256615) is rounded to
nearest. The outward form would be `0.0825–0.1745`.

Where the five unsafe strings appear (outside the summary):
- **chain50:** `open-instances-wave2/cops/report.md:19,173`,
  `reviews/cops-verification/verification-report.md:35,193`,
  `reviews/closing-audit-a.md:132`,
  `publication/reviews/solver-campaign-review-r1.md:43`.
- **chain200:** `open-instances-wave2/cops/report.md:21,175`,
  `reviews/cops-verification/verification-report.md:37,195`.
- **catmix200 author:** `open-instances-wave2/cops/report.md:24,281`,
  `reviews/cops-verification/verification-report.md:45,388`,
  `publication/reproduction/README.md:175`.
- **catmix100 reviewer configuration B:** `open-instances-wave2/cops/report.md:357`,
  `reviews/cops-verification/verification-report.md:39,350,382`,
  `publication/reproduction/README.md:174`.
- **catmix800 recheck:** `reviews/catmix-recheck.md:23,37,235`,
  `publication/reproduction/README.md:177`.

Safe 17-digit forms of the five strings:

| value | safe display |
|---|---|
| chain50 | 5.0722614939828627 |
| chain200 | 5.0689173417931616 |
| catmix200 author | −0.048059145600671712 |
| catmix100 reviewer configuration B | −0.048069432031144562 |
| catmix800 recheck | −0.048055901479675652 |

`publication/reproduction/cops/report.md` lines 65 and 69 wrongly say these
strings are in the "summary text" or "summary bracket".

Understated gaps in detailed notes (outside the summary):

| location | stated | exact | safe display |
|---|---|---|---|
| `open-instances-wave2/cops/report.md`, chain50 | 9.4e-15 | 9.6328e-15 | 9.7e-15 |
| same note, chain100 | 9.9e-15 | 9.9046e-15 | 1.0e-14 |
| same note, chain200 | 9.0e-15 | 9.3375e-15 | 9.4e-15 |
| same note, catmix100 | 7.9e-12 | 7.9231e-12 | 8.0e-12 |
| same note, catmix400 | 1.9e-10 | 1.9368e-10 | 2.0e-10 |
| same note, catmix800 | 5.1e-10 | 5.1023e-10 | 5.2e-10 |
| same note, relative gap (lines 280–283) | 1.6e-10 | 1.648e-10 | 1.7e-10 |
| same note, relative gap (lines 280–283) | 4.0e-9 | 4.030e-9 | 4.1e-9 |
| `reviews/catmix-recheck.md:36`, catmix400 width | 6.8e-11 | 6.805973e-11 | 6.9e-11 |
| `reviews/catmix-recheck.md:37`, catmix800 width | 1.48e-10 | — | 1.49e-10 |

The reproduction COPS report repeats the catmix800 width as 1.48e-10; it
should also read 1.49e-10.
