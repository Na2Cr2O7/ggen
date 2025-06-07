import os
#



from random import choice
from sys import argv

from colorama import Fore
import configparser
# from string import punctuation
# punctuation=punctuation+'。，！？、：；“”‘’《》'

config = configparser.ConfigParser()
with open('config.ini', 'r') as f:
    config.read_file(f)
os.environ['ARGOS_DEVICE_TYPE']=config['DEFAULT']['device']
from argostranslate import package, translate
if not config['DEFAULT']['installed']=='True':
    import tqdm
    for i in tqdm.tqdm(os.listdir()):
        if i.endswith(".argosmodel"):
            package.install_from_path(i)


iso639={
    'English':'en',
    'Albanian':'sq',
    'Arabic':'ar',
    'Chinese':'zh',
    'French':'fr',
    'German':'de',
    'Italian':'it',
    'Japanese':'ja',
    'Portuguese':'pt',
    'Russian':'ru',
    'Spanish':'es'
}
iso639_Chinese={
    '英语':'en',
    '阿尔巴尼亚语':'sq',
    '阿拉伯语':'ar',
    '中文':'zh',
    '法语':'fr',
    '德语':'de',
    '意大利语':'it',
    '日语':'ja',
    '葡萄牙语':'pt',
    '俄语':'ru',
    '西班牙语':'es'
}
reversedIso639={v:k for k,v in iso639.items()}
reversedIso639_Chinese={v:k for k,v in iso639_Chinese.items()}


srclang= 'Chinese'
dstlang= srclang
srclang=iso639[srclang]
dstlang=iso639[dstlang]


installed_languages = translate.get_installed_languages()
lang=[str(lang) for lang in installed_languages]
lang=[iso639[i] for i in lang if i in iso639]
langPair=[srclang,choice(lang)]


tries=int(argv[1])
translatedText=' '.join(argv[2:])
if os.path.isfile(translatedText):
    
    with open(translatedText,'r',encoding='utf-8') as f:
        translatedText=f.read()
    print(Fore.CYAN,'<<\n',Fore.RESET,translatedText)


def getTranslation(text,src,dst):
    
    print(Fore.RESET)
    print(Fore.CYAN,reversedIso639[src],f"({reversedIso639_Chinese[src]})",'->',reversedIso639[dst],f"({reversedIso639_Chinese[dst]})",Fore.RESET)
    try:
        target = translate.translate(text,src,dst)
    except AttributeError:
        return None
    except Exception as e:
        print(Fore.RESET,e)
        return None
    return target


for i in range(tries):
        print(Fore.RESET)
        print(Fore.YELLOW,f"{i+1}/{tries}")
        target= getTranslation(translatedText,*langPair)
        if not target:
            langPair=[langPair[0],choice(lang)]
            continue
        translatedText=target
        langPair.pop(0)
        langPair.append(choice(lang))
        print(translatedText)


langPair[1]=dstlang
target= getTranslation(translatedText,*langPair)


while not target:
    langPair[1]=choice(lang)
    target=getTranslation(translatedText,*langPair)
    if not target:
        langPair[1]=choice(lang)
        continue
    translatedText=target
    print(Fore.RED,translatedText)
    target= translate.translate(translatedText,langPair[1],dstlang)
translatedText=target
print(Fore.GREEN,translatedText)
print(Fore.RESET)
with open('result.txt','w',encoding='utf-8') as f:
    f.write(translatedText)
os.startfile('result.txt')
