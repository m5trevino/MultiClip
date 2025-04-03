from PyHotKey import Key, keyboard
import time

# Flag to track if we should continue running
running = True

# Callback for when a key is pressed
def key_pressed(key, *args, **kwargs):
    print(f"Key pressed: {key}")
    # If Esc is pressed, set the flag to stop the loop
    if key == Key.esc:
        global running
        running = False

# Callback for when the Super key is pressed (we'll try different possible names)
def super_pressed(*args, **kwargs):
    print("Super key pressed!")

if __name__ == "__main__":
    # Print all available keys
    print("Available keys in PyHotKey:")
    for attr in dir(Key):
        if not attr.startswith('_'):  # Skip private attributes
            print(f"Key.{attr}")
    
    print("\nPress keys to see how they're detected. Press Esc to exit.")
    
    # Try to set magickeys for different possible Super key names
    try:
        keyboard.set_magickey_on_press(Key.cmd_l, super_pressed)
        print("Registered Key.cmd_l")
    except AttributeError:
        pass
    
    try:
        keyboard.set_magickey_on_press(Key.cmd, super_pressed)
        print("Registered Key.cmd")
    except AttributeError:
        pass
    
    try:
        keyboard.set_magickey_on_press(Key.meta, super_pressed)
        print("Registered Key.meta")
    except AttributeError:
        pass
    
    try:
        keyboard.set_magickey_on_press(Key.super, super_pressed)
        print("Registered Key.super")
    except AttributeError:
        pass
    
    # Set a magickey for Esc to exit
    keyboard.set_magickey_on_press(Key.esc, key_pressed, Key.esc)
    
    # Set magickeys for all keys to see what's pressed
    for attr in dir(Key):
        if not attr.startswith('_'):  # Skip private attributes
            try:
                key = getattr(Key, attr)
                keyboard.set_magickey_on_press(key, key_pressed, key)
            except (AttributeError, TypeError):
                pass
    
    try:
        # Keep the program running until Esc is pressed or Ctrl+C
        while running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        # Remove all magickeys
        keyboard.remove_all_magickeys()
        print("Exiting...")