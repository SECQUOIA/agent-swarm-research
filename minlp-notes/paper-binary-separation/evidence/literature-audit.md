# Literature audit: separation complexity

**Review cutoff:** 6 October 2026. This is a focused, claim-driven review of
the cited predecessors and adjacent exact-separation results for the
hypermetric, rounded-PSD, gap-1, Boolean-quadric, and integer-quadratic split
families. It covers the source lists and notes supplied with the manuscript,
the named novelty-sensitive citations, and the direct citation chains needed
to distinguish unrestricted separation from bounded-gonality, bounded-family,
or fixed-coefficient problems. A failure to find a matching proof in this
bounded review is not a priority claim.

## Claim and source ledger

| Manuscript issue | Source evidence inspected | Safe reading for the manuscript |
|---|---|---|
| Unrestricted hypermetric separation | Avis and Grishukhin (1993), §4, problem P6 and the ensuing discussion; Avis (2003), §1, p. 1; Deza and Grishukhin (1997), report pp. 3–4. The first source proves co-NP membership and distinguishes bounded `(2m+1)`-gonality testing (co-NP-complete) and “strong hypermetricity” (output the smallest violated gonality; NP-hard) from yes/no unrestricted recognition. Avis (2003) explicitly says the unrestricted separation status is unknown. Deza and Grishukhin describe hypermetric-correlation recognition as co-NP and state that NP-hardness was unknown. | These results do not establish hardness of the exact unrestricted decision problem studied here. The paper can safely say that the primary complexity literature left that problem open, then state that it gives a complete reduction for its precise input model and promises. Do not describe the bounded-gonality or output problem as unrestricted separation. |
| Secondary hypermetric-hardness assertions | Liers (2004), thesis p. 23, §1.3 (“Known facets of the cut polytope”), says ordinary hypermetric separation is NP-hard and cites Deza and Laurent (1997), Chapter 28. Krishnan and Terlaky (2005), §6 (“The hypermetric inequalities”), author manuscript p. 32, makes a similar assertion for inequalities with `a^T X a >= 1`, odd coefficient sum, and `min_{x∈{−1,1}^n}(a^T x)^2=1`. The author manuscript occupies book pp. 101–157, so its p. 32 corresponds to book p. 132. Neither passage supplies a reduction. | Preserve these statements as secondary evidence that hardness was anticipated, while disclosing that no proof is supplied there. The Liers paragraph concerns ordinary hypermetrics. The Krishnan–Terlaky condition is gap-1 under this manuscript’s definitions, a subclass of rounded-PSD inequalities; it is not evidence for the entire rounded-PSD class. The cited Deza–Laurent chapter was not retrieved, so the secondary citation chain could not be checked directly. |
| Gap-0 computation versus gap-0 separation | Galli, Kaparis, and Letchford (2012), §2, journal p. 150, define `γ(b)` and state that testing `γ(b)=0` for a specified integer vector is equivalent to PARTITION and is NP-complete. Their §4, p. 151, says separation for the remaining gap and cut-polytope families is unknown, including gap-0 separation. Galli, Kaparis, and Letchford (2011) studies gap inequalities in nonconvex MIQPs but does not settle this exact separation problem. | The known PARTITION result concerns computing/testing a property of a fixed coefficient vector. It is not a reduction for finding a violated gap-0 inequality at a supplied point. The manuscript’s separate point-separation reduction therefore addresses a distinct decision problem. |
| Hypermetric-correlation, rounded-PSD, and Boros–Hammer relationships | Letchford and Sørensen (2012), §5.3 and conclusion, journal p. 270, give reductions among the hypermetric-correlation, rounded-PSD, hypermetric, and Boros–Hammer settings and call the relevant unrestricted separation complexity an open question. The manuscript’s covariance and family mappings are also proved directly. | Cite the earlier reductions and open-problem statement, but do not present the correspondence itself as new. The manuscript’s novelty-sensitive claim is the reduction and its stated promises for the exact separation languages. |
| Boolean quadric family definitions and open questions | Letchford (2022), accepted author manuscript, §3.1, pp. 8–9, equations (10)–(13), distinguishes Padberg clique, cut, signed generalized-cut, and unrestricted Boros–Hammer families. In §7.2, pp. 18–20, it records unknown separation complexity for the Padberg families and related cut-polytope classes; §8, p. 21, explicitly asks whether hypermetric separation is polynomial. | For the signed-coefficient Boros–Hammer family, `S,T` are disjoint and `s` ranges over all integers; the facet condition `1-|T| <= s <= |S|-2` (with `|S|+|T| >= 3`) is narrower and is not a validity-family restriction. For Padberg clique inequalities, `0 <= s <= |S|-1` is the family range and `1 <= s <= |S|-2` is the facet range when `|S| >= 3`; Padberg cut is the signed family with `s=0`. Keep these definitions and facet conditions separate. The open-problem survey supports a qualified novelty claim, not priority clearance. |
| Boolean quadric clique/cut and odd-clique facets | Padberg (1989) is the primary source for the BQP clique/cut families; Letchford (2022), equations (10)–(13), gives the definitions and ranges in a directly locatable form. Barahona and Mahjoub (1986), original p. 159, Theorem 2.1, proves validity of the all-positive clique inequality and that it is a facet when the clique size is odd. Galli et al. (2012), §2, identifies the odd-clique cut family; Letchford (2022) records its separation status as open. | The all-positive odd-clique attribution to Barahona–Mahjoub is correct. The manuscript supplies its own facet argument for the specific witnesses. Padberg/BM facet facts are background, not the technical basis for the new hardness proof. |
| Polynomially separable proper subclasses | Letchford and Sørensen (2014), full author copy, gives exact separation for particular odd bicycle-wheel and `(2p+1,2)`-circulant families and switchings. Kaparis, Letchford, and Mourtos (2022), full author copy, gives an `O(n^5)` separator for generalized and extended generalized 2-circulant classes. Neither is a separator for all odd-clique, hypermetric, rounded-PSD, or Boros–Hammer inequalities. | Mention these only to delimit the tractable subclasses; they do not undermine the full-family hardness claims. |
| Recent QCQP context | Dey et al. (2026), arXiv v1, §4.1.2, pp. 15–16, uses a nonconvex integer-quadratic subproblem to search for Boros–Hammer-related eigenvector cuts in computational SDP-relaxation experiments. Each variable coefficient `w_i` is restricted to `[-2,2]`; the offset `w_0` is integer and is not bounded. | The introduction’s sentence is accurate when it says “bounded variable coefficients.” Avoid saying that all coefficients are bounded or that this is an exact separator for the unrestricted family. |
| General integer-quadratic split separation | Buchheim and Traversi’s 2013 Optimization Online author preprint, §§3–4, equations (5)–(7), studies unnormalized split separation for general integer-quadratic moment matrices and leaves its complexity open. The published 2015 article is cited in the manuscript. Burer and Letchford’s 2011 author preprint, §5.2, Proposition 11, and §8, also poses a related open separation question. Caprara and Letchford (2003), Theorem 1, journal p. 286, proves strong NP-completeness for split-cut separation in mixed-integer linear programming. | General MILP split-cut hardness does not imply hardness for the IQP moment-matrix input, particularly under binary diagonal/first-row identities. No inspected source establishes the manuscript’s normalized-threshold XP bound, rank-one gcd formula, or `{0,1}`-restricted IQP split hardness. The paper makes no separate novelty claim for its lattice algorithm. The binary hard instances do imply unrestricted integer-quadratic split hardness if the stated embedding proof is correct. |
| Exact fixed-rank CVP bound | Kannan (1987), §4, Theorem 4.5, in the openly hosted CMU-CS-96-105 author report (report p. 24), gives `O(r^r s)` arithmetic operations for rational-basis/target CVP with input length `s` and bounds intermediate rational bit lengths by `O(r^2(s+log r))`. Thus it yields `r^{O(r)} poly(L)` bit time. The theorem is stated for rational vectors in `Q^r`; the manuscript’s rational-Gram input is represented by an explicit polynomial-size rational Euclidean embedding. | Attribute the fixed-rank bound to Kannan, but describe the Gram-only implementation as an exact representation-level application/inference. The theorem is not literally stated for Gram-matrix-only input. The theorem locator is secure; a precise crosswalk from report p. 24 to the journal pagination was not established. |
| Polynomial HNF/preimage step and standard reductions | Kannan and Bachem (1979) is the cited source for polynomial-time Smith/Hermite normal forms and integral solutions. Karp (1972) and Garey–Johnson (1979) are the standard cited complexity references. Full source text for these three works was not obtained in this review. | Their bibliography metadata and identifiers were checked, but the exact theorem locators were not source-audited here. Keep the manuscript’s HNF and NP-completeness claims proved or stated self-contained where possible; do not attribute an unverified theorem number. |

