import os

# Imports the Google Cloud client library
from google.cloud import vision


AUTHENTICATION_KEY_PATH = r"C:\Users\shani\Downloads\dyinterview-8a7ec547ca93.json"


def authenticate() -> None:
    """Try setting up credentials for using google Cloud vision API"""
    if not os.path.exists(AUTHENTICATION_KEY_PATH):
        print("Path to authentication key was not found. If no other existing key is found an error will be shown.")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = AUTHENTICATION_KEY_PATH


def classify_image(image_content: bytes) -> list:
    """
    Send image to classification engine and return resulted labels

    Args:
        image_content: Image to classify

    Returns:
        Labels identified in the image provided

    """
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    return [label.description for label in labels if label.score > 0.5]


authenticate()
"""
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
"""
