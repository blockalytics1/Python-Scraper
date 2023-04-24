import shutil
import os
import json
import requests
import time
import csv
import qrcode
from bs4 import BeautifulSoup

csv_dest_dir = "G:/My Drive/csv"
png_dest_dir = "G:/My Drive/png"

if not os.path.exists(csv_dest_dir): os.makedirs(csv_dest_dir)
if not os.path.exists(png_dest_dir): os.makedirs(png_dest_dir)

filename = 1
x = False
# Replace this with the URL of the webpage you want to scrape
url = "http://10.224.125.155/file"
while(x == False):
    # Make a GET request to the webpage
    response = requests.get(url)
    filename = 1
    # Check if the request was successful
    if response.status_code == 200:
        x = True
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract the text from the page
        text = soup.get_text()

        

        # Define the output filename
        # Create a dictionary with the text as the value
        data = {"readings":{}}
        reading_entry = data["readings"]
        entry_id = 1
        data_array = [entry for entry in text.split('\n') if len(entry) > 0]
        n = len(data_array)
        for i in range(0, n, 2):
            temp_reading = data_array[i].split(':\t')
            time_reading = data_array[i + 1].split(':\t')
            reading_entry[str(entry_id)] = {temp_reading[0]:temp_reading[1], time_reading[0]: time_reading[1]}
            entry_id += 1

        print(json.dumps(data))
        
        csv_filename = str(filename) + ".csv"
        with open(csv_filename, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["ID", str(filename)])
            csv_writer.writerow(["entry_id", "Temperature", "Time"])

            # Write data
            for entry_id, entry_data in data["readings"].items():
                csv_writer.writerow([entry_id, entry_data["Temperature"], entry_data["Time"]])

        print(f"Text has been extracted and written to {filename}.")
        # GDrive stuff
        # file_id = upload_to_google_drive(csv_filename, 'text/csv')
        shutil.move(csv_filename, os.path.join(csv_dest_dir, csv_filename))
        print(f"File  {csv_filename} has been uploaded to Google Drive")

        # Generate QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(csv_filename)
        qr.make(fit=True)
        qr_image = qr.make_image(file_color="black", back_color="white")
        qr_code_filename = f"{csv_filename}_qr.png"
        qr_image.save(qr_code_filename)
        print(f"QR code generated for {csv_filename} and saved as {qr_code_filename}")

        # qr_file_id = upload_to_google_drive(qr_code_filename, 'image/png')
        shutil.move(qr_code_filename, os.path.join(png_dest_dir, qr_code_filename))
        print(f"QR code {qr_code_filename} uploaded to Google Drive")
        filename += 1

    else:
        # If the request failed, print an error message
        print("Error: Could not retrieve page content.")
        time.sleep(60)

# Google Drive
# 1. Convert text -> JSON -> CSV file
# 2. Put JSON file in Blockalytics GDrive
# 3. Generate a QR code associated with the data ID