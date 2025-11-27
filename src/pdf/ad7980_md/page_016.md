

AD7980

Transfer Functions
The ideal transfer characteristic for the AD7980 is shown in Figure 25 and Table 9.

Table 9. Output Codes and Ideal Input Voltages

<table>
  <tr>
    <th>Description</th>
    <th>V<sub>REF</sub> = 5 V</th>
    <th>Analog Input</th>
    <th>Digital Output Code (Hex)</th>
  </tr>
  <tr>
    <td>FSR – 1 LSB</td>
    <td>4.999924 V</td>
    <td></td>
    <td>FFFF<sup>1</sup></td>
  </tr>
  <tr>
    <td>Midscale + 1 LSB</td>
    <td>2.500076 V</td>
    <td></td>
    <td>8001</td>
  </tr>
  <tr>
    <td>Midscale</td>
    <td>2.5 V</td>
    <td></td>
    <td>8000</td>
  </tr>
  <tr>
    <td>Midscale – 1 LSB</td>
    <td>2.499924 V</td>
    <td></td>
    <td>7FFF</td>
  </tr>
  <tr>
    <td>–FSR + 1 LSB</td>
    <td>76.3 μV</td>
    <td></td>
    <td>0001</td>
  </tr>
  <tr>
    <td>–FSR</td>
    <td>0 V</td>
    <td></td>
    <td>0000<sup>2</sup></td>
  </tr>
</table>

<sup>1</sup>This is also the code for an overranged analog input (V<sub>IN+</sub> – V<sub>IN–</sub> above V<sub>REF</sub> – V<sub>GND</sub>).
<sup>2</sup>This is also the code for an underranged analog input (V<sub>IN+</sub> – V<sub>IN–</sub> below V<sub>GND</sub>).

TYPICAL APPLICATION CIRCUIT WITH MULTIPLE SUPPLIES
Figure 26 shows an example of a typical application circuit for the AD7980 when multiple supplies are available.

1SEE THE VOLTAGE REFERENCE INPUT SECTION FOR REFERENCE SELECTION.
2C<sub>REF</sub> IS USUALLY A 10μF CERAMIC CAPACITOR (X5R).
3SEE THE DRIVER AMPLIFIER CHOICE SECTION.
4RECOMMENDED FILTER CONFIGURATION. SEE THE ANALOG INPUTS SECTION.
5SEE THE DIGITAL INTERFACE FOR THE MOST CONVENIENT INTERFACE MODE.

Figure 25. ADC Ideal Transfer Function

Figure 26. Typical Application Circuit with Multiple Supplies