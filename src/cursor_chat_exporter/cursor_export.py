#!/usr/bin/env python3
"""
Cursor Chat History Export Tool

Converts Cursor chat history to markdown and HTML formats.
Equivalent functionality to the JavaScript cursor_export.js file.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import markdown
import re
from typing import Dict, List, Optional, Any


def format_datetime(date_str: str) -> str:
    """Format datetime to yyyy-mm-dd hh:mm:ss"""
    try:
        if isinstance(date_str, (int, float)):
            date = datetime.fromtimestamp(date_str / 1000 if date_str > 1e10 else date_str)
        else:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return str(date_str)


def get_safe_filename(timestamp: Any, title: str) -> str:
    """Generate safe filename from timestamp and title"""
    date_str = format_datetime(timestamp).replace(' ', '-').replace(':', '-')

    # Remove or replace invalid filename characters
    safe_title = re.sub(r'[<>:"/\\|?*]', '-', title)
    safe_title = re.sub(r'\s+', '-', safe_title)

    # Limit total filename length
    MAX_FILENAME_LENGTH = 160
    combined_name = f"{date_str}--{safe_title}"

    if len(combined_name) > MAX_FILENAME_LENGTH:
        # Truncate title if too long
        truncated_title = safe_title[:MAX_FILENAME_LENGTH - len(date_str) - 4]
        return f"{date_str}--{truncated_title}"

    return combined_name


def convert_cursor_session_to_markdown(session_data: Dict[str, Any], workspace_info: Dict[str, Any]) -> str:
    """Convert Cursor chat session to markdown format"""
    markdown_content = ""

    if workspace_info.get('folder'):
        # Remove 'file://' prefix if it exists
        clean_path = workspace_info['folder'].replace('file://', '')
        markdown_content += f"# Workspace: {clean_path}\n\n"
    else:
        markdown_content += f"# Workspace: {workspace_info.get('id', 'Unknown')}\n\n"

    # Add creation date
    if session_data.get('creationDate'):
        markdown_content += f"Created: {format_datetime(session_data['creationDate'])}\n\n"

    # Add chat title
    title = session_data.get('customTitle') or f"Chat Session {session_data.get('sessionId', 'Unknown')}"
    markdown_content += f"## {title}\n\n"

    # Process requests (conversations)
    if session_data.get('requests'):
        for request in session_data['requests']:
            # User message
            if request.get('message', {}).get('text'):
                user_text = request['message']['text']
                markdown_content += f"**User**:\n\n{user_text}\n\n"

            # AI response
            if request.get('response'):
                response_parts = []
                for response_item in request['response']:
                    if response_item.get('value'):
                        response_parts.append(response_item['value'])

                if response_parts:
                    ai_response = '\n'.join(response_parts)
                    markdown_content += f"**Cursor**:\n\n{ai_response}\n\n"

            # Add separator between conversations
            markdown_content += "---\n\n"

    return markdown_content


def convert_cursor_editing_session_to_markdown(session_data: Dict[str, Any], workspace_info: Dict[str, Any]) -> str:
    """Convert Cursor chat editing session to markdown format"""
    markdown_content = ""

    if workspace_info.get('folder'):
        # Remove 'file://' prefix if it exists
        clean_path = workspace_info['folder'].replace('file://', '')
        markdown_content += f"# Workspace: {clean_path}\n\n"
    else:
        markdown_content += f"# Workspace: {workspace_info.get('id', 'Unknown')}\n\n"

    # Add chat title
    session_id = session_data.get('sessionId', 'Unknown')
    markdown_content += f"## Chat Editing Session: {session_id}\n\n"

    # Process linear history (editing conversation)
    if session_data.get('linearHistory'):
        for i, entry in enumerate(session_data['linearHistory']):
            markdown_content += f"### Edit {i + 1}\n\n"

            # Show files that were modified
            if entry.get('stops'):
                for stop in entry['stops']:
                    if stop.get('entries'):
                        for file_entry in stop['entries']:
                            resource = file_entry.get('resource', '')
                            if resource.startswith('file://'):
                                file_path = resource.replace('file://', '')
                                markdown_content += f"**Modified File**: `{file_path}`\n\n"

            # Show post-edit information
            if entry.get('postEdit'):
                markdown_content += "**Changes Made**:\n\n"
                for edit in entry['postEdit']:
                    resource = edit.get('resource', '')
                    if resource.startswith('file://'):
                        file_path = resource.replace('file://', '')
                        markdown_content += f"- Modified: `{file_path}`\n"

                        # Show edit details if available
                        if edit.get('originalToCurrentEdit'):
                            markdown_content += "  - Edits:\n"
                            for change in edit['originalToCurrentEdit'][:5]:  # Limit to first 5 changes
                                if change.get('txt'):
                                    markdown_content += f"    - Added: `{change['txt'][:100]}...`\n"

                markdown_content += "\n"

            markdown_content += "---\n\n"

    return markdown_content


# Backward compatibility function
def convert_to_markdown(chat_data: Dict[str, Any], workspace_info: Dict[str, Any]) -> str:
    """Backward compatibility wrapper for convert_cursor_session_to_markdown"""
    return convert_cursor_session_to_markdown(chat_data, workspace_info)


def convert_to_html(markdown_content: str) -> str:
    """Convert markdown to HTML with GitHub styling"""
    html_content = markdown.markdown(markdown_content, extensions=['codehilite', 'fenced_code'])

    # GitHub-like CSS styling
    css_content = """
        .markdown-body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #24292e;
            background-color: #fff;
        }

        .markdown-body h1, .markdown-body h2, .markdown-body h3 {
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }

        .markdown-body pre {
            background-color: #f6f8fa;
            border-radius: 3px;
            padding: 16px;
            overflow: auto;
        }

        .markdown-body code {
            background-color: rgba(27,31,35,0.05);
            border-radius: 3px;
            padding: 0.2em 0.4em;
            font-size: 85%;
        }

        .markdown-body ul, .markdown-body ol {
            margin-top: 0.5em !important;
            margin-bottom: 0.5em !important;
            padding-left: 2em !important;
        }

        .markdown-body ul {
            list-style-type: disc !important;
        }

        .markdown-body ol {
            list-style-type: decimal !important;
        }

        @media (max-width: 767px) {
            .markdown-body {
                padding: 15px;
            }
        }
    """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cursor Chat History</title>
    <style>
        {css_content}
    </style>
</head>
<body class="markdown-body">
    {html_content}
</body>
</html>"""


