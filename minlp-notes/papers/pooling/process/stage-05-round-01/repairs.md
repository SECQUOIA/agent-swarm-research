Stage 5, round 1: repair record for accepted m1

The repair agent applied only m1 from `adjudication.md`, after reading that adjudication, `review07.md`, and the exceptional-only branch and surrounding proof in `sections/05-contract-algorithms.tex`. Root retains responsibility for inspecting this repair and closing the stage.

The manuscript now defines `J_E` as the exceptional products with an allowed pool outlet, with `r=|J_E|`. The retained outlet flows and fraction variables are indexed by `J_E`; at every other exceptional product, `v_j=theta_j=0` is a convention, not an added variable. The fraction nonnegativity, outlet identity, and simplex explicitly use `J_E`. The text explicitly retains demand and homogeneous quality bounds for every product in `E_J`, including products without pool outlets, using the already stated quality-mass and throughput expressions.

The empty-outlet case remains the original rational LP with all pool arcs fixed to zero. In the nonempty case, no coordinate was added: there are still `r` fractions and at most `3|E_I|+4|E_J|` core coordinates. The theorem statement, hypotheses, degree and complexity claims, objective, physical lifting argument, and other branches are unchanged. The exact diff below consists of two local hunks in the exceptional-only branch.

Review07's infeasible instance remains rejected by the stated core. Its exceptional products are `E_J={X,Y}`, while `J_E={X}`. Thus `theta_X=1` and `v_Y=theta_Y=0`. The bypass `z_iY` is retained because it is incident to exceptional product Y. Its retained arc bounds give `0<=z_iY<=1`. Y's explicitly retained demand bound gives `2<=v_Y+z_iY<=3`, hence `2<=z_iY<=3`. These inequalities contradict its capacity, regardless of the pool flow. Y's quality mass is `theta_Y Q+C_i z_iY=0`, and its homogeneous quality bounds remain `0<=0<=z_iY`; they do not remove the demand contradiction. The erroneous candidate described by the reviewer, with feed and outlet flow one to X and zero bypass to Y, fails Y's lower demand bound. This is an exact symbolic check of the retained constraints; no numerical experiment or historical experiment rerun was needed.

Validation command, run in `papers/pooling`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The command exited 0. Latexmk ran pdflatex twice and BibTeX once and finished with `All targets (main.pdf) are up-to-date`. The output is a 73-page `main.pdf` (761666 bytes). The first pdflatex pass requested a cross-reference rerun; the second pass resolved it. Inspection of the final `main.log` and `main.blg` found no actual LaTeX/package warnings, undefined references or citations, overfull or underfull boxes, or errors. A broad warning-text scan matched only the `infwarerr` package's descriptive metadata and BibTeX's `warning$ -- 0` function-use count, neither of which is a warning.

The pre-repair Section 5 hash matched the supplied frozen hash. SHA-256 comparison after the repair and build confirmed that all 22 captured protected files were byte-for-byte unchanged: Sections 01–04, the bibliography, the frozen Stage 5 snapshot, the round's adjudication, and all 15 round reviews. The manuscript source edit was limited to Section 5, and this repair record is the only authored process file. Latexmk refreshed generated build artifacts. No review, snapshot, bibliography, accepted earlier section, or later-stage file was edited; no subagent or later-stage work was started.

Section 5 before: `b7930df8e95ebcd597051e24357aaa62f9ee11083642ae1a826c142ecc91aa62`.

Section 5 after: `ccb69faa00989209af3be2b152ca721e51deedf3c2139ea8c3ec0fe87ff02aa5`.

The repair record's own final hash is reported to root separately, since embedding that hash in the file would change it.

Exact manuscript diff against the preserved frozen snapshot:

