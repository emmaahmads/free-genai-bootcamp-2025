import streamlit as st
from PIL import Image
import random
from dotenv import load_dotenv
import os
import traceback
import sys

# Configure error handling
def handle_exception(exc_type, exc_value, exc_traceback):
    print(f"Uncaught exception: {exc_type.__name__}: {exc_value}")
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    
sys.excepthook = handle_exception

# Set environment variables to help prevent segmentation faults with EasyOCR
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

# Load environment variables
load_dotenv()

try:
    # Import utilities
    from llm import LLMGenerator
    from grading import GradingSystem
    from data import fetch_words
    from canvas import CanvasManager
except Exception as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# Set page configuration
st.set_page_config(
    page_title="Malay-Jawi Learning App",
    page_icon="📝",
    layout="centered"
)

# Initialize session state
if 'state' not in st.session_state:
    st.session_state.state = "setup"
    st.session_state.words = []
    st.session_state.current_sentence = {}
    st.session_state.drawing_data = None
    st.session_state.grading_result = None

# Initialize the grading system once
if 'grading_system' not in st.session_state:
    try:
        st.session_state.grading_system = GradingSystem()
    except Exception as e:
        st.error(f"Error initializing grading system: {e}")
        st.session_state.grading_system = None

def go_to_practice():
    """Transition to practice state."""
    try:
        # Select a random word
        if not st.session_state.words:
            st.error("No words available. Please check the data source.")
            return
            
        word = random.choice(st.session_state.words)
        
        # Generate a sentence
        llm = LLMGenerator()
        sentence = llm.generate_sentence(word)
        
        # Update session state
        st.session_state.current_sentence = sentence
        st.session_state.drawing_data = None
        st.session_state.grading_result = None
        st.session_state.state = "practice"
    except Exception as e:
        st.error(f"Error transitioning to practice: {e}")
        print(traceback.format_exc())

def go_to_review(image: Image.Image):
    """Transition to review state."""
    try:
        if st.session_state.grading_system is None:
            st.error("Grading system is not available.")
            return
            
        # Preprocess the image
        processed_image = GradingSystem.preprocess_image(image)
        
        # Grade the submission
        grading_result = st.session_state.grading_system.grade_submission(
            processed_image,
            st.session_state.current_sentence["jawi"]
        )
        
        # Update session state
        st.session_state.grading_result = grading_result
        st.session_state.state = "review"
    except Exception as e:
        st.error(f"Error during review: {e}")
        print(traceback.format_exc())

def convert_canvas_to_image(canvas_data):
    """Convert canvas data to PIL Image."""
    try:
        if canvas_data is not None and canvas_data.image_data is not None:
            # Convert the canvas data to a PIL Image
            img_data = canvas_data.image_data
            # Convert RGBA to RGB if necessary
            if img_data.shape[2] == 4:
                img_data = Image.fromarray(img_data).convert('RGB')
            else:
                img_data = Image.fromarray(img_data)
            return img_data
        return None
    except Exception as e:
        st.error(f"Error converting canvas to image: {e}")
        print(traceback.format_exc())
        return None

