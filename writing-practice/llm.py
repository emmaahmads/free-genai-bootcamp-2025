import os
from typing import TypedDict, Optional
from groq import Groq

class SentenceResponse(TypedDict):
    rumi: str
    jawi: str
    english: str

class LLMGenerator:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def generate_sentence(self, word: dict) -> SentenceResponse:
        """Generate a sentence using Groq LLM."""
        if not self.client:
            return self._generate_mock_sentence(word)
        
        try:
            prompt = self._create_prompt(word)
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract and parse the response
            response_text = response.choices[0].message.content
            import re
            import json
            
            # Find JSON in the response
            json_match = re.search(r'({.*})', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            return json.loads(response_text)
            
        except Exception as e:
            print(f"Error generating sentence with Groq: {e}")
            return self._generate_mock_sentence(word)

    def _create_prompt(self, word: dict) -> str:
        """Create the prompt for sentence generation."""
        return f"""
        Generate a simple Malay sentence using the following word: {word['rumi']}.
        The sentence should be in both Rumi and Jawi script.
        Follow basic Malay grammar and use vocabulary from these categories:
        - Common objects (e.g., buku, kereta, nasi, kucing)
        - Simple verbs (e.g., makan, minum, tidur, baca)
        - Time expressions (e.g., hari ini, esok, semalam)
        
        Return the result in JSON format with the following structure:
        {{
            "rumi": "The sentence in Malay using Latin script",
            "jawi": "The sentence in Jawi script",
            "english": "English translation of the sentence"
        }}
        """

    def _generate_mock_sentence(self, word: dict) -> SentenceResponse:
        """Generate a mock sentence when LLM is unavailable."""
        templates = {
            "buku": {
                "rumi": "Saya membaca buku setiap hari.",
                "jawi": "ساي ممباچ بوكو ستياڤ هاري.",
                "english": "I read a book every day."
            },
            "kereta": {
                "rumi": "Kereta saya berwarna biru.",
                "jawi": "كريتا ساي برورنا بيرو.",
                "english": "My car is blue."
            }
        }
        
        return templates.get(word['rumi'], {
            "rumi": f"Saya suka {word['rumi']}.",
            "jawi": f"ساي سوک {word['jawi']}.",
            "english": f"I like {word['english']}."
        })
