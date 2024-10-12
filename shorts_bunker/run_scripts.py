import subprocess

def run_script(script_name):
    """Run a Python script using subprocess."""
    subprocess.run(['python', script_name])

def runner_01():
    """Run the voice generator and image fetching scripts."""
    run_script('voice_generator.py')
    run_script('get_images_from_pixabay.py')

def runner_02():
    """Run the image creation and video creation scripts."""
    run_script('image_creator.py')
    run_script('video_creator.py')

# Call the runner functions
if __name__ == "__main__":
    runner_01()  # Run the first set of scripts
    # runner_02()  # Run the second set of scripts
