import ollama
import base64
import os
from PIL import Image

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

folder_path = './images'
all_images = []


def getResponse():
    # Encode the image
    base64_image = encode_image(image_path)

    # Send request to Ollama
    response = ollama.chat(
        model="llava:latest",
        messages=[
            {
                'role': 'user',
                'content': 'tell me in 3 or four words if this structure is damaged, and how bad if it is? and what part of the building is damaged?',
                'images': [base64_image]
            }
        ]
    )

    # Print the response
    print(response['message']['content'])


for root, _, files in os.walk(folder_path):
    for file in files:
        # Path to your image
        image_path = os.path.join(root, file)
        print('For image: ', file)
        img = Image.open(image_path)
        img.show()
        getResponse()