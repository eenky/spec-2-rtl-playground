

THEORY OF OPERATION

![ADC Simplified Schematic](https://i.imgur.com/3Q5z5QG.png)

Figure 24. ADC Simplified Schematic

CIRCUIT INFORMATION

The AD7980 is a fast, low power, single-supply, precise 16-bit ADC that uses a successive approximation architecture.

The AD7980 is capable of converting 1,000,000 samples per second (1 MSPS) and powers down between conversions.
When operating at 10 kSPS, for example, it consumes 70 \( \mu \)W typically, ideal for battery-powered applications.

The AD7980 provides the user with on-chip track-and-hold and does not exhibit any pipeline delay or latency, making it ideal for multiple multiplexed channel applications.

The AD7980 can be interfaced to any 1.8 V to 5 V digital logic family. It is housed in a 10-lead MSOP or a tiny 10-lead LFCSP that combines space savings and allows flexible configurations.

It is pin-for-pin compatible with the 18-bit AD7982.

CONVERTER OPERATION

The AD7980 is a successive approximation ADC based on a charge redistribution DAC. Figure 24 shows the simplified schematic of the ADC. The capacitive DAC consists of two identical arrays of 16 binary weighted capacitors, which are connected to the two comparator inputs.

During the acquisition phase, terminals of the array tied to the input of the comparator are connected to GND via SW+ and SW–. All independent switches are connected to the analog inputs. Therefore, the capacitor arrays are used as sampling capacitors and acquire the analog signal on the IN+ and IN– inputs. When the acquisition phase is completed and the CNV input goes high, a conversion phase is initiated. When the conversion phase begins, SW+ and SW– are opened first. The two capacitor arrays are then disconnected from the inputs and connected to the GND input. Therefore, the differential voltage between the inputs IN+ and IN– captured at the end of the acquisition phase are applied to the comparator inputs, causing the comparator to become unbalanced. By switching each element of the capacitor array between GND and REF, the comparator input varies by binary weighted voltage steps (\( V_{REF}/2, V_{REF}/4 \ldots V_{REF}/65,536 \)). The control logic toggles these switches, starting with the MSB, to bring the comparator back into a balanced condition. After the completion of this process, the device returns to the acquisition phase and the control logic generates the ADC output code and a busy signal indicator.

Because the AD7980 has an on-board conversion clock, the serial clock, SCK, is not required for the conversion process.