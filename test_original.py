import pyperclip
import keyboard
import json
import os
import pyautogui
import subprocess
import time

# Paths
dict_file = "/home/flintx/multiclip/clipboard_dict.json"
icon_path = "/home/flintx/multiclip/chargers.png"

def load_dictionary():
    if os.path.exists(dict_file):
        with open(dict_file, "r") as file:
            return json.load(file)
    else:
        return {}

def save_dictionary(dictionary):
    with open(dict_file, "w") as file:
        json.dump(dictionary, file, indent=4)

def show_toast(title, message):
    try:
        subprocess.run(["notify-send", "-i", icon_path, title, message, "-t", "4000"])
    except Exception as e:
        print(f"Error showing toast notification: {e}")

def add_to_dictionary(slot_name):
    try:
        print(f"DEBUG: Attempting to copy to {slot_name}")
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.1)
        clipboard_content = pyperclip.paste()
        print(f"DEBUG: Got clipboard content: {clipboard_content[:50]}...")
        
        dictionary = load_dictionary()
        dictionary[slot_name] = clipboard_content
        save_dictionary(dictionary)
        show_toast("Slot Updated", f"{slot_name.capitalize()} updated.")
        print(f"Copied to {slot_name}: {clipboard_content}")
    except Exception as e:
        print(f"Error copying to clipboard: {e}")

def paste_from_dictionary(slot_name):
    try:
        dictionary = load_dictionary()
        if slot_name in dictionary:
            content_to_paste = dictionary[slot_name]
            pyperclip.copy(content_to_paste)
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")
            show_toast("Slot Pasted", f"Slot {slot_name[-1]} content pasted.")
            print(f"Pasted from {slot_name}: {content_to_paste}")
        else:
            show_toast("Slot Empty", f"No content found in {slot_name}.")
            print(f"No content found in {slot_name}.")
    except Exception as e:
        print(f"Error pasting from clipboard: {e}")

def register_hotkeys():
    for i in range(1, 10):
        slot_name = f"slot_{i}"
        keyboard.add_hotkey(f"ctrl+{i}", add_to_dictionary, args=[slot_name])
        keyboard.add_hotkey(f"ctrl+shift+{i}", paste_from_dictionary, args=[slot_name])

    print("Hotkeys registered for Ctrl+1-9 (copy) and Ctrl+Shift+1-9 (paste)")

if __name__ == "__main__":
    print("Testing original multiclip logic...")
    register_hotkeys()
    print("Press Ctrl+C to exit.")
    while True:
        time.sleep(1)
