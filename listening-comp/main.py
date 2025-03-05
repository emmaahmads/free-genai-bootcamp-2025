import streamlit as st
import sys
import os
import json
from datetime import datetime
from question_generator import QuestionGenerator
from audio_generator import AudioGenerator
from get_transcript import YouTubeTranscriptDownloader
import asyncio

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page config
st.set_page_config(
    page_title="Malay Listening Practice",
    page_icon="🎧",
    layout="wide"
)

def load_stored_questions():
    """Load previously stored questions from JSON file"""
    questions_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data/stored_questions.json"
    )
    if os.path.exists(questions_file):
        with open(questions_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_question(question, practice_type, topic, audio_file=None):
    """Save a generated question to JSON file"""
    questions_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data/stored_questions.json"
    )
    
    # Load existing questions
    stored_questions = load_stored_questions()
    
    # Create a unique ID for the question using timestamp
    question_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Add metadata
    question_data = {
        "question": question,
        "practice_type": practice_type,
        "topic": topic,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "audio_file": audio_file
    }
    
    # Add to stored questions
    stored_questions[question_id] = question_data
    
    # Save back to file
    os.makedirs(os.path.dirname(questions_file), exist_ok=True)
    with open(questions_file, 'w', encoding='utf-8') as f:
        json.dump(stored_questions, f, ensure_ascii=False, indent=2)
    
    return question_id

