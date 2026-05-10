"""
I2C Communication Handler for Power Supply
Uses i2cdriver library for USB-I2C interface
"""

import serial
import struct
import time
from typing import List, Optional, Union

class I2CDriver:
    """I2C Driver interface wrapper"""
    
    def __init__(self, port: str = None):
        """
        Initialize I2C Driver
        
        Args:
            port: Serial port for I2C driver (e.g., 'COM3' or '/dev/ttyUSB0')
        """
        self.port = port
        self.ser = None
        self.is_connected = False
        
    def connect(self, port: str = None) -> bool:
        """
        Connect to I2C driver
        
        Args:
            port: Serial port (overrides initialization port if provided)
            
        Returns:
            True if connection successful
        """
        if port:
            self.port = port
            
        if not self.port:
            raise ValueError("No port specified")
        
        try:
            # Open serial connection at 1Mbaud
            self.ser = serial.Serial(self.port, baudrate=1000000, timeout=1)
            
            # Send 'e' command to echo and verify connection
            self.ser.write(b'e')
            response = self.ser.read(1)
            
            if response == b'e':
                self.is_connected = True
                # Initialize I2C bus with default settings
                self._initialize()
                return True
            else:
                self.ser.close()
                self.ser = None
                return False
                
        except Exception as e:
            print(f"Connection error: {e}")
            if self.ser:
                self.ser.close()
                self.ser = None
            return False
    
    def disconnect(self):
        """Disconnect from I2C driver"""
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.ser = None
        self.is_connected = False
    
    def _initialize(self):
        """Initialize I2C bus to default state"""
        if not self.ser:
            return
        
        # Set speed to 100kHz (suitable for PMBus)
        # Command 'c' sets speed, followed by speed code
        # Speed codes: 1=100kHz, 2=400kHz, 3=1MHz
        self.ser.write(b'c\x01')
        
    def start(self, address: int, read: bool = False) -> bool:
        """
        Send I2C start condition and address
        
        Args:
            address: 7-bit I2C address
            read: True for read operation, False for write
            
        Returns:
            True if ACK received
        """
        if not self.is_connected:
            return False
        
        # Start condition command 's'
        self.ser.write(b's')
        
        # Send address byte (bit 0 is R/W)
        addr_byte = (address << 1) | (1 if read else 0)
        self.ser.write(bytes([addr_byte]))
        
        # Wait for ACK/NAK (1 byte response: 0=ACK, 1=NAK)
        ack = self.ser.read(1)
        return ack == b'\x00'
    
    def stop(self):
        """Send I2C stop condition"""
        if self.is_connected:
            self.ser.write(b'p')
    
    def write_byte(self, data: int) -> bool:
        """
        Write a single byte
        
        Args:
            data: Byte to write
            
        Returns:
            True if ACK received
        """
        if not self.is_connected:
            return False
        
        self.ser.write(bytes([data]))
        ack = self.ser.read(1)
        return ack == b'\x00'
    
    def read_byte(self, ack: bool = True) -> int:
        """
        Read a single byte
        
        Args:
            ack: Send ACK after read (False = NAK for last byte)
            
        Returns:
            Byte value read
        """
        if not self.is_connected:
            return 0
        
        # Read command with ACK/NAK
        if ack:
            self.ser.write(b'r')  # Read with ACK
        else:
            self.ser.write(b'n')  # Read with NAK
        
        return ord(self.ser.read(1))
    
    def scan(self) -> List[int]:
        """
        Scan I2C bus for devices
        
        Returns:
            List of 7-bit addresses that responded
        """
        devices = []
        
        if not self.is_connected:
            return devices
        
        for addr in range(0x08, 0x78):
            if self.start(addr, False):
                devices.append(addr)
            self.stop()
            time.sleep(0.01)
        
        return devices


