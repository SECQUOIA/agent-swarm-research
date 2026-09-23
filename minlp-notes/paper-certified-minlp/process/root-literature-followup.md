# Additional primary literature for Stage 5 integration

These sources supplement the accepted Stage 1 comparison. They further restrict
novelty to the documented certificate integration, checked semantics and audit;
rigorous numerical lower bounds and support-function correction are established.

1. Christian Jansson, **A Rigorous Lower Bound for the Optimal Value of Convex
   Optimization Problems**, Journal of Global Optimization 28(1), 121–137 (2004),
   DOI `10.1023/B:JOGO.0000006720.68398.8c`. Publisher/institutional abstract and
   author's official bibliography checked at
   https://tore.tuhh.de/entities/publication/04aeefc8-d033-4fb5-84aa-fb27d8aaac2e
   and https://www.tuhh.de/ti3/publications.shtml?author=jansson . The abstract
   describes rigorous lower error bounds for convex optimization, including
   uncertain interval coefficients. The old linked 2003 PostScript is unavailable;
   do not imply that the 2004 full text was read.
2. Christian Jansson, **On Verified Numerical Computations in Convex Programming**,
   Japan Journal of Industrial and Applied Mathematics 26, 337–363 (2009), DOI
   `10.1007/BF03186539`. Full author manuscript read at
   https://www.tuhh.de/ti3/paper/jansson/ConvexPshort081117.pdf . PDF pp. 1–2
   explicitly situate verified convex/conic relaxations in reliable global and
   combinatorial optimization. Useful general attribution, not a claim of saved
   MINLP certificate replay.
3. Frédéric Messine and Gilles Trombettoni, **Reliable Bounds for Convex Relaxation
   in Interval Global Optimization Codes**, AIP Conference Proceedings 2070,
   020050 (2019), DOI `10.1063/1.5090017`. Full four-page author workshop version:
   https://www.lirmm.fr/~trombetton/publis/reliableconvexrelaxation_gow_2018.pdf .
   PDF p. 2 Theorem 1 minimizes a supporting affine function over a finite box;
   PDF p. 3 Theorem 2 uses a Lagrangian support, explicitly attributed to Jansson.
   Our finite-box correction is an application of this established support
   minimization to the residual after subtracting the proposed affine row. Do not
   claim a new general rigorous bounding principle. Verify final metadata when
   adding the bibliography entry.
   Follow-up: the publisher-deposited Crossref record at
   https://api.crossref.org/works/10.1063/1.5090017 confirms both authors, year
   2019, AIP Conference Proceedings volume 2070 and page/article locator 020050.
   The author's publication page also lists the separate 2018 workshop version.
4. Sourour Elloumi, Amélie Lambert, Bertrand Neveu, Gilles Trombettoni,
   **Global solution of quadratic problems using interval methods and convex
   relaxations**, Journal of Global Optimization **91(2), 331–353 (2025)**,
   DOI `10.1007/s10898-024-01370-8` (online 12 February 2024; use issue year 2025).
   Publisher metadata https://doi.org/10.1007/s10898-024-01370-8 . Full author
   manuscript downloaded from https://hal.science/hal-04016716v2/document to
   `/tmp/cert-minlp-qibex.pdf`; extracted text `/tmp/cert-minlp-qibex.txt`.
   Section 5, manuscript pp. 11–14 (PDF one page later), describes QIBEX-R's
   reliability: curvature correction and rigorous lower bounding inside an
   interval branch-and-bound method for quadratic mixed-integer problems.
   Section 5.2 explicitly applies Jansson/Messine–Trombettoni. Describe the
   reported approach; this reading is not an independent validation of its
   complete implementation or every proof. Contrast our explicit saved-artifact
   contract and replay architecture, without asserting that their software lacks
   all proof export features or claiming priority beyond inspected evidence.

Integration recommendation: one concise prior-work paragraph with these sources,
and an attribution next to the finite-box correction theorem if useful. Keep the
main contribution statement concrete; no broad first-ever claim is needed.
Do not copy these downloaded literature PDFs into a distributed supplement.

Additional wording precision for integration: the Baes et al. source's Theorems 1
and 3 bound the **number of certificate points** by 2^n (n integer variables);
this is not a bound on the bit length of their real-valued data or on the
coordinate dimension. Replace the introduction's loose “certificate size” with
“number of certificate points” when presenting that specific comparison. Root
checked the local full text, especially the paragraph immediately before
Theorem 1 and the constrained certificate discussion. No underlying novelty
claim or theorem in this paper changes.
