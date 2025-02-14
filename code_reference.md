# PYNQ Code Reference

### By Don

##### Date : 16/10/2024

Making overlay 

```python
import pynq
from pynq import Overlay
from pynq import MMIO
import time
from operator import*
import matplotlib.pyplot as plt

# Load the SPI overlay
ol = Overlay("axispi.bit")
```

detect overlay ips

```python
print(ol.ip_dict)  # To view the IP block details
print(dir(spi_axi_ip))  # To view available attributes for the IP block
```

Making mmio object

```python
# Access the IP dictionary to find the address of the axi_quad_spi_0
spi_ip = ol.ip_dict['axi_quad_spi_0']
spi_base_address = (spi_ip['phys_addr'])
spi_address_range = (spi_ip['addr_range']) 

print(spi_base_address) 


#spi_base_address = 0x41E00000
#spi_address_range= 0x1000
# Set up MMIO for AXI Quad SPI
spi_mmio = MMIO(spi_address_range, spi_address_range)
spi_mmio.debug = True
```

Quad SPI

The Qspi documentaion : [Support Keyword Search (xilinx.com)](https://www.xilinx.com/search/support-keyword-search.html#q=AXI%20Quad%20SPI)

doc: [AMD Technical Information Portal](https://docs.amd.com/r/en-US/pg153-axi-quad-spi/SPI-Control-Register)

```python
import pynq
from pynq import Overlay
from pynq import MMIO
import time
from operator import*
import matplotlib.pyplot as plt

# Load the SPI overlay
ol = Overlay("spi.bit")
spi = ol.axi_quad_spi_0
```

init function 

```python
def init(spi, phase=0, polarity=0):
    spi.write(0x40, 0x0a)
    spi.write(0x28, 0x04)
    spi.write(0x1c, 0)
    spi.write(0x70, 0xFFFFFFFF)
    ctrlreg = spi.read(0x60)
    ctrlreg = ctrlreg | 0xe6
    spi.write(0x60, ctrlreg)
    ctrlreg = spi.read(0x60)
    ctrlreg = ctrlreg & ~(0x18) 
    if phase == 1:
        ctrlreg = ctrlreg | 0x10
    if polarity == 1:
        ctrlreg = ctrlreg | 0x08
    spi.write(0x60, ctrlreg)
```

Transfer function 

```python
def transfer(packet, spi):
    for data in packet:
        spi.write(0x68, data)
        spi.write(0x70, 0xFFFFFFFE)
        ctrlreg = spi.read(0x60)
        ctrlreg = ctrlreg & ~(0x100)
        spi.write(0x60, ctrlreg)
        statReg = spi.read(0x64)
        while (statReg & 0x04) == 0:
            statReg = spi.read(0x64)
        ctrlreg = spi.read(0x60)
        ctrlreg = ctrlreg | 0x100
        spi.write(0x60, ctrlreg)
    spi.write(0x70, 0xFFFFFFFF)
    recvData = list()
    RxFifoStatus = spi.read(0x64) & 0x01
    while RxFifoStatus == 0:
        temp = spi.read(0x6c)
        recvData.append(temp)
        RxFifoStatus = spi.read(0x64) & 0x01
    return recvData
```

Print Function 

```python
# Initialize SPI with correct phase/polarity for the ADC
init(spi, phase=1, polarity=1)  # Modify based on the ADC requirements

values_channel_0 = []  # List to store Channel 0 readings
for i in range(200):  # Increase the number of readings
    sendData = transfer([128+i, i*i+2], spi)  # Send dummy data
    recvData = transfer([0], spi)  # Read data (Channel 0)
    values_channel_0.append(recvData[0])  # Append the first received value
    time.sleep(0.01)  # Shorten delay for faster sampling




# Assuming a 12-bit ADC with 3.3V reference voltage
V_ref = 3.3
resolution = 4096  # 2^12 for 12-bit ADC

scaled_values = [value * V_ref /resolution for value in values_channel_0]

# Plot the scaled data
plt.plot(scaled_values)
plt.title('ADC Channel 0 Voltage Plot')
plt.xlabel('Reading Index')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.show()
```

# Date  23/10/2024

read from mimo

```python
print(spi_mmio.read(0x04))
```

-----

# Date 12/11/2024

```verilog
import pynq
from pynq import Overlay
from pynq import MMIO
import time
from operator import*
import matplotlib.pyplot as plt
import numpy as np
from pynq import allocate

# Load the SPI overlay
ol = Overlay("dma.bit")
```

data log 

![](C:\Users\don.gunasinha\AppData\Roaming\marktext\images\2024-12-10-16-00-39-image.png)
