from openai import OpenAI
import base64
import os
import pandas as pd

client = OpenAI()
df = pd.DataFrame(columns=['number', 'answer'])

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

hand_type = "Second"

folder_path = f'clock_one_arrow_twisted_dataset/{hand_type}'

# prompt = '''I will provide an image of an analog clock with only one hand visible.\
#  Your task is to determine its position as a number in the range of [0-59], where 0 corresponds to 12 o'clock,\
#  and each increment represents a proportional movement.'''

prompt = '''I will provide an image of an analog clock with only one hand visible. Your task is to determine its \
position as a number in the range of [0-59], where each number corresponds to a tick mark on the clock face, with 0 \
representing the 12 o'clock position and each increment representing a proportional movement along the clock's scale.'''

# prompt = '''I will provide an image of an analog clock with only one hand visible.\
#  Your task is to determine its position.'''

# prompt = '''What time is shown on the clock in the given image?'''




for i in range(60):
    filename = f'{hand_type}_{i:02d}.png'
    image_path = os.path.join(folder_path, filename)
# image_path = "clock_one_arrow_dataset/Second/Second_01.png"
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500,
        temperature=0,
    )
    df.at[i, 'number'] = i
    df.at[i, 'answer'] = response.choices[0].message.content
    print(response.choices[0].message.content)
df.to_excel(f'twisted_one_hand_result/{hand_type}.xlsx', index=False, engine='openpyxl')