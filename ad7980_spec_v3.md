# Hardware Requirements: 3-Wire CS Mode With Busy Indicator

## 1. Interface Definition
### 1.1 External Device Interface (PHY)
(List ONLY pins physically present on the chip. Source: Pinout Table)

*   `cnv_i`: Convert Input (Active High)
*   `sck_i`: Serial Clock Input
*   `sdo_o`: Serial Data Output / Busy Indicator Output

### 1.2 FPGA System Interface (User Side)
(List clk_i, rstn_i, and data_o valid/ready handshaking signals)

*   `clk_i`: FPGA System Clock Input
*   `rstn_i`: FPGA System Reset Input (Active Low)
*   `start_i`: Start Conversion Input (Active High)
*   `data_o[15:0]`: Converted Data Output
*   `data_valid_o`: Data Valid Output (Active High)

## 2. Timing Constraints (REQT-TMG-xxx)

*   REQT-TMG-001: Throughput Rate max 833 kSPS
*   REQT-TMG-002: Conversion Time (`t_CONV`) min 500 ns
*   REQT-TMG-003: Conversion Time (`t_CONV`) max 800 ns
*   REQT-TMG-004: Acquisition Time (`t_ACQ`) min 290 ns
*   REQT-TMG-005: Time Between Conversions (`t_CYC`) min 1200 ns (1.2 us)
*   REQT-TMG-006: CNV Pulse Width (`t_CNVH`) min 10 ns
*   REQT-TMG-007: SCK Period (`t_SCK_CS_Mode`) min 22 ns
*   REQT-TMG-008: SCK Low Time (`t_SCKL`) min 6 ns
*   REQT-TMG-009: SCK High Time (`t_SCKH`) min 6 ns
*   REQT-TMG-010: SCK Falling Edge to Data Remains Valid (`t_HSDO`) min 3 ns
*   REQT-TMG-011: SCK Falling Edge to Data Valid Delay (`t_DSDO`) min 14 ns
*   REQT-TMG-012: SCK Falling Edge to Data Valid Delay (`t_DSDO`) typ 21 ns
*   REQT-TMG-013: CNV Low to SDO D15 MSB Valid (`t_EN`) min 18 ns
*   REQT-TMG-014: CNV Low to SDO D15 MSB Valid (`t_EN`) typ 40 ns
*   REQT-TMG-015: CNV High or Last SCK Falling Edge to SDO High Impedance (`t_DIS`) max 20 ns

## 3. Functional Logic (REQT-LOG-xxx)

*   REQT-LOG-001: The `sdi` pin of the AD7980 shall be tied to VIO (logic high) to enable 3-Wire CS Mode with Busy Indicator.
*   REQT-LOG-002: A rising edge on `cnv_i` shall initiate an analog-to-digital conversion and select the CS mode.
*   REQT-LOG-003: Upon the rising edge of `cnv_i`, the `sdo_o` pin shall transition to a High-Impedance state.
*   REQT-LOG-004: The `sdo_o` pin shall remain in a High-Impedance state for the duration of the conversion time (`t_CONV`).
*   REQT-LOG-005: Upon completion of the conversion (`t_CONV`), the `sdo_o` pin shall transition from High-Impedance to Logic Low, indicating the end of the conversion (Busy Indicator).
*   REQT-LOG-006: The transition of `sdo_o` from High-Impedance to Logic Low shall be used as an interrupt signal to the FPGA system, triggering the data readout sequence.
*   REQT-LOG-007: After the `sdo_o` pin goes low, subsequent falling edges of `sck_i` shall clock out the 16-bit conversion result, MSB (D15) first, on the `sdo_o` pin.
*   REQT-LOG-008: The `data_valid_o` signal shall be asserted by the FPGA system when the full 16-bit conversion result is available on `data_o`.
*   REQT-LOG-009: The `sdo_o` pin shall return to a High-Impedance state after the 17th falling edge of `sck_i` or when `cnv_i` goes high, whichever occurs first.
*   REQT-LOG-010: After the data readout, the AD7980 shall enter the acquisition phase and power down.

## 4. Architecture Strategy

The FPGA implementation shall consist of two main modules: a `ad7980_3wire_cs_busy_core` module and a `ad7980_3wire_cs_busy_wrapper` module.

*   **`ad7980_3wire_cs_busy_core`**: This module shall implement the core state machine logic for controlling the AD7980 in 3-Wire CS Mode with Busy Indicator. It will manage the `cnv_i` and `sck_i` signals, monitor the `sdo_o` for the busy indicator and data, and shift out the 16-bit conversion data. This module will operate in the FPGA system clock domain (`clk_i`).
*   **`ad7980_3wire_cs_busy_wrapper`**: This module shall instantiate the `ad7980_3wire_cs_busy_core` and handle the direct physical interface to the AD7980 pins. It will connect the FPGA system signals (`clk_i`, `rstn_i`, `start_i`, `data_o`, `data_valid_o`) to the `_core` module and the external PHY pins (`cnv_i`, `sck_i`, `sdo_o`) to the `_core` module.