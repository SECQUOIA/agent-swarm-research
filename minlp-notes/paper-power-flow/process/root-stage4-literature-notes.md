# Primary metadata and integration cautions

Verified via primary/publisher/university pages during stage2 review:
- Gan--Low 2014, IEEE TPS29(6),2892--2904, DOI10.1109/TPWRS.2014.2313514; primary record https://authors.library.caltech.edu/records/zf7qf-8jb24 .
- Jeeninga--De Persis--van der Schaft PartI, IEEE TAC68(1),2--17,2023, DOI10.1109/TAC.2022.3157076; primary https://research.rug.nl/en/publications/dc-power-grids-with-constant-power-loadspart-i-a-full-characteriz/ . Arxiv2010.01076 abstract explicitly says necessary/sufficient LMI for feasibility UNDER SMALL PERTURBATION; inspect full theorem not old novelty-note gloss.
- Bienstock--Verma2019, ORL47(6),494--501, DOI10.1016/j.orl.2019.08.009, primary https://www.sciencedirect.com/science/article/pii/S0167637719302470 . Journal organization differs from archived arxivv2: modelSection2, proofSection3, approximationSection4. Do NOT attribute arxivv2 Section1.3 NP question to journal Section1.3; cite version-specific preprint when necessary.

Old novelty note has broad absence claims, an exact-Turing-P inference from LMI, and a global torus uniqueness reading that should NOT be copied. Credit concrete prior theorems/models and prove our own scoped statements. Literature claims must be checked against originals. Sourcecache PDFs are available under build/source-cache. Source coverage audit confirms relevant result/review/code copies in the other worktree are identical (worktree-coverage-audit.json).

Legacy evidence: root reran code/power_flow_existential_reals/check_winding_count_exact.py,
PASS360 scaled pairs,4136 cycles,256 nonzero windings; actual output in
verification/root/legacy-winding.log. It is valid only for acute/right arcs,
whereas the paper checker extends to all short arcs. Original solver script
has eight source cases including inverse-square-root and golden-ratio values,
and two infeasible systems; numerical/time-limit results are recorded in
results/ac-power-flow-existential-reals.md Section5. Do not describe old solver
upper bounds as formal exact certificates or imply they were rerun here.
The eight toy source outcomes may be derived analytically in a concise table
if useful for comprehensive verification coverage; no need repeat a licensed
solver run or add dependencies. Paper-local exact graph checks supersede its
construction checks, and proofs establish irrational cases universally.

Additional verified metadata: Lehmann--Grastien--Van Hentenryck2016,
IEEE TPS31(1),798--801, DOI10.1109/TPWRS.2015.2407363;
primary https://researchportalplus.anu.edu.au/en/publications/ac-feasibility-on-tree-networks-is-np-hard/ .
Jeronimo--Perrucci--Tsigaridas2013, SIAM J Optim23(1),241--255,
DOI10.1137/110857751; journal theorem1.1 p242 verified via web PDF,
arxiv Theorem1 in cachedlocalsource. Root direct PDFdownload of journalfailed404;
do not claim localjournalPDFexists. Primary webcache open supported the stated theorem.

Root subsequently read Jeeninga PartI cached Theorem3.22 in full: it actually
covers BOTH exact and interior feasibility. Exact feasible demand iff there
is NO positive nu for which displayed matrix(46) is positive definite;
interior feasibility iff there is NO positive nu for which it is positive
semidefinite. Therefore do not suggest that the paper only characterizes
perturbed/interior feasibility. Say it characterizes the fixed-source
constant-power-demand model (including a distinction for its interior), with
convex feasible demand set and LMI alternatives. The missing justified step
in the old novelty note is exact polynomial-time Turing decidability, not
existence of an exact characterization. Our bounded voltages and injections
at all bus types are materially different constraints.

Stage 3 review later found a substantive error in a cited arithmetic source:
Dynamic Toolbox Lemma A's general Boolean conversion does not preserve a
rational bijection. The stage 3 corrector is replacing this dependency with
an explicit conjunction-only construction, sharp rational universality for
compact basic closed sets, and separate topological universality for arbitrary
compact semialgebraic sets. Integration must use the corrected statements,
not the earlier broad rational-universality slogan. The original bounded
ETR-INV hardness and the explicit ETR-INV-to-network bijection are unaffected.
See stage03-round01 root assessment and corrected stage 3 acceptance record.

Packaging: generated reviewer build directories and rendered diagnostic images
should be ignored by Git while retaining review reports, exact checker code,
manifests, and useful text logs. The final README should give all commands and
state actual verification scope, with no staged-draft placeholders. Author
identity is not supplied; an anonymous manuscript is appropriate without
inventing names. Prefer a concise abstract led by the combined structural
hardness and the distinction between exact and approximate feasibility.

Root independently checked the eight legacy source examples analytically:
1. x*x=1: x=1.
2. x+x=y, x*y=1: x=1/sqrt(2), y=sqrt(2).
3. x+y=z, x*y=1, z*z=1: infeasible, since z=1 but x+y>=2.
4. x+x=y, y+y=z, z*z=1: infeasible, since x=1/4 violates x>=1/2.
5. x+x=y, y*y=1: x=1/2, y=1.
6. x+x=y, y+y=z: unique x=1/2, y=1, z=2 from x>=1/2 and z<=2.
7. x+y=z, x*z=1, y*y=1: y=1, x=(sqrt(5)-1)/2, z=(sqrt(5)+1)/2.
8. u+u=w, w*w=1, u*y_i=1 for i=1,2,3: u=1/2, w=1, all y_i=2.
All six feasible examples are unique in the source box. A concise exact table
can account for the legacy numerical examples without new solver experiments.
