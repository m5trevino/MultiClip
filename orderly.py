# START ### IMPORTS ###
import tkinter as tk
from tkinter import ttk, filedialog, messagebox # Keep necessary tkinter modules
import json
import os
import sys
import keyboard
import pyperclip
import pyautogui
import subprocess
import time
from threading import Thread # For running the GUI in a separate thread
import re # Need regex for pattern matching commands
# FINISH ### IMPORTS ###

# START ### CONFIG ###
# !! IMPORTANT !! Make sure this path points to the *SAME* dict file Multiclip uses.
MULTICLIP_DICT_FILE = "/home/flintx/multiclip/clipboard_dict.json"
# Icon for notifications, keepin' it consistent with Multiclip
ICON_PATH = "/home/flintx/multiclip/chargers-icon.png"

# Hotkey to toggle Orderly mode on/off (Global Hotkey managed by main multiclip.py or this script if standalone)
# TOGGLE_ORDERLY_HOTKEY = "ctrl+alt+o" # This hotkey is handled by multiclip.py now

# Paste modes (using integers for radio buttons)
PASTE_MODE_NONE = 0
PASTE_MODE_SEQ_CTRL_V = 1
PASTE_MODE_SEQ_CTRL_SHIFT_V = 2
# PASTE_MODE_DIRECT = 3 # Direct paste handled by main multiclip hotkeys

# Define number of slots for sequential use (matching Multiclip)
NUM_SEQUENTIAL_SLOTS = 10 # Use the first 10 slots (slot_1 to slot_9, then slot_0)
SEQUENTIAL_SLOT_NAMES = [f"slot_{i}" for i in range(1, NUM_SEQUENTIAL_SLOTS)] + [f"slot_{0}"]

# END ### CONFIG ###

# START ### DATA HANDLING ###
# Helper to load the dictionary (shared with Multiclip)
def load_dictionary():
    """Loads the clipboard dictionary from the specified JSON file."""
    if not os.path.exists(MULTICLIP_DICT_FILE):
        print(f"[WARNING] Dictionary file not found at: {MULTICLIP_DICT_FILE}. Returning empty.")
        return {}
    try:
        with open(MULTICLIP_DICT_FILE, "r", encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                print(f"Dictionary file {MULTICLIP_DICT_FILE} is empty. Returning empty.")
                return {}
            file.seek(0)
            return json.load(file)
        except json.JSONDecodeError:
            print(f"[ERROR] Damn, the dictionary file {MULTICLIP_DICT_FILE} is messed up JSON. Returning empty.")
            # show_toast("File Error", f"Corrupted dictionary file:\n{os.path.basename(MULTICLIP_DICT_FILE)}") # Avoid toast if main script handles it
            return {}
        except Exception as e:
            print(f"[ERROR] Unexpected error loading dictionary from {MULTICLIP_DICT_FILE}: {e}")
            # show_toast("File Error", f"Error loading dictionary:\n{os.path.basename(MULTICLIP_DICT_FILE)}") # Avoid toast if main script handles it
            return {}

# Helper to save the dictionary (shared with Multiclip)
def save_dictionary(dictionary):
    """Saves the clipboard dictionary to the specified JSON file."""
    try:
        os.makedirs(os.path.dirname(MULTICLIP_DICT_FILE), exist_ok=True)
        with open(MULTICLIP_DICT_FILE, "w", encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4)
    except Exception as e:
        print(f"[ERROR] Couldn't save the dictionary file {MULTICLIP_DICT_FILE}: {e}")
        # show_toast("Save Error", f"Failed to save changes to\n{os.path.basename(MULTIClip_DICT_FILE)}") # Avoid toast if main script handles it
# FINISH ### DATA HANDLING ###


# START ### NOTIFICATION UTIL ###
# Re-using the toast function (can be called by Ordely itself)
def show_toast(title, message):
    """Displays a system notification using notify-send."""
    try:
        subprocess.run(["which", "notify-send"], check=True, capture_output=True, text=True)
        subprocess.Popen(["notify-send", "-i", ICON_PATH, title, message, "-t", "4000"])
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[WARNING] notify-send command not found. Cannot display desktop notifications.")
        print(f"Notification: {title} - {message}")
    except Exception as e:
        print(f"[ERROR] Error showing toast notification: {e}")
        print(f"Notification: {title} - {message}")
# FINISH ### NOTIFICATION UTIL ###

# START ### TOOLTIP HELPER ###
# Simple tooltip class (kept local to Ordely GUI)
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if not self.widget.winfo_exists(): return # Check if widget is still valid
        x, y, _, _ = self.widget.bbox("insert")
        # Adjust position to avoid covering the widget and stay near mouse
        x += self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y += self.widget.winfo_rooty() + self.widget.winfo_height() + 5 # Position below widget

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True) # Window without borders
        # Ensure tooltip stays on top
        self.tooltip.attributes('-topmost', True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1,
                         font=("tahoma", "8", "normal"), justify=tk.LEFT, wraplength=300)
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tooltip:
            try:
                self.tooltip.destroy()
            except tk.TclError:
                pass # Window might already be destroyed
        self.tooltip = None
# FINISH ### TOOLTIP HELPER ###

