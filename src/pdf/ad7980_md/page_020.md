

3-WIRE \(\overline{CS}\) MODE WITH BUSY INDICATOR

This mode is usually used when a single AD7980 is connected to an SPI-compatible digital host having an interrupt input.

The connection diagram is shown in Figure 32, and the corresponding timing is given in Figure 33.

With SDI tied to VIO, a rising edge on CNV initiates a conversion, selects the CS mode, and forces SDO to high impedance. SDO is maintained in high impedance until the completion of the conversion irrespective of the state of CNV. Prior to the minimum conversion time, CNV can be used to select other SPI devices, such as analog multiplexers, but CNV must be returned low before the minimum conversion time elapses and then held low for the maximum conversion time to guarantee the generation of the busy signal indicator. When the conversion is complete, SDO goes from high impedance to low. With a pull-up on the SDO line, this transition can be used as an interrupt signal to initiate the data reading controlled by the digital host. The AD7980 then enters the acquisition phase and powers down. The data bits are clocked out, MSB first, by subsequent SCK falling edges. The data is valid on both SCK edges. Although the rising edge can be used to capture the data, a digital host using the SCK falling edge allows a faster reading rate provided it has an acceptable hold time. After the optional 17th SCK falling edge or when CNV goes high, whichever is earlier, SDO returns to high impedance.

If multiple AD7980 devices are selected at the same time, the SDO output pin handles this contention without damage or induced latch-up. Meanwhile, it is recommended to keep this contention as short as possible to limit extra power dissipation.

Figure 32. 3-Wire \(\overline{CS}\) Mode with Busy Indicator Connection Diagram (SDI High)

Figure 33. 3-Wire \(\overline{CS}\) Mode with Busy Indicator Serial Interface Timing (SDI High)