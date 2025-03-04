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
        """Generate a two-word sentence using Groq LLM."""
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
        """Create the prompt for two-word sentence generation."""
        return f"""
        Generate a simple TWO-WORD Malay phrase using the word: {word['rumi']}.
        The phrase should be a basic subject-verb or adjective-noun combination.

        Rules:
        1. MUST be exactly two words
        2. Use basic vocabulary suitable for beginners
        3. The phrase should make logical sense
        4. Can be a simple command, description, or statement

        Examples of valid two-word phrases:
        - "kucing tidur" (cat sleeping)
        - "makan nasi" (eat rice)
        - "buku baru" (new book)

        Return ONLY the result in this JSON format:
        {{
            "rumi": "The two-word phrase in Malay using Latin script",
            "jawi": "The two-word phrase in Jawi script",
            "english": "English translation"
        }}
        """

    def _generate_mock_sentence(self, word: dict) -> SentenceResponse:
        """Generate a mock two-word sentence when LLM is unavailable."""
        templates = {
            "buku": {
                "rumi": "buku baru",
                "jawi": "بوكو بارو",
                "english": "new book"
            },
            "kereta": {
                "rumi": "kereta biru",
                "jawi": "كريتا بيرو",
                "english": "blue car"
            },
            "nasi": {
                "rumi": "nasi panas",
                "jawi": "ناسي ڤانس",
                "english": "hot rice"
            },
            "kucing": {
                "rumi": "kucing tidur",
                "jawi": "كوچيڠ تيدور",
                "english": "sleeping cat"
            },
            "makan": {
                "rumi": "makan nasi",
                "jawi": "ماكن ناسي",
                "english": "eat rice"
            },
            "minum": {
                "rumi": "minum kopi",
                "jawi": "مينوم كوڤي",
                "english": "drink coffee"
            },
            "tidur": {
                "rumi": "tidur nyenyak",
                "jawi": "تيدور ڽڽق",
                "english": "sleep soundly"
            },
            "baca": {
                "rumi": "baca buku",
                "jawi": "باچ بوكو",
                "english": "read book"
            }
        }
        
        return templates.get(word['rumi'], {
            "rumi": f"{word['rumi']} baik",
            "jawi": f"{word['jawi']} باءيق",
            "english": f"good {word['english']}"
        })

