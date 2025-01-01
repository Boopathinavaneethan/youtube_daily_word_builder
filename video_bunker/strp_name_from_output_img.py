import os

# Define the folder and file paths
output_folder = 'images'  # Modify this path if necessary
video_data_file = 'video_data.txt'

# Get the list of file names in the output folder
file_names = os.listdir(output_folder)

# Create a list to store the unique extracted data
extracted_data = []

# Extract the portion of each file name before the first underscore
for file_name in file_names:
    if '_' in file_name:
        name_part = file_name.split('_')[0]
        if name_part not in extracted_data:  # Check for duplicates
            extracted_data.append(name_part)

# Clear the contents of video_data.txt and write the unique data
with open(video_data_file, 'w') as f:
    for data in extracted_data:
        f.write(data + '\n')

print(f"Unique data has been written to {video_data_file}")
