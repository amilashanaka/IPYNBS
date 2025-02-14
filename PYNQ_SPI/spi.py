from pynq import Overlay, MMIO

# Load the overlay (this should be the one that includes axi_quad_spi_0)
overlay = Overlay("spi.bit")

# Access the IP dictionary to find the address of the axi_quad_spi_0
spi_ip = overlay.ip_dict['axi_quad_spi_0']
spi_base_address = spi_ip['phys_addr']
spi_address_range = spi_ip['addr_range']

# Set up MMIO for AXI Quad SPI
spi_mmio = MMIO(spi_base_address, spi_address_range)

# SPI register offsets (these depend on the AXI Quad SPI IP configuration)
SPI_CTRL_REG = 0x00  # Control register
SPI_STATUS_REG = 0x04  # Status register
SPI_TXD_REG = 0x08  # Transmit data register
SPI_RXD_REG = 0x0C  # Receive data register

# SPI control parameters
SPI_MODE = 0b00  # SPI Mode 0 (CPOL = 0, CPHA = 0)
MAX_SPEED_HZ = 1000000  # 1 MHz (Adjust based on your requirements)

# Function to transfer data via SPI
def spi_transfer(ctrl_byte):
    """Write the control byte and receive the response byte via SPI."""
    
    # Wait for the SPI to be ready (TXFIFO Empty)
    while not (spi_mmio.read(SPI_STATUS_REG) & 0x02):
        pass

    # Write the control byte to the TXD register
    spi_mmio.write(SPI_TXD_REG, ctrl_byte)

    # Wait for the response to be available (RXFIFO Not Empty)
    while not (spi_mmio.read(SPI_STATUS_REG) & 0x01):
        pass

    # Read the received byte from the RXD register
    received_byte = spi_mmio.read(SPI_RXD_REG)
    
    return received_byte

# Function to read ADC data from Pmod AD1
def read_adc_data(channel):
    """Read 12-bit ADC data from the specified channel."""
    
    # Control byte to select channel (Channel 0 or 1)
    if channel == 0:
        ctrl_byte = 0b11010000  # Channel 0
    else:
        ctrl_byte = 0b11110000  # Channel 1

    # Send control byte and dummy bytes to read the ADC value
    spi_transfer(ctrl_byte)  # Send control byte
    byte_1 = spi_transfer(0x00)  # Read first byte
    byte_2 = spi_transfer(0x00)  # Read second byte

    # Combine the two bytes into a 12-bit ADC value
    adc_value = ((byte_1 & 0x0F) << 8) | byte_2

    return adc_value

# Example of reading ADC values from both channels of Pmod AD1
channel_0_value = read_adc_data(0)
channel_1_value = read_adc_data(1)

print(f"Channel 0 ADC Value: {channel_0_value}")
print(f"Channel 1 ADC Value: {channel_1_value}")