# START ### ORDERLY APP CLASS ###
class OrderlyApp:
    def __init__(self, master=None):
        # master is the root window that launches this (from multiclip.py)
        self.master = master
        self.root = None # This will be the Toplevel window for Ordely GUI
        self.is_active = False
        self.multiclip_data = {} # Full dictionary from the JSON file
        self.sequential_slots_data = [] # List of dictionaries for GUI items
        self.current_paste_index = 0 # Index for sequential paste
        self.current_copy_index = 0 # Index for sequential copy
        self.current_paste_mode = PASTE_MODE_NONE # Mode from Radiobuttons
        self.orderly_hotkeys_registered = False
        self.paste_in_progress = False # Flag to prevent re-triggering paste during execution
        self.copy_in_progress = False # Flag to prevent re-triggering copy during execution
        self.pasted_item_indices = set() # Keep track of indices already pasted in the current sequence

        # Regex patterns for extraction (kept here as they relate to extraction UI)
        self.eof_start_pattern = re.compile(r"^\s*cat\s+<<\s*'EOF'\s+>\s*(.+)$")
        self.eof_end_pattern = re.compile(r"^\s*EOF\s*$")
        self.sed_pattern = re.compile(r"^\s*sed\s+-i\s+.*$")

        # Load initial data but don't build UI yet
        self._load_multiclip_data() # Load data on init
        self._reset_sequential_indices() # Initialize indices

        print("OrderlyApp initialized.")

    # --- Mode Activation/Deactivation (Toggled by Multiclip GUI button or Global Hotkey) ---
    # This method is called externally by multiclip.py
    def toggle_mode(self):
        """Activates or deactivates Orderly mode and shows/hides UI."""
        if self.paste_in_progress or self.copy_in_progress:
            print("Hold up, paste/copy action in progress. Try toggling again shortly.")
            show_toast("Orderly Busy", "Wait for current action to finish.")
            return

        if not self.is_active:
            print("Activating Orderly mode...")
            # Check file exists only on activation attempt
            if not os.path.exists(MULTICLIP_DICT_FILE):
                show_toast("Orderly Error", f"Multiclip data file not found:\n{MULTICLIP_DICT_FILE}\nMake sure Multiclip is set up.")
                print(f"[!] Multiclip dictionary not found at {MULTICLIP_DICT_FILE}. Orderly needs this.")
                return # Cannot activate without the dictionary file

            self.is_active = True
            show_toast("Orderly Activated", f"Mode ON.") # Hotkey info is handled by Multiclip start message
            # Launch UI in a separate thread to avoid blocking the main thread (where keyboard listener runs)
            self.ui_thread = Thread(target=self.build_and_run_ui, daemon=True)
            self.ui_thread.start()
            # Give UI thread a moment to start and build window
            time.sleep(0.2)
            self.register_orderly_hotkeys() # Register Ctrl+C/V/Shift+V hooks *only* when active
            self._reset_sequential_indices() # Reset sequence on activation
            self.pasted_item_indices = set() # Clear pasted history on activation

        else:
            print("Deactivating Orderly mode...")
            self.is_active = False
            self.unregister_orderly_hotkeys() # Unregister hotkeys when inactive
            # Schedule window destruction from the main thread if UI thread is separate
            if self.root and self.root.winfo_exists():
                try:
                    # Signaling quit first can help mainloop exit cleanly
                    self.root.after(0, self.root.quit)
                    # Destroy the window shortly after
                    self.root.after(10, self.root.destroy)
                except tk.TclError as e:
                    print(f"Error closing UI window: {e}")
                self.root = None
                self.sequential_slots_data = [] # Clear displayed data

            show_toast("Orderly Deactivated", "Mode OFF.")
            print("Orderly mode deactivated.")

    # --- UI Management ---
    def build_and_run_ui(self):
        """Builds and runs the Tkinter UI for Orderly mode."""
        # Check if a window already exists and is active
        if self.root is not None and self.root.winfo_exists():
             print("Orderly UI window already exists. Attempting to focus.")
             self.root.lift()
             self.root.focus_force()
             return

        try:
            # Create a Toplevel window, linking it to the master if provided
            # If master is None (running standalone), tk.Toplevel acts like Tk
            self.root = tk.Toplevel(self.master)
            self.root.title("Orderly Sequence")
            # Make sure it stays on top
            self.root.attributes('-topmost', True)
            # Bind closing the window to deactivating the mode
            self.root.protocol("WM_DELETE_WINDOW", self.handle_window_close)

            # Set geometry (can be adjusted)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = 300 # Narrower width
            window_height = 500 # Decent height
            x_pos = screen_width - window_width - 60 # Position towards right (adjust value)
            y_pos = 60 # Position towards top (adjust value)
            self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")


            # --- Top Controls Frame ---
            controls_frame = ttk.Frame(self.root, padding="5")
            controls_frame.pack(side=tk.TOP, fill=tk.X)

            # Check/Uncheck Buttons
            btn_check_all = ttk.Button(controls_frame, text="Check All", command=lambda: self.check_uncheck_all(True))
            btn_check_all.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
            btn_uncheck_all = ttk.Button(controls_frame, text="Uncheck All", command=lambda: self.check_uncheck_all(False))
            btn_uncheck_all.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

            # Refresh Button
            btn_refresh = ttk.Button(controls_frame, text="Refresh", command=self.load_and_display_data)
            btn_refresh.pack(side=tk.TOP, fill=tk.X, pady=(5, 0)) # Put Refresh below Check/Uncheck
            ToolTip(btn_refresh, "Reload slot 1-0 content from Multiclip's saved data file.")


            # --- Extraction Frame ---
            extraction_frame = ttk.LabelFrame(self.root, text="Command Extraction", padding="5")
            extraction_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(5,0))

            extract_button = ttk.Button(extraction_frame, text="Extract EOF/SED from File...", command=self.trigger_extraction)
            extract_button.pack(fill=tk.X)
            ToolTip(extract_button, "Select a file to scan for 'cat << EOF > ...' blocks\nand 'sed -i ...' commands. Found commands\nwill overwrite slots 1-0 in Multiclip and this list.")

            # --- Paste Mode Selection ---
            self.paste_mode_var = tk.IntVar(value=PASTE_MODE_NONE)
            mode_frame = ttk.LabelFrame(self.root, text="Paste Mode", padding="5")
            mode_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

            rb_mode_none = ttk.Radiobutton(mode_frame, text="Disabled", variable=self.paste_mode_var, value=PASTE_MODE_NONE, command=self.update_paste_mode)
            rb_mode_none.pack(anchor=tk.W)
            ToolTip(rb_mode_none, "Orderly is idle. Ctrl+V and Ctrl+Shift+V work normally.")

            rb_mode_ctrlv = ttk.Radiobutton(mode_frame, text="Sequential Ctrl+V", variable=self.paste_mode_var, value=PASTE_MODE_SEQ_CTRL_V, command=self.update_paste_mode)
            rb_mode_ctrlv.pack(anchor=tk.W)
            ToolTip(rb_mode_ctrlv, "Paste checked items one by one using Ctrl+V.\nHighlight moves to the next item after each paste.")

            rb_mode_ctrlshiftv = ttk.Radiobutton(mode_frame, text="Sequential Ctrl+Shift+V (Terminal)", variable=self.paste_mode_var, value=PASTE_MODE_SEQ_CTRL_SHIFT_V, command=self.update_paste_mode)
            rb_mode_ctrlshiftv.pack(anchor=tk.W)
            ToolTip(rb_mode_ctrlshiftv, "Paste checked items one by one using Ctrl+Shift+V.\nUse this for pasting commands into most terminals.")


            # --- Slot List Frame ---
            # Using Treeview for a cleaner look like in the (potential) Snippets viewer
            list_container_frame = ttk.Frame(self.root, padding="5")
            list_container_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

            slot_list_label = ttk.Label(list_container_frame, text="Sequential Slots (Checked for Paste):")
            slot_list_label.pack(side=tk.TOP, anchor=tk.W)

            self.slot_tree = ttk.Treeview(list_container_frame, columns=('Content',), show='headings')
            self.slot_tree.heading('Content', text='Content Preview', anchor=tk.W)
            # Adjust width later based on actual window size if needed, stretch to fill
            self.slot_tree.column('Content', width=window_width - 30, stretch=tk.YES)

            # Add a scrollbar
            scrollbar = ttk.Scrollbar(list_container_frame, orient=tk.VERTICAL, command=self.slot_tree.yview)
            self.slot_tree.configure(yscrollcommand=scrollbar.set)

            # Pack treeview and scrollbar
            self.slot_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.load_and_display_data() # Initial load and display

            # Start the Tkinter event loop for this window
            self.root.mainloop()
            print("Orderly UI main loop finished.")

        except Exception as e:
            print(f"[!] Fatal error building or running Orderly UI: {e}")
            show_toast("Orderly UI Error", "Could not display Orderly window.")
            # Attempt graceful shutdown if mode was active when error occurred
            if self.is_active:
                # Schedule deactivation on the main thread if possible, otherwise just print
                print("Attempting to deactivate orderly mode after UI error...")
                self.is_active = False # Force state change
                self.unregister_orderly_hotkeys()
                print("Orderly mode forcefully deactivated.")


    def handle_window_close(self):
        """Handles closing the Orderly UI window."""
        print("Orderly window closed by user.")
        # Deactivating mode handles unregistering hotkeys and cleaning up
        if self.is_active:
            self.toggle_mode() # This sets self.is_active = False and unregisters hotkeys

    def _load_multiclip_data(self):
        """Loads ALL data from Multiclip JSON into self.multiclip_data."""
        print("Loading full Multiclip data...")
        self.multiclip_data = load_dictionary()
        print(f"Loaded {len(self.multiclip_data)} total items from dictionary.")
        # This does NOT populate the sequential_slots_data list or refresh the UI
        # That's handled by load_and_display_data or refresh calls.

    def load_and_display_data(self):
        """Loads the relevant sequential slots data and populates the Treeview display."""
        print("Loading Multiclip sequential slot data for display...")
        self._load_multiclip_data() # Ensure we have the latest data

        # Clear existing items in the treeview
        for i in self.slot_tree.get_children():
            self.slot_tree.delete(i)

        self.sequential_slots_data = [] # Clear the list that holds item data for the UI

        if not self.multiclip_data: # Handle case where full dictionary is empty
             self.slot_tree.insert('', 'end', values=('Multiclip data is empty or file not found.',))
             self._reset_sequential_indices() # Reset indices if no data
             self.pasted_item_indices = set() # Clear pasted history
             return

        # Populate sequential_slots_data list and Treeview in the desired order (slot_1 to slot_9, then slot_0)
        for index, slot_name in enumerate(SEQUENTIAL_SLOT_NAMES):
            content = self.multiclip_data.get(slot_name, "*Empty*")
            # Create a preview, handle multiple lines and length
            preview = content.split('\n')[0][:70] + ('...' if len(content) > 70 or '\n' in content else '')

            item_data = {
                'slot_name': slot_name,
                'content': content,
                'is_checked': tk.BooleanVar(value=False), # Checkbox state
                'tree_item_id': None # Will store the ID of the item in the treeview
            }
            self.sequential_slots_data.append(item_data)

            # Insert into Treeview and store the item ID
            slot_display_name = slot_name.replace('slot_', 'Slot ')
            item_id = self.slot_tree.insert('', 'end', values=(f"{slot_display_name}: {preview}",))
            item_data['tree_item_id'] = item_id

             # Add a checkbox column? Treeview doesn't support checkboxes directly easily.
             # Using the Checkbutton widget is easier in a standard Frame list,
             # but we switched to Treeview. Let's handle selection state updates
             # internally or via external Checkbuttons if we revert UI approach.
             # For now, selection state is just tracked internally with 'is_checked'.

        # Bind double-click on Treeview items to toggle 'checked' state and update display
        # This replaces the original checkbox functionality for the Treeview
        self.slot_tree.bind('<Double-1>', self.on_tree_double_click)


        self._reset_sequential_indices() # Reset indices on data load/refresh
        self.pasted_item_indices = set() # Clear pasted history on data load/refresh
        self.update_display_highlighting() # Update highlighting based on current state
        print(f"Displayed {len(self.sequential_slots_data)} sequential slots.")


    def on_tree_double_click(self, event):
        """Handles double-clicking an item in the Treeview to toggle its checked state."""
        if self.paste_in_progress or self.copy_in_progress: return # Don't allow changes during operation

        item_id = self.slot_tree.identify_row(event.y)
        if not item_id: return # Click was not on an item

        # Find the item_data corresponding to the clicked tree item ID
        clicked_item = next((item for item in self.sequential_slots_data if item['tree_item_id'] == item_id), None)

        if clicked_item:
            # Toggle the 'is_checked' state
            clicked_item['is_checked'].set(not clicked_item['is_checked'].get())
            print(f"Toggled checked state for {clicked_item['slot_name']} to {clicked_item['is_checked'].get()}")
            self.update_display_highlighting() # Update colors based on new state
            self._reset_paste_index() # Reset paste index when selection changes
            self.pasted_item_indices = set() # Clear pasted history when selection changes


    def check_uncheck_all(self, state):
        """Checks or unchecks all items in the list."""
        if self.paste_in_progress or self.copy_in_progress: return
        print(f"{'Checking' if state else 'Unchecking'} all items.")
        for item_data in self.sequential_slots_data:
            if item_data['is_checked'].winfo_exists(): # Check if the BooleanVar widget exists (should always in this setup)
                 item_data['is_checked'].set(state)
        self.update_display_highlighting() # Update colors
        self._reset_paste_index() # Reset paste index when selection changes
        self.pasted_item_indices = set() # Clear pasted history when selection changes


    def update_paste_mode(self):
        """Updates the current paste mode based on radio button selection."""
        if self.paste_in_progress or self.copy_in_progress: return
        if hasattr(self, 'paste_mode_var') and self.paste_mode_var.winfo_exists():
            self.current_paste_mode = self.paste_mode_var.get()
            mode_map = {0: "Disabled", 1: "Sequential Ctrl+V", 2: "Sequential Ctrl+Shift+V", 3: "Direct"}
            print(f"Orderly Paste mode set to: {mode_map.get(self.current_paste_mode, 'Unknown')}")
            self._reset_paste_index() # Reset paste index when mode changes
            self.pasted_item_indices = set() # Clear pasted history when mode changes
        else:
            print("Paste mode variable not accessible, cannot update mode.")


    def _reset_sequential_indices(self):
        """Resets the sequential copy and paste indices."""
        self.current_copy_index = 0
        self.current_paste_index = 0
        print("Sequential copy/paste indices reset.")
        self.update_display_highlighting() # Update highlighting after reset


    def update_display_highlighting(self):
        """Visually highlights the current paste item and marks pasted items."""
        if not self.root or not self.root.winfo_exists() or not self.is_active or not self.sequential_slots_data:
            # print("Highlighting skipped: UI not ready or mode inactive.") # Too chatty
            return

        try:
            # Find the list of items that are checked for sequential paste
            checked_items = [item for item in self.sequential_slots_data if item['is_checked'].get()]

            for i, item_data in enumerate(self.sequential_slots_data):
                tree_item_id = item_data['tree_item_id']
                if not self.slot_tree.exists(tree_item_id):
                    # print(f"Skipping highlighting for destroyed tree item: {tree_item_id}") # Debug
                    continue # Skip if the Treeview item no longer exists

                is_checked = item_data['is_checked'].get()
                # Default colors
                bg_color = '' # Use system default Treeview row background
                fg_color = 'black'
                font_weight = 'normal'
                tags = () # Reset tags

                # Find the index of this item within the *checked* list
                try:
                    index_in_checked = checked_items.index(item_data) if is_checked else -1
                except ValueError:
                     index_in_checked = -1 # Should not happen if is_checked is True

                if is_checked:
                    if index_in_checked == self.current_paste_index:
                        # Highlight the item currently targeted for pasting
                        tags = ('current_paste',)
                        # Treeview row background color is tricky with default themes.
                        # Using tags and styling can be more reliable than setting bg directly on item.
                        # ttk Style configuration would be needed, or we just change text color/font.
                        fg_color = 'blue' # Indicate current with text color
                        font_weight = 'bold'
                    elif item_data['slot_name'] in self.pasted_item_indices:
                        # Mark items that have already been pasted in this sequence
                        tags = ('pasted',)
                        fg_color = 'grey' # Indicate pasted with text color

                else: # Not checked
                     # Make text grey if unchecked
                     fg_color = 'grey'


                # Apply the determined colors and tags to the Treeview item
                # Ensure we update the item's display properties via the Treeview API
                current_values = self.slot_tree.item(tree_item_id, 'values')
                self.slot_tree.item(tree_item_id, values=current_values, tags=tags)

                # Need to update text color/font on the label inside the cell if direct item config doesn't work well.
                # Treeview styling for cell text color/font usually requires defining styles based on tags.
                # Let's define basic styles for the tags.
                style = ttk.Style()
                style.configure('current_paste', foreground='blue', font=('TkDefaultFont', 9, 'bold'))
                style.configure('pasted', foreground='grey') # Use default font size, just change color
                # Default style for unchecked? Treeview handles default text color usually.
                # Might need a specific style if default isn't black when not tagged.


        except tk.TclError as e:
            print(f"[ERROR] Error during Orderly highlighting (likely widget destroyed): {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error during Orderly highlighting: {e}")


    # --- Pasting Logic (Sequential) ---
    def paste_sequential(self, use_ctrl_shift_v=False):
        """
        Pastes the next item in the checked sequence.
        Returns True if the hotkey should NOT be suppressed, False if it was handled.
        """
        # Block if Ordely mode is not active, or if another paste/copy is in progress
        if not self.is_active or self.paste_in_progress or self.copy_in_progress:
            return True # Let the original key combo pass through

        # Check if the mode is correct for the triggered action
        correct_mode = (use_ctrl_shift_v and self.current_paste_mode == PASTE_MODE_SEQ_CTRL_SHIFT_V) or \
                       (not use_ctrl_shift_v and self.current_paste_mode == PASTE_MODE_SEQ_CTRL_V)

        if not correct_mode:
             # print(f"Paste skipped: Mode ({self.current_paste_mode}) doesn't match trigger ({'Ctrl+Shift+V' if use_ctrl_shift_v else 'Ctrl+V'}).") # Too chatty
             return True # Let the original key combo pass through

        # Ensure UI and data are ready
        if not self.root or not self.root.winfo_exists() or not self.sequential_slots_data:
             print("Paste skipped: Orderly UI not ready.")
             show_toast("Orderly Paste Error", "UI not ready.") # Notify user if trying to paste before UI is up
             return False # Handled the hotkey press by suppressing

        # Get the list of items that are currently checked for sequential paste
        checked_items = [item for item in self.sequential_slots_data if item['is_checked'].get()]

        if not checked_items:
            print("No items checked for sequential pasting.")
            show_toast("Orderly Paste", "No items selected in sequence.")
            self._reset_paste_index() # Ensure index is 0 if nothing checked
            self.pasted_item_indices = set() # Clear history
            return False # Suppress original paste - Orderly handled the key press

        if self.current_paste_index >= len(checked_items):
            print("End of sequence reached.")
            show_toast("Orderly Paste", "End of sequence.")
            self._reset_paste_index() # Reset sequence index
            self.pasted_item_indices = set() # Clear pasted history for the new sequence
            self.update_display_highlighting() # Update UI to remove highlighting
            return False # Suppress original paste - Orderly handled the key press


        self.paste_in_progress = True # Set flag

        try:
            # Get the item data for the current sequential index
            item_to_paste = checked_items[self.current_paste_index]
            content = item_to_paste['content']
            slot_name = item_to_paste['slot_name']
            list_pos = self.current_paste_index + 1 # 1-based index for user feedback
            total_in_sequence = len(checked_items)

            print(f"Pasting item {list_pos}/{total_in_sequence} ('{slot_name}') via {'Ctrl+Shift+V' if use_ctrl_shift_v else 'Ctrl+V'}...")

            # Step 1: Copy content to the system clipboard
            pyperclip.copy(content)
            time.sleep(0.05) # Small delay for clipboard update

            # Step 2: Simulate paste hotkey
            # Ensure running as root warning is printed if needed
            if os.geteuid() == 0:
                print("[WARNING] Running as root. pyautogui.hotkey might not work reliably.")

            if use_ctrl_shift_v:
                pyautogui.hotkey('ctrl', 'shift', 'v')
                paste_method_name = "Ctrl+Shift+V"
            else:
                pyautogui.hotkey('ctrl', 'v')
                paste_method_name = "Ctrl+V"
            time.sleep(0.05) # Small delay after pasting

            # Step 3: Update state and UI *after* successful paste simulation
            show_toast("Orderly Paste", f"Pasted {list_pos}/{total_in_sequence} ({slot_name})\nvia {paste_method_name}")

            # Mark item as pasted and increment index
            self.pasted_item_indices.add(slot_name) # Mark the slot name as pasted
            self.current_paste_index += 1

            # Update UI highlighting for the next item or end state
            self.update_display_highlighting()

            # Optional: Bring the Orderly window to front after paste? Might be annoying.
            # if self.root and self.root.winfo_exists():
            #      self.root.lift()
            #      self.root.focus_force()


        except Exception as e:
            print(f"[ERROR] Error during sequential paste: {e}")
            show_toast("Orderly Paste Error", f"Failed to paste item {list_pos}: {e}")
             # Decide whether to stop sequence or try next? Let's stop for now.
            self._reset_paste_index()
            self.pasted_item_indices = set()
            self.update_display_highlighting()

        finally:
            self.paste_in_progress = False # Release flag

        return False # We handled the key, suppress original paste


    # --- Copy Logic (Sequential) ---
    def handle_ctrl_c(self, event):
        """
        Handles Ctrl+C press when Orderly mode is active.
        Copies current clipboard content to the next sequential slot.
        Returns True if the hotkey should NOT be suppressed, False if it was handled.
        """
        # Block if Orderly mode is not active, or if another copy/paste is in progress
        if not self.is_active or self.copy_in_progress or self.paste_in_progress:
            return True # Let the original Ctrl+C pass through

        self.copy_in_progress = True # Set flag

        try:
            # Step 1: Simulate Ctrl+C to copy (This should ideally already be done by the user press,
            # but simulating again ensures the very latest content is captured after hook processing)
            if os.geteuid() == 0:
                print("[WARNING] Running as root. pyautogui.hotkey might not work in all environments.")
            pyautogui.hotkey("ctrl", "c")
            time.sleep(0.05) # Give system time to update clipboard

            # Step 2: Get clipboard content
            clipboard_content = pyperclip.paste()

            # Check if clipboard content is empty after copy simulation
            if not clipboard_content.strip():
                print("Clipboard empty after Ctrl+C simulation. Skipping sequential save.")
                # show_toast("Copy Skipped", "Clipboard empty") # Too chatty maybe
                return False # Suppress Ctrl+C if Orderly is active but clipboard is empty

            # Step 3: Find the next sequential slot index for copying
            # Wrap around if all slots are filled
            next_slot_index = self.current_copy_index % NUM_SEQUENTIAL_SLOTS
            slot_name = SEQUENTIAL_SLOT_NAMES[next_slot_index]

            # Step 4: Load dictionary, update slot, save dictionary
            dictionary = load_dictionary()
            dictionary[slot_name] = clipboard_content
            save_dictionary(dictionary)

            # Step 5: Update state and UI
            show_toast("Orderly Copy", f"Copied to Slot {slot_name.replace('slot_', '')}") # Notify which slot was filled
            print(f"Orderly copied to {slot_name}: {clipboard_content.splitlines()[0][:50]}...")

            self.current_copy_index += 1 # Move to the next slot for the *next* copy

            # Optional: Update the list display in the UI to show the new content?
            # This might be slow if done on every copy. Refresh button is safer.
            # self.load_and_display_data() # Avoid frequent refreshes

        except Exception as e:
            print(f"[ERROR] Error during sequential copy (Ctrl+C handler): {e}")
            show_toast("Orderly Copy Error", "Failed sequential copy.")

        finally:
            self.copy_in_progress = False # Release flag

        return False # We handled the key, suppress original Ctrl+C behavior


    # START ### COMMAND EXTRACTION LOGIC (Kept local to Orderly UI) ###
    # This logic is triggered by a button press *within* the Orderly GUI

    def trigger_extraction(self):
        """Handles the 'Extract Commands' button click."""
        # Orderly mode must be active to trigger extraction via UI
        if not self.is_active:
            show_toast("Orderly Inactive", "Activate Orderly first.")
            return

        print("Triggering command extraction...")
        # File dialog runs on the UI thread
        file_path = filedialog.askopenfilename(
            title="Select File to Extract Commands From",
            initialdir=os.path.expanduser("~"), # Start dialog in user's home directory
            filetypes=(("Text files", "*.txt"),
                       ("Shell scripts", "*.sh"),
                       ("Python files", "*.py"),
                       ("All files", "*.*"))
        )

        if not file_path:
            print("File selection cancelled.")
            return

        print(f"Attempting to extract EOF/SED commands from: {file_path}")
        # Extraction logic runs on the UI thread
        extracted_commands = self.extract_commands_from_file(file_path)

        if not extracted_commands:
            show_toast("Extraction Result", f"No EOF or SED commands found in\n{os.path.basename(file_path)}")
            print("No commands found.")
            return

        num_extracted = len(extracted_commands)
        # We only load into the NUM_SEQUENTIAL_SLOTS (first 10, slot_1 to slot_0)
        num_to_load = min(num_extracted, NUM_SEQUENTIAL_SLOTS)

        # Confirmation before overwriting (runs on UI thread)
        confirm = messagebox.askyesno(
             "Confirm Overwrite",
             f"Found {num_extracted} commands.\nThis will OVERWRITE Multiclip slots 1-9 and 0 with the first {num_to_load} commands.\n\nProceed?"
        )

        if not confirm:
            print("Overwrite cancelled by user.")
            show_toast("Extraction Cancelled", "Overwrite operation cancelled.")
            return

        print(f"Loading first {num_to_load} of {num_extracted} commands into slots 1-0...")
        # Loading logic runs on the UI thread
        self.load_commands_into_slots(extracted_commands[:num_to_load])

        # Notify user (runs on UI thread)
        result_message = f"Extracted {num_extracted} commands.\nLoaded first {num_to_load} into slots 1-0."
        if num_extracted > NUM_SEQUENTIAL_SLOTS:
             result_message += f"\n(More than {NUM_SEQUENTIAL_SLOTS} found, only first {NUM_SEQUENTIAL_SLOTS} loaded)"
        show_toast("Extraction Complete", result_message)
        print(result_message)

        # Refresh the UI list to show the new content (runs on UI thread)
        self.load_and_display_data()
        self._reset_sequential_indices() # Reset copy/paste sequence after loading new data
        self.pasted_item_indices = set() # Clear pasted history


    def extract_commands_from_file(self, file_path):
        """Scans a file for EOF blocks and SED commands."""
        commands = []
        try:
            with open(file_path, "r", encoding='utf-8', errors='ignore') as infile:
                current_eof_block = []
                in_eof_block = False
                target_filename = ""

                for line in infile:
                    # Check for SED command first
                    sed_match = self.sed_pattern.match(line)
                    if sed_match and not in_eof_block:
                        commands.append(line.strip())
                        continue

                    # Check for EOF block start/end
                    eof_start_match = self.eof_start_pattern.match(line)
                    eof_end_match = self.eof_end_pattern.match(line)

                    if eof_start_match:
                        if in_eof_block:
                            print(f"Warning: New EOF start found before previous one ended for '{target_filename}'. Starting new block.")
                        in_eof_block = True
                        # Capture filename, stripping any surrounding quotes or whitespace
                        target_filename = eof_start_match.group(1).strip().strip("'\"")
                        current_eof_block = [line]
                    elif eof_end_match and in_eof_block:
                        current_eof_block.append(line)
                        commands.append("".join(current_eof_block))
                        in_eof_block = False
                        current_eof_block = []
                    elif in_eof_block:
                        current_eof_block.append(line)

            if in_eof_block:
                 print(f"Warning: Reached end of file, but EOF block for '{target_filename}' was not closed. Ignoring incomplete block.")

        except Exception as e:
            print(f"[!] Error reading or parsing file {file_path}: {e}")
            show_toast("Extraction Error", f"Failed to read/parse file:\n{os.path.basename(file_path)}")
            return []

        print(f"Extraction finished. Found {len(commands)} commands total.")
        return commands


    def load_commands_into_slots(self, command_list):
        """Loads the provided list of command strings into the sequential slots (1-0)."""
        if not command_list:
            print("No commands provided to load into slots.")
            return

        # Load the full dictionary, we're only modifying the sequential slots
        dictionary = load_dictionary()
        target_slots = SEQUENTIAL_SLOT_NAMES

        # Optional: Clear the target slots first? Safer if user expects a clean load.
        # for slot in target_slots:
        #     dictionary[slot] = "" # Clear existing content in these slots

        for i, command in enumerate(command_list):
            # The list might be shorter than target_slots if num_to_load was less than 10
            if i < len(target_slots):
                slot_name = target_slots[i]
                dictionary[slot_name] = command
                # print(f"  - Loaded into {slot_name} (preview: {command.splitlines()[0][:50]}...)") # Too chatty
            else:
                 # Should not happen due to min(num_extracted, NUM_SEQUENTIAL_SLOTS) slicing
                 print(f"Warning: Attempted to load command beyond sequential slots limit ({NUM_SEQUENTIAL_SLOTS}).")


        save_dictionary(dictionary) # Save the modified dictionary
        print(f"Updated Multiclip dictionary saved with {len(command_list)} extracted commands in sequential slots.")

    # FINISH ### COMMAND EXTRACTION LOGIC ###


    # --- Hotkey Management ---
    def register_orderly_hotkeys(self):
        """
        Registers hooks for Ctrl+C, Ctrl+V, Ctrl+Shift+V that check if Orderly
        mode is active before potentially suppressing and handling the hotkey.
        """
        if self.orderly_hotkeys_registered: return
        try:
            # Use hook_key with suppress=False so our handler ALWAYS runs first.
            # Our handler then checks self.is_active and the mode, and decides
            # whether to perform the Orderly action and return False (suppress original)
            # or do nothing and return True (let original hotkey run).
            keyboard.hook_key('ctrl+c', self._handle_keydown_wrapper(self.handle_ctrl_c), suppress=False)
            keyboard.hook_key('ctrl+v', self._handle_keydown_wrapper(self.handle_ctrl_v), suppress=False)
            keyboard.hook_key('ctrl+shift+v', self._handle_keydown_wrapper(self.handle_ctrl_shift_v), suppress=False)

            self.orderly_hotkeys_registered = True
            print("Orderly hotkeys registered (Ctrl+C, Ctrl+V, Ctrl+Shift+V hooks active).")
        except Exception as e:
            print(f"[ERROR] Failed to register Orderly hotkeys: {e}")
            show_toast("Orderly Hotkey Error", "Failed to register sequence hotkeys.")


    def unregister_orderly_hotkeys(self):
        """Unregisters the Orderly specific hotkey hooks."""
        if not self.orderly_hotkeys_registered: return
        try:
            keyboard.unhook_key('ctrl+c')
            keyboard.unhook_key('ctrl+v')
            keyboard.unhook_key('ctrl+shift+v')
            self.orderly_hotkeys_registered = False
            print("Orderly hotkeys unregistered.")
        except Exception as e:
             print(f"[WARNING] Failed to unregister Orderly hotkeys cleanly: {e}")


    # Wrapper to ensure we only process key down events from the hook
    def _handle_keydown_wrapper(self, target_handler):
        def handler(event):
            # Ensure we only act on the key *down* event, not key up
            if event.event_type == keyboard.KEY_DOWN:
                # Call the specific handler (handle_ctrl_c, handle_ctrl_v, etc.)
                # and return its result to the hook_key suppress parameter.
                return target_handler(event)
            # For key up events or if the handler didn't run, don't suppress
            return True # Let key up events pass through

        return handler


    # Handlers for the hotkeys (called by the wrapper if keydown)
    # These decide if the hotkey should be suppressed and handled by Orderly


    def handle_ctrl_v(self, event):
        """Handles Ctrl+V keydown. Pastes sequentially if mode is active."""
        # paste_sequential() returns False if it handled the paste (meaning suppress original Ctrl+V)
        # and True if it didn't handle it (meaning let original Ctrl+V pass through)
        return not self.paste_sequential(use_ctrl_shift_v=False)


    def handle_ctrl_shift_v(self, event):
        """Handles Ctrl+Shift+V keydown. Pastes sequentially (terminal mode) if active."""
        # paste_sequential() returns False if it handled the paste (meaning suppress original Ctrl+Shift+V)
        # and True if it didn't handle it (meaning let original Ctrl+Shift+V pass through)
        return not self.paste_sequential(use_ctrl_shift_v=True)

    # handle_ctrl_c logic is implemented above within the sequential copy section


