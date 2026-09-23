# Stage 5B query/output author audit

Authored `sections/12d-query-output.tex` only; parent must integrate it and the bibliography entries below. No shared main/bibliography/source-map edit was made. Prefix: `query:`. Syntax-only isolated qipm pdflatex check passed (8 pages); undefined references/citations are expected in that isolated driver. The one overfull line found there was changed to a display. Parent should run the full reference-resolving build.

## Source disposition

- `symmetric-cone-exposed-rank-query-readout-boundary`: full mathematical theorem retained, explicit rank-one EJA certificate normalization, exact Delta=1, constant-distortion Fourier/Holevo proof, real-coordinate Albert scope, controlled rotations and classical compilation. Earlier rank-frontier/quantifier-reversal and movement theorems cited, not duplicated.
- `hermitian-exposed-rank-query-readout-boundary`: subsumed by all-EJA result; its R/C/H normalizations match Lemma perspective. Retained the whole-affine-slice certificate requirement and raw clean-bit contract.
- `product-disk-central-readout-query-hierarchy`: full finite checkpoint, parity/OR, optimizer output, exact simple states, sliced precision laws, hidden equality transfer, same-PSD-formulation movement retained. Corrected half-gap ties to strictly smaller than half-gap; retained heralded versus deterministic state distinction; output/norm restrictions explicit.
- `one-sharing-cone-disk-qipm-separation`: same public-objective sparse equality family retained; optimal ambient parameter refers to already proved shared spectral theorem; full all-LH primal--dual movement with precise central-start and gap-target scope; displayed barrier state claims only. Verified strict primal and dual Slater points.
- `product-ball-central-state-readout-separation`: retained unique-mark diagnostic family, exact central point, cap-optimal formulation reference, joint k-output adversary/direct sum, exact known-number amplitude-amplification upper bound (no log loss), randomized direct sum, scaled Hessian condition 27/2 and direct branch 5/3. Newton structural details belong to sibling Newton section.
- `one-lorentz-constant-barrier-value-lower`: retained direct-ball raw-normalized precision comparison with exact OPT, checkpoint derivative, conditioning, heralded exact state preparation, explicit-output threshold, hidden-equation equivalent encoding, and same fixed-barrier movement. Explicitly a different body from sliced product disks, not a same-body reformulation comparison.
- Context-only spectral low-rank readout, sparse parity chains, zero-query conversion, normalized-shift staircase, and dynamic repeated QLS are separate solver/access projects; no new claim here needs them. In particular fixed-input queries are never multiplied by path checkpoints. Parent should retain their existing context disposition rather than claim full coverage of unrelated QLS projects.

## Independent author checks

1. EJA rank-one eigenvalue `(q+1)/(2q)` times reference compression `2/(q+1)` is `1/q`; the rank-q support scale is exactly1. The reference is Slater, not called analytic center. Structured primal lifted vectors have only linear hidden signs, unlike a packed PSD fiber Gram matrix.
2. Recovery proof derived at amplitude level (degreeT), not probability degree2T. Ensemble span dimension sum_{j<=T}binom(n,j); purification includes input-independent randomness. Expected error on arbitrary failure at most `(1+4epsilon)/3<1/2`; elementary conditional entropy proves rate-distortion inequality, without invoking a stronger per-bit worst-case guarantee.
3. Full-disk bit is directly the axis output register: one clean query suffices, with no unused bit garbage. Sliced unequal-magnitude preparations query/rotate/uncompute and postselect: only O(1) expected heralded exact or bounded-error worst-case, not deterministic exact. Predictor claim only at displayed finite checkpoint and for central derivative RHS.
4. Hessian h(a)=sqrt(1+a²)(sqrt(1+a²)+1), and h(a)/a²=s/(s-1) decreasing proves h(2a)<=4h(a). Sliced checkpoint gap `(sqrt17-sqrt5)/(2sqrt5)` checked algebraically. Direct-ball checkpoint value simplifies to `-Gamma(sqrt(1+phi²)-1)`, avoiding an unnecessary derivative expression.
5. Classical mean lower regime uses concentration only above C/sqrtN, then monotonicity for fine errors; raw SQ magnitude data public, reduced coefficient norm excluded. Canonical coherent completions include public reference slot so controlled phase/clean-bit equivalence holds with constant overhead.
6. Joint unique-mark diagnostics use positive spectral adversary (HLS2007 Theorem1), valid multi-output, avoiding the negative-weight theorem's error-constant subtlety. Tensor-factor sum has norm ks/2 and masked norm sqrt(s/2). Exact known-number amplification gives sum_{j=1}^k sqrt(ks/j)=O(k sqrt s).
7. Norm-tree/packed movement results are only invoked with their own proven standard metric scope. Shared cone theorem is all ambient LH barriers but requires exact central primal--dual start; no easy state claim for arbitrary barrier. Query and movement lower bounds combine by maximum.
8. Global smooth cap-frontier class is the previously defined full-slack selection class; sliced interval domains are not assigned full-product disk minimality.

