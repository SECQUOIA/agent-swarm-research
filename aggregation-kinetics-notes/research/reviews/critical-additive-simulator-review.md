# Independent review of the critical additive particle simulator

Date: 2026-09-06. Reviewer: `extinction_proof/review_simulator`, independent of the implementation author.

Reviewed [the C++ simulator](../verification/critical_additive_particles.cpp) and [the experiment runner](../verification/run_critical_additive_particles.py). The event algorithm and reported observables are correct after the minimum-size correction described below. This review validates the finite stochastic simulation; it does not establish a new theorem or literature novelty.

## Event law and timing

With total mass n and L active particles, the sum of unordered additive coagulation rates is

\[
\sum_{i<j}(x_i+x_j)/n=(L-1)\sum_i x_i/n=L-1.
\]

Each particle splits into equal halves at rate one, so the total event rate is 2L−1. The implementation samples an exponential waiting time with this rate, chooses fragmentation with probability L/(2L−1), and chooses its parent uniformly. The rate of fragmentation of each particle is therefore one.

For coagulation, the first particle has mass-weighted probability x_i/n; the second is uniform over the other L−1 particles. The resulting unordered pair rate is

\[
(L-1)\left[\frac{x_i}{n(L-1)}+\frac{x_j}{n(L-1)}\right]
=\frac{x_i+x_j}{n}.
\]

The implementation uses its tracked total mass in place of n for weighted selection. This is equivalent in exact arithmetic, and conservation checks bound its floating-point discrepancy. The L=1 case necessarily fragments, so the second-particle sampler is never called with an empty choice set.

An event time is sampled once and retained while all preceding snapshot times are emitted. Thus snapshots do not truncate or restart the clock. A snapshot exactly at an event is emitted after that event, consistent with a right-continuous process. The 53-bit uniform generator admits a zero waiting time with probability 2^-53; this is a negligible standard discretization issue, not an error in the Gillespie rate construction.

## Dynamic mass array and Fenwick tree

Append, replacement, removal by moving the last particle, and capacity growth preserve the correspondence between the array and the cumulative tree. Keeping the lower index during merging ensures that subsequent removal of the higher index cannot discard the newly merged mass. Splitting replaces the selected mass with half and appends its other half. Binary lifting returns the first cumulative mass strictly greater than its target, including exact left endpoints of intervals.

I independently exercised 20,000 randomized operations against a simple vector implementation: append, arbitrary replacement, merge, and arbitrary removal. After every operation I checked the entire active vector, its total, and selection at every interval's left endpoint and midpoint. These checks passed with AddressSanitizer and UndefinedBehaviorSanitizer enabled. The test used integer masses to make the tree comparisons exact and isolate structural errors. The author's self-test separately exercises fractional masses and conservation over 10,000 valid coagulation/fragmentation events.

Finite precision can eventually lose very small weights in cumulative sums with large mass ratios. Long double and the short simulation horizon make the present experiment reasonable; the checks do not establish reliable arbitrarily long simulations or unlimited size dynamic range. The reported mass errors are errors in printed numerical totals, not exact-arithmetic guarantees.

## Observable and runner checks

The empirical measure is n^-1 times the sum of particle point masses. Accordingly `M_half` is n^-1 Σ√x_i, while normalized count is L/n and normalized mass is n^-1 Σx_i. Log mean and log variance use the number probability measure L^-1 Σδ_x_i, with population variance denominator L. Number CDFs divide counts by L. Mass CDFs sum masses at or below their inclusive thresholds and divide by n. Largest mass fraction divides the largest particle by n. These are the appropriate, distinct normalizations.

The original `smallest = 1` initialization could misreport minimum size if every particle exceeded unit mass. For example, a mass-2 singleton would report one. I reported this to the author, who changed the initialization to infinity. I verified that a mass-2 singleton now reports two. The nine planned runs were unaffected because their noninitial minimum sizes were below one.

The runner consistently uses the same three declared seeds at each of the three sizes, preserves all ten snapshots per run, and summarizes the final time correctly. Its count references are

\[
\mathbb E L_t=n+t,\qquad \operatorname{Var}(L_t)=(2n-1)t+t^2.
\]

As a separate distributional check, I compiled the reviewed simulator and ran n=50, t=10 for seeds 0 through 1999. The 2,000 final counts had mean 60.473 versus exact mean 60, with theoretical standard error 0.73824 and standardized discrepancy 0.64071. Their sample variance was 1098.2614 versus exact variance 1090. The smallest observed count was one. These checks support the event clock and count law without treating the nine research runs as a sufficient statistical ensemble.

The author also changed the summary's normalized mass-error calculation to `Decimal`, preventing conversion of printed deviations to zero through ordinary float rounding. This preserves the precision present in the CSV; it cannot recover digits beyond those printed.

## Interpretation of continuum references

For unit initial sizes and b=1, the continuum references e^(-κt), the log-mean interval from −2t log 2 to −2t log 2+(1−e^(-2κt))/(2κ), and compound-Poisson reference variance 2t(log 2)^2 have the correct constants, with κ=3−2√2. Their source statements concern the deterministic population equation or its comparison process. They are not pathwise bounds for these finite stochastic trajectories. In particular, convergence in distribution or Wasserstein-1 after scaling log size does not by itself prove convergence of its second moment. The reported empirical log variance should not be called a verification of continuum variance asymptotics.

The displayed log(n)/log 2 is the coefficient boundary in a sufficient asymptotic obstruction: the theorem requires t=C log n with a fixed C>1/log 2. It is not an identified first breakdown time, does not guarantee a large finite-n discrepancy at equality, and does not show that smaller growing times are accurate. At t=10, the experiments alone do not measure a distance to the continuum solution because that solution is not computed. Their large mass concentrations, small-particle counts, and count fluctuations illustrate the finite process and can motivate further experiments; they do not independently demonstrate the asymptotic mass-CDF theorem or a Gaussian limit.

No unresolved algorithmic error was found in the reviewed code. The fixed three-seed experiment remains descriptive, as the runner explicitly states.
