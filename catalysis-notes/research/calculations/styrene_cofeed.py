#!/usr/bin/env python3
"""Offline screening equilibrium for the proposed styrene cofeed experiment."""
import hashlib
import json
import math
from pathlib import Path

from styrene_thermochemistry import check_atom_balance, gas_properties


def calculate():
    folder = Path(__file__).resolve().parent
    input_path = folder / "styrene_cofeed_inputs.json"
    inputs = json.loads(input_path.read_text())
    base_path = folder / inputs["base_inputs"]
    base = json.loads(base_path.read_text())
    constants = base["constants"]
    species = {name: base["species"][name] for name in ("ethylbenzene", "hydrogen")}
    species["styrene"] = inputs["styrene"]
    route = {"ethylbenzene": -1, "styrene": 1, "hydrogen": 1}
    check_atom_balance(route, species)
    rows = []
    for temperature in inputs["temperatures_K"]:
        properties = {name: gas_properties(data, temperature, constants)
                      for name, data in species.items()}
        dg = sum(route[name] * data["g_for_reaction_sums_kJ_mol"]
                 for name, data in properties.items())
        dh = sum(route[name] * data["Hf298_plus_sensible_kJ_mol"]
                 for name, data in properties.items())
        ds = sum(route[name] * data["S_absolute_J_mol_K"]
                 for name, data in properties.items())
        rt = constants["R"] * temperature / 1000
        equilibrium_constant = math.exp(-dg / rt)
        factor = math.exp(inputs["delta_G_sensitivity_kJ_mol"] / rt)
        rows.append({
            "temperature_K": temperature,
            "delta_H_kJ_mol": dh,
            "delta_S_J_mol_K": ds,
            "delta_G_kJ_mol": dg,
            "K_dimensionless": equilibrium_constant,
            "K_sensitivity_not_confidence_interval": [equilibrium_constant/factor, equilibrium_constant*factor],
            "S_over_E_at_target_eta": {
                str(pressure): inputs["target_eta"] * equilibrium_constant
                * constants["standard_pressure_kPa"] / pressure
                for pressure in inputs["hydrogen_pressures_kPa"]
            },
            "H2_kPa_at_target_eta_and_S_over_E_1": inputs["target_eta"]
            * equilibrium_constant * constants["standard_pressure_kPa"],
        })
    return {
        "inputs_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "base_inputs_sha256": hashlib.sha256(base_path.read_bytes()).hexdigest(),
        "target_eta": inputs["target_eta"],
        "standard_pressure_kPa": constants["standard_pressure_kPa"],
        "rows": rows,
        "limits": inputs["limits"],
    }


if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2))