## Primary literature checked

Read local literature notes for Beals2001, NayakWu1999 and Hoyer2005 composition; these packages currently expose `paper.md` only. Opened primary full texts online:

- Beals et al., https://arxiv.org/pdf/quant-ph/9802049 ; amplitude polynomial method and parity. Journal metadata confirmed by author Cleve's publication page and Rutgers institutional record: JACM48(4),778–797,2001, DOI10.1145/502090.502097.
- Nayak--Wu, https://www.math.uwaterloo.ca/~anayak/papers/NayakW99.pdf ; central separated weights / additive counting. Existing `NayakWu1999` bibliography entry used.
- Nayak, https://www.math.uwaterloo.ca/~anayak/papers/Nayak99.pdf ; Holevo/entropy theorem; author publication page https://www.math.uwaterloo.ca/~anayak/Site/Publications.html explicitly lists FOCS1999 pages369–376. IEEE primary DOI10.1109/SFFCS.1999.814608. Some secondary metadata incorrectly says369–377; use author's369–376, consistent with8-page primary PDF.
- Hoyer--Lee--Spalek, https://arxiv.org/pdf/quant-ph/0611054 ; Theorem1 states positive spectral adversary lower bound for arbitrary finite output. Theorem2's negative-weight general-output coefficient differs; not needed. Author primary page https://www.ucw.cz/~robert/papers.html confirms STOC2007,526–535. Author bibliography https://www.ucw.cz/~robert/papers/bib.html confirms same.
- BHMT2002 primary arxiv quant-ph/0005055: exact amplitude amplification when success probability known, estimation; existing bib entry used. BBBV1997, vanDam1998, ApersGribling2026 existing entries used as classical ingredients/comparators.

No novel Boolean query or generic quantum-IPM lower bound claimed. The manuscript's novelty is restricted to explicitly proved conic synthesis, exact scales and access distinctions; no priority claim inferred from failure to find an older matching paper.

## New bibliography entries for parent integration

```bibtex
@article{Beals2001,
 author={Beals, Robert and Buhrman, Harry and Cleve, Richard and Mosca, Michele and de Wolf, Ronald},
 title={Quantum Lower Bounds by Polynomials},
 journal={Journal of the ACM}, volume={48}, number={4}, pages={778--797},
 year={2001}, doi={10.1145/502090.502097},
 eprint={quant-ph/9802049}, archivePrefix={arXiv}}
@inproceedings{Nayak1999,
 author={Nayak, Ashwin},
 title={Optimal Lower Bounds for Quantum Automata and Random Access Codes},
 booktitle={Proceedings of the 40th Annual IEEE Symposium on Foundations of Computer Science},
 pages={369--376}, year={1999}, doi={10.1109/SFFCS.1999.814608},
 eprint={quant-ph/9904093}, archivePrefix={arXiv}}
@inproceedings{HoyerLeeSpalek2007,
 author={H{\o}yer, Peter and Lee, Troy and {\v S}palek, Robert},
 title={Negative Weights Make Adversaries Stronger},
 booktitle={Proceedings of the Thirty-Ninth Annual ACM Symposium on Theory of Computing},
 pages={526--535}, year={2007}, doi={10.1145/1250790.1250867},
 eprint={quant-ph/0611054}, archivePrefix={arXiv}}
```
