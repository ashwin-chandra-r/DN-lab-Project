# Sallen-Key crossover - plots for the report (fig 2 and fig 3)
# needs numpy and matplotlib

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'serif'

blue = '#2f72d0'
orange = '#e5683a'

K = 0.94   # source follower gain

# LPF: R1 = R2 = 10k, C1 = 22n (feedback), C2 = 10n
R1l, R2l, C1l, C2l = 10e3, 10e3, 22e-9, 10e-9
# HPF: C1 = C2 = 10n, R1 = 10k (feedback), R2 = 22k
R1h, R2h, C1h, C2h = 10e3, 22e3, 10e-9, 10e-9


def lpf(f):
    s = 2j * np.pi * f
    return K / (1 + s*(C2l*(R1l + R2l) + R1l*C1l*(1 - K)) + s**2 * R1l*R2l*C1l*C2l)


def hpf(f):
    s = 2j * np.pi * f
    w0 = 1 / np.sqrt(R1h*R2h*C1h*C2h)
    b = (C1h + C2h)/(R2h*C1h*C2h) + (1 - K)/(R1h*C2h)
    return K * s**2 / (s**2 + b*s + w0**2)


# measured values from table 3 (Vin = 1 Vpp)
fm = np.array([50, 100, 200, 500, 1000, 1070, 2000, 5000, 10000])
lpf_m = np.array([0.96, 0.95, 0.94, 0.89, 0.69, 0.64, 0.32, 0.10, 0.03])
hpf_m = np.array([np.nan, 0.04, 0.10, 0.36, 0.78, 0.82, 0.95, 0.99, 1.00])  # no reading at 50 Hz
# readings marked * in the table (noise floor), drawn hollow
lpf_noise = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1], dtype=bool)
hpf_noise = np.array([0, 1, 1, 0, 0, 0, 0, 0, 0], dtype=bool)

ticks = [10, 100, 1000, 10000]
tick_labels = ['10', '100', '1k', '10k']


# ---- fig 2: magnitude + phase ----
f = np.logspace(1, np.log10(20e3), 1000)
HL = lpf(f)
HH = hpf(f)
magL = 20*np.log10(abs(HL))
magH = 20*np.log10(abs(HH))

fc = 1 / (2*np.pi*np.sqrt(R1l*R2l*C1l*C2l))   # same Q for both, so they cross at fc

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 6.4), sharex=True,
                               gridspec_kw={'height_ratios': [1.15, 1], 'hspace': 0.08})

ax1.semilogx(f, magL, color=blue, lw=2, label='Low-pass (woofer)')
ax1.semilogx(f, magH, color=orange, lw=2, label='High-pass (tweeter)')
lvl = 20*np.log10(K) - 3
ax1.axhline(lvl, color='gray', lw=0.8, ls=':')
ax1.text(13, lvl - 1.2, '-3 dB below passband level', color='dimgray', fontsize=8.5, va='top')
ax1.axvline(fc, color='k', lw=1, ls='--')
ax1.text(fc*1.06, -50, 'crossover %.2f kHz' % (fc/1000), fontsize=9)
ax1.set_ylim(-60, 2)
ax1.set_ylabel('Magnitude (dB)')
ax1.legend(loc='upper left', bbox_to_anchor=(0.005, 0.86), fontsize=9)

ax2.semilogx(f, np.angle(HL, deg=True), color=blue, lw=2)
ax2.semilogx(f, np.angle(HH, deg=True), color=orange, lw=2)
ax2.axvline(fc, color='k', lw=1, ls='--')
ax2.set_ylim(-185, 185)
ax2.set_yticks([-180, -90, 0, 90, 180])
ax2.set_ylabel('Phase (deg)')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_xlim(9, 22e3)
ax2.set_xticks(ticks)
ax2.set_xticklabels(tick_labels)

for ax in (ax1, ax2):
    ax.grid(True, which='both', color='#e4e4e4')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.savefig('fig2_calculated.png', dpi=200, bbox_inches='tight')


# ---- fig 3: measured vs calculated gain ----
f = np.logspace(np.log10(30), np.log10(15e3), 800)

# measured crossover - interpolate between the two points where LPF drops below HPF
d = lpf_m - hpf_m
i = np.where(d < 0)[0][0]
x = np.log10(fm[i-1]) + (np.log10(fm[i]) - np.log10(fm[i-1])) * d[i-1] / (d[i-1] - d[i])
fx = 10**x

fig, ax = plt.subplots(figsize=(7, 4.2))
ax.semilogx(f, abs(lpf(f)), color=blue, lw=2, label='LPF calculated')
ax.semilogx(f, abs(hpf(f)), color=orange, lw=2, label='HPF calculated')

ax.plot(fm, lpf_m, ':', color=blue, lw=1)
ax.plot(fm, hpf_m, ':', color=orange, lw=1)
ax.plot(fm[~lpf_noise], lpf_m[~lpf_noise], 's', color=blue, ms=7, mec='white', label='LPF measured')
ax.plot(fm[~hpf_noise], hpf_m[~hpf_noise], '^', color=orange, ms=7, mec='white', label='HPF measured')
ax.plot(fm[lpf_noise], lpf_m[lpf_noise], 's', mfc='white', mec=blue, mew=1.4, ms=7)
ax.plot(fm[hpf_noise], hpf_m[hpf_noise], '^', mfc='white', mec=orange, mew=1.4, ms=7)

ax.axvline(fx, color='k', lw=1, ls='--')
ax.text(fx*1.05, 0.04, 'measured\ncrossover\n~ %.1f kHz' % (fx/1000), fontsize=8.5)

ax.set_xlim(30, 15e3)
ax.set_ylim(0, 1.08)
ax.set_xticks(ticks[1:])
ax.set_xticklabels(tick_labels[1:])
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Gain (Vout/Vin)')
ax.grid(True, which='both', color='#e4e4e4')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='center left', fontsize=8.5)

plt.savefig('fig3_measured_vs_calc.png', dpi=200, bbox_inches='tight')
plt.show()
