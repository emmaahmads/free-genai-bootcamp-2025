from typing import TypedDict, Optional
from PIL import Image
import random
import time

class GradingResult(TypedDict):
    transcribed_jawi: str
    transcribed_rumi: str
    english_translation: str
    grade: str
    feedback: str

class GradingSystem:
    @staticmethod
    def grade_submission(image: Image.Image, expected_jawi: str) -> GradingResult:
        """Grade the submitted Jawi writing."""
        # Simulate OCR process
        time.sleep(1)
        
        # Mock OCR result - in a real app, this would use actual OCR
        ocr_accuracy = random.choice(["correct", "partial", "incorrect"])
        
        if ocr_accuracy == "correct":
            return {
                "transcribed_jawi": expected_jawi,
                "transcribed_rumi": "Saya membaca buku setiap hari.",
                "english_translation": "I read a book every day.",
                "grade": "A",
                "feedback": "Excellent! Your Jawi writing is accurate and clear."
            }
        elif ocr_accuracy == "partial":
            return {
                "transcribed_jawi": expected_jawi[:-1] + ".",
                "transcribed_rumi": "Saya membaca buku setiap hari",
                "english_translation": "I read a book every day",
                "grade": "B",
                "feedback": "Good effort! Your writing is mostly correct, but pay attention to the final characters."
            }
        else:
            return {
                "transcribed_jawi": "ساي تيدق تاهو جاوي.",
                "transcribed_rumi": "Saya tidak tahu Jawi.",
                "english_translation": "I don't know Jawi.",
                "grade": "C",
                "feedback": "Keep practicing! Your writing needs improvement in letter formation and connections."
            }
