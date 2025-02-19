from setuptools import setup, find_packages

setup(
    name="excel-processor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # Core Dependencies
        "pandas>=1.5.0,<2.0.0",
        "openpyxl>=3.0.0,<4.0.0",
        "numpy>=1.21.0,<2.0.0",
        
        # Web Interface
        "streamlit>=1.31.0",
        "streamlit-option-menu>=0.3.12",
        "streamlit-extras>=0.4.0",
        "plotly>=5.19.0",
        "fastapi>=0.68.1",
        "uvicorn>=0.15.0",
        
        # DICOM Support
        "pydicom>=2.3.0",
        "pillow>=9.0.0",
        "opencv-python>=4.5.0",
        
        # Security
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.5",
        "python-dotenv>=0.19.0",
        
        # CLI Tools
        "rich>=13.7.0",
        "typer>=0.9.0",
        
        # Testing
        "pytest>=6.2.5",
        "pytest-cov>=2.12.1",
        "pytest-asyncio>=0.15.1"
    ],
    extras_require={
        'dev': [
            "black>=21.9b0",
            "flake8>=3.9.2",
            "mypy>=0.910",
            "pre-commit>=2.15.0"
        ],
        'doc': [
            "sphinx>=4.2.0",
            "sphinx-rtd-theme>=1.0.0"
        ]
    },
    author="ZanKinZuiTH",
    author_email="zankinzuith@example.com",
    description="ระบบประมวลผลและจัดการเอกสาร Excel อัจฉริยะ พร้อมระบบ DICOM",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ZanKinZuiTH/excel-processor",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "excel-processor=cli:app",
            "excel-processor-ui=ui:main",
        ],
    },
    package_data={
        "excel_processor": ["assets/*", "templates/*"],
    },
    include_package_data=True,
) 