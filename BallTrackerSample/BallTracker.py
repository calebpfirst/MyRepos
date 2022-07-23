# import the necessary packages
import numpy as np
import cv2
  
  
# Capturing video through webcam 
webcam = cv2.VideoCapture(0) 
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('output.avi',fourcc, 30.0,(int(webcam.get(3)),int(webcam.get(4))))

# Start a while loop 
while(1): 
      
    # Reading the video from the 
    # webcam in image frames 
    _, imageFrame = webcam.read() 
  
    # Convert the imageFrame in  
    # BGR(RGB color space) to  
    # HSV(hue-saturation-value) 
    # color space 
    blurr = cv2.GaussianBlur(imageFrame, (11, 11), 0)
    hsvFrame = cv2.cvtColor(blurr, cv2.COLOR_BGR2HSV) 

    # Set range for red color and  
    # define mask 
    lower = np.array([21, 86, 6], np.uint8) 
    upper = np.array([64, 255, 255], np.uint8) 
    post_mask = cv2.inRange(hsvFrame, lower, upper)
    eroded = cv2.erode(post_mask, None, 2)
    dilated = cv2.dilate(eroded, None, 2)
    # Creating contour to track red color 
    contours, hierarchy = cv2.findContours(dilated, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
      
    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        if(area > 250): 
            x, y, w, h = cv2.boundingRect(contour) 
            imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                       (x + w, y + h),  
                                       (0, 0, 255), 2) 
              
            cv2.putText(imageFrame, "Dory's Ball", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                        (0, 0, 255))     

    out.write(imageFrame)
    # Program Termination 
    cv2.imshow("Where is the ball?!", imageFrame) 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        cap.release() 
        cv2.destroyAllWindows() 
        break
