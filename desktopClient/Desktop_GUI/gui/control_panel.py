"""
Control Panel - Power supply control and configuration
"""

import customtkinter as ctk
from tkinter import messagebox
from core.registers import LinearDataFormat


class ControlPanel(ctk.CTkFrame):
    """Panel for PSU control functions"""
    
    def __init__(self, parent, read_callback, write_callback):
        super().__init__(parent, fg_color="transparent")
        
        self.read_callback = read_callback
        self.write_callback = write_callback
        
        self._create_widgets()
        self._layout_widgets()
    
    def _create_widgets(self):
        """Create control widgets"""
        
        # Operation control
        self.operation_frame = ctk.CTkFrame(self)
        self.operation_label = ctk.CTkLabel(
            self.operation_frame,
            text="Operation Control",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        self.operation_status = ctk.CTkLabel(
            self.operation_frame,
            text="Status: Unknown",
            font=ctk.CTkFont(size=14)
        )
        
        self.btn_frame = ctk.CTkFrame(self.operation_frame, fg_color="transparent")
        
        self.psu_on_btn = ctk.CTkButton(
            self.btn_frame,
            text="Turn ON",
            command=lambda: self._set_operation(0x80),
            width=150,
            height=50,
            font=ctk.CTkFont(size=14),
            fg_color="#2B7A0B",
            hover_color="#1F5A08"
        )
        
        self.psu_off_btn = ctk.CTkButton(
            self.btn_frame,
            text="Turn OFF",
            command=lambda: self._set_operation(0x00),
            width=150,
            height=50,
            font=ctk.CTkFont(size=14),
            fg_color="#C53030",
            hover_color="#9B2C2C"
        )
        
        self.read_operation_btn = ctk.CTkButton(
            self.operation_frame,
            text="Read Status",
            command=self._read_operation_status,
            width=150
        )
        
        # Fan control
        self.fan_frame = ctk.CTkFrame(self)
        self.fan_label = ctk.CTkLabel(
            self.fan_frame,
            text="Fan Control",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        self.fan_mode_label = ctk.CTkLabel(
            self.fan_frame,
            text="Fan Mode:",
            font=ctk.CTkFont(size=13)
        )
        
        self.fan_mode_value = ctk.CTkLabel(
            self.fan_frame,
            text="Unknown",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        
        self.fan_speed_label = ctk.CTkLabel(
            self.fan_frame,
            text="Current Speed:",
            font=ctk.CTkFont(size=13)
        )
        
        self.fan_speed_value = ctk.CTkLabel(
            self.fan_frame,
            text="--",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        
        self.fan_offset_label = ctk.CTkLabel(
            self.fan_frame,
            text="Fan Offset (RPM):",
            font=ctk.CTkFont(size=13)
        )
        
        self.fan_offset_entry = ctk.CTkEntry(
            self.fan_frame,
            placeholder_text="0-10000",
            width=150
        )
        
        self.set_fan_offset_btn = ctk.CTkButton(
            self.fan_frame,
            text="Set Fan Offset",
            command=self._set_fan_offset,
            width=150
        )
        
        self.read_fan_btn = ctk.CTkButton(
            self.fan_frame,
            text="Read Fan Status",
            command=self._read_fan_status,
            width=150
        )
        
        # Health check
        self.health_frame = ctk.CTkFrame(self)
        self.health_label = ctk.CTkLabel(
            self.health_frame,
            text="Health Check",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        self.health_status = ctk.CTkLabel(
            self.health_frame,
            text="Status: Unknown",
            font=ctk.CTkFont(size=13)
        )
        
        self.health_result = ctk.CTkLabel(
            self.health_frame,
            text="Result: --",
            font=ctk.CTkFont(size=13)
        )
        
        self.start_health_check_btn = ctk.CTkButton(
            self.health_frame,
            text="Start Health Check",
            command=self._start_health_check,
            width=150
        )
        
        self.abort_health_check_btn = ctk.CTkButton(
            self.health_frame,
            text="Abort Health Check",
            command=self._abort_health_check,
            width=150
        )
        
        self.read_health_btn = ctk.CTkButton(
            self.health_frame,
            text="Read Health Status",
            command=self._read_health_status,
            width=150
        )
        
        self.clear_health_btn = ctk.CTkButton(
            self.health_frame,
            text="Clear Health Failure",
            command=self._clear_health_failure,
            width=150,
            fg_color="#C53030",
            hover_color="#9B2C2C"
        )
        
        # Watchdog
        self.watchdog_frame = ctk.CTkFrame(self)
        self.watchdog_label = ctk.CTkLabel(
            self.watchdog_frame,
            text="Watchdog Timer",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        self.watchdog_status = ctk.CTkLabel(
            self.watchdog_frame,
            text="Enabled: Unknown",
            font=ctk.CTkFont(size=13)
        )
        
        self.watchdog_timer_label = ctk.CTkLabel(
            self.watchdog_frame,
            text="Timer (seconds):",
            font=ctk.CTkFont(size=13)
        )
        
        self.watchdog_timer_entry = ctk.CTkEntry(
            self.watchdog_frame,
            placeholder_text="300-65535",
            width=150
        )
        
        self.watchdog_enable_btn = ctk.CTkButton(
            self.watchdog_frame,
            text="Enable Watchdog",
            command=lambda: self._set_watchdog(True),
            width=150,
            fg_color="#2B7A0B",
            hover_color="#1F5A08"
        )
        
        self.watchdog_disable_btn = ctk.CTkButton(
            self.watchdog_frame,
            text="Disable Watchdog",
            command=lambda: self._set_watchdog(False),
            width=150
        )
        
        self.set_watchdog_timer_btn = ctk.CTkButton(
            self.watchdog_frame,
            text="Set Timer Value",
            command=self._set_watchdog_timer,
            width=150
        )
        
        self.reset_watchdog_btn = ctk.CTkButton(
            self.watchdog_frame,
            text="Reset Counter",
            command=self._reset_watchdog,
            width=150
        )
    
    def _layout_widgets(self):
        """Layout all widgets"""
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Operation control
        self.operation_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.operation_label.pack(pady=(15, 10))
        self.operation_status.pack(pady=10)
        self.btn_frame.pack(pady=10)
        self.psu_on_btn.pack(side="left", padx=10)
        self.psu_off_btn.pack(side="left", padx=10)
        self.read_operation_btn.pack(pady=10)
        
        # Fan control
        self.fan_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.fan_label.pack(pady=(15, 10))
        self.fan_mode_label.pack(pady=(10, 0))
        self.fan_mode_value.pack(pady=(0, 5))
        self.fan_speed_label.pack(pady=(10, 0))
        self.fan_speed_value.pack(pady=(0, 10))
        self.fan_offset_label.pack(pady=(10, 5))
        self.fan_offset_entry.pack(pady=5)
        self.set_fan_offset_btn.pack(pady=5)
        self.read_fan_btn.pack(pady=10)
        
        # Health check
        self.health_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.health_label.pack(pady=(15, 10))
        self.health_status.pack(pady=5)
        self.health_result.pack(pady=5)
        self.start_health_check_btn.pack(pady=5)
        self.abort_health_check_btn.pack(pady=5)
        self.read_health_btn.pack(pady=5)
        self.clear_health_btn.pack(pady=5)
        
        # Watchdog
        self.watchdog_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.watchdog_label.pack(pady=(15, 10))
        self.watchdog_status.pack(pady=5)
        self.watchdog_timer_label.pack(pady=(10, 5))
        self.watchdog_timer_entry.pack(pady=5)
        self.set_watchdog_timer_btn.pack(pady=5)
        self.watchdog_enable_btn.pack(pady=5)
        self.watchdog_disable_btn.pack(pady=5)
        self.reset_watchdog_btn.pack(pady=5)
    
    def _set_operation(self, value):
        """Set operation state"""
        if self.write_callback(0x01, value):
            state = "ON" if value == 0x80 else "OFF"
            messagebox.showinfo("Success", f"PSU turned {state}")
            self._read_operation_status()
        else:
            messagebox.showerror("Error", "Failed to set operation state")
    
    def _read_operation_status(self):
        """Read operation status"""
        data = self.read_callback(0x01, 1)
        if data:
            if data[0] == 0x80:
                self.operation_status.configure(text="Status: ON", text_color="#38A169")
            elif data[0] == 0x00:
                self.operation_status.configure(text="Status: OFF", text_color="#E53E3E")
            else:
                self.operation_status.configure(text=f"Status: 0x{data[0]:02X}", text_color="#DD6B20")
    
    def _set_fan_offset(self):
        """Set fan offset"""
        try:
            offset = int(self.fan_offset_entry.get())
            if offset < 0 or offset > 10000:
                messagebox.showerror("Invalid Input", "Offset must be 0-10000 RPM")
                return
            
            # Convert to Linear11 format
            data = LinearDataFormat.encode_linear11(float(offset))
            
            if self.write_callback(0xE9, data):
                messagebox.showinfo("Success", f"Fan offset set to {offset} RPM")
                self._read_fan_status()
            else:
                messagebox.showerror("Error", "Failed to set fan offset")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
    
    def _read_fan_status(self):
        """Read fan status"""
        # Read fan config
        config = self.read_callback(0x3A, 1)
        if config:
            if config[0] == 0x99:
                self.fan_mode_value.configure(text="RPM Mode")
            else:
                self.fan_mode_value.configure(text=f"0x{config[0]:02X}")
        
        # Read fan speed
        speed = self.read_callback(0x90, 2)
        if speed:
            rpm = LinearDataFormat.decode_linear11(speed)
            self.fan_speed_value.configure(text=f"{rpm:.0f} RPM")
    
    def _start_health_check(self):
        """Start health check"""
        if self.write_callback(0xDB, 0x01):
            messagebox.showinfo("Health Check", "Health check started")
            self._read_health_status()
        else:
            messagebox.showerror("Error", "Failed to start health check")
    
    def _abort_health_check(self):
        """Abort health check"""
        if self.write_callback(0xDB, 0x00):
            messagebox.showinfo("Health Check", "Health check aborted")
            self._read_health_status()
        else:
            messagebox.showerror("Error", "Failed to abort health check")
    
    def _read_health_status(self):
        """Read health check status"""
        data = self.read_callback(0xDC, 2)
        if data:
            low_byte = data[0]
            
            # Bit 0: Health check result
            result = "PASS" if (low_byte & 0x01) else "FAIL"
            self.health_result.configure(
                text=f"Result: {result}",
                text_color="#38A169" if result == "PASS" else "#E53E3E"
            )
            
            # Check other status bits
            status_msgs = []
            if low_byte & 0x02:
                status_msgs.append("Output power > 95%")
            if low_byte & 0x04:
                status_msgs.append("Vin not OK")
            if low_byte & 0x10:
                status_msgs.append("PSM not OK")
            if low_byte & 0x80:
                status_msgs.append("Not performed")
            
            status_text = ", ".join(status_msgs) if status_msgs else "Ready"
            self.health_status.configure(text=f"Status: {status_text}")
    
    def _clear_health_failure(self):
        """Clear health check failure"""
        if self.write_callback(0xDD, 0xE2):
            messagebox.showinfo("Success", "Health check failure cleared")
            self._read_health_status()
        else:
            messagebox.showerror("Error", "Failed to clear health check failure")
    
    def _set_watchdog(self, enable):
        """Enable/disable watchdog"""
        value = 0x01 if enable else 0x00
        if self.write_callback(0xE7, value):
            state = "enabled" if enable else "disabled"
            messagebox.showinfo("Success", f"Watchdog {state}")
            self._read_watchdog_status()
        else:
            messagebox.showerror("Error", "Failed to set watchdog state")
    
    def _set_watchdog_timer(self):
        """Set watchdog timer value"""
        try:
            timer = int(self.watchdog_timer_entry.get())
            if timer < 300 or timer > 65535:
                messagebox.showerror("Invalid Input", "Timer must be 300-65535 seconds")
                return
            
            # Convert to 2 bytes (little endian)
            data = [timer & 0xFF, (timer >> 8) & 0xFF]
            
            if self.write_callback(0xE5, data):
                messagebox.showinfo("Success", f"Watchdog timer set to {timer} seconds")
            else:
                messagebox.showerror("Error", "Failed to set watchdog timer")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
    
    def _reset_watchdog(self):
        """Reset watchdog counter"""
        # Write any value to reset counter
        if self.write_callback(0xE3, [0x00, 0x00]):
            messagebox.showinfo("Success", "Watchdog counter reset")
        else:
            messagebox.showerror("Error", "Failed to reset watchdog counter")
    
    def _read_watchdog_status(self):
        """Read watchdog status"""
        data = self.read_callback(0xE7, 1)
        if data:
            enabled = (data[0] & 0x01) == 0x01
            self.watchdog_status.configure(
                text=f"Enabled: {'Yes' if enabled else 'No'}",
                text_color="#38A169" if enabled else "#E53E3E"
            )
