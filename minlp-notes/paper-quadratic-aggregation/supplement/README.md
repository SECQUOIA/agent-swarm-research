# Reproducible exact checks

The following scripts require Python 3 and only its standard library.
From the paper directory run:

```sh
python3 supplement/check_examples.py
python3 supplement/check_infinite_aggregation.py
python3 supplement/check_approximation.py
python3 supplement/check_four_aggregation.py
python3 supplement/check_three_dimensional_span.py
```

The first checks the coefficient identities, rational semidefinite lifts,
conflict-repair margins, and boundary examples in the consequences,
hypotheses/examples sections, and application appendix. The second checks
the infinite-aggregation example:
2,601 rational ray identities, six finite-family outside witnesses, and
additional exact slack and prior-example calculations.
The third checks 64 integer multiplier meshes, 606 exact Gram witnesses,
the finite-grid separation constants, and the radial repair identity in
the approximation section.
The fourth checks the PDLC polynomial identity, a strict feasible point,
the four indispensable-ray witnesses (including exact radical signs), and
the four-ray cone decomposition identity in the finite-bound section.
The fifth checks the Vandermonde, ellipsoid witness, and negative-cone
identities by exact symbolic coefficient arithmetic, plus 1,235 rational
witness evaluations and the strict signs of the two added rows in the
three-dimensional-span appendix.

These finite checks supplement the manuscript's proofs. They do not prove
HHC, statements quantified over arbitrary multiplier families, quartic
irreducibility, or novelty. Formal verification has its own separately
documented scope. None of these scripts needs repository notes or external data.

## Approximation figure

The PDF figure is already included, so building the paper does not require
Python or plotting packages. To regenerate it, use Python 3 with NumPy
and Matplotlib 3.7 or later:

```sh
python3 supplement/plot_aggregation_slice.py
```

This writes `figures/finite-aggregation-slice.pdf` and a PNG preview from
explicit radial formulas on the plane `u=x e1`, `v=y e2`. The exact boundary
solves `(1-x^2)(1-y^2)=1/4` within the coordinate bounds. For polar angle
`phi`, its squared radius is
`1.5/(1+sqrt(1-3*cos(phi)^2*sin(phi)^2))`. A mesh cut with angle `theta`
has squared radial bound
`(1-cos(theta)*sin(theta))/(cos(theta)^2*cos(phi)^2+sin(theta)^2*sin(phi)^2)`;
the minimum over the mesh gives the outer boundary. A zero denominator
imposes no radial restriction. The script checks the boundary equations,
outer containment, and nested meshes on 8,001 sampled directions. These
floating-point checks validate the plotting calculation, not the
full-dimensional Hausdorff bound or any universal theorem.
