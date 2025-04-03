import json
import os
from typing import Dict, Optional

# START ### STORAGE ###
class ClipStorage:
   def __init__(self):
     self.storage_path = os.path.expand('~/.multiclip')
     self.state_file = os.path.join(self.storage_path, 'state.json')
     self._ensure_storage_dir()

  def _ensure_storage_dir(self) -> None:
    """Ensure storage directory exists"""
    if not os.path.exists(self.storage_path):
        os.makedirs(self.storage_path)

  def load(self) -> Optional[Dict]:
    """Load saved state"""
    try:
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
               return json.load(f)
    except Exception as e:
        print(f"Error loading state: {e}")
    return None

    def save(self, state: Dict) -> None:
      """Save current state"""
      try:
         with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=4)
      except Exception as e:
         print(f"Error saving state: {e}")
# FINISH ### STORAGE ###
