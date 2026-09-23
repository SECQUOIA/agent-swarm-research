# Novelty checks for the two-pool/two-output hardness candidate

Date: 2026-09-05. This is a search record, not a proof of novelty.

The precise candidate is NP-hardness with two pools, two outputs, arbitrary
inputs and quality coordinates, no bypasses, and an underlying undirected
tree. A single nonmixing anchor pool can instead be replaced by one bypass.
Only upper flow and upper quality bounds are used. The candidate does not
claim strong hardness.

## Primary sources checked

- Haugland's final 2016 paper, Section 6, asks about fixed numbers of pools
  together with bounded inputs, terminals, or quality parameters:
  [[haugland2016-the-computational-complexity-of-the]] p.16. The
  [earlier audit](pooling-fixed-pools-qualities-source-audit.md) explains why
  an unproved two-pool claim in the 2014 abstract cannot substitute for the
  final paper's classification.
- Boland, Kalinowski, and Rigterink's
  [open author manuscript](https://optimization-online.org/wp-content/uploads/2015/08/5059.pdf)
  gives the single-pool fixed-input algorithm and lists remaining
  two-pool parameter cases in its complexity discussion. The present
  reduction permits unrestricted input and quality counts, with two
  terminals fixed.
- Baltean-Lugojan and Misener's
  [*Piecewise parametric structure in the pooling problem*](https://d-nb.info/1149002905/34)
  deserves explicit comparison. Remark 4.6 on PDF pages 27–28 makes broad
  hardness statements when relaxing assumptions of a single-quality,
  fixed-demand, uncapacitated-feed/pool model, referring to polynomial
  systems. It does not give a two-pool/two-output reduction there.
  Theorem 5.2 on PDF page 29 is a one-output sparsity theorem, not a
  two-output hardness theorem. No Matsui citation occurs in its searchable
  text. These observations do not rule out an equivalent result elsewhere;
  they identify why the displayed statements alone do not establish the
  precise cardinality result investigated here.
- The source reduction itself is established, not new:
  [Matsui, METR95-13](https://www.keisu.t.u-tokyo.ac.jp/data/1995/METR95-13.pdf),
  Section 3, Theorem 3.1, proves hardness of positive linear multiplicative
  programming with polynomially encoded bounded rational polytopes.

## Searches

Open web searches included:

```
pooling problem "two pools" "two outputs" complexity
pooling problem fixed terminals qualities NP-hard Matsui multiplicative
pooling problem complexity bounded pools terminals Haugland 2016 open problem
```

The inspected results did not supply a matching fixed-two-pool,
fixed-two-output reduction. Search completeness is limited. The current
description should be "candidate resolution of the published case; no
matching open result located", subject to independent source comparison.

The PMC copy of Baltean-Lugojan–Misener presented a browser challenge. No attempt
was made to bypass it; the openly accessible German National Library PDF
provided the primary text instead.
