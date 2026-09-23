"""Illustrative transport limits, not a fit to the Fang catalyst experiments.

Run from any directory. Output contains explicit assumed ranges and units.
Only the reported feed, temperature, and conversion anchor the source scale.
"""

import json
import math
from pathlib import Path


def main():
    # Fang 2026: 2400 mL/(g catalyst h), H2/CO/Ar = 64/32/4,
    # about 44.1% CO conversion, 220 C. One water per converted CO is
    # an illustrative hydrocarbon-dominated oxygen balance, not raw water data.
    temperature_k = 493.15
    gas_constant = 8.314462618
    flow_ml_g_h = 2400.0
    co_fraction = 0.32
    co_conversion = 0.441
    molar_volumes_ml_mol = [22414.0, 24465.0]  # 0 C and 25 C at ~1 atm.
    # Mesh 40-60 approximated as 250-425 micrometre diameter spheres.
    radii_m = [125e-6, 212.5e-6]
    # Analyst assumptions; not measured pellet densities or water pressures.
    densities_g_m3 = [0.5e6, 1.5e6]
    boundary_water_pa = [1e5, 4e5]
    # Numerical value used in the paper's model, from earlier molecular MD.
    # It is NOT an experimentally measured gas-pore effective diffusivity.
    illustrative_diffusivity_m2_s = 2.2e-7
    rows = []
    for molar_volume in molar_volumes_ml_mol:
        q_mass = flow_ml_g_h * co_fraction * co_conversion / molar_volume / 3600
        for radius in radii_m:
            for density in densities_g_m3:
                q_volume = q_mass * density
                # Uniform positive source in a sphere, fixed surface c_b.
                # c(r)-c_b = q_v*(R^2-r^2)/(6*D).
                delta_c = q_volume * radius**2 / (6 * illustrative_diffusivity_m2_s)
                delta_p = delta_c * gas_constant * temperature_k
                thresholds = {}
                for p_boundary in boundary_water_pa:
                    c_boundary = p_boundary / (gas_constant * temperature_k)
                    # Effective D required to support a 10% centre excess.
                    thresholds[str(p_boundary)] = q_volume * radius**2 / (6 * 0.1 * c_boundary)
                rows.append({
                    "molar_volume_ml_mol": molar_volume,
                    "radius_m": radius,
                    "density_g_m3": density,
                    "source_mol_g_s": q_mass,
                    "source_mol_m3_s": q_volume,
                    "centre_excess_pa": delta_p,
                    "D_for_10percent_excess_m2_s_by_boundary_pa": thresholds,
                })

    # Same normalized fast washout can arise from lower B or greater G.
    storage_cases = []
    for name, capacity, conductance in [("reference", 1.0, 1.0),
                                       ("lower_storage", 0.5, 1.0),
                                       ("higher_conductance", 1.0, 2.0)]:
        tau = capacity / conductance
        source = 1.0
        steady_excess = source / conductance
        # Unit source begins at time 0 from c=0. Integrated c over [0, 1].
        ingress_exposure = steady_excess * (1 - tau * (1 - math.exp(-1 / tau)))
        storage_cases.append({"name": name, "B": capacity, "G": conductance,
                              "tau": tau, "steady_excess": steady_excess,
                              "unit_time_ingress_exposure": ingress_exposure})

    assert storage_cases[1]["tau"] == storage_cases[2]["tau"]
    assert storage_cases[1]["steady_excess"] == storage_cases[0]["steady_excess"]
    assert storage_cases[1]["unit_time_ingress_exposure"] > storage_cases[0]["unit_time_ingress_exposure"]
    # Doubling radius and D checks the analytic square/inverse scaling.
    def centre_excess(q, radius, diffusion):
        return q * radius**2 / (6 * diffusion)
    assert math.isclose(centre_excess(1, 2, 1), 4 * centre_excess(1, 1, 1))
    assert math.isclose(centre_excess(1, 1, 2), 0.5 * centre_excess(1, 1, 1))

    result = {
        "status": "illustrative assumptions; no fitted or measured transport coefficients",
        "temperature_k": temperature_k,
        "illustrative_diffusivity_m2_s": illustrative_diffusivity_m2_s,
        "centre_excess_pa_range": [min(x["centre_excess_pa"] for x in rows),
                                    max(x["centre_excess_pa"] for x in rows)],
        "sphere_cases": rows,
        "dimensionless_storage_cases": storage_cases,
    }
    destination = Path(__file__).with_name("water_transport_limits_output.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(destination),
                      "centre_excess_pa_range": result["centre_excess_pa_range"],
                      "storage_cases": storage_cases}, indent=2))


if __name__ == "__main__":
    main()
