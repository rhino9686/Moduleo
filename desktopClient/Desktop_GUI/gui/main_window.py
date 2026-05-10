"""
Main Window for Moduelo Websocket Interface
CustomTkinter-based GUI with modern dark theme
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
import time
from typing import Optional
import websockets
import socket
import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor

from core.i2c_comm import I2CDriver, PSUCommunication, MockI2CDriver, MockPSUCommunication
from core.registers import REGISTERS, REGISTER_GROUPS, get_register_info, format_register_value, LinearDataFormat
from gui.register_panel import RegisterPanel
from gui.telemetry_panel import TelemetryPanel
from gui.control_panel import ControlPanel


class MainWindow(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Moduleo- Drone Interface")
        self.geometry("1300x800")
        
        # Initialize state
        self.i2c_driver: Optional[I2CDriver] = None
        self.psu_comm: Optional[PSUCommunication] = None
        self.is_connected = False
        self.auto_refresh = False
        self.refresh_rate = 1.0  # seconds
        
        # Build UI
        self._create_widgets()
        self._layout_widgets()
        
        # Start with mock mode for development
       ## self._init_mock_mode()
    
    def _create_widgets(self):
        """Create all UI widgets"""
        
        # Top toolbar frame
        self.toolbar_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        # Connection section
        self.conn_label = ctk.CTkLabel(
            self.toolbar_frame,
            text="IP Adress:",
            font=ctk.CTkFont(size=13)
        )
        
        self.port_entry = ctk.CTkEntry(
            self.toolbar_frame,
            placeholder_text="192.0.2.0/24",
            width=180
        )
        
        self.connect_btn = ctk.CTkButton(
            self.toolbar_frame,
            text="Connect",
            command=self._toggle_connection,
            width=100,
            fg_color="#2B7A0B",
            hover_color="#1F5A08"
        )
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            self.toolbar_frame,
            text="● Disconnected",
            font=ctk.CTkFont(size=13),
            text_color="#E53E3E"
        )
        
        # Auto refresh controls
        self.refresh_switch = ctk.CTkSwitch(
            self.toolbar_frame,
            text="Auto Refresh",
            command=self._toggle_auto_refresh,
            font=ctk.CTkFont(size=13)
        )
        
        self.refresh_rate_label = ctk.CTkLabel(
            self.toolbar_frame,
            text="Rate:",
            font=ctk.CTkFont(size=13)
        )
        
        self.refresh_rate_slider = ctk.CTkSlider(
            self.toolbar_frame,
            from_=0.5,
            to=5.0,
            number_of_steps=9,
            width=120,
            command=self._update_refresh_rate
        )
        self.refresh_rate_slider.set(1.0)
        
        self.refresh_rate_value = ctk.CTkLabel(
            self.toolbar_frame,
            text="1.0s",
            font=ctk.CTkFont(size=13),
            width=50
        )
        """
        # Mock mode toggle (for testing)
        self.mock_mode_switch = ctk.CTkSwitch(
            self.toolbar_frame,
            text="Mock Mode",
            font=ctk.CTkFont(size=13)
        )
        self.mock_mode_switch.select()
        """
        # Main content frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        # Left sidebar with control buttons
        self.sidebar = ctk.CTkFrame(self.main_frame, width=200)
        
        self.sidebar_label = ctk.CTkLabel(
            self.sidebar,
            text="Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        self.scan_btn = ctk.CTkButton(
            self.sidebar,
            text="Scan IP Addresses",
            command=self._scan_bus
        )
        
        self.clear_faults_btn = ctk.CTkButton(
            self.sidebar,
            text="Clear Faults",
            command=self._clear_faults
        )
        
        self.psu_on_btn = ctk.CTkButton(
            self.sidebar,
            text="PSU ON",
            command=lambda: self._set_operation(0x80),
            fg_color="#2B7A0B",
            hover_color="#1F5A08"
        )
        
        self.psu_off_btn = ctk.CTkButton(
            self.sidebar,
            text="PSU OFF",
            command=lambda: self._set_operation(0x00),
            fg_color="#C53030",
            hover_color="#9B2C2C"
        )
        
        # Tabview for different panels
        self.tabview = ctk.CTkTabview(self.main_frame)
        
        # Create tabs
        self.tabview.add("Registers")
        self.tabview.add("Telemetry")
        self.tabview.add("Control")
        
        # Register panel
        self.register_panel = RegisterPanel(
            self.tabview.tab("Registers"),
            self._read_register_callback,
            self._write_register_callback
        )
        
        # Telemetry panel
        self.telemetry_panel = TelemetryPanel(
            self.tabview.tab("Telemetry"),
            self._read_register_callback
        )
        
        # Control panel
        self.control_panel = ControlPanel(
            self.tabview.tab("Control"),
            self._read_register_callback,
            self._write_register_callback
        )
    
    def _layout_widgets(self):
        """Layout all widgets"""
        
        # Toolbar layout
        self.toolbar_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.conn_label.pack(side="left", padx=(0, 5))
        self.port_entry.pack(side="left", padx=(0, 10))
        self.connect_btn.pack(side="left", padx=(0, 15))
        self.status_label.pack(side="left", padx=(0, 30))
        
        self.refresh_switch.pack(side="left", padx=(0, 10))
        self.refresh_rate_label.pack(side="left", padx=(0, 5))
        self.refresh_rate_slider.pack(side="left", padx=(0, 5))
        self.refresh_rate_value.pack(side="left", padx=(0, 20))
        
       ## self.mock_mode_switch.pack(side="right")
        
        # Main content layout
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Sidebar layout
        self.sidebar.pack(side="left", fill="y", padx=(0, 15))
        self.sidebar.pack_propagate(False)
        
        self.sidebar_label.pack(pady=(20, 30))
        self.scan_btn.pack(pady=(0, 10), padx=15, fill="x")
        self.clear_faults_btn.pack(pady=(0, 10), padx=15, fill="x")
        self.psu_on_btn.pack(pady=(0, 10), padx=15, fill="x")
        self.psu_off_btn.pack(pady=(0, 10), padx=15, fill="x")
        
        # Tabview layout
        self.tabview.pack(side="left", fill="both", expand=True)
    
    def _init_mock_mode(self):
        """Initialize in mock mode for testing"""
        self.i2c_driver = MockI2CDriver()
        self.psu_comm = MockPSUCommunication(self.i2c_driver)
        
    def _toggle_connection(self):
        """Toggle websocket connection"""
        if self.is_connected:
            self._disconnect()
        else:
            self._connect()
    
    def _connect(self):
        """Connect to websocket device"""
        port = self.port_entry.get().strip()
        
        # Check if mock mode is enabled
        if False:
            self.i2c_driver = MockI2CDriver()
            self.psu_comm = MockPSUCommunication(self.i2c_driver)
            success = self.i2c_driver.connect("MOCK")
        else:
            if not port:
                messagebox.showerror("Error", "Please enter a valid port")
                return
            
            self.i2c_driver = I2CDriver()
            success = self.i2c_driver.connect(port)
            
            if success:
                self.psu_comm = PSUCommunication(self.i2c_driver)
        
        if False:
            self.is_connected = True
            self.connect_btn.configure(text="Disconnect", fg_color="#C53030", hover_color="#9B2C2C")
            self.status_label.configure(text="● Connected", text_color="#38A169")
            self.port_entry.configure(state="disabled")
        ##    self.mock_mode_switch.configure(state="disabled")
            
            # Read VOUT_MODE
            if self.psu_comm:
                self.psu_comm.read_vout_mode()
        else:
            messagebox.showerror("Connection Error", "Failed to connect to I2C device")
    
    def _disconnect(self):
        """Disconnect from I2C device"""
        if self.i2c_driver:
            self.i2c_driver.disconnect()
        
        self.is_connected = False
        self.auto_refresh = False
        self.refresh_switch.deselect()
        
        self.connect_btn.configure(text="Connect", fg_color="#2B7A0B", hover_color="#1F5A08")
        self.status_label.configure(text="● Disconnected", text_color="#E53E3E")
        self.port_entry.configure(state="normal")
     ##   self.mock_mode_switch.configure(state="normal")
    
    def _toggle_auto_refresh(self):
        """Toggle auto refresh"""
        self.auto_refresh = self.refresh_switch.get()
        
        if self.auto_refresh and self.is_connected:
            threading.Thread(target=self._auto_refresh_loop, daemon=True).start()
    
    def _auto_refresh_loop(self):
        """Auto refresh loop running in background thread"""
        while self.auto_refresh and self.is_connected:
            try:
                # Refresh telemetry panel
                self.after(0, self.telemetry_panel.refresh)
            except Exception as e:
                print(f"Auto refresh error: {e}")
            
            time.sleep(self.refresh_rate)
    
    def _update_refresh_rate(self, value):
        """Update refresh rate from slider"""
        self.refresh_rate = float(value)
        self.refresh_rate_value.configure(text=f"{self.refresh_rate:.1f}s")
    
    def _scan_bus(self):
        """Scan network for IP addresses """
        """if not self.is_connected:
            messagebox.showwarning("Not Connected", "Please connect to I2C device first")
            return"""
        
        devices = self._scan_IP()
        
        if devices:
            device_list = ", ".join([f"0x{addr:02X}" for addr in devices])
            messagebox.showinfo("IP Address Results", f"Found devices at:\n{device_list}")
        else:
            messagebox.showinfo("IP Address Results", "No devices found")
    
    def _clear_faults(self):
        """Send CLEAR_FAULTS command"""
        if not self.is_connected or not self.psu_comm:
            messagebox.showwarning("Not Connected", "Please connect to I2C device first")
            return
        
        if self.psu_comm.send_command(0x03):
            messagebox.showinfo("Success", "Faults cleared")
        else:
            messagebox.showerror("Error", "Failed to clear faults")
    
    def _set_operation(self, value):
        """Set OPERATION register"""
        if not self.is_connected or not self.psu_comm:
            messagebox.showwarning("Not Connected", "Please connect to I2C device first")
            return
        
        if self.psu_comm.write_register(0x01, value):
            state = "ON" if value == 0x80 else "OFF"
            messagebox.showinfo("Success", f"PSU turned {state}")
        else:
            messagebox.showerror("Error", "Failed to set operation state")
    
    def _read_register_callback(self, address, length=2):
        """Callback for reading registers"""
        if not self.is_connected or not self.psu_comm:
            return None
        
        reg_info = get_register_info(address)
        if reg_info and reg_info.get("type") == "block":
            return self.psu_comm.read_block(address)
        else:
            return self.psu_comm.read_register(address, length)
    
    def _write_register_callback(self, address, data):
        """Callback for writing registers"""
        if not self.is_connected or not self.psu_comm:
            return False
        
        return self.psu_comm.write_register(address, data)

    def _scan_network(self,base_ip, start, end, port=8765):
        print(f"Scanning {base_ip}.{start}-{end} on port {port}...")
        ips = [f"{base_ip}.{i}" for i in range(start, end + 1)]
        
        # Use 100 threads to scan many IPs at once
        with ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(lambda ip: self._check_port(ip, port,1), ips)
        
        active_hosts = [ip for ip in results if ip]
        return active_hosts


    def _scan_IP(self):
        ip_range =" 192.168.1.1/254"
        
        base_ip = "192.168.1"
        start = 1
        end = 254
        return self._scan_network(base_ip, start, end)
        # 1. Create an ARP request for the target range
        # 2. Wrap it in an Ethernet frame with the broadcast MAC
        """  arp_request = ARP(pdst=ip_range)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast / arp_request

        # 3. Send the packet and wait for responses
        # srp() is used for sending/receiving at Layer 2
        print(f"Scanning network: {ip_range}...")
        answered, _ = srp(packet, timeout=2, verbose=False)

        devices = []
        for sent, received in answered:
            # Extract IP and MAC from the response
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})"""
        
    def _check_port(self, ip, port, timeout=1):
        """Attempts a standard TCP connection to a specific port."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            # connect_ex returns 0 if the connection is successful
            result = s.connect_ex((ip, port))
            if result == 0:
                return ip
            return None

