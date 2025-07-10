#!/usr/bin/env python3
"""
Setup script for Cursor Chat History Export Tool
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cursor-chat-exporter",
    version="1.0.0",
    author="Josh Hartzell",
    author_email="josh.hartzell@example.com",
    description="A Python tool to export Cursor chat history to markdown and HTML formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhartzel/cursor_chat_exporter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cursor-chat-exporter=cursor_chat_exporter.cursor_export:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