```diff
--- papers/pooling/process/snapshots/stage-05-round-01.tex
+++ papers/pooling/sections/05-contract-algorithms.tex
@@ -772,10 +772,12 @@
 
 It remains to handle flows whose only active outlets are exceptional.
 Force all ordinary outlets to zero, checking their lower bounds.
-If there are no exceptional outlets, force all pool arcs to zero and
-solve the remaining rational LP. Otherwise let $r\le|E_J|$ be their
-number. Retain exceptional input feeds, these $r$ outlet flows, every
-bypass arc incident to an exceptional node, and $r$ outlet fractions.
+Let $J_E\subseteq E_J$ be the products with an allowed pool outlet and
+put $r=|J_E|$. For $j\in E_J\setminus J_E$, put $v_j=\theta_j=0$
+by convention. If $r=0$, force all pool arcs to zero and solve the
+remaining rational LP. Otherwise retain exceptional input feeds, the
+$r$ outlet flows indexed by $J_E$, every bypass arc incident to an
+exceptional node, and $r$ outlet fractions $\theta_j$, $j\in J_E$.
 There are at most $3|E_I|+4|E_J|$ coordinates. Exceptional source
 withdrawals $A_i=y_i+\sum_jz_{ij}$ are core expressions. Ordinary
 inputs give the local affine feed bounds, while ordinary products now
@@ -796,8 +798,10 @@
 Every term uses only retained coordinates or constants. Summing
 ordinary product contracts and all source equations proves
 $T=\sum_i y_i$ and $Q=\sum_iC_i y_i$ for every local lift. Impose
-$\theta\ge0$, $\sum\theta_j=1$, and $v_j=\theta_jT$ on the exceptional
-outlets. Keep their demand and quality bounds, using mass
+$\theta_j\ge0$ and $v_j=\theta_jT$ for $j\in J_E$, and
+$\sum_{j\in J_E}\theta_j=1$. Keep the demand and homogeneous quality
+bounds at every $j\in E_J$, including products without pool outlets,
+using quality mass
 $\theta_jQ+\sum_iC_i z_{ij}$ and throughput $v_j+\sum_i z_{ij}$,
 as well as all retained arc and source bounds. These rows are quadratic
 in a fixed number of variables independently of the ambient quality
```

Protected-file SHA-256 manifest, verified unchanged after the repair and build:

```text
42325c354526840aa25926e4520974f413d6b2254209153140b8fb480a0e2c3c  papers/pooling/bibliography.bib
b7930df8e95ebcd597051e24357aaa62f9ee11083642ae1a826c142ecc91aa62  papers/pooling/process/snapshots/stage-05-round-01.tex
d5057d29d05c03b85d5a587ce711759ea19bafc84ed884dec29418bb400cb197  papers/pooling/process/stage-05-round-01/adjudication.md
b1b1161d4da7d32e0f5c1ee6edb16a586aec0c67288f9652547424c494e575dc  papers/pooling/process/stage-05-round-01/review01.md
85375e6c6215291a29d67b8e1aae27a7b155624fcccab8de975fab00be1e7659  papers/pooling/process/stage-05-round-01/review02.md
0e294da25bcdf45091f3cf0d8894c8680bf2272a21ddca4a163a7ac75993b6b4  papers/pooling/process/stage-05-round-01/review03.md
ee5c1398e13b345176347496ecd47a5daeef2397c13c364737fa41772ea920bb  papers/pooling/process/stage-05-round-01/review04.md
82f771ea3ce3cbed052b94ecef25f8ed44b92c19779054fc3180829a30971443  papers/pooling/process/stage-05-round-01/review05.md
4d0acdbcf16e1afe578c3dd9e830c237074cd6d0a44886d1a9e466a040668172  papers/pooling/process/stage-05-round-01/review06.md
1f73d5cf19bb4151e56024422847a9c9d2d1ad18bebee1f4bbf364537bab7100  papers/pooling/process/stage-05-round-01/review07.md
c5c55abeb66aab112518988d96a232640609fe9ac5f30a4bd402b1d24d5006d5  papers/pooling/process/stage-05-round-01/review08.md
e9314fb76fb8951fc5a63e1abe81426f02c6b9401b894c17b239b3ce17320e08  papers/pooling/process/stage-05-round-01/review09.md
c07e16864ddec4ab9a3590d22319dbd92ae8b979b6be99978727cd98f063ffda  papers/pooling/process/stage-05-round-01/review10.md
385fd263b66fee45bd155941ed30c65568e699d2beec0fae255d6f8e74da098d  papers/pooling/process/stage-05-round-01/review11.md
dae066a96aafc0e42b886fc0d2de3b8b22f1ef78e1be29a898b9d3764ea296de  papers/pooling/process/stage-05-round-01/review12.md
b79618ca895f3a980821ec5c0eea31601d8b4439948d77e389b15bd40c69c93f  papers/pooling/process/stage-05-round-01/review13.md
8df88dd235fa48caa570129fef721982cff00bc4ed4214530973c59e761e021a  papers/pooling/process/stage-05-round-01/review14.md
a0f516b91c171eb4cd895589a1ef916bfda3f4e7a6248695a51aaacfdd0e1b59  papers/pooling/process/stage-05-round-01/review15.md
e023daa9d8ceb445d931e193dce9d47ae1934e17ac13b54d4591710e3f8f76ae  papers/pooling/sections/01-foundations.tex
8abd1d862cc58d23ee4671f2610c02ca04c27390353ba023b442325565514e67  papers/pooling/sections/02-algebraic-complexity.tex
b8201a4bc6a61d4304f888649afe97bfc4aeefd9234d314a8cae3b805b3fad40  papers/pooling/sections/03-restricted-hardness.tex
88b1c181cde7f72b48535054de702a2ff4688a470633eb56e528c519974189de  papers/pooling/sections/04-structural-algorithms.tex
```
