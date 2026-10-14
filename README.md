# Tunable fibre Faraday rotator at 1550 nm

Master's mini-project, Laboratoire de Photonique d'Angers (LphiA),
University of Angers. Eight weeks full time, defended in March 2026.
Individual project under the guidance of a supervisor.

## Question

A Faraday rotator turns the polarisation of light by an angle fixed at
manufacture, usually 45°. In a commercial fibre device the material and its
length cannot be changed, so the only handle left is the magnetic field.
The project asked whether an external field can tune the angle of a
commercial 45° fibre rotator at 1550 nm, and which way of applying that
field works best.

## Set-up and method

- All-fibre bench: 1550 nm DFB laser, isolator, the rotator on
  polarisation-maintaining fibre, a polarising beam splitter and two power
  meters.
- The rotation angle is derived from the power ratio between the two
  outputs, with a measurement without external field as reference. The
  method gives the angle modulo 90°.
- Three ways of applying the field were compared against the same criteria:
  two ferrite ring magnets; a solenoid; a hybrid configuration where a
  magnet sets the operating point and the solenoid modulates it.
- The field was measured with a teslameter at each current.

## Results

| Configuration | Result |
|---|---|
| Ring magnets, opposing the internal field | Angle brought from about 44° to about 9° (three trials). Step-wise tuning only. |
| Ring magnets, aligned with the internal field | No measurable effect. |
| Solenoid alone | Field linear in current, 1.05 mT/A (4.2 mT at 4 A); too weak for a usable change in angle. |
| Hybrid (35 mT bias + solenoid) | Angle linear in current, about 1°/mT, 4.8° at 4 A (linear fit on 12 points, R² = 0.92). Only configuration giving continuous tuning. |

## Limits

- No quantified measurement uncertainty.
- The field was measured next to the active region, not inside it.
- Small fluctuations of the polarisation state made readings harder.
- The device most likely uses a garnet close to magnetic saturation, which
  would explain why aligned magnets have no effect. In that regime the
  measured slope is a sensitivity around the operating point, not a Verdet
  constant. This interpretation was not checked by measuring the
  magnetisation.

## Contents

```
report/mini-project-report-2026-fr.pdf   full mini-project report (French, 43 pages)
src/coil_design.py        sizing of a multilayer solenoid (field at the centre, wire length)
tests/                    checks of the field formula (long-solenoid limit, linearity)
data/                     measurement tables (to be added)
figures/                  figures (to be added)
```

### Coil sizing

```bash
pip install -r requirements.txt
python src/coil_design.py --current 1          # field per ampere for the default design
python src/coil_design.py --layers 10 --csv coil.csv
python -m pytest tests
```

The default parameters (3.5 cm long, 25 layers, 700 turns) describe a
design study. They predict about 16.8 mT/A, whereas the solenoid used in
the experiment gave 1.05 mT/A. The script was not compared with the coil
actually built, whose final parameters differ from this design.

## Author

Mouhssine Ait Said. Supervision: LphiA, University of Angers.
Publication of the code, results and report authorised by the supervisor.

## Licence

MIT, see `LICENSE`.
