import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import AudioFileClip, concatenate_audioclips, VideoFileClip
import os
from tqdm import tqdm, trange
from cout import cout,endl
import dill as pickle
from colorama import Fore, Back, Style, init
def bgImage():
    white=255*np.ones((1080,1920,3),np.uint8)
    cv2.imwrite("A.jpg",white)
if not os.path.exists("A.jpg"):
    bgImage()
def clean(audioFiles):
    print(Fore.CYAN+'清理')
    for file in tqdm(audioFiles):
        if os.path.exists(file):
            os.remove(file)

def drawText(img,text_center,text_bottom,font,text_color,bottom_margin,width,height):
        newtext_center=''
        count=0
        for text in text_center:
            count+=1
            newtext_center+=text
            if count>20:
                 newtext_center+='\n'
                 count=0
        text_center=newtext_center

        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        draw = ImageDraw.Draw(pil_img)

        # 居中文本
        bbox_center = draw.textbbox((0, 0), text_center, font=font)
        tw_c = bbox_center[2] - bbox_center[0]
        th_c = bbox_center[3] - bbox_center[1]
        x_c = (width - tw_c) // 2
        y_c = (height - th_c) // 2
        draw.text((x_c, y_c), text_center, fill=text_color, font=font)

        # 底部文本
        bbox_bottom = draw.textbbox((0, 0), text_bottom, font=font)
        tw_b = bbox_bottom[2] - bbox_bottom[0]
        th_b = bbox_bottom[3] - bbox_bottom[1]
        y_b = height - bottom_margin - th_b
        draw.text((50, y_b), text_bottom, fill=text_color, font=font)
        frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        return frame
from threading import Thread
thread=None
def createAudio(audioFiles:list,output:str='temp_audio.mp3')->int:
    global thread
    audio_clips = []
    #audioFiles:[file name,duration]
    currentTime=0
    cout<<"开始合成音频文件..."<<endl
    for file in tqdm(audioFiles):
            try:
                audio_clips.append(file[0].with_start(currentTime))
                currentTime+=file[1]
            except Exception as e:
                cout<<e<<endl
    finalAudio = concatenate_audioclips(audio_clips)
    thread=Thread(target=finalAudio.write_audiofile,args=(output,))
    thread.start()
    return finalAudio.duration

def pairTextWithAudio(frameList:list,textsCenter:list,textsBottom:list,audioFiles:list,fps:int)->list:
    frameCount=len(frameList)
    framePointer=0
    textPointer=0
    audioFilesWithFramestartandEnd=[]
    currentFrames=0
    for i in range(len(audioFiles)):
        audioName=audioFiles[i][0]
        audioDuration=audioFiles[i][1]
        audioFrames=audioDuration*fps
        audioFilesWithFramestartandEnd.append([audioName,currentFrames,currentFrames+audioFrames])
        currentFrames+=audioFrames

    currentIndex=0 
    pbar=tqdm(total=frameCount,desc="对齐文本与音频")
    while framePointer<frameCount:
        
        if audioFilesWithFramestartandEnd[currentIndex][1]<=framePointer<audioFilesWithFramestartandEnd[currentIndex][2]:
                frameList[framePointer]=[textsCenter[textPointer],textsBottom[textPointer]]
        if framePointer>=audioFilesWithFramestartandEnd[currentIndex][2]:
            currentIndex+=1
            textPointer+=1
        framePointer+=1
        pbar.update(1)

            
    return frameList
def pairTextWithAudio2(frameList:list,textsBottom:list,audioFiles:list,fps:int)->list:
    frameCount=len(frameList)
    framePointer=0
    textPointer=0
    audioFilesWithFramestartandEnd=[]
    currentFrames=0
    for i in range(len(audioFiles)):
        audioName=audioFiles[i][0]
        audioDuration=audioFiles[i][1]
        audioFrames=audioDuration*fps
        audioFilesWithFramestartandEnd.append([audioName,currentFrames,currentFrames+audioFrames])
        currentFrames+=audioFrames

    currentIndex=0 
    pbar=tqdm(total=frameCount,desc="对齐文本与音频")
    while framePointer<frameCount:
        
        if audioFilesWithFramestartandEnd[currentIndex][1]<=framePointer<audioFilesWithFramestartandEnd[currentIndex][2]:
                frameList[framePointer]=[textsBottom[textPointer]]
        if framePointer>=audioFilesWithFramestartandEnd[currentIndex][2]:
            currentIndex+=1
            textPointer+=1
        framePointer+=1
        pbar.update(1)

            
    return frameList
    
def createVideo(textsCenter:list,textsBottom:list,audioFiles:list,output:str)->None:
    # 背景图片
    global thread
    img = cv2.imread("A.jpg")
    if img is None:
        bgImage()
        img = cv2.imread("A.jpg")
    Bgimg=cv2.imread("A.jpg")
    fps=30
    fontSizeCenter=60

    fontPath=r"./AlibabaPuHuiTi-3-55-Regular.ttf"
    textColor=(0,0,0)
    bottomMargin=200
    fontCenter=ImageFont.truetype(fontPath,fontSizeCenter)
    height, width, _ = img.shape
    audioDuration=createAudio(audioFiles)
    audioFrames=int(audioDuration*fps)
    frameList=[0 for i in range(audioFrames)]
    frameList=pairTextWithAudio(frameList,textsCenter,textsBottom,audioFiles,fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(f'{output}temp.mp4', fourcc, fps, (width, height))
    for i in trange(len(frameList)):
            try:
                if frameList[i]!=frameList[i-1]:
                    img = cv2.imread("A.jpg")
                    img=drawText(img,*frameList[i],fontCenter,textColor,bottomMargin,width,height)    
                video_writer.write(img)
            except TypeError as e:
                video_writer.write(Bgimg)
            
    video_writer.release()
    thread.join()
    combineAV("temp_audio.mp3",f'{output}temp.mp4',output)
    clean([f'{i}.wav' for i in range(len(audioFiles))]+[f'{output}temp.mp4',"temp_audio.mp3"])

def combineAV(audio_file:str,video_file:str,output_file:str)->None:
    os.system(f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac {output_file}")
