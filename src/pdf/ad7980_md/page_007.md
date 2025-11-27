

VDD = 2.37 V to 2.63 V, VIO = 1.71 V to 2.3 V, T_A = -40°C to +125°C, unless otherwise stated. See Figure 2 for load conditions.

Table 5.

<table>
  <tr>
    <th>Parameter<sup>1</sup></th>
    <th>Symbol</th>
    <th>Min</th>
    <th>Typ</th>
    <th>Max</th>
    <th>Unit</th>
  </tr>
  <tr>
    <td>Throughput Rate</td>
    <td></td>
    <td></td>
    <td></td>
    <td>833</td>
    <td>kSPS</td>
  </tr>
  <tr>
    <td>Conversion Time: CNV Rising Edge to Data Available</td>
    <td>t_{CONV}</td>
    <td>500</td>
    <td>800</td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>Acquisition Time</td>
    <td>t_{ACQ}</td>
    <td>290</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>Time Between Conversions<sup>2</sup></td>
    <td>t_{CYC}</td>
    <td>1.2</td>
    <td></td>
    <td></td>
    <td>\mu s</td>
  </tr>
  <tr>
    <td>CNV Pulse Width (\(\overline{CS}\) Mode)</td>
    <td>t_{CNVH}</td>
    <td>10</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SCK Period (\(\overline{CS}\) Mode)</td>
    <td>t_{SCK}</td>
    <td>22</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SCK Period (Chain Mode)</td>
    <td>t_{SCK}</td>
    <td>23</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SCK Low Time</td>
    <td>t_{SCKL}</td>
    <td>6</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SCK High Time</td>
    <td>t_{SCKH}</td>
    <td>6</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SCK Falling Edge to Data Remains Valid</td>
    <td>t_{HSDO}</td>
    <td>3</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SCK Falling Edge to Data Valid Delay</td>
    <td>t_{DSDO}</td>
    <td>14</td>
    <td>21</td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>CNV or SDI Low to SDO D15 MSB Valid (\(\overline{CS}\) Mode)</td>
    <td>t_{EN}</td>
    <td>18</td>
    <td>40</td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>CNV or SDI High or Last SCK Falling Edge to SDO High Impedance (\(\overline{CS}\) Mode)</td>
    <td>t_{DIS}</td>
    <td></td>
    <td></td>
    <td>20</td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SDI Valid Setup Time from CNV Rising Edge</td>
    <td>t_{SSDICNV}</td>
    <td>5</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SDI Valid Hold Time from CNV Rising Edge (\(\overline{CS}\) Mode)</td>
    <td>t_{HSDICNV}</td>
    <td>10</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SDI Valid Hold Time from CNV Rising Edge (Chain Mode)</td>
    <td>t_{HSDICNV}</td>
    <td>0</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SCK Valid Setup Time from CNV Rising Edge (Chain Mode)</td>
    <td>t_{SSCKCNV}</td>
    <td>5</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SCK Valid Hold Time from CNV Rising Edge (Chain Mode)</td>
    <td>t_{HSCKCNV}</td>
    <td>5</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SDI Valid Setup Time from SCK Falling Edge (Chain Mode)</td>
    <td>t_{SSDISCK}</td>
    <td>2</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SDI Valid Hold Time from SCK Falling Edge (Chain Mode)</td>
    <td>t_{HSDISCK}</td>
    <td>3</td>
    <td></td>
    <td></td>
    <td>ns</td>
  </tr>
  <tr>
    <td>SDI High to SDO High (Chain Mode with Busy Indicator)</td>
    <td>t_{DSDOSDI}</td>
    <td></td>
    <td></td>
    <td>22</td>
    <td>ns</td>
  </tr>
</table>

<sup>1</sup> Timing parameters measured with respect to a falling edge are defined as triggered at x% VIO. Timing parameters measured with respect to a rising edge are defined as triggered at y% VIO. For VIO \leq 3\ \mathrm{V}, x = 90 and y = 10. For VIO > 3\ \mathrm{V}, x = 70 and y = 30. The minimum V_{IH} and maximum V_{IL} are used. See the Digital Inputs Specifications in Table 2.
<sup>2</sup> The time required to clock out N bits of data, t_{READ}, may be greater than t_{ACQ}, depending on the magnitude of VIO. If t_{READ} is greater than t_{ACQ}, the throughput must be limited to ensure that all N bits are read back from the device.

Timing Diagrams

![Load Circuit for Digital Interface Timing](https://i.imgur.com/3Q5z5QG.png)

Figure 2. Load Circuit for Digital Interface Timing