import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import keyboard
import tkinter as tk
from tkinter import filedialog
import os

def main(mainimg):
    global ix, iy, drawing , img, crop
    aimg = cv.imread(mainimg)
    img = aimg.copy()

    ix = -1
    iy = -1
    drawing = False
    def draw_reactangle_with_drag(event, x, y, flags, param):
        global ix, iy, drawing , img
        global posa, posb
        if event == cv.EVENT_LBUTTONDOWN:       #mouse button down initiates the illustration of rectangle
            drawing = True
            ix = x
            iy = y

        elif event == cv.EVENT_MOUSEMOVE:
            if drawing == True:
                img2 = aimg.copy()              #mouse move keeps refreshing img and draws new rectangles at each move
                cv.rectangle(img2, pt1=(ix,iy), pt2=(x, y),color=(0,0,255),thickness=1)    
                img = img2.copy()

        elif event == cv.EVENT_LBUTTONUP:
            drawing = False
            img2 = aimg.copy()
            cv.rectangle(img2, pt1=(ix,iy), pt2=(x, y),color=(0,0,255),thickness=1)
            img = img2.copy()
            posa = [x , y]              #gets the final coordinations of rectangle(bottom right)
            posb = [ix , iy]            #gets the initial coordinations of rectangle(top left)

      
    cv.namedWindow("Title of Popup Window",cv.WINDOW_NORMAL)
    cv.resizeWindow("Title of Popup Window", 500,500)
    cv.setMouseCallback("Title of Popup Window", draw_reactangle_with_drag)
    while True:
        cv.imshow("Title of Popup Window", img)
        n,m = img.shape[:2]
        if keyboard.is_pressed("esc"):
            break
        elif cv.waitKey(10) == ord('u'):  # Zoom in, make image double size
            if img.shape[0]<11 or img.shape[1]<11:
                
                print("a")
            elif ((posa[1]-posb[1]) ,(posa[0]-posb[0])) ==img.shape[:2]:
                img = aimg = aimg[1:img.shape[0]-1,1:img.shape[1]-1]
                
                posa[0]=posa[0]-1
                posa[1]=posa[1]-1
                posb[0]=posb[0]+1
                posb[1]=posb[1]+1
            else:
                img = aimg = aimg[posb[1]:posa[1],posb[0]:posa[0]]
        elif keyboard.is_pressed("i"):  # Zoom down, make image half the size
            img = aimg = cv.imread(mainimg)
        elif keyboard.is_pressed('enter'):
     
            crop = img[posb[1]:posa[1],posb[0]:posa[0]]     #crops image at final rectangle
      
##            cv.imshow("cropped",crop)
##            cv.waitKey(0)
##            cv.destroyAllWindows()
            
            break
    cv.destroyAllWindows()
    return crop
def measure(temp,base):
    template = temp
    img = cv.imread(base)
    img2 = img.copy()

    #template = cv.imread(template,0)
    h, w,_ = template.shape
    # All the 6 methods for comparison in a list
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    methods =['cv.TM_SQDIFF']

    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img,top_left, bottom_right, 255, 1)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        ## plt.show()

        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,cv.flip(template,1),method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left2 = min_loc
        else:
            top_left2 = max_loc

        bottom_right2 = (top_left2[0] + w, top_left2[1] + h)
        cv.rectangle(img,top_left2, bottom_right2, 255, 1)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result FLIPPED'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point FLIPPED'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        ## plt.show()

        if top_left[0]>top_left2[0]:
            print(meth, bottom_right2[0] - top_left[0])
        else:
            print(meth, bottom_right[0] - top_left2[0])

def measurev(temp,base):
    template = temp
    img = cv.imread(base)
    img2 = img.copy()


    h, w,_ = template.shape
    # All the 6 methods for comparison in a list
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    methods =['cv.TM_SQDIFF']

    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img,top_left, bottom_right, 255, 1)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        #plt.show()

        print(top_left[1])
            
base = filedialog.askopenfilename()
template=main(base)
templatev=main(base)


list = os.listdir( os.path.dirname(base) )
for size in list:
    dirsize=os.path.dirname(base)+'/'+size
    print(size)
    measure(template,dirsize)
    measurev(templatev,dirsize)

