# Cursor Chat History Export Tool

A Python script to export Cursor chat history to markdown and HTML formats. This is a Python equivalent of the original JavaScript `cursor_export.js` file.

## Features

- **Direct Workspace Import**: Reads directly from Cursor's workspace storage directory
- **Flexible Input**: Supports both workspace directories and JSON files
- **Complete Export**: Converts all chat history to markdown and HTML formats
- **Multiple Workspaces**: Handles all workspaces in your Cursor storage
- **Chat Sessions**: Exports regular chat conversations
- **Composers**: Exports chat editing sessions (composers)
- **GitHub Styling**: Generates HTML files with professional GitHub-style CSS
- **Organized Output**: Creates structured directory layout for easy browsing
- **JSON Summaries**: Provides structured data for programmatic access

## Requirements

- Python 3.7+
- `markdown` library

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make the script executable (optional):
```bash
chmod +x cursor_export.py
```

## Usage

### Command Line Usage

```bash
python cursor_export.py <input_path> <output_dir>
```

**Parameters:**
- `input_path`: Path to either:
  - A Cursor chat history JSON file, OR
  - The Cursor workspace storage directory (e.g., `~/Library/Application Support/Cursor/User/workspaceStorage`)
- `output_dir`: Directory where exported files will be saved

### Examples

**From workspace storage directory (recommended):**
```bash
python cursor_export.py "/Users/username/Library/Application Support/Cursor/User/workspaceStorage" ./exports
```

**From JSON file:**
```bash
python cursor_export.py chat_history.json ./exports
```

**macOS typical workspace storage location:**
```bash
python cursor_export.py "$HOME/Library/Application Support/Cursor/User/workspaceStorage" ./cursor_exports
```

### Finding Your Cursor Workspace Storage Directory

**macOS:**
```bash
~/Library/Application Support/Cursor/User/workspaceStorage
```

**Windows:**
```bash
%APPDATA%\Cursor\User\workspaceStorage
```

**Linux:**
```bash
~/.config/Cursor/User/workspaceStorage
```

### Output Structure

This will create the following directory structure:

```
exports/
├── html/
│   └── WorkspaceName/
│       ├── chat1.html
│       └── chat2.html
├── markdown/
│   └── WorkspaceName/
│       ├── chat1.md
│       └── chat2.md
└── json/
    └── WorkspaceName.json
```

## Output Formats

### Markdown Files
- Clean markdown format with workspace info, timestamps, and chat content
- Code blocks are properly formatted with syntax highlighting markers
- Organized by workspace and conversation

### HTML Files
- GitHub-style CSS styling
- Responsive design that works on mobile devices
- Syntax highlighting for code blocks
- Professional appearance suitable for sharing

### JSON Files
- Structured data format for programmatic access
- Contains all conversation metadata
- Useful for further processing or analysis

## Error Handling

The script includes comprehensive error handling for:
- Invalid JSON input files
- Missing input files
- File system permissions
- Malformed chat data

## Functions

### Core Functions

- `format_datetime()`: Formats timestamps consistently
- `get_safe_filename()`: Creates filesystem-safe filenames
- `convert_to_markdown()`: Converts chat data to markdown format
- `convert_to_html()`: Converts markdown to styled HTML
- `export_workspace()`: Processes a single workspace
- `export_all_workspaces()`: Processes all workspaces in the input

### Utility Functions

- `create_export_directories()`: Sets up output directory structure
- `export_chat_tab()`: Exports individual chat conversations
- `export_composer()`: Exports composer conversations

## Differences from JavaScript Version

This Python version maintains the same functionality as the original JavaScript version but includes:
- Type hints for better code documentation
- More robust error handling
- Better cross-platform path handling using `pathlib`
- Cleaner code structure with proper Python conventions
- Command-line interface for easier usage

## License

This tool is provided as-is for exporting Cursor chat history data.

