

TERMINOLOGY

Integral Nonlinearity Error (INL)
INL refers to the deviation of each individual code from a line drawn from negative full scale through positive full scale. The point used as negative full scale occurs ½ LSB before the first code transition. Positive full scale is defined as a level 1½ LSB beyond the last code transition. The deviation is measured from the middle of each code to the true straight line (see Figure 25).

Differential Nonlinearity Error (DNL)
In an ideal ADC, code transitions are 1 LSB apart. DNL is the maximum deviation from this ideal value. It is often specified in terms of resolution for which no missing codes are guaranteed.

Offset Error
The first transition should occur at a level ½ LSB above analog ground (38.1 μV for the 0 V to 5 V range). The offset error is the deviation of the actual transition from that point.

Gain Error
The last transition (from 111 ... 10 to 111 ... 11) should occur for an analog voltage 1½ LSB below the nominal full scale (4.999886 V for the 0 V to 5 V range). The gain error is the deviation of the actual level of the last transition from the ideal level after the offset is adjusted out.

Spurious-Free Dynamic Range (SFDR)
SFDR is the difference, in decibels (dB), between the rms amplitude of the input signal and the peak spurious signal.

Effective Number of Bits (ENOB)
ENOB is a measurement of the resolution with a sine wave input. It is expressed in bits and related to SINAD by the following formula:

\[
ENOB = (SINAD_{dB} - 1.76)/6.02
\]

Noise-Free Code Resolution
Noise-free code resolution is the number of bits beyond which it is impossible to distinctly resolve individual codes. It is calculated as

\[
Noise-Free\ Code\ Resolution = \log_2(2^N/Peak-to-Peak\ Noise)
\]

and is expressed in bits.

Effective Resolution
Effective resolution is calculated as

\[
Effective\ Resolution = \log_2(2^N/RMS\ Input\ Noise)
\]

and is expressed in bits.

Total Harmonic Distortion (THD)
THD is the ratio of the rms sum of the first five harmonic components to the rms value of a full-scale input signal and is expressed in dB.

Dynamic Range
Dynamic range is the ratio of the rms value of the full scale to the total rms noise measured with the inputs shorted together. The value for dynamic range is expressed in dB. It is measured with a signal at –60 dBFS to include all noise sources and DNL artifacts.

Signal-to-Noise Ratio (SNR)
SNR is the ratio of the rms value of the actual input signal to the rms sum of all other spectral components below the Nyquist frequency, excluding harmonics and dc. The value for SNR is expressed in dB.

Signal-to-Noise-and-Distortion Ratio (SINAD)
SINAD is the ratio of the rms value of the actual input signal to the rms sum of all other spectral components below the Nyquist frequency, including harmonics but excluding dc. The value for SINAD is expressed in dB.

Aperture Delay
Aperture delay is the measure of the acquisition performance. It is the time between the rising edge of the CNV input and when the input signal is held for a conversion.

Transient Response
Transient response is the time required for the ADC to accurately acquire its input after a full-scale step function is applied.