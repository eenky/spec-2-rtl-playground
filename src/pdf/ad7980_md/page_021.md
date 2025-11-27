

4-WIRE CS MODE WITHOUT BUSY INDICATOR

This mode is usually used when multiple AD7980 devices are connected to an SPI-compatible digital host.

A connection diagram example using two AD7980 devices is shown in Figure 34, and the corresponding timing is given in Figure 35.

With SDI high, a rising edge on CNV initiates a conversion, selects the CS mode, and forces SDO to high impedance. In this mode, CNV must be held high during the conversion phase and the subsequent data readback (if SDI and CNV are low, SDO is driven low). Prior to the minimum conversion time, SDI can be used to select other SPI devices, such as analog multiplexers, but SDI must be returned high before the minimum conversion time elapses and then held high for the maximum conversion time to avoid the generation of the busy signal indicator.

When the conversion is complete, the AD7980 enters the acquisition phase and powers down. Each ADC result can be read by bringing its SDI input low, which consequently outputs the MSB onto SDO. The remaining data bits are then clocked by subsequent SCK falling edges. The data is valid on both SCK edges. Although the rising edge can be used to capture the data, a digital host using the SCK falling edge allows a faster reading rate provided it has an acceptable hold time. After the 16th SCK falling edge or when SDI goes high, whichever is earlier, SDO returns to high impedance and another AD7980 can be read.

![4-Wire CS Mode Without Busy Indicator Connection Diagram](https://i.imgur.com/4WireCSConn.png)

Figure 34. 4-Wire CS Mode Without Busy Indicator Connection Diagram

![4-Wire CS Mode Without Busy Indicator Serial Interface Timing](https://i.imgur.com/4WireCSTiming.png)

Figure 35. 4-Wire CS Mode Without Busy Indicator Serial Interface Timing