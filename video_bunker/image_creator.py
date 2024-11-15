from PIL import Image, ImageDraw, ImageFont
import os

# Define the folder containing your images and output
images_folder = 'images'
output_folder = 'output_images'
os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

# Define the aspect ratio for normal YouTube videos (16:9) resolution, e.g., 1920x1080
blank_image_size = (1920, 1080)

# Coordinates for left and right side positioning
def get_left_center_coordinates(blank_size, text_size, padding=50):
    blank_width, blank_height = blank_size
    text_width, text_height = text_size
    x = padding  # Start from the left with some padding
    y = (blank_height - text_height) // 2 - 150  # Center vertically and move up by 50px
    return (x, y)

def get_right_center_coordinates(blank_size, image_size, margin=50):
    blank_width, blank_height = blank_size
    img_width, img_height = image_size
    x = blank_width * 3 // 4 - img_width // 2  # Right side, center horizontally on right half
    y = (blank_height - img_height) // 2 + margin - 150  # Center vertically with margin and move up by 50px
    return (x, y)

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

# Load and resize the logo
logo_path = 'logo/daily word builder.png'  # Specify the path to your logo
logo = Image.open(logo_path)

# Ensure the logo has an alpha channel (transparency)
logo = logo.convert("RGBA")

# Resize the logo to keep it small
logo_size = (150, 150)  # Adjust this size as needed
logo = logo.resize(logo_size)

# Loop through each image in the folder
for filename in os.listdir(images_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        img_name = filename.split('_')[0]  # Get the part before the underscore
        img_path = os.path.join(images_folder, filename)
        img = Image.open(img_path)

        # Example RGB color (you can input any RGB values directly)
        rgb_color = (135, 255, 254)

        # Resize the image to fit properly on the right side without exceeding half the screen width
        img.thumbnail((blank_image_size[0] // 2 - 100, blank_image_size[1] - 100))

        # Create the blank image with the specified RGB color
        blank_image_question = Image.new('RGB', blank_image_size, rgb_color)

        # Get the position for the image (right side center with margin)
        position_right = get_right_center_coordinates(blank_image_size, img.size, margin=100)

        # Paste the image onto the blank canvas (right side)
        blank_image_question.paste(img, position_right)

        # Add the question text at the left side of the blank image
        draw_question = ImageDraw.Draw(blank_image_question)
        text_bbox = draw_question.textbbox((0, 0), question_text, font=font)
        position_left = get_left_center_coordinates(blank_image_size, (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]))

        # Add the question text
        draw_question.text(position_left, question_text, font=font, fill=text_color)

        # Add the logo at the bottom right corner of the question image
        logo_position = (blank_image_size[0] - logo_size[0] - 50, blank_image_size[1] - logo_size[1] - 50)  # 50px padding

        # Get the alpha channel of the logo to use as a mask
        alpha_mask = logo.split()[-1]  # The alpha channel (transparency)

        # Paste the logo with transparency support
        blank_image_question.paste(logo, logo_position, alpha_mask)

        # Save the question image
        question_image_path = os.path.join(output_folder, f"{img_name}_question.jpg")
        blank_image_question.save(question_image_path)
        print(f"Processed and saved question image: {question_image_path}")

        # Create a new blank image for the answer
        blank_image_answer = Image.new('RGB', blank_image_size, rgb_color)

        # Paste the image onto the blank canvas for the answer (right side)
        blank_image_answer.paste(img, position_right)

        # Add both the question and answer text to the answer image
        draw_answer = ImageDraw.Draw(blank_image_answer)

        # Add the question text (same position as before)
        draw_answer.text(position_left, question_text, font=font, fill=text_color)

        # Define the answer text (the part before the underscore)
        answer_text = img_name

        # Define the position for the answer text (left side, below the question)
        answer_bbox = draw_answer.textbbox((0, 0), answer_text, font=font)
        answer_position = (position_left[0], position_left[1] + text_bbox[3] + 50)  # 50px below the question

        # Add the answer text to the image
        draw_answer.text(answer_position, answer_text, font=font, fill=text_color)

        # Add the logo at the bottom right corner of the answer image
        blank_image_answer.paste(logo, logo_position, alpha_mask)

        # Save the answer image
        answer_image_path = os.path.join(output_folder, f"{img_name}_answer.jpg")
        blank_image_answer.save(answer_image_path)
        print(f"Processed and saved answer image: {answer_image_path}")

print("All images processed.")
