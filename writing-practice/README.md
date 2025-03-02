# Malay-Jawi Learning Application

This Streamlit application helps users learn to write Malay in Jawi script through interactive practice.

## Features

- Generates simple Malay sentences for practice using Groq LLM
- Allows users to upload images of their handwritten Jawi
- Provides feedback and grading on the uploaded writing
- Includes hints and translations for learning support

## Setup Instructions

1. Install the required dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

2. Set up your Groq API key:
   \`\`\`
   export GROQ_API_KEY=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
   \`\`\`
   
   Or on Windows:
   \`\`\`
   set GROQ_API_KEY=your_api_key_here
   \`\`\`

3. Run the Streamlit application:
   \`\`\`
   streamlit run app.py
   \`\`\`

4. Open your browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

## Usage

1. Click "Generate Sentence" to start practicing
2. Write the displayed English sentence in Jawi script on paper
3. Take a photo of your writing and upload it
4. Click "Submit for Review" to get feedback
5. Review your grade and feedback
6. Click "Next Question" to continue practicing

## Notes

- This application uses Groq's LLM for sentence generation
- The app will fall back to mock responses if the Groq API key is not set
- In a production environment, you would need to:
  - Connect to a real API endpoint for word collection
  - Implement actual OCR for Jawi script
  - Use a proper LLM integration for grading

