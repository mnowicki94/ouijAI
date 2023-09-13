import pyttsx3 as tts
# import speech_recognition as sr

def txt2speech(mytext):
    engine = tts.init()
    voices = engine.getProperty('voices')
    newVoiceRate = 250
    engine.setProperty('rate',newVoiceRate)
    engine.setProperty('voice', voices[1].id)
    engine.say(mytext)
    engine.runAndWait()
    engine.stop()


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