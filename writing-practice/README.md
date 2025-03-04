# Malay-Jawi Learning Application

A Streamlit application for learning and practicing Jawi script writing.

## Overview

This application helps users learn to write in Jawi script by:
1. Displaying Malay phrases in Jawi script
2. Providing a canvas for users to practice writing
3. Giving feedback on the user's writing using OCR technology

## Running the Application

```bash
streamlit run app.py
```

## Features

- Interactive drawing canvas for practicing Jawi script
- OCR-based grading of handwritten Jawi script
- Feedback on writing accuracy and quality
- Malay-English-Jawi translations for learning context

## Setup Instructions

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Groq API key (optional, for LLM-based sentence generation):
   ```bash
   export GROQ_API_KEY=your_api_key_here
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Troubleshooting

If you encounter issues with the OCR functionality:

1. Make sure you have the correct versions of EasyOCR and PyTorch installed
2. Try updating your graphics drivers if you're using GPU acceleration
3. Check the console output for specific error messages
4. Ensure your writing has good contrast against the background

## Dependencies

- streamlit
- streamlit_drawable_canvas
- Pillow
- numpy
- python-dotenv
- groq (optional, for LLM integration)
- easyocr (for OCR functionality)
- torch (required by easyocr)

## Project Structure

- `app.py`: Main application with OCR integration
- `data.py`: Word data management
- `grading.py`: OCR-based grading system for evaluating writing
- `llm.py`: LLM integration for generating sentences
- `canvas.py`: Canvas management utilities

## Technical Notes

- The OCR functionality uses Arabic language models since Jawi script is based on Arabic script
- The application uses environment variables to optimize OCR performance
- Error handling is implemented throughout the application to ensure stability
