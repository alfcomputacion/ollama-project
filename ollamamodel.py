import ollama
import speech_recognition as sr
# from sounddevice import play, sd
# from  pocketsphinx LiveSpeech


# recog = sr.Recognizer()
# mic = sr.Microphone()
# if not mic:
#     raise ValueError("No microphone found")
# file_name = "voice_command.mp3"


response = ollama.chat(
    model='deepseek-r1:8b', 
    messages=[{'role': 'user', 'content': 'como crear un script de reconocimiento de voz offline en python'}]
)

if response:
    print(response['message']['content'])