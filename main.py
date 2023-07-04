from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
from PIL import Image
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

# Global variable to store the output folder path
output_folder = "outputs"

@app.route("/")
def in_or_out():
    return render_template('home.html')

@app.route('/inside', methods=['GET', 'POST'])
def inside():
    if request.method == 'POST':
        # Get the uploaded files
        files = request.files.getlist('files')

        # Check if no files were selected
        if len(files) == 0:
            return render_template('inside.html', error="Please choose at least one file.")

        # Process each file
        for file in files:
            # Save the uploaded file to a temporary folder
            file_path = os.path.join('temp', file.filename)
            temp_path_pgm = file_path
            file.save(file_path)

            # Get the input folder path
            # input_folder = os.path.dirname(file_path)

            # Check if the file extension is .pgm
            if file.filename.lower().endswith('.pgm'):
                # Generate a new file name with the .jpg extension
                jpg_image_path = os.path.splitext(file_path)[0] + '.jpg'

                # Load the PGM image using PIL and convert it to RGB
                with Image.open(file_path) as pgm_image:
                    pgm_image = pgm_image.convert("RGB")

                    # Save the image as JPG format
                    pgm_image.save(jpg_image_path)

                # Update the file path to the JPG image
                file_path = jpg_image_path
                temp_path_jpg = file_path


            # Load the Bayer image
            bayer_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            # Calculate the height of the image
            height = bayer_image.shape[0]

            # Divide the image into two parts
            top_half = bayer_image[:height // 2, :]
            bottom_half = bayer_image[height // 2:, :]

            # Convert the top half using cv2.COLOR_BAYER_GR2BGR
            bgr_top_half = cv2.cvtColor(top_half, cv2.COLOR_BAYER_GR2BGR)

            # Convert the bottom half using cv2.COLOR_BAYER_GR2RGB
            rgb_bottom_half = cv2.cvtColor(bottom_half, cv2.COLOR_BAYER_GR2BGR)

            # Concatenate the converted parts vertically
            result_image = np.concatenate((bgr_top_half, rgb_bottom_half), axis=0)

            # Generate the output file path
            output_file_path = os.path.join(output_folder, file.filename)
            
            # Check if the file extension is .pgm
            if output_file_path.lower().endswith('.pgm'):
                # Generate a new file name with the .jpg extension
                output_file_path = os.path.splitext(output_file_path)[0] + '.jpg'

            # Save the resulting image
            cv2.imwrite(output_file_path, result_image)


            print(temp_path_jpg, temp_path_pgm)
            # Remove the temporary file
            os.remove(temp_path_pgm)
            os.remove(temp_path_jpg)

        return redirect(url_for('inside'))

    return render_template('inside.html')



@app.route('/outside', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the uploaded files
        files = request.files.getlist('files')

        # Process each file
        for file in files:
            # Save the uploaded file to a temporary folder
            file_path = os.path.join('temp', file.filename)
            temp_path_pgm = file_path
            file.save(file_path)

            # Get the input folder path
            # input_folder = os.path.dirname(file_path)

            # Check if the file extension is .pgm
            if file.filename.lower().endswith('.pgm'):
                # Generate a new file name with the .jpg extension
                jpg_image_path = os.path.splitext(file_path)[0] + '.jpg'

                # Load the PGM image using PIL and convert it to RGB
                with Image.open(file_path) as pgm_image:
                    pgm_image = pgm_image.convert("RGB")

                    # Save the image as JPG format
                    pgm_image.save(jpg_image_path)

                # Update the file path to the JPG image
                file_path = jpg_image_path
                temp_path_jpg = file_path


            # Load the Bayer image
            bayer_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            # Calculate the height of the image
            height = bayer_image.shape[0]

            # Divide the image into three parts
            top_third = bayer_image[:height // 3, :]
            middle_third = bayer_image[height // 3:2 * height // 3, :]
            bottom_third = bayer_image[2 * height // 3:, :]

            # Convert the top 1/3 and bottom 1/3 using cv2.COLOR_BAYER_GR2BGR
            bgr_top_third = cv2.cvtColor(top_third, cv2.COLOR_BAYER_GR2BGR)
            bgr_bottom_third = cv2.cvtColor(bottom_third, cv2.COLOR_BAYER_GR2BGR)

            # Convert the middle 1/3 using cv2.COLOR_BAYER_RG2RGB
            rgb_middle_third = cv2.cvtColor(middle_third, cv2.COLOR_BAYER_RG2RGB)

            # Concatenate the converted parts vertically
            result_image = np.concatenate((bgr_top_third, rgb_middle_third, bgr_bottom_third), axis=0)

            # Generate the output file path
            output_file_path = os.path.join(output_folder, file.filename)
            
            # Check if the file extension is .pgm
            if output_file_path.lower().endswith('.pgm'):
                # Generate a new file name with the .jpg extension
                output_file_path = os.path.splitext(output_file_path)[0] + '.jpg'

            # Save the resulting image
            cv2.imwrite(output_file_path, result_image)

            # Remove the temporary file
            os.remove(temp_path_pgm)
            os.remove(temp_path_jpg)

        return redirect(url_for('upload'))

    return render_template('upload.html')

if __name__ == '__main__':
    # Create the temporary folder if it doesn't exist
    if not os.path.exists('temp'):
        os.makedirs('temp')

    app.run(host='0.0.0.0', port=5000, debug=True)
