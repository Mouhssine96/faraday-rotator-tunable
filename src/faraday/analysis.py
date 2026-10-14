"""Linear fit with standard uncertainties, used for the hybrid configuration."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class LinearFit:
    slope: float
    intercept: float
    slope_std: float
    intercept_std: float
    r2: float
    n: int

    def __call__(self, x):
        return self.slope * np.asarray(x, float) + self.intercept


def linear_fit(x, y) -> LinearFit:
    """Least-squares line y = a x + b with one-sigma standard errors on a and b."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    n = x.size
    (a, b), cov = np.polyfit(x, y, 1, cov="unscaled")
    res = y - (a * x + b)
    s2 = np.sum(res ** 2) / (n - 2)
    cov = cov * s2
    r2 = 1.0 - np.sum(res ** 2) / np.sum((y - y.mean()) ** 2)
    return LinearFit(float(a), float(b), float(np.sqrt(cov[0, 0])), float(np.sqrt(cov[1, 1])),
                     float(r2), int(n))


def load_hybrid(path) -> dict:
    """Read data/hybrid_configuration.csv into arrays."""
    data = np.genfromtxt(Path(path), delimiter=",", names=True)
    return {name: data[name] for name in data.dtype.names}
