"""Size a multilayer solenoid: turns, wire length and field at the centre.

    python scripts/coil_design.py --current 1
    python scripts/coil_design.py --layers 10 --csv coil.csv
"""
import argparse
import csv

import _common  # noqa: F401
from faraday.coil import design


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--length-cm", type=float, default=3.5, help="axial length of the coil (cm)")
    p.add_argument("--inner-radius-cm", type=float, default=0.5, help="inner radius (cm)")
    p.add_argument("--wire-diameter-mm", type=float, default=1.25, help="wire diameter (mm)")
    p.add_argument("--turns-per-cm", type=float, default=8, help="turns per cm along the axis")
    p.add_argument("--layers", type=int, default=25, help="number of layers")
    p.add_argument("--current", type=float, default=8.0, help="current (A)")
    p.add_argument("--csv", help="optional per-layer CSV table")
    a = p.parse_args()

    layers = design(a.length_cm / 100, a.inner_radius_cm / 100, a.wire_diameter_mm / 1000,
                    a.turns_per_cm, a.layers, a.current)
    b = sum(l.field for l in layers)
    print(f"Turns per layer      : {layers[0].turns}")
    print(f"Layers               : {len(layers)}")
    print(f"Total turns          : {sum(l.turns for l in layers)}")
    print(f"Wire length          : {sum(l.wire_length for l in layers):.1f} m")
    print(f"Field at the centre  : {b * 1e3:.2f} mT at {a.current} A")
    print(f"Field per ampere     : {b / a.current * 1e3:.2f} mT/A")
    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["layer", "radius_cm", "turns", "field_T", "cumulative_field_T",
                        "wire_length_m", "cumulative_wire_length_m"])
            cb = cl = 0.0
            for l in layers:
                cb += l.field
                cl += l.wire_length
                w.writerow([l.index, f"{l.radius * 100:.4f}", l.turns, f"{l.field:.6e}",
                            f"{cb:.6e}", f"{l.wire_length:.4f}", f"{cl:.4f}"])
        print("Table written to", a.csv)


if __name__ == "__main__":
    main()
