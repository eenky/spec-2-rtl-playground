

AD7980

VOLTAGE REFERENCE INPUT
The AD7980 voltage reference input, REF, has a dynamic input impedance and should therefore be driven by a low impedance source with efficient decoupling between the REF and GND pins, as explained in the Layout section.

When REF is driven by a very low impedance source, for example, a reference buffer using the AD8031, the ADA4805-1, or the ADA4807-1, a ceramic chip capacitor is appropriate for optimum performance.

If an unbuffered reference voltage is used, the decoupling value depends on the reference used. For instance, a 22 μF (X5R, 1206 size) ceramic chip capacitor is appropriate for optimum performance using a low temperature drift reference, such as the ADR435, ADR445, LTC6655, or ADR4550.

If desired, a reference-decoupling capacitor value as small as 2.2 μF can be used with a minimal impact on performance, especially DNL.

Regardless, there is no need for an additional lower value ceramic decoupling capacitor (for example, 100 nF) between the REF and GND pins.

POWER SUPPLY
The AD7980 uses two power supply pins: a core supply, VDD, and a digital input/output interface supply, VIO. VIO allows direct interface with any logic between 1.8 V and 5.0 V. To reduce the number of supplies needed, VIO and VDD can be tied together. When VIO is greater than or equal to VDD, the AD7980 is insensitive to power supply sequencing. In normal operation, if the magnitude of VIO is less than the magnitude of VDD, VIO must be applied before VDD. Additionally, it is very insensitive to power supply variations over a wide frequency range, as shown in Figure 28.

![PSRR vs. Frequency graph](https://i.imgur.com/psrr_vs_freq.png)
Figure 28. PSRR vs. Frequency

The AD7980 powers down automatically at the end of each conversion phase and, therefore, the power scales linearly with the sampling rate. This makes the device ideal for low sampling rate (even of a few Hz) and low battery-powered applications.

![Operating Currents vs. Sampling Rate graph](https://i.imgur.com/operating_currents_vs_sampling_rate.png)
Figure 29. Operating Currents vs. Sampling Rate

DIGITAL INTERFACE
Though the AD7980 has a reduced number of pins, it offers flexibility in its serial interface modes.

The AD7980, when in \(\overline{\mathrm{CS}}\) mode, is compatible with SPI, QSPI™, and digital hosts. This interface can use either a 3-wire or 4-wire interface. A 3-wire interface using the CNV, SCK, and SDO signals minimizes wiring connections useful, for instance, in isolated applications. A 4-wire interface using the SDI, CNV, SCK, and SDO signals allows CNV, which initiates the conversions, to be independent of the readback timing (SDI). This is useful in low jitter sampling or simultaneous sampling applications.

The AD7980, when in chain mode, provides a daisy-chain feature using the SDI input for cascading multiple ADCs on a single data line similar to a shift register.

The mode in which the device operates depends on the SDI level when the CNV rising edge occurs. The \(\overline{\mathrm{CS}}\) mode is selected if SDI is high, and the chain mode is selected if SDI is low. The SDI hold time is such that when SDI and CNV are connected together, the chain mode is selected.

In either mode, the AD7980 offers the flexibility to optionally force a start bit in front of the data bits. This start bit can be used as a busy signal indicator to interrupt the digital host and trigger the data reading. Otherwise, without a busy indicator, the user must time out the maximum conversion time prior to readback.

The busy indicator feature is enabled in the \(\overline{\mathrm{CS}}\) mode if CNV or SDI is low when the ADC conversion ends (see Figure 33 and Figure 37). The busy indicator feature is enabled in the chain mode if SCK is high during the CNV rising edge (see Figure 41).