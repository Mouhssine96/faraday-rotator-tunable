"""Analyse the hybrid configuration: field calibration and rotation vs current/field.

    python scripts/analyse_hybrid.py --out figures

Fits rotation(I), rotation(B_total) and B_solenoid(I) with a straight line,
prints slopes with one-sigma uncertainties and saves the figures.
"""
import argparse
from pathlib import Path

import _common
from faraday.analysis import linear_fit, load_hybrid


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--data", default=str(_common.ROOT / "data" / "hybrid_configuration.csv"))
    p.add_argument("--out", default="figures")
    a = p.parse_args()

    d = load_hybrid(a.data)
    i, bsol, btot, rot = (d["current_A"], d["solenoid_field_mT"],
                          d["total_field_mT"], d["rotation_deg"])
    fits = {
        "B_solenoid(I) [mT/A]": linear_fit(i, bsol),
        "rotation(I) [deg/A]": linear_fit(i, rot),
        "rotation(B_total) [deg/mT]": linear_fit(btot, rot),
    }
    for name, f in fits.items():
        print(f"{name:28s} slope {f.slope:.3f} ± {f.slope_std:.3f}   R2 = {f.r2:.4f}   (n = {f.n})")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    f = fits["B_solenoid(I) [mT/A]"]
    ax[0].plot(i, bsol, "o", label="measured")
    ax[0].plot(i, f(i), "-", label=f"{f.slope:.3f} mT/A, R² = {f.r2:.4f}")
    ax[0].set(xlabel="current (A)", ylabel="solenoid field (mT)", title="Solenoid calibration")
    ax[0].legend()
    f = fits["rotation(B_total) [deg/mT]"]
    ax[1].plot(btot, rot, "o", label="measured")
    ax[1].plot(btot, f(btot), "-",
               label=f"{f.slope:.2f} ± {f.slope_std:.2f} °/mT, R² = {f.r2:.3f}")
    ax[1].set(xlabel="total field (mT)", ylabel="rotation change (°)",
              title="Hybrid configuration (35 mT bias)")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(out / "hybrid_configuration.png", dpi=160)
    print("figure:", out / "hybrid_configuration.png")


if __name__ == "__main__":
    main()
