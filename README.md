# MOSFET-Based 2-Way Sallen-Key Active Crossover

A 2-way active audio crossover built from two second-order Sallen-Key filters: a low-pass for the woofer and a high-pass for the tweeter, both with a crossover frequency of about 1.07 kHz. Instead of the usual op-amp buffer, each filter uses a single 2N7000 MOSFET wired as a source follower, and the whole circuit runs from one 9 V supply.

We designed, simulated (LTspice), built and tested this on a breadboard for the ECPR21 Devices and Networks Laboratory at NIT Tiruchirappalli.

## Design

- **Buffer:** 2N7000 source follower with RS = 1.68 kΩ. Its gain is about 0.94 instead of 1, which lowers the filter Q.
- **Keeping Q near 0.707:** the LPF uses a 2.2 : 1 capacitor ratio (C1 = 22 nF, C2 = 10 nF). The HPF uses the same 2.2 : 1 ratio on its resistors (R1 = 10 kΩ, R2 = 22 kΩ). This gives Q ≈ 0.70 with the follower's gain.
- **Biasing:** the gate sits at 4.5 V through two 1 MΩ resistors. In the HPF, a 1 µF capacitor in series with R2 stops it from pulling the gate bias down to about 0.2 V.
- **Cutoff:** fc = 1 / (2π√(R1R2C1C2)) ≈ 1073 Hz for both channels.

The full component list and calculations are in the report.

## Results

| | Calculated | Measured |
|---|---|---|
| Passband gain | 0.94 | 0.95 – 1.00 |
| LPF −3 dB point | 1.07 kHz | 1.01 kHz |
| HPF −3 dB point | 1.07 kHz | 0.86 kHz |
| Crossover frequency | 1.07 kHz | 0.9 kHz |
| Source voltage / drain current | 2.5 V / 1.49 mA | 2.75 V / 1.64 mA |

The calculated magnitude and phase response is in Figure 2 of the report, and Figure 3 compares the measured gain with the calculated curves.

The measured cutoffs are lower than calculated, mainly because of the ±10–20% tolerance of the ceramic capacitors we used. An LTspice simulation of both channels matches the calculated gains to within 0.02 at every test frequency.

## Files

| File | What it is |
|---|---|
| `Sallen-Key_LPF_Channel1.asc` | LTspice schematic, channel 1 (low-pass) |
| `Sallen-Key_HPF_Channel2.asc` | LTspice schematic, channel 2 (high-pass) |
| `Sallen-Key_LPF_Channel1_TB.asc`, `Sallen-Key_HPF_Channel2_TB.asc` | LTspice testbenches: DC bias voltages and gain at each test frequency, plus an optional AC sweep |
| `make_report_figures.py` | Python script that regenerates Figures 2 and 3 of the report |
| `MOSFET_Sallen-Key_Lab_Report.pdf` | Full lab report |

## Running it

**LTspice:** open one of the `_TB.asc` files and click Run. The results are in View → SPICE Error Log, where steps 1–9 are 50 Hz, 100 Hz, 200 Hz, 500 Hz, 1 kHz, 1.07 kHz, 2 kHz, 5 kHz and 10 kHz.

**Plots:**
```
pip install numpy matplotlib
python make_report_figures.py
```

## Notes

- The two outputs are 180° apart at the crossover frequency, so one speaker should be wired with reversed polarity to avoid a dip in the combined response.
- The outputs are line level and need a power amplifier to drive speakers.
- Possible improvements: Linkwitz-Riley alignment, a constant-current source in place of RS to bring the gain closer to 1, and film or C0G capacitors for a more accurate fc.

## Team

Ashwin Chandra R and C P Amanjith, Department of ECE, NIT Tiruchirappalli (2029)
