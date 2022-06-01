# Frank Wang / FWPhys Creation. June 2022.

import numpy as np
from PIL import Image, ImageCms
import PIL
import matplotlib.pyplot as plt

# Define the Most Readily Available Brick Colours

# Source: Lego Moulding Palette 2016

BrickColors = {}

#### Greyscale
BrickColors["Black"] = np.zeros(3) # 26
BrickColors["White"] = np.ones(3) # 1
BrickColors["Grey"] = np.array([150,151,149])/255 # 194

#### Blue
BrickColors["Bright Blue"] = np.array([14,96,172])/255 # 23
BrickColors["Dark Azur"] = np.array([20,151,210])/255 # 321

#### Green
BrickColors["Yellowish Green"] = np.array([197,221,143])/255 # 326
BrickColors["Bright Green"] = np.array([19,165,71])/255 # 37

#### Yellow
BrickColors["Bright Yellow"] = np.array([254,200,41])/255 # 24

#### Orange
BrickColors["Bright Orange"] = np.array([242,116,43])/255 # 106
BrickColors["Nougat"] = np.array([216,129,89])/255 # 18

#### Red
BrickColors["Bright Red"]  = np.array([214,32,39])/255 # 21
BrickColors["Reddish Brown"] = np.array([93,42,23])/255 # 192


#### Purple
BrickColors["Bright Purple"] = np.array([228,85,152])/255 # 221
BrickColors["Med Lavender"] = np.array([139,105,169])/255 # 324


def ShowColors():

    for key in BrickColors.keys():

        plt.figure(facecolor=BrickColors[key], figsize=(2, 2))
        plt.axis('off')
        plt.title(key,
                  color=(np.round(np.sum(1 - BrickColors[key])/3, decimals=0)) *
                  np.ones(3))  # What sourcery did I write!?
        plt.show()
        
        
def ProjectToDCS(Photo,BoardSize = (48,48), OverSample = 4,BoardColor = 'Grey'):
    
    GlobalCount = {}
    for key in BrickColors.keys():
        GlobalCount[key] = 0
    
    BoardX, BoardY = BoardSize

    PPhoto = 200 * np.ones([BoardX,BoardY,3], dtype='uint8')
            
    RPhoto = Photo.resize((int(OverSample*BoardX),int(OverSample*BoardY)), resample = 3)
    
    RPhoto.show()
    
    print(RPhoto.size)
    
    for ii in range(BoardX):
        LocX = OverSample * (ii)
        
        for ij in range(BoardY):
            LocY = OverSample * (ij)
            
            LocalPixels = np.array(RPhoto)[LocX:LocX+OverSample,LocY:LocY+OverSample,:]
            
            LocalPixel = np.average(LocalPixels,axis = (0,1))
                
            # Project to Brick Color Space
            
            Compare = {}
            
            for key in BrickColors.keys():

                Color = BrickColors[key]*255
                Compare[key] = np.sqrt(np.sum((LocalPixel-Color)**2))

            MinKey = min(Compare, key=Compare.get)
            PPhoto[ii,ij] = 255*BrickColors[MinKey]
            
            GlobalCount[MinKey] += 1
            
        
    
    
    IPhoto = Image.fromarray(PPhoto, mode = 'RGB')
    
    print(IPhoto.size)
    
    IPhoto.show()
    return IPhoto, GlobalCount