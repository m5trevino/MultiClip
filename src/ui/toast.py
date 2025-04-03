# START ### IMPORTS ###
import tkinter as tk
from typing import Callable, Optional
import time
# FINISH ### IMPORTS ###

# START ### TOAST_IMPLEMENTATION ###
class ToastManager:
   def __init__(self):
     self.active_toasts = []
     self.fade_time = 3000 # milliseconds before fade out

  def show_sequence_prompt(self, clip_preview: str, on_continue: Callable, on_restart: Callable):
    """Show sequence interrupt prompt"""
    toast = SequenceToast(
       clip_preview,
       on_continue,
       on_restart,
       self.fade_time
    )
    self.active_toasts.append(toast)
    toast.show()

  def show_notification(self, message: str, duration: int = 3000):
    """Show simple notification toast"""
    toast = NotificationToast(message, duration)
    self.active_toasts.append(toast)
    toast.show()

class BaseToast:
   def __init__(self, duration: int):
     self.window = tk.Tk()
     self.window.withdraw() # Hide initially
␌     self.window.overrideredirect(True)
     self.window.attributes('-topmost', True)
     self.duration = duration
     self.setup_window()

  def setup_window(self):
    """Setup basic window properties"""
    self.window.configure(bg='#2e2e2e')
    # Position near cursor but not on it
    x = self.window.winfo_screenwidth() - 350
    y = self.window.winfo_screenheight() - 150
    self.window.geometry(f"+{x}+{y}")

  def show(self):
    """Show the toast window"""
    self.window.deiconify()
    self.window.after(self.duration, self.fade_out)

  def fade_out(self):
    """Fade out and destroy the window"""
    self.window.destroy()

class SequenceToast(BaseToast):
   def __init__(self, clip_preview: str, on_continue: Callable, on_restart: Callable, duration: int):
     super().__init__(duration)
     self.clip_preview = clip_preview
     self.on_continue = on_continue
     self.on_restart = on_restart
     self.create_widgets()

  def create_widgets(self):
    """Create the toast UI elements"""
    tk.Label(
       self.window,
       text="New clip during sequence:",
       fg='#ffffff',
       bg='#2e2e2e',
       font=('Arial', 10, 'bold')
    ).pack(pady=5)

     tk.Label(
        self.window,
        text=self.clip_preview[:50] + "..." if len(self.clip_preview) > 50 else self.clip_preview,
        fg='#cccccc',
        bg='#2e2e2e',
        wraplength=280
     ).pack(pady=5)

     btn_frame = tk.Frame(self.window, bg='#2e2e2e')
     btn_frame.pack(pady=10)

     tk.Button(
        btn_frame,
        text="Continue Sequence",
        command=self._handle_continue,
        bg='#404040',
        fg='white'
     ).pack(side=tk.LEFT, padx=5)

     tk.Button(
        btn_frame,
        text="Restart from #1",
        command=self._handle_restart,
        bg='#404040',
        fg='white'
     ).pack(side=tk.LEFT, padx=5)

  def _handle_continue(self):
␌      """Handle continue button click"""
      self.on_continue()
      self.window.destroy()

  def _handle_restart(self):
    """Handle restart button click"""
    self.on_restart()
    self.window.destroy()

class NotificationToast(BaseToast):
   def __init__(self, message: str, duration: int):
     super().__init__(duration)
     self.message = message
     self.create_widgets()

    def create_widgets(self):
      """Create notification UI elements"""
      tk.Label(
         self.window,
         text=self.message,
         fg='#ffffff',
         bg='#2e2e2e',
         font=('Arial', 10),
         wraplength=280
      ).pack(pady=10)
# FINISH ### TOAST_IMPLEMENTATION ###
