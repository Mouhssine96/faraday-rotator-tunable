# Data

`hybrid_configuration.csv`: hybrid configuration (ferrite magnet + solenoid),
12 measurement points.

| Column | Meaning |
|---|---|
| `current_A` | solenoid current |
| `solenoid_field_mT` | field added by the solenoid, measured with a teslameter next to the active region |
| `total_field_mT` | 35 mT bias from the magnet + solenoid field |
| `rotation_deg` | change of the polarisation angle relative to 0 A |

The solenoid field column is also the calibration of the solenoid alone
(about 1.05 mT/A). Polarisation angles measured with the solenoid alone are
not published.
