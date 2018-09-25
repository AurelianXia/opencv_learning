import cv2
import numpy as np
#load image
srcImg = cv2.imread('test.jpg')
WindowName1 = 'src'
cv2.imshow(WindowName1,srcImg)
print(srcImg.shape[:2])
#鼠标操作
rect = [200,50,50,50]
def draw_rect(event,x,y,flags,param):
	global ix,iy,drawing,mode
	if event==cv2.EVENT_LBUTTONDOWN:
		drawing=True
		ix = x
		iy = y
	elif event==cv2.EVENT_MOUSEMOVE and flags==cv2.EVENT_FLAG_LBUTTON:
		if drawing==True:
			mode = 1
	elif event==cv2.EVENT_LBUTTONUP:
		drawing==False
		tmpImg = srcImg.copy()
		if ix > x:
			ix, x = x, ix
		if iy > y:
			iy, y = y, iy
		rect=(ix, iy, x - ix, y - iy)
		print('present Rect: ', rect)
		cv2.rectangle(tmpImg,(ix,iy),(x,y),(0,0,255),0)
		cv2.imshow(WindowName1,tmpImg)
		grabCutImg(srcImg, rect)
cv2.setMouseCallback(WindowName1, draw_rect)

#processing img
def grabCutImg(srcImg, rect):
        mask = np.zeros(srcImg.shape[:2], np.uint8)   #与srcImg同大小的掩膜
        bgdModel = np.zeros((1, 65), np.float64)   #以0填充的背景模型
        fgdModel = np.zeros((1, 65), np.float64)    #以0填充的前景模型

           #初始矩形
        mask, bgdModel, fgdModel = cv2.grabCut(srcImg, mask, rect, bgdModel, fgdModel, 3, cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')   #mask中0和2的值转为0， 1和3的值转为1
        dstImg = srcImg * mask2[:, :, np.newaxis]
        cv2.imshow('grabcut', dstImg)
        cv2.waitKey(0)
