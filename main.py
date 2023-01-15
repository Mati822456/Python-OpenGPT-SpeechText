import openai
import pyttsx3
import speech_recognition as sr

openai.api_key = "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"

def gpt(stext):
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=stext,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response)
    return response.choices[0].text

def sayResponse(sentence):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)
    engine.setProperty('rate', 125)

    engine.say(sentence)
    engine.runAndWait()
    engine.stop()

def recognizeSpeech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Say Anything: ')
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print('Prompt: {}'.format(text))
        response = gpt(format(text))
        print(response)
        sayResponse(response)
    except:
        print('Cannot recognize your voice')
        sayResponse('Cannot recognize your voice')

#recognizeSpeech()
