

16-Bit, 1 MSPS, PulSAR ADC in MSOP/LFCSP

Data Sheet

AD7980

FEATURES
High performance
Pseudo differential analog input range
0 V to \( V_{REF} \) with \( V_{REF} \) between 2.5 V to 5 V
Throughput: 1 MSPS
Zero latency architecture
16-bit resolution with no missing codes
INL: ±0.6 LSB typical, ±1.25 LSB maximum
Dynamic range: 92 dB, \( V_{REF} = 5 \) V
SNR: 91.5 dB at \( f_{IN} = 10 \) kHz, \( V_{REF} = 5 \) V
THD: –114 dB at \( f_{IN} = 10 \) kHz, \( V_{REF} = 5 \) V
SINAD: 91 dB at \( f_{IN} = 10 \) kHz, \( V_{REF} = 5 \) V
Low power dissipation
Single-supply 2.5 V operation with 1.8 V/2.5 V/3 V/5 V logic interface
4 mW at 1 MSPS (VDD only)
7 mW at 1 MSPS (total)
70 \( \mu \)W at 10 kSPS
Proprietary serial interface
SPI/QSPI/MICROWIRE™/DSP compatible
Daisy-chain multiple ADCs and busy indicator
10-lead MSOP, 10-lead, 3 mm × 3 mm LFCSP
Wide operating temperature range: –40°C to +125°C

APPLICATIONS
Automated test equipment
Data acquisition systems
Medical instruments
Machine automation

TYPICAL APPLICATION CIRCUIT

![Typical application circuit diagram](https://i.imgur.com/3Q5z5QG.png)

Figure 1.

GENERAL DESCRIPTION
The AD7980\( ^1 \) is a 16-bit, successive approximation, analog-to-digital converter (ADC) that operates from a single power supply, VDD. It contains a low power, high speed, 16-bit sampling ADC and a versatile serial interface port. On the CNV rising edge, it samples an analog input, IN+, between 0 V to REF with respect to a ground sense, IN–. The reference voltage, REF, is applied externally and can be set independent of the supply voltage, VDD. Its power scales linearly with throughput.

The SPI-compatible serial interface also features the ability, using the SDI input, to daisy-chain several ADCs on a single, 3-wire bus and provides an optional busy indicator. It is compatible with 1.8 V, 2.5 V, 3 V, or 5 V logic, using the separate supply VIO.

The AD7980 is housed in a 10-lead MSOP or a 10-lead LFCSP with operation specified from –40°C to +125°C.

\( ^1 \) Protected by U.S. Patent 6,703,961.

Table 1. MSOP, LFCSP 16-/18-/20-Bit Precision SAR ADCs and SAR ADC-Based μModule Data Acquisition Solutions

<table>
  <tr>
    <th>Type</th>
    <th>≤100 kSPS</th>
    <th>≤250 kSPS</th>
    <th>≤500 kSPS</th>
    <th>≤1000 kSPS</th>
    <th>≤2000 kSPS</th>
    <th>μModule Data Acquisition Solutions</th>
  </tr>
  <tr>
    <td>Differential<br>20-Bit<br>18-Bit</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td>AD4022<sup>1</sup><br>AD4021<sup>1</sup><br>AD4020<sup>1</sup></td>
  </tr>
  <tr>
    <td>16-Bit</td>
    <td>AD7989-1<sup>1</sup></td>
    <td>AD7691<sup>1</sup></td>
    <td>AD4011<sup>1</sup><br>AD4007<sup>1</sup><br>AD7690<sup>1</sup><br>AD7982<sup>1</sup><br>AD7984<sup>1</sup></td>
    <td>AD7688<sup>1</sup><br>AD7693<sup>1</sup><br>AD7916<sup>1</sup></td>
    <td>AD4005<sup>1</sup><br>AD4001<sup>1</sup></td>
    <td></td>
  </tr>
  <tr>
    <td>Pseudo Differential<br>18-Bit<br>16-Bit</td>
    <td></td>
    <td></td>
    <td>AD4010<sup>1</sup><br>AD4006<sup>1</sup><br>AD4002<sup>1</sup></td>
    <td>AD4004<sup>1</sup><br>AD4000<sup>1</sup></td>
    <td>ADAQ7980<br>ADAQ7988</td>
    <td></td>
  </tr>
  <tr>
    <td>16-Bit</td>
    <td>AD7684</td>
    <td>AD7687<sup>1</sup></td>
    <td>AD7688<sup>1</sup><br>AD7693<sup>1</sup><br>AD7916<sup>1</sup></td>
    <td>AD4005<sup>1</sup><br>AD4001<sup>1</sup></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>16-Bit</td>
    <td>AD7988-1<sup>1</sup><br>AD7680<br>AD7683</td>
    <td>AD7685<sup>1</sup><br>AD7694</td>
    <td>AD7988-5<sup>1</sup><br>AD7686<sup>1</sup></td>
    <td>AD7980<sup>1</sup><br>AD7983<sup>1</sup></td>
    <td></td>
    <td></td>
  </tr>
</table>

1 Pin for pin compatible.