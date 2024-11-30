import pyperclip
import keyboard
import json
import os
import pyautogui
import time  # Import time to add delay

# Path to the dictionary file
dict_file = "clipboard_dict.json"

# Load the dictionary from the file if it exists, otherwise create an empty dictionary
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

# Function to add the current clipboard content to the dictionary
def add_to_dictionary(slot_name):
    # Simulate Ctrl+C to copy selected text
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)  # Add a small delay to ensure clipboard is updated
    clipboard_content = pyperclip.paste()  # Get the clipboard content after copying
    dictionary = load_dictionary()
    dictionary[slot_name] = clipboard_content
    save_dictionary(dictionary)
    print(f"Added to dictionary: {slot_name} -> {clipboard_content}")

# Function to paste the content from the dictionary
def paste_from_dictionary(slot_name):
    dictionary = load_dictionary()
    if slot_name in dictionary:
        pyperclip.copy(dictionary[slot_name])  # Copy the content to clipboard
        time.sleep(0.1)  # Add a small delay to ensure the clipboard has been updated
        pyautogui.hotkey('ctrl', 'v')  # Simulate pressing Ctrl+V to paste the clipboard content
        print(f"Pasted from dictionary: {slot_name} -> {dictionary[slot_name]}")
    else:
        print(f"No content found for {slot_name}.")

# Register hotkeys for adding and pasting content
keyboard.add_hotkey('ctrl+1', add_to_dictionary, args=['slot_1'])
keyboard.add_hotkey('ctrl+shift+1', paste_from_dictionary, args=['slot_1'])
keyboard.add_hotkey('ctrl+2', add_to_dictionary, args=['slot_2'])
keyboard.add_hotkey('ctrl+shift+2', paste_from_dictionary, args=['slot_2'])
keyboard.add_hotkey('ctrl+3', add_to_dictionary, args=['slot_3'])
keyboard.add_hotkey('ctrl+shift+3', paste_from_dictionary, args=['slot_3'])
keyboard.add_hotkey('ctrl+4', add_to_dictionary, args=['slot_4'])
keyboard.add_hotkey('ctrl+shift+4', paste_from_dictionary, args=['slot_4'])
keyboard.add_hotkey('ctrl+5', add_to_dictionary, args=['slot_5'])
keyboard.add_hotkey('ctrl+shift+5', paste_from_dictionary, args=['slot_5'])
keyboard.add_hotkey('ctrl+6', add_to_dictionary, args=['slot_6'])
keyboard.add_hotkey('ctrl+shift+6', paste_from_dictionary, args=['slot_6'])
keyboard.add_hotkey('ctrl+7', add_to_dictionary, args=['slot_7'])
keyboard.add_hotkey('ctrl+shift+7', paste_from_dictionary, args=['slot_7'])
keyboard.add_hotkey('ctrl+8', add_to_dictionary, args=['slot_8'])
keyboard.add_hotkey('ctrl+shift+8', paste_from_dictionary, args=['slot_8'])
keyboard.add_hotkey('ctrl+9', add_to_dictionary, args=['slot_9'])
keyboard.add_hotkey('ctrl+shift+9', paste_from_dictionary, args=['slot_9'])
keyboard.add_hotkey('ctrl+0', add_to_dictionary, args=['slot_0'])
keyboard.add_hotkey('ctrl+shift+0', paste_from_dictionary, args=['slot_0'])


print("Hotkey set: [Ctrl+1] adds selected text to [slot_1], [Ctrl+Shift+1] to paste [slot_1]")
print("Hotkey set: [Ctrl+2] adds selected text to [slot_2], [Ctrl+Shift+2] to paste [slot_2]")
print("Hotkey set: [Ctrl+3] adds selected text to [slot_3], [Ctrl+Shift+3] to paste [slot_3]")
print("Hotkey set: [Ctrl+4] adds selected text to [slot_4], [Ctrl+Shift+4] to paste [slot_4]")
print("Hotkey set: [Ctrl+5] adds selected text to [slot_5], [Ctrl+Shift+5] to paste [slot_5]")
print("Hotkey set: [Ctrl+6] adds selected text to [slot_6], [Ctrl+Shift+6] to paste [slot_6]")
print("Hotkey set: [Ctrl+7] adds selected text to [slot_7], [Ctrl+Shift+7] to paste [slot_7]")
print("Hotkey set: [Ctrl+8] adds selected text to [slot_8], [Ctrl+Shift+8] to paste [slot_8]")
print("Hotkey set: [Ctrl+9] adds selected text to [slot_9], [Ctrl+Shift+9] to paste [slot_9]")
print("Hotkey set: [Ctrl+0] adds selected text to [slot_0], [Ctrl+Shift+0] to paste [slot_0]")
keyboard.wait('esc')  # Wait for the Escape key to stop the script
