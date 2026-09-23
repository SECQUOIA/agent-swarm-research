# Iterated optimality-based bound tightening (OBBT): plan

Date: 2026-09-23. Status: plan.

## Motivation (from `../scouting/brainstorm2-solvercore.md`, probes A and A2)

- On 140 MINLPLib instances with a positive root gap, one OBBT round closes a
  mean 31.6% of the root gap (10% fully closed); up to six rounds close 42.8%
  (20% fully closed). Per-round LP budget barely matters; the number of rounds does.
- On the 41 instances where rounds 2+ add at least 10 points, full solves from
  the iterated box need 2.9 times fewer nodes (shifted geometric mean).
- Caveats: the cutoff was the known optimal value, and the naive loop reran the
  SCIP root, so total time got worse.
- SCIP runs OBBT once at the root; Gleixner et al. (2017) found OBBT alone gives
  no significant average speedup.

## Targets

1. Contraction theory of the OBBT operator `T_U(B)` near a minimizer, for
   relaxations with second-order pointwise convergence: rates under quadratic
   growth and under sharp (first-order) growth, the fixed-point width as a
   function of the cutoff slack `epsilon`, stalling, and tight examples.
2. Exact analysis of model families (for example `x^2 + y^2 + a xy` with McCormick:
   contraction ratio `(sqrt(2a^2 + 4a) - a)/2`, derived 2026-09-23, to be proved
   including the evolution of box shape).
3. Consequences for branch and bound (cluster problem; relation to the
   repository's Theorem 3 on width-tight domain reduction).
4. An adaptive iterated-OBBT rule derived from the theory (continue while the
   observed contraction ratio is below a threshold; restrict to variables that
   moved; re-trigger on incumbent improvement).
5. Computational study with realistic incumbents and an efficient
   implementation (own LP relaxation with warm starts, or SCIP probing), measuring
   nodes and total time.

## Novelty questions to settle first

Caprara and Locatelli (Math. Program. 2010), Caprara, Locatelli and Monaci
(COAP 2016), Ryoo and Sahinidis (1996), Zamora and Grossmann (1999), Faria and
Bagajewicz (bound contraction, 2011+), Coffrin et al. (2015), Alpine
(Nagarajan et al.), Gleixner et al. (2017), Puranik and Sahinidis (2017),
Kannan and Barton (2017, 2018), Schichl–Neumaier exclusion regions.
