#!/usr/bin/env python
#Version 0.1
from tkinter.constants import N
from PySimpleGUI.PySimpleGUI import Image
import cv2
import os
import PySimpleGUI as sg
import time
import numpy as np
version=str(0.1)
rgb=0 ,bgr=0, asr=0, nwa=0, nw=0, nh=0
print ("Version ", version)
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
layout6 = [[sg.Text('All files were successfully safed. Thank you for the job!')],
[sg.Quit()]]
font=cv2.FONT_HERSHEY_SIMPLEX
rimg=np.zeros((200,640,1), np.uint8)
rimg[0:200,0:640]=[255]
cv2.putText(rimg,'Ready - press q to quit',(175,94),font,.75,(0,0,0),1)
window = sg.Window('Batcher - Computer Vision Image Optimization v '+ version, layout)
event, values = window.read()
window.close()
path, path2, ors, asr, gs  = values[0], values[1], values[2], values[3], values[4]     
if ors == True:
    pass
if ors == 0 and asr != True:
    window2 = sg.Window('Batcher - Computer Vision Image Optimization v '+ version, layout2)
    event, sizes = window2.read()
    window2.close()
    nw, nh, = sizes[0], sizes[1]
    nw=int(nw)
    nh=int(nh)
if asr == True:
    window3 = sg.Window('Batcher - Computer Vision Image Optimization v '+ version, layout3)
    event, sizesa = window3.read()
    window3.close()
    nwa = sizesa[0]
    nwa=int(nwa)
if gs != True:
    window4 = sg.Window('Batcher - Computer Vision Image Optimization v '+ version, layout4)
    event, colors = window4.read()
    window4.close()
    rgb, bgr = colors[0], colors[1]
for root, dirs, files in os.walk(path):
    for file in files:
        ImagePath=os.path.join(root,file)
        saveImagePath=path2 + '/' + file
        print('Loading ', ImagePath)
        img=cv2.imread(ImagePath)
        height,width,channels = img.shape
        if rgb == True:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            print('Converted ',ImagePath , ' to RGB')
        if bgr == True:
            img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            print('Converted ',ImagePath , ' to BGR')
        if gs == True:
            img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            print('Converted ',ImagePath , ' to Grayscale')
        if asr  == True:
            if height > width:
                aspectRatio=width/height
                nw=nwa*aspectRatio
                nw=int(nw)
                img=cv2.resize(img,(nw,nwa))
                print('Resized ',ImagePath , ' to ', nw, 'x', nwa, 'px')
            if width >= height:
                aspectRatio=height/width
                nh=nwa*aspectRatio
                nh=int(nh)
                img=cv2.resize(img,(nwa,nh))
                print('Resized ',ImagePath, ' to ', nwa, 'x', nh, 'px')
            cv2.imshow(file,img)
            cv2.imwrite(saveImagePath, img)
            print('Saved optimized image ',ImagePath , ' to ', saveImagePath) 
        else: 
            if ors!= True:   
                img=cv2.resize(img,(nw,nh))
            cv2.imshow(file,img)
            cv2.imwrite(saveImagePath, img)
            print('Saved optimized image ',ImagePath , ' to ', saveImagePath)
cv2.imshow('Ready',rimg)
print('All Done!')
cv2.imshow('Ready',rimg)
if cv2.waitKey(0)==ord('q'):
    window6 = sg.Window('Batcher - Computer Vision Image Optimization v '+ version, layout6)
    event, stuff = window6.read()
    window6.close()
    exit()