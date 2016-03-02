import numpy as np
import cv2
import base64
import copy

gray = 0
s1,s2 = np.array([255,255,255]),np.array([0,0,0])    
cap = cv2.VideoCapture(0)
nframes=0
#fourcc = cv2.cv.CV_FOURCC(*'XVID')
r=75
ix,iy= -1,-1
jx,jy = -1,-1
draw,start = 0,0
ret, frame= cap.read()
def nothing(x):
    pass

def mouse_callback(event,x,y,flags,param ):
    global frame,gray
    global s1,s2,r,draw,start
    global ix,iy,jx,jy
    
    if event == cv2.EVENT_LBUTTONDOWN:
        ix,iy = x,y
        draw = 1

    elif event == cv2.EVENT_MOUSEMOVE:
        if draw == 1:
            fr = copy.copy(frame)
            r = cv2.rectangle(fr,(ix,iy),(x,y),(0,0,255),1)
            jx=x
            jy=y
            cv2.imshow('frame',fr)
            
            #print x,y
        #s = gray[y,x].astype(np.int16)
        #s = np.array([0,255,0])
            
            
    elif event == cv2.EVENT_LBUTTONUP:
        draw = 0
        start = 1
        s1,s2 = np.array([255,255,255]),np.array([0,0,0])    

        f = np.array([0,0])
        f = gray[iy:jy, ix:jx]
        for x in range(0, f.shape[0]):
            for y in range(0, f.shape[1]):
                s = f[x,y]
                s1[0] = min(s1[0],s[0])
                s1[1] = min(s1[1],s[1])
                s1[2] = min(s1[2],s[2])

                s2[0] = max(s2[0],s[0])
                s2[1] = max(s2[1],s[1])
                s2[2] = max(s2[2],s[2])
                #print s1,s2
        cv2.namedWindow('frame1')  
        cv2.imshow('frame1',f)
        print s1,s2
        

#cv2.namedWindow('range')        
cv2.namedWindow('frame')        
cv2.setMouseCallback('frame',mouse_callback)
cv2.createTrackbar('Range','range',75,100,nothing)
kernel = np.ones((5,5),np.uint8)

while(True):

    if draw == 0:
        ret, frame= cap.read()
        thresh = frame
        #cv2.imshow('frame',frame)
        gray = cv2.medianBlur(frame,5)
        #cv2.imshow('filtered',gray)
        #r = cv2.getTrackbarPos('Range','range')
        cv2.cvtColor(gray,cv2.COLOR_BGR2HSV,gray)
        #s1 = s - r
        #s2 = s + r

        #for i in range(0,len(s1)):
         #   s1[i] = max(0,s1[i])
                
        #for i in range(0,len(s2)):
         #   s2[i] = min(255,s2[i])

        thresh = cv2.inRange(gray,s1,s2)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        contours, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        max1 = 0
        x=0
        y=0
        w=0
        h=0
        if start == 1:
            for cnt in contours:
                if max1 < cv2.contourArea(cnt):
                    max1 = cv2.contourArea(cnt)
                    x,y,w,h = cv2.boundingRect(cnt)

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)        
        cv2.imshow('frame',frame)
        #cv2.imshow('Thresh',thresh)
        #cv2.imshow('Morphed',opening)
        nframes = (nframes+1)%50
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# When everything done, release the capture

cap.release()
cv2.destroyAllWindows()


