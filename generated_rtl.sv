
// ad7980_3wire_cs_busy_core.sv
//
// SystemVerilog RTL for AD7980 ADC in 3-Wire CS Mode with Busy Indicator.
// This module acts as the controller (FPGA is master).
//
// Features:
// - Initiates conversion via CNV pulse.
// - Waits for busy indicator (SDO goes low).
// - Clocks out 16-bit data via SCLK, sampling SDO.
// - Provides a simple valid/ready user interface.
// - Includes SystemVerilog Assertions (SVA) for critical timing constraints.
//
// Naming Conventions:
// - FPGA outputs to AD7980 are suffixed with _o.
// - FPGA inputs from AD7980 are suffixed with _i.
// - System signals: clk_i, rstn_i.
// - User interface: start_conversion_i, data_o, data_valid_o.
//
// Architectural Pattern:
// - ad7980_3wire_cs_busy_core: Contains the FSM and timing logic.
// - ad7980_3wire_cs_busy_wrapper: Top-level instantiation, handles I/O.

module ad7980_3wire_cs_busy_core #(
  parameter CLK_PERIOD_NS = 10, // System clock period in ns (e.g., 10 for 100MHz)
  parameter DATA_WIDTH    = 16  // AD7980 data width is 16 bits
) (
  input  logic        clk_i,
  input  logic        rstn_i,

  // User Interface
  input  logic        start_conversion_i, // Strobe to initiate a conversion
  output logic [DATA_WIDTH-1:0] data_o,             // Output converted data
  output logic        data_valid_o,         // Strobe indicating data_o is valid

  // AD7980 Interface (FPGA perspective)
  output logic        cnv_o,  // Convert/Chip Select (FPGA drives this)
  output logic        sclk_o, // Serial Clock (FPGA drives this)
  input  logic        sdo_i   // Serial Data Output (FPGA reads this)
);

  // Internal Signals
  logic        cnv_reg;
  logic        sclk_reg;
  logic [4:0]  sclk_cnt;  // Counter for SCLK generation (up to 16 bits + setup)
  logic [7:0]  timer_cnt; // General purpose timer (e.g., for t_CONV, t_CYC)
  logic [DATA_WIDTH-1:0] sdo_data_reg;
  logic [4:0]  bit_cnt;   // Counter for data bits during readout

  // State Machine
  typedef enum logic [2:0] {
    IDLE,              // Waiting for a conversion request
    PULSE_CNV,         // Generating the CNV pulse
    WAIT_CONVERSION,   // Waiting for the ADC conversion to complete (busy indicator)
    READ_DATA,         // Clocking out the converted data
    END_CYCLE          // Ensuring minimum cycle time between conversions
  } state_e;

  state_e current_state, next_state;

  // Parameters for timing based on CLK_PERIOD_NS
  // These calculations ensure that the minimum timing requirements from the datasheet are met.
  localparam CNV_PULSE_CYCLES = (10 + CLK_PERIOD_NS - 1) / CLK_PERIOD_NS; // t_CNVH min 10ns
  localparam CONV_TIME_CYCLES = (500 + CLK_PERIOD_NS - 1) / CLK_PERIOD_NS; // t_CONV min 500ns
  localparam SCLK_MIN_HIGH_CYCLES = (6 + CLK_PERIOD_NS - 1) / CLK_PERIOD_NS; // t_SCKH min 6ns
  localparam SCLK_MIN_LOW_CYCLES  = (6 + CLK_PERIOD_NS - 1) / CLK_PERIOD_NS; // t_SCKL min 6ns
  localparam SCLK_MIN_PERIOD_CYCLES = (22 + CLK_PERIOD_NS - 1) / CLK_PERIOD_NS; // t_SCK min 22ns

  // Calculate SCLK_HIGH_CYCLES and SCLK_LOW_CYCLES to meet all minimums
  // Ensure SCLK_PERIOD_CYCLES is at least SCLK_MIN_PERIOD_CYCLES
  // And SCLK_HIGH_CYCLES >= SCLK_MIN_HIGH_CYCLES, SCLK_LOW_CYCLES >= SCLK_MIN_LOW_CYCLES
  localparam SCLK_HIGH_CYCLES_TEMP = (SCLK_MIN_HIGH_CYCLES > SCLK_MIN_PERIOD_CYCLES / 2) ? SCLK_MIN_HIGH_CYCLES : (SCLK_MIN_PERIOD_CYCLES / 2);
  localparam SCLK_LOW_CYCLES_TEMP  = (SCLK_MIN_LOW_CYCLES > SCLK_MIN_PERIOD_CYCLES - SCLK_HIGH_CYCLES_TEMP) ? SCLK_MIN_LOW_CYCLES : (SCLK_MIN_PERIOD_CYCLES - SCLK_HIGH_CYCLES_TEMP);

  localparam SCLK_HIGH_CYCLES = SCLK_HIGH_CYCLES_TEMP;
  localparam SCLK_LOW_CYCLES  = SCLK_LOW_CYCLES_TEMP;
  localparam SCLK_PERIOD_CYCLES = SCLK_HIGH_CYCLES + SCLK_LOW_CYCLES;

  localparam CYCLE_TIME_CYCLES = (1200 + CLK_PERIOD_NS - 1) / CLK_PERIOD_NS; // t_CYC min 1.2us

  // State Register and Output Logic
  always_ff @(posedge clk_i or negedge rstn_i) begin
    if (!rstn_i) begin
      current_state <= IDLE;
      cnv_reg       <= 1'b0;
      sclk_reg      <= 1'b0;
      timer_cnt     <= '0;
      sclk_cnt      <= '0;
      bit_cnt       <= '0;
      sdo_data_reg  <= '0;
      data_valid_o  <= 1'b0;
      data_o        <= '0;
    end else begin
      current_state <= next_state;
      data_valid_o  <= 1'b0; // Default to low, set high only when valid

      case (current_state)
        IDLE: begin
          cnv_reg  <= 1'b0;
          sclk_reg <= 1'b0;
          timer_cnt <= '0;
          sclk_cnt <= '0;
          bit_cnt  <= '0;
          if (start_conversion_i) begin
            next_state <= PULSE_CNV;
          end else begin
            next_state <= IDLE;
          end
        end

        PULSE_CNV: begin
          cnv_reg <= 1'b1; // Drive CNV high
          if (timer_cnt == CNV_PULSE_CYCLES - 1) begin
            cnv_reg <= 1'b0; // CNV goes low after pulse
            timer_cnt <= '0;
            next_state <= WAIT_CONVERSION;
          end else begin
            timer_cnt <= timer_cnt + 1;
            next_state <= PULSE_CNV;
          end
        end

        WAIT_CONVERSION: begin
          // CNV is low here. SDI is assumed to be tied high externally.
          // Wait for t_CONV (min 500ns) and SDO to go low (busy indicator).
          if (timer_cnt < CONV_TIME_CYCLES - 1) begin
            timer_cnt <= timer_cnt + 1;
            next_state <= WAIT_CONVERSION;
          end else if (sdo_i == 1'b0) begin // SDO goes low, conversion complete
            timer_cnt <= '0;
            bit_cnt <= '0; // Reset bit counter for data readout
            next_state <= READ_DATA;
          end else begin
            // Still waiting for SDO to go low after min CONV_TIME_CYCLES
            next_state <= WAIT_CONVERSION;
          end
        end

        READ_DATA: begin
          cnv_reg <= 1'b0; // Keep CNV low during data readout

          // Generate SCLK
          if (sclk_cnt == SCLK_PERIOD_CYCLES - 1) begin
            sclk_cnt <= '0;
            sclk_reg <= ~sclk_reg; // Toggle SCLK
          end else begin
            sclk_cnt <= sclk_cnt + 1;
          end

          // Sample SDO when SCLK is high (middle of SCLK high period)
          // Data is driven by AD7980 on SCK falling edge and is stable when SCK is high.
          if (sclk_reg == 1'b1 && sclk_cnt == (SCLK_HIGH_CYCLES / 2)) begin
            sdo_data_reg <= {sdo_data_reg[DATA_WIDTH-2:0], sdo_i};
            bit_cnt <= bit_cnt + 1;
            if (bit_cnt == DATA_WIDTH - 1) begin // All bits received
              data_o <= {sdo_data_reg[DATA_WIDTH-2:0], sdo_i}; // Capture last bit
              data_valid_o <= 1'b1;
              timer_cnt <= '0; // Reset timer for END_CYCLE
              next_state <= END_CYCLE;
            end else begin
              next_state <= READ_DATA;
            end
          end else begin
            next_state <= READ_DATA;
          end
        end

        END_CYCLE: begin
          cnv_reg <= 1'b0;
          sclk_reg <= 1'b0; // Ensure SCLK is low
          if (timer_cnt == CYCLE_TIME_CYCLES - 1) begin
            timer_cnt <= '0;
            next_state <= IDLE;
          end else begin
            timer_cnt <= timer_cnt + 1;
            next_state <= END_CYCLE;
          end
        end

        default: next_state <= IDLE;
      endcase
    end
  end

  // Assign outputs
  assign cnv_o  = cnv_reg;
  assign sclk_o = sclk_reg;

  // SystemVerilog Assertions (SVA) for timing constraints
  // These assertions help verify that the generated signals meet the AD7980's requirements.

  // t_CNVH: CNV Pulse Width (CS Mode) min 10 ns
  property p_t_CNVH;
    @(posedge clk_i) disable iff (!rstn_i)
    (current_state == PULSE_CNV && cnv_o == 1'b1) |=> (timer_cnt >= CNV_PULSE_CYCLES - 1);
  endproperty
  assert property (p_t_CNVH) else $error("AD7980_3WIRE_CS_BUSY: t_CNVH (CNV Pulse Width) violation!");

  // t_SCK: SCK Period (CS Mode) min 22 ns
  property p_t_SCK_period;
    @(posedge clk_i) disable iff (!rstn_i)
    (current_state == READ_DATA && sclk_reg == 1'b1 && sclk_cnt == SCLK_HIGH_CYCLES - 1) |->
    (##[SCLK_LOW_CYCLES] sclk_reg == 1'b0 && ##[SCLK_HIGH_CYCLES] sclk_reg == 1'b1);
  endproperty
  assert property (p_t_SCK_period) else $error("AD7980_3WIRE_CS_BUSY: t_SCK (SCK Period) violation!");

  // t_SCKL: SCK Low Time min 6 ns
  property p_t_SCKL;
    @(posedge clk_i) disable iff (!rstn_i)
    (current_state == READ_DATA && sclk_reg == 1'b0 && sclk_cnt == SCLK_HIGH_CYCLES) |->
    (##[SCLK_LOW_CYCLES - 1] sclk_reg == 1'b0);
  endproperty
  assert property (p_t_SCKL) else $error("AD7980_3WIRE_CS_BUSY: t_SCKL (SCK Low Time) violation!");

  // t_SCKH: SCK High Time min 6 ns
  property p_t_SCKH;
    @(posedge clk_i) disable iff (!rstn_i)
    (current_state == READ_DATA && sclk_reg == 1'b1 && sclk_cnt == 0) |->
    (##[SCLK_HIGH_CYCLES - 1] sclk_reg == 1'b1);
  endproperty
  assert property (p_t_SCKH) else $error("AD7980_3WIRE_CS_BUSY: t_SCKH (SCK High Time) violation!");

  // t_CONV: Conversion Time min 500 ns
  // Asserts that SDO goes low (busy indicator) after the minimum conversion time.
  property p_t_CONV;
    @(posedge clk_i) disable iff (!rstn_i)
    (current_state == WAIT_CONVERSION && timer_cnt == CONV_TIME_CYCLES - 1) |=> (sdo_i == 1'b0);
  endproperty
  assert property (p_t_CONV) else $error("AD7980_3WIRE_CS_BUSY: t_CONV (Conversion Time) violation! SDO did not go low after min conversion time.");

  // t_CYC: Time Between Conversions min 1.2 us
  property p_t_CYC;
    @(posedge clk_i) disable iff (!rstn_i)
    (current_state == END_CYCLE && timer_cnt == CYCLE_TIME_CYCLES - 1) |=> (next_state == IDLE);
  endproperty
  assert property (p_t_CYC) else $error("AD7980_3WIRE_CS_BUSY: t_CYC (Cycle Time) violation!");

endmodule


// ad7980_3wire_cs_busy_wrapper.sv
//
// Wrapper module for the AD7980 3-Wire CS Mode with Busy Indicator core.
// This module instantiates the core and provides the top-level interface.
// No special I/O buffers are typically needed for this configuration as all signals
// are either dedicated inputs or outputs from the FPGA perspective.
// SDI is assumed to be tied high externally on the PCB.

module ad7980_3wire_cs_busy_wrapper #(
  parameter CLK_PERIOD_NS = 10, // System clock period in ns (e.g., 10 for 100MHz)
  parameter DATA_WIDTH    = 16  // AD7980 data width is 16 bits
) (
  input  logic        clk_i,
  input  logic        rstn_i,

  // User Interface
  input  logic        start_conversion_i,
  output logic [DATA_WIDTH-1:0] data_o,
  output logic        data_valid_o,

  // AD7980 Interface
  output logic        cnv_o,
  output logic        sclk_o,
  input  logic        sdo_i
);

  // Instantiate the core module
  ad7980_3wire_cs_busy_core #(
    .CLK_PERIOD_NS (CLK_PERIOD_NS),
    .DATA_WIDTH    (DATA_WIDTH)
  ) i_ad7980_core (
    .clk_i              (clk_i),
    .rstn_i             (rstn_i),
    .start_conversion_i (start_conversion_i),
    .data_o             (data_o),
    .data_valid_o       (data_valid_o),
    .cnv_o              (cnv_o),
    .sclk_o             (sclk_o),
    .sdo_i              (sdo_i)
  );

  // No special I/O buffers (e.g., IOBUF for bidirectional signals) are required
  // for this 3-wire CS mode with busy indicator, as all AD7980 interface pins
  // are either inputs or outputs from the FPGA's perspective.
  // The AD7980's SDI pin is specified to be tied high externally in this mode.

endmodule