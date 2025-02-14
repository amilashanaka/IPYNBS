
# coding: utf-8

# In[1]:


from pynq import Overlay

ol = Overlay("fdma.bit")


# In[4]:


dma = ol.axi_dma_0
dma_send = ol.axi_dma_0.sendchannel
dma_recv = ol.axi_dma_0.recvchannel


# In[5]:


from pynq import allocate
import numpy as np

data_size = 1000
input_buffer = allocate(shape=(data_size,), dtype=np.uint32)


# In[6]:


for i in range(data_size):
    input_buffer[i] = i + 0xcafe0000


# In[8]:


dma_send.transfer(input_buffer)


# In[9]:


output_buffer = allocate(shape=(data_size,), dtype=np.uint32)


# In[10]:


dma_recv.transfer(output_buffer)


# In[11]:


for i in range(10):
    print('0x' + format(output_buffer[i], '02x'))

