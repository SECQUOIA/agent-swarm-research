# Final synthesis brief

This is preparation while stage 4 undergoes review, not authorization to
begin stage 5 before that review and every accepted repair are complete.

The final manuscript should be a coherent research article, with the exact
centrality factor, explicit finite-step separation, coupled-barrier
persistence, and same-data primal–dual completion comparison as its main
contributions. Formulation results are complete supporting consequences.
The paper must explain the significance of each, rather than present a
catalogue of repository notes. Preserve all theorem hypotheses and scope
distinctions while reducing repetitive audit-style statements.

## Front matter and synthesis

- Replace the temporary abstract, supply a substantive introduction,
  precise qualified contribution statements, theorem roadmap, literature
  comparison and conclusion. Existing geometric prior-work text can move
  into the introduction where that improves continuity.
- Repository `paper/main.tex` identifies the author as Sergey Gusev. Use
  that name; do not invent affiliation, contact, funding or disclosure.
- Distinguish same endpoint from same objective accuracy, primal from
  primal–dual metric, arclength from finite local-norm moves, and movement
  complexity from arithmetic or oracle complexity.
- Credit NT2002's full feasible small-gap-set comparison explicitly.
  NN2008 already studies primal shortcuts and target sets; its precise
  general upper bound appears in the foundations. Lorentz's prefix
  inequality, classical spectral calculus, canonical barriers, metric
  projections and product-ball barriers are antecedents, not new results.
- To the best of our knowledge is appropriate for precise original
  results after the targeted primary-literature review, not for an
  unqualified first treatment of central-path inefficiency. The inspected
  literature does not prove an exhaustive priority claim.
- Include the modern finite-sequence context in
  `audit/root-additional-literature.md`: Allamigeon–Dadush–Loho–Natura–Végh
  is now SICOMP 54(5) (2025), FOCS22-178--FOCS22-264,
  DOI 10.1137/23M1554588. Its affine-segment resource in wide neighborhoods
  differs from fixed-radius local-Hessian moves and unrestricted target
  distance. Also give proportionate context for Allamigeon–Gaubert–Vandame
  STOC2022 and Deza–Nematollahi–Terlaky2008. Verify primary sources again
  whenever making a comparison not already supported by the audit.
- Remove every temporary stage marker from submission-facing sources.
  Do not include workflow history, unproved future promises, or assertions
  that numerical diagnostics establish theorem validity in the paper.

## Reproducible figures and package

One or two scientifically useful vector figures would improve the paper.
For example, display a two-dimensional central arc and its straight
shortcut in flattened coordinates, and the three exact lengths of the
dyadic family. If using the latter, distinguish the finite-start endpoint
distance from the minimum distance to the whole accurate target set.

A stable exact evaluation, without rounding the original coordinate to
one, is

```
L = 0.5 * np.logaddexp(0, 2*s)
v = np.sqrt(-np.expm1(-L))
H = L + 2*np.log1p(v) - np.sqrt(2)*np.arctanh(v/np.sqrt(2))
```

Here H(s)=rho(q(exp(s))). On the existing dyadic family with T=a_r,
finite initial parameter eta=1, the exact endpoint distance is
`norm(H(T-a)-H(-a))`, primal central length is the integral from 0 to T
of `norm(v(s-a))`, and full central length is `sqrt(2*r)*T`. Break
quadrature at activation thresholds and store the data and script.
These figures illustrate proved results; they do not certify them.

Use existing qipm NumPy/SciPy/Matplotlib only, no installs. Add a README
with standalone build commands, artifact map and the distinction between
the exact Fraction certificate and numerical diagnostics. The PDF, TeX,
bibliography and figures must build independently of the rest of the
repository. Do not copy literature originals. Preserve optional audits
separately from submission sources.

After stage 5 author handoff, the five independent reviewers must review
the **entire manuscript**, including every proof, global structure,
originality scope, citations, figures, scripts and reproducibility. This
is both stage 5 review and the user's final full-manuscript review. A
different agent repairs every accepted issue; any major issue triggers
another full five-reviewer round.
