
# MultiClip

Create a Copy/Paste function with unique hotkeys that stores distinct text in up to 10 slots (clipboards). Each slot can be pasted using an assigned hotkey.


## Authors

- [@Matthew Trevino](https://github.com/m5trevino)


## Dependencies

The Python packages needed for MultiClip are as follows: 
 
PyAutoGUI
pyperclip
keyboard
## Step 1 [Poetry Installation]

Install MultiClip with:
#1 Poetry 
or 
#2 Manually 

Poetry Installation: 
Poetry is a dependency and package manager for Python.

You can install Poetry by using:

 ```bash
   curl -sSL https://install.python-poetry.org | python3 - 
```

 or 

 ```bash
sudo apt install python3-poetry
```
 
    
## Step 2 [Install MultiClip with Poetry]

Once Poetry is installed you can use it to install MultiClip.

#1  Run: In the main MultiClip dir
```bash
poetry install
``` 
#2 Run: 
```bash
 poetry shell
 ```
        
## Install dependencies manually. 

If you are having trouble installing or using Poetry you can install manually.

#1 run:
```bash 
python3 -m venv venv-multiclip
source ./venv/bin/activate
```

#2 run:
```bash
 "pip install -r requirements.txt"
```

 
## Usage/Examples
```bash
python3 multiclip.py
```
or 
```bash
python multiclip.py
```

To copy into Slot_1 select text and press [Control+1]
## Copy to [Slot_1] = [Control+1] 

To paste the contents of [Slot_1] press [Control+Shift+1]
## Paste from [Slot_1] = [Control+Shift+1]

Copy to [Slot_1] = [Control+1]  
Paste from [Slot_1] = [Control+Shift+1]

Copy to [Slot_2] = [Control+2]  
Paste from [Slot_2] = [Control+Shift+2]

Copy to [Slot_3] = [Control+3]  
Paste from [Slot_3] = [Control+Shift+3]

Copy to [Slot_4] = [Control+4]  
Paste from [Slot_4] = [Control+Shift+4]

Copy to [Slot_5] = [Control+5]  
Paste from [Slot_5] = [Control+Shift+5]

Copy to [Slot_6] = [Control+6]  
Paste from [Slot_6] = [Control+Shift+6]

Copy to [Slot_7] = [Control+7]  
Paste from [Slot_7] = [Control+Shift+7]

Copy to [Slot_8] = [Control+8]  
Paste from [Slot_8] = [Control+Shift+8]

Copy to [Slot_9] = [Control+9]  
Paste from [Slot_9] = [Control+Shift+9]

Copy to [Slot_0] = [Control+0]  
Paste from [Slot_0] = [Control+Shift+0]

