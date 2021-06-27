# import numpy as np 
# import cv2 
# import glob
# import matplotlib.pyplot as plt 

# def setCalibValues(img_size):
#   a4_size = (210,297)
#   calib_x_mm =  max(a4_size) / max(img_size)
#   calib_y_mm =  min(a4_size) / min(img_size)
#   return (calib_x_mm , calib_y_mm)

# def perspectiveTransform(img,src,offset_leftright,offset_topbottom,offset_right):
#   img_size =  (img.shape[1], img.shape[0])
#   # print("Image Size ",img_size)

#   dst = np.float32([[offset_leftright, img_size[1]-offset_topbottom] , [offset_leftright, offset_topbottom],\
#                                [img_size[0]+offset_right, offset_topbottom],\
#                                [img_size[0]+offset_right, img_size[1]-offset_topbottom]])        
#   M = cv2.getPerspectiveTransform(src, dst)
#   wraped = cv2.warpPerspective(img, M, img_size , flags=cv2.INTER_LINEAR)
#   return wraped

# def getROI(raw_image):
#   (low_H, low_L, low_S) = (0,150,5)
#   (high_H, high_L, high_S) = (250,250,55)
#   hls = cv2.cvtColor(raw_image, cv2.COLOR_RGB2HLS)
#   frame_threshold = cv2.inRange(hls, (low_H, low_L, low_S), (high_H, high_L, high_S))
#   cnts = cv2.findContours(frame_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#   cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#   contour_max = max(cnts, key = cv2.contourArea)
#   rect = cv2.minAreaRect(contour_max)
#   poly = cv2.boxPoints(rect)
#   box = cv2.boxPoints(rect)
#   box = np.int0(box)
#   return np.float32(box)
#   # cv2.drawContours(raw_image,[box],0,(255,0,255),2) 


#   # print("LEFT BOTTOM" , contour_max[contour_max[:,:,0].argmin()])
#   # print("RIGHT BOTTOM" , contour_max[contour_max[:,:,0].argmax()])
#   # print("RIGHT TOP" , tuple(contour_max[contour_max[:,:,1].argmin()][0]))
#   # print("LEFT TOP" , tuple(contour_max[contour_max[:,:,1].argmax()][0]))
# # rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
#   # x,y,w,h = cv.boundingRect(cnt)
#   # approx = cv2.approxPolyDP(contour_max, 0.009 * cv2.arcLength(contour_max, True), True) 
#   # print("Approz " , approx)
#   # n = approx.ravel()  
#   # print("Approx points ",n)
#   # cv2.drawContours(raw_image, [contour_max], -1, (36,255,12), -1)
  
#   # return raw_image

# def getRectangleAdaptiveThreshold(raw_image):
#   gray = cv2.cvtColor(raw_image,cv2.COLOR_BGR2GRAY)
#   thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,13)
#   cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#   cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#   # print(len(cnts))
#   cnts = filter(lambda x:cv2.contourArea(x) > 1200 and cv2.contourArea(x) < 5000, cnts)
#   list_of_heights = []
#   list_of_width = []
#   for c in cnts:
#     # x,y,w,h = cv2.boundingRect(c)
#     # list_of_heights.append(h)
#     # cv2.drawContours(raw_image, [c], -1, (36,255,12), -1)
#     # cv2.rectangle(raw_image, (x, y), (x + w, y + h), (36,255,12), 3)

#     # rect = cv2.minAreaRect(c)
#     # (x, y), (width, height), angle = rect
#     # list_of_heights.append(height)
#     # list_of_width.append(width)
#     # box = cv2.boxPoints(rect)
#     # box = np.int0(box)
#     # cv2.drawContours(raw_image,[box],0,(0,0,255),2)

#     ellipse = cv2.fitEllipse(c)
#     (x,y),(MA,ma),angle = ellipse
#     cv2.ellipse(raw_image,ellipse,(0,255,0),2)
#     list_of_heights.append(ma)
#     # list_of_width.append(MA)

#   # list_of_heights_numpy = np.array(list_of_heights)
#   # list_of_width_numpy = np.array(list_of_width)
#   # print("List of heights " , list_of_heights)
#   # print("List of widths " , list_of_width)
#   # print("Any width > Height ? \n" , list_of_width_numpy[np.where(list_of_width_numpy > list_of_heights_numpy)[0]])
#   return raw_image ,list_of_heights
  

# def getRectangleStructure(raw_image):
#   result = raw_image.copy()
#   kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
#   gray = cv2.cvtColor(raw_image,cv2.COLOR_BGR2GRAY)
#   thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)
#   opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
#   cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#   # print("Contours " , cnts)
#   cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#   list_of_heights = []
#   for c in cnts:
#     x,y,w,h = cv2.boundingRect(c)
#     # print('Width ',w,' Height',h)
#     list_of_heights.append(h)
#     # cv2.drawContours(result, [c], -1, (36,255,12), -1)
#     cv2.rectangle(result, (x, y), (x + w, y + h), (36,255,12), 3)
#   return result , list_of_heights



# def process(upload_image):
   
#   offset_leftright = 0
#   offset_topbottom = 10
#   offset_right = 370

#   img = cv2.imread(upload_image)
#   src = getROI(img)
#   pt_image = perspectiveTransform(img,src,offset_leftright,offset_topbottom,offset_right)
#   calib_params = setCalibValues((pt_image.shape[1], pt_image.shape[0]))
#   r_image ,list_of_heights = getRectangleAdaptiveThreshold(pt_image)
#   count_of_objs = len(list_of_heights)
#   mean_height = np.mean(list_of_heights)
#   std_dev = np.std(list_of_heights)
#   min_height = np.min(list_of_heights)
#   max_height = np.max(list_of_heights)
 

#   return r_image , count_of_objs , mean_height , std_dev , min_height , max_height



# if __name__ == "__main__": 
  
#   images = glob.glob('/home/sreeja/Jemshid_projects/image_process_api/media/a.jpeg')
#   print(images)
#   r_image , count_of_objs , mean_height , std_dev , min_height , max_height= process(images[0])
#   print("Count :" , count_of_objs, " | Mean Height :" , mean_height ,' | Std Dev: ' , std_dev , " \n" )
#   print("Min Height : " , min_height, " | Max Height : " , max_height , " \n" )
#   # print("Calib Params ", calib_params)

#   plt.imshow(r_image)
#   plt.show()