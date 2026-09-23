#!/usr/bin/env python3
"""Reproduce the bounded styrene-cleaning thermodynamic screen offline.

Python 3 standard library only. Input values and evaluation choices are in the
adjacent JSON. Results are screening calculations, not certified confidence bounds.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def integrate_cp(table, start, end):
    """Integrate piecewise-linear Cp and Cp/T; return J/mol and J/(mol K)."""
    if not table[0][0] <= start <= end <= table[-1][0]:
        raise ValueError("Temperature outside Cp table; extrapolation prohibited")
    if any(b[0] <= a[0] for a, b in zip(table, table[1:])):
        raise ValueError("Cp temperatures must increase")
    dh = ds = 0.0
    for (ta, ca), (tb, cb) in zip(table, table[1:]):
        left, right = max(start, ta), min(end, tb)
        if right <= left:
            continue
        slope = (cb - ca) / (tb - ta)
        intercept = ca - slope * ta
        dh += intercept * (right - left) + slope * (right**2 - left**2) / 2
        ds += intercept * math.log(right / left) + slope * (right - left)
    return dh, ds


def reference_entropy(species, constants):
    """Convert toluene's raw older datum; otherwise use stated screening S298."""
    if "entropy_measurement" not in species:
        return species["S298"]
    raw = species["entropy_measurement"]
    return (
        raw["value_cal_mol_K"] * constants["cal_to_J"]
        + constants["R"] * math.log(raw["pressure_kPa"] / constants["standard_pressure_kPa"])
        + raw["Cp_for_temperature_correction_J_mol_K"]
        * math.log(constants["reference_temperature"] / raw["temperature_K"])
    )


def gas_properties(species, temperature, constants):
    """H uses formation enthalpy at 298 plus sensible heat; S is absolute.

    g_for_reaction_sums is Hf298 + sensible heat - T*S, NOT a species' Gibbs
    energy of formation at T. Element reference terms cancel in balanced routes.
    """
    s0 = reference_entropy(species, constants)
    if "Cp_table" in species:
        dh, ds = integrate_cp(species["Cp_table"], constants["reference_temperature"], temperature)
        h = species["Hf298"] + dh / 1000
        s = s0 + ds
    elif "Shomate" in species:
        c = species["Shomate"]
        if not c["range_K"][0] <= temperature <= c["range_K"][1]:
            raise ValueError("Temperature outside Shomate range")
        t = temperature / 1000
        dh = (c["A"]*t + c["B"]*t**2/2 + c["C"]*t**3/3
              + c["D"]*t**4/4 - c["E"]/t + c["F"] - c["H"])
        h = species["Hf298"] + dh
        s = (c["A"]*math.log(t) + c["B"]*t + c["C"]*t**2/2
             + c["D"]*t**3/3 - c["E"]/(2*t**2) + c["G"])
    else:
        return {"S298_J_mol_K": s0, "missing": "Cp(T); no temperature-dependent Gibbs energy calculated"}
    g = h - temperature * s / 1000
    reference_part = species["Hf298"] - temperature*s0/1000
    return {
        "S298_J_mol_K": s0,
        "Hf298_plus_sensible_kJ_mol": h,
        "S_absolute_J_mol_K": s,
        "g_for_reaction_sums_kJ_mol": g,
        "Cp_correction_kJ_mol": g - reference_part,
    }


def check_atom_balance(route, species):
    atoms = {}
    for name, nu in route.items():
        for element, count in species[name]["formula"].items():
            atoms[element] = atoms.get(element, 0) + nu * count
    if any(atoms.values()):
        raise ValueError(f"Unbalanced reaction: {atoms}")


