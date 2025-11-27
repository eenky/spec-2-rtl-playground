

4-WIRE \(\overline{CS}\) MODE WITH BUSY INDICATOR

This mode is usually used when a single AD7980 is connected to an SPI-compatible digital host that has an interrupt input, and it is desired to keep CNV, which is used to sample the analog input, independent of the signal used to select the data reading. This requirement is particularly important in applications where low jitter on CNV is desired.

The connection diagram is shown in Figure 36, and the corresponding timing is given in Figure 37.

With SDI high, a rising edge on CNV initiates a conversion, selects the CS mode, and forces SDO to high impedance. In this mode, CNV must be held high during the conversion phase and the subsequent data readback (if SDI and CNV are low, SDO is driven low). Prior to the minimum conversion time, SDI can be used to select other SPI devices, such as analog multiplexers, but SDI must be returned low before the minimum conversion time elapses and then held low for the maximum conversion time to guarantee the generation of the busy signal indicator. When the conversion is complete, SDO goes from high impedance to low.

With a pull-up on the SDO line, this transition can be used as an interrupt signal to initiate the data readback controlled by the digital host. The AD7980 then enters the acquisition phase and powers down. The data bits are clocked out, MSB first, by subsequent SCK falling edges. The data is valid on both SCK edges. Although the rising edge can be used to capture the data, a digital host using the SCK falling edge allows a faster reading rate provided it has an acceptable hold time. After the optional 17th SCK falling edge or SDI going high, whichever is earlier, the SDO returns to high impedance.

![4-Wire CS Mode with Busy Indicator Connection Diagram](https://i.imgur.com/3Q5z5QG.png)

Figure 36. 4-Wire \(\overline{CS}\) Mode with Busy Indicator Connection Diagram

![4-Wire CS Mode with Busy Indicator Serial Interface Timing](https://i.imgur.com/7Q5z5QG.png)

Figure 37. 4-Wire \(\overline{CS}\) Mode with Busy Indicator Serial Interface Timing