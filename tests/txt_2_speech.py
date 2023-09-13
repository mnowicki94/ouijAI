import pyttsx3 as tts

def txt2speech(mytext):
    # engine = tts.init()
    # voices = engine.getProperty('voices')
    # newVoiceRate = 100
    # engine.setProperty('rate',newVoiceRate)
    # engine.setProperty('voice', voices[1].id)
    # engine.setProperty('pitch', 55)

    engine = tts.init('sapi5')
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 100)
    engine.setProperty('pitch', 0.9)
    engine.say(mytext)
    engine.runAndWait()
    engine.stop()


txt='helllo o o o  booo i am ghost'
txt2speech(txt)

