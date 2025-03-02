from typing import Optional
from PIL import Image
import numpy as np
import streamlit as st
from streamlit_drawable_canvas import st_canvas

class CanvasManager:
    @staticmethod
    def create_canvas(key: str = "canvas") -> tuple[Optional[Image.Image], bool]:
        """Create and manage the drawing canvas."""
        # Create columns for canvas controls
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            stroke_width = st.slider("Stroke width", 1, 25, 3)
        with col2:
            stroke_color = st.color_picker("Stroke color", "#000000")
        with col3:
            bg_color = st.color_picker("Background color", "#FFFFFF")
        
        # Create the canvas
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            height=200,
            width=600,
            drawing_mode="freedraw",
            key=key,
        )
        
        # Add writing direction guidance
        st.markdown("""
        <div style="text-align: right; color: gray; font-style: italic;">
        ← Write from right to left
        </div>
        """, unsafe_allow_html=True)
        
        # Convert canvas data to image if available
        image = None
        has_drawing = False
        
        if canvas_result.image_data is not None:
            has_drawing = True
            img_data = canvas_result.image_data
            if img_data.shape[2] == 4:
                image = Image.fromarray(img_data).convert('RGB')
            else:
                image = Image.fromarray(img_data)
        
        return image, has_drawing
