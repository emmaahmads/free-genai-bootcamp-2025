from typing import TypedDict, Optional
from PIL import Image, ImageEnhance
import pytesseract
import cv2
import numpy as np
from difflib import SequenceMatcher
import traceback

class GradingResult(TypedDict):
    grade: str
    feedback: str
    detected_text: str

class GradingSystem:
    def __init__(self):
        # Configure Tesseract to use Arabic
        self.tesseract_config = r'--oem 3 --psm 6 -l ara'
        print("Initialized GradingSystem with Tesseract config:", self.tesseract_config)
        
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity ratio."""
        similarity = SequenceMatcher(None, str1, str2).ratio()
        print(f"Calculated similarity between '{str1}' and '{str2}': {similarity}")
        return similarity

    def grade_submission(self, image: Image.Image, expected_jawi: str) -> GradingResult:
        """Grade the submitted Jawi writing using Tesseract OCR."""
        print("Grading submission...")
        try:
            # Convert PIL Image to OpenCV format
            img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            print("Converted image to OpenCV format.")
            
            # Preprocess the image
            img_processed = self.preprocess_image_for_ocr(img_cv)
            print("Preprocessed image for OCR.")
            
            # Perform OCR using Arabic library since Jawi is based on Arabic except that Jawi has extra characters 'ڠ''ݣ''چ
            detected_text = pytesseract.image_to_string(
                img_processed, 
                lang='ara',
                config=self.tesseract_config
            ).strip()
            pytesseract.image_to_string(
                img_processed, 
                lang='ara',
                config=self.tesseract_config
            )
            print("Detected text from OCR:", detected_text)
            
            # Calculate similarity between detected and expected text
            similarity = self.calculate_similarity(detected_text, expected_jawi)
            
            # Grade based on similarity
            if similarity >= 0.9:
                grade = "A"
                feedback = (
                    "Excellent! Your Jawi writing is accurate and clear.\n"
                    "- Letter forms are well-executed\n"
                    "- Connections are correct\n"
                    "- Spacing is appropriate"
                )
            elif similarity >= 0.7:
                grade = "B"
                feedback = (
                    "Good effort! Your writing is mostly correct. Pay attention to:\n"
                    "- Letter connections\n"
                    "- Letter proportions\n"
                    "- Spacing between letters"
                )
            else:
                grade = "C"
                feedback = (
                    "Keep practicing! Focus on:\n"
                    "- Basic letter shapes\n"
                    "- Writing direction\n"
                    "- Letter spacing\n"
                    "Try copying the letters one by one."
                )
            print(f"Grading result: {grade}, Feedback: {feedback}")
            
            return {
                "grade": grade,
                "feedback": feedback,
                "detected_text": detected_text
            }
            
        except Exception as e:
            error_message = f"Error in OCR processing: {e}"
            print(error_message)
            return {
                "grade": "C",
                "feedback": "Unable to process the writing clearly. Please ensure:\n"
                          "- Writing is clear and dark enough\n"
                          "- Background has good contrast\n"
                          "- Letters are properly formed",
                "detected_text": ""
            }

    @staticmethod
    def preprocess_image_for_ocr(image: np.ndarray) -> np.ndarray:
        """Preprocess the image for better OCR results."""
        print("Preprocessing image for OCR...")
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Converted image to grayscale.")
        
        # Apply thresholding to get black and white image
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        print("Applied thresholding to obtain binary image.")
        
        # Remove noise
        kernel = np.ones((2,2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        print("Applied morphological operations to remove noise.")
        
        # Dilate to connect components
        binary = cv2.dilate(binary, kernel, iterations=1)
        print("Dilated image to connect components.")
        
        # Invert back
        binary = cv2.bitwise_not(binary)
        print("Inverted binary image.")
        
        return binary

    @staticmethod
    def preprocess_image(image: Image.Image) -> Image.Image:
        """Preprocess the image before OCR processing."""
        print("Preprocessing image before OCR...")
        # Convert to grayscale
        img_gray = image.convert('L')
        print("Converted image to grayscale.")
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(img_gray)
        img_contrast = enhancer.enhance(2.0)
        print("Enhanced image contrast.")
        
        # Resize if too small
        if img_contrast.width < 400:
            ratio = 400 / img_contrast.width
            new_size = (400, int(img_contrast.height * ratio))
            img_contrast = img_contrast.resize(new_size, Image.Resampling.LANCZOS)
            print("Resized image to:", new_size)
        
        return img_contrast

