import time
import pyperclip
from typing import List, Optional

# START ### IMPORTS ###
import keyboard
import json
import os
from datetime import datetime
from .utils.storage import ClipStorage
from .ui.tray import MultiClipTray
from .ui.toast import ToastManager
from .ui.history import HistoryWindow
from .utils.hotkeys import HotkeyManager
# FINISH ### IMPORTS ###

# START ### CONFIG ###
DEFAULT_CONFIG = {
  'max_clips': 50,
  'show_sequence_prompts': True,
  'paste_on_select': False,
  'hotkeys': {
     'show_history': 'ctrl+shift+v',
     'sequential_mode': 'ctrl+shift+s',
     'pin_clip': 'ctrl+shift+p',
     'command_center': 'ctrl+shift+space'
  }
}
# FINISH ### CONFIG ###

# START ### CLIP_ITEM ###
class ClipItem:
   def __init__(self, content: str):
     self.content = content
     self.timestamp = datetime.now()
     self.preview = self._make_preview()
     self.pinned = False

  def _make_preview(self) -> str:
     """Create a clean preview of the clip content"""
     preview = self.content.replace('\n', ' ').strip()
     return preview[:50] + '...' if len(preview) > 50 else preview
# FINISH ### CLIP_ITEM ###

# START ### MULTICLIP_CORE ###
class MultiClip:
   def __init__(self):
     self.clips: List[ClipItem] = []
     self.pinned: List[ClipItem] = []
     self.sequential_mode = False
     self.current_sequence_position = 0
     self.config = DEFAULT_CONFIG.copy()

     # Initialize components
␌     self.storage = ClipStorage()
     self.tray = MultiClipTray(self)
     self.toast = ToastManager()
     self.hotkeys = HotkeyManager(self)

     # Load saved state
     self._load_state()

  def add_clip(self, content: str) -> None:
    """Add new clip to history"""
    if not content or (self.clips and content == self.clips[0].content):
        return

     clip = ClipItem(content)

     if self.sequential_mode:
         self._handle_sequential_interrupt(clip)
     else:
         self.clips.insert(0, clip)
         while len(self.clips) > self.config['max_clips']:
            self.clips.pop()

     self._save_state()

  def _handle_sequential_interrupt(self, clip: ClipItem) -> None:
    """Handle new clip during sequential paste mode"""
    if self.config['show_sequence_prompts']:
        self.toast.show_sequence_prompt(
           clip,
           on_continue=lambda: self._continue_sequence(clip),
           on_restart=lambda: self._restart_sequence(clip)
        )
    else:
        self._restart_sequence(clip)

  def pin_current(self) -> None:
    """Pin current clipboard content"""
    content = pyperclip.paste()
    if not content:
        return

     clip = ClipItem(content)
     clip.pinned = True
     self.pinned.append(clip)
     self._save_state()

  def _load_state(self) -> None:
    """Load saved clips and settings"""
    saved_state = self.storage.load()
    if saved_state:
        self.clips = saved_state.get('clips', [])
        self.pinned = saved_state.get('pinned', [])
        self.config.update(saved_state.get('config', {}))

    def _save_state(self) -> None:
      """Save current state"""
      state = {
         'clips': self.clips,
         'pinned': self.pinned,
         'config': self.config
      }
      self.storage.save(state)
# FINISH ### MULTICLIP_CORE ###
