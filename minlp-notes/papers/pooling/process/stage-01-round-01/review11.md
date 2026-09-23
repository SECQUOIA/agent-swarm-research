# Stage 1, round 1 — reviewer 11

Scope: all of `sections/01-foundations.tex`, with emphasis on primary-source attribution and citation accuracy. I read the assigned protocol and the local literature instructions. I did not edit the manuscript or read other reviewers' reports.

## Finding 1 — major: the endpoint formulation omits an essential restriction on lower quality bounds

Location: `sections/01-foundations.tex:641–672`, particularly the equivalence at lines 647–658 and the exact-MILP claim at lines 660–667.

The stated special case requires input attributes in `[0,1]` and product **upper** bounds in `{0,1}`, but does not require lower quality bounds to be absent or redundant, or exclude additional polyhedral quality restrictions. The model and this subsection previously permit such restrictions. The disjunction only enforces the upper bounds. Consequently the stated equivalence and exact MILP are false under the written assumptions.

Concrete counterexample: one input of quality zero, one pool, one product, feed and outlet capacities one, all lower flow bounds zero, and product quality interval `[1,1]`. Send one unit along both arcs. The input quality lies in `[0,1]`, and the product upper bound is one, as required by the paragraph. Both `D` and `S` are zero, so the disjunction and proposed MILP accept this flow. Its product mass is zero and its delivery is one, violating the lower quality bound. This example even has a facial product intersection (the empty face), so the preceding faciality assumption does not rescue the assertion.

Correction: explicitly restrict this paragraph and its certificate conclusion to coordinatewise upper quality specifications only, with all lower bounds redundant (for instance at most zero) and no additional product-region constraints. If lower endpoint specifications are intended as well, develop the additional disjunctions and revise the binary count; the simpler restriction fully repairs the current argument.

## Finding 2 — minor: two authors are incorrectly named in the bibliography

Location: `bibliography.bib:34`, used at `sections/01-foundations.tex:197`.

The entry identifies “Gupte, Ankur” and “Cheon, Min-Soo.” The actual source title page identifies **Akshay Gupte** and **Myun Seok Cheon**. This is a concrete attribution error, although the DOI and title identify the intended article and its Remark 2.2 does contain the stated question.

Correction: replace those author names with `Gupte, Akshay` and `Cheon, Myun Seok` (or the author's standard hyphenated `Myun-Seok` spelling, consistently). Do not copy the erroneous local `paper.md` author metadata back into the manuscript bibliography.

Evidence: local `literature/papers/gupte2017-relaxations-and-discretizations-for-the/fulltext.md`, PDF p.2 title page and p.6 Remark 2.2. The author-posted [Optimization Online record](https://optimization-online.org/2015/04/4883/) independently names Akshay Gupte and Myun-Seok Cheon and gives the 2017 volume/issue/pages.

## Attribution and source checks without further findings

- The Dey–Gupte citation at lines 194–197 correctly credits the standard-pooling one-product approximation principle. I checked the actual article manuscript at `/tmp/pooling-paper-sources/dey-gupte-article.txt`, Proposition 1 and its proof (printed pp.7–8), Theorem 2 (printed p.12), and the closing single-output observation. Its relaxation rounding keeps one output and gives the output-count approximation. I did not rely on the misleading local slides artifact. The present text does not claim this standard result as a new contribution.
- The Boland–Kalinowski–Rigterink attribution at lines 191–192 is supported by the June 2015 open manuscript, Section 4.2.1, PDF pp.8–9: its output fraction is evaluated at the head of an incoming arc, precisely as in the present destination decomposition. The 2016 reference denotes the later journal publication; I did not equate its final text with the inspected manuscript.
- The caution at lines 513–516 is appropriately limited. The inspected Boland manuscript, Section 4.3, PDF pp.11–12, makes a blanket invertibility assertion that fails on the isolated positive circulation illustrated in the present text. The present text proves its own singular-case treatment and does not accuse the uninspected final journal article of retaining that defect. I found no source-scope problem here.
- The Dey–Kocuk–Santana citation at lines 174–176 supports the relationship between pooling and nonnegative rank-one matrix sets with row/column bounds. The local preprint, PDF p.2, explicitly motivates these bounds by pooling. The author’s [publication list](https://www2.isye.gatech.edu/~sdey30/publications.html) confirms the 2020 publication title, authors, and pages. The manuscript correctly separates arbitrary matrix objectives from physical feed/outlet arc objectives.
- Bibliographic presentation can be polished by putting volume, number, and pages in their own BibTeX fields and filling in the Dey–Gupte page range, but this is not a mathematical or priority finding. No manuscript claim I checked depends on a specific unchecked journal theorem numbering other than the accurately located Remark 2.2.

## Mathematical verification

I checked the physical equations and zero-throughput conventions; affine-rank elimination; the nonnegative rank-one identity and induced objective; destination decomposition; exact single-product projection; the signs and directions of both approximation chains; the shortest-path mixture construction, support bound, and rational-size argument; the conic-hull equalities and capacity counterexample; the cyclic SCC reconstruction, absorption decomposition, negative-cycle alternative, attained optimum, and conditioning example; and the facial-integrality necessity/sufficiency, recognition LP, and fixed-dimension face enumeration. These arguments are coherent under their stated assumptions, apart from Finding 1. In particular, ordinary flow cycles do not invalidate cyclic single-product reconstruction: the proof separates closed circulation components and bounds the remaining rational linear system correctly.

## Verdict and limits

**Major findings present:** one missing essential hypothesis in the endpoint formulation. There is also one minor bibliographic correction involving two author names.

This review checks the complete assigned stage and targeted primary-source claims; it does not establish exhaustive correctness or publication priority. I have not inspected the final publisher PDFs of every cited article, conducted an exhaustive independent search for prior facial-integrality results, checked later paper stages, or assessed the whole paper's eventual contribution statement. All version-specific observations above refer to the named inspected artifacts.
