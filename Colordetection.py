import cv2
import numpy as np
def empty(a):
    pass
def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

path="Resources/car3.jpg"
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",640,240)
cv2.createTrackbar("Huemin","Trackbars",0,179,empty)
cv2.createTrackbar("Huemax","Trackbars",83,179,empty)
cv2.createTrackbar("Satmin","Trackbars",0,255,empty)
cv2.createTrackbar("Satmax","Trackbars",255,255,empty)
cv2.createTrackbar("Valmin","Trackbars",162,255,empty)
cv2.createTrackbar("Valmax","Trackbars",255,255,empty)
while True:
    img=cv2.imread(path)
    imgResize=cv2.resize(img,(640,480))
    imgHsv=cv2.cvtColor(imgResize,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Huemin", "Trackbars")
    h_max = cv2.getTrackbarPos("Huemax", "Trackbars")
    s_min = cv2.getTrackbarPos("Satmin", "Trackbars")
    s_max = cv2.getTrackbarPos("Satmax", "Trackbars")
    v_min = cv2.getTrackbarPos("Valmin", "Trackbars")
    v_max = cv2.getTrackbarPos("Valmax", "Trackbars")
    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv2.inRange(imgHsv,lower,upper)
    imgF=cv2.bitwise_and(imgResize,imgResize,mask=mask)
    new1=stackImages(0.5,([imgResize,imgHsv],[mask,imgF]))
 #   cv2.imshow("Org",imgResize)
  #  cv2.imshow("HSV",imgHsv)
  #  cv2.imshow("Mask",mask)
    cv2.imshow("Final",new1)
    cv2.waitKey(1)