# 🎵 Virtual Soundboard

A customizable Python-based soundboard application with an intuitive GUI for playing audio files. Create multiple soundboards, organize your sounds, and switch between different audio collections with ease!

![Soundboard Preview](![image](https://github.com/user-attachments/assets/3df1bee1-4c02-49c8-a821-4b663f29a0db)
)

## 📑 Table of Contents
- [✨ Features](#-features)
- [🎮 How to Use](#-how-to-use)
- [🛠️ Installation](#️-installation)
  - [Option 1: Download Executable](#option-1-download-executable-recommended)
  - [Option 2: Clone and Run from Source](#option-2-clone-and-run-from-source)
- [⚙️ Configuration](#️-configuration)
  - [config.json](#configjson)
  - [soundboards.json](#soundboardsjson)
- [🔧 Building from Source](#-building-from-source)
- [📋 Requirements](#-requirements)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🐛 Issues & Support](#-issues--support)
- [☕ Support the Project](#-support-the-project)

## ✨ Features

- **Multiple Soundboards**: Create and switch between different soundboard collections
- **Customizable Grid Layout**: Configure button grid size (rows/columns)
- **Theme Support**: Light and dark theme options
- **Audio Format Support**: MP3, WAV, and OGG file formats
- **Intuitive Interface**: Clean, modern GUI with circular sound buttons
- **Compact Design**: Optimized window size for desktop use

## 🎮 How to Use

1. **Launch the application**
2. **Create a New Soundboard**: Click the "New" button to create a new soundboard collection
3. **Add Sounds**: Click on empty sound buttons to add audio files
4. **Switch Soundboards**: Use the dropdown menu to switch between different soundboard collections
5. **Play Sounds**: Click any sound button to play the associated audio file
## 🛠️ Installation

Choose one of the following installation methods:

### Option 1: Download Executable (Recommended)

**For Windows users - No Python required!**

1. Go to the [**Releases**](../../releases) section
2. Download the latest VirtualSoundboard_Setup_v*.*.*.exe installer
3. Run the installer and follow the setup wizard
4. Launch from Start Menu or Desktop shortcut

### Option 2: Clone and Run from Source

**For developers or users who want to modify the code:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/refentseg/soundboard
   cd soundboard
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   ```
   ```bash
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### config.json

The main configuration file that controls the application behavior:

```json
{
  "theme": "dark",
  "window": {
    "width": 500,
    "height": 350,
    "resizable": false
  },
  "audio": {
    "supported_formats": [
      "*.mp3",
      "*.wav",
      "*.ogg"
    ],
    "default_volume": 0.7
  },
  "ui": {
    "button_grid": {
      "rows": 2,
      "columns": 3
    },
    "button_size": 70,
    "max_label_length": 10
  }
}
```

**Configuration Options:**
- **theme**: Choose between "light" or "dark" themes
- **window**: Set application window dimensions and resizing behavior
- **audio**: Configure supported audio formats and default volume (0.0-1.0)
- **ui**: Customize button grid layout, button size, and label length

### soundboards.json

Stores your soundboard collections and sound file mappings. Each soundboard can contain multiple sounds with custom names and file paths.

## 🔧 Building from Source

To create a standalone executable:

```bash
pyinstaller --onefile --windowed --name "Soundboard" --icon=assets/icons/icon.ico main.py
```

The executable will be created in the `dist/` folder.

## 📋 Requirements

- Python 3.7+
- tkinter (usually included with Python)
- pygame (for audio playback)
- Additional dependencies listed in `requirements.txt`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Issues & Support

If you encounter any issues or have suggestions, please [open an issue](../../issues) on GitHub.

## ☕ Support the Project

If you find this project helpful, consider buying me a coffee!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-orange.svg?style=flat-square)](https://coff.ee/refentseg)

---

**Enjoy your Virtual Soundboard! 🎵**
