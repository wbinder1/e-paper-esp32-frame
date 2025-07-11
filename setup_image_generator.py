#!/usr/bin/env python3
"""
Setup Image Generator for E-Paper Frame
Creates a BMP image with setup instructions for WiFi configuration
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_setup_image():
    """Create a setup instruction image for the e-paper display"""
    
    # E-paper display dimensions
    width = 800
    height = 480
    
    # Create a white background
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to use a system font, fallback to default if not available
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 32)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    title = "WiFi Setup Required"
    title_bbox = draw.textbbox((0, 0), title, font=font_large)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 50), title, fill=(0, 0, 0), font=font_large)
    
    # Instructions
    instructions = [
        "1. Connect to WiFi network:",
        "   'E-Paper Frame Setup'",
        "",
        "2. Password: 12345678",
        "",
        "3. Open web browser and go to:",
        "   http://frame.local",
        "",
        "4. Select your WiFi network",
        "   and enter password",
        "",
        "5. Device will restart and",
        "   connect automatically"
    ]
    
    y_position = 120
    line_height = 35
    
    for instruction in instructions:
        if instruction.startswith("   "):
            # Indented line
            draw.text((100, y_position), instruction, fill=(0, 0, 0), font=font_medium)
        elif instruction == "":
            # Empty line
            pass
        else:
            # Regular line
            draw.text((50, y_position), instruction, fill=(0, 0, 0), font=font_medium)
        
        y_position += line_height
    
    # Add a border
    border_width = 3
    draw.rectangle([border_width, border_width, width-border_width, height-border_width], 
                   outline=(0, 0, 0), width=border_width)
    
    # Save the image
    output_path = "setup_instructions.bmp"
    image.save(output_path, "BMP")
    print(f"Setup instruction image saved as: {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_setup_image() 