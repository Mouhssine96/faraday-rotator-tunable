"""Sizing of a multilayer solenoid used to bias a fibre Faraday rotator.

The field on the axis, at the centre of a single layer of N turns of
radius R spread over a length l, is

    B = mu0 * N * I / sqrt(l**2 + 4 * R**2)

A multilayer coil is treated as a stack of such layers whose radius grows
by one wire diameter per layer; the fields of the layers are added.

The command-line tool is ``scripts/coil_design.py``.
"""
from __future__ import annotations

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
