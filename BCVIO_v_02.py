#!/usr/bin/env python
#Batcher by Philipp Hanke
#Version 0.2
from tkinter.constants import DISABLED
from PySimpleGUI.PySimpleGUI import Image
import cv2
import os
import PySimpleGUI as sg
import time
import numpy as np
version=str(0.2)
rgb=0
bgr=0
asr=0
nwa=0
nw=0
nh=0
image_batch=[]
save_path=[]
heightArray=[]
widthArray=[]
channelArray=[]
pathArray=[]
print ("Batcher__Version__", version, "__by Philipp Hanke")
sg.theme('Dark Blue 3')
layout = [[sg.Text('Give me a batch of images to optimize')],
[sg.Text('Original image folder ', size=(30, 1)), sg.InputText(), sg.FolderBrowse()],
[sg.Text('Save optimized images to ', size=(30, 1)), sg.InputText(), sg.FolderBrowse()],
[[sg.Checkbox('Keep original size', default=0), sg.Checkbox('Keep aspect ratio', default=0), sg.Checkbox('Grayscale', default=0),]],
[sg.Submit(), sg.Cancel()]]
layout2 = [[sg.Text('New Image Size')],
[sg.Text('New width in px', size=(10, 1)), sg.InputText()],
[sg.Text('New height in px', size=(10, 1)), sg.InputText()],
[sg.Submit()]]
layout3 = [[sg.Text('New Image Size')],
[sg.Text('New long edge in px ', size=(30, 1)), sg.InputText()],
[sg.Submit()]]
layout4 = [[sg.Text('Color Conversion')],
[[sg.Checkbox('RGB', default=0), sg.Checkbox('BGR',default=0)]],
[sg.Submit()]]
layout5 = [[sg.Text('Press q to quit')]]
layout6 = [[sg.Text('Ready - Thank you for the job!')],
[sg.Button('Safe and Exit')],
[sg.Button('Exit')]]
font=cv2.FONT_HERSHEY_SIMPLEX
window = sg.Window('Batcher v '+ version, layout)

event, values = window.read()
path, path2, ors, asr, gs  = values[0], values[1], values[2], values[3], values[4]
window.close()     

if ors == True:
    pass
if ors == 0 and asr != True:
    window2 = sg.Window('Batcher v '+ version, layout2)
    event, sizes = window2.read()
    window2.close()
    nw, nh, = sizes[0], sizes[1]
    nw=int(nw)
    nh=int(nh)
if asr == True:
    window3 = sg.Window('Batcher v '+ version, layout3)
    event, sizesa = window3.read()
    window3.close()
    nwa = sizesa[0]
    nwa=int(nwa)
if gs != True:
    window4 = sg.Window('Batcher v '+ version, layout4)
    event, colors = window4.read()
    window4.close()
    rgb, bgr = colors[0], colors[1]
def read_image():
    for img in os.listdir(path):
        if not img.startswith("."):
            if img.endswith(".jpg") or img.endswith(".png") or img.endswith(".jpeg"):
                os.chdir(path)
                ImagePath=os.path.join(path,img)
                saveImagePath=os.path.join(path2,img)
                print('Loading ', ImagePath)
                proimg=cv2.imread(ImagePath)
                height,width,channels = proimg.shape
                pathArray.append(ImagePath)
                image_batch.append(proimg)
                save_path.append(saveImagePath)
                widthArray.append(width)
                heightArray.append(height)
    return image_batch
    return widthArray
    return heightArray
    return pathArray
def colorConversion():
    i=0
    for proimg in image_batch:       
        if rgb == True:
            image_batch[i]=cv2.cvtColor(image_batch[i],cv2.COLOR_BGR2RGB)
            print('Converted ',pathArray[i] , ' to RGB')
        if bgr == True:
            image_batch[i]=cv2.cvtColor(image_batch[i],cv2.COLOR_RGB2BGR)
            print('Converted ',pathArray[i] , ' to BGR')
        if gs == True:
            image_batch[i]=cv2.cvtColor(image_batch[i],cv2.COLOR_RGB2GRAY)
            print('Converted ',pathArray[i] , ' to Grayscale')
        if gs!= True and bgr != True and rgb != True:
            pass
        i=i+1
    return image_batch

def resize():
    i=0
    for proimg in image_batch:
        height=heightArray[i]
        width=widthArray[i]
        if asr  == True:
            if height > width:
                aspectRatio=width/height
                nw=nwa*aspectRatio
                nw=int(nw)
                image_batch[i]=cv2.resize(image_batch[i],(nw,nwa))
                print('Resized ',pathArray[i] , ' to ', nw, 'x', nwa, 'px')
            if width >= height:
                aspectRatio=height/width
                nh=nwa*aspectRatio
                nh=int(nh)
                image_batch[i]=cv2.resize(image_batch[i],(nwa,nh))
                print('Resized ',pathArray[i], ' to ', nwa, 'x', nh, 'px')
        if asr != True:   
            image_batch[i]=cv2.resize(image_batch[i],(nw,nh))
        #if ors == True:
        #    pass
        i=i+1
    return image_batch
def showImage():
    i=0
    for proimg in image_batch:               
        cv2.imshow(pathArray[i],image_batch[i])
        i=i+1

def saveImage():
    i=0
    for proimg in image_batch:
        cv2.imwrite(save_path[i], image_batch[i])
        print('Saved optimized image ',pathArray[i], ' to ', save_path[i])
        i=i+1

read_image()
colorConversion()

if ors != True:
    resize()
    
showImage()
print('All Done!')
window6 = sg.Window('Batcher v '+ version, layout6)
event, stuff = window6.read()
if event == 'Safe and Exit':
    saveImage()
    window6.close()
    exit()
if event == 'Exit':
    window6.close()
    exit()