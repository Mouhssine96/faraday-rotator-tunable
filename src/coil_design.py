"""Sizing of a multilayer solenoid used to bias a fibre Faraday rotator.

The field on the axis, at the centre of a single layer of N turns of
radius R spread over a length l, is

    B = mu0 * N * I / sqrt(l**2 + 4 * R**2)

A multilayer coil is treated as a stack of such layers whose radius grows
by one wire diameter per layer; the fields of the layers are added.

Usage
-----
    python src/coil_design.py                     # default parameters
    python src/coil_design.py --current 4 --layers 10 --csv coil.csv

The script prints a summary, the field per ampere, and optionally writes a
per-layer table to CSV.
"""
from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from typing import List

MU0 = 4 * math.pi * 1e-7  # vacuum permeability, T·m/A


def layer_field(n_turns: int, current: float, length: float, radius: float) -> float:
    """Axial field (T) at the centre of one layer of a finite solenoid."""
    return MU0 * n_turns * current / math.sqrt(length**2 + 4 * radius**2)


def layer_wire_length(n_turns: int, radius: float) -> float:
    """Wire length (m) needed for one layer."""
    return n_turns * 2 * math.pi * radius


@dataclass
class Layer:
    index: int
    radius: float       # m
    turns: int
    field: float        # T
    wire_length: float  # m


def design(length: float, inner_radius: float, wire_diameter: float,
           turns_per_cm: float, n_layers: int, current: float) -> List[Layer]:
    """Return the list of layers of the coil, innermost first."""
    turns_per_layer = int(round(turns_per_cm * length * 100))
    layers = []
    for k in range(n_layers):
        radius = inner_radius + wire_diameter / 2 + k * wire_diameter
        layers.append(Layer(
            index=k + 1,
            radius=radius,
            turns=turns_per_layer,
            field=layer_field(turns_per_layer, current, length, radius),
            wire_length=layer_wire_length(turns_per_layer, radius),
        ))
    return layers


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--length-cm", type=float, default=3.5, help="axial length of the coil (cm)")
    p.add_argument("--inner-radius-cm", type=float, default=0.5, help="inner radius (cm)")
    p.add_argument("--wire-diameter-mm", type=float, default=1.25, help="wire diameter (mm)")
    p.add_argument("--turns-per-cm", type=float, default=8, help="turns per cm along the axis")
    p.add_argument("--layers", type=int, default=25, help="number of layers")
    p.add_argument("--current", type=float, default=8.0, help="current (A)")
    p.add_argument("--csv", help="optional path of a per-layer CSV table")
    a = p.parse_args()

    layers = design(a.length_cm / 100, a.inner_radius_cm / 100, a.wire_diameter_mm / 1000,
                    a.turns_per_cm, a.layers, a.current)
    b_total = sum(l.field for l in layers)
    wire_total = sum(l.wire_length for l in layers)
    turns_total = sum(l.turns for l in layers)

    print(f"Turns per layer      : {layers[0].turns}")
    print(f"Layers               : {len(layers)}")
    print(f"Total turns          : {turns_total}")
    print(f"Wire length          : {wire_total:.1f} m")
    print(f"Field at the centre  : {b_total * 1e3:.2f} mT at {a.current} A")
    print(f"Field per ampere     : {b_total / a.current * 1e3:.2f} mT/A")

    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["layer", "radius_cm", "turns", "field_T",
                        "cumulative_field_T", "wire_length_m", "cumulative_wire_length_m"])
            cum_b = cum_l = 0.0
            for l in layers:
                cum_b += l.field
                cum_l += l.wire_length
                w.writerow([l.index, f"{l.radius * 100:.4f}", l.turns, f"{l.field:.6e}",
                            f"{cum_b:.6e}", f"{l.wire_length:.4f}", f"{cum_l:.4f}"])
        print(f"Table written to {a.csv}")


if __name__ == "__main__":
    main()