### Novelty wording supported by this review

The current introduction’s qualified sentence is appropriate: “To the best of
our knowledge, no prior work gives complete proofs of the unrestricted
hardness results in the first, second, and fourth items with the stated
domains and promises.” It should remain tied to those exact problems and
promises. The directly inspected primary sources leave unrestricted
hypermetric or related family separation open; the two older secondary
hardness assertions are disclosed as assertions without reductions. The
review does not clear priority beyond that bounded source set.

The distinction among the relevant problems should remain explicit:

- Avis–Grishukhin/Avis: bounded-gonality testing and a “strong” output task;
- Liers: ordinary hypermetric separation assertion, with no reduction shown;
- Krishnan–Terlaky: gap-1 assertion under a restricted minimum-value condition,
  with no reduction shown;
- Galli–Kaparis–Letchford: NP-completeness for `γ(b)=0` for a specified
  coefficient vector, separate from point-separation for gap-0 inequalities;
- Caprara–Letchford: generic MILP split cuts, separate from IQP split
  inequalities over structured moment inputs.

## Inspected-source record

The following full sources were inspected for the claims above, either from
the round-1 lawful retrievals or from existing project source copies whose
manifest records the public author/repository URL: Avis–Grishukhin (1993),
Avis (2003), Deza–Grishukhin (1997), Deza–Grishukhin–Laurent (1993),
Krishnan–Terlaky (2005), Liers (2004), Padberg (1989), Barahona–Mahjoub
(1986), Galli–Kaparis–Letchford (2011 and 2012), Letchford–Sørensen (2012 and
2014), Letchford (2022), Caprara–Letchford (2003), Buchheim–Traversi (2013
author preprint), Burer–Letchford (2011 author preprint), Letchford (2010),
Kaparis–Letchford–Mourtos (2022), Dey et al. (2026, arXiv v1), and Kannan
(1987, author report). Important statements and the Barahona–Mahjoub facet
equation were checked against the source PDFs where needed. Kannan’s report
Theorem 4.5 was checked against the extracted text and locators.

