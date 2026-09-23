# Screen: approximability of the minimum number of matches (2026-09-22)

Read-only screening agent; kept as a candidate direction. No result.

- Single temperature interval: strongly NP-hard (Furman–Sahinidis 2001); Simple
  Greedy 2-approximate, Improved Greedy 1.5 (Letsios–Kouyialis–Misener, CACE 113
  (2018) 57–85, arXiv:1709.04688); best known `6/5 + eps` via balanced set
  packing (Chen–Li–Liang, arXiv:2504.18037, TAMC 2025, Theorem 3), APX-hard
  with no explicit constant (their Theorem 7, from bounded-frequency 3DM,
  unless NP = BPP). Equivalent to maximum zero-sum partition (Fertin et al.,
  TCS 1019 (2024)): OPT = n + m - (number of parts).
- Multi-interval (cascade `s <= t`): only `O(k)` guarantees (water filling,
  LP rounding; Letsios et al. Theorem 6 shows water filling is `Theta(k)`),
  `O(log n + log(h_max/eps))` for the LP-guided greedy (Theorem 7, harmonic
  set-cover argument over heat units). No constant factor independent of `k`
  and no super-constant hardness known; Set-Cover hardness judged implausible
  (unit cost per stream pair; cascade gives only threshold adjacency).
- Observation from the screen (unverified here): with `n` hot streams having unit
  heat in each of `k` intervals and `k` cold streams each demanding `n` units in
  its own interval, OPT = `nk` while the standard big-M LP with
  `U_ij = min(h_i, c_j)` has value `max(n, k)`: integrality gap `Theta(min(n, k))`,
  so no LP-based analysis of that relaxation can beat `O(k)`. With the
  tightened `U_ij = MaxHeat(i, j)` of Letsios et al. the same LP is exact on
  this instance; the integrality gap of the tightened LP is open.
- Realistic few-day deliverables: the gap instance above; a gap bound or
  bad instance for the tightened LP; removing `log h_max` from Theorem 7.
  A `k`-independent constant factor or an `Omega(log n)` hardness are not
  judged to be few-day results.
- No 2025–2026 follow-up found in CACE, JOGO, IJOC, or arXiv beyond
  Chen–Li–Liang (which does not cite the HENS literature).