def render_interactive_stage():
    """Render the interactive learning stage
    
    This function renders the main user interface for the Malay Listening
    Practice application. It displays the current question, options, and
    audio controls. It also handles user input and submits answers to the
    feedback system.
    """
    # Initialize session state
    if 'question_generator' not in st.session_state:
        st.session_state.question_generator = QuestionGenerator()
    if 'audio_generator' not in st.session_state:
        st.session_state.audio_generator = AudioGenerator(output_directory="audio_files")
    if 'transcript_downloader' not in st.session_state:
        st.session_state.transcript_downloader = YouTubeTranscriptDownloader(languages=["ms", "en"])
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    if 'current_practice_type' not in st.session_state:
        st.session_state.current_practice_type = "Dialogue Practice"
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    if 'youtube_transcript' not in st.session_state:
        st.session_state.youtube_transcript = None
    
    # Load stored questions for sidebar
    stored_questions = load_stored_questions()
    
    # Create sidebar
    with st.sidebar:
        st.title("Malay Listening Practice")
        st.write("Practice your Malay listening skills with AI-generated questions and audio.")
        
        # Show saved questions in sidebar
        if stored_questions:
            st.header("Saved Questions")
            for qid, qdata in stored_questions.items():
                # Create a button for each question
                button_label = f"{qdata['practice_type']} - {qdata['topic']}\n{qdata['created_at']}"
                if st.button(button_label, key=qid):
                    st.session_state.current_question = qdata['question']
                    st.session_state.current_practice_type = qdata['practice_type']
                    st.session_state.current_topic = qdata['topic']
                    st.session_state.current_audio = qdata.get('audio_file')
                    st.session_state.feedback = None
                    st.rerun()
        else:
            st.info("No saved questions yet. Generate some questions to see them here!")
    
    st.title("Malay Listening Comprehension Practice")
    
    # Practice type selection
    practice_type = st.selectbox(
        "Select Practice Type",
        ["Dialogue Practice", "Phrase Matching", "YouTube Content"],
        index=["Dialogue Practice", "Phrase Matching", "YouTube Content"].index(st.session_state.current_practice_type) if st.session_state.current_practice_type else 0
    )
    
    # Update current practice type in session state
    st.session_state.current_practice_type = practice_type
    
    # Topic selection
    topics = {
        "Dialogue Practice": ["Daily Conversation", "Shopping", "Restaurant", "Travel", "School/Work"],
        "Phrase Matching": ["Announcements", "Instructions", "Weather Reports", "News Updates"],
        "YouTube Content": ["Use YouTube Transcript"]
    }
    
    topic = st.selectbox(
        "Select Topic",
        topics[practice_type]
    )
    
    # Save current topic to session state
    st.session_state.current_topic = topic
    
    # YouTube transcript section
    if practice_type == "YouTube Content":
        st.header("YouTube Transcript")
        
        # Create tabs for downloading new transcript or loading saved ones
        transcript_tab1, transcript_tab2 = st.tabs(["Download New Transcript", "Load Saved Transcript"])
        
        with transcript_tab1:
            youtube_url = st.text_input("Enter YouTube URL")
            if st.button("Get Transcript"):
                if youtube_url:
                    with st.spinner("Downloading transcript..."):
                        # Get transcript
                        transcript = st.session_state.transcript_downloader.get_transcript(youtube_url)
                        if transcript:
                            # Save transcript to file
                            video_id = st.session_state.transcript_downloader.extract_video_id(youtube_url)
                            if st.session_state.transcript_downloader.save_transcript(transcript, video_id):
                                st.session_state.youtube_transcript = transcript
                                st.success(f"Transcript downloaded and saved successfully as {video_id}.txt!")
                                st.rerun()
                            else:
                                st.error("Failed to save transcript to file.")
                        else:
                            st.error("Failed to download transcript. Make sure the video has Malay or English subtitles.")
        
        with transcript_tab2:
            # List saved transcripts
            saved_transcripts = st.session_state.transcript_downloader.list_saved_transcripts()
            if saved_transcripts:
                selected_transcript = st.selectbox(
                    "Select a saved transcript",
                    saved_transcripts,
                    format_func=lambda x: f"Video ID: {x}"
                )
                
                if st.button("Load Selected Transcript"):
                    with st.spinner("Loading transcript..."):
                        transcript = st.session_state.transcript_downloader.load_transcript(selected_transcript)
                        if transcript:
                            st.session_state.youtube_transcript = transcript
                            st.success(f"Transcript loaded successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to load transcript.")
            else:
                st.info("No saved transcripts found.")
    
    # YouTube transcript processing
    if practice_type == "YouTube Content" and st.session_state.youtube_transcript:
        st.subheader("YouTube Transcript Content")
        
        # Display transcript
        transcript_text = " ".join([entry['text'] for entry in st.session_state.youtube_transcript])
        st.text_area("Transcript", transcript_text, height=200)
        
        # Generate audio from transcript
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate Full Audio"):
                with st.spinner("Generating full audio with ElevenLabs..."):
                    audio_file = st.session_state.audio_generator.generate_audio_from_transcript(
                        st.session_state.youtube_transcript
                    )
                    if audio_file:
                        st.session_state.current_audio = audio_file
                        st.success("Full audio generated successfully!")
                        st.audio(audio_file)
                    else:
                        st.error("Failed to generate audio.")
        
        with col2:
            if st.button("Generate 30-Second Audio (Afifah Voice)"):
                with st.spinner("Generating 30-second audio with ElevenLabs..."):
                    # Limit transcript to approximately first 30 seconds
                    limited_transcript = []
                    total_chars = 0
                    char_limit = 450  # ~30 seconds of speech
                    
                    for entry in st.session_state.youtube_transcript:
                        limited_transcript.append(entry)
                        total_chars += len(entry['text'])
                        if total_chars >= char_limit:
                            break
                    
                    # Generate audio using Afifah's voice
                    audio_file = st.session_state.audio_generator.generate_audio_from_transcript_with_voice(
                        limited_transcript, "Xb7hH8MSUJpSbSDYk0k2"  # Afifah voice ID
                    )
                    
                    if audio_file:
                        st.session_state.current_audio = audio_file
                        st.success("30-second audio generated successfully!")
                        st.audio(audio_file)
                    else:
                        st.error("Failed to generate audio.")
    
    # Display saved questions
    if st.checkbox("Show Saved Questions"):
        if os.path.exists("data/saved_questions.json"):
            with open("data/saved_questions.json", "r", encoding="utf-8") as f:
                saved_questions = json.load(f)
                
            if saved_questions:
                for i, q in enumerate(saved_questions):
                    with st.expander(f"Question {i+1}: {q['question'][:50]}..."):
                        st.write(f"**Question:** {q['question']}")
                        st.write(f"**Answer:** {q['answer']}")
                        st.write(f"**Practice Type:** {q['practice_type']}")
                        st.write(f"**Topic:** {q['topic']}")
                        
                        if st.button(f"Load Question {i+1}"):
                            st.session_state.current_question = q
                            st.session_state.current_practice_type = q['practice_type']
                            st.rerun()
            else:
                st.info("No saved questions yet. Generate some questions to see them here!")
    
    # Generate new question button (for non-YouTube content)
    if practice_type != "YouTube Content" and st.button("Generate New Question"):
        section_num = 2 if practice_type == "Dialogue Practice" else 3
        new_question = st.session_state.question_generator.generate_similar_question(
            section_num, topic
        )
        st.session_state.current_question = new_question
        st.session_state.current_practice_type = practice_type
        st.session_state.current_topic = topic
        st.session_state.feedback = None
        
        # Save the generated question
        print(f"Saving question {new_question['question']} to file")
        save_question(new_question, practice_type, topic)
        st.session_state.current_audio = None
    
    if st.session_state.current_question:
        st.subheader("Practice Scenario")
        
        # Display question components
        if practice_type == "Dialogue Practice":
            st.write("**Introduction:**")
            st.write(st.session_state.current_question['Introduction'])
            st.write("**Conversation:**")
            st.write(st.session_state.current_question['Conversation'])
        else:
            st.write("**Situation:**")
            st.write(st.session_state.current_question['Situation'])
        
        st.write("**Question:**")
        st.write(st.session_state.current_question['Question'])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display options
            options = st.session_state.current_question['Options']
            
            # If we have feedback, show which answers were correct/incorrect
            if st.session_state.feedback:
                correct = st.session_state.feedback.get('correct', False)

        with col2:
            # Generate audio button
            if st.session_state.current_audio:
                st.audio(st.session_state.current_audio)
            
            if st.button("Generate Audio"):
                with st.spinner("Generating audio with ElevenLabs..."):
                    # Determine text to convert to audio based on practice type
                    if practice_type == "Dialogue Practice":
                        text = st.session_state.current_question['Conversation']
                    else:
                        text = st.session_state.current_question['Situation']
                    
                    # Generate audio
                    audio_file = st.session_state.audio_generator.generate_audio(text)
                    
                    if audio_file:
                        st.session_state.current_audio = audio_file
                        
                        # Update saved question with audio file
                        if st.session_state.current_question.get('id'):
                            save_question(
                                st.session_state.current_question,
                                practice_type,
                                topic,
                                audio_file
                            )
                        
                        st.success("Audio generated successfully!")
                        st.audio(audio_file)
                    else:
                        st.error("Failed to generate audio.")

def main():
    """Main application entry point"""
    st.title("Malay Listening Practice")
    st.markdown("""
    Welcome to the Malay Listening Practice app! This application helps you practice your Malay listening skills
    through interactive exercises and real-world content from YouTube.
    """)
    
    render_interactive_stage()

if __name__ == "__main__":
    main()