# FINISH ### HOTKEY MANAGEMENT ###


# START ### MAIN EXECUTION ###
def main(master=None):
    """
    Main function to run the Orderly application.
    Accepts an optional Tkinter master window reference.
    """
    global orderly_app_instance

    # Check if an instance already exists and mode is active
    if orderly_app_instance and orderly_app_instance.is_active:
         print("Orderly mode is already active.")
         # If active and UI exists, try to bring it to front
         if orderly_app_instance.root and orderly_app_instance.root.winfo_exists():
              orderly_app_instance.root.lift()
              orderly_app_instance.root.focus_force()
         else:
             # If active but UI is gone, something is wrong, maybe re-toggle?
             print("Orderly mode active but UI window missing. Attempting to re-toggle.")
             orderly_app_instance.toggle_mode() # Deactivate and reactivate
         return # Exit if already active and handled

    # Check if an instance exists but mode is *not* active
    if orderly_app_instance and not orderly_app_instance.is_active:
         print("Orderly instance exists but is inactive. Activating mode.")
         orderly_app_instance.toggle_mode() # Just toggle the existing instance
         return # Exit after toggling

    # If no instance exists, create a new one
    print("--- Orderly Clipboard Sequencer Starting ---")
    print(f"Multiclip data file: {MULTICLIP_DICT_FILE}")

    # Create a hidden root window if running standalone and no master provided.
    # This is needed for Tkinter to run in the background.
    # If run by multiclip.py, master will be provided and this hidden root is not used.
    hidden_root = None
    if master is None:
         print("Running standalone, creating hidden root window.")
         hidden_root = tk.Tk()
         hidden_root.withdraw() # Hide the main window
         master = hidden_root # Use the hidden root as the master for OrderlyApp

    # Create the OrderlyApp instance
    orderly_app_instance = OrderlyApp(master=master)

    # The OrderlyApp instance will register its own hotkeys and build its UI
    # when toggle_mode() is called.

    # If running standalone, we need to listen for the initial toggle hotkey.
    # If launched by multiclip, multiclip handles the global hotkey to call main(root).
    # However, Orderly needs its *own* hotkey hooks (Ctrl+C/V/Shift+V) active
    # *only when its mode is ON*. The toggle_mode method handles this.

    # We need to keep the script running in the background to listen for hotkeys.
    # If launched standalone, keyboard.wait() does this.
    # If launched by multiclip, the multiclip script is already doing this.
    # The simplest is to let the OrderlyApp instance manage its own state and hooks.
    # The initial toggle hotkey must be registered *globally*. This should happen
    # in the main multiclip.py script.

    # For standalone testing: Register the toggle hotkey and wait for it.
    # This block will NOT run if launched via Popen by multiclip.py
    if hidden_root:
        try:
            # Register the global toggle hotkey for standalone testing
            toggle_hotkey_str = "ctrl+alt+o" # Keep the config variable local to class?
            keyboard.add_hotkey(toggle_hotkey_str, lambda: orderly_app_instance.toggle_mode())
            print(f"Global toggle hotkey '{toggle_hotkey_str}' registered (standalone mode).")

            print("Orderly is running in the background (standalone). Waiting for activation...")
            # Use keyboard.wait() to keep listening
            keyboard.wait()
        except KeyboardInterrupt:
            print("\nCtrl+C detected. Shutting down.")
        except Exception as e:
            print(f"\nKeyboard listener stopped unexpectedly: {e}")
            # show_toast("Orderly Error", "Keyboard listener crashed.") # Avoid toast on shutdown
        finally:
             print("--- Orderly Shutting Down (Standalone) ---")
             # Ensure proper cleanup
             if orderly_app_instance:
                  # Ensure hotkeys are unregistered and UI is closed
                  orderly_app_instance.unregister_orderly_hotkeys()
                  if orderly_app_instance.root and orderly_app_instance.root.winfo_exists():
                       try:
                            orderly_app_instance.root.after(0, orderly_app_instance.root.quit)
                            orderly_app_instance.root.after(10, orderly_app_instance.root.destroy)
                       except tk.TclError: pass
                  orderly_app_instance.root = None # Clear reference
                  orderly_app_instance.is_active = False # Ensure state is off
                  orderly_app_instance = None # Clear instance reference
             # Ensure the hidden root is destroyed
             if hidden_root and hidden_root.winfo_exists():
                  try: hidden_root.destroy()
                  except tk.TclError: pass
             print("Standalone cleanup complete. Peace.")

    # If launched by multiclip via Popen, this main function is called once.
    # The OrderlyApp is initialized, but the script needs to keep running
    # in the background for the hotkey listener. Popen keeps the script process alive.
    # The toggle hotkey press (handled by multiclip) will trigger toggle_mode(),
    # which runs the UI in a thread and registers/unregisters the hooks.

# If this script is run directly, execute main()
if __name__ == "__main__":
    # When run directly, call main. It will handle standalone setup.
    # If run by multiclip.py via Popen, this block runs, main() is called.
    # The multiclip.py script is responsible for registering the global hotkey
    # that calls the main() function here (or toggle_mode directly)
    # and keeping its own process alive with its own hotkey listener.
    # Let's make the main() function the entry point that gets called by Popen.
    main()
# FINISH ### MAIN EXECUTION ###