# Scouting brief (2026-09-28, second continuation)

Goal: find the highest-potential direction for a substantial, original,
correct theoretical contribution to mixed-integer nonlinear programming
(MINLP) with a clear route to better solvers or wider applicability.

Each scout writes one report `research-20260928b/scouting/<area>.md` with:

1. Frontier map: strongest relevant results (with exact assumptions and
   conclusions), including 2024-2026 arXiv work. Record every source
   examined (URL/arXiv id/local slug) and what was checked.
2. Two to four precisely stated open questions that remain open after the
   search, with evidence that they are open (and a caution that an
   unsuccessful search does not establish novelty).
3. For the best question: a concrete attack plan, first-pass mathematical
   progress (lemmas, small cases, counterexample search, computations),
   and an honest estimate of difficulty and risk.
4. Significance: what a solution would establish, what solver capability it
   could enable, what would remain necessary for practical value. Separate
   proved consequences from plausible and speculative benefits.
5. A one-paragraph recommendation with a score (1-10) for
   significance x feasibility x originality.

Rules: only edit your own report and scratch files under
`research-20260928b/scouting/<area>/`. Do not commit. Do not run
project-wide checks or inspect CI. Use local literature
(`literature/papers/*/fulltext.md`, `literature/topics/*.md`) and open web
sources. Repository topics already developed extensively (avoid duplicating
unless a strong new mechanism exists): multilinear/McCormick gaps,
quadratic aggregation and HHC hulls, penalty encodings, exact-arithmetic
complexity of convex quartics (PosSLP), sparse Lasserre/Putinar rates and
private recourse, indicator quadratic stars/trees and smoothed messages,
switching-control CIA rounding, potential-flow (gas/water) networks,
pooling complexity, bilevel structured algorithms, spatial B&B exponential
lower bounds, FBBT hardness, integer precision/dimension of convex
functions, curvature-based convex covers, certified MINLP/VIPR.
