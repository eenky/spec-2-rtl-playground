

CHAIN MODE WITHOUT BUSY INDICATOR

This mode can be used to daisy-chain multiple AD7980 devices on a 3-wire serial interface. This feature is useful for reducing component count and wiring connections, for example, in isolated multi-converter applications or for systems with a limited interfacing capacity. Data readback is analogous to clocking a shift register.

A connection diagram example using two AD7980s is shown in Figure 38, and the corresponding timing is given in Figure 39.

When SDI and CNV are low, SDO is driven low. With SCK low, a rising edge on CNV initiates a conversion, selects the chain mode, and disables the busy indicator. In this mode, CNV is held high during the conversion phase and the subsequent data readback. When the conversion is complete, the MSB is output onto SDO and the AD7980 enters the acquisition phase and powers down. The remaining data bits stored in the internal shift register are clocked by subsequent SCK falling edges. For each ADC, SDI feeds the input of the internal shift register and is clocked by the SCK falling edge. Each ADC in the chain outputs its data MSB first, and \(16 \times N\) clocks are required to readback the N ADCs. The data is valid on both SCK edges. Although the rising edge can be used to capture the data, a digital host using the SCK falling edge allows a faster reading rate and, consequently, more AD7980 devices in the chain, provided the digital host has an acceptable hold time. The maximum conversion rate may be reduced due to the total readback time.

![Chain Mode Without Busy Indicator Connection Diagram](https://i.imgur.com/3Q5z5QG.png)

Figure 38. Chain Mode Without Busy Indicator Connection Diagram

![Chain Mode Without Busy Indicator Serial Interface Timing](https://i.imgur.com/7Q5z5QG.png)

Figure 39. Chain Mode Without Busy Indicator Serial Interface Timing