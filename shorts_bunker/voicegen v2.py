import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_video_data(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    set1 = lines[:3]
    set2 = lines[3:]
    return set1, set2

def format_text(data_set):
    formatted_text = ""
    for item in data_set:
        formatted_text += f'What is this called?<break time="1.5s"/>\n{item}<break time="2s"/>\n'
    return formatted_text

def generate_and_download_speech(formatted_text):
    # Path to your Chrome user profile
    profile_path = "C:\\Users\\boopa\\AppData\\Local\\Google\\Chrome\\User Data\\Default"  # Update this

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_path}")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://voicemaker.in/")
        time.sleep(5)

        # Change text area using XPath
        text_area = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "main-textarea"))
        )
        text_area.clear()
        text_area.send_keys(formatted_text)

        # Click to change voice using XPath (this opens the popup)
        change_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="voiceType"]'))
        )
        change_button.click()
        time.sleep(2)  # Wait for the popup to appear

        # Click the Convert to Speech button using XPath
        convert_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="convert-button"]'))
        )
        convert_button.click()

        # Wait for the conversion to complete and the download button to appear
        time.sleep(15)

        # Find the download button using XPath
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "standard-download-btn")]'))
        )
        download_button.click()

        # Wait for the download to complete
        time.sleep(5)
        print("Voice generation completed and downloaded.")

    finally:
        pass
        #driver.quit()

set1, set2 = load_video_data('video_data.txt')
formatted_text_set1 = format_text(set1)
formatted_text_set2 = format_text(set2)

print("Processing Set 1...")
generate_and_download_speech(formatted_text_set1)

print("Processing Set 2...")
generate_and_download_speech(formatted_text_set2)
