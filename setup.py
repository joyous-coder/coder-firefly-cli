from setuptools import setup, find_packages

setup(
    name="coder-firefly-cli",
    version="1.0.0",
    description="Firefly III CLI - 个人财务管理命令行工具",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="coder",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "coder-firefly-cli=cli:main",
        ],
    },
    install_requires=[
        "click>=8.0",
        "requests>=2.25",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "responses>=0.25",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
    ],
    keywords="firefly-iii cli finance personal-finance",
    license="MIT",
)
