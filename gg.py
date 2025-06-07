
import os
punctuation='.。\n'
os.environ['ARGOS_DEVICE_TYPE'] = 'auto'
from colorama import Fore





import Audio
from cout import cout

from sys import argv
tries=int(argv[1])
text=argv[2:]
if os.path.exists(text[0]):
    with open(text[0],'r',encoding='utf-8') as f:
        text=f.read()
else:
    text=' '.join(text)

text=text.replace('\n\n','\n')
for i in punctuation:
    text=text.replace(i,'[SPLIT]')
text=text.replace(' ','')
text=text.replace('[SPLIT]'*2,'[SPLIT]')
text=text.split('[SPLIT]')
for i in text:
    print(Fore.GREEN,f'{i}')
print(Fore.RESET)
if tries :
    import Translator
    translatedTextList=Translator.getTranslationList(textList=text,tries=tries)
else:
    translatedTextList=text

audioList=[]
import tqdm
newTranslatedTextList:list=[]
newTextList:list=[]
if len(translatedTextList)- len(text)>0:
    for i in range(len(text)):
        newTranslatedTextList.append(translatedTextList[i])
    translatedTextList=newTranslatedTextList
elif len(text)-len(translatedTextList)>0:
    for i in range(len(translatedTextList)):
        newTextList.append(text[i])
    text=newTextList




for i in translatedTextList:
    print(Fore.GREEN,f'{i}',Fore.RESET,end='\r')
    
    audioList.append(Audio.getAudioDuration(i))

import getVideo
getVideo.createVideo(
    textsCenter=translatedTextList,
    textsBottom=text,
    audioFiles=audioList,
    output=f'{argv[2]}.mp4')
