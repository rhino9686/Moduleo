#!/usr/bin/env python3
"""
Moduleo Interface Client 
"""

import customtkinter as ctk
from gui.main_window import MainWindow
import sys

def main():
    """Main entry point for the application"""
    # Set appearance mode and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create and run the main window
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
