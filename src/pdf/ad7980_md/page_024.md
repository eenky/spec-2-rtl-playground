

CHAIN MODE WITH BUSY INDICATOR

This mode can also be used to daisy-chain multiple AD7980 devices on a 3-wire serial interface while providing a busy indicator. This feature is useful for reducing component count and wiring connections, for example, in isolated multiconverter applications or for systems with a limited interfacing capacity. Data readback is analogous to clocking a shift register.

A connection diagram example using three AD7980 devices is shown in Figure 40, and the corresponding timing is given in Figure 41.

When SDI and CNV are low, SDO is driven low. With SCK high, a rising edge on CNV initiates a conversion, selects the chain mode, and enables the busy indicator feature. In this mode, CNV is held high during the conversion phase and the subsequent data readback. When all ADCs in the chain have completed their conversions, the SDO pin of the ADC closest to the digital host (see the AD7980 ADC labeled C in Figure 40) is driven high. This transition on SDO can be used as a busy indicator to trigger the data readback controlled by the digital host. The AD7980 then enters the acquisition phase and powers down. The data bits stored in the internal shift register are clocked out, MSB first, by subsequent SCK falling edges. For each ADC, SDI feeds the input of the internal shift register and is clocked by the SCK falling edge. Each ADC in the chain outputs its data MSB first, and \( 16 \times N + 1 \) clocks are required to readback the N ADCs. Although the rising edge can be used to capture the data, a digital host using the SCK falling edge allows a faster reading rate and, consequently, more AD7980 devices in the chain, provided the digital host has an acceptable hold time.

![Chain Mode with Busy Indicator Connection Diagram](https://i.imgur.com/3Q5z5QG.png)

Figure 40. Chain Mode with Busy Indicator Connection Diagram

![Chain Mode with Busy Indicator Serial Interface Timing](https://i.imgur.com/7Q5z5QG.png)

Figure 41. Chain Mode with Busy Indicator Serial Interface Timing