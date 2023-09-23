import pyttsx3 as tts
import base64
import requests
import os
# import speech_recognition as sr

def txt2speech(mytext):
    engine = tts.init()
    voices = engine.getProperty('voices')
    newVoiceRate = 150
    engine.setProperty('rate',newVoiceRate)
    engine.setProperty('voice', voices[0].id)
    engine.say(mytext)
    engine.runAndWait()
    engine.stop()


def generate_face():

    stabilityai_key = os.getenv("STABILITYAI_APIKEY")


    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    body = {
      "steps": 40,
      "width": 1024,
      "height": 1024,
      "seed": 0,
      "cfg_scale": 5,
      "samples": 1,
      "text_prompts": [
        {
          "text": "face of scary, creepy unnatural person",
          "weight": 1
        },

        {
          "text": "blurry, bad, anime",
          "weight": -1
        }
      ],
    }

    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": stabilityai_key,
    }

    response = requests.post(
      url,
      headers=headers,
      json=body,
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    # make sure the out directory exists
    if not os.path.exists("./out"):
        os.makedirs("./out")


    return data["artifacts"][0]['base64']




# def spch2txt():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         r.pause_threshold = 1
#         r.adjust_for_ambient_noise(source)
#         print("Listening...")
#         audio = r.listen(source)
#     try:
#         print("Recognizing...")
#         query= r.recognize_google(audio,language= 'pl-PL')
#         print(f"user said: {query}\n")
#     except Exception as e:
#         # speak("Miss stark couldn't recognize what you said, speak once more.")
#         print("Miss stark couldn't recognize what you said, speak once more.")
#         return None
#     return query

# spch2txt()