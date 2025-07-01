import requests
import os

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"  # Assuming your FastAPI app is running locally on port 8000
UPLOAD_ENDPOINT = f"{BASE_URL}/upload_doc/"

# --- Image Details ---
CUSTOMER_ID = 1  # Replace with an existing customer ID from your database
DOCUMENT_TYPE = "Passport Photo"
IMAGE_FILE_PATH = "uploaded_docs/customer_4_doc_3.jpg" # Make sure this image file exists in the same directory as your script or provide a full path

try:
    with open(IMAGE_FILE_PATH, 'rb') as f:
        files = {'file': (os.path.basename(IMAGE_FILE_PATH), f, 'image/jpeg')}
        data = {
            'customer_id': CUSTOMER_ID,
            'document_type': DOCUMENT_TYPE
        }

        print(f"Attempting to upload image for Customer ID: {CUSTOMER_ID} with Document Type: {DOCUMENT_TYPE}")
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)

    if response.status_code == 200:
        print("Image uploaded successfully!")
        print(response.json())
    else:
        print(f"Failed to upload image. Status code: {response.status_code}")
        print(response.json())

except FileNotFoundError:
    print(f"Error: The image file '{IMAGE_FILE_PATH}' was not found.")
except requests.exceptions.ConnectionError:
    print(f"Error: Could not connect to the FastAPI application at {BASE_URL}. Make sure it's running.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")