The Krishnan–Terlaky page crosswalk is based on the author manuscript’s p. 32
and the chapter pagination pp. 101–157; the current introduction therefore
cites its section/subheading without asserting a page. The bibliography
fragment is ready at `evidence/literature.bib` and matches
`references.bib`. It protects capitalization needed by plainnat, including
Boolean Quadric, Max-Cut, NP, Smith, Hermite, and the Dey arXiv identifier and
version URL.

## Supplied-batch and KB receipt

The identified-source batch is recorded intact at
`evidence/literature-run/round-1/` (copied from the unique temporary run
`/tmp/binary-separation-lit.QevKVJ/round-1/`) with five `lane-*.jsonl` files,
`candidates.jsonl`, `decisions.jsonl`, and `results.jsonl`. The ingest session
64190 exited 0. The batch produced 16 package creations and one duplicate
rejection; the candidate outcomes are summarized below. `lit.py check` was
run once after ingestion and exited 0 with `KB_CHECK=ok`, `UNREAD=171`, and
`READ_UNCITED=752`; three preview warnings concerned unrelated records.
Packages remain `status: unread` in the shared KB because this work was
released before notes could be edited. That status does not mean the local
source review above was not performed.

| Candidate | Batch outcome | Source review outcome |
|---|---|---|
| Deza–Grishukhin (1997) | Created, open full text | Read; primary open-status statement inspected. |
| Krishnan–Terlaky (2005) | Created, open full text | Read; secondary gap-1 assertion and definition inspected. |
| Liers (2004) | Created, open full text | Read; secondary ordinary-hypermetric assertion inspected. |
| Boros–Hammer (1993) | Created, access none | Full paper not retrieved; see missing-source list. |
| Kaparis–Letchford–Mourtos (2022) | Created, open full text | Read; exact subclass separator inspected. |
| Hrga–Povh (2023) | Created, access none | Full paper not retrieved; metadata only. |
| Barahona–Mahjoub (1986) | Created, open full text | Read; Theorem 2.1 visually checked in original PDF. |
| Padberg (1989) | Rejected as duplicate; existing read package reused | Full source already in KB and read. |
| De Simone (1990) | Created, access none | Full paper not retrieved; see missing-source list. |
| Letchford–Sørensen (2012) | Created, open full text | Read; reductions and open-status locator inspected. |
| Galli–Kaparis–Letchford (2012) | Created, open full text | Read; `γ(b)` and separation distinctions inspected. |
| Letchford–Sørensen (2014) | Created, open full text | Read; polynomial subclasses inspected. |
| Letchford (2022) | Created, access none after the KB downloader timed out | Existing author copy in `research-20261001/binary-separation/sources/` was read; this is an ingest/retrieval failure in the KB batch, not missing review content. |
| Dey et al. (2026) | Created, open full text | Read; arXiv v1, §4.1.2 inspected. |
| Kannan (1987) | Created, open full text | Author report read; theorem 4.5 inspected. |
| Avis–Grishukhin (1993) | Created from identified local source | Full author-posted source read. |
| Deza–Grishukhin–Laurent (1993) | Created, access none in batch | Existing publicly sourced copy in the project source directory was read; KB candidate remains access none because no file/URL was supplied to that candidate. |

