from moviepy.editor import ImageClip, concatenate_videoclips
import os

# Define the folder containing your images and the output video name
images_folder = 'output_images'
video_data_file = 'video_data.txt'
output_video_path = 'final_video.mp4'

# Read the order of images from the video_data.txt file
with open(video_data_file, 'r') as file:
    image_order = [line.strip() for line in file.readlines()]

# Create a list to hold the video clips
clips = []

# Loop through each image in the specified order
for img_name in image_order:
    # Construct the full file path for the question and answer images
    question_img_path = os.path.join(images_folder, f"{img_name}_question.jpg")
    answer_img_path = os.path.join(images_folder, f"{img_name}_answer.jpg")

    # Check if the question image exists and create a clip for it
    if os.path.exists(question_img_path):
        question_clip = ImageClip(question_img_path).set_duration(2.37)  # 1.0 seconds
        clips.append(question_clip)

    # Check if the answer image exists and create a clip for it
    if os.path.exists(answer_img_path):
        answer_clip = ImageClip(answer_img_path).set_duration(2.77)  # 1.5 seconds
        clips.append(answer_clip)

# Concatenate all the clips into a single video
final_clip = concatenate_videoclips(clips, method="compose")

# Write the video file
final_clip.write_videofile(output_video_path, fps=24)

print(f"Video created successfully: {output_video_path}")
