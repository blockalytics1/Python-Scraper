import requests
import json
import time
from bs4 import BeautifulSoup
x = False
# Replace this with the URL of the webpage you want to scrape
url = "http://10.224.125.155/file"
while(x == False):
    # Make a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        x = True
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        # Extract the text from the page
        text = soup.get_text()

        # Define the output filename
        filename = "1"
        # Create a dictionary with the text as the value
        data = {"text": text}

        # Write the data to a JSON file
        #f = open(filename, "w")
        with open(filename, "w") as f:
            json.dump(data, f)
            
        print(f"Text has been extracted and written to {filename}.")
    else:
        # If the request failed, print an error message
        print("Error: Could not retrieve page content.")
        time.sleep(60)