def main():
    """Main application."""
    try:
        # Display header
        st.title("Malay-Jawi Learning Application")
        
        # Fetch words if not already done
        if not st.session_state.words:
            try:
                st.session_state.words = fetch_words()
            except Exception as e:
                st.error(f"Error fetching words: {e}")
                print(traceback.format_exc())
                st.stop()
        
        # Handle different states
        if st.session_state.state == "setup":
            st.write("Welcome to the Malay-Jawi Learning Application!")
            st.write("Press the button below to generate a phrase to practice writing in Jawi.")
            
            if st.button("Generate Phrase"):
                go_to_practice()
        
        elif st.session_state.state == "practice":
            st.subheader("Practice Writing in Jawi")
            
            # Display the Jawi script to copy
            st.markdown("### Copy this Jawi script:")
            st.markdown(f"""
            <div dir="rtl" style="
                font-size: 48px;
                margin: 20px 0;
                padding: 20px;
                background-color: #f0f2f6;
                border-radius: 10px;
                text-align: center;">
                {st.session_state.current_sentence['jawi']}
            </div>
            """, unsafe_allow_html=True)
            
            # Show meaning
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Malay (Rumi):**")
                st.info(st.session_state.current_sentence['rumi'])
            with col2:
                st.markdown("**English:**")
                st.info(st.session_state.current_sentence['english'])
            
            # Drawing canvas
            st.markdown("### Write the Jawi script here:")
            
            try:
                # Create the canvas for drawing
                from streamlit_drawable_canvas import st_canvas
                
                # Create three columns for the canvas controls
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    stroke_width = st.slider("Stroke width", 1, 25, 3)
                with col2:
                    stroke_color = st.color_picker("Stroke color", "#000000")
                with col3:
                    bg_color = st.color_picker("Background color", "#FFFFFF")
                
                canvas_result = st_canvas(
                    fill_color="rgba(255, 255, 255, 0)",
                    stroke_width=stroke_width,
                    stroke_color=stroke_color,
                    background_color=bg_color,
                    height=200,
                    width=600,
                    drawing_mode="freedraw",
                    key="canvas",
                )
                
                # Add writing direction guidance
                st.markdown("""
                <div style="text-align: right; color: gray; font-style: italic;">
                ← Write from right to left
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    # Clear canvas button
                    if st.button("Clear Canvas"):
                        st.session_state.drawing_data = None
                        st.experimental_rerun()
                
                with col2:
                    # Submit button
                    if st.button("Submit"):
                        if canvas_result is not None and canvas_result.image_data is not None:
                            image = convert_canvas_to_image(canvas_result)
                            if image:
                                st.session_state.drawing_data = image
                                go_to_review(image)
                            else:
                                st.warning("Could not process the drawing. Please try again.")
                        else:
                            st.warning("Please write something before submitting.")
            except Exception as e:
                st.error(f"Error with canvas: {e}")
                print(traceback.format_exc())
        
        elif st.session_state.state == "review":
            try:
                st.subheader("Review")
                
                # Display the original Jawi script
                st.markdown("### Original Jawi script:")
                st.markdown(f"""
                <div dir="rtl" style="
                    font-size: 48px;
                    margin: 20px 0;
                    padding: 20px;
                    background-color: #f0f2f6;
                    border-radius: 10px;
                    text-align: center;">
                    {st.session_state.current_sentence['jawi']}
                </div>
                """, unsafe_allow_html=True)
                
                # Show meaning
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Malay (Rumi):**")
                    st.info(st.session_state.current_sentence['rumi'])
                with col2:
                    st.markdown("**English:**")
                    st.info(st.session_state.current_sentence['english'])
                
                # Display the student's writing
                st.markdown("### Your writing:")
                if st.session_state.drawing_data:
                    st.image(st.session_state.drawing_data, caption="Your Jawi writing", use_column_width=True)
                
                # Display grading results
                if st.session_state.grading_result:
                    st.markdown("### Feedback:")
                    
                    # Show grade
                    grade = st.session_state.grading_result["grade"]
                    if grade == "A":
                        grade_color = "green"
                    elif grade == "B":
                        grade_color = "orange"
                    else:
                        grade_color = "red"
                    
                    st.markdown(f"<h2 style='color: {grade_color};'>Grade: {grade}</h2>", unsafe_allow_html=True)
                    
                    # Show feedback
                    st.markdown("#### Feedback:")
                    st.write(st.session_state.grading_result["feedback"])
                    
                    # Show detected text if any
                    if st.session_state.grading_result["detected_text"]:
                        st.markdown("#### Detected Text:")
                        st.markdown(f"""
                        <div dir="rtl" style="
                            font-size: 24px;
                            margin: 10px 0;
                            padding: 10px;
                            background-color: #f9f9f9;
                            border-radius: 5px;">
                            {st.session_state.grading_result["detected_text"]}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Practice again button
                if st.button("Practice Again"):
                    go_to_practice()
                
                # Return to home button
                if st.button("Return to Home"):
                    st.session_state.state = "setup"
                    st.experimental_rerun()
            except Exception as e:
                st.error(f"Error in review screen: {e}")
                print(traceback.format_exc())
                if st.button("Return to Home"):
                    st.session_state.state = "setup"
                    st.experimental_rerun()
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
