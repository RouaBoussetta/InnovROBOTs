import cv2
from camera.Camera import Camera
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
camera = Camera()
camera.start_capture()
# grab the reference to the webcam
# keep looping
while True:
 # grab the current frame
 frame = camera.current_frame.read()
  
 # if we are viewing a video and we did not grab a frame,
 # then we have reached the end of the video
 if frame is None:
  break
  
 faces = faceCascade.detectMultiScale(frame)

 for (x, y, w, h) in faces:
  cv2.rectangle(frame, (x, y), (x+w, y+h), (255,0,0), 2)
  cv2.putText(frame,"Human detected" , ( x, y ),cv2.FONT_HERSHEY_TRIPLEX, 0.1,(244,134,66),2)

 # show the frame to our screen
 cv2.imshow("Video", frame)
 key = cv2.waitKey(1) & 0xFF

 # if the 'q' key is pressed, stop the loop
 if key == ord("q"):
  break
 
# close all windows
cv2.destroyAllWindows()
