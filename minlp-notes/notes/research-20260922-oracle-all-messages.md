# Exact smoothed message construction: development record

Date: 2026-09-22. The complete proof has been promoted to
[Exact smoothed indicator messages under spectral bounds](../results/smoothed-spectral-indicator-messages.md).

The result constructs exact full quadratic representations of all bounded-box
separator messages for fixed-treewidth indicator QPs with certified spectral
bounds. Uniform finite-grid penalty perturbations need only a power-of-two
grid with at least twice as many points as variables. The algorithm is correct
for every sample and has polynomial expected bit time under the stated
numerical bounds. It uses a first-moment near-optimal-support estimate,
approximate partition enumeration, and a parameter net.

Two fresh independent reviews checked the [enumeration and full proof](review-20260922-nearopt-enumeration.md)
and the [spectral assumptions and bit complexity](review-20260922-spectral-parametric-oracle.md).
The promoted result records the exact checks, sources, limitations, and
provisional novelty assessment. This note remains as a stable link from
earlier investigations and reviews.
