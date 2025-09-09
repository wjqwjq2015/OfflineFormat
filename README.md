不同语言: 
[中文文档](README_ZH.md)

# 🔹 Offline JSON Formatter

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

A powerful offline JSON formatting desktop application built with Python + PyQt5, providing Postman Beautify-like
functionality with additional features including JSON sorting, compression, validation, and advanced search & replace
capabilities.

## 🌟 Key Features

- 🚀 **Completely Offline**: No internet connection required, protecting your data privacy
- 🎨 **Modern Interface**: Beautiful GUI design with embedded search and replace functionality
- ⚡ **High Performance**: Built on PyQt5 for fast and responsive user experience
- 🔧 **Multiple Formatting Options**: Beautify, sort, minify, and validate JSON with ease
- 📋 **Convenient Operations**: One-click copy, clear, with keyboard shortcuts support
- 🎯 **Precise Search**: Case-sensitive and whole-word matching search & replace
- 🌈 **Smart Highlighting**: Modern blue background with white text and bold formatting for search results
- 🌳 **Tree View**: Expandable/collapsible JSON structure tree for intuitive hierarchy visualization
- 🔄 **Dual View Mode**: Text view and tree view with real-time synchronization

## 📸 Screenshots

*Main Interface*

- Left panel: JSON input area (editable)
- Right panel: JSON output area (read-only)
- Bottom: Function buttons and embedded search/replace tools

## 🚀 Quick Start

### Option 1: Download Executable (Recommended)

