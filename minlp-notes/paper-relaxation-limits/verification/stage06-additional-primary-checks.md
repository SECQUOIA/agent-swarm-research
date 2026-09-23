# Additional primary checks for Stage 6 preparation

Coordinator direct checks, 2026-09-06 local date. This is source preparation,
not authoring or acceptance of Stage 6. Literature instructions were read;
no literature package, generated index or bibliography was modified.

## Approximate LP source

Braun, Fiorini, Pokutta and Steurer, *Approximation Limits of Linear Programs
(Beyond Hierarchies)*, author manuscript dated July 2, 2013:
https://www.bayesianestimation.org/paper/approxlp.pdf . Downloaded to
`/tmp/minlp-relaxation-limits-sources/braun2013-approxlp.pdf`, SHA-256
ac7119dc3ed440f3f1e3a5b103b34d16435c76d0865f294ba0c181a2dfbb475b.

Read the hard-pair definition and Theorem 6(i), printed/PDF page18; visually
checked that page. Its fixed dilation factor2 supplies the exponential LP
sandwich lower bound used in the repository. Also read Section4.3/Lemma9,
which gives a small PSD lift for that pair: it cannot itself supply the
unrestricted SDP lower bound. The local bibliography metadata records the
published article in Mathematics of Operations Research40(3),756–772(2015),
DOI10.1287/moor.2014.0694. The inspected author version has different
pagination from the local arXiv package. No full audit of the external
rectangle-corruption proof is claimed.

## Monotone-system convergence antecedents

Read Stewart, Etessami and Yannakakis, author manuscript Section4.1,
equation18 and its following argument (PDF21–22, printedA:21–A:22), and
visually checked both pages. Primary URL:
https://homepages.inf.ed.ac.uk/kousha/final-jacm-cav13-jversion.pdf .
The local original SHA-256 is
e6fb2c29e17560818491fd7fa6ddf91352f79b89601b588345536d124b2a20fe.
The source explicitly gives the scalar critical quadratic, an error-amplifying
chain, and repeated-squaring small fixed points. Its Newton result is distinct
from the repository's bidirectional primitive FBBT contractor theorem.

Read Esparza, Kiefer and Luttenberger, Section7/Theorem7.1 and proof, local
arXiv author version PDF34 (visual equation14 and theorem included), SHA-256
d8375a6deca95523b703d0664686063eee714619d29a457ae094ab0a09a75005.
Primary https://arxiv.org/pdf/1001.0340 . Published SICOMP39(6),2282–2335,
DOI10.1137/090749591. This is the original slow-Newton chain antecedent;
its exact formula differs from Stewart's simpler variant.

Coordinator inference, if a Kleene comparison is useful: for Stewart's chain,
Kleene errors satisfy e_0(k+1)=e_0(k)-e_0(k)^2/2 and
 e_i(k)>=sqrt(e_{i-1}(k)), since each iterate is below its next update.
Induction gives e_0(k)>=1/(k+1), hence e_n(k)>1/2 when
k+1<2^(2^n). Thus doubly exponential ordinary monotone iteration alone
is already a consequence of established examples. This is an elementary
inference from the displayed source system, not a quoted source theorem.
No new result is proposed from it. The repository's specific restrictions
remain primitive bidirectional interval hulls, every fair schedule, and one
feedback component linear after fixing its acyclic inputs.

## Classical Shapley–Folkman input

Starr, *Quasi-Equilibria in Markets with Non-Convex Preferences*, Econometrica
37(1),25–38(1969), DOI10.2307/1909201. Author-hosted public original:
https://econweb.ucsd.edu/~rstarr/Non-Convex%20Preferences.pdf .
Read Appendix2, Lemma2/corollary and complete proof, printed35–36
(PDF12–13 due to the prefatory page); visually checked both original pages.
They give the at-most-d exceptional-summands statement needed for the
repository's compact-set scaling comparison. The any-norm diameter estimate
and Lipschitz consequence then follow directly; no constrained rounding
claim follows without preserving added constraints.

