#!/usr/bin/env python3
"""
Cursor Chat History Export Tool

A Python package to export Cursor chat history to markdown and HTML formats.
"""

__version__ = "1.0.0"
__author__ = "Josh Hartzell"
__email__ = "josh.hartzell@example.com"

from .cursor_export import (
    export_all_workspaces,
    load_chat_history_from_directory,
    convert_cursor_session_to_markdown,
    convert_cursor_editing_session_to_markdown,
    convert_to_html
)

__all__ = [
    'export_all_workspaces',
    'load_chat_history_from_directory', 
    'convert_cursor_session_to_markdown',
    'convert_cursor_editing_session_to_markdown',
    'convert_to_html'
]
