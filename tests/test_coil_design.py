import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from coil_design import MU0, design, layer_field  # noqa: E402


def test_long_solenoid_limit():
    """For l >> R the field tends to mu0 * n * I."""
    length, radius, turns, current = 1.0, 1e-3, 1000, 2.0
    expected = MU0 * turns / length * current
    assert math.isclose(layer_field(turns, current, length, radius), expected, rel_tol=1e-5)


def test_field_is_linear_in_current():
    b1 = sum(l.field for l in design(0.035, 0.005, 1.25e-3, 8, 25, 1.0))
    b4 = sum(l.field for l in design(0.035, 0.005, 1.25e-3, 8, 25, 4.0))
    assert math.isclose(b4, 4 * b1, rel_tol=1e-12)


def test_turn_count():
    layers = design(0.035, 0.005, 1.25e-3, 8, 25, 1.0)
    assert sum(l.turns for l in layers) == 700
