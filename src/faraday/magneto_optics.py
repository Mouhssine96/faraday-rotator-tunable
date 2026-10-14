"""Faraday rotation in the linear (unsaturated) regime: beta = V B d.

V is the Verdet constant (rad T^-1 m^-1), B the longitudinal field (T) and d
the interaction length (m). These relations are useful to size a rotator made
of a paramagnetic or diamagnetic material. For a ferrimagnetic garnet close to
saturation, as in commercial 45 degree rotators, the rotation is no longer
proportional to B and V should be read as a local sensitivity only.

No material values are built in: the Verdet constant depends strongly on the
material and the wavelength and must come from a cited source.
"""
from __future__ import annotations

import numpy as np


def rotation_deg(verdet, field_T, length_m):
    """Rotation angle in degrees."""
    return np.degrees(np.asarray(verdet) * np.asarray(field_T) * np.asarray(length_m))


def required_length_m(verdet, field_T, rotation_deg_target):
    """Interaction length giving the target rotation at a given field."""
    return np.radians(rotation_deg_target) / (np.asarray(verdet) * np.asarray(field_T))


def required_field_T(verdet, length_m, rotation_deg_target):
    """Field giving the target rotation over a given length."""
    return np.radians(rotation_deg_target) / (np.asarray(verdet) * np.asarray(length_m))
