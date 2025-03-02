# Malay-Jawi Learning Application Technical Specification

## Initialization Step
When the app initializes, it will:
- Fetch data from `GET localhost:5000/api/groups/:id/raw`, returning a collection of words in a JSON structure.
- The JSON will contain Malay words in both Rumi (Latin script) and Jawi script, along with their English translations.
- This collection of words will be stored in memory for use in sentence generation.

## Page States
This section describes the user experience and the app's behavior at different states.

### Setup State
- When the user starts the app, they will see a button labeled **"Generate Sentence"**.
- Pressing the button triggers the **Sentence Generator LLM**, which creates a sentence using a word from the stored collection.
- The app transitions to **Practice State**.

### Practice State
- The user is presented with a sentence in **English**.
- Below the sentence, an **interactive drawing canvas** is provided with the following features:
  - Canvas dimensions: 600x200 pixels
  - Customizable stroke width (1-25 pixels)
  - Color pickers for stroke and background colors
  - Clear canvas button
  - Right-to-left writing guidance
- The user writes the sentence in **Jawi script** directly on the canvas.
- A **"Submit for Review"** button sends the canvas data to the **Grading System**.
- Optional "Show hint" checkbox reveals the Malay sentence in Rumi script.
- The app transitions to **Review State** upon submission.

### Review State
- The user still sees the **English sentence**.
- The drawing canvas is replaced with a static image of their submission.
- The system displays feedback from the **Grading System**, including:
  - **Transcription of the Drawing** (extracted Jawi text)
  - **Translation of the Transcription** (Malay in Rumi and English translation)
  - **Grading**:
    - A **letter score** (A, B, C)
    - A **feedback description**, assessing accuracy and providing improvement suggestions
- A **"Next Question"** button generates a new sentence and transitions the app back to **Practice State**.

## Sentence Generator LLM
The app uses Groq's LLM to generate simple Malay sentences based on a given word.

### Configuration
- Model: llama3-8b-8192
- Temperature: 0.7
- Max tokens: 500

### Prompt Template