class PSUCommunication:
    """Power Supply Unit communication handler"""
    
    def __init__(self, i2c_driver: I2CDriver, psu_address: int = 0xB0):
        """
        Initialize PSU communication
        
        Args:
            i2c_driver: I2CDriver instance
            psu_address: PSU I2C address (default 0xB0 for microcontroller)
        """
        self.driver = i2c_driver
        self.psu_address = psu_address >> 1  # Convert to 7-bit
        self.vout_mode = 0x17  # Default VOUT_MODE value
        
    def read_register(self, command: int, length: int = 2) -> Optional[List[int]]:
        """
        Read register from PSU using PMBus protocol
        
        Args:
            command: Command/register address
            length: Number of bytes to read
            
        Returns:
            List of bytes read, or None on error
        """
        if not self.driver.is_connected:
            return None
        
        try:
            # Write command code
            if not self.driver.start(self.psu_address, False):
                self.driver.stop()
                return None
            
            if not self.driver.write_byte(command):
                self.driver.stop()
                return None
            
            # Repeated start for read
            if not self.driver.start(self.psu_address, True):
                self.driver.stop()
                return None
            
            # Read data bytes
            data = []
            for i in range(length):
                # Send ACK for all but last byte
                byte = self.driver.read_byte(ack=(i < length - 1))
                data.append(byte)
            
            self.driver.stop()
            return data
            
        except Exception as e:
            print(f"Read error: {e}")
            self.driver.stop()
            return None
    
    def write_register(self, command: int, data: Union[int, List[int]]) -> bool:
        """
        Write register to PSU using PMBus protocol
        
        Args:
            command: Command/register address
            data: Single byte or list of bytes to write
            
        Returns:
            True if write successful
        """
        if not self.driver.is_connected:
            return False
        
        # Convert single int to list
        if isinstance(data, int):
            data = [data]
        
        try:
            # Start with write address
            if not self.driver.start(self.psu_address, False):
                self.driver.stop()
                return False
            
            # Write command code
            if not self.driver.write_byte(command):
                self.driver.stop()
                return False
            
            # Write data bytes
            for byte in data:
                if not self.driver.write_byte(byte):
                    self.driver.stop()
                    return False
            
            self.driver.stop()
            return True
            
        except Exception as e:
            print(f"Write error: {e}")
            self.driver.stop()
            return False
    
    def read_block(self, command: int) -> Optional[bytes]:
        """
        Read block data (SMBus block read protocol)
        
        Args:
            command: Command/register address
            
        Returns:
            Bytes read, or None on error
        """
        if not self.driver.is_connected:
            return None
        
        try:
            # Write command
            if not self.driver.start(self.psu_address, False):
                self.driver.stop()
                return None
            
            if not self.driver.write_byte(command):
                self.driver.stop()
                return None
            
            # Repeated start for read
            if not self.driver.start(self.psu_address, True):
                self.driver.stop()
                return None
            
            # First byte is length
            length = self.driver.read_byte(ack=True)
            
            # Read data bytes
            data = []
            for i in range(length):
                byte = self.driver.read_byte(ack=(i < length - 1))
                data.append(byte)
            
            self.driver.stop()
            return bytes(data)
            
        except Exception as e:
            print(f"Block read error: {e}")
            self.driver.stop()
            return None
    
    def send_command(self, command: int) -> bool:
        """
        Send command without data (e.g., CLEAR_FAULTS)
        
        Args:
            command: Command code
            
        Returns:
            True if successful
        """
        if not self.driver.is_connected:
            return False
        
        try:
            if not self.driver.start(self.psu_address, False):
                self.driver.stop()
                return False
            
            success = self.driver.write_byte(command)
            self.driver.stop()
            return success
            
        except Exception as e:
            print(f"Command error: {e}")
            self.driver.stop()
            return False
    
    def read_vout_mode(self) -> int:
        """Read and cache VOUT_MODE register"""
        result = self.read_register(0x20, 1)
        if result:
            self.vout_mode = result[0]
        return self.vout_mode
    
    def get_vout_mode(self) -> int:
        """Get cached VOUT_MODE value"""
        return self.vout_mode


class MockI2CDriver:
    """Mock I2C Driver for testing without hardware"""
    
    def __init__(self, port: str = None):
        self.port = port
        self.is_connected = False
        self.registers = {}  # Mock register storage
        
    def connect(self, port: str = None) -> bool:
        """Simulate connection"""
        if port:
            self.port = port
        self.is_connected = True
        self._init_mock_data()
        return True
    
    def disconnect(self):
        """Simulate disconnection"""
        self.is_connected = False
    
    def _init_mock_data(self):
        """Initialize mock register values"""
        # Simulate some typical values
        self.registers = {
            0x01: [0x80],  # OPERATION = ON
            0x20: [0x17],  # VOUT_MODE
            0x79: [0x00, 0x00],  # STATUS_WORD
            0x88: [0x00, 0x1C],  # READ_VIN ~230V
            0x8B: [0x00, 0x0C],  # READ_VOUT ~12V
            0x8C: [0x00, 0x64],  # READ_IOUT ~100A
            0x8D: [0x00, 0x19],  # READ_TEMP_1 ~25C
            0x90: [0x00, 0x1F],  # FAN_SPEED ~8000 RPM
            0x96: [0x00, 0x4B],  # READ_POUT ~1200W
            0x98: [0x22],  # PMBUS_REVISION
        }
    
    def start(self, address: int, read: bool = False) -> bool:
        return self.is_connected
    
    def stop(self):
        pass
    
    def write_byte(self, data: int) -> bool:
        return self.is_connected
    
    def read_byte(self, ack: bool = True) -> int:
        return 0
    
    def scan(self) -> List[int]:
        if self.is_connected:
            return [0x50, 0x58]  # Mock EEPROM and PSU addresses
        return []


class MockPSUCommunication(PSUCommunication):
    """Mock PSU communication for testing"""
    
    def read_register(self, command: int, length: int = 2) -> Optional[List[int]]:
        if not self.driver.is_connected:
            return None
        
        if hasattr(self.driver, 'registers'):
            return self.driver.registers.get(command, [0] * length)
        return [0] * length
    
    def write_register(self, command: int, data: Union[int, List[int]]) -> bool:
        if not self.driver.is_connected:
            return False
        
        if hasattr(self.driver, 'registers'):
            if isinstance(data, int):
                data = [data]
            self.driver.registers[command] = data
        return True
    
    def read_block(self, command: int) -> Optional[bytes]:
        if not self.driver.is_connected:
            return None
        
        # Return mock block data
        if command == 0x99:  # MFR_ID
            return b"QCS"
        elif command == 0x9A:  # MFR_MODEL
            return b"JPSU-3000W-AC-AFO"
        elif command == 0xF6:  # FW_VERSION
            return b"\x04\x00\x02\x05\x02"
        return b"MOCK"
    
    def send_command(self, command: int) -> bool:
        return self.driver.is_connected
