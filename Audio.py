import pyttsx3
from moviepy import *
count=0
def getAudio(text):
    global count
    count+=1
    engine = pyttsx3.init()
    engine.save_to_file(text, f'{count}.wav')
    engine.runAndWait()
    engine.stop()
    return f'{count}.wav'

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def getDuration(path)->tuple:
    
    try:
        clip = AudioFileClip(path)
        duration = clip.duration
    except Exception as e:
        print(path, e)
        duration = 0
        clip = None
    return clip,duration
def getAudioDuration(text):
    audio_path = getAudio(text)
    cd = getDuration(audio_path)
    return cd


