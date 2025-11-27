

APPLICATIONS INFORMATION

LAYOUT
The printed circuit board (PCB) that houses the AD7980 should be designed so that the analog and digital sections are separated and confined to certain areas of the board. The pinout of the AD7980, with all its analog signals on the left side and all its digital signals on the right side, eases this task.

Avoid running digital lines under the device because these couple noise onto the die, unless a ground plane under the AD7980 is used as a shield. Fast switching signals, such as CNV or clocks, should never run near analog signal paths. Crossover of digital and analog signals should be avoided.

At least one ground plane should be used. The ground plane can be common or split between the digital and analog section. In the latter case, the planes should be joined underneath the AD7980 devices.

The AD7980 voltage reference input REF has a dynamic input impedance and should be decoupled with minimal parasitic inductances. This is done by placing the reference decoupling ceramic capacitor close to, ideally right up against, the REF and GND pins and connecting them with wide, low impedance traces.

Finally, the power supplies VDD and VIO of the AD7980 should be decoupled with ceramic capacitors, typically 100 nF, placed close to the AD7980 and connected using short and wide traces to provide low impedance paths and reduce the effect of glitches on the power supply lines.

An example of a layout following these rules is shown in Figure 42 and Figure 43.

EVALUATING THE PERFORMANCE OF THE AD7980
Other recommended layouts for the AD7980 are outlined in the documentation of the evaluation board for the AD7980 (EVAL-AD7980SDZ). The evaluation board package includes a fully assembled and tested evaluation board, documentation, and software for controlling the board from a PC via the EVAL-SDP-CB1Z.