Browser fetch failed502; ordinary HTTPS download failed because the public
server certificate expired. The public scholarly PDF was then retrieved
with certificate verification disabled, without credentials or bypassing
an access control. Its original printed title/author/journal metadata match
the JSTOR issue listing. SHA-256:
cc89b844233d50dda436a8bb7ea63de12531cfd77633ba11387daea16401ad42.
Saved only at `/tmp/minlp-relaxation-limits-sources/starr1969.pdf` with
extracted text alongside. This retrieval detail limits transport authentication;
the mathematical statement and proof were read directly.

Primary page renders inspected are in verification/stage06-source-renders/.
The accidentally first rendered Starr printed34 is only a pagination check;
the substantive inspected theorem/proof pages are35–36. No claim of reading
all unrelated equilibrium theory or the complete external fixed-point
literature is made.


## Adjacent integer-precision context

Read Lubin, Vielma and Zadik, author original arXiv1706.05135, Definitions4.2–4.3 and Lemma4.1 with its complete parity proof; visually checked PDF/printed12. Local SHA78a871cefbb4027435c0b0952c3a29e0d23260c3e76e8236150651add70c83b8. Published DOI10.1287/moor.2021.1146. The integer-parity mechanism is established; arbitrary-accuracy graph bounds are a quantitative application, not a source theorem as stated.

Read Beach et al., local original arXiv2211.00876v1, Section5.1.1 and Proposition2; visually checked PDF/printed21 for the sawtooth overerror2^(-2L-2). Local SHAa1d71952719c8c9c7917213964676802bb4e37de085a80ddd5801cec991e726f. This package contains the 2022 combined PREPRINT, with different numbering from published PartI. Cite the inspected version explicitly if using its locator; do not claim publisher-page verification from this file. Printed21 confirms the rate used in a brief resource comparison. No audit of all this preprint's formulations is claimed.

The root also read the scaling audit and full rectangularity correction, and the scalar binary source including its midpoint and area proofs. The simultaneous-bilinear source's parity/width lower proof and shared-expansion upper construction were read through its displayed formulation; later algorithmic/novelty sections are unnecessary for this supporting comparison and are not claimed read here.


### Locator recheck after author query

On fresh recheck, the exact local Beach package above remains the71-page2022v1 original; pdftotext -f21 -l21 again gives Section5.1.1 and its stated rate. An initial hypothesis of concurrent replacement was not supported and is withdrawn. The author is comparing its file/render path; the preserved root render matches this exact PDF. Freshly computed hashes:
- beach2024-enhancements-of-discretization-approaches-for/original.pdf: a1d71952719c8c9c7917213964676802bb4e37de085a80ddd5801cec991e726f
- lubin2022-mixed-integer-convex-representability/original.pdf: 78a871cefbb4027435c0b0952c3a29e0d23260c3e76e8236150651add70c83b8

Resolved: author initially selected the different package `literature/papers/beach2022-compact-mixed-integer-programming-formulations/original.pdf` (arXiv2011.08823v2). The intended package path is `literature/papers/beach2024-enhancements-of-discretization-approaches-for/original.pdf` (arXiv2211.00876v1); its page21 locator remains correct. No source replacement occurred.


## Belotti nonempty-limit qualification, Stage6 review follow-up

On September7,2026, the coordinator directly extracted and read original PDF13–15 of `literature/papers/belotti2012-on-feasibility-based-bounds-tightening/original.pdf`, and visually inspected original page14 using reviewer11's saved render. Theorem4.1 conditions its LP recovery of the FBBT limit on the limiting box being nonempty. The following infeasibility discussion explicitly says that an empty FBBT result need not make that LP infeasible. This supports accepted local finding R11-1; the introduction must state the qualification. Both manuscript constructions are feasible and their proofs do not rely on this contextual LP result. The original SHA remains `8f3c24c55422b5c65483dc7bd2f70d7233df69d9218386628fc8cebacd90196e`.
