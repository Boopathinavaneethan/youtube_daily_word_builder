import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Function to load data from video_data.txt
def load_video_data(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    # Split the data into set1, set2, and set3
    set1 = lines[:3]  # First 3 entries
    set2 = lines[3:6]  # Next 3 entries
    set3 = [lines[6], lines[7]]  # Entries for the 7th and 8th lines
    return set1, set2, set3

# Format the text as per the given format
def format_text(data_set, default_string=False):
    formatted_text = ""
    for i, item in enumerate(data_set):
        formatted_text += f'What is this called?<break time="1s"/>\n{item}<break time="1.5s"/>\n'
    if default_string:
        formatted_text += 'Comment the name of this and subscribe to our channel.<break time="1s"/>\n'
    return formatted_text

# Function to generate and download speech using Selenium
def generate_and_download_speech(formatted_text):
    # Initialize the webdriver
    driver = webdriver.Chrome()

    try:
        # Open Voicemaker website
        driver.get("https://voicemaker.in/")
        time.sleep(5)  # Wait for the page to load

        # Locate the text input area and enter formatted text
        text_area = driver.find_element("id", "main-textarea")
        text_area.clear()
        text_area.send_keys(formatted_text)

        # Click on the Convert to Speech button
        convert_button = driver.find_element("id", "convert-button")
        convert_button.click()

        # Wait for the conversion to complete and the download button to appear
        time.sleep(15)  # Adjust this based on network speed

        # Find the download button and click it
        download_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-block.btn-outline-secondary.standard-download-btn.mr-2.my-1")
        download_button.click()

        # Wait for the download to complete
        time.sleep(5)

        print("Voice generation completed and downloaded.")

    finally:
        # Close the browser
        driver.quit()

# Load data from video_data.txt
set1, set2, set3 = load_video_data('video_data.txt')

# Format the text for set1, set2, and set3 (with default string for set3)
formatted_text_set1 = format_text(set1)
formatted_text_set2 = format_text(set2)
formatted_text_set3 = format_text(set3, default_string=True)

# Generate and download speech for set1
print("Processing Set 1...")
generate_and_download_speech(formatted_text_set1)

# Generate and download speech for set2
print("Processing Set 2...")
generate_and_download_speech(formatted_text_set2)

# Generate and download speech for set3 (7th and 8th entries followed by comment)
print("Processing Set 3...")
generate_and_download_speech(formatted_text_set3)
