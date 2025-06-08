import time
from typing import List, Optional, Callable
from shared.clipboard_manager import ClipboardManager

class OrderlyState:
    def __init__(self):
        self.active = False
        self.current_slot = 0
        self.sequence: List[int] = []
        self.paste_index = 0
        self.max_slots = 10
    
    def reset(self):
        self.active = False
        self.current_slot = 0
        self.sequence.clear()
        self.paste_index = 0
    
    def to_dict(self):
        return {
            "active": self.active,
            "current_slot": self.current_slot,
            "sequence": self.sequence,
            "paste_index": self.paste_index
        }

class OrderlyManager:
    def __init__(self, clipboard_manager: ClipboardManager):
        self.clipboard_manager = clipboard_manager
        self.state = OrderlyState()
        self.status_callback: Optional[Callable] = None
        self.completion_callback: Optional[Callable] = None
    
    def set_status_callback(self, callback: Callable):
        self.status_callback = callback
    
    def set_completion_callback(self, callback: Callable):
        self.completion_callback = callback
    
    def activate_orderly_mode(self) -> bool:
        if not self.state.active:
            self.state.reset()
            self.state.active = True
            self.state.current_slot = 0
            self._notify_status("Orderly mode activated - ready for sequential copying")
            return True
        return False
    
    def deactivate_orderly_mode(self):
        if self.state.active:
            self.state.reset()
            self._notify_status("Orderly mode deactivated")
    
    def handle_copy_operation(self) -> bool:
        if not self.state.active:
            return False
        
        if self.state.current_slot >= self.state.max_slots:
            self._notify_status("Maximum slots reached - deactivating Orderly mode")
            self.deactivate_orderly_mode()
            return False
        
        # Store clipboard content in current slot
        success = self.clipboard_manager.copy_to_slot(self.state.current_slot)
        
        if success:
            self.state.sequence.append(self.state.current_slot)
            slot_content = self.clipboard_manager.get_slot_preview(self.state.current_slot)
            self._notify_status(f"Stored in slot {self.state.current_slot}: {slot_content}")
            self.state.current_slot += 1
            return True
        
        return False
    
    def handle_paste_operation(self) -> bool:
        if not self.state.active or not self.state.sequence:
            return False
        
        if self.state.paste_index >= len(self.state.sequence):
            self._notify_status("All slots pasted - completing Orderly workflow")
            if self.completion_callback:
                self.completion_callback()
            self.deactivate_orderly_mode()
            return False
        
        # Paste from the next slot in sequence
        slot_to_paste = self.state.sequence[self.state.paste_index]
        success = self.clipboard_manager.paste_from_slot(slot_to_paste)
        
        if success:
            slot_content = self.clipboard_manager.get_slot_preview(slot_to_paste)
            self._notify_status(f"Pasted from slot {slot_to_paste}: {slot_content}")
            self.state.paste_index += 1
            
            # Check if workflow is complete
            if self.state.paste_index >= len(self.state.sequence):
                self._notify_status("Orderly workflow completed!")
                if self.completion_callback:
                    self.completion_callback()
                self.deactivate_orderly_mode()
            
            return True
        
        return False
    
    def get_current_status(self) -> str:
        if not self.state.active:
            return "Orderly mode inactive"
        
        if not self.state.sequence:
            return f"Ready to copy - slot {self.state.current_slot}"
        
        if self.state.paste_index < len(self.state.sequence):
            remaining = len(self.state.sequence) - self.state.paste_index
            return f"Ready to paste - {remaining} items remaining"
        
        return "Workflow complete"
    
    def get_sequence_preview(self) -> List[str]:
        previews = []
        for slot_id in self.state.sequence:
            preview = self.clipboard_manager.get_slot_preview(slot_id)
            previews.append(f"Slot {slot_id}: {preview}")
        return previews
    
    def reset_paste_sequence(self):
        self.state.paste_index = 0
        self._notify_status("Paste sequence reset to beginning")
    
    def skip_current_paste(self) -> bool:
        if self.state.active and self.state.paste_index < len(self.state.sequence):
            self.state.paste_index += 1
            self._notify_status(f"Skipped paste - moving to next item")
            return True
        return False
    
    def _notify_status(self, message: str):
        if self.status_callback:
            self.status_callback(message)
        print(f"[Orderly] {message}")
    
    def is_active(self) -> bool:
        return self.state.active
    
    def get_state_dict(self) -> dict:
        return self.state.to_dict()
