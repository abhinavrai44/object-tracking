import numpy as np
import cv2
import cv2.cv as cv
from common import clock, draw_str

flag = 0

def mo(event,x,y,flags,param):
    global sx 
    global sy 
    global ex 
    global ey 
    global flag     
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'Down Mouse Position: '+str(x)+', '+str(y)
        sx = x
        sy = y
    elif event == cv2.EVENT_LBUTTONUP:
        flag = 1
        print 'Up Mouse Position: '+str(x)+', '+str(y)
        ex = x
        ey = y

    

cv2.namedWindow('image')
cap = cv2.VideoCapture(0)
_, frame  = cap.read()
cv2.imshow('image',frame)
cv2.setMouseCallback('image',mo)
while(1):
    _, frame  = cap.read()
    cv2.imshow('image',frame)
    #cv2.setMouseCallback('image',mo)
    if flag == 1:
        break
    ch = 0xFF & cv2.waitKey(5)
    if ch == 27:
        break
if(ex > sx):
    c = sx
    w = ex - sx
else:
    c = ex
    w = sx - ex
if(ey > sy):
    r = sy
    h = ey - sy
else:
    r = ey
    h = sy - ey

track_window = (c,r,w,h)

cx = 320
cy = 240

roi = frame[r:r+h, c:c+w]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret ,frame = cap.read()
    
    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
        
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        #pts = cv2.boxPoints(ret)
        #pts = np.int0(pts)
        #img2 = cv2.polylines(frame,[pts],True, 255,2)
        x,y,w,h = track_window
        ox = x + (w / 2) 
        oy = y + (h / 2)

        img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)

        if (ox > cx):
            cv2.putText(frame,"Right", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif (ox < cx):
            cv2.putText(frame,"Left", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        if (oy > cy):
            cv2.putText(frame,"Down", (50,80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        elif (oy < cy):
            cv2.putText(frame,"Up", (50,80), cv2.FONT_HERSHEY_SIMPLEX, 2, 2) 
        
        cv2.imshow('Video',frame)
        

        if 0xFF & cv2.waitKey(1) == 27:
            break
        
cv2.destroyAllWindows()
cap.release()