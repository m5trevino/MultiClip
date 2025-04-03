# START ### IMPORTS ###
import pystray
from PIL import Image
import tkinter as tk
from typing import Callable
# FINISH ### IMPORTS ###

# START ### TRAY_IMPLEMENTATION ###
class MultiClipTray:
   def __init__(self, core):
     self.core = core
     self.icon = None
     self.setup_tray()

  def setup_tray(self):
    """Initialize system tray icon and menu"""
    try:
       image = Image.open("chargers-icon.png")
       self.icon = pystray.Icon(
          "multiclip",
          image,
          "MultiClip",
          self._create_menu()
       )
    except Exception as e:
       print(f"Error setting up tray: {e}")
       # Fallback to a blank icon if custom icon fails
       self.icon = pystray.Icon(
          "multiclip",
          self._create_default_image(),
          "MultiClip",
          self._create_menu()
       )

  def _create_default_image(self):
    """Create a default icon if custom icon fails to load"""
    image = Image.new('RGB', (64, 64), color='black')
    return image

  def _create_menu(self):
    """Create the system tray menu"""
    return pystray.Menu(
       pystray.MenuItem(
          "Sequential Mode",
          self._toggle_sequential_mode,
          checked=lambda _: self.core.sequential_mode
       ),
       pystray.MenuItem(
          "History",
          self._show_history
       ),
       pystray.MenuItem(
          "Settings",
          pystray.Menu(
            pystray.MenuItem(
                "Paste on Select",
                self._toggle_paste_on_select,
                checked=lambda _: self.core.config['paste_on_select']
            ),
            pystray.MenuItem(
                "Show Prompts",
                self._toggle_prompts,
                checked=lambda _: self.core.config['show_sequence_prompts']
            )
          )
       ),
␌         pystray.MenuItem("Quit", self._quit)
     )

  def _toggle_sequential_mode(self):
    """Toggle sequential paste mode"""
    self.core.sequential_mode = not self.core.sequential_mode
    self.core._save_state()

  def _show_history(self):
    """Show clipboard history window"""
    self.core.show_history()

  def _toggle_paste_on_select(self):
    """Toggle paste on select setting"""
    self.core.config['paste_on_select'] = not self.core.config['paste_on_select']
    self.core._save_state()

  def _toggle_prompts(self):
    """Toggle sequence prompts setting"""
    self.core.config['show_sequence_prompts'] = not self.core.config['show_sequence_prompts']
    self.core._save_state()

  def _quit(self):
    """Quit the application"""
    self.icon.stop()
    self.core.quit()

  def run(self):
     """Run the system tray icon"""
     self.icon.run()
# FINISH ### TRAY_IMPLEMENTATION ###
