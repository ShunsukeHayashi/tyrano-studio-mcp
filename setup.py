"""
TyranoStudio MCP Server
Setup script for distribution
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").split("\n")
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="tyrano-studio-mcp",
    version="1.0.0",
    author="Shunsuke Hayashi",
    author_email="noreply@example.com",
    description="MCP Server for TyranoStudio project management and development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ShunsukeHayashi/tyrano-studio-mcp",
    project_urls={
        "Bug Tracker": "https://github.com/ShunsukeHayashi/tyrano-studio-mcp/issues",
        "Documentation": "https://github.com/ShunsukeHayashi/tyrano-studio-mcp#readme",
        "Source Code": "https://github.com/ShunsukeHayashi/tyrano-studio-mcp",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="tyranoscript visual-novel game-development mcp claude-code",
    py_modules=["server"],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tyrano-mcp=server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["README.md", "LICENSE", "requirements.txt"],
    },
    zip_safe=False,
)