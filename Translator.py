import os
#
from cout import cout
from random import choice
from colorama import Fore
import configparser


config = configparser.ConfigParser()
with open('config.ini', 'r') as f:
    config.read_file(f)





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


# installed_languages = translate.get_installed_languages()
# lang=[str(lang) for lang in installed_languages]
# lang=[iso639[i] for i in lang if i in iso639]

lang=['en', 'sq', 'ar', 'zh', 'fr', 'de', 'it', 'ja', 'pt', 'ru', 'es']



import threading
import time
loadingShouldStop=False
threadingShouldStop=False
loadingIndex=0
def loading():
    global loadingShouldStop
    global loadingIndex
    global threadingShouldStop
    b=['|', '/', '-', '\\']

    while not threadingShouldStop:
        TA=0
        while not loadingShouldStop:
            print(b[loadingIndex % 4],'\t',f'{TA:.1f}s',end='\r')
            loadingIndex+=1
            time.sleep(0.1)
            TA+=.1
        time.sleep(.1)
threading.Thread(target=loading).start()





#argos translate

os.environ['ARGOS_DEVICE_TYPE']=config['argos']['device']


from argostranslate import package, translate

if not config['argos']['installed']=='True':
    import tqdm
    for i in tqdm.tqdm(os.listdir()):
        if i.endswith(".argosmodel"):
            package.install_from_path(i)

def getTranslation(text,src,dst):
    
    print(Fore.RESET)
    print(Fore.CYAN,reversedIso639[src],f"({reversedIso639_Chinese[src]})",'->',reversedIso639[dst],f"({reversedIso639_Chinese[dst]})",Fore.RESET)
    startLoading()
    try:
        target = translate.translate(text,src,dst)
    except AttributeError:
        stopLoading()
        return None
    except Exception as e:
        stopLoading()
        print(Fore.RESET,e)
        return None
    stopLoading()
    return target

def startLoading():
    global loadingShouldStop
    loadingShouldStop=False
def stopLoading():
    global loadingShouldStop
    loadingShouldStop=True
def stopThreading():
    global threadingShouldStop
    global loadingShouldStop
    loadingShouldStop=True

    threadingShouldStop=True

def getTranslation2(text,src,dst):
    '''Translate text into english first'''
    
    target=getTranslation(text,src,'en')
    if not target:
        return getTranslation(text,src,dst)
    return getTranslation(target,'en',dst)



import OllamaTranslation
def getTranslation3(text,src,dst):

    '''use LLM to translate text'''

    #src is useless
    text=text.replace('\n\n','\n')
    print(Fore.CYAN,reversedIso639[src],f"({reversedIso639_Chinese[src]})",'->',reversedIso639[dst],f"({reversedIso639_Chinese[dst]})",Fore.RESET)
    startLoading()
    result=''
    for i in text.split('\n'):
        target=OllamaTranslation.translate(i,reversedIso639[dst])
        print(Fore.RESET,target)
        result+=target+'\n'
    stopLoading()
    return result


#another translate function
try:
    from translate import Translator
    def translateText(text,src,dst):
        startLoading()

        translator = Translator(to_lang=dst)
        translated=''
        for i in text.split('\n'):    
            translated_text = translator.translate(i)
            print(translated_text)
            translated+=translated_text+'\n'
        
        stopLoading()
        return translated
except ImportError:
    pass



functionDict={'argos':getTranslation,'ollama':getTranslation3,'translate':translateText}

#change translate function here
translateFunction=functionDict[config['DEFAULT']['translateFunction']]
def getTranslationList(textList,tries=10)->list:
    langPair=[srclang,choice(lang)]
    translatedText='\n'.join(textList)
    i=0
    while True:
            print(Fore.RESET)
            print(Fore.YELLOW,f"{i+1}/{tries}")
            target= translateFunction(translatedText,*langPair)
            if not target:
                langPair=[langPair[0],choice(lang)]
                continue
            translatedText=target
            langPair.pop(0)
            langPair.append(choice(lang))
            print(translatedText)
            i+=1
            if i>=tries:
                break
        


    langPair[1]=dstlang
    target= translateFunction(translatedText,*langPair)


    while not target:
        langPair[1]=choice(lang)
        target=translateFunction(translatedText,*langPair)
        if not target:
            langPair[1]=choice(lang)
            continue
        translatedText=target
        print(Fore.RED,translatedText)
        target=translateFunction(translatedText,langPair[1],dstlang)
        cout <<Fore.GREEN << target << Fore.RESET<<'\n'
    
    cout<<Fore.RESET<<'\n'

    
    translatedText=target

    cout<<translatedText<<'\n'

    print(Fore.RESET)
    stopThreading()
    return translatedText.split('\n')

if __name__ == '__main__':
    
    print( getTranslationList(['你好，世界！'],2))
