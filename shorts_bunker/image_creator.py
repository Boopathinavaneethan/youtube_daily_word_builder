from PIL import Image, ImageDraw, ImageFont
import os

# Define the folder containing your images
images_folder = 'images'
output_folder = 'output_images'
os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

# Define the aspect ratio (9:16) resolution, e.g., 1080x1920
blank_image_size = (1080, 1920)

# Coordinates to paste the image (centered but moved up)
def get_center_coordinates(blank_size, image_size, offset_y=0):
    blank_width, blank_height = blank_size
    img_width, img_height = image_size
    x = (blank_width - img_width) // 2
    y = (blank_height - img_height) // 2 - offset_y  # Subtract offset_y to move it up
    return (x, y)

# Example offset: move image up by 160 pixels
offset_y = 160

# Define the question string
question_text = "What is this called?"

# Try to load DM Sans or fall back to Arial
try:
    font = ImageFont.truetype("DMSans.ttf", 84)  # Ensure the DM Sans font file is in the same directory or specify full path
except IOError:
    print("DM Sans font not found. Using Arial font as fallback.")
    font = ImageFont.truetype("arial.ttf", 84)  # Fallback to Arial

# Define text color (black)
text_color = (0, 0, 0)

# Loop through each image in the folder
for filename in os.listdir(images_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        img_name = filename.split('_')[0]  # Get the part before the underscore
        img_path = os.path.join(images_folder, filename)
        img = Image.open(img_path)

                # Example RGB color (you can input any RGB values directly)
        rgb_color = (135, 255, 254)  # This is the RGB value you want (e.g., a shade of orange)

        # Create the blank image with the specified RGB color
        blank_image_question = Image.new('RGB', blank_image_size, rgb_color)
        # # Create a blank image for the question
        # blank_image_question = Image.new('RGB', blank_image_size, '')

        # Get the position to paste (adjusted upwards by the offset)
        position = get_center_coordinates(blank_image_size, img.size, offset_y=offset_y)

        # Paste the image onto the blank canvas
        blank_image_question.paste(img, position)

        # Add the question text at the top of the blank image
        draw_question = ImageDraw.Draw(blank_image_question)

        # Define the text position for the question
        text_bbox = draw_question.textbbox((0, 0), question_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]  # Calculate height here
        text_position = ((blank_image_size[0] - text_width) // 2, 150)  # Position text at 150 pixels from the top

        # Add the question text to the image
        draw_question.text(text_position, question_text, font=font, fill=text_color)

        # Save the question image
        question_image_path = os.path.join(output_folder, f"{img_name}_question.jpg")
        blank_image_question.save(question_image_path)
        print(f"Processed and saved question image: {question_image_path}")

        # Create a new blank image for the answer
        blank_image_answer = Image.new('RGB', blank_image_size, rgb_color)

        # Get the position to paste the image for the answer
        answer_position = get_center_coordinates(blank_image_size, img.size, offset_y=offset_y)

        # Paste the image onto the blank canvas for the answer
        blank_image_answer.paste(img, answer_position)

        # Add both the question and answer text to the answer image
        draw_answer = ImageDraw.Draw(blank_image_answer)

        # Add the question text to the answer image at the same position
        draw_answer.text(text_position, question_text, font=font, fill=text_color)

        # Define the answer text (the part before the underscore)
        answer_text = img_name

        # Define the position for the answer text (below the image)
        answer_bbox = draw_answer.textbbox((0, 0), answer_text, font=font)
        answer_width = answer_bbox[2] - answer_bbox[0]
        answer_height = answer_bbox[3] - answer_bbox[1]  # Calculate the height of the answer text
        answer_position = ((blank_image_size[0] - answer_width) // 2, position[1] + img.size[1] + 20)  # Position below the image

        # Add the answer text to the answer image
        draw_answer.text(answer_position, answer_text, font=font, fill=text_color)

        # Save the answer image
        answer_image_path = os.path.join(output_folder, f"{img_name}_answer.jpg")
        blank_image_answer.save(answer_image_path)
        print(f"Processed and saved answer image: {answer_image_path}")

print("All images processed.")
