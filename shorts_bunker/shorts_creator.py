import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from gtts import gTTS  # For voice generation
from pydub import AudioSegment  # For analyzing audio duration

# Paths
images_folder = 'output_images'
video_data_file = 'video_data.txt'
output_video_path = 'final_video.mp4'
voices_folder = 'voices'
common_question_audio_path = os.path.join(voices_folder, "common_question.mp3")
subscribe_audio_path = os.path.join(voices_folder, "subscribe.mp3")

# Function to get the duration of the audio file in seconds
def get_audio_duration(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return len(audio) / 1000  # duration in seconds

# Function to create the common question audio only once
def create_common_question_audio():
    if not os.path.exists(common_question_audio_path):
        question_text = "Whhatt is this called?"
        question_tts = gTTS(text=question_text, lang='en')
        question_tts.save(common_question_audio_path)
        print(f"Common question audio created: {common_question_audio_path}")

# Function to create the 'comment and subscribe' audio
def create_subscribe_audio():
    if not os.path.exists(subscribe_audio_path):
        subscribe_text = "Comment the name of this and subscribe to our channel."
        subscribe_tts = gTTS(text=subscribe_text, lang='en')
        subscribe_tts.save(subscribe_audio_path)
        print(f"Subscribe audio created: {subscribe_audio_path}")

# Function to create voice clips (only answer voice varies)
def voice_creator():
    # Ensure the voices folder exists
    if not os.path.exists(voices_folder):
        os.makedirs(voices_folder)

    # Create the common question audio (if it doesn't exist)
    create_common_question_audio()

    # Create the 'comment and subscribe' audio (if it doesn't exist)
    create_subscribe_audio()

    # Read the data from video_data.txt
    with open(video_data_file, 'r') as file:
        image_order = [line.strip() for line in file.readlines()]

    # Loop through each item in the list and create the answer voice clips
    for i, img_name in enumerate(image_order):
        if i == len(image_order) - 1:
            # Skip for the last entry (handled separately in video_creator)
            continue
        else:
            # Create the answer prompt
            answer = img_name.split('_')[0]  # Assuming answer is derived from the image filename

            # Save only the answer voice (without "The answer is")
            answer_tts = gTTS(text=answer, lang='en')
            answer_tts.save(os.path.join(voices_folder, f"{img_name}_answer.mp3"))

# Function to create the video
def video_creator():
    # Read the order of images from the video_data.txt file
    with open(video_data_file, 'r') as file:
        image_order = [line.strip() for line in file.readlines()]

    # Create a list to hold the video clips
    clips = []

    # Get the common question audio duration
    question_duration = get_audio_duration(common_question_audio_path)
    # Get the subscribe audio duration
    subscribe_duration = get_audio_duration(subscribe_audio_path)

    # Loop through each image in the specified order
    for i, img_name in enumerate(image_order):
        question_img_path = os.path.join(images_folder, f"{img_name}_question.jpg")
        answer_img_path = os.path.join(images_folder, f"{img_name}_answer.jpg")

        # For the last entry, use the "subscribe" audio
        if i == len(image_order) - 1:
            if os.path.exists(question_img_path):
                # For the last question, use the subscribe audio
                question_clip = ImageClip(question_img_path).set_duration(subscribe_duration)
                question_clip = question_clip.set_audio(AudioFileClip(subscribe_audio_path))
                clips.append(question_clip)
            continue

        # Check if the question image exists and create a clip for it
        if os.path.exists(question_img_path):
            # Use the common question audio for each question
            question_clip = ImageClip(question_img_path).set_duration(question_duration)
            question_clip = question_clip.set_audio(AudioFileClip(common_question_audio_path))
            clips.append(question_clip)

            # Add an additional 1-second pause using the same question image (for audience thinking time)
            pause_clip = ImageClip(question_img_path).set_duration(1)
            clips.append(pause_clip)

        # Check if the answer image exists and create a clip for it
        if os.path.exists(answer_img_path):
            # Get the audio duration for the answer
            answer_audio_path = os.path.join(voices_folder, f"{img_name}_answer.mp3")
            answer_duration = get_audio_duration(answer_audio_path)

            answer_clip = ImageClip(answer_img_path).set_duration(answer_duration)
            answer_clip = answer_clip.set_audio(AudioFileClip(answer_audio_path))
            clips.append(answer_clip)

    # Concatenate all the clips into a single video
    final_clip = concatenate_videoclips(clips, method="compose")

    # Write the video file
    final_clip.write_videofile(output_video_path, fps=24)

    print(f"Video created successfully: {output_video_path}")

# Main function to handle voice and video creation
def shorts_creator():
    # Step 1: Create the voices
    voice_creator()

    # Step 2: Call the video creator function
    video_creator()

# Run the shorts creation process
if __name__ == "__main__":
    shorts_creator()
