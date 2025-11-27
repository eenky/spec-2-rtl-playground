

VDD = 2.5 V, VIO = 1.71 V to 5.5 V, \( V_{REF} = 5 \) V, \( T_A = -40^\circ C \) to \( +125^\circ C \), unless otherwise noted.

Table 3.

<table>
  <tr>
    <th>Parameter</th>
    <th>Test Conditions/Comments</th>
    <th>Min</th>
    <th>Typ</th>
    <th>Max</th>
    <th>Unit</th>
  </tr>
  <tr>
    <td rowspan="2">REFERENCE<br>Voltage Range<br>Load Current</td>
    <td rowspan="2">1 MSPS, REF = 5 V</td>
    <td>2.4</td>
    <td>330</td>
    <td>5.1</td>
    <td>V<br>\( \mu A \)</td>
  </tr>
  <tr></tr>
  <tr>
    <td>SAMPLING DYNAMICS<br>–3 dB Input Bandwidth<br>Aperture Delay</td>
    <td>VDD = 2.5 V</td>
    <td>10</td>
    <td>2.0</td>
    <td></td>
    <td>MHz<br>ns</td>
  </tr>
  <tr>
    <td>DIGITAL INPUTS<br>Logic Levels<br>\( V_{IL} \)<br>\( V_{IH} \)<br>\( V_{IL} \)<br>\( V_{IH} \)<br>\( I_{IL} \)<br>\( I_{IH} \)</td>
    <td>VIO > 3V<br>VIO > 3V<br>VIO \( \leq 3V \)<br>VIO \( \leq 3V \)<br>\( I_{IL} \)<br>\( I_{IH} \)</td>
    <td>–0.3<br>0.7 \( \times \) VIO<br>–0.3<br>0.9 \( \times \) VIO<br>–1<br>–1</td>
    <td>0.3 \( \times \) VIO<br>VIO + 0.3<br>0.1 \( \times \) VIO<br>VIO + 0.3<br>+1<br>+1</td>
    <td></td>
    <td>V<br>V<br>\( \mu A \)<br>\( \mu A \)<br>\( \mu A \)<br>\( \mu A \)</td>
  </tr>
  <tr>
    <td>DIGITAL OUTPUTS<br>Data Format<br>Pipeline Delay<br>\( V_{OL} \)<br>\( V_{OH} \)</td>
    <td></td>
    <td colspan="4">Serial 16 bits straight binary<br>Conversion results available immediately after completed conversion<br>0.4<br>VIO – 0.3</td>
    <td>V<br>V</td>
  </tr>
  <tr>
    <td>POWER SUPPLIES<br>VDD<br>VIO<br>Standby Current<sup>1,2</sup><br>Power Dissipation<br>Total<br>VDD Only<br>REF Only<br>VIO Only<br>Energy per Conversion</td>
    <td>VDD and VIO = 2.5 V, 25°C<br>VDD = 2.625 V, \( V_{REF} = 5 \) V, VIO = 3 V<br>10 kSPS throughput<br>1 MSPS throughput, B grade<br>1 MSPS throughput, A grade</td>
    <td>2.375<br>1.71<br>0.35<br>70<br>7.0<br>7.0<br>4<br>1.7<br>1.3<br>7.0</td>
    <td>2.5<br>5.5<br>0.35<br>7.0<br>9.0<br>10<br>mW<br>mW<br>mW<br>nJ/sample</td>
    <td>2.625<br>5.5<br>\( \mu A \)<br>\( \mu W \)<br>mW<br>mW<br>mW<br>nJ/sample</td>
    <td>V<br>V<br>\( \mu A \)<br>\( \mu W \)<br>mW<br>mW<br>mW<br>nJ/sample</td>
  </tr>
  <tr>
    <td>TEMPERATURE RANGE<sup>3</sup><br>Specified Performance</td>
    <td>\( T_{MIN} \) to \( T_{MAX} \)</td>
    <td>–40</td>
    <td>+125</td>
    <td></td>
    <td>\( ^\circ C \)</td>
  </tr>
</table>

<sup>1</sup> With all digital inputs forced to VIO or GND as required.
<sup>2</sup> During the acquisition phase.
<sup>3</sup> Contact sales for extended temperature range.