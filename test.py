from sys import argv
punctuation='.。\n'
import os
from colorama import Fore, Back, Style, init
init()
import Audio
from cout import cout
argv=['www','0','input.txt']
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

print(text)
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
