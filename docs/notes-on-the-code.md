# Notes on the code

The code comes from two Jupyter notebooks written during the mini-project
(solenoid field and rotator sizing, analysis of the hybrid configuration). It
was reorganised into functions with tests; the physics is unchanged.

## What changed

- Repeated notebook cells (the coil calculation appeared four times with
  different parameters) became one function, `faraday.coil.design`, and one
  command with arguments.
- The measurement table, typed in several cells, is now a single CSV file in
  `data/`, read by every script.
- Fits now report one-sigma standard errors on the slope.
- Tests check the coil formula (long-solenoid limit, linearity), the Faraday
  relations and the published fit values.

## Points corrected or left out

- **Data value at 3.0 A.** One cell used 2.95° and the others 2.98°. The CSV
  keeps 2.98°, the value used in the report and in the fits quoted.
- **Material constants.** The notebooks contained Verdet constants for silica,
  TGG and Bi:YIG written as comments. They are not built into the code: the
  silica value (3.3e-6 rad/(T m)) is several orders of magnitude too small, and
  values for a garnet near saturation are not Verdet constants in the linear
  sense. The design script takes V as a required argument, to be taken from a
  cited source.
- **Theory curve.** A cell compared the measurements with beta = V B d using
  the total field B. This is not reproduced: in a saturated garnet the change of
  angle is not proportional to the total field.
