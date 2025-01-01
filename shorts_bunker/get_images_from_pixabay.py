import requests
import os
from PIL import Image
from io import BytesIO

# Your Pixabay API key
API_KEY = '34125495-f9af36a5836109aa4aa9db750'  # Replace with your actual API key

# Function to load data from video_data.txt
def load_video_data(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
    return lines

# Function to download images from Pixabay and process them
def download_images(search_terms):
    base_url = "https://pixabay.com/api/"

    for term in search_terms:
        try:
            # Set up parameters for the API request
            params = {
                'key': API_KEY,
                'q': term,
                'image_type': 'allphotos',
                'per_page': 6 # Number of images to download per search term
            }

            # Make a GET request to the Pixabay API
            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()
                hits = data.get('hits', [])

                if not hits:
                    print(f"No images found for '{term}', skipping.")
                    continue  # Skip to the next term if no images are found

                # Create a directory for the images if it doesn't exist
                os.makedirs('images', exist_ok=True)

                for i, hit in enumerate(hits):
                    try:
                        image_url = hit['largeImageURL']
                        img_data = requests.get(image_url).content

                        # Open the image using Pillow
                        img = Image.open(BytesIO(img_data))

                        # Check the size of the image and resize/flip as needed
                        if img.size == (800, 1200):
                            # Flip the image to 1200x800
                            img = img.transpose(method=Image.Transpose.ROTATE_270)
                        elif img.size != (1200, 800):
                            # Resize to 1200x800, maintaining the aspect ratio
                            img = img.resize((1200, 800), Image.LANCZOS)

                        # Save the processed image
                        img.save(f'images/{term}_{i + 1}.jpg')
                        print(f"Downloaded and processed: {term}_{i + 1}.jpg")
                    except Exception as e:
                        print(f"Error processing image for '{term}': {e}")
            else:
                print(f"Failed to retrieve images for '{term}': {response.status_code}")

        except Exception as e:
            print(f"Error retrieving data for '{term}': {e}")

# Load data from video_data.txt
search_terms = load_video_data('video_data.txt')

# Download images based on the search terms
download_images(search_terms)