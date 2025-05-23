## Overview

This project is an AI-powered application designed to help individuals prepare for the U.S. Naturalization Test. It provides an interactive platform where users can practice answering the 100 civics questions that are part of the naturalization test.

### Key Features
- Interactive Q&A interface for practicing civics questions
- Real-time feedback on answers
- Comprehensive coverage of all 100 official civics questions
- User-friendly interface built with Streamlit
- Progress tracking and performance analytics

### Purpose
The application aims to make the naturalization test preparation process more engaging and effective by providing an interactive learning experience. It helps applicants build confidence and improve their knowledge of U.S. history, government, and civics.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/naturalization_civic_qa.git
cd naturalization_civic_qa
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the Streamlit application:

```bash
streamlit run app.py
```

The application will start and open in your default web browser. If it doesn't open automatically, you can access it at http://localhost:8501

## Development

- The application uses Streamlit for the web interface
- Watchdog is used for file system monitoring
- Make sure to activate your virtual environment before running the application
