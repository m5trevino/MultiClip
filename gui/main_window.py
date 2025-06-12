import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Callable, Optional
import threading
from diff_marker.diff_interface import DiffInterface

class SlotDisplay(ttk.Frame):
    def __init__(self, parent, slot_id: int, on_select: Callable):
        super().__init__(parent)
        self.slot_id = slot_id
        self.on_select = on_select
        self.content = ""
        self.preview = ""
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Slot header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', padx=2, pady=1)
        
        self.slot_label = ttk.Label(header_frame, text=f"Slot {self.slot_id}", 
                                   font=('Arial', 9, 'bold'))
        self.slot_label.pack(side='left')
        
        self.status_label = ttk.Label(header_frame, text="Empty", 
                                     font=('Arial', 8), foreground='gray')
        self.status_label.pack(side='right')
        
        # Content preview
        self.preview_text = tk.Text(self, height=2, width=40, wrap='word',
                                   font=('Consolas', 8), state='disabled',
                                   cursor='hand2')
        self.preview_text.pack(fill='both', expand=True, padx=2, pady=1)
        
        # Bind click event
        self.preview_text.bind('<Button-1>', self._on_click)
        
        # Context menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copy to Clipboard", 
                                     command=self._copy_to_clipboard)
        self.context_menu.add_command(label="Clear Slot", 
                                     command=self._clear_slot)
        
        self.preview_text.bind('<Button-3>', self._show_context_menu)
    
    def update_content(self, content: str, preview: str):
        self.content = content
        self.preview = preview
        
        # Update preview display
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, 'end')
        self.preview_text.insert(1.0, preview)
        self.preview_text.config(state='disabled')
        
        # Update status
        if content:
            self.status_label.config(text=f"{len(content)} chars", foreground='blue')
            self.preview_text.config(bg='#f0f8ff')
        else:
            self.status_label.config(text="Empty", foreground='gray')
            self.preview_text.config(bg='white')
    
    def _on_click(self, event):
        if self.content:
            self.on_select(self.slot_id)
    
    def _show_context_menu(self, event):
        if self.content:
            self.context_menu.post(event.x_root, event.y_root)
    
    def _copy_to_clipboard(self):
        if self.content:
            self.on_select(self.slot_id)
    
    def _clear_slot(self):
        # This should call back to the main manager
        pass

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MultiClip System")
        self.root.geometry("900x700")
        
        # Callbacks
        self.slot_select_callback: Optional[Callable] = None
        self.mode_change_callback: Optional[Callable] = None
        self.orderly_callback: Optional[Callable] = None
        
        self.slot_displays: Dict[int, SlotDisplay] = {}
        self.current_mode = "Multiclip"
        
        # Add clipboard manager reference
        self.clipboard_manager = None
        
        self._create_ui()
    
    def set_clipboard_manager(self, clipboard_manager):
        """Set the clipboard manager reference"""
        self.clipboard_manager = clipboard_manager
    
    def _create_ui(self):
        # Main menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save State", command=self._save_state)
        file_menu.add_command(label="Load State", command=self._load_state)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Top toolbar
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        # Mode buttons
        ttk.Label(toolbar, text="Mode:", font=('Arial', 10, 'bold')).pack(side='left')
        
        self.mode_var = tk.StringVar(value="Multiclip")
        mode_frame = ttk.Frame(toolbar)
        mode_frame.pack(side='left', padx=10)
        
        # Updated mode list to include Diff-Marker
        for mode in ["Multiclip", "Orderly", "Snippers", "Diff-Marker"]:
            btn = ttk.Radiobutton(mode_frame, text=mode, variable=self.mode_var,
                                 value=mode, command=self._on_mode_change)
            btn.pack(side='left', padx=5)
        
        # Status display
        self.status_label = ttk.Label(toolbar, text="Ready", 
                                     font=('Arial', 9), foreground='green')
        self.status_label.pack(side='right')
        
        # Main content area
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - slot displays
        left_panel = ttk.LabelFrame(content_frame, text="Clipboard Slots", padding=5)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Create slot displays in grid
        slots_frame = ttk.Frame(left_panel)
        slots_frame.pack(fill='both', expand=True)
        
        for i in range(10):
            row = i // 2
            col = i % 2
            
            slot_display = SlotDisplay(slots_frame, i, self._on_slot_select)
            slot_display.grid(row=row, column=col, sticky='nsew', 
                             padx=2, pady=2)
            
            self.slot_displays[i] = slot_display
        
        # Configure grid weights
        for i in range(5):  # 5 rows
            slots_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):  # 2 columns
            slots_frame.grid_columnconfigure(i, weight=1)
        
        # Right panel - mode-specific controls
        self.right_panel = ttk.LabelFrame(content_frame, text="Controls", padding=5)
        self.right_panel.pack(side='right', fill='both', padx=(5, 0))
        
        self._create_mode_panels()
        
        # Bottom status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill='x', padx=5, pady=5)
        
        self.bottom_status = ttk.Label(status_frame, text="MultiClip System Ready", 
                                      relief='sunken', anchor='w')
        self.bottom_status.pack(fill='x')
    
    def _create_mode_panels(self):
        # Multiclip panel
        self.multiclip_panel = ttk.Frame(self.right_panel)
        
        ttk.Label(self.multiclip_panel, text="Multiclip Mode", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Button(self.multiclip_panel, text="Clear All Slots",
                  command=self._clear_all_slots).pack(pady=5)
        
        ttk.Separator(self.multiclip_panel, orient='horizontal').pack(fill='x', pady=10)
        
        help_text = """Hotkeys:
Ctrl+0-9: Copy to slot
Ctrl+Shift+0-9: Paste from slot
Ctrl+Alt+0-9: Transfer to clipboard"""
        
        ttk.Label(self.multiclip_panel, text=help_text, 
                 font=('Arial', 9), justify='left').pack(pady=5)
        
        # Orderly panel
        self.orderly_panel = ttk.Frame(self.right_panel)
        
        ttk.Label(self.orderly_panel, text="Orderly Mode", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.orderly_status = ttk.Label(self.orderly_panel, text="Inactive", 
                                       font=('Arial', 10), foreground='gray')
        self.orderly_status.pack(pady=5)
        
        btn_frame = ttk.Frame(self.orderly_panel)
        btn_frame.pack(pady=10)
        
        self.orderly_toggle_btn = ttk.Button(btn_frame, text="Activate Orderly",
                                           command=self._toggle_orderly)
        self.orderly_toggle_btn.pack(pady=2)
        
        ttk.Button(btn_frame, text="Reset Sequence",
                  command=self._reset_orderly).pack(pady=2)
        
        # Snippers panel
        self.snippers_panel = ttk.Frame(self.right_panel)
        
        ttk.Label(self.snippers_panel, text="Snippers Mode", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Button(self.snippers_panel, text="View Snippets",
                  command=self._open_snippers_view).pack(pady=5)
        
        ttk.Button(self.snippers_panel, text="Save New Snippet",
                  command=self._open_snippers_save).pack(pady=5)
        
        # NEW: Diff-Marker panel
        self.diff_marker_panel = ttk.Frame(self.right_panel)
        
        ttk.Label(self.diff_marker_panel, text="Diff-Marker Mode", 
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Create the diff interface
        self.diff_interface = DiffInterface(self.diff_marker_panel, self.clipboard_manager)
        self.diff_interface.pack(fill='both', expand=True)
        
        # Set up status callback
        self.diff_interface.set_status_callback(self.update_status)
        
        # Show initial panel
        self._show_mode_panel("Multiclip")
    
    def _show_mode_panel(self, mode: str):
        # Hide all panels
        for panel in [self.multiclip_panel, self.orderly_panel, 
                     self.snippers_panel, self.diff_marker_panel]:
            panel.pack_forget()
        
        # Show selected panel
        if mode == "Multiclip":
            self.multiclip_panel.pack(fill='both', expand=True)
        elif mode == "Orderly":
            self.orderly_panel.pack(fill='both', expand=True)
        elif mode == "Snippers":
            self.snippers_panel.pack(fill='both', expand=True)
        elif mode == "Diff-Marker":
            # Update clipboard manager reference if needed
            if self.clipboard_manager:
                self.diff_interface.clipboard_manager = self.clipboard_manager
            self.diff_marker_panel.pack(fill='both', expand=True)
    
    def _on_mode_change(self):
        new_mode = self.mode_var.get()
        if new_mode != self.current_mode:
            self.current_mode = new_mode
            self._show_mode_panel(new_mode)
            
            if self.mode_change_callback:
                self.mode_change_callback(new_mode)
    
    def _on_slot_select(self, slot_id: int):
        if self.slot_select_callback:
            self.slot_select_callback(slot_id)
    
    def _toggle_orderly(self):
        if self.orderly_callback:
            self.orderly_callback("toggle")
    
    def _reset_orderly(self):
        if self.orderly_callback:
            self.orderly_callback("reset")
    
    def _clear_all_slots(self):
        if messagebox.askyesno("Confirm", "Clear all clipboard slots?"):
            # This should call back to the main manager
            pass
    
    def _save_state(self):
        # Implement state saving
        pass
    
    def _load_state(self):
        # Implement state loading
        pass
    
    def _open_snippers_view(self):
        # Launch snippers view window
        pass
    
    def _open_snippers_save(self):
        # Launch snippers save window
        pass
    
    # Public interface methods
    def update_slot(self, slot_id: int, content: str, preview: str):
        if slot_id in self.slot_displays:
            self.slot_displays[slot_id].update_content(content, preview)
    
    def update_status(self, status: str, color: str = 'black'):
        self.status_label.config(text=status, foreground=color)
    
    def update_bottom_status(self, status: str):
        self.bottom_status.config(text=status)
    
    def update_orderly_status(self, status: str, active: bool):
        self.orderly_status.config(text=status, 
                                  foreground='green' if active else 'gray')
        self.orderly_toggle_btn.config(text="Deactivate Orderly" if active else "Activate Orderly")
    
    def set_slot_select_callback(self, callback: Callable):
        self.slot_select_callback = callback
    
    def set_mode_change_callback(self, callback: Callable):
        self.mode_change_callback = callback
    
    def set_orderly_callback(self, callback: Callable):
        self.orderly_callback = callback
    
    def run(self):
        self.root.mainloop()
    
    def destroy(self):
        self.root.destroy()