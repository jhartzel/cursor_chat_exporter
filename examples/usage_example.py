#!/usr/bin/env python3
"""
Usage Example for Cursor Chat History Export Tool

This script demonstrates how to use the cursor_export.py tool with real files.
"""

import json
import os
from pathlib import Path
from cursor_export import export_all_workspaces

def main():
    """Example usage of the cursor export tool"""

    # Example 1: Command line usage
    print("=" * 60)
    print("CURSOR CHAT HISTORY EXPORT TOOL - USAGE EXAMPLES")
    print("=" * 60)

    print("\n1. Command Line Usage:")
    print("   python cursor_export.py <input_path> <output_directory>")
    print("   ")
    print("   From workspace storage directory (recommended):")
    print("   python cursor_export.py \"/Users/username/Library/Application Support/Cursor/User/workspaceStorage\" ./exports")
    print("   ")
    print("   From JSON file:")
    print("   python cursor_export.py chat_history.json ./exports")

    print("\n2. Python API Usage:")
    print("   from cursor_export import export_all_workspaces, load_chat_history_from_directory")
    print("   import json")
    print("   ")
    print("   # Option A: Load from workspace storage directory")
    print("   workspace_dir = '/Users/username/Library/Application Support/Cursor/User/workspaceStorage'")
    print("   chat_history = load_chat_history_from_directory(workspace_dir)")
    print("   results = export_all_workspaces(chat_history, './exports')")
    print("   ")
    print("   # Option B: Load from JSON file")
    print("   with open('chat_history.json', 'r') as f:")
    print("       chat_history = json.load(f)")
    print("   results = export_all_workspaces(chat_history, './exports')")
    print("   print(f'Exported {len(results)} workspaces')")

    print("\n3. Virtual Environment Setup:")
    print("   python3 -m venv cursor_export_env")
    print("   source cursor_export_env/bin/activate  # On Windows: cursor_export_env\\Scripts\\activate")
    print("   pip install -r requirements.txt")
    print("   ")
    print("   # Run with workspace storage directory")
    print("   python cursor_export.py \"$HOME/Library/Application Support/Cursor/User/workspaceStorage\" ./exports")

    print("\n4. Expected Output Structure:")
    print("   exports/")
    print("   ├── html/")
    print("   │   └── WorkspaceName/")
    print("   │       ├── chat1.html")
    print("   │       └── chat2.html")
    print("   ├── markdown/")
    print("   │   └── WorkspaceName/")
    print("   │       ├── chat1.md")
    print("   │       └── chat2.md")
    print("   └── json/")
    print("       └── WorkspaceName.json")

    print("\n" + "=" * 60)
    print("For more information, see README.md")
    print("To run tests, use: python test_cursor_export.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
