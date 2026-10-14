import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from faraday.analysis import linear_fit, load_hybrid  # noqa: E402
from faraday.coil import MU0, design, layer_field  # noqa: E402
from faraday.magneto_optics import required_field_T, required_length_m, rotation_deg  # noqa: E402

DATA = Path(__file__).resolve().parents[1] / "data" / "hybrid_configuration.csv"


def test_long_solenoid_limit():
    length, radius, turns, current = 1.0, 1e-3, 1000, 2.0
    assert math.isclose(layer_field(turns, current, length, radius),
                        MU0 * turns / length * current, rel_tol=1e-5)


def test_field_is_linear_in_current():
    b1 = sum(l.field for l in design(0.035, 0.005, 1.25e-3, 8, 25, 1.0))
    b4 = sum(l.field for l in design(0.035, 0.005, 1.25e-3, 8, 25, 4.0))
    assert math.isclose(b4, 4 * b1, rel_tol=1e-12)


def test_turn_count():
    assert sum(l.turns for l in design(0.035, 0.005, 1.25e-3, 8, 25, 1.0)) == 700


def test_faraday_relations_are_consistent():
    v, b, d = 40.0, 0.5, 0.02
    beta = rotation_deg(v, b, d)
    assert math.isclose(required_length_m(v, b, beta), d)
    assert math.isclose(required_field_T(v, d, beta), b)


def test_linear_fit_on_exact_line():
    x = np.arange(10.0)
    f = linear_fit(x, 2 * x + 1)
    assert math.isclose(f.slope, 2) and math.isclose(f.intercept, 1, abs_tol=1e-12)
    assert f.slope_std < 1e-12 and f.r2 == 1.0


def test_published_hybrid_results():
    d = load_hybrid(DATA)
    assert d["current_A"].size == 12
    np.testing.assert_allclose(d["total_field_mT"], 35 + d["solenoid_field_mT"])
    cal = linear_fit(d["current_A"], d["solenoid_field_mT"])
    assert abs(cal.slope - 1.045) < 0.005 and cal.r2 > 0.999
    rot = linear_fit(d["total_field_mT"], d["rotation_deg"])
    assert abs(rot.slope - 1.02) < 0.01 and abs(rot.r2 - 0.92) < 0.01
