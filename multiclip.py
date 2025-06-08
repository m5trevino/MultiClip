import pyperclip
import keyboard
import json
import os
import pyautogui
import subprocess
import time
import tkinter as tk
from tkinter import ttk
import threading

class MultiClipSystem:
    def __init__(self):
        # Paths
        self.dict_file = "/home/flintx/multiclip/clipboard_dict.json"
        self.icon_path = "/home/flintx/multiclip/chargers.png"
        
        # Initialize
        self.clipboard_slots = self.load_dictionary()
        self.current_mode = "MultiClip"
        self.orderly_active = False
        self.orderly_index = 1
        
        # Drag and drop state
        self.drag_source = None
        self.drag_data = None
        
        # Setup UI
        self.root = tk.Tk()
        self.root.title("MultiClip System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_ui()
        self.register_hotkeys()
        
    def load_dictionary(self):
        """Load clipboard slots from file"""
        if os.path.exists(self.dict_file):
            with open(self.dict_file, "r") as file:
                return json.load(file)
        else:
            return {f"slot_{i}": "" for i in range(1, 16)}
    
    def save_dictionary(self):
        """Save clipboard slots to file"""
        with open(self.dict_file, "w") as file:
            json.dump(self.clipboard_slots, file, indent=4)
    
    def show_toast(self, title, message):
        """Show system notification with custom icon"""
        try:
            subprocess.run([
                "notify-send", 
                "-i", self.icon_path, 
                title, 
                message, 
                "-t", "3000"
            ], check=False)
        except Exception as e:
            print(f"Toast notification error: {e}")
    
    def setup_ui(self):
        """Setup the UI to match your wireframe with swappable slots"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Top frame for mode buttons
        top_frame = tk.Frame(self.root, bg='#f0f0f0', height=50)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        top_frame.pack_propagate(False)
        
        # Mode buttons (top right)
        buttons_frame = tk.Frame(top_frame, bg='#f0f0f0')
        buttons_frame.pack(side=tk.RIGHT, pady=5)
        
        self.multiclip_btn = tk.Button(buttons_frame, text="MultiClip", 
                                      command=lambda: self.switch_mode("MultiClip"),
                                      width=10, height=1, font=('Arial', 9, 'bold'),
                                      bg='#3498db' if self.current_mode == "MultiClip" else '#ecf0f1',
                                      fg='white' if self.current_mode == "MultiClip" else 'black')
        self.multiclip_btn.pack(side=tk.LEFT, padx=2)
        
        self.orderly_btn = tk.Button(buttons_frame, text="Orderly", 
                                    command=lambda: self.switch_mode("Orderly"),
                                    width=10, height=1, font=('Arial', 9, 'bold'),
                                    bg='#e74c3c' if self.current_mode == "Orderly" else '#ecf0f1',
                                    fg='white' if self.current_mode == "Orderly" else 'black')
        self.orderly_btn.pack(side=tk.LEFT, padx=2)
        
        self.snippers_btn = tk.Button(buttons_frame, text="Snippers", 
                                     width=10, height=1, font=('Arial', 9, 'bold'),
                                     bg='#95a5a6', fg='white', state=tk.DISABLED)
        self.snippers_btn.pack(side=tk.LEFT, padx=2)
        
        # Title label (top left)
        title_label = tk.Label(top_frame, text="switch clipboard slot", 
                              font=('Arial', 10), bg='#f0f0f0', fg='blue')
        title_label.pack(side=tk.LEFT, pady=10)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create slots list (right side, matching your wireframe)
        self.create_slots_list(main_frame)
        
    def create_slots_list(self, parent):
        """Create the vertical list of slots like in your wireframe"""
        # Slots container
        slots_frame = tk.Frame(parent, bg='#f0f0f0')
        slots_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create scrollable area
        canvas = tk.Canvas(slots_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(slots_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create the individual slot widgets
        self.slot_widgets = {}
        for i in range(1, 16):
            self.create_slot_widget(i)
    
    def create_slot_widget(self, slot_num):
        """Create a single slot widget with drag/drop capability"""
        slot_key = f"slot_{slot_num}"
        content = self.clipboard_slots.get(slot_key, "")
        
        # Main slot frame
        slot_frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RAISED, bd=1)
        slot_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Slot number (left side, draggable)
        number_frame = tk.Frame(slot_frame, bg='#3498db', width=40)
        number_frame.pack(side=tk.LEFT, fill=tk.Y)
        number_frame.pack_propagate(False)
        
        number_label = tk.Label(number_frame, text=str(slot_num), 
                               font=('Arial', 12, 'bold'), bg='#3498db', fg='white')
        number_label.pack(expand=True)
        
        # Content preview (right side)
        content_frame = tk.Frame(slot_frame, bg='white')
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        if content.strip():
            # Show content preview
            preview = content.replace('\n', ' ')[:100] + ('...' if len(content) > 100 else '')
            content_label = tk.Label(content_frame, text=preview, 
                                   font=('Arial', 9), bg='white', fg='black',
                                   anchor='w', justify=tk.LEFT)
            content_label.pack(fill=tk.BOTH, expand=True, pady=5)
        else:
            # Empty slot
            content_label = tk.Label(content_frame, text="clipped content from a document or webpage that you copied by pressing ctrl + 1 and you can paste it with ctrl + shift + 1", 
                                   font=('Arial', 9), bg='white', fg='#7f8c8d',
                                   anchor='w', justify=tk.LEFT)
            content_label.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Store widget references
        self.slot_widgets[slot_num] = {
            'frame': slot_frame,
            'number_frame': number_frame,
            'number_label': number_label,
            'content_frame': content_frame,
            'content_label': content_label
        }
        
        # Bind drag and drop events to the number area
        self.bind_drag_events(slot_num, number_frame, number_label)
    
    def bind_drag_events(self, slot_num, number_frame, number_label):
        """Bind drag and drop events for slot swapping"""
        def start_drag(event):
            self.drag_source = slot_num
            self.drag_data = self.clipboard_slots.get(f"slot_{slot_num}", "")
            number_frame.config(bg='#e74c3c')  # Red when dragging
            print(f"Started dragging slot {slot_num}")
        
        def end_drag(event):
            if self.drag_source:
                number_frame.config(bg='#3498db')  # Back to blue
                self.drag_source = None
                self.drag_data = None
        
        def on_drop(event):
            if self.drag_source and self.drag_source != slot_num:
                # Swap the content between slots
                self.swap_slot_content(self.drag_source, slot_num)
                print(f"Swapped content between slot {self.drag_source} and slot {slot_num}")
                
                # Reset drag state
                if self.drag_source in self.slot_widgets:
                    self.slot_widgets[self.drag_source]['number_frame'].config(bg='#3498db')
                self.drag_source = None
                self.drag_data = None
                
                # Refresh the UI
                self.refresh_slots_display()
        
        def on_drag_enter(event):
            if self.drag_source and self.drag_source != slot_num:
                number_frame.config(bg='#f39c12')  # Orange when hovering over drop target
        
        def on_drag_leave(event):
            if self.drag_source and self.drag_source != slot_num:
                number_frame.config(bg='#3498db')  # Back to blue
        
        # Bind events
        number_frame.bind("<Button-1>", start_drag)
        number_frame.bind("<ButtonRelease-1>", end_drag)
        number_frame.bind("<B1-Motion>", lambda e: None)  # Track dragging
        number_frame.bind("<Button-1><ButtonRelease-1>", on_drop)
        number_frame.bind("<Enter>", on_drag_enter)
        number_frame.bind("<Leave>", on_drag_leave)
        
        number_label.bind("<Button-1>", start_drag)
        number_label.bind("<ButtonRelease-1>", end_drag)
        number_label.bind("<B1-Motion>", lambda e: None)
        number_label.bind("<Button-1><ButtonRelease-1>", on_drop)
        number_label.bind("<Enter>", on_drag_enter)
        number_label.bind("<Leave>", on_drag_leave)
    
    def swap_slot_content(self, source_slot, target_slot):
        """Swap content between two slots"""
        source_key = f"slot_{source_slot}"
        target_key = f"slot_{target_slot}"
        
        # Get current content
        source_content = self.clipboard_slots.get(source_key, "")
        target_content = self.clipboard_slots.get(target_key, "")
        
        # Swap the content
        self.clipboard_slots[source_key] = target_content
        self.clipboard_slots[target_key] = source_content
        
        # Save to file
        self.save_dictionary()
        
        # Show notification
        self.show_toast("Slots Swapped", 
                       f"Swapped content between slot {source_slot} and slot {target_slot}")
    
    def refresh_slots_display(self):
        """Refresh the display of all slots"""
        for slot_num in range(1, 16):
            if slot_num in self.slot_widgets:
                slot_key = f"slot_{slot_num}"
                content = self.clipboard_slots.get(slot_key, "")
                content_label = self.slot_widgets[slot_num]['content_label']
                
                if content.strip():
                    preview = content.replace('\n', ' ')[:100] + ('...' if len(content) > 100 else '')
                    content_label.config(text=preview, fg='black')
                else:
                    content_label.config(text="clipped content from a document or webpage that you copied by pressing ctrl + 1 and you can paste it with ctrl + shift + 1", 
                                       fg='#7f8c8d')
    
    def switch_mode(self, mode):
        """Switch between modes"""
        self.current_mode = mode
        
        if mode == "Orderly":
            self.orderly_active = True
            self.orderly_index = 1
            self.show_toast("Orderly Mode", "Sequential copying activated")
        else:
            self.orderly_active = False
            self.show_toast("Multiclip Mode", "Manual slot selection activated")
            
        self.setup_ui()  # Refresh UI with new button states
    
    def add_to_slot(self, slot_num):
        """Copy selected content to clipboard slot - using your proven method"""
        try:
            # Use your working method: simulate Ctrl+C first
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.1)  # Give it time to copy
            
            # Get the copied content
            clipboard_content = pyperclip.paste()
            
            if self.orderly_active:
                # Orderly mode: use sequential slot
                actual_slot = f"slot_{self.orderly_index}"
                self.clipboard_slots[actual_slot] = clipboard_content
                self.save_dictionary()
                
                self.show_toast("Orderly Copy", 
                              f"Slot {self.orderly_index} updated")
                
                # Move to next slot
                self.orderly_index += 1
                if self.orderly_index > 15:
                    self.orderly_index = 1
            else:
                # Normal multiclip mode
                slot_key = f"slot_{slot_num}"
                self.clipboard_slots[slot_key] = clipboard_content
                self.save_dictionary()
                
                self.show_toast("Slot Updated", 
                              f"Slot {slot_num} updated")
            
            # Refresh the visual display
            self.refresh_slots_display()
            
        except Exception as e:
            self.show_toast("Copy Error", str(e))
    
    def paste_from_slot(self, slot_num):
        """Paste content from clipboard slot"""
        try:
            slot_key = f"slot_{slot_num}"
            content = self.clipboard_slots.get(slot_key, "")
            
            if content:
                pyperclip.copy(content)
                time.sleep(0.1)
                pyautogui.hotkey("ctrl", "v")
                
                self.show_toast("Slot Pasted", 
                              f"Slot {slot_num} content pasted")
            else:
                self.show_toast("Slot Empty", 
                              f"No content in slot {slot_num}")
                
        except Exception as e:
            self.show_toast("Paste Error", str(e))
    
    def transfer_to_default(self, slot_num):
        """Transfer slot content to default clipboard"""
        try:
            slot_key = f"slot_{slot_num}"
            content = self.clipboard_slots.get(slot_key, "")
            
            if content:
                pyperclip.copy(content)
                self.show_toast("Slot Transferred", 
                              f"Slot {slot_num} transferred to clipboard")
            else:
                self.show_toast("Slot Empty", 
                              f"No content in slot {slot_num}")
                
        except Exception as e:
            self.show_toast("Transfer Error", str(e))
    
    def register_hotkeys(self):
        """Register all hotkeys using your proven method"""
        def hotkey_thread():
            try:
                # Copy hotkeys (Ctrl + 1-9)
                for i in range(1, 10):
                    keyboard.add_hotkey(f"ctrl+{i}", self.add_to_slot, args=[i])
                
                # Paste hotkeys (Ctrl + Shift + 1-9)
                for i in range(1, 10):
                    keyboard.add_hotkey(f"ctrl+shift+{i}", self.paste_from_slot, args=[i])
                
                # Transfer hotkeys (Ctrl + Alt + 1-9)
                for i in range(1, 10):
                    keyboard.add_hotkey(f"ctrl+alt+{i}", self.transfer_to_default, args=[i])
                
                print("All hotkeys registered successfully!")
                
            except Exception as e:
                print(f"Hotkey registration error: {e}")
        
        # Start hotkeys in background thread
        threading.Thread(target=hotkey_thread, daemon=True).start()
    
    def run(self):
        """Start the application"""
        self.show_toast("MultiClip Started", "System ready - drag slot numbers to swap content!")
        self.root.mainloop()

if __name__ == "__main__":
    app = MultiClipSystem()
    app.run()
