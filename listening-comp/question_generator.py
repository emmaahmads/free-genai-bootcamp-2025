import json
from typing import Dict, List, Optional
from vector_store import QuestionVectorStore
import requests
from transformers import AutoTokenizer

class QuestionGenerator:
    def __init__(self):
        """Initialize Hugging Face client and vector store"""
        self.vector_store = QuestionVectorStore()
        self.model_id = "mistralai/Mistral-7B-Instruct-v0.2"  # Example model
        self.api_url = "https://api-inference.huggingface.co/models/" + self.model_id
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.headers = {"Authorization": f"Bearer {self._get_hf_api_key()}"}

    def _get_hf_api_key(self):
        """Get Hugging Face API key from environment variables"""
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            print("Warning: HUGGINGFACE_API_KEY not found in environment variables")
            return ""
        return api_key

    def _invoke_huggingface(self, prompt: str) -> Optional[str]:
        """Invoke Hugging Face with the given prompt"""
        try:
            # Format prompt for the model
            messages = [
                {"role": "user", "content": prompt}
            ]
            
            # Prepare payload
            payload = {
                "inputs": self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True),
                "parameters": {
                    "temperature": 0.7,
                    "max_new_tokens": 1024,
                    "top_p": 0.95,
                }
            }
            
            # Make API request
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            # Extract generated text
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0]["generated_text"].split("<assistant>")[-1].strip()
            return None
        except Exception as e:
            print(f"Error invoking Hugging Face: {str(e)}")
            return None

    def generate_similar_question(self, section_num: int, topic: str) -> Dict:
        """Generate a new question similar to existing ones on a given topic"""
        # Get similar questions for context
        similar_questions = self.vector_store.search_similar_questions(section_num, topic, n_results=3)
        
        if not similar_questions:
            return None
        
        # Create context from similar questions
        context = "Here are some example Malay listening questions:\n\n"
        for idx, q in enumerate(similar_questions, 1):
            if section_num == 2:
                context += f"Example {idx}:\n"
                context += f"Introduction: {q.get('Introduction', '')}\n"
                context += f"Conversation: {q.get('Conversation', '')}\n"
                context += f"Question: {q.get('Question', '')}\n"
                if 'Options' in q:
                    context += "Options:\n"
                    for i, opt in enumerate(q['Options'], 1):
                        context += f"{i}. {opt}\n"
            else:  # section 3
                context += f"Example {idx}:\n"
                context += f"Situation: {q.get('Situation', '')}\n"
                context += f"Question: {q.get('Question', '')}\n"
                if 'Options' in q:
                    context += "Options:\n"
                    for i, opt in enumerate(q['Options'], 1):
                        context += f"{i}. {opt}\n"
            context += "\n"

        # Create prompt for generating new question
        prompt = f"""Based on the following example Malay listening questions, create a new question about {topic}.
        The question should follow the same format but be different from the examples.
        Make sure the question tests listening comprehension and has a clear correct answer.
        
        {context}
        
        Generate a new question following the exact same format as above. Include all components (Introduction/Situation, 
        Conversation/Question, and Options). Make sure the question is challenging but fair, and the options are plausible 
        but with only one clearly correct answer. Return ONLY the question without any additional text.
        
        Use Malay language for all text. If you don't have examples in Malay, create a new question in Malay about {topic}.
        
        New Question:
        """

        # Generate new question
        response = self._invoke_huggingface(prompt)
        if not response:
            return None

        # Parse the generated question
        try:
            lines = response.strip().split('\n')
            question = {}
            current_key = None
            current_value = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if line.startswith("Introduction:"):
                    if current_key:
                        question[current_key] = ' '.join(current_value)
                    current_key = 'Introduction'
                    current_value = [line.replace("Introduction:", "").strip()]
                elif line.startswith("Conversation:"):
                    if current_key:
                        question[current_key] = ' '.join(current_value)
                    current_key = 'Conversation'
                    current_value = [line.replace("Conversation:", "").strip()]
                elif line.startswith("Situation:"):
                    if current_key:
                        question[current_key] = ' '.join(current_value)
                    current_key = 'Situation'
                    current_value = [line.replace("Situation:", "").strip()]
                elif line.startswith("Question:"):
                    if current_key:
                        question[current_key] = ' '.join(current_value)
                    current_key = 'Question'
                    current_value = [line.replace("Question:", "").strip()]
                elif line.startswith("Options:"):
                    if current_key:
                        question[current_key] = ' '.join(current_value)
                    current_key = 'Options'
                    current_value = []
                elif line[0].isdigit() and line[1] == "." and current_key == 'Options':
                    current_value.append(line[2:].strip())
                elif current_key:
                    current_value.append(line)
            
            if current_key:
                if current_key == 'Options':
                    question[current_key] = current_value
                else:
                    question[current_key] = ' '.join(current_value)
            
            # Ensure we have exactly 4 options
            if 'Options' not in question or len(question.get('Options', [])) != 4:
                # Use default options if we don't have exactly 4
                question['Options'] = [
                    "Makan nasi lemak",
                    "Makan roti canai",
                    "Makan char kway teow",
                    "Makan laksa"
                ]
            
            return question
        except Exception as e:
            print(f"Error parsing generated question: {str(e)}")
            return None

    def get_feedback(self, question: Dict, selected_answer: int) -> Dict:
        """Generate feedback for the selected answer"""
        if not question or 'Options' not in question:
            return None

        # Create prompt for generating feedback
        prompt = f"""Given this Malay listening question and the selected answer, provide feedback explaining if it's correct 
        and why. Keep the explanation clear and concise.
        
        """
        if 'Introduction' in question:
            prompt += f"Introduction: {question['Introduction']}\n"
            prompt += f"Conversation: {question['Conversation']}\n"
        else:
            prompt += f"Situation: {question['Situation']}\n"
        
        prompt += f"Question: {question['Question']}\n"
        prompt += "Options:\n"
        for i, opt in enumerate(question['Options'], 1):
            prompt += f"{i}. {opt}\n"
        
        prompt += f"\nSelected Answer: {selected_answer}\n"
        prompt += "\nProvide feedback in JSON format with these fields:\n"
        prompt += "- correct: true/false\n"
        prompt += "- explanation: brief explanation of why the answer is correct/incorrect\n"
        prompt += "- correct_answer: the number of the correct option (1-4)\n"

        # Get feedback
        response = self._invoke_huggingface(prompt)
        if not response:
            return None

        try:
            # Parse the JSON response
            feedback = json.loads(response.strip())
            return feedback
        except:
            # If JSON parsing fails, return a basic response with a default correct answer
            return {
                "correct": False,
                "explanation": "Unable to generate detailed feedback. Please try again.",
                "correct_answer": 1  # Default to first option
            }
