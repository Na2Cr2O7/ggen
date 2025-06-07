import os
import shutil
import tqdm
if not os.path.exists(r'.\temp'):
    os.makedirs(r'.\temp')

fileExt=['.txt','.py','.ini','.argosmodel','.ttc','.U','.ttf','.jpg']
for file in tqdm.tqdm(os.listdir()):
    print(os.path.splitext(file)[1])
    if os.path.isdir(file):
        print(f'>>{file}')
    if not os.path.splitext(file)[1] in fileExt:
        shutil.move(file,r'.\temp')
i=input('需要删除d:\AllArgosTranslateModels\temp文件夹吗？(y/n)')
if i=='y':
    shutil.rmtree(r'.\temp')