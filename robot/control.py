from time import sleep
from gpiozero import Robot
import cv2
import numpy as np
import math
from camera.Camera import Camera
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

x = 0.1

a = 0.4
b = 0.9
c = 0.8
d = 0.7
e = 0.6
f = 0.5
g = 0.4

testmode = 2 #to enable added features such as view and save on file

key = ''
r = Robot(left=(23, 24), right=(11,9))

def ishuman(frame):
    faces = faceCascade.detectMultiScale(frame)
    for (x, y, w, h) in faces:
      cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
      cv2.putText(frame,"Human detected" , ( x+5, y+5 ),cv2.FONT_HERSHEY_TRIPLEX, 0.6,(244,134,66),2)
      print("Human presence")
      stop()
      sleep(3)


def forward(): #... add onto the left 
    m1_speed = a #mr
    m2_speed = a #ml
    r.value = (m1_speed, m2_speed)

def backward(): 
    r.reverse()

def right():
    r.right(speed=a)
    print ("Going right")
    sleep(0.6) #0.5
    forward()

 
def left(): 
    r.left(speed=a)
    print ("Going left")
    sleep(0.6) #0.5
    forward()

def stop():
    m1_speed = 0.0
    m2_speed = 0.0
    r.value = (m1_speed, m2_speed)
    print('stop')
   
def calc_dist(p1,p2):

    x1 = p1[0]

    y1 = p1[1]

    x2 = p2[0]

    y2 = p2[1]
    
    dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)

    return dist


def getChunks(l, n):

    """Yield successive n-sized chunks from l."""

    a = []

    for i in range(0, len(l), n):   

        a.append(l[i:i + n])

    return a


camera = Camera()
camera.start_capture()


StepSize = 20
currentFrame = 0




while True:

    frame = camera.current_frame.read()
    ishuman(frame)
    sleep(0.05)

    
    img = frame.copy()

    blur = cv2.bilateralFilter(img,9,40,40)

    edges = cv2.Canny(blur,50,100)

    img_h = img.shape[0] - 1

    img_w = img.shape[1] - 1

    EdgeArray = []

    for j in range(0,img_w,StepSize):

        pixel = (j,0)

        for i in range(img_h-5,0,-1):

            if edges.item(i,j) == 255:

                pixel = (j,i)

                break

        EdgeArray.append(pixel)


    for x in range(len(EdgeArray)-1):

        cv2.line(img, EdgeArray[x], EdgeArray[x+1], (0,255,0), 1)



    for x in range(len(EdgeArray)):

        cv2.line(img, (x*StepSize, img_h), EdgeArray[x],(0,255,0),1)


    chunks = getChunks(EdgeArray,int(len(EdgeArray)/3)) # 5

    max_dist = 0

    c = []

    for i in range(len(chunks)-1):        

        x_vals = []

        y_vals = []

        for (x,y) in chunks[i]:

            x_vals.append(x)

            y_vals.append(y)


        avg_x = int(np.average(x_vals))

        avg_y = int(np.average(y_vals))

        c.append([avg_y,avg_x])

        cv2.line(frame,(160,240),(avg_x,avg_y),(255,0,0),2)  

    #print(c)

    forwardEdge = c[1]
    #print(forwardEdge)

    cv2.line(frame,(160,240),(forwardEdge[1],forwardEdge[0]),(0,255,0),3)   
     
    y = (min(c))
    #print(y)
    
    if forwardEdge[0] > 100: #200 # >230 works better 

       if y[1] < 140:
          forward()
          sleep(0.004)
          #pwm.start(0)
          #pwm1.start(40)
          direction = "forward "
          print(direction)
        

       else:
          forward()
          sleep(0.004)
          direction = "go "
          print(direction)
          


    elif  100 < forwardEdge[0] < 150:
       forward()
       sleep(0.004)
       direction = "stop "
       print(direction)
       
    
    else:
       stop()
       sleep(0.004)
       direction = "stop"
       print(direction)
    #   backward()
      # sleep(0.009)
       #direction = "reverse"
       #print(direction)
       
   

    if testmode == 2:

       cv2.imshow("frame",frame)

       cv2.imshow("Canny",edges)

       cv2.imshow("result",img)


    k = cv2.waitKey(5) & 0xFF  ##change to 5

    if k == 27:

        break


cv2.destroyAllWindows
camera.release()

