import pyperclip
import keyboard
import json
import os
import pyautogui
import subprocess
import time
import tkinter as tk

# Paths
dict_file = "/home/flintx/multiclip/clipboard_dict.json"  # Clipboard slots storage
icon_path = "/home/flintx/multiclip/chargers-icon.png"    # Custom icon path for notifications

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

# Function to display a toast notification using notify-send
def show_toast(title, message):
    """
    Displays a system notification using notify-send.
    """
    try:
        subprocess.run(["notify-send", "-i", icon_path, title, message, "-t", "4000"])
    except Exception as e:
        print(f"Error showing toast notification: {e}")

# Copy to clipboard slot
def add_to_dictionary(slot_name):
    try:
        pyautogui.hotkey("ctrl", "c")  # Simulate Ctrl+C to copy
        time.sleep(0.1)               # Delay to ensure clipboard updates
        clipboard_content = pyperclip.paste()
        dictionary = load_dictionary()
        dictionary[slot_name] = clipboard_content
        save_dictionary(dictionary)
        show_toast("Slot Updated", f"{slot_name.capitalize()} updated.")
        print(f"Copied to {slot_name}: {clipboard_content}")
    except Exception as e:
        print(f"Error copying to clipboard: {e}")

# Paste from clipboard slot
def paste_from_dictionary(slot_name):
    try:
        dictionary = load_dictionary()
        if slot_name in dictionary:
            content_to_paste = dictionary[slot_name]
            pyperclip.copy(content_to_paste)  # Copy content to clipboard
            time.sleep(0.1)                  # Delay to ensure clipboard updates
            pyautogui.hotkey("ctrl", "v")    # Simulate Ctrl+V to paste
            show_toast("Slot Pasted", f"Slot {slot_name[-1]} content pasted.")
            print(f"Pasted from {slot_name}: {content_to_paste}")
        else:
            show_toast("Slot Empty", f"No content found in {slot_name}.")
            print(f"No content found in {slot_name}.")
    except Exception as e:
        print(f"Error pasting from clipboard: {e}")

# Transfer slot content to default clipboard
def transfer_to_default(slot_name):
    try:
        dictionary = load_dictionary()
        if slot_name in dictionary:
            content_to_transfer = dictionary[slot_name]
            pyperclip.copy(content_to_transfer)  # Copy content to clipboard
            show_toast("Slot Transferred", f"{slot_name.capitalize()} contents transferred to default system clipboard.")
            print(f"Transferred {slot_name} content to default clipboard: {content_to_transfer}")
        else:
            show_toast("Slot Empty", f"No content found in {slot_name}.")
            print(f"No content found in {slot_name}.")
    except Exception as e:
        print(f"Error transferring clipboard content: {e}")

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
    """
    Registers all hotkeys for the application.
    """
    for i in range(10):  # Slots 0-9
        slot_name = f"slot_{i}"
        keyboard.add_hotkey(f"ctrl+{i}", add_to_dictionary, args=[slot_name])  # Copy hotkeys
        keyboard.add_hotkey(f"ctrl+shift+{i}", paste_from_dictionary, args=[slot_name])  # Paste hotkeys
        keyboard.add_hotkey(f"ctrl+alt+{i}", transfer_to_default, args=[slot_name])  # Transfer hotkeys

    # Show clipboard UI hotkey
    keyboard.add_hotkey("ctrl+shift+u", show_clipboard_ui)

    # Reserved hotkeys for future functionality
    print("Reserved: Ctrl + Shift + F1, F2, F3 for future toast position handling")

    print("Hotkeys registered:")

# Main
if __name__ == "__main__":
    print("Multiclip running with the following commands:")
    print("- Ctrl + 1-0: Copy to slot 1-0")
    print("- Ctrl + Shift + 1-0: Paste from slot 1-0")
    print("- Ctrl + Alt + 1-0: Transfer slot content to default clipboard")
    print("- Ctrl + Shift + U: Show clipboard UI")
    print("- Reserved: Ctrl + Shift + F1, F2, F3 for future toast position handling")
    register_hotkeys()
    print("Press Ctrl+C to exit.")
    while True:
        time.sleep(1)
