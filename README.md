# 🚀 MultiClip System
### Advanced Multi-Clipboard Manager with Global Hotkeys

> **The ultimate clipboard management solution for power users who demand efficiency and control.**

[![Version](https://img.shields.io/badge/version-v2.0.1-blue.svg)](https://github.com/yourusername/multiclip/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Linux-orange.svg)](https://www.linux.org/)

---

## 🎯 **What This Beast Does**

MultiClip transforms your clipboard into a **10-slot powerhouse** with instant global hotkey access. Copy multiple items and retrieve them lightning-fast without losing focus from your current application.

### ⚡ **Key Features**
- **🔥 10 Independent Clipboard Slots** - Store up to 10 different text snippets simultaneously
- **⌨️ Global Hotkey Access** - Works system-wide, no matter what application has focus
- **🛡️ System Service Integration** - Runs automatically at startup with systemd
- **📱 Visual Notifications** - Toast notifications for copy/paste confirmations  
- **🔧 Poetry Package Management** - Modern dependency management and virtual environments
- **🚀 Auto-Recovery** - Service automatically restarts on failure
- **💻 Easy Management** - Simple command-line control interface

---

## 👨‍💻 **Author**
**Matthew Trevino** - *Lead Developer & System Architect*  
📧 Contact: [Your Email]  
🐙 GitHub: [@yourusername](https://github.com/yourusername)

---

## 🛠️ **Installation**

### **Prerequisites**
- **OS**: Linux (Debian/Ubuntu tested)
- **Python**: 3.8+ 
- **Desktop Environment**: X11 support required
- **Permissions**: Root access for global hotkeys

### **Method 1: Poetry Installation (Recommended)**

#### **Step 1: Install Poetry**
```bash
# Option A: Official installer (recommended)
curl -sSL https://install.python-poetry.org | python3 -

# Option B: Package manager  
sudo apt install python3-poetry

# Verify installation
poetry --version
```

#### **Step 2: Install MultiClip**
```bash
# Clone the repository
git clone https://github.com/yourusername/multiclip.git
cd multiclip

# Install dependencies with Poetry
poetry install

# Install additional system dependencies
sudo apt install python3-tk python3-dev -y
```

#### **Step 3: Deploy as System Service**
```bash
# Install and start the service
sudo ./install-service.sh

# Verify service is running
multiclip-ctl status
```

### **Method 2: Manual Installation**

#### **For Advanced Users**
```bash
# Create virtual environment
python3 -m venv venv-multiclip
source venv-multiclip/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install system dependencies
sudo apt install python3-tk python3-dev -y

# Run manually
python3 multiclip.py
```

---

## 🎮 **Usage**

### **Quick Start**
1. **Service automatically starts** after installation
2. **Copy text** as normal (Ctrl+C)
3. **Store in slot** using `Ctrl + [1-0]`
4. **Retrieve from slot** using `Ctrl + Shift + [1-0]`

### **Hotkey Reference**

| Action | Store Hotkey | Retrieve Hotkey | Slot |
|--------|--------------|-----------------|------|
| 📋 Slot 1 | `Ctrl + 1` | `Ctrl + Shift + 1` | Primary |
| 📋 Slot 2 | `Ctrl + 2` | `Ctrl + Shift + 2` | Secondary |
| 📋 Slot 3 | `Ctrl + 3` | `Ctrl + Shift + 3` | Tertiary |
| 📋 Slot 4 | `Ctrl + 4` | `Ctrl + Shift + 4` | Work Notes |
| 📋 Slot 5 | `Ctrl + 5` | `Ctrl + Shift + 5` | Passwords* |
| 📋 Slot 6 | `Ctrl + 6` | `Ctrl + Shift + 6` | Code Snippets |
| 📋 Slot 7 | `Ctrl + 7` | `Ctrl + Shift + 7` | URLs |
| 📋 Slot 8 | `Ctrl + 8` | `Ctrl + Shift + 8` | Templates |
| 📋 Slot 9 | `Ctrl + 9` | `Ctrl + Shift + 9` | Temporary |
| 📋 Slot 0 | `Ctrl + 0` | `Ctrl + Shift + 0` | Archive |

> **\*Security Note**: Stored text is kept in memory only. For sensitive data, consider using a dedicated password manager.

### **Workflow Example**
```bash
# 1. Copy different pieces of text
#    Select text → Ctrl+C (copy normally)
#    Press Ctrl+1 (store in slot 1)

# 2. Copy more text 
#    Select different text → Ctrl+C
#    Press Ctrl+2 (store in slot 2)

# 3. Later, retrieve any stored text
#    Press Ctrl+Shift+1 (paste from slot 1)
#    Press Ctrl+Shift+2 (paste from slot 2)

# 4. Visual confirmation
#    Toast notifications confirm successful operations
```

---

## 🔧 **Service Management**

### **MultiClip Control Commands**
```bash
# Service status and control
multiclip-ctl status          # Check service status
multiclip-ctl start           # Start the service
multiclip-ctl stop            # Stop the service  
multiclip-ctl restart         # Restart the service
multiclip-ctl logs            # View service logs
multiclip-ctl enable          # Enable auto-start at boot
multiclip-ctl disable         # Disable auto-start
multiclip-ctl test            # Run manual test mode
```

### **Service Features**
- **🔄 Auto-Restart**: Service automatically recovers from crashes
- **📊 Logging**: Full systemd journal integration
- **🚀 Boot Integration**: Starts automatically with system
- **⚡ Low Resource Usage**: Minimal CPU and memory footprint
- **🛡️ Root Privileges**: Secure global hotkey registration

---

## 📋 **Dependencies**

### **Core Python Packages**
```toml
[tool.poetry.dependencies]
python = "^3.8"
pyperclip = "^1.9.0"      # Clipboard operations
keyboard = "^0.13.5"      # Global hotkey detection  
pyautogui = "^0.9.54"     # GUI automation and notifications
```

### **System Dependencies**
```bash
# Required for GUI notifications
python3-tk python3-dev

# Automatically installed during setup
```

---

## 🏗️ **Architecture**

### **System Design**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   MultiClip      │───▶│   Clipboard     │
│   (Hotkeys)     │    │   Service        │    │   Slots 0-9     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Visual Feedback │
                       │  (Notifications) │
                       └──────────────────┘
```

### **File Structure**
```
multiclip/
├── 📄 multiclip.py                    # Core application
├── 🔧 multiclip-control.sh           # Service management script  
├── ⚙️ multiclip-poetry-service.sh    # Service wrapper script
├── 📦 pyproject.toml                 # Poetry configuration
├── 📋 requirements.txt               # Pip dependencies
├── 🚀 install-service.sh             # Service installer
├── 📖 README.md                      # This file
└── 📜 LICENSE                        # MIT License
```

---

## 🔥 **Advanced Configuration**

### **Custom Hotkey Mapping**
Edit `multiclip.py` to customize hotkeys:
```python
# Example: Change store hotkeys to Alt instead of Ctrl
STORE_HOTKEYS = {
    f'alt+{i}': i for i in range(10)
}
```

### **Notification Settings**
Modify notification behavior:
```python
# Disable notifications
SHOW_NOTIFICATIONS = False

# Customize notification duration  
NOTIFICATION_DURATION = 2000  # milliseconds
```

### **Slot Persistence**
Enable persistent storage across restarts:
```python
# Add to multiclip.py
PERSISTENT_STORAGE = True
STORAGE_FILE = "/home/user/.multiclip_slots.json"
```

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Service Won't Start**
```bash
# Check service status
multiclip-ctl status

# View detailed logs
multiclip-ctl logs

# Test manually
multiclip-ctl test
```

#### **Hotkeys Not Working**
```bash
# Verify root permissions
sudo systemctl status multiclip.service

# Check for conflicting applications
ps aux | grep -i clipboard

# Restart service
multiclip-ctl restart
```

#### **GUI Notifications Missing**
```bash
# Install missing dependencies
sudo apt install python3-tk python3-dev -y

# Verify X11 access
echo $DISPLAY
xauth list
```

#### **Permission Errors**
```bash
# Fix service permissions
sudo systemctl daemon-reload
sudo systemctl restart multiclip.service

# Check file ownership
ls -la /home/flintx/multiclip/
```

### **Debug Mode**
```bash
# Run with verbose logging
PYTHONPATH=/home/flintx/multiclip python3 -m pdb multiclip.py

# Enable debug output
export MULTICLIP_DEBUG=1
multiclip-ctl test
```

---

## 🤝 **Contributing**

### **Development Setup**
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/multiclip.git
cd multiclip

# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .
```

### **Pull Request Guidelines**
1. **🧪 Add tests** for new features
2. **📝 Update documentation** for user-facing changes  
3. **🎨 Follow code style** (Black + isort)
4. **✅ Ensure CI passes** before submitting

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🎯 **Roadmap**

### **v2.1.0 - Enhanced Features**
- [ ] **📱 Cross-platform support** (Windows/macOS)
- [ ] **🔐 Encrypted storage** for sensitive data
- [ ] **🌐 Network sync** between devices
- [ ] **📊 Usage analytics** and reporting

### **v2.2.0 - UI Improvements**  
- [ ] **🖥️ System tray interface**
- [ ] **⌨️ Custom hotkey configuration GUI**
- [ ] **📋 Clipboard history viewer**
- [ ] **🎨 Themes and customization**

### **v3.0.0 - Enterprise Features**
- [ ] **👥 Multi-user support**
- [ ] **🔧 Admin configuration panel**
- [ ] **📈 Performance monitoring**
- [ ] **🔌 Plugin system**

---

## 🔗 **Links**

- **📦 [Releases](https://github.com/yourusername/multiclip/releases)** - Download latest versions
- **🐛 [Issues](https://github.com/yourusername/multiclip/issues)** - Report bugs or request features  
- **💬 [Discussions](https://github.com/yourusername/multiclip/discussions)** - Community support
- **📚 [Wiki](https://github.com/yourusername/multiclip/wiki)** - Detailed documentation

---

## ⭐ **Show Your Support**

If MultiClip helps boost your productivity, consider:
- ⭐ **Starring this repository**
- 🐛 **Reporting bugs** and suggesting features
- 💻 **Contributing code** or documentation  
- 📢 **Sharing with fellow developers**

---

<div align="center">

**Built with 💻 and ☕ by developers, for developers.**

*MultiClip - Because context switching is expensive.*

</div>