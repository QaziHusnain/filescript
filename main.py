import os
import shutil
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
def organize_files(source_folder, destination_folder):
    # Ensure the source and destination directories exist
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(destination_folder, exist_ok=True)

    # Create a log file
    log_file_path = os.path.join(destination_folder, 'organizer_log.txt')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"Organizing files on {datetime.now()}\n\n")

    # Dictionary to map file extensions to folder names
    file_types = {
        'images': ['.jpg', '.jpeg', '.png', '.gif'],
        'documents': ['.pdf', '.docx', '.txt'],
        'videos': ['.mp4', '.mov', '.avi']
        # Add more file types as needed
    }

    # Create folders if they don't exist
    for folder in file_types.keys():
        folder_path = os.path.join(destination_folder, folder)
        os.makedirs(folder_path, exist_ok=True)

    # Iterate through files in the source folder
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Determine the file type based on the extension
        file_type = None
        for folder, extensions in file_types.items():
            if any(filename.lower().endswith(ext) for ext in extensions):
                file_type = folder
                break

        if file_type:
            # Move the file to the corresponding folder
            destination_path = os.path.join(destination_folder, file_type, filename)
            # Handle duplicates by adding a timestamp to the filename
            if os.path.exists(destination_path):
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename, extension = os.path.splitext(filename)
                filename = f"{filename}_{timestamp}{extension}"
                destination_path = os.path.join(destination_folder, file_type, filename)

            shutil.move(file_path, destination_path)

            # Log the file organization
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"Moved: {filename} to {file_type} folder\n")

    print("File organization completed. Check the log file for details.")

# Example usage
source_directory = r'C:\Users\Qazi\Documents\SourceFolder'
destination_directory = r'C:\Users\Qazi\Documents\DestinationFolder'

organize_files(source_directory, destination_directory)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organize', methods=['POST'])
def organize():
    source_directory = request.form['source_directory']
    destination_directory = request.form['destination_directory']

    organize_files(source_directory, destination_directory)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)