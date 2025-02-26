import streamlit as st
import json
import os
import requests
import re
from dotenv import load_dotenv

# Function to clean malformed JSON with unescaped parentheses in values
def clean_json_with_parentheses(json_str):
    # First attempt: Fix unescaped parentheses in values
    # This handles cases like: "english": "Father" (Informal)
    cleaned = re.sub(r'("english":\s*"[^"]+)"\s*\(([^)]+)\)', r'\1 (\2)"', json_str)
    
    # Second attempt: If there are still issues, try a more aggressive approach
    try:
        json.loads(cleaned)
        return cleaned
    except json.JSONDecodeError:
        # Try to extract all valid word entries and rebuild the JSON
        words = []
        pattern = r'\{\s*"malay":\s*"([^"]+)",\s*"jawi":\s*"([^"]+)",\s*"english":\s*"([^"]+)(?:\s*\([^)]+\))?"'
        matches = re.findall(pattern, json_str)
        
        for malay, jawi, english in matches:
            words.append({
                "malay": malay,
                "jawi": jawi,
                "english": english
            })
        
        if words:
            return json.dumps({"words": words})
        
        # If all else fails, return the original string
        return json_str

# Set page configuration
st.set_page_config(
    page_title="Malay Vocabulary Generator",
    page_icon="📚",
    layout="centered"
)

# Add custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .json-output {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1rem;
        font-family: monospace;
        white-space: pre-wrap;
    }
    .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<p class="main-header">Malay Vocabulary Generator</p>', unsafe_allow_html=True)
st.markdown("Generate Malay vocabulary words based on thematic categories")

# Initialize Ollama client
@st.cache_resource
def get_ollama_client():
    # Default to localhost:8008 if not specified in environment
    # The docker-compose.yml maps port 8008 to 11434
    ollama_host = os.environ.get("OLLAMA_HOST", "localhost")
    ollama_port = os.environ.get("OLLAMA_PORT", "8008")
    ollama_endpoint = f"http://{ollama_host}:{ollama_port}"
    return ollama_endpoint

# Get the Ollama endpoint
ollama_endpoint = get_ollama_client()

