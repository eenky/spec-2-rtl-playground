

3-WIRE CS MODE WITHOUT BUSY INDICATOR

This mode is usually used when a single AD7980 is connected to an SPI-compatible digital host. The connection diagram is shown in Figure 30, and the corresponding timing is given in Figure 31.

With SDI tied to VIO, a rising edge on CNV initiates a conversion, selects the CS mode, and forces SDO to high impedance. Once a conversion is initiated, it continues until completion irrespective of the state of CNV. This can be useful, for instance, to bring CNV low to select other SPI devices, such as analog multiplexers; however, CNV must be returned high before the minimum conversion time elapses and then held high for the maximum conversion time to avoid the generation of the busy signal indicator. When the conversion is complete, the AD7980 enters the acquisition phase and powers down.

When CNV goes low, the MSB is output onto SDO. The remaining data bits are then clocked by subsequent SCK falling edges. The data is valid on both SCK edges. Although the rising edge can be used to capture the data, a digital host using the SCK falling edge allows a faster reading rate provided that it has an acceptable hold time. After the 16th SCK falling edge or when CNV goes high, whichever is earlier, SDO returns to high impedance.

Figure 30. 3-Wire \(\overline{CS}\) Mode Without Busy Indicator Connection Diagram (SDI High)

Figure 31. 3-Wire \(\overline{CS}\) Mode Without Busy Indicator Serial Interface Timing (SDI High)