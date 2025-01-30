from setuptools import setup, find_packages

setup(
    name="excel-processor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas==2.1.0",
        "openpyxl==3.1.2",
        "sqlalchemy==2.0.20",
        "fastapi==0.103.1",
        "uvicorn==0.23.2",
        "python-multipart==0.0.6",
        "pywin32==306",
        "pydantic==2.3.0",
        "requests==2.31.0"
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
            "excel-processor=main:main",
            "excel-processor-demo=demo.demo:demo_system",
        ],
    },
) 