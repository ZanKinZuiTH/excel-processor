# 🚀 Excel Processor

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Discord](https://img.shields.io/badge/discord-join%20chat-7289da)]()

> Intelligent Excel Processing System with AI-powered Analysis and Template Management

[🇹🇭 Thai](README.md) | [🇺🇸 English](README_EN.md) | [🎮 Demo](README_DEMO.md)

<p align="center">
  <img src="docs/images/demo.gif" alt="Excel Processor Demo" width="600">
</p>

## 📑 Table of Contents
- [✨ Key Features](#-key-features)
- [🛠️ Installation](#️-installation)
- [📖 Usage](#-usage)
- [🔧 Configuration](#-configuration)
- [📚 Documentation](#-documentation)

## ✨ Key Features

### 🎯 Template Management
- Create and edit templates automatically
- Share templates between users
- Control template versions
- AI-powered template recommendations

### 📊 Data Processing
- Automatic data structure analysis
- Error detection and correction
- Automatic data format conversion
- Batch processing support

### 🤖 AI Intelligence
- Trend analysis with Prophet
- Data forecasting with LSTM
- Feature importance calculation
- Automatic learning and improvement

### 🖨️ Print System
- Automatic print queue management
- Batch printing support
- Flexible printer selection
- Automatic document formatting

### 🌐 Web API & UI
- Complete REST API
- Beautiful UI with Streamlit
- Async operation support
- Real-time notification system

### 🔒 Security System
- JWT Authentication support
- Access control management
- Automatic data encryption
- Attack prevention

### 📈 Monitoring System
- Resource usage tracking
- Performance analysis
- Threshold-based alerts
- Automatic report generation

## 🛠️ Installation

1. Clone the project:
```bash
git clone https://github.com/yourusername/excel-processor.git
cd excel-processor
```

2. Create Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install Dependencies:
```bash
pip install -r requirements.txt
```

4. Setup the system:
```bash
python cli.py setup
```

## 📖 Usage

### 🖥️ Web Interface
1. Start the system:
```bash
python cli.py start
```
2. Open your browser and navigate to `http://localhost:8501`

### 💻 Command Line
```bash
# Process a file
python cli.py process input.xlsx

# Create template
python cli.py template create

# Analyze with AI
python cli.py analyze data.xlsx
```

## 🔧 Configuration

### ⚙️ Basic Settings
```env
APP_NAME=Excel Template Manager
APP_VERSION=1.0.0
DEBUG=False
```

### 🔐 Security Settings
```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 🗄️ Database Settings
```env
DATABASE_URL=sqlite:///./excel_data.db
```

## 📚 Documentation

- [📘 User Guide](docs/user_guide.md)
- [🔧 Installation Guide](docs/server_setup.md)
- [📊 Presentation Guide](docs/presentation_guide.md)
- [🧪 Testing Guide](docs/testing_guide.md)

## 👥 Developer

- **ZanKinZuiTH** - [GitHub](https://github.com/ZanKinZuiTH)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details

## 📫 Support

If you encounter issues or need assistance:
- 🐛 [GitHub Issues](https://github.com/ZanKinZuiTH/excel-processor/issues)
- 📧 Email: support@brxg.co.th
- 💬 Line Official: @brxgdev

---
⌨️ with ❤️ by [ZanKinZuiTH](https://github.com/ZanKinZuiTH) 