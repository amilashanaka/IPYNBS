from pynq import Overlay, MMIO
import time

# Load the overlay (bitstream) that includes the SPI IP
overlay = Overlay("spi.bit")

# Get the base address of the AXI Quad SPI IP block from the loaded overlay
spi_ip = overlay.ip_dict['axi_quad_spi_0']
spi_base_address = spi_ip['phys_addr']
spi_address_range = spi_ip['addr_range']

# Setup MMIO for AXI Quad SPI
spi_mmio = MMIO(spi_base_address, spi_address_range)

# SPI register offsets (replace if different from your configuration)
SPI_CTRL_REG = 0x00  # Control register
SPI_STATUS_REG = 0x04  # Status register
SPI_TXD_REG = 0x08  # Transmit data register
SPI_RXD_REG = 0x0C  # Receive data register

BUFFER_SIZE = 2  # Size of the SPI data buffer (2 bytes per transfer)
NUM_SAMPLES = 1000  # Number of samples to collect
SAMPLE_DELAY = 0.000005  # 5 microseconds delay between samples

# SPI initialization (mimicking SpiInit function in C)
def spi_init():
    # Set the SPI control register (Master mode, manual slave select)
    spi_mmio.write(SPI_CTRL_REG, 0x186)  # Set control options

# SPI transfer function (mimicking SpiTransfer function in C)
def spi_transfer(send_buffer, byte_count):
    recv_buffer = []
    for i in range(byte_count):
        # Wait for the SPI TX FIFO to be empty
        while not (spi_mmio.read(SPI_STATUS_REG) & 0x02):
            pass

        # Write data to the SPI transmit register
        spi_mmio.write(SPI_TXD_REG, send_buffer[i])

        # Wait for SPI RX FIFO to be full
        while not (spi_mmio.read(SPI_STATUS_REG) & 0x01):
            pass

        # Read data from the SPI receive register
        recv_buffer.append(spi_mmio.read(SPI_RXD_REG))

    return recv_buffer

# Main function to perform SPI transfers and collect samples
def main():
    spi_init()

    send_buffer = [0x00, 0x00]  # Command to send (dummy values)
    samples = []

    # Collect NUM_SAMPLES samples from the Pmod AD1 via SPI
    for i in range(NUM_SAMPLES):
        recv_buffer = spi_transfer(send_buffer, BUFFER_SIZE)

        # Convert received bytes to integer format (similar to C code)
        sample = (recv_buffer[0] << 8) | recv_buffer[1]
        samples.append(sample)

        # Delay to control the sampling rate
        time.sleep(SAMPLE_DELAY)

    # Print the collected samples (mimicking UART transmission)
    for sample in samples:
        print(sample)

# Run the main function
if __name__ == "__main__":
    main()
