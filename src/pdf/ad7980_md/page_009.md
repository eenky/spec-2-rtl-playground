

PIN CONFIGURATIONS AND FUNCTION DESCRIPTIONS

Figure 3. 10-Lead MSOP Pin Configuration

Figure 4. 10-Lead LFCSP Pin Configuration

NOTES
1. CONNECT THE EXPOSED PAD TO GND. THIS CONNECTION IS NOT REQUIRED TO MEET THE ELECTRICAL PERFORMANCES.

Table 8. Pin Function Descriptions

<table>
  <tr>
    <th>Pin No.</th>
    <th>MSOP</th>
    <th>LFCSP</th>
    <th>Mnemonic</th>
    <th>Type<sup>1</sup></th>
    <th>Description</th>
  </tr>
  <tr>
    <td>1</td>
    <td>1</td>
    <td>1</td>
    <td>REF</td>
    <td>AI</td>
    <td>Reference Input Voltage. The REF range is from 2.4 V to 5.1 V. It is referred to the GND pin. This pin should be decoupled closely to the pin with a 10 μF capacitor.<br>Power Supply.</td>
  </tr>
  <tr>
    <td>2</td>
    <td>2</td>
    <td>2</td>
    <td>VDD</td>
    <td>P</td>
    <td>Power Supply.</td>
  </tr>
  <tr>
    <td>3</td>
    <td>3</td>
    <td>3</td>
    <td>IN+</td>
    <td>AI</td>
    <td>Analog Input. It is referred to IN–. The voltage range, for example, the difference between IN+ and IN–, is 0 V to \( V_{REF} \).</td>
  </tr>
  <tr>
    <td>4</td>
    <td>4</td>
    <td>4</td>
    <td>IN–</td>
    <td>AI</td>
    <td>Analog Input Ground Sense. To be connected to the analog ground plane or to a remote sense ground.</td>
  </tr>
  <tr>
    <td>5</td>
    <td>5</td>
    <td>5</td>
    <td>GND</td>
    <td>P</td>
    <td>Power Supply Ground.</td>
  </tr>
  <tr>
    <td>6</td>
    <td>6</td>
    <td>6</td>
    <td>CNV</td>
    <td>DI</td>
    <td>Convert Input. This input has multiple functions. On its leading edge, it initiates the conversions and selects the interface mode of the device, chain, or CS mode. In CS mode, it enables the SDO pin when low. In chain mode, the data should be read when CNV is high.<br>Serial Data Output. The conversion result is output on this pin. It is synchronized to SCK.<br>Serial Data Clock Input. When the device is selected, the conversion result is shifted out by this clock.</td>
  </tr>
  <tr>
    <td>7</td>
    <td>7</td>
    <td>7</td>
    <td>SDO</td>
    <td>DO</td>
    <td>Serial Data Output. The conversion result is output on this pin. It is synchronized to SCK.</td>
  </tr>
  <tr>
    <td>8</td>
    <td>8</td>
    <td>8</td>
    <td>SCK</td>
    <td>DI</td>
    <td>Serial Data Clock Input. When the device is selected, the conversion result is shifted out by this clock.</td>
  </tr>
  <tr>
    <td>9</td>
    <td>9</td>
    <td>9</td>
    <td>SDI</td>
    <td>DI</td>
    <td>Serial Data Input. This input provides multiple features. It selects the interface mode of the ADC as follows. Chain mode is selected if SDI is low during the CNV rising edge. In this mode, SDI is used as a data input to daisy-chain the conversion results of two or more ADCs onto a single SDO line. The digital data level on SDI is output on SDO with a delay of 16 SCK cycles. CS mode is selected if SDI is high during the CNV rising edge. In this mode, either SDI or CNV can enable the serial output signals when low; if SDI or CNV is low when the conversion is complete, the busy indicator feature is enabled.</td>
  </tr>
  <tr>
    <td>10</td>
    <td>10</td>
    <td>10</td>
    <td>VIO</td>
    <td>P</td>
    <td>Input/Output Interface Digital Power. Nominally at the same supply as the host interface (1.8 V, 2.5 V, 3 V, or 5 V).</td>
  </tr>
  <tr>
    <td>Not applicable</td>
    <td>0</td>
    <td>0</td>
    <td>EPAD</td>
    <td>Not applicable</td>
    <td>Exposed Pad. Connect the exposed pad to GND. This connection is not required to meet the electrical performances.</td>
  </tr>
</table>

<sup>1</sup>AI = analog input, DI = digital input, DO = digital output, and P = power.