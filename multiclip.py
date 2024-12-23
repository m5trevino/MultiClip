import pyperclip
import keyboard
import json
import os
import pyautogui
import time
import signal
import sys
import tkinter as tk

# Paths
dict_file = "/home/flintx/multiclip/clipboard_dict.json"  # Use an absolute path for consistency

# Load the dictionary from the file if it exists
def load_dictionary():
    if os.path.exists(dict_file):
        with open(dict_file, "r") as file:
            return json.load(file)
    else:
        return {}

# Save the dictionary to the file
def save_dictionary(dictionary):
    with open(dict_file, "w") as file:
        json.dump(dictionary, file, indent=4)

# Copy to clipboard slot
def add_to_dictionary(slot_name):
    try:
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.1)  # Delay to ensure clipboard updates
        clipboard_content = pyperclip.paste()
        dictionary = load_dictionary()
        dictionary[slot_name] = clipboard_content
        save_dictionary(dictionary)
        print(f"Copied to clipboard {slot_name}: {clipboard_content}")
    except Exception as e:
        print(f"Error copying to clipboard: {e}")

# Paste from clipboard slot
def paste_from_dictionary(slot_name):
    try:
        dictionary = load_dictionary()
        if slot_name in dictionary:
            content_to_paste = dictionary[slot_name]
            pyperclip.copy(content_to_paste)  # Copy content to clipboard
            time.sleep(0.1)  # Delay to ensure clipboard updates
            pyautogui.hotkey("ctrl", "v")  # Simulate Ctrl+V to paste
            print(f"Pasted from clipboard {slot_name}: {content_to_paste}")
        else:
            print(f"No content found in {slot_name}.")
    except Exception as e:
        print(f"Error pasting from clipboard: {e}")

# Show clipboard UI
def show_clipboard_ui():
    try:
        dictionary = load_dictionary()

        # Create the main window
        root = tk.Tk()
        root.title("Clipboard Manager")

        # Create a table-style UI
        tk.Label(root, text="Slot", font=("Arial", 12, "bold"), borderwidth=2, relief="ridge", width=15).grid(row=0, column=0)
        tk.Label(root, text="Content", font=("Arial", 12, "bold"), borderwidth=2, relief="ridge", width=50).grid(row=0, column=1)
        for idx, (slot, content) in enumerate(dictionary.items()):
            tk.Label(root, text=slot, font=("Arial", 10), borderwidth=2, relief="ridge", width=15).grid(row=idx+1, column=0)
            tk.Label(root, text=content, font=("Arial", 10), borderwidth=2, relief="ridge", width=50, anchor="w").grid(row=idx+1, column=1)

        # Add a close button
        tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12)).grid(row=len(dictionary)+1, column=0, columnspan=2, pady=10)

        root.mainloop()
    except Exception as e:
        print(f"Error displaying UI: {e}")

# Register hotkeys
def register_hotkeys():
    for i in range(10):
        slot_name = f"slot_{i}"
        keyboard.add_hotkey(f"ctrl+{i}", add_to_dictionary, args=[slot_name])  # Copy hotkeys
        keyboard.add_hotkey(f"ctrl+shift+{i}", paste_from_dictionary, args=[slot_name])  # Paste hotkeys
    keyboard.add_hotkey("ctrl+shift+u", show_clipboard_ui)  # UI table

# Main
if __name__ == "__main__":
    register_hotkeys()
    print("Multiclip running. Press Ctrl+C to stop.")
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    while True:
        time.sleep(1)
