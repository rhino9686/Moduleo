## script for 
import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh
import numpy as np





class STLViewerMatplotlib:
    def __init__(self, root):
        self.root = root
        self.root.title("STL Viewer - Matplotlib")
        self.root.geometry("900x700")
        
        # Create menu
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open STL", command=self.load_stl)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Add toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        
        # Status bar
        self.status = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_stl(self):
        filename = filedialog.askopenfilename(
            title="Select STL file",
            filetypes=[('STL files', '*.stl'), ('All files', '*.*')]
        )
        
        if filename:
            try:
                # Load the STL file
                self.status.config(text=f"Loading {filename}...")
                self.root.update()
                
                stl_mesh = mesh.Mesh.from_file(filename)
                
                # Clear previous plot
                self.ax.clear()
                
                # Create 3D polygon collection from mesh
                collection = Poly3DCollection(
                    stl_mesh.vectors,
                    alpha=0.7,
                    facecolor='cyan',
                    edgecolor='black',
                    linewidths=0.5
                )
                
                self.ax.add_collection3d(collection)
                
                # Auto-scale the axes
                scale = stl_mesh.points.flatten()
                self.ax.auto_scale_xyz(scale, scale, scale)

                # Hide grid lines
                self.ax.grid(False)
                self.ax.set_axis_off()
                self.ax.set_facecolor('#2E2E2E')  # Dark gray for 3D plot area
                self.fig.patch.set_facecolor('#1E1E1E')  # Darker gray for figure background

                # Set labels
                #self.ax.set_xlabel('X')
                #self.ax.set_ylabel('Y')
                #self.ax.set_zlabel('Z')
                
                # Refresh canvas
                self.canvas.draw()
                
                num_faces = len(stl_mesh.vectors)
                self.status.config(text=f"Loaded: {filename} ({num_faces} faces)")
                
            except Exception as e:
                self.status.config(text=f"Error: {str(e)}")

# Run application
if __name__ == "__main__":
    root = tk.Tk()
    app = STLViewerMatplotlib(root)
    root.mainloop()