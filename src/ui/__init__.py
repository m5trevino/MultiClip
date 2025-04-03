"""
MultiClip UI Components
Handles all the  interface elements including system tray, toasts, and history window
"""
from .tray import MultiClipTray
from .toast import ToastManager
from .history import HistoryWindow

__all__ = ['MultiClipTray', 'ToastManager', 'HistoryWindow']
