import os
from cout import *
import argostranslate.package
import tqdm
cout << "请将.argosmodel 放在该目录("<< os.getcwd() <<")下\n"
input("按任意键继续...")
for i in tqdm.tqdm(os.listdir()):
    if i.endswith(".argosmodel"):
        argostranslate.package.install_from_path(i)