def calculate(data):
    constants, conditions, species = data["constants"], data["conditions"], data["species"]
    t0, t = constants["reference_temperature"], conditions["temperature"]
    rt = constants["R"] * t / 1000
    pstd, total = constants["standard_pressure_kPa"], conditions["total_pressure_kPa"]
    eb = conditions["ethylbenzene_pressure_kPa"] / total
    water = conditions["water_ppm"] * 1e-6
    states = {name: gas_properties(sp, t, constants) for name, sp in species.items()}
    for route in data["routes"].values():
        check_atom_balance(route, species)
    answer = {
        "description": "Calculated screening outputs; decimal digits expose reproducibility, not justified experimental precision.",
        "assumptions": data["evaluation_choices"],
        "RT_kJ_mol": rt,
        "species_at_target_temperature": states,
        "closed_gas_routes": {},
    }
    for route_id, aromatic, alcohol in [
        ("benzene_ethanol", "benzene", "ethanol"),
        ("toluene_methanol", "toluene", "methanol"),
    ]:
        route = data["routes"][route_id]
        dg = sum(nu * states[name]["g_for_reaction_sums_kJ_mol"] for name, nu in route.items())
        k = math.exp(-dg / rt)
        # Δn=0: total pressure and standard pressure cancel from this quotient.
        a = k * eb
        closed_feed = []
        for ppm in conditions["water_cases_ppm"]:
            inlet_water = ppm * 1e-6
            # Stable positive root of x² + a*x - a*inlet_water = 0.
            x = 2*a*inlet_water / (math.sqrt(a*a + 4*a*inlet_water) + a)
            closed_feed.append({"inlet_water_ppm": ppm, "equal_products_ppm": x*1e6,
                                "remaining_water_ppm": (inlet_water-x)*1e6})
        feed = data["comparator_feed"]["mass_percent"]
        ratio = ((feed[aromatic]/species[aromatic]["molecular_weight"])
                 / (feed["ethylbenzene"]/species["ethylbenzene"]["molecular_weight"]))
        comparator_alcohol = k * water / ratio * 1e6
        sensitivity_factor = math.exp(conditions["delta_G_sensitivity_kJ_mol"]/rt)
        answer["closed_gas_routes"][route_id] = {
            "delta_G_standard_kJ_mol": dg,
            "K_dimensionless": k,
            "Hf_uncertainty_RSS_diagnostic_kJ_mol": math.sqrt(sum(
                (nu * species[name].get("Hf298_reported_uncertainty", 0))**2
                for name, nu in route.items())),
            "equal_products_at_fixed_local_water_ppm": math.sqrt(k*eb*water)*1e6,
            "product_free_feed_equilibrium": closed_feed,
            "fixed_local_aromatic_cases": [
                {"aromatic_ppm": ppm, "alcohol_boundary_ppm": k*eb*water/(ppm*1e-6)*1e6}
                for ppm in conditions["aromatic_cases_ppm"]],
            "comparator_aromatic_per_EB_molar_ratio": ratio,
            "comparator_aromatic_gas_ppm": ratio*eb*1e6,
            "comparator_alcohol_boundary_ppm": comparator_alcohol,
            "comparator_alcohol_sensitivity_interval_ppm": [
                comparator_alcohol/sensitivity_factor, comparator_alcohol*sensitivity_factor],
            "sensitivity_note": "Delta-G sensitivity only; not a statistical confidence interval.",
        }
    route = data["routes"]["acetophenone_hydrogen"]
    dh0 = sum(nu*species[name]["Hf298"] for name, nu in route.items())
    ds0 = sum(nu*states[name]["S298_J_mol_K"] for name, nu in route.items())
    base = dh0-t*ds0/1000
    known_correction = sum(nu*states[name]["Cp_correction_kJ_mol"]
                           for name, nu in route.items() if name != "acetophenone")
    weight = t*math.log(t/t0)-(t-t0)
    ap_cases = []
    for ppm in conditions["acetophenone_cases_ppm"]:
        ap_activity = ppm*1e-6*total/pstd
        q = (ap_activity*(conditions["hydrogen_pressure_kPa"]/pstd)**2
             / ((conditions["ethylbenzene_pressure_kPa"]/pstd)*(water*total/pstd)))
        mixing = rt*math.log(q)
        required_c = -base-mixing
        required_cp = (known_correction-required_c)*1000/weight
        ap_cases.append({"acetophenone_ppm": ppm, "Q": q, "RT_ln_Q_kJ_mol": mixing,
                         "total_Cp_correction_must_be_below_kJ_mol": required_c,
                         "AP_weighted_Cp_must_exceed_J_mol_K": required_cp})
    answer["acetophenone_conditional"] = {
        "delta_H298_kJ_mol": dh0, "delta_S298_J_mol_K": ds0,
        "reference_state_part_of_delta_G773_kJ_mol": base,
        "known_Cp_correction_excluding_AP_kJ_mol": known_correction,
        "weight_integral_K": weight,
        "EB_weighted_Cp_J_mol_K": -states["ethylbenzene"]["Cp_correction_kJ_mol"]*1000/weight,
        "cases": ap_cases,
        "hydrogen_perturbation_delta_G_kJ_mol": 2*rt*math.log(
            conditions["alternative_hydrogen_pressure_kPa"]/conditions["hydrogen_pressure_kPa"]),
        "hydrogen_perturbation_equilibrium_AP_multiplier": (
            conditions["hydrogen_pressure_kPa"]/conditions["alternative_hydrogen_pressure_kPa"])**2,
    }
    answer["scope_limits"] = [
        "Alcohol boundaries concern terminal alcohol products, not total cleaning flux if alcohols react further.",
        "Local water and product activities are required; an inlet value need not represent the bed.",
        "Finite prelabel transients change solid-state inventories; closed gas-cycle equilibria alone do not apply.",
        "The product-free-feed solutions hold ethylbenzene constant because its depletion by ppm oxygen transfer is negligible; other reactions are excluded.",
    ]
    return answer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=Path(__file__).with_name("styrene_thermochemistry_inputs.json"))
    parser.add_argument("--output", type=Path, help="Write JSON here; default is stdout")
    args = parser.parse_args()
    raw = args.inputs.read_bytes()
    answer = calculate(json.loads(raw))
    answer["input_sha256"] = hashlib.sha256(raw).hexdigest()
    text = json.dumps(answer, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
