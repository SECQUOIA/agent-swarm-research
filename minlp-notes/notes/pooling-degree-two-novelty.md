# Novelty audit: one-quality pooling with bounded degrees

Date: 2026-09-04. Companion to
[the hardness result](../results/pooling-one-quality-degree-two-hardness.md).
A literature agent searched for later resolutions of the open problems of
Boland, Kalinowski, and Rigterink (2017, Section 4); the root agent checked the
key source statements. An unsuccessful search does not establish priority.

## Status of the four open problems (Boland et al. 2017, Section 4)

| # | Question | Status found |
| --- | --- | --- |
| 1 | Strongly polynomial algorithms for the cases solved by polynomially many LPs | Partially addressed by Baltean-Lugojan and Misener (JOGO 71 (2018) 655–690): strongly polynomial algorithms for single-quality subclasses only under their Assumption 2.2 (no feed availability or pool capacity bounds, fixed demands). Cases 5–7 of the Boland table with full bounds remain without a strongly polynomial algorithm. |
| 2 | One quality, in-degrees of pools and outputs at most two | No resolution found. **Now strongly NP-hard** (Theorem 2 of the result note), even with output in-degree one. |
| 3 | One quality, out-degrees of inputs and pools at most two | No resolution found. **Now strongly NP-hard** (Theorem 1 of the result note), even with input out-degree one. |
| 4 | Two pools with bounds on inputs, outputs, qualities | No paper found. Open. |

## Later literature examined

- Baltean-Lugojan, Misener (2018), read in full via Europe PMC. Single quality,
  p-formulation, direct arcs allowed. Positive results: Theorem 3.1.6(ii),
  Theorem 3.3.9, Corollary 4.5, Corollary 5.4 (strongly polynomial algorithms
  for one pool, or one output, under Assumption 2.2). Hardness content: none
  new; Remark 4.6 cites Alfaki–Haugland strong NP-hardness. The strings
  "in-degree" and "out-degree" do not occur. Does not resolve problems 2–4.
- Dai, Diao, Fu, J. Oper. Res. Soc. China 6 (2018) 249–266: an independent
  proof that one quality is strongly NP-hard (abstract verified; full text not
  read). Its reference list does not cite Haugland 2016. No degree bounds
  claimed in the abstract.
- Haugland, INOC 2019 "Pooling problems with single-flow constraints"
  (read in full): NP-hardness of single-flow variants (Proposition 3.1) using
  Haugland 2016 Theorems 6/7 and a PARTITION reduction; a different problem.
- Letsios, Bradley, Dey, Misener, Shah, Comput. Chem. Eng. 2020
  (arXiv:1909.12328): survey; compiles known results only. Its Table 1
  misattributes the one-quality hardness to Boland et al. 2017.
- Haugland, Hendrix, JOTA 170 (2016) 591–615 (abstract verified):
  pseudo-polynomial algorithm for two inputs, two outputs, one quality.
- Dey, Gupte, Oper. Res. 63 (2015): `n`-approximation and `n^(1-ε)`
  inapproximability; the inapproximability instance has `|I|=|J|=|K|=n` and
  one pool, so it says nothing about one quality. Their open-problem list asks
  for the complexity for a fixed pool out-degree; Haugland's Theorem 6 answered it for
  unbounded qualities, and Theorem 1 of the result note answers it for one
  quality.
- Semantic Scholar citation lists of Boland et al. 2017, Haugland 2016,
  Haugland–Hendrix 2016, and Gupte et al. 2017; the arXiv listing for
  "pooling problem"; dblp; Haugland's publication list (no pooling entries
  after 2019). Nothing else with complexity content for the standard pooling
  problem was found. Searches for treewidth, series-parallel, or
  fixed-parameter results on pooling returned nothing.

## Haugland 2016 attribution caveat

The full text of Haugland (2016) was not accessible. Theorem numbers
(Theorem 3: `|I|=|J|=2`, `|K|=1`, bin packing with two bins; Theorems 4–5:
`|I|=2` or `|J|=2`, one quality, exact cover by 3-sets; Theorems 6–7:
out-degrees or in-degrees at most two, unbounded qualities, MAX/MIN 2-SAT;
Proposition 3: pools of in-degree one or out-degree one) come from Table 2 of
Boland et al. and from cross-references in Haugland's INOC 2019 paper. The
result note relies only on the open-problem statements in Boland et al. and on
the Asahiro et al. (2011) hardness theorem, which was read in the author PDF.

## Assessment

The two theorems resolve explicitly posed open problems with a short reduction
whose only external ingredient is the strong NP-hardness of `{1,2}`-weighted
minimum-maximum-outdegree orientation (Asahiro, Jansson, Miyano, Ono, Zenmyo
2011). The pool-degree pattern `(2,2)` is the smallest hard pattern because
degree-one pools reduce to LP. Remaining open cells recorded in the result
note: all four degree bounds simultaneously at most two; strong hardness with
`|J|=2` and bounded input out-degree (or `|I|=2` and bounded output
in-degree); two pools.
