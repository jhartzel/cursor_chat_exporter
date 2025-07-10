#!/usr/bin/env python3
"""
Test script for the Cursor Chat History Export Tool
Creates sample chat history data and demonstrates the export functionality
"""

import json
import tempfile
import os
from pathlib import Path
from cursor_export import export_all_workspaces

def create_sample_chat_history():
    """Create sample chat history data for testing"""
    sample_data = [
        {
            "workspaceInfo": {
                "id": "sample-workspace-1",
                "folder": "/Users/example/projects/sample-project",
                "lastModified": "2024-01-15T10:30:00Z"
            },
            "chatData": {
                "tabs": [
                    {
                        "title": "Python Function Help",
                        "timestamp": "2024-01-15T10:30:00Z",
                        "bubbles": [
                            {
                                "type": "user",
                                "text": "How do I create a function that calculates the factorial of a number?"
                            },
                            {
                                "type": "ai",
                                "text": "Here's a simple Python function to calculate factorial:",
                                "codeBlocks": [
                                    {
                                        "language": "python",
                                        "code": "def factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n - 1)\n\n# Example usage\nprint(factorial(5))  # Output: 120"
                                    }
                                ]
                            },
                            {
                                "type": "user",
                                "text": "Can you also show me an iterative version?"
                            },
                            {
                                "type": "ai",
                                "text": "Sure! Here's an iterative approach:",
                                "codeBlocks": [
                                    {
                                        "language": "python",
                                        "code": "def factorial_iterative(n):\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result\n\n# Example usage\nprint(factorial_iterative(5))  # Output: 120"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "title": "JavaScript Array Methods",
                        "timestamp": "2024-01-15T14:45:00Z",
                        "bubbles": [
                            {
                                "type": "user",
                                "text": "What are the most commonly used JavaScript array methods?"
                            },
                            {
                                "type": "ai",
                                "text": "Here are the most commonly used JavaScript array methods:",
                                "codeBlocks": [
                                    {
                                        "language": "javascript",
                                        "code": "// Array methods examples\nconst numbers = [1, 2, 3, 4, 5];\n\n// map - transform each element\nconst doubled = numbers.map(n => n * 2);\nconsole.log(doubled); // [2, 4, 6, 8, 10]\n\n// filter - select elements that match condition\nconst evens = numbers.filter(n => n % 2 === 0);\nconsole.log(evens); // [2, 4]\n\n// reduce - accumulate values\nconst sum = numbers.reduce((acc, n) => acc + n, 0);\nconsole.log(sum); // 15\n\n// forEach - execute function for each element\nnumbers.forEach(n => console.log(n));\n\n// find - get first element that matches condition\nconst found = numbers.find(n => n > 3);\nconsole.log(found); // 4"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "composers": {
                    "allComposers": [
                        {
                            "composerId": "comp-1",
                            "name": "Database Query Helper",
                            "lastUpdatedAt": "2024-01-15T16:20:00Z",
                            "conversation": [
                                {
                                    "type": 1,  # User message
                                    "text": "Help me write a SQL query to find all users who registered in the last 30 days"
                                },
                                {
                                    "type": 2,  # AI message
                                    "text": "Here's a SQL query to find users who registered in the last 30 days:",
                                    "suggestedCodeBlocks": [
                                        {
                                            "language": "sql",
                                            "code": "SELECT \n    user_id,\n    username,\n    email,\n    registration_date\nFROM users \nWHERE registration_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)\nORDER BY registration_date DESC;"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
    ]

    return sample_data

def test_export():
    """Test the export functionality with sample data"""
    print("Creating sample chat history data...")
    chat_history = create_sample_chat_history()

    # Create temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Exporting to temporary directory: {temp_dir}")

        # Export the data
        results = export_all_workspaces(chat_history, temp_dir)

        print(f"Export completed. Processing {len(results)} workspaces.")

        # Check what was created
        output_path = Path(temp_dir)

        print("\nGenerated directory structure:")
        for root, dirs, files in os.walk(temp_dir):
            level = root.replace(temp_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")

        # Show content of one markdown file
        markdown_files = list(output_path.glob("**/*.md"))
        if markdown_files:
            print(f"\nSample markdown content from {markdown_files[0].name}:")
            print("-" * 50)
            content = markdown_files[0].read_text()
            # Show first 500 characters
            print(content[:500] + "..." if len(content) > 500 else content)

        # Show JSON summary
        json_files = list(output_path.glob("**/*.json"))
        if json_files:
            print(f"\nJSON summary from {json_files[0].name}:")
            print("-" * 50)
            with open(json_files[0]) as f:
                data = json.load(f)
                print(f"Workspace: {data['workspace']}")
                print(f"Chats: {len(data['chats'])}")
                print(f"Composers: {len(data['composers'])}")
                if data['chats']:
                    print(f"First chat title: {data['chats'][0]['title']}")
                    print(f"First chat messages: {len(data['chats'][0]['conversation'])}")

if __name__ == "__main__":
    print("Cursor Chat History Export Tool - Test Script")
    print("=" * 50)

    try:
        test_export()
        print("\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