# Input form
with st.form("vocabulary_form"):
    category = st.text_input("Enter vocabulary category (e.g., 'Food', 'Family')")
    model = st.selectbox("Select model", ["llama3.1:latest", "llama3.2:1b", "llama3:8b", "mistral:latest"], index=0)
    submitted = st.form_submit_button("Generate Vocabulary")
    
    if submitted and category:
        with st.spinner("Generating vocabulary..."):
            try:
                # Create the prompt for the LLM
                prompt = f"""Generate a list of 10 Malay vocabulary words related to the category "{category}". 
                For each word, provide the Malay word, its Jawi script representation, and English translation.
                Format the response as a JSON object with a "words" array containing objects with "malay", "jawi", and "english" properties.
                
                IMPORTANT: Make sure to properly escape any special characters in the JSON. If the English translation contains parentheses, 
                include them as part of the string value and not outside the quotes. For example, use "english": "Father (Informal)" 
                and NOT "english": "Father" (Informal).
                
                Example format:
                {{
                  "words": [
                    {{
                      "malay": "Kawan",
                      "jawi": "كوان",
                      "english": "Friend"
                    }},
                    {{
                      "malay": "Bapa",
                      "jawi": "بابا",
                      "english": "Father (Informal)"
                    }}
                  ]
                }}"""
                
                # Call the Ollama API
                response = requests.post(
                    f"{ollama_endpoint}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                # Extract and parse the response
                if response.status_code == 200:
                    result = response.json()
                    result_text = result.get("response", "")
                    
                    # Find JSON content in the response (in case the model adds extra text)
                    json_start = result_text.find('{')
                    json_end = result_text.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_content = result_text[json_start:json_end]
                        try:
                            vocabulary_data = json.loads(clean_json_with_parentheses(json_content))
                        except json.JSONDecodeError:
                            st.error(f"Failed to parse JSON from response: {json_content}")
                            st.info("Attempting manual extraction of vocabulary data...")
                            # Try to manually extract the data using regex
                            words_data = []
                            word_pattern = re.compile(r'"malay":\s*"([^"]+)",\s*"jawi":\s*"([^"]+)",\s*"english":\s*"([^"]+)(?:\([^)]+\)[^"]*)?')
                            matches = word_pattern.findall(json_content)
                            if matches:
                                for malay, jawi, english in matches:
                                    words_data.append({
                                        "malay": malay,
                                        "jawi": jawi,
                                        "english": english
                                    })
                                vocabulary_data = {"words": words_data}
                            else:
                                # Try one more approach - parse the exact format from the error message
                                try:
                                    # This handles the specific format in the error message
                                    import re
                                    # Extract all the word entries
                                    pattern = r'\{\s*"malay":\s*"([^"]+)",\s*"jawi":\s*"([^"]+)",\s*"english":\s*"([^"]+)(?:\s*\([^)]+\))?"(?:\s*\})(?:,|\s*\])'
                                    matches = re.findall(pattern, json_content)
                                    if matches:
                                        words_data = []
                                        for malay, jawi, english in matches:
                                            words_data.append({
                                                "malay": malay,
                                                "jawi": jawi, 
                                                "english": english
                                            })
                                        vocabulary_data = {"words": words_data}
                                    else:
                                        st.error("Could not extract vocabulary data from the response.")
                                except Exception as e:
                                    st.error(f"Error during manual extraction: {str(e)}")
                                    st.error("Could not extract vocabulary data from the response.")
                    else:
                        try:
                            vocabulary_data = json.loads(clean_json_with_parentheses(result_text))
                        except json.JSONDecodeError:
                            st.error(f"Failed to parse JSON from response: {result_text}")
                            st.info("Attempting manual extraction of vocabulary data...")
                            # Try to manually extract the data using regex
                            words_data = []
                            word_pattern = re.compile(r'"malay":\s*"([^"]+)",\s*"jawi":\s*"([^"]+)",\s*"english":\s*"([^"]+)(?:\([^)]+\)[^"]*)?')
                            matches = word_pattern.findall(result_text)
                            if matches:
                                for malay, jawi, english in matches:
                                    words_data.append({
                                        "malay": malay,
                                        "jawi": jawi,
                                        "english": english
                                    })
                                vocabulary_data = {"words": words_data}
                            else:
                                # Try one more approach - parse the exact format from the error message
                                try:
                                    # This handles the specific format in the error message
                                    import re
                                    # Extract all the word entries
                                    pattern = r'\{\s*"malay":\s*"([^"]+)",\s*"jawi":\s*"([^"]+)",\s*"english":\s*"([^"]+)(?:\s*\([^)]+\))?"(?:\s*\})(?:,|\s*\])'
                                    matches = re.findall(pattern, result_text)
                                    if matches:
                                        words_data = []
                                        for malay, jawi, english in matches:
                                            words_data.append({
                                                "malay": malay,
                                                "jawi": jawi, 
                                                "english": english
                                            })
                                        vocabulary_data = {"words": words_data}
                                    else:
                                        st.error("Could not extract vocabulary data from the response.")
                                except Exception as e:
                                    st.error(f"Error during manual extraction: {str(e)}")
                                    st.error("Could not extract vocabulary data from the response.")
                    
                    # Store the result in session state
                    st.session_state.vocabulary = vocabulary_data
                    st.session_state.json_str = json.dumps(vocabulary_data, indent=2)
                else:
                    st.error(f"Error from Ollama API: {response.status_code} - {response.text}")
                
            except Exception as e:
                st.error(f"Error generating vocabulary: {str(e)}")

# Display results if available
if 'vocabulary' in st.session_state:
    st.subheader("Generated Vocabulary")
    
    # Display the vocabulary as a table
    if 'words' in st.session_state.vocabulary:
        words = st.session_state.vocabulary['words']
        
        # Create columns for the table
        cols = st.columns(3)
        cols[0].markdown("**Malay**")
        cols[1].markdown("**Jawi**")
        cols[2].markdown("**English**")
        
        for word in words:
            cols = st.columns(3)
            cols[0].write(word.get('malay', ''))
            cols[1].write(word.get('jawi', ''))
            cols[2].write(word.get('english', ''))
    
    # Display the raw JSON
    st.subheader("JSON Output")
    st.markdown(f'<div class="json-output">{st.session_state.json_str}</div>', unsafe_allow_html=True)
    
    # Copy button
    if st.button("Copy JSON to Clipboard"):
        # Use JavaScript to copy to clipboard
        js = f"""
        <script>
            navigator.clipboard.writeText('{st.session_state.json_str.replace("'", "\\'")}');
            // Create a toast notification
            const toast = document.createElement('div');
            toast.style.position = 'fixed';
            toast.style.bottom = '20px';
            toast.style.left = '50%';
            toast.style.transform = 'translateX(-50%)';
            toast.style.backgroundColor = '#4CAF50';
            toast.style.color = 'white';
            toast.style.padding = '16px';
            toast.style.borderRadius = '4px';
            toast.style.zIndex = '1000';
            toast.textContent = 'Copied to clipboard!';
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        </script>
        """
        st.components.v1.html(js)

# Add instructions at the bottom
with st.expander("How to use"):
    st.markdown("""
    1. Enter a thematic category in the text field (e.g., "Food", "Family", "Travel")
    2. Click "Generate Vocabulary" to create a list of Malay words related to that category
    3. View the generated vocabulary in both table format and JSON format
    4. Click "Copy JSON to Clipboard" to copy the JSON data
    """)