from gtts import gTTS
from moviepy.editor import *
import os

# File paths for the conversation, images, and output
convo_file = 'convo_data.txt'
john_img_path = 'john_image.jpg'  # Path to John's image
emma_img_path = 'emma_image.jpg'  # Path to Emma's image
audio_output = 'convo_audio.mp3'
video_output = 'convo_video.mp4'

# Step 1: Read and parse the conversation from the text file
with open(convo_file, 'r') as file:
    lines = file.readlines()

# Dictionary to associate speakers with images
speakers_images = {
    "John": john_img_path,
    "Emma": emma_img_path
}

# Step 2: Generate individual speech audio clips for each line
audio_clips = []
image_clips = []
total_duration = 0

for line in lines:
    if ':' in line:
        speaker, dialogue = line.split(':', 1)
        speaker = speaker.strip()  # Get the speaker name
        dialogue = dialogue.strip()  # Get the actual dialogue

        # Step 3: Create the speech for the dialogue
        tts = gTTS(text=dialogue, lang='en')
        dialogue_audio = f"{speaker}_audio_{len(audio_clips)}.mp3"
        tts.save(dialogue_audio)

        # Load the audio clip to get its duration
        audio = AudioFileClip(dialogue_audio)
        audio_clips.append(audio)

        # Step 4: Use the corresponding image and set its duration based on the audio length
        img_path = speakers_images.get(speaker, john_img_path)  # Default to John's image if speaker not found
        img_clip = ImageClip(img_path).set_duration(audio.duration)
        image_clips.append(img_clip)

        total_duration += audio.duration  # Keep track of the total video duration

# Step 5: Concatenate the image clips
video_clip = concatenate_videoclips(image_clips, method="compose")

# Step 6: Concatenate the audio clips
final_audio = concatenate_audioclips(audio_clips)

# Step 7: Add the final audio to the video clip
final_video = video_clip.set_audio(final_audio)

# Step 8: Write the video to file
final_video.write_videofile(video_output, fps=24)

print("Video created successfully!")
