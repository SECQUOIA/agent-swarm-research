# Stage 4b adjudication

The lead read all five independent reports in full, the complete frozen section, the author report, and the validation outputs. Reviewers r1–r5 all found no major issue. The lead agrees. Their audits explicitly included the new independent directional-coefficient extension, original-parameter recovery, exact filters, and rational-profile theorem.

Three minor corrections are accepted; there are no rejected substantive criticisms:

1. Threshold dual degeneracy (r1, r3, r4, r5): a feasible dual may be constant with no actual breakpoint, even with nonzero flows. Use the listed edge weights as partition boundaries, or explicitly handle a globally constant dual. The candidate lemma and algorithm remain correct.
2. Zero-objective face output (r1, r5): an arbitrary rational feasible nomination need not lie on the promised small face. Fill the balanced box from its lower bounds in order, leaving at most one interior coordinate, and fix all other coordinates at endpoints. This supplies the theorem's stated output in the trivial objective case.
3. Vigneron source locator (r5): retain the journal metadata but add the author-manuscript URL and date. The lead independently checked the original PDF's first page: October 21, 2011. Theorem 6 and section locators refer to that version.

r2 found no required correction. Numerical checks support but do not replace the reviewed proofs. These minor repairs do not require a repeated five-reviewer round unless correction or lead verification reveals a major issue.

Status: accepted. A separate correction agent applied all three repairs. The lead inspected the actual proof and citation edits and read the complete fix report. All 14 build input hashes independently match; Paper A builds with zero errors, unresolved references/citations, duplicate labels, or overfull boxes. Final section SHA-256: `58989dcde36c0a3ce6bce0d5f509fba1f5c27dc1f6231582d8ce082d2bcd2980`. No major issue arose during correction.