1. Download the latest `JSON格式化工具.exe` from
   the [Releases](https://github.com/your-username/offline-json-formatter/releases) page
2. Double-click to run - no Python installation required!

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/your-username/offline-json-formatter.git
cd offline-json-formatter

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📋 Core Functions

### 🎨 JSON Operations

- **Beautify**: Format JSON with proper indentation (4 spaces)
- **Sort**: Sort JSON keys alphabetically and beautify
- **Minify**: Compress JSON to single line
- **Validate**: Check JSON syntax validity
- **Copy**: Copy formatted result to clipboard
- **Expand All**: Expand all nodes in tree view
- **Collapse All**: Collapse all nodes in tree view
- **Clear**: Clear both input and output areas

### 🌳 Dual View Display

- **Text View**: Traditional text format display with search and replace support
- **Tree View**: Interactive JSON structure tree with expandable/collapsible nodes
- **Tab Switching**: Seamlessly switch between views with real-time data synchronization

### 🔍 Search & Replace

- **Embedded Search Box**: Integrated search interface in text areas
- **Advanced Options**: Case-sensitive and whole-word matching
- **Modern Highlighting**: Blue background with white text and bold formatting
- **Navigation**: Previous/Next buttons for easy navigation
- **Replace Functions**: Replace current match or replace all occurrences

### ⚙️ Additional Features

- **Font Size Control**: Adjustable font sizes for better readability
- **Keyboard Shortcuts**: Ctrl+F for search, Ctrl+H for replace
- **Error Handling**: Detailed error messages for invalid JSON
- **Status Bar**: Real-time feedback on operations

## 💻 System Requirements

- **Operating System**: Windows 7/10/11/Windows Server
- **Python Version**: 3.8+ (if running from source)
- **Memory**: 2GB RAM recommended
- **Disk Space**: 50MB for executable, 100MB for source installation

## 🛠️ Building from Source

### Standard Build (~36MB)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="JSON格式化工具" main.py
```

### Optimized Build (~15-20MB)

```bash
# Use the optimization script
build_optimized.bat
```

### Ultra-Compact Build (~8-15MB)

```bash
# Use spec configuration file
build_small.bat
```

### Further Compression (Optional)

1. **Install UPX compression tool**
    - Download: https://github.com/upx/upx/releases
    - Extract to system PATH or project directory

2. **Manual compression**
   ```bash
   upx --ultra-brute "dist\JSON格式化工具.exe"
   ```

## 📖 Usage Examples

### Basic JSON Formatting

**Input:**

```json
{"name":"John Doe","age":30,"city":"New York","skills":["Python","JavaScript"]}
```

**After Beautify:**

```json
{
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "skills": [
        "Python",
        "JavaScript"
    ]
}
```

**After Sort:**

```json
{
    "age": 30,
    "city": "New York",
    "name": "John Doe",
    "skills": [
        "Python",
        "JavaScript"
    ]
}
```

### Search & Replace Operations

1. **Open Search**: Press `Ctrl+F` or click the search button
2. **Enter Search Term**: Type the text you want to find
3. **Navigate Results**: Use ↑/↓ buttons to navigate matches
4. **Replace Text**: Use `Ctrl+H` for replace functionality
5. **Advanced Options**: Toggle case sensitivity and whole-word matching

## 🏗️ Technical Architecture

### Technology Stack

- **Language**: Python 3.8+
- **GUI Framework**: PyQt5 5.15+
- **JSON Processing**: Python standard library `json`
- **Packaging**: PyInstaller 6.3.0

### Project Structure

```
offline-json-formatter/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Chinese documentation
├── README_EN.md           # English documentation
├── LICENSE                # MIT license file
├── build_optimized.bat    # Optimized build script
├── build_small.bat        # Ultra-compact build script
├── main_optimized.spec    # PyInstaller spec file
└── dist/                  # Build output directory
    └── JSON格式化工具.exe  # Executable file
```

### Core Classes

- **JSONFormatterApp**: Main window class inheriting from QMainWindow
- **EmbeddedSearchWidget**: Embedded search functionality
- **EmbeddedReplaceWidget**: Embedded search & replace functionality

## 🐛 Troubleshooting

### Common Issues

**Q: Application won't start**
A: Ensure PyQt5 is installed: `pip install PyQt5`

**Q: JSON formatting fails**
A: Verify input is valid JSON format. The application will show specific error messages.

**Q: Executable file is too large**
A: This is normal as it includes Python runtime and PyQt5 libraries. Use optimized build scripts for smaller size.

**Q: Error on Windows 7**
A: Ensure Visual C++ Redistributable is installed on the system.

**Q: Search highlighting not working**
A: The new blue highlighting system requires proper QTextCharFormat support. Restart the application if issues persist.

## 📝 Changelog

### v1.3 (2025-01-XX)

- 🌳 **New JSON Tree View**: Implemented expandable/collapsible JSON structure tree display
- 🔄 **Dual View Mode**: Added text view and tree view tabs with real-time switching
- 📂 **Tree Operations**: New "Expand All" and "Collapse All" buttons for quick tree manipulation
- 🎨 **Visual Enhancements**: Tree view supports alternating row colors and modern styling
- ⚡ **Performance Optimization**: Improved tree display performance for large JSON data

### v1.2 (2025-01-XX)

- 🔍 **New Search & Replace**: Added embedded search box with modern blue highlighting
- 🎨 **UI Improvements**: Enhanced search match highlighting with blue background + white text + bold formatting
- 🐛 **Bug Fixes**: Resolved QTextDocument.find parameter type errors
- ⚙️ **Feature Enhancements**: Added circular search, case sensitivity, and whole-word matching options

### v1.1 (2024-12-XX)

- 🔧 **Feature Extensions**: Added font size adjustment functionality
- 📱 **Interface Improvements**: Optimized layout and user experience
- 🎯 **Error Handling**: Enhanced JSON validation and error messaging

### v1.0 (2024-01-XX)

- ✅ Implemented basic JSON formatting functionality
- ✅ Added JSON sorting feature
- ✅ Implemented clipboard copy functionality
- ✅ Added clear function and error handling
- ✅ Extended features: Minify and Validate
- ✅ Beautiful GUI interface design
- ✅ Complete packaging and distribution solution

## 🤝 Contributing

We welcome Issues and Pull Requests to help improve this project!

### Development Setup

```bash
git clone https://github.com/your-username/offline-json-formatter.git
cd offline-json-formatter
pip install -r requirements.txt
python main.py
```

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **Author**: wangjunqi
- **Current Version**: 0.1
- **Development Period**: 2025.09

## ⭐ Support the Project

If this project helps you, please give it a ⭐ Star!

## 🌐 Language Versions

- [中文文档](README_ZH.md) - Chinese Documentation
- [English Documentation](README_EN.md) - This file

---

**🎉 Thank you for using Offline JSON Formatter! For questions or suggestions, feel free to open an issue.**
