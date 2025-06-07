import configparser


config = configparser.ConfigParser()
config.read('config.ini')

MODEL=config['ollama']['model']


import ollama
for mod in ollama.list().models:
    if MODEL in mod.model:
        MODEL=mod.model
        break




def translate(text,toLang='en'):
    X='you are a translation API,now you should translate the following text to'+toLang+'. reply translation only . Never reply with useless words'#
    stream = ollama.chat(
        model=MODEL,
        messages=[{'role':'system','content':X},{'role': 'user', 'content': text}],
        stream=True,
    )
    res=''
    for chunk in stream:
        i=chunk['message']['content']
        res+=i
    res=res.replace('\n','')
    return res

if __name__ == '__main__':
    text='你好。'
    print(translate(text,'jp'))