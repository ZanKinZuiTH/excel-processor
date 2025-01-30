# 📊 Excel Processor - Intelligent Excel Processing System

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-BRXG%20Co.-green)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()

## 📌 Table of Contents
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Core Features](#-core-features)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Future Development](#-future-development)
- [Developers](#-developers)

## ⭐ Key Features
- 🚀 **Easy to Use**: Install and start using within 5 minutes
- 🔄 **Automatic Processing**: Automated Excel data analysis
- 🔍 **Data Validation**: Detect null values, duplicates, and outliers
- 📊 **Deep Analysis**: Basic statistics, grouping, and trends
- 🧹 **Data Cleaning**: Automatic handling of nulls and duplicates
- 🌐 **Bilingual**: Thai/English support
- ⚙️ **Customizable**: Flexible configuration options
- 📱 **Responsive**: Works on both Desktop and Mobile

## 📥 Installation
1. Install Python 3.8 or higher
```bash
# Download the project
git clone https://github.com/BRXG/excel-processor.git
cd excel-processor

# Install dependencies
pip install -r requirements.txt

# Setup the system
python cli.py setup
```

## 🚀 Usage
### GUI (Streamlit)
```bash
python cli.py start
```
Open your browser and navigate to http://localhost:8501

### CLI
```bash
# Process a file
python cli.py process input.xlsx

# Run tests
python cli.py test

# Check version
python cli.py version
```

## 🛠️ Core Features

### 1. Data Processing
```python
from excel_processor import ExcelProcessor

# Create instance
processor = ExcelProcessor("data.xlsx")

# Process data
result = processor.process_file()
```

### 2. Data Validation
```python
# Validate data
validation = processor.validate_data()

# View validation results
print(f"Null values: {validation['null_check']}")
print(f"Duplicates: {validation['duplicate_check']}")
print(f"Outliers: {validation['outliers']}")
```

### 3. Data Analysis
```python
# Analyze data
analysis = processor.analyze_data()

# View analysis results
print(f"Statistics: {analysis['numeric_stats']}")
print(f"Grouping: {analysis['groupby_results']}")
```

### 4. Data Cleaning
```python
# Clean data
processor.clean_data()
```

## 📁 Project Structure
```
excel_processor/
├── processor.py     # Main processing system
├── config.py        # System configuration
├── security.py      # Security system
├── ui.py            # User interface
└── tests/           # Test suite
```

## 🧪 Testing
```bash
# Run all tests
pytest tests/

# Run tests with coverage report
pytest tests/ --cov=./ --cov-report=xml
```

## 🔄 Future Development
1. Add advanced data analytics
2. Implement real-time reporting
3. Develop external API services
4. Add support for additional file formats
5. Add automatic data pattern detection
6. Develop data correction recommendations

## 👨‍💻 Developers
- BRXG Co. Development Team
- Email: contact@brxg.co.th
- Website: https://brxg.co.th

## 📝 License
Copyright © 2024 BRXG Co. All rights reserved.

This software is proprietary and confidential. 
Unauthorized copying of this file, via any medium is strictly prohibited.
Written by BRXG Development Team <dev@brxg.co.th>, 2024

## 📫 Support
If you encounter issues or need assistance, contact us at:
- 🐛 [GitHub Issues](https://github.com/BRXG/excel-processor/issues)
- 📧 Email: support@brxg.co.th
- 💬 Line Official: @brxgdev

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details

## 👥 Developer

- **ZanKinZuiTH** - [GitHub](https://github.com/ZanKinZuiTH)

---
⌨️ with ❤️ by [ZanKinZuiTH](https://github.com/ZanKinZuiTH) 