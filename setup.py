from setuptools import setup, find_packages

setup(
    name="excel-processor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl",
        "pytest",
        "pytest-cov",
        "streamlit>=1.31.0",
        "streamlit-option-menu>=0.3.12",
        "streamlit-extras>=0.4.0",
        "plotly>=5.19.0",
        "rich>=13.7.0",
        "typer>=0.9.0"
    ],
    author="ZanKinZuiTH",
    author_email="zankinzuith@example.com",
    description="ระบบประมวลผลและจัดการเอกสาร Excel อัจฉริยะ",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ZanKinZuiTH/excel-processor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "excel-processor=cli:app",
            "excel-processor-ui=ui:main",
        ],
    },
) 