The KB mutation was serialized at the user’s later direction. The active
ingest was allowed to finish and its required check completed; the owner then
ceased all KB writes and checks. No second mutation was queued. Release
notifications to the sparse root and the reusable Luna-max literature lead
were successfully delivered by the parent. The intact temp run was not copied
into `literature/runs/` because that would have been a further shared-KB write
after release. Future promotions or note updates must go through the single
reusable literature lead.

## In-scope source content still unavailable to the KB review

The following list includes every access-none candidate from the supplied
batch, even where another existing local copy let the manuscript claims be
checked. It also records identified direct sources whose full text was not
obtained. “No content gap” means the stated limitation does not block the
manuscript claims audited above; it does not change a KB package’s access
metadata.

1. Endre Boros and Peter L. Hammer (1993), “Cut-Polytopes, Boolean Quadric
   Polytopes and Nonnegative Quadratic Pseudo-Boolean Functions,”
   *Mathematics of Operations Research* 18(1), 245–253,
   DOI [10.1287/moor.18.1.245](https://doi.org/10.1287/moor.18.1.245).
   Best lawful landing page: [INFORMS article page](https://pubsonline.informs.org/doi/10.1287/moor.18.1.245).
   The full publisher text was unavailable; only bibliographic/abstract-level
   information was obtained. The BQP/cut and nonnegative pseudo-Boolean
   context is supported by the inspected Letchford–Sørensen and Letchford
   sources instead.
2. Timotej Hrga and Janez Povh (2023), “Solving SDP Relaxations of Max-Cut
   Problem with Large Number of Hypermetric Inequalities by L-BFGS-B,”
   *Optimization Letters* 17(5), 1201–1213,
   DOI [10.1007/s11590-022-01944-z](https://doi.org/10.1007/s11590-022-01944-z).
   Best lawful landing page: [Springer article page](https://doi.org/10.1007/s11590-022-01944-z).
   No lawful full-text copy was located in the batch; metadata only. It is not
   used as evidence for an exact complexity result.
3. Caterina De Simone (1990), “The Cut Polytope and the Boolean Quadric
   Polytope,” *Discrete Mathematics* 79(1), 71–75,
   DOI [10.1016/0012-365X(90)90056-N](https://doi.org/10.1016/0012-365X(90)90056-N).
   Best lawful landing page: [Elsevier article page](https://doi.org/10.1016/0012-365X(90)90056-N).
   Full text was not obtained. The manuscript proves its needed covariance
   correspondence directly, so this source is not a technical premise.
4. Michel Deza and Monique Laurent (1997), “Hypermetric Inequalities,” in
   *Geometry of Cuts and Metrics*, pp. 445–465, DOI
   [10.1007/978-3-642-04295-9_28](https://doi.org/10.1007/978-3-642-04295-9_28).
   Best lawful landing page: [Springer chapter page](https://link.springer.com/chapter/10.1007/978-3-642-04295-9_28).
   The chapter’s full text was not retrieved. Liers cites this chapter for an
   NP-hardness assertion, so the chapter’s own wording and locator remain
   unverified; the manuscript does not treat the secondary assertion as a
   proof.
5. Michel Deza, Viacheslav P. Grishukhin, and Monique Laurent (1993),
   “Hypermetrics in Geometry of Numbers,” LIENS Report 93-4,
   [official report PDF](https://www.di.ens.fr/reports/1993/liens-93-4.A4.pdf).
   DOI not assigned. The KB candidate is `access: none`, because the round-1
   candidate omitted the already existing file path. The same publicly
   sourced report copy was inspected locally, so there is no remaining
   manuscript-evidence content gap; the batch’s package retrieval/ingest
   issue remains unresolved.
6. Adam N. Letchford (2022), “The Boolean Quadric Polytope,” in
   *The Quadratic Unconstrained Binary Optimization Problem: Theory,
   Algorithms, and Applications*, pp. 97–120, DOI
   [10.1007/978-3-031-04520-2_4](https://doi.org/10.1007/978-3-031-04520-2_4).
   Best lawful source: [Lancaster author manuscript](https://eprints.lancs.ac.uk/id/eprint/172098/1/qubo_chapter.pdf).
   The KB downloader failed with HTTP 000/SSL timeout, leaving that batch
   candidate `access: none`. The existing author manuscript in the project
   source directory was read directly, so the source content is available for
   this audit; a KB promotion is deferred to the reusable literature lead.
7. Monique Laurent and Svatopluk Poljak (1996), “Gap Inequalities for the Cut
   Polytope,” *European Journal of Combinatorics* 17(2–3), 233–254,
   DOI [10.1006/eujc.1996.0020](https://doi.org/10.1006/eujc.1996.0020).
   Best lawful landing page: [Elsevier article page](https://doi.org/10.1006/eujc.1996.0020).
   Full text was not independently retrieved. Its historical role as the
   origin of gap inequalities is cited by Galli–Kaparis–Letchford; the
   manuscript relies on that inspected source for the history, not for a
   separation-complexity theorem.
8. Ravi Kannan and Achim Bachem (1979), “Polynomial Algorithms for Computing
   the Smith and Hermite Normal Forms of an Integer Matrix,” *SIAM Journal on
   Computing* 8(4), 499–507, DOI
   [10.1137/0208040](https://doi.org/10.1137/0208040).
   Best lawful landing page: [SIAM article page](https://doi.org/10.1137/0208040).
   Full article text was not obtained. The algorithm section cites it for the
   polynomial HNF/integral-preimage step; direct theorem-level source checking
   remains outstanding.
9. Richard M. Karp (1972), “Reducibility Among Combinatorial Problems,” in
   *Complexity of Computer Computations*, pp. 85–103, DOI
   [10.1007/978-1-4684-2001-2_9](https://doi.org/10.1007/978-1-4684-2001-2_9).
   Best lawful landing page: [Springer chapter page](https://link.springer.com/chapter/10.1007/978-1-4684-2001-2_9).
   Full source text was not retrieved; it is included as the standard
   NP-completeness citation, not as evidence for the paper’s new reduction.
10. Michael R. Garey and David S. Johnson (1979), *Computers and
    Intractability: A Guide to the Theory of NP-Completeness*, W. H. Freeman,
    ISBN 978-0-7167-1045-5. Best lawful catalog landing page:
    [WorldCat ISBN search](https://search.worldcat.org/search?q=bn%3A9780716710455).
    Full source text was not obtained; it is a standard problem-complexity
    reference and is not used as evidence for the new reduction.
11. Christoph Buchheim and Emiliano Traversi (2015), “On the Separation of
    Split Inequalities for Non-Convex Quadratic Integer Programming,”
    *Discrete Optimization* 15, 1–14, DOI
    [10.1016/j.disopt.2014.08.002](https://doi.org/10.1016/j.disopt.2014.08.002).
    The published version was not obtained. The lawful 2013 author preprint
    was read at [Optimization Online](https://optimization-online.org/wp-content/uploads/2013/07/3953.pdf)
    and supports the open-complexity statement used here; the published
    version’s text was not independently checked.
12. Samuel Burer and Adam N. Letchford (2014), “Unbounded Convex Sets for
    Non-Convex Mixed-Integer Quadratic Programming,” *Mathematical
    Programming* 143(1–2), 231–256, DOI
    [10.1007/s10107-012-0609-9](https://doi.org/10.1007/s10107-012-0609-9).
    The published text was not obtained. The 2011 author preprint was read at
    [Optimization Online](https://optimization-online.org/wp-content/uploads/2011/09/3172.pdf)
    and is the evidence for the related open separation question; no claim
    depends on uninspected differences in the final publication.

Entries 1, 2, 3, 5, and 6 correspond to every round-1 candidate whose KB
result was `access: none`. Entries 5 and 6 had local full source copies
inspected, and are listed because the batch packages nevertheless remained
access-none. Entry 4 is an additional in-scope citation-chain source whose
full text was not retrieved.
The remaining items are in-scope direct or standard references encountered
while checking manuscript citations. Further source retrieval or promotion,
if needed, should be routed through the single reusable literature lead after
the current shared-KB release.
