# What an interrupted-aging experiment can identify

2026-09-15. This is a mathematical design check, not a fitted model or prediction of zeolite performance. All numerical parameters and time units below are arbitrary. The equations illustrate competing explanations that experiments must distinguish.

## Main result

Slow irreversible aggregation does **not** by itself make interruption beneficial. If the vulnerable population re-establishes rapidly whenever steam returns, each wet period incurs almost the same damage per unit wet time. A useful schedule needs a resolvable relaxation process, a recovery path, and sufficiently little damage during recovery. Measuring a slow overall loss rate is insufficient.

This is a material concern because Class-Martínez et al. interpret their H-CHA data using quasi-equilibrated hydrolysis followed by slower Al association. Their source does not measure a useful recovery-window duration. Their repeated assay also includes an NH3/water treatment that can restore some sites. [[martinez2026-consequences-of-non-mean-field]] p.4-5, p.7-9; [DOI](https://doi.org/10.1016/j.jcat.2026.116848). The original PDF's pp.4–5 were independently checked against the extracted text for these protocol statements.

## Equal exposure is necessary, but insufficient

For a separable irreversible model

`dF/dt = -k(u(t))*g(F)`,

where `u` contains measured temperature and water activity, integration gives `integral dF/g(F) = -integral k(u)dt`. Schedules with the same time distribution of **joint** conditions give the same endpoint. This includes nonlinear loss in F. Independent heterogeneous populations with separate separable laws also have this property. Equal mean water pressure alone does not give equal integrated k when water dependence is nonlinear.

However, a general scalar, memory-free law can be order dependent. Consider initially `F=1`, one time unit wet with `dF/dt=-F²`, and one dry with `dF/dt=-F`. Wet then dry gives `F=e^-1/2`; dry then wet gives `F=e^-1/(1+e^-1)`. The endpoints differ despite equal wet/dry durations and no hidden intermediate. The wet and dry loss laws act differently on the same F population.

Therefore, calibrate dry-only loss, use measured waveforms, and compare fitted scalar and heterogeneous null models before attributing a schedule effect to recovery. An order effect rejects particular nulls, not all irreversible models. Even evidence of hidden state does not uniquely identify Al agglomeration: hydration, pore accessibility, counterions, and unobserved site classes can carry history.

## Minimal recoverable-state illustration

Let F denote framework-connected Al equivalents, R a recoverable population, and D irrecoverable Al equivalents on the experimental timescale. Use:

```text
dF/dt = -kh F + kr R
dR/dt =  kh F - kr R - kd R²
dD/dt =                    kd R²
F + R + D = 1
```

The coefficient kd incorporates the Al-equivalent stoichiometry of the effective association sink. These are coarse states; the equations do not establish their molecular identity. An alternative R–F association sink is also compatible with the source's unresolved mechanism and must not be excluded by this illustration.

[aging_schedule.py](aging_schedule.py) compares schedules with ten wet and ten dry arbitrary time units, segmented into 1–100 wet/dry pairs. Each ends dry. An ideal common terminal assay is assumed to restore all R to F without causing additional loss, so the reported surviving inventory is F+R. Real assay kinetics and damage must be measured rather than assumed to follow this idealization.

The parameter sets deliberately distinguish finite hydrolysis relaxation, very fast equilibration, no dry-state evolution, and damage during the dry interval. The dry-inert case retains recovery during wet exposure; all three dry rates are zero. None is fitted to literature. [CSV](aging_schedule.csv), [parameters and numerical checks](aging_schedule_summary.json), and [plot](aging_schedule.png) preserve the complete calculation.

Under the finite-relaxation example, segmentation preserves substantially more F+R. Under the fast-equilibration example, the difference nearly vanishes. With no dry-state evolution, segmentation gives the same endpoint to numerical precision. Allowing dry damage changes the tradeoff; its rate must be measured. These examples establish logical possibilities, not a distribution of likely outcomes.

In the fast-equilibration example, F before the ideal assay differs strongly between pulse counts even though F+R does not. The final dry bout has different duration in each schedule. Thus an apparent functional difference can reflect the sampling phase and elapsed recovery time without preventing permanent loss. Experiments must specify the final phase, delay, and common conditioning when comparing these outputs.

## Experimental consequences

1. Measure the actual steam step response and sample temperature before choosing pulse widths. Resolve a candidate relaxation relative to switching, pore equilibration, and the assay's own time response.
2. Begin with sacrificial samples to prevent intervening measurements from becoming unrecorded regeneration treatments. Compare a repeatedly assayed trajectory against specimens with no intermediate assay at matched initial state and damaging exposure, with explicit sham controls for the added thermal/water/handling history.
3. Separate **functional state before treatment**, **recovery caused by an explicit treatment**, and **inventory after a standardized recovery assay**. Endpoint agreement after a strong assay may erase a real transient difference; endpoint disagreement alone may reflect unequal conditioning.
4. Use dry-only and handling controls to constrain nonseparable nulls. Compare restart hazards after different histories at matched measured retained inventory; add structural/functional observations to reduce remaining hidden-state ambiguity.
5. Fit several schedules and predict a withheld one. Do not select a model only because it fits the same endpoint curve used to tune it.
6. If the accessible pulses are all much longer than hydrolysis relaxation, stop the timing-based improvement claim. A measured upper bound on relaxation can still support a useful cumulative-damage model.

## Numerical verification

The script checks conservation and nonnegative states after each segment, verifies successful integration, and repeats pulse-count extremes at tighter integration tolerances. The dry-inert limit and analytic direct-loss examples provide independent checks. The tolerance comparison is numerical accuracy only; it says nothing about physical model validity.
