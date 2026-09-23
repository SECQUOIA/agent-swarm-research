# Root's stage 2 investigation

This record accompanies the stage author and precedes the 15-reviewer rounds.

## Source transformation requiring a narrow application

Read the local original of Abrahamsen and Miltzow, *Dynamic Toolbox for ETRINV*, including the image of PDF p.6, not just its incomplete text extraction. Lemma A's Step (2) replaces an atomic `q>0` by `qz-1=0` and appends `z>=0` at the end of the whole formula. Its later rational-bijection argument assigns `z=1/q`.

For the compact singleton formula

`(x=0) AND ((x=0) OR (x>0))`,

this rule produces

`(x=0) AND ((x=0) OR (xz-1=0)) AND z>=0`.

Every pair `(0,z)` with `z>=0` satisfies it. Subsequent replacement of the disjunction by the product equation `x(xz-1)=0` does not remove the free auxiliary. Hence this particular transformation does not preserve the claimed rational bijection when a strict predicate lies in an inactive disjunct. This is a defect in the displayed general proof route, not a refutation of the existence statement of Theorem 1 by every possible construction.

The pooling algebraic-degree argument starts instead with the basic closed conjunction `p(x)=0`, `c<=x<=d`, isolating one irrational algebraic root. It has neither strict inequalities nor disjunctions. The problematic step is unnecessary; weak-inequality slack variables are uniquely determined. The stage author was asked to verify and state only the compact basic-closed route required for this argument, including the remaining ETR-INV transformations and the coordinatewise affine recovery.

The arXiv record checked during this work lists only v1 (18 December 2019): https://arxiv.org/abs/1912.08674. No claim is made about every unpublished correction or later treatment.

## Encoding and implementation observations

The one-pool reduction has linearly many nodes, arcs and attributes, but its full dense source-quality and terminal-specification tables can have quadratically many entries. The manuscript must claim polynomial full encoding, unless a sparse-default representation is expressly defined.

The historical one-pool verification builder generates auxiliary variable names such as `u0` without checking whether an original variable already has that name. The mathematical reduction calls for fresh variables and is unaffected. New independent verification should use collision-safe identifiers; historical finite check results do not establish correctness of this naming implementation for every string-labelled input.

The exact irrational example is proved in `root-foundations-check.md`; its missing normalization denominator was identified before drafting, and the full global argument was supplied to the stage author.

## Independent exact checks

`verification/check_one_pool_etr_exact.py` passes 104 independently constructed physical one-pool witnesses, comprising 980 normalized equations and 1775 pinned terminals. All physical conservation, source caps, pool/terminal caps, dense quality rows, and forcing-objective counts are checked with exact rational arithmetic. Cases include repeated summands, boundary values, unused variables, and original labels that collide with the historical auxiliary naming convention. Tuple identifiers prevent those collisions. These finite forward checks supplement, and do not replace, both directions of the proof.

The existing bounded-data exact checker was also rerun successfully: seven exact rational systems and 300 randomized structural cases. Its log is `verification/logs/bounded-etr-exact.txt`. The checker is supplemental evidence about the gadget implementation, not a proof for all instances.

## Root draft and build check

Read the entire initial algebraic-complexity draft, including both directions of each physical construction, chain allocation and slack bounds, fixed-data refinements, one-pool dense attribute semantics, the singleton transfer, the global irrational example, and all certificate parameterizations. No additional defect was identified in that draft. The source transfer was narrowed to the basic closed case, and the author reports checking the original PDF equations in Lemmas C–G; this dependency remains an explicit focus for independent review.

A forced `latexmk -g -pdf -interaction=nonstopmode -halt-on-error main.tex` rebuild produced 22 pages with no final warnings, undefined references, or overfull/underfull boxes. Forcing was necessary because the earlier build did not track the then-missing conditional stage-2 input. Root visually inspected PDF page 11, covering the section transition and saturation lemma; it rendered cleanly. This preliminary build is not the final whole-paper inspection.

Root additionally viewed the original Toolbox PDF p.18, checked Figure 3's directed arithmetic, and independently simplified its final expression to `(x+1)^2`. The author supplied `verification/check_etr_source_identities.py`; root read and reran it successfully. It checks both Figures 2 and 3 identities and uses exact polynomial coefficient enclosures on the entire rational box of radius `10^-6` to verify all auxiliary values remain in `[1/2,2]` with positive denominators. This is a symbolic identity and interval proof check, not a finite sampling check. The manuscript can choose a sufficiently small scale; it does not need the source's particular loose constants for its existential singleton claim.

## Reviewer artifact retention

Reviewer 02 independently built all three physical constructions using exact fractions, including a capacity-seven family with 3993 nodes and 4102 arcs. The finite checks passed under that review. Root retained the reviewer's temporary script, unchanged except for a provenance/scope docstring, as `verification/check_reviewer02_physical.py` so the evidence in `stage-02-round-01/review02.md` remains reproducible. It is a supplemental forward-witness check, not a general converter or a proof of the reverse implications.
