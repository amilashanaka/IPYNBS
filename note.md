# PYNQ Introduction

Date 26/03/2024

By : Don 

------------

Fpga customize   hardware 

![](C:\Users\don.gunasinha\AppData\Roaming\marktext\images\2024-03-26-09-26-53-image.png)

1. pynq.io  - download image 

2. write 📝  sample programme 

3. run it in jupiter  notebook 

## Date : 02/04/2024

PYNQ overlay design 

visit : https://pynq.readthedocs.io/en/latest/overlay_design_methodology.html

An overlay consists of two main parts; the PL design (bitstream) and the project HWH file. Overlay design is a specialized task for hardware engineers. This section assumes the reader has some experience with digital design, building Zynq systems, and with the Vivado design tools.

## PL Design

The Xilinx® Vivado software is used to create a Zynq design. A *bitstream* or *binary* file (.bit file) will be generated that can be used to program the Zynq PL.

```cil
sudo pip3 install --upgrade --upgrade-strategy only-if-needed pynq
```

update pynq
