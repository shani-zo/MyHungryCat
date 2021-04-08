import io
import os

# Imports the Google Cloud client library
from google.cloud import vision


AUTHENTICATION_KEY_PATH = r"C:\Users\shani\Downloads\dyinterview-8a7ec547ca93.json"


def authenticate():
    """Try setting up credentials for using google Cloud vision API"""
    if not os.path.exists(AUTHENTICATION_KEY_PATH):
        print("Path to authentication key was not found. If no other existing key is found an error will be shown.")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = AUTHENTICATION_KEY_PATH


authenticate()

# Google example code

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('resources/wakeupcat.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)