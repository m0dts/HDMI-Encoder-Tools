# HDMI-Encoder-Tools
Bits of code for the Brovotech(?) ON-DMI-16D HDMI Encoder box

Tested with Firmware verions:<br>
<br>1.96.200323 - Note line-in only works as mono input!!!
<br>1.60.190919

encoder.py is a python class which has a few functions to control the encoder, i'm using a raspberry pi as the logic control in GB3KM which this is all based on.

The older encoder_control.php is very basic but allows the functions required for the ADALM Pluto to configure the encoder over the network - just for reference.
