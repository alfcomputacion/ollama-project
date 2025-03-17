import ollama
import speech_recognition as sr
import json
# from sounddevice import play, sd
# from  pocketsphinx LiveSpeech


# recog = sr.Recognizer()
# mic = sr.Microphone()
# if not mic:
#     raise ValueError("No microphone found")
# file_name = "voice_command.mp3"

texto = ""
instruction = ""
with open('./data/text1.txt', 'r') as f:
    str_txt = f.read()
    texto = str_txt
with open('./data/instructions.txt', 'r') as f:
    str_txt = f.read()
    instruction = str_txt

def response():
    response = ollama.chat(
        model='deepseek-r1:8b', 
        messages=[{'role': 'user', 'content': instruction + texto}]
        
    )

    if response:
        # print(response['message']['content'])
        print(json.dumps(response.json(), indent=4))
response()