"""Length or field needed for a target Faraday rotation, in the linear regime.

    python scripts/rotator_design.py --verdet 40 --rotation 45 --field-mT 10 100 1000

The Verdet constant (rad T^-1 m^-1) must be taken from a source for the chosen
material and wavelength. Prints the required length for each field value.
"""
import argparse

import _common  # noqa: F401
from faraday.magneto_optics import required_length_m


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--verdet", type=float, required=True, help="Verdet constant, rad/(T m)")
    p.add_argument("--rotation", type=float, default=45.0, help="target rotation (deg)")
    p.add_argument("--field-mT", type=float, nargs="+", required=True)
    a = p.parse_args()
    for b in a.field_mT:
        d = required_length_m(a.verdet, b * 1e-3, a.rotation)
        print(f"B = {b:8.1f} mT  ->  d = {d * 100:10.3f} cm")


if __name__ == "__main__":
    main()