def create_export_directories(output_dir: str) -> None:
    """Create base output directory and format-specific directories"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Create format-specific directories
    formats = ['html', 'markdown', 'json']
    for format_name in formats:
        (output_path / format_name).mkdir(parents=True, exist_ok=True)


def export_chat_session(session: Dict[str, Any], workspace: Dict[str, Any], workspace_name: str,
                        output_dir: str, workspace_data: Dict[str, Any]) -> None:
    """Export a single chat session"""
    title = session.get('customTitle') or f"Chat Session {session.get('sessionId', 'Unknown')}"
    timestamp = session.get('creationDate', '')
    filename = get_safe_filename(timestamp, title)

    # Convert to markdown
    markdown_content = convert_cursor_session_to_markdown(session, workspace['workspaceInfo'])

    # Save markdown version
    md_path = Path(output_dir) / 'markdown' / workspace_name / f"{filename}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(markdown_content, encoding='utf-8')

    # Convert to HTML and save
    html_content = convert_to_html(markdown_content)
    html_path = Path(output_dir) / 'html' / workspace_name / f"{filename}.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html_content, encoding='utf-8')

    # Add to workspace JSON data
    conversation = []
    if session.get('requests'):
        for request in session['requests']:
            # User message
            if request.get('message', {}).get('text'):
                conversation.append({
                    'role': 'User',
                    'text': request['message']['text'],
                    'timestamp': request.get('timestamp', '')
                })

            # AI response
            if request.get('response'):
                response_parts = []
                for response_item in request['response']:
                    if response_item.get('value'):
                        response_parts.append(response_item['value'])

                if response_parts:
                    conversation.append({
                        'role': 'Cursor',
                        'text': '\n'.join(response_parts),
                        'timestamp': request.get('timestamp', '')
                    })

    workspace_data['chats'].append({
        'title': title,
        'sessionId': session.get('sessionId', ''),
        'timestamp': timestamp,
        'conversation': conversation
    })


def export_editing_session(editing_session: Dict[str, Any], workspace: Dict[str, Any], workspace_name: str,
                          output_dir: str, workspace_data: Dict[str, Any]) -> None:
    """Export a single chat editing session"""
    # Skip empty editing sessions
    if not editing_session.get('linearHistory'):
        return

    session_id = editing_session.get('sessionId', 'Unknown')
    title = f"Chat Editing Session {session_id}"
    filename = f"editing-session-{session_id}"

    # Convert to markdown
    markdown_content = convert_cursor_editing_session_to_markdown(editing_session, workspace['workspaceInfo'])

    # Save markdown version
    md_path = Path(output_dir) / 'markdown' / workspace_name / f"{filename}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(markdown_content, encoding='utf-8')

    # Convert to HTML and save
    html_content = convert_to_html(markdown_content)
    html_path = Path(output_dir) / 'html' / workspace_name / f"{filename}.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html_content, encoding='utf-8')

    # Add to workspace JSON data
    workspace_data['editingSessions'].append({
        'title': title,
        'sessionId': session_id,
        'version': editing_session.get('version', ''),
        'editCount': len(editing_session.get('linearHistory', []))
    })


def export_workspace(workspace: Dict[str, Any], output_dir: str) -> Optional[Dict[str, Any]]:
    """Export a single workspace"""
    # Check if workspace has any data
    has_chat_sessions = workspace.get('chatSessions') and len(workspace['chatSessions']) > 0
    has_editing_sessions = workspace.get('editingSessions') and len(workspace['editingSessions']) > 0

    # Extract workspace name from folder path
    workspace_folder = workspace.get('workspaceInfo', {}).get('folder', '')
    if workspace_folder.startswith('file://'):
        workspace_folder = workspace_folder.replace('file://', '')

    workspace_name = Path(workspace_folder).name if workspace_folder else 'Unknown'

    if not has_chat_sessions and not has_editing_sessions:
        print(f'  - Skipping empty workspace: {workspace_name}')
        return None

    print(f'Processing workspace: {workspace_name}')

    # Create workspace directories for markdown and html
    for format_name in ['html', 'markdown']:
        (Path(output_dir) / format_name / workspace_name).mkdir(parents=True, exist_ok=True)

    # Prepare workspace JSON data
    workspace_data = {
        'workspace': workspace_name,
        'workspaceInfo': workspace.get('workspaceInfo', {}),
        'chats': [],
        'editingSessions': []
    }

    # Export chat sessions
    if has_chat_sessions:
        print(f"  - Exporting {len(workspace['chatSessions'])} chat sessions")
        for session in workspace['chatSessions']:
            export_chat_session(session, workspace, workspace_name, output_dir, workspace_data)

    # Export editing sessions
    if has_editing_sessions:
        print(f"  - Exporting {len(workspace['editingSessions'])} editing sessions")
        for editing_session in workspace['editingSessions']:
            export_editing_session(editing_session, workspace, workspace_name, output_dir, workspace_data)

    # Save workspace JSON file if there's data
    if workspace_data['chats'] or workspace_data['editingSessions']:
        json_path = Path(output_dir) / 'json' / f"{workspace_name}.json"
        json_path.write_text(json.dumps(workspace_data, indent=2), encoding='utf-8')

    return workspace_data


def export_all_workspaces(chat_history: List[Dict[str, Any]], output_dir: str) -> List[Optional[Dict[str, Any]]]:
    """Export all workspaces from chat history"""
    create_export_directories(output_dir)

    results = []
    for workspace in chat_history:
        workspace_data = export_workspace(workspace, output_dir)
        results.append(workspace_data)

    return results


def load_workspace_data(workspace_dir: Path) -> Optional[Dict[str, Any]]:
    """Load workspace data from Cursor workspace directory structure"""
    try:
        # Load workspace metadata
        workspace_json_path = workspace_dir / 'workspace.json'
        if not workspace_json_path.exists():
            return None

        with open(workspace_json_path, 'r', encoding='utf-8') as f:
            workspace_info = json.load(f)

        # Load chat sessions
        chat_sessions = []
        chat_sessions_dir = workspace_dir / 'chatSessions'
        if chat_sessions_dir.exists():
            session_count = 0
            for session_file in chat_sessions_dir.glob('*.json'):
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                        # Only include sessions that have actual conversations
                        if session_data.get('requests') and len(session_data['requests']) > 0:
                            chat_sessions.append(session_data)
                            session_count += 1
                except Exception as e:
                    print(f"  Warning: Could not load chat session {session_file.name}: {e}")

            if session_count > 0:
                print(f"  - Loaded {session_count} chat sessions")

        # Load chat editing sessions
        editing_sessions = []
        editing_sessions_dir = workspace_dir / 'chatEditingSessions'
        if editing_sessions_dir.exists():
            editing_count = 0
            for session_dir in editing_sessions_dir.iterdir():
                if session_dir.is_dir():
                    state_file = session_dir / 'state.json'
                    if state_file.exists():
                        try:
                            with open(state_file, 'r', encoding='utf-8') as f:
                                state_data = json.load(f)
                                # Only include sessions that have actual editing history
                                if state_data.get('linearHistory') and len(state_data['linearHistory']) > 0:
                                    editing_sessions.append(state_data)
                                    editing_count += 1
                        except Exception as e:
                            print(f"  Warning: Could not load editing session {session_dir.name}: {e}")

            if editing_count > 0:
                print(f"  - Loaded {editing_count} editing sessions")

        # Only return workspace data if there are actual conversations
        if chat_sessions or editing_sessions:
            return {
                'workspaceInfo': workspace_info,
                'chatSessions': chat_sessions,
                'editingSessions': editing_sessions
            }
        else:
            return None

    except Exception as e:
        print(f"Error loading workspace data from {workspace_dir}: {e}")
        return None


def load_chat_history_from_directory(workspace_storage_dir: str) -> List[Dict[str, Any]]:
    """Load chat history from Cursor workspace storage directory"""
    storage_path = Path(workspace_storage_dir)

    if not storage_path.exists():
        raise FileNotFoundError(f"Workspace storage directory not found: {workspace_storage_dir}")

    if not storage_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {workspace_storage_dir}")

    workspaces = []

    # Iterate through each workspace directory
    for workspace_dir in storage_path.iterdir():
        if workspace_dir.is_dir() and workspace_dir.name != 'images':
            print(f"Processing workspace directory: {workspace_dir.name}")
            workspace_data = load_workspace_data(workspace_dir)
            if workspace_data:
                workspaces.append(workspace_data)
            else:
                print(f"  - Skipping {workspace_dir.name} (no valid data)")

    return workspaces


def main():
    """Main function to run the export process"""
    import argparse

    parser = argparse.ArgumentParser(description='Export Cursor chat history to markdown and HTML')
    parser.add_argument('input_path', help='Path to the chat history JSON file or workspace storage directory')
    parser.add_argument('output_dir', help='Output directory for exported files')

    args = parser.parse_args()

    # Check if input path exists
    if not Path(args.input_path).exists():
        print(f"Error: Input path '{args.input_path}' not found")
        return 1

    try:
        input_path = Path(args.input_path)

        # Determine if input is a file or directory
        if input_path.is_file():
            print("Loading chat history from JSON file...")
            # Load from JSON file (original behavior)
            with open(input_path, 'r', encoding='utf-8') as f:
                chat_history = json.load(f)
        elif input_path.is_dir():
            print("Loading chat history from workspace storage directory...")
            # Load from workspace storage directory (new behavior)
            chat_history = load_chat_history_from_directory(str(input_path))
        else:
            print(f"Error: Input path is neither a file nor directory: {args.input_path}")
            return 1

        if not chat_history:
            print("No chat history data found to export.")
            return 1

        # Export all workspaces
        results = export_all_workspaces(chat_history, args.output_dir)

        # Print summary
        processed_count = sum(1 for r in results if r is not None)
        print(f"\nExport complete! Processed {processed_count} workspaces.")
        print(f"Files saved to: {args.output_dir}")

        return 0

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
