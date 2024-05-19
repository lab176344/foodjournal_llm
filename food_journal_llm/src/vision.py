import base64
import requests  # type: ignore
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_KEY")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyse_image(image_path):

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What are the main ingredients of \
                        the food in the photo? Just give the top 5 \
                        ingredients as response. For example, 'rice,\
                        # lentils, tomatoes, onions, and spices. return \
                        it is a dictionary with the key 'ingredients'. \
                        Don't return anything else. Just the dictionary."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload)

    response_content = response.json()
    assistant_role = response_content['choices'][0]['message']['content']
    return assistant_role
