import streamlit as st
from PIL import Image
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import utilities
from llm import LLMGenerator
from grading import GradingSystem
from canvas import CanvasManager
from data import fetch_words, Word

# Set page configuration
st.set_page_config(
    page_title="Malay-Jawi Learning App",
    page_icon="📝",
    layout="centered"
)

# Initialize session state
if 'state' not in st.session_state:
    st.session_state.state = "setup"
if 'words' not in st.session_state:
    st.session_state.words = []
if 'current_sentence' not in st.session_state:
    st.session_state.current_sentence = {}
if 'drawing_data' not in st.session_state:
    st.session_state.drawing_data = None
if 'grading_result' not in st.session_state:
    st.session_state.grading_result = None

def go_to_practice():
    """Transition to practice state."""
    # Select a random word
    word = random.choice(st.session_state.words)
    
    # Generate a sentence
    llm = LLMGenerator()
    sentence = llm.generate_sentence(word)
    
    # Update session state
    st.session_state.current_sentence = sentence
    st.session_state.drawing_data = None
    st.session_state.grading_result = None
    st.session_state.state = "practice"

def go_to_review(image: Image.Image):
    """Transition to review state."""
    # Grade the submission
    grading_result = GradingSystem.grade_submission(
        image,
        st.session_state.current_sentence["jawi"]
    )
    
    # Update session state
    st.session_state.grading_result = grading_result
    st.session_state.state = "review"

def main():
    """Main application."""
    # Display header
    st.title("Malay-Jawi Learning Application")
    
    # Fetch words if not already done
    if not st.session_state.words:
        with st.spinner("Loading word collection..."):
            st.session_state.words = fetch_words()
    
    # Handle different states
    if st.session_state.state == "setup":
        st.write("Welcome to the Malay-Jawi Learning Application!")
        st.write("Press the button below to generate a sentence and start practicing.")
        
        if st.button("Generate Sentence", key="generate_btn"):
            go_to_practice()
    
    elif st.session_state.state == "practice":
        st.subheader("Practice Writing in Jawi")
        
        # Display the English sentence
        st.markdown(f"**Translate this sentence to Jawi:**")
        st.markdown(f"### {st.session_state.current_sentence['english']}")
        
        # Provide a hint option
        if st.checkbox("Show hint (Malay in Rumi script)"):
            st.info(st.session_state.current_sentence['rumi'])
        
        # Drawing canvas
        st.markdown("### Write your answer here:")
        image, has_drawing = CanvasManager.create_canvas()
        
        # Clear canvas button
        if st.button("Clear Canvas"):
            st.session_state.drawing_data = None
            st.experimental_rerun()
        
        # Submit button
        if st.button("Submit for Review", key="submit_btn"):
            if has_drawing and image is not None:
                st.session_state.drawing_data = image
                go_to_review(image)
            else:
                st.warning("Please write something before submitting.")
    
    elif st.session_state.state == "review":
        st.subheader("Review")
        
        # Display the English sentence again
        st.markdown(f"**Original sentence:**")
        st.markdown(f"### {st.session_state.current_sentence['english']}")
        
        # Display the drawing
        if st.session_state.drawing_data:
            st.image(st.session_state.drawing_data, caption="Your Jawi writing", use_column_width=True)
        
        # Display grading results
        if st.session_state.grading_result:
            st.markdown("### Grading Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Your Writing (Jawi):**")
                st.markdown(f"<div dir='rtl' style='font-size: 24px;'>{st.session_state.grading_result['transcribed_jawi']}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Expected (Jawi):**")
                st.markdown(f"<div dir='rtl' style='font-size: 24px;'>{st.session_state.current_sentence['jawi']}</div>", unsafe_allow_html=True)
            
            st.markdown("**Transcription (Rumi):**")
            st.markdown(f"{st.session_state.grading_result['transcribed_rumi']}")
            
            st.markdown("**Translation:**")
            st.markdown(f"{st.session_state.grading_result['english_translation']}")
            
            # Display grade with appropriate color
            grade = st.session_state.grading_result['grade']
            grade_color = "green" if grade == "A" else "orange" if grade == "B" else "red"
            st.markdown(f"**Grade:** <span style='color:{grade_color}; font-size:24px; font-weight:bold;'>{grade}</span>", unsafe_allow_html=True)
            
            st.markdown("**Feedback:**")
            st.markdown(f"{st.session_state.grading_result['feedback']}")
        
        # Next question button
        if st.button("Next Question", key="next_btn"):
            go_to_practice()

if __name__ == "__main__